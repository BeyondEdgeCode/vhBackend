from flask import Blueprint

from .auth import auth
from .testing import testing
from .roles import roles
from .permissions import permissions
from .category import category
from .product import product
from .objectstorage import s3
from .shop import shop
from .imagecarousel import imagecarousel

from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies
from datetime import datetime, timedelta, timezone

router = Blueprint('router', __name__)

router.register_blueprint(auth)
router.register_blueprint(testing)
router.register_blueprint(roles)
router.register_blueprint(permissions)
router.register_blueprint(category)
router.register_blueprint(product)
router.register_blueprint(s3)
router.register_blueprint(shop)
router.register_blueprint(imagecarousel)


@auth.after_request
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
