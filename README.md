# YottaFlex Batch Data Pipeline

## Project Overview

This project implements a batch data processing pipeline using Python and Pandas. It ingests customer and order CSV files, validates records, transforms valid data, rejects invalid records, and publishes curated data into a SQLite database.

The pipeline also generates execution reports, maintains run history, and performs data reconciliation.

## Features

- CSV ingestion for customer and order data.
- Required-column and malformed CSV validation.
- Customer and order business-rule validation.
- Duplicate record detection.
- Handling of missing values and invalid records.
- Rejected-record exports with rejection reasons.
- Data transformation and standardization.
- SQLite database publishing.
- Pipeline execution tracking with unique run IDs.
- Success and failure status logging.
- Data reconciliation checks.
- JSON execution reports.
- Automated tests using Pytest.
- Reproducible synthetic dataset generation.

## Technology Stack

- Python 3
- Pandas
- SQLite
- Pytest
- CSV
- JSON
- Git

## Project Structure

```text
yottaflex-batch-data-pipeline/
│
├── data/
│   ├── input/
│   ├── output/
│   └── rejected/
│
├── src/
│   ├── generate_data.py
│   ├── ingestion.py
│   ├── validation.py
│   ├── transformation.py
│   ├── publishing.py
│   ├── pipeline.py
│   └── logger.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_validation.py
│   ├── test_pipeline.py
│   └── test_publishing.py
│
├── docs/
├── prompt_history/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd yottaflex-batch-data-pipeline
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

For macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Generate Input Data

Generate the synthetic customer and order datasets:

```bash
python src/generate_data.py
```

The generated CSV files are stored in:

- `data/input/customers.csv`
- `data/input/orders.csv`

## Run the Pipeline

Execute the complete batch pipeline:

```bash
python main.py
```

The pipeline performs ingestion, validation, transformation, rejection handling, reconciliation, and database publishing.

## Run Automated Tests

Execute all tests:

```bash
python -m pytest -v
```

## Output Locations

| Output | Location |
|---|---|
| SQLite database | `data/output/warehouse.db` |
| Latest execution report | `data/output/run_report.json` |
| Individual run reports | `data/output/run_report_<run_id>.json` |
| Rejected customers | `data/rejected/rejected_customers.csv` |
| Rejected orders | `data/rejected/rejected_orders.csv` |
| Pipeline logs | `logs/pipeline.log` |

## Data Reconciliation

The pipeline verifies that:

`Input Records = Accepted Records + Rejected Records`

Reconciliation is performed separately for customers and orders. If the counts do not balance, the pipeline reports a failure.

## Database Tables

The SQLite warehouse contains:

- `customers` – validated and transformed customer records.
- `orders` – validated and transformed order records.
- `rejected_customers` – rejected customer records and reasons.
- `rejected_orders` – rejected order records and reasons.
- `pipeline_runs` – execution history, status, record counts, duration, and error details.

## Design Considerations

- Invalid records are separated instead of silently discarded.
- Duplicate identifiers are rejected.
- Orders referencing invalid or unknown customers are rejected.
- Each execution receives a unique run ID.
- Curated tables represent the latest successful data snapshot.
- Pipeline execution history is maintained separately.
- Reconciliation checks help ensure record-count consistency.

## AI Assistance Disclosure

AI tools were used as development assistance for understanding requirements, exploring implementation approaches, debugging, and improving documentation.

The project code, implementation decisions, test results, and final outputs were reviewed and validated by the candidate. The candidate is responsible for explaining the implementation and its design decisions.