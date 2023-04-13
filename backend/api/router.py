import json
import time
import flask
from flask import Blueprint
from flask import g, request, current_app
from .user import user
from .testing import testing
from .product import product
from .objectstorage import s3
from .shop import shop
from .imagecarousel import imagecarousel
from .basket import basket
from .promocode import promocode
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies, jwt_required
from datetime import datetime, timedelta, timezone
from api.app import apifairy
from .utils import permission_required

router = Blueprint('app', __name__)

router.register_blueprint(user)
router.register_blueprint(testing)
router.register_blueprint(product)
router.register_blueprint(s3)
router.register_blueprint(shop)
router.register_blueprint(imagecarousel)
router.register_blueprint(basket)
router.register_blueprint(promocode)


@router.before_request
def add_time_measure():
    g.start = time.time()


@router.before_request
def logging_before():
    # Store the start time for the request
    g.start_time = time.perf_counter()


@router.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - g.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response


# TODO: Need to rewrite this code, because sometimes causes exception when token expired
# TODO: Need example of exception
@router.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(days=1))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
