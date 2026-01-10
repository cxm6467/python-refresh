from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.api.dependencies import SessionDep, ItemServiceDep, StoreManagerDep
from app.database.models import Item
from app.api.schemas.item import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/{id}", response_model=Item)
async def get_item(id: UUID, service: ItemServiceDep, manager: StoreManagerDep) -> Item:
    return await service.get(id, manager)


@router.get("/", response_model=dict[UUID, Item])
async def get_items(service: ItemServiceDep, manager: StoreManagerDep) -> dict[UUID, Item]:
    items = await service.get_all(manager)
    return {item.id: item for item in items}


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, service: ItemServiceDep, manager: StoreManagerDep) -> Item:
    return await service.add(item, manager)


@router.patch("/{id}", response_model=Item)
async def update_item(id: UUID, update: ItemUpdate, service: ItemServiceDep, manager: StoreManagerDep) -> Item:
    return await service.update(id, update, manager)


@router.delete("/{id}", status_code=204)
async def delete_item(id: UUID, service: ItemServiceDep, manager: StoreManagerDep) -> None:
    await service.delete(id, manager)

