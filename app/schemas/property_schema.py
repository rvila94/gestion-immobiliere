from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.property import Property
from app.schemas.room_schema import NestedRoomSchema
from app.core.extensions import db

class PropertySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        load_instance = True
        sqla_session = db.session
        include_fk = True
        dump_only = ("created_at", "updated_at")

    rooms = fields.Nested(NestedRoomSchema, many=True)


class PropertyUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        load_instance = False
        sqla_session = db.session
        exclude = ("id", "created_at", "updated_at")

    name = fields.String(required=False)
    description = fields.String(required=False)
    property_type = fields.String(required=False)
    city = fields.String(required=False)