from datetime import date, timedelta

today = date(2026, 10, 31)  # Fictional current date
valid_range_days = 7


class Opportunity:
    def __init__(self, company, role, deadline):
        self.company = company
        self.role = role
        self.deadline = deadline

    def __str__(self):
        return f"{self.company} | {self.role} | {self.deadline}"


# Fictional sample opportunities
opportunities = [
    Opportunity("RedHat", "Junior Developer", date(2026, 11, 4)),  # Supplied date +4
    Opportunity(
        "Cern", "Junior Software Developer", date(2026, 11, 7)
    ),  # Supplied date +7
    Opportunity("Google DeepMind", "Junior ML Engineer", date(2027, 1, 10)),
    Opportunity("Anthropic", "Junior MLOps Engineer", date(2026, 10, 27)),
]  # Supplied date -4


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


for opportunity in upcoming_opportunities(opportunities, today, valid_range_days):
    print(opportunity)
