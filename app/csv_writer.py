import csv
from pathlib import Path


def save_record_to_csv(record, csv_path):
    csv_path = Path(csv_path)

    file_exists = csv_path.exists()

    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=record.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(record)