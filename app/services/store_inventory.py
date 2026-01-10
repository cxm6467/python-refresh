from uuid import UUID
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.store_inventory import StoreInventoryCreate, StoreInventoryUpdate
from app.database.models import StoreInventory, Item


class StoreInventoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> StoreInventory | None:
        return await self.session.get(StoreInventory, id)

    async def get_all(self) -> list[StoreInventory]:
        result = await self.session.execute(select(StoreInventory))
        return list(result.scalars().all())

    async def add(self, inventory: StoreInventoryCreate) -> StoreInventory:
        created = StoreInventory(**inventory.model_dump())
        self.session.add(created)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update(self, id: UUID, update: StoreInventoryUpdate) -> StoreInventory:
        inventory = await self.session.get(StoreInventory, id)
        if inventory is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"StoreInventory with id {id} not found"
            )

        inventory.sqlmodel_update(update.model_dump(exclude_unset=True))
        self.session.add(inventory)
        await self.session.commit()
        await self.session.refresh(inventory)
        return inventory

    async def delete(self, id: UUID) -> None:
        inventory = await self.session.get(StoreInventory, id)
        if inventory is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"StoreInventory with id {id} not found"
            )

        # Check if inventory has items
        result = await self.session.execute(
            select(Item).where(Item.store_inventory_id == id).limit(1)
        )
        if result.scalar() is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Cannot delete store inventory with assigned items"
            )

        await self.session.delete(inventory)
        await self.session.flush()
        await self.session.commit()
