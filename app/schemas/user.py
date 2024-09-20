from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from app.dependencies.status import Status

# Pydantic model for user creation
class UserCreate(BaseModel):
    first_name: str
    middle_name: str = None
    last_name: str = None
    username: str
    email: EmailStr
    password: str = Field(min_length=8)  # Ensure password is at least 8 characters long
    role_id: int
    status: Status = Status.active  # Default to active status

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @validator('role_id')
    def validate_role_id(cls, v):
        if v <= 0:
            raise ValueError('Role ID must be a positive integer')
        return v

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
        orm_mode = True  # Allow ORM models
        from_attributes = True  # Allow usage of from_orm
