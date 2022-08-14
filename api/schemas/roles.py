from api.app import ma
from api.models import UserRole, UserRolePermission
from .users import UserSchema

user_schema = UserSchema()


class UserRolePermissionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserRolePermission

    permission = ma.auto_field()


class UserRoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserRole
        ordered = True
        # include_fk = True

    id = ma.auto_field(dump_only=True)
    roleName = ma.auto_field(dump_only=True)
    roleDescription = ma.auto_field(dump_only=True)
    is_default = ma.auto_field(dump_only=True)

    users = ma.Nested(UserSchema, dump_only=True, many=True)
    permissions = ma.Nested(UserRolePermissionSchema, dump_only=True, many=True)


