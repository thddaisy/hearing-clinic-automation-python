import sys
from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print("File does not exist.")
        return ""
    if not pdf_path.is_file():
        print("Path is not a file.")
        return ""
    if pdf_path.suffix.lower() != ".pdf":
        print("File is not a PDF.")
        return ""
    
    reader = PdfReader(pdf_path)
    texts = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            texts.append(text)
        
    return "\n".join(texts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app/pdf_reader.py <pdf_path>")
    else:
        pdf_path = sys.argv[1]
        pdf_text = extract_text_from_pdf(pdf_path)
        
        if pdf_text:
            print(pdf_text)