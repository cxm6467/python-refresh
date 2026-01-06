from datetime import datetime, timezone, timedelta
import jwt
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from passlib.context import CryptContext

from app.api.schemas.store_manager import StoreManagerCreate
from config import security_config
from app.database.models import StoreManager

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StoreManagerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> StoreManager | None:
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

    async def token(self, email, password_hash) -> dict[str, str]:
        result = await self.session.execute(select(StoreManager).where(StoreManager.email == email))
        store_manager = result.scalar()

        if store_manager is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Store Manager not found")
        if not pwd_ctx.verify(password_hash, store_manager.password_hash):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")

        access_token = jwt.encode(
            payload={
                "user": store_manager.name,
                "email": store_manager.email,
                "exp": datetime.now(timezone.utc) + timedelta(hours=3)
            },
            algorithm=security_config.JWT_ALGORITHM,
            key=security_config.JWT_SECRET
        )
        return {"access_token": access_token, "token_type": "jwt"}
            
    # async def delete(self, id: int) -> None:
    #     manager = await self.session.get(StoreManager, id)
    #     if manager is None:
    #         raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    #     await self.session.delete(manager)
    #     await self.session.flush()
    #     await self.session.commit()