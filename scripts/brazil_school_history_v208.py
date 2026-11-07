"""Apply sourced FIRST results and school dossiers from the Latin American review."""
import json
from pathlib import Path

from nearby_wro_v191 import _upsert


def enrich_v208(data):
    path = Path(__file__).resolve().parents[1] / 'data/brazil-school-history-native-v208.json'
    facts = json.loads(path.read_text())
    assert facts['version'] == 208

    data['schools'] = _upsert(data['schools'], facts['school_dossiers'])
    history = data['school_history']
    aliases = set(facts['retired_entity_aliases'])
    history['entities'] = _upsert(
        [row for row in history['entities'] if row['id'] not in aliases], facts['history_entities'])
    history['results'] = _upsert(history['results'], facts['history_results'])
    history['coverage'] = _upsert(history['coverage'], facts['history_coverage'])
    route = facts['family_route']
    history['family_routes'] = [r for r in history['family_routes'] if r['name'] != route['name']] + [route]
    history['gaps'] = list(dict.fromkeys([*history['gaps'], facts['history_gap']]))
    history.update(version=208, checked=facts['checked'], conclusion=facts['conclusion'])

    urls = {source['url'] for source in data['sources']}
    data['sources'].extend(source for source in facts['sources'] if source['url'] not in urls)
