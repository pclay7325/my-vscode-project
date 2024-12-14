from models import Base, engine

# Ensure database tables are created
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
