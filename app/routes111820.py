from app import app
from flask import Flask, render_template, request, session, jsonify
from flask_mysqldb import MySQL
from app import db

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

	if request.method == 'POST':
		details   = request.form
		userName  = details['User_Name']
		password  = details['password']

		// db look up user
		tmp = vlg.validateLogIn(userName, password, mysql)
		dbList=tmp	
		if dbList is None:
			loginSuccess = False	
		else:
			loginSuccess = validateLogin(dbList, userName, password)
			if loginSuccess:
				print("Login Successful!")
				print(dbList)
			else:
				loginSuccess = False
				print("Error: DB login Failure")

		if loginSuccess:
			acct = dbList[0] 
			session['loggedin'] = True
			session['key']      = randomString(10)
			session['username'] = userName
			session['uid']      = password
			session['acct']	    = acct	
			if acct == 'usr':
				return 'TEST User * {} * Logged In, Session ID = {}, UID = {}'.format(userName, session['key'], session['uid'])
			elif acct == 'adm':
				return 'TEST Admin * {} * Logged In, Session ID = {}, UID = {}'.format(userName, session['key'], session['uid'])		
			else:
				return 'Error on getting account type for user'
		else:
			return 'Error on getting creditials'					
	return render_template('login.html')
	#return 'success = {},  {}, {}, {}'.format(success, acct, uid, userName)
	#return "Login Page"

@app.route('/api/v1/login', methods=['GET'])
def ApIlogin():

	response = [
    {'id': 0,
     'Test': 'A Fire Upon the Deep'
	 } ]
	#print(request.get_query_string())
	TEST_username = request.args.get('username', None)
	TEST_password = request.args.get('password', None)
	print(TEST_username)
	print(TEST_password)
	return jsonify(response)

# @app.route('/adduser', methods=['GET', 'POST'])
# def adduser():
# 	if request.method == 'POST':
# 		details   = request.form
# 		acct      = details['perm']
# 		firstName = details['First_Name']
# 		lastName  = details['Last_Name']
# 		userName  = details['User_Name']
# 		email     = details['email']
# 		password  = details['password']
# 		cur = mysql.connection.cursor()
# 		cur.execute("INSERT INTO Users(User_Id, Perm, First_Name, Last_Name, User_Name, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (0, acct, firstName, lastName, userName, email, password))
# 		mysql.connection.commit()
# 		cur.close()
# 		return 'success'
# 	return render_template('adduser.html')
# 	#return "Not Real World, but tests a micro world"

@app.route('/bye')
def bye():
	return "Bye-Bye"

def validateLogin(dbEntry, userName, password): 
	
	loginSuccessful = False
	if len(dbEntry) == 0:
		loginSuccessful = False
	else:
		if dbEntry[2] == userName and dbEntry[3] == password:
			loginSuccessful = True
		else:
			loginSuccessful = False
	return loginSuccessful	

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))