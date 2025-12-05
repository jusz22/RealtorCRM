import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tests.e2e.utils.api_client import ApiClient

DEFAULT_PASSWORD = "password123"


def _build_chrome_options() -> Options:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options


@pytest.fixture(scope="session")
def frontend_base_url() -> str:
    return "http://localhost:4200"


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return "http://localhost:8000/api/v1"


@pytest.fixture(scope="session")
def api_client(api_base_url: str) -> ApiClient:
    return ApiClient(api_base_url)


@pytest.fixture(scope="session")
def register_user(api_client: ApiClient) -> dict:
    username = f"{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    res = api_client.register_user(
        username=username, password=DEFAULT_PASSWORD, email=email
    )
    return {
        "username": res["username"],
        "password": DEFAULT_PASSWORD,
        "email": res["email"],
    }


@pytest.fixture(scope="session")
def api_token(api_client: ApiClient, register_user: dict) -> str:
    return api_client.login(
        username=register_user["username"],
        password=register_user["password"],
    )


@pytest.fixture()
def listing_factory(api_client: ApiClient, api_token: str):
    created_ids: list[str] = []

    def _create_listing(**overrides) -> dict:
        listing = api_client.create_listing(api_token, **overrides)
        created_ids.append(listing["id"])
        return listing

    yield _create_listing

    for listing_id in created_ids:
        api_client.delete_listing(api_token, listing_id)


@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = _build_chrome_options()
    chrome_driver = webdriver.Chrome(service=service, options=options)
    chrome_driver.delete_all_cookies()
    yield chrome_driver
    chrome_driver.quit()
