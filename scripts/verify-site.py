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

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
source = json.loads((ROOT / 'data/catalog.json').read_text())
text = (DIST / 'assets/data.js').read_text().strip()
assert text.startswith('window.STEM_DATA=') and text.endswith(';')
web = json.loads(text[len('window.STEM_DATA='):-1])
for key in ['events', 'countries', 'schools', 'league_guide', 'development_routes', 'camp_programmes']:
    assert web[key] == source[key], f'Browser data diverges from source: {key}'
for key in ['events', 'schools']:
    ids = [row['id'] for row in web[key]]
    assert len(ids) == len(set(ids)), f'Duplicate IDs in {key}'
profiles = web['camp_programmes']['profiles']
assert len({p['slug'] for p in profiles}) == len(profiles)
assert web['camp_programmes']['counts']['dossiers'] == len(profiles)
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
            assert target.is_file(), f'Missing linked asset: {value}'

html = (DIST / 'index.html').read_text()
Links().feed(html)
assert re.search(r'data-ui-version="\d+"', html)

downloads = DIST / 'downloads'
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
print(json.dumps({'events': len(web['events']), 'camp_dossiers': len(profiles),
                  'schools': len(web['schools']), 'leagues': len(web['league_guide']['profiles']),
                  'source_matches_browser': True, 'full_exports_verified': True,
                  'project_relative_links_verified': True}))
