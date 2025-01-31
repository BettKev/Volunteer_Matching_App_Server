# Volunteer Matching App - Server

This project sets up a backend Flask server for the Volunteer Matching App. The server provides RESTful API endpoints for managing users, projects, and applications.

## Prerequisites

Ensure you have the following installed on your system:
- **Python 3.7 or later** - Required to run the Flask application.
- **pipenv** - A dependency management tool for Python.
- **A code editor** (e.g., Visual Studio Code) - Recommended for development.

---

## Project Structure

```
bettkev-volunteer_matching_app_server/
├── README.md              # Documentation for the project
├── Pipfile                # Dependencies and virtual environment configuration
├── app.py                 # Main application entry point
├── seed.py                # Script to seed the database with initial data
├── instance/
│   └── app.db             # SQLite database (if used locally)
├── migrations/            # Alembic migration scripts
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   ├── __pycache__/
│   └── versions/
│       ├── 5b6f25736a53_initial_migration.py
│       └── __pycache__/
├── models/                # Database models
│   ├── __init__.py
│   ├── models.py
│   └── __pycache__/
└── routes/                # API routes
    ├── application_routes.py
    ├── project_routes.py
    ├── user_routes.py
    └── __pycache__/                                        
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/volunteer-matching-app-server.git
cd volunteer-matching-app-server
```

### 2. Install Dependencies

Use `pipenv` to install the required dependencies:

```bash
pipenv install flask flask_cors flask_restful flask_sqlalchemy alembic
```

### 3. Activate the Virtual Environment

```bash
pipenv shell
```

### 4. Set Up the Database

Run the following commands to initialize the database:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

If using SQLite, a database file (`instance/app.db`) will be created.

### 5. Seed the Database (Optional)

You can populate the database with sample data by running:

```bash
python seed.py
```

### 6. Run the Application

Ensure you're in the virtual environment and start the Flask app:

```bash
flask --app app run --debug
```

If you encounter the error:

```bash
Error: Could not locate a Flask application.
```

Make sure the file `app.py` exists in the current directory, then run:

```bash
export FLASK_APP=app.py
flask run --debug
```

### 7. Access the API

Once the server is running, open your browser and navigate to:

```
http://127.0.0.1:5000
```

You should see the API documentation or a confirmation message.

---

## API Endpoints

The server exposes RESTful API endpoints for managing users, projects, and applications. Example routes include:

- **Users**
  - `GET /users` - Retrieve all users.
  - `POST /users` - Create a new user.

- **Projects**
  - `GET /projects` - Retrieve all projects.
  - `POST /projects` - Create a new project.

- **Applications**
  - `GET /applications` - Retrieve all applications.
  - `POST /applications` - Submit a new volunteer application.

More endpoints and detailed API documentation will be provided in future updates.

---

## Notes

- Always activate the virtual environment (`pipenv shell`) before running Flask commands.
- For database migrations, ensure `flask db upgrade` is run after making changes to the models.
- Logging can be enabled for debugging API requests and responses.

---

## Resources & Links

- **Deployed Frontend**: [Volunteer Matching App - Frontend](https://volunteer-liard.vercel.app/)
- **Deployed Backend**: [Volunteer Matching App - Backend](https://volunteer-matching-app-server.onrender.com/)
- **Demo Video**: [YouTube Video Demo](https://youtu.be/fqeVZi8tRKk)

## Contribution Guidelines

Contributions are welcome! If you want to contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to your fork (`git push origin feature-name`).
5. Submit a pull request.

---

For any issues, suggestions, or feedback, feel free to open an issue or submit a pull request.
