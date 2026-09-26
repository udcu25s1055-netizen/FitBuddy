from __future__ import annotations

import os
from typing import Any

from google import generativeai as genai

from app.config import get_settings

settings = get_settings()

if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)


def build_fallback_plan(data: dict[str, Any]) -> dict[str, Any]:
    goal = data.get("goal", "general fitness")
    days = int(data.get("days_per_week", 4))
    weekly_schedule = []
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for i in range(days):
        focus = [
            "Strength",
            "Cardio",
            "Mobility",
            "Power",
            "Recovery",
            "Conditioning",
            "Core",
        ][i % 7]
        weekly_schedule.append(
            {
                "day": day_names[i],
                "focus": focus,
                "workout": [
                    f"Warm-up and activation block ({data.get('minutes_per_session', 30)} minutes)",
                    f"Main {focus.lower()} circuit with controlled tempo",
                    "Finisher: short conditioning set",
                ],
                "recovery": "Hydrate, stretch, and sleep 7-9 hours.",
            }
        )

    return {
        "title": f"{goal.title()} Fitness Plan",
        "overview": (
            f"This {days}-day plan is structured around {goal.lower()} with a focus on "
            f"steady progression, recovery, and sustainable effort."
        ),
        "weekly_schedule": weekly_schedule,
    }


def generate_workout_plan(data: dict[str, Any]) -> dict[str, Any]:
    if not settings.gemini_api_key:
        return build_fallback_plan(data)

    try:
        model = genai.GenerativeModel(settings.gemini_workout_model)
        prompt = f"""
        Create a realistic weekly fitness plan for the user.
        Goal: {data.get('goal')}
        Experience: {data.get('experience')}
        Days per week: {data.get('days_per_week')}
        Minutes per session: {data.get('minutes_per_session')}
        Equipment: {data.get('equipment')}
        Focus areas: {data.get('focus_areas')}
        Notes: {data.get('notes')}

        Return JSON only with keys: title, overview, weekly_schedule.
        Each weekly_schedule item must contain: day, focus, workout, recovery.
        The workout should be a list of 3 short exercise instructions.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        import json
        return json.loads(text)
    except Exception:
        return build_fallback_plan(data)
