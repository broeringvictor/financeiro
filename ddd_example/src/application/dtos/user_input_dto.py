from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInputDTO:
    """
    DTO de entrada — dados brutos vindos da interface (HTTP, CLI, fila…).
    Não é uma entidade; não tem regras de negócio.
    """

    name: str
    email: str
