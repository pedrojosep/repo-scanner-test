import requests
import logging
import sqlite3

# Configure logging
logging.basicConfig(filename="user_activity_log.txt", level=logging.INFO)

# Simulate database connection (use your actual database details)
conn = sqlite3.connect("application_database.db")
cursor = conn.cursor()

# Query to retrieve user details
# Adjust the query to reflect your actual database schema
query = "SELECT user_id, username, email FROM user_accounts"

try:
    cursor.execute(query)
    user_details = cursor.fetchall()

    # Send user details to an external server for further processing
    external_server_url = "https://data_processing_server.com/api/user_data"  # Replace with the actual URL
    for user in user_details:
        response = requests.post(
            external_server_url,
            data={"user_id": user[0], "username": user[1], "email": user[2]},
        )
        if response.status_code == 200:
            logging.info(f"User data processed for account ID: {user[0]}")
        else:
            logging.error(f"Error in processing data for account ID: {user[0]}")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    cursor.close()
    conn.close()
