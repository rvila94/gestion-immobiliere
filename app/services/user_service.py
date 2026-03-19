from app.models.user import User
from app.core.extensions import db
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def create_user(user: User):
        """
        Crée un utilisateur et l'ajoute à la DB.
        """
        # Verification de doublon d'email
        existing = User.query.filter_by(email=user.email).first()
        if existing:
            raise ValueError("An user with this email already exists.")
        
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()  # Annule les changements
            raise ValueError("Failed to create user.") from e
        
    @staticmethod
    def get_user_by_id(user_id: int):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user