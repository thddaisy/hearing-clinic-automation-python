from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file."""
    pdf_path = Path(pdf_path)

    reader = PdfReader(pdf_path)

    first_page = reader.pages[0]

    text = first_page.extract_text()

    return text

if __name__ == "__main__":
    pdf_path = "data/sample_pdfs/sample_001.pdf"
    text = extract_text_from_pdf(pdf_path)
    print(text)
    