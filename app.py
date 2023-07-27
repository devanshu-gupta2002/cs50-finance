import os
import time
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
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
    userid=session["user_id"]
    rows=db.execute("SELECT * FROM portfolio WHERE userid=:userid", userid=userid)
    cash=db.execute("SELECT cash FROM users WHERE id=:id", id=userid)
    cash=cash[0]['cash']    #current balance
    sum=cash                #total value of all the cash holdings

    for row in rows:        #adding name, current price, total in rows
        look=lookup(row['symbol'])
        row['name']=look['name']
        row['price']=look['price']
        row['total']=row['price']*row['shares']

        sum+=row['total']

        #convert price and total to usd
        row['price']=usd(row['price'])
        row['total']=usd(row['total'])

    return render_template("home.html", rows=rows, cash=usd(cash), sum=usd(sum))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must provide symbol", 403)
        elif not shares:
            return apology("must provide shares")
        
        symbol=symbol.upper()
        shares=int(shares)
        quote = lookup(symbol)
        if quote==None:
            return apology("must provide valid symbol")
        
        userid=session["user_id"]
        purchase=quote['price']*shares
        balance=db.execute("SELECT cash FROM users WHERE id = :id", id=userid)
        remainder=balance[0]["cash"]-purchase
        ts=time.time()
        date_time = datetime.fromtimestamp(ts)
        # return jsonify(date_time)
        # return jsonify(balance)
        # return jsonify(remainder)
        
        if remainder<0:
            return apology("insufficient balance", 403)
        
        row = db.execute("SELECT * FROM portfolio WHERE userid=:userid AND symbol=:symbol", userid=userid, symbol=symbol)
        if len(row)!=1:
            db.execute("INSERT INTO portfolio (userid, symbol) VALUES (:userid, :symbol)", userid=userid, symbol=symbol)
        
        oldshares=db.execute("SELECT shares FROM portfolio WHERE userid=:userid AND symbol=:symbol", userid=userid, symbol=symbol)
        # return jsonify(oldshares)
        oldshares=int(oldshares[0]["shares"])
        newshares=oldshares+shares
        db.execute("UPDATE portfolio SET shares=:newshares where userid=:userid AND symbol=:symbol", newshares=newshares, userid=userid, symbol=symbol)             
        db.execute("UPDATE users SET cash=:remainder WHERE id=:id", remainder=remainder, id=userid)

        return redirect("/")

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
    userid=session["user_id"]

    if request.method == "GET":
        portfolio = db.execute("SELECT symbol FROM portfolio WHERE userid=:userid", userid=userid)

        return render_template("sell.html", portfolio=portfolio)
    
    else:
        symbol=request.form.get("symbol")
        shares=request.form.get("shares")
        quote=lookup(symbol)
        rows=db.execute("SELECT * FROM portfolio WHERE userid=:userid AND symbol=:symbol", userid=userid, symbol=symbol)

        if not shares:
            return apology("must provide number of shares", 403)
        
        oldshares = rows[0]['shares']
        shares=int(shares)
        if shares>oldshares:
            return apology("shares sold can't exceed shares owned", 403)
        
        sold=quote['price']*shares                      #selling price of stocks sold

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session['user_id'])
        cash = cash[0]['cash']
        cash = cash + sold                              #final balance

        #update cash in db
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=userid)      

        #if shares remain update portfolio with updated stocks
        newshares=oldshares-shares
        if newshares>0:
            db.execute("UPDATE portfolio SET shares=:newshares WHERE userid=:userid AND symbol=:symbol", newshares=newshares, userid=userid, symbol=symbol)
        else:
            db.execute("DELETE FROM portfolio WHERE userid=:userid AND symbol=:symbol", userid=userid, symbol=symbol)
        
        return redirect("/")




