from flask import Flask, render_template, request
import datetime

app = Flask(__name__)
today = datetime.date.today()



@app.route("/")
def index():
    # if today.month == 1 and today.day == 1:
    #     confirm = True
    # else:
    #     confirm = False
    
    confirm = today.month == 1 and today.day == 1

    return render_template("index.html", date=today, confirm=confirm)