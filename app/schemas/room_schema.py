from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.room import Room
from app.core.extensions import db

class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        sqla_session = db.session
        include_fk = True


class NestedRoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        sqla_session = db.session
        exclude = ("property_id",)

    name = fields.String(required=True)
    size = fields.Float(required=False)