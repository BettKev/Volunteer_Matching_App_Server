from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models.user import db  # Import the db object from user.py

app = Flask(__name__)

# Enable CORS
CORS(app)

# Configure the app's secret key and database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database (for development)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Optional JWT secret key (if using JWT)

# Initialize the db with the app
db.init_app(app)

@app.route("/")
def home():
    return {"message": "Welcome to Dexters Lab API!"}, 200

if __name__ == "__main__":
    # Create the database and tables if they don't already exist
    with app.app_context():
        db.create_all()

    # Get the port from environment variable or use 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
