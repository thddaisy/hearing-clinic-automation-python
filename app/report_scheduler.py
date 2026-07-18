import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from app.email_reporter import send_monthly_report
from app.logger import setup_logger

logger = setup_logger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "clinic_sales_records.csv"


def run_monthly_report_job():
    logger.info("Monthly report job started")

    try:
        send_monthly_report(CSV_PATH)
    except Exception:
        logger.exception("Monthly report job failed")
        raise

    logger.info("Monthly report job finished")


def create_dev_scheduler():
    scheduler = BackgroundScheduler()
    run_time = datetime.now() + timedelta(seconds=5)
    scheduler.add_job(
        run_monthly_report_job,
        "date", 
        run_date=run_time,
    )

    return scheduler, run_time

def create_monthly_scheduler():
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_monthly_report_job,
        "cron",
        day="last",
        hour=17,
        minute=30,
        id="monthly_report",
        replace_existing=True,
    )

    return scheduler


def run_dev_scheduler():
    scheduler, run_time = create_dev_scheduler()

    scheduler.start()
    logger.info("Dev job scheduled for: %s", run_time)

    time.sleep(7)

    scheduler.shutdown()
    logger.info("Dev scheduler stopped")

def run_monthly_scheduler():
    scheduler = create_monthly_scheduler()

    logger.info(
        "Monthly report scheduled for the last day of each month at 17:30"
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Monthly scheduler stopped by user")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.report_scheduler [dev|monthly]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "dev":
        run_dev_scheduler()
    elif mode == "monthly":
        run_monthly_scheduler()
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'dev' or 'monthly'.")
        sys.exit(1)