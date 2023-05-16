from api.models import User, UserRole, UserRolePermission
from api.app import db
from apifairy import response, body, arguments
from api.utils import permission_required
from flask_jwt_extended import jwt_required
from .schema import GetUserSchema
from api.schemas.users import UserSchema


@jwt_required()
@permission_required('admin.user.read')
@arguments(GetUserSchema)
@response(UserSchema)
def get(args):
    user: User = db.session.get(User, args['id'])
    return user

