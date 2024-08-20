from redis import asyncio as aioredis

from .settings import settings

redis = aioredis.from_url(
    settings.URL,
    encoding="utf-8",
    decode_responses=True
)