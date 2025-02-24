from flask import Flask, request, jsonify
import psycopg2
import json
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQL Connection Details
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "DB123@hpe456"

# Establish a connection function
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/upload-json', methods=['POST'])
def upload_json():
    try:
        # Check if file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        json_data = json.load(file)  # Load JSON file

        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert data in bulk for efficiency
        insert_query = """
            INSERT INTO employeeDetails (first_name, last_name, company_name, city, state, zip, email, web, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Convert JSON data into tuples
        records = [
            (
                record.get("first_name"),
                record.get("last_name"),
                record.get("company_name"),
                record.get("city"),
                record.get("state"),
                record.get("zip"),
                record.get("email"),
                record.get("web"),
                record.get("age")
            ) for record in json_data
        ]

        # Execute bulk insert
        cursor.executemany(insert_query, records)

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": f"{len(records)} records inserted successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))  # Default page is 1
        limit = int(request.args.get('limit', 5))  # Default limit is 5
        search = request.args.get('search', '').strip().lower()  # Search string
        sort = request.args.get('sort', 'id')  # Default sorting by id

        # Define sorting field and order
        sort_order = "ASC"
        if sort.startswith("-"):
            sort_order = "DESC"
            sort = sort[1:]  # Remove "-" for field name

        # Ensure the sorting field is valid
        allowed_sort_fields = ["id", "first_name", "last_name", "age", "email", "city", "state"]
        if sort not in allowed_sort_fields:
            return jsonify({"error": "Invalid sort field"}), 400

        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Base Query
        query = "SELECT * FROM employeeDetails WHERE TRUE"
        params = []

        # Apply Search
        if search:
            query += " AND (LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])

        # Apply Sorting
        query += f" ORDER BY {sort} {sort_order}"

        # Apply Pagination
        offset = (page - 1) * limit
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        # Execute Query
        cursor.execute(query, params)
        users = cursor.fetchall()

        # Close connections
        cursor.close()
        connection.close()

        return app.response_class(
            response=json.dumps({"page": page, "limit": limit, "users": users}, indent=4),
            status=200,
            mimetype="application/json"
        )


    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users',methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()

        required_fields = ["first_name", "last_name", "company_name", "city", "state", "zip", "email", "web", "age"]
        if not all(field in user_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO employeeDetails (first_name, last_name, company_name, city, state, zip, email, web, age)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """, (
                user_data["first_name"], user_data["last_name"], user_data["company_name"],
                user_data["city"], user_data["state"], user_data["zip"], user_data["email"],
                user_data["web"], user_data["age"]
        ))

        connection.commit()

        user_id = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Employee created successfully",
            "id": user_id,
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "email": user_data["email"]
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Fetch user by ID
        cursor.execute("SELECT * FROM employeeDetails WHERE id = %s;", (id,))
        user = cursor.fetchone()

        # Close connections
        cursor.close()
        connection.close()

        # If user not found
        if not user:
            return jsonify({"error": "User not found"}), 404

        return app.response_class(
            response=json.dumps(user, indent=4),  # Pretty-printed JSON
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user_data = request.get_json()

        # Validate required fields
        required_fields = ["first_name", "last_name", "company_name", "city", "state", "zip", "email", "web", "age"]
        if not all(field in user_data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Update query
        cursor.execute("""
            UPDATE employeeDetails
            SET first_name = %s, last_name = %s, company_name = %s, city = %s, state = %s,
                zip = %s, email = %s, web = %s, age = %s
            WHERE id = %s RETURNING id;
        """, (
            user_data["first_name"], user_data["last_name"], user_data["company_name"],
            user_data["city"], user_data["state"], user_data["zip"], user_data["email"],
            user_data["web"], user_data["age"], id
        ))

        updated_user = cursor.fetchone()

        if not updated_user:
            return jsonify({"error": "User not found"}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            "message": "User updated successfully",
            "id": id,
            "updated_data": user_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM employeeDetails WHERE id = %s;", (id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete the user
        cursor.execute("DELETE FROM employeeDetails WHERE id = %s;", (id,))
        connection.commit()

        # Close connections
        cursor.close()
        connection.close()

        return jsonify({"message": f"User with ID {id} deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users/<int:id>', methods=['PATCH'])
def patch_user(id):
    try:
        # Get the request data
        user_data = request.get_json()
        if not user_data:
            return jsonify({"error": "No data provided"}), 400

        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM employeeDetails WHERE id = %s;", (id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Generate dynamic query
        update_fields = []
        values = []

        for field in user_data:
            if field in ["first_name", "last_name", "company_name", "city", "state", "zip", "email", "web", "age"]:
                update_fields.append(f"{field} = %s")
                values.append(user_data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # Construct SQL query
        query = f"UPDATE employeeDetails SET {', '.join(update_fields)} WHERE id = %s;"
        values.append(id)

        # Execute query
        cursor.execute(query, tuple(values))
        connection.commit()

        # Close connections
        cursor.close()
        connection.close()

        return jsonify({"message": f"User with ID {id} updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/users/summary', methods=['GET'])
def get_user_summary():
    try:
        # Connect to PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get total user count
        cursor.execute("SELECT COUNT(*) FROM employeeDetails;")
        total_users = cursor.fetchone()[0]

        # Get count of users by city
        cursor.execute("SELECT city, COUNT(*) FROM employeeDetails GROUP BY city ORDER BY COUNT(*) DESC;")
        city_counts = cursor.fetchall()
        city_summary = [{"city": row[0], "count": row[1]} for row in city_counts]

        # Get average age
        cursor.execute("SELECT AVG(age) FROM employeeDetails;")
        avg_age = cursor.fetchone()[0]
        avg_age = float(avg_age) if avg_age else None


        # Close connections
        cursor.close()
        connection.close()

        # Return formatted JSON response
        return app.response_class(
            response=json.dumps({
                "total_users": total_users,
                "average_age": round(avg_age, 2) if avg_age else None,
                "users_by_city": city_summary
            }, indent=4),  # Formatting with indentation
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
