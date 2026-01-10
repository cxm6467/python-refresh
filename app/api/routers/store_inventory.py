from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.api.dependencies import StoreInventoryServiceDep, StoreManagerDep
from app.database.models import StoreInventory
from app.api.schemas.store_inventory import StoreInventoryCreate, StoreInventoryUpdate

router = APIRouter(prefix="/store-inventories", tags=["store-inventories"])


@router.get("/{id}", response_model=StoreInventory)
async def get_store_inventory(
    id: UUID,
    service: StoreInventoryServiceDep,
    _: StoreManagerDep
) -> StoreInventory:
    inventory = await service.get(id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Store inventory not found")
    return inventory


@router.get("/", response_model=dict[UUID, StoreInventory])
async def get_store_inventories(
    service: StoreInventoryServiceDep,
    _: StoreManagerDep
) -> dict[UUID, StoreInventory]:
    inventories = await service.get_all()
    return {inv.id: inv for inv in inventories}


@router.post("/", response_model=StoreInventory, status_code=201)
async def create_store_inventory(
    inventory: StoreInventoryCreate,
    service: StoreInventoryServiceDep,
    _: StoreManagerDep
) -> StoreInventory:
    return await service.add(inventory)


@router.patch("/{id}", response_model=StoreInventory)
async def update_store_inventory(
    id: UUID,
    update: StoreInventoryUpdate,
    service: StoreInventoryServiceDep,
    _: StoreManagerDep
) -> StoreInventory:
    return await service.update(id, update)


@router.delete("/{id}", status_code=204)
async def delete_store_inventory(
    id: UUID,
    service: StoreInventoryServiceDep,
    _: StoreManagerDep
) -> None:
    await service.delete(id)
