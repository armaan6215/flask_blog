import sqlite3 as sql
from flask import Flask, render_template

app = Flask(__name__)


def db_connection():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/posts")
def posts():
    query = "SELECT * FROM POSTS"
    conn = db_connection()
    posts = conn.execute(query).fetchall()
    conn.close()
    return render_template("posts.html", posts=posts)


app.run(debug=True)
