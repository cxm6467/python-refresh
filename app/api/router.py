from fastapi import APIRouter, HTTPException
from app.database.session import SessionDep
from app.database.models import Item
from app.api.schemas.models import ItemCreate, ItemUpdate
from app.services.item import ItemService

router = APIRouter()


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, session: SessionDep) -> Item:
    service = ItemService(session)
    item = await service.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items", response_model=dict[int, Item])
async def get_items(session: SessionDep) -> dict[int, Item]:
    service = ItemService(session)
    items = await service.get_all()
    return {item.id: item for item in items}


@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, session: SessionDep) -> Item:
    service = ItemService(session)
    return await service.add(item)


@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, update: ItemUpdate, session: SessionDep) -> Item:
    service = ItemService(session)
    return await service.update(item_id, update)


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, session: SessionDep) -> None:
    service = ItemService(session)
    await service.delete(item_id)

