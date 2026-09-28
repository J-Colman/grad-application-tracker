from datetime import timedelta


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
