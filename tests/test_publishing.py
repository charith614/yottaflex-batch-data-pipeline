
import sqlite3
import pandas as pd

from src import publishing


def test_publishing_is_idempotent(monkeypatch, tmp_path):
    # Use a separate temporary database for this test.
    test_db = tmp_path / "test_warehouse.db"

    monkeypatch.setattr(
        publishing, "DB_PATH", str(test_db)
    )

    customers = pd.DataFrame([
        {
            "customer_id": "C001",
            "first_name": "Ravi",
            "last_name": "Kumar",
            "email": "ravi@example.com"
        },
        {
            "customer_id": "C002",
            "first_name": "Priya",
            "last_name": "Reddy",
            "email": "priya@example.com"
        }
    ])

    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "amount": 500
        },
        {
            "order_id": "O002",
            "customer_id": "C002",
            "amount": 700
        }
    ])

    rejected_customers = pd.DataFrame([
        {
            "customer_id": "C003",
            "rejection_reason": "Invalid email"
        }
    ])

    rejected_orders = pd.DataFrame([
        {
            "order_id": "O003",
            "rejection_reason": "Invalid amount"
        }
    ])

    # First pipeline publishing run.
    publishing.publish_data(
        customers,
        orders,
        rejected_customers,
        rejected_orders,
        run_id="RUN001",
        status="SUCCESS"
    )

    # Second pipeline publishing run with the same data.
    publishing.publish_data(
        customers,
        orders,
        rejected_customers,
        rejected_orders,
        run_id="RUN002",
        status="SUCCESS"
    )

    connection = sqlite3.connect(test_db)

    try:
        customer_count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        order_count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        rejected_customer_count = connection.execute(
            "SELECT COUNT(*) FROM rejected_customers"
        ).fetchone()[0]

        rejected_order_count = connection.execute(
            "SELECT COUNT(*) FROM rejected_orders"
        ).fetchone()[0]

        run_count = connection.execute(
            "SELECT COUNT(*) FROM pipeline_runs"
        ).fetchone()[0]

    finally:
        connection.close()

    assert customer_count == 2
    assert order_count == 2
    assert rejected_customer_count == 1
    assert rejected_order_count == 1
    assert run_count == 2
