"""Pytest configuration and fixtures for FastAPI tests"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice team offense, defense, and competitive games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Build endurance and improve stroke technique in the pool",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["nina@mergington.edu"]
        },
        "Art Studio": {
            "description": "Work on drawing, painting, and creative mixed-media projects",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["ryan@mergington.edu"]
        },
        "Drama Club": {
            "description": "Develop acting, improvisation, and stage performance skills",
            "schedule": "Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["julia@mergington.edu"]
        },
        "Debate Society": {
            "description": "Practice research, public speaking, and formal debate tournaments",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["liam@mergington.edu"]
        },
        "Robotics Workshop": {
            "description": "Build and program robots while learning engineering concepts",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 14,
            "participants": ["zoe@mergington.edu"]
        }
    }
    
    # Clear and restore
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(original_activities)
