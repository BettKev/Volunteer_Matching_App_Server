from flask import Blueprint, jsonify, request
from models.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_routes = Blueprint("user_routes", __name__)

# User registration route
@user_routes.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({"error": "All fields (name, email, password, role) are required."}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "A user with this email already exists."}), 400

    try:
        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully!",
            "user_id": new_user.user_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while registering the user.", "details": str(e)}), 500

# Login route
@user_routes.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password."}), 401

    access_token = create_access_token(identity=str(user.user_id))

    return jsonify({
        "message": "Login successful!",
        "access_token": access_token
    }), 200

# Logout route
@user_routes.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    user_id = get_jwt_identity()
    return jsonify({"message": f"User {user_id} logged out successfully!"}), 200

# Fetch single user route
@user_routes.route("/details", methods=["GET"])
@jwt_required()  # Require valid JWT token
def fetch_user_details():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    # Return user details (excluding sensitive data like password)
    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200

# Update user route
@user_routes.route("/update", methods=["PUT"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    if name:
        user.name = name
    if password:
        user.password = generate_password_hash(password)  # Hash the password

    try:
        db.session.commit()
        return jsonify({"message": "User updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the user.", "details": str(e)}), 500

# Delete user route
@user_routes.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    """
    Deletes the currently authenticated user's account.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    try:
        db.session.delete(user)  # Delete the user
        db.session.commit()
        return jsonify({"message": "User account deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error while deleting user: {e}")  # Log the error to the console or a log file
        return jsonify({"error": "An error occurred while deleting the user.", "details": str(e)}), 500