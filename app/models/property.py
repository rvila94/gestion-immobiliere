from datetime import datetime

from app.core.extensions import db


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    property_type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relation avec User
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relation avec Room
    rooms = db.relationship("Room", backref="property", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Property {self.id} {self.name} ({self.city})>"