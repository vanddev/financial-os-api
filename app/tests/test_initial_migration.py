import ast
import importlib
from pathlib import Path

from app.core.database import Base

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODULES_ROOT = PROJECT_ROOT / "app" / "modules"
MIGRATIONS_ROOT = PROJECT_ROOT / "alembic" / "versions"


def _import_all_domain_models() -> None:
    for models_file in MODULES_ROOT.glob("*/models.py"):
        module_name = ".".join(models_file.relative_to(PROJECT_ROOT).with_suffix("").parts)
        importlib.import_module(module_name)


def _root_migration() -> ast.Module:
    root_migrations: list[ast.Module] = []

    for migration_file in MIGRATIONS_ROOT.glob("*.py"):
        migration = ast.parse(migration_file.read_text())
        for statement in migration.body:
            if not isinstance(statement, ast.AnnAssign):
                continue
            if not isinstance(statement.target, ast.Name):
                continue
            if statement.target.id != "down_revision":
                continue
            if isinstance(statement.value, ast.Constant) and statement.value.value is None:
                root_migrations.append(migration)

    assert len(root_migrations) == 1, "Expected exactly one root migration"
    return root_migrations[0]


def _created_tables(migration: ast.Module) -> set[str]:
    tables: set[str] = set()

    for node in ast.walk(migration):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute):
            continue
        if not isinstance(node.func.value, ast.Name):
            continue
        if node.func.value.id != "op" or node.func.attr != "create_table":
            continue
        if node.args and isinstance(node.args[0], ast.Constant):
            tables.add(node.args[0].value)

    return tables


def test_initial_migration_creates_every_domain_table() -> None:
    _import_all_domain_models()

    assert _created_tables(_root_migration()) == set(Base.metadata.tables)
