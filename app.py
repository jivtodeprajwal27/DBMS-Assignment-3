# from flask import Flask, render_template, request, redirect, session, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
# #from flaskext.mysql import MySQL


# app = Flask(__name__)
# #app = Flask(__name__, template_folder='template')

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/maintenance_portal'
# #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# app.secret_key = 'your secret key'
 
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'maintenance_portal'

# mysql = MySQL(app)

# # def login():
# #     msg = ''
# #     if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
# #         email_id = request.form['emial_id']
# #         password = request.form['password']
# #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# #         cursor.execute('SELECT * FROM user WHERE email_id = % s AND password = % s', (email_id, password, ))
# #         account = cursor.fetchone()
# #         if account:
# #             session['loggedin'] = True
# #             session['id'] = account['id']
# #             session['username'] = account['username']
# #             msg = 'Logged in successfully !'
# #             return render_template('home.html', msg = msg)
# #         else:
# #             msg = 'Incorrect username / password !'
# #     return render_template('index123.html', msg = msg)
 



# # @app.route('/logout')
# # def logout():
# #    session.pop('loggedin', None)
# #    session.pop('id', None)
# #    session.pop('username', None)
# #    return redirect(url_for('login'))

# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'User_id' in request.form and 'Name' in request.form and 'Email_id' in request.form and 'Contact_no' in request.form and 'password' in request.form and 'confirm_password' in request.form:
#         username = request.form['User_id']
#         email_id = request.form['Email_id']
#         name = request.form['Name']
#         contact_no = request.form['Contact_no']

#         password = request.form['password']
        
#         confirm_password = request.form['confirm_password']
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM user WHERE email_id = % s', (email_id, ))
#         account = cursor.fetchone()
#         if account: 
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#         elif password != confirm_password:
#             msg = 'Password does not match !'
#         else:
#             cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (username, email_id,name,contact_no,password, ))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('index123.html', msg = msg)


 
    
# if __name__ == "__main__":
#     # app.run(host ="localhost", port = int("5000"))
#     app.run(debug=True)












from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from mysql.connector import connect
import yaml

app = Flask(__name__)

db=yaml.safe_load(open('db.yaml'))


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'maintenance_portal'
# def get_db():
#     conn = connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="maintenance_portal"
#     )

#     return conn


mysql = MySQL(app)

# by soumya
@app.route('/test_guest', methods =['GET', 'POST'])
def test_guest():
	return render_template('test_guest.html')

@app.route('/test_hostel', methods =['GET', 'POST'])
def test_hostel():
	return render_template('test_hostel.html')

@app.route('/test_housing', methods =['GET', 'POST'])
def test_housing():
	return render_template('test_housing.html')

@app.route('/test_specific', methods =['GET', 'POST'])
def test_specific():
	return render_template('test_specific.html')

@app.route('/home', methods =['GET', 'POST'])
def home():
	return render_template('home.html')





@app.route('/', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		username = request.form['Email_id']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM user WHERE email_id = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			msg = 'Logged in successfully !'
			return home()
		else:
			msg = 'Incorrect username / password !'
	return render_template('index123.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST':
		user_details = request.form
		user_type= user_details['User_Type']
		user_id = user_details['User_id']
		email_id = user_details['Email_id']
		name = user_details['Name']
		contact_no = user_details['Contact_no']
		password = user_details['password']
		confirm_password = user_details['confirm_password']
		

		'''if password != confirm_password:
			msg = 'Password does not match !'
'''
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE email_id = % s', (email_id, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', name):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO user(email_id,name,contact_no,password ) VALUES(%s,%s,%s,%s)', ( email_id,name,contact_no,password, ))
			if user_type == 'Employee':
				cursor.execute('INSERT INTO employee(employee_no, email_id) VALUES(%s,%s)', (user_id, email_id))

			else:
				cursor.execute('INSERT INTO student(roll_no, email_id) VALUES(%s,%s)', (user_id, email_id))
			mysql.connection.commit()
		msg = 'You have successfully registered !'
		cursor.close()
		return redirect('/')
	#elif request.method == 'POST':
	#	msg = 'Please fill out the form !'
	return render_template('index123.html')




# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route("/index")
# def index():
# 	if 'loggedin' in session:
# 		return render_template("index.html")
# 	return redirect(url_for('login'))


# @app.route("/display")
# def display():
# 	if 'loggedin' in session:
# 		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
# 		account = cursor.fetchone()
# 		return render_template("display.html", account = account)
# 	return redirect(url_for('login'))

# @app.route("/update", methods =['GET', 'POST'])
# def update():
# 	msg = ''
# 	if 'loggedin' in session:
# 		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
# 			username = request.form['username']
# 			password = request.form['password']
# 			email = request.form['email']
# 			organisation = request.form['organisation']
# 			address = request.form['address']
# 			city = request.form['city']
# 			state = request.form['state']
# 			country = request.form['country']
# 			postalcode = request.form['postalcode']
# 			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 			cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
# 			account = cursor.fetchone()
# 			if account:
# 				msg = 'Account already exists !'
# 			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 				msg = 'Invalid email address !'
# 			elif not re.match(r'[A-Za-z0-9]+', username):
# 				msg = 'name must contain only characters and numbers !'
# 			else:
# 				cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
# 				mysql.connection.commit()
# 				msg = 'You have successfully updated !'
# 		elif request.method == 'POST':
# 			msg = 'Please fill out the form !'
# 		return render_template("update.html", msg = msg)
# 	return redirect(url_for('login'))

if __name__ == "__main__":
	# app.run(host ="localhost", port = int("5000"))
	app.run(debug=True)





# from flask import Flask, render_template, request, redirect, session, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
# #from flaskext.mysql import MySQL


# app = Flask(__name__)
# #app = Flask(__name__, template_folder='template')

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/maintenance_portal'
# #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# app.secret_key = 'your secret key'
 
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'maintenance_portal'

# mysql = MySQL(app)

# # def login():
# #     msg = ''
# #     if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
# #         email_id = request.form['emial_id']
# #         password = request.form['password']
# #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# #         cursor.execute('SELECT * FROM user WHERE email_id = % s AND password = % s', (email_id, password, ))
# #         account = cursor.fetchone()
# #         if account:
# #             session['loggedin'] = True
# #             session['id'] = account['id']
# #             session['username'] = account['username']
# #             msg = 'Logged in successfully !'
# #             return render_template('home.html', msg = msg)
# #         else:
# #             msg = 'Incorrect username / password !'
# #     return render_template('index123.html', msg = msg)
 



# # @app.route('/logout')
# # def logout():
# #    session.pop('loggedin', None)
# #    session.pop('id', None)
# #    session.pop('username', None)
# #    return redirect(url_for('login'))

# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'User_id' in request.form and 'Name' in request.form and 'Email_id' in request.form and 'Contact_no' in request.form and 'password' in request.form and 'confirm_password' in request.form:
#         username = request.form['User_id']
#         email_id = request.form['Email_id']
#         name = request.form['Name']
#         contact_no = request.form['Contact_no']

#         password = request.form['password']
        
#         confirm_password = request.form['confirm_password']
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM user WHERE email_id = % s', (email_id, ))
#         account = cursor.fetchone()
#         if account: 
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#         elif password != confirm_password:
#             msg = 'Password does not match !'
#         else:
#             cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (username, email_id,name,contact_no,password, ))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('index123.html', msg = msg)


 
    
# if __name__ == "__main__":
#     # app.run(host ="localhost", port = int("5000"))
#     app.run(debug=True)










