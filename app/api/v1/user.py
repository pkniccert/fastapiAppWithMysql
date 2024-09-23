from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserCheckInDB
from app.models import User
from app.utils.successResponse import success_response
from app.utils.handle_db_error import handle_db_error
from app.core.auth_service import AuthService
from app.dependencies.current_user import get_current_user
from typing import Dict

router = APIRouter()
auth_service = AuthService()
@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # sourcery skip: raise-from-previous-error
    try:
        db_user = User(
            first_name= user.first_name,
            middle_name= user.middle_name,
            last_name= user.last_name,
            email=user.email,
            username=user.username,
            password=auth_service.get_password_hash(user.password),
            role_id= user.role_id,
            status= user.status
        )
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
        raise handle_db_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.post("/login")
async def login(form_data: UserCheckInDB, db: Session = Depends(get_db)) -> Dict[str, str]:
    # sourcery skip: raise-from-previous-error
    try:
        # Use the query method to filter by username
        user = db.query(User).filter(User.username == form_data.username).first()

        if user is None or not auth_service.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        # Create and return access token
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return {"status": "success", "access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session in case of an error
        raise handle_db_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/me")
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return {"status": "success", "data": current_user}

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # sourcery skip: raise-from-previous-error
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
        raise handle_db_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
