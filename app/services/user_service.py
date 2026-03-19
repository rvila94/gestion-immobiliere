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
        """
        Récupère un utilisateur par son ID.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    
    @staticmethod
    def update_user(user_id: int, update_data: dict):
        """
        Met à jour les informations d'un utilisateur.
        """
        user = UserService.get_user_by_id(user_id)
        
        # Vérification email unique
        if 'email' in update_data and update_data['email'] != user.email:
            existing = User.query.filter_by(email=update_data['email']).first()
            if existing:
                raise ValueError("An user with this email already exists.")
        
        # Mise à jour des champs
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to update user.") from e

