import json
from pathlib import Path
import pytest
import uuid
from utils.commands import create_user, create_user_post, create_post_comment, get_post_comments,  cleanup_user
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
        "name": "Test User Comments",
        "email": f"{uuid.uuid4()}@example.com",
        "body": "Sample comment body."
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

    # Return user_id and post_id for use in other tests
    return user_id, post_id

def test_get_user_comments(test_data):
    """
    Test the get_post_comments function.
    """
    # Use the user and post created in the test_create_user_comment function
    user_id, post_id = test_create_user_comment(test_data)
    check = Check()

    # Retrieve the comments for the post
    post_comments = get_post_comments(post_id, check)
    check(len(post_comments) > 0, "Post should have at least one comment")
    check(post_comments[0]["name"] == "Test User Comments", "Retrieved comment name should match the created comment name")
    check(post_comments[0]["body"] == "Sample comment body.", "Retrieved comment body should match the created comment body")
    logger.info("Post comments retrieved successfully for post ID: %s", post_id)
 
    # Consume and print errors if any
    errors = check.consume_errors()
    check(not errors, f"Errors occurred: {errors}")

    # Clean up by deleting the created user
    cleanup_user(user_id, check)