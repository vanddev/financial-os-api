from datetime import datetime

from pydantic import BaseModel, ConfigDict

class SubCategoryDTO(BaseModel):
    id: int
    category_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class CategoryDTO(BaseModel):
    id: int
    name: str
    color: str
    icon: str
    type: str
    created_at: datetime
    updated_at: datetime
    subcategories: list[SubCategoryDTO] = []
    model_config = ConfigDict(from_attributes=True)
