from app.modules.dashboard.router import get_dashboard_cashflow_trend


def test_cashflow_trend_returns_thirty_days() -> None:
    data = get_dashboard_cashflow_trend(None)["data"]
    assert len(data) == 30
    assert data[0]["day"] == 1
    assert data[-1]["day"] == 30
