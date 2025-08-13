from __future__ import annotations

from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from ..models import User
from ..schemas import LoginSchema


login_schema = LoginSchema()


class LoginResource(Resource):
    def post(self):
        json_data = request.get_json(silent=True) or {}
        errors = login_schema.validate(json_data)
        if errors:
            return {"errors": errors}, 400

        email = json_data["email"].lower()
        password = json_data["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid email or password"}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {"id": user.id, "email": user.email, "name": user.name},
        }, 200


class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200