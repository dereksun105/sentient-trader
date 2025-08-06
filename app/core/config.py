"""
Sentient Trader - 應用程式配置管理
使用 Pydantic Settings 進行類型安全的配置管理
"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """
    應用程式配置類別
    使用環境變數進行配置，支援 .env 文件
    """
    
    # 應用程式基本設定
    APP_NAME: str = Field(default="Sentient Trader", description="應用程式名稱")
    DEBUG: bool = Field(default=True, description="除錯模式")
    ENVIRONMENT: str = Field(default="development", description="執行環境")
    
    # 服務器配置
    HOST: str = Field(default="0.0.0.0", description="服務器主機")
    PORT: int = Field(default=8000, description="服務器端口")
    STREAMLIT_PORT: int = Field(default=8501, description="Streamlit 端口")
    
    # 資料庫配置
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/sentient_trader",
        description="PostgreSQL 資料庫連接字串"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="Redis 連接字串"
    )
    
    # API 金鑰配置
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API 金鑰")
    GOOGLE_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API 金鑰")
    
    # Twitter/X API 配置
    TWITTER_BEARER_TOKEN: Optional[str] = Field(default=None, description="Twitter Bearer Token")
    TWITTER_API_KEY: Optional[str] = Field(default=None, description="Twitter API Key")
    TWITTER_API_SECRET: Optional[str] = Field(default=None, description="Twitter API Secret")
    TWITTER_ACCESS_TOKEN: Optional[str] = Field(default=None, description="Twitter Access Token")
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = Field(default=None, description="Twitter Access Token Secret")
    
    # 新聞 API 配置
    NEWS_API_KEY: Optional[str] = Field(default=None, description="News API 金鑰")
    
    # 金融數據 API 配置
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None, description="Alpha Vantage API 金鑰")
    YAHOO_FINANCE_API_KEY: Optional[str] = Field(default=None, description="Yahoo Finance API 金鑰")
    
    # 向量資料庫配置
    PINECONE_API_KEY: Optional[str] = Field(default=None, description="Pinecone API 金鑰")
    PINECONE_ENVIRONMENT: Optional[str] = Field(default=None, description="Pinecone 環境")
    
    # 監控配置
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN")
    
    # 安全配置
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT 密鑰"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT 演算法")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="訪問令牌過期時間（分鐘）")
    
    # 速率限制配置
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="每分鐘請求限制")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, description="每小時請求限制")
    
    # AI 模型配置
    SENTIMENT_MODEL: str = Field(
        default="cardiffnlp/twitter-roberta-base-sentiment-latest",
        description="情緒分析模型"
    )
    NER_MODEL: str = Field(
        default="dbmdz/bert-large-cased-finetuned-conll03-english",
        description="命名實體識別模型"
    )
    EMBEDDING_MODEL: str = Field(
        default="text-embedding-ada-002",
        description="文本嵌入模型"
    )
    
    # 功能開關
    ENABLE_REAL_TIME_UPDATES: bool = Field(default=True, description="啟用即時更新")
    ENABLE_ANOMALY_DETECTION: bool = Field(default=True, description="啟用異常檢測")
    ENABLE_PREDICTIVE_MODELING: bool = Field(default=False, description="啟用預測建模")
    ENABLE_RAG_FEATURE: bool = Field(default=False, description="啟用 RAG 功能")
    
    # CORS 配置
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:8501", "http://127.0.0.1:8501"],
        description="允許的 CORS 主機"
    )
    
    class Config:
        """
        Pydantic 配置
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 建立全域設定實例
settings = Settings()


def get_settings() -> Settings:
    """
    獲取設定實例的工廠函數
    """
    return settings


# 驗證關鍵配置
def validate_settings():
    """
    驗證關鍵配置是否已設置
    """
    required_settings = [
        "DATABASE_URL",
        "REDIS_URL",
        "SECRET_KEY"
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"缺少必要的配置: {', '.join(missing_settings)}")
    
    # 驗證 API 金鑰（如果啟用相關功能）
    if settings.ENABLE_REAL_TIME_UPDATES and not settings.TWITTER_BEARER_TOKEN:
        print("警告: 啟用即時更新但未設置 Twitter API 金鑰")
    
    if settings.ENABLE_RAG_FEATURE and not settings.OPENAI_API_KEY:
        print("警告: 啟用 RAG 功能但未設置 OpenAI API 金鑰")


# 在模組載入時驗證配置
try:
    validate_settings()
except ValueError as e:
    print(f"配置驗證失敗: {e}")
    # 在開發環境中，我們可以繼續運行，但在生產環境中應該停止
    if settings.ENVIRONMENT == "production":
        raise 