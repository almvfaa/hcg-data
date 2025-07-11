from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
from starlette.exceptions import HTTPException as StarletteHTTPException

class AppException(HTTPException):
    """Base exception class for application-specific exceptions"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Union[dict, None] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class RateLimitExceeded(AppException):
    """Raised when too many requests are made in a short time period"""
    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": "60"}
        )

async def http_exception_handler(request, exc):
    """Global exception handler for HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
        }
    )
