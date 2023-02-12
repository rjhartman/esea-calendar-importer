import cfscrape
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime
from dateutil import parser
from config import config
from better_profanity import profanity


ESEA_URL = "https://play.esea.net"
UNASSIGNED_MATCH_TITLE = "Default time for ESEA Match (unassigned)"


@dataclass
class Match:
    date: datetime
    map: str
    title: str
    enemy_team: Optional[str] = None
    id: Optional[int] = None

    @property
    def url(self):
        return f"{ESEA_URL}/match/{self.id}" if self.id else None


team_number = config.esea_team_number


def parse_match(match: Dict[str, any]) -> Match:
    """Parses a match returned by ESEA's API

    Args:
        match (Dict[str, any]): The match returned by ESEA

    Returns:
        Match: A dataclass containing the match's information
    """
    date = match["date"]
    enemy_team = None
    map = None
    if home_team := match.get("home"):
        enemy_team = match["away" if home_team["id"] == team_number else "home"]["name"]
        if config.censor:
            enemy_team = profanity.censor(enemy_team)
    if isinstance(match["map"], dict):
        map = match["map"]["id"]
    return Match(
        date=parser.parse(date),
        id=match.get("id"),
        enemy_team=enemy_team,
        map=map if map else "Pending map veto",
        title=f"ESEA match vs. {enemy_team}" if enemy_team else UNASSIGNED_MATCH_TITLE,
    )


def get_all_matches() -> List[Match]:
    """Gets all matches for the configured ESEA team

    Returns:
        List[Match]: All matches for the configured ESEA team
    """
    scraper = cfscrape.create_scraper()
    res = scraper.get(f"{ESEA_URL}/api/teams/{team_number}/matches")
    data = res.json()["data"]
    return [parse_match(match) for match in data]


def get_assigned_matches() -> List[Match]:
    """Gets only the confirmed matches for the configured ESEA team

    Returns:
        List[Match]: All matches that have assigned teams
    """
    return [m for m in get_all_matches() if m.title != UNASSIGNED_MATCH_TITLE]
