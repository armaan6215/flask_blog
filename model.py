import sqlite3 as sql

connection = sql.connect("database.db")


def create_table():
    with open("table.sql") as f:
        try:
            connection.executescript(f.read())
        except Exception as e:
            print(e)
