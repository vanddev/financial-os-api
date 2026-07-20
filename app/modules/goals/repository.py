from typing import List as _List
from sqlalchemy.orm import Session

from app.modules.goals import models


class GoalRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, goal_id: int) -> models.Goal | None:
        return self.db.query(models.Goal).filter(models.Goal.id == goal_id).first()

    def list(self, skip: int = 0, limit: int = 20, completed: bool | None = None, sort: str = "id", order: str = "asc") -> tuple[_List[models.Goal], int]:
        q = self.db.query(models.Goal)
        if completed is not None:
            q = q.filter(models.Goal.completed == completed)
        total = q.count()
        if order.lower() == "desc":
            q = q.order_by(getattr(models.Goal, sort).desc())
        else:
            q = q.order_by(getattr(models.Goal, sort))
        items = q.offset(skip).limit(limit).all()
        return items, total

    def create(self, goal: models.Goal) -> models.Goal:
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def update(self, goal: models.Goal) -> models.Goal:
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def delete(self, goal: models.Goal) -> None:
        self.db.delete(goal)
        self.db.commit()
