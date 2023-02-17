import sys

import flask_jwt_extended
from apifairy import APIFairy
from flask import Flask, request, g
from alchemical.flask import Alchemical
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .config import Config
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
apifairy = APIFairy()
cors = CORS()
# metrics = PrometheusMetrics.for_app_factory()


def register_cli(app: Flask):
    from .permissions.cli import perm as perm_cli
    from .auth.cli import auth as auth_cli
    from .roles.cli import roles as roles_cli
    from .category.cli import category as category_cli
    from .objectstorage.cli import s3 as objectstorage_cli
    from .product.cli import product as product_cli
    from .shop.cli import shop as shop_cli
    from .imagecarousel.cli import ic as ic_cli

    app.cli.add_command(perm_cli, name='perm')
    app.cli.add_command(auth_cli, name='auth')
    app.cli.add_command(roles_cli, name='roles')
    app.cli.add_command(category_cli, name='category')
    app.cli.add_command(objectstorage_cli, name='s3')
    app.cli.add_command(product_cli, 'product')
    app.cli.add_command(shop_cli, 'shop')
    app.cli.add_command(ic_cli, 'ic')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # modules
    from . import models
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    apifairy.init_app(app)
    register_cli(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[
            FlaskIntegration(),
        ],
        _experiments={
            "profiles_sample_rate": 1.0,
        },
        environment=Config.ENVIRONMENT,
        attach_stacktrace=True,
        send_default_pii=True,
        traces_sample_rate=1.0,
        release=Config.APP_VERSION[0:7] if Config.ENVIRONMENT == 'production' else f'dev:{Config.APP_VERSION[0:7]}',
    )

    if app.config['USE_CORS']:
        cors.init_app(app)

    from .router import router
    app.register_blueprint(router)

    @app.shell_context_processor
    def shell_context():
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx

    @app.after_request
    def after_request(response):
        # Clear Werkzeug context
        request.get_data()
        return response

    return app

