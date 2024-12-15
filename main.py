from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from routes.upload_routes import upload_routes
from routes.report_routes import report_routes
from routes.schema_routes import schema_routes
from database import SessionLocal, init_db  # Ensure init_db is called
from models import KPIRecord
from pydantic import BaseModel
from routes.schema_routes import schema_routes


import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Manufacturing Analytics Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the database
init_db()

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
@app.get("/", tags=["Root"], summary="Welcome Endpoint")
def read_root():
    """
    Root endpoint with welcome message.
    """
    return {"message": "Welcome to the Manufacturing Analytics Backend!"}

# Health Check Endpoint
@app.get("/health", tags=["Health"], summary="Health Check")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify database connectivity.
    """
    try:
        # Perform a simple query to verify DB connection
        db.execute("SELECT 1")
        return {"status": "Healthy", "message": "Database connection is active."}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Pydantic model for input validation (moved to schemas.py for maintainability)
class KPIRecordInput(BaseModel):
    file_id: str
    availability: float
    performance: float
    quality: float
    oee: float

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
        logger.error(f"Failed to fetch records: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch KPI records")

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
        logger.error(f"Filter operation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Filter operation failed")

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
        db.refresh(new_record)
        return {"message": "Record added successfully", "record_id": new_record.file_id}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add record: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add KPI record")
