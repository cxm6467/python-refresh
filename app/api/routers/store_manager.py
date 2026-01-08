from http import HTTPStatus
from typing import Annotated
from app.database.redis import add_to_token_blacklist
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import AccessTokenDep, StoreManagerServiceDep, SessionDep
from app.api.schemas.store_manager import StoreManagerCreate
from app.database.models import StoreManager
from app.utils import decode_access_token

router = APIRouter(prefix="/store-managers", tags=["store-managers"])

from app.api.core.security import oauth2_scheme

@router.post("/", response_model=StoreManager, status_code=201)
async def create_storemanager(storemanager: StoreManagerCreate, session: SessionDep, service: StoreManagerServiceDep) -> StoreManager:
    return await service.add(storemanager)

@router.post("/token")
async def get_access_token(request: Annotated[OAuth2PasswordRequestForm, Depends()], service: StoreManagerServiceDep) -> dict[str, str]:
    return await service.token(request.username, request.password)

@router.get("/logout")
async def logout(token: AccessTokenDep, service: StoreManagerServiceDep):
    token_id = token
    await add_to_token_blacklist(token_id)
    return {"message": "Logged out successfully"}

# @router.get("/{id}", response_model=StoreManager)
# async def get_storemanager(id: int, session: SessionDep, service: StoreManagerServiceDep) -> StoreManager:
#     manager = await service.get(id)
#     if manager is None:
#         raise HTTPException(status_code=404, detail="StoreManager not found")
#     return manager

# @router.patch("/{id}", response_model=StoreManager)
# async def update_storemanager(id: int, update: StoreManagerUpdate, session: SessionDep, service: StoreManagerServiceDep) -> StoreManager:
#     return await service.update(id, update)


# @router.delete("/{id}", status_code=204)
# async def delete_storemanager(id: int, session: SessionDep, service: StoreManagerServiceDep) -> None:
#     await service.delete(id)

# @router.get("/", response_model=dict[int, StoreManager])
# async def get_storemanagers(session: SessionDep, service: StoreManagerServiceDep) -> dict[int, StoreManager]:
#     storemanagers = await service.get_all()
#     return {storemanager.id: storemanager for storemanager in storemanagers}
