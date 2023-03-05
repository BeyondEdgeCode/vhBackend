from functools import wraps
from .app import db
from flask import request, jsonify, logging, current_app
from flask_jwt_extended import current_user


class ResponsesClass:

    def throw_400(self, err):
        return jsonify(status=400, msg=err), 400

    def throw_200(self, msg):
        return jsonify(status=200, msg=msg), 200


responses = ResponsesClass()


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
                return fn(*args, **kwargs)
            else:
                return jsonify(status=403, msg=f'Role <{permission}> not found in role <{current_user.role.roleName}>')

        return decorator

    return wrapper


def catch_exception(exception, title):
    return jsonify(code=500, title=title, desc=exception.args[0]), 500
