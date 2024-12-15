from database import Base, engine, ProductionPerformance  # Import WorkOrder model to register it with Base

# Create tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
