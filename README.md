# Python FastAPI CRUD API

A FastAPI-based REST API for managing items and store managers with PostgreSQL persistence, JWT authentication, and async operations.

Following the tutorial: https://www.udemy.com/course/fastapi-guide/

## Project Structure

```
app/
├── main.py                          # Application entry point
├── api/
│   ├── router.py                    # Master router combining all routers
│   ├── dependencies.py              # Dependency injection for services
│   ├── routers/
│   │   ├── item.py                  # Item route handlers
│   │   └── store_manager.py         # Store manager route handlers
│   └── schemas/
│       ├── item.py                  # Pydantic models for items
│       └── store_manager.py         # Pydantic models for store managers
├── database/
│   ├── models.py                    # SQLModel database models
│   └── session.py                   # Async database session management
└── services/
    ├── item.py                      # Business logic for items
    └── store_manager.py             # Business logic for store managers
config.py                            # Configuration management
.env.example                         # Example environment variables
```

## Setup

1. Copy `.env.example` to `.env` and configure your environment variables:
   - PostgreSQL connection details
   - JWT secret and algorithm

2. Install dependencies (ensure PostgreSQL is running)

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
Redirects to `/scalar` (API documentation)

### Items

#### Get All Items
```
GET /items
```
Returns: `dict[int, Item]` - Dictionary mapping item IDs to Item objects

#### Get Item by ID
```
GET /items/{id}
```
Returns: `Item` object or 404 if not found

#### Create Item
```
POST /items
```
Request body: `ItemCreate`
Returns: `Item` with auto-generated ID
Status: 201

#### Update Item
```
PATCH /items/{id}
```
Request body: `ItemUpdate` (all fields optional)
Returns: Updated `Item` or 404 if not found

#### Delete Item
```
DELETE /items/{id}
```
Returns: 204 No Content on success, 404 if not found

### Store Managers

#### Create Store Manager
```
POST /store-managers
```
Request body: `StoreManagerCreate`
Returns: `StoreManager` with auto-generated ID
Status: 201

#### Login (Get Access Token)
```
POST /store-managers/token
```
Request body: OAuth2PasswordRequestForm (username=email, password)
Returns: `{"access_token": string, "token_type": "jwt"}`

### API Documentation
```
GET /scalar
```
Interactive Scalar API documentation

## Models

### Category (Enum)
- `GROCERY` - "Grocery"
- `HOUSEHOLD` - "Household"
- `ELECTRONICS` - "Electronics"
- `STATIONERY` - "Stationery"
- `PERSONAL_CARE` - "Personal Care"
- `APPAREL` - "Apparel"
- `HOME_IMPROVEMENT` - "Home Improvement"
- `PET` - "Pet"

### Item
- `id: int | None` - Auto-generated unique identifier (primary key)
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

### StoreManager
- `id: int | None` - Auto-generated unique identifier (primary key)
- `name: str` - Store manager name (max 64 characters)
- `email: EmailStr` - Valid email address
- `password_hash: str` - Bcrypt hashed password

### StoreManagerCreate
- `name: str` - Store manager name (max 64 characters)
- `email: EmailStr` - Valid email address
- `password_hash: str` - Plain password (will be hashed before storage)

## Database

The application uses PostgreSQL for persistent storage with SQLModel ORM and async database operations.

### Configuration

Database connection is configured via environment variables:
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Database host
- `POSTGRES_PORT` - Database port (default: 5432)
- `POSTGRES_DB` - Database name

Connection URL format: `postgresql+psycopg://{user}:{password}@{host}:{port}/{db}`

### Connection Pool Settings
- `pool_pre_ping: True` - Verify connections before using
- `pool_size: 5` - Number of connections to maintain
- `max_overflow: 10` - Maximum overflow connections
- `echo: True` - SQL query logging (for debugging)

### Database Tables

#### items
- `id` - INTEGER PRIMARY KEY (auto-increment)
- `name` - TEXT NOT NULL (max 64 chars)
- `category` - TEXT NOT NULL
- `price_usd` - REAL NOT NULL (>= 0)
- `in_stock` - BOOLEAN NOT NULL

#### store_managers
- `id` - INTEGER PRIMARY KEY (auto-increment)
- `name` - TEXT NOT NULL (max 64 chars)
- `email` - TEXT NOT NULL (validated email)
- `password_hash` - TEXT NOT NULL (bcrypt hash)

### Service Layer

Both `ItemService` and `StoreManagerService` use async operations and provide CRUD methods via dependency injection.

#### ItemService Methods
- `async get(id: int) -> Item | None` - Fetch single item by ID
- `async get_all() -> list[Item]` - Fetch all items
- `async add(item: ItemCreate) -> Item` - Create new item
- `async update(id: int, update: ItemUpdate) -> Item` - Update existing item
- `async delete(id: int) -> None` - Delete item by ID

#### StoreManagerService Methods
- `async get(id: int) -> StoreManager | None` - Fetch single store manager by ID
- `async add(manager: StoreManagerCreate) -> StoreManager` - Create new store manager with password hashing
- `async token(email: str, password_hash: str) -> dict[str, str]` - Authenticate and generate JWT token

### Automatic Table Creation

Tables are automatically created on application startup via the `lifespan_handler` in `main.py`.

## Security Features

### Authentication
- JWT-based authentication for store managers
- OAuth2 password flow for login
- Tokens expire after 3 hours
- Configurable JWT algorithm and secret via environment variables

### Password Security
- Bcrypt password hashing with `passlib`
- Passwords are hashed before database storage
- Secure password verification during login

### Database Security
- Async SQLAlchemy with parameterized queries (SQL injection prevention)
- Type-safe with Pydantic validation
- Auto-increment IDs eliminate race conditions
- Connection pooling with automatic cleanup
