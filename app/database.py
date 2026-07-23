import csv
import psycopg
from datetime import datetime
from pathlib import Path

from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from app.logger import setup_logger

logger = setup_logger(__name__)


def get_connection():
    connection = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return connection


def save_parsed_record(record):
    consultation_date = datetime.strptime(
        record["consultation_date"],
        "%d-%m-%Y",
    ).date()

    query = """
        INSERT INTO parsed_records (
            patient_name,
            clinic_name,
            consultation_date,
            doctor,
            audiologist,
            chart_no,
            ear_side,
            demo_model,
            record_type,
            device_model,
            total_amount,
            summary
        )
        VALUES (
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
        )
    """

    values = (
        record["patient_name"],
        record["clinic_name"],
        consultation_date,
        record.get("doctor"),
        record.get("audiologist"),
        record["chart_no"],
        record.get("ear_side"),
        record.get("demo_model"),
        record.get("record_type"),
        record.get("device_model"),
        record.get("total_amount"),
        record.get("summary"),
    )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

        connection.commit()
        logger.info(
            "Parsed record saved: %s",
            record["chart_no"],
        )
        return True

    except psycopg.errors.UniqueViolation:
        connection.rollback()
        logger.warning(
            "Duplicate chart number skipped: %s",
            record["chart_no"],
        )
        return False

    except Exception:
        connection.rollback()
        logger.exception(
            "Failed to save parsed record: %s",
            record["chart_no"],
        )
        raise

    finally:
        connection.close()


def save_sales_record(record):
    record_date = datetime.strptime(
        record["record_date"],
        "%d-%m-%Y",
    ).date()

    query = """
        INSERT INTO sales_records (
            record_id,
            record_date,
            hospital_id,
            patient_name,
            chart_no,
            doctor_name,
            audiologist_name,
            transaction_type,
            brand,
            product_model,
            ear_side,
            sale_price_nzd,
            repair_fee_nzd,
            memo
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
    """

    values = (
        record["record_id"],
        record_date,
        record["hospital_id"],
        record["patient_name"],
        record.get("chart_no"),
        record.get("doctor_name"),
        record.get("audiologist_name"),
        record["transaction_type"],
        record.get("brand"),
        record.get("product_model"),
        record.get("ear_side"),
        record.get("sale_price_nzd") or 0,
        record.get("repair_fee_nzd") or 0,
        record.get("memo"),
    )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

        connection.commit()

        logger.info(
            "Sales record saved: %s",
            record["record_id"],
        )
        return True

    except psycopg.errors.UniqueViolation:
        connection.rollback()

        logger.warning(
            "Duplicate sales record skipped: %s",
            record["record_id"],
        )
        return False

    except Exception:
        connection.rollback()

        logger.exception(
            "Failed to save sales record: %s",
            record.get("record_id"),
        )
        raise

    finally:
        connection.close()

def import_sales_records(csv_path):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Sales CSV file not found: {csv_path}")

    saved_count = 0
    duplicate_count = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for record in reader:
            saved = save_sales_record(record)

            if saved:
                saved_count += 1
            else:
                duplicate_count += 1

    logger.info(
        "Sales CSV import completed: saved=%s, duplicates=%s, file=%s",
        saved_count,
        duplicate_count,
        csv_path,
    )

    return saved_count, duplicate_count

def get_sales_summary():
    query = """
        SELECT
            COUNT(*) AS total_records,
            COALESCE(SUM(sale_price_nzd), 0) AS total_sales,
            COALESCE(SUM(repair_fee_nzd), 0) AS total_repair_fees,
            COALESCE(
                SUM(sale_price_nzd + repair_fee_nzd),
                0
            ) AS total_revenue
        FROM sales_records
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        logger.info("Sales summary query completed")

        return {
            "total_records": result[0],
            "total_sales": result[1],
            "total_repair_fees": result[2],
            "total_revenue": result[3],
        }

    except Exception:
        logger.exception("Failed to calculate sales summary")
        raise

    finally:
        connection.close()

def get_hospital_sales_summary():
    query = """
        SELECT
            hospital_id,
            COUNT(*) AS total_records,
            COALESCE(SUM(sale_price_nzd), 0) AS total_sales,
            COALESCE(SUM(repair_fee_nzd), 0) AS total_repair_fees,
            COALESCE(
                SUM(sale_price_nzd + repair_fee_nzd),
                0
            ) AS total_revenue
        FROM sales_records
        GROUP BY hospital_id
        ORDER BY hospital_id
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        logger.info(
            "Hospital sales summary query completed: hospitals=%s",
            len(rows),
        )

        return [
            {
                "hospital_id": row[0],
                "total_records": row[1],
                "total_sales": row[2],
                "total_repair_fees": row[3],
                "total_revenue": row[4],
            }
            for row in rows
        ]

    except Exception:
        logger.exception("Failed to calculate hospital sales summary")
        raise

    finally:
        connection.close()