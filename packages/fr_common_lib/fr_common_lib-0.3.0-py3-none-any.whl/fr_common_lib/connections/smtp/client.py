from .settings import settings
from aiosmtplib import SMTP
from contextlib import asynccontextmanager
from typing import AsyncContextManager


@asynccontextmanager
async def smtp_client() -> AsyncContextManager[SMTP]:
    async with SMTP(hostname=settings.HOST, port=settings.PORT, validate_certs=False, use_tls=True) as client:
        await client.login(settings.EMAIL, settings.PASSWORD)
        yield client
