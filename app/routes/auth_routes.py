from flask import Blueprint, request, jsonify, g
from app.services.auth_service import AuthService
from app.utils.auth_utils import token_required


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    required_fields = ["first_name", "last_name", "email", "password"]
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing fields: {', '.join(missing)}"
        }), 400

    if len(data["password"]) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters long"
        }), 400

    response, status = AuthService.register(data)
    return jsonify(response), status


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    if not data.get("email") or not data.get("password"):
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    response, status = AuthService.login(data)
    return jsonify(response), status


@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    return jsonify({
        "success": True,
        "data": g.current_user.to_dict()
    }), 200