"""Convert sourced local schedules consistently on old and new host tzdbs."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

PERMANENT_LOCAL_TIME = {
    # B.C. Pacific time covers the Surrey and Langley venues.
    # https://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/daylight-saving-time
    'America/Vancouver': (datetime(2026, 3, 8, 3), timezone(timedelta(hours=-7))),
    # Alberta stays on UTC-6 from the first skipped clock change.
    # https://www.alberta.ca/albertas-new-time-system-abt
    'America/Edmonton': (datetime(2026, 11, 1, 2), timezone(timedelta(hours=-6))),
}


def local_to_utc(day, clock, zone):
    local = datetime.fromisoformat(day + 'T' + clock)
    rule = PERMANENT_LOCAL_TIME.get(zone)
    tz = rule[1] if rule and local >= rule[0] else ZoneInfo(zone)
    return local.replace(tzinfo=tz).astimezone(timezone.utc)


def session_keys(event_id, sessions):
    """Keep the first session's calendar ID and number further slots that day."""
    slots = {}
    for session in sessions:
        day = session['date']
        slots[day] = slot = slots.get(day, 0) + 1
        yield f'{event_id}-{day}' if slot == 1 else f'{event_id}-{day}-{slot}'


def timed_public_days(event):
    """Keep the existing calendar UID for the first exact public day."""
    days = event.get('public_days', [])
    if not days or not all(isinstance(day, dict) and day.get('ical_timed') for day in days):
        return []
    dates = [day['date'] for day in days]
    assert dates == sorted(dates), event['id']
    if dates[0] != event['start'] or dates[-1] != event['end']:
        return []
    return [('-' + key if index else '', day)
            for index, (key, day) in enumerate(zip(session_keys('visit', days), days))]
