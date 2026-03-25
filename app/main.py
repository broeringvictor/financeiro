from fastapi import FastAPI

from app.api.v1.routers.user_router import router as user_router

app = FastAPI(title="Financeiro API")

app.include_router(user_router, prefix="/api/v1")
