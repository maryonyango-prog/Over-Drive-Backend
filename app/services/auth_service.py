import os
import jwt
from datetime import datetime, timedelta, timezone

from app.models import user
from app.models.user import User
from app.database.database import db


class AuthService:

    @staticmethod
    def generate_token(user):
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }

        secret = os.getenv("JWT_SECRET_KEY", "change-me")
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def register(data):

        email = data["email"].strip().lower()

        if User.query.filter_by(email=email).first():
            return {"success": False, "message": "Email already exists"}, 409

        new_user = User(
            full_name=data["full_name"].strip(),
            email=email,
            phone=data.get("phone")
        )

        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        token = AuthService.generate_token(new_user)

        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user": new_user.to_dict(),
                "access_token": token
            }
        }, 201

    @staticmethod
    def login(data):

        email = data["email"].strip().lower()

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(data["password"]):
            return {"success": False, "message": "Invalid credentials"}, 401

        token = AuthService.generate_token(user)

        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "user": user.to_dict(),
                "access_token": token
            }
        }, 200
    
    @staticmethod
    def delete_account(user):
        db.session.delete(user)     
        db.session.commit()
        return {"message": "Account deleted"}, 200
    
    @staticmethod
    def change_password(user, data):
        if not user.check_password(data["currentPassword"]):
            return {"message": "Current password is incorrect"}, 400

        user.set_password(data["newPassword"])
        db.session.commit()

        return {"message": "Password updated"}, 200
    
    @staticmethod
    def update_profile(user_id, data):
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        user.full_name = data.get("name", user.full_name)
        user.phone = data.get("phone", user.phone)

        db.session.commit()

        return {"user": user.to_dict()}, 200