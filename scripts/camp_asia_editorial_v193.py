"""Apply the sourced Asian camp revisions, retaining previous dates and tariff history."""
import json
from pathlib import Path


def enrich_v193(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                       'data/camp-asia-editorial-native-v193.json').read_text())
    additions = {row['id']: row for row in facts['budget_offers']}
    existing = data['camp_planning']['offers']
    seen = {row['id'] for row in existing}
    data['camp_planning']['offers'] = [additions.get(row['id'], row) for row in existing] + [
        row for row in facts['budget_offers'] if row['id'] not in seen]
    deadlines = {row['event_id']: row for row in facts['deadline_updates']}
    for event in data['events']:
        if event.get('camp_programme_id') == facts['withdrawn_programme_id']:
            event.update(date_status='Анонсировано', date_precision='announced_window',
                         date_rule=facts['withdrawn_announcement_note'], registration_status=facts['withdrawn_announcement_note'],
                         proof=facts['withdrawn_announcement_note'])
        if event['id'] in deadlines:
            update = deadlines[event['id']]
            event.update(deadline=update['deadline'], deadline_label=update['deadline_label'])
