from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserInDB, UserResponse
from app.models import User
from app.utils.successResponse import success_response
from app.utils.handle_db_error import handle_db_error
from app.core.auth_service import AuthService
from typing import Dict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_service = AuthService()
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserInDB:
    try:
        # Verify the token and extract the payload
        payload = auth_service.verify_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Query the user from the database using query()
        user = db.execute(
            db.query(User).filter(User.username == payload["sub"])
        )
        user = user.scalars().first()

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Return user as UserInDB schema
        user_response = UserResponse.from_orm(user)

        # Convert datetime fields to ISO format strings
        user_response_dict = user_response.dict()
        user_response_dict['created_at'] = user_response.created_at.isoformat()
        user_response_dict['updated_at'] = user_response.updated_at.isoformat()

        return user_response_dict

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session
        raise handle_db_error(e) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

