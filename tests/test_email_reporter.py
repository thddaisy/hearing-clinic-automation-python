from app.email_reporter import build_monthly_sales_email, calculate_sales_summary
import pytest

def test_record_count():
    records = [
        {
            "hospital_id": "H001",
            "sale_price_nzd": "1000",
            "repair_fee_nzd": "100",
        },
        {
            "hospital_id": "H002",
            "sale_price_nzd": "2000",
            "repair_fee_nzd": "200",
        },
    ]

    summary = calculate_sales_summary(records)

    assert summary["total_records"] == 2
    assert summary["total_sales"] == 3000
    assert summary["total_repair_fees"] == 300
    assert summary["total_revenue"] == 3300


def test_hospital_summary():
    records = [
        {
            "hospital_id": "H001",
            "sale_price_nzd": "1000",
            "repair_fee_nzd": "100",
        },
        {
            "hospital_id": "H001",
            "sale_price_nzd": "500",
            "repair_fee_nzd": "50",
        },
        {
            "hospital_id": "H002",
            "sale_price_nzd": "2000",
            "repair_fee_nzd": "200",
        },
    ]


    summary = calculate_sales_summary(records)

    hospital_summary = summary["hospital_summary"]

    assert hospital_summary["H001"]["record_count"] == 2
    assert hospital_summary["H001"]["total_sales"] == 1500
    assert hospital_summary["H001"]["total_repair_fees"] == 150
    assert hospital_summary["H001"]["total_revenue"] == 1650

    assert hospital_summary["H002"]["record_count"] == 1
    assert hospital_summary["H002"]["total_revenue"] == 2200


def test_email_content():
    summary = {
        "total_records": 2,
        "total_sales": 3000,
        "total_repair_fees": 300,
        "total_revenue": 3300,
        "hospital_summary": {
            "H001": {
                "record_count": 2,
                "total_sales": 3000,
                "total_repair_fees": 300,
                "total_revenue": 3300,
            }
        },
    }

    subject, body = build_monthly_sales_email(summary)

    assert subject == "Monthly Hearing Clinic Sales Report"
    assert "Total records: 2" in body
    assert "Total sales: NZD 3,000.00" in body
    assert "Total revenue: NZD 3,300.00" in body
    assert "H001" in body


def test_empty_records():
    summary = calculate_sales_summary([])

    assert summary["total_records"] == 0
    assert summary["total_sales"] == 0
    assert summary["total_repair_fees"] == 0
    assert summary["total_revenue"] == 0
    assert summary["hospital_summary"] == {}


def test_invalid_sales_value():
    records = [
        {
            "hospital_id": "H001",
            "sale_price_nzd": "invalid",
            "repair_fee_nzd": "100",
        }
    ]

    with pytest.raises(ValueError):
        calculate_sales_summary(records)