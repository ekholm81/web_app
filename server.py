from flask import Flask, app, request
import database_helper
import sqlite3
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/signup',  methods=['POST'])
def signup():
	if request.method == 'POST':
		database_helper.add_user("mangge@mail.se","passs", "magnus", "qvig", "m","lkpg", "sweden")
		return json.dumps({'success' : True, 'message' : 'Signup successful'})

@app.route("/signin", methods=["POST"])
def signin():
	if request.method == 'POST':
		print database_helper.get_user_by_email("mange@mail.se")
	return json.dumps({'success' : True, 'message' : 'Signin successful'})

if __name__ == '__main__':
	#database_helper.init_db(app)
	app.debug = True
	app.run()

