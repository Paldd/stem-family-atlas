"""Apply the reviewed local WRO calendar and separately scoped qualification history."""
import json
from pathlib import Path


def _upsert(existing, additions):
    managed = {row['id']: row for row in additions}
    seen = {row['id'] for row in existing}
    return [managed.get(row['id'], row) for row in existing] + [
        row for row in additions if row['id'] not in seen]


def enrich_v191(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                       'data/nearby-wro-native-v191.json').read_text())
    assert facts['version'] == 191
    data['events'] = _upsert(data['events'], facts['event_records'])
    guide = data['league_guide']
    guide['profiles'] = _upsert(guide['profiles'], facts['league_profiles'])
    guide.update(version=191, checked=facts['checked'])
    history = data['school_history']
    history['entities'] = _upsert(history['entities'], facts['history_entities'])
    history['results'] = _upsert(history['results'], facts['history_results'])
    history['coverage'] = _upsert(history['coverage'], [facts['history_coverage']])
    history.update(version=191, checked=facts['checked'])
    for route in data['national_routes']['routes']:
        route.update(facts['route_patches'].get(route['id'], {}))
    known_sources = {row['url'] for row in data['sources']}
    for source in facts['sources']:
        assert source['evidence']
        if source['url'] not in known_sources:
            data['sources'].append(source)
            known_sources.add(source['url'])
