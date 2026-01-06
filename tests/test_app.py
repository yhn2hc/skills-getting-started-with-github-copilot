import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 302)
    assert response.headers["location"].endswith("/static/index.html")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Get activities
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    test_email = "pytest-student@mergington.edu"

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert signup.status_code == 200
    assert "message" in signup.json()

    # Unregister
    unregister = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
    assert unregister.status_code == 200
    assert "message" in unregister.json()
