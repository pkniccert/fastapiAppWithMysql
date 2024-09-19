from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.dependencies.status import Status

# Pydantic model for user creation
class UserCreate(BaseModel):
    first_name: str
    middle_name: str = None
    last_name: str = None
    username: str
    email: EmailStr
    password: str
    role_id: int
    status: Status = Status.active  # Default to active status

# Pydantic model for user response
class UserResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str = None
    last_name: str = None
    username: str
    email: EmailStr
    role_id: int
    status: Status
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated from 'orm_mode' to 'from_attributes'
        
