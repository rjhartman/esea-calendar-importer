# ESEA Google Calendar Importer

An over-complicated python script to automatically import upcoming ESEA matches into your Google calendar of choice.

## Requirements

- Python >= 3.10
- Node.js (for Cloudflare compliant web scraper)

## Setup & Usage

1. Edit `config.json` in the project's root to valid values.
2. Install dependencies (recommended in a virtual environment):

```sh
$ pip install -r requirements.txt
```

3. Follow the [quickstart guide](https://developers.google.com/calendar/api/quickstart/python#enable_the_api) for the Google Calendar API to enable the API and download OAuth credentials. Save this to `credentials.json` in the project's root.

4. Run the script!

```sh
$ python main.py
```

Upon running, the script will ask you to authenticate via OAuth in your default browser. Log in and allow access to calendars/events. Once logged in, the OAuth token will be cached under `.cache`, so this will not be necessary again until the token expires.

## Configuration Values

Below are the configuration values allowed in `config.json`. All are required for the script to run.

| Key                  | Description                                                                                                                                                      | Type   |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| `esea.team_number`   | Your ESEA team number (e.g: https://play.esea.net/teams/<team_number>).                                                                                          | `int`  |
| `esea.censor`        | Whether or not to censor enemy team names when importing them to the calendar. Uses [better-profanity](https://pypi.org/project/better-profanity/), not perfect. | `bool` |
| `google_calendar.id` | The Google Calendar ID to create match events on. You can get this under "Integrate calendar" in calendar settings.                                              | `str`  |
