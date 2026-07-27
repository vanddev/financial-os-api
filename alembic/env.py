from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import settings
from app.core.database import Base

# Import every model so SQLAlchemy registers all tables in Base.metadata before
# Alembic compares the metadata with the database schema.
from app.modules.accounts import models as _accounts_models  # noqa: F401
from app.modules.assets import models as _assets_models  # noqa: F401
from app.modules.budgets import models as _budgets_models  # noqa: F401
from app.modules.categories import models as _categories_models  # noqa: F401
from app.modules.credit_cards import models as _credit_cards_models  # noqa: F401
from app.modules.goals import models as _goals_models  # noqa: F401
from app.modules.investments import models as _investments_models  # noqa: F401
from app.modules.loans import models as _loans_models  # noqa: F401
from app.modules.owners import models as _owners_models  # noqa: F401
from app.modules.settings import models as _settings_models  # noqa: F401
from app.modules.subscriptions import models as _subscriptions_models  # noqa: F401
from app.modules.transactions import models as _transactions_models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
