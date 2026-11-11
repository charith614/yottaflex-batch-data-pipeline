
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = "data/output/warehouse.db"


def get_connection():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def ensure_pipeline_runs_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            run_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            started_at TEXT,
            completed_at TEXT,
            customer_count INTEGER,
            order_count INTEGER,
            rejected_customer_count INTEGER,
            rejected_order_count INTEGER,
            duration_seconds REAL,
            error_message TEXT
        )
    """)

    # Add error_message to databases created by an older version.
    columns = [
        row[1]
        for row in connection.execute(
            "PRAGMA table_info(pipeline_runs)"
        ).fetchall()
    ]

    if "error_message" not in columns:
        connection.execute(
            "ALTER TABLE pipeline_runs ADD COLUMN error_message TEXT"
        )


def publish_data(
    customers,
    orders,
    rejected_customers,
    rejected_orders,
    run_id=None,
    status="SUCCESS",
    started_at=None,
    completed_at=None,
    duration_seconds=None
):
    connection = get_connection()

    try:
        # Replace the current snapshot tables.
        customers.to_sql(
            "customers", connection,
            if_exists="replace", index=False
        )

        orders.to_sql(
            "orders", connection,
            if_exists="replace", index=False
        )

        rejected_customers.to_sql(
            "rejected_customers", connection,
            if_exists="replace", index=False
        )

        rejected_orders.to_sql(
            "rejected_orders", connection,
            if_exists="replace", index=False
        )

        # Create or update the pipeline run history table.
        ensure_pipeline_runs_table(connection)

        if run_id is not None:
            connection.execute("""
                INSERT OR REPLACE INTO pipeline_runs (
                    run_id,
                    status,
                    started_at,
                    completed_at,
                    customer_count,
                    order_count,
                    rejected_customer_count,
                    rejected_order_count,
                    duration_seconds,
                    error_message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
            """, (
                run_id,
                status,
                started_at,
                completed_at,
                len(customers),
                len(orders),
                len(rejected_customers),
                len(rejected_orders),
                duration_seconds
            ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def record_failed_run(
    run_id,
    started_at,
    completed_at,
    duration_seconds,
    error_message
):
    connection = get_connection()

    try:
        ensure_pipeline_runs_table(connection)

        connection.execute("""
            INSERT OR REPLACE INTO pipeline_runs (
                run_id,
                status,
                started_at,
                completed_at,
                customer_count,
                order_count,
                rejected_customer_count,
                rejected_order_count,
                duration_seconds,
                error_message
            )
            VALUES (?, 'FAILED', ?, ?, NULL, NULL, NULL, NULL, ?, ?)
        """, (
            run_id,
            started_at,
            completed_at,
            duration_seconds,
            error_message
        ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_table_counts():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        tables = [
            "customers",
            "orders",
            "rejected_customers",
            "rejected_orders",
            "pipeline_runs"
        ]

        counts = {}

        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                counts[table] = 0

        return counts

    finally:
        connection.close()
