
import pandas as pd


def transform_customers(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["first_name"] = df["first_name"].astype(str).str.strip().str.title()
    df["last_name"] = df["last_name"].astype(str).str.strip().str.title()
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["city"] = df["city"].astype(str).str.strip().str.title()

    df["created_at"] = pd.to_datetime(
        df["created_at"], errors="coerce"
    )

    return df


def transform_orders(df):
    df = df.copy()

    df["order_id"] = df["order_id"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()

    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"], errors="coerce"
    ).round(2)

    df["status"] = df["status"].astype(str).str.strip().str.upper()

    return df
