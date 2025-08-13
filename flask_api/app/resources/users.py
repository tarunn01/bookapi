from __future__ import annotations

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import User
from ..schemas import UserReadSchema, UserWriteSchema, UserUpdateSchema


user_read_schema = UserReadSchema()
user_list_read_schema = UserReadSchema(many=True)
user_write_schema = UserWriteSchema()
user_update_schema = UserUpdateSchema()


class UserListResource(Resource):
    @jwt_required()
    def get(self):
        users = User.query.order_by(User.id.asc()).all()
        return user_list_read_schema.dump(users), 200

    @jwt_required()
    def post(self):
        json_data = request.get_json(silent=True) or {}
        errors = user_write_schema.validate(json_data)
        if errors:
            return {"errors": errors}, 400

        email = json_data["email"].lower()
        name = json_data["name"]
        password = json_data["password"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            return {"message": "Email already in use"}, 400

        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user_read_schema.dump(user), 201


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id: int):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user_read_schema.dump(user), 200

    @jwt_required()
    def put(self, user_id: int):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        json_data = request.get_json(silent=True) or {}
        errors = user_update_schema.validate(json_data)
        if errors:
            return {"errors": errors}, 400

        if "email" in json_data and json_data["email"]:
            new_email = json_data["email"].lower()
            if new_email != user.email:
                if User.query.filter(User.email == new_email, User.id != user.id).first():
                    return {"message": "Email already in use"}, 400
                user.email = new_email

        if "name" in json_data and json_data["name"]:
            user.name = json_data["name"].strip()

        if "password" in json_data and json_data["password"]:
            user.set_password(json_data["password"]) 

        db.session.commit()
        return user_read_schema.dump(user), 200

    @jwt_required()
    def delete(self, user_id: int):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200