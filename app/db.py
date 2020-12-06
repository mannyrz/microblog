
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

    def postBoxerData(self, boxer, mysql):
        
        print("In post boxer")

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO boxers(User_Id, Perm, First_Name, Last_Name, User_Name, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (0, boxer[0], boxer[1], boxer[2], boxer[3], boxer[4], boxer[5]))
        
        try:
            print("In commit")
            mysql.connection.commit()
        except TypeError as e:
            print(e)
            print('Database connection Error')
            return False
        finally:	
            cur.close()
        print(True)
        return True