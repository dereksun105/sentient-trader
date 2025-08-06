"""
Sentient Trader - 簡化版 FastAPI 主應用程式
AI 驅動的金融情報平台後端 API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
from typing import Dict, Any
from datetime import datetime

# 配置結構化日誌
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    應用程式生命週期管理
    """
    # 啟動時執行
    logger.info("正在啟動 Sentient Trader API 服務...")
    
    logger.info("Sentient Trader API 服務啟動完成")
    
    yield
    
    # 關閉時執行
    logger.info("正在關閉 Sentient Trader API 服務...")


def create_application() -> FastAPI:
    """
    建立 FastAPI 應用程式實例
    """
    app = FastAPI(
        title="Sentient Trader",
        description="AI 驅動的金融情報平台 API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # 添加中間件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_application()


@app.get("/")
async def root() -> Dict[str, Any]:
    """
    根端點 - API 健康檢查
    """
    return {
        "message": "歡迎使用 Sentient Trader API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    健康檢查端點
    """
    return {
        "status": "healthy",
        "service": "sentient-trader-api",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/info")
async def info() -> Dict[str, Any]:
    """
    應用程式資訊端點
    """
    return {
        "app_name": "Sentient Trader",
        "environment": "development",
        "debug": True,
        "version": "1.0.0"
    }


@app.get("/api/v1/kols")
async def get_kols() -> Dict[str, Any]:
    """
    獲取 KOL 列表
    """
    return {
        "kols": [
            {
                "id": 1,
                "name": "Elon Musk",
                "platform": "Twitter",
                "username": "@elonmusk",
                "influence_score": 0.95,
                "followers_count": 150000000
            },
            {
                "id": 2,
                "name": "Cathie Wood",
                "platform": "Twitter",
                "username": "@CathieDWood",
                "influence_score": 0.85,
                "followers_count": 2500000
            }
        ]
    }


@app.get("/api/v1/posts")
async def get_posts() -> Dict[str, Any]:
    """
    獲取社交媒體貼文
    """
    return {
        "posts": [
            {
                "id": 1,
                "kol_id": 1,
                "content": "Tesla stock looking strong today! 🚀",
                "sentiment_score": 0.8,
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 