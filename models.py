from sqlalchemy import (
    create_engine, Column, Float, String, DateTime, Integer, ForeignKey, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database configuration
DATABASE_URL = "sqlite:///./analytics.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

# Model definitions
class KPIRecord(Base):
    """
    Stores Key Performance Indicator (KPI) records for analytics.
    """
    __tablename__ = "kpi_records"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    availability = Column(Float)
    performance = Column(Float)
    quality = Column(Float)
    oee = Column(Float)  # Overall Equipment Effectiveness
    downtime_percentage = Column(Float)
    utilization_percentage = Column(Float)
    yield_percentage = Column(Float)
    throughput = Column(Float)
    scrapped_parts = Column(Integer, default=0)
    standard_cost = Column(Float, default=0)
    profit_per_part = Column(Float, default=0)
    planned_downtime = Column(Float, default=0)
    unplanned_downtime = Column(Float, default=0)

class WidgetDefinition(Base):
    """
    Defines widgets for dashboards with configurable options and validation.
    """
    __tablename__ = "widget_definitions"

    id = Column(Integer, primary_key=True, index=True)
    widget_type = Column(String, index=True)  # Example: "Text", "Number"
    label = Column(String, nullable=False)
    options = Column(JSON, nullable=True)  # Options for dropdowns or multiselects
    validation_rules = Column(JSON, nullable=True)  # Validation logic for inputs

class UserTable(Base):
    """
    Stores metadata about user-created tables.
    """
    __tablename__ = "user_tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to fields and data
    fields = relationship("TableField", back_populates="user_table")
    data = relationship("TableData", back_populates="user_table")

class TableField(Base):
    """
    Defines the schema (fields) for user-created tables.
    """
    __tablename__ = "table_fields"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("user_tables.id"))
    field_name = Column(String, nullable=False)
    field_type = Column(String, nullable=False)  # Example: "Text", "Number"

    # Relationship to parent table
    user_table = relationship("UserTable", back_populates="fields")

class TableData(Base):
    """
    Stores data rows for user-created tables.
    """
    __tablename__ = "table_data"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("user_tables.id"))
    data = Column(JSON, nullable=False)  # Stores row data as JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to parent table
    user_table = relationship("UserTable", back_populates="data")

# Create all tables in the database
Base.metadata.create_all(bind=engine)
