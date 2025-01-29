from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

# Project Model
class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # ForeignKey to User
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Example statuses: Pending, Active, Completed

    # Relationship
    organization = db.relationship('User', backref='projects')

    def __init__(self, title, description, organization_id, status='Pending'):
        self.title = title
        self.description = description
        self.organization_id = organization_id
        self.status = status
