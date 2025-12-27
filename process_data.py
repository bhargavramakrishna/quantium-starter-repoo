import csv
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "output/final_output.csv"

csv_files = list(DATA_DIR.glob("*.csv"))

with OUTPUT_FILE.open("w", newline="") as out_f:
    writer = csv.writer(out_f)
    writer.writerow(["Sales", "Date", "Region"])
    for file_path in csv_files:
        with file_path.open("r", newline="") as in_f:
            reader = csv.DictReader(in_f)
            print(reader.fieldnames)

            for row in reader:
                if row["product"] != "pink morsel":
                    continue

                quantity = float(row["quantity"])
                price = float(row["price"].replace("$", ""))
                sales = quantity * price

                date = row["date"]
                region = row["region"]

                writer.writerow([sales, date, region])

print(f"✅ Wrote output to: {OUTPUT_FILE}")