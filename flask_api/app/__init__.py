import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from .config import Config
from .extensions import db, ma, migrate, jwt, oauth
from .resources.users import UserListResource, UserResource
from .resources.auth import LoginResource, TokenRefreshResource
from .resources.oauth import GoogleLoginResource, GoogleCallbackResource


def _build_database_uri_from_env() -> str:
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url
    user = os.getenv("POSTGRES_USER", "flaskuser")
    password = os.getenv("POSTGRES_PASSWORD", "flaskpass")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    name = os.getenv("POSTGRES_DB", "flaskdb")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def _register_google_oauth(app: Flask) -> None:
    client_id = os.getenv("OAUTH_GOOGLE_CLIENT_ID")
    client_secret = os.getenv("OAUTH_GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        return
    oauth.init_app(app)
    oauth.register(
        name="google",
        server_metadata_url=(
            "https://accounts.google.com/.well-known/openid-configuration"
        ),
        client_id=client_id,
        client_secret=client_secret,
        client_kwargs={"scope": "openid email profile"},
    )


def create_app(config_object: Optional[type] = None) -> Flask:
    # Load environment variables from .env, if present
    load_dotenv(override=False)

    app = Flask(__name__)

    # Configuration
    app.config.from_object(config_object or Config)
    # Ensure DB URL is set from environment precedence
    app.config["SQLALCHEMY_DATABASE_URI"] = _build_database_uri_from_env()

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # OAuth (optional)
    _register_google_oauth(app)

    # RESTful API and routes
    api = Api(app)
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(TokenRefreshResource, "/auth/refresh")
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/users/<int:user_id>")
    api.add_resource(GoogleLoginResource, "/oauth/login/google")
    api.add_resource(GoogleCallbackResource, "/oauth/callback/google")

    # Create DB tables if they don't exist yet
    with app.app_context():
        db.create_all()

    return app