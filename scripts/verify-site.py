"""Check that the published site contains the committed research and complete exports."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sqlite3
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile
from atlas_web_data import read_web_data, verify_core_data
from atlas_workbook import WORKBOOKS, verify_workbook
from calendar_time import local_to_utc, session_keys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
source = json.loads((ROOT / 'data/catalog.json').read_text())
web = read_web_data(DIST / 'assets/data.js')
verify_core_data(DIST, web)
for key in ['events', 'countries', 'schools', 'league_guide', 'development_routes', 'camp_programmes']:
    assert web[key] == source[key], f'Browser data diverges from source: {key}'
for key in ['events', 'schools']:
    ids = [row['id'] for row in web[key]]
    assert len(ids) == len(set(ids)), f'Duplicate IDs in {key}'
events_by_id = {row['id']: row for row in web['events']}
for alias in (row for row in web['events'] if row.get('canonical_event_id')):
    target = events_by_id.get(alias['canonical_event_id'])
    assert target and target['block'] == alias['block'] and not target.get('canonical_event_id'), (
        f"Invalid canonical target for {alias['id']}: {alias['canonical_event_id']}")
for profile in web['league_guide']['profiles']:
    assert profile['group'] in web['league_guide']['groups'], (
        f"Unknown league filter group: {profile['id']} / {profile['group']}")
profiles = web['camp_programmes']['profiles']
assert len({p['slug'] for p in profiles}) == len(profiles)
assert web['camp_programmes']['counts']['dossiers'] == len(profiles)
camp_markdown=(DIST/'downloads/STEM_camp_programmes_deep_2026_2027.md').read_text()
markdown_ids=re.findall(r'^## (CP\d+) · ',camp_markdown,re.M)
assert len(markdown_ids)==len(profiles) and set(markdown_ids)=={p['id'] for p in profiles}, 'Detailed camp report is stale or incomplete'
markdown_parts=re.split(r'^## (CP\d+) · ',camp_markdown,flags=re.M)
markdown_blocks=dict(zip(markdown_parts[1::2],markdown_parts[2::2]))
for profile in profiles:
    block=markdown_blocks[profile['id']]
    assert profile['programme'] in block, profile['id']+' programme missing from detailed report'
    assert all(s['url'] in block for s in profile['sources']), profile['id']+' source missing from detailed report'
assert (DIST / 'assets/directions.js').is_file()

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ['href', 'src'] or not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path:
                continue
            assert not url.path.startswith('/'), f'Link loses the GitHub Pages project prefix: {value}'
            target = (DIST / unquote(url.path)).resolve()
            assert target.is_relative_to(DIST.resolve())
            if target.is_dir():
                target = target / 'index.html'
            assert target.is_file(), f'Missing linked asset: {value}'

html = (DIST / 'index.html').read_text()
Links().feed(html)
assert re.search(r'data-ui-version="\d+"', html)

downloads = DIST / 'downloads'
assert re.findall(r'href="downloads/([^"]+\.xlsx)"', html) == [
    WORKBOOKS['ru'], WORKBOOKS['ru'], 'STEM_семейный_календарь_2026-2027.xlsx'
], 'The current atlas and original audit must have distinct Excel links'
verify_workbook(downloads / WORKBOOKS['ru'], web, 'ru')
db_manifest = json.loads((downloads / 'STEM_database_download.json').read_text())
archive = downloads / db_manifest['download']
assert hashlib.sha256(archive.read_bytes()).hexdigest() == db_manifest['archive_sha256']
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    db = z.read(db_manifest['sqlite_entry'])
assert hashlib.sha256(db).hexdigest() == db_manifest['sqlite_sha256']
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / 'catalogue.sqlite'
    path.write_bytes(db)
    con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0] == len(web['events'])
    assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0] == len(profiles)
    con.close()
json_manifest = json.loads((downloads / 'STEM_database_json_download.json').read_text())
archive = downloads / json_manifest['download']
assert hashlib.sha256(archive.read_bytes()).hexdigest() == json_manifest['archive_sha256']
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    body = z.read(json_manifest['json_entry'])
assert hashlib.sha256(body).hexdigest() == json_manifest['json_sha256']
assert json.loads(body) == source
for name in ['STEM_подтвержденные_даты.ics', 'STEM_крупные_выставки.ics']:
    body = (downloads / name).read_text()
    assert body.startswith('BEGIN:VCALENDAR') and body.rstrip().endswith('END:VCALENDAR')
    assert body.count('BEGIN:VEVENT') == body.count('END:VEVENT')
    uids = re.findall(r'(?m)^UID:(.+)$', re.sub(r'\r?\n[ \t]', '', body))
    assert len(uids) == len(set(uids)) == body.count('BEGIN:VEVENT'), name
# Permanent Canadian time rules must work with older host tzdbs.
assert local_to_utc('2026-12-21', '09:00', 'America/Vancouver').isoformat() == '2026-12-21T16:00:00+00:00'
assert local_to_utc('2027-07-05', '09:00', 'America/Vancouver').isoformat() == '2027-07-05T16:00:00+00:00'
assert local_to_utc('2026-02-26', '09:00', 'America/Edmonton').isoformat() == '2026-02-26T16:00:00+00:00'
assert local_to_utc('2027-02-26', '09:00', 'America/Edmonton').isoformat() == '2027-02-26T15:00:00+00:00'
assert local_to_utc('2026-12-21', '09:00', 'America/Los_Angeles').isoformat() == '2026-12-21T17:00:00+00:00'
calendar = re.sub(r'\r?\n[ \t]', '', (downloads / 'STEM_подтвержденные_даты.ics').read_text())
calendar_rows = {re.search(r'(?m)^UID:(.+)$', block).group(1): block
                 for block in re.findall(r'BEGIN:VEVENT\n.*?END:VEVENT', calendar, re.S)}
for event in web['events']:
    sessions = event.get('sessions', [])
    for key, session in zip(session_keys(event['id'], sessions), sessions):
        if not session.get('ical_timed') or session['date'] < web['asof']:
            continue
        for instant, clock in [('start_utc', 'start_time'), ('end_utc', 'end_time')]:
            expected = local_to_utc(session['date'], session[clock], session['timezone']).isoformat().replace('+00:00', 'Z')
            assert session[instant] == expected, (event['id'], session['date'], instant)
        uid = 'stem-' + key + '@family-stem.local'
        if uid in calendar_rows:
            for property_name, field in [('DTSTART', 'start_utc'), ('DTEND', 'end_utc')]:
                value = session[field].replace('-', '').replace(':', '')
                assert property_name + ':' + value in calendar_rows[uid], (uid, property_name)
print(json.dumps({'events': len(web['events']), 'camp_dossiers': len(profiles),
                  'schools': len(web['schools']), 'leagues': len(web['league_guide']['profiles']),
                  'source_matches_browser': True, 'full_exports_verified': True,
                  'project_relative_links_verified': True, 'timed_calendar_exports_consistent': True}))
