import sqlite3 as sql
from flask import Flask, render_template, request, url_for, redirect
import model
from datetime import datetime

app = Flask(__name__)

model.create_table()


def db_connection():
    with sql.connect("database.db") as conn:
        conn.row_factory = sql.Row
        return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=("GET", "POST"))
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        current_time = datetime.now()

        conn = db_connection()

        conn.execute(
            "INSERT INTO POSTS (title, content, author, date_created) VALUES (?, ?, ?, ?)",
            (title, content, author, current_time),
        )
        conn.commit()
        return redirect(url_for("posts"))

    return render_template("create_post.html")


@app.route("/posts")
def posts():
    if request.args:
        args = request.args
        if "order" in args:
            order = args.get("order")
        if order == "asc":
            query = "SELECT * FROM POSTS"
        elif order == "desc":
            query = ("SELECT * FROM POSTS ORDER BY id DESC")
    
    else:
        query = "SELECT * FROM POSTS"

    conn = db_connection()
    posts = conn.execute(query).fetchall()
    return render_template("posts.html", posts=posts), 200


app.run(debug=True)
