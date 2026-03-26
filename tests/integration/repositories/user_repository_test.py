import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.infra.repositories.user_repository import UserRepository
from tests.factories.user import UserFactory


@pytest_asyncio.fixture
async def repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)


@pytest_asyncio.fixture
async def saved_user(repo: UserRepository, session: AsyncSession) -> User:
    user = User.create("João", "Silva", "Senha@1234", "joao@example.com")
    await repo.save(user)
    await session.flush()
    return user


class TestUserRepositorySave:
    @pytest.mark.asyncio
    async def test_save_persists_user(self, repo: UserRepository, session: AsyncSession):
        user = User.create("Maria", "Costa", "Senha@1234", "maria@example.com")
        await repo.save(user)
        await session.flush()

        found = await repo.find_by_id(user.id)

        assert found is not None
        assert found.id == user.id

    @pytest.mark.asyncio
    async def test_save_preserves_email(self, repo: UserRepository, session: AsyncSession):
        user = User.create("Carlos", "Lima", "Senha@1234", "carlos@example.com")
        await repo.save(user)
        await session.flush()

        found = await repo.find_by_id(user.id)

        assert found.email == "carlos@example.com"

    @pytest.mark.asyncio
    async def test_save_preserves_active_status(self, repo: UserRepository, session: AsyncSession):
        user = User.create("Ana", "Souza", "Senha@1234", "ana@example.com")
        await repo.save(user)
        await session.flush()

        found = await repo.find_by_id(user.id)

        assert found.is_active is True


class TestUserRepositoryFindById:
    @pytest.mark.asyncio
    async def test_find_by_id_returns_user(self, repo: UserRepository, saved_user: User):
        found = await repo.find_by_id(saved_user.id)

        assert found is not None
        assert found.id == saved_user.id

    @pytest.mark.asyncio
    async def test_find_by_id_returns_none_when_not_found(self, repo: UserRepository):
        from uuid import uuid8
        found = await repo.find_by_id(uuid8())

        assert found is None

    @pytest.mark.asyncio
    async def test_find_by_id_reconstructs_name(self, repo: UserRepository, saved_user: User):
        found = await repo.find_by_id(saved_user.id)

        assert found.name.value == saved_user.name.value

    @pytest.mark.asyncio
    async def test_find_by_id_reconstructs_password(self, repo: UserRepository, saved_user: User):
        found = await repo.find_by_id(saved_user.id)

        assert found.password.verify("Senha@1234") is True


class TestUserRepositoryFindByEmail:
    @pytest.mark.asyncio
    async def test_find_by_email_returns_user(self, repo: UserRepository, saved_user: User):
        found = await repo.find_by_email("joao@example.com")

        assert found is not None
        assert found.email == "joao@example.com"

    @pytest.mark.asyncio
    async def test_find_by_email_is_case_insensitive(self, repo: UserRepository, saved_user: User):
        found = await repo.find_by_email("JOAO@EXAMPLE.COM")

        assert found is not None
        assert found.email == "joao@example.com"

    @pytest.mark.asyncio
    async def test_find_by_email_returns_none_when_not_found(self, repo: UserRepository):
        found = await repo.find_by_email("naoexiste@example.com")

        assert found is None


class TestUserRepositoryListAll:
    @pytest.mark.asyncio
    async def test_list_all_returns_empty(self, repo: UserRepository):
        users = await repo.list_all()

        assert users == []

    @pytest.mark.asyncio
    async def test_list_all_returns_all_users(self, repo: UserRepository, session: AsyncSession):
        u1 = User.create("João", "Silva", "Senha@1234", "u1@example.com")
        u2 = User.create("Maria", "Costa", "Senha@1234", "u2@example.com")
        await repo.save(u1)
        await repo.save(u2)
        await session.flush()

        users = await repo.list_all()

        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_list_all_returns_correct_entities(self, repo: UserRepository, session: AsyncSession):
        user = User.create("Carlos", "Lima", "Senha@1234", "carlos2@example.com")
        await repo.save(user)
        await session.flush()

        users = await repo.list_all()
        emails = [u.email for u in users]

        assert "carlos2@example.com" in emails


class TestUserRepositoryDelete:
    @pytest.mark.asyncio
    async def test_delete_removes_user(self, repo: UserRepository, saved_user: User, session: AsyncSession):
        await repo.delete(saved_user.id)
        await session.flush()

        found = await repo.find_by_id(saved_user.id)

        assert found is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_does_not_raise(self, repo: UserRepository):
        from uuid import uuid8
        await repo.delete(uuid8())  # não deve lançar
