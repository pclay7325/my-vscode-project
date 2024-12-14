import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from utils import process_csv
from charts import generate_bar_chart, generate_oee_line_chart
from html_generator import generate_html
from weasyprint import HTML

# Ensure these directories exist
UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define API routers
upload_routes = APIRouter()  # Must be defined before being used
report_routes = APIRouter()  # Must be defined before being used

@upload_routes.post("/upload/")
async def upload_file_and_calculate_kpis(file: UploadFile = File(...)):
    logging.info(f"Received file: {file.filename}")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    logging.info(f"File saved to: {file_path}")

    try:
        df, summary = process_csv(file_path)
        logging.info(f"File processed successfully. Summary: {summary}")
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "rows": len(df),
        "kpi_summary": summary,
    }

@report_routes.post("/report/")
async def generate_report(file: UploadFile = File(...)):
    logging.info(f"Received file for PDF report generation: {file.filename}")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    logging.info(f"File saved for report generation: {file_path}")

    try:
        df, summary = process_csv(file_path)
        logging.info(f"CSV processed successfully. Summary: {summary}")
    except Exception as e:
        logging.error(f"Error processing CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

    try:
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
