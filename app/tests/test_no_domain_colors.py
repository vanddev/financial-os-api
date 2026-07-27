from app.core.database import Base
from app.main import app


def _property_names(value: object) -> set[str]:
    if isinstance(value, dict):
        names = set(value.get("properties", {}))
        for child in value.values():
            names.update(_property_names(child))
        return names
    if isinstance(value, list):
        names: set[str] = set()
        for child in value:
            names.update(_property_names(child))
        return names
    return set()


def test_domain_tables_have_no_color_columns() -> None:
    for table_name in ("accounts", "categories", "credit_cards", "goals"):
        assert "color" not in Base.metadata.tables[table_name].columns


def test_openapi_has_no_color_fields() -> None:
    assert "color" not in _property_names(app.openapi())
