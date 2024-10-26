import json
from pathlib import Path
import pytest
import logging
from utils.fixtures import create_user, get_user_by_id, cleanup_user
from utils.check import Check

# Define the path to the JSON repository
json_repo_dir = Path(__file__).resolve().parent.parent / "json_repo"

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module", params=["users.json"])
def test_data(request):
    """
    Fixture to load test data from a JSON file.
    """
    json_file = json_repo_dir / request.param
    logger.info("Loading test data from: %s", json_file)
    assert json_file.exists(), f"{json_file} does not exist. Check the path."

    with json_file.open() as f:
        data = json.load(f)
        logger.info("Test data loaded successfully.")
        yield data

@pytest.fixture
def user_data(test_data):
    """
    Fixture to provide user data from test data.
    """
    users = test_data.get("users")
    assert users and isinstance(users, list), "Expected 'users' key with a list of users in the test data."
    return users[0]

def test_get_user_by_id(user_data, check):
    """
    Test the get_user_by_id function.
    """
    # Create a user
    user_id, _ = create_user(user_data, check)
    check(user_id is not None, f"User ID should not be None. Actual value: {user_id}")
    logger.info("User created successfully with ID: %s", user_id)

    # Retrieve the user by ID
    user_details = get_user_by_id(user_id, check)
    check(user_details.get("id") == user_id, 
          f"Retrieved user ID should match the created user ID. Expected: {user_id}, Actual: {user_details.get('id')}")
    logger.info("User retrieved successfully with ID: %s", user_id)

    # Check for any accumulated errors
    errors = check.consume_errors()
    assert not errors, f"Errors occurred: {errors}"

    # Clean up by deleting the created user
    cleanup_user(user_id, check)
    logger.info("User cleanup completed for ID: %s", user_id)
