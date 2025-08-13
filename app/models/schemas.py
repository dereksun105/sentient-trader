"""
Sentient Trader - Pydantic 模型
定義 API 請求和響應的數據結構
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# 枚舉定義
class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class AlertType(str, Enum):
    SENTIMENT_THRESHOLD = "sentiment_threshold"
    KOL_MENTION = "kol_mention"
    STOCK_MENTION = "stock_mention"
    ANOMALY_DETECTION = "anomaly_detection"


class Platform(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"


# 基礎模型
class BaseSchema(BaseModel):
    """基礎 Pydantic 模型"""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# 使用者相關模型
class UserBase(BaseSchema):
    email: str = Field(..., description="使用者 Email")
    full_name: Optional[str] = Field(None, description="使用者姓名")
    preferences: Optional[Dict[str, Any]] = Field(None, description="偏好設定")


class UserCreate(BaseSchema):
    email: str = Field(..., description="Email")
    full_name: Optional[str] = Field(None, description="姓名")
    password: str = Field(..., min_length=6, description="密碼")


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class LoginRequest(BaseSchema):
    email: str = Field(...)
    password: str = Field(...)


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = Field("bearer")


class UserPreferencesUpdate(BaseSchema):
    preferences: Dict[str, Any]


# KOL 相關模型
class KOLBase(BaseSchema):
    name: str = Field(..., description="KOL 姓名")
    username: str = Field(..., description="社交媒體用戶名")
    platform: Platform = Field(..., description="平台")
    bio: Optional[str] = Field(None, description="個人簡介")
    followers_count: int = Field(0, description="粉絲數量")
    influence_score: float = Field(0.0, ge=0.0, le=1.0, description="影響力評分")


class KOLCreate(KOLBase):
    pass


class KOLUpdate(BaseSchema):
    name: Optional[str] = None
    bio: Optional[str] = None
    followers_count: Optional[int] = None
    influence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_active: Optional[bool] = None


class KOLResponse(KOLBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


# 社交媒體貼文相關模型
class PostBase(BaseSchema):
    platform_post_id: str = Field(..., description="平台原始貼文 ID")
    platform: Platform = Field(..., description="平台")
    content: str = Field(..., description="貼文內容")
    url: Optional[str] = Field(None, description="貼文連結")
    likes_count: int = Field(0, description="點讚數")
    retweets_count: int = Field(0, description="轉發數")
    replies_count: int = Field(0, description="回覆數")
    posted_at: datetime = Field(..., description="發布時間")


class PostCreate(PostBase):
    kol_id: int = Field(..., description="KOL ID")


class PostUpdate(BaseSchema):
    content: Optional[str] = None
    likes_count: Optional[int] = None
    retweets_count: Optional[int] = None
    replies_count: Optional[int] = None


class PostResponse(PostBase):
    id: int
    kol_id: int
    fetched_at: datetime
    kol: KOLResponse


# 情緒分析相關模型
class SentimentBase(BaseSchema):
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="情緒分數")
    sentiment_label: SentimentLabel = Field(..., description="情緒標籤")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="置信度")
    mentioned_stocks: Optional[List[str]] = Field(None, description="提及的股票代碼")
    mentioned_companies: Optional[List[str]] = Field(None, description="提及的公司名稱")
    model_used: str = Field(..., description="使用的 AI 模型")


class SentimentCreate(SentimentBase):
    post_id: int = Field(..., description="貼文 ID")
    kol_id: int = Field(..., description="KOL ID")


class SentimentResponse(SentimentBase):
    id: int
    post_id: int
    kol_id: int
    analysis_timestamp: datetime


# 股票價格相關模型
class StockPriceBase(BaseSchema):
    symbol: str = Field(..., description="股票代碼")
    price: float = Field(..., description="當前價格")
    volume: Optional[int] = Field(None, description="成交量")
    open_price: Optional[float] = Field(None, description="開盤價")
    high_price: Optional[float] = Field(None, description="最高價")
    low_price: Optional[float] = Field(None, description="最低價")
    close_price: Optional[float] = Field(None, description="收盤價")
    timestamp: datetime = Field(..., description="時間戳")
    data_source: str = Field(..., description="數據來源")


class StockPriceCreate(StockPriceBase):
    pass


class StockPriceResponse(StockPriceBase):
    id: int


# 警報相關模型
class AlertBase(BaseSchema):
    name: str = Field(..., description="警報名稱")
    description: Optional[str] = Field(None, description="警報描述")
    alert_type: AlertType = Field(..., description="警報類型")
    conditions: Dict[str, Any] = Field(..., description="警報條件")


class AlertCreate(AlertBase):
    user_id: int = Field(..., description="用戶 ID")


class AlertUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class AlertResponse(AlertBase):
    id: int
    user_id: int
    is_active: bool
    last_triggered: Optional[datetime] = None
    trigger_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None


# 關聯分析相關模型
class CorrelationRequest(BaseSchema):
    kol_id: int = Field(..., description="KOL ID")
    stock_symbol: str = Field(..., description="股票代碼")
    time_period_days: int = Field(30, ge=1, le=365, description="分析時間範圍（天）")


class CorrelationResponse(BaseSchema):
    id: int
    kol_id: int
    stock_symbol: str
    correlation_coefficient: float = Field(..., description="皮爾遜相關係數")
    p_value: Optional[float] = Field(None, description="統計顯著性")
    sample_size: int = Field(..., description="樣本數量")
    time_period_days: int = Field(..., description="分析時間範圍")
    analysis_timestamp: datetime
    kol: KOLResponse


# 新聞文章相關模型
class NewsArticleBase(BaseSchema):
    title: str = Field(..., description="文章標題")
    content: str = Field(..., description="文章內容")
    url: str = Field(..., description="文章連結")
    source: str = Field(..., description="新聞來源")
    author: Optional[str] = Field(None, description="作者")
    published_at: datetime = Field(..., description="發布時間")


class NewsArticleResponse(NewsArticleBase):
    id: int
    fetched_at: datetime
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[SentimentLabel] = None
    mentioned_stocks: Optional[List[str]] = None


# 異常檢測相關模型
class AnomalyDetectionBase(BaseSchema):
    kol_id: int = Field(..., description="KOL ID")
    anomaly_type: str = Field(..., description="異常類型")
    severity_score: float = Field(..., ge=0.0, le=1.0, description="嚴重程度")
    description: str = Field(..., description="異常描述")


class AnomalyDetectionResponse(AnomalyDetectionBase):
    id: int
    detected_at: datetime
    is_resolved: bool
    kol: KOLResponse


# 統計和聚合模型
class SentimentStats(BaseSchema):
    total_posts: int = Field(..., description="總貼文數")
    positive_count: int = Field(..., description="正面貼文數")
    negative_count: int = Field(..., description="負面貼文數")
    neutral_count: int = Field(..., description="中性貼文數")
    average_sentiment: float = Field(..., description="平均情緒分數")
    sentiment_trend: List[Dict[str, Any]] = Field(..., description="情緒趨勢")


class KOLStats(BaseSchema):
    kol_id: int
    kol_name: str
    total_posts: int
    average_sentiment: float
    influence_score: float
    most_mentioned_stocks: List[str]
    recent_sentiment_trend: List[Dict[str, Any]]


# 即時數據模型
class RealTimeUpdate(BaseSchema):
    """即時更新數據模型"""
    update_type: str = Field(..., description="更新類型")
    timestamp: datetime = Field(..., description="時間戳")
    data: Dict[str, Any] = Field(..., description="更新數據")


class DashboardData(BaseSchema):
    """儀表板數據模型"""
    recent_posts: List[PostResponse]
    sentiment_summary: SentimentStats
    top_kols: List[KOLStats]
    market_alerts: List[AlertResponse]
    correlation_insights: List[CorrelationResponse]


# 驗證器
@validator('sentiment_score')
def validate_sentiment_score(cls, v):
    """驗證情緒分數範圍"""
    if not -1.0 <= v <= 1.0:
        raise ValueError('情緒分數必須在 -1.0 到 1.0 之間')
    return v


@validator('confidence_score')
def validate_confidence_score(cls, v):
    """驗證置信度範圍"""
    if not 0.0 <= v <= 1.0:
        raise ValueError('置信度必須在 0.0 到 1.0 之間')
    return v


@validator('influence_score')
def validate_influence_score(cls, v):
    """驗證影響力評分範圍"""
    if not 0.0 <= v <= 1.0:
        raise ValueError('影響力評分必須在 0.0 到 1.0 之間')
    return v 