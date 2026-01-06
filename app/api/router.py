from sqlmodel import select
from fastapi import APIRouter, HTTPException
from app.database.session import SessionDep
from app.database.models import Item
from app.api.models import ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, session: SessionDep) -> Item:
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items", response_model=dict[int, Item])
async def get_items(session: SessionDep) -> dict[int, Item]:
    result = await session.execute(select(Item))
    items = result.scalars().all()
    return {item.id: item for item in items}


@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, session: SessionDep) -> Item:
    created = Item(**item.model_dump())
    session.add(created)
    await session.commit()
    await session.refresh(created)
    return created


@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, update: ItemUpdate, session: SessionDep) -> Item:
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    item.sqlmodel_update(update.model_dump(exclude_unset=True))
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, session: SessionDep) -> None:
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(item)
    await session.commit()

