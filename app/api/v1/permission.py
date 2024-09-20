from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models import Permission  # Import your SQLAlchemy Permission model
from app.schemas.permission import PermissionCreate, PermissionResponse  # Import your Pydantic models
from app.db.database import get_db  # Assuming you have a function to get DB sessions
from app.utils.successResponse import success_response
from app.utils.handle_db_error import handle_db_error

router = APIRouter()

@router.post("/create", response_model=PermissionResponse)
async def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
 try:
    db_permission = Permission(**permission.dict())  # Create a new Permission instance from the Pydantic model
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    # Convert SQLAlchemy model to Pydantic model
    permission_response = PermissionResponse.from_orm(db_permission)

    # Convert datetime fields to ISO format strings
    permission_response_dict = permission_response.dict()
    permission_response_dict['created_at'] = permission_response.created_at.isoformat()
    permission_response_dict['updated_at'] = permission_response.updated_at.isoformat()

    return success_response(permission_response_dict)
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{permission_id}", response_model=PermissionResponse)
async def read_permission(permission_id: int, db: Session = Depends(get_db)):
 try:
    stmt = select(Permission).where(Permission.id == permission_id)
    result = db.execute(stmt)
    permission = result.scalars().first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    # Convert SQLAlchemy model to Pydantic model
    permission_response = PermissionResponse.from_orm(permission)

    # Convert datetime fields to ISO format strings
    permission_response_dict = permission_response.dict()
    permission_response_dict['created_at'] = permission_response.created_at.isoformat()
    permission_response_dict['updated_at'] = permission_response.updated_at.isoformat()

    return success_response(permission_response_dict)
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
