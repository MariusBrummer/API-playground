import json
from pathlib import Path
import pytest
import uuid
from utils.commands import create_user, create_user_post, create_post_comment, delete_user
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

def test_create_user_comment(test_data):
    """
    Test the create_post_comment function.
    """
    user_data = test_data["users"][0]  # Use the first user in the JSON file
    check = Check()

    # Call the create_user function to create a user
    user_id, create_user_response = create_user(user_data, check)

    if user_id is None:
        logger.error("User creation failed: %s", create_user_response)
        pytest.fail("User creation failed due to invalid token")

    check(user_id is not None, "User ID should not be None")
    logger.info("User created successfully with ID: %s", user_id)

    # Create a post for the user
    post_data = {
        "title": "Sample Post Title",
        "body": "This is a sample post body."
    }
    created_post = create_user_post(user_id, post_data, check)

    if "title" not in created_post:
        logger.error("Post creation failed: %s", created_post)
        pytest.fail("Post creation failed due to invalid token")

    check(created_post["title"] == post_data["title"], "Post title should be created correctly")
    check(created_post["body"] == post_data["body"], "Post body should be created correctly")
    check(created_post["id"] is not None, "Post ID should not be None or empty")
    post_id = created_post["id"]
    logger.info("Post created successfully for user ID: %s", user_id)

    # Create a comment for the post
    comment_data = {
        "name": "Hiranya Somayaji IV",
        "email": f"{uuid.uuid4()}@example.com",
        "body": "Iste ducimus iusto. Ratione similique aut."
    }
    created_comment = create_post_comment(post_id, comment_data, check)

    if "name" not in created_comment:
        logger.error("Comment creation failed: %s", created_comment)
        pytest.fail("Comment creation failed due to invalid token")

    check(created_comment["name"] == comment_data["name"], "Comment name should be created correctly")
    check(created_comment["email"] == comment_data["email"], "Comment email should be created correctly")
    check(created_comment["body"] == comment_data["body"], "Comment body should be created correctly")
    check(created_comment["id"] is not None, "Comment ID should not be None or empty")
    logger.info("Comment created successfully for post ID: %s", post_id)

    # Consume and print errors if any
    errors = check.consume_errors()
    check(not errors, f"Errors occurred: {errors}")

    # Clean up by deleting the created user
    if user_id:
        delete_user(user_id, check)
        logger.info("User deleted successfully with ID: %s", user_id)

        # Consume and print errors if any during deletion
        errors = check.consume_errors()
        check(not errors, f"Errors occurred during deletion: {errors}")