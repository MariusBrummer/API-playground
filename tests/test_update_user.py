import json
from pathlib import Path
import pytest
import uuid
import logging
from utils.fixtures import create_user, update_user_details, cleanup_user
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

def test_update_user_details(test_data):
    """
    Test the update_user_details function.
    """
    # Get initial user data and create a Check instance
    user_data = test_data.get("users", [{}])[0]
    assert user_data, "No user data found in test data."
    check = Check()

    # Create a user
    user_id, _ = create_user(user_data, check)
    check(user_id is not None, "User ID should not be None.")
    logger.info("User created successfully with ID: %s", user_id)

    # Prepare and update user details
    updated_data = {
        "name": "Updated Name",
        "email": f"{uuid.uuid4()}@example.com",
        "gender": "male",
        "status": "active"
    }
    updated_user_details = update_user_details(user_id, updated_data, check)
    check(updated_user_details.get("name") == updated_data["name"], "User name should be updated.")
    check(updated_user_details.get("email") == updated_data["email"], "User email should be updated.")
    logger.info("User updated successfully with ID: %s", user_id)

    # Check for errors and assert if any exist
    errors = check.consume_errors()
    assert not errors, f"Errors occurred: {errors}"

    # Clean up by deleting the created user
    cleanup_user(user_id, check)
    logger.info("User cleanup completed for ID: %s", user_id)
