import pytest

from app.domain.entities.user import User


class TestUserCreate:
    def test_create_valid_user(self):
        user = User.create(
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            password="Senha@1234",
        )

        assert user.name.value == "João Silva"
        assert user.email == "joao@example.com"
        assert user.is_active is True
        assert user.id is not None
        assert user.create_at is not None
        assert user.modified_at is not None

    def test_email_is_normalized(self):
        user = User.create(
            first_name="João",
            last_name="Silva",
            email="  JOAO@EXAMPLE.COM  ",
            password="Senha@1234",
        )

        assert user.email == "joao@example.com"

    def test_password_is_hashed(self):
        user = User.create(
            first_name="João",
            last_name="Silva",
            email="joao@example.com",
            password="Senha@1234",
        )

        assert user.password.hashed_value != "Senha@1234"
        assert user.password.verify("Senha@1234") is True

    def test_each_user_has_unique_id(self):
        user1 = User.create("João", "Silva", "Senha@1234", "joao@example.com")
        user2 = User.create("Maria", "Costa", "Senha@1234", "b@example.com")

        assert user1.id != user2.id


class TestUserChangePassword:
    def test_change_password_success(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        user.change_password("Senha@1234", "NovaSenha@5678")

        assert user.password.verify("NovaSenha@5678") is True
        assert user.password.verify("Senha@1234") is False

    def test_change_password_wrong_current_raises(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        with pytest.raises(ValueError, match="Senha atual incorreta"):
            user.change_password("SenhaErrada@1", "NovaSenha@5678")

    def test_change_password_updates_modified_at(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")
        before = user.modified_at

        user.change_password("Senha@1234", "NovaSenha@5678")

        assert user.modified_at >= before


class TestUserUpdate:
    def test_update_first_name(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        user.update(first_name="Carlos")

        assert user.name.first_name == "Carlos"
        assert user.name.last_name == "Silva"

    def test_update_last_name(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        user.update(last_name="Costa")

        assert user.name.first_name == "João"
        assert user.name.last_name == "Costa"

    def test_update_email(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        user.update(email="novo@example.com")

        assert user.email == "novo@example.com"

    def test_update_updates_modified_at(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")
        before = user.modified_at

        user.update(first_name="Carlos")

        assert user.modified_at >= before

    def test_update_no_args_keeps_data(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        user.update()

        assert user.name.value == "João Silva"
        assert user.email == "joao@example.com"


class TestUserPublicUser:
    def test_public_user_excludes_password(self):
        user = User.create("João", "Silva", "Senha@1234", "joao@example.com")

        data = user.public_user()

        assert "password" not in data
        assert "email" in data
