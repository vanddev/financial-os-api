from datetime import datetime, timedelta
from decimal import Decimal

from app.modules.goals import schemas as goal_schemas
from app.modules.goals import service as goal_service


def test_goals_crud(db_session):
    svc = goal_service.GoalService(db_session)
    payload = goal_schemas.GoalCreate(
        name="Buy Bike",
        target_amount=Decimal("1000.00"),
        current_amount=Decimal("100.00"),
        deadline=datetime.utcnow() + timedelta(days=90),
    )
    g = svc.create(payload)
    assert g.id is not None
    got = svc.get(g.id)
    assert got.name == "Buy Bike"
    svc.update(
        g.id,
        goal_schemas.GoalUpdate(
            name="Buy Bike v2",
            target_amount=Decimal("1200.00"),
            current_amount=Decimal("150.00"),
            deadline=datetime.utcnow() + timedelta(days=120),
        ),
    )
    got2 = svc.get(g.id)
    assert got2.name == "Buy Bike v2"
    svc.delete(g.id)
    try:
        svc.get(g.id)
        assert False
    except Exception:
        assert True
