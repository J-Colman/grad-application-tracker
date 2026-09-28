import json
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

from .models import Opportunity


def opportunity_to_dict(opportunity: Opportunity) -> dict[str, str | None]:
    """Convert an Opportunity into a dictionary"""
    return {
        "id": opportunity.id,
        "company": opportunity.company,
        "role": opportunity.role,
        "deadline": (
            opportunity.deadline.isoformat()
            if opportunity.deadline is not None
            else None
        ),
        "status": opportunity.status,
    }


def opportunity_from_dict(data: dict[str, Any]) -> Opportunity:
    """Create an Opportunity from a dictionary"""
    return Opportunity(
        id=data.get("id"),
        company=data["company"],
        role=data["role"],
        deadline=date.fromisoformat(data["deadline"])
        if data["deadline"] is not None
        else None,
        status=data.get("status", "saved"),
    )


def save_opportunities(opportunities: list[Opportunity], file_path: str | Path) -> None:
    """Save opportunities atomically using a temporary JSON file"""
    dir_name = os.path.dirname(file_path) or "."
    os.makedirs(dir_name, exist_ok=True)

    data = [opportunity_to_dict(opportunity) for opportunity in opportunities]

    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
            file.flush()
            os.fsync(file.fileno())

        os.replace(tmp_path, file_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def load_opportunities(file_path: str | Path) -> list[Opportunity]:
    """Load opportunities from a JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Could not load opportunities: file not found: {file_path}: {error}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Could not load opportunities: the JSON file is malformed: {error}"
        ) from error

    if not isinstance(data, list):
        raise TypeError("Could not load opportunities: expected a JSON list")

    try:
        return [opportunity_from_dict(item) for item in data]
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            f"Could not load opportunities: invalid opportunity data: {error}"
        ) from error
