import pytest
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.hookimpl(tryfirst=True)
def pytest_configure():
    logging.getLogger().setLevel(logging.DEBUG)