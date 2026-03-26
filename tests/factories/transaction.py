import random
import uuid
from decimal import Decimal

import factory as factory_boy

from app.domain.entities.transaction import Transaction
from app.domain.enums.e_transaction import TransactionType
from app.infra.model.transaction_model import TransactionModel


class TransactionFactory(factory_boy.Factory):
    class Meta:
        model = TransactionModel
        exclude = ["user_id", "category_id", "type", "amount", "description"]

    user_id = factory_boy.LazyFunction(uuid.uuid8)
    category_id = factory_boy.LazyFunction(lambda: random.randint(1, 100))
    type = factory_boy.LazyFunction(lambda: random.choice(list(TransactionType)))
    amount = factory_boy.LazyFunction(lambda: Decimal(str(round(random.uniform(1.0, 10000.0), 2))))
    description = None

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        transaction = Transaction.create(
            user_id=kwargs.pop("user_id"),
            category_id=kwargs.pop("category_id"),
            type=kwargs.pop("type"),
            amount=kwargs.pop("amount"),
            description=kwargs.pop("description", None),
        )
        return model_class(
            id=transaction.id,
            user_id=transaction.user_id,
            category_id=transaction.category_id,
            type=transaction.type.name,
            amount=transaction.amount.value,
            occurred_at=transaction.occurred_at,
            description=transaction.description,
        )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._build(model_class, *args, **kwargs)
