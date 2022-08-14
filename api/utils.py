from functools import wraps

from .app import db
from flask import request, jsonify
from flask_jwt_extended import current_user
from werkzeug.exceptions import BadRequest, HTTPException
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
            if permission in current_user.role.get_rights():
                return fn(*args, **kwargs)
            else:
                return jsonify(msg=f'Role <{permission}> not found in role <{current_user.role.roleName}>'), 403

        return decorator

    return wrapper


def catch_exception(exception, title):
    return jsonify(code=500, title=title, desc=exception.args[0]), 500
