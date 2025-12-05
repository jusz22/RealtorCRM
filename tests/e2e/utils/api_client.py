import uuid
from typing import Any, Dict, List

import requests

DEFAULT_TIMEOUT = 15.0


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = requests.Session()

    def register_user(self, username: str, password: str, email: str) -> Dict[str, Any]:
        payload = {"username": username, "hashed_password": password, "email": email}
        response = self.session.post(
            f"{self.base_url}/register", json=payload, timeout=DEFAULT_TIMEOUT
        )

        if response.status_code == 400 and "already exists" in response.text:
            return {
                "username": payload["username"],
                "password": payload["hashed_password"],
                "email": payload["email"],
            }

        return response.json()

    def login(self, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = self.session.post(
            f"{self.base_url}/login",
            data=data,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
        token_response = response.json()
        return token_response["access_token"]

    def create_listing(self, token: str, **overrides: Any) -> Dict[str, Any]:
        payload = {
            "client_id": overrides.get("client_id"),
            "title": overrides.get("title", f"{uuid.uuid1().hex[:8]}"),
            "location": overrides.get("location", "Test City"),
            "street": overrides.get("street", "123 Ave"),
            "price": overrides.get("price", 350000),
            "area": overrides.get("area", 120),
            "property_type": overrides.get("property_type", "House"),
            "description": overrides.get("description", "Test listing."),
            "transaction_type": overrides.get("transaction_type", "Sell"),
            "floor": overrides.get("floor", "1"),
            "num_of_floors": overrides.get("num_of_floors", "2"),
            "build_year": overrides.get("build_year", "2015"),
        }

        response = self.session.post(
            f"{self.base_url}/listings",
            json=[payload],
            headers=self._auth_headers(token),
            timeout=DEFAULT_TIMEOUT,
        )
        return response.json()[0]

    def list_listings(
        self,
        token: str,
        *,
        sort_by: str | None = None,
        sort_order: str | None = None,
        filter: str | None = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {}
        if sort_by:
            params["sort_by"] = sort_by
        if sort_order:
            params["sort_order"] = sort_order
        if filter:
            params["filter"] = filter

        response = self.session.get(
            f"{self.base_url}/listings",
            headers=self._auth_headers(token),
            params=params or None,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def get_listing(self, token: str, listing_id: str) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/listings/{listing_id}",
            headers=self._auth_headers(token),
            timeout=DEFAULT_TIMEOUT,
        )
        return response.json()

    def get_notes(self, token: str, listing_id: str) -> List[Dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/notes/{listing_id}",
            headers=self._auth_headers(token),
            timeout=DEFAULT_TIMEOUT,
        )
        return response.json()

    def delete_note(self, token: str, note_id: str) -> None:
        response = self.session.delete(
            f"{self.base_url}/notes/{note_id}",
            headers=self._auth_headers(token),
            timeout=DEFAULT_TIMEOUT,
        )
        if response.status_code != 200:
            response.raise_for_status()

    def delete_listing(self, token: str, listing_id: str) -> None:
        response = self.session.delete(
            f"{self.base_url}/listings/{listing_id}",
            headers=self._auth_headers(token),
            timeout=DEFAULT_TIMEOUT,
        )
        if response.status_code != 200:
            response.raise_for_status()

    def _auth_headers(self, token: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
