from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models import db, User

app = Flask(__name__)

# Configure JWT secret key (Change this in production!)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(debug=True)
