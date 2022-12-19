import os
import sqlite3
from helpers import error
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session


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

        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        db.commit()
        rows = db.execute('SELECT * FROM users WHERE username = (?)', (username,))
        
        session["user_id"] = rows.fetchone()["id"]
        session["user"] = username
        db.close()
        return f"user with ID {session['user_id']} registered and logged in"
    else:
        return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return error("must provide username", 403)
        if not password:
            return error("must provide password", 403)
        username = username.lower()
        db = get_db_connection()
        rows = db.execute('SELECT * FROM users WHERE username = (?)', (username,))
        hash = rows.fetchone()["password_hash"]
        if hash != generate_password_hash(password):
            db.close()
            return error('invalid username or password', 403)
        session["user_id"] = rows.fetchone()["id"]
        session["user"] = username
        db.close()
        return f"user with ID {session['user_id']} registered and logged in"
    else:
        return render_template('login.html')


@app.route("/members", methods=['GET'])
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/details/<string:info>")
def details(info):
    return "working"

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        #check if new course or coursework
        if request.form.get('course'):
            code = request.form.get('code')
            title = request.form.get('title')
            info = request.form.get('info')
            db = get_db_connection()
            db.execute("INSERT INTO courses (code, title, info) VALUES (?, ?, ?)", (code, title, info))
            db.commit()
            return {"status": "New course registered successfully"}
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            due = request.form.get('due')
            course_type = request.form.get('course_type')
            course_id = request.form.get('coruse_id')
            return render_template('error.html', content, due, course_type, course_id)
    else:
        #return create page
        return f"create page here"

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

@app.route("/search", methods = ["GET", "POST"])
def search():
	if session.get("user") is None:
		return render_template("login.html")
	if request.method == "POST":
		entry = request.form.get("search")
		entry_lower = entry.lower()
		entry_upper = entry.capitalize()
		if not entry:
			return "enter a search term"
		#perform database query with entry
		results= db.execute("SELECT isbn, author, title, year FROM books WHERE isbn LIKE :entry OR isbn LIKE :entry2 OR author LIKE :entry OR author LIKE :entry2 OR title LIKE :entry  OR title LIKE :entry2", {"entry": '%' +entry_lower+ '%', "entry2": '%' +entry_upper+ '%'}).fetchall()
		return render_template("results.html", results=results)
	else:
		return render_template("index.html")
	#return database results to "/"

if __name__ == "__main__":
    app.run(debug=True)
