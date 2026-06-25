"""
backend/routers/diet.py – Diet planning and calorie logging endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database import models as db_models
from backend.schemas import DietLogCreate, DietLogOut, DietPlanRequest
from models.diet_planner import DietPlanner

router = APIRouter(prefix="/diet", tags=["Diet"])
planner = DietPlanner()


@router.post("/plan")
def get_diet_plan(payload: DietPlanRequest):
    """Generate a personalised diet plan (not persisted)."""
    return planner.get_diet_plan(
        weight_kg=payload.weight_kg,
        height_cm=payload.height_cm,
        age=payload.age,
        is_male=payload.is_male,
        goal=payload.goal,
        activity_level=payload.activity_level,
    )


@router.post("/log", response_model=DietLogOut, status_code=201)
def log_meal(payload: DietLogCreate, db: Session = Depends(get_db)):
    """Persist a meal log entry."""
    user = db.query(db_models.User).filter(db_models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {payload.user_id} not found")

    entry = db_models.DietLog(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/log/{user_id}", response_model=list[DietLogOut])
def get_diet_logs(user_id: int, db: Session = Depends(get_db)):
    """Return all diet logs for a user."""
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    return (
        db.query(db_models.DietLog)
        .filter(db_models.DietLog.user_id == user_id)
        .order_by(db_models.DietLog.log_date.desc())
        .all()
    )


@router.get("/tip/{goal}")
def diet_tip(goal: str):
    """Return a single diet tip for the given goal."""
    return {"tip": planner.diet_tip(goal)}
