# Eneco# Eneco

## Description
This repository contains a test suite for the Eneco project. The test suite includes various tests to ensure the functionality of the API endpoints.

## Setup Instructions

### Prerequisites
- Python 3.x
- `pip` (Python package installer)

### Dependencies
Install the required dependencies using the following command:
```bash
pip install -r requirements.txt

Configuration
Ensure you have the necessary configuration files in place. For example, the json_repo directory should contain the users.json file with the test data.

Test Suite Structure
The test suite is organized as follows:

tests/: Contains all the test files.
test_create_user.py: Tests for creating a user.
test_get_user_by_id.py: Tests for retrieving a user by ID.
test_update_user.py: Tests for updating user details.
utils/: Contains utility functions and classes.
commands.py: Contains functions to interact with the API (create, get, update, delete users).
check.py: Contains the Check class for assertions.
How to Execute the Tests
Run the tests using pytest. You can execute all tests with the following command:

To run a specific test file, use:

Additional Information
Ensure the API base URL and headers are correctly configured in commands.py.
The users.json file should contain valid user data for testing.
Example users.json File
