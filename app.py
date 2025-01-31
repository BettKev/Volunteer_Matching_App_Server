from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models.models import User, Project, db # Import models
from routes.user_routes import user_routes  # Import user routes
from routes.project_routes import project_routes # Import project routes
from routes.application_routes import application_routes # Import application routes
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)


# Enable CORS
CORS(app)

# Configure the app's secret key and database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database (for development)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Optional JWT secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 30 minutes


jwt = JWTManager(app)

# Initialize the db and Flask-Migrate with the app
db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(user_routes)
app.register_blueprint(project_routes)
app.register_blueprint(application_routes)

# Test route
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volunteer Matching API Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #121212;
            color: #e0e0e0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            background: #1e1e1e;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        h1, h2, h3 {
            color: #bb86fc;
        }
        p {
            color: #b0b0b0;
        }
        code {
            background: #333;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            color: #bb86fc;
        }
        pre {
            background: #292929;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #bb86fc;
            font-size: 14px;
            color: #e0e0e0;
            text-align: left;
        }
        .section {
            margin-bottom: 30px;
            text-align: left;
        }
        .endpoint {
            background: #2a2a2a;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .auth-required {
            background: #cf6679;
            color: white;
            padding: 5px;
            border-radius: 3px;
            font-size: 12px;
            margin-left: 10px;
        }
        .footer {
            margin-top: 30px;
            font-size: 14px;
            color: #b0b0b0;
        }
        a {
            color: #bb86fc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Volunteer Matching API Documentation</h1>
        <p>Welcome to the Volunteer Matching API! This API helps organizations and volunteers connect through projects. Below is a list of available endpoints with their usage details.</p>

        <div class="section">
            <h2>Authentication</h2>

            <div class="endpoint">
                <h3>Register</h3>
                <p><code>POST /register</code></p>
                <p>Registers a new user (volunteer or organization).</p>
                <pre>
Request:
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "volunteer"
}

Response:
{
    "message": "User registered successfully",
    "user_id": 123
}
                </pre>
            </div>

            <div class="endpoint">
                <h3>Login</h3>
                <p><code>POST /login</code></p>
                <p>Authenticates a user and returns a JWT token.</p>
                <pre>
Request:
{
    "email": "john@example.com",
    "password": "password123"
}

Response:
{
    "access_token": "jwt_token_here"
}
                </pre>
            </div>

            <div class="endpoint">
                <h3>Fetch User Details</h3>
                <p><code>GET /details</code> <span class="auth-required">Requires JWT Token</span></p>
                <p>Fetches the authenticated user's details.</p>
                <pre>
Response:
{
    "user_id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "volunteer"
}
                </pre>
            </div>

            <div class="endpoint">
                <h3>Update User</h3>
                <p><code>PUT /update</code> <span class="auth-required">Requires JWT Token</span></p>
                <p>Updates the authenticated user's details.</p>
                <pre>
Request:
{
    "name": "John Doe Updated",
    "password": "newpassword"
}

Response:
{
    "message": "User updated successfully!"
}
                </pre>
            </div>

            <div class="endpoint">
                <h3>Delete User Account</h3>
                <p><code>DELETE /delete</code> <span class="auth-required">Requires JWT Token</span></p>
                <p>Deletes the currently authenticated user's account.</p>
                <pre>
Response:
{
    "message": "User account deleted successfully!"
}
                </pre>
            </div>
        </div>

        <div class="section">
            <h2>Projects</h2>

            <div class="endpoint">
                <h3>Create a Project</h3>
                <p><code>POST /projects</code> <span class="auth-required">Only organizations</span></p>
                <pre>
Request:
{
    "title": "Community Cleanup",
    "description": "A project to clean up the park."
}

Response:
{
    "message": "Project created successfully",
    "project_id": 45
}
                </pre>
            </div>

            <div class="endpoint">
                <h3>View All Projects</h3>
                <p><code>GET /projects</code> <span class="auth-required">Authenticated users</span></p>
                <pre>
Response:
[
    {
        "project_id": 45,
        "title": "Community Cleanup",
        "description": "A project to clean up the park.",
        "organization_id": 12
    }
]
                </pre>
            </div>

            <div class="endpoint">
                <h3>Apply for a Project</h3>
                <p><code>POST /projects/:id/apply</code> <span class="auth-required">Only volunteers</span></p>
                <pre>
Response:
{
    "message": "Application submitted successfully!"
}
                </pre>
            </div>

            <div class="endpoint">
                <h3>View User Applications</h3>
                <p><code>GET /user/applications</code> <span class="auth-required">Only volunteers</span></p>
                <pre>
Response:
[
    {
        "project_id": 45,
        "project_title": "Community Cleanup",
        "project_description": "A project to clean up the park.",
        "project_status": "Open"
    }
]
                </pre>
            </div>

            <div class="endpoint">
                <h3>Cancel Application</h3>
                <p><code>DELETE /projects/:id/cancel</code> <span class="auth-required">Only volunteers</span></p>
                <pre>
Response:
{
    "message": "Application canceled successfully!"
}
                </pre>
            </div>
        </div>

        <div class="footer">
            <p>For any questions or support, contact us at <a href="mailto:support@volunteerapi.com">support@volunteerapi.com</a></p>
            <p>&copy; 2025 Volunteer Matching API</p>
        </div>
    </d


    """

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before running the app

    # Get the port from environment variable or use 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
