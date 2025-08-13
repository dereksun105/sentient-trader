"""
Sentient Trader - 簡化版 FastAPI 主應用程式
AI 驅動的金融情報平台後端 API
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog
from typing import Dict, Any, Optional
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
        allow_origins=[
            "http://localhost:8501",
            "http://127.0.0.1:8501",
            "http://localhost:8502",
            "http://127.0.0.1:8502",
        ],
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


# ========== 簡化版 Auth 與使用者（記憶體儲存） ==========
from app.core.security import hash_password, verify_password, create_access_token, decode_token

_users_store: Dict[str, Dict[str, Any]] = {}
_users_by_id: Dict[int, Dict[str, Any]] = {}
_next_user_id: int = 1


def _get_authorization_token(request: Request) -> Optional[str]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return None
    return auth_header.split(" ", 1)[1].strip()


@app.post("/api/v1/auth/register")
async def register_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    global _next_user_id
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    full_name = payload.get("full_name")
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password are required")
    if email in _users_store:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_obj = {
        "id": _next_user_id,
        "email": email,
        "full_name": full_name,
        "password_hash": hash_password(password),
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "preferences": {}
    }
    _users_store[email] = user_obj
    _users_by_id[_next_user_id] = user_obj
    _next_user_id += 1
    # 回傳不含敏感資訊
    resp = {k: v for k, v in user_obj.items() if k != "password_hash"}
    return resp


@app.post("/api/v1/auth/login")
async def login_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    user = _users_store.get(email)
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token(str(user["id"]), expires_minutes=60 * 24)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/v1/auth/me")
async def auth_me(request: Request) -> Dict[str, Any]:
    token = _get_authorization_token(request)
    payload = decode_token(token or "") if token else None
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = int(payload["sub"])
    user = _users_by_id.get(user_id)
    if not user or not user.get("is_active"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or not found")
    return {k: v for k, v in user.items() if k != "password_hash"}


@app.put("/api/v1/users/me/preferences")
async def update_preferences(payload: Dict[str, Any], request: Request) -> Dict[str, Any]:
    token = _get_authorization_token(request)
    payload_token = decode_token(token or "") if token else None
    if payload_token is None or "sub" not in payload_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = int(payload_token["sub"])
    user = _users_by_id.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["preferences"] = payload.get("preferences", {})
    user["updated_at"] = datetime.now().isoformat()
    return {k: v for k, v in user.items() if k != "password_hash"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 