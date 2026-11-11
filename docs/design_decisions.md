# Design Decisions

## 1. Technology Selection

### Python
Python was selected because it provides simple and effective tools for batch data processing.

### Pandas
Pandas is used to read CSV files, validate records, transform data, and prepare datasets for publishing.

### SQLite
SQLite was selected as a lightweight relational database. It does not require a separate database server and is suitable for this standalone batch pipeline.

### Pytest
Pytest is used to automate unit and integration tests.

## 2. Data Ingestion

Customer and order data are ingested from separate CSV files.

The ingestion layer checks:
- Whether the input file exists.
- Whether the CSV structure is readable.
- Whether required columns are present.
- Whether rows have the expected number of fields.

Malformed input files cause the pipeline to fail with an error instead of silently ignoring structural problems.

## 3. Validation Strategy

Validation is performed before transformation and publishing.

### Customer validation
- Customer ID must be present and unique.
- First name, last name, email, city, and creation date must be valid.
- Email must follow a basic email format check.

### Order validation
- Order ID must be present and unique.
- Customer ID must reference a valid customer.
- Order amount must be numeric and greater than zero.
- Order date must be valid.
- Order status must belong to the allowed status list.

The first occurrence of an identifier is retained for further validation. Later duplicate occurrences are rejected.

## 4. Rejected Record Handling

Invalid records are not silently discarded.

They are:
- Stored separately from accepted records.
- Exported to CSV files.
- Tagged with rejection reasons.
- Associated with the source filename and pipeline run ID.

This improves traceability and makes data-quality issues easier to investigate.

## 5. Transformation Strategy

Accepted records are standardized before publishing.

Examples:
- Customer names and cities are converted to title case.
- Email addresses are converted to lowercase.
- Order statuses are converted to uppercase.
- Date fields are converted to datetime values.
- Order amounts are converted to numeric values and rounded to two decimal places.

## 6. Publishing Strategy

SQLite is used to publish curated datasets.

The customer, order, and rejected-record tables are replaced with the latest execution's snapshot.

A separate `pipeline_runs` table stores execution history using a unique run ID. This keeps the latest data snapshot separate from historical execution information.

## 7. Idempotency

Repeated executions with the same input data produce the same curated snapshot instead of appending duplicate records.

Each execution receives a unique run ID, allowing multiple executions to be tracked independently.

## 8. Failure Handling and Logging

The pipeline uses structured logging to record:
- Pipeline start and completion.
- Records loaded.
- Accepted and rejected record counts.
- Reconciliation results.
- Execution duration.
- Failure details.

Failed executions are recorded in the `pipeline_runs` table with an error message before the error is raised again.

## 9. Data Reconciliation

The pipeline checks the following rule:

**Input Records = Accepted Records + Rejected Records**

Customer and order counts are checked independently. The pipeline proceeds to publishing only when both checks pass.

## 10. Testing Strategy

Automated tests cover:
- Valid CSV ingestion.
- Missing input files.
- Missing required columns.
- Empty CSV files.
- Malformed CSV rows.
- Valid customer and order records.
- Missing and duplicate customer IDs.
- Invalid order amounts.
- Orders referencing unknown customers.
- Empty customer datasets.
- Pipeline success and failure handling.
- Idempotent database publishing.
- Invalid customer email formats.
- Invalid order statuses.
- Null customer IDs.
- Null order amounts.

## 11. Current Limitations

- SQLite is suitable for this standalone demonstration but may not be ideal for concurrent, large-scale production workloads.
- Email validation uses a basic format check and does not verify whether an address actually exists.
- The pipeline currently uses full snapshot replacement instead of incremental database updates.
- The input datasets are CSV-based and do not currently support streaming ingestion.
- Publishing uses Pandas `to_sql()` with a SQLite connection. If publishing fails midway, a partial database update may occur because rollback of inserted records is not guaranteed.

## Large-Scale Performance Testing

The pipeline was tested using 100,000 generated customer records and 100,000 generated order records, with one intentional duplicate in each dataset.

### Results

| Metric | Customers | Orders |
|---|---:|---:|
| Input records | 100,001 | 100,001 |
| Accepted records | 99,899 | 99,610 |
| Rejected records | 102 | 391 |
| Reconciliation | PASSED | PASSED |

### Performance Observations

- Total execution time: 33.16 seconds.
- Pipeline completed with SUCCESS status.
- All accepted records were published to SQLite.
- Rejected records were stored separately.
- Database counts matched the pipeline reconciliation report.
- The original 10K input dataset was preserved.

### Scalability Consideration

The data generator supports configurable customer and order counts. This allows testing with different dataset sizes without changing the pipeline implementation.


## 12. Pipeline Architecture

The batch pipeline follows a modular, sequential workflow:

```text
Customer CSV + Order CSV
          |
          v
    Data Ingestion
          |
          v
    Data Validation
          |
       +--+--+
       |     |
       v     v
   Accepted Rejected
       |     |
       v     v
 Data       Rejection
Transformation CSV Export
       |
       v
 SQLite Publishing
       |
       v
 Curated Tables
       |
       v
 Run Reports and Logs
```

### Workflow Description

1. Customer and order CSV files are loaded from the input directory.
2. Structural checks ensure that the input files are readable and contain the required columns.
3. Validation separates valid records from invalid records.
4. Accepted records are standardized through transformation.
5. Rejected records are exported separately with rejection reasons.
6. Accepted and rejected datasets are published to SQLite.
7. Execution details, record counts, reconciliation results, and status are stored in reports and logs.
