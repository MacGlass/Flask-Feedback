
from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Mode"""
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

