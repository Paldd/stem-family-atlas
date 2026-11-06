"""Apply reviewed mandatory camp costs without changing unrelated budget scenarios."""
import json
from pathlib import Path


def enrich_v192(data):
    facts = json.loads((Path(__file__).resolve().parents[1] /
                       'data/camp-editorial-native-v192.json').read_text())
    assert facts['version'] == 192
    additions = {row['id']: row for row in facts['budget_offers']}
    existing = data['camp_planning']['offers']
    seen = {row['id'] for row in existing}
    data['camp_planning']['offers'] = [additions.get(row['id'], row) for row in existing] + [
        row for row in facts['budget_offers'] if row['id'] not in seen]
