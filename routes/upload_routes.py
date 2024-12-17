from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, ProductionPerformance
from utils.auth_utils import decode_access_token
from datetime import datetime
import pandas as pd
from io import BytesIO
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
upload_routes = APIRouter()

# JWT dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------- FILE UPLOAD ENDPOINT ----------------------

@upload_routes.post("/api/v1/upload/upload-production-performance", tags=["Upload"], summary="Upload production performance data")
async def upload_production_performance(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Upload production performance data file (CSV or Excel).
    Requires a valid JWT token.
    """
    # Validate JWT token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Process file
    try:
        contents = await file.read()

        # Detect file type and parse the file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload CSV or Excel files.")

        # Validate and insert data into the database
        total_rows = 0
        for _, row in df.iterrows():
            if "machine" in row and "runtime_minutes" in row and "planned_time_minutes" in row:
                new_record = ProductionPerformance(
                    machine=row.get("machine"),
                    runtime_minutes=row.get("runtime_minutes"),
                    planned_time_minutes=row.get("planned_time_minutes"),
                    good_units=row.get("good_units", 0),
                    total_units=row.get("total_units", 0),
                    downtime_minutes=row.get("downtime_minutes", 0),
                )
                db.add(new_record)
                total_rows += 1
        db.commit()

        return {
            "message": "File uploaded and data processed successfully",
            "total_rows_processed": total_rows
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")
    finally:
        db.close()
