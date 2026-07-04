from app.config import OPENAI_API_KEY
from openai import OpenAI
import json

def parse_hearing_text(text):
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = f"""
                Extract the following information from the hearing clinic text.
                Return only valid JSON.
                Do not include markdown code fences.
                Use these keys:
                client_name, clinic_name, date, product, total_amount.

                Text:
                {text}
                """
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
        result_text = response.output_text
        data = json.loads(result_text)
        return data
    else:
        print("API key not found.")

if __name__ == "__main__":
    sample_text = """
                Client: John Smith
                Clinic: ABC Hearing Clinic
                Date: 2026-07-04
                Product: Hearing Aid Model A
                Total: $1,250
                """
    result = parse_hearing_text(sample_text)
    if result:
        print(result)