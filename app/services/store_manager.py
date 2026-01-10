from datetime import timedelta
from http import HTTPStatus
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from passlib.context import CryptContext

from app.api.schemas.store_manager import StoreManagerCreate, StoreManagerUpdate
from app.utils import generate_access_token
from app.database.models import StoreManager, Store
from app.database.redis import add_to_token_blacklist

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StoreManagerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> StoreManager | None:
        return await self.session.get(StoreManager, id)

    # async def get_all(self) -> list[StoreManager]:
    #     result = await self.session.execute(select(StoreManager))
    #     return list(result.scalars().all())

    async def add(self, manager: StoreManagerCreate) -> StoreManager:
        created = StoreManager(**manager.model_dump(exclude=["password_hash"]),
         password_hash= pwd_ctx.hash(manager.password_hash)
         )
        self.session.add(created)
        await self.session.commit()
        await self.session.refresh(created)
        return created   

    async def token(self, email: str, password_hash: str) -> dict[str, str]:
        result = await self.session.execute(select(StoreManager).where(StoreManager.email == email))
        store_manager = result.scalar()

        if store_manager is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Store Manager not found")
        if not pwd_ctx.verify(password_hash, store_manager.password_hash):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")

        access_token = generate_access_token(data={"user": store_manager.name, "id": str(store_manager.id)}, expiry=timedelta(days=1))
        return {"access_token": access_token, "token_type": "jwt"}

    async def logout(self, token_id: str) -> None:
        await add_to_token_blacklist(token_id)

    async def update(self, id: UUID, update: StoreManagerUpdate, current_manager: StoreManager) -> StoreManager:
        # Verify manager is updating their own profile
        if current_manager.id != id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Cannot update another manager's profile"
            )

        manager = await self.session.get(StoreManager, id)
        if manager is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"StoreManager with id {id} not found"
            )

        update_dict = update.model_dump(exclude_unset=True)

        # Handle password update separately
        if "password" in update_dict:
            password = update_dict.pop("password")
            update_dict["password_hash"] = pwd_ctx.hash(password)

        # Handle email uniqueness check
        if "email" in update_dict and update_dict["email"] != manager.email:
            result = await self.session.execute(
                select(StoreManager).where(StoreManager.email == update_dict["email"])
            )
            if result.scalar() is not None:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Email already in use"
                )

        # Handle store assignment
        if "store_id" in update_dict:
            store_id = update_dict["store_id"]

            if store_id is not None:
                # Verify store exists
                store = await self.session.get(Store, store_id)
                if store is None:
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail=f"Store with id {store_id} not found"
                    )

                # Check if store already has a manager (query to avoid lazy loading issue)
                result = await self.session.execute(
                    select(StoreManager).where(StoreManager.store_id == store_id)
                )
                existing_manager = result.scalar()
                if existing_manager and existing_manager.id != manager.id:
                    raise HTTPException(
                        status_code=HTTPStatus.CONFLICT,
                        detail="Store already has a manager assigned"
                    )

        manager.sqlmodel_update(update_dict)
        self.session.add(manager)
        await self.session.commit()
        await self.session.refresh(manager)
        return manager

    # async def delete(self, id: int) -> None:
    #     manager = await self.session.get(
    #         StoreManager, 
    #         id
    #     )
    #     if manager is None:
    #         raise HTTPException(
    #             status_code=404, 
    #             detail=f"Item with id {id} not found"
    #         )
    #     await self.session.delete(
    #         manager
    #     )
    #     await self.session.flush()
    #     await self.session.commit()