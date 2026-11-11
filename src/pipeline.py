
import json
import time
import uuid
from pathlib import Path
from datetime import datetime

from src.ingestion import load_customers, load_orders
from src.validation import validate_customers, validate_orders
from src.transformation import transform_customers, transform_orders
from src.publishing import publish_data, record_failed_run
from src.logger import setup_logger


def run_pipeline():
    logger = setup_logger()
    start_time = time.time()
    started_at = datetime.now().isoformat()
    run_id = str(uuid.uuid4())

    try:
        logger.info("Pipeline started. Run ID: %s", run_id)

        # 1. Ingestion
        customers = load_customers()
        orders = load_orders()

        logger.info("Customer records loaded: %s", len(customers))
        logger.info("Order records loaded: %s", len(orders))

        # 2. Validation
        valid_customers, rejected_customers = validate_customers(
            customers,
            source_file="customers.csv",
            run_id=run_id
        )

        valid_customer_ids = set(
            valid_customers["customer_id"].astype(str)
        )

        valid_orders, rejected_orders = validate_orders(
            orders,
            valid_customer_ids,
            source_file="orders.csv",
            run_id=run_id
        )

        logger.info("Valid customers: %s", len(valid_customers))
        logger.info("Rejected customers: %s", len(rejected_customers))
        logger.info("Valid orders: %s", len(valid_orders))
        logger.info("Rejected orders: %s", len(rejected_orders))

        # 3. Data reconciliation
        customer_input = len(customers)
        customer_accepted = len(valid_customers)
        customer_rejected = len(rejected_customers)

        order_input = len(orders)
        order_accepted = len(valid_orders)
        order_rejected = len(rejected_orders)

        customer_balanced = (
            customer_input == customer_accepted + customer_rejected
        )

        order_balanced = (
            order_input == order_accepted + order_rejected
        )

        reconciliation = {
            "customers": {
                "input": customer_input,
                "accepted": customer_accepted,
                "rejected": customer_rejected,
                "balanced": customer_balanced
            },
            "orders": {
                "input": order_input,
                "accepted": order_accepted,
                "rejected": order_rejected,
                "balanced": order_balanced
            },
            "overall_status": (
                "PASSED"
                if customer_balanced and order_balanced
                else "FAILED"
            )
        }

        logger.info("Customer reconciliation: %s", customer_balanced)
        logger.info("Order reconciliation: %s", order_balanced)

        if not customer_balanced or not order_balanced:
            raise RuntimeError(
                "Data reconciliation failed. "
                "Input records do not match accepted + rejected records."
            )

        logger.info("Data reconciliation passed.")

        # 4. Transformation
        valid_customers = transform_customers(valid_customers)
        valid_orders = transform_orders(valid_orders)

        # 5. Export rejected records
        rejected_folder = Path("data/rejected")
        rejected_folder.mkdir(parents=True, exist_ok=True)

        rejected_customers.to_csv(
            rejected_folder / "rejected_customers.csv",
            index=False
        )

        rejected_orders.to_csv(
            rejected_folder / "rejected_orders.csv",
            index=False
        )

        logger.info("Rejected records exported successfully.")

        # 6. Publishing and run history
        duration = round(time.time() - start_time, 2)
        completed_at = datetime.now().isoformat()

        publish_data(
            valid_customers,
            valid_orders,
            rejected_customers,
            rejected_orders,
            run_id=run_id,
            status="SUCCESS",
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration
        )

        # 7. Run report
        report = {
            "run_id": run_id,
            "status": "SUCCESS",
            "started_at": started_at,
            "completed_at": completed_at,
            "customers": {
                "input": customer_input,
                "accepted": customer_accepted,
                "rejected": customer_rejected
            },
            "orders": {
                "input": order_input,
                "accepted": order_accepted,
                "rejected": order_rejected
            },
            "reconciliation": reconciliation,
            "duration_seconds": duration
        }

        output_folder = Path("data/output")
        output_folder.mkdir(parents=True, exist_ok=True)

        # Save the latest run report
        with open(output_folder / "run_report.json", "w") as file:
            json.dump(report, file, indent=4)

        # Save a separate report for this specific run
        with open(output_folder / f"run_report_{run_id}.json", "w") as file:
            json.dump(report, file, indent=4)

        logger.info("Pipeline completed successfully.")
        logger.info("Execution time: %s seconds", duration)

        print("\n========== PIPELINE SUMMARY ==========")
        print(json.dumps(report, indent=4))
        print("======================================")

    except Exception as error:
        logger.exception("Pipeline failed.")

        # Record the failed execution in the database
        try:
            failed_duration = round(time.time() - start_time, 2)
            failed_completed_at = datetime.now().isoformat()

            record_failed_run(
                run_id=run_id,
                started_at=started_at,
                completed_at=failed_completed_at,
                duration_seconds=failed_duration,
                error_message=str(error)
            )

            logger.info("Failed run recorded in database.")

        except Exception:
            logger.exception("Could not record failed run.")

        raise
