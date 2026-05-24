"""Test suite for Mergington High School Activities API"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_200(self, client):
        """Arrange-Act-Assert: Verify activities endpoint returns 200 status"""
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_all_activities(self, client):
        """Verify all 9 activities are returned"""
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_returns_activity_structure(self, client):
        """Verify activity objects have required fields"""
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities.get("Chess Club")
        
        # Assert
        assert chess_club is not None
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
    
    def test_get_activities_returns_participants_list(self, client):
        """Verify participants are returned as a list"""
        # Act
        response = client.get("/activities")
        activities = response.json()
        participants = activities["Chess Club"]["participants"]
        
        # Assert
        assert isinstance(participants, list)
        assert len(participants) == 2
        assert "michael@mergington.edu" in participants


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful_adds_participant(self, client):
        """Arrange-Act-Assert: Verify new participant is added"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Art Studio"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Signed up" in result["message"]
        assert email in result["message"]
        assert activity in result["message"]
    
    def test_signup_returns_success_message(self, client):
        """Verify signup returns appropriate message"""
        # Act
        response = client.post(
            "/activities/Drama Club/signup",
            params={"email": "test@mergington.edu"}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Verify error when signing up for non-existent activity"""
        # Act
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_email_returns_400(self, client):
        """Verify error when student tries to sign up twice"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_adds_participant_to_activity(self, client):
        """Verify participant appears in activity after signup"""
        # Arrange
        email = "newcomer@mergington.edu"
        activity = "Basketball Team"
        
        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        participants = activities[activity]["participants"]
        assert email in participants
    
    def test_signup_updates_spot_count(self, client):
        """Verify available spots decrease after signup"""
        # Arrange
        activity = "Swimming Club"
        email = "newswimmer@mergington.edu"
        
        # Get initial availability
        response_before = client.get("/activities")
        before_count = response_before.json()
        initial_participants = len(before_count[activity]["participants"])
        max_spots = before_count[activity]["max_participants"]
        spots_before = max_spots - initial_participants
        
        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Get availability after signup
        response_after = client.get("/activities")
        after_count = response_after.json()
        new_participants = len(after_count[activity]["participants"])
        spots_after = max_spots - new_participants
        
        # Assert
        assert spots_after == spots_before - 1


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""
    
    def test_remove_participant_successful(self, client):
        """Arrange-Act-Assert: Verify participant is removed"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Removed" in result["message"]
    
    def test_remove_participant_returns_message(self, client):
        """Verify remove returns appropriate message"""
        # Act
        response = client.delete(
            "/activities/Chess Club/participants/michael@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_remove_nonexistent_activity_returns_404(self, client):
        """Verify error when removing from non-existent activity"""
        # Act
        response = client.delete(
            "/activities/Fake Activity/participants/test@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_remove_nonexistent_participant_returns_404(self, client):
        """Verify error when removing participant not in activity"""
        # Act
        response = client.delete(
            "/activities/Chess Club/participants/notaparticipant@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_remove_participant_from_activity(self, client):
        """Verify participant is actually removed from activity"""
        # Arrange
        email = "daniel@mergington.edu"
        activity = "Chess Club"
        
        # Act
        client.delete(f"/activities/{activity}/participants/{email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        participants = activities[activity]["participants"]
        assert email not in participants
    
    def test_remove_restores_spot(self, client):
        """Verify a spot becomes available after removal"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Get initial spot count
        response_before = client.get("/activities")
        before_data = response_before.json()
        initial_count = len(before_data[activity]["participants"])
        
        # Act
        client.delete(f"/activities/{activity}/participants/{email}")
        
        # Get spot count after removal
        response_after = client.get("/activities")
        after_data = response_after.json()
        final_count = len(after_data[activity]["participants"])
        
        # Assert
        assert final_count == initial_count - 1


class TestEdgeCases:
    """Tests for edge cases and validation"""
    
    def test_signup_then_remove_same_participant(self, client):
        """Verify signup and remove work together"""
        # Arrange
        email = "test@mergington.edu"
        activity = "Art Studio"
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert signup worked
        assert signup_response.status_code == 200
        
        # Act - Remove
        remove_response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        
        # Assert remove worked
        assert remove_response.status_code == 200
        
        # Verify participant is gone
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]
    
    def test_cannot_signup_after_being_removed(self, client):
        """Verify participant can sign up again after removal"""
        # Arrange
        email = "comeback@mergington.edu"
        activity = "Drama Club"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Remove participant
        client.delete(f"/activities/{activity}/participants/{email}")
        
        # Signup again
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert - should be able to sign up again
        assert response2.status_code == 200
    
    def test_email_parameter_encoding(self, client):
        """Verify email with special characters is handled correctly"""
        # Arrange
        email = "test+plus@mergington.edu"
        activity = "Robotics Workshop"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        result = client.get("/activities")
        assert email in result.json()[activity]["participants"]
    
    def test_activity_name_with_spaces(self, client):
        """Verify activity names with spaces are handled correctly"""
        # Arrange
        activity = "Programming Class"
        email = "coder@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
