from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import StoreManagerServiceDep, SessionDep, get_access_token_data
from app.api.schemas.store_manager import StoreManagerCreate
from app.database.models import StoreManager

router = APIRouter(prefix="/store-managers", tags=["store-managers"])

@router.post("/", response_model=StoreManager, status_code=201)
async def create_storemanager(storemanager: StoreManagerCreate, session: SessionDep, service: StoreManagerServiceDep) -> StoreManager:
    return await service.add(storemanager)

@router.post("/token")
async def get_access_token(request: Annotated[OAuth2PasswordRequestForm, Depends()], service: StoreManagerServiceDep) -> dict[str, str]:
    return await service.token(request.username, request.password)

@router.get("/logout")
async def logout(token_data: Annotated[dict[str, str | int], Depends(get_access_token_data)], service: StoreManagerServiceDep) -> dict[str, str]:
    token_id = token_data["jti"]
    await service.logout(token_id)
    return {"message": "Logged out successfully"}
