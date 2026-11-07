"""Integrate the verified WRC schedule and current Chinese exhibition releases."""
import json
from pathlib import Path


def enrich_v205(data):
    path = Path(__file__).resolve().parents[1] / 'data/china-wrc-latam-camps-native-v205.json'
    facts = json.loads(path.read_text())
    events = {event['id']: event for event in data['events']}
    data['events'].extend(row for row in facts['new_events'] if row['id'] not in events)
    for event_id, patch in facts['event_updates'].items():
        events[event_id].update(patch)
    known = {row['url'] for row in data['sources']}
    data['sources'].extend(row for row in facts['sources'] if row['url'] not in known)
    guide = next(row for row in data['league_guide']['profiles'] if row['id'] == 'wrc')
    patch = facts['wrc_guide']
    sources = {row['url']: row for row in [*guide['sources'], *patch['sources']]}
    guide.update(patch, sources=list(sources.values()))
