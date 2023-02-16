from api.config import Config
from api.models import User, Shop, Settings
from api.utils import get_all, get_first
from flask import jsonify
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from sentry_sdk import capture_exception


@jwt_required()
@permission_required('admin.test')
def get_shops():
    query = get_all(Settings.select())
    parsed_query = [[r.key, r.value] for r in query]
    return jsonify(parsed_query)


@jwt_required()
@permission_required('admin.test')
def get_users():
    users = get_all(User.select())
    return jsonify([[u.email, u.password] for u in users])


def zerodivision_test():
    try:
        е = 1/0
    except ZeroDivisionError as err:
        capture_exception(err)
        return jsonify(status=f'{Config.APP_VERSION}')

