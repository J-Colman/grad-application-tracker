import json
import os
import tempfile
import uuid
from datetime import date, timedelta

import click


class Opportunity:
    VALID_STATUSES = ("saved", "applied", "interviewed", "accepted", "rejected")

    def __init__(self, company, role, deadline, status="saved", id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.company = company
        self.role = role
        self.deadline = deadline
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        self._status = value

    def __str__(self):
        deadline = self.deadline if self.deadline else "No deadline"
        return f"{self.id} | {self.company} | {self.role} | {deadline} | {self.status}"


def upcoming_opportunities(opportunities, today, valid_range_days):
    """Find opportunities whose deadline is within a specified horizon"""
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


def opportunity_from_dict(data):
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


def save_opportunities(opportunities, file_path):
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


def load_opportunities(file_path):
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


@click.group()
def cli():
    """Track graduate job opportunities."""


@cli.command("list")
def list_opportunities():
    """Show all saved opportunities."""
    file_path = "data/opportunities.json"

    try:
        opportunities = load_opportunities(file_path)
    except FileNotFoundError:
        click.echo("No opportunities saved yet.")
        return
    except (TypeError, ValueError) as error:
        raise click.ClickException(str(error)) from error

    if not opportunities:
        click.echo("No opportunities saved yet.")
        return

    for opportunity in opportunities:
        click.echo(opportunity)


@cli.command("add")
@click.option("--company", required=True, help="Company name.")
@click.option("--role", required=True, help="Job title.")
@click.option("--deadline", help="Deadline in YYYY-MM-DD format.")
@click.option(
    "--status",
    type=click.Choice(Opportunity.VALID_STATUSES, case_sensitive=False),
    default="saved",
    show_default=True,
)
def add_opportunity(company, role, deadline, status):
    """Save a new opportunity."""
    file_path = "data/opportunities.json"

    try:
        parsed_deadline = date.fromisoformat(deadline) if deadline else None
    except ValueError as error:
        raise click.BadParameter(
            "Use YYYY-MM-DD format.", param_hint="--deadline"
        ) from error

    try:
        opportunities = load_opportunities(file_path)
    except FileNotFoundError:
        opportunities = []
    except (TypeError, ValueError) as error:
        raise click.ClickException(str(error)) from error

    opportunities.append(Opportunity(company, role, parsed_deadline, status))

    try:
        save_opportunities(opportunities, file_path)
    except OSError as error:
        raise click.ClickException(f"Could not save opportunities: {error}") from error

    click.echo(f"Added '{role}' at '{company}'. Status: {status}")


if __name__ == "__main__":
    cli()
