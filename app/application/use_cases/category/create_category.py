from app.application.dto.category_dto import CategoryResponse, CreateCategoryInput
from app.domain.entities.category import Category
from app.domain.repositories.category_repository import ICategoryRepository


class CreateCategoryUseCase:
    def __init__(self, repo: ICategoryRepository) -> None:
        self._repo = repo

    async def execute(self, input_data: CreateCategoryInput) -> CategoryResponse:
        category = Category.create(
            name=input_data.name,
            type=input_data.type,
            description=input_data.description,
        )
        saved = await self._repo.save(category)
        return CategoryResponse(
            category_id=saved.id,
            name=saved.name,
            type=saved.type.name,
            description=saved.description,
        )
