from flask import Flask
from flask_ckeditor import CKEditor
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = "verysecretkey"
app.config['MONGODB_SETTINGS'] = {
    'db': 'KKN',
    'host': '127.0.0.1',
    'port': 27017,
}
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

csrf = CSRFProtect(app)
ckeditor = CKEditor(app)
db = MongoEngine(app)
bcrypt = Bcrypt(app)

from app import models, views