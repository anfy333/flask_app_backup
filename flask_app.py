from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
import json
import requests
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

@app.route("/")
def signup():
	return render_template("signup.html", status=request.args.get('status'))

@app.route("/signup", methods=['POST'])
def sign():
	# hashes the password
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users WHERE Email=?",
		(request.form['em'],))
	result = cur.fetchone()
	print(result)
	if result is None:
	#inserts hashed password with the other details into the login database
		cur.execute("""INSERT INTO Users (Name, Password, Email) VALUES (?,?,?)""",
			(request.form['un'], password, request.form['em'],))
		con.commit()
		session['email'] = request.form['em']
		name = request.form['un']
		return redirect(url_for('home', name = name))
	else:
		status = "User already exists"
		return redirect(url_for('signup', status=status))

@app.route("/login")
def login():
	return render_template("login.html", status=request.args.get('status'))

@app.route('/verify', methods=['POST'])
def verify():
	#the entered password has to be hashed, because all passwords are stored in hash in the database
	password = request.form['pw']
	en = password.encode()
	h = hashlib.sha256(en)
	password = h.hexdigest()
 	# database looks for corresponding username and password
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM Users WHERE Email=? AND Password=?",
		(request.form['em'],password))
	result = cur.fetchone()
	if result is None:
		print(cur.fetchone())
		status = "Incorrect email or password"
		return redirect(url_for('login', status = status))
	else:
		print(f"Match found: {result}")
		name = result[0]
		session['email'] = request.form['em']
		# redirecting to home page carrying the username
		return redirect(url_for('home', name = name))


@app.route("/chat",methods=['GET'])
def chat():
	input = request.args
	msg = input['msg']
	print(msg)

	def query(payload):
		payload = payload.lower()
		messages.append(payload)
		data = json.dumps(payload)
		response = requests.request("POST", API_URL, headers=headers, data=data)
		return json.loads(response.content.decode("utf-8"))

	with open("Bot.json", "r") as f:
		file = json.load(f)

	#create 2 lists
	high_score0 = []
	high_score1 = []

	def assessment(feeling):
		feelings.append(feeling)
		return "I understand you are feeling "+ feeling +". Am I correct?"

	def choice(answer):
		for i in file[3]["user_input"]:
			if i in answer:
				return "Would you like a quick relief exercise? Or would you like to talk about it?"
		for i in file[4]["user_input"]:
			if i in answer:
				messages.clear()
				feelings.clear()
				return "Let's try again. Please tell me, how are you feeling today?"

	def response3(answer):
		for i in file[5]["user_input"]:
				if i in answer:
					if feelings[0] == "anxiety":
						return "Please check out this meditation video: "+ file[0]["URL"]
					elif feelings[0] == "anger":
						return "Please check out this meditation video: "+ file[2]["URL"]
					elif feelings[0] == "sadness":
						return "Please check out this meditation video: "+ file[13]["URL"]
		for i in file[6]["user_input"]:
			if i in answer:
				return "I hear you. Is there any specific thought on your mind?"
		messages.clear()
		feelings.clear()
		return "Im sorry, looks like I don't understand this yet. Let's try again. Please tell me, how are you feeling today?"

	def response4(answer):
		for i in file[4]["user_input"]:
			if i in answer:
				messages.pop(3)
				messages.pop(2)
				return "I see. Let's try again. Would you like a quick relief exercise? Or would you like to talk about it?"
		for i in file[3]["user_input"]:
			if i in answer:
				return "Please tell me the thought or thoughts that bother you. If you would like to list a several thoughts, please divide them with a '.' sign."


	def response5(answer):
		list =" "
		global thoughts
		thoughts = answer.split(".")
		print(thoughts)
		for i in range(len(thoughts)):
			num = str(i + 1)
			list += num +". "+ thoughts[i]+ " "
		return "I have put together the list of the thoughts that bother you:" + list+". Is this correct?"

	def response6(answer):
		for i in file[3]["user_input"]:
			if i in answer:
				return random.choice(file[6]["response"])
		for i in file[4]["user_input"]:
			if i in answer:
				messages.pop(5)
				messages.pop(4)
				return "Let's try again. Please tell me the thought or thoughts that bother you. If you would like to list a several thoughts, please divide them with a '.' sign."

	def response7(answer):
		for i in file[3]["user_input"]:
			if i in answer:
				return "Awesome! Please tell me which thought you would like to work on. Just type in the number from the list like '1'"
		for i in file[4]["user_input"]:
			if i in answer:
				return "Okay, then I'm here to listen! Tell me all about how you are feeling"
		for i in file[7]["user_input"]:
			if i in answer:
				messages.pop(6)
				return random.choice(file[7]["response"])

	def response8(answer):
		for i in file[8]["user_input"]:
			if i in answer:
				answer = int(answer)
				print(thoughts)
				output = thoughts[answer-1]
				thoughts.clear()
				return "You would like to work on this thought: "+ output+". Am I correct?"
		for i in file[4]["user_input"]:
			if i in answer:
				random.choice(file[10]["response"])
		for i in file[4]["user_input"]:
			if i not in answer:
				messages.pop(7)
				return random.choice(file[9]["response"])
		messages.pop(7)
		return "I'm afraid I didn't understand it. Please tell me which thought you would like to work on. Just type in the number from the list like '1'"


	def response9(answer):
		for i in file[3]["user_input"]:
			if i in answer:
				return "Then I will ask you a few questions, please answer 'yes' or 'no'. Do you think in this thought you might be confusing assumption with reality?"
		for i in file[4]["user_input"]:
			if i in answer:
				messages.pop(8)
				messages.pop(7)
				return "I'm sorry, let's try again. Please tell me which thought you would like to reframe. Just type in the number from the list like '1'"
		messages.pop(8)
		return "Sorry, I didn't understand this. Please tell me if the thought is correct."


	def response10(answer):
		for i in file[3]["user_input"]:
			if i in answer:
				return "Sometimes we can jump into conclustions, basing them on poor evidence. This is called 'catastrophizing' or 'mind-reading'. Is there an alterantive explanation or a more constructive thought you can think of?"
		for i in file[4]["user_input"]:
			if i in answer:
				return "Do you think you might be thinking in the terms of all-or-nothing?"
		messages.pop(9)
		return "Sorry, I didn't get this. Please answer the questions using 'yes' or 'no' answers. Do you think in this thought you might be confusing assumption with reality?"

	def response11(answer):
		for i in file[3]["user_input"]:
			if (i in answer) and (i not in messages[9]):
				return "Sometimes we can see things in in extremes, believing something is entirely good or entirely bad, with no in between. This is called 'black and white thinking'. Can you think of a more balanced thought?"
		for i in file[4]["user_input"]:
			if (i in answer) and (i not in messages[9]):
				return "Maybe an example can help: a thought: 'My friend didn't call me back, so she must hate me.', and the explanation could be 'There isn't any evidence that my friend hates me, maybe she didn't hear my calls'. Can you think of a similar explanation?"
		for i in file[3]["user_input"]:
			if (i in answer):
				messages.clear()
				feelings.clear()
				return random.choice(file[11]["response"])
		for i in file[4]["user_input"]:
			if (i in answer):
				return "Is it possible that in this thought you're only paying attention to the negative side of things?"
		messages.pop(10)
		return "I'm afraid I didn't get this. Please answer the questions using 'yes' or 'no' answers."

	def response12(answer):
		for i in file[3]["user_input"]:
			if ((i in answer) and (i not in messages[10]) and (i in messages[9])) or ((i in answer) and (i in messages[10]) and (i not in messages[9])):
				messages.clear()
				feelings.clear()
				return random.choice(file[11]["response"])
		for i in file[4]["user_input"]:
			if (i in answer) and (i not in messages[10]) and (i in messages[9]):
				return "Maybe an example can help: a thought: 'If I don't get an A on this test, I'm a total failure.', and a more balanced thought could be ' It would be nice to get an A, but it’s okay if I don’t, this test doesn't define me'. Can you think of a similar thought?"
		for i in file[3]["user_input"]:
			if (i in answer) and (i in messages[10]) and (i not in messages[9]):
				messages.clear()
				feelings.clear()
				return random.choice(file[10]["response"])
		for i in file[3]["user_input"]:
			if (i in answer) and (i not in messages[10]) and (i not in messages[9]):
				return "Sometimes we can forget or minimise positive experiences, qualities or accomplishments. Can you think of any postitive aspects you might be missing?"
		for i in file[4]["user_input"]:
			if (i in answer):
				return "In this thought are you worrying about something that is not in your control?"
		messages.pop(11)
		return "I'm sorry I didn't understand this. Please answer the questions using 'yes' or 'no' answers."

	def response13(answer):
		for i in file[3]["user_input"]:
			if ((i in answer) and (i not in messages[11]) and (i in messages[10]) and (i not in messages[9])) or ((i in answer) and (i in messages[11]) and (i not in messages[10]) and (i not in messages[9])):
				messages.clear()
				feelings.clear()
				return random.choice(file[11]["response"])
		for i in file[4]["user_input"]:
			if (i in answer) and (i in messages[11]) and (i not in messages[10]) and (i in messages[9]):
				messages.clear()
				feelings.clear()
				return random.choice(file[10]["response"])
		for i in file[4]["user_input"]:
			if (i in answer) and (i not in messages[11]) and (i in messages[10]) and (i in messages[9]):
				return "Maybe an example can help: a thought: 'I was late to work and had a terrible day', a more constructive thought could be 'I was late, but on the whole my work went well and I had ice cream in the evening'. Can you think of a similar thought?"
		for i in file[3]["user_input"]:
			if (i in answer):
				return "It is natural for us to worry about things that are not in our control. Is there anything you can do to influence them positively? Is there any way you can accept the situation?"
		for i in file[4]["user_input"]:
			if (i in answer):
				return "I see. Sometimes thoughts can get too overwhelming for us to sort through them. It's important to remember to take care of yourself during hard times like this. Would you like a calming meditation?"
		messages.pop(12)
		return "I'm sorry I didn't get this. Please answer the questions using 'yes' or 'no' answers."

	def response14(answer):
		for i in file[4]["user_input"]:
			if (i in answer) and (i in messages[12]) and (i not in messages[11]) and (i in messages[10]) and (i in messages[9]):
				messages.clear()
				feelings.clear()
				return random.choice(file[10]["response"])
		for i in file[3]["user_input"]:
			if ((i in answer) and (i not in messages[12]) and (i in messages[11]) and (i not in messages[10]) and (i not in messages[9])) or ((i in answer) and (i in messages[12]) and (i not in messages[11]) and (i not in messages[10]) and (i not in messages[9])):
				messages.clear()
				feelings.clear()
				return random.choice(file[11]["response"])
		for i in file[4]["user_input"]:
			if (i in answer) and (i not in messages[12]) and (i in messages[11]) and (i in messages[10]) and (i in messages[9]):
				messages.clear()
				feelings.clear()
				return "I hear you. Please remember that it's okay to feel anxious or uncertain, but challenges are a natural part of life, and they often lead to growth and resilience."
		for i in file[3]["user_input"]:
			if (i in answer):
				messages.clear()
				feelings.clear()
				return "Please check out this meditation video: "+ file[0]["URL"]
		for i in file[4]["user_input"]:
			if (i in answer):
				messages.clear()
				feelings.clear()
				return "I see. It might be helpful to reach out to someone you can trust. Please, remember to take care of yourself and stay hydrated. It is okay to not be okay and remember that things can get better with time<3."
		messages.pop(13)
		return "Sorry, I didn't get this. Please answer the questions using 'yes' or 'no' answers."
	# assign first 2 dictionaries in the list to variables dict0 and dict1
	def sorting(data):
		sentiment = data[0]
		dict0 = sentiment[0]
		dict1 = sentiment[1]

	#clear the lists so that when the request is sent again, the list would not hold the old information
		high_score0.clear()
		high_score1.clear()

		for x in dict0.values():
			high_score0.append(x)
		for x in dict1.values():
			if dict1['score'] <= 0.01:
				high_score1.append("0")
			else:
				high_score1.append(x)

	#  opens a file "Bot.json" in read mode and loads its contents into a variable "file" using the json module
		#with open("Bot.json", "r") as f:
			#file = json.load(f)
	# looks for the corresponding "sentiment" ion the file and returns a URL if found
		if (file[0]["sentiment"] == high_score0[0] or file[0]["sentiment"] == high_score1[0]) and len(messages) == 1:
			return assessment(file[0]["feeling"])
		elif msg in file[1]["user_input"]:
			messages.clear()
			feelings.clear()
			return file[1]["response"]
		elif msg in file[12]["user_input"]:
			messages.clear()
			feelings.clear()
			return file[12]["response"]
		elif (file[2]["sentiment"] == high_score0[0] or file[2]["sentiment"] == high_score1[0]) and len(messages) == 1:
			return assessment(file[2]["feeling"])
		elif (file[13]["sentiment"] == high_score0[0] or file[13]["sentiment"] == high_score1[0]) and len(messages) == 1:
			return assessment(file[13]["feeling"])
		elif len(messages) == 2:
			return choice(messages[1])
		elif len(messages) == 3:
			return response3(messages[2])
		elif len(messages) == 4:
			return response4(messages[3])
		elif len(messages) == 5:
			return response5(messages[4])
		elif len(messages) == 6:
			return response6(messages[5])
		elif len(messages) == 7:
			return response7(messages[6])
		elif len(messages) == 8:
			return response8(messages[7])
		elif len(messages) == 9:
			return response9(messages[8])
		elif len(messages) == 10:
			return response10(messages[9])
		elif len(messages) == 11:
			return response11(messages[10])
		elif len(messages) == 12:
			return response12(messages[11])
		elif len(messages) == 13:
			return response13(messages[12])
		elif len(messages) == 14:
			return response14(messages[13])
		else:
			messages.clear()
			feelings.clear()
			return "Sorry, I don't understand this yet. Please let's try again. How are you feeling?"


	API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
	API_TOKEN = "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"
	headers = {"Authorization": f"Bearer {API_TOKEN}"}


	list = query(msg)
	print(messages)
	print("Bot:",list)
	info = json.dumps(sorting(list))
	print(messages)


	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("""INSERT INTO Messages (SenderId, Message) VALUES (?,?)""",
		(session['email'] , msg,))
	cur.execute("""INSERT INTO Messages (SenderId, Message) VALUES (?,?)""",
		("Bot", info,))
	con.commit()

	return info

@app.route("/home")
def home():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT Name FROM Users WHERE Email == ? ",(session['email'],))
	name = cur.fetchone()[0]
	global messages
	global feelings
	messages = []
	feelings = []
	#print(messages)
	#print(feelings)
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute("SELECT Message FROM Messages WHERE SenderId == ? OR SenderId ==?",(session['email'], "Bot",))
	rows = (cur.fetchall())
	history = []
	if len(rows) != 0:
		for i in rows:
			history.append(i)
		print(history)
		return render_template("home.html", name = name, history = history)
	else:
		return render_template("home.html", name = name)
@app.route('/account', methods=['GET', 'POST'])
def account():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	user = session['email']
	status = ""
	if request.method == 'POST':
		email = request.form['email']
		username = request.form['username']
		old_password = request.form['old_password']
		new_password = request.form['new_password']

		# check if old password is correct
		cur.execute('SELECT Password FROM Users WHERE Email=?', (user,))
		db_password = cur.fetchone()[0]
		en = old_password.encode()
		h = hashlib.sha256(en)
		old_password = h.hexdigest()
		if old_password != db_password:
			status = "error"
			return redirect(url_for('account', status = status))

		# update email and username
		cur.execute('UPDATE Users SET Email=?, Name=? WHERE Email=?', (email, username, user))

		# update password
		if new_password:
			cur.execute('UPDATE Users SET Password=? WHERE Name=?', (new_password, name))

		con.commit()

		# redirect to account page to show updated information
		return redirect(url_for('account', status = status))

	# get user info to display on account page
	cur.execute('SELECT Email, Name FROM Users WHERE Email=?', (user,))
	user_info = cur.fetchone()

	return render_template('account.html', user_info=user_info, status=request.args.get('status'))


@app.route("/db")
def db():
	con = sqlite3.connect("login.db")
	cur = con.cursor()
	try:
		cur.execute("""
		CREATE TABLE Users(
		Name VARCHAR(50) NOT NULL, Email VARCHAR(50) NOT NULL PRIMARY KEY,
	Password VARCHAR(20) NOT NULL)
		""")
		cur.execute("PRAGMA foreign_keys = 1")
		cur.execute("""
		CREATE TABLE Messages (MessageId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		SenderId VARCHAR(50) NOT NULL REFERENCES Users(Email),
		Message VARCHAR(200) NOT NULL, DateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)  """)
	except sqlite3.OperationalError as e:
		return str(e)
	return "tables created"

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
	cur.execute("SELECT Message FROM Messages WHERE SenderId = ?",(session['email'],))
	rows = cur.fetchall()
	return str(rows)

@app.route('/alter')
def alter():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute(	"""	ALTER TABLE Messages
						ADD DateTime INTEGER AUTOINCREMENT NOT NULL DEFAULT CURRENT_TIMESTAMP
			""")
	con.commit()
	return 'alter'
