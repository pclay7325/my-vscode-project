from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from dependencies import get_db
from models import TableField, UserTable
from pydantic import BaseModel
from typing import Dict

schema_routes = APIRouter()

class SchemaMappingRequest(BaseModel):
    mappings: Dict[str, str]  # Customer columns mapped to internal columns

@schema_routes.post("/schema-mapping/")
def save_schema_mapping(
    request: SchemaMappingRequest,  # Required first (no default value)
    table_id: int = Query(..., description="The ID of the table to map"),  # Default value after
    db: Session = Depends(get_db)
):
    """
    Save customer-specific schema mapping for data ingestion.
    """
    # Check if the table_id exists
    table = db.query(UserTable).filter(UserTable.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table ID not found")

    try:
        # Process and insert each mapping
        for customer_field, internal_field in request.mappings.items():
            mapping = TableField(
                table_id=table_id,
                field_name=customer_field,
                field_type=internal_field  # Use the value of the dictionary as field_type
            )
            db.add(mapping)
        db.commit()

        return {"message": "Schema mapping saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
