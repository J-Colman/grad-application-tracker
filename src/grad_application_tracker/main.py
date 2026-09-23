import json
import os
import tempfile
from datetime import date, timedelta


class Opportunity:
    def __init__(self, company, role, deadline):
        self.company = company
        self.role = role
        self.deadline = deadline

    def __str__(self):
        return f"{self.company} | {self.role} | {self.deadline}"


def upcoming_opportunities(opportunities, today, valid_range_days):
    end_date = today + timedelta(days=valid_range_days)  # Calculate the last valid date

    # Filter by opportunities within the valid range
    valid_opportunities = [
        opportunity
        for opportunity in opportunities
        if opportunity.deadline is not None
        and today <= opportunity.deadline <= end_date
    ]

    # Sort by opportunity deadline ascending
    valid_opportunities.sort(key=lambda opportunity: opportunity.deadline)
    return valid_opportunities


def opportunity_to_dict(opportunity):
    # Convert an Opportunity into a dictionary
    return {
        "company": opportunity.company,
        "role": opportunity.role,
        "deadline": (
            opportunity.deadline.isoformat()
            if opportunity.deadline is not None
            else None
        ),
    }


def opportunity_from_dict(data):
    # Create an Opportunity from a dictionary
    return Opportunity(
        data["company"],
        data["role"],
        date.fromisoformat(data["deadline"]) if data["deadline"] is not None else None,
    )


def save_opportunities(opportunities, file_path):
    # Save opportunities atomically using a temporary JSON file
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


def load_opportunities(file_path):
    # Load opportunities from a JSON file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Could not load opportunities: file not found: {file_path}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            "Could not load opportunities: the JSON file is malformed"
        ) from error

    if not isinstance(data, list):
        raise TypeError("Could not load opportunities: expected a JSON list")

    try:
        return [opportunity_from_dict(item) for item in data]
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            "Could not load opportunities: invalid opportunity data"
        ) from error


def main():
    file_path = "data/opportunities.json"

    # Fictional sample opportunities
    if not os.path.exists(file_path):
        opportunities = [
            Opportunity("RedHat", "Junior Developer", date(2026, 11, 4)),
            Opportunity("Cern", "Junior Software Developer", date(2026, 11, 7)),
            Opportunity("Google DeepMind", "Junior ML Engineer", date(2027, 1, 10)),
            Opportunity("Anthropic", "Junior MLOps Engineer", date(2026, 10, 27)),
        ]

        save_opportunities(opportunities, file_path)

    try:
        loaded_opportunities = load_opportunities(file_path)
        valid_opportunities = upcoming_opportunities(loaded_opportunities, date(2026, 10, 31), 7)
    except (FileNotFoundError, TypeError, ValueError) as error:
        print(f"Error: {error}")
        return

    for opportunity in valid_opportunities:
        print(opportunity)


if __name__ == "__main__":
    main()
