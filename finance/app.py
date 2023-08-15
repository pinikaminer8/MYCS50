import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


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
    cash_balance_result = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cash_balance = cash_balance_result[0]["cash"]

    holdings_result = db.execute(
        "SELECT * FROM (SELECT symbol, SUM(shares) as num_shares FROM purchases WHERE user_id = :user_id GROUP BY symbol)", user_id=session["user_id"])

    holdings = []
    total = cash_balance

    for holding in holdings_result:
        symbol = holding["symbol"]
        shares = holding["num_shares"]
        stock_info = lookup(symbol)
        price = stock_info["price"]
        total_value = stock_info["price"] * shares

        holdings.append({
            "symbol": symbol,
            "shares": int(shares),
            "price": price,
            "total_value": usd(total_value)
        })

        total += total_value

    return render_template("index.html", holdings=holdings, cash_balance=usd(cash_balance), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        stock_info = lookup(symbol)
        if not stock_info:
            return apology("invalid symbol")

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide shares")
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive num of shares")

        shares = int(shares)
        share_price = usd(stock_info["price"])
        cost = stock_info["price"] * shares
        balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

        if balance < cost:
            return apology("there is not enough money in your balance to make the purchase")

        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :user_id", cost=cost, user_id=session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, timestamp) VALUES (:user_id, :symbol, :shares, :price, :timestamp)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, price=share_price, timestamp=datetime.now())

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    history_result = db.execute("SELECT * FROM purchases WHERE user_id = :user_id", user_id=session["user_id"])

    history_list = []
    for result in history_result:
        symbol = result["symbol"]
        shares = result["shares"]
        stock_info = lookup(symbol)
        price = stock_info["price"]
        time = result["timestamp"]

        history_list.append({
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "time": time
        })
    return render_template("history.html", history_list=history_list)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        stock_info = lookup(symbol)

        if not stock_info:
            return apology("invalid symbol")
        stock_info["price"] = usd(stock_info["price"])

        return render_template("quoted.html", stock_info=stock_info)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("All fields must be filled")

        if password != confirmation:
            return apology("Passwords do not match")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) > 0:
            return apology("Username already exists")

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password_hash)",
                   username=username, password_hash=password_hash)

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide num of shares")
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive num of shares")

        holdings_result = db.execute(
            "SELECT symbol, SUM(shares) as num_shares FROM purchases WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

        is_exist_symbol = False
        maintenance_amount = 0
        price = 0

        for holding in holdings_result:
            cur_symbol = holding["symbol"]
            cur_shares = holding["num_shares"]
            stock_info = lookup(symbol)
            cur_price = stock_info["price"]
            if symbol == cur_symbol:
                is_exist_symbol = True
                maintenance_amount = cur_shares
                price = cur_price

        if not is_exist_symbol:
            return apology("You don't own any shares of that stock")
        if int(shares) > int(maintenance_amount):
            return apology("You don't own enough shares of that stock")

        balance_result = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = balance_result[0]["cash"]

        refund = float(price) * int(shares)

        balance += refund
        refund = -1 * (float(price) * int(shares))
        shares = int(shares) * -1
        db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", balance=balance, user_id=session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price, timestamp) VALUES (:user_id, :symbol, :shares, :price, :timestamp)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, price=refund, timestamp=datetime.now())
        return redirect("/")
    else:
        holdings = db.execute(
            "SELECT symbol FROM purchases WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])
        return render_template("sell.html", holdings=holdings)
