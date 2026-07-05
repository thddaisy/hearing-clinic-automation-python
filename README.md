# Hearing Clinic Automation (Python)

Python implementation of the Hearing Clinic Automation workflow.

This project rebuilds an existing n8n automation workflow in Python, step by step, to process hearing clinic PDF documents and convert them into structured data.

## Project Pipeline

The current automation pipeline is:

```text
PDF file
→ text extraction
→ OpenAI parsing
→ structured data
→ CSV or database storage
→ reporting or automation
```

## PDF Reader

The PDF Reader is the first feature of this project.

It reads a PDF file, extracts text from all pages, and prints the extracted text in the terminal.

This feature is the foundation for the next steps of the automation pipeline.

### Current Features

* Reads a PDF file from a terminal argument
* Extracts text from all pages
* Skips empty pages or pages without extractable text
* Checks whether the input path exists
* Checks whether the input path is a file
* Checks whether the file extension is `.pdf`
* Prints the extracted text in the terminal

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

The OpenAI Parser is the second feature of this project.

It takes extracted text from a hearing clinic PDF and sends it to the OpenAI API.

The response is returned as structured JSON-like data and converted into a Python dictionary.

This feature connects the PDF Reader to the next stage of the automation pipeline:

```text
PDF file
→ text extraction
→ OpenAI parsing
→ structured data
→ CSV or database storage
→ reporting or automation
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

### OpenAI Parser Error Handling

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

## What I Learned

While building the PDF Reader, I learned and practiced:

* How to use `pypdf` to read PDF files
* The difference between installing a package and importing it
* How to use `pathlib.Path` for file paths
* How to use `sys.argv` to receive terminal arguments
* How to check whether a file exists with `Path.exists()`
* How to check whether a path is a file with `Path.is_file()`
* How to check file extensions with `Path.suffix`
* How to handle `None` values from `extract_text()`
* How `if text:` works with truthy and falsy values
* How `return` sends a result back from a function
* How to separate reusable function logic from script execution logic

While building the OpenAI Parser, I learned and practiced:

* How to load environment variables from a `.env` file
* Why API keys should not be hardcoded in source code
* How to create an OpenAI client
* How to send extracted PDF text to the OpenAI API
* How to design a prompt for structured JSON output
* Why prompts should prevent guessing or inferred values
* How markdown code fences can break `json.loads()`
* How to convert a JSON string into a Python dictionary
* How to connect functions from different files using imports
* How to run a module with `python -m app.openai_parser`

## Next Steps

The PDF Reader and OpenAI Parser are now connected.

The next planned steps are:

```text
structured data
→ CSV export or PostgreSQL storage
→ automated reporting
→ Google API integration
```

Planned features:

* Refactor the script execution flow into a dedicated `main()` function
* Add better error handling for invalid OpenAI JSON responses
* Save parsed data into a CSV file
* Design a PostgreSQL table for hearing clinic chart records
* Insert parsed records into PostgreSQL
* Add logging for successful and failed processing