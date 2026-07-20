"""Create tables omitted by the initial no-op migration.

Revision ID: repair_missing_schema
Revises: 334e843a8cb4
"""

from alembic import op
from app.core.database import Base
from app.modules.accounts import models as _accounts_models  # noqa: F401
from app.modules.assets import models as _assets_models  # noqa: F401
from app.modules.budgets import models as _budgets_models  # noqa: F401
from app.modules.categories import models as _categories_models  # noqa: F401
from app.modules.credit_cards import models as _credit_cards_models  # noqa: F401
from app.modules.goals import models as _goals_models  # noqa: F401
from app.modules.investments import models as _investments_models  # noqa: F401
from app.modules.loans import models as _loans_models  # noqa: F401
from app.modules.settings import models as _settings_models  # noqa: F401
from app.modules.subscriptions import models as _subscriptions_models  # noqa: F401
from app.modules.transactions import models as _transactions_models  # noqa: F401

revision = "repair_missing_schema"
down_revision = "334e843a8cb4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
