import json
from pathlib import Path
import pytest
import logging
from utils.fixtures import create_user, create_user_post, get_user_posts, cleanup_user
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
    logger.info(f"Loading test data from: {json_file}")
    assert json_file.exists(), f"{json_file} does not exist. Check the path."

    with json_file.open() as f:
        data = json.load(f)
        logger.info("Test data loaded successfully.")
        yield data

@pytest.fixture
def user_with_post(test_data, check):
    """
    Fixture to create a user and a post for that user.
    Returns the user_id and post_data for further tests.
    """
    # Set up user data
    user_data = test_data.get("users", [{}])[0]
    assert user_data, "No user data found in test data."

    # Create a user
    user_id, _ = create_user(user_data, check)
    check(user_id is not None, "User ID should not be None.")
    logger.info(f"User created successfully with ID: {user_id}")

    # Create a post for the user
    post_data = {
        "title": "Sample Post Title",
        "body": "This is a sample post body."
    }
    post_id, response_data = create_user_post(user_id, post_data, check)  # Update this line
    check(response_data.get("title") == post_data["title"], "Post title should be created correctly.")
    check(response_data.get("body") == post_data["body"], "Post body should be created correctly.")
    check(post_id is not None, "Post ID should not be None.")
    logger.info(f"Post created successfully for user ID: {user_id}")

    # Verify no errors occurred during user and post creation
    errors = check.consume_errors()
    assert not errors, f"Errors occurred during setup: {errors}"

    # Teardown: Clean up the user after the test
    yield user_id, post_data
    cleanup_user(user_id, check)

def test_get_user_posts(user_with_post, check):
    """
    Test the get_user_posts function.
    """
    user_id, post_data = user_with_post

    # Retrieve the posts for the user
    user_posts = get_user_posts(user_id, check)
    check(len(user_posts) > 0, "User should have at least one post.")
    check(user_posts[0].get("title") == post_data["title"], "Retrieved post title should match the created post title.")
    check(user_posts[0].get("body") == post_data["body"], "Retrieved post body should match the created post body.")
    logger.info(f"User posts retrieved successfully for user ID: {user_id}")

    # Confirm no errors occurred during retrieval
    errors = check.consume_errors()
    assert not errors, f"Errors occurred: {errors}"
