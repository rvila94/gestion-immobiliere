from marshmallow import validates, ValidationError, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import User
from app.core.extensions import db
import re
from datetime import date

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ('created_at', 'updated_at')

    email = fields.Email(required=True)

    @validates('birth_date')
    def validate_birth_date(self, value, **kwargs):
        if value > date.today():
            raise ValidationError('Birth date cannot be in the future.')
        # Pas de d'age minimum.