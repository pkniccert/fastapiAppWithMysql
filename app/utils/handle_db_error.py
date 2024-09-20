from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from fastapi import HTTPException
import logging

logger = logging.getLogger("uvicorn.error")

def handle_db_error(e: SQLAlchemyError) -> HTTPException:
    error_message = str(e.__cause__) if e.__cause__ else str(e)

    # Log the error for debugging
    logger.error(f"Database error: {error_message}")

    # Check for specific error types
    if isinstance(e, IntegrityError):
        return HTTPException(status_code=400, detail="Integrity constraint violation.")
    elif isinstance(e, OperationalError):
        return HTTPException(status_code=500, detail="Operational error, please try again.")
    elif "unique constraint" in error_message.lower():
        return HTTPException(status_code=400, detail="Unique constraint violation.")
    elif "foreign key constraint" in error_message.lower():
        return HTTPException(status_code=400, detail="Foreign key constraint violation.")
    else:
        return HTTPException(status_code=500, detail=f"Database error occurred: {error_message}")
