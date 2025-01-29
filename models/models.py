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

    # Relationship to projects (for organizations)
    projects = db.relationship('Project', backref='organization', lazy=True, cascade="all, delete-orphan")

    # Relationship to applications (for volunteers)
    applications = db.relationship('Application', backref='applicant', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)  # Hash password
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Project Model
class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign Key to User (Organization)
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Example statuses: Pending, Active, Completed

    # Relationship to applications
    applications = db.relationship('Application', backref='project', lazy=True, cascade="all, delete-orphan")

    def __init__(self, title, description, organization_id, status='Pending'):
        self.title = title
        self.description = description
        self.organization_id = organization_id
        self.status = status


# Application Model
class Application(db.Model):
    __tablename__ = 'applications'

    application_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign Key to User (Volunteer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)  # Foreign Key to Project
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Status: Pending, Approved, Rejected

    def __init__(self, user_id, project_id, status='Pending'):
        self.user_id = user_id
        self.project_id = project_id
        self.status = status
