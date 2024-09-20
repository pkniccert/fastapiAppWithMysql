# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
# Database URL
DATABASE_URL = (
    f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()