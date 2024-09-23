from fastapi import HTTPException, Request, Depends, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.auth_service import AuthService

auth_service = AuthService()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define public routes
        public_routes = {"/api/v1/users/login", "/api/v1/users/register"}  # Example of public routes

        # If the request path is public, skip authentication
        if request.url.path in public_routes:
            response = await call_next(request)
            return response
        # Extract token from the Authorization header
        token = request.headers.get("Authorization")
        
        # If token is missing, raise an error
        if not token:
            return JSONResponse(
                content={"status": "error", "message": "Authorization token is missing"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = token.replace("Bearer ", "", 1)  # Remove "Bearer " prefix

        try:
            # Verify the token and attach user info to request state
            payload = auth_service.verify_token(token)
            request.state.user = payload
        except HTTPException as e:
            # Return JSON response with specific error message from the exception
            return JSONResponse(
                content={"status": "error", "message": str(e.detail)},
                status_code=e.status_code
            )
        except Exception:
            # Catch any other exceptions and return a generic 401 response
            return JSONResponse(
                content={"status": "error", "message": "User Unauthorized"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Proceed with the request if the token is valid
        response = await call_next(request)
        return response
