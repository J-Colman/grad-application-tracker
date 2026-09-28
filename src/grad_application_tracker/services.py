from datetime import date, timedelta
from pathlib import Path

from .models import Opportunity
from .storage import load_opportunities, save_opportunities


def upcoming_opportunities(
    opportunities: list[Opportunity], today: date, valid_range_days: int
) -> list[Opportunity]:
    """Find opportunities whose deadline is within a specified horizon"""

    def _deadline(opportunity: Opportunity) -> date:
        """Sort key for opportunities already known to have a deadline"""
        assert opportunity.deadline is not None
        return opportunity.deadline

    end_date = today + timedelta(days=valid_range_days)  # Calculate the last valid date

    # Filter by opportunities within the valid range
    valid_opportunities = [
        opportunity
        for opportunity in opportunities
        if opportunity.deadline is not None
        and today <= opportunity.deadline <= end_date
    ]

    # Sort by opportunity deadline ascending
    valid_opportunities.sort(key=_deadline)
    return valid_opportunities


def get_opportunities(file_path: str | Path) -> list[Opportunity]:
    """Return an empty list if file not found"""
    try:
        return load_opportunities(file_path)

    except FileNotFoundError:
        return []


def add_opportunity(
    file_path: str | Path, company: str, role: str, deadline: date | None, status: str
) -> Opportunity:
    """Save a new opportunity"""
    opportunities = get_opportunities(file_path)

    opportunity = Opportunity(company, role, deadline, status)
    opportunities.append(opportunity)

    save_opportunities(opportunities, file_path)
    return opportunity
