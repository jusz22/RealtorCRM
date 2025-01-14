import resend

from app.application.interfaces.iemail_service import IEmailService


class EmailService(IEmailService):
    def __init__(self, API_KEY: str):
        resend.api_key=API_KEY

    async def send_email(self, to, subject, html):
        
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