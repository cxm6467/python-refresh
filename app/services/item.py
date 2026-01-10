from uuid import UUID
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.item import ItemCreate, ItemUpdate
from app.database.models import Item, StoreManager


class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID, manager: StoreManager) -> Item | None:
        item = await self.session.get(Item, id)
        if item is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {id} not found")

        # Verify ownership
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")
        if item.store_id != manager.store_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Item does not belong to manager's store")

        return item

    async def get_all(self, manager: StoreManager) -> list[Item]:
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")

        result = await self.session.execute(select(Item).where(Item.store_id == manager.store_id))
        return list(result.scalars().all())

    async def add(self, item: ItemCreate, manager: StoreManager) -> Item:
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")

        created = Item(**item.model_dump(), store_id=manager.store_id)
        self.session.add(created)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update(self, id: UUID, update: ItemUpdate, manager: StoreManager) -> Item:
        item = await self.session.get(Item, id)
        if item is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {id} not found")

        # Verify ownership
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")
        if item.store_id != manager.store_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Item does not belong to manager's store")

        item.sqlmodel_update(update.model_dump(exclude_unset=True))
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, id: UUID, manager: StoreManager) -> None:
        item = await self.session.get(Item, id)
        if item is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {id} not found")

        # Verify ownership
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")
        if item.store_id != manager.store_id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Item does not belong to manager's store")

        await self.session.delete(item)
        await self.session.flush()
        await self.session.commit()