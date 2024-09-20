from fastapi import APIRouter

# Import routers from respective modules
from .user import router as user_router
from .role import router as role_router
from .permission import router as permission_router
from .role_permission import router as role_permission_router

# Create a main router to include all routers
main_router = APIRouter()

# Include all sub-routers
main_router.include_router(user_router, prefix="/users", tags=["users"])
# main_router.include_router(role_router, prefix="/roles", tags=["roles"])
# main_router.include_router(permission_router, prefix="/permissions", tags=["permissions"])
# main_router.include_router(role_permission_router, prefix="/role-permissions", tags=["role-permissions"])
