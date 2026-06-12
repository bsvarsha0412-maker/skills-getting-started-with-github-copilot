import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities_returns_activity_list():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    new_email = "alex@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup?email=alex%40mergington.edu"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up alex@mergington.edu for Chess Club"
    assert "alex@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_404():
    response = client.post(
        "/activities/Unknown%20Club/signup?email=test%40example.com"
    )

    assert response.status_code == 404
    error_data = response.json()
    assert error_data["detail"] == "Activity not found"
