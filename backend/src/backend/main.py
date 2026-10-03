from fastapi import APIRouter, FastAPI

from backend.api import health

API_V1_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    app = FastAPI(title="EMG Formulary API")

    v1 = APIRouter(prefix=API_V1_PREFIX)
    v1.include_router(health.router)
    app.include_router(v1)

    return app


app = create_app()
