"""
Sentient Trader - API 路由主入口點
整合所有 API 端點
"""

from fastapi import APIRouter

from app.api.v1.endpoints import kols, posts, sentiment, stocks, alerts, correlations, dashboard, auth, users

# 建立主 API 路由器
api_router = APIRouter()

# 包含所有子路由
api_router.include_router(
    kols.router,
    prefix="/kols",
    tags=["KOLs"]
)

api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["Social Media Posts"]
)

api_router.include_router(
    sentiment.router,
    prefix="/sentiment",
    tags=["Sentiment Analysis"]
)

api_router.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["Stock Data"]
)

api_router.include_router(
    alerts.router,
    prefix="/alerts",
    tags=["Alerts"]
)

api_router.include_router(
    correlations.router,
    prefix="/correlations",
    tags=["Correlation Analysis"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
) 

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)