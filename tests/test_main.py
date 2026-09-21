from datetime import date

from grad_application_tracker.main import Opportunity, upcoming_opportunities


def test_deadline_today():
    today = date(2026, 10, 31)

    opportunity = Opportunity("Cern", "Junior Software Developer", date(2026, 10, 31))

    result = upcoming_opportunities([opportunity], today, 7)

    assert result == [opportunity]


def test_deadline_on_final_day():
    today = date(2026, 10, 31)

    opportunity = Opportunity("Cern", "Junior Software Developer", date(2026, 11, 7))

    result = upcoming_opportunities([opportunity], today, 7)

    assert result == [opportunity]


def test_expired_deadline_excluded():
    today = date(2026, 10, 31)

    opportunity = Opportunity("Cern", "Junior Software Developer", date(2026, 10, 30))

    result = upcoming_opportunities([opportunity], today, 7)

    assert result == []


def test_unknown_deadline_excluded():
    today = date(2026, 10, 31)

    opportunity = Opportunity("Cern", "Junior Software Developer", None)

    result = upcoming_opportunities([opportunity], today, 7)

    assert result == []


def test_uses_supplied_range():
    today = date(2026, 10, 31)

    opportunity = Opportunity("Cern", "Junior Software Developer", date(2026, 11, 4))

    result = upcoming_opportunities([opportunity], today, 3)

    assert result == []


def test_results_sorted():
    today = date(2026, 10, 31)

    later = Opportunity("Cern", "Junior Software Developer", date(2026, 11, 7))
    earlier = Opportunity("Anthropic", "Junior ML Engineer", date(2026, 11, 3))
    opportunities = [later, earlier]

    result = upcoming_opportunities(opportunities, today, 7)

    assert result == [earlier, later]


def test_empty_input():
    today = date(2026, 10, 31)

    result = upcoming_opportunities([], today, 7)

    assert result == []


def test_nothing_valid():
    today = date(2026, 10, 31)

    opportunities = [
        Opportunity("Cern", "Junior Software Developer", date(2026, 10, 30)),
        Opportunity("Anthropic", "Junior ML Engineer", date(2026, 11, 30)),
    ]

    result = upcoming_opportunities(opportunities, today, 7)

    assert result == []


def test_original_input_unchanged():
    today = date(2026, 10, 31)

    opportunities = [
        Opportunity("Cern", "Junior Developer", date(2026, 11, 6)),
        Opportunity("Anthropic", "Junior Engineer", date(2026, 11, 2)),
    ]
    original_order = opportunities.copy()

    upcoming_opportunities(opportunities, today, 7)

    assert opportunities == original_order
