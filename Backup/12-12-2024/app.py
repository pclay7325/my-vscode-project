from fastapi import FastAPI
from routes import upload_routes, report_routes

app = FastAPI()

# Include routes for upload and report
app.include_router(upload_routes)
app.include_router(report_routes)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Manufacturing Analytics Backend!"}
