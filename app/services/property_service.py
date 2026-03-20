from app.models.property import Property
from app.core.extensions import db
from app.services.user_service import UserService


class PropertyService:
    @staticmethod
    def create_property(property: Property):
        """
        Crée une propriété avec ses rooms.
        """
        # Verifier que le propriétaire existe
        UserService.get_user_by_id(property.owner_id)

        try:
            db.session.add(property)
            db.session.commit()
            return property
        except Exception as e:
            db.session.rollback()
            raise ValueError("Failed to create property.") from e