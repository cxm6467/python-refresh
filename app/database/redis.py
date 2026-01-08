from redis.asyncio import Redis
from config import db_config

_token_blacklist_conn = Redis(
    host=db_config.REDIS_HOST,
    port=db_config.REDIS_PORT,
    db=db_config.REDIS_DB,
)

async def add_to_token_blacklist(token_id: str) -> None:
    await _token_blacklist_conn.set(token_id, "blacklisted")

async def is_token_blacklisted(token_id: str) -> bool:
    return await _token_blacklist_conn.exists(token_id)