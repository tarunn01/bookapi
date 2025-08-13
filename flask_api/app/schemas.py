from __future__ import annotations

from marshmallow import Schema, fields, validate, validates, ValidationError, pre_load


class UserReadSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class UserWriteSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=8, max=128)
    )

    @pre_load
    def strip_fields(self, data: dict, **_: dict) -> dict:
        for key in ("email", "name"):
            if key in data and isinstance(data[key], str):
                data[key] = data[key].strip()
        return data


class UserUpdateSchema(Schema):
    email = fields.Email(required=False)
    name = fields.Str(required=False, validate=validate.Length(min=1, max=120))
    password = fields.Str(required=False, load_only=True, validate=validate.Length(min=8, max=128))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)