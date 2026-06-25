"""
backend/routers/workout.py – Workout session logging and analysis endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database import models as db_models
from backend.schemas import WorkoutCreate, WorkoutOut
from models.performance_analyzer import PerformanceAnalyzer

router = APIRouter(prefix="/workout", tags=["Workout"])
analyzer = PerformanceAnalyzer()


@router.post("/log", response_model=WorkoutOut, status_code=201)
def log_workout(payload: WorkoutCreate, db: Session = Depends(get_db)):
    """Persist a workout session and compute a performance score."""
    user = db.query(db_models.User).filter(db_models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {payload.user_id} not found")

    issues = [i.strip() for i in payload.posture_issues.split(",") if i.strip()]
    score_data = analyzer.score_session(
        exercise=payload.exercise,
        reps=payload.reps,
        duration_sec=payload.duration_sec,
        posture_issues=issues,
    )
    session_data = payload.model_dump()
    session = db_models.WorkoutSession(
        **session_data,
        performance_score=score_data["score"],
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/user/{user_id}", response_model=list[WorkoutOut])
def get_user_workouts(user_id: int, db: Session = Depends(get_db)):
    """Return all workout sessions for a user."""
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    return (
        db.query(db_models.WorkoutSession)
        .filter(db_models.WorkoutSession.user_id == user_id)
        .order_by(db_models.WorkoutSession.session_date.desc())
        .all()
    )


@router.get("/progress/{user_id}")
def get_progress(user_id: int, db: Session = Depends(get_db)):
    """Return weekly progress summary for a user."""
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    sessions = (
        db.query(db_models.WorkoutSession)
        .filter(db_models.WorkoutSession.user_id == user_id)
        .all()
    )
    rows = [
        {
            "exercise": s.exercise,
            "reps": s.reps,
            "duration_sec": s.duration_sec,
            "performance_score": s.performance_score,
            "session_date": s.session_date,
        }
        for s in sessions
    ]
    return analyzer.weekly_progress(rows)
