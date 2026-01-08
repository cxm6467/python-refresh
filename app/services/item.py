from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.item import ItemCreate, ItemUpdate
from app.database.models import Item


class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> Item | None:
        return await self.session.get(Item, id)

    async def get_all(self) -> list[Item]:
        result = await self.session.execute(select(Item))
        return list(result.scalars().all())

    async def add(self, item: ItemCreate, store_manager_id: UUID) -> Item:
        created = Item(**item.model_dump(), store_manager_id=store_manager_id)
        self.session.add(created)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update(self, id: UUID, update: ItemUpdate) -> Item:
        item = await self.session.get(Item, id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        item.sqlmodel_update(update.model_dump(exclude_unset=True))
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, id: UUID) -> None:
        item = await self.session.get(Item, id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        await self.session.delete(item)
        await self.session.flush()
        await self.session.commit()