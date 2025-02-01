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
            padding: 20px;
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
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background: #292929;
            border-radius: 5px;
            overflow: hidden;
        }
        th, td {
            border: 1px solid #444;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #2a2a2a;
            color: #bb86fc;
        }
        .auth-required {
            background: #cf6679;
            color: white;
            padding: 4px;
            border-radius: 3px;
            font-size: 12px;
        }
        .footer {
            margin-top: 20px;
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
            <table>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Description</th>
                    <th>Auth</th>
                </tr>
                <tr>
                    <td><code>/register</code></td>
                    <td>POST</td>
                    <td>Registers a new user (volunteer or organization).</td>
                    <td>❌</td>
                </tr>
                <tr>
                    <td><code>/login</code></td>
                    <td>POST</td>
                    <td>Authenticates user & returns JWT token.</td>
                    <td>❌</td>
                </tr>
                <tr>
                    <td><code>/details</code></td>
                    <td>GET</td>
                    <td>Fetches authenticated user details.</td>
                    <td><span class="auth-required">✔️ JWT</span></td>
                </tr>
                <tr>
                    <td><code>/update</code></td>
                    <td>PUT</td>
                    <td>Updates user details.</td>
                    <td><span class="auth-required">✔️ JWT</span></td>
                </tr>
                <tr>
                    <td><code>/delete</code></td>
                    <td>DELETE</td>
                    <td>Deletes user account.</td>
                    <td><span class="auth-required">✔️ JWT</span></td>
                </tr>
            </table>
        </div>

        <div class="section">
            <h2>Projects</h2>
            <table>
                <tr>
                    <th>Endpoint</th>
                    <th>Method</th>
                    <th>Description</th>
                    <th>Auth</th>
                </tr>
                <tr>
                    <td><code>/projects</code></td>
                    <td>POST</td>
                    <td>Creates a new project.</td>
                    <td><span class="auth-required">✔️ Org</span></td>
                </tr>
                <tr>
                    <td><code>/projects</code></td>
                    <td>GET</td>
                    <td>Fetches all projects.</td>
                    <td><span class="auth-required">✔️ JWT</span></td>
                </tr>
                <tr>
                    <td><code>/projects/:id/apply</code></td>
                    <td>POST</td>
                    <td>Apply for a project.</td>
                    <td><span class="auth-required">✔️ Volunteer</span></td>
                </tr>
                <tr>
                    <td><code>/user/applications</code></td>
                    <td>GET</td>
                    <td>View user's applications.</td>
                    <td><span class="auth-required">✔️ Volunteer</span></td>
                </tr>
                <tr>
                    <td><code>/projects/:id/cancel</code></td>
                    <td>DELETE</td>
                    <td>Cancel application.</td>
                    <td><span class="auth-required">✔️ Volunteer</span></td>
                </tr>
            </table>
        </div>

        <div class="footer">
            <p>For any questions or support, contact us at <a href="mailto:support@volunteerapi.com">support@volunteerapi.com</a></p>
            <p>&copy; 2025 Volunteer Matching API</p>
        </div>
    </div>
</body>
</html>

    """

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before running the app

    # Get the port from environment variable or use 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
