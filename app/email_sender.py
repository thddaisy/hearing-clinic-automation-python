import base64
from email.message import EmailMessage
from pathlib import Path
from app.config import REPORT_RECIPIENT_EMAIL

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def create_email(recipient, subject, body):
    message = EmailMessage()
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    return message


def get_gmail_service():
    token_path = Path("token.json")

    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES,
        )

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES,
        )
    
        credentials = flow.run_local_server(port=0)


        with open("token.json", "w") as token_file:
            token_file.write(credentials.to_json())


    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    return service


def send_email(recipient, subject, body):
    
    message = create_email(recipient, subject, body)
    service = get_gmail_service()

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
        ).decode()
    
    email_body = {
        "raw": encoded_message
    }

    sent_message = (
        service.users()
        .messages()
        .send(
            userId="me",
            body=email_body,
        )
        .execute()
    )

    return sent_message
