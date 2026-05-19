import os
import jwt
from datetime import datetime, timedelta, timezone

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
        email_addr = data["email"].strip().lower()

        existing_user = User.query.filter_by(email=email_addr).first()
        if existing_user:
            return {
                "success": False,
                "message": "Email already exists"
            }, 409

        fullname = data["fullname"].strip()

        new_user = User(
            fullname=fullname,
            email=email_addr,
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
        email_addr = data["email"].strip().lower()
        user_obj = User.query.filter_by(email=email_addr).first()

        if not user_obj or not user_obj.check_password(data["password"]):
            return {
                "success": False,
                "message": "Invalid email or password"
            }, 401

        token = AuthService.generate_token(user_obj)

        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "user": user_obj.to_dict(),
                "access_token": token
            }
        }, 200
    