"""
backend/routers/tracker.py – Fitness Habit Tracker endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database import models as db_models
from backend.schemas import HabitCreate, HabitOut
from models.habit_tracker import HabitTracker

router = APIRouter(prefix="/tracker", tags=["Habit Tracker"])
tracker = HabitTracker()


@router.post("/log", response_model=HabitOut, status_code=201)
def log_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    """Log today's habit check-in and persist it."""
    user = db.query(db_models.User).filter(db_models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {payload.user_id} not found")

    record = db_models.HabitRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/predict")
def predict_skip(mood: int = 5, sleep_hours: float = 7.0, stress_level: int = 5):
    """Predict the probability of skipping a workout and return a nudge."""
    prob = tracker.predict_skip_probability(mood, sleep_hours, stress_level)
    nudge = tracker.get_nudge(prob)
    return {"skip_probability": prob, "nudge": nudge}


@router.get("/summary/{user_id}")
def get_habit_summary(user_id: int, db: Session = Depends(get_db)):
    """Return a habit summary for the last 7 records."""
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    records = (
        db.query(db_models.HabitRecord)
        .filter(db_models.HabitRecord.user_id == user_id)
        .order_by(db_models.HabitRecord.record_date.desc())
        .limit(7)
        .all()
    )
    rows = [
        {
            "workout_done": r.workout_done,
            "mood": r.mood,
            "sleep_hours": r.sleep_hours,
            "stress_level": r.stress_level,
        }
        for r in records
    ]
    return tracker.weekly_summary(rows)
