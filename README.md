# Python FastAPI CRUD API

## Project Structure

```
python-refresh/
├── main.py          # FastAPI app and route handlers
├── models.py        # Pydantic models
├── database.py      # In-memory database
└── README.md
```

## Running the Application

```bash
fastapi dev
```

## API Endpoints

### Root
```
GET /
```

### Get All Items
```
GET /items
```

### Get Item by ID
```
GET /items/{item_id}
```

### Create Item
```
POST /items
```

### Update Item
```
PATCH /items/{item_id}
```

### Delete Item
```
DELETE /items/{item_id}
```

### API Documentation
```
GET /scalar
```

## Models

### Item
- `id: int`
- `name: str`
- `category: str`
- `price_usd: float`
- `in_stock: bool`

### ItemCreate
- `name: str`
- `category: str`
- `price_usd: float`
- `in_stock: bool`

### ItemUpdate
- `name: str | None`
- `category: str | None`
- `price_usd: float | None`
- `in_stock: bool | None`
