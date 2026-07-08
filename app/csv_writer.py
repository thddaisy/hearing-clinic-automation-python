import csv
from pathlib import Path


def is_duplicate_record(record, csv_path):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        return False
    
    new_chart_no = record.get("chart_no")

    if not new_chart_no:
        return False
    
    with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            existing_chart_no = row.get("chart_no")

            if existing_chart_no == new_chart_no:
                return True
    return False
        

def save_record_to_csv(record, csv_path):
    csv_path = Path(csv_path)

    file_exists = csv_path.exists()

    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=record.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(record)