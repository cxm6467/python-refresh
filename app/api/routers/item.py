from fastapi import APIRouter, HTTPException
from app.api.dependencies import SessionDep, ItemServiceDep, StoreManagerDep
from app.database.models import Item
from app.api.schemas.item import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/{id}", response_model=Item)
async def get_item(id: int, session: SessionDep, service: ItemServiceDep, _: StoreManagerDep) -> Item:
    item = await service.get(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/", response_model=dict[int, Item])
async def get_items(session: SessionDep, service: ItemServiceDep, _: StoreManagerDep) -> dict[int, Item]:
    items = await service.get_all()
    return {item.id: item for item in items}


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, session: SessionDep, service: ItemServiceDep, _: StoreManagerDep) -> Item:
    return await service.add(item)


@router.patch("/{id}", response_model=Item)
async def update_item(id: int, update: ItemUpdate, session: SessionDep, service: ItemServiceDep) -> Item:
    return await service.update(id, update)


@router.delete("/{id}", status_code=204)
async def delete_item(id: int, session: SessionDep, service: ItemServiceDep) -> None:
    await service.delete(id)

