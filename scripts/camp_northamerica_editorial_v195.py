"""Apply North America camp budgets and sourced early-price reminders."""
import json
from pathlib import Path


def enrich_v195(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                       'data/camp-northamerica-editorial-native-v195.json').read_text())
    offers = data['camp_planning']['offers']
    additions = {row['id']: row for row in facts['budget_offers']}
    seen = {row['id'] for row in offers}
    data['camp_planning']['offers'] = [additions.get(row['id'], row) for row in offers] + [
        row for row in facts['budget_offers'] if row['id'] not in seen]
    deadlines = {row['event_id']: row for row in facts['deadline_updates']}
    for event in data['events']:
        if event['id'] in deadlines:
            row = deadlines[event['id']]
            event.update(deadline=row['deadline'], deadline_label=row['deadline_label'])
