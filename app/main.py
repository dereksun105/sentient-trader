"""
Sentient Trader - FastAPI 主應用程式
AI 驅動的金融情報平台後端 API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog
from typing import Dict, Any

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router


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
    
    # 初始化資料庫
    await init_db()
    
    logger.info("Sentient Trader API 服務啟動完成")
    
    yield
    
    # 關閉時執行
    logger.info("正在關閉 Sentient Trader API 服務...")


def create_application() -> FastAPI:
    """
    建立 FastAPI 應用程式實例
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="AI 驅動的金融情報平台 API",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # 添加中間件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    
    # 包含 API 路由
    app.include_router(api_router, prefix="/api/v1")
    
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
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    健康檢查端點
    """
    return {
        "status": "healthy",
        "service": "sentient-trader-api",
        "timestamp": structlog.processors.TimeStamper(fmt="iso")()
    }


@app.get("/info")
async def info() -> Dict[str, Any]:
    """
    應用程式資訊端點
    """
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 