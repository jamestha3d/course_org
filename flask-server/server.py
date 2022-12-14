import os
import sqlite3
from helpers import error
#import requests
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
#from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

SESSION_TYPE = 'filesystem'

app = Flask(__name__)
app.config.from_object(__name__)
Session(app)

#set up access to database
def get_db_connection():
    conn = sqlite3.connect('tables.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db_connection()
    courses = db.execute('SELECT * FROM courses').fetchall()
    students = db.execute("SELECT * FROM users").fetchall()
    db.close()
    return render_template("index.html", courses=courses, students=students)

@app.route('/register', methods=['GET', 'POST'])
def  register():
    session.clear()
    if request.method == 'POST':
        if not request.form.get("username"):
            return error("must provide username", 403)

        if not request.form.get("password"):
            return error("must provide password", 403)

        if request.form.get("password") != request.form.get("confirmation"):
            return error("password mismatch", 403)

        username = request.form.get("username").lower()
        db = get_db_connection()
        rows = db.execute('SELECT * FROM users WHERE username = (?)', (username,))
        if rows.fetchone():
            db.close()
            return error('username already taken', 403)

            #return render_template('error.html', rows=rows)

        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        db.commit()
        rows = db.execute('SELECT * FROM users WHERE username = (?)', (username,))
        
        session["user_id"] = rows.fetchone()["id"]
        session["user"] = username
        db.close()
        # Redirect user to home page
        return f"user with ID {session['user_id']} registered and logged in"
    else:
        return render_template("register.html")

# Members API Route
@app.route("/members", methods=['GET'])
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True)
