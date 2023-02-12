from esea import get_assigned_matches
from google_calendar import create_or_update_match


def main() -> None:
    for match in get_assigned_matches():
        create_or_update_match(match)


if __name__ == "__main__":
    main()
