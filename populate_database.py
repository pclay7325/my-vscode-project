from models import SessionLocal, KPIRecord, WidgetDefinition
from datetime import datetime

# Create a new database session
db = SessionLocal()

try:
    # Add sample KPI record
    kpi = KPIRecord(
        file_id="sample_file",
        timestamp=datetime.utcnow(),
        availability=90.0,
        performance=85.0,
        quality=95.0,
        oee=85.0,
        downtime_percentage=10.0,
        utilization_percentage=75.0,
        yield_percentage=90.0,
        throughput=500,
    )
    db.add(kpi)

    # Add sample widget definition
    widget = WidgetDefinition(
        widget_type="Number",
        label="Sample Widget",
        options={"min": 0, "max": 100},
        validation_rules={"required": True},
    )
    db.add(widget)

    # Commit the transaction
    db.commit()
    print("Data added successfully.")
except Exception as e:
    db.rollback()
    print(f"Error adding data: {e}")
finally:
    db.close()
from datetime import datetime, timezone

# Update the timestamp to use timezone-aware UTC
timestamp=datetime.now(timezone.utc)
