from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute(" INSERT INTO user (username, password) VALUES (?,?)",
                    (request.form['un'],request.form['pw']))
    return 'Hello ' + request.form['un']
# request.args.get gets the argument 'un' from the html
# request.form is if you use methods near /signup to hide the data

@app.route('/login', methods=['POST'])
def login():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute(" INSERT INTO user (username, password) VALUES (?,?)",
                    (request.form['un'],request.form['pw']))
    return 'Hello ' + request.form['un']
    
@app.route('/create')
def create():
    con = sqlite3.connect('login.db')
    #cursor is an object that provides facility to write SQL. dont pay attention doesnt make sense
    cur = con.cursor()
    cur.execute(""" CREATE TABLE user(
                    username VARCHAR(20) NOT NULL PRIMARY KEY,
                    password VARCHAR(20) NOT NULL)
                """)
                #TRIPLE QUOTES ALLOWS TO WRITE SQL IN FEW LINES
    return 'table created'


@app.route('/insert')
def insert():
    con = sqlite3.connect('login.db')
    #cursor is an object that provides facility to write SQL. dont pay attention doesnt make sense
    cur = con.cursor()
    cur.execute(""" INSERT INTO user (username, password)
                    VALUES ('anfy', '3456')
                """)
    con.commit()
    return 'insert'

@app.route('/select')
def select():
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute(" SELECT * FROM user ")
    rows = cur.fetchall()
    #fetchall means send the command "SELECT *..." to the database and return the result
    return str(rows)
