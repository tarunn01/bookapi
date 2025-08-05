from flask_marshmallow import Marshmallow
from domain.book import Book

ma = Marshmallow()

class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book

    id = ma.auto_field(dump_only=True)
    title = ma.Str(required=True, validate=lambda t: len(t) > 0)
    author = ma.Str(required=True, validate=lambda a: len(a) > 0)
