from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .api import v1_router
from .middleware.auth import AuthMiddleware

app = FastAPI()


app.add_middleware(AuthMiddleware)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "errors": [
                {
                    "field": error['loc'][-1],
                    "message": error['msg'],
                    "input": error['input'],
                }
                for error in exc.errors()
            ],
        },
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
        },
    )

@app.get("/")
async def read_get():
    return {"status":"success", "message": "This is test route"}

# Include the main router with a prefix
app.include_router(v1_router)
