import pandas as pd
from models import SessionLocal, KPIRecord

# Open a database session
db = SessionLocal()

try:
    # Query all KPI records
    records = db.query(KPIRecord).all()
    data = [
        {
            "file_id": r.file_id,
            "timestamp": r.timestamp,
            "availability": r.availability,
            "performance": r.performance,
            "quality": r.quality,
            "oee": r.oee,
        }
        for r in records
    ]
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Print the DataFrame
    print(df)
finally:
    # Close the database session
    db.close()
