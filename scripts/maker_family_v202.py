"""Apply current family visitor and national science fair evidence."""
import json
from pathlib import Path


def enrich_v202(data):
    path = Path(__file__).resolve().parents[1] / 'data/maker-family-native-v202.json'
    facts = json.loads(path.read_text())
    events = {event['id']: event for event in data['events']}
    data['events'].extend(row for row in facts['new_events'] if row['id'] not in events)
    for event_id, patch in facts['event_updates'].items():
        events[event_id].update(patch)
    known = {row['url'] for row in data['sources']}
    data['sources'].extend(row for row in facts['sources'] if row['url'] not in known)
