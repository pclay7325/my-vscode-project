from fastapi import APIRouter

schema_routes = APIRouter()

@schema_routes.get("/schemas", tags=["Schemas"])
def get_schemas():
    return {"message": "Schemas endpoint placeholder"}
