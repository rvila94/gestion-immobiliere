from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.schemas.property_schema import PropertySchema
from app.services.property_service import PropertyService

# Définition du Blueprint
properties_bp = Blueprint("properties_bp", __name__, url_prefix="/api/properties")

# Schemas
property_schema = PropertySchema()
property_list_schema = PropertySchema(many=True)


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


@properties_bp.route("/city/<string:city>", methods=["GET"])
def get_properties_by_city(city):
    """
    Récupère les propriétés d'une ville avec pagination.
    Query params : page (int), per_page (int)
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    properties, total, pages = PropertyService.get_properties_by_city(city, page, per_page)

    result = property_list_schema.dump(properties)

    return jsonify({
        "properties": result,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": pages
    }), 200
