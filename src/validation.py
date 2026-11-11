
import pandas as pd


def validate_customers(
    df,
    source_file="customers.csv",
    run_id=None
):
    df = df.copy()
    df["_source_row"] = range(2, len(df) + 2)

    valid_indices = []
    rejected_records = []
    seen_ids = set()

    for index, row in df.iterrows():
        errors = []
        customer_id = row["customer_id"]

        if pd.isna(customer_id) or str(customer_id).strip() == "":
            errors.append("Missing customer ID")
        elif customer_id in seen_ids:
            errors.append("Duplicate customer ID")
        else:
            seen_ids.add(customer_id)

        for column in [
            "first_name", "last_name", "city", "email", "created_at"
        ]:
            if pd.isna(row[column]) or str(row[column]).strip() == "":
                errors.append(f"Missing {column}")

        email = str(row["email"])

        if not pd.isna(row["email"]) and (
            "@" not in email or "." not in email.split("@")[-1]
        ):
            errors.append("Invalid email format")

        if pd.isna(pd.to_datetime(row["created_at"], errors="coerce")):
            errors.append("Invalid customer creation date")

        if errors:
            record = row.to_dict()
            record["rejection_reason"] = "; ".join(errors)
            record["source_file"] = source_file
            record["run_id"] = run_id
            rejected_records.append(record)
        else:
            valid_indices.append(index)

    valid_df = df.loc[valid_indices].copy()
    rejected_df = pd.DataFrame(rejected_records)

    return valid_df, rejected_df


def validate_orders(
    df,
    valid_customer_ids,
    source_file="orders.csv",
    run_id=None
):
    df = df.copy()
    df["_source_row"] = range(2, len(df) + 2)

    valid_indices = []
    rejected_records = []
    seen_ids = set()

    allowed_statuses = {"COMPLETED", "PENDING", "CANCELLED"}

    for index, row in df.iterrows():
        errors = []

        order_id = row["order_id"]
        customer_id = row["customer_id"]

        if pd.isna(order_id) or str(order_id).strip() == "":
            errors.append("Missing order ID")
        elif order_id in seen_ids:
            errors.append("Duplicate order ID")
        else:
            seen_ids.add(order_id)

        if pd.isna(customer_id) or str(customer_id).strip() == "":
            errors.append("Missing customer ID")
        elif customer_id not in valid_customer_ids:
            errors.append("Unknown or invalid customer ID")

        amount = pd.to_numeric(row["amount"], errors="coerce")

        if pd.isna(amount):
            errors.append("Invalid order amount")
        elif amount <= 0:
            errors.append("Order amount must be greater than zero")

        order_date = pd.to_datetime(row["order_date"], errors="coerce")

        if pd.isna(order_date):
            errors.append("Invalid order date")

        status = str(row["status"]).strip().upper()

        if status not in allowed_statuses:
            errors.append("Invalid order status")

        if errors:
            record = row.to_dict()
            record["rejection_reason"] = "; ".join(errors)
            record["source_file"] = source_file
            record["run_id"] = run_id
            rejected_records.append(record)
        else:
            valid_indices.append(index)

    valid_df = df.loc[valid_indices].copy()
    rejected_df = pd.DataFrame(rejected_records)

    return valid_df, rejected_df
