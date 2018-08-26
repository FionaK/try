from flask import Flask, Blueprint, jsonify, request
from App.models import *
from functools import wraps
import datetime
import jwt
from __init__ import *

questions_blueprint = Blueprint('questions', __name__)
def require_auth(k):
	@wraps(k)
	token = request.headers.get('x-access-token')
	if not token:
		return jsonify({'message' : 'Missing Token'}), 403
	try:
		data = jwt.decode(token, 'fifi')
	except:
		return jsonify({'message' : 'Invalid Token'}), 408
	return k(*args, **kwargs)
return authorization

@questions_blueprint.route('/api/v1/ask_question/', methods=['POST'])
@require_auth
def ask_question():
	try:
		question = request.get_json()['question'].strip()
		data = jwt.decode(request.headers.get('x-access_token'), 'fifi')
		username = data['user']
		cur.execute("INSERT INTO question(question)VALUES(%s, %s);",(question))
		conn.commit()
		return jsonify({'message': 'New entry has been created'}), 200
	except KeyError:
		return jsonify({'message':'Field can not be blank or check on the field spelling'}), 406

@questions_blueprint.route('/api/v1/display_question/', methods=['GET'])
@require_auth
def display_question():
	cur.execute("SELECT * FROM questions WHERE username = '"+username+"'" )
	questions=cur.fetchall()
	return jsonify(questions), 200

@questions_blueprint.route('/api/v1/single_question/<int:questionid>', methods= ['GET'])
@require_auth
def single_question(questionid):
	data = jwt.decode(request.headers.get('x-access_token'), 'fifi')
	username = data['user']
	cur.execute("SELECT * FROM questions WHERE questid='"+str(questid)+"'")
	question=cur.fetchone()
	conn.commit()
	return jsonify(question), 200

@questions_blueprint.route('/api/v1/delete_question/', methods=['DELETE'])
@require_auth
def delete_question():
