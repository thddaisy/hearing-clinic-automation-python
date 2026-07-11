# Hearing Clinic Automation (Python)

A Python backend automation project that processes hearing clinic PDF charts, extracts structured data with the OpenAI API, saves parsed records to CSV, prevents duplicate entries, and generates a monthly sales email report preview.

This project rebuilds an existing n8n automation workflow in Python with a modular backend structure.

## Overview

The project currently has two main workflows:

```text
1. PDF Processing Workflow

PDF files
→ text extraction
→ OpenAI parsing
→ structured records
→ CSV export
→ duplicate prevention
```

```text
2. Monthly Sales Reporting Workflow

Sales CSV
→ monthly sales summary
→ hospital-level summary
→ email report preview
```

## Features

- Extract text from hearing clinic PDF charts
- Parse chart text into structured data using the OpenAI API
- Save parsed records to CSV
- Prevent duplicate records using `chart_no`
- Process multiple PDF files in batch
- Read monthly sales records from CSV
- Calculate total sales, repair fees, and revenue
- Generate hospital-level sales summaries
- Print a monthly sales email report preview

## Project Structure

```text
hearing-clinic-automation-python/

├── app/
│   ├── __init__.py
│   ├── pdf_reader.py
│   ├── openai_parser.py
│   ├── csv_writer.py
│   ├── batch_processor.py
│   ├── email_reporter.py
│   ├── config.py
│   └── logger.py
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

## Tech Stack

Current:

- Python
- OpenAI API
- CSV
- pypdf
- python-dotenv
- Git / GitHub

Planned:

- PostgreSQL
- Docker
- Google APIs
- APScheduler

## Setup

Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root directory.

```env
OPENAI_API_KEY=your_api_key_here
```

The `.env` file must not be committed to GitHub.

Make sure `.gitignore` includes:

```text
.env
.venv/
```

## Usage

### Process a single PDF

Run from the project root directory:

```bash
python -m app.openai_parser data/sample_pdfs/sample_001.pdf
```

This extracts text from the PDF, sends it to the OpenAI API, converts the response into structured data, and saves the result to CSV.

### Process multiple PDFs

Run from the project root directory:

```bash
python -m app.batch_processor data/sample_pdfs
```

This processes all `.pdf` files in the given folder.

Example output:

```text
Processing: data\sample_pdfs\sample_001.pdf
Saved to CSV.
Processing: data\sample_pdfs\sample_002.pdf
Saved to CSV.
```

If a record with the same `chart_no` already exists, it is skipped.

```text
Duplicate record. Skipping.
```

### Generate a monthly sales email preview

Run from the project root directory:

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

## PDF Processing Workflow

```text
PDF Charts
→ Text Extraction
→ OpenAI Parsing
→ Structured Records
→ Duplicate Check
   ├── Yes → Skip Record
   └── No  → Save to CSV
→ parsed_records.csv
```

Main modules:

- `app/pdf_reader.py`: extracts text from PDF files
- `app/openai_parser.py`: parses extracted text into structured data using the OpenAI API
- `app/csv_writer.py`: saves parsed records to CSV and checks duplicates
- `app/batch_processor.py`: processes all PDF files in a folder

## Monthly Reporting Workflow

```text
clinic_sales_records.csv
→ Read Sales Records
→ Monthly Sales Summary
→ Hospital Summary
→ Email Report Preview
```

Main module:

- `app/email_reporter.py`: reads sales records, calculates monthly totals, groups revenue by hospital, and prints an email preview

## Output Files

### Parsed PDF Records

```text
data/parsed_records.csv
```

This file stores structured records extracted from PDF charts.

### Monthly Sales Records

```text
data/clinic_sales_records.csv
```

This file stores sample monthly sales records used for report generation.

## Current Status

Completed MVP features:

- PDF text extraction
- OpenAI-based chart parsing
- CSV export
- Duplicate record prevention
- Batch PDF processing
- Monthly sales email report preview

## Future Improvements

- Add real email sending with SMTP or Gmail API
- Move email settings into environment variables
- Add scheduled monthly reports with APScheduler
- Store parsed records and sales transactions in PostgreSQL
- Add Docker support
- Add Google API integration