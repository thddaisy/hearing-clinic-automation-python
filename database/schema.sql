CREATE TABLE IF NOT EXISTS parsed_records (
    id BIGSERIAL PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    clinic_name VARCHAR(150) NOT NULL,
    consultation_date DATE NOT NULL,
    doctor VARCHAR(100),
    audiologist VARCHAR(100),
    chart_no VARCHAR(50) NOT NULL UNIQUE,
    ear_side VARCHAR(20),
    demo_model VARCHAR(150),
    record_type VARCHAR(100),
    device_model VARCHAR(150),
    total_amount NUMERIC(12, 2),
    summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_records (
    id BIGSERIAL PRIMARY KEY,
    record_id VARCHAR(50) NOT NULL UNIQUE,
    record_date DATE NOT NULL,
    hospital_id VARCHAR(100) NOT NULL,
    patient_name VARCHAR(100) NOT NULL,
    chart_no VARCHAR(50),
    doctor_name VARCHAR(100),
    audiologist_name VARCHAR(100),
    transaction_type VARCHAR(50) NOT NULL,
    brand VARCHAR(100),
    product_model VARCHAR(150),
    ear_side VARCHAR(20),
    sale_price_nzd NUMERIC(12, 2) NOT NULL DEFAULT 0,
    repair_fee_nzd NUMERIC(12, 2) NOT NULL DEFAULT 0,
    memo TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);