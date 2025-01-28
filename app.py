from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models.user import db # Import db from user.py
from routes.user_routes import user_routes  # Import user routes
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
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 1 hour


jwt = JWTManager(app)

# Initialize the db and Flask-Migrate with the app
db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(user_routes, url_prefix="/user")

# Test route
@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Volunteer Matching App</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="text-center mb-4">Welcome to the Volunteer Matching App</h1>
                
                <p>This API allows organizations to manage volunteers, projects, and applications. Below are the key endpoints:</p>
                
                <div class="alert alert-info">
                    <h4 class="alert-heading">Available Endpoints:</h4>
                    <ul>
                        <li><strong><code>/register</code></strong>: <em>POST</em> - Register a new user (volunteer or organization)</li>
                        <li><strong><code>/login</code></strong>: <em>POST</em> - Login with email and password</li>
                        <li><strong><code>/user/<user_id></code></strong>: <em>GET</em> - Get user details by ID</li>
                        <li><strong><code>/project</code></strong>: <em>GET</em> - List all available projects</li>
                        <li><strong><code>/application</code></strong>: <em>POST</em> - Submit an application for a project</li>
                    </ul>
                </div>

                <p class="mt-4">For detailed information on each endpoint, refer to the API documentation.</p>

                <div class="alert alert-warning">
                    <strong>Note:</strong> This app uses Flask for the backend and React for the frontend. 
                    Make sure to have the frontend running on <code>http://localhost:3000</code> and the backend on <code>http://localhost:5000</code>.
                </div>
            </div>
            
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.0.3/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
    </html>
    """

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created before running the app

    # Get the port from environment variable or use 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
