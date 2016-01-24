from flask import Flask, app, request
import database_helper as dh
import sqlite3
import json
import string
import random

app = Flask(__name__)


def gen_tok(size=16, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def hello_world():
    return 'Hello World!'	

@app.route("/sign_in",methods=['POST'])
def sign_in():
	email=request.args.get("email")
	password=request.args.get("password")
	if request.method == 'POST':
		if dh.is_user(email)==False:
			return json.dumps([{'success': False, 'message': "No user with specifyed email"}])
		if dh.is_user_logged_in_email(email)==True:
			return json.dumps([{'success': False, 'message': "User already signed in"}])
		cpass=dh.get_password(email)
		if cpass==password:
			token=gen_tok()
			dh.signin_user(email,token)
			return json.dumps([{'success': True, 'message': "User successfully singed in!",'token': token}])
		return json.dumps([{'success': False, 'message': "Wrong password"}]) 

@app.route("/sign_up",methods=['POST'])
def sign_up():
	email     =request.args.get("email")
	password  =request.args.get("password")
	firstname =request.args.get("firstname")
	familyname=request.args.get("familyname")
	gender    =request.args.get("gender")
	city      =request.args.get("gender")
	country   =request.args.get("country")
	if request.method == 'POST':
		if dh.is_user(email)==True:
			return json.dumps([{'success': False, 'message': "User exists"}])
		dh.add_user(email,password,firstname,familyname,gender,city,country)
		return json.dumps([{'success': True, 'message': "User added!"}])

@app.route("/sign_out",methods=["POST"])
def sign_out():
	token=request.args.get("token")
	if request.method == 'POST':
		if dh.is_user_logged_in_token(token)==True:
			dh.signout_user(token)
			return json.dumps([{'success': True, 'message': "User Signed out!"}])
		return json.dumps([{'success': False, 'message': "No such user is signed in"}])

@app.route("/change_password",methods=["POST"])
def change_password():
	email=dh.get_email_by_token(request.args.get("token"))
	old=request.args.get("old_password")
	new=request.args.get("new_password")
	if request.method == 'POST':
		if dh.is_user_logged_in_email(email)==True:
			if dh.get_password(email)==old:
				dh.update_pass(email,new)
				return json.dumps([{'success': True, 'message': "Password changed"}])
			return json.dumps([{'success': False, 'message': "Wrong password"}])
		return json.dumps([{'success': False, 'message': "User not signed in"}])

@app.route("/get_user_data_by_token",methods=["GET"])
def get_user_data_by_token():
	token=request.args.get("token")
	if request.method == 'GET':
		if dh.is_user_logged_in_token(token)==True:	
			data=dh.get_user_data_by_token(token)
			data.pop(1)
			return json.dumps([{'success': True, 'message': "Success",'data': tuple(data)}])
		return json.dumps([{'success': False, 'message': "User not signed in"}])

@app.route("/get_user_data_by_email",methods=["GET"])
def get_user_data_by_email():
	email=request.args.get("email")
	token=request.args.get("token")
	if request.method == 'GET':
		if dh.is_user_logged_in_token(token)==True:
			if dh.is_user(email)==False:
				return json.dumps([{'success': False, 'message': "No such user"}])
			data=dh.get_user_data_by_email(email)
			data.pop(1)
			return json.dumps([{'success': True, 'message': "Success",'data': tuple(data)}])
		return json.dumps([{'success': False, 'message': "User not signed in"}])

@app.route("/get_user_messages_by_token",methods=["GET"])
def get_user_messages_by_token():
	token=request.args.get("token")
	if request.method == 'GET':
		if dh.is_user(dh.get_email_by_token(token))==False:
			return json.dumps([{'success': False, 'message': "No such user"}])
		return json.dumps([{'success': True, 'message': "Success",'data':dh.messages_by_token(token)}]) 

@app.route("/post_message",methods=["POST"])
def post_message():
	email=request.args.get("email")
	token=request.args.get("token")
	mess =request.args.get("message")
	if request.method == 'POST':
		if dh.is_user_logged_in_token(token)==False:
			return json.dumps([{'success': False, 'message': "Not signed in"}])
		if dh.is_user(email)==False:
			return json.dumps([{'success': False, 'message': "Illegal recipient"}])
		return json.dumps([{'success': dh.post_msg(dh.get_email_by_token(token),email,mess),'message':"message sent"}])
		

if __name__ == '__main__':
	#database_helper.init_db(app)
	app.debug = True
	app.run()

