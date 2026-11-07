"""Apply the ADC source snapshot, preserving stable event and league IDs."""
from pathlib import Path
import json


def enrich_v197(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                       'data/adc-global-native-v197.json').read_text())
    additions = {event['id']: event for event in facts['new_events']}
    updates = {row['id']: row['fields'] for row in facts['event_updates']}
    seen = {event['id'] for event in data['events']}
    for index, event in enumerate(data['events']):
        if event['id'] in updates:
            event.update(updates[event['id']])
        if event['id'] in additions:
            data['events'][index] = additions[event['id']]
    data['events'].extend(event for event in facts['new_events'] if event['id'] not in seen)
    for index, profile in enumerate(data['league_guide']['profiles']):
        if profile['id'] in facts['league_updates']:
            data['league_guide']['profiles'][index] = facts['league_updates'][profile['id']]
