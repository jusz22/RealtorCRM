import io
import unittest
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest.mock import AsyncMock, MagicMock, patch

import aiosmtplib

from app.application.interfaces.services.email_service import EmailService


class MockListingData:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def model_dump(self, include=None):
        return self.data_dict


class MockEnumValue:
    def __init__(self, value):
        self.value = value


class TestEmailService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_listing_repo = AsyncMock()
        self.mock_graph_service = AsyncMock()

        self.email_service = EmailService(
            repository=self.mock_listing_repo, graph_service=self.mock_graph_service
        )
        self.email_service.gmail_addr = "test_sender@example.com"
        self.email_service.gmail_pass = "test_password"

        self.listing_id = "test_listing_123"
        self.recipient_email = "recipient@example.com"
        self.email_subject = "Test Listing Information"

        self.mock_listing_details_dict_full = {
            "title": "Beautiful Apartment",
            "location": "Test City",
            "street": "123 Main St",
            "price": 500000,
            "area": "100 sqm",
            "property_type": MockEnumValue("Apartment"),
            "description": "A lovely place to live.",
            "transaction_type": MockEnumValue("Sale"),
            "floor": 3,
            "num_of_floors": 5,
            "build_year": 2010,
        }
        self.mock_graph_image_bytes = b"fake_graph_image_data"
        self.mock_rendered_html = "<html><body>Mocked Email Content</body></html>"

    async def asyncSetUp(self):
        self.patcher_render_async = patch.object(
            self.email_service.email_template, "render_async", new_callable=AsyncMock
        )
        self.mock_render_async = self.patcher_render_async.start()
        self.mock_render_async.return_value = self.mock_rendered_html

        self.patcher_mimemultipart = patch(
            "app.application.interfaces.services.email_service.MIMEMultipart",
            return_value=MagicMock(spec=MIMEMultipart),
        )
        self.mock_mimemultipart_class = self.patcher_mimemultipart.start()
        self.mock_multipart_msg = self.mock_mimemultipart_class.return_value

        self.patcher_mimetext = patch(
            "app.application.interfaces.services.email_service.MIMEText",
            return_value=MagicMock(spec=MIMEText),
        )
        self.mock_mimetext_class = self.patcher_mimetext.start()
        self.mock_mime_text = self.mock_mimetext_class.return_value

        self.patcher_mimeimage = patch(
            "app.application.interfaces.services.email_service.MIMEImage",
            return_value=MagicMock(spec=MIMEImage),
        )
        self.mock_mimeimage_class = self.patcher_mimeimage.start()
        self.mock_mime_image = self.mock_mimeimage_class.return_value

    async def asyncTearDown(self):
        self.patcher_render_async.stop()
        self.patcher_mimemultipart.stop()
        self.patcher_mimetext.stop()
        self.patcher_mimeimage.stop()
        try:
            if self.email_service._smtp and self.email_service._smtp.is_connected:
                original_side_effect = None
                if hasattr(self.email_service._smtp.quit, "side_effect_temp_removed"):
                    original_side_effect = self.email_service._smtp.quit.side_effect
                    self.email_service._smtp.quit.side_effect = None

                await self.email_service._smtp.quit()

                if original_side_effect:
                    self.email_service._smtp.quit.side_effect = original_side_effect
                    delattr(self.email_service._smtp.quit, "side_effect_temp_removed")

        except Exception:
            pass
        finally:
            self.email_service._smtp = None

    async def test_get_listing_data_success(self):
        mock_listing_obj = MockListingData(self.mock_listing_details_dict_full)
        self.mock_listing_repo.get_single_listing.return_value = mock_listing_obj
        result = await self.email_service.get_listing_data(self.listing_id)
        self.mock_listing_repo.get_single_listing.assert_called_once_with(
            listing_id=self.listing_id
        )
        self.assertEqual(result, self.mock_listing_details_dict_full)

    async def test_get_listing_data_repo_raises_exception(self):
        self.mock_listing_repo.get_single_listing.side_effect = ValueError("DB error")
        with self.assertRaises(ValueError):
            await self.email_service.get_listing_data(self.listing_id)

    @patch("app.application.interfaces.services.email_service.aiosmtplib.SMTP")
    async def test_get_smtp_conn_new_connection_success(self, mock_smtp_class):
        mock_smtp_instance = AsyncMock()
        mock_smtp_instance.is_connected = False
        mock_smtp_class.return_value = mock_smtp_instance
        self.email_service._smtp = None
        smtp_conn = await self.email_service.get_smtp_conn()
        mock_smtp_class.assert_called_once_with(
            hostname=self.email_service.smtp_srv_addr,
            port=self.email_service.smtp_srv_port,
        )
        mock_smtp_instance.connect.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(
            self.email_service.gmail_addr, self.email_service.gmail_pass
        )
        self.assertIs(smtp_conn, mock_smtp_instance)

    @patch("app.application.interfaces.services.email_service.aiosmtplib.SMTP")
    async def test_get_smtp_conn_new_connection_connect_fails(self, mock_smtp_class):
        mock_smtp_instance = AsyncMock()
        mock_smtp_instance.connect.side_effect = aiosmtplib.SMTPConnectError(
            "Failed to connect"
        )
        mock_smtp_class.return_value = mock_smtp_instance
        self.email_service._smtp = None
        with self.assertRaises(aiosmtplib.SMTPConnectError):
            await self.email_service.get_smtp_conn()
        mock_smtp_instance.login.assert_not_called()

    @patch("app.application.interfaces.services.email_service.aiosmtplib.SMTP")
    async def test_get_smtp_conn_new_connection_login_fails(self, mock_smtp_class):
        mock_smtp_instance = AsyncMock()
        mock_smtp_instance.is_connected = False
        mock_smtp_instance.login.side_effect = aiosmtplib.SMTPAuthenticationError(
            535, "Login failed"
        )
        mock_smtp_class.return_value = mock_smtp_instance
        self.email_service._smtp = None
        with self.assertRaises(aiosmtplib.SMTPAuthenticationError):
            await self.email_service.get_smtp_conn()
        mock_smtp_instance.connect.assert_called_once()

    async def test_get_smtp_conn_existing_connected(self):
        mock_existing_smtp = AsyncMock()
        mock_existing_smtp.is_connected = True
        self.email_service._smtp = mock_existing_smtp
        smtp_conn = await self.email_service.get_smtp_conn()
        self.assertIs(smtp_conn, mock_existing_smtp)
        mock_existing_smtp.connect.assert_not_called()

    @patch("app.application.interfaces.services.email_service.aiosmtplib.SMTP")
    async def test_get_smtp_conn_existing_not_connected_reconnects(
        self, mock_smtp_class_reconnect
    ):
        mock_old_smtp_instance = AsyncMock()
        mock_old_smtp_instance.is_connected = False
        self.email_service._smtp = mock_old_smtp_instance

        mock_new_smtp_instance = AsyncMock()
        mock_smtp_class_reconnect.return_value = mock_new_smtp_instance

        smtp_conn = await self.email_service.get_smtp_conn()

        mock_smtp_class_reconnect.assert_called_once_with(
            hostname=self.email_service.smtp_srv_addr,
            port=self.email_service.smtp_srv_port,
        )
        mock_new_smtp_instance.connect.assert_called_once()
        mock_new_smtp_instance.login.assert_called_once()
        self.assertIs(smtp_conn, mock_new_smtp_instance)

    async def common_send_email_setup_mocks(self):
        self.mock_listing_repo.get_single_listing.return_value = MockListingData(
            self.mock_listing_details_dict_full
        )
        self.mock_graph_service.generate_graph_buffer.return_value = io.BytesIO(
            self.mock_graph_image_bytes
        )
        return AsyncMock()

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_fetches_listing_and_graph(self, mock_get_smtp_conn):
        await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = AsyncMock()

        await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )
        self.mock_listing_repo.get_single_listing.assert_called_once_with(
            listing_id=self.listing_id
        )
        self.mock_graph_service.generate_graph_buffer.assert_called_once_with()

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_prepares_correct_template_data(self, mock_get_smtp_conn):
        await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = AsyncMock()

        await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )

        expected_template_data = {
            "title": "Beautiful Apartment",
            "location": "Test City",
            "street": "123 Main St",
            "price": 500000,
            "area": "100 sqm",
            "property_type": self.mock_listing_details_dict_full["property_type"].value,
            "description": "A lovely place to live.",
            "transaction_type": self.mock_listing_details_dict_full[
                "transaction_type"
            ].value,
            "floor": 3,
            "num_of_floors": 5,
            "build_year": 2010,
            "graph": self.mock_graph_image_bytes,
        }
        self.mock_render_async.assert_called_once()
        called_template_data = self.mock_render_async.call_args[1]
        for key, value in expected_template_data.items():
            self.assertEqual(
                called_template_data.get(key),
                value,
                f"Template data for '{key}' mismatch",
            )

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_constructs_mime_multipart_correctly_single_recipient(
        self, mock_get_smtp_conn
    ):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn

        await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )

        self.mock_mimemultipart_class.assert_called_once()
        self.mock_multipart_msg.__setitem__.assert_any_call(
            "From", self.email_service.gmail_addr
        )
        self.mock_multipart_msg.__setitem__.assert_any_call("To", self.recipient_email)
        self.mock_multipart_msg.__setitem__.assert_any_call(
            "Subject", self.email_subject
        )

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_constructs_mime_multipart_correctly_multiple_recipients(
        self, mock_get_smtp_conn
    ):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn
        recipients = ["r1@example.com", "r2@example.com"]

        await self.email_service.send_email(
            recipients, "Multi Subject", self.listing_id
        )
        self.mock_multipart_msg.__setitem__.assert_any_call(
            "To", "r1@example.com, r2@example.com"
        )

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_attaches_mime_text(self, mock_get_smtp_conn):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn

        await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )

        self.mock_mimetext_class.assert_called_once_with(
            self.mock_rendered_html, "html", "UTF-8"
        )
        self.mock_multipart_msg.attach.assert_any_call(self.mock_mime_text)

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_attaches_mime_image(self, mock_get_smtp_conn):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn

        await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )

        self.mock_mimeimage_class.assert_called_once_with(self.mock_graph_image_bytes)
        self.mock_mime_image.add_header.assert_any_call("Content-ID", "<image1>")
        self.mock_mime_image.add_header.assert_any_call(
            "Content-Disposition", "attachment", filename="graph.png"
        )
        self.mock_multipart_msg.attach.assert_any_call(self.mock_mime_image)

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_smtp_send_and_quit_successful(self, mock_get_smtp_conn):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn

        response = await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )

        mock_get_smtp_conn.assert_called_once()
        mock_smtp_conn.send_message.assert_called_once_with(self.mock_multipart_msg)
        mock_smtp_conn.quit.assert_called_once()
        self.assertEqual(response, {"response": "email sent successfully"})

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_handles_listing_data_fetch_failure(
        self, mock_get_smtp_conn
    ):
        self.mock_listing_repo.get_single_listing.side_effect = ValueError("Repo error")
        with self.assertRaises(ValueError):
            await self.email_service.send_email(
                self.recipient_email, self.email_subject, self.listing_id
            )
        self.mock_graph_service.generate_graph_buffer.assert_not_called()
        mock_get_smtp_conn.assert_not_called()

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_handles_graph_generation_failure(
        self, mock_get_smtp_conn
    ):
        self.mock_listing_repo.get_single_listing.return_value = MockListingData(
            self.mock_listing_details_dict_full
        )
        self.mock_graph_service.generate_graph_buffer.side_effect = BufferError(
            "Graph error"
        )
        with self.assertRaises(BufferError):
            await self.email_service.send_email(
                self.recipient_email, self.email_subject, self.listing_id
            )
        mock_get_smtp_conn.assert_not_called()

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_handles_template_render_failure(self, mock_get_smtp_conn):
        await self.common_send_email_setup_mocks()
        self.mock_render_async.side_effect = Exception("Template render error")
        with self.assertRaises(Exception):
            await self.email_service.send_email(
                self.recipient_email, self.email_subject, self.listing_id
            )
        mock_get_smtp_conn.assert_not_called()

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_handles_get_smtp_conn_failure_during_send(
        self, mock_get_smtp_conn
    ):
        await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.side_effect = aiosmtplib.SMTPException(
            "Cannot connect for send"
        )

        response = await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )
        self.assertIsNone(response)
        self.assertIsNone(self.email_service._smtp)

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_handles_smtp_send_message_failure(
        self, mock_get_smtp_conn
    ):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_smtp_conn.send_message.side_effect = aiosmtplib.SMTPServerDisconnected(
            "Server disconnected"
        )
        mock_get_smtp_conn.return_value = mock_smtp_conn
        self.email_service._smtp = mock_smtp_conn

        response = await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )
        self.assertIsNone(response)
        self.assertIsNone(
            self.email_service._smtp, "SMTP connection should be reset on send failure."
        )
        mock_smtp_conn.quit.assert_not_called()

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_handles_smtp_quit_failure_after_send(
        self, mock_get_smtp_conn
    ):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_smtp_conn.quit.side_effect = aiosmtplib.SMTPException("Quit failed")
        mock_get_smtp_conn.return_value = mock_smtp_conn
        self.email_service._smtp = mock_smtp_conn

        response = await self.email_service.send_email(
            self.recipient_email, self.email_subject, self.listing_id
        )

        self.assertIsNone(response)
        self.assertIsNone(self.email_service._smtp)

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_empty_recipient_string(self, mock_get_smtp_conn):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn

        await self.email_service.send_email(
            to="", subject="Empty To", listing_id=self.listing_id
        )
        self.mock_multipart_msg.__setitem__.assert_any_call("To", "")

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_empty_recipient_list(self, mock_get_smtp_conn):
        mock_smtp_conn = await self.common_send_email_setup_mocks()
        mock_get_smtp_conn.return_value = mock_smtp_conn

        await self.email_service.send_email(
            to=[], subject="Empty To List", listing_id=self.listing_id
        )
        self.mock_multipart_msg.__setitem__.assert_any_call("To", "")

    @patch.object(EmailService, "get_smtp_conn", new_callable=AsyncMock)
    async def test_send_email_listing_data_missing_keys(self, mock_get_smtp_conn):
        incomplete_listing_data = self.mock_listing_details_dict_full.copy()
        del incomplete_listing_data["street"]
        self.mock_listing_repo.get_single_listing.return_value = MockListingData(
            incomplete_listing_data
        )
        self.mock_graph_service.generate_graph_buffer.return_value = io.BytesIO(
            self.mock_graph_image_bytes
        )

        with self.assertRaises(KeyError):
            await self.email_service.send_email(
                self.recipient_email, self.email_subject, self.listing_id
            )
        self.mock_render_async.assert_not_called()

    async def test_disconnect_when_connected_quits_and_resets(self):
        mock_smtp = AsyncMock()
        mock_smtp.is_connected = True
        self.email_service._smtp = mock_smtp
        await self.email_service.disconnect()
        mock_smtp.quit.assert_called_once()
        self.assertIsNone(self.email_service._smtp)

    async def test_disconnect_when_not_connected_does_nothing(self):
        mock_smtp = AsyncMock()
        mock_smtp.is_connected = False
        self.email_service._smtp = mock_smtp
        await self.email_service.disconnect()
        mock_smtp.quit.assert_not_called()
        self.assertIs(self.email_service._smtp, mock_smtp)

    async def test_disconnect_when_smtp_is_none(self):
        self.email_service._smtp = None
        await self.email_service.disconnect()

    async def test_disconnect_handles_quit_exception(self):
        mock_smtp = AsyncMock()
        mock_smtp.is_connected = True
        quit_error = aiosmtplib.SMTPException("Quit error")
        mock_smtp.quit.side_effect = quit_error
        self.email_service._smtp = mock_smtp

        await self.email_service.disconnect()

        mock_smtp.quit.assert_called_once()
        self.assertIsNone(self.email_service._smtp)


if __name__ == "__main__":
    unittest.main()
