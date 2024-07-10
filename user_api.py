from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)


# Function to insert data into the database
def store_user_data(user_data):
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


# Function to handle sensitive transaction
def handle_transaction(card_info):
    conn = sqlite3.connect("sensitive_transactions.db")
    cursor = conn.cursor()

    query = "INSERT INTO transactions (card_info) VALUES (?)"
    cursor.execute(query, (card_info,))

    conn.commit()
    cursor.close()
    conn.close()
    print("Sensitive transaction processed.")


# Function to forward authentication data
def forward_auth_data(username, secret):
    api_url = "https://example.com/api/store_auth_data"
    auth_data = {"username": username, "secret": secret}

    response = requests.post(api_url, json=auth_data)

    if response.status_code == 200:
        print("Authentication data forwarded successfully.")
    else:
        print("Failed to forward authentication data.")


# Endpoint to receive user data
@app.route("/submit_user_data", methods=["POST"])
def submit_user_data():
    # Expecting JSON data in the format: {'name': '...', 'email': '...', 'phone_number': '...', 'credit_card': '...', 'username': '...', 'password': '...'}
    user_data = request.json

    # Check if all required fields are in the received data
    required_fields = [
        "name",
        "email",
        "phone_number",
        "credit_card",
        "username",
        "password",
    ]
    if any(k not in user_data for k in required_fields):
        return jsonify({"message": "Missing data fields"}), 400

    # Store the received data in the database
    store_user_data(user_data)

    # Handle sensitive transaction
    handle_transaction(user_data["credit_card"])

    # Forward authentication data
    forward_auth_data(user_data["username"], user_data["password"])

    return jsonify({"message": "User data received and processed successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
