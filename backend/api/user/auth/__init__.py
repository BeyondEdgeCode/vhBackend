from flask import Blueprint
from .routes import login
from .routes import register
from .routes import me
from .routes import me_update
from .routes import logout
from .routes import change_password
from .cli import cli_register_user

auth = Blueprint('auth', __name__, url_prefix='/auth')

auth.add_url_rule('/register', 'auth_register', register, methods=['POST'])
auth.add_url_rule('/login', 'auth_login', login, methods=['POST'])
auth.add_url_rule('/logout', 'auth_logout', logout, methods=['GET'])
auth.add_url_rule('/me', 'auth_me', me, methods=['GET'])
auth.add_url_rule('/me', 'me_update', me_update, methods=['PATCH'])
auth.add_url_rule('/change_password', 'change_password', change_password, methods=['PATCH'])
