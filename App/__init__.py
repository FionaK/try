from flask import Flask, Blueprint

app = Flask(__name__)
app.secret_key = 'fifi'

from users.views import users_blueprint
"""from questions.views import questions_blueprint"""

app.register_blueprint(users_blueprint)
"""app.register_blueprint(questions_blueprint)"""
