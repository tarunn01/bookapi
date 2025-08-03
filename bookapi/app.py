from flask import Flask
from flask_restful import Api
from models.book import db
from schemas.book import ma
from config import Config
# from resources.book import BookListResource, BookResource
from resources.book_resources import BookListResource,BookResource,UploadFile

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB & Marshmallow
db.init_app(app)
ma.init_app(app)

# RESTful API setup
api = Api(app)

# Routes
api.add_resource(UploadFile, '/upload')
api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

@app.route('/')
def home():
    return "Hello, Flask-RESTful!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
