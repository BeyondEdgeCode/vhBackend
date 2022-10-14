from apifairy import APIFairy
from flask import Flask, request
from alchemical.flask import Alchemical
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .config import Config
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.middleware.proxy_fix import ProxyFix


db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
apifairy = APIFairy()
cors = CORS()
metrics = PrometheusMetrics.for_app_factory()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    from api import models
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    apifairy.init_app(app)
    metrics.init_app(app)
    if app.config['USE_CORS']:
        cors.init_app(app)

    metrics.info('vh_backend', 'VapeHookah Backend', version=app.config['APP_VERSION'])

    from .router import router
    app.register_blueprint(router)

    # define the shell context
    @app.shell_context_processor
    def shell_context():  # pragma: no cover
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
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    return app

