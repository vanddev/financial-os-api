from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):  # noqa: UP046
    success: bool = True
    data: T


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: dict[str, Any] | None = None
