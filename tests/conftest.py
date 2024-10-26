import pytest
import logging
from utils.fixtures import create_user, cleanup_user 
from utils.check import Check

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture
def check():
    """
    Fixture to provide a Check instance.
    """
    return Check()

@pytest.fixture
def user(check):
    """
    Fixture to create a user and clean up afterwards.
    """
    user_data = {
        "name": "Test User",
        "email": "test@example.com",  # Placeholder; can be modified in tests
        "gender": "male",
        "status": "active"
    }
    user_id, _ = create_user(user_data, check)
    yield user_id
    cleanup_user(user_id, check)
