"""create db

Revision ID: 334e843a8cb4
Revises:
Create Date: 2026-07-17 17:18:45.282768

"""

from collections.abc import Sequence

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

# revision identifiers, used by Alembic.
revision: str = "334e843a8cb4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
