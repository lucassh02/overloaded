from flask import Flask, request, jsonify
from models import db, User, Workout_Sessions, Exercises, Exercise_Log, Routines, Routine_Exercises
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure JWT secret key (Change this in production!)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def home():
    return {"message": "Flask API is running!"}, 200

@app.before_request
def log_request_info():
    print(f"Incoming Request: {request.method} {request.url}")


@app.route("/test-login", methods=["POST"])
def login_test():
    data = request.json
    if data["email"] == "test@example.com" and data["password"] == "password":
        return jsonify({"access_token": "mock-jwt-token"}), 200
    return jsonify({"error": "Invalid credentials"}), 401




# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already in use'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    #refresh_token = create_refresh_token(identity=user.id)
    return jsonify({'access_token': access_token, 'user_id': user.id}), 200

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

# Get User Profile
@app.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at
    })

# Update User Profile
@app.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    user = User.query.get_or_404(user_id)
    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify({'message': 'User profile updated'}), 200

# Delete User
@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


# Create workout session
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.json
    new_workout = Workout_Sessions(
        user_id=data['user_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d'),  # Convert date string to datetime object
        duration=data['duration'],
        workout_type=data['workout_type']
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "Workout session created", "id": new_workout.id}), 201

# Get all workout sessions
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout_Sessions.query.all()
    return jsonify([{
        "id": w.id,
        "user_id": w.user_id,
        "date": w.date.strftime('%Y-%m-%d'),  # Convert datetime object to date string
        "duration": w.duration,
        "workout_type": w.workout_type
    } for w in workouts]), 200

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

# Delete a workout session
@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout_Sessions.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)






