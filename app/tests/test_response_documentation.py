from app.main import app


def test_financial_get_responses_have_detailed_openapi_schemas():
    paths = app.openapi()["paths"]
    expected_paths = [
        "/assets/",
        "/assets/{asset_id}",
        "/investments/",
        "/investments/{investment_id}",
        "/investments/allocation",
        "/investments/performance",
        "/investments/dividends",
        "/loans/",
        "/loans/{loan_id}",
        "/loans/{loan_id}/amortization",
        "/dashboard/summary",
        "/dashboard/monthly-flow",
        "/dashboard/cashflow-trend",
        "/dashboard/expense-breakdown",
        "/budgets/",
        "/budgets/{budget_id}",
        "/dashboard/cashflow-calendar",
        "/net-worth/series",
        "/net-worth/breakdown",
        "/accounts/{account_id}/balance-history",
        "/accounts/{account_id}/transactions",
        "/credit-cards/installments",
        "/credit-cards/{card_id}/spending-history",
        "/credit-cards/{card_id}/category-breakdown",
        "/credit-cards/{card_id}/biggest-purchases",
    ]

    for path in expected_paths:
        schema = paths[path]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        response_schema = app.openapi()["components"]["schemas"][schema["$ref"].split("/")[-1]]
        assert response_schema["properties"]["data"] != {"type": "string"}


def test_net_worth_openapi_data_structures_are_explicit():
    openapi = app.openapi()
    paths = openapi["paths"]
    schemas = openapi["components"]["schemas"]

    assert "/kpis/" not in paths
    assert "/cash_flow/monthly" not in paths
    assert "/cash_flow/trend" not in paths
    assert "/dashboard/budget-progress" not in paths

    assert set(paths["/budgets/"].keys()) == {"get", "post"}
    assert set(paths["/budgets/{budget_id}"].keys()) == {"delete", "get", "put"}

    series_schema = schemas[
        paths["/net-worth/series"]["get"]["responses"]["200"]["content"]
        ["application/json"]["schema"]["$ref"].split("/")[-1]
    ]
    assert series_schema["properties"]["data"]["items"]["$ref"].endswith(
        "NetWorthSeriesItem"
    )

    breakdown_schema = schemas[
        paths["/net-worth/breakdown"]["get"]["responses"]["200"]["content"]
        ["application/json"]["schema"]["$ref"].split("/")[-1]
    ]
    breakdown_data_schema = schemas[
        breakdown_schema["properties"]["data"]["$ref"].split("/")[-1]
    ]
    assert set(breakdown_data_schema["properties"]) == {
        "accounts_total",
        "investments_total",
        "assets_total",
        "liabilities_total",
        "net_worth",
    }
