from models import SessionLocal, KPIRecord

# Create a new database session
db = SessionLocal()

try:
    # Query all KPI records
    kpi_records = db.query(KPIRecord).all()
    print("KPI Records:")
    for record in kpi_records:
        print(
            f"File ID: {record.file_id}, Timestamp: {record.timestamp}, OEE: {record.oee}"
        )
finally:
    db.close()
