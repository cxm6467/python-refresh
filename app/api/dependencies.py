from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.item import ItemService
from app.database.session import get_session
from fastapi import Depends

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_item_service(session: SessionDep) -> ItemService:
    return ItemService(session)

ServiceDep = Annotated[ItemService, Depends(get_item_service)]