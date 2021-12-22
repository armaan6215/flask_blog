import sqlite3 as sql

content = "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ipsam, ullam hic repudiandae quam minus illo ea sunt velit? Iusto laborum quam nostrum nobis veritatis reprehenderit, est ipsum aspernatur quasi sit consectetur rem optio nemo?"
connection = sql.connect("database.db")

with open("table.sql") as f:
    try:
        connection.executescript(f.read())
    except Exception as e:
        print(e)

cur = connection.cursor()
cur.execute(
    "INSERT INTO POSTS (title, content, author) VALUES (?, ?, ?)",
    ("First Post", content , "Manish"),
)


connection.commit()
connection.close()
