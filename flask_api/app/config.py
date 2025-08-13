import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "devjwtsecret")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug settings
    DEBUG = os.getenv("FLASK_ENV") == "development"
    JSON_SORT_KEYS = False

    # JWT options
    JWT_TOKEN_LOCATION = ["headers", "cookies", "query_string"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False

    # OAuth
    OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI")

    # Misc
    PROPAGATE_EXCEPTIONS = True