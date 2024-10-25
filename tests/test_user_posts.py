import json
from pathlib import Path
import pytest
from utils.commands import (create_user, create_user_post, get_user_posts,
                            cleanup_user)
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


def test_create_user_post(test_data):
    """
    Test the create_user_post function.
    """
    user_data = test_data["users"][0]  # Use the first user in the JSON file
    check = Check()

    # Call the create_user function to create a user
    user_id, _ = create_user(user_data, check)

    check(user_id is not None, "User ID should not be None")
    logger.info("User created successfully with ID: %s", user_id)

    # Create a post for the user
    post_data = {
        "title": "Sample Post Title",
        "body": "This is a sample post body."
    }
    created_post = create_user_post(user_id, post_data, check)
    check(created_post["title"] == post_data["title"],
          "Post title should be created correctly")
    check(created_post["body"] == post_data["body"],
          "Post body should be created correctly")
    check(created_post["id"] is not None, "Post ID should not be None")
    logger.info("Post created successfully for user ID: %s", user_id)

    # Consume and print errors if any
    errors = check.consume_errors()
    check(not errors, f"Errors occurred: {errors}")

    # Return user_id and post_data for use in other tests
    return user_id, post_data


def test_get_user_posts(test_data):
    """
    Test the get_user_posts function.
    """
    # Use the user and post created in the test_create_user_post function
    user_id, post_data = test_create_user_post(test_data)
    check = Check()

    # Retrieve the posts for the user
    user_posts = get_user_posts(user_id, check)
    check(len(user_posts) > 0, "User should have at least one post")
    check(user_posts[0]["title"] == post_data["title"],
          "Retrieved post title should match the created post title")
    check(user_posts[0]["body"] == post_data["body"],
          "Retrieved post body should match the created post body")
    logger.info("User posts retrieved successfully for user ID: %s", user_id)

    # Consume and print errors if any
    errors = check.consume_errors()
    assert not errors, f"Errors occurred: {errors}"

    # Clean up by deleting the created user
    cleanup_user(user_id, check)
