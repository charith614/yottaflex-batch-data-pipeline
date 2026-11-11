# AI Prompt History

## Purpose

AI assistance was used during the development of the YottaFlex Batch Data Pipeline challenge to understand requirements, explore implementation approaches, troubleshoot errors, and improve documentation.

## Prompts and Assistance Areas

### 1. Project Planning
**Prompt topic:** How to structure a Python batch data pipeline project.

**Assistance received:**
- Understanding the challenge requirements.
- Planning project folders and modules.
- Separating ingestion, validation, transformation, and publishing responsibilities.

### 2. Environment Setup
**Prompt topic:** Setting up the Python project in VS Code on macOS.

**Assistance received:**
- Creating and activating a virtual environment.
- Installing Python dependencies.
- Organizing source code and test folders.

### 3. Synthetic Data Generation
**Prompt topic:** Generating reproducible customer and order CSV datasets.

**Assistance received:**
- Creating sample customer and order records.
- Introducing controlled invalid records and duplicate identifiers.
- Using a reproducible random seed.

### 4. CSV Ingestion
**Prompt topic:** Implementing CSV ingestion with structural checks.

**Assistance received:**
- Checking input file existence.
- Checking required columns.
- Handling malformed CSV structures.

### 5. Data Validation
**Prompt topic:** Implementing customer and order validation rules.

**Assistance received:**
- Detecting missing identifiers.
- Detecting duplicate identifiers.
- Validating email formats, dates, amounts, and statuses.
- Checking customer references in orders.
- Separating accepted and rejected records.

### 6. Data Transformation
**Prompt topic:** Standardizing accepted customer and order records.

**Assistance received:**
- Standardizing names, email addresses, and statuses.
- Converting dates and numeric values.

### 7. Database Publishing
**Prompt topic:** Publishing curated data into SQLite.

**Assistance received:**
- Creating database tables.
- Publishing accepted and rejected records.
- Maintaining pipeline execution history.
- Handling failed execution records.

### 8. Logging and Reporting
**Prompt topic:** Implementing pipeline logs and execution reports.

**Assistance received:**
- Generating unique run IDs.
- Tracking execution duration and status.
- Exporting rejected records.
- Creating JSON run reports.
- Implementing reconciliation checks.

### 9. Automated Testing
**Prompt topic:** Creating and debugging Pytest tests.

**Assistance received:**
- Testing ingestion and validation.
- Testing pipeline success and failure handling.
- Testing idempotent publishing.
- Troubleshooting test failures.

### 10. Documentation
**Prompt topic:** Preparing project documentation.

**Assistance received:**
- Creating the README.
- Documenting the data dictionary.
- Recording design decisions.
- Preparing this AI assistance disclosure.

## Candidate Review and Responsibility

AI-generated suggestions were used as development assistance. The candidate ran the project locally, reviewed the implementation, executed the pipeline, inspected generated outputs, and ran automated tests.

The candidate is responsible for understanding the final implementation and explaining its behavior, design decisions, limitations, and test results.