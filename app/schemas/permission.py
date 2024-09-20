from pydantic import BaseModel
from datetime import datetime
from app.dependencies.status import Status

# Pydantic model for permission creation
class PermissionCreate(BaseModel):
    name: str
    status: Status = Status.active  # Default to active status

# Pydantic model for permission response
class PermissionResponse(BaseModel):
    id: int
    name: str
    status: Status
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allow ORM models
        from_attributes = True  # Allow usage of from_orm
