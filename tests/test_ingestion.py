
import pandas as pd
import pytest

from src.ingestion import load_csv, load_customers, load_orders


def test_load_valid_csv(tmp_path):
    file = tmp_path / "customers.csv"
    file.write_text(
        "customer_id,first_name,last_name,email,city,created_at\n"
        "C001,Ravi,Kumar,ravi@example.com,Hyderabad,2026-10-01\n"
    )
    df = load_customers(file)
    assert len(df) == 1
    assert df.iloc[0]["customer_id"] == "C001"


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_customers("missing_customers.csv")


def test_missing_required_column(tmp_path):
    file = tmp_path / "customers.csv"
    file.write_text("customer_id,first_name\nC001,Ravi\n")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_customers(file)


def test_empty_csv_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(file, ["customer_id"])


def test_malformed_csv(tmp_path):
    file = tmp_path / "malformed.csv"
    file.write_text(
        "customer_id,first_name\n"
        "C001,Ravi,ExtraValue\n"
    )
    with pytest.raises(pd.errors.ParserError):
        load_csv(file, ["customer_id", "first_name"])


def test_load_valid_orders(tmp_path):
    file = tmp_path / "orders.csv"
    file.write_text(
        "order_id,customer_id,order_date,amount,status\n"
        "O001,C001,2026-10-01,500,COMPLETED\n"
    )
    df = load_orders(file)
    assert len(df) == 1
    assert df.iloc[0]["order_id"] == "O001"


