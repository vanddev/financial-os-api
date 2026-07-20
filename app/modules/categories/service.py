from sqlalchemy.orm import Session
from app.core.exceptions import AppException

from app.modules.categories import models, repository, schemas


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.CategoryRepository(db)

    def create(self, payload: schemas.CategoryCreate) -> models.Category:
        cat = models.Category(name=payload.name, color=payload.color, icon=payload.icon, type=payload.type)
        if payload.subcategories:
            cat.subcategories = [models.Subcategory(name=s.name) for s in payload.subcategories]
        return self.repo.create(cat)

    def get(self, category_id: int) -> models.Category:
        c = self.repo.get(category_id)
        if not c:
            raise AppException("Category not found")
        return c

    def list(self, page: int = 1, page_size: int = 20, sort: str = "id", order: str = "asc"):
        skip = (page - 1) * page_size
        items, total = self.repo.list(skip=skip, limit=page_size, sort=sort, order=order)
        return items, total

    def update(self, category_id: int, payload: schemas.CategoryUpdate) -> models.Category:
        c = self.get(category_id)
        c.name = payload.name
        c.color = payload.color
        c.icon = payload.icon
        c.type = payload.type
        return self.repo.update(c)

    def delete(self, category_id: int) -> None:
        c = self.get(category_id)
        self.repo.delete(c)
