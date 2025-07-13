import json

from flask import Flask, jsonify, Response, request
from models import db,Book
from config import Config
from schemas import ma
from schemas import BookSchema

bookschema = BookSchema
app = Flask(__name__)
app.config.from_object(Config) # loading db config
db.init_app(app)  # BIND SQLALCHEMY WITH THE APP
ma.init_app(app)  #initialize marshmallow

@app.route('/')
def home():
    return "Hello, Flask!"

# '/books', methods=['GET']
# books = [
#     {"id": 0, "title": "The Alchemist", "author": "Paulo Coelho"},
#     {"id": 1, "title": "1984", "author": "George Orwell"},
#     {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"}
# ]
#
# @app.route('/books', methods= ["GET"])
# def get_data():
#     return jsonify(books)


@app.route('/books', methods=["GET"])
def get_books():
    books = Book.query.all()  # ORM: SELECT * FROM books;
    # return jsonify([book.to_dict() for book in books])
    return bookschema(many=True).dump(books),200

@app.route('/add_book', methods= ['POST'])
def add_book():
    # data = {'name': 'Alice', 'age': 30}
    json_data = request.get_json()
    if not json_data:
        return {'error': 'no data provided'},400
    error = bookschema.validate(json_data)
    if error:
        return {f"error in input data: {error}"},422
    #create and save data
    book = Book(**json_data)
    db.session.add(book) # add to  db
    db.session.commit() #save to db
    return bookschema.dump(book),201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id) #fetch book by primary id
    if not book:
        return {'error': 'book not found'}, 404
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return {'message': 'book_updated'}

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {'error': 'book not found'}, 404
    db.session.delete(book)
    db.session.commit()
    return {'message': 'book deleted'}

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # ensures tables are created before running the app
    app.run(debug=True)
