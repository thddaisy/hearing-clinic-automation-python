# Hearing Clinic Automation (Python)

Python implementation of the Hearing Clinic Automation workflow.

## PDF Reader

The PDF Reader is the first feature of this project.

It reads a PDF file, extracts text from all pages, and prints the extracted text in the terminal.

This feature is the foundation for the next steps of the automation pipeline:

```text
PDF file
→ text extraction
→ OpenAI parsing
→ CSV or database storage
→ reporting or automation
```

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

### What I Learned

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

### Next Steps

The next feature will connect the extracted PDF text to the OpenAI API and convert it into structured data.

Planned next step:

```text
PDF text
→ OpenAI Parser
→ structured JSON-like data
```
