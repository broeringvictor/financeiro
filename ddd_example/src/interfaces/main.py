from fastapi import FastAPI

from app.infrastructure.database.session import Base, engine
from app.interfaces.api.v1.routers import user_router


def create_app() -> FastAPI:
    # Cria as tabelas (em produção use Alembic)
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="DDD com FastAPI — Exemplo",
        description="Exemplo didático de Domain-Driven Design com FastAPI",
        version="0.1.0",
    )

    app.include_router(user_router.router, prefix="/api/v1")

    return app


app = create_app()
