from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geoscope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "lol123lolzzzzz"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
db = SQLAlchemy(app)


from app import routes, models
