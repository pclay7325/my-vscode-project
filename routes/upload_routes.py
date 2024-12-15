from fastapi import APIRouter, UploadFile, File
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, ProductionPerformance
from pydantic import BaseModel, ValidationError
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

upload_routes = APIRouter()

# Standardized required column mappings
REQUIRED_COLUMNS = {
    "machine": ["machine"],
    "runtime_minutes": ["runtime (minutes)"],
    "planned_time_minutes": ["planned time (minutes)"],
    "good_units": ["good units"],
    "total_units": ["total units"],
    "downtime_minutes": ["downtime (minutes)"]
}

class ProductionPerformanceSchema(BaseModel):
    machine: str
    runtime_minutes: int
    planned_time_minutes: int
    good_units: int
    total_units: int
    downtime_minutes: int

def map_columns(data):
    """
    Dynamically map uploaded file columns to the standardized schema.
    """
    # Standardize the column names in the uploaded file
    data.columns = data.columns.str.strip().str.lower()
    logger.info(f"Standardized Columns: {data.columns.tolist()}")

    # Create a mapping from required columns to uploaded file columns
    column_mapping = {}
    for key, possible_names in REQUIRED_COLUMNS.items():
        for name in possible_names:
            if name.lower() in data.columns:
                column_mapping[name.lower()] = key
                break

    # Check for missing required columns
    missing_columns = [key for key in REQUIRED_COLUMNS if key not in column_mapping.values()]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Rename the columns in the DataFrame to match the schema keys
    data.rename(columns=column_mapping, inplace=True)
    logger.info(f"Mapped Columns: {data.columns.tolist()}")
    return data

@upload_routes.post("/upload-production-performance", tags=["Upload"])
async def upload_production_performance(file: UploadFile = File(...)):
    """
    Endpoint to upload production performance data and save it to the database.
    """
    session: Session = SessionLocal()
    try:
        # Validate file size
        file.file.seek(0, 2)  # Move to the end of the file
        file_size = file.file.tell()  # Get the file size
        file.file.seek(0)  # Reset pointer
        if file_size > 10 * 1024 * 1024:  # 10 MB
            return {"error": "File size exceeds the allowed limit of 10 MB."}

        # Read the uploaded file
        if file.content_type == "text/csv":
            data = pd.read_csv(file.file)
        elif file.content_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            data = pd.read_excel(file.file)
        else:
            return {"error": "Unsupported file format. Please upload a CSV or Excel file."}

        # Map and validate columns dynamically
        data = map_columns(data)

        # Validate each row using Pydantic schema
        validated_data = []
        skipped_rows = 0
        for index, row in data.iterrows():
            try:
                validated_row = ProductionPerformanceSchema(**row.to_dict())
                validated_data.append(validated_row.dict())
            except ValidationError as ve:
                logger.warning(f"Validation Error for row {index}: {ve}")
                skipped_rows += 1

        # Bulk insert validated rows into the database
        session.bulk_save_objects([
            ProductionPerformance(
                machine=row["machine"],
                runtime_minutes=row["runtime_minutes"],
                planned_time_minutes=row["planned_time_minutes"],
                good_units=row["good_units"],
                total_units=row["total_units"],
                downtime_minutes=row["downtime_minutes"]
            )
            for row in validated_data
        ])
        session.commit()

        return {
            "message": f"File uploaded successfully. Processed {len(validated_data)} rows.",
            "skipped_rows": skipped_rows
        }

    except ValueError as ve:
        session.rollback()
        logger.error(f"Validation Error: {str(ve)}")
        return {"error": f"Validation Error: {str(ve)}"}

    except Exception as e:
        session.rollback()
        logger.error(f"Error: {str(e)}")
        return {"error": f"File processing failed: {str(e)}"}

    finally:
        session.close()
