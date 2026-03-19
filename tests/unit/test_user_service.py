import pytest
from app.models.user import User
from app.services.user_service import UserService
from app.core.extensions import db
import datetime

class TestUserService:
    """Tests pour UserService."""

    def test_create_user_success(self, app):
        """Test création utilisateur réussie."""
        user = User(
            first_name="Will",
            last_name="Smith",
            email="will.smith@example.com",
            birth_date=datetime.date(1985, 5, 15)
        )

        result = UserService.create_user(user)

        assert result.id is not None
        assert result.first_name == "Will"
        assert result.email == "will.smith@example.com"
        assert result.created_at is not None
        assert result in db.session

    def test_create_user_duplicate_email(self, app, sample_user):
        """Test échec création avec email dupliqué."""
        user = User(
            first_name="Duplicate",
            last_name="User",
            email=sample_user.email,
            birth_date=datetime.date(2000, 1, 1)
        )

        with pytest.raises(ValueError, match="An user with this email already exists"):
            UserService.create_user(user)

    def test_get_user_by_id_success(self, app, sample_user):
        """Test récupération utilisateur par ID réussie."""
        result = UserService.get_user_by_id(sample_user.id)

        assert result.id == sample_user.id
        assert result.first_name == sample_user.first_name
        assert result.email == sample_user.email

    def test_get_user_by_id_not_found(self, app):
        """Test récupération utilisateur par ID inexistant."""
        with pytest.raises(ValueError, match="User not found"):
            UserService.get_user_by_id(-1)  # ID qui n'existe pas

    def test_update_user_success(self, app, sample_user):
        """Test mise à jour utilisateur réussie."""
        update_data = {"first_name": "Updated", "last_name": "Name"}
        result = UserService.update_user(sample_user.id, update_data)

        assert result.first_name == "Updated"
        assert result.last_name == "Name"
        assert result.email == sample_user.email  # Non modifié

    def test_update_user_email_duplicate(self, app, sample_user):
        """Test échec update avec email dupliqué."""
        # Crée un autre user
        other_user = User(
            first_name="Other",
            last_name="User",
            email="other@example.com",
            birth_date=datetime.date(1990, 1, 1)
        )
        db.session.add(other_user)
        db.session.commit()

        # Essaie de changer l'email de sample_user vers celui de other_user
        update_data = {"email": other_user.email}
        with pytest.raises(ValueError, match="An user with this email already exists"):
            UserService.update_user(sample_user.id, update_data)

    def test_update_user_not_found(self, app):
        """Test update utilisateur inexistant."""
        update_data = {"first_name": "Test"}
        with pytest.raises(ValueError, match="User not found"):
            UserService.update_user(-1, update_data)