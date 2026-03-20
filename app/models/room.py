from app.core.extensions import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Float, nullable=True)  # en m²

    # Relation avec Property
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)

    def __repr__(self):
        return f"<Room {self.id} {self.name} ({self.size}m²)>"