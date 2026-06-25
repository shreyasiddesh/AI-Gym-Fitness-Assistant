import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from database.db import Base, get_db


@pytest.fixture()
def client():
    fd, db_path = tempfile.mkstemp(prefix="fitness_test_", suffix=".db")
    os.close(fd)

    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
        if os.path.exists(db_path):
            os.remove(db_path)


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_user_and_enforce_enum_validation(client: TestClient):
    payload = {
        "name": "Alex",
        "age": 25,
        "weight_kg": 75,
        "height_cm": 175,
        "goal": "lose",
        "activity_level": "moderate",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Alex"

    bad_payload = {**payload, "goal": "cutting-hard"}
    bad_response = client.post("/users/", json=bad_payload)
    assert bad_response.status_code == 422


def test_user_guardrails_on_dependent_routes(client: TestClient):
    workout_payload = {
        "user_id": 999,
        "exercise": "Squat",
        "reps": 10,
        "duration_sec": 60,
        "posture_issues": "",
    }
    meal_payload = {
        "user_id": 999,
        "meal_name": "Lunch",
        "calories": 500,
        "protein_g": 30,
        "carbs_g": 50,
        "fat_g": 15,
    }
    habit_payload = {
        "user_id": 999,
        "workout_done": True,
        "mood": 7,
        "sleep_hours": 7.5,
        "stress_level": 4,
    }

    assert client.post("/workout/log", json=workout_payload).status_code == 404
    assert client.post("/diet/log", json=meal_payload).status_code == 404
    assert client.post("/tracker/log", json=habit_payload).status_code == 404


def test_end_to_end_core_flow(client: TestClient):
    user_response = client.post(
        "/users/",
        json={
            "name": "Priya",
            "age": 29,
            "weight_kg": 62,
            "height_cm": 165,
            "goal": "maintain",
            "activity_level": "active",
        },
    )
    user_id = user_response.json()["id"]

    workout_response = client.post(
        "/workout/log",
        json={
            "user_id": user_id,
            "exercise": "Push-up",
            "reps": 24,
            "duration_sec": 120,
            "posture_issues": "elbows flared",
        },
    )
    assert workout_response.status_code == 201
    assert workout_response.json()["performance_score"] > 0

    progress_response = client.get(f"/workout/progress/{user_id}")
    assert progress_response.status_code == 200
    progress = progress_response.json()
    assert progress["total_sessions"] == 1
    assert progress["total_reps"] == 24

    diet_plan_response = client.post(
        "/diet/plan",
        json={
            "weight_kg": 62,
            "height_cm": 165,
            "age": 29,
            "is_male": False,
            "goal": "maintain",
            "activity_level": "active",
        },
    )
    assert diet_plan_response.status_code == 200
    assert "meal_plan" in diet_plan_response.json()

