import re
import sqlite3 as sql
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "96159"


def db_connection():
    conn = sql.connect("database.db")
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

        conn = db_connection()
        conn.execute(
            "INSERT INTO POSTS (title, content, author) VALUES (?, ?, ?)",
            (title, content, author),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("posts"))

    return render_template("create_post.html")


@app.route("/posts")
def posts():
    query = "SELECT * FROM POSTS"
    conn = db_connection()
    posts = conn.execute(query).fetchall()
    conn.close()
    return render_template("posts.html", posts=posts)


app.run(host="192.168.1.103", port=5000, threaded=True, debug=True)
