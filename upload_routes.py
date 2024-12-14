from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import process_csv
from models import KPIRecord
from dependencies import get_db
from uuid import uuid4
import os
import logging
import pandas as pd

UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

upload_routes = APIRouter()

@upload_routes.post("/upload/")
async def upload_file_and_calculate_kpis(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logging.info(f"Received file: {file.filename}")

    if not (file.filename.endswith(".csv") or file.filename.endswith(".xls") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV, XLS, or XLSX files are allowed.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Process and validate the DataFrame
        df, summary = process_csv(df)

        # Save data to the database
        for _, row in df.iterrows():
            record = KPIRecord(**row.to_dict())
            db.add(record)
        db.commit()

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
