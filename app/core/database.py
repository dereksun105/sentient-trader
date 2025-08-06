"""
Sentient Trader - 資料庫配置和連接管理
包含 PostgreSQL 和 Redis 連接配置
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis
import structlog
from typing import Optional
import asyncio

from app.core.config import settings

logger = structlog.get_logger()

# SQLAlchemy 配置
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 建立資料庫引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# 建立會話工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立基礎模型類別
Base = declarative_base()

# Redis 連接
redis_client: Optional[redis.Redis] = None


def get_db():
    """
    獲取資料庫會話的依賴注入函數
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """
    初始化資料庫連接和表結構
    """
    global redis_client
    
    try:
        # 初始化 Redis 連接
        redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
        # 測試 Redis 連接
        redis_client.ping()
        logger.info("Redis 連接成功")
        
        # 測試 PostgreSQL 連接
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("PostgreSQL 連接成功")
        
    except Exception as e:
        logger.error(f"資料庫初始化失敗: {e}")
        raise


def get_redis_client() -> redis.Redis:
    """
    獲取 Redis 客戶端實例
    """
    if redis_client is None:
        raise RuntimeError("Redis 客戶端尚未初始化")
    return redis_client


async def close_db():
    """
    關閉資料庫連接
    """
    global redis_client
    
    if redis_client:
        redis_client.close()
        logger.info("Redis 連接已關閉")


# 資料庫健康檢查
async def check_db_health() -> dict:
    """
    檢查資料庫健康狀態
    """
    health_status = {
        "postgresql": "unknown",
        "redis": "unknown",
        "overall": "unknown"
    }
    
    try:
        # 檢查 PostgreSQL
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        health_status["postgresql"] = "healthy"
    except Exception as e:
        health_status["postgresql"] = f"unhealthy: {str(e)}"
    
    try:
        # 檢查 Redis
        if redis_client:
            redis_client.ping()
            health_status["redis"] = "healthy"
        else:
            health_status["redis"] = "unhealthy: client not initialized"
    except Exception as e:
        health_status["redis"] = f"unhealthy: {str(e)}"
    
    # 整體健康狀態
    if all(status == "healthy" for status in [health_status["postgresql"], health_status["redis"]]):
        health_status["overall"] = "healthy"
    else:
        health_status["overall"] = "unhealthy"
    
    return health_status


# 資料庫統計資訊
async def get_db_stats() -> dict:
    """
    獲取資料庫統計資訊
    """
    stats = {
        "postgresql": {},
        "redis": {}
    }
    
    try:
        # PostgreSQL 統計
        with engine.connect() as conn:
            # 獲取資料庫大小
            result = conn.execute("""
                SELECT pg_size_pretty(pg_database_size(current_database())) as db_size
            """)
            stats["postgresql"]["database_size"] = result.fetchone()[0]
            
            # 獲取表數量
            result = conn.execute("""
                SELECT count(*) as table_count 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            stats["postgresql"]["table_count"] = result.fetchone()[0]
            
    except Exception as e:
        stats["postgresql"]["error"] = str(e)
    
    try:
        # Redis 統計
        if redis_client:
            stats["redis"]["info"] = redis_client.info()
            stats["redis"]["dbsize"] = redis_client.dbsize()
    except Exception as e:
        stats["redis"]["error"] = str(e)
    
    return stats 