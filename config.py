from pathlib import Path
from schema import config_validator
import json


class Config:
    google_calendar_id: str
    esea_team_number: int
    censor: bool

    def __init__(self):
        with open(Path.cwd() / "config.json", "r") as config_file:
            config = json.load(config_file)

        if not config_validator.validate(config):
            raise ValueError(
                f"config.json is invalid!\n{json.dumps(config_validator.errors, indent=2)}"
            )

        self.esea_team_number = config["esea"]["team_number"]
        self.google_calendar_id = config["google_calendar"]["id"]
        self.censor = config["esea"]["censor"]


config = Config()
