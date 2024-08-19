"""Test general functions for teamup api."""

from unittest.mock import patch

import pytest

from teamup_connect import DEFAULT_CALENDAR_ID, TeamUP


@pytest.fixture(scope="session")
def teamup() -> TeamUP:
    """Return the TeamUP object that handles all contact with the api."""
    return TeamUP()


def test__get_calendar(teamup: TeamUP):
    """Test the get_calendar function."""
    with patch.object(teamup, "get_calendar", return_value={}) as mock_get_calendar:
        calendar = teamup.get_calendar("12345")
        mock_get_calendar.assert_called_once_with("12345")
        assert isinstance(calendar, dict)


@pytest.mark.calls_api
def test__create_and_delete_event(teamup: TeamUP):
    """Test the create and delete event functions."""
    # Get the ID of the first sub-calendar
    sub_calendar = teamup.get_subcalendars(DEFAULT_CALENDAR_ID)[0]
    sub_calendar_id = sub_calendar["id"]
    sub_calendar_name = sub_calendar["name"]
    # create a new calendar event object
    new_cal_event = teamup.CalendarEvent([sub_calendar_id], "pytest event")
    # create the event in the Teamup calendar
    created_cal_event = teamup.create_calendar_event(DEFAULT_CALENDAR_ID, new_cal_event)
    created_cal_id = created_cal_event["id"]
    # Check if the event was actually created
    assert created_cal_id
    # Delete the event from the Teamup calendar
    undo_id = teamup.delete_calendar_event(DEFAULT_CALENDAR_ID, created_cal_id)
    # Check if the event was actually deleted
    print(
        f"Succesfully deleted event with id:{created_cal_id}, from calendar: {sub_calendar_name}, with undo_id: {undo_id}"
    )
    assert undo_id
