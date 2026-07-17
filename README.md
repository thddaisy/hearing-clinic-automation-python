# Hearing Clinic Automation (Python)

A Python backend automation project that processes hearing clinic PDF charts, extracts structured data with the OpenAI API, prevents duplicate records, saves results to CSV, generates monthly sales reports, and sends them through the Gmail API.

This project rebuilds an existing n8n automation workflow in Python using a modular backend structure.

## Overview

The project currently has two main workflows:

```text
1. PDF Processing Workflow

PDF files
→ text extraction
→ OpenAI parsing
→ structured records
→ duplicate prevention
→ CSV export
```

```text
2. Monthly Sales Reporting Workflow

Sales CSV
→ monthly sales summary
→ hospital-level summary
→ email subject and body generation
→ Gmail API delivery
```

## Features

* Extract text from hearing clinic PDF charts
* Parse chart text into structured data using the OpenAI API
* Save parsed records to CSV
* Prevent duplicate records using `chart_no`
* Process multiple PDF files in batch
* Read monthly sales records from CSV
* Calculate total sales, repair fees, and revenue
* Generate hospital-level sales summaries
* Build a monthly sales email subject and body
* Preview the generated report in the terminal
* Authenticate with Google using OAuth 2.0
* Save and reuse Gmail authentication tokens
* Send monthly reports through the Gmail API
* Load sensitive configuration values from environment variables

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
│   ├── email_sender.py
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
├── .gitignore
├── requirements.txt
└── README.md
```

Local configuration files such as `.env`, `credentials.json`, and `token.json` are excluded from Git.

## Tech Stack

Current:

* Python
* OpenAI API
* Gmail API
* Google OAuth 2.0
* CSV
* pypdf
* python-dotenv
* Google API Python Client
* Git / GitHub

Planned:

* PostgreSQL
* Docker
* APScheduler
* Automated tests
* Structured logging

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
OPENAI_API_KEY=your_openai_api_key_here
REPORT_RECIPIENT_EMAIL=recipient@example.com
```

The `.env` file must not be committed to GitHub.

Make sure `.gitignore` includes:

```gitignore
.env
.venv/
credentials.json
token.json
```

## Gmail API Setup

To enable email delivery:

1. Enable the Gmail API in Google Cloud.
2. Configure the OAuth consent screen.
3. Create an OAuth Client ID using the `Desktop app` application type.
4. Download the OAuth JSON file.
5. Rename it to `credentials.json`.
6. Place it in the project root directory.

The first time the reporting workflow runs, a browser window opens for Google login and permission approval.

After successful authentication, the program automatically creates:

```text
token.json
```

This file stores the authorized Gmail credentials locally and is reused for future executions.

## Usage

Run all commands from the project root directory.

### Process a single PDF

```bash
python -m app.openai_parser data/sample_pdfs/sample_001.pdf
```

This extracts text from the PDF, sends it to the OpenAI API, converts the response into structured data, and saves the result to CSV.

### Process multiple PDFs

```bash
python -m app.batch_processor data/sample_pdfs
```

This processes all `.pdf` files in the selected folder.

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

### Generate and send a monthly sales report

```bash
python -m app.email_reporter data/clinic_sales_records.csv
```

This command:

```text
reads the sales CSV
→ calculates monthly totals
→ creates hospital-level summaries
→ builds the email subject and body
→ prints a terminal preview
→ sends the report through the Gmail API
```

Example output:

```text
Loaded 96 records.

To: recipient@example.com
Subject: Monthly Hearing Clinic Sales Report

Total records: 96
Total sales: NZD 243,700.00
Total repair fees: NZD 3,880.00
Total revenue: NZD 247,580.00

Hospital Summary:
- H-001 | Records: 32 | Sales: NZD 90,600.00 | Repairs: NZD 1,400.00 | Revenue: NZD 92,000.00
- H-002 | Records: 32 | Sales: NZD 74,900.00 | Repairs: NZD 1,280.00 | Revenue: NZD 76,180.00
- H-003 | Records: 32 | Sales: NZD 78,200.00 | Repairs: NZD 1,200.00 | Revenue: NZD 79,400.00

Email sent: 19f6e9d45933cf2c
```

The value printed after `Email sent:` is the Gmail message ID returned by the Gmail API.

## PDF Processing Workflow

```text
PDF Charts
→ Text Extraction
→ OpenAI Parsing
→ Structured Record
→ Duplicate Check
   ├── Duplicate → Skip Record
   └── New Record → Save to CSV
→ parsed_records.csv
```

Main modules:

* `app/pdf_reader.py`: extracts text from PDF files
* `app/openai_parser.py`: parses extracted text using the OpenAI API
* `app/csv_writer.py`: saves parsed records and checks duplicates
* `app/batch_processor.py`: processes all PDF files in a folder

## Monthly Reporting Workflow

```text
clinic_sales_records.csv
→ Read Sales Records
→ Calculate Monthly Totals
→ Calculate Hospital Summaries
→ Build Email Subject and Body
→ Print Terminal Preview
→ Gmail API Authentication
→ Send Email
```

Main modules:

* `app/email_reporter.py`: reads sales records, calculates summaries, builds the report, and coordinates email delivery
* `app/email_sender.py`: creates email messages, authenticates with Gmail, and sends emails
* `app/config.py`: loads configuration values from the `.env` file

## Output Files

### Parsed PDF Records

```text
data/parsed_records.csv
```

Stores structured records extracted from PDF charts.

### Monthly Sales Records

```text
data/clinic_sales_records.csv
```

Contains sample monthly sales data used for report generation.

### Gmail Authentication Token

```text
token.json
```

Created automatically after the first successful Google OAuth login.

This file is used locally and must not be committed to GitHub.

## Current Status

Completed MVP features:

* PDF text extraction
* OpenAI-based chart parsing
* CSV export
* Duplicate record prevention
* Batch PDF processing
* Monthly sales calculations
* Hospital-level reporting
* Email subject and body generation
* Environment-based configuration
* Gmail OAuth authentication
* Gmail token storage and reuse
* Gmail API email delivery
* Basic email delivery error handling

## Future Improvements

* Add scheduled monthly reports with APScheduler
* Store parsed records and sales transactions in PostgreSQL
* Replace CSV-based storage with database repositories
* Add Docker support
* Add structured logging
* Add automated tests
* Add HTML email templates
* Improve Gmail API error handling
