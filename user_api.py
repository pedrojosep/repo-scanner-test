from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# Function to insert data into the database
def insert_into_database(user_data):
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    # Insert query
    query = "INSERT INTO users (name, email, phone_number) VALUES (?, ?, ?)"
    cursor.execute(
        query, (user_data["name"], user_data["email"], user_data["phone_number"])
    )

    conn.commit()
    cursor.close()
    conn.close()


# Endpoint to receive user data
@app.route("/receive_user_data", methods=["POST"])
def receive_user_data():
    # Expecting JSON data in the format: {'name': '...', 'email': '...', 'phone_number': '...'}
    user_data = request.json

    # Check if all required fields are in the received data
    if not all(k in user_data for k in ("name", "email", "phone_number")):
        return jsonify({"message": "Missing data fields"}), 400

    # Insert the received data into the database
    insert_into_database(user_data)

    return jsonify({"message": "User data received and stored successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
