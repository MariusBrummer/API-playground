import os
import requests
import uuid
from utils.check import Check
import logging
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = "https://gorest.co.in/public/v2"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GOREST_BEARER_TOKEN')}",
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
    check(response_email == unique_email,
          "Email in the response should match the email sent in the request")

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


def delete_user(user_id, check: Check):
    """
    Function to delete a user by user ID.
    Returns a success message if the user is deleted.
    """
    logger.info("Deleting user with ID: %s", user_id)  # Log the user ID being deleted

    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    logger.info("Delete User Response: %s", response.status_code)  # Log the response status code for debugging

    check(response.status_code == 204, "Expected status code 204 for successful user deletion")

    if response.status_code != 204:  # Handle the case where the API returns an error message
        check(False, f"Failed to delete user: {response.json()}")

    return "User successfully deleted"


def update_user_details(user_id, user_data, check: Check):
    """
    Function to update user details by user ID.
    Returns the updated user details as a JSON object.
    """
    logger.info("Updating user with ID: %s and data: %s", user_id, user_data)  # Log the user ID and data being updated

    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=HEADERS, json=user_data)
    logger.info("Update User Response: %s", response.json())  # Log the response for debugging

    check(response.status_code == 200, "Expected status code 200 for successful user update")

    if isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to update user: {response.json()}")

    return response.json()


def get_user_posts(user_id, check: Check):
    """
    Function to retrieve posts for a user by user ID.
    Returns the list of posts as a JSON object.
    """
    logger.info("Retrieving posts for user with ID: %s", user_id)

    response = requests.get(f"{BASE_URL}/users/{user_id}/posts", headers=HEADERS)
    logger.info("Get User Posts Response: %s", response.json())

    check(response.status_code == 200, "Expected status code 200 for successful retrieval of user posts")

    if not isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to retrieve user posts: {response.json()}")

    return response.json()


def get_post_comments(post_id, check: Check):
    """
    Function to retrieve comments for a post by post ID.
    Returns the list of comments as a JSON object.
    """
    logger.info("Retrieving comments for post with ID: %s", post_id)

    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS)
    logger.info("Get Post Comments Response: %s", response.json())

    check(response.status_code == 200, "Expected status code 200 for successful retrieval of post comments")

    if not isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to retrieve post comments: {response.json()}")

    return response.json()


def get_user_todos(user_id, check: Check):
    """
    Function to retrieve todos for a user by user ID.
    Returns the list of todos as a JSON object.
    """
    logger.info("Retrieving todos for user with ID: %s", user_id)

    response = requests.get(f"{BASE_URL}/users/{user_id}/todos", headers=HEADERS)
    logger.info("Get User Todos Response: %s", response.json())

    check(response.status_code == 200, "Expected status code 200 for successful retrieval of user todos")

    if not isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to retrieve user todos: {response.json()}")

    return response.json()


def create_user_post(user_id, post_data, check: Check):
    """
    Function to create a post for a user by user ID.
    Returns the created post details as a JSON object.
    """
    logger.info("Creating post for user with ID: %s and data: %s", user_id, post_data)

    response = requests.post(f"{BASE_URL}/users/{user_id}/posts", headers=HEADERS, json=post_data)
    logger.info("Create User Post Response: %s", response.json())

    check(response.status_code == 201, "Expected status code 201 for successful post creation")

    if isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to create user post: {response.json()}")

    return response.json()


def create_post_comment(post_id, comment_data, check: Check):
    """
    Function to create a comment for a post by post ID.
    Returns the created comment details as a JSON object.
    """
    logger.info("Creating comment for post with ID: %s and data: %s", post_id, comment_data)

    response = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
    logger.info("Create Post Comment Response: %s", response.json())

    check(response.status_code == 201, "Expected status code 201 for successful comment creation")

    if isinstance(response.json(), list):  # Handle the case where the API returns an error message
        check(False, f"Failed to create post comment: {response.json()}")

    return response.json()


def cleanup_user(user_id, check: Check):
    """
    Function to clean up by deleting the created user.
    """
    if user_id:
        delete_user(user_id, check)
        logger.info("User deleted successfully with ID: %s", user_id)

        # Consume and print errors if any during deletion
        errors = check.consume_errors()
        check(not errors, f"Errors occurred during deletion: {errors}")
