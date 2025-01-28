from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models.user import db, User  # Import db from user.py
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash
from datetime import timedelta


app = Flask(__name__)


# Enable CORS
CORS(app)

# Configure the app's secret key and database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database (for development)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Optional JWT secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 1 hour


jwt = JWTManager(app)

# Initialize the db and Flask-Migrate with the app
db.init_app(app)
migrate = Migrate(app, db)

# Test route
@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Volunteer Matching App</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="text-center mb-4">Welcome to the Volunteer Matching App</h1>
                
                <p>This API allows organizations to manage volunteers, projects, and applications. Below are the key endpoints:</p>
                
                <div class="alert alert-info">
                    <h4 class="alert-heading">Available Endpoints:</h4>
                    <ul>
                        <li><strong><code>/register</code></strong>: <em>POST</em> - Register a new user (volunteer or organization)</li>
                        <li><strong><code>/login</code></strong>: <em>POST</em> - Login with email and password</li>
                        <li><strong><code>/user/<user_id></code></strong>: <em>GET</em> - Get user details by ID</li>
                        <li><strong><code>/project</code></strong>: <em>GET</em> - List all available projects</li>
                        <li><strong><code>/application</code></strong>: <em>POST</em> - Submit an application for a project</li>
                    </ul>
                </div>

                <p class="mt-4">For detailed information on each endpoint, refer to the API documentation.</p>

                <div class="alert alert-warning">
                    <strong>Note:</strong> This app uses Flask for the backend and React for the frontend. 
                    Make sure to have the frontend running on <code>http://localhost:3000</code> and the backend on <code>http://localhost:5000</code>.
                </div>
            </div>
            
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.0.3/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
    </html>
    """

# User registration route
@app.route("/register", methods=["POST"])
def register_user():
    """
    Route to register a new user.
    Expects JSON payload with 'name', 'email', 'password', and 'role'.
    """
    data = request.get_json()  # Parse JSON payload

    # Validate input
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({"error": "All fields (name, email, password, role) are required."}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "A user with this email already exists."}), 400

    # Create a new user
    try:
        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully!",
            "user_id": new_user.user_id  # Assuming `user_id` is a field in the User model
        }), 201
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an error
        return jsonify({"error": "An error occurred while registering the user.", "details": str(e)}), 500
    
# Login Route
@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Check if password is correct (assuming password is hashed)
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password."}), 401

    # Create JWT token
    access_token = create_access_token(identity=user.user_id)

    return jsonify({
        "message": "Login successful!",
        "access_token": access_token  # Send the token to the frontend
    }), 200

# Logout Route
@app.route("/logout", methods=["POST"])
def logout_user():
    """
    Route to log out the user.
    This simply tells the frontend to remove the JWT token from storage.
    """
    return jsonify({"message": "Logout successful!"}), 200


# # Dashboard Route (protected by JWT)
# @app.route("/dashboard", methods=["GET"])
# @jwt.required  # This decorator ensures that the user must be authenticated
# def dashboard():
#     return jsonify({"message": "Welcome to the Dashboard!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before running the app
    app.run(debug=True)

    # Get the port from environment variable or use 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
