from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.store_manager import StoreManagerCreate, StoreManagerUpdate
from app.database.models import StoreManager


class StoreManagerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> StoreManager | None:
        return await self.session.get(StoreManager, id)

    async def get_all(self) -> list[StoreManager]:
        result = await self.session.execute(select(StoreManager))
        return list(result.scalars().all())

    async def add(self, manager: StoreManagerCreate) -> StoreManager:
        manager_data = manager.model_dump()
        # Map password to password_hash (for now, just use password as hash - should use proper hashing)
        manager_data["password_hash"] = manager_data.pop("password")
        created = StoreManager(**manager_data)
        self.session.add(created)
        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update(self, id: int, update: StoreManagerUpdate) -> StoreManager:
        manager = await self.session.get(StoreManager, id)
        if manager is None:
            raise HTTPException(status_code=404, detail=f"Manager with id {id} not found")
        update_data = update.model_dump(exclude_unset=True)
        # Map password to password_hash if password is being updated
        if "password" in update_data:
            update_data["password_hash"] = update_data.pop("password")
        manager.sqlmodel_update(update_data)
        self.session.add(manager)
        await self.session.commit()
        await self.session.refresh(manager)
        return manager

    async def delete(self, id: int) -> None:
        manager = await self.session.get(StoreManager, id)
        if manager is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        await self.session.delete(manager)
        await self.session.flush()
        await self.session.commit()