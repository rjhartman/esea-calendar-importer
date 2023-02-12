"""Contains schema and a validator for the config file (config.json)"""
from cerberus import Validator

CONFIG_SCHEMA = {
    "google_calendar": {"type": "dict", "schema": {"id": {"type": "string"}}},
    "esea": {
        "type": "dict",
        "schema": {"team_number": {"type": "integer"}, "censor": {"type": "boolean"}},
    },
}

config_validator = Validator(CONFIG_SCHEMA, require_all=True)
