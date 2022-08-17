from functools import wraps

from .app import db
from flask import request, jsonify, logging, current_app
from flask_jwt_extended import current_user
# from flask_jwt_extended import


def get_first(query):
    scalar = db.session.scalar(query)
    return scalar if scalar else None


def get_first_or_false(query):
    scalar = db.session.scalar(query)
    return scalar if scalar else False


def get_all(query): return db.session.scalars(query)


def permission_required(permission):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            permissions = current_user.role.get_rights()
            if 'admin.all' in permissions or permission in permissions:
                current_app.logger.info(f'{current_user.role.roleName}->{current_user.email} requested access to '
                                        f'{request.path} -> ACCESS GRANTED')
                return fn(*args, **kwargs)
            else:
                current_app.logger.info(f'{current_user.role.roleName}->{current_user.email} requested access to '
                                        f'{request.path} -> ACCESS DENIED')
                return jsonify(msg=f'Role <{permission}> not found in role <{current_user.role.roleName}>'), 403

        return decorator

    return wrapper


def catch_exception(exception, title):
    return jsonify(code=500, title=title, desc=exception.args[0]), 500
