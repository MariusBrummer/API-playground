import requests
import uuid
from utils.check import Check
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://gorest.co.in/public/v2"
HEADERS = {
    "Authorization": "Bearer 57621ecf98c8e77b78140f5cf2a77ce536fd44f535f19ca904fb87b1803492c4",
    "Accept": "application/json"
}

def create_user(user_data, check: Check):
    """
    Function to create a user using the provided data.
    Returns the user ID and the full API response.
    """
    # Update the email field to use a unique UUID
    unique_email = f"{uuid.uuid4()}@example.com"
    user_data["email"] = unique_email

    logger.info("Creating user with data: %s", user_data)  # Log the data being sent

    response = requests.post(f"{BASE_URL}/users", headers=HEADERS, json=user_data)
    logger.info("Create User Response: %s", response.json())  # Log the response for debugging

    check(response.status_code == 201, "Expected status code 201 for successful user creation")

    if isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to create user: {response.json()}")

    user_id = response.json().get("id")
    check(user_id is not None, "User ID should not be None")

    # Assert that the email in the response matches the email sent in the request
    response_email = response.json().get("email")
    check(response_email == unique_email, "Email in the response should match the email sent in the request")
    
    return user_id, response.json()

def get_user_by_id(user_id, check: Check):
    """
    Function to retrieve user details by user ID.
    Returns the user details as a JSON object.
    """
    logger.info("Retrieving user with ID: %s", user_id)  # Log the user ID being retrieved

    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    logger.info("Get User Response: %s", response.json())  # Log the response for debugging

    check(response.status_code == 200, "Expected status code 200 for successful user retrieval")

    if isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to retrieve user: {response.json()}")

    return response.json()