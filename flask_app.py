from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib
import json
import requests



app = Flask(__name__)

global username

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def sign():
	global username
	# hashes the password
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("""INSERT INTO Users (Username, Password, FirstName, LastName, Email) VALUES (?,?,?,?,?)""",
		(request.form['un'], password, request.form['fn'], request.form['ln'], request.form['em']))
	con.commit()
	#inserts hashed password with the other details into the login database
	username = request.form['un']
	user = request.form['un']
	return redirect(url_for('home', name = user))

@app.route("/login")
def login():
	return render_template("login.html")

@app.route('/verify', methods=['POST'])
def verify():
	global username
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
	#the entered password has to be hashed, because all passwords are stored in hash in the database
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
		(request.form['un'],password))
	# database looks for corresponding username and password
	match = len(cur.fetchall())
	user = request.form['un']
	if match == 0:
		return "Wrong username or password"
	else:
		username = user
		# the username varible is a global variable, which is used later in a different function
		# redirecting to home page carrying the username
		return redirect(url_for('home', name = user))


@app.route("/chat",methods=['GET'])
def chat():
	global username
	input = request.args
	print(input)

	def query(payload):
		data = json.dumps(payload)
		response = requests.request("POST", API_URL, headers=headers, data=data)
		return json.loads(response.content.decode("utf-8"))

	high_score0 = []
	high_score1 = []
	high_score2 = []


	def sorting(data):
		sentiment = data[0]
		dict0 = sentiment[0]
		dict1 = sentiment[1]
		dict2 = sentiment[2]

		high_score0.clear()
		high_score1.clear()
		high_score2.clear()

		for x in dict0.values():
			high_score0.append(x)

		for x in dict1.values():
			if dict1['score'] >= 0.01:
				high_score1.append(x)

		for x in dict2.values():
			if dict2['score'] >= 0.01:
				high_score2.append(x)

		with open("Bot.json", "r") as f:
			file = json.load(f)

		if file[0]["sentiment"] == high_score0[0] or file[0]["sentiment"] == high_score1[0]:
			return "I understand you are feeling "+ file[0]["feeling"]+". Please check out this video "+ file[0]["URL"]
		elif input in file[1]["user_input"]:
			return file[1]["response"]
		else:
			return "Sorry, I don't understand this yet"

	while True:
		API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
		API_TOKEN = "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"
		headers = {"Authorization": f"Bearer {API_TOKEN}"}


		list = query(input['msg'])
		info = json.dumps(sorting(list))
		print("Bot:",sorting(list))
		break

	#con = sqlite3.connect('login.db')
	#cur = con.cursor()
	#cur.execute("""INSERT INTO Messages (SenderId, RecipientId, Message) VALUES (?,?,?)""",
		#([username],"Bot" , input))
	#con.commit()

	return info

@app.route("/home/<name>")
def home(name):
	return render_template("home.html", name = name)


@app.route("/account")
def account():
	global username
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users WHERE Username= ?", [username])
	rows = cur.fetchall()
	return str(rows)

@app.route("/db")
def db():
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    try:
        cur.execute("""
        CREATE TABLE Users(
        Username VARCHAR(20) NOT NULL PRIMARY KEY,
	Password VARCHAR(20) NOT NULL, FirstName TINYTEXT, LastName	TINYTEXT, Email	VARCHAR(50))
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
