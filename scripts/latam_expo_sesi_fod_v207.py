"""Integrate Latin American exhibitions and the current SESI competition calendar."""
import json
from pathlib import Path


def enrich_v207(data):
    path = Path(__file__).resolve().parents[1] / 'data/latam-expo-sesi-fod-native-v207.json'
    facts = json.loads(path.read_text())
    event_ids = {row['id'] for row in data['events']}
    data['events'].extend(row for row in facts['new_events'] if row['id'] not in event_ids)
    source_urls = {row['url'] for row in data['sources']}
    data['sources'].extend(row for row in facts['sources'] if row['url'] not in source_urls)

    profile = facts['league_profile']
    profiles = data['league_guide']['profiles']
    if all(row['id'] != profile['id'] for row in profiles):
        profiles.append(profile)
    first = next(row for row in profiles if row['id'] == 'first')
    first['event_ids'] = list(dict.fromkeys([*first['event_ids'], *profile['event_ids']]))
