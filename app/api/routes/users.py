from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas.user_schema import UserSchema, UserUpdateSchema
from app.services.user_service import UserService

# Définition du Blueprint
users_bp = Blueprint("user_bp", __name__, url_prefix="/api/users")

# Schemas
user_schema = UserSchema()
user_update_schema = UserUpdateSchema()


# --------------------------------- Endpoints ---------------------------------

@users_bp.route("/", methods=["POST"])
def create_user():
    """
    Crée un nouvel utilisateur.
    """
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

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Récupère un utilisateur par son ID.
    """
    try:
        user = UserService.get_user_by_id(user_id)
    except ValueError as e:
        return jsonify({"errors": str(e)}), 404

    result = user_schema.dump(user)
    return jsonify(result), 200

# NOTE:
# N'importe qui peux mettre à jour n'importe quel utilisateur, 
# pas de vérification d'authentification ou d'autorisation.
@users_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    """
    Met à jour les informations d'un utilisateur.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input provided"}), 400

    # Validation avec UserUpdateSchema
    try:
        update_data = user_update_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    # Mise à jour
    try:
        user = UserService.update_user(user_id, update_data)
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400

    # Sérialisation de la réponse
    result = user_schema.dump(user)
    return jsonify(result), 200