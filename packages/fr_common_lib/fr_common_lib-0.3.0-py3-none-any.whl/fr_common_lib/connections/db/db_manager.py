from contextlib import asynccontextmanager, contextmanager
from typing import AsyncContextManager
from typing import ContextManager

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .settings import settings as db_settings, Settings


class DBManager:
    execution_options = {
        "isolation_level": "READ COMMITTED",
    }

    def __init__(self, settings: Settings):

        self._settings = settings
        self._sync_engine = self.create_sync_engine(self._settings)
        self._async_engine = self.create_async_engine(self._settings)
        self._sync_session_factory = self.sync_sessionmaker(self._sync_engine)
        self._async_session_factory = self.async_sessionmaker(self._async_engine)

    @classmethod
    def sync_sessionmaker(cls, sync_engine: Engine):
        return sessionmaker(
            bind=sync_engine
        )

    @classmethod
    def async_sessionmaker(cls, async_engine: AsyncEngine):
        return async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
        )

    @classmethod
    def create_async_engine(cls, settings: Settings) -> AsyncEngine:
        return create_async_engine(
            settings.ASYNC_URI,
            echo=settings.ECHO,
            future=True,
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
            execution_options=cls.execution_options,
        )

    @classmethod
    def create_sync_engine(cls, settings: Settings) -> Engine:
        return create_engine(
            settings.SYNC_URI,
            echo=settings.ECHO,
            future=True,
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
            execution_options=cls.execution_options,
        )

    @property
    def sync_engine(self) -> Engine:
        return self._sync_engine

    @property
    def async_engine(self) -> AsyncEngine:
        return self._async_engine

    @asynccontextmanager
    async def async_session(self, schema: str, **kwargs) -> AsyncContextManager[AsyncSession]:

        connectable = self._async_engine.execution_options(schema_translate_map=dict(tenant=schema))
        session = self._async_session_factory(bind=connectable, **kwargs)

        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise
        finally:
            await session.close()

    @contextmanager
    def session(self, schema: str, **kwargs) -> ContextManager[Session]:

        connectable = self._sync_engine.execution_options(
            schema_translate_map=dict(tenant=schema)
        )

        session = self._sync_session_factory(bind=connectable, **kwargs)

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


db = DBManager(db_settings)
