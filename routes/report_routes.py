from fastapi import APIRouter, Query, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal, ProductionPerformance  # Corrected import
import pandas as pd
from io import BytesIO
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
report_routes = APIRouter()

# Dependency to get database session
def get_db():
    """
    Dependency function to provide a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@report_routes.get(
    "/generate-production-performance-report",
    tags=["Reports"],
    summary="Generate Production Performance Report",
    description="Generate a production performance report and export it as JSON, CSV, or Excel."
)
async def generate_production_performance_report(
    export_format: str = Query("json", description="Export format: 'json', 'csv', or 'excel'"),
    db: Session = Depends(get_db)  # Use shared dependency
):
    """
    Generate a production performance report based on uploaded production data.
    """
    try:
        # Fetch all production performance records from the database
        result = db.query(ProductionPerformance).all()

        # Convert data to a list of dictionaries
        report_data = [
            {
                "machine": record.machine,
                "runtime_minutes": record.runtime_minutes,
                "planned_time_minutes": record.planned_time_minutes,
                "good_units": record.good_units,
                "total_units": record.total_units,
                "downtime_minutes": record.downtime_minutes
            }
            for record in result
        ]

        if not report_data:
            return {"message": "No production performance data available."}

        # Convert to pandas DataFrame
        df = pd.DataFrame(report_data)

        # Export report
        if export_format == "csv":
            output = BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return Response(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=production_performance_report.csv"}
            )
        elif export_format == "excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Production Performance")
            output.seek(0)
            return Response(
                content=output.getvalue(),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=production_performance_report.xlsx"}
            )
        else:
            return {
                "message": "Generated production performance report.",
                "report": report_data
            }

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
