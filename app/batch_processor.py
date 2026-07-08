import sys
from pathlib import Path

from app.pdf_reader import extract_text_from_pdf
from app.openai_parser import parse_hearing_text
from app.csv_writer import save_record_to_csv, is_duplicate_record


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.batch_processor <folder_path>")
        return
    
    folder_path = Path(sys.argv[1])

    if not folder_path.exists():
        print("Folder does not exist.")
        return
    if not folder_path.is_dir():
        print("Path is not a folder.")
        return
    
    pdf_files = list(folder_path.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file}")

        pdf_text = extract_text_from_pdf(pdf_file)

        if not pdf_text:
            print("No text extracted. Skipping.")
            continue

        result = parse_hearing_text(pdf_text)

        if not result:
            print("Parsing failed. Skipping.")
            continue

        if is_duplicate_record(result,"data/parsed_records.csv"):
            print("Duplicate record. Skipping.")
            continue

        save_record_to_csv(result, "data/parsed_records.csv")
        print("Saved to CSV.")


if __name__ == "__main__":
    main()