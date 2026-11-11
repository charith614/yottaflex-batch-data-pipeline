
import pandas as pd

from src.validation import validate_customers, validate_orders


def test_valid_customer():
    df = pd.DataFrame([
        {
            "customer_id": "C001",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "email": "ravi@example.com",
            "city": "Hyderabad",
            "created_at": "2026-10-01T09:00:00"
        }
    ])

    valid, rejected = validate_customers(df)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_missing_customer_id():
    df = pd.DataFrame([
        {
            "customer_id": "",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "email": "ravi@example.com",
            "city": "Hyderabad",
            "created_at": "2026-10-01T09:00:00"
        }
    ])

    valid, rejected = validate_customers(df)

    assert len(valid) == 0
    assert len(rejected) == 1


def test_duplicate_customer_id():
    df = pd.DataFrame([
        {
            "customer_id": "C001",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "email": "ravi@example.com",
            "city": "Hyderabad",
            "created_at": "2026-10-01T09:00:00"
        },
        {
            "customer_id": "C001",
            "first_name": "Sita",
            "last_name": "Reddy",
            "email": "sita@example.com",
            "city": "Chennai",
            "created_at": "2026-10-02T09:00:00"
        }
    ])

    valid, rejected = validate_customers(df)

    assert len(valid) == 1
    assert len(rejected) == 1


def test_invalid_order_amount():
    df = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "2026-10-01T10:00:00",
            "amount": -100,
            "status": "COMPLETED"
        }
    ])

    valid, rejected = validate_orders(df, {"C001"})

    assert len(valid) == 0
    assert len(rejected) == 1


def test_unknown_customer_order():
    df = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C999",
            "order_date": "2026-10-01T10:00:00",
            "amount": 500,
            "status": "COMPLETED"
        }
    ])

    valid, rejected = validate_orders(df, {"C001"})

    assert len(valid) == 0
    assert len(rejected) == 1


def test_empty_customer_data():
    df = pd.DataFrame(columns=[
        "customer_id", "first_name", "last_name",
        "email", "city", "created_at"
    ])

    valid, rejected = validate_customers(df)

    assert len(valid) == 0
    assert len(rejected) == 0

def test_invalid_customer_email():
    df = pd.DataFrame([
        {
            "customer_id": "C002",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "email": "invalid-email",
            "city": "Hyderabad",
            "created_at": "2026-10-01T09:00:00"
        }
    ])

    valid, rejected = validate_customers(df)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid email format" in rejected.iloc[0]["rejection_reason"]


def test_invalid_order_status():
    df = pd.DataFrame([
        {
            "order_id": "O002",
            "customer_id": "C001",
            "order_date": "2026-10-01T10:00:00",
            "amount": 500,
            "status": "PROCESSING"
        }
    ])

    valid, rejected = validate_orders(df, {"C001"})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid order status" in rejected.iloc[0]["rejection_reason"]
