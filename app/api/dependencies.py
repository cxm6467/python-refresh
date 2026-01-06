from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.item import ItemService
from app.database.session import get_session
from fastapi import Depends

from app.services.store_manager import StoreManagerService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_item_service(session: SessionDep) -> ItemService:
    return ItemService(session)

def get_store_manager_service(session: SessionDep) -> StoreManagerService:
    return StoreManagerService(session)

ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
StoreManagerServiceDep = Annotated[StoreManagerService, Depends(get_store_manager_service)]