from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.api.exception_handlers import format_errors
from app.api.v1.dependencies import (
    get_all_categories_use_case,
    get_categories_by_type_use_case,
    get_category_use_case,
    get_create_category_use_case,
    get_delete_category_use_case,
    get_update_category_use_case,
)
from app.application.dto.category_dto import (
    CategoryResponse,
    CreateCategoryInput,
    UpdateCategoryInput,
)
from app.application.use_cases.category.create_category import CreateCategoryUseCase
from app.application.use_cases.category.delete_category import DeleteCategoryUseCase
from app.application.use_cases.category.get_all_categories import GetAllCategoriesUseCase
from app.application.use_cases.category.get_category import GetCategoriesByTypeUseCase, GetCategoryUseCase
from app.application.use_cases.category.update_category import UpdateCategoryUseCase
from app.domain.enums.e_transaction import TransactionType

router = APIRouter(prefix="/categories", tags=["categories"])


def _handle_exc(exc: Exception) -> None:
    if isinstance(exc, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=format_errors(exc.errors()),
        )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
    )


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CreateCategoryInput,
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(body)
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)


@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(
    use_case: GetAllCategoriesUseCase = Depends(get_all_categories_use_case),
) -> list[CategoryResponse]:
    return await use_case.execute()


@router.get("/by-type/{type}", response_model=list[CategoryResponse])
async def get_categories_by_type(
    type: TransactionType,
    use_case: GetCategoriesByTypeUseCase = Depends(get_categories_by_type_use_case),
) -> list[CategoryResponse]:
    return await use_case.execute(type)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    use_case: GetCategoryUseCase = Depends(get_category_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(category_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    body: UpdateCategoryInput,
    use_case: UpdateCategoryUseCase = Depends(get_update_category_use_case),
) -> CategoryResponse:
    try:
        return await use_case.execute(
            UpdateCategoryInput(
                category_id=category_id,
                name=body.name,
                description=body.description,
            )
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends(get_delete_category_use_case),
) -> None:
    try:
        await use_case.execute(category_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
