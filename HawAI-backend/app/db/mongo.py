from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.config import settings


client: Optional[AsyncIOMotorClient] = None


async def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGO_URL)
    return client


async def get_db():
    cli = await get_client()
    return cli[settings.MONGO_DB]


