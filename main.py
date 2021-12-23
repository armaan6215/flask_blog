import sqlite3 as sql
from flask import Flask, render_template, request, url_for, redirect
import model
from datetime import datetime

app = Flask(__name__)

try:
    model.create_table()
except Exception as e:
    print("Error is", e)


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
        for k, v in args.items():
            if k=='order' and v == "asc":
                query = "SELECT * FROM POSTS LIMIT 5"
            elif k=='order' and v == "desc":
                query = "SELECT * FROM POSTS ORDER BY id DESC LIMIT 5"
            elif k == "author":
                query = ("SELECT * FROM POSTS WHERE author='%s'" %v)
    else:
        query = "SELECT * FROM POSTS LIMIT 5"
   

    conn = db_connection()
    posts = conn.execute(query).fetchall()
    return render_template("posts.html", posts=posts), 200


app.run(debug=True)
