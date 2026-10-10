"""Expose the revision that actually produced a deployed Pages artifact."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
commit = os.environ.get('GITHUB_SHA') or subprocess.check_output(
    ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert re.fullmatch(r'[a-f0-9]{40}', commit)
html = (ROOT / 'dist/index.html').read_text()
version = int(re.search(r'data-ui-version="(\d+)"', html).group(1))
record = dict(source_commit=commit, ui_version=version,
              repository=os.environ.get('GITHUB_REPOSITORY', 'Paldd/stem-family-atlas'),
              branch=os.environ.get('GITHUB_REF_NAME', 'main'),
              built_at_utc=datetime.now(timezone.utc).isoformat(),
              research_asof=json.loads((ROOT / 'data/catalog.json').read_text())['asof'])
if (ROOT/'dist/es/index.html').is_file():
    record['languages'] = ['ru','es']
    record['translation_coverage'] = json.loads((ROOT/'data/i18n/coverage.json').read_text())
    (ROOT/'dist/es/release.json').write_text(json.dumps({**record,'language':'es'},ensure_ascii=False,indent=2)+'\n')
(ROOT / 'dist/release.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(record))
