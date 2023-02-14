from typing import List

import click
from flask.cli import with_appcontext
from ..models import User, UserRole
from api.app import db
from werkzeug.security import generate_password_hash


@click.group()
def auth():
    """Auth/Register functions"""
    pass


@auth.command('register')
@click.argument('email', required=True)
@click.argument("email_confirmed", required=True)
@click.argument('password', required=True)
@click.argument('role', default=None)
@with_appcontext
def cli_register_user(email: str, password: str,  email_confirmed: bool, role: int):
    """Register new user"""
    role: UserRole = db.session.scalar(UserRole.select().where(UserRole.id == role))
    user: User = User(email=email, password=generate_password_hash(password), email_confirmed=bool(email_confirmed),
                role=role)
    db.session.add(user)
    db.session.commit()
    print(f'New User created with [email] {email}, [password] {password}, [email_confirmed] {email_confirmed},'
          f' [role] {role}')


@auth.command('change_password')
@click.argument('email', required=True)
@click.argument('new_password', required=True)
@with_appcontext
def cli_change_password(email: str, new_password: str):
    """Change user password by email"""
    user: User = db.session.scalar(User.select().where(User.email == email))
    user.password = generate_password_hash(new_password)
    db.session.add(user)
    db.session.commit()
    print('Done')


@auth.command('ls')
def cli_ls():
    users: List[User] = db.session.scalars(User.select())
    from prettytable import PrettyTable
    table = PrettyTable(['id', 'email', 'email_confirmed', 'role', 'firstName', 'lastName', 'birthday', 'registrationDate'])
    for user in users:
        table.add_row([user.id, user.email, user.email_confirmed, user.role.roleName, user.firstName, user.lastName,
                       user.birthday, user.registrationDate])
    print(table)