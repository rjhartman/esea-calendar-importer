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
    title: str
    map: str
    enemy_team: Optional[str] = None


team_number = config.esea_team_number


def parse_match(match: Dict[str, any]) -> Match:
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
        map=map if map else "Pending map veto",
        title=f"ESEA match vs. {enemy_team}" if enemy_team else UNASSIGNED_MATCH_TITLE,
        enemy_team=enemy_team,
    )


def get_all_matches() -> List[Match]:
    scraper = cfscrape.create_scraper()
    res = scraper.get(f"{ESEA_URL}/api/teams/{team_number}/matches")
    data = res.json()["data"]
    return [parse_match(match) for match in data]


def get_confirmed_matches() -> List[Match]:
    return [m for m in get_all_matches() if m.title != UNASSIGNED_MATCH_TITLE]
