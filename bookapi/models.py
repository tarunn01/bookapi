from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120),nullable = False)
    author = db.Column(db.String(120),nullable = False)
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)