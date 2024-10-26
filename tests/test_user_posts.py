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
def user(check, test_data):
    """
    Fixture to create a user and ensure cleanup after the test.
    """
    user_data = test_data.get("users", [{}])[0]
    assert user_data, "No user data found in test data."

    user_id, _ = create_user(user_data, check)
    check(user_id is not None, "User ID should not be None.")
    logger.info(f"User created successfully with ID: {user_id}")

    yield user_id

    # Cleanup the user after the test
    cleanup_user(user_id, check)

def test_create_post(user, check):
    """
    Test creating a post for a user.
    """
    post_data = {
        "title": "Sample Post Title",
        "body": "This is a sample post body."
    }
    post_id, response_data = create_user_post(user, post_data, check)
    check(response_data.get("title") == post_data["title"],
          f"Post title should be created correctly. Expected: {post_data['title']}, Actual: {response_data.get('title')}")
    check(response_data.get("body") == post_data["body"],
          f"Post body should be created correctly. Expected: {post_data['body']}, Actual: {response_data.get('body')}")
    check(post_id is not None, "Post ID should not be None.")
    logger.info(f"Post created successfully for user ID: {user}")

    # Confirm no errors occurred during creation
    errors = check.consume_errors()
    assert not errors, f"Errors occurred during post creation: {errors}"

def test_get_post(user, check):
    """
    Test retrieving posts for a user.
    """
    # Create a post for the user first
    post_data = {
        "title": "Sample Post Title",
        "body": "This is a sample post body."
    }
    post_id, _ = create_user_post(user, post_data, check)

    # Retrieve the posts for the user
    user_posts = get_user_posts(user, check)
    check(len(user_posts) > 0, "User should have at least one post.")

    # Check the retrieved post details
    retrieved_post = user_posts[0]
    check(retrieved_post.get("title") == post_data["title"],
          f"Retrieved post title should match the created post title. Expected: {post_data['title']}, Actual: {retrieved_post.get('title')}")
    check(retrieved_post.get("body") == post_data["body"],
          f"Retrieved post body should match the created post body. Expected: {post_data['body']}, Actual: {retrieved_post.get('body')}")

    logger.info(f"User posts retrieved successfully for user ID: {user}")

    # Confirm no errors occurred during retrieval
    errors = check.consume_errors()
    assert not errors, f"Errors occurred during post retrieval: {errors}"
