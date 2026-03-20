import pytest
from app.models.property import Property
from app.models.room import Room  # Ajout de l'import pour Room
from app.models.user import User
from app.services.property_service import PropertyService
from app.core.extensions import db
import datetime

class TestPropertyService:
    """Tests pour PropertyService."""

    def test_create_property_without_rooms_success(self, app, sample_user):
        """Test création propriété sans pièces réussie."""
        property = Property(
            name="Maison Test",
            description="Belle maison à Paris",
            property_type="maison",
            city="Paris",
            owner_id=sample_user.id
        )

        result = PropertyService.create_property(property)

        assert result.id is not None
        assert result.name == "Maison Test"
        assert result.owner_id == sample_user.id
        assert result in db.session

    def test_create_property_with_rooms_success(self, app, sample_user):
        """Test création propriété avec pièces réussie."""
        
        room1 = Room(name="Chambre 1", size=15.5)
        room2 = Room(name="Salle de bain", size=8.0)

        property = Property(
            name="Maison Test",
            description="Belle maison à Paris",
            property_type="maison",
            city="Paris",
            owner_id=sample_user.id,
            rooms=[room1, room2]
        )

        result = PropertyService.create_property(property)

        assert result.id is not None
        assert result.name == "Maison Test"
        assert result.owner_id == sample_user.id
        assert len(result.rooms) == 2
        assert result.rooms[0].name == "Chambre 1"
        assert result.rooms[1].name == "Salle de bain"
        assert result.rooms[0].size == 15.5
        assert result.rooms[1].size == 8.0
        assert result in db.session

    def test_create_property_owner_not_found(self, app):
        """Test échec création propriété avec propriétaire inexistant."""
        property = Property(
            name="Maison Test",
            city="Paris",
            owner_id=-1  # ID inexistant
        )

        with pytest.raises(ValueError, match="User not found"):
            PropertyService.create_property(property)