import os
from flask import Flask
from models.user import db, User  # Ensure the path to the User model is correct

# Create the Flask app
app = Flask(__name__)

# Set the correct database path
base_dir = os.path.abspath(os.path.dirname(__file__))  # Directory of seed.py
db_path = os.path.join(base_dir, "instance", "app.db")  # Path to app.db in instance/
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

def seed_data():
    """Seed the database with initial data."""
    with app.app_context():
        # Drop all tables and recreate them for a fresh start
        db.drop_all()
        db.create_all()

        # Create seed users
        users = [
            User(name="Alice Johnson", email="alice@example.com", password="password123", role="volunteer"),
            User(name="Bob Smith", email="bob@example.com", password="securepassword", role="organization"),
            User(name="Charlie Brown", email="charlie@example.com", password="mypassword", role="volunteer"),
            User(name="Diana Prince", email="diana@example.com", password="wonderwoman", role="organization"),
        ]

        # Add users to the database session
        db.session.add_all(users)

        # Commit the session to save the changes
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
