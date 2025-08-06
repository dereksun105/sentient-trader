"""
Sentient Trader - 股票數據 API 端點
處理股票價格數據的查詢
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.models.schemas import StockPriceResponse

logger = structlog.get_logger()
router = APIRouter()


@router.get("/{symbol}/price", response_model=List[StockPriceResponse])
async def get_stock_prices(
    symbol: str,
    days: int = Query(30, ge=1, le=365, description="獲取天數"),
    db: Session = Depends(get_db)
):
    """
    獲取股票價格歷史數據
    """
    # TODO: 實現股票數據服務
    return []


@router.get("/{symbol}/current")
async def get_current_price(
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    獲取股票當前價格
    """
    # TODO: 實現股票數據服務
    return {"symbol": symbol, "price": 0.0, "timestamp": "2024-01-01T00:00:00Z"} 