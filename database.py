from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database connection string
SQLALCHEMY_DATABASE_URL = "sqlite:///./analytics.db"  # Updated for clarity

# Initialize the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# ProductionPerformance Table
class ProductionPerformance(Base):
    __tablename__ = "production_performance"

    id = Column(Integer, primary_key=True, index=True)
    machine = Column(String, nullable=False)
    runtime_minutes = Column(Float, nullable=False)
    planned_time_minutes = Column(Float, nullable=False)
    good_units = Column(Integer, nullable=False)
    total_units = Column(Integer, nullable=False)
    downtime_minutes = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# UploadedFileLog Table
class UploadedFileLog(Base):
    __tablename__ = "uploaded_file_logs"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False)
    processed_rows = Column(Integer, default=0)
    skipped_rows = Column(Integer, default=0)
    validation_errors = Column(String, nullable=True)

# KPIRecord Table (Assumed Definition)
class KPIRecord(Base):
    __tablename__ = "kpi_records"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    availability = Column(Float, nullable=False)
    performance = Column(Float, nullable=False)
    quality = Column(Float, nullable=False)
    oee = Column(Float, nullable=False)

# Function to initialize the database and create tables
def init_db():
    """
    Initialize the database and create tables if they don't already exist.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
