from app.application.dto.category_dto import CategoryResponse
from app.domain.repositories.category_repository import ICategoryRepository


class GetAllCategoriesUseCase:
    def __init__(self, repo: ICategoryRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[CategoryResponse]:
        categories = await self._repo.list_all()
        return [
            CategoryResponse(
                category_id=c.id,
                name=c.name,
                type=c.type.name,
                description=c.description,
            )
            for c in categories
        ]
