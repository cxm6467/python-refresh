from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    category: str
    price_usd: float
    in_stock: bool


class ItemCreate(BaseModel):
    name: str
    category: str
    price_usd: float
    in_stock: bool


class ItemUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price_usd: float | None = None
    in_stock: bool | None = None


db: dict[str, list[Item]] = {
    "items": [
        Item(
            id=1,
            name="Whole Bean Coffee (12 oz)",
            category="grocery",
            price_usd=12.99,
            in_stock=True,
        ),
        Item(
            id=2,
            name="Dish Soap (24 oz)",
            category="household",
            price_usd=4.49,
            in_stock=True,
        ),
        Item(
            id=3,
            name="USB-C Charging Cable (1m)",
            category="electronics",
            price_usd=9.99,
            in_stock=True,
        ),
        Item(
            id=4,
            name="Notebook (College Ruled)",
            category="stationery",
            price_usd=2.29,
            in_stock=True,
        ),
        Item(
            id=5,
            name="Shampoo (16 oz)",
            category="personal_care",
            price_usd=7.79,
            in_stock=False,
        ),
        Item(
            id=6,
            name="Extra Virgin Olive Oil (500ml)",
            category="grocery",
            price_usd=11.49,
            in_stock=True,
        ),
        Item(
            id=7,
            name="Men's Cotton T-Shirt (M)",
            category="apparel",
            price_usd=14.99,
            in_stock=True,
        ),
        Item(
            id=8,
            name="LED Light Bulb (60W Equivalent)",
            category="home_improvement",
            price_usd=3.99,
            in_stock=True,
        ),
        Item(
            id=9,
            name="Toothpaste (6 oz)",
            category="personal_care",
            price_usd=3.49,
            in_stock=False,
        ),
        Item(
            id=10,
            name="Dog Treats (8 oz)",
            category="pet",
            price_usd=6.99,
            in_stock=True,
        ),
    ]
}


def find_item_by_id(item_id: int) -> Item | None:
    return next((i for i in db["items"] if i.id == item_id), None)


# GET /items/{item_id}
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items", response_model=list[Item])
def get_items() -> list[Item]:
    return db["items"]


# POST /items
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate) -> Item:
    next_id = max((i.id for i in db["items"]), default=0) + 1
    created = Item(id=next_id, **item.model_dump())
    db["items"].append(created)
    return created


# PATCH /items/{item_id}
@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: int, update: ItemUpdate) -> Item:
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    return item


# DELETE /items/{item_id}
@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> None:
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db["items"].remove(item)


# Scalar docs
@app.get("/scalar", include_in_schema=False)
def get_scalar_api_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
