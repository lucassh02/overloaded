from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Workout_Sessions, Exercises, Exercise_Log, Routines, Routine_Exercises

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///overloaded.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

