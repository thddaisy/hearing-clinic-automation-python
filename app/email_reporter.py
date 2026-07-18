import csv
import sys
from pathlib import Path
from app.config import REPORT_RECIPIENT_EMAIL
from app.email_sender import send_email


def read_sales_records(csv_path):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        return False
    
    records = []
    
    with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)
    return records


def calculate_sales_summary(records):
    total_records = len(records)
    total_sales = 0
    total_repair_fees = 0
    hospital_summary = {}

    for row in records:
        sale_price = float(row["sale_price_nzd"])
        repair_fee = float(row["repair_fee_nzd"])
        hospital_id = row["hospital_id"]

        if hospital_id not in hospital_summary:
            hospital_summary[hospital_id] = {
                "record_count": 0,
                "total_sales": 0,
                "total_repair_fees": 0,
                "total_revenue": 0,
            }

        hospital_data = hospital_summary[hospital_id]

        hospital_data["record_count"] = hospital_data["record_count"] + 1
        hospital_data["total_sales"] = hospital_data["total_sales"] + sale_price
        hospital_data["total_repair_fees"] = hospital_data["total_repair_fees"] + repair_fee
        hospital_data["total_revenue"] = hospital_data["total_revenue"] + sale_price + repair_fee

        total_sales = total_sales + sale_price
        total_repair_fees = total_repair_fees + repair_fee

    total_revenue = total_sales + total_repair_fees

    summary = {
        "total_records": total_records,
        "total_sales": total_sales,
        "total_repair_fees": total_repair_fees,
        "total_revenue": total_revenue,
        "hospital_summary": hospital_summary,
    }

    return summary


def build_monthly_sales_email(summary):
    subject = "Monthly Hearing Clinic Sales Report"

    hospital_lines = []

    for hospital_id, hospital_data in summary["hospital_summary"].items():
        line = (
            f"- {hospital_id} | "
            f"Records: {hospital_data['record_count']} | "
            f"Sales: NZD {hospital_data['total_sales']:,.2f} | "
            f"Repairs: NZD {hospital_data['total_repair_fees']:,.2f} | "
            f"Revenue: NZD {hospital_data['total_revenue']:,.2f}"
        )
        hospital_lines.append(line)
    
    hospital_summary_text = "\n".join(hospital_lines)

    body = f"""
Total records: {summary["total_records"]}
Total sales: NZD {summary["total_sales"]:,.2f}
Total repair fees: NZD {summary["total_repair_fees"]:,.2f}
Total revenue: NZD {summary["total_revenue"]:,.2f}

Hospital Summary:
{hospital_summary_text}
"""
    

    return subject, body


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.email_reporter <csv_path>")
        return
    
    csv_path = sys.argv[1]
    send_monthly_report(csv_path)



def send_monthly_report(csv_path):
    records = read_sales_records(csv_path)

    if records is False:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    print(f"Loaded {len(records)} records.")

    summary = calculate_sales_summary(records)
    subject, body = build_monthly_sales_email(summary)

    print()
    print(f"To: {REPORT_RECIPIENT_EMAIL}")
    print(f"Subject: {subject}")
    print(body)

    try:
        result = send_email(
            REPORT_RECIPIENT_EMAIL,
            subject,
            body,
        )

        print(f"Email sent: {result['id']}")

    except Exception as error:
        print(f"Email sending failed: {error}")
        raise

        
if __name__ == "__main__":
    main()