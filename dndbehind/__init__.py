"""The flask application package."""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class: Config = Config) -> Flask:
    """Create a new Flask application.

    Args:
        config_class (Config, optional): The configuration class to use.
                                         Defaults to Config.

    Returns:
        Flask: the new Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def index():
        return "Placeholder for index page."

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .mgmt import bp as mgmt_bp
    app.register_blueprint(mgmt_bp)

    return app
