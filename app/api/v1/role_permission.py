from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models import RolePermission  # Import your SQLAlchemy RolePermission model
from app.schemas.role_permission import RolePermissionCreate, RolePermissionResponse  # Import your Pydantic models
from app.db.database import get_db  # Assuming you have a function to get DB sessions
from app.utils.successResponse import success_response
from app.utils.handle_db_error import handle_db_error

router = APIRouter()

@router.post("/create", response_model=RolePermissionResponse)
async def create_role_permission(role_permission: RolePermissionCreate, db: Session = Depends(get_db)):
 try:
    db_role_permission = RolePermission(**role_permission.dict())  # Create a new RolePermission instance from the Pydantic model
    db.add(db_role_permission)
    db.commit()
    db.refresh(db_role_permission)
    # Convert SQLAlchemy model to Pydantic model
    role_permission_response = RolePermissionResponse.from_orm(db_role_permission)

    # Convert datetime fields to ISO format strings
    role_permission_response_dict = role_permission_response.dict()
   
    return success_response(role_permission_response_dict)
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{role_id}/{permission_id}", response_model=RolePermissionResponse)
async def read_role_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
 try:
    stmt = select(RolePermission).where(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == permission_id
    )
    result = db.execute(stmt)
    role_permission = result.scalars().first()
    if role_permission is None:
        raise HTTPException(status_code=404, detail="RolePermission not found")
    # Convert SQLAlchemy model to Pydantic model
    role_permission_response = RolePermissionResponse.from_orm(role_permission)

    # Convert datetime fields to ISO format strings
    role_permission_response_dict = role_permission_response.dict()

    return success_response(role_permission_response_dict)
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
