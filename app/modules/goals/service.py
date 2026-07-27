from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.goals import models, repository, schemas


class GoalService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.GoalRepository(db)

    def create(self, payload: schemas.GoalCreate) -> models.Goal:
        if payload.target_amount < 0:
            raise AppException("Target amount cannot be negative")
        if payload.current_amount and payload.current_amount < 0:
            raise AppException("Current amount cannot be negative")
        g = models.Goal(**payload.model_dump())
        return self.repo.create(g)

    def get(self, goal_id: int) -> models.Goal:
        g = self.repo.get(goal_id)
        if not g:
            raise AppException("Goal not found")
        return g

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        completed: bool | None = None,
        sort: str = "id",
        order: str = "asc",
    ):
        skip = (page - 1) * page_size
        items, total = self.repo.list(
            skip=skip, limit=page_size, completed=completed, sort=sort, order=order
        )
        return items, total

    def update(self, goal_id: int, payload: schemas.GoalUpdate) -> models.Goal:
        g = self.get(goal_id)
        for k, v in payload.model_dump().items():
            setattr(g, k, v)
        return self.repo.update(g)

    def delete(self, goal_id: int) -> None:
        g = self.get(goal_id)
        self.repo.delete(g)
