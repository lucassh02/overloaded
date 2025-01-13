from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Workout_Sessions, Exercises, Exercise_Log, Routines, Routine_Exercises
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Disables the modification tracking system to save memory.
# It is recommended to disable it unless you need to use it.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SESSION_PERMANENT determines if the session should be permanent or not.
app.config['SESSION_PERMANENT'] = False
# Specifies the type of session interface to use. 'filesystem' stores session data on the file system.
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False


Session(app)

# The database URI that specifies the database to be used for the application
db.init_app(app)

# Create all the tables in the database
with app.app_context():
    db.create_all()

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required


