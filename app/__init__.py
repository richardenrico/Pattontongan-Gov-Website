from operator import imod
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'KKN',
    'host': '127.0.0.1',
    'port': 27017,
}

db = MongoEngine(app)

from app import models, views