import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .models.base import Base
import asyncio

# Build the database URL
DATABASE_URL = (
    f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

async def init():
    async with engine.begin() as conn:
        # Drop all tables (useful for development)
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized!")

async def main():
    try:
        await init()
    finally:
        await engine.dispose()  # Ensure the engine is disposed of properly

if __name__ == "__main__":
    asyncio.run(main())