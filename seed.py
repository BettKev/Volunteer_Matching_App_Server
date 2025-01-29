import os
from flask import Flask
from models.models import db, User, Project, Application  # Ensure this imports correctly from your models package

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

        # Seed Users (Organizations & Volunteers)
        users = [
            User(name="Alice Johnson", email="alice@example.com", password="password123", role="volunteer"),
            User(name="Bob Smith", email="bob@example.com", password="securepassword", role="organization"),
            User(name="Charlie Brown", email="charlie@example.com", password="mypassword", role="volunteer"),
            User(name="Diana Prince", email="diana@example.com", password="wonderwoman", role="organization"),
        ]
        
        for i in range(16):  # Adding 16 more users
            users.append(User(name=f"User{i}", email=f"user{i}@example.com", password=f"password{i}", role="volunteer" if i % 2 == 0 else "organization"))
        
        db.session.add_all(users)
        db.session.commit()

        # Fetch organization users to assign them projects
        organizations = User.query.filter_by(role="organization").all()

        # Seed Projects (Owned by Organizations)
        projects = [
            Project(title="Clean the Park", description="A community cleanup initiative.", organization_id=organizations[0].user_id, status="Active"),
            Project(title="Teach Coding to Kids", description="A volunteer-based coding bootcamp.", organization_id=organizations[1].user_id, status="Pending"),
            Project(title="Plant Trees", description="An effort to increase green cover in the city.", organization_id=organizations[0].user_id, status="Completed"),
        ]
        
        for i in range(17):  # Adding 17 more projects
            projects.append(Project(title=f"Project{i}", description=f"Description for project {i}", organization_id=organizations[i % len(organizations)].user_id, status="Active" if i % 3 == 0 else "Pending"))
        
        db.session.add_all(projects)
        db.session.commit()

        # Fetch volunteers to assign them applications
        volunteers = User.query.filter_by(role="volunteer").all()
        projects = Project.query.all()

        # Seed Applications (Volunteers applying for projects)
        applications = [
            Application(user_id=volunteers[0].user_id, project_id=projects[0].project_id, status="Pending"),
            Application(user_id=volunteers[1].user_id, project_id=projects[1].project_id, status="Approved"),
            Application(user_id=volunteers[0].user_id, project_id=projects[2].project_id, status="Rejected"),
        ]
        
        for i in range(27):  # Adding 27 more applications
            applications.append(Application(user_id=volunteers[i % len(volunteers)].user_id, project_id=projects[i % len(projects)].project_id, status="Approved" if i % 2 == 0 else "Pending"))
        
        db.session.add_all(applications)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
