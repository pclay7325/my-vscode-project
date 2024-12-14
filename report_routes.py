from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import KPIRecord
from sqlalchemy import func

report_routes = APIRouter()

@report_routes.get("/kpi-summary/")
def get_kpi_summary(db: Session = Depends(get_db)):
    """
    Fetch KPI summary statistics from the database.
    """
    try:
        # Aggregate KPIs from database
        summary = db.query(
            func.avg(KPIRecord.oee).label("average_oee"),
            func.avg(KPIRecord.downtime_percentage).label("average_downtime_percentage"),
            func.avg(KPIRecord.utilization_percentage).label("average_utilization_percentage"),
            func.avg(KPIRecord.yield_percentage).label("average_yield_percentage"),
            func.avg(KPIRecord.throughput).label("average_throughput")
        ).first()

        if not summary:
            return {"message": "No KPI data available"}

        return {
            "average_oee": round(summary.average_oee, 2) if summary.average_oee else 0,
            "average_downtime_percentage": round(summary.average_downtime_percentage, 2) if summary.average_downtime_percentage else 0,
            "average_utilization_percentage": round(summary.average_utilization_percentage, 2) if summary.average_utilization_percentage else 0,
            "average_yield_percentage": round(summary.average_yield_percentage, 2) if summary.average_yield_percentage else 0,
            "average_throughput": round(summary.average_throughput, 2) if summary.average_throughput else 0,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving KPI summary: {str(e)}")


@report_routes.get("/kpi-history/")
def get_kpi_history(db: Session = Depends(get_db)):
    """
    Fetch historical OEE data for the line chart.
    """
    try:
        # Query historical data from the database
        records = db.query(KPIRecord.timestamp, KPIRecord.oee).order_by(KPIRecord.timestamp).all()

        if not records:
            raise HTTPException(status_code=404, detail="No historical data available")

        # Format data for the frontend
        timestamps = [record.timestamp.strftime("%Y-%m-%d") for record in records]
        values = [record.oee for record in records]

        return {"timestamps": timestamps, "values": values}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving historical data: {str(e)}")
