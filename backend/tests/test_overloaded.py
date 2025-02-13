import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Workout_Sessions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_workout(client):
    response = client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    })
    assert response.status_code == 201
    assert b'Workout session created' in response.data

def test_get_workouts(client):
    response = client.get('/workouts')
    assert response.status_code == 200

def test_get_workout(client):
    client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    })
    response = client.get('/workouts/1')
    assert response.status_code == 200

def test_update_workout(client):
    client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    })
    response = client.put('/workouts/1', json={
        'duration': 90,
        'workout_type': 'Strength'
    })
    assert response.status_code == 200
    assert b'Workout updated' in response.data

def test_delete_workout(client):
    client.post('/workouts', json={
        'user_id': 1,
        'date': '2025-02-11',
        'duration': 60,
        'workout_type': 'Cardio'
    })
    response = client.delete('/workouts/1')
    assert response.status_code == 200
    assert b'Workout deleted' in response.data