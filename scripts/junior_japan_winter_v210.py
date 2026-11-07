"""Integrate verified junior routes, winter programmes and public STEM events."""
import json
from pathlib import Path

from nearby_wro_v191 import _upsert


def enrich_v210(data):
    path = Path(__file__).resolve().parents[1] / 'data/junior-japan-winter-native-v210.json'
    facts = json.loads(path.read_text())
    assert facts['version'] == 210

    events = data['events']
    existing = {e['id']: e for e in events}
    managed = {e['id'] for e in facts['new_events']}
    events[:] = [e for e in events if e['id'] not in managed]
    events.extend(existing.get(e['id'], e) for e in facts['new_events'])
    for ident, patch in facts['event_updates'].items():
        existing[ident].update(patch)

    planning = data['camp_planning']
    planning['offers'] = _upsert(planning['offers'], facts['budget_offers'])
    guide = data['league_guide']
    guide['profiles'] = _upsert(guide['profiles'], facts['league_profiles'])
    rcj = next(p for p in guide['profiles'] if p['id'] == 'rcj')
    rcj['event_ids'] = list(dict.fromkeys([*rcj['event_ids'], *facts['rcj_event_ids']]))

    known = {s['url'] for s in data['sources']}
    data['sources'].extend(s for s in facts['sources'] if s['url'] not in known)
