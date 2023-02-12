"""Module for interacting with the configured Google calendar"""

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from esea import Match
from config import config
from typing import Dict, List

# If modifying these scopes, delete the .cache directory
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",
]

CREDENTIALS_PATH = Path.cwd() / "credentials.json"
CACHE_PATH = Path.cwd() / ".cache"
TOKEN_PATH = CACHE_PATH / "token.json"

CACHE_PATH.mkdir(exist_ok=True)

creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)

service = build("calendar", "v3", credentials=creds)


def get_events(start: datetime, end: datetime) -> List[Dict]:
    """Retrieves the events on the configured calendar in the given time range.

    Args:
        start (datetime): The start of the time range to fetch
        end (datetime): The end of the time range to fetch

    Returns:
        List[Dict]: A list of event dictionaries as returned by Google
    """
    return (
        service.events()
        .list(
            calendarId=config.google_calendar_id,
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        .get("items", [])
    )


def get_match_event_body(match: Match) -> Dict:
    """Gets the Google Calendar API event payload for an ESEA match

    Args:
        match (Match): The ESEA match to create an event for

    Returns:
        Dict: The payload that can be sent to the Google Calendar API
    """
    return {
        "start": {
            "dateTime": match.date.isoformat(),
        },
        "end": {"dateTime": (match.date + timedelta(hours=1)).isoformat()},
        "reminders": {"useDefault": True},
        "summary": match.title,
        "description": f"Match page: {match.url}\n\nAutomatically imported on {datetime.utcnow().strftime('%c')} UTC.",
        "location": match.map,
    }


def create_match_event(match: Match):
    """Creates an event on the configured Google calendar for an ESEA match

    Args:
        match (Match): The ESEA match to create an event for
    """
    service.events().insert(
        calendarId=config.google_calendar_id, body=get_match_event_body(match)
    ).execute()


def update_match_event(match: Match, event: Dict):
    """Updates an existing event with the information for an ESEA match

    Args:
        match (Match): The ESEA match to update the event's information to
        event (Dict): The existing event's data as returned by Google's API
    """
    service.events().update(
        calendarId=config.google_calendar_id,
        eventId=event["id"],
        body=event | get_match_event_body(match),
    ).execute()


def create_or_update_match(match: Match) -> None:
    """Idempotently creates or updates an ESEA match's event on the calendar

    Args:
        match (Match): The ESEA match to create or update an event for
    """
    events = get_events(
        match.date - timedelta(minutes=1), match.date + timedelta(hours=1, minutes=1)
    )
    existing_event = None
    for event in events:
        if event["summary"] == match.title:
            existing_event = event
            break
    else:
        print(f"Creating new event for {match}")
        create_match_event(match)
        return
    print(f"Updating existing event for {match}")
    update_match_event(match, existing_event)
