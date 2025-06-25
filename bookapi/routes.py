from flask import Blueprint, request, jsonify, session
from models import db, Book
from schemas import book_schema,books_schema

book_bp = Blueprint('book_bp',__name__)
# books_schema = BookSchema(many=True)

@book_bp.route('/books',methods=['POST'])
def add_book():
    data = request.json
    new_book= book_schema.load(data,session=db.session)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(book_schema.dump(new_book)),201
@book_bp.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return jsonify(books_schema.dump(all_books))

@book_bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = db.session.get_or_404(Book,id)
    data = request.json
    updated_book_instance = book_schema.load(data, instance=book, partial=True, session=db.session)
    db.session.commit()
    return jsonify(book_schema.dump(updated_book_instance))

@book_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = db.session.get_or_404(Book, id)  # Replaces Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return '', 204  # CORRECT: No content for successful deletion.
