from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.user_schema import UserSchema
from app.services.user_service import UserService

# Définition du Blueprint
users_bp = Blueprint("user_bp", __name__, url_prefix="/api/users")

# Schemas
user_schema = UserSchema()


# --------------------------------- Endpoints ---------------------------------

@users_bp.route("/", methods=["POST"])
def create_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input provided"}), 400

    # Validation et désérialisation
    try:
        user = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    # Création via le service
    try:
        user = UserService.create_user(user)
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400

    # Sérialisation de la réponse
    result = user_schema.dump(user)
    return jsonify(result), 201