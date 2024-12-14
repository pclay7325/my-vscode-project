from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from upload_routes import upload_routes
from report_routes import report_routes
from schema_routes import schema_routes
from models import SessionLocal, KPIRecord
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers for modular API structure
app.include_router(upload_routes, prefix="/api")
app.include_router(report_routes, prefix="/api")
app.include_router(schema_routes, prefix="/api")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Manufacturing Analytics Backend!"}

# Retrieve all KPI records
@app.get("/api/kpi_records/", tags=["KPI Records"], summary="Get all KPI records")
def get_kpi_records(db: Session = Depends(get_db)):
    """
    Retrieve all KPI records from the database.
    """
    try:
        records = db.query(KPIRecord).all()
        return [
            {
                "file_id": r.file_id,
                "timestamp": r.timestamp,
                "availability": r.availability,
                "performance": r.performance,
                "quality": r.quality,
                "oee": r.oee,
            }
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch records: {str(e)}")

# Filter KPI records by minimum OEE
@app.get("/api/kpi_records/filter/", tags=["KPI Records"], summary="Filter KPI records by minimum OEE")
def filter_kpi_records(oee_min: float, db: Session = Depends(get_db)):
    """
    Filter KPI records based on a minimum OEE value.
    """
    try:
        records = db.query(KPIRecord).filter(KPIRecord.oee >= oee_min).all()
        if not records:
            return {"message": "No records found for the given filter"}
        return [
            {
                "file_id": r.file_id,
                "timestamp": r.timestamp,
                "availability": r.availability,
                "performance": r.performance,
                "quality": r.quality,
                "oee": r.oee,
            }
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filter operation failed: {str(e)}")

# Pydantic model for input validation
class KPIRecordInput(BaseModel):
    file_id: str
    availability: float
    performance: float
    quality: float
    oee: float

# Add a new KPI record
@app.post("/api/kpi_records/", tags=["KPI Records"], summary="Add a new KPI record")
def create_kpi_record(record: KPIRecordInput, db: Session = Depends(get_db)):
    """
    Add a new KPI record to the database.
    """
    try:
        # Validate OEE range
        if record.oee < 0 or record.oee > 100:
            raise HTTPException(status_code=400, detail="OEE must be between 0 and 100")

        # Create and commit new record
        new_record = KPIRecord(**record.dict())
        db.add(new_record)
        db.commit()
        return {"message": "Record added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add record: {str(e)}")
