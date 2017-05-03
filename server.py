"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():
    """Render register template"""
    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Registers new user"""
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = int(request.form["zipcode"])

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    user_match = User.query.filter_by(email=email).first()
    if not user_match:
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")


@app.route("/login", methods=["GET"])
def login_form():
    """Render login page"""
    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    check_email = User.query.filter_by(email=email).first()

    if email != check_email.email:
        return redirect("/register_form")
    elif password != check_email.password:
        flash('Invalid credentials')
        return redirect("/login")
    else:
        flash('You were successfully logged in')
        return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
