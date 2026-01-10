from uuid import UUID
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.schemas.store import StoreCreate, StoreUpdate
from app.database.models import Store, StoreManager, Item


class StoreService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID, manager: StoreManager) -> Store | None:
        # Verify ownership
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")
        if manager.store_id != id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager does not own this store")

        return await self.session.get(Store, id)

    async def get_all(self, manager: StoreManager) -> list[Store]:
        # Managers can only see their own store
        if manager.store_id is None:
            return []

        store = await self.session.get(Store, manager.store_id)
        return [store] if store else []

    async def add(self, store: StoreCreate, manager: StoreManager, assign_to_self: bool = False) -> Store:
        created = Store(**store.model_dump())
        self.session.add(created)
        await self.session.flush()  # Get the ID

        if assign_to_self:
            # Check if manager already has a store
            if manager.store_id is not None:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Manager is already assigned to a store"
                )

            # Assign store to manager
            manager.store_id = created.id
            self.session.add(manager)

        await self.session.commit()
        await self.session.refresh(created)
        return created

    async def update(self, id: UUID, update: StoreUpdate, manager: StoreManager) -> Store:
        # Verify ownership
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")
        if manager.store_id != id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager does not own this store")

        store = await self.session.get(Store, id)
        if store is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Store with id {id} not found"
            )

        store.sqlmodel_update(update.model_dump(exclude_unset=True))
        self.session.add(store)
        await self.session.commit()
        await self.session.refresh(store)
        return store

    async def delete(self, id: UUID, manager: StoreManager) -> None:
        # Verify ownership
        if manager.store_id is None:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager is not assigned to any store")
        if manager.store_id != id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Manager does not own this store")

        store = await self.session.get(Store, id)
        if store is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Store with id {id} not found"
            )

        # Check if store has items
        result = await self.session.execute(
            select(Item).where(Item.store_id == id).limit(1)
        )
        if result.scalar() is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Cannot delete store with existing items"
            )

        # Unassign manager before deleting (query to avoid lazy loading issue)
        result = await self.session.execute(
            select(StoreManager).where(StoreManager.store_id == id)
        )
        existing_manager = result.scalar()
        if existing_manager:
            existing_manager.store_id = None
            self.session.add(existing_manager)

        await self.session.delete(store)
        await self.session.flush()
        await self.session.commit()
