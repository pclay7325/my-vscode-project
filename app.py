from fastapi import FastAPI
from routes.upload_routes import upload_routes
from routes.report_routes import report_routes

# Create FastAPI instance
app = FastAPI()

# Include routers
app.include_router(upload_routes, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(report_routes, prefix="/api/v1/report", tags=["Reports"])

@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Manufacturing Analytics Backend!"}
