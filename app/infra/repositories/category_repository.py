from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.enums.e_transaction import TransactionType
from app.infra.model.category_model import CategoryModel


class CategoryRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── persistência ──────────────────────────────────────────────────────────

    async def save(self, category: Category) -> Category:
        model = self._to_model(category)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def update(self, category: Category) -> Category:
        model = await self._session.get(CategoryModel, category.id)
        if not model:
            raise LookupError(f"Categoria '{category.id}' não encontrada.")
        model.name = category.name
        model.description = category.description
        await self._session.flush()
        return self._to_entity(model)

    async def delete(self, category_id: int) -> None:
        model = await self._session.get(CategoryModel, category_id)
        if model:
            await self._session.delete(model)

    # ── consultas ─────────────────────────────────────────────────────────────

    async def find_by_id(self, category_id: int) -> Category | None:
        model = await self._session.get(CategoryModel, category_id)
        return self._to_entity(model) if model else None

    async def find_by_type(self, type: TransactionType) -> list[Category]:
        result = await self._session.execute(
            select(CategoryModel).where(CategoryModel.type == type)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def list_all(self) -> list[Category]:
        result = await self._session.execute(select(CategoryModel))
        return [self._to_entity(m) for m in result.scalars().all()]

    # ── mapeamento Entity ↔ Model ─────────────────────────────────────────────

    @staticmethod
    def _to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            name=category.name,
            type=category.type,
            description=category.description,
        )

    @staticmethod
    def _to_entity(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            type=model.type,
            description=model.description,
        )
