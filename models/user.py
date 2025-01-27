from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize extensions
db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed password
    role = db.Column(db.String(50), nullable=False)  # volunteer or organization

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        # Hash password using Werkzeug
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        # Check if the provided password matches the hashed password
        return check_password_hash(self.password, password)
