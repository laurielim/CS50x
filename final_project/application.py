import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.route("/")
@login_required
def index():
    """Show pomodoro timer"""
    # Assign user_id to variable
    user_id = session["user_id"]

    # Access user setting
    user_setting = db.execute("SELECT chime, pomo FROM users WHERE id = :user_id",
                            user_id=user_id)
    return render_template("index.html", chime=user_setting[0]["chime"], pomo=user_setting[0]["pomo"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Assign form username to variable
        username = request.form.get("username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        # Ensure username does not exist already
        if len(rows) != 0:
            return apology("username already in use", 403)

        # Assign form password to variable and hash password
        password = request.form.get("password")
        phash = generate_password_hash(password)

        # Insert username and hashed password into database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :phash)",
                    username=username, phash=phash)

        # Inform user that they have been successfully registered
        return render_template("registered.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Show settings of pomodoros"""
    # Assign user_id to variable
    user_id = session["user_id"]

    # Access user setting
    user_setting = db.execute("SELECT chime, pomo FROM users WHERE id = :user_id",
                            user_id=user_id)

    if request.method == "POST":

        # Assign form inputs to variables
        new_chime = request.form.get("chime")
        new_pomo = request.form.get("pomo")

        # Check if chime has changed
        if user_setting[0]["chime"] != new_chime:
        # If chime has changed, update database
            db.execute("UPDATE users SET chime = :chime WHERE id = :user_id", chime=new_chime, user_id=user_id)

        # Check if pomo has changed
        if user_setting[0]["pomo"] != new_pomo:
        # If pomo has changed, update database
            db.execute("UPDATE users SET pomo = :pomo WHERE id = :user_id", pomo=new_pomo, user_id=user_id)

        flash('Settings updated.')
        return redirect("/")

    else:
        return render_template("settings.html", chime=user_setting[0]["chime"], pomo=user_setting[0]["pomo"])

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
