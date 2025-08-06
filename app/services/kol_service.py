"""
Sentient Trader - KOL 服務層
處理關鍵意見領袖相關的業務邏輯
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import List, Optional, Dict, Any
import structlog
from datetime import datetime, timedelta

from app.models.database_models import KOL, SocialMediaPost, SentimentAnalysis
from app.models.schemas import KOLCreate, KOLUpdate, KOLResponse

logger = structlog.get_logger()


class KOLService:
    """
    KOL 業務邏輯服務類
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_kols(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
        platform: Optional[str] = None
    ) -> List[KOLResponse]:
        """
        獲取 KOL 列表
        """
        query = self.db.query(KOL)
        
        if active_only:
            query = query.filter(KOL.is_active == True)
        
        if platform:
            query = query.filter(KOL.platform == platform)
        
        kols = query.offset(skip).limit(limit).all()
        
        return [KOLResponse.from_orm(kol) for kol in kols]
    
    async def get_kol_by_id(self, kol_id: int) -> Optional[KOLResponse]:
        """
        根據 ID 獲取 KOL
        """
        kol = self.db.query(KOL).filter(KOL.id == kol_id).first()
        return KOLResponse.from_orm(kol) if kol else None
    
    async def create_kol(self, kol_data: KOLCreate) -> KOLResponse:
        """
        創建新的 KOL
        """
        # 檢查用戶名是否已存在
        existing_kol = self.db.query(KOL).filter(
            and_(
                KOL.username == kol_data.username,
                KOL.platform == kol_data.platform
            )
        ).first()
        
        if existing_kol:
            raise ValueError(f"用戶名 {kol_data.username} 在平台 {kol_data.platform} 上已存在")
        
        # 創建新的 KOL
        db_kol = KOL(**kol_data.dict())
        self.db.add(db_kol)
        self.db.commit()
        self.db.refresh(db_kol)
        
        logger.info(f"創建 KOL: {db_kol.username} ({db_kol.platform})")
        return KOLResponse.from_orm(db_kol)
    
    async def update_kol(self, kol_id: int, kol_update: KOLUpdate) -> Optional[KOLResponse]:
        """
        更新 KOL 資訊
        """
        kol = self.db.query(KOL).filter(KOL.id == kol_id).first()
        if not kol:
            return None
        
        # 更新非空字段
        update_data = kol_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(kol, field, value)
        
        kol.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(kol)
        
        logger.info(f"更新 KOL {kol_id}: {update_data}")
        return KOLResponse.from_orm(kol)
    
    async def delete_kol(self, kol_id: int) -> bool:
        """
        軟刪除 KOL（設置為非活躍）
        """
        kol = self.db.query(KOL).filter(KOL.id == kol_id).first()
        if not kol:
            return False
        
        kol.is_active = False
        kol.updated_at = datetime.utcnow()
        self.db.commit()
        
        logger.info(f"軟刪除 KOL {kol_id}")
        return True
    
    async def get_kol_stats(self, kol_id: int, days: int = 30) -> Optional[Dict[str, Any]]:
        """
        獲取 KOL 統計資訊
        """
        kol = self.db.query(KOL).filter(KOL.id == kol_id).first()
        if not kol:
            return None
        
        # 計算時間範圍
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # 獲取貼文統計
        posts_query = self.db.query(SocialMediaPost).filter(
            and_(
                SocialMediaPost.kol_id == kol_id,
                SocialMediaPost.posted_at >= start_date
            )
        )
        
        total_posts = posts_query.count()
        
        # 獲取情緒分析統計
        sentiment_query = self.db.query(SentimentAnalysis).filter(
            and_(
                SentimentAnalysis.kol_id == kol_id,
                SentimentAnalysis.analysis_timestamp >= start_date
            )
        )
        
        sentiment_stats = sentiment_query.with_entities(
            func.avg(SentimentAnalysis.sentiment_score).label('avg_sentiment'),
            func.count(SentimentAnalysis.id).label('total_analyses')
        ).first()
        
        # 獲取最常提及的股票
        mentioned_stocks = sentiment_query.with_entities(
            SentimentAnalysis.mentioned_stocks
        ).filter(SentimentAnalysis.mentioned_stocks.isnot(None)).all()
        
        stock_counts = {}
        for result in mentioned_stocks:
            if result.mentioned_stocks:
                for stock in result.mentioned_stocks:
                    stock_counts[stock] = stock_counts.get(stock, 0) + 1
        
        top_stocks = sorted(stock_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "kol_id": kol_id,
            "kol_name": kol.name,
            "total_posts": total_posts,
            "total_analyses": sentiment_stats.total_analyses if sentiment_stats else 0,
            "average_sentiment": float(sentiment_stats.avg_sentiment) if sentiment_stats and sentiment_stats.avg_sentiment else 0.0,
            "influence_score": kol.influence_score,
            "most_mentioned_stocks": [stock for stock, count in top_stocks],
            "analysis_period_days": days
        }
    
    async def search_kols(
        self,
        query: str,
        platform: Optional[str] = None,
        min_followers: Optional[int] = None
    ) -> List[KOLResponse]:
        """
        搜尋 KOL
        """
        search_query = self.db.query(KOL).filter(
            and_(
                KOL.is_active == True,
                or_(
                    KOL.name.ilike(f"%{query}%"),
                    KOL.username.ilike(f"%{query}%"),
                    KOL.bio.ilike(f"%{query}%")
                )
            )
        )
        
        if platform:
            search_query = search_query.filter(KOL.platform == platform)
        
        if min_followers:
            search_query = search_query.filter(KOL.followers_count >= min_followers)
        
        kols = search_query.order_by(desc(KOL.influence_score)).limit(50).all()
        return [KOLResponse.from_orm(kol) for kol in kols]
    
    async def refresh_kol_data(self, kol_id: int) -> bool:
        """
        刷新 KOL 數據（觸發數據獲取）
        """
        kol = self.db.query(KOL).filter(KOL.id == kol_id).first()
        if not kol:
            return False
        
        # TODO: 實現數據獲取邏輯
        # 這裡應該觸發異步任務來獲取最新的社交媒體數據
        
        logger.info(f"觸發 KOL {kol_id} 數據刷新")
        return True
    
    async def update_influence_score(self, kol_id: int) -> bool:
        """
        更新 KOL 影響力評分
        """
        kol = self.db.query(KOL).filter(KOL.id == kol_id).first()
        if not kol:
            return False
        
        # 計算影響力評分的邏輯
        # 基於粉絲數、貼文頻率、互動率等因素
        
        # 獲取最近的貼文統計
        recent_posts = self.db.query(SocialMediaPost).filter(
            and_(
                SocialMediaPost.kol_id == kol_id,
                SocialMediaPost.posted_at >= datetime.utcnow() - timedelta(days=30)
            )
        ).count()
        
        # 獲取平均互動率
        avg_engagement = self.db.query(
            func.avg(
                SocialMediaPost.likes_count + 
                SocialMediaPost.retweets_count + 
                SocialMediaPost.replies_count
            )
        ).filter(SocialMediaPost.kol_id == kol_id).scalar() or 0
        
        # 簡化的影響力評分計算
        followers_factor = min(kol.followers_count / 1000000, 1.0)  # 粉絲數因子
        activity_factor = min(recent_posts / 100, 1.0)  # 活躍度因子
        engagement_factor = min(avg_engagement / 1000, 1.0)  # 互動率因子
        
        new_score = (followers_factor * 0.4 + activity_factor * 0.3 + engagement_factor * 0.3)
        
        kol.influence_score = new_score
        kol.updated_at = datetime.utcnow()
        self.db.commit()
        
        logger.info(f"更新 KOL {kol_id} 影響力評分: {new_score:.3f}")
        return True 