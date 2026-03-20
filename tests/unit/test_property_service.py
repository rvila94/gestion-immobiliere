import pytest
from app.models.property import Property
from app.models.room import Room
from app.services.property_service import PropertyService
from app.core.extensions import db

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

    def test_get_properties_by_city_success(self, app, sample_user):
        """Test récupération propriétés par ville réussie."""
        # Créer des propriétés dans la même ville
        prop1 = Property(
            name="Maison 1",
            description="Belle maison",
            property_type="maison",
            city="Paris",
            owner_id=sample_user.id
        )
        prop2 = Property(
            name="Appartement 1",
            description="Bel appartement",
            property_type="appartement",
            city="Paris",
            owner_id=sample_user.id
        )
        prop3 = Property(
            name="Maison Lyon",
            description="Maison à Lyon",
            property_type="maison",
            city="Lyon",
            owner_id=sample_user.id
        )
        db.session.add_all([prop1, prop2, prop3])
        db.session.commit()

        # Récupérer pour Paris
        properties, total, pages = PropertyService.get_properties_by_city("Paris")

        assert len(properties) == 2
        assert total == 2
        assert pages == 1
        assert properties[0].name == "Maison 1"
        assert properties[1].name == "Appartement 1"

    def test_get_properties_by_city_no_results(self, app):
        """Test récupération propriétés par ville sans résultats."""
        properties, total, pages = PropertyService.get_properties_by_city("VilleInexistante")

        assert len(properties) == 0
        assert total == 0
        assert pages == 0

    def test_get_properties_by_city_pagination(self, app, sample_user):
        """Test récupération propriétés par ville avec pagination."""
        # Créer 7 propriétés dans Paris
        properties_list = []
        for i in range(7):
            prop = Property(
                name=f"Propriété {i}",
                description=f"Description {i}",
                property_type="maison",
                city="Paris",
                owner_id=sample_user.id
            )
            properties_list.append(prop)
        db.session.add_all(properties_list)
        db.session.commit()

        # Page 1, 5 par page
        properties, total, pages = PropertyService.get_properties_by_city("Paris", page=1, per_page=5)

        assert len(properties) == 5
        assert total == 7
        assert pages == 2

        # Page 2, 5 par page
        properties, total, pages = PropertyService.get_properties_by_city("Paris", page=2, per_page=5)

        assert len(properties) == 2
        assert total == 7
        assert pages == 2