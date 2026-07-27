from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    general_exception_handler,
)
from app.core.lifespan import lifespan
from app.modules.accounts import router as accounts_router
from app.modules.ai import router as ai_router
from app.modules.analytics import router as analytics_router
from app.modules.assets import router as assets_router
from app.modules.budgets import router as budgets_router
from app.modules.categories import router as categories_router
from app.modules.credit_cards import router as credit_cards_router
from app.modules.dashboard import router as dashboard_router
from app.modules.goals import router as goals_router
from app.modules.health import router as health_router
from app.modules.investments import router as investments_router
from app.modules.loans import router as loans_router
from app.modules.networth import router as net_worth_router
from app.modules.owners import router as owners_router
from app.modules.settings import router as settings_router
from app.modules.subscriptions import router as subscriptions_router
from app.modules.transactions import router as transactions_router
from app.shared.middleware import LoggingMiddleware, setup_cors

app = FastAPI(
    title=settings.APP_NAME,
    description="Personal Finance Platform",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

setup_cors(app)
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(health_router)
app.include_router(accounts_router)
app.include_router(analytics_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(credit_cards_router)
app.include_router(budgets_router)
app.include_router(goals_router)
app.include_router(subscriptions_router)
app.include_router(assets_router)
app.include_router(investments_router)
app.include_router(loans_router)
app.include_router(settings_router)
app.include_router(net_worth_router)
app.include_router(owners_router)
app.include_router(dashboard_router)
app.include_router(ai_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }
