from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from scalar_fastapi import get_scalar_api_reference
from app.database.session import create_db_tables
from app.api.router import router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)

@app.get("/")
def root():
    return RedirectResponse(url="scalar", status_code=302)


@app.get("/scalar", include_in_schema=False)
async def get_scalar_api_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

