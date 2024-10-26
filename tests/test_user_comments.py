import json
from pathlib import Path
import pytest
import uuid
import logging
from utils.fixtures import (create_user, create_user_post, create_post_comment,
                            get_post_comments, cleanup_user)
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
    Returns user_id and post_id for further tests.
    """
    # Set up user data
    user_data = test_data.get("users", [{}])[0]
    assert user_data, "No user data found in test data."

    # Create a user
    user_id, create_user_response = create_user(user_data, check)
    if user_id is None:
        logger.error(f"User creation failed: {create_user_response}")
        pytest.fail("User creation failed due to invalid token.")

    check(user_id is not None, "User ID should not be None.")
    logger.info(f"User created successfully with ID: {user_id}")

    # Create a post for the user
    post_data = {
        "title": "Sample Post Title",
        "body": "This is a sample post body."
    }
    created_post_id, created_post_response = create_user_post(user_id, post_data, check)

    # Check the response format
    if not isinstance(created_post_response, dict):
        logger.error(f"Post creation failed: {created_post_response}")
        pytest.fail("Post creation failed due to invalid token.")

    check(created_post_response.get("title") == post_data["title"],
          f"Post title should be created correctly. Expected: {post_data['title']}, Actual: {created_post_response.get('title')}")
    check(created_post_response.get("body") == post_data["body"],
          f"Post body should be created correctly. Expected: {post_data['body']}, Actual: {created_post_response.get('body')}")
    check(created_post_response.get("id") is not None, "Post ID should not be None.")
    
    post_id = created_post_response["id"]
    logger.info(f"Post created successfully for user ID: {user_id}")

    yield user_id, post_id

    # Teardown: Clean up the user after the test
    cleanup_user(user_id, check)

def test_create_comment(user_with_post, check):
    """
    Test creating a comment for a post.
    """
    user_id, post_id = user_with_post
    comment_data = {
        "name": "Test User Comments",
        "email": f"{uuid.uuid4()}@example.com",
        "body": "Sample comment body."
    }

    created_comment_id, created_comment_response = create_post_comment(post_id, comment_data, check)

    # Check the comment response
    if not isinstance(created_comment_response, dict):
        logger.error(f"Comment creation failed: {created_comment_response}")
        pytest.fail("Comment creation failed due to invalid token.")

    check(created_comment_response.get("name") == comment_data["name"],
          f"Comment name should be created correctly. Expected: {comment_data['name']}, Actual: {created_comment_response.get('name')}")
    check(created_comment_response.get("email") == comment_data["email"],
          f"Comment email should be created correctly. Expected: {comment_data['email']}, Actual: {created_comment_response.get('email')}")
    check(created_comment_response.get("body") == comment_data["body"],
          f"Comment body should be created correctly. Expected: {comment_data['body']}, Actual: {created_comment_response.get('body')}")
    check(created_comment_response.get("id") is not None, "Comment ID should not be None.")
    logger.info(f"Comment created successfully for post ID: {post_id}")

    # Confirm no errors occurred during creation
    errors = check.consume_errors()
    assert not errors, f"Errors occurred during comment creation: {errors}"

def test_get_comments(user_with_post, check):
    """
    Test retrieving comments for a post.
    """
    user_id, post_id = user_with_post

    # Create a comment for the post first
    comment_data = {
        "name": "Test User Comments",
        "email": f"{uuid.uuid4()}@example.com",
        "body": "Sample comment body."
    }
    create_post_comment(post_id, comment_data, check)

    # Retrieve the comments for the post
    post_comments = get_post_comments(post_id, check)
    check(len(post_comments) > 0, "Post should have at least one comment.")

    # Check the retrieved comment
    check(post_comments[0].get("name") == comment_data["name"],
          f"Retrieved comment name should match the created comment name. Expected: '{comment_data['name']}', Actual: '{post_comments[0].get('name')}'")
    check(post_comments[0].get("body") == comment_data["body"],
          f"Retrieved comment body should match the created comment body. Expected: '{comment_data['body']}', Actual: '{post_comments[0].get('body')}'")

    logger.info(f"Post comments retrieved for post ID: {post_id}")

    # Confirm no errors occurred during retrieval
    errors = check.consume_errors()
    assert not errors, f"Errors occurred during comment retrieval: {errors}"
