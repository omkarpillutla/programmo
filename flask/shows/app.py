import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

db = sqlite3.connect("shows.db", check_same_thread=False)
def dict_factory(cursor, row):
    dict = {}
    for id, col in enumerate(cursor.description):
        dict[col[0]] = row[id]
    return dict
db.row_factory = dict_factory


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    shows = db.execute("SELECT * FROM shows WHERE title LIKE ?", ("%" + request.args.get("q") + "%", )).fetchall()

    return jsonify(shows)