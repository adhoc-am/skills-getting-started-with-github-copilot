import pytest
from fastapi.testclient import TestClient

from src.app import app, get_initial_activities

import copy

@pytest.fixture(autouse=True)
def reset_activities():
    app.state.activities = copy.deepcopy(get_initial_activities())

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    get_response = client.get("/activities")
    assert get_response.status_code == 200
    data = get_response.json()
    assert email in data[activity]["participants"]


def test_signup_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity():
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    get_response = client.get("/activities")
    assert get_response.status_code == 200
    data = get_response.json()
    assert email not in data[activity]["participants"]


def test_unregister_not_found():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
