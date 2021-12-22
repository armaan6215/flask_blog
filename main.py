import re
import sqlite3 as sql
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


def db_connection():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=("GET", "POST"))
def create_post():
    if (request.method == "POST"):
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]

        conn = db_connection()
        conn.execute(
            "INSERT INTO POSTS (title, content, author) VALUES (?, ?, ?)",
            (title, content, author),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('posts'))

    return render_template("create_post.html")


@app.route("/posts")
def posts():
    query = "SELECT * FROM POSTS"
    conn = db_connection()
    posts = conn.execute(query).fetchall()
    conn.close()
    return render_template("posts.html", posts=posts)


app.run(debug=True)
