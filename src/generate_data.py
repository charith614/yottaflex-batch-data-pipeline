
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta


def generate_data(customer_count=10000, order_count=10000, seed=42):
    random.seed(seed)

    folder = Path("data/input")
    folder.mkdir(parents=True, exist_ok=True)

    customer_ids = [
        f"C{i:06d}" for i in range(1, customer_count + 1)
    ]

    # Generate customer records
    with open(folder / "customers.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "customer_id", "first_name", "last_name",
            "email", "city", "created_at"
        ])

        for i in range(customer_count):
            customer_id = customer_ids[i]
            email = f"customer{i+1}@example.com"

            if i % 1000 == 0:
                email = "invalid-email"

            if i == 1:
                customer_id = ""

            writer.writerow([
                customer_id,
                f"First{i+1}",
                f"Last{i+1}",
                email,
                random.choice([
                    "Hyderabad", "Bengaluru", "Chennai", "Pune"
                ]),
                (
                    datetime(2026, 1, 1)
                    + timedelta(days=random.randint(0, 300))
                ).isoformat()
            ])

        # Add duplicate customer
        writer.writerow([
            customer_ids[0], "Duplicate", "Customer",
            "duplicate@example.com", "Hyderabad",
            "2026-10-01T09:00:00"
        ])

    # Generate order records
    with open(folder / "orders.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "order_id", "customer_id", "order_date",
            "amount", "status"
        ])

        for i in range(order_count):
            customer_id = random.choice(customer_ids)
            amount = round(random.uniform(100, 10000), 2)

            if i % 1000 == 0:
                customer_id = ""
            elif i % 1000 == 1:
                customer_id = "C999999"
            elif i % 1000 == 2:
                amount = -100.00

            writer.writerow([
                f"O{i+1:07d}",
                customer_id,
                (
                    datetime(2026, 1, 1)
                    + timedelta(days=random.randint(0, 300))
                ).isoformat(),
                amount,
                random.choice([
                    "COMPLETED", "PENDING", "CANCELLED"
                ])
            ])

        # Add duplicate order
        writer.writerow([
            "O0000001", customer_ids[0],
            "2026-10-01T10:00:00", 1500.00, "COMPLETED"
        ])

    print("Data generation successful!")
    print(f"Customers generated: {customer_count}")
    print(f"Orders generated: {order_count}")


if __name__ == "__main__":
    generate_data()
