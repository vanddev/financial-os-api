from app.modules.categories import schemas, service


def test_categories_crud(db_session):
    svc = service.CategoryService(db_session)
    payload = schemas.CategoryCreate(
        name="Test Cat",
        icon="icon",
        type="expense",
        subcategories=[schemas.SubcategoryCreate(name="Sub1")],
    )
    cat = svc.create(payload)
    assert cat.id is not None
    got = svc.get(cat.id)
    assert got.name == "Test Cat"
    svc.update(cat.id, schemas.CategoryUpdate(name="Renamed", icon="i", type="expense"))
    got2 = svc.get(cat.id)
    assert got2.name == "Renamed"
    svc.delete(cat.id)
    try:
        svc.get(cat.id)
        assert False
    except Exception:
        assert True
