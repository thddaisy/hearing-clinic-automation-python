from app.csv_writer import is_duplicate_record

def test_duplicate_record(tmp_path):
    csv_path = tmp_path / "records.csv"

    csv_path.write_text(
        "chart_no,hospital_id\n"
        "CH001,H001\n",
        encoding="utf-8",
    )

    record = {
        "chart_no": "CH001",
        "hospital_id": "H001",
    }

    result = is_duplicate_record(record, csv_path)

    assert result is True


def test_non_duplicate_record(tmp_path):
    csv_path = tmp_path / "records.csv"

    csv_path.write_text(
        "chart_no,hospital_id\n"
        "CH001,H001\n",
        encoding="utf-8",
    )

    record = {
        "chart_no": "CH002",
        "hospital_id": "H001",
    }

    result = is_duplicate_record(record, csv_path)

    assert result is False


def test_missing_csv(tmp_path):
    csv_path = tmp_path / "missing.csv"

    record = {
        "chart_no": "CH001",
        "hospital_id": "H001",
    }

    result = is_duplicate_record(record, csv_path)

    assert result is False