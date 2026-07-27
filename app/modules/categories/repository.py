from typing import List as _List
from sqlalchemy.orm import Session

from app.modules.categories import models


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, category_id: int) -> models.Category | None:
        return self.db.query(models.Category).filter(models.Category.id == category_id).first()

    def list(
        self, skip: int = 0, limit: int = 20, sort: str = "id", order: str = "asc"
    ) -> tuple[_List[models.Category], int]:
        q = self.db.query(models.Category)
        total = q.count()
        if order.lower() == "desc":
            q = q.order_by(getattr(models.Category, sort).desc())
        else:
            q = q.order_by(getattr(models.Category, sort))
        items = q.offset(skip).limit(limit).all()
        return items, total

    def create(self, category: models.Category) -> models.Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: models.Category) -> models.Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: models.Category) -> None:
        self.db.delete(category)
        self.db.commit()
