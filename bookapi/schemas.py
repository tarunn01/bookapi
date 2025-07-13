from flask_marshmallow import Marshmallow
from sqlalchemy.orm import validates

from models import Book

ma = Marshmallow()


class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model= Book

    id = ma.auto_field(dump_only = True) #auto generate on serialization
    title =ma.Str(required= True,validate = lambda t:len(t)>0)
    author= ma.Str(required=True,validate = lambda a:len(a)>0)