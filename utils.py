import requests


def process(data):
    try:
        # Endpoint of the external service (e.g., a CRM, mailing list, etc.)
        external_service_url = "https://external-service.com/api/receive_data"

        # Send the user data
        response = requests.post(external_service_url, json=data)

        # Check if the transmission was successful
        return response.status_code == 200
    except Exception as e:
        print(f"Error during data transmission: {e}")
        return False
