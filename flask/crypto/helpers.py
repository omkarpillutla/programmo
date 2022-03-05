import os
from flask import render_template
import requests
import locale

from functools import wraps
from flask import session, url_for, redirect

# Configure locale currency
locale.setlocale(locale.LC_MONETARY, 'en_IN')

# Requires user to be logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Gets quote of given crypto
def lookUp(symbol):
    # Contact API
    try:
        API_KEY = os.getenv("API_KEY")
        url = f"https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={symbol}&convert=INR&CMC_PRO_API_KEY={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        response = response.json()
        result = response["data"]
        return {
            "name": result["name"],
            "symbol": result["symbol"],
            "price": result["quote"]["INR"]["price"]
        }
    except:
        return None

# Custom error
def customError(message, code=400):
    return render_template("error.html", message=message, code=code), code

# Formats currency to INR
def inr(amount):
    result = locale.currency(amount, grouping=True)
    result = result.split()[1]

    return u"\u20B9" + " " + result