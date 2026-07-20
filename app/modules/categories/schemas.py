from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SubcategoryBase(BaseModel):
    name: str


class SubcategoryCreate(SubcategoryBase):
    pass


class SubcategoryOut(SubcategoryBase):
    id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    name: str
    color: str | None = None
    icon: str | None = None
    type: str


class CategoryCreate(CategoryBase):
    subcategories: list[SubcategoryCreate] | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    icon: str | None = None
    type: str | None = None


class CategoryOut(CategoryBase):
    id: int
    subcategories: list[SubcategoryOut] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
