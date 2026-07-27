from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):  # noqa: UP046
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    code: str
    message: str
    details: dict[str, Any] | list["ErrorDetail"] | None = None
    request_id: str | None = None


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str
    type: str | None = None
    context: dict[str, Any] | None = None


ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {
        "model": ErrorResponse,
        "description": "Malformed request or invalid request syntax.",
    },
    401: {
        "model": ErrorResponse,
        "description": "Authentication credentials are missing or invalid.",
    },
    403: {
        "model": ErrorResponse,
        "description": "The authenticated principal cannot perform this operation.",
    },
    404: {
        "model": ErrorResponse,
        "description": "The requested resource was not found.",
    },
    409: {
        "model": ErrorResponse,
        "description": "The request conflicts with the current resource state.",
    },
    422: {
        "model": ErrorResponse,
        "description": "The request is syntactically valid but failed validation.",
    },
    429: {
        "model": ErrorResponse,
        "description": "The request rate limit was exceeded.",
    },
    "5XX": {
        "model": ErrorResponse,
        "description": "An unexpected server or upstream service error occurred.",
    },
}


ErrorResponse.model_rebuild()
