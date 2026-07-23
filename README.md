# Hearing Clinic Automation (Python)

A Python backend automation project that processes hearing clinic PDF charts, extracts structured data using the OpenAI API, stores records in CSV and PostgreSQL, generates SQL-based monthly sales reports, and sends reports through the Gmail API.

This project rebuilds an existing n8n workflow as a modular Python backend application.

## Overview

The project contains two main automation workflows.

### PDF Processing Workflow

```text
PDF files
→ text extraction
→ OpenAI parsing
→ structured records
→ duplicate prevention
→ CSV storage
→ PostgreSQL storage
```

### Monthly Sales Reporting Workflow

```text
Sales CSV
→ PostgreSQL import
→ SQL aggregation
→ hospital-level summaries
→ email generation
→ Gmail API delivery
```

The original CSV workflow remains available while PostgreSQL provides persistent storage, database-level constraints, and SQL-based reporting.

## Features

* Extract text from hearing clinic PDF charts
* Parse chart text into structured data using the OpenAI API
* Save parsed records to CSV and PostgreSQL
* Prevent duplicate parsed records using `chart_no`
* Prevent duplicate sales imports using `record_id`
* Process multiple PDF files in batch
* Import sales records from CSV into PostgreSQL
* Calculate reporting totals using SQL
* Generate hospital-level summaries with `GROUP BY`
* Calculate total sales, repair fees, and revenue
* Build monthly sales email content
* Preview generated reports in the terminal
* Authenticate with Google using OAuth 2.0
* Send reports through the Gmail API
* Schedule reporting workflows with APScheduler
* Load sensitive configuration from environment variables
* Log successful operations, duplicates, and error tracebacks
* Run automated tests with `pytest`

## Architecture

```text
PDF Processing

PDF
→ pdf_reader.py
→ openai_parser.py
→ csv_writer.py
→ database.py
```

```text
Database Reporting

clinic_sales_records.csv
→ database.py
→ PostgreSQL
→ SQL COUNT / SUM / GROUP BY
→ email_reporter.py
→ email_sender.py
```

The reporting and email formatting logic is shared between CSV-backed and PostgreSQL-backed workflows.

## Project Structure

```text
hearing-clinic-automation-python/

├── app/
│   ├── __init__.py
│   ├── pdf_reader.py
│   ├── openai_parser.py
│   ├── csv_writer.py
│   ├── database.py
│   ├── batch_processor.py
│   ├── email_reporter.py
│   ├── email_sender.py
│   ├── report_scheduler.py
│   ├── config.py
│   └── logger.py
│
├── database/
│   └── schema.sql
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
├── logs/
├── .gitignore
├── requirements.txt
└── README.md
```

Local configuration files, OAuth credentials, tokens, and generated logs are excluded from Git.

## Tech Stack

* Python
* PostgreSQL
* SQL
* psycopg
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
* Git and GitHub

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The project uses psycopg as the PostgreSQL driver:

```text
psycopg[binary]==3.3.4
```

### 3. Create the environment file

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
REPORT_RECIPIENT_EMAIL=recipient@example.com

DB_HOST=localhost
DB_PORT=5432
DB_NAME=hearing_clinic
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

The `.env` file must not be committed.

Make sure `.gitignore` includes:

```gitignore
.env
.venv/
credentials.json
token.json
logs/
__pycache__/
.pytest_cache/
```

## PostgreSQL Setup

### 1. Create the database

Open PostgreSQL SQL Shell and run:

```sql
CREATE DATABASE hearing_clinic;
```

Connect to the database:

```sql
\c hearing_clinic
```

### 2. Initialize the schema

From PostgreSQL SQL Shell:

```sql
\i 'D:/hearing-clinic-automation-python/database/schema.sql'
```

Replace the path if the project is stored elsewhere.

The schema creates:

```text
parsed_records
sales_records
```

Confirm the tables:

```sql
\dt
```

Inspect their structure:

```sql
\d parsed_records
```

```sql
\d sales_records
```

### Database Constraints

`parsed_records.chart_no` uses a unique constraint:

```sql
UNIQUE (chart_no)
```

`sales_records.record_id` also uses a unique constraint:

```sql
UNIQUE (record_id)
```

These constraints prevent duplicates at the database level even if an application-level duplicate check fails.

Money values use PostgreSQL `NUMERIC(12, 2)` rather than floating-point storage:

```sql
sale_price_nzd NUMERIC(12, 2)
repair_fee_nzd NUMERIC(12, 2)
total_amount NUMERIC(12, 2)
```

This provides exact decimal storage for monetary values.

## Gmail API Setup

To enable Gmail delivery:

1. Enable the Gmail API in Google Cloud.
2. Configure the OAuth consent screen.
3. Create an OAuth Client ID using the `Desktop app` type.
4. Download the OAuth JSON file.
5. Rename it to `credentials.json`.
6. Place it in the project root.

The first Gmail execution opens a browser for authentication.

After authorization, the application creates:

```text
token.json
```

The token is reused for later executions and must not be committed.

## Usage

Run all commands from the project root.

### Process a Single PDF

```bash
python -m app.openai_parser data/sample_pdfs/sample_001.pdf
```

This workflow:

```text
extracts PDF text
→ sends the text to the OpenAI API
→ returns structured data
→ checks for duplicates
→ saves the result
```

### Process Multiple PDFs

```bash
python -m app.batch_processor data/sample_pdfs
```

The batch processor keeps the CSV and PostgreSQL save paths independent.

Example output:

```text
Processing: data\sample_pdfs\sample_001.pdf
CSV duplicate. Skipping CSV save.
Saved to PostgreSQL.
```

When the record already exists in both locations:

```text
Processing: data\sample_pdfs\sample_001.pdf
CSV duplicate. Skipping CSV save.
PostgreSQL duplicate. Skipping DB save.
```

### Import Sales CSV into PostgreSQL

```bash
python -c "from app.database import import_sales_records; print(import_sales_records('data/clinic_sales_records.csv'))"
```

The function returns:

```text
(saved_count, duplicate_count)
```

Example:

```text
(95, 1)
```

Running the same import again safely skips existing rows because `record_id` is unique.

### Generate a CSV-Based Monthly Report

```bash
python -m app.email_reporter data/clinic_sales_records.csv
```

This original workflow:

```text
reads the CSV
→ calculates totals in Python
→ creates hospital summaries
→ builds the email
→ sends it through Gmail
```

### Preview a PostgreSQL-Based Report

```bash
python -c "from app.email_reporter import calculate_db_sales_summary, build_monthly_sales_email; summary=calculate_db_sales_summary(); subject, body=build_monthly_sales_email(summary); print(subject); print(body)"
```

### Send a PostgreSQL-Based Monthly Report

```bash
python -c "from app.email_reporter import send_monthly_db_report; send_monthly_db_report()"
```

The PostgreSQL report calculates the main business metrics in SQL:

```sql
COUNT(*)
SUM(sale_price_nzd)
SUM(repair_fee_nzd)
SUM(sale_price_nzd + repair_fee_nzd)
GROUP BY hospital_id
```

Example report:

```text
Total records: 96
Total sales: NZD 243,700.00
Total repair fees: NZD 3,880.00
Total revenue: NZD 247,580.00

Hospital Summary:
- H-001 | Records: 32 | Sales: NZD 90,600.00 | Repairs: NZD 1,400.00 | Revenue: NZD 92,000.00
- H-002 | Records: 32 | Sales: NZD 74,900.00 | Repairs: NZD 1,280.00 | Revenue: NZD 76,180.00
- H-003 | Records: 32 | Sales: NZD 78,200.00 | Repairs: NZD 1,200.00 | Revenue: NZD 79,400.00
```

## Report Scheduler

Development mode:

```bash
python -m app.report_scheduler dev
```

Development mode runs the reporting job once after five seconds.

Monthly mode:

```bash
python -m app.report_scheduler monthly
```

Monthly mode sends the scheduled report at 5:30 PM on the last day of each month.

Stop the scheduler with:

```text
Ctrl + C
```

## Database Verification

Check the number of parsed records:

```sql
SELECT COUNT(*) FROM parsed_records;
```

Check the number of sales records:

```sql
SELECT COUNT(*) FROM sales_records;
```

Check the overall sales summary:

```sql
SELECT
    COUNT(*) AS total_records,
    SUM(sale_price_nzd) AS total_sales,
    SUM(repair_fee_nzd) AS total_repair_fees,
    SUM(sale_price_nzd + repair_fee_nzd) AS total_revenue
FROM sales_records;
```

Check hospital-level summaries:

```sql
SELECT
    hospital_id,
    COUNT(*) AS total_records,
    SUM(sale_price_nzd) AS total_sales,
    SUM(repair_fee_nzd) AS total_repair_fees,
    SUM(sale_price_nzd + repair_fee_nzd) AS total_revenue
FROM sales_records
GROUP BY hospital_id
ORDER BY hospital_id;
```

## Logging and Error Handling

Application logs are saved to:

```text
logs/app.log
```

Database operations log:

* successful record inserts
* duplicate parsed records
* duplicate sales records
* completed CSV imports
* completed SQL reporting queries
* unexpected errors and tracebacks

Database passwords are never written to the logs.

Insert operations use transactions:

```text
successful insert
→ commit

failed insert
→ rollback

success or failure
→ close connection
```

Parameterized SQL queries keep SQL statements separate from record values:

```python
cursor.execute(query, values)
```

This prevents user-provided values from being interpreted as SQL syntax.

## Automated Tests

The project uses `pytest` for reporting calculations and duplicate-prevention behavior.

Run all tests:

```bash
python -m pytest
```

Run detailed tests:

```bash
python -m pytest -v
```

The current test suite covers:

* total record counts
* total sales
* total repair fees
* total revenue
* hospital-level summaries
* email subject and body generation
* empty sales records
* invalid numeric input
* duplicate parsed records
* non-duplicate parsed records
* missing CSV files

CSV-related tests use pytest's `tmp_path` fixture so tests do not modify real project data.

Current result:

```text
8 passed
```

## Main Modules

### Configuration and Infrastructure

* `app/config.py`: loads API, email, and PostgreSQL environment variables
* `app/logger.py`: configures terminal and file logging
* `app/database.py`: manages PostgreSQL connections, inserts, imports, transactions, and SQL reporting queries

### PDF Processing

* `app/pdf_reader.py`: extracts text from PDF files
* `app/openai_parser.py`: converts extracted text into structured records
* `app/csv_writer.py`: saves CSV records and performs CSV duplicate checks
* `app/batch_processor.py`: processes multiple PDFs and saves results to CSV and PostgreSQL

### Reporting and Delivery

* `app/email_reporter.py`: supports CSV-based and database-based reporting
* `app/email_sender.py`: authenticates with Gmail and sends messages
* `app/report_scheduler.py`: schedules development and monthly report jobs

## Storage Strategy

The first version of the project used CSV files as the primary storage layer.

PostgreSQL was added incrementally without immediately removing the working CSV implementation.

```text
CSV
→ original MVP storage and fallback

PostgreSQL
→ persistent storage
→ unique constraints
→ transaction handling
→ SQL aggregation
```

This migration strategy reduced the risk of breaking the existing workflow while the database implementation was being verified.

## Current Status

Completed:

* PDF text extraction
* OpenAI-based chart parsing
* CSV storage
* PostgreSQL storage
* Batch PDF processing
* Application-level duplicate checks
* Database-level duplicate constraints
* Sales CSV import
* SQL-based total calculations
* SQL `GROUP BY` hospital summaries
* CSV-based reporting
* PostgreSQL-based reporting
* Gmail OAuth authentication
* Gmail API email delivery
* APScheduler reporting jobs
* Environment-based configuration
* File and terminal logging
* Transaction commit and rollback
* Error tracebacks
* Automated pytest tests

## Future Improvements

* Add PostgreSQL integration tests using a dedicated test database
* Replace command-line one-liners with dedicated database CLI commands
* Add connection pooling
* Introduce repository classes if the persistence layer grows
* Update the scheduler to select CSV or PostgreSQL through configuration
* Add Docker support for the application and PostgreSQL
* Add GitHub Actions continuous integration
* Mock Gmail and OpenAI API calls in tests
* Add HTML email templates
* Improve retry handling for external API failures
* Add database migrations
* Add log rotation and retention
