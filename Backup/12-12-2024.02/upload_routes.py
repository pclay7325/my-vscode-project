from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import process_csv
from models import KPIRecord
from dependencies import get_db
from uuid import uuid4
import os
import logging

UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

upload_routes = APIRouter()

@upload_routes.post("/upload/")
async def upload_file_and_calculate_kpis(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logging.info(f"Received file: {file.filename}")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        df, summary = process_csv(file_path)
        logging.info(f"File processed successfully. Summary: {summary}")

        # Save KPI records to the database
        for _, row in df.iterrows():
            record = KPIRecord(
                file_id=file_id,
                timestamp=row["timestamp"],
                availability=row["availability"],
                performance=row["performance"],
                quality=row["quality"],
                oee=row["oee"],
                downtime_percentage=row["downtime_percentage"],
                utilization_percentage=row["utilization_percentage"],
                yield_percentage=row["yield_percentage"],
                throughput=row["throughput"],
            )
            db.add(record)
        db.commit()
        logging.info(f"KPI records saved to database for file ID: {file_id}")

    except Exception as e:
        logging.error(f"Error processing CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "rows": len(df),
        "kpi_summary": summary,
    }
