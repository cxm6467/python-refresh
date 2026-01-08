from typing import Annotated
from app.database.models import StoreManager

from app.database.redis import is_token_blacklisted
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.core.security import AccessTokenBearer, oauth2_scheme
from app.services.item import ItemService
from app.database.session import get_session
from fastapi import Depends, HTTPException
from http import HTTPStatus

from app.services.store_manager import StoreManagerService
from app.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]
AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]

async def get_access_token_data(token: AccessTokenDep) -> dict:
    result = decode_access_token(token)
    if result is None or await is_token_blacklisted(result["jti"]):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    return result

async def get_current_manager(token: AccessTokenDep, session: SessionDep) -> StoreManager:
    result = await get_access_token_data(token)
    manager = await session.get(StoreManager, result["id"])
    if manager is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    return manager

def get_item_service(session: SessionDep) -> ItemService:
    return ItemService(session)

def get_store_manager_service(session: SessionDep) -> StoreManagerService:
    return StoreManagerService(session)

ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
StoreManagerServiceDep = Annotated[StoreManagerService, Depends(get_store_manager_service)]
StoreManagerDep = Annotated[StoreManager, Depends(get_current_manager)]
