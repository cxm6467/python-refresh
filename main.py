import os
from contextlib import asynccontextmanager
from sqlmodel import select
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from scalar_fastapi import get_scalar_api_reference
from models import Item, ItemCreate, ItemUpdate
from session import SessionDep, create_db_tables

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    # Skip table creation in dev if SKIP_DB_INIT=1 is set
    if not os.getenv("SKIP_DB_INIT"):
        await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)

# GET /items/{item_id}
@app.get("/")
def root():
    # return {"message": "Hello World"}
    return RedirectResponse(url="scalar", status_code=302)

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, session: SessionDep) -> Item:
        item = await session.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item


@app.get("/items", response_model=dict[int, Item])
async def get_items(session: SessionDep) -> dict[int, Item]:
    result = await session.exec(select(Item))
    items = result.all()
    return {item.id: item for item in items}


# POST /items
@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, session: SessionDep) -> Item:
        created = Item(**item.model_dump())
        session.add(created)
        await session.commit()
        await session.refresh(created)
        return created


# PATCH /items/{item_id}
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, update: ItemUpdate, session: SessionDep) -> Item:
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    item.sqlmodel_update(update.model_dump(exclude_unset=True))
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item



# DELETE /items/{item_id}
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, session: SessionDep) -> None:
        item = await session.get(Item, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        await session.commit()


# Scalar docs
@app.get("/scalar", include_in_schema=False)
async def get_scalar_api_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
