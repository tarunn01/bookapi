from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
oauth = OAuth()