"""
Sentient Trader - 資料庫模型
定義所有資料庫表結構和關聯
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

from app.core.database import Base


class KOL(Base):
    """
    關鍵意見領袖 (Key Opinion Leader) 模型
    追蹤影響力人物的基本資訊和社交媒體帳號
    """
    __tablename__ = "kols"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    platform = Column(String(50), nullable=False)  # twitter, linkedin, etc.
    bio = Column(Text, nullable=True)
    followers_count = Column(Integer, default=0)
    influence_score = Column(Float, default=0.0)  # 影響力評分
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 關聯
    posts = relationship("SocialMediaPost", back_populates="kol")
    sentiment_analyses = relationship("SentimentAnalysis", back_populates="kol")
    
    def __repr__(self):
        return f"<KOL(id={self.id}, name='{self.name}', username='{self.username}')>"


class SocialMediaPost(Base):
    """
    社交媒體貼文模型
    儲存從各種平台獲取的貼文內容
    """
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    kol_id = Column(Integer, ForeignKey("kols.id"), nullable=False)
    platform_post_id = Column(String(255), unique=True, nullable=False)  # 平台原始貼文 ID
    platform = Column(String(50), nullable=False)  # twitter, linkedin, etc.
    content = Column(Text, nullable=False)
    url = Column(String(500), nullable=True)
    likes_count = Column(Integer, default=0)
    retweets_count = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    posted_at = Column(DateTime(timezone=True), nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 關聯
    kol = relationship("KOL", back_populates="posts")
    sentiment_analysis = relationship("SentimentAnalysis", back_populates="post", uselist=False)
    
    def __repr__(self):
        return f"<SocialMediaPost(id={self.id}, kol_id={self.kol_id}, platform='{self.platform}')>"


class SentimentAnalysis(Base):
    """
    情緒分析結果模型
    儲存 AI 分析的情緒分數和相關資訊
    """
    __tablename__ = "sentiment_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("social_media_posts.id"), nullable=False)
    kol_id = Column(Integer, ForeignKey("kols.id"), nullable=False)
    
    # 情緒分析結果
    sentiment_score = Column(Float, nullable=False)  # -1.0 到 1.0
    sentiment_label = Column(String(50), nullable=False)  # positive, negative, neutral
    confidence_score = Column(Float, nullable=False)  # 0.0 到 1.0
    
    # 實體識別結果
    mentioned_stocks = Column(JSON, nullable=True)  # 提及的股票代碼
    mentioned_companies = Column(JSON, nullable=True)  # 提及的公司名稱
    
    # 分析元數據
    model_used = Column(String(100), nullable=False)  # 使用的 AI 模型
    analysis_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # 關聯
    post = relationship("SocialMediaPost", back_populates="sentiment_analysis")
    kol = relationship("KOL", back_populates="sentiment_analyses")
    
    def __repr__(self):
        return f"<SentimentAnalysis(id={self.id}, sentiment_score={self.sentiment_score})>"


class StockPrice(Base):
    """
    股票價格模型
    儲存股票價格歷史數據
    """
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)  # 股票代碼
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=True)
    open_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    data_source = Column(String(50), nullable=False)  # yahoo, alpha_vantage, etc.
    
    def __repr__(self):
        return f"<StockPrice(id={self.id}, symbol='{self.symbol}', price={self.price})>"


class Alert(Base):
    """
    警報模型
    儲存用戶設定的警報規則和觸發記錄
    """
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 簡化版本，實際應有用戶表
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # 警報條件
    alert_type = Column(String(50), nullable=False)  # sentiment_threshold, kol_mention, etc.
    conditions = Column(JSON, nullable=False)  # 警報條件配置
    
    # 狀態
    is_active = Column(Boolean, default=True)
    last_triggered = Column(DateTime(timezone=True), nullable=True)
    trigger_count = Column(Integer, default=0)
    
    # 時間戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Alert(id={self.id}, name='{self.name}', type='{self.alert_type}')>"


class CorrelationAnalysis(Base):
    """
    關聯分析模型
    儲存 KOL 情緒與股票價格的關聯分析結果
    """
    __tablename__ = "correlation_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    kol_id = Column(Integer, ForeignKey("kols.id"), nullable=False)
    stock_symbol = Column(String(20), nullable=False, index=True)
    
    # 關聯分析結果
    correlation_coefficient = Column(Float, nullable=False)  # 皮爾遜相關係數
    p_value = Column(Float, nullable=True)  # 統計顯著性
    sample_size = Column(Integer, nullable=False)  # 樣本數量
    
    # 分析參數
    time_period_days = Column(Integer, nullable=False)  # 分析時間範圍
    analysis_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # 關聯
    kol = relationship("KOL")
    
    def __repr__(self):
        return f"<CorrelationAnalysis(id={self.id}, kol_id={self.kol_id}, symbol='{self.stock_symbol}')>"


class NewsArticle(Base):
    """
    新聞文章模型
    儲存從新聞 API 獲取的文章
    """
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    source = Column(String(100), nullable=False)
    author = Column(String(100), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 情緒分析結果
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String(50), nullable=True)
    mentioned_stocks = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<NewsArticle(id={self.id}, title='{self.title[:50]}...')>"


class AnomalyDetection(Base):
    """
    異常檢測模型
    儲存 AI 檢測到的異常模式
    """
    __tablename__ = "anomaly_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    kol_id = Column(Integer, ForeignKey("kols.id"), nullable=False)
    anomaly_type = Column(String(50), nullable=False)  # frequency, sentiment, content
    severity_score = Column(Float, nullable=False)  # 0.0 到 1.0
    description = Column(Text, nullable=False)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    is_resolved = Column(Boolean, default=False)
    
    # 關聯
    kol = relationship("KOL")
    
    def __repr__(self):
        return f"<AnomalyDetection(id={self.id}, type='{self.anomaly_type}', severity={self.severity_score})>" 