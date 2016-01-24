import sqlite3 as sq
import flask as f
#Database tables: users, logged_in_users, messages
def connect():
	return sq.connect("../database.db");

def get_db():
	db=getattr(f,'db',None);
	if db is None:
		db=f._database=connect();
	return db

def close_db():
	db=getattr(f,'db',None)
	if db is not None:
		db.close();

def init_db(app):
	with app.app_context():
		db = get_db()
		with app.open_resource('database.schema', mode='r') as fi:
			db.cursor().executescript(fi.read())
		db.commit()

def add_user(mail,pwd,fname,lname,sex,city,country):
	con=connect()
	cur=con.cursor()
	try:
		con.execute('''INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)''',[mail,pwd,fname,lname,sex,city,country])
		con.commit()
	except Exception,e:
		print "______"+str(e)
		return False
	return True

def get_email_by_token(token):
	con = connect()
	cur = con.cursor()
	token=(token,)
	try:
		cur.execute('''SELECT email FROM logged_in_users WHERE token=?''', token)
		res = cur.fetchone()
		return res[0]
	except Exception,e:
		print "______"+str(e)
		return False
	
def is_user_logged_in_token(token):
	con=connect()
	cur=con.cursor()
	token=(token,)
	try:
		cur.execute('''SELECT EXISTS(SELECT * FROM logged_in_users WHERE token=?)''', token)
	except Exception,e:
		print "______"+str(e)
		return False
	if cur.fetchone()[0] == 1:
		return True
	return False

def is_user_logged_in_email(email):
	con=connect()
	cur=con.cursor()
	email=(email,)
	try:
		cur.execute('''SELECT EXISTS(SELECT * FROM logged_in_users WHERE email=?)''', email)
	except Exception,e:
		print "______"+str(e)
		return False
	if cur.fetchone()[0] == 1:
		return True
	return False
    
def signin_user(email,token):
	con=connect()
	cur=con.cursor()
	data=(token,email)
	try:
		con.execute('''INSERT INTO logged_in_users VALUES(?, ?)''', data)
		con.commit()
		return True
	except Exception,e:
		print "______"+str(e)
		return False
		
def signout_user(token):
	con=connect()
	cur=con.cursor()
	token = (token,)
	try:
		con.execute('''DELETE FROM logged_in_users WHERE token=?''', token)
		con.commit()
		return True
	except:
		return False
		
def update_pass(email,new_pwd):
	con=connect()
	cur=con.cursor()
	try:
		cur.execute('''UPDATE users SET password=? WHERE email=?''',(new_pwd,email))
		con.commit()
		return True
	except Exception,e:
		print "______"+str(e)
		return False
 
def get_password(email):
	con=connect()
	cur=con.cursor()
	email=(email,)
	try:
		cur.execute('''SELECT password FROM users WHERE email=?''', email)
		res=cur.fetchone()
		return res[0]
	except Exception,e:
		print "______"+str(e)
		return False
		
def get_user_data_by_token(token):
	con=connect()
	cur=con.cursor()
	email=(get_email_by_token(token),)
	try:
		cur.execute('''SELECT * FROM users WHERE email=?''', email)
		res=list(cur.fetchone())
		return res
	except Exception,e:
		print "______"+str(e)
		return False

def is_user(email):
	con=connect()
	cur=con.cursor()
	email=(email,)
	try:
		cur.execute('''SELECT EXISTS(SELECT * FROM users WHERE email=?)''',email)
	except Exception,e:
		print "______"+str(e)
		return False
	if cur.fetchone()[0] == 1:
		return True
	return False

def get_user_data_by_email(email):
	con=connect()
	cur=con.cursor()
	email=(email,)
	try:
		cur.execute('''SELECT * FROM users WHERE email=?''', email)
		res=list(cur.fetchone())
		return res
	except Exception,e:
		print "______"+str(e)
		return False
		
def messages_by_email(email):
	con=connect()
	cur=con.cursor()
	email=(email,)
	try:
		cur.execute('''SELECT message FROM posts WHERE rec=?''',email)
	except Exception,e:
		print "______"+str(e)
		return False
	res= cur.fetchall()
	msg=[]
	for i in res:
		msg.append(i)
	return msg

def messages_by_token(token):
	con=connect()
	cur=con.cursor()
	email=(get_email_by_token(token),)
	try:
		cur.execute('''SELECT message FROM posts WHERE rec=?''',email)
	except Exception,e:
		print "______"+str(e)
		return False
	res= cur.fetchall()
	msg=[]
	for i in res:
		msg.append(i)
	return msg

def post_msg(s_email,r_email,text):
	con=connect()
	cur=con.cursor()
	try:
		cur.execute('''INSERT INTO posts VALUES (?, ?, ?)''',(s_email,r_email,text))
		con.commit()
		return True
	except Exception,e:
		print "______"+str(e)
		return False	
		
def close_db():
	get_db.close()
