
import csv
import pandas as pd
from pathlib import Path

REQUIRED_CUSTOMER_COLUMNS = [
    "customer_id", "first_name", "last_name",
    "email", "city", "created_at"
]

REQUIRED_ORDER_COLUMNS = [
    "order_id", "customer_id", "order_date", "amount", "status"
]


def load_csv(file_path, required_columns):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file, strict=True)
            header = next(reader, None)

            if header is not None:
                for line_number, row in enumerate(reader, start=2):
                    if not row:
                        continue

                    if len(row) != len(header):
                        raise pd.errors.ParserError(
                            f"Malformed CSV row at line {line_number}: "
                            f"expected {len(header)} fields, found {len(row)}"
                        )

    except csv.Error as error:
        raise pd.errors.ParserError(
            f"Malformed CSV file: {error}"
        ) from error

    df = pd.read_csv(path)

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns in {path.name}: {missing_columns}"
        )

    return df


def load_customers(file_path="data/input/customers.csv"):
    return load_csv(file_path, REQUIRED_CUSTOMER_COLUMNS)


def load_orders(file_path="data/input/orders.csv"):
    return load_csv(file_path, REQUIRED_ORDER_COLUMNS)

