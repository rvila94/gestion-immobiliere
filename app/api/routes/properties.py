from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas.property_schema import PropertySchema
from app.services.property_service import PropertyService

# Définition du Blueprint
properties_bp = Blueprint("properties_bp", __name__, url_prefix="/api/properties")

# Schemas
property_schema = PropertySchema()


# --------------------------------- Endpoints ---------------------------------

@properties_bp.route("/", methods=["POST"])
def create_property():
    """
    Crée un nouveau bien immobilier.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input provided"}), 400

    # Validation et désérialisation
    try:
        property_obj = property_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    # Création via le service
    try:
        property_obj = PropertyService.create_property(property_obj)
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400

    # Sérialisation de la réponse
    result = property_schema.dump(property_obj)
    return jsonify(result), 201