from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models import User
from app.utils.successResponse import success_response
from app.utils.handle_db_error import handle_db_error

router = APIRouter()

@router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
       # Convert SQLAlchemy model to Pydantic model
        user_response = UserResponse.from_orm(db_user)

        # Convert datetime fields to ISO format strings
        user_response_dict = user_response.dict()
        user_response_dict['created_at'] = user_response.created_at.isoformat()
        user_response_dict['updated_at'] = user_response.updated_at.isoformat()

        return success_response(user_response_dict)
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)  # Use the error handler
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
         # Convert SQLAlchemy model to Pydantic model
        user_response = UserResponse.from_orm(user)

        # Convert datetime fields to ISO format strings
        user_response_dict = user_response.dict()
        user_response_dict['created_at'] = user_response.created_at.isoformat()
        user_response_dict['updated_at'] = user_response.updated_at.isoformat()

        return success_response(user_response_dict)
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
