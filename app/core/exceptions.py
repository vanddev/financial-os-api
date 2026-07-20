from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):  # noqa: N818
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": exc.message,
            "details": exc.details,
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    content: dict[str, Any] = {
        "success": False,
        "message": "Internal server error",
        "details": {},
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )
