from flask import Flask, request, jsonify
from models import db, User, Workout_Sessions, Exercises, Exercise_Log, Routines, Routine_Exercises
from flask_cors import CORS
from flask_migrate import upgrade, Migrate 
from datetime import datetime, timedelta, timezone
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
import os
import re
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
load_dotenv()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure JWT secret key (Change this in production!)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def home():
    return {"message": "Flask API is running!"}, 200

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
USERNAME_REGEX = r'^[a-zA-Z0-9_.+-]+$'
PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d).{8,}$'

@app.before_request
def log_request_info():
    print(f"Incoming Request: {request.method} {request.url}")
    print("Headers:", dict(request.headers))
    if 'Authorization' in request.headers:
        print("Auth header:", request.headers['Authorization'])


@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"Invalid token error: {error}")
    return jsonify({
        'status': 422,
        'sub_status': 'invalid_token',
        'msg': 'Invalid token'
    }), 422

@jwt.unauthorized_loader
def missing_token_callback(error):
    print(f"Missing token error: {error}")
    return jsonify({
        'status': 422,
        'sub_status': 'missing_token',
        'msg': 'Missing token'
    }), 422

@app.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    print(f"Invalid header error: {e}")
    return jsonify({
        'status': 422,
        'sub_status': 'invalid_header',
        'msg': str(e)
    }), 422

@app.route("/test-login", methods=["POST"])
def login_test():
    data = request.json
    if data["email"] == "test@example.com" and data["password"] == "password":
        return jsonify({"access_token": "mock-jwt-token"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

def sanitize_input(data):
    """Sanitize user input by trimming whitespace and normalizing case for emails."""
    return {
        "email": data.get("email", "").strip().lower(),
        "username": data.get("username", "").strip().lower(),
        "password": data.get("password", "").strip()
    }

def validate_registration_data(email, username, password):
    """Validate registration inputs."""
    if not re.match(EMAIL_REGEX, email):
        return "Invalid email format"
    if not re.match(USERNAME_REGEX, username):
        return "Invalid username format"
    if not re.match(PASSWORD_REGEX, password):
        return "Password must be at least 8 characters long and contain at least one letter and one number"
    return None

def validate_login_data(email, password):
    """Validate login inputs."""
    if not email or not password:
        return "Email and password are required"
    if not re.match(EMAIL_REGEX, email):
        return "Invalid email format"
    return None

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = sanitize_input(request.json)

    # Validate inputs
    validation_error = validate_registration_data(data["email"], data["username"], data["password"])
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        # Check for duplicate email or username
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already in use"}), 400
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already in use"}), 400

        # Create new user
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        new_user = User(username=data["username"], email=data["email"], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500

    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        return jsonify({"error": "Unexpected server error"}), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = sanitize_input(request.json)

    # Validate inputs
    validation_error = validate_login_data(data["email"], data["password"])
    if validation_error:
        return jsonify({"error": validation_error}), 400

    # Authenticate user
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify({"access_token": access_token, "user_id": str(user.id)}), 200

'''
# Token Refresh
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=15))
    return jsonify({'access_token': new_access_token}), 200
'''

# Protected Route (Example)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': f'Hello {user.username}, you have accessed a protected route!'}), 200


@app.errorhandler(NoAuthorizationError)
def handle_no_auth_error(e):
    return jsonify({'error': 'Missing or invalid token'}), 401

@app.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    return jsonify({'error': 'Invalid token format'}), 401




@app.route('/user/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        print(f"🔍 Debug: current_user_id={current_user_id}, requested_user_id={user_id}")

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if str(current_user_id) != str(user.id):
            return jsonify({"error": "Unauthorized access"}), 403

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }), 200
    except Exception as e:
        print(f"🔥 Exception in /user/{user_id}: {e}")
        return jsonify({'error': 'Unexpected server error'}), 500

# Update User Profile
@app.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    user = User.query.get_or_404(user_id)
    data = request.json
    # Validation is already handled in @app.before_request
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({'message': 'User profile updated'}), 200

# Delete User
@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
# probably can make a decorator like
# @user_auth()
# that internally handles both the jwt_required() check AND grabbing the user's ID
# directly from the JWT token so you know it's trusted
# i.e. Matt calls the DELETE /user endpoint, and we extract the user ID from the JWT token
# (and can trust it because it's signed with our secret), vs. having the user (browser) provide an ID
# and having to remember to compare
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

 

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/workout-sessions', methods=['POST'])
@jwt_required()
def start_workout_session():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("workout_type"):
        return jsonify({"error": "Workout type is required"}), 400

    new_session = Workout_Sessions(
        user_id=user_id,
        workout_type=data["workout_type"],
        date=datetime.now(timezone.utc),  # Corrected timezone usage
        duration=0  # can update this later
    )

    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        "message": "Workout session started",
        "session_id": new_session.id
    }), 201


# Create workout session
@app.route('/workouts', methods=['POST'])
@jwt_required()
def create_workout():
    user_id = get_jwt_identity()  # Get logged-in user's ID
    data = request.json
    if not data or not data.get('date') or not data.get('duration') or not data.get('workout_type'):
        return jsonify({'error': 'Missing required fields'}), 400

    
    new_workout = Workout_Sessions(
        user_id=user_id,
        date=datetime.strptime(data['date'], '%Y-%m-%d'),  # Convert date string to datetime object
        duration=data['duration'],
        workout_type=data['workout_type']
    )


    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "Workout session created", "id": new_workout.id}), 201

# Get all workout sessions
@app.route('/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()
    workouts = Workout_Sessions.query.filter_by(
        user_id=user_id
    ).order_by(Workout_Sessions.date.desc()).all()

    session_ids = [w.id for w in workouts]

    # Grab all exercise logs for these sessions in ONE query, joined with exercise names
    logs_by_session = {}
    if session_ids:
        logs = db.session.query(Exercise_Log, Exercises.name).join(
            Exercises, Exercise_Log.exercise_id == Exercises.id
        ).filter(Exercise_Log.workout_session_id.in_(session_ids)).all()

        for log, exercise_name in logs:
            logs_by_session.setdefault(log.workout_session_id, []).append({
                "name": exercise_name,
                "sets": log.sets,
                "reps": log.reps,
                "weight": log.weight,
                "rpe": log.rpe
            })

    return jsonify([{
        "id": w.id,
        "date": w.date.strftime('%Y-%m-%d'),
        "workout_type": w.workout_type,
        "exercises": logs_by_session.get(w.id, [])
    } for w in workouts]), 200

'''
# Get a specific workout session
@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout_Sessions.query.get_or_404(workout_id)
    return jsonify({
        "id": workout.id,
        "user_id": workout.user_id,
        "date": workout.date.strftime('%Y-%m-%d'),  # Convert datetime object to date string
        "duration": workout.duration,
        "workout_type": workout.workout_type
    })


# Update a workout session
@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    workout = Workout_Sessions.query.get_or_404(workout_id)
    data = request.json
    workout.duration = data.get('duration', workout.duration)
    workout.workout_type = data.get('workout_type', workout.workout_type)
    if 'date' in data:
        workout.date = datetime.strptime(data['date'], '%Y-%m-%d')  # Convert date string to datetime object
    db.session.commit()
    return jsonify({"message": "Workout updated"}), 200
'''

# Delete a workout session
@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout_Sessions.query.get_or_404(workout_id)
    print(f"🔍 Debug: workout.user_id={workout.user_id}, user_id={user_id}")
    if workout.user_id != int(user_id):
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200



@app.route('/exercises', methods=['GET'])
@jwt_required()
def get_exercises():
    user_id = get_jwt_identity()
    exercises = Exercises.query.filter(
        (Exercises.user_id == None) | (Exercises.user_id == user_id)
    ).order_by(Exercises.name.asc()).all()

    result = [{"id": ex.id, "name": ex.name} for ex in exercises]
    return jsonify(result), 200




#new workout logging method using lazy creation
@app.route('/log-workout', methods=['POST'])
@jwt_required()
def log_workout():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('workout_type') or not data.get('exercises'):
        return jsonify({"error": "Missing workout_type or exercises"}), 400

    if len(data['exercises']) == 0:
        return jsonify({"error": "Must log at least one exercise"}), 400

    try:
        # Create the session only if we have real exercises to save
        new_session = Workout_Sessions(
            user_id=user_id,
            workout_type=data['workout_type'],
            date=datetime.now(timezone.utc),
            duration=0
        )
        db.session.add(new_session)
        db.session.flush()  # gets us the new session ID without committing yet

        # Log all exercises against that session
        for ex in data['exercises']:
            log = Exercise_Log(
                workout_session_id=new_session.id,
                exercise_id=ex['exercise_id'],
                sets=ex['sets'],
                reps=ex['reps'],
                weight=ex['weight'],
                rpe=ex.get('rpe')
            )
            db.session.add(log)

        db.session.commit()  # commits everything at once
        return jsonify({"message": "Workout logged successfully", "session_id": new_session.id}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error logging workout: {e}")
        return jsonify({"error": "Failed to log workout"}), 500

if __name__ == '__main__':
    app.run(debug=True)


""" OLD AND UNUSED
# Log a workout session
@app.route('/exercise-log', methods=['POST'])
@jwt_required()
def add_exercise_log():
    user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['workout_session_id', 'exercise_id', 'sets', 'reps', 'weight']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Verify the workout session belongs to this user
    session = Workout_Sessions.query.filter_by(
        id=data['workout_session_id'],
        user_id=user_id
    ).first()
    if not session:
        return jsonify({"error": "Workout session not found or unauthorized"}), 404

    new_log = Exercise_Log(
        workout_session_id=data['workout_session_id'],
        exercise_id=data['exercise_id'],
        sets=data['sets'],
        reps=data['reps'],
        weight=data['weight'],
        rpe=data.get('rpe')
    )

    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "Exercise logged successfully", "id": new_log.id}), 201
"""