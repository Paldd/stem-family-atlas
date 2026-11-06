"""ITU worldwide chapter audit and reviewed national learning routes."""
import json
from pathlib import Path


def _upsert(existing, additions):
    managed = {row['id']: row for row in additions}
    seen = {row['id'] for row in existing}
    return [managed.get(row['id'], row) for row in existing] + [
        row for row in additions if row['id'] not in seen]


def enrich_v188(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                        'data/world-routes-native-v188.json').read_text())
    assert facts['version'] == 188
    data['events'] = _upsert(data['events'], facts['event_records'])
    data['schools'] = _upsert(data['schools'], facts['school_records'])
    guide = data['league_guide']
    guide['profiles'] = _upsert(guide['profiles'], facts['league_profiles'])
    guide.update(version=188, checked=facts['checked'])
    history = data['school_history']
    history['entities'] = _upsert(history['entities'], facts['history_entities'])
    history['results'] = _upsert(history['results'], facts['history_results'])
    history.update(version=188, checked=facts['checked'])
    for route in data['national_routes']['routes']:
        route.update(facts['route_patches'].get(route['id'], {}))
    for source in facts['sources']:
        if not any(old['url'] == source['url'] for old in data['sources']):
            data['sources'].append(source)
    for country in data['countries']:
        if country['iso'] in facts['new_country_codes']:
            country['coverage'] = facts['coverage_note']
