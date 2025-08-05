from flask_restful import Resource
from flask import request
from domain.book import Book, db
from serializers.book import BookSchema
# from services.aws.s3_service import upload_file_to_s3
import os

book_schema = BookSchema()
books_schema = BookSchema(many=True)

class UploadFile(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error":"no file uploaded"},400
        file = request.files['file']
        file_path = os.path.join('/tmp',file.filename)
        file.save(file_path)

        s3_key = f"uploads/{file.filename}"
        s3_url = upload_file_to_s3(file_path,s3_key)

        return {'message': 'fileuploaded',"s3_url": s3_url}, 200

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return books_schema.dump(books), 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"error": "No input provided"}, 400

        try:
            book_data = book_schema.load(json_data)
        except Exception as err:
            return {"error": str(err)}, 422

        book = Book(**book_data)
        db.session.add(book)
        db.session.commit()
        return book_schema.dump(book), 201

class BookResource(Resource):
    def put(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404

        data = request.get_json()
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        db.session.commit()
        return {"message": "Book updated"}

    def get(self,book_id):
        book = Book.query.get(book_id)
        return book_schema.dump(book), 200
        # {"message":"book with id"}

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404

        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}
