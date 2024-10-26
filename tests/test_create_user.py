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
    logger.info("Loading test data from: %s", json_file)
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
    return test_data.get("users", [])[0]


def test_create_user(user_data, check):
    """
    Test the create_user function.
    """
    user_id, response_data = create_user(user_data, check)

    check(user_id is not None, "User ID should not be None.")
    check(response_data is not None, "Response data should not be None.")
    logger.info("User created successfully with ID: %s", user_id)

    errors = check.consume_errors()
    assert not errors, f"Errors occurred: {errors}"

    # Cleanup
    cleanup_user(user_id, check)
