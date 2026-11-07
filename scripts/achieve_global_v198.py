"""Apply the reviewed Achieve snapshot without changing stable record IDs."""
from pathlib import Path
import json


def enrich_v198(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                        'data/achieve-global-native-v198.json').read_text())
    additions = {event['id']: event for event in facts['new_events']}
    updates = {row['id']: row['fields'] for row in facts['event_updates']}
    seen = {event['id'] for event in data['events']}
    for index, event in enumerate(data['events']):
        if event['id'] in updates:
            event.update(updates[event['id']])
        if event['id'] in additions:
            data['events'][index] = additions[event['id']]
    data['events'].extend(event for event in facts['new_events'] if event['id'] not in seen)
    profiles = data['league_guide']['profiles']
    seen_profiles = {profile['id'] for profile in profiles}
    for index, profile in enumerate(profiles):
        if profile['id'] in facts['league_updates']:
            profiles[index] = facts['league_updates'][profile['id']]
    profiles.extend(profile for key, profile in facts['league_updates'].items()
                    if key not in seen_profiles)
