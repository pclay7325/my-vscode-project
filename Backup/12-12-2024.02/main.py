from fastapi import FastAPI
from upload_routes import upload_routes
from report_routes import report_routes

app = FastAPI()
app.include_router(upload_routes, prefix="/api")
app.include_router(report_routes, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Manufacturing Analytics Backend!"}
