"""Apply the sourced CR/Mexico tariff and admission corrections after older passes."""
import json
from pathlib import Path


def enrich_v194(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                       'data/camp-nearby-editorial-native-v194.json').read_text())
    additions = {row['id']: row for row in facts['budget_offers']}
    existing = data['camp_planning']['offers']
    seen = {row['id'] for row in existing}
    data['camp_planning']['offers'] = [additions.get(row['id'], row) for row in existing] + [
        row for row in facts['budget_offers'] if row['id'] not in seen]
    deadlines = {row['event_id']: row for row in facts['deadline_updates']}
    updates = {row['programme_id']: row['fields'] for row in facts['event_updates']}
    for event in data['events']:
        if event.get('camp_programme_id') in updates:
            event.update(updates[event['camp_programme_id']])
        if event['id'] in deadlines:
            update = deadlines[event['id']]
            event.update(deadline=update['deadline'], deadline_label=update['deadline_label'])
