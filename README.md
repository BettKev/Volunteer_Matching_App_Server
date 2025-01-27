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
project/
├── server/
│   └── (Flask project files)
└── README.md
```

---

## Setup Instructions

1. **Create and Navigate to the Project Directory**

   ```bash
   mkdir project
   cd project
   mkdir server
   code .
   ```

2. **Navigate to the `server` Directory**

   ```bash
   cd server
   ```

3. **Install Dependencies**

   Use `pipenv` to install the required Python packages:

   ```bash
   pipenv install flask flask_cors flask_restful
   ```

4. **Activate the Virtual Environment**

   ```bash
   pipenv shell
   ```

5. **Create the Application File**

   Inside the `server` directory, create a file named `app.py` with the following basic structure:

   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def home():
       return "Hello, Flask!"

   if __name__ == "__main__":
       app.run(debug=True)
   ```

6. **Run the Application**

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

   You should see the message: `Hello, Flask!`

---

## Notes

- Always activate the virtual environment (`pipenv shell`) before running Flask commands.
- For further debugging, ensure the `FLASK_APP` environment variable is correctly set.

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pipenv Documentation](https://pipenv.pypa.io/)