import json
from pathlib import Path
import pytest
from utils.commands import create_user, get_user_by_id, cleanup_user
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


def test_get_user_by_id(test_data):
    """
    Test the get_user_by_id function.
    """
    user_data = test_data["users"][0]  # Use the first user in the JSON file
    check = Check()

    # Call the create_user function to create a user
    user_id, _ = create_user(user_data, check)

    check(user_id is not None, "User ID should not be None")
    logger.info("User created successfully with ID: %s", user_id)

    # Retrieve the user by ID
    user_details = get_user_by_id(user_id, check)
    check(user_details["id"] == user_id,
          "Retrieved user ID should match the created user ID")
    logger.info("User retrieved successfully with ID: %s", user_id)

    # Consume and print errors if any
    errors = check.consume_errors()
    assert not errors, f"Errors occurred: {errors}"

    # Clean up by deleting the created user
    cleanup_user(user_id, check)
