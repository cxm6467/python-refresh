from app.api.routers import item, store_manager
from fastapi import APIRouter

master_router = APIRouter()
master_router.include_router(item.router)
master_router.include_router(store_manager.router)