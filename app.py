import logging
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Enables Swagger UI

# Configure logging
logging.basicConfig(
    filename="app.log",  # Logs saved to app.log
    level=logging.DEBUG,  # Log everything (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@app.route("/")
def home():
    logging.info("Home route accessed")  # Log INFO message
    return "Welcome to the API"


@app.route("/api/data")
def api_data():
    logging.debug("Fetching API data")  # Log DEBUG message
    return jsonify({"message": "Here is your data"}), 200


@app.route("/hello", methods=["GET"])
def hello():
    logging.warning("Hello route accessed")  # Log WARNING message
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
