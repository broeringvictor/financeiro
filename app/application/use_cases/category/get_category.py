from app.application.dto.category_dto import CategoryResponse
from app.domain.enums.e_transaction import TransactionType
from app.domain.repositories.category_repository import ICategoryRepository


class GetCategoryUseCase:
    def __init__(self, repo: ICategoryRepository) -> None:
        self._repo = repo

    async def execute(self, category_id: int) -> CategoryResponse:
        category = await self._repo.find_by_id(category_id)
        if not category:
            raise LookupError(f"Categoria '{category_id}' não encontrada.")
        return CategoryResponse(
            category_id=category.id,
            name=category.name,
            type=category.type.name,
            description=category.description,
        )


class GetCategoriesByTypeUseCase:
    def __init__(self, repo: ICategoryRepository) -> None:
        self._repo = repo

    async def execute(self, type: TransactionType) -> list[CategoryResponse]:
        categories = await self._repo.find_by_type(type)
        return [
            CategoryResponse(
                category_id=c.id,
                name=c.name,
                type=c.type.name,
                description=c.description,
            )
            for c in categories
        ]
