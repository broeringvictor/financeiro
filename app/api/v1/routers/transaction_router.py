from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.api.exception_handlers import format_errors
from app.api.v1.dependencies import (
    get_create_transaction_use_case,
    get_delete_transaction_use_case,
    get_transaction_use_case,
    get_update_transaction_use_case,
    get_user_transactions_by_type_use_case,
    get_user_transactions_use_case,
)
from app.application.dto.transaction_dto import (
    CreateTransactionInput,
    TransactionResponse,
    UpdateTransactionInput,
)
from app.application.use_cases.transaction.create_transaction import CreateTransactionUseCase
from app.application.use_cases.transaction.delete_transaction import DeleteTransactionUseCase
from app.application.use_cases.transaction.get_all_transactions import GetUserTransactionsByTypeUseCase, GetUserTransactionsUseCase
from app.application.use_cases.transaction.get_transaction import GetTransactionUseCase
from app.application.use_cases.transaction.update_transaction import UpdateTransactionUseCase
from app.domain.enums.e_transaction import TransactionType

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _handle_exc(exc: Exception) -> None:
    if isinstance(exc, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=format_errors(exc.errors()),
        )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
    )


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    body: CreateTransactionInput,
    use_case: CreateTransactionUseCase = Depends(get_create_transaction_use_case),
) -> TransactionResponse:
    try:
        return await use_case.execute(body)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)


@router.get("/user/{user_id}", response_model=list[TransactionResponse])
async def get_user_transactions(
    user_id: UUID,
    use_case: GetUserTransactionsUseCase = Depends(get_user_transactions_use_case),
) -> list[TransactionResponse]:
    return await use_case.execute(user_id)


@router.get("/user/{user_id}/type/{type}", response_model=list[TransactionResponse])
async def get_user_transactions_by_type(
    user_id: UUID,
    type: TransactionType,
    use_case: GetUserTransactionsByTypeUseCase = Depends(get_user_transactions_by_type_use_case),
) -> list[TransactionResponse]:
    return await use_case.execute(user_id, type)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    use_case: GetTransactionUseCase = Depends(get_transaction_use_case),
) -> TransactionResponse:
    try:
        return await use_case.execute(transaction_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    body: UpdateTransactionInput,
    use_case: UpdateTransactionUseCase = Depends(get_update_transaction_use_case),
) -> TransactionResponse:
    try:
        return await use_case.execute(
            UpdateTransactionInput(
                transaction_id=transaction_id,
                category_id=body.category_id,
                type=body.type,
                amount=body.amount,
                description=body.description,
            )
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    use_case: DeleteTransactionUseCase = Depends(get_delete_transaction_use_case),
) -> None:
    try:
        await use_case.execute(transaction_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
