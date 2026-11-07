"""Integrate verified seasonal fixtures and the distinct Bebras directory."""
import json
from pathlib import Path


def enrich_v201(data):
    path = Path(__file__).resolve().parents[1] / 'data/bebras-games-native-v201.json'
    facts = json.loads(path.read_text())
    data['asof'] = max(data['asof'], facts['checked'])
    events = {event['id']: event for event in data['events']}
    for row in facts['events']:
        if row['id'] not in events:
            data['events'].append(row)
            events[row['id']] = row
    for event_id, patch in facts['event_updates'].items():
        events[event_id].update(patch)

    guide = data['league_guide']
    updates = {profile['id']: profile for profile in facts['league_updates']}
    for profile in guide['profiles']:
        update = updates.get(profile['id'])
        if update is not None:
            # Older profile snapshots must preserve fixtures added to the current catalogue.
            update['event_ids'] = list(dict.fromkeys(update['event_ids'] + profile['event_ids']))
    guide['profiles'] = [updates.pop(profile['id'], profile) for profile in guide['profiles']]
    guide['profiles'].extend(updates.values())

    directory = data['national_routes']
    prior_ids = {route['id'] for route in directory['routes']}
    assert not prior_ids.intersection(route['id'] for route in facts['routes'])
    directory['routes'].extend(facts['routes'])
    directory['pathways'].append(facts['pathway'])
    directory['summary'].update(
        routes=len(directory['routes']),
        countries=len({route['iso'] for route in directory['routes']}),
        bebras_directory_cards=len(facts['routes']),
        bebras_routes_with_local_rule=sum(route['evidence_level']=='operator_calendar' for route in facts['routes']),
    )
    countries = {country['iso']: country for country in data['countries']}
    for route in facts['routes']:
        countries[route['iso']]['network_route_ids'].append(route['id'])

    known_sources = {source['url'] for source in data['sources']}
    data['sources'].extend(source for source in facts['sources'] if source['url'] not in known_sources)
