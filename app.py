""" User application """

from flask import Flask, redirect, render_template, flash, url_for, request, session
from forms import AddUser, LogInForm
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretsecretseacreats'

connect_db(app)


@app.route("/")
def rediect_register():
    """ redirects to register page """
    return redirect("/register")

@app.route("/register")
def show_registration_form():
    """ show the registration form for user """
    form = AddUser()
    return render_template("register.html", form=form)


@app.route("/register", methods=["POST"])
def add_user_registration_form():
    """ show the registration form for user """
    form = AddUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
    
        new_user = User.register(username, password)

        new_user.email = email
        new_user.first_name = first_name
        new_user.last_name = last_name

        db.session.add(new_user)
        db.session.commit()

        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login")
def login():
    """ Show user login page """

    form = LogInForm()

    return render_template("login.html", form=form)


@app.route("/login", methods=["POST"])
def validate_login():
    """ show the registration form for user """
    form = LogInForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id 
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]
            return redirect("/login")
    

@app.route("/secret")
def show_the_secrets():
    """ Authenticate the user and see if they can see the secrets """

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    else:
        redner_template("secret.html")


