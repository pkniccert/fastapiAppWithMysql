from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models import Permission  # Import your SQLAlchemy Permission model
from app.schemas.permission import PermissionCreate, PermissionResponse  # Import your Pydantic models
from app.db.database import get_db  # Assuming you have a function to get DB sessions

router = FastAPI()

@router.post("/", response_model=PermissionResponse)
async def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
 try:
    db_permission = Permission(**permission.dict())  # Create a new Permission instance from the Pydantic model
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    return db_permission
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{permission_id}", response_model=PermissionResponse)
async def read_permission(permission_id: int, db: Session = Depends(get_db)):
 try:
    stmt = select(Permission).where(Permission.id == permission_id)
    result = await db.execute(stmt)
    permission = result.scalars().first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
