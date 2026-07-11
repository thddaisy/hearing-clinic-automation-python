# Hearing Clinic Automation (Python)

Python implementation of the Hearing Clinic Automation workflow.

This project rebuilds an existing n8n automation workflow in Python, step by step, to process hearing clinic PDF documents, extract structured data, save records to CSV, and generate monthly reporting output.

The goal of this project is not only to recreate the automation, but also to learn practical Python backend development through a real workflow.

## Project Pipeline

The current automation pipeline is:

```text
PDF files
→ text extraction
→ OpenAI parsing
→ structured data
→ CSV export
→ duplicate prevention
→ sales CSV reporting
→ monthly email preview
```

The project currently supports two main workflows:

```text
1. PDF Processing Workflow

PDF file or folder
→ text extraction
→ OpenAI parsing
→ structured data
→ CSV export
```

```text
2. Monthly Sales Reporting Workflow

Sales CSV
→ read sales records
→ calculate monthly sales summary
→ calculate hospital-level summary
→ generate email preview
```

## Project Structure

```text
hearing-clinic-automation-python/

├── app/
│   ├── __init__.py
│   ├── pdf_reader.py
│   ├── config.py
│   ├── logger.py
│   ├── openai_parser.py
│   ├── csv_writer.py
│   ├── batch_processor.py
│   └── email_reporter.py
│
├── data/
│   ├── sample_pdfs/
│   │   ├── sample_001.pdf
│   │   ├── sample_002.pdf
│   │   ├── sample_003.pdf
│   │   ├── sample_004.pdf
│   │   └── sample_005.pdf
│   │
│   ├── parsed_records.csv
│   └── clinic_sales_records.csv
│
├── docs/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Environment Variables

This project uses a `.env` file to store sensitive configuration values.

Create a `.env` file in the project root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

The `.env` file must not be committed to GitHub.

Make sure `.gitignore` includes:

```text
.env
.venv/
```

## PDF Reader

The PDF Reader is the first feature of this project.

It reads a PDF file, extracts text from all pages, and returns the extracted text as a single string.

This feature is the foundation for the next steps of the automation pipeline.

```text
PDF file
→ text extraction
```

### Current Features

* Reads a PDF file from a terminal argument
* Extracts text from all pages
* Skips empty pages or pages without extractable text
* Checks whether the input path exists
* Checks whether the input path is a file
* Checks whether the file extension is `.pdf`
* Returns extracted text for reuse by other modules
* Prints the extracted text when run directly

### Usage

Run the PDF Reader from the project root directory:

```bash
python app/pdf_reader.py data/sample_pdfs/sample_001.pdf
```

If no PDF path is provided, the program shows a usage message:

```bash
python app/pdf_reader.py
```

Example output:

```text
Usage: python app/pdf_reader.py <pdf_path>
```

### Error Handling

If the file does not exist:

```text
File does not exist.
```

If the path is not a file:

```text
Path is not a file.
```

If the file is not a PDF:

```text
File is not a PDF.
```

## OpenAI Parser

The OpenAI Parser takes extracted text from a hearing clinic PDF and sends it to the OpenAI API.

The response is returned as structured JSON-like data and converted into a Python dictionary.

This feature connects the PDF Reader to the next stage of the automation pipeline:

```text
PDF file
→ text extraction
→ OpenAI parsing
→ structured data
```

### Current Features

* Reads extracted PDF text from the PDF Reader
* Sends the text to the OpenAI API
* Extracts structured hearing clinic chart information
* Returns valid JSON from the OpenAI response
* Converts the JSON string into a Python dictionary with `json.loads()`
* Uses environment variables for the OpenAI API key
* Avoids hardcoding sensitive API keys in the source code
* Handles missing PDF text before calling the OpenAI API

### Extracted Fields

The parser currently extracts the following fields:

```text
patient_name
clinic_name
consultation_date
doctor
audiologist
chart_no
ear_side
demo_model
record_type
device_model
total_amount
summary
```

If a value is missing or shown as `-`, the parser should return `null`.

### Usage

Run the OpenAI Parser from the project root directory:

```bash
python -m app.openai_parser data/sample_pdfs/sample_001.pdf
```

Example output:

```python
{
    'patient_name': 'Sophia Turner',
    'clinic_name': 'Christchurch ENT Clinic',
    'consultation_date': '04-06-2026',
    'doctor': 'James Hargreaves',
    'audiologist': 'Daisy Song',
    'chart_no': 'P1-007',
    'ear_side': 'Right',
    'demo_model': None,
    'record_type': 'Repair Completed',
    'device_model': 'Signia Styletto X',
    'total_amount': None,
    'summary': '...'
}
```

### Error Handling

If the API key is missing:

```text
API key not found.
```

If no PDF path is provided:

```text
Usage: python -m app.openai_parser <pdf_path>
```

If no text can be extracted from the PDF:

```text
No text extracted from the PDF.
```

## CSV Export

Parsed hearing clinic records can be saved to a CSV file.

Output file:

```bash
data/parsed_records.csv
```

The CSV Export feature saves a parsed Python dictionary as a CSV row.

```text
structured data
→ CSV export
```

### Current Features

* Saves parsed OpenAI results into a CSV file
* Uses Python's built-in `csv` module
* Uses `csv.DictWriter` to write dictionary data as CSV rows
* Writes the CSV header only when the file does not already exist
* Appends new records without deleting existing records
* Saves missing values as empty CSV cells

### Example CSV Output

```csv
patient_name,clinic_name,consultation_date,doctor,audiologist,chart_no,ear_side,demo_model,record_type,device_model,total_amount,summary
Sophia Turner,Christchurch ENT Clinic,04-06-2026,James Hargreaves,Daisy Song,P1-007,Right,,Repair Completed,Signia Styletto X,,"Sophia's right Signia Styletto X hearing aid was repaired..."
```

Missing values are saved as empty CSV cells.

For example, if `demo_model` or `total_amount` is missing, the CSV may show empty fields:

```csv
Sophia Turner,Christchurch ENT Clinic,04-06-2026,James Hargreaves,Daisy Song,P1-007,Right,,Repair Completed,Signia Styletto X,,
```

These empty fields can later be converted to `NULL` when inserting records into PostgreSQL.

## Batch PDF Processing

The Batch Processor processes multiple PDF files from a folder.

It finds all `.pdf` files in a given folder, extracts text from each file, sends the text to the OpenAI Parser, and saves each parsed result to the CSV file.

This feature extends the automation pipeline from processing one PDF at a time to processing multiple PDF files automatically.

```text
PDF folder
→ find PDF files
→ process each PDF
→ extract text
→ OpenAI parsing
→ structured data
→ CSV export
```

### Duplicate Prevention

The batch processor prevents duplicate CSV records by checking the `chart_no` field before saving parsed data.

If a record with the same `chart_no` already exists in `data/parsed_records.csv`, the processor skips the record and prints:

```text
Duplicate record. Skipping.
```

### Current Features

* Receives a folder path from a terminal argument
* Checks whether the folder exists
* Checks whether the path is a folder
* Finds all `.pdf` files in the folder using `Path.glob("*.pdf")`
* Converts the found files into a list
* Handles empty folders with no PDF files
* Processes each PDF file one by one
* Skips PDFs with no extractable text
* Skips records when OpenAI parsing fails
* Checks duplicate records by `chart_no`
* Saves successful parsed records to `data/parsed_records.csv`

### Usage

Run the Batch Processor from the project root directory:

```bash
python -m app.batch_processor data/sample_pdfs
```

Example output:

```text
Processing: data\sample_pdfs\sample_001.pdf
Saved to CSV.
Processing: data\sample_pdfs\sample_002.pdf
Saved to CSV.
Processing: data\sample_pdfs\sample_003.pdf
Saved to CSV.
Processing: data\sample_pdfs\sample_004.pdf
Saved to CSV.
Processing: data\sample_pdfs\sample_005.pdf
Saved to CSV.
```

If the same records already exist in the CSV file:

```text
Processing: data\sample_pdfs\sample_001.pdf
Duplicate record. Skipping.
```

If no folder path is provided:

```text
Usage: python -m app.batch_processor <folder_path>
```

If the folder does not exist:

```text
Folder does not exist.
```

If the path is not a folder:

```text
Path is not a folder.
```

If no PDF files are found:

```text
No PDF files found in the folder.
```

## Email Reporter

The Email Reporter generates a monthly sales report from a clinic sales CSV file.

This feature is part of the reporting stage of the automation pipeline. It reads sales records, calculates total revenue, summarizes sales by hospital, and prints an email preview in the terminal.

The current version does not send real emails yet. It only generates a preview so the report content can be checked safely before email sending is added.

```text
Sales CSV
→ read sales records
→ calculate monthly sales summary
→ calculate hospital-level summary
→ generate email preview
```

### Input File

The Email Reporter uses the following sample sales CSV file:

```bash
data/clinic_sales_records.csv
```

The sales CSV contains monthly clinic transaction records such as:

```text
record_id
record_date
hospital_id
patient_name
chart_no
doctor_name
audiologist_name
transaction_type
brand
product_model
ear_side
sale_price_nzd
repair_fee_nzd
memo
```

### Current Features

* Reads sales records from a CSV file
* Counts the total number of records
* Calculates total hearing aid sales
* Calculates total repair fees
* Calculates total revenue
* Groups sales records by `hospital_id`
* Calculates hospital-level sales, repair fees, and revenue
* Generates a monthly sales email preview
* Prints the email preview in the terminal
* Keeps real email sending separate for a future step

### Usage

Run the Email Reporter from the project root directory:

```bash
python -m app.email_reporter data/clinic_sales_records.csv
```

Example output:

```text
To: company@example.com
Subject: Monthly Hearing Clinic Sales Report

Total records: 96
Total sales: NZD 243,700.00
Total repair fees: NZD 3,880.00
Total revenue: NZD 247,580.00

Hospital Summary:
- H-001 | Records: 32 | Sales: NZD 90,600.00 | Repairs: NZD 1,400.00 | Revenue: NZD 92,000.00
- H-002 | Records: 32 | Sales: NZD 74,900.00 | Repairs: NZD 1,280.00 | Revenue: NZD 76,180.00
- H-003 | Records: 32 | Sales: NZD 78,200.00 | Repairs: NZD 1,200.00 | Revenue: NZD 79,400.00
```

If no CSV path is provided:

```text
Usage: python -m app.email_reporter <csv_path>
```

If the CSV file does not exist:

```text
CSV file not found.
```

## Updated Project Pipeline

The current project can now process one PDF, process multiple PDFs, prevent duplicate parsed records, and generate a monthly sales email preview.

Single PDF flow:

```text
PDF file
→ text extraction
→ OpenAI parsing
→ structured data
→ CSV export
```

Batch PDF flow:

```text
PDF folder
→ PDF file list
→ text extraction for each PDF
→ OpenAI parsing for each PDF
→ structured data
→ duplicate check
→ CSV export
```

Email reporting flow:

```text
Sales CSV
→ monthly sales summary
→ hospital-level summary
→ email preview
```

Current MVP flow:

```text
PDF files
→ text extraction
→ OpenAI parsing
→ structured data
→ CSV export
→ sales CSV reporting
→ monthly email preview
```

## Next Steps

Planned next steps:

* Add real email sending with SMTP or Gmail API
* Move company email settings into environment variables
* Add scheduled monthly reports with APScheduler
* Refactor repeated file path values into configuration
* Add better logging for successful and failed processing
* Design a PostgreSQL table for hearing clinic chart records
* Design a PostgreSQL table for sales transactions
* Convert empty CSV values to PostgreSQL `NULL`
* Insert parsed records and sales records into PostgreSQL
* Add Google API integration
* Add Docker support for deployment

```
```
