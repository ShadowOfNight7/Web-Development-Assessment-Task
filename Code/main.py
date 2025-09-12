from flask import Flask, render_template, request, redirect, url_for, flash
from flask import render_template
from flask import request
import databaseManager as dbHandler
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB_PATH = "Code/leaf&LushDatabase.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/index.html", methods=["GET"])
@app.route("/", methods=["POST", "GET"])
def index():
    data = dbHandler.listExtension()
    return render_template("/index.html", content=data)


@app.route("/produce.html")
def produce():
    return render_template("produce.html")


@app.route("/recipes.html")
def recipes():
    return render_template("recipes.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM userData WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        conn.close()

        if user:
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("signin"))

    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()
        existing_user = conn.execute(
            "SELECT * FROM userData WHERE username = ?", (username,)
        ).fetchone()

        if existing_user:
            conn.close()
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for("signup"))

        conn.execute(
            "INSERT INTO userData (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
        conn.close()

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for("signin"))

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
