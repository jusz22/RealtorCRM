import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import jwt
from fastapi import HTTPException

from app.infrastructure.security import (
    authenticate_user,
    create_token,
    get_password_hash,
    verify_password,
    verify_token,
)


class MockUser:
    def __init__(
        self,
        username,
        email="test@example.com",
        hashed_password="hashed_password_str",
        id=1,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password


class TestSecurityModule(unittest.IsolatedAsyncioTestCase):
    async def test_get_password_hash_returns_string(self):
        hashed = await get_password_hash("password123")
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, "password123")

    @patch("app.infrastructure.security.password_context.hash")
    async def test_get_password_hash_calls_context_hash(self, mock_hash):
        mock_hash.return_value = "mocked_hashed_password"
        await get_password_hash("password123")
        mock_hash.assert_called_once_with("password123")

    @patch("app.infrastructure.security.password_context.verify")
    async def test_verify_password_correct(self, mock_verify):
        mock_verify.return_value = True
        result = await verify_password("password123", "some_hash")
        self.assertTrue(result)
        mock_verify.assert_called_once_with("password123", "some_hash")

    @patch("app.infrastructure.security.password_context.verify")
    async def test_verify_password_incorrect(self, mock_verify):
        mock_verify.return_value = False
        result = await verify_password("wrong_password", "some_hash")
        self.assertFalse(result)
        mock_verify.assert_called_once_with("wrong_password", "some_hash")

    @patch("app.infrastructure.security.verify_password", new_callable=AsyncMock)
    @patch("app.infrastructure.security.get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_user_successful(
        self, mock_get_user_by_username, mock_verify_password
    ):
        mock_user_instance = MockUser(
            username="testuser", hashed_password="hashed_password123"
        )
        mock_get_user_by_username.return_value = mock_user_instance
        mock_verify_password.return_value = True

        authenticated_user = await authenticate_user("testuser", "password123")

        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, "testuser")
        mock_get_user_by_username.assert_called_once_with(username="testuser")
        mock_verify_password.assert_called_once_with(
            password="password123", hashed_password="hashed_password123"
        )

    @patch("app.infrastructure.security.verify_password", new_callable=AsyncMock)
    @patch("app.infrastructure.security.get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_user_not_found(
        self, mock_get_user_by_username, mock_verify_password
    ):
        mock_get_user_by_username.return_value = None

        authenticated_user = await authenticate_user("nonexistent", "password123")

        self.assertIsNone(authenticated_user)
        mock_get_user_by_username.assert_called_once_with(username="nonexistent")
        mock_verify_password.assert_not_called()

    @patch("app.infrastructure.security.verify_password", new_callable=AsyncMock)
    @patch("app.infrastructure.security.get_user_by_username", new_callable=AsyncMock)
    async def test_authenticate_user_wrong_password(
        self, mock_get_user_by_username, mock_verify_password
    ):
        mock_user_instance = MockUser(
            username="testuser", hashed_password="hashed_password123"
        )
        mock_get_user_by_username.return_value = mock_user_instance
        mock_verify_password.return_value = False

        authenticated_user = await authenticate_user("testuser", "wrong_password")

        self.assertIsNone(authenticated_user)
        mock_get_user_by_username.assert_called_once_with(username="testuser")
        mock_verify_password.assert_called_once_with(
            password="wrong_password", hashed_password="hashed_password123"
        )

    @patch("app.infrastructure.security.datetime")
    @patch("app.infrastructure.security.jwt.encode")
    @patch("app.infrastructure.security.config")
    async def test_create_token_default_expiration(
        self, mock_config, mock_jwt_encode, mock_datetime_module
    ):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"
        mock_config.ACCESS_TOKEN_EXPIRE_MINUTES = 15

        data_to_encode = {"sub": "testuser"}
        expected_token_str = "mocked.jwt.token"
        mock_jwt_encode.return_value = expected_token_str

        mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime_module.datetime.now.return_value = mock_now
        mock_datetime_module.timedelta = timedelta
        mock_datetime_module.timezone.utc = timezone.utc

        token = await create_token(data_to_encode.copy())

        self.assertEqual(token, expected_token_str)

        expected_expire_time = mock_now + timedelta(
            minutes=mock_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        expected_payload_to_encode = data_to_encode.copy()
        expected_payload_to_encode.update({"exp": expected_expire_time})

        mock_jwt_encode.assert_called_once_with(
            expected_payload_to_encode, mock_config.SECRET_KEY, mock_config.ALGORITHM
        )

    @patch("app.infrastructure.security.datetime")
    @patch("app.infrastructure.security.jwt.encode")
    @patch("app.infrastructure.security.config")
    async def test_create_token_custom_expiration(
        self, mock_config, mock_jwt_encode, mock_datetime_module
    ):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"

        data_to_encode = {"sub": "testuser"}
        custom_delta = timedelta(hours=2)
        expected_token_str = "mocked.jwt.token.custom_exp"
        mock_jwt_encode.return_value = expected_token_str

        mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime_module.datetime.now.return_value = mock_now
        mock_datetime_module.timedelta = timedelta
        mock_datetime_module.timezone.utc = timezone.utc

        token = await create_token(data_to_encode.copy(), expieres_delta=custom_delta)

        self.assertEqual(token, expected_token_str)

        expected_expire_time = mock_now + custom_delta
        expected_payload_to_encode = data_to_encode.copy()
        expected_payload_to_encode.update({"exp": expected_expire_time})

        mock_jwt_encode.assert_called_once_with(
            expected_payload_to_encode, mock_config.SECRET_KEY, mock_config.ALGORITHM
        )

    @patch("app.infrastructure.security.datetime")
    @patch("app.infrastructure.security.get_user_by_username", new_callable=AsyncMock)
    @patch("app.infrastructure.security.jwt.decode")
    @patch("app.infrastructure.security.config")
    async def test_verify_token_successful(
        self, mock_config, mock_jwt_decode, mock_get_user, mock_datetime_module
    ):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"

        mock_user_instance = MockUser(username="testuser")
        mock_get_user.return_value = mock_user_instance

        token_creation_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        expiration_datetime_obj = token_creation_time + timedelta(minutes=30)

        decoded_payload_for_schema = {"sub": "testuser", "exp": expiration_datetime_obj}
        mock_jwt_decode.return_value = decoded_payload_for_schema

        mock_now_for_verify = token_creation_time + timedelta(minutes=1)
        mock_datetime_module.datetime.now.return_value = mock_now_for_verify
        mock_datetime_module.timezone.utc = timezone.utc

        result = await verify_token(token="fake.valid.token")

        self.assertTrue(result)
        mock_jwt_decode.assert_called_once_with(
            "fake.valid.token",
            key=mock_config.SECRET_KEY,
            algorithms=[mock_config.ALGORITHM],
        )
        mock_get_user.assert_called_once_with(username="testuser")

    @patch("app.infrastructure.security.jwt.decode")
    @patch("app.infrastructure.security.config")
    async def test_verify_token_invalid_jwt_error(self, mock_config, mock_jwt_decode):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"
        mock_jwt_decode.side_effect = jwt.InvalidTokenError("bad token")

        with self.assertRaises(HTTPException) as cm:
            await verify_token(token="invalid.token.string")

        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(cm.exception.detail, "Could not validate credentials")
        mock_jwt_decode.assert_called_once()

    @patch("app.infrastructure.security.datetime")
    @patch("app.infrastructure.security.jwt.decode")
    @patch("app.infrastructure.security.config")
    async def test_verify_token_expired(
        self, mock_config, mock_jwt_decode, mock_datetime_module
    ):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"
        mock_config.ACCESS_TOKEN_EXPIRE_MINUTES = 15

        token_issue_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        expiration_datetime_obj = token_issue_time + timedelta(
            minutes=mock_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        decoded_payload_for_schema = {"sub": "testuser", "exp": expiration_datetime_obj}
        mock_jwt_decode.return_value = decoded_payload_for_schema

        mock_now_for_verify = token_issue_time + timedelta(
            minutes=mock_config.ACCESS_TOKEN_EXPIRE_MINUTES + 5
        )
        mock_datetime_module.datetime.now.return_value = mock_now_for_verify
        mock_datetime_module.timezone.utc = timezone.utc

        with self.assertRaises(HTTPException) as cm:
            await verify_token(token="expired.token.string")

        self.assertEqual(cm.exception.status_code, 401)
        mock_jwt_decode.assert_called_once()

    @patch("app.infrastructure.security.datetime")
    @patch("app.infrastructure.security.jwt.decode")
    @patch("app.infrastructure.security.config")
    async def test_verify_token_no_sub_in_payload(
        self, mock_config, mock_jwt_decode, mock_datetime_module
    ):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"

        expiration_datetime_obj = datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        decoded_payload_for_schema = {"exp": expiration_datetime_obj}
        mock_jwt_decode.return_value = decoded_payload_for_schema

        mock_now_for_verify = datetime(2023, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
        mock_datetime_module.datetime.now.return_value = mock_now_for_verify
        mock_datetime_module.timezone.utc = timezone.utc

        with self.assertRaises(HTTPException) as cm:
            await verify_token(token="token.no.sub")

        self.assertEqual(cm.exception.status_code, 401)
        mock_jwt_decode.assert_called_once()

    @patch("app.infrastructure.security.datetime")
    @patch("app.infrastructure.security.get_user_by_username", new_callable=AsyncMock)
    @patch("app.infrastructure.security.jwt.decode")
    @patch("app.infrastructure.security.config")
    async def test_verify_token_user_not_found_from_sub(
        self, mock_config, mock_jwt_decode, mock_get_user, mock_datetime_module
    ):
        mock_config.SECRET_KEY = "test_secret"
        mock_config.ALGORITHM = "HS256"

        mock_get_user.return_value = None

        expiration_datetime_obj = datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        decoded_payload_for_schema = {
            "sub": "unknown_user",
            "exp": expiration_datetime_obj,
        }
        mock_jwt_decode.return_value = decoded_payload_for_schema

        mock_now_for_verify = datetime(2023, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
        mock_datetime_module.datetime.now.return_value = mock_now_for_verify
        mock_datetime_module.timezone.utc = timezone.utc

        with self.assertRaises(HTTPException) as cm:
            await verify_token(token="token.unknown.user")

        self.assertEqual(cm.exception.status_code, 401)
        mock_jwt_decode.assert_called_once()
        mock_get_user.assert_called_once_with(username="unknown_user")


if __name__ == "__main__":
    unittest.main()
