# Python FastAPI CRUD API

A FastAPI-based REST API for managing items with SQLite persistence.

Following the tutorial: https://www.udemy.com/course/fastapi-guide/

## Project Structure

```
app/
├── main.py                   # Application entry point
├── api/
│   ├── router.py             # API route handlers
│   ├── dependencies.py       # Dependency injection
│   └── schemas/
│       └── models.py         # Pydantic models
├── database/
│   ├── config.py             # Database configuration
│   ├── models.py             # Database models
│   └── session.py            # Database session management
└── services/
    └── item.py               # Business logic for items
```

## Running the Application

```bash
fastapi dev
```

The server will start at `http://localhost:8000`

## API Endpoints

### Root
```
GET /
```
Returns: `{"message": "Hello World"}`

### Get All Items
```
GET /items
```
Returns: `dict[int, Item]` - Dictionary mapping item IDs to Item objects

### Get Item by ID
```
GET /items/{item_id}
```
Returns: `Item` object or 404 if not found

### Create Item
```
POST /items
```
Request body: `ItemCreate`
Returns: `Item` with auto-generated ID
Status: 201

### Update Item
```
PATCH /items/{item_id}
```
Request body: `ItemUpdate` (all fields optional)
Returns: Updated `Item` or 404 if not found

### Delete Item
```
DELETE /items/{item_id}
```
Returns: 204 No Content on success, 404 if not found

### API Documentation
```
GET /scalar
```
Interactive Scalar API documentation

## Models

### Category (Enum)
- `GROCERY`
- `HOUSEHOLD`
- `ELECTRONICS`
- `STATIONERY`
- `PERSONAL_CARE`
- `APPAREL`
- `HOME_IMPROVEMENT`
- `PET`

### Item
- `id: int` - Auto-generated unique identifier
- `name: str` - Item name (max 64 characters)
- `category: Category` - Item category enum
- `price_usd: float` - Price in USD (>= 0)
- `in_stock: bool` - Availability status

### ItemCreate
- `name: str` - Item name (max 64 characters)
- `category: Category` - Item category enum
- `price_usd: float` - Price in USD (>= 0)
- `in_stock: bool` - Availability status

### ItemUpdate
All fields are optional for partial updates:
- `name: str | None`
- `category: Category | None`
- `price_usd: float | None`
- `in_stock: bool | None`

## Database

The application uses SQLite for persistent storage with automatic connection management via context managers.

### Database Schema

```sql
CREATE TABLE items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_usd REAL NOT NULL,
    in_stock INTEGER NOT NULL
);
```

### Database Class Methods

- `create_item(item: ItemCreate) -> Item` - Insert new item with auto-generated ID
- `get_item(item_id: int) -> Item | None` - Fetch single item by ID
- `get_items() -> dict[int, Item]` - Fetch all items as dictionary
- `update_item(item_id: int, update: ItemUpdate) -> Item` - Update existing item
- `delete_item(item_id: int) -> None` - Delete item by ID
- `close()` - Close database connection

### Context Manager Support

The Database class implements the context manager protocol (`__enter__` and `__exit__`), allowing automatic connection cleanup:

```python
with Database() as db:
    item = db.get_item(item_id)
    # Connection automatically closed when exiting the 'with' block
```

This ensures proper resource management and prevents connection leaks.

### Security Features

- Parameterized queries using `?` placeholders to prevent SQL injection
- Type-safe with Pydantic validation
- Auto-increment IDs eliminate race conditions
- Automatic connection cleanup via context managers
