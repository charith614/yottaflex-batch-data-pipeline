# Data Dictionary

## 1. Customers Dataset

**Source file:** `data/input/customers.csv`

| Column | Data Type | Description | Validation |
|---|---|---|---|
| customer_id | String | Unique customer identifier | Required and unique |
| first_name | String | Customer first name | Cannot be empty |
| last_name | String | Customer last name | Cannot be empty |
| email | String | Customer email address | Must have a valid basic email format |
| city | String | Customer city | Cannot be empty |
| created_at | Date/Datetime | Customer creation date | Must be a valid date |

## 2. Orders Dataset

**Source file:** `data/input/orders.csv`

| Column | Data Type | Description | Validation |
|---|---|---|---|
| order_id | String | Unique order identifier | Required and unique |
| customer_id | String | Customer associated with the order | Required and must reference a valid customer |
| order_date | Date/Datetime | Date when the order was placed | Must be a valid date |
| amount | Numeric | Order transaction amount | Must be numeric and greater than zero |
| status | String | Current order status | COMPLETED, PENDING, or CANCELLED |

## 3. Rejected Records

Rejected records are exported separately to the `data/rejected/` directory.

Additional metadata fields:

| Column | Description |
|---|---|
| rejection_reason | Explains why the record was rejected |
| source_file | Original input CSV filename |
| run_id | Unique identifier of the pipeline execution |

The validation process may assign multiple rejection reasons to one record.

## 4. SQLite Warehouse Tables

**Database:** `data/output/warehouse.db`

| Table | Description |
|---|---|
| customers | Validated and transformed customer records |
| orders | Validated and transformed order records |
| rejected_customers | Rejected customer records |
| rejected_orders | Rejected order records |
| pipeline_runs | Pipeline execution history and status |

## 5. Pipeline Run History

The `pipeline_runs` table contains:

| Column | Description |
|---|---|
| run_id | Unique execution identifier |
| status | SUCCESS or FAILED |
| started_at | Pipeline start timestamp |
| completed_at | Pipeline completion timestamp |
| customer_count | Number of accepted customers for successful runs |
| order_count | Number of accepted orders for successful runs |
| rejected_customer_count | Number of rejected customers for successful runs |
| rejected_order_count | Number of rejected orders for successful runs |
| duration_seconds | Total execution duration |
| error_message | Error details when execution fails |

## 6. Reconciliation Rules

For each dataset:

**Input Records = Accepted Records + Rejected Records**

The pipeline checks this condition separately for customers and orders. A reconciliation failure causes the pipeline to fail rather than silently publishing unbalanced results.