from datetime import datetime
from app import db

class User(db.Document):
    name = db.StringField(required=True)
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=5)
    role = db.StringField(default='author')

class Article(db.Document):
    author = db.StringField(required=True)
    title = db.StringField(required=True)
    cover = db.StringField(required=True)
    slug = db.StringField(required=True)
    content = db.StringField(required=True)
    category = db.StringField(required=True)
    posted_at = db.ComplexDateTimeField(default=datetime.utcnow)
    
class Profile(db.Document):
    code = db.StringField(required=True)
    name = db.StringField(required=True)
    logo = db.StringField(required=True)
    address = db.StringField(required=True)
    email = db.StringField(required=True)
    phone_number = db.StringField(required=True)