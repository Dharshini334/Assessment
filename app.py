from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Enables Swagger UI


@app.route("/hello", methods=["GET"])
def hello():
    """
    Example Hello API
    ---
    tags:
      - Example API
    responses:
      200:
        description: A simple hello world response
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Hello, World!"
    """
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
