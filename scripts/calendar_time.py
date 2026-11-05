"""Convert sourced local schedules consistently on old and new host tzdbs."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# Official B.C. rule, checked 2026-11-05:
# https://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/daylight-saving-time
# America/Vancouver covers the Surrey/Langley venues in this release. This does
# not apply the provincial rule to the distinct mountain-time regions of B.C.
BC_PERMANENT_PACIFIC_START = datetime(2026, 3, 8, 3)
BC_PACIFIC = timezone(timedelta(hours=-7))


def local_to_utc(day, clock, zone):
    local = datetime.fromisoformat(day + 'T' + clock)
    tz = BC_PACIFIC if zone == 'America/Vancouver' and local >= BC_PERMANENT_PACIFIC_START else ZoneInfo(zone)
    return local.replace(tzinfo=tz).astimezone(timezone.utc)
