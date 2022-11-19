from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def sign():
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("""INSERT INTO Users (Username, Password, FirstName, LastName, Email) VALUES (?,?,?,?,?)""",
		(request.form['un'], password, request.form['fn'], request.form['ln'], request.form['em']))
	con.commit()
	user = request.form['un']
	return redirect(url_for('home', name = user))

@app.route("/login")
def login():
	return render_template("login.html")

@app.route('/verify', methods=['POST'])
def verify():
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
		(request.form['un'],password))
	match = len(cur.fetchall())
	user = request.form['un']
	if match == 0:
		return "Wrong username or password"
	else:
		return redirect(url_for('home', name = user))

@app.route("/home/<name>")
def home(name):
	#text = request.get_json().get("message")
	return render_template("home.html", name = name)

@app.route("/db")
def db():
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    try:
        cur.execute("""
        CREATE TABLE Users(
        Username VARCHAR(20) NOT NULL PRIMARY KEY,
	Password VARCHAR(20) NOT NULL)
        """)
    except sqlite3.OperationalError as e:
        return str(e)
    return "table created"

@app.route('/insert')
def insert():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute(	"""	INSERT INTO Users (Username, Password)
					VALUES ("anfy", "7295")
			""")
	con.commit()
	return 'INSERT'

@app.route('/select')
def select():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users")
	rows = cur.fetchall()
	return str(rows)

@app.route('/alter')
def alter():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute(	"""	ALTER TABLE Users
					ADD Email VARCHAR(50)
			""")
	con.commit()
	return 'alter'
