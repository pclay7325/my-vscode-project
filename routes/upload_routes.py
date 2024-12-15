from fastapi import APIRouter, UploadFile, File
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, ProductionPerformance, UploadedFileLog
from pydantic import BaseModel, ValidationError
from datetime import datetime
import logging
import json
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
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

# Function to save validation errors to a JSON file
def save_validation_errors(errors, file_name):
    error_file = f"validation_errors_{file_name}.json"
    with open(error_file, "w") as f:
        json.dump(errors, f, indent=4)
    return os.path.abspath(error_file)

# Function to map uploaded columns to the schema
def map_columns(data):
    data.columns = data.columns.str.strip().str.lower()
    logger.info(f"Standardized Columns: {data.columns.tolist()}")
    column_mapping = {}
    for key, possible_names in REQUIRED_COLUMNS.items():
        for name in possible_names:
            if name.lower() in data.columns:
                column_mapping[name.lower()] = key
                break
    missing_columns = [key for key in REQUIRED_COLUMNS if key not in column_mapping.values()]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    data.rename(columns=column_mapping, inplace=True)
    logger.info(f"Mapped Columns: {data.columns.tolist()}")
    return data

# API endpoint for uploading production performance data
@upload_routes.post("/upload-production-performance", tags=["Upload"])
async def upload_production_performance(file: UploadFile = File(...)):
    session: Session = SessionLocal()
    file_metadata = {
        "file_name": file.filename,
        "upload_date": datetime.now(),
        "status": "Processing",
        "processed_rows": 0,
        "skipped_rows": 0
    }
    validation_errors = []
    temp_directory = "uploaded_files"
    os.makedirs(temp_directory, exist_ok=True)

    try:
        # Save uploaded file temporarily
        temp_file_path = os.path.join(temp_directory, file.filename)
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        # Validate file size
        if os.path.getsize(temp_file_path) > 10 * 1024 * 1024:  # 10 MB
            return {"error": "File size exceeds the allowed limit of 10 MB."}

        # Process file in chunks
        if file.filename.endswith('.csv'):
            chunks = pd.read_csv(temp_file_path, chunksize=500)
        else:
            df = pd.read_excel(temp_file_path)  # Read full Excel file
            num_chunks = len(df) // 500 + 1
            chunks = [df[i * 500:(i + 1) * 500] for i in range(num_chunks)]

        # Process chunks
        total_rows, skipped_rows = 0, 0
        for chunk in chunks:
            try:
                chunk = map_columns(chunk)
            except ValueError as ve:
                logger.error(f"Column Mapping Error: {str(ve)}")
                return {"error": f"Validation Error: {str(ve)}"}

            # Validate rows
            for index, row in chunk.iterrows():
                total_rows += 1
                try:
                    validated_row = ProductionPerformanceSchema(**row.to_dict())
                    session.add(ProductionPerformance(**validated_row.dict()))
                except ValidationError as ve:
                    skipped_rows += 1
                    validation_errors.append({"row": index + total_rows, "errors": str(ve)})

        # Commit valid data
        session.commit()

        # Update file metadata
        file_metadata["status"] = "Success"
        file_metadata["processed_rows"] = total_rows - skipped_rows
        file_metadata["skipped_rows"] = skipped_rows

        # Save validation errors if any
        error_file = None
        if skipped_rows > 0:
            error_file = save_validation_errors(validation_errors, os.path.splitext(file.filename)[0])
            file_metadata["validation_errors"] = error_file
        else:
            file_metadata["validation_errors"] = None

        # Log file upload
        session.add(UploadedFileLog(**file_metadata))
        session.commit()

        return {
            "message": "File uploaded successfully.",
            "file_name": file.filename,
            "processed_rows": file_metadata["processed_rows"],
            "skipped_rows": skipped_rows,
            "validation_errors_file": error_file
        }

    except Exception as e:
        session.rollback()
        logger.error(f"Error: {str(e)}")
        return {"error": f"File processing failed: {str(e)}"}

    finally:
        session.close()
