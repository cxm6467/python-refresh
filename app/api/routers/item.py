from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.api.dependencies import SessionDep, ItemServiceDep, StoreManagerDep
from app.database.models import Item
from app.api.schemas.item import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/{id}", response_model=Item)
async def get_item(id: UUID, session: SessionDep, service: ItemServiceDep, _: StoreManagerDep) -> Item:
    item = await service.get(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/", response_model=dict[UUID, Item])
async def get_items(session: SessionDep, service: ItemServiceDep, _: StoreManagerDep) -> dict[UUID, Item]:
    items = await service.get_all()
    return {item.id: item for item in items}


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, session: SessionDep, service: ItemServiceDep, manager: StoreManagerDep) -> Item:
    return await service.add(item, manager.id)


@router.patch("/{id}", response_model=Item)
async def update_item(id: UUID, update: ItemUpdate, session: SessionDep, service: ItemServiceDep) -> Item:
    return await service.update(id, update)


@router.delete("/{id}", status_code=204)
async def delete_item(id: UUID, session: SessionDep, service: ItemServiceDep) -> None:
    await service.delete(id)

