import os
import sqlite3

from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_session import Session
from werkzeug.exceptions import HTTPException, default_exceptions, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, customError, inr, lookUp

# Configure flask app
app = Flask(__name__)

# Ensure templates reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses are not cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["inr"] = inr

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
db = sqlite3.connect("crypto.db", check_same_thread=False, timeout=20)
def dict_factory(cursor, row):
    dict = {}
    for id, col in enumerate(cursor.description):
        dict[col[0]] = row[id]
    return dict
db.row_factory = dict_factory

# Ensure API_KEY is set
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Portfolio"""
    
    # Query the database for transaction details
    PORT = db.execute("SELECT name, symbol, quantity, value FROM transactions WHERE user_id = ?", (session["user_id"], )).fetchall()
    MAX_VAL = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"], )).fetchall()
    max_val = list(MAX_VAL[0].values())
    max_val = max_val[0]

    SUM = db.execute("SELECT SUM(value) FROM transactions WHERE user_id = ?", (session["user_id"], )).fetchall()
    sum = list(SUM[0].values())
    if sum[0] is None:
        sum[0] = 0 
    int_sum = float(sum[0])

    balance = max_val - int_sum
    balance = inr(balance)
    
    return render_template("portfolio.html", port=PORT, bal = balance)

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get quote of crypto"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        RESULTS = lookUp(symbol)
        name = RESULTS["name"]
        price = inr(RESULTS["price"])
        
        return render_template("quote.html", name=name, price=price, symbol=symbol)
    
    return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy Crypto"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quantity = int(request.form.get("qty"))
        trans_type = "Buy"
        BUYS = lookUp(symbol)
        value = BUYS["price"]*quantity

        MAX_VAL = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"], )).fetchall()
        max_val = list(MAX_VAL[0].values())
        max_val = max_val[0]

        SUM = db.execute("SELECT SUM(value) FROM transactions WHERE user_id = ?", (session["user_id"], )).fetchall()
        sum = list(SUM[0].values())
        if sum[0] is None:
            sum[0] = 0 
        int_sum = float(sum[0])

        balance = max_val - int_sum
        if (value <= balance):
            RECORD_EXISTS = db.execute("SELECT name, symbol, quantity, value FROM transactions WHERE symbol = ? AND user_id = ?", (BUYS["symbol"], session["user_id"])).fetchall()
            print("Record", RECORD_EXISTS)
            
            # Add transaction to database
            if RECORD_EXISTS:
                exist_val = list(RECORD_EXISTS[0].values())
                e_qty = quantity + exist_val[2]
                e_value = value + exist_val[3]
                print("record ",e_value )
                print("qty = ", e_qty)
                db.execute("UPDATE transactions SET value = ?, quantity = ? WHERE symbol = ? AND user_id = ?", (e_value, e_qty, BUYS["symbol"], session["user_id"]))
            else:
                db.execute("INSERT INTO transactions(user_id, name, symbol, quantity, value) VALUES (?, ?, ?, ?, ?)", (session["user_id"], BUYS["name"], BUYS["symbol"], quantity, value))
            
            db.execute("INSERT INTO history(user_id, name, symbol, quantity, value, type) VALUES (?, ?, ?, ?, ?, ?)", (session["user_id"], BUYS["name"], BUYS["symbol"], quantity, value, trans_type))
            db.commit()

            return redirect("/")
        
        else:
            flash("That shit's too expensive")

    return render_template("buy.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """"Sell crypto"""
    PORT = db.execute("SELECT name, symbol, quantity FROM transactions WHERE user_id = ?", (session["user_id"], )).fetchall()
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quantity = int(request.form.get("qty"))
        trans_type = "Sell"
        SELLS = lookUp(symbol)
        value = SELLS["price"]*quantity

        # Add transaction to database
        RECORD_EXISTS = db.execute("SELECT name, symbol, quantity, value FROM transactions WHERE symbol = ? AND user_id = ?", (symbol, session["user_id"])).fetchall()
        print("Sell_Record", RECORD_EXISTS)
        
        # Add transaction to database
        if RECORD_EXISTS:
            exist_val = list(RECORD_EXISTS[0].values())
            e_val = exist_val[3] - value
            e_qty = exist_val[2] - quantity
            print("record ", e_qty )
            db.execute("UPDATE transactions SET value=?, quantity = ? WHERE symbol = ? AND user_id = ?", (e_val, e_qty, symbol, session["user_id"]))
            if e_qty <= 0:
                db.execute("DELETE FROM transactions WHERE quantity <= 0")

            name = exist_val[0]
            db.execute("INSERT INTO history(user_id, name, symbol, quantity, value, type) VALUES (?, ?, ?, ?, ?, ?)", (session["user_id"], name, symbol, quantity, value, trans_type))
            db.commit()

            return redirect("/")
        
        else:
            flash("Invalid Entry")

    return render_template("sell.html", exists=PORT)

@app.route("/history")
@login_required
def history():
    """History of all transactions"""
    # Query the database for transaction details
    HISTORY = db.execute("SELECT name, id, symbol, quantity, type, value FROM history WHERE user_id = ?", (session["user_id"], )).fetchall()

    return render_template("history.html", history=HISTORY)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs in the user"""

    # Forget any user_id
    session.clear()

    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
           return customError("Missing Username", 403)

        if not password:
            return customError("Missing Password", 403)

        # Query the database for user details
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return customError("Invalid Username or Password", 403)

        # Remember which user logged in
        session["user_id"] = rows[0]["id"]

        # Flash
        flash("You have successfully logged in!")

        # Redirect to home page
        return redirect("/")

    # GET
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""

    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        USERS_EXIST = db.execute("SELECT username FROM users WHERE username = ?", (username, )).fetchall()

        if not username:
           return customError("Missing Username", 403)

        if not password:
            return customError("Missing Password", 403)

        if password != confirm_password:
            return customError("Invalid Password", 403)

        if USERS_EXIST:
            return customError("Invalid Username", 403)
        
        print("USERS_EXIST ", USERS_EXIST)

        # encrypt password
        encrypt = generate_password_hash(password)

        # Add user into database
        db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", (username, encrypt))
        db.commit()

        flash("Hello, you have succeessfully registered!")
        
        # Redirect to home page
        return redirect("/")
    
    # GET
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


def errorhandler(e):
    """Handle errors"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return customError(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
