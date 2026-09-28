from datetime import timedelta

from .models import Opportunity
from .storage import load_opportunities, save_opportunities


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

def get_opportunities(file_path):
    """Return an empty list if file not found"""
    try:
        return load_opportunities(file_path)

    except FileNotFoundError:
        return []

def add_opportunity(file_path, company, role, deadline, status):
    """Save a new opportunity"""
    opportunities = get_opportunities(file_path)

    opportunity = Opportunity(company, role, deadline, status)
    opportunities.append(opportunity)

    save_opportunities(opportunities, file_path)
    return opportunity
