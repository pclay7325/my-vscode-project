from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal, ProductionPerformance
from utils.auth_utils import decode_access_token
from io import BytesIO
import pandas as pd
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upload_routes")

upload_routes = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@upload_routes.post("/upload-production-performance", tags=["Upload"], summary="Upload production performance data")
async def upload_production_performance(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Validate token
    logger.info("Starting token validation...")
    payload = decode_access_token(token)
    if not payload:
        logger.error("Invalid or expired token.")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    logger.info(f"Token validated for user: {payload.get('sub')}")

    # Process file
    try:
        contents = await file.read()
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents))
        else:
            logger.error("Unsupported file type.")
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Save records to database
        total_rows = 0
        for _, row in df.iterrows():
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

        return {"message": "File uploaded successfully.", "total_rows_processed": total_rows}
    except Exception as e:
        logger.error(f"File processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
