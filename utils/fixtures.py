import os
import requests
import uuid
import logging
from dotenv import load_dotenv
from utils.check import Check

# Load environment variables from .env file if present
load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = "https://gorest.co.in/public/v2"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GOREST_BEARER_TOKEN')}",
    "Accept": "application/json"
}

def create_user(user_data: dict, check: Check):
    unique_email = f"{uuid.uuid4()}@example.com"
    user_data["email"] = unique_email

    logger.info(f"Creating user with data: {user_data}")

    response = requests.post(f"{BASE_URL}/users", headers=HEADERS, json=user_data)
    response_data = response.json()
    logger.info(f"Create User Response: {response_data}")

    check(response.status_code == 201, "Expected status code 201 for successful user creation.")
    check(isinstance(response_data, dict), f"Unexpected response format: {response_data}")

    user_id = response_data.get("id")
    check(user_id is not None, "User ID should not be None.")
    check(response_data.get("email") == unique_email, "Response email should match the request email.")

    return user_id, response_data

def create_user_post(user_id: int, post_data: dict, check: Check):
    """
    Function to create a post for a specific user.
    
    Parameters:
    - user_id (int): The ID of the user for whom the post is being created.
    - post_data (dict): A dictionary containing the title and body of the post.
    - check (Check): An instance of the Check class for validation of response.

    Returns:
    - tuple: A tuple containing:
        - post_id (int): The ID of the created post.
        - response_data (dict): The full response data from the API.
    """
    logger.info(f"Creating post for user ID: {user_id} with data: {post_data}")

    response = requests.post(f"{BASE_URL}/users/{user_id}/posts", headers=HEADERS, json=post_data)
    response_data = response.json()
    logger.info(f"Create Post Response: {response_data}")

    check(response.status_code == 201, "Expected status code 201 for successful post creation.")
    check(isinstance(response_data, dict), f"Unexpected response format: {response_data}")

    post_id = response_data.get("id")
    check(post_id is not None, "Post ID should not be None.")

    return post_id, response_data  # Returning a tuple with post_id and response_data

def create_post_comment(post_id: int, comment_data: dict, check: Check):
    logger.info(f"Creating comment for post ID: {post_id} with data: {comment_data}")

    response = requests.post(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS, json=comment_data)
    response_data = response.json()
    logger.info(f"Create Comment Response: {response_data}")

    check(response.status_code == 201, "Expected status code 201 for successful comment creation.")
    check(isinstance(response_data, dict), f"Unexpected response format: {response_data}")

    comment_id = response_data.get("id")
    check(comment_id is not None, "Comment ID should not be None.")

    return comment_id, response_data

def get_post_comments(post_id: int, check: Check):
    logger.info(f"Retrieving comments for post ID: {post_id}")

    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments", headers=HEADERS)
    response_data = response.json()
    logger.info(f"Get Comments Response: {response_data}")

    check(response.status_code == 200, "Expected status code 200 for successful retrieval of comments.")
    check(isinstance(response_data, list), f"Unexpected response format: {response_data}")

    return response_data

def get_user_by_id(user_id, check: Check):
    """
    Function to retrieve user details by user ID.
    Returns the user details as a JSON object.
    """
    logger.info(f"Retrieving user with ID: {user_id}")  # Log the user ID being retrieved

    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    response_data = response.json()
    logger.info(f"Get User Response: {response_data}")  # Log the response for debugging

    check(response.status_code == 200, "Expected status code 200 for successful user retrieval")

    if isinstance(response_data, list):  # Handle the case where the API returns an error message
        check(False, f"Failed to retrieve user: {response_data}")

    return response_data

def update_user_details(user_id, user_data, check: Check):
    """
    Function to update user details by user ID.
    Returns the updated user details as a JSON object.
    """
    logger.info(f"Updating user with ID: {user_id} and data: {user_data}")  # Log the user ID and data being updated

    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=HEADERS, json=user_data)
    response_data = response.json()  # Retrieve response data after the request
    logger.info(f"Update User Response: {response_data}")  # Log the response for debugging

    check(response.status_code == 200, "Expected status code 200 for successful user update")

    if isinstance(response_data, list):  # Handle the case where the API returns an error message
        check(False, f"Failed to update user: {response_data}")

    return response_data

def get_user_posts(user_id, check: Check):
    """
    Function to retrieve posts for a user by user ID.
    Returns the list of posts as a JSON object.
    """
    logger.info(f"Retrieving posts for user with ID: {user_id}")

    response = requests.get(f"{BASE_URL}/users/{user_id}/posts", headers=HEADERS)
    response_data = response.json()  # Retrieve response data after the request
    logger.info(f"Get User Posts Response: {response_data}")

    check(response.status_code == 200, "Expected status code 200 for successful retrieval of user posts")

    if not isinstance(response_data, list):  # Handle the case where the API returns an error message
        check(False, f"Failed to retrieve user posts: {response_data}")

    return response_data

def cleanup_user(user_id: int, check: Check):
    if user_id:
        delete_user(user_id, check)
        logger.info(f"User successfully deleted with ID: {user_id}")

        errors = check.consume_errors()
        assert not errors, f"Errors occurred during deletion: {errors}"

# Existing delete_user function
def delete_user(user_id: int, check: Check):
    logger.info(f"Deleting user with ID: {user_id}")

    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
    logger.info(f"Delete User Response status: {response.status_code}")

    check(response.status_code == 204, "Expected status code 204 for successful user deletion.")
    if response.status_code != 204:
        check(False, f"Failed to delete user: {response.json()}")

    return "User successfully deleted"
