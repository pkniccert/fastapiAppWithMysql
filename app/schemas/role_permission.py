from pydantic import BaseModel

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionCreate(RolePermissionBase):
    pass  # You can add any validation or default values if needed

class RolePermissionResponse(RolePermissionBase):
    
    class Config:
        from_attributes = True  # Updated from 'orm_mode' to 'from_attributes'
