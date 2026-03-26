from app.domain.repositories.category_repository import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, repo: ICategoryRepository) -> None:
        self._repo = repo

    async def execute(self, category_id: int) -> None:
        if not await self._repo.find_by_id(category_id):
            raise LookupError(f"Categoria '{category_id}' não encontrada.")
        await self._repo.delete(category_id)
