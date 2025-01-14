from typing import Iterable
from jinja2 import Environment
import resend
import importlib

from app.application.interfaces.iemail_service import IEmailService
from app.domain.repositories.ilisting_repository import IListingRepository


class EmailService(IEmailService):
    def __init__(self, API_KEY: str, repository: IListingRepository):

        self._repository = repository
        
        resend.api_key=API_KEY

        self.env = Environment(enable_async=True)
    
        self.email_template = self.env.from_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
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
                    color: #666666;
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
                {{ location }},<br>
                {{ street }}<br>
                {{ area }}
            </div>
        </header>
        <div class="table-container">
            <table>
                <tr>
                    <td colspan="4">Additional information</td>
                </tr>
                <tr>
                    <td>Property type</td>
                    <td>{{ property_type }}</td>
                    <td>Floor</td>
                    <td>{{ floor }}</td>
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
            <div class="footer">
                <p>This is an automated email from RealtorCRM</p>
            </div>
    </body>
    </html>""")

    def _get_enum_value(enum_str: str):

        module = importlib.import_module("app.infrastructure.models.listing_model")
        
        enum_class_name, property_name = enum_str.split('.')

        enum_class = getattr(module, enum_class_name)

        property_value = enum_class[property_name].value

        return property_value

    async def get_listing_data(self, listing_id: str) -> Iterable:

        listing_data = await self._repository.get_single_listing(listing_id=listing_id)
        return listing_data.model_dump()


    async def send_email(self, to, subject, listing_id: str):

        listing_data = await self.get_listing_data(listing_id=listing_id)
        
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
            "build_year": listing_data["build_year"]
        }
        
        html = await self.email_template.render_async(**template_data)
        
        params = {
            "from": "onboarding@resend.dev",
            "to": to,
            "subject": subject,
            "html": html
        }

        if isinstance(to, str):
            to = [to]

        response = resend.Emails.send(params=params)
        
        return response