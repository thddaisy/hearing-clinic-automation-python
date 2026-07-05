import json
import sys
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.pdf_reader import extract_text_from_pdf


def parse_hearing_text(text):
    if not OPENAI_API_KEY:
        print("API key not found.")
        return None

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
Use these keys:
patient_name, clinic_name, consultation_date, doctor, audiologist, chart_no, ear_side, demo_model, record_type, device_model, total_amount, summary.

Rules:
- Extract only information explicitly present in the text.
- If a value is missing or shown as "-", use null.
- Do not guess or infer missing values.
- device_model should be a hearing aid or device model clearly mentioned in the note.
- total_amount should be null if no price or total amount appears in the text.
- Return only valid JSON.
- Do not include ```json.
- Do not include markdown code fences.
- Do not include explanation.

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.openai_parser <pdf_path>")
    else:
        pdf_path = sys.argv[1]
        pdf_text = extract_text_from_pdf(pdf_path)

        if not pdf_text:
            print("No text extracted from the PDF.")
        else:
            result = parse_hearing_text(pdf_text)

            if result:
                print(result)