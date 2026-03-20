from marshmallow import validates, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import User
from app.core.extensions import db
from datetime import date

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        dump_only  = ('created_at', 'updated_at')

    email = fields.Email(required=True)

    @validates('birth_date')
    def validate_birth_date(self, value, **kwargs):
        if value > date.today():
            raise ValidationError('Birth date cannot be in the future.')
        # Pas d'age minimum.


class UserUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        sqla_session = db.session
        exclude = ('id', 'created_at', 'updated_at')

    # Rendre tous les champs optionnels pour les updates partiels
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.Email(required=False)
    birth_date = fields.Date(required=False)

    @validates('birth_date')
    def validate_birth_date(self, value, **kwargs):
        if value and value > date.today():  # Vérifier seulement si fourni
            raise ValidationError('Birth date cannot be in the future.')
        # Pas d'age minimum