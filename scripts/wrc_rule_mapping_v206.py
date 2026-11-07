"""Link current World Robot Contest discipline evidence to the season schedule."""
import json
from pathlib import Path


def enrich_v206(data):
    path = Path(__file__).resolve().parents[1] / 'data/wrc-rule-mapping-native-v206.json'
    facts = json.loads(path.read_text())
    events = {event['id']: event for event in data['events']}
    data['events'].extend(row for row in facts['new_events'] if row['id'] not in events)
    for event_id, fields in facts['event_updates'].items():
        events[event_id].update(fields)
    guide = next(row for row in data['league_guide']['profiles'] if row['id'] == 'wrc')
    guide.update(facts['wrc_guide'])
