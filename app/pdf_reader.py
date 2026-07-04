from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    pdf_path = Path(pdf_path)

    reader = PdfReader(pdf_path)
    texts = []

    for page in reader.pages:
        text = page.extract_text()
        texts.append(text)
        
    return "\n".join(texts)


if __name__ == "__main__":
    pdf_path = "data/sample_pdfs/sample_001.pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text)