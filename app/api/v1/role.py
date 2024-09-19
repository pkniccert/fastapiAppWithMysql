from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models import Role  # Import your SQLAlchemy Role model
from app.schemas.role import RoleCreate, RoleResponse  # Import your Pydantic models
from app.db.database import get_db  # Assuming you have a function to get DB sessions

router = FastAPI()

@router.post("/", response_model=RoleResponse)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
 try:
    db_role = Role(**role.dict())  # Create a new Role instance from the Pydantic model
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(role_id: int, db: Session = Depends(get_db)):
 try:
    stmt = select(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    role = result.scalars().first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
 except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
