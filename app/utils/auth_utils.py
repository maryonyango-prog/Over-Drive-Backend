import os
import jwt
from functools import wraps
from flask import request, jsonify, g

from app.models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Authorization header missing"
            }), 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({
                "success": False,
                "message": "Invalid authorization format. Use: Bearer <token>"
            }), 401

        token = parts[1]

        try:
            secret = os.getenv("JWT_SECRET_KEY", "change-me")

            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"]
            )

            user_id = payload.get("sub")

            if not user_id:
                return jsonify({
                    "success": False,
                    "message": "Invalid token payload"
                }), 401

            # -----------------------------
            # SAFE USER FETCH (IMPROVED)
            # -----------------------------
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "message": "Invalid user ID in token"
                }), 401

            user = User.query.get(user_id)

            if user is None:
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

        except Exception as e:
            return jsonify({
                "success": False,
                "message": "Authentication error",
                "error": str(e)
            }), 500

        return f(*args, **kwargs)

    return decorated