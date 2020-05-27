import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Assign user id to variable
    user_id = session["user_id"]

    # Query user's portfolio
    rows = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)

    # Query user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)

    # Set equity to empty string if user owns zero shares
    if len(rows) == 0:
        equity = ""
    else:
        # Update share prices and calculate total value of shares
        value_shares = 0
        for row in rows:
            quote = lookup(row["symbol"])
            if row["price"] != quote["price"]:
                total = row["share"] * quote["price"]
                db.execute("UPDATE portfolio SET price = :price, total = :total WHERE id = :user_id AND symbol = :symbol",
                price=quote["price"], total=total, user_id=user_id, symbol=row["symbol"])
                value_shares += total
            else:
                value_shares += row["total"]

        # Query user's updated portfolio
        rows = db.execute("SELECT * FROM portfolio WHERE id = :user_id", user_id=user_id)

        # Calculate user's equity
        equity = round(cash[0]["cash"] + value_shares, 2)

    # Render homepage with portfolio and cash
    return render_template("index.html", rows=rows, cash=cash[0]["cash"], equity=equity)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Assign user id to variable
        user_id = session["user_id"]

        # Assign form inputs to variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Check that there is a symbol present
        if symbol == "":
            return apology("missing symbol", 400)

        # Check that a number of shares has been selected
        if shares.isnumeric():
            shares = int(shares)
        else:
            return apology("missing shares", 400)

        # Query API for symbol
        quote = lookup(symbol)
        # Ensure symbol is valid
        if  quote == None:
            return apology("invalid symbol", 400)

        name = quote["name"]
        symbol = quote["symbol"]
        price = quote["price"]
        cost = float(shares) * price

        # Check that user has sufficent funds
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        if cash[0]["cash"] < cost:
            return apology("you poor", 400)

        # Calculate user's cash total after buying shares
        total_cash = round(cash[0]["cash"] - cost, 2)
        # Update user's cash total
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=total_cash, user_id=user_id)

        # Insert acquisition into transaction table
        db.execute("INSERT INTO transactions (id, symbol, share, price) VALUES (:user_id, :symbol, :share, :price)",
                    user_id=user_id, symbol=symbol, share=shares, price=price)

        # Check if user already owns shares of this company
        owned = db.execute("SELECT * FROM portfolio WHERE id = :user_id AND symbol = :symbol",
                          user_id=user_id, symbol = symbol)
        # Update share, price and total
        if len(owned) == 1:
            new_shares = owned[0]["share"] + shares
            new_total = new_shares * price
            db.execute("UPDATE portfolio SET share = :share, price = :price, total = :total WHERE id = :user_id AND symbol = :symbol",
                    share=new_shares, price=price, total=new_total, user_id=user_id, symbol=symbol)
        # Add new acquisition to portfolio
        else:
            db.execute("INSERT INTO portfolio (id, symbol, name, share, price, total) VALUES (:user_id, :symbol, :name, :share, :price, :cost)",
                    user_id=user_id, symbol=symbol, name=name, share=shares, price=price, cost=cost)

        # Flash message
        flash('Shares bought!')
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Assign user id to variable
    user_id = session["user_id"]

    # Query user's transactions
    rows = db.execute("SELECT * FROM transactions WHERE id = :user_id", user_id=user_id)

    # Render rend history with transactions
    return render_template("history.html", rows=rows)


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

        # Flash message
        flash('You were successfully logged in')
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Assign form input to variable
        symbol = request.form.get("symbol")
        # Query API for symbol quote
        quote = lookup(symbol)
        # Ensure symbol is valid
        if  quote == None:
            return apology("invalid symbol", 400)
        # Show user their quotation
        else:
            return render_template("quote_result.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Assign user id to variable
    user_id = session["user_id"]

    if request.method == "POST":

        # Assign form inputs to variables
        symbol = request.form.get("symbol")
        disposal = request.form.get("shares")

        # Check that a symbol has been selected
        if symbol == "symbol":
            return apology("no symbol selected", 400)

        # Check that a number of shares has been selected
        if disposal.isnumeric():
            disposal = int(disposal)
        else:
            return apology("missing shares", 400)

        # Query API for symbol
        quote = lookup(symbol)

        # Query database for price and share
        asset = db.execute("SELECT price, share FROM portfolio WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)

        # Check that user is not selling more shares than owned
        if asset[0]["share"] < disposal:
            return apology("too many shares", 400)

        # Insert disposal into transaction table
        db.execute("INSERT INTO transactions (id, symbol, share, price) VALUES (:user_id, :symbol, :share, :price)",
                    user_id=user_id, symbol=symbol, share=(disposal*-1), price=quote["price"])

        # Update user's portfolio
        if asset[0]["share"] == disposal:
            # Remove item from portfolio if selling all shares
            db.execute("DELETE FROM portfolio WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
        else:
            # Update share, price and total
            new_shares = asset[0]["share"] - disposal
            new_total = new_shares * quote["price"]
            db.execute("UPDATE portfolio SET share = :share, price = :price, total = :total WHERE id = :user_id AND symbol = :symbol",
                    share=new_shares, price=quote["price"], total=new_total, user_id=user_id, symbol=symbol)

        # Calculate capital gain
        gain = disposal * quote["price"]

        # Query user's cash total
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        # Calculate user's cash total after selling shares
        total_cash = round(cash[0]["cash"] + gain , 2)
        # Update user's cash total
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=total_cash, user_id=user_id)

        # Flash message
        flash('Shares sold!')
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute("SELECT symbol FROM portfolio WHERE id = :user_id", user_id=user_id)
        return render_template("sell.html", rows=rows)

@app.route("/funds", methods=["GET", "POST"])
@login_required
def funds():
    """Deposit or withdraw cash from account"""

    if request.method == "POST":

        # Assign form inputs to variables
        action = request.form.get("action")
        amount = request.form.get("amount")

        # Check that an amount has been entered
        try:
            float(amount)
        except ValueError:
            return apology("No amount selected", 400)

        # Convert amount from a string to a float
        amount = float(amount)

        # Assign user id to variable
        user_id = session["user_id"]

        # Query database for user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)

        # If user wants to deposit money to their account
        if action == "deposit":
            # Calcute user's new cash total
            new_cash = cash[0]["cash"] + amount
            # Update user's cash in database

        # If user wants to withdraw money from their account
        else:
            # Check that user has sufficent funds
            if amount > cash[0]["cash"]:
                return apology("insufficient funds", 400)
            # Calcute user's new cash total
            else:
                new_cash = cash[0]["cash"] - amount

        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=new_cash, user_id=user_id)
        flash('Balance updated.')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("funds.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

