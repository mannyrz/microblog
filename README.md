microblog:

Objective of this little project is to demostrate some simple testing techinces 
i.e,  Python Tavern,  Python Selenium, Java Selenium, other test plateforms TBD

The project uses a very simple web service running on flask
 - API 
	Routes: /, /login, /adduser
 
 - WEB
	localhost:5000

It uses a mysql databases  

Uses python3 virturals enviorments*
*** NOTE ***
		Make sure you run everything from within the proper directory and evniroments

======================================================
Start
======================================================

To start:
     Start MYSQL
	 mysql.server start
	 mysql -u root -p        (return will promot for password, use same)	
     Env run:
		source ~/.virtualenvs/microblog/bin/activate
		source ~/.virtualenvs/microblogTest/bin/activate
    
	Set Debug:
		export FLASK_DEBUG=1

	Run Flask:
		Flask run
	
	Verify Flash:	
		from a Chrome browser tyep localhost:5000/
		expect the login page to load

======================================================
Test Python Tavern
======================================================

1) To TEST using Python Tavern
	Start a new terminal 
	cd to the microblog directoy
	source microblog venv (source ~/.virtualenvs/microblog/bin/activate)
        run:
		 pytest ./tests/test_helloWorld.tavern.yaml -vv

Note:
Test are defined in the mircoblog, flask root directoy
	~/dev/py/microblog/tests

======================================================
Test Python Selenium
======================================================

2) To Test using Python Selenium
	DIR:        /Users/mrodriguez/dev/py/microblogSeleniumTest

	Open a new terminal and source microblogTest
		source ~/.virtualenvs/microblogTest/bin/activate
	Run:
		python seleniumTest.py
  	