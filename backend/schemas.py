"""
backend/schemas.py – Pydantic request/response schemas for the FastAPI backend.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

GoalType = Literal["lose", "gain", "maintain"]
ActivityLevelType = Literal["sedentary", "light", "moderate", "active", "very_active"]
WorkoutType = Literal["strength", "cardio", "flexibility"]
FitnessLevelType = Literal["beginner", "intermediate", "advanced"]
PriceTierType = Literal["low", "mid", "high", "none"]


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str
    age: int = Field(ge=10, le=100)
    weight_kg: float = Field(gt=0, le=500)
    height_cm: float = Field(gt=0, le=300)
    goal: GoalType = "maintain"
    activity_level: ActivityLevelType = "moderate"

class UserOut(UserCreate):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Workout
# ---------------------------------------------------------------------------

class WorkoutCreate(BaseModel):
    user_id: int
    exercise: str
    reps: int = 0
    duration_sec: int = 0
    posture_issues: str = ""

class WorkoutOut(WorkoutCreate):
    id: int
    performance_score: float
    session_date: datetime
    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Diet
# ---------------------------------------------------------------------------

class DietLogCreate(BaseModel):
    user_id: int
    meal_name: str
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0

class DietLogOut(DietLogCreate):
    id: int
    log_date: datetime
    model_config = {"from_attributes": True}


class DietPlanRequest(BaseModel):
    weight_kg: float = Field(gt=0, le=500)
    height_cm: float = Field(gt=0, le=300)
    age: int = Field(ge=10, le=100)
    is_male: bool = True
    goal: GoalType = "maintain"
    activity_level: ActivityLevelType = "moderate"


# ---------------------------------------------------------------------------
# Habit
# ---------------------------------------------------------------------------

class HabitCreate(BaseModel):
    user_id: int
    workout_done: bool = False
    mood: int = Field(ge=1, le=10, default=5)
    sleep_hours: float = Field(ge=0, le=24, default=7.0)
    stress_level: int = Field(ge=1, le=10, default=5)

class HabitOut(HabitCreate):
    id: int
    record_date: datetime
    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Chatbot
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    reply: str
    sentiment: str


# ---------------------------------------------------------------------------
# IoT
# ---------------------------------------------------------------------------

class IoTRequest(BaseModel):
    age: int = Field(ge=10, le=100, default=25)
    fitness_level: str = "moderate"


# ---------------------------------------------------------------------------
# Recommender
# ---------------------------------------------------------------------------

class WorkoutRecommendRequest(BaseModel):
    goal: GoalType = "maintain"
    fitness_level: FitnessLevelType = "beginner"
    workout_type: Optional[WorkoutType] = None
    max_duration: int = Field(ge=10, le=240, default=120)
    top_n: int = Field(ge=1, le=20, default=5)

class GymRecommendRequest(BaseModel):
    focus: WorkoutType = "strength"
    price_tier: Optional[PriceTierType] = None
    top_n: int = Field(ge=1, le=20, default=3)
