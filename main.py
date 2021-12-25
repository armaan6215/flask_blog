import sqlite3 as sql
from flask import Flask, render_template, request, url_for, redirect
import model
from datetime import datetime

app = Flask(__name__)

try:
    model.create_table()
except Exception as e:
    print(e)


def db_connection():
    with sql.connect("database.db") as conn:
        conn.row_factory = sql.Row
        return conn


@app.route("/")
def index():
    message = "Welcome to Index page of Blog Created by Manish"
    return render_template("index.html", message=message)


@app.route("/create", methods=("GET", "POST"))
def create_post():
    message = ""
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        current_time = datetime.now()

        if not title or not content:
            message = "Title and Description cannot be empty..."
        else:
            conn = db_connection()
            conn.execute(
                "INSERT INTO POSTS (title, content, author, date_created) VALUES (?, ?, ?, ?)",
                (title, content, author, current_time),
            )
            conn.commit()
            return redirect(url_for("posts"))

    return render_template("create_post.html", message=message)


@app.route("/posts")
def posts():
    req_query = "SELECT * FROM POSTS {value}"
    if request.args:
        args = request.args
        for k, v in args.items():
            if k == "order" and v == "asc":
                query = req_query.format(value="ORDER BY id ASC")
            elif k == "order" and v == "desc":
                query = req_query.format(value="ORDER BY id DESC")
            elif k == "author":
                query = req_query.format(value="WHERE author='%s'" % v)
            elif k == "limit":
                query = req_query.format(value="LIMIT %s" % v)
    else:
        query = req_query.format(value="")

    conn = db_connection()
    posts = conn.execute(query).fetchall()
    return render_template("posts.html", posts=posts), 200


app.run(debug=True)
