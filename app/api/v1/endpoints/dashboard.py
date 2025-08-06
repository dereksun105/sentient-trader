"""
Sentient Trader - 儀表板 API 端點
提供儀表板所需的聚合數據
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.models.schemas import DashboardData, RealTimeUpdate

logger = structlog.get_logger()
router = APIRouter()


@router.get("/overview", response_model=DashboardData)
async def get_dashboard_overview(
    db: Session = Depends(get_db)
):
    """
    獲取儀表板概覽數據
    """
    # TODO: 實現儀表板服務
    return {
        "recent_posts": [],
        "sentiment_summary": {
            "total_posts": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "average_sentiment": 0.0,
            "sentiment_trend": []
        },
        "top_kols": [],
        "market_alerts": [],
        "correlation_insights": []
    }


@router.get("/realtime")
async def get_realtime_updates(
    db: Session = Depends(get_db)
):
    """
    獲取即時更新數據
    """
    # TODO: 實現即時更新服務
    return {"updates": []} 