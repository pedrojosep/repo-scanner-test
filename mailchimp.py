from flask import Flask, request, jsonify
import mailchimp_marketing as Mailchimp
from mailchimp_marketing.api_client import ApiClientError

app = Flask(__name__)

# Mailchimp configuration (replace with your actual details)
mailchimp_client = Mailchimp.Client()
mailchimp_client.set_config(
    {
        "api_key": "your_mailchimp_api_key",
        "server": "your_mailchimp_server_prefix",  # e.g., 'us1', 'us2', etc.
    }
)

MAILCHIMP_AUDIENCE_ID = "your_mailchimp_audience_id"


# Function to add user to Mailchimp audience
def add_to_mailchimp(user_data):
    member_info = {
        "email_address": user_data["email"],
        "status": "subscribed",  # Use 'pending' for double opt-in
        "merge_fields": {
            "FNAME": user_data["first_name"],
            "LNAME": user_data["last_name"],
        },
    }
    try:
        response = mailchimp_client.lists.add_list_member(
            MAILCHIMP_AUDIENCE_ID, member_info
        )
        return response
    except ApiClientError as error:
        return error.text


# Endpoint to receive user data
@app.route("/add_user_to_mailchimp", methods=["POST"])
def add_user_to_mailchimp():
    user_data = request.json

    # Check if all required fields are in the received data
    if not all(k in user_data for k in ("first_name", "last_name", "email")):
        return jsonify({"message": "Missing data fields"}), 400

    # Add user to Mailchimp
    response = add_to_mailchimp(user_data)

    if "title" in response and response["title"] == "Member Exists":
        return (
            jsonify({"message": "User already exists in the Mailchimp audience"}),
            200,
        )
    elif "status" in response and response["status"] == "subscribed":
        return (
            jsonify({"message": "User added to Mailchimp audience successfully"}),
            200,
        )
    else:
        return (
            jsonify({"message": "Failed to add user to Mailchimp", "error": response}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
