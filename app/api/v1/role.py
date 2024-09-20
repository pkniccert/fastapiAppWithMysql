from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models import Role  # Import your SQLAlchemy Role model
from app.schemas.role import RoleCreate, RoleResponse  # Import your Pydantic models
from app.db.database import get_db  # Assuming you have a function to get DB sessions
from app.utils.successResponse import success_response
from app.utils.handle_db_error import handle_db_error

router = APIRouter()

@router.post("/create", response_model=RoleResponse)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
 try:
    # Create a new Role instance from the Pydantic model
        db_role = Role(**role.dict())
        
        # Use synchronous methods
        db.add(db_role)
        db.commit()
        db.refresh(db_role)

       # Convert SQLAlchemy model to Pydantic model
        role_response = RoleResponse.from_orm(db_role)

        # Convert datetime fields to ISO format strings
        role_response_dict = role_response.dict()
        role_response_dict['created_at'] = role_response.created_at.isoformat()
        role_response_dict['updated_at'] = role_response.updated_at.isoformat()

        return success_response(role_response_dict)

 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(role_id: int, db: Session = Depends(get_db)):
 try:
    stmt = select(Role).where(Role.id == role_id)
    result = db.execute(stmt)
    role = result.scalars().first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
   
    # Convert SQLAlchemy model to Pydantic model
    role_response = RoleResponse.from_orm(role)

    # Convert datetime fields to ISO format strings
    role_response_dict = role_response.dict()
    role_response_dict['created_at'] = role_response.created_at.isoformat()
    role_response_dict['updated_at'] = role_response.updated_at.isoformat()

    return success_response(role_response_dict)
    
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
