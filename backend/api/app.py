import logging

import flask
from apifairy import APIFairy
from flask import Flask, request
from alchemical.flask import Alchemical
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .config import Config
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import flask_monitoringdashboard as dashboard
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_caching import Cache
from elasticsearch import Elasticsearch


db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
apifairy = APIFairy()
cors = CORS()
cache = Cache()
# metrics = PrometheusMetrics.for_app_factory()


def register_cli(app: Flask):
    from .user.permissions.cli import perm as perm_cli
    from .user.auth.cli import auth as auth_cli
    from .user.roles.cli import roles as roles_cli
    from .product.category.cli import category as category_cli
    from .objectstorage.cli import s3 as objectstorage_cli
    from .product.cli import product as product_cli
    from .shop.cli import shop as shop_cli
    from .imagecarousel.cli import ic as ic_cli
    from .fill_db import fill

    app.cli.add_command(perm_cli, name='perm')
    app.cli.add_command(auth_cli, name='auth')
    app.cli.add_command(roles_cli, name='roles')
    app.cli.add_command(category_cli, name='category')
    app.cli.add_command(objectstorage_cli, name='s3')
    app.cli.add_command(product_cli, name='product')
    app.cli.add_command(shop_cli, name='shop')
    app.cli.add_command(ic_cli, name='ic')
    app.cli.add_command(fill, name='fill')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config.from_object(config_class)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.ERROR)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    # modules
    from . import models
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    # APIFairy security
    from flask_jwt_extended import jwt_required
    from .utils import permission_required
    # app.config['APIFAIRY_APISPEC_DECORATORS'] = [(permission_required('admin.docs')), (jwt_required())]
    # app.config['APIFAIRY_UI_DECORATORS'] = [(permission_required('admin.docs')), (jwt_required())]
    apifairy.init_app(app)
    register_cli(app)
    cache.init_app(app)
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
        release=f'{Config.APP_VERSION}-{Config.GIT_VERSION[0:5]}' if Config.ENVIRONMENT == 'production'
        else f'dev:{Config.APP_VERSION}-{Config.GIT_VERSION[0:5]}',
    )

    cors.init_app(app)

    from .router import router
    app.register_blueprint(router)
    dashboard.config.link = '/monitor'
    dashboard.bind(app)
    dashboard.config.show_login_banner = 0
    dashboard.config.show_login_footer = 0
    dashboard.config.brand_name = 'VapeHookah'

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

