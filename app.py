import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    
    # cash = db.execute("SELECT cash FROM users WHERE id = ?", id=session["user_id"])

    return render_template("home.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        
        elif not request.form.get("shares"):
            return apology("must provide shares")
        

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    """Register User"""
    session.clear()

    if request.method=="POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        #ensure password are equal
        elif request.form.get("password")!=request.form.get("confirmation"):
            return apology("password do not match")
        
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        #ensure thath the username is unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows)!=0:
            return apology("username is already taken", 403)
        
        #insert (username, hash) into DB
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

        return redirect("/")
    
    else:
        return render_template("register.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if GET method, return quote.html form
    if request.method == "GET":
        return render_template("quote.html")

    # if POST method, get info from form, make sure it's a valid stock
    else:

        # lookup ticker symbol from quote.html form
        symbol = lookup(request.form.get("symbol"))

        # if lookup() returns None, it's not a valid stock symbol
        if symbol == None:
            return apology("invalid stock symbol", 403)

        # Return template with stock quote, passing in symbol dict
        return render_template("quoted.html", symbol=symbol)



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return render_template("sell.html")
