from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///./analytics.db"  # Adjust the URL if necessary
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ProductionPerformance model
class ProductionPerformance(Base):
    __tablename__ = "production_performance"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    machine = Column(String, nullable=False)  # Machine name
    runtime_minutes = Column(Integer, nullable=False)  # Runtime (minutes)
    planned_time_minutes = Column(Integer, nullable=False)  # Planned Time (minutes)
    good_units = Column(Integer, nullable=False)  # Good Units produced
    total_units = Column(Integer, nullable=False)  # Total Units produced
    downtime_minutes = Column(Integer, nullable=False)  # Downtime in minutes
