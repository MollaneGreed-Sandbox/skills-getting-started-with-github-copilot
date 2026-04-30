import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """Reset activities to a clean state before each test."""
    original_activities = activities.copy()
    yield
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def test_email():
    """Provide a test email address."""
    return "test@mergington.edu"


@pytest.fixture
def test_activity():
    """Provide a test activity name."""
    return "Chess Club"
