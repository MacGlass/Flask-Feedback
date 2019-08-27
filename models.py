
from flask_sqlalchemy import SQLAlchemy
import bcrypt
# from flask_bcrypt import Bcrypt

db = SQLAlchemy()
# bcrypt = Bcrypt()


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

    @classmethod
    def register(cls, username, password):
        """ Register user w/ hashed password and return user. """
        # hashes as password
        hashed = bcrypt.generate_password_hash(password)
        # turning the password from bit interperlation into utf8
        hased_utf8 = hashed.decode("utf8")
        # creates a instance of the user
        return cls(username=username, password=hased_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """ Validates if user exits and password is correct
        returns if user is vaild else False """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
