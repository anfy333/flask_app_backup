from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("signup.html")

@app.route("/home", methods=['POST'])
def signup():
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("""INSERT INTO Users (Username, Password) VALUES (?,?)""",
		(request.form['un'], password))
	con.commit()
	return 'welcome '+ request.form['un']

@app.route("/login")
def login():
	return render_template("login.html")

@app.route('/verify', methods=['POST'])
def verify():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
		(request.form['un'],request.form['pw']))
	match = len(cur.fetchall())
	if match == 0:
		return "Wrong username and password"
	else:
		return "Welcome " + request.form['un']

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
