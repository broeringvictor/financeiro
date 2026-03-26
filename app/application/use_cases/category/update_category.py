from app.application.dto.category_dto import CategoryResponse, UpdateCategoryInput
from app.domain.repositories.category_repository import ICategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, repo: ICategoryRepository) -> None:
        self._repo = repo

    async def execute(self, input_data: UpdateCategoryInput) -> CategoryResponse:
        category = await self._repo.find_by_id(input_data.category_id)
        if not category:
            raise LookupError(f"Categoria '{input_data.category_id}' não encontrada.")

        category.update(
            name=input_data.name,
            description=input_data.description,
        )
        updated = await self._repo.update(category)

        return CategoryResponse(
            category_id=updated.id,
            name=updated.name,
            type=updated.type.name,
            description=updated.description,
        )
