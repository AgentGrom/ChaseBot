import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text, URL
from sqlalchemy.orm import Session, sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(
    DATABASE_URL,
    echo=True, # Все запросы в консоль выводить
    # pool_size=5, # Максимальное кол-во подключений к базе данных
    # max_overflow=10, # Доп. подключения
    )
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session