import time

from sqlalchemy.engine import CursorResult

from api.config import Config
from api.models import User, Shop, Settings
from api.utils import get_all, get_first
from flask import jsonify
from flask_jwt_extended import jwt_required
from api.utils import permission_required
from sentry_sdk import capture_exception
from api.app import db
from ..utils import responses


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


def version():
    # current_db_ver: CursorResult = db.session.execute("SELECT version_num FROM public.alembic_version").scalar()
    # return responses.throw_200(msg='Its fine')
    return jsonify(app_version=f'{Config.ENVIRONMENT}_{Config.APP_VERSION}_{Config.GIT_VERSION[0:8]}',
                    sha=Config.GIT_VERSION)

