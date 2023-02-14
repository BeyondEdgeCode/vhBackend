from flask import Blueprint
from .routes import login
from .routes import register
from .routes import me
from .cli import cli_register_user

auth = Blueprint('auth', __name__)

auth.add_url_rule('/auth/login', 'auth_login', login, methods=['POST'])
auth.add_url_rule('/auth/register', 'auth_register', register, methods=['POST'])
auth.add_url_rule('/auth/me', 'auth_me', me, methods=['GET'])

auth.cli.add_command(cli_register_user, 'register')
