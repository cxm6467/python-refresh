import json
from datetime import datetime, timedelta, timezone
from redis.asyncio import Redis
from config import db_config

_token_blacklist_conn = Redis(
    host=db_config.REDIS_HOST,
    port=db_config.REDIS_PORT,
    db=db_config.REDIS_DB,
)

async def add_to_token_blacklist(token_id: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    blacklist_data = {
        "jti": token_id,
        "status": "blacklisted",
        "created_at": now,
        "updated_at": now
    }
    await _token_blacklist_conn.set(token_id, json.dumps(blacklist_data), ex=timedelta(days=1))

async def is_token_blacklisted(token_id: str) -> bool:
    return await _token_blacklist_conn.exists(token_id)