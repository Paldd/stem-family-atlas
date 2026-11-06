"""Reviewed African routes and programmes; no dates inferred from old seasons."""
import json
from pathlib import Path


def _upsert(existing, additions):
    managed = {row['id']: row for row in additions}
    seen = {row['id'] for row in existing}
    return [managed.get(row['id'], row) for row in existing] + [
        row for row in additions if row['id'] not in seen]


def enrich_v186(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                        'data/africa-routes-native-v186.json').read_text())
    assert facts['version'] == 186
    data['events'] = _upsert(data['events'], facts['event_records'])
    data['schools'] = _upsert(data['schools'], facts['school_records'])
    guide = data['league_guide']
    guide['profiles'] = _upsert(guide['profiles'], facts['league_profiles'])
    for event in data['events']:
        patch = facts['refreshed_event_patches'].get(event['id'])
        if patch:
            event.update(patch)
    for league in guide['profiles']:
        patch = facts['refreshed_league_patches'].get(league['id'])
        if patch:
            league.update(patch)
    for route in data['national_routes']['routes']:
        route.update(facts['route_patches'].get(route['id'], {}))
    history = data['school_history']
    history['entities'] = _upsert(history['entities'], facts['history_entities'])
    history['results'] = _upsert(history['results'], facts['history_results'])
    history.update(version=186, checked=facts['checked'])
    guide.update(version=186, checked=facts['checked'])
    for source in facts['sources']:
        if not any(old['url'] == source['url'] for old in data['sources']):
            data['sources'].append(source)
    for country in data['countries']:
        if country['iso'] in ['LSO', 'SLE', 'SWZ', 'STP']:
            country['coverage'] = facts['coverage_note']
