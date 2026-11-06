"""Reviewed Levant routes and bilingual camps, retaining unresolved admission gates."""
import json
from pathlib import Path


def _facts():
    return json.loads((Path(__file__).resolve().parents[1] /
                       'data/levant-camps-native-v189.json').read_text())


def _upsert(existing, additions):
    managed = {row['id']: row for row in additions}
    seen = {row['id'] for row in existing}
    return [managed.get(row['id'], row) for row in existing] + [
        row for row in additions if row['id'] not in seen]


def register_links_v189():
    from camp_catalog_bridge import RELATED
    RELATED.update(_facts()['profile_links'])


def enrich_v189(data):
    facts = _facts()
    assert facts['version'] == 189
    data['events'] = _upsert(data['events'], facts['event_records'])
    guide = data['league_guide']
    guide['profiles'] = _upsert(guide['profiles'], facts['league_profiles'])
    guide.update(version=189, checked=facts['checked'])
    planning = data['camp_planning']
    planning['offers'] = _upsert(planning['offers'], facts['budget_offers'])
    for route in data['national_routes']['routes']:
        route.update(facts['route_patches'].get(route['id'], {}))
    for source in facts['sources']:
        existing = next((old for old in data['sources']
                         if old['url'] == source['url']), None)
        if existing is None:
            data['sources'].append(source)
        elif 'evidence' not in existing:
            existing['evidence'] = source['evidence']
    for country in data['countries']:
        if country['iso'] in facts['new_country_codes']:
            country['coverage'] = facts['coverage_note']
