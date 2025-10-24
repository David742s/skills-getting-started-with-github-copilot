from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# Copia de los participantes originales
original_activities = copy.deepcopy(activities)

def reset_activities():
    """Restablece la lista de participantes de cada actividad antes de cada test"""
    for key in original_activities:
        activities[key]["participants"] = copy.deepcopy(original_activities[key]["participants"])

def test_root_redirect():
    reset_activities()
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_activities():
    reset_activities()
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    reset_activities()
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]

def test_signup_existing_student():
    reset_activities()
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_from_activity():
    reset_activities()
    email = "tempstudent@mergington.edu"
    activity_name = "Programming Class"
    activities[activity_name]["participants"].append(email)
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

def test_unregister_nonexistent_student():
    reset_activities()
    email = "nonexistent@mergington.edu"
    activity_name = "Programming Class"
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    # Comparación más robusta
    assert "not registered for this activity" in response.json()["detail"]

def test_activity_not_found():
    reset_activities()
    email = "test@mergington.edu"
    response = client.post("/activities/NoClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    response = client.post("/activities/NoClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404


