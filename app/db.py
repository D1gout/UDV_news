import os
from typing import Any, AsyncGenerator

from dotenv import load_dotenv

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False,)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with AsyncSessionLocal() as session:
        yield session

# Для дальнейшего использования потребуется БД (postgresql)