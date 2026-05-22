from flask import Blueprint, request, jsonify, g
from app.services.auth_service import AuthService
from app.utils.auth_utils import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# -------------------------
# REGISTER
# -------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    required_fields = ["name", "email", "password"]
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing fields: {', '.join(missing)}"
        }), 400

    confirm_password = data.get("confirmPassword")
    if confirm_password and data["password"] != confirm_password:
        return jsonify({
            "success": False,
            "message": "Passwords do not match"
        }), 400

    if len(data["password"]) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters long"
        }), 400

    service_data = {
        "full_name": data["name"],
        "email": data["email"],
        "phone": data.get("phone"),  
        "password": data["password"]
    }

    response, status = AuthService.register(service_data)

    # OPTIONAL: flatten response for frontend consistency
    if status == 201:
        return jsonify({
            "success": True,
            "user": response["data"]["user"],
            "token": response["data"]["token"]
        }), 201

    return jsonify(response), status


# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    if not data.get("email") or not data.get("password"):
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    response, status = AuthService.login(data)

    # OPTIONAL: flatten for frontend consistency
    if status == 200:
        return jsonify({
            "success": True,
            "user": response["data"]["user"],
            "token": response["data"]["access_token"]
        }), 200

    return jsonify(response), status


# -------------------------
# DELETE ACCOUNT 
# -------------------------
@auth_bp.route("/account", methods=["DELETE"])
@token_required
def delete_account():
    user = g.current_user  

    response, status = AuthService.delete_account(user)
    return jsonify(response), status


# -------------------------
# CURRENT USER
# -------------------------
@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    return jsonify({
        "success": True,
        "user": g.current_user.to_dict()
    }), 200