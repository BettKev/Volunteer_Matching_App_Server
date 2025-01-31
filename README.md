# Volunteer Matching App Server

This project sets up a basic Flask server with the following dependencies:
- `Flask`
- `Flask-CORS`
- `Flask-RESTful`

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.7 or later
- `pipenv` (Python dependency management tool)
- A code editor (e.g., Visual Studio Code)

---

## Project Structure

```
bettkev-volunteer_matching_app_server/
    ├── README.md
    ├── Pipfile
    ├── app.py
    ├── seed.py
    ├── instance/
    │   └── app.db
    ├── migrations/
    │   ├── README
    │   ├── alembic.ini
    │   ├── env.py
    │   ├── script.py.mako
    │   ├── __pycache__/
    │   └── versions/
    │       ├── 5b6f25736a53_initial_migration.py
    │       └── __pycache__/
    ├── models/
    │   ├── __init__.py
    │   ├── models.py
    │   └── __pycache__/
    └── routes/
        ├── application_routes.py
        ├── project_routes.py
        ├── user_routes.py
        └── __pycache__/                                       
```
---

## Setup Instructions

1. **Navigate to the Project Directory**

   ```bash
   cd project
   cd server
   code .
   ```

2. **Install Dependencies**

   Use `pipenv` to install the required Python packages:

   ```bash
   pipenv install flask flask_cors flask_restful
   ```

3. **Activate the Virtual Environment**

   ```bash
   pipenv shell
   ```

4. **Run the Application**

   Ensure you're in the virtual environment and run the Flask app:

   ```bash
   flask --app app run --debug
   ```

   If you encounter the error:

   ```bash
   Error: Could not locate a Flask application.
   ```

   Make sure the file `app.py` exists in the current directory, and run:

   ```bash
   export FLASK_APP=app.py
   flask run --debug
   ```

7. **Access the Server**

   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

   You should see the API documentation page

---

## Notes

- Always activate the virtual environment (`pipenv shell`) before running Flask commands.
- For further debugging, ensure the `FLASK_APP` environment variable is correctly set.

---

## Resources & Links

- [Deployed Link](https://volunteer-matching-app-server.onrender.com/)

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pipenv Documentation](https://pipenv.pypa.io/)