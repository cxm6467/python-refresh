from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import StoreServiceDep, StoreManagerDep
from app.database.models import Store
from app.api.schemas.store import StoreCreate, StoreUpdate

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/{id}", response_model=Store)
async def get_store(id: UUID, service: StoreServiceDep, manager: StoreManagerDep) -> Store:
    store = await service.get(id, manager)
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.get("/", response_model=dict[UUID, Store])
async def get_stores(service: StoreServiceDep, manager: StoreManagerDep) -> dict[UUID, Store]:
    stores = await service.get_all(manager)
    return {store.id: store for store in stores}


@router.post("/", response_model=Store, status_code=201)
async def create_store(
    store: StoreCreate,
    service: StoreServiceDep,
    manager: StoreManagerDep,
    assign_to_self: bool = Query(default=False, description="Assign this store to the current manager")
) -> Store:
    return await service.add(store, manager, assign_to_self)


@router.patch("/{id}", response_model=Store)
async def update_store(
    id: UUID,
    update: StoreUpdate,
    service: StoreServiceDep,
    manager: StoreManagerDep
) -> Store:
    return await service.update(id, update, manager)


@router.delete("/{id}", status_code=204)
async def delete_store(id: UUID, service: StoreServiceDep, manager: StoreManagerDep) -> None:
    await service.delete(id, manager)
