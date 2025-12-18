from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable

import aiosmtplib
from jinja2 import Environment

from app.application.interfaces.iemail_service import IEmailService
from app.application.interfaces.igraph_service import IGraphService
from app.domain.repositories.ilisting_repository import IListingRepository
from app.infrastructure.config import config


class EmailService(IEmailService):
    def __init__(self, repository: IListingRepository, graph_service: IGraphService):
        self.smtp_srv_addr: str = "smtp.gmail.com"
        self.smtp_srv_port = 587
        self.gmail_pass: str = config.GMAIL_GENERATED_PASSWORD
        self.gmail_addr: str = config.GMAIL_ADDRESS
        self._smtp: aiosmtplib.SMTP | None = None

        self._repository = repository
        self.graph_service = graph_service

        self.env = Environment(enable_async=True)

        self.email_template = self.env.from_string(
            """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #000000;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    display: flex;
                    background-color: #f8f9fa;
                    justify-content: center;
                }
                .header-div {
                    flex: 1;
                    padding: 15px;
                    text-align: center;
                    border: 1px solid #dee2e6;
                }
                @media (max-width: 768px) {
                    .header {
                        flex-direction: column;
                    }
                }
                .table-container {
                    padding: 20px;
                    }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                    
                td {
                    border: 1px solid #dee2e6;
                    padding: 15px;
                    text-align: center;
                }
                .footer {
                    text-align: center;
                    padding: 20px;
                    font-size: 0.9em;
                    color: #1cba46;
                }
            </style>
        </head>
    <body>
        <header class="header">
            <div class="header-div">
                Real estate to {{ transaction_type }}<br>
                Price: {{ price }} PLN
            </div>
            <div class="header-div">
                {{ location }}, {{ street }}
            </div>
        </header>
        <div class="table-container">
            <table>
                <tr>
                    <td colspan="6">Additional information</td>
                </tr>
                <tr>
                    <td>Property type</td>
                    <td>{{ property_type }}</td>
                    <td>Floor</td>
                    <td>{{ floor }}</td>
                    <td>Area</td>
                    <td>{{ area }}</td>
                </tr>
                <tr>
                    <td>Number of floors</td>
                    <td> {{ num_of_floors }} </td>
                    <td>Build year</td>
                    <td> {{build_year}} </td>
                </tr>
            </table>
        </div>
        <div>
            <b>Description</b>
        </div>
        <div>
            {{ description }}
        </div>
        <div>
            <img src="cid:image1">
        </div>
        <div class="footer">
            <p>This is an automated email from RealtorCRM</p>
        </div>
    </body>
    </html>"""
        )

    async def get_listing_data(self, listing_id: str) -> Iterable:
        listing_data = await self._repository.get_single_listing(listing_id=listing_id)
        return listing_data.model_dump()

    async def get_smtp_conn(self):
        if self._smtp is None or not self._smtp.is_connected:
            self._smtp = aiosmtplib.SMTP(
                hostname=self.smtp_srv_addr, port=self.smtp_srv_port
            )
            await self._smtp.connect()
            await self._smtp.login(self.gmail_addr, self.gmail_pass)
        return self._smtp

    async def send_email(self, to, subject, listing_id: str):
        listing_data = await self.get_listing_data(listing_id=listing_id)

        graph_buffer = await self.graph_service.generate_graph_buffer()

        graph = graph_buffer.getvalue()

        graph_buffer.close()

        template_data = {
            "title": listing_data["title"],
            "location": listing_data["location"],
            "street": listing_data["street"],
            "price": listing_data["price"],
            "area": listing_data["area"],
            "property_type": listing_data["property_type"].value,
            "description": listing_data["description"],
            "transaction_type": listing_data["transaction_type"].value,
            "floor": listing_data["floor"],
            "num_of_floors": listing_data["num_of_floors"],
            "build_year": listing_data["build_year"],
            "graph": graph,
        }

        html = await self.email_template.render_async(**template_data)

        if isinstance(to, str):
            to = [to]

        body = MIMEMultipart()
        body["From"] = self.gmail_addr
        body["To"] = ", ".join(to)
        body["Subject"] = subject

        body.attach(MIMEText(html, "html", "UTF-8"))

        img = MIMEImage(graph)
        img.add_header("Content-ID", "<image1>")
        img.add_header("Content-Disposition", "attachment", filename="graph.png")

        body.attach(img)

        try:
            smtp = await self.get_smtp_conn()
            await smtp.send_message(body)
            await smtp.quit()
            return {"response": "email sent successfully"}
        except Exception:
            self._smtp = None

    async def disconnect(self):
        if self._smtp and self._smtp.is_connected:
            try:
                await self._smtp.quit()
            except aiosmtplib.SMTPException:
                pass
            finally:
                self._smtp = None
