from fastapi import APIRouter

# Import routers from respective modules
from .v1 import main_router

# Create a main router to include all routers
v1_router = APIRouter()

# Include all sub-routers
v1_router.include_router(main_router, prefix="/api/v1")
