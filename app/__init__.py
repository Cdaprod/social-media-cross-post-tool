# app/__init__.py

from flask import Flask
from flask_restx import Api
from flask_login import LoginManager
from flask_caching import Cache
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from .config import Config
from .rate_limiter import RedisRateLimiter
from .tasks import celery
from .api.crosspost import ns as crosspost_ns
from .api.health import ns as health_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Sentry
    if app.config['SENTRY_DSN']:
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )

    # Initialize Flask-RESTX
    api = Api(app, version='1.0', title='Crosspost API',
              description='API for cross-posting content between Threads and Twitter',
              doc='/swagger/')
    api.add_namespace(crosspost_ns)
    api.add_namespace(health_ns)

    # Initialize Cache
    cache = Cache(app)

    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Import User model and user_loader here if implementing authentication
    # from .models import User
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.get(user_id)

    # Register Blueprints or additional setup if necessary

    return app