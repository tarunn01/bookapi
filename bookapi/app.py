from flask import Flask
from config import Config
from models import db
from schemas import ma
from routes import book_bp

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)

app.register_blueprint(book_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)