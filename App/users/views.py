from flask import Flask, Blueprint, jsonify, request
from App.models import *
import datetime
import jwt
import re
import base64

users_blueprint=Blueprint('users', __name__)
	
def valid_password(password):
	if not re.match(r'^(?=\S{6,25}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',password):
		return jsonify({'message':'False'})
	else:
		return jsonify({'message':'True'})
def valid_email(email):
	if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
		return True
	return False
@users_blueprint.route('/api/v1/signup/', methods= ['POST'])
def signup():
	try:
		name=request.get_json()['name'].strip()
		username=request.get_json()['username'].strip()
		password=base64.b64encode(bytes(request.get_json()['password'])).strip()
		rpt_password=base64.b64encode(bytes(request.get_json()['repeat_password'])).strip()
		email=request.get_json()['email'].strip()
		if len(name)==0 or len(email)==0:
			return jsonify({'message':'This field can not be empty!'}), 406
		if len(password)<6:
			return jsonify({'message':'Try again! Password should be 6 characters or more'}), 406
		if len(username)<4:
			return jsonify({'message': 'Try again! Username should be 4 characters or more'}), 406
		if password != rpt_password:
			return jsonify({'message':'Password do not match. Try again!'}), 403
		else:
			cur.execute("SELECT * FROM users WHERE username = '"+username+"' OR email = '"+email+"'")
			if cur.fetchone() is None:
				if valid_password(password):
					if valid_email(email):
						cur.execute("INSERT INTO users(name,username,password,email)VALUES(%s, %s, %s, %s);",(name, username, password, email))
					else:
						return jsonify({'message':'invalid email format'}), 417
				else:
					return jsonify({'message':'Try again! Password must contain upper/lower case letters and numbers'}), 417
			else:
				return jsonify({'message':'username or email already taken'}), 409
		conn.commit()
		return jsonify({'message': 'You are successfully registered'})
	except KeyError():
		return jsonify({'message':'Field can not be blank or check on the spelling'}), 406

@users_blueprint.route('/api/v1/login/', methods= ['POST'])
def login():
	try:
		username=request.get_json()['username'].strip()
		password=base64.b64encode(bytes(request.get_json()['password'])).strip()
		cur.execute("SELECT COUNT(1) FROM users WHERE username = '"+username+"'")
		if cur.fetchone() is not None:
			cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
			for row in cur.fetchall():
				if password == row[3]:
					token= jwt.encode ({'user':username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, 'fifi')
					return jsonify({'message': 'Login successful', 'x-access_token': token.decode('UTF-8')}), 200
				return jsonify({'message':'wrong password'}), 400
		return jsonify({'message':'Invalid username'}), 401
	except KeyError():
		return jsonify({'message':'Field can not be blank or check on the spelling'}), 406
