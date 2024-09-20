from pydantic import BaseModel

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionCreate(RolePermissionBase):
    pass  # You can add any validation or default values if needed

class RolePermissionResponse(RolePermissionBase):
    
    class Config:
        orm_mode = True  # Allow ORM models
        from_attributes = True  # Allow usage of from_orm
