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
    listing_factory,
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


def test_user_can_add_listing_through_navbar(
    driver: Chrome,
    frontend_base_url: str,
    register_user: dict,
    api_client: ApiClient,
    api_token: str,
) -> None:
    unique_title = f"E2E Listing {uuid.uuid4().hex[:6]}"

    login_through_ui(
        driver,
        frontend_base_url,
        register_user["username"],
        register_user["password"],
    )

    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    add_menu_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='add-listing-menu-button']")
        )
    )
    add_menu_button.click()

    add_action = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='add-listing-action']")
        )
    )
    add_action.click()

    _fill_text_input(wait, "add-listing-title", unique_title)
    _fill_text_input(wait, "add-listing-location", "Test City")
    _fill_text_input(wait, "add-listing-street", "123 Ave")
    _fill_text_input(wait, "add-listing-price", "450000")
    _fill_text_input(wait, "add-listing-area", "150")
    _fill_text_input(wait, "add-listing-floor", "2")
    _fill_text_input(wait, "add-listing-num-of-floors", "3")
    _fill_text_input(wait, "add-listing-description", "Test listing")

    _set_build_year(wait, "add-listing-build-year", "2015")
    _select_dropdown_option(driver, wait, "add-listing-property-type", "House")
    _select_dropdown_option(driver, wait, "add-listing-transaction-type", "Sell")

    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='add-listing-save']")
        )
    )
    save_button.click()

    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='add-listing-save']")
        )
    )

    created_listing = _wait_for_listing_by_title(
        api_client, api_token, unique_title, timeout=40
    )

    try:
        driver.get(f"{frontend_base_url}/listings/{created_listing['id']}")
        detail_wait = WebDriverWait(driver, WAIT_TIMEOUT)
        title_input = detail_wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='editable-input-title']")
            )
        )
        assert title_input.get_attribute("value") == unique_title, (
            "Listing title should match the newly created listing"
        )
    finally:
        api_client.delete_listing(api_token, created_listing["id"])


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


def _wait_for_listing_by_title(
    api_client: ApiClient,
    token: str,
    title: str,
    timeout: int = 30,
):
    filter_query = f"title_eq={title}"
    end_time = time.time() + timeout
    while time.time() < end_time:
        listings = api_client.list_listings(token, filter=filter_query)
        for listing in listings:
            if listing.get("title") == title:
                return listing
        time.sleep(1)
    raise AssertionError(f"Listing with title '{title}' was not created in time")


def _fill_text_input(wait: WebDriverWait, test_id: str, value: str) -> None:
    field = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='{test_id}']"))
    )
    field.clear()
    field.send_keys(value)


def _set_build_year(wait: WebDriverWait, test_id: str, year: str) -> None:
    year_input = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f"[data-testid='{test_id}'] input")
        )
    )
    year_input.click()
    year_input.send_keys(Keys.CONTROL, "a")
    year_input.send_keys(Keys.DELETE)
    year_input.send_keys(year)
    year_input.send_keys(Keys.ENTER)


def _select_dropdown_option(
    driver: Chrome,
    wait: WebDriverWait,
    test_id: str,
    option_text: str,
) -> None:
    trigger = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f"[data-testid='{test_id}'] [role='combobox']")
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        trigger,
    )
    trigger.click()

    option_locator = (
        By.XPATH,
        f"//li[@role='option' and normalize-space(.)='{option_text}']",
    )

    option = wait.until(EC.element_to_be_clickable(option_locator))
    option.click()
    wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.p-select-panel"))
    )
