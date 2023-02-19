from api.app import ma
from marshmallow import fields


class LoginSchema(ma.SQLAlchemySchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    remember = fields.Boolean(default=False)


class RegisterSchema(ma.SQLAlchemySchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    birthday = fields.Date(required=True)


class LoginResponseSchema(ma.SQLAlchemySchema):
    access_token = fields.String(length=261)
    refresh_token = fields.String(length=263)
