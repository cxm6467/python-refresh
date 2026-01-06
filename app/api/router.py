from fastapi import APIRouter, HTTPException
from app.api.dependencies import SessionDep, ServiceDep
from app.database.models import Item
from app.api.schemas.models import ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, session: SessionDep, service: ServiceDep) -> Item:
    item = await service.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items", response_model=dict[int, Item])
async def get_items(session: SessionDep, service: ServiceDep) -> dict[int, Item]:
    items = await service.get_all()
    return {item.id: item for item in items}


@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, session: SessionDep, service: ServiceDep) -> Item:
    return await service.add(item)


@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, update: ItemUpdate, session: SessionDep, service: ServiceDep) -> Item:
    return await service.update(item_id, update)


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, session: SessionDep, service: ServiceDep) -> None:
    await service.delete(item_id)

