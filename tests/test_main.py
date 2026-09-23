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


# --------------------------------------------------------------------------------
import json

import pytest

from grad_application_tracker.main import load_opportunities, save_opportunities

tmp_path = "data/tmp/"


def test_save_opportunities(tmp_path):
    file_path = tmp_path / "opportunities.json"
    opportunity = Opportunity("Cern", "Junior Developer", date(2026, 10, 31))

    save_opportunities([opportunity], file_path)

    with file_path.open("r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == [
        {
            "company": "Cern",
            "role": "Junior Developer",
            "deadline": "2026-10-31",
        }
    ]


def test_load_opportunities(tmp_path):
    file_path = tmp_path / "opportunities.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            [
                {
                    "company": "Cern",
                    "role": "Junior Developer",
                    "deadline": "2026-10-31",
                }
            ],
            file,
        )

    loaded_data = load_opportunities(file_path)

    assert len(loaded_data) == 1
    assert loaded_data[0].company == "Cern"
    assert loaded_data[0].role == "Junior Developer"
    assert loaded_data[0].deadline == date(2026, 10, 31)


def test_none_deadline_survives(tmp_path):
    file_path = tmp_path / "opportunities.json"
    opportunity = Opportunity("Cern", "Junior Developer", None)

    save_opportunities([opportunity], file_path)
    loaded_data = load_opportunities(file_path)

    assert len(loaded_data) == 1
    assert loaded_data[0].deadline is None


def test_empty_list_survives(tmp_path):
    file_path = tmp_path / "opportunities.json"

    save_opportunities([], file_path)
    loaded_data = load_opportunities(file_path)

    assert loaded_data == []


def test_missing_file_raises_file_not_found(tmp_path):
    file_path = tmp_path / "opportunities.json"

    with pytest.raises(FileNotFoundError, match="file not found"):
        load_opportunities(file_path)


def test_malformed_json_raises_value_error(tmp_path):
    file_path = tmp_path / "opportunities.json"
    file_path.write_text('[{"company": "Cern"', encoding="utf-8")

    with pytest.raises(ValueError, match="the JSON file is malformed"):
        load_opportunities(file_path)


def test_non_list_json_raises_type_error(tmp_path):
    file_path = tmp_path / "opportunities.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "company": "Cern",
            },
            file,
        )

    with pytest.raises(TypeError, match="expected a JSON list"):
        load_opportunities(file_path)


def test_missing_opportunity_field_raises_value_error(tmp_path):
    file_path = tmp_path / "opportunities.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            [
                {
                    "company": "Cern",
                    "role": "Junior Developer",
                }
            ],
            file,
        )

    with pytest.raises(ValueError, match="invalid opportunity data"):
        load_opportunities(file_path)


def test_invalid_deadline_raises_value_error(tmp_path):
    file_path = tmp_path / "opportunities.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            [
                {
                    "company": "Cern",
                    "role": "Junior Developer",
                    "deadline": "2026/10/31",
                }
            ],
            file,
        )

    with pytest.raises(ValueError, match="invalid opportunity data"):
        load_opportunities(file_path)


def test_save_creates_parent_directory(tmp_path):
    data_dir = tmp_path / "data"
    file_path = data_dir / "opportunities.json"
    opportunity = Opportunity("Cern", "Junior Developer", None)

    assert not data_dir.exists()

    save_opportunities([opportunity], file_path)

    assert data_dir.is_dir()
    assert file_path.is_file()


def test_save_replaces_previous_state(tmp_path):
    file_path = tmp_path / "opportunities.json"
    opportunity_a = Opportunity("Cern", "Junior Software Developer", date(2026, 10, 30))
    opportunity_b = Opportunity("Anthropic", "Junior ML Engineer", date(2026, 11, 3))

    save_opportunities([opportunity_a], file_path)
    save_opportunities([opportunity_b], file_path)

    loaded_data = load_opportunities(file_path)

    assert len(loaded_data) == 1
    assert loaded_data[0].company == "Anthropic"
    assert loaded_data[0].role == "Junior ML Engineer"
    assert loaded_data[0].deadline == date(2026, 11, 3)
