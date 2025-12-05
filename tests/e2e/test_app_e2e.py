import time
import uuid
from typing import Callable

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.e2e.utils.api_client import ApiClient

WAIT_TIMEOUT = 30


def login_through_ui(
    driver: Chrome, base_url: str, username: str, password: str
) -> None:
    driver.get(f"{base_url}/login")
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    username_input = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
    password_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input#password"))
    )
    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)
    submit_button.click()

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Sign out')]"))
    )


def test_listings_route_requires_login(driver: Chrome, frontend_base_url: str) -> None:
    driver.get(f"{frontend_base_url}/listings")
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    wait.until(lambda d: "/login" in d.current_url)
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    assert "/login" in driver.current_url


def test_user_can_login(
    driver: Chrome, frontend_base_url: str, register_user: dict
) -> None:
    login_through_ui(
        driver,
        frontend_base_url,
        register_user["username"],
        register_user["password"],
    )
    assert "/login" not in driver.current_url
    token_in_storage = driver.execute_script(
        "return window.localStorage.getItem('token');"
    )
    assert token_in_storage, "Token should be saved in localStorage after login"


def test_user_can_view_listing_details(
    driver: Chrome,
    frontend_base_url: str,
    register_user: dict,
    listing_factory,
) -> None:
    listing = listing_factory()
    login_through_ui(
        driver,
        frontend_base_url,
        register_user["username"],
        register_user["password"],
    )
    driver.get(f"{frontend_base_url}/listings/{listing['id']}")
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    title_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='editable-input-title']")
        )
    )
    assert title_input.get_attribute("value") == listing["title"]


def test_user_can_edit_listing_field(
    driver: Chrome,
    frontend_base_url: str,
    register_user: dict,
    listing_factory: Callable[..., dict],
    api_client: ApiClient,
    api_token: str,
) -> None:
    listing = listing_factory(price=275000)
    base_price = int(listing["price"])
    updated_price = str(base_price + 5000)

    login_through_ui(
        driver,
        frontend_base_url,
        register_user["username"],
        register_user["password"],
    )
    driver.get(f"{frontend_base_url}/listings/{listing['id']}")
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    price_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='editable-input-price']")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", price_input
    )
    price_input.click()
    wait.until(lambda _: price_input.get_attribute("readonly") is None)
    price_input.send_keys(Keys.CONTROL, "a")
    price_input.send_keys(Keys.DELETE)
    price_input.send_keys(updated_price)

    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='editable-save-price']")
        )
    )
    driver.execute_script(
        "arguments[0].dispatchEvent(new PointerEvent('pointerdown', {bubbles: true}));",
        save_button,
    )

    wait.until(lambda _: price_input.get_attribute("value") == updated_price)

    _wait_for_listing_update(
        api_client, api_token, listing["id"], "price", int(updated_price)
    )


def test_user_can_add_note(
    driver: Chrome,
    frontend_base_url: str,
    register_user: dict,
    listing_factory: Callable[..., dict],
    api_client: ApiClient,
    api_token: str,
) -> None:
    listing = listing_factory()
    note_text = f"{uuid.uuid4().hex[:8]}"

    login_through_ui(
        driver,
        frontend_base_url,
        register_user["username"],
        register_user["password"],
    )

    driver.get(f"{frontend_base_url}/listings/{listing['id']}")
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    add_menu_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='add-note-menu-button']")
        )
    )
    add_menu_button.click()

    add_action = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='add-note-action']"))
    )
    add_action.click()

    textarea = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='note-textarea']")
        )
    )
    textarea.clear()
    textarea.send_keys(note_text)

    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='note-save-button']")
        )
    )
    save_button.click()

    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='note-textarea']")
        )
    )

    driver.get(f"{frontend_base_url}/listings/{listing['id']}/notes")
    notes_wait = WebDriverWait(driver, WAIT_TIMEOUT)
    note_element = notes_wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                f"//p[contains(text(), '{note_text}')]",
            )
        )
    )
    assert note_text in note_element.text

    created_note_id = _wait_for_note_to_exist(
        api_client, api_token, listing["id"], note_text
    )
    api_client.delete_note(api_token, created_note_id)


def _wait_for_listing_update(
    api_client: ApiClient,
    token: str,
    listing_id: str,
    field: str,
    expected_value: int,
    timeout: int = 20,
) -> None:
    end_time = time.time() + timeout
    while time.time() < end_time:
        listing = api_client.get_listing(token, listing_id)
        if listing.get(field) == expected_value:
            return
        time.sleep(1)
    raise AssertionError(
        f"Listing {listing_id} field '{field}' did not update to {expected_value}"
    )


def _wait_for_note_to_exist(
    api_client: ApiClient,
    token: str,
    listing_id: str,
    note_text: str,
    timeout: int = 20,
) -> str:
    end_time = time.time() + timeout
    while time.time() < end_time:
        notes = api_client.get_notes(token, listing_id)
        for note in notes:
            if note.get("note") == note_text:
                return note["id"]
        time.sleep(1)
    raise AssertionError(
        f"Note with text '{note_text}' was not persisted for listing {listing_id}"
    )
