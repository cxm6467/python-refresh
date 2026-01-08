# Python FastAPI CRUD API

A FastAPI-based REST API for managing items and store managers with PostgreSQL persistence, Redis token blacklisting, JWT authentication, and async operations.

Following the tutorial: https://www.udemy.com/course/fastapi-guide/

## Project Structure

```
app/
├── main.py                          # Application entry point
├── api/
│   ├── router.py                    # Master router combining all routers
│   ├── dependencies.py              # Dependency injection for services
│   ├── core/
│   │   └── security.py              # OAuth2 security schemes
│   ├── routers/
│   │   ├── item.py                  # Item route handlers
│   │   └── store_manager.py         # Store manager route handlers
│   └── schemas/
│       ├── item.py                  # Pydantic models for items
│       └── store_manager.py         # Pydantic models for store managers
├── database/
│   ├── models.py                    # SQLModel database models
│   ├── session.py                   # Async database session management
│   └── redis.py                     # Redis connection and token blacklisting
├── services/
│   ├── item.py                      # Business logic for items
│   └── store_manager.py             # Business logic for store managers
└── utils.py                         # JWT token generation and validation
config.py                            # Configuration management (DatabaseConfig, SecurityConfig)
alembic.ini                          # Alembic configuration for migrations
migrations/                          # Database migration scripts
.env.example                         # Example environment variables
```

## Setup

1. Copy `.env.example` to `.env` and configure your environment variables:
   - PostgreSQL connection details
   - Redis connection details
   - JWT secret and algorithm

2. Install dependencies (ensure PostgreSQL and Redis are running)

3. Run database migrations:
   ```bash
   alembic upgrade head
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
Redirects to `/scalar` (API documentation)

### Items

**Note: All item endpoints require authentication (Bearer JWT token)**

#### Get All Items
```
GET /items
```
Returns: `dict[UUID, Item]` - Dictionary mapping item UUIDs to Item objects

#### Get Item by ID
```
GET /items/{id}
```
Path parameter: `id` (UUID)
Returns: `Item` object or 404 if not found

#### Create Item
```
POST /items
```
Request body: `ItemCreate`
Returns: `Item` with auto-generated UUID, associated with authenticated store manager
Status: 201

#### Update Item
```
PATCH /items/{id}
```
Path parameter: `id` (UUID)
Request body: `ItemUpdate` (all fields optional)
Returns: Updated `Item` or 404 if not found

#### Delete Item
```
DELETE /items/{id}
```
Path parameter: `id` (UUID)
Returns: 204 No Content on success, 404 if not found

### Store Managers

#### Create Store Manager
```
POST /store-managers
```
Request body: `StoreManagerCreate`
Returns: `StoreManager` with auto-generated UUID
Status: 201

#### Login (Get Access Token)
```
POST /store-managers/token
```
Request body: OAuth2PasswordRequestForm (username=email, password)
Returns: `{"access_token": string, "token_type": "jwt"}`

#### Logout (Blacklist Token)
```
GET /store-managers/logout
```
Requires: Bearer JWT token in Authorization header
Returns: `{"message": "Logged out successfully"}`
Note: Blacklists the current token in Redis, preventing further use

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
- `id: UUID | None` - Auto-generated UUID primary key
- `name: str` - Item name (max 64 characters)
- `category: Category` - Item category enum
- `price_usd: float` - Price in USD (>= 0)
- `in_stock: bool` - Availability status
- `store_manager_id: UUID` - Foreign key to store manager who owns this item
- `store_manager: StoreManager` - Related store manager object

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
- `id: UUID | None` - Auto-generated UUID primary key
- `name: str` - Store manager name (max 64 characters)
- `email: EmailStr` - Valid email address
- `password_hash: str` - Bcrypt hashed password
- `items: list[Item]` - Related items owned by this store manager

### StoreManagerCreate
- `name: str` - Store manager name (max 64 characters)
- `email: EmailStr` - Valid email address
- `password_hash: str` - Plain password (will be hashed before storage)

## Database

The application uses PostgreSQL for persistent storage and Redis for token blacklisting, with SQLModel ORM and async database operations.

### PostgreSQL Configuration

Database connection is configured via environment variables:
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Database host
- `POSTGRES_PORT` - Database port (default: 5432)
- `POSTGRES_DB` - Database name

Connection URL format: `postgresql+psycopg://{user}:{password}@{host}:{port}/{db}`

### Redis Configuration

Redis is used for JWT token blacklisting (logout functionality):
- `REDIS_HOST` - Redis server host
- `REDIS_PORT` - Redis server port (default: 6379)
- `REDIS_DB` - Redis database number (default: 0)

### Connection Pool Settings
- `pool_pre_ping: True` - Verify connections before using
- `pool_size: 5` - Number of connections to maintain
- `max_overflow: 10` - Maximum overflow connections
- `echo: True` - SQL query logging (for debugging)

### PostgreSQL Database Tables

#### items
- `id` - UUID PRIMARY KEY (auto-generated)
- `name` - TEXT NOT NULL (max 64 chars)
- `category` - TEXT NOT NULL
- `price_usd` - REAL NOT NULL (>= 0)
- `in_stock` - BOOLEAN NOT NULL
- `store_manager_id` - UUID FOREIGN KEY REFERENCES store_managers(id)

#### store_managers
- `id` - UUID PRIMARY KEY (auto-generated)
- `name` - TEXT NOT NULL (max 64 chars)
- `email` - TEXT NOT NULL (validated email)
- `password_hash` - TEXT NOT NULL (bcrypt hash)

### Redis Token Blacklist

Redis stores blacklisted JWT tokens with the following structure:
- Key: JWT `jti` (token ID)
- Value: JSON object with `{"jti": string, "status": "blacklisted", "created_at": ISO timestamp, "updated_at": ISO timestamp}`

### Service Layer

Both `ItemService` and `StoreManagerService` use async operations and provide CRUD methods via dependency injection.

#### ItemService Methods
- `async get(id: UUID) -> Item | None` - Fetch single item by UUID
- `async get_all() -> list[Item]` - Fetch all items
- `async add(item: ItemCreate, store_manager_id: UUID) -> Item` - Create new item associated with store manager
- `async update(id: UUID, update: ItemUpdate) -> Item` - Update existing item
- `async delete(id: UUID) -> None` - Delete item by UUID

#### StoreManagerService Methods
- `async get(id: int) -> StoreManager | None` - Fetch single store manager by ID
- `async add(manager: StoreManagerCreate) -> StoreManager` - Create new store manager with bcrypt password hashing
- `async token(email: str, password_hash: str) -> dict[str, str]` - Authenticate and generate JWT token with jti
- `async logout(token_id: str) -> None` - Blacklist JWT token in Redis

### Database Migrations

The application uses Alembic for database schema migrations:

- **Configuration**: `alembic.ini` - Alembic configuration file
- **Migration scripts**: `migrations/` - Contains version scripts and environment configuration
- **Create migration**: `alembic revision --autogenerate -m "description"`
- **Apply migrations**: `alembic upgrade head`
- **Rollback**: `alembic downgrade -1`

### Automatic Table Creation

Tables are automatically created on application startup via the `lifespan_handler` in `main.py` if not using Alembic migrations.

## Security Features

### Authentication
- JWT-based authentication for store managers
- OAuth2 password flow for login
- Tokens expire after 1 day (24 hours)
- Each token includes a unique `jti` (JWT ID) for tracking
- Configurable JWT algorithm and secret via environment variables
- Token blacklisting via Redis for logout functionality
- Tokens are validated on each protected endpoint request
- Blacklisted tokens are immediately invalidated

### Password Security
- Bcrypt password hashing with `passlib`
- Passwords are hashed before database storage
- Secure password verification during login
- CryptContext with bcrypt scheme and auto-deprecation

### Database Security
- Async SQLAlchemy with parameterized queries (SQL injection prevention)
- Type-safe with Pydantic validation
- UUID primary keys for better security and scalability
- Foreign key constraints ensure referential integrity
- Connection pooling with automatic cleanup
- Pre-ping verification to prevent stale connections
