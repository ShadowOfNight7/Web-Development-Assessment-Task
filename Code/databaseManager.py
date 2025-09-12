import sqlite3 as sql


def listExtension():
    con = sql.connect("Code/leaf&LushDatabase.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM allData").fetchall()
    con.close()
    return data
