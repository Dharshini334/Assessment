# Flask API Project

This is a Flask-based API that provides various endpoints with OpenAPI documentation and logging.

## 🚀 Features

- RESTful API endpoints
- OpenAPI documentation using Flasgger
- Logging for debugging
- Unit tests using `pytest`

---

## 📌 Setup and Installation

### 1️⃣ Clone the repository

``sh
git clone https://github.com/YOUR_GITHUB_USERNAME/flask-api-project.git
cd flask-api-project

Create and activate environment
python -m venv venv
source venv/bin/activate


Install Dependencies
pip install -r requirements.txt
poetry install


Running FlaskAPI
Run the application - flask run
Run app module - FLASK_APP=app.py flask run

API Endpoints
/api/data - Returns data
/api/users/summary - Fetch user summary


Running tests
pytest

Logging
Logs are stores in app.log

API Documentation
http://127.0.0.1:5000/apidocs/
