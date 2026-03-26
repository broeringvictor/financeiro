import random

import factory as factory_boy
from faker import Faker

from app.domain.entities.category import Category
from app.domain.enums.e_transaction import TransactionType
from app.infra.model.category_model import CategoryModel

_faker = Faker("pt_BR")


class CategoryFactory(factory_boy.Factory):
    class Meta:
        model = CategoryModel
        exclude = ["name", "type", "description"]

    name = factory_boy.LazyFunction(lambda: _faker.word())
    type = factory_boy.LazyFunction(lambda: random.choice(list(TransactionType)))
    description = factory_boy.LazyFunction(lambda: None)

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        category = Category.create(
            name=str(kwargs.pop("name")),
            type=TransactionType(kwargs.pop("type")),
            description=kwargs.pop("description", None),
        )
        return model_class(
            name=category.name,
            type=category.type,
            description=category.description,
        )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._build(model_class, *args, **kwargs)
