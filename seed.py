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
            User(name="Sophia Turner", email="sophia.turner@greenearth.org", password="volunteerpass123", role="volunteer"),
            User(name="John Patterson", email="john.patterson@techforgood.org", password="techpass987", role="organization"),
            User(name="Olivia Carter", email="olivia.carter@helpinghands.com", password="communitylove456", role="volunteer"),
            User(name="David Bennett", email="david.bennett@ecoalliance.org", password="greenworld321", role="organization"),
            User(name="Emily Rodriguez", email="emily.rodriguez@animalrights.org", password="petlovers789", role="volunteer"),
            User(name="Michael Clark", email="michael.clark@codingforkids.org", password="codingpass567", role="organization"),
            User(name="Isabella Martinez", email="isabella.martinez@childcarefoundation.org", password="helpingkids234", role="volunteer"),
            User(name="James Anderson", email="james.anderson@disasterrelief.com", password="reliefpass123", role="organization"),
            User(name="Lily Moore", email="lily.moore@foodbank.org", password="givingfood456", role="volunteer"),
            User(name="Matthew Lee", email="matthew.lee@unitedglobal.org", password="peaceforall987", role="organization"),
            # Additional Organizations to ensure there are 10
            User(name="Nathaniel Green", email="nathaniel.green@restoreearth.org", password="earthkeeper123", role="organization"),
            User(name="Laura Gomez", email="laura.gomez@techskillsforgood.com", password="skillsfortech789", role="organization"),
            User(name="Daniel Young", email="daniel.young@healthforall.org", password="healthforall123", role="organization"),
            User(name="Sophia Wells", email="sophia.wells@communitycare.org", password="carecommunity987", role="organization"),
            User(name="Robert King", email="robert.king@greeninitiative.org", password="greenlife456", role="organization"),
            # Additional Volunteers to ensure there are 10
            User(name="Charlotte Harris", email="charlotte.harris@volunteer.org", password="charitypass123", role="volunteer"),
            User(name="Daniel Foster", email="daniel.foster@volunteerhelp.com", password="volunteerpass456", role="volunteer"),
            User(name="Grace Walker", email="grace.walker@humanity.org", password="helpinghand123", role="volunteer"),
            User(name="Lucas Walker", email="lucas.walker@helpinghands.com", password="makingadifference789", role="volunteer"),
            User(name="Ava Johnson", email="ava.johnson@communitycare.org", password="givinglove234", role="volunteer"),
        ]
        
        db.session.add_all(users)
        db.session.commit()

        # Fetch organization users to assign them projects
        organizations = User.query.filter_by(role="organization").all()

        # Seed Projects (Owned by Organizations)
        projects = [
            Project(title="Community Park Cleanup", description="Organizing a weekend cleanup drive in the local park to keep it beautiful and safe for families.", organization_id=organizations[0].user_id, status="Active"),
            Project(title="Tech for Good: Coding Bootcamp", description="Providing coding workshops for underprivileged youth in urban communities to create job opportunities in the tech industry.", organization_id=organizations[1].user_id, status="Pending"),
            Project(title="Green Energy Solutions", description="Promoting renewable energy projects and education about sustainable energy solutions to reduce environmental impact.", organization_id=organizations[2].user_id, status="Active"),
            Project(title="Urban Farming Initiative", description="Building community gardens in urban areas to promote healthy eating and sustainable living practices.", organization_id=organizations[3].user_id, status="Pending"),
            Project(title="Animal Shelter Support", description="Volunteering and fundraising for local animal shelters to help them care for abandoned animals and improve their facilities.", organization_id=organizations[4].user_id, status="Completed"),
            Project(title="Coding for All: Computer Literacy", description="A series of workshops aimed at teaching basic computer literacy to senior citizens and people with disabilities.", organization_id=organizations[5].user_id, status="Active"),
            Project(title="Childhood Education Access", description="An outreach program providing educational materials and mentoring services to children from disadvantaged families.", organization_id=organizations[6].user_id, status="Active"),
            Project(title="Disaster Relief Fundraising", description="Organizing fundraisers and donation drives to support victims of natural disasters worldwide.", organization_id=organizations[7].user_id, status="Pending"),
            Project(title="Feeding the Homeless", description="A regular program that prepares and delivers nutritious meals to homeless individuals in the local community.", organization_id=organizations[8].user_id, status="Active"),
            Project(title="Global Peace Education", description="Campaigns and initiatives designed to foster peace and conflict resolution skills for people in conflict zones.", organization_id=organizations[9].user_id, status="Completed"),
        ]
        
        db.session.add_all(projects)
        db.session.commit()

        # Fetch volunteers to assign them applications
        volunteers = User.query.filter_by(role="volunteer").all()
        projects = Project.query.all()

        # Seed Applications (Volunteers applying for projects)
        applications = []
        for i in range(min(len(volunteers), len(projects))):  # Avoid index out of range
            applications.append(Application(user_id=volunteers[i].user_id, project_id=projects[i].project_id, status="Pending"))

        db.session.add_all(applications)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
