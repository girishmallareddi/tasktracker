import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from db import init_db

TEST_DB = "test_tasks.db"


@pytest.fixture
def app():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    app = create_app(TEST_DB)
    with app.app_context():
        init_db()

    yield app

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


@pytest.fixture
def client(app):
    return app.test_client()