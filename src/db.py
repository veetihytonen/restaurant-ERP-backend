from app import app
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)
