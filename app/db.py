
# from app import app
# from flask import Flask, render_template, request, session
# from flask_mysqldb import MySQL

class SQLblogOps:
    
    def validateLogIn(self, userName, password, mysql):

        userQL=[]

        cur = mysql.connection.cursor()
        sq = "SELECT PERM, USER_ID, USER_NAME, PASSWORD  FROM users WHERE user_name = %s"
        success = cur.execute(sq, (userName,))
        try:
            userQL = cur.fetchone()
            mysql.connection.commit()
        except TypeError as e:
            print(e)
            return 'Database connection Error'
        finally:	
            cur.close()
        return userQL