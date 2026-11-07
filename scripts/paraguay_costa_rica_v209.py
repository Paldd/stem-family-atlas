"""Integrate the sourced Paraguay and Costa Rica calendar and school updates."""
import json
from pathlib import Path

from camp_catalog_bridge import RELATED
from nearby_wro_v191 import _upsert


def _facts():
    path = Path(__file__).resolve().parents[1] / 'data/paraguay-costa-rica-native-v209.json'
    return json.loads(path.read_text())


def register_links_v209():
    RELATED.update({f'mot-asuncion-{track}': ['L161'] for track in
                    ['retro', 'movie', 'escape', 'pygamers', 'lego', 'eco']})


def enrich_v209(data):
    facts = _facts()
    assert facts['version'] == 209
    events = data['events']
    existing = {e['id']: e for e in events}
    managed = {e['id'] for e in facts['new_events']}
    events[:] = [e for e in events if e['id'] not in managed]
    events.extend(existing.get(e['id'], e) for e in facts['new_events'])
    for ident, patch in facts['event_updates'].items():
        existing[ident].update(patch)

    data['schools'] = _upsert(data['schools'], facts['schools'])
    planning = data['camp_planning']
    planning['offers'] = _upsert(planning['offers'], [facts['budget_offer']])
    history = data['school_history']
    history['entities'] = _upsert(history['entities'], facts['history_entities'])
    history['results'] = _upsert(history['results'], facts['history_results'])
    history['coverage'] = _upsert(history['coverage'], facts['history_coverage'])
    route = facts['family_route']
    history['family_routes'] = [r for r in history['family_routes'] if r['name'] != route['name']] + [route]
    history.update(version=209, checked=facts['checked'])

    known = {s['url'] for s in data['sources']}
    data['sources'].extend(s for s in facts['sources'] if s['url'] not in known)
