# API playground

## Description

This repository contains a test suite for the Eneco project. The test suite includes various tests to ensure the functionality of the API endpoints.

## Setup Instructions

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Dependencies

You can install the required dependencies using the `install.py` script provided in the repository.

#### Windows

Run the following command to install the dependencies:

```bash
python install.py
```

### Linux and MacOS (NOT TESTED ON THESE PLATFORMS)

```bash
python3 install.py
```

### Configuration

Ensure you have the necessary configuration files in place. For example, the `json_repo` directory should contain the `users.json` file with the test data.

### Environment Variables

Create a .env file in the root directory of the project and add the following environment variables:

```bash
GOREST_BEARER_TOKEN=<your_bearer_token>
```

## Test Suite Structure

The test suite is organized as follows:

- `tests/`: Contains all the test files.
  - `test_create_user.py`: Tests for creating a user.
  - `test_get_user_by_id.py`: Tests for retrieving a user by ID.
  - `test_update_user.py`: Tests for updating user details.
  - `test_user_posts.py`: Tests for creating and getting user posts.
  - `test_user_comments`: Tests for creating and getting comments.
  - `utils/`: Contains utility functions and classes.
  - `utils/fixture.py`: Contains fixtures to interact with the API (create, get, update, delete users, cleanup_user).
  - `utils/check.py`: Contains the `Check` class for assertions.

## How to Execute the Tests

Run the tests using `pytest`. You can execute all tests with the following command:

```bash
pytest tests
```

To run a specific test file, use:

```bash
pytest tests/test_create_user.py
```

For detailed logging, run this command

```bash
pytest -s tests
```

To generate an HTML report after the test, run this command

```bash
pytest tests --html=report.html --self-contained-html

```

## Additional Information

- Ensure the API base URL and headers are correctly configured in `commands.py`.
- The `users.json` file should contain valid user data for testing.

## Example `users.json` File

```json
{
  "users": [
    {
      "name": "Test User",
      "email": "testuser@example.com",
      "gender": "male",
      "status": "active"
    }
  ]
}
```
