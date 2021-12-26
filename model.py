import sqlite3 as sql

connection = sql.connect("database.db")

tables_list = ['table_users.sql', 'table_posts.sql']
def create_table():
    for table in tables_list:
        with open(f"tables/{table}") as f:
            try:
                connection.executescript(f.read())
            except Exception as e:
                print(e)


def drop_table():
    try:
        connection.executescript("DROP TABLE POSTS")
        connection.executescript("DROP TABLE USERS")
    except Exception as e:
        print(e)

# drop_table()