
import json

from src import pipeline


def test_pipeline_success(monkeypatch, tmp_path):
    # Prepare sample input data for this isolated test.
    import pandas as pd

    customers = pd.DataFrame([
        {
            "customer_id": "C001",
            "first_name": "ravi",
            "last_name": "kumar",
            "email": "ravi@example.com",
            "city": "hyderabad",
            "created_at": "2026-10-01"
        }
    ])

    orders = pd.DataFrame([
        {
            "order_id": "O001",
            "customer_id": "C001",
            "order_date": "2026-10-02",
            "amount": 500,
            "status": "completed"
        }
    ])

    monkeypatch.setattr(
        pipeline, "load_customers", lambda: customers
    )
    monkeypatch.setattr(
        pipeline, "load_orders", lambda: orders
    )

    published = {}

    def fake_publish(
    customers,
    orders,
    rejected_customers,
    rejected_orders,
    **kwargs
):
        published["customers"] = customers
        published["orders"] = orders
        published["rejected_customers"] = rejected_customers
        published["rejected_orders"] = rejected_orders

    monkeypatch.setattr(pipeline, "publish_data", fake_publish)

    class FakeLogger:
        def info(self, *args, **kwargs):
            pass

        def exception(self, *args, **kwargs):
            pass

    monkeypatch.setattr(
        pipeline, "setup_logger", lambda: FakeLogger()
    )

    monkeypatch.chdir(tmp_path)

    pipeline.run_pipeline()

    report_file = tmp_path / "data" / "output" / "run_report.json"
    assert report_file.exists()

    report = json.loads(report_file.read_text())

    assert report["status"] == "SUCCESS"
    assert report["customers"]["input"] == 1
    assert report["customers"]["accepted"] == 1
    assert report["customers"]["rejected"] == 0
    assert report["orders"]["input"] == 1
    assert report["orders"]["accepted"] == 1
    assert report["orders"]["rejected"] == 0

    assert len(published["customers"]) == 1
    assert len(published["orders"]) == 1
    assert len(published["rejected_customers"]) == 0
    assert len(published["rejected_orders"]) == 0


def test_pipeline_failure_records_failed_run(monkeypatch):
    import pytest

    monkeypatch.setattr(
        pipeline,
        "load_customers",
        lambda: (_ for _ in ()).throw(
            RuntimeError("Test failure")
        )
    )

    recorded = {}

    def fake_record_failed_run(**kwargs):
        recorded.update(kwargs)

    monkeypatch.setattr(
        pipeline,
        "record_failed_run",
        fake_record_failed_run
    )

    class FakeLogger:
        def info(self, *args, **kwargs):
            pass

        def exception(self, *args, **kwargs):
            pass

    monkeypatch.setattr(
        pipeline,
        "setup_logger",
        lambda: FakeLogger()
    )

    with pytest.raises(RuntimeError, match="Test failure"):
        pipeline.run_pipeline()

    assert recorded["run_id"]
    assert recorded["error_message"] == "Test failure"
    assert recorded["started_at"]
    assert recorded["completed_at"]

