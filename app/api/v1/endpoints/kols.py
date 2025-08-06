"""
Sentient Trader - KOL API 端點
處理關鍵意見領袖的 CRUD 操作
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from app.core.database import get_db
from app.models.database_models import KOL
from app.models.schemas import KOLCreate, KOLUpdate, KOLResponse
from app.services.kol_service import KOLService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", response_model=List[KOLResponse])
async def get_kols(
    skip: int = Query(0, ge=0, description="跳過的記錄數"),
    limit: int = Query(100, ge=1, le=1000, description="返回的記錄數"),
    active_only: bool = Query(True, description="只返回活躍的 KOL"),
    platform: Optional[str] = Query(None, description="平台篩選"),
    db: Session = Depends(get_db)
):
    """
    獲取 KOL 列表
    
    - **skip**: 跳過的記錄數
    - **limit**: 返回的記錄數
    - **active_only**: 是否只返回活躍的 KOL
    - **platform**: 平台篩選
    """
    try:
        service = KOLService(db)
        kols = await service.get_kols(
            skip=skip,
            limit=limit,
            active_only=active_only,
            platform=platform
        )
        return kols
    except Exception as e:
        logger.error(f"獲取 KOL 列表失敗: {e}")
        raise HTTPException(status_code=500, detail="獲取 KOL 列表失敗")


@router.get("/{kol_id}", response_model=KOLResponse)
async def get_kol(
    kol_id: int,
    db: Session = Depends(get_db)
):
    """
    根據 ID 獲取特定 KOL
    
    - **kol_id**: KOL 的唯一標識符
    """
    try:
        service = KOLService(db)
        kol = await service.get_kol_by_id(kol_id)
        if not kol:
            raise HTTPException(status_code=404, detail="KOL 不存在")
        return kol
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取 KOL {kol_id} 失敗: {e}")
        raise HTTPException(status_code=500, detail="獲取 KOL 失敗")


@router.post("/", response_model=KOLResponse)
async def create_kol(
    kol: KOLCreate,
    db: Session = Depends(get_db)
):
    """
    創建新的 KOL
    
    - **kol**: KOL 創建數據
    """
    try:
        service = KOLService(db)
        created_kol = await service.create_kol(kol)
        logger.info(f"創建 KOL: {created_kol.username}")
        return created_kol
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"創建 KOL 失敗: {e}")
        raise HTTPException(status_code=500, detail="創建 KOL 失敗")


@router.put("/{kol_id}", response_model=KOLResponse)
async def update_kol(
    kol_id: int,
    kol_update: KOLUpdate,
    db: Session = Depends(get_db)
):
    """
    更新 KOL 資訊
    
    - **kol_id**: KOL 的唯一標識符
    - **kol_update**: 更新的 KOL 數據
    """
    try:
        service = KOLService(db)
        updated_kol = await service.update_kol(kol_id, kol_update)
        if not updated_kol:
            raise HTTPException(status_code=404, detail="KOL 不存在")
        logger.info(f"更新 KOL {kol_id}")
        return updated_kol
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新 KOL {kol_id} 失敗: {e}")
        raise HTTPException(status_code=500, detail="更新 KOL 失敗")


@router.delete("/{kol_id}")
async def delete_kol(
    kol_id: int,
    db: Session = Depends(get_db)
):
    """
    刪除 KOL（軟刪除）
    
    - **kol_id**: KOL 的唯一標識符
    """
    try:
        service = KOLService(db)
        success = await service.delete_kol(kol_id)
        if not success:
            raise HTTPException(status_code=404, detail="KOL 不存在")
        logger.info(f"刪除 KOL {kol_id}")
        return {"message": "KOL 已刪除"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刪除 KOL {kol_id} 失敗: {e}")
        raise HTTPException(status_code=500, detail="刪除 KOL 失敗")


@router.get("/{kol_id}/stats")
async def get_kol_stats(
    kol_id: int,
    days: int = Query(30, ge=1, le=365, description="統計天數"),
    db: Session = Depends(get_db)
):
    """
    獲取 KOL 統計資訊
    
    - **kol_id**: KOL 的唯一標識符
    - **days**: 統計天數
    """
    try:
        service = KOLService(db)
        stats = await service.get_kol_stats(kol_id, days)
        if not stats:
            raise HTTPException(status_code=404, detail="KOL 不存在")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取 KOL {kol_id} 統計失敗: {e}")
        raise HTTPException(status_code=500, detail="獲取統計資訊失敗")


@router.post("/{kol_id}/refresh")
async def refresh_kol_data(
    kol_id: int,
    db: Session = Depends(get_db)
):
    """
    刷新 KOL 數據（觸發數據獲取）
    
    - **kol_id**: KOL 的唯一標識符
    """
    try:
        service = KOLService(db)
        success = await service.refresh_kol_data(kol_id)
        if not success:
            raise HTTPException(status_code=404, detail="KOL 不存在")
        logger.info(f"刷新 KOL {kol_id} 數據")
        return {"message": "數據刷新已啟動"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刷新 KOL {kol_id} 數據失敗: {e}")
        raise HTTPException(status_code=500, detail="刷新數據失敗")


@router.get("/search/", response_model=List[KOLResponse])
async def search_kols(
    q: str = Query(..., description="搜尋關鍵字"),
    platform: Optional[str] = Query(None, description="平台篩選"),
    min_followers: Optional[int] = Query(None, ge=0, description="最小粉絲數"),
    db: Session = Depends(get_db)
):
    """
    搜尋 KOL
    
    - **q**: 搜尋關鍵字
    - **platform**: 平台篩選
    - **min_followers**: 最小粉絲數
    """
    try:
        service = KOLService(db)
        kols = await service.search_kols(
            query=q,
            platform=platform,
            min_followers=min_followers
        )
        return kols
    except Exception as e:
        logger.error(f"搜尋 KOL 失敗: {e}")
        raise HTTPException(status_code=500, detail="搜尋 KOL 失敗") 