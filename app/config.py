import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPORT_RECIPIENT_EMAIL = os.getenv("REPORT_RECIPIENT_EMAIL")