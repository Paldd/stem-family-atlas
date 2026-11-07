"""Integrate Latin American exhibitions and the current SESI competition calendar."""
import json
from pathlib import Path


def enrich_v207(data):
    path = Path(__file__).resolve().parents[1] / 'data/latam-expo-sesi-fod-native-v207.json'
    facts = json.loads(path.read_text())
    events = data['events']
    existing_events = {row['id']: row for row in events}
    release_ids = {row['id'] for row in facts['new_events']}
    events[:] = [row for row in events if row['id'] not in release_ids]
    events.extend(existing_events.get(row['id'], row) for row in facts['new_events'])
    source_urls = {row['url'] for row in data['sources']}
    data['sources'].extend(row for row in facts['sources'] if row['url'] not in source_urls)

    profile = facts['league_profile']
    profiles = data['league_guide']['profiles']
    current_profile = next((row for row in profiles if row['id'] == profile['id']), profile)
    profiles[:] = [row for row in profiles if row['id'] != profile['id']]
    profiles.append(current_profile)
    first = next(row for row in profiles if row['id'] == 'first')
    first['event_ids'] = list(dict.fromkeys([*first['event_ids'], *profile['event_ids']]))
