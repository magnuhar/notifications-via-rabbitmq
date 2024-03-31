from sendgrid.helpers.mail import *
from sendgrid import SendGridAPIClient
import os

def send_email(recipient: str, subject: str, body: str):
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    from_email = os.getenv("FROM_EMAIL")
    to_email = recipient
    subject = subject
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)