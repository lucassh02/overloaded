import sys
import os
import pytest
from datetime import datetime
from flask_jwt_extended import create_access_token
from app import app, db, Workout_Sessions, User, bcrypt

# Ensure the tests import the backend package correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up the test database location
TEST_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_workout.db"))



@pytest.fixture
def client():
    """ Set up test client with a temporary database """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{TEST_DB_PATH}'
    app.config['JWT_SECRET_KEY'] = 'testsecretkey'
    
    with app.test_client() as client:
        with app.app_context():
            if not os.path.exists(TEST_DB_PATH):  # ✅ Fix: Create DB file if missing
                open(TEST_DB_PATH, 'a').close()
            db.create_all()
        yield client  # Run tests
        with app.app_context():
            db.drop_all()
            if os.path.exists(TEST_DB_PATH):  # ✅ Fix: Prevent error if file is already deleted
                os.remove(TEST_DB_PATH)



@pytest.fixture
def create_user():
    """Create a test user and return a session-bound instance"""
    def _create_user(username, email, password):
        with app.app_context():
            # Delete any existing user with the same email
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()

            # Create new user
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

            # ✅ Fix: Re-fetch the user from the database within the same session
            return db.session.query(User).filter_by(email=email).first()

    return _create_user

@pytest.fixture
def auth_token(client, create_user):
    """Create a test user and return a JWT token"""
    user = create_user("testuser", "test@example.com", "password")

    with app.app_context():
        access_token = create_access_token(identity=str(user.id))  # ✅ Ensure ID is a string

    return {"Authorization": f"Bearer {access_token}"}

# ---------------------
# Workout Tests (Require Auth)
# ---------------------

def test_create_workout(client, auth_token):
    """ Test creating a workout session """
    response = client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    }, headers=auth_token)
    assert response.status_code == 201
    assert b'Workout session created' in response.data

def test_get_workouts(client, auth_token):
    """ Test retrieving all workout sessions """
    response = client.get('/workouts', headers=auth_token)
    assert response.status_code == 200

def test_get_workout(client, auth_token):
    """ Test retrieving a specific workout session """
    client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    }, headers=auth_token)
    response = client.get('/workouts/1', headers=auth_token)
    assert response.status_code == 200

def test_update_workout(client, auth_token):
    """ Test updating a workout session """
    client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    }, headers=auth_token)
    response = client.put('/workouts/1', json={
        'duration': 90,
        'workout_type': 'Strength'
    }, headers=auth_token)
    assert response.status_code == 200
    assert b'Workout updated' in response.data

def test_delete_workout(client, auth_token):
    """ Test deleting a workout session """
    client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    }, headers=auth_token)
    response = client.delete('/workouts/1', headers=auth_token)
    assert response.status_code == 200
    assert b'Workout deleted' in response.data

# ---------------------
# User Tests (Require Auth)
# ---------------------

def test_get_user_profile(client, auth_token, create_user):
    """ Test retrieving a user profile with valid JWT """
    user = create_user('testuser', 'test@example.com', 'password')

    # Ensure session refresh is inside app context
    with app.app_context():
        db.session.refresh(user)

    response = client.get(f'/user/{user.id}', headers=auth_token)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == user.id
    assert data['username'] == user.username
    assert data['email'] == user.email
    assert 'created_at' in data


def test_get_user_profile_unauthorized(client, create_user):
    """Test retrieving a different user's profile (should fail)"""
    user = create_user('testuser', 'test@example.com', 'password')
    other_user = create_user('otheruser', 'other@example.com', 'password')

    # ✅ Ensure token identity is a string
    with app.app_context():
        access_token = create_access_token(identity=str(other_user.id))

    response = client.get(f'/user/{user.id}', headers={"Authorization": f"Bearer {access_token}"})

    print(f"🚨 Debug Response: {response.status_code}, {response.get_json()}")  # ✅ Debugging

    assert response.status_code == 403  # Ensure API returns correct status
    data = response.get_json()
    assert data['error'] == 'Unauthorized access'