from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./analytics.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

class KPIRecord(Base):
    __tablename__ = "kpi_records"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    availability = Column(Float)
    performance = Column(Float)
    quality = Column(Float)
    oee = Column(Float)
    downtime_percentage = Column(Float)
    utilization_percentage = Column(Float)
    yield_percentage = Column(Float)
    throughput = Column(Float)

Base.metadata.create_all(bind=engine)
