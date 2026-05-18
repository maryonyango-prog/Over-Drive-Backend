import os
import jwt
from functools import wraps
from flask import request, jsonify, g
from app.database.database import db
from app.models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Missing token"
            }), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms=["HS256"]
            )

            user = User.query.get(int(payload["sub"]))

            if not user:
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404

            g.current_user = user

        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "message": "Token expired"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 401

        return f(*args, **kwargs)

    return decorated