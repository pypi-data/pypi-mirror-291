"""This module provides functions for managing resources in TeamUp (calendar app)."""

import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DEFAULT_CALENDAR_ID = os.getenv("TEAMUP_DEFAULT_CALENDAR_ID") or "zXXXXXX"

TEAMUP_TOKEN = os.getenv("TEAMUP_TOKEN")
TEAMUP_BEARER_TOKEN = os.getenv("TEAMUP_BEARER_TOKEN")
if not TEAMUP_TOKEN or not TEAMUP_BEARER_TOKEN:
    raise OSError(
        "Required environment variables TEAMUP_TOKEN or TEAMUP_BEARER_TOKEN not set. Please set them in a env file."
    )


class TeamUP:
    """Returns an object for interacting with the TeamUP."""

    _BASE_URL = "https://api.teamup.com/"

    def __init__(self):
        """Initialize the TeamUP object."""
        self.headers = {
            "Teamup-Token": TEAMUP_TOKEN,
            "Accept": "application/json",
            "Authorization": f"Bearer {TEAMUP_BEARER_TOKEN}",
        }

    def _request(self, method: str, resource: str, **kwargs) -> dict:
        url = self._BASE_URL + resource
        response = requests.request(
            method=method, url=url, headers=self.headers, timeout=20.00, **kwargs
        )
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {"status": "success"}
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(
                f"Failed to {method} for url -> {url}: {response.status_code} - {response.text}"
            ) from e

    def get(self, resource: str, params=None) -> dict:
        """General request."""
        return self._request(method="GET", resource=resource, params=params)

    def put(self, resource: str, params=None) -> dict:
        """General request."""
        return self._request(method="PUT", resource=resource, params=params)

    def delete(self, resource: str, params=None) -> dict:
        """General request."""
        return self._request(method="DELETE", resource=resource, params=params)

    def post(self, resource: str, params: dict | None = None, data: dict | None = None) -> dict:
        """General request."""
        return self._request(method="POST", resource=resource, params=params, json=data)

    def get_calendar(self, calendar_key_or_id: str) -> dict:
        """Get information of calendar by its key or id.

        Either the calendar_secret_key (ksXXXXX)
        Or calendar_id (tied to user account - requires login creds)
        """
        return self.get(f"{calendar_key_or_id}/configuration")["configuration"]

    def get_subcalendars(self, calendar_key_or_id: str) -> list[dict]:
        """Returns children calendars for given calendar id."""
        return self.get(f"{calendar_key_or_id}/subcalendars")["subcalendars"]

    def get_subcalendar_id_from_name(
        self, calendar_key_or_id: str, calendar_name: str
    ) -> int | None:
        """Returns subcalendar_id for the given calendar_name under the main_calendar_K_ID provided."""
        sub_calendars = self.get_subcalendars(calendar_key_or_id)
        for sub_calendar in sub_calendars:
            if sub_calendar["name"] == calendar_name:
                return int(sub_calendar["id"])
        return None

    def delete_subcalendar(self, calendar_key_or_id: str, subcalendar_id: int) -> str:
        """Deletes a subcalendar from the specified calendar.

        Returns a success message if the deletion was successful.
        """
        response_status = self.delete(
            resource=f"{calendar_key_or_id}/subcalendars/{subcalendar_id}"
        )
        return response_status["status"]

    def get_calendar_events(
        self, calendar_key_or_id: str, query: dict | None = None
    ) -> list[dict]:
        """Returns events for today if date range not given.

        Ex. Query parameters for events for the specific date.
        dates = {
            "startDate": "2024-07-19",
            "endDate": "2024-07-19",
        }
        """
        return self.get(f"{calendar_key_or_id}/events", params=query)["events"]

    def create_calendar_event(
        self, calendar_key_or_id: str, calendar_event: "CalendarEvent"
    ) -> dict:
        """Creates event for specified calendar, provided the CalendarEvent object.

        Returns: response in the general formal of a dictionary.
            Ex. { "event": {"id": "string", "subcalendar_ids": list, ...} }
        """
        if not isinstance(calendar_event, self.CalendarEvent):
            raise TypeError("The method create_calendar_event requires a CalendarEvent object.")
        response = self.post(
            f"{calendar_key_or_id}/events", data=calendar_event._convert_to_dict()
        )
        event = response.get("event")
        event["undo_id"] = response.get("undo_id")  # type: ignore
        return event  # type: ignore

    def delete_calendar_event(
        self,
        calendar_key_or_id: str,
        event_id: str,
        recuring_deletion: "RecurringDeletion" = None,  # type: ignore
    ) -> str:
        """Deletes an event from the specified calendar.

        Returns: undo_id for this deletion action.
        """
        params = {"reddit": recuring_deletion.value if recuring_deletion else None}
        return self.delete(resource=f"{calendar_key_or_id}/events/{event_id}", params=params)[
            "undo_id"
        ]

    @dataclass
    class CalendarEvent:
        """Data class used to create events in teamup. By default all parameters are null except for the required ones.

        - Required parameters of subcalendar_ids and title. The minimum information required to
        create an event.
        - start_dt and end_dt, these are set to be all day events (by default).

        """

        subcalendar_ids: list[int | None]
        title: str
        start_dt: datetime = field(
            default_factory=lambda: datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        )
        end_dt: datetime = field(
            default_factory=lambda: datetime.now().replace(
                hour=0, minute=59, second=59, microsecond=0
            )
        )
        all_day: bool = False
        rrule: str | None = None
        notes: str | None = None
        location: str | None = None
        who: str | None = None
        signup_enabled: bool = False
        comments_enabled: bool = False
        custom: dict[str, str | list[str]] | None = None

        def _convert_to_dict(self) -> dict:
            """Convert the dataclass to a dictionary. Required for the API request."""
            if not isinstance(self, dict):
                event_dict = asdict(self)
                # Convert datetime fields to string format
                if isinstance(event_dict["start_dt"], datetime):
                    event_dict["start_dt"] = event_dict["start_dt"].isoformat()
                if isinstance(event_dict["end_dt"], datetime):
                    event_dict["end_dt"] = event_dict["end_dt"].isoformat()
            else:
                event_dict = self
            return event_dict

    class RecurringDeletion(Enum):
        """Enum class for specifying types of recurring deletions."""

        SINGLE = "single"
        FUTURE = "future"
        ALL = "all"
