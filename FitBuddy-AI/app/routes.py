from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ai.init import generate_workout_plan

router = APIRouter()


class WorkoutRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=100)
    experience: Literal["Beginner", "Intermediate", "Advanced"] = "Beginner"
    days_per_week: int = Field(4, ge=2, le=7)
    minutes_per_session: int = Field(30, ge=20, le=90)
    equipment: str = Field("Dumbbells and bodyweight", max_length=200)
    focus_areas: str = Field("General strength and cardio", max_length=200)
    notes: str = Field("", max_length=300)


class WorkoutDay(BaseModel):
    day: str
    focus: str
    workout: list[str]
    recovery: str


class WorkoutPlan(BaseModel):
    title: str
    overview: str
    weekly_schedule: list[WorkoutDay]


@router.get("/health")
def health():
    return {"status": "ok", "service": "fitbuddy"}


@router.post("/api/generate-plan")
async def generate_plan(payload: WorkoutRequest) -> WorkoutPlan:
    plan = generate_workout_plan(payload.model_dump())
    return WorkoutPlan(**plan)
