"""Serialize the catalogue and its browser snapshots."""

from collections import Counter
import json
import re

PREFIX = 'window.STEM_DATA='
CORE_PREFIX = """window.STEM_DATA=(function (data) {
    const {layouts, stringFields, strings, rows} = data.events;
    const pooled = new Set(stringFields);
    data.events = rows.map(row => {
        const fields = layouts[row[0]];
        return Object.fromEntries(fields.map((key, index) => {
            const value = row[index + 1];
            return [key, typeof value === 'number' && pooled.has(key) ? strings[value] : value];
        }));
    });
    return data;
})(
"""
CORE_SUFFIX = '\n);\n'


def compact_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def write_source_catalog(path, catalog):
    """Use one line per event so the canonical file has readable record diffs."""
    fields = []
    for key, value in catalog.items():
        if key == 'events' and value:
            encoded = '[\n' + ',\n'.join('    ' + compact_json(event) for event in value) + '\n  ]'
        else:
            encoded = json.dumps(value, ensure_ascii=False, indent=2).replace('\n', '\n  ')
        fields.append('  ' + compact_json(key) + ': ' + encoded)
    path.write_text('{\n' + ',\n'.join(fields) + '\n}\n')


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


def pack_events(events):
    # Numeric references are unambiguous only in fields that contain strings.
    string_fields = set()
    other_fields = set()
    layouts = {}
    for event in events:
        layouts.setdefault(tuple(event), len(layouts))
        for key, value in event.items():
            (string_fields if isinstance(value, str) else other_fields).add(key)
    string_fields -= other_fields
    counts = Counter(value for event in events for key, value in event.items()
                     if key in string_fields and len(value) >= 20)
    strings = [value for value, count in counts.most_common() if count > 1]
    references = {value: index for index, value in enumerate(strings)}
    rows = [
        [layouts[tuple(event)], *(references.get(value, value) if key in string_fields else value
                                 for key, value in event.items())]
        for event in events
    ]
    return dict(layouts=[list(fields) for fields in layouts],
                stringFields=sorted(string_fields), strings=strings, rows=rows)


def packed_core(web):
    core = core_data(web)
    core['events'] = pack_events(core['events'])
    return core


def write_web_data(assets, web):
    (assets / 'data.js').write_text(PREFIX + compact_json(web) + ';\n')
    (assets / 'atlas-core.js').write_text(CORE_PREFIX + compact_json(packed_core(web)) + CORE_SUFFIX)


def verify_core_data(site, web):
    encoded = (site / 'assets/atlas-core.js').read_text()
    assert encoded.startswith(CORE_PREFIX) and encoded.endswith(CORE_SUFFIX), 'Unexpected Atlas decoder'
    packed = json.loads(encoded[len(CORE_PREFIX):-len(CORE_SUFFIX)])
    assert packed == packed_core(web), 'Packed catalogue and dossier links differ from the full snapshot'
    report = site / 'downloads/STEM_camp_programmes_deep_2026_2027.json'
    assert json.loads(report.read_text()) == web['camp_programmes'], 'On-demand dossiers differ from the full snapshot'
    scripts = re.findall(r'<script\b[^>]*\bsrc="([^"]+)"', (site / 'index.html').read_text())
    script_paths = [url.split('?', 1)[0] for url in scripts]
    assert script_paths.count('assets/atlas-core.js') == 1 and 'assets/data.js' not in script_paths
    assert script_paths.index('assets/atlas-core.js') < script_paths.index('assets/app.js')
