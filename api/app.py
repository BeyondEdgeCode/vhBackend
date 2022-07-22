from flask import Flask, redirect, url_for, request
from alchemical.flask import Alchemical
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import Config

db = Alchemical()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    from api import models
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    # if app.config['USE_CORS']:  # pragma: no branch
    #     cors.init_app(app)

    # blueprints
    # from api.errors import errors
    # app.register_blueprint(errors)
    # from api.tokens import tokens
    # app.register_blueprint(tokens, url_prefix='/api')
    # from api.users import users
    # app.register_blueprint(users, url_prefix='/api')
    # from api.posts import posts
    # app.register_blueprint(posts, url_prefix='/api')
    # from api.fake import fake
    # app.register_blueprint(fake)

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

    return app
