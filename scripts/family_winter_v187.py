"""Reviewed winter programmes and local routes, with closed-entry and age gates."""
import json
from pathlib import Path


def _upsert(existing, additions):
    managed = {row['id']: row for row in additions}
    seen = {row['id'] for row in existing}
    return [managed.get(row['id'], row) for row in existing] + [
        row for row in additions if row['id'] not in seen]


def enrich_v187(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                        'data/family-winter-native-v187.json').read_text())
    assert facts['version'] == 187
    data['events'] = _upsert(data['events'], facts['event_records'])
    guide = data['league_guide']
    guide['profiles'] = _upsert(guide['profiles'], facts['league_profiles'])
    guide.update(version=187, checked=facts['checked'])
    for event in data['events']:
        event.update(facts['refreshed_event_patches'].get(event['id'], {}))
        if event.get('camp_programme_id') == facts['closed_course_profile']:
            event['priority'] = 'P4 — срок записи прошёл'
            event['registration_status'] = 'Форма закрыта; новый набор не объявлен.'
    for source in facts['sources']:
        if not any(old['url'] == source['url'] for old in data['sources']):
            data['sources'].append(source)
