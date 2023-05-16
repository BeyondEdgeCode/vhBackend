from flask import Blueprint
from .auth import auth
from .roles import roles
from .permissions import permissions
from .admin import admin

user = Blueprint('user', __name__, url_prefix='/user')

user.register_blueprint(auth)
user.register_blueprint(roles)
user.register_blueprint(permissions)
user.register_blueprint(admin)