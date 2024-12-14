
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from utils import process_csv
from charts import generate_bar_chart, generate_oee_line_chart
from html_generator import generate_html
from weasyprint import HTML
from dependencies import get_db
from uuid import uuid4
import os
import logging

UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

report_routes = APIRouter()

@report_routes.post("/report/")
async def generate_report(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logging.info(f"Received file for PDF report generation: {file.filename}")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        df, summary = process_csv(file_path)
        logging.info(f"CSV processed successfully. Summary: {summary}")

        # Generate bar chart and OEE line chart
        bar_chart_path = generate_bar_chart(file.filename, summary, UPLOAD_DIR)
        oee_line_chart_path = generate_oee_line_chart(df, UPLOAD_DIR)
        logging.info(f"Charts generated: {bar_chart_path}, {oee_line_chart_path}")

    except Exception as e:
        logging.error(f"Error generating charts: {e}")
        raise HTTPException(status_code=500, detail="Error generating charts.")

    pdf_file_path = os.path.join(UPLOAD_DIR, f"{file.filename}_report.pdf")
    try:
        # Generate HTML and PDF
        html_content = generate_html(file.filename, summary, bar_chart_path, oee_line_chart_path)
        HTML(string=html_content).write_pdf(pdf_file_path)
        logging.info(f"PDF report generated at: {pdf_file_path}")

    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail="Error generating PDF.")

    if not os.path.exists(pdf_file_path):
        logging.error(f"PDF file not found: {pdf_file_path}")
        raise HTTPException(status_code=500, detail="PDF file not generated.")

    return FileResponse(pdf_file_path, media_type="application/pdf", filename=f"{file.filename}_report.pdf")
