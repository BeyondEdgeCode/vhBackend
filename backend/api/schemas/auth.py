from api.app import ma
from marshmallow import fields
from api.schemas.users import UserSchema, UserIdSchema


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


class UserInfoSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered = True
    id = fields.Integer()
    role = fields.String()
    permissions = fields.List(fields.String())
    user = ma.Nested(UserIdSchema)


class UserPasswordChangeSchema(ma.SQLAlchemySchema):
    class Meta:
        ordered = True

    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
