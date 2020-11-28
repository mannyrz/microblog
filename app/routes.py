from app import app
from flask import Flask, render_template, request, session, jsonify
from flask_mysqldb import MySQL
from app import db
import json

import random
import string

#Database creditentials
app.config['MYSQL_HOST'] 		= 'localhost'
app.config['MYSQL_USER'] 		= 'root'
app.config['MYSQL_PASSWORD'] 	= 'password'
app.config['MYSQL_DB'] 			= 'videodb'

mysql = MySQL(app)
vlg = db.SQLblogOps()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login(): 
	
	dbList=[]
	loginSuccess = False

	# Get users creditentials from web page
	if request.method == 'POST':
		details   = request.form
		userName  = details['User_Name']
		password  = details['password']

		# Validate Users Creditials
		dbList = validateCreditials(userName, password)
		loginSuccess = dbList[0]
		
		print(dbList)
		
		# Register user with current session
		if loginSuccess:
			return render_template('logInSuccess.html', role=dbList[1], usr = userName)		
		else:
			return 'Error on getting creditials'					
	return render_template('login.html')	

# Get users creditentials from web page
@app.route('/api/v1/login', methods=['GET'])
def APIlogin():
	
	userName = request.args.get('username', None)
	password = request.args.get('password', None)

	# Validate Users Creditials
	dbList = validateCreditials(userName, password)
	loginSuccess = dbList[0]

	if loginSuccess:
		response = json.dumps({'success': 'True', 'status': '200', 'ContentType': 'application/json', 'id': dbList[1], 'username': dbList[3]})
		return response
	else:
		return 'Error on getting creditials'

# Add Boxer via HTML post 	
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
	if request.method == 'POST':
		details   = request.form
		acct      = details['perm']
		firstName = details['First_Name']
		lastName  = details['Last_Name']
		userName  = details['User_Name']
		email     = details['email']
		password  = details['password']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Users(User_Id, Perm, First_Name, Last_Name, User_Name, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (0, acct, firstName, lastName, userName, email, password))
		mysql.connection.commit()
		cur.close()
		return 'success'
	return render_template('adduser.html')
	#return "Not Real World, but tests a micro world"

# Add Boxer via JSON post or Command line agrs 
@app.route('/api/v1/adduser', methods=['POST'])
def APIadduser():
	req = request.get_json()
	acct     	= req['perm']
	firstname   = req['firstname']
	lastname   	= req['lastname']
	username 	= req['username']
	email   	= req['email']
	password 	= req['password']

	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO Boxer(User_Id, Perm, First_Name, Last_Name, User_Name, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (0, acct, firstname, lastname, username, email, password))
	mysql.connection.commit()
	cur.close()
	return json.dumps({'success': 'True', 'status': 201, 'ContentType':'application/json'}) 

@app.route('/bye')
def bye():
	return "Bye-Bye"
# # # # # # # # #
def	validateCreditials(userName, password):
	dbList = []
	# verify db creditials
	tmp = vlg.validateLogIn(userName, password, mysql)
	if tmp is None:
		#dbList=list(tmp)
		print()
		loginStatus = False	
	else:
		dbList=list(tmp)
		loginStatus = validateUserID(dbList, userName, password)
		if loginStatus:
			print("Login Successful!")
		else:
			loginStatus = False
			print("Error: DB login Failure")
	dbList.insert(0,loginStatus)		
	return dbList

def validateUserID(dbList, userName, password): 
	
	loginSuccessful = False
	if len(dbList) == 0:
		loginSuccessful = False
	else:
		if dbList[2] == userName and dbList[3] == password:
			loginSuccessful = True
		else:
			loginSuccessful = False
	return loginSuccessful	

def registerUserLogin(dbList):
		
	session['loggedin'] = True
	session['key']      = randomString(10)
	session['username'] = dbList[3]
	session['uid']      = dbList[2]
	session['acct']     = dbList[1]
	return 	session['key']
			

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))