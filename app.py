""" User application """

from flask import Flask, redirect, render_template, flash, url_for, request, session
from forms import AddUser, LogInForm, AddFeedback, EditFeedback
from models import db, connect_db, User, Feedback


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
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
        print("Hi!")
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.username

        return redirect(f"/users/{new_user.username}")
    else:
        return redirect("/register")


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
            session["user_id"] = user.username

            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]
            return redirect("/login")


@app.route("/users/<username>")
def show_the_secrets(username):
    """ Authenticate the user and see if they can see the secrets """

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).first()
        # import pdb; pdb.set_trace()
        feedback = user.feedbacks
        return render_template("secret.html", user=user, feedback=feedback)


@app.route("/users/<username>/delete")
def delete_a_user(username):
    """ Delete a user from the database """

    comprablename = session["user_id"]

    if username == comprablename:
        deleteing_user = User.query.filter_by(username=username).first()
        db.session.delete(deleteing_user)
        db.session.commit()
        session.pop("user_id")

        return redirect("/")

    else:
        flash(f"You must be the {username} to delete")
        return redirect(f"/users/{username}")


@app.route("/logout")
def logout():
    """ Logout current user """

    session.pop("user_id")

    return redirect("/")


@app.route("/users/<username>/feedback/add")
def show_feedback(username):
    """ Authenticate the user and show form """

    form = AddFeedback()

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).first()
        return render_template("feedback_add.html", user=user, form=form)


@app.route("/users/<username>/feedback/add", methods=["POST"])
def process_feedback(username):
    """ Authenticate the user and process the feedback_add """

    form = AddFeedback()

    if "user_id" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(
                title=title, content=content, username=username)

            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f"/users/{username}")
        else:
            return redirect(f"/users/{username}/feedback/add")


@app.route("/feedback/<int:id>/update")
def get_edit_feedback_form(id):

    comprablename = session["user_id"]
    feedback = Feedback.query.get_or_404(id)
    form = EditFeedback()

    if feedback.username == comprablename:
        return render_template("feedback_edit.html", form=form, feedback=feedback)

    else:
        return redirect("/")


@app.route("/feedback/<int:id>/update", methods=["POST"])
def update_feedback(id):

    comprablename = session["user_id"]
    feedback = Feedback.query.get_or_404(id)
    form = EditFeedback()

    if feedback.username == comprablename:
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.add(feedback)
            db.session.commit()

            return redirect(f"/users/{feedback.username}")

    else:

        return redirect(f"/feedback/{feedback.id}/update")


@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(id):

    comprablename = session["user_id"]
    feedback = Feedback.query.get_or_404(id)
    username = feedback.username

    if feedback.username == comprablename:
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        flash(f"You must be the {username} to delete")
        return redirect(f"/users/{username}")