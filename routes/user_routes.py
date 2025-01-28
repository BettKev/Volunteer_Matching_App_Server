from flask import Blueprint, jsonify, request
from models.user import User, db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

user_routes = Blueprint("user_routes", __name__)

# User registration route
@user_routes.route("/register", methods=["POST"])
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
@user_routes.route("/login", methods=["POST"])
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
@user_routes.route("/logout", methods=["POST"])
def logout_user():
    """
    Route to log out the user.
    This simply tells the frontend to remove the JWT token from storage.
    """
    return jsonify({"message": "Logout successful!"}), 200
