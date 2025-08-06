"""
Sentient Trader - 社交媒體貼文 API 端點
處理貼文的 CRUD 操作和查詢
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.models.schemas import PostResponse

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0, description="跳過的記錄數"),
    limit: int = Query(100, ge=1, le=1000, description="返回的記錄數"),
    kol_id: Optional[int] = Query(None, description="KOL ID 篩選"),
    platform: Optional[str] = Query(None, description="平台篩選"),
    db: Session = Depends(get_db)
):
    """
    獲取社交媒體貼文列表
    """
    # TODO: 實現貼文服務
    return []


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    根據 ID 獲取特定貼文
    """
    # TODO: 實現貼文服務
    raise HTTPException(status_code=404, detail="貼文不存在") 