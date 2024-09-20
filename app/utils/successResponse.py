from fastapi.responses import JSONResponse
def success_response(data: dict):
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": data
        }
    )