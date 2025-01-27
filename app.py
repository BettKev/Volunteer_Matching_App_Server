from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models.user import db, User  # Import db from user.py
from flask_migrate import Migrate

app = Flask(__name__)

# Enable CORS
CORS(app)

# Configure the app's secret key and database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database (for development)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Optional JWT secret key

# Initialize the db and Flask-Migrate with the app
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return {"message": "Welcome to Dexters Lab API!"}, 200

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
    new_user = User(name=name, email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!", "user_id": new_user.user_id}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before running the app
    app.run(debug=True)


if __name__ == "__main__":
    # Get the port from environment variable or use 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
