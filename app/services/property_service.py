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
        

    @staticmethod
    def get_properties_by_city(city: str, page: int = 1, per_page: int = 5):
        """
        Récupère les propriétés d'une ville avec pagination.

        :param city: nom de la ville
        :param page: numéro de page (défaut 1)
        :param per_page: nombre de propriétés par page (défaut 5)
        :return: tuple (liste des propriétés, total, pages totales)
        """
        query = Property.query.filter_by(city=city)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination.items, pagination.total, pagination.pages