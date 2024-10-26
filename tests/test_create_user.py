import json
from pathlib import Path
import pytest
import logging
from utils.fixtures import create_user, cleanup_user
from utils.check import Check

# Setup
json_repo_dir = Path(__file__).resolve().parent.parent / "json_repo"
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module", params=["users.json"])
def test_data(request):
    """
    Fixture to load test data from a JSON file.
    """
    json_file = json_repo_dir / request.param
    logger.info(f"Loading test data from: {json_file}")
    assert json_file.exists(), f"{json_file} does not exist. Check the path."

    with json_file.open() as f:
        data = json.load(f)
        logger.info("Test data loaded successfully")
        yield data

@pytest.fixture
def user_data(test_data):
    """
    Fixture to provide user data from test data.
    """
    return test_data.get("users", [])

def test_create_users(user_data, check):
    """
    Test the create_user function for multiple users.
    """
    created_users = []

    for user in user_data:
        user_id, response_data = create_user(user, check)

        # Use the 'name' key for logging
        check(user_id is not None, f"User ID should not be None for user {user['name']}. Actual value: {user_id}")
        check(response_data is not None, f"Response data should not be None for user {user['name']}. Actual value: {response_data}")

        logger.info(f"User created successfully with ID: {user_id}")

        # Store created user ID for cleanup later
        created_users.append(user_id)

    errors = check.consume_errors()
    assert not errors, f"Errors occurred during user creation: {errors}"

    # Cleanup: Remove created users
    for user_id in created_users:
        cleanup_user(user_id, check)
