from pydantic import BaseModel
from datetime import datetime
from app.dependencies.status import Status
from typing import List, Optional

# Pydantic model for role creation
class RoleCreate(BaseModel):
    name: str
    status: Status = Status.active  # Default to active status

# Pydantic model for role response
class RoleResponse(BaseModel):
    id: int
    name: str
    status: Status
    created_at: datetime
    updated_at: datetime
    permissions: List[str] = []  # Include permissions if needed

    class Config:
        orm_mode = True  # Allow ORM models
        from_attributes = True  # Allow usage of from_orm
