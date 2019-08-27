from flask_wtf import FlaskForm
from wtforms import StringField


class AddUser(FlaskForm):
    """ Form to add new users. """

    username = StringField("Username")

    password = StringField("Password")

    email = StringField("Email")

    first_name = StringField("First Name")

    last_name = StringField("Last Name")


class LogInForm(FlaskForm):
    """ Form to log in. """

    username = StringField("Username")

    password = StringField("Password")
