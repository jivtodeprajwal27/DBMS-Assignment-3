from flask import *
from flask_mysqldb import MySQL
from auth_decorator import login_required
import MySQLdb.cursors
import re
from mysql.connector import connect
import yaml
import uuid
from authlib.integrations.flask_client import OAuth
import random
import smtplib
from email.message import EmailMessage
app = Flask(__name__)

db=yaml.safe_load(open('db.yaml'))


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

name = ''
email_id = ''
OTP = None
to_mail = None
complaint_email=""
mysql = MySQL(app)
oauth = OAuth(app)


@app.route('/test_guest', methods =['GET', 'POST'])
@login_required
def test_guest():
	return render_template('test_guest.html')

@app.route('/test_hostel', methods =['GET', 'POST'])
@login_required
def test_hostel():
	return render_template('test_hostel.html')

@app.route('/test_housing', methods =['GET', 'POST'])
@login_required
def test_housing():
	return render_template('test_housing.html')

@app.route('/test_specific', methods =['GET', 'POST'])
@login_required
def test_specific():
	return render_template('test_specific.html')

@app.route('/home', methods =['GET', 'POST'])
@login_required
def home():
	print(session)
	return render_template('home.html')
	

@app.route('/test_guest_fill', methods = ['GET','POST'])
@login_required
def test_guest_fill():
	if request.method == 'POST':
		username = request.form['username']
		# email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']	
		b_r = request.form['b_r']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		floor = request.form['floor']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),complaint_email,subject,domain,subdomain,subdomain1,'Guest House',b_r,'Always','Pending','NULL','NULL'))
		check=cursor.execute('Select * from Guest_House where Floor = %s and Room_No = %s',(floor,b_r))
		if not check:
			cursor.execute('INSERT INTO Guest_House (Floor,Room_No,Email_Id) VALUES (%s,%s,%s)',(floor,b_r,complaint_email))
		mysql.connection.commit()
		return render_template('logout.html')
	return render_template('test_guest.html')

@app.route('/test_hostel_fill', methods = ['GET','POST'])
@login_required
def test_hostel_fill():
	if request.method == 'POST':
		username = request.form['username']
		# email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']
		hostel = request.form['nh']	
		room = request.form['room']
		availability = request.form['time']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		image=['image']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),complaint_email,subject,domain,subdomain,subdomain1,hostel,room,availability,'Pending',image,'NULL'))
		check = cursor.execute('Select * from Hostel where Hostel_Name = %s and Room_No = %s',(hostel,room))
		if not check:
			cursor.execute('INSERT INTO Hostel (Hostel_Name,Room_No,Student_Email_ID) VALUES\
		 	(%s,%s,%s)', (hostel,room,complaint_email))
		mysql.connection.commit()
		cursor.close()
		return render_template('logout.html')
	return render_template('test_hostel.html')

@app.route('/test_housing_fill', methods = ['GET','POST'])
@login_required
def test_housing_fill():
	if request.method == 'POST':
		username = request.form['username']
		# email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']
		apartment = request.form['apartment']	
		corridor = request.form['corridor']
		block = request.form['Block']
		availability = request.form['availability']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		image=['image']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),complaint_email,subject,domain,subdomain,subdomain1,apartment,corridor,availability,'Pending',image,'NULL'))
		check=cursor.execute('Select * from Housing_Updated where Block_Name = %s and Apartment_No = %s',(block,apartment))
		print(check)
		if not check:
			cursor.execute('INSERT into Housing_Updated (Block_Name,Apartment_No,Email_ID)\
		 	Values (%s,%s,%s)',(block,apartment,complaint_email))
		mysql.connection.commit()
		cursor.close()
		return render_template('logout.html')
	return render_template('test_housing.html')

@app.route('/test_specific_fill', methods = ['GET','POST'])
@login_required
def test_specific_fill():
	if request.method == 'POST':
		username = request.form['username']
		# email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']
		nh = request.form['nh']	
		location = request.form['location']
		availability = request.form['availability']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		image=['image']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),complaint_email,subject,domain,subdomain,subdomain1,nh,location,availability,'Pending',image,'NULL'))
		mysql.connection.commit()
		cursor.close()
		return redirect('logout.html')
	return render_template('test_specific.html')


@app.route('/filter',methods=['Get','Post'])
@login_required
def filter():
	if request.method == 'POST':
		filter = request.form['filter']
		cursor = mysql.connection.cursor()
		print(filter)
		if filter == 'Civil':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'Electrical':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'Air-Conditioning':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'Water Cooler':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'All':
			cursor.execute('Select * from Complaint')
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)

@app.route('/', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		username = request.form['Email_id']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM User WHERE email_id = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		login = False
		if account:
			global complaint_email
			complaint_email = username
			msg = 'Logged in successfully !'
			session['user'] = username		
			print(session['user'])	
			return render_template('home.html',login=login)
		else:
			msg = 'Incorrect username / password !'
	return render_template('index123.html', msg = msg)

@app.route('/forgot_password')
def forgot_password():
	return render_template("forgot_password.html")

@app.route('/verify')
def verify():
	return render_template("verify.html")


def regError(message):
    flash(message)
    return render_template("index123.html",pageType=['register'],flashType="danger")

@app.route('/admin_page')
def admin_page():
	return render_template('Admin_page.html')


@app.route('/admin', methods = ['GET', 'POST'])
def admin():
	if request.method == 'POST':
		username = request.form['ID']
		password = request.form['password']
		print(username,password)
		if username.lower() == 'admin' and password == 'pass':
			cursor = mysql.connection.cursor()
			cursor.execute("SELECT * FROM Complaint")
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
	return render_template('admin_login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST':
		user_details = request.form
		user_type= user_details['User_Type']
		user_id = user_details['User']
		password = user_details['pas1']
		confirm_password = user_details['pas2']
		contact_no = user_details['number']

		
		global name
		global email_id
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM User WHERE email_id = % s', (email_id, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', name):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO User(Email_ID,Name,Contact_No,password ) VALUES(%s,%s,%s,%s)', ( email_id,name,contact_no,password, ))
			if user_type == 'Employee':
				cursor.execute('INSERT INTO employee(Employee_ID, Employee_Email_ID) VALUES(%s,%s)', (user_id, email_id))

			else:
				cursor.execute('INSERT INTO Student(Roll_No, Student_Email_ID) VALUES(%s,%s)', (user_id, email_id))
			mysql.connection.commit()
		msg = 'You have successfully registered !'
		cursor.close()
		return redirect('/')
	#elif request.method == 'POST':
	#	msg = 'Please fill out the form !'
	return render_template('register.html',msg=msg)

 
@app.route('/OTP', methods =["GET", "POST"])
def OTP():
	if request.method == "POST":
		user_details = request.form
		global to_mail
		to_mail = user_details['To_mail']
		#print(to_mail)
		cursor = mysql.connection.cursor()
		cursor.execute("select email_id from User where email_id = %s",(to_mail,))
		account = cursor.fetchone()
		for i in account:
			if i==to_mail:
				global OTP
				OTP=random.randrange(2000, 5000, 3)
				mail = EmailMessage()
				mail.set_content("{} is your OTP for Password Reset ".format(OTP))
				mail['Subject'] = 'Password Reset OTP'
				mail['From'] = "patidarritesh@iitgn.ac.in"
				mail['To'] = "{}".format( to_mail )
				server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				server.login("patidarritesh@iitgn.ac.in", "Patidar@143321")
				server.send_message(mail)
				server.quit()
				return render_template('new_password.html')
	return render_template("reset.html")
	return render_template("table.html")

@app.route('/new_password', methods =["GET", "POST"])
def new_password():
	if request.method == 'POST':
		global OTP
		global to_mail
		password = request.form['pas1']
		confirm = request.form['pas2']
		otp = request.form['OTP']
		print(password,confirm,otp,OTP)
		if password == confirm and int(otp)==OTP:
			cursor = mysql.connection.cursor()
			cursor.execute("Select * from User where email_id = %s",(to_mail,))
			email = cursor.fetchone()
			for i in email:
				print(i,to_mail)
				if i == to_mail:
					cursor.execute("update User Set password = %s where email_id =%s",(password,to_mail,))
					flash('hooray password changed successfully!')
					mysql.connection.commit()
					return render_template('index123.html')
				flash("Account does not exist")
				return render_template('index123.html')
	error = "Wrong OTP"
	return render_template('forgot_password.html',error = error)

@app.route('/logout', methods = ['post','get'])
def logout():
	session.pop('user')
	print(session)
	return redirect('/')



@app.route('/google',  methods =['GET', 'POST'])
def google():

	# Google Oauth Config
	# Get client_id and client_secret from environment variables
	# For developement purpose you can directly put it
	# here inside double quotes
	GOOGLE_CLIENT_ID = "14105763444-75bvq8dpckghed5kougj1q83538hdn3v.apps.googleusercontent.com"
	GOOGLE_CLIENT_SECRET = "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"
	
	CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
	oauth.register(
		name='google',
		client_id=GOOGLE_CLIENT_ID,
		client_secret=GOOGLE_CLIENT_SECRET,
		server_metadata_url=CONF_URL,
		userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
		client_kwargs={
			'scope': 'openid email profile'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/', methods =['GET', 'POST'])
def google_auth():
	token = oauth.google.authorize_access_token()
	#user = oauth.google.parse_id_token(token)
	#print(" Google User ", user)
	global name
	global email_id
	user = oauth.google.userinfo()
	name = user['name']
	email_id = user['email']
	print(user)

	return redirect('/register')


if __name__ == "__main__":
	# app.run(host ="localhost", port = int("5000"))
	app.run(debug=True)





