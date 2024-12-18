from fastapi import FastAPI, HTTPException
from routes.upload_routes import upload_routes
from routes.report_routes import report_routes
from routes.auth_routes import auth_routes
import os

# Verify required environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise HTTPException(status_code=500, detail="SECRET_KEY is not configured.")

print("Environment variables loaded successfully.")

# Initialize FastAPI app
app = FastAPI(
    title="Manufacturing Analytics API",
    description="API for managing manufacturing analytics, including data upload, reporting, and authentication.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include routers with prefixes
app.include_router(upload_routes, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(report_routes, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(auth_routes, tags=["Authentication"])

@app.get("/", summary="Root Endpoint", tags=["Root"])
async def root():
    return {"message": "Welcome to the Manufacturing Analytics API"}
