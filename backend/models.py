from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    

    def __repr__(self):
        return f'<User {self.username}>'
    
class Workout_Sessions(db.Model):
    __tablename__ = 'workout_sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Workout_Sessions {self.id}>'
    
class Exercises(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(50), nullable=False)
    #how to make this only a list of certain values
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Exercises {self.name}>'
    
class Exercise_Log(db.Model):
    __tablename__ = 'exercise_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    rpe = db.Column(db.Integer)

    def __repr__(self):
        return f'<Exercise_Log {self.id}>'
    
class Routines(db.Model):
    __tablename__ = 'routines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Routines {self.name}>'
    
class Routine_Exercises(db.Model):
    __tablename__ = 'routine_exercises'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    exercise_order = db.Column(db.Integer, nullable=False)
    
    #only connsidering "asigning sets, reps, and weight to a routine" as a future feature
    #sets = db.Column(db.Integer, nullable=False)
    #reps = db.Column(db.Integer, nullable=False)
    #weight = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    #rpe = db.Column(db.Integer)

    def __repr__(self):
        return f'<Routine_Exercises {self.id}>'