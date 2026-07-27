from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    422: "validation_error",
    429: "rate_limit_exceeded",
}


class AppException(Exception):  # noqa: N818
    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        code: str | None = None,
        details: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code or error_code_for_status(status_code)
        self.details = details
        self.headers = headers
        super().__init__(message)


def error_code_for_status(status_code: int) -> str:
    if status_code in ERROR_CODES:
        return ERROR_CODES[status_code]
    if status_code >= 500:
        return "internal_server_error"
    return "http_error"


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | list[dict[str, Any]] | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "code": code,
            "message": message,
            "details": details,
            "request_id": _request_id(request),
        },
        headers=headers,
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return error_response(
        request,
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
        headers=exc.headers,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    default_message = HTTPStatus(exc.status_code).phrase
    details: dict[str, Any] | list[dict[str, Any]] | None = None
    if isinstance(exc.detail, str):
        message = exc.detail
    elif isinstance(exc.detail, dict):
        message = str(exc.detail.get("message") or default_message)
        details = exc.detail
    elif isinstance(exc.detail, list):
        message = default_message
        details = exc.detail
    else:
        message = default_message
    return error_response(
        request,
        status_code=exc.status_code,
        code=error_code_for_status(exc.status_code),
        message=message,
        details=details,
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    invalid_json = any(error.get("type") == "json_invalid" for error in errors)
    status_code = (
        status.HTTP_400_BAD_REQUEST if invalid_json else status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    details = [
        {
            "field": ".".join(str(part) for part in error.get("loc", ())) or None,
            "message": error.get("msg", "Invalid value"),
            "type": error.get("type"),
            "context": error.get("ctx"),
        }
        for error in errors
    ]
    return error_response(
        request,
        status_code=status_code,
        code="invalid_json" if invalid_json else "validation_error",
        message="Malformed JSON body" if invalid_json else "Request validation failed",
        details=details,
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    return error_response(
        request,
        status_code=status.HTTP_409_CONFLICT,
        code="conflict",
        message="The request conflicts with the current resource state",
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return error_response(
        request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="internal_server_error",
        message="Internal server error",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(IntegrityError, integrity_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, general_exception_handler)
