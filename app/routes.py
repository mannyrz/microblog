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


	# HTTP: Get users creditentials from web page
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


# API: Get users creditentials
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


# HTTP: Add Boxer via HTML post 	
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
	success = False

	if request.method == 'POST':
		print("******** test **************")
		details   = request.form
		#print(type(details))
		#print(details)

		# TODO:		
		# accountNumber  = details['password']

		boxerDetails = getApiBoxerDetials(details)
		print(boxerDetails)
		
		success = vlg.postBoxerData(boxerDetails, mysql)
		print(success)
		if success:
			return json.dumps({'success': 'True', 'status': 201, 'ContentType':'application/json'})
		else:
			return json.dumps({'success': 'False', 'status': 500, 'ContentType':'application/json'})
	return render_template('adduser.html')

###
# API: Add Boxer via JSON post or Command line agrs
### 
@app.route('/api/v1/adduser/', methods=['GET','POST'])
def APIadduser():
	loginSuccess = False
	#acctVal = False

	# TODO:		
	# Improve restricted access, currently use user credentials
	userName = request.args.get('username', None)
	password = request.args.get('password', None)

	print(userName)
	print(password)

	# Validate Users Creditials
	dbList = validateCreditials(userName, password)
	print(dbList)
	loginStatus = dbList[0]
	print(loginStatus)

	if loginStatus:
		req = request.get_json()
		boxerDetails = getApiBoxerDetials(req)
		
		success = vlg.postBoxerData(boxerDetails, mysql)
	else:
		success = False
		
	if success:
		return json.dumps({'success': 'True', 'status': 201, 'ContentType':'application/json'})
	else:
		return json.dumps({'success': 'False', 'status': 500, 'ContentType':'application/json'})


###
# Verify status
###
@app.route('/bye')
def bye():
	return json.dumps({'success': 'True', 'status': 201, 'ContentType':'application/json'})


# # # # # # # # # # # # # # # # # #
#	Support Fuctions
# # # # # # # # # # # # # # # # # #

def	validateCreditials(userName, password):
	dbList = []
	loginStatus = False
	# verify db creditials
	tmp = vlg.validateLogIn(userName, password, mysql)
	if tmp is None:
		#dbList=list(tmp)
		print(tmp)
		print('Validation Failed')
		loginStatus = False	
	else:
		dbList=list(tmp)
		loginStatus = validateUserID(dbList, userName, password)
		if loginStatus:
			loginStatus = True
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

def getApiBoxerDetials(req):	
	boxerDetails = []

	boxerDetails.append(req['perm'])
	boxerDetails.append(req['firstname'])
	boxerDetails.append(req['lastname'])
	boxerDetails.append(req['username'])
	boxerDetails.append(req['email'])
	boxerDetails.append(req['password'])
	return boxerDetails

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))