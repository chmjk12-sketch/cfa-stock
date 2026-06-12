"""Database Connection Manager - SQLite 适配版"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 使用环境变量或默认 SQLite
SYNC_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cfa_test.db")

sync_engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False} if "sqlite" in SYNC_DATABASE_URL else {})
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Async engine
if "sqlite" in SYNC_DATABASE_URL:
    ASYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    ASYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in ASYNC_DATABASE_URL else {}
)
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def get_sync_session() -> Session:
    """获取同步数据库会话"""
    db = SyncSessionLocal()
    try:
        return db
    finally:
        db.close()


async def get_async_session() -> AsyncSession:
    """获取异步数据库会话"""
    async with AsyncSessionLocal() as session:
        yield session
