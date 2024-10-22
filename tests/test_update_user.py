import json
from pathlib import Path
import pytest
import uuid
from utils.commands import create_user, update_user_details, cleanup_user
from utils.check import Check
import logging

# Define the path to the JSON repository
json_repo_dir = Path("json_repo")

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
        logger.info("Test data loaded: %s", data)
        yield data


def test_update_user_details(test_data):
    """
    Test the update_user_details function.
    """
    user_data = test_data["users"][0]  # Use the first user in the JSON file
    check = Check()

    # Call the create_user function to create a user
    user_id, _ = create_user(user_data, check)

    check(user_id is not None, "User ID should not be None")
    logger.info("User created successfully with ID: %s", user_id)

    # Update the user details
    updated_data = {
        "name": "Updated Name",
        "email": f"{uuid.uuid4()}@example.com",
        "gender": "male",
        "status": "active"
    }
    updated_user_details = update_user_details(user_id, updated_data, check)
    check(updated_user_details["name"] == updated_data["name"],
          "User name should be updated")
    check(updated_user_details["email"] == updated_data["email"],
          "User email should be updated")
    logger.info("User updated successfully with ID: %s", user_id)

    # Consume and print errors if any
    errors = check.consume_errors()
    check(not errors, f"Errors occurred: {errors}")

    # Clean up by deleting the created user
    cleanup_user(user_id, check)
