# models.py
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object (binds with Flask app later)
db = SQLAlchemy()

# Define the Book model/table
class Book(db.Model):
    __tablename__ = 'new_book'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(200),nullable = False)

    def to_dict(self):
        # Helper method to convert model object to dictionary for JSON responses
        return {"id": self.id, "title": self.title, "author": self.author}