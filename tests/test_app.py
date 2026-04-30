import pytest
from src.app import activities


class TestActivities:
    """Tests for the Mergington High School Activities API."""

    def test_get_activities(self, client, clean_activities):
        """Test that GET /activities returns all activities."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        
        # Verify activity details
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_root_redirect(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_signup_for_activity(self, client, clean_activities, test_email, test_activity):
        """Test that a student can successfully sign up for an activity."""
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert test_activity in data["message"]
        
        # Verify participant was added
        assert test_email in activities[test_activity]["participants"]

    def test_unregister_from_activity(self, client, clean_activities, test_email, test_activity):
        """Test that a student can successfully unregister from an activity."""
        # First, sign up the student
        client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        
        # Verify student is registered
        assert test_email in activities[test_activity]["participants"]
        
        # Now unregister
        response = client.delete(
            f"/activities/{test_activity}/participants/{test_email}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        
        # Verify participant was removed
        assert test_email not in activities[test_activity]["participants"]
