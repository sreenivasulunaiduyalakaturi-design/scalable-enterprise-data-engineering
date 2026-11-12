"""Generate a sample raw sales CSV (with duplicates and bad rows on purpose)."""
import csv, random
from datetime import date, timedelta

random.seed(42)
CATEGORIES = ["electronics", "grocery", "fashion", "home", "toys"]


def main(rows: int = 10_000, out: str = "data/raw/sales.csv"):
    start = date(2024, 1, 1)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["order_id", "customer_id", "category", "quantity", "unit_price", "order_date"])
        for i in range(rows):
            row = [i, f"C{random.randint(1, 500):04d}", random.choice(CATEGORIES),
                   random.randint(1, 5), round(random.uniform(5, 500), 2),
                   (start + timedelta(days=random.randint(0, 89))).isoformat()]
            if random.random() < 0.02:  row[3] = -1          # invalid quantity
            if random.random() < 0.01:  row[1] = ""          # missing customer
            w.writerow(row)
            if random.random() < 0.01:  w.writerow(row)      # duplicate
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
