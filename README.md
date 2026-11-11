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
- Configurable input directory for large-scale testing.
- Support for 100K customer and order datasets.

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
│   ├── input_100k/
│   ├── output/
│   └── rejected/
│
├── src/
│   ├── __init__.py
│   ├── generate_data.py
│   ├── ingestion.py
│   ├── validation.py
│   ├── transformation.py
│   ├── publishing.py
│   ├── pipeline.py
│   └── logger.py
│
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_validation.py
│   ├── test_pipeline.py
│   └── test_publishing.py
│
├── docs/
│   ├── data_dictionary.md
│   └── design_decisions.md
│
├── prompt_history/
│   └── ai_prompts.md
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/charith614/yottaflex-batch-data-pipeline.git
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

## Input Data Generation

The project includes a reproducible synthetic data generator.

Run:

```bash
python src/generate_data.py
```

This generates 100,000 customers and 100,000 orders, including intentional duplicate records, in:

- `data/input_100k/customers.csv`
- `data/input_100k/orders.csv`

The original 10K sample dataset is maintained separately in `data/input/`.

The generator uses a fixed random seed to support reproducible testing.

## Run the Pipeline

To execute the pipeline using the original input dataset:

```bash
python main.py
```

The pipeline performs:

1. CSV ingestion.
2. Schema and business-rule validation.
3. Data transformation.
4. Rejected-record handling.
5. Data reconciliation.
6. SQLite database publishing.
7. Execution reporting and logging.

## Run the 100K Data Processing Test

After generating the large-scale dataset, execute:

```bash
python -c "from src.pipeline import run_pipeline; run_pipeline('data/input_100k')"
```

The pipeline supports a configurable input directory, allowing different datasets to be processed without changing the core implementation.

## Run Automated Tests

Execute all automated tests:

```bash
python -m pytest -v
```

The project contains **19 automated tests** covering:

- Valid and invalid CSV ingestion.
- Missing files and required columns.
- Empty and malformed CSV files.
- Valid customer records.
- Missing and duplicate customer IDs.
- Null customer IDs.
- Invalid customer email addresses.
- Invalid order amounts.
- Null order amounts.
- Unknown customer references.
- Invalid order statuses.
- Empty customer datasets.
- Pipeline success and failure handling.
- Idempotent database publishing.

**Latest test result: 19 passed.**

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

```text
Input Records = Accepted Records + Rejected Records
```

Reconciliation is performed separately for customers and orders.

If the record counts do not balance, the pipeline reports a failure.

## Database Tables

The SQLite warehouse contains five tables:

- `customers` – validated and transformed customer records.
- `orders` – validated and transformed order records.
- `rejected_customers` – rejected customer records and rejection reasons.
- `rejected_orders` – rejected order records and rejection reasons.
- `pipeline_runs` – execution history, status, record counts, duration, and error details.

## Design Considerations

- Invalid records are separated instead of silently discarded.
- Duplicate identifiers are rejected.
- Orders referencing invalid or unknown customers are rejected.
- Each execution receives a unique run ID.
- Curated tables represent the latest processed data snapshot.
- Pipeline execution history is maintained separately.
- Reconciliation checks help ensure record-count consistency.
- Large-scale testing uses a separate input directory.
- Generated output files and large test datasets are excluded from version control.

Additional design decisions and trade-offs are documented in `docs/design_decisions.md`.

## AI Assistance Disclosure

AI tools were used as development assistance for understanding requirements, exploring implementation approaches, debugging, writing tests, and improving documentation.

The candidate reviewed and validated the implementation, test results, and final outputs and is responsible for understanding and explaining the project's design decisions.

AI assistance and relevant prompts are documented in `prompt_history/ai_prompts.md`.

## Large-Scale Data Processing Test (100K)

The pipeline was tested with 100,000 generated customers and 100,000 generated orders, plus one intentional duplicate record in each dataset.

### Test Results

| Metric | Customers | Orders |
|---|---:|---:|
| Input records | 100,001 | 100,001 |
| Accepted records | 99,899 | 99,610 |
| Rejected records | 102 | 391 |
| Reconciliation | PASSED | PASSED |

### Performance

- Total execution time: 33.16 seconds.
- Pipeline status: SUCCESS.
- Database: SQLite.
- Reconciliation status: PASSED.
- Generated dataset: 100K customers and 100K orders.

### Verification

- All five SQLite tables verified.
- Database record counts matched the pipeline report.
- All 19 automated tests passed.
- Original 10K input dataset preserved.
- Large-scale dataset generated separately using a fixed random seed.
- Rejected records exported successfully.

---

**Repository:** [YottaFlex Batch Data Pipeline](https://github.com/charith614/yottaflex-batch-data-pipeline)