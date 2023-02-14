import click
from flask.cli import with_appcontext
from ..models import User, UserRole
from api.app import db
from werkzeug.security import generate_password_hash


@click.command('register')
@click.argument('email', required=True)
@click.argument("email_confirmed", required=True)
@click.argument('password', required=True)
@click.argument('role', default=None)
@with_appcontext
def cli_register_user(email: str, password: str,  email_confirmed: bool, role: int):
    role = db.session.scalar(UserRole.select().where(UserRole.id == role))
    user = User(email=email, password=generate_password_hash(password), email_confirmed=bool(email_confirmed),
                role=role)
    db.session.add(user)
    db.session.commit()
    print(f'New User created with [email] {email}, [password] {password}, [email_confirmed] {email_confirmed},'
          f' [role] {role}')

