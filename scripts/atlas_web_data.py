"""Publish the initial Atlas payload and retain the full compatibility snapshot."""
import json
import re

PREFIX = 'window.STEM_DATA='


def read_web_data(path):
    text = path.read_text().strip()
    assert text.startswith(PREFIX) and text.endswith(';'), path
    return json.loads(text[len(PREFIX):-1])


def core_data(web):
    core = {key: value for key, value in web.items() if key != 'camp_programmes'}
    camps = web['camp_programmes']
    slugs = {profile['id']: profile['slug'] for profile in camps['profiles']}
    core['camp_dossier_links'] = {
        link['event_id']: slugs[link['programme_id']] for link in camps['event_links']
    }
    return core


def write_web_data(assets, web):
    for name, data in [('data.js', web), ('atlas-core.js', core_data(web))]:
        (assets / name).write_text(PREFIX + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')


def verify_core_data(site, web):
    core = read_web_data(site / 'assets/atlas-core.js')
    assert core == core_data(web), 'Initial catalogue and dossier links differ from the full snapshot'
    report = site / 'downloads/STEM_camp_programmes_deep_2026_2027.json'
    assert json.loads(report.read_text()) == web['camp_programmes'], 'On-demand dossiers differ from the full snapshot'
    scripts = re.findall(r'<script\b[^>]*\bsrc="([^"]+)"', (site / 'index.html').read_text())
    script_paths = [url.split('?', 1)[0] for url in scripts]
    assert script_paths.count('assets/atlas-core.js') == 1 and 'assets/data.js' not in script_paths
    assert script_paths.index('assets/atlas-core.js') < script_paths.index('assets/app.js')
