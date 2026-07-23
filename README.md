# Hearing Clinic Automation (Python)

A Python backend automation project that processes hearing clinic PDF charts, extracts structured data with the OpenAI API, prevents duplicate records, saves results to CSV, generates monthly sales reports, and sends them through the Gmail API.

This project rebuilds an existing n8n automation workflow in Python using a modular backend structure.

## Overview

The project contains two main automation workflows.

### PDF Processing Workflow

```text
PDF files
→ text extraction
→ OpenAI parsing
→ structured records
→ duplicate prevention
→ CSV export
```

### Monthly Sales Reporting Workflow

```text
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
* Preview generated reports in the terminal
* Authenticate with Google using OAuth 2.0
* Save and reuse Gmail authentication tokens
* Send reports through the Gmail API
* Load sensitive configuration from environment variables
* Schedule monthly reports with APScheduler
* Support development and monthly scheduler modes
* Save application logs to `logs/app.log`
* Record failures and error tracebacks
* Run automated tests with `pytest`

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
│   ├── report_scheduler.py
│   ├── config.py
│   └── logger.py
│
├── data/
│   ├── sample_pdfs/
│   ├── parsed_records.csv
│   └── clinic_sales_records.csv
│
├── tests/
│   ├── test_csv_writer.py
│   └── test_email_reporter.py
│
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

Local configuration files and generated logs such as `.env`, `credentials.json`, `token.json`, and `logs/` are excluded from Git.

## Tech Stack

* Python
* OpenAI API
* Gmail API
* Google OAuth 2.0
* CSV
* pypdf
* python-dotenv
* Google API Python Client
* APScheduler
* Python logging
* pytest
* Git / GitHub

Planned:

* PostgreSQL
* Docker
* GitHub Actions CI

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
logs/
```

## Gmail API Setup

To enable Gmail delivery:

1. Enable the Gmail API in Google Cloud.
2. Configure the OAuth consent screen.
3. Create an OAuth Client ID using the `Desktop app` type.
4. Download the OAuth JSON file.
5. Rename it to `credentials.json`.
6. Place it in the project root directory.

The first time the Gmail workflow runs, a browser window opens for login and permission approval.

After successful authentication, the application creates:

```text
token.json
```

This file stores the authorized Gmail credentials locally and is reused for future executions.

## Usage

Run all commands from the project root directory.

### Process a Single PDF

```bash
python -m app.openai_parser data/sample_pdfs/sample_001.pdf
```

This command extracts text from the PDF, sends it to the OpenAI API, converts the result into structured data, checks for duplicates, and saves the record to CSV.

### Process Multiple PDFs

```bash
python -m app.batch_processor data/sample_pdfs
```

This processes all `.pdf` files in the selected folder.

Example output:

```text
Processing: data\sample_pdfs\sample_001.pdf
Saved to CSV.

Processing: data\sample_pdfs\sample_002.pdf
Duplicate record. Skipping.
```

### Generate and Send a Monthly Sales Report

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

### Run the Report Scheduler

Development mode:

```bash
python -m app.report_scheduler dev
```

Development mode schedules the report once after 5 seconds. It is used to test the complete reporting workflow without waiting until the end of the month.

Monthly mode:

```bash
python -m app.report_scheduler monthly
```

Monthly mode keeps the scheduler running and sends the report at 5:30 PM on the last day of every month.

Stop the scheduler with:

```text
Ctrl + C
```

Application logs are saved to:

```text
logs/app.log
```

## Automated Tests

The project uses `pytest` to test reporting calculations and duplicate-prevention behavior.

Run all tests:

```bash
python -m pytest
```

Run tests with detailed test names:

```bash
python -m pytest -v
```

The current test suite covers:

* total record counts
* total sales, repair fees, and revenue
* hospital-level summaries
* email subject and body generation
* empty sales records
* invalid numeric values
* duplicate records
* non-duplicate records
* missing CSV files

CSV-related tests use pytest's `tmp_path` fixture to create temporary files. This prevents the tests from modifying real project data.

Current result:

```text
8 passed
```

## Main Modules

### PDF Processing

* `app/pdf_reader.py`: extracts text from PDF files
* `app/openai_parser.py`: parses extracted text using the OpenAI API
* `app/csv_writer.py`: saves records and checks duplicates
* `app/batch_processor.py`: processes multiple PDF files

### Monthly Reporting

* `app/email_reporter.py`: reads sales data, calculates summaries, and builds the report
* `app/email_sender.py`: authenticates with Gmail and sends emails
* `app/report_scheduler.py`: schedules development and monthly report jobs
* `app/config.py`: loads environment variables
* `app/logger.py`: writes terminal and file logs

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

Created automatically after the first successful OAuth login.

This file must remain local and must not be committed to GitHub.

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
* Gmail API email delivery
* APScheduler-based reporting
* File-based logging
* Error logging with tracebacks
* Automated tests with pytest
* Empty and invalid input tests
* Temporary CSV test files using pytest fixtures

## Future Improvements

* Store parsed records and sales transactions in PostgreSQL
* Replace CSV storage with database repositories
* Add Docker support
* Add GitHub Actions CI
* Add mocking tests for Gmail and external APIs
* Add HTML email templates
* Improve Gmail API error handling
* Add log rotation and retention

