"""Reduce the Pages artifact size without changing any exported JSON values."""

import json
from pathlib import Path

from atlas_web_data import compact_json


def main():
    dist = Path(__file__).resolve().parents[1] / 'dist'
    files = 0
    saved = 0
    for folder in (dist / 'downloads', dist / 'es/downloads'):
        for path in sorted(folder.glob('*.json')):
            size = path.stat().st_size
            if size < 1_000_000:
                continue
            value = json.loads(path.read_bytes())
            body = (compact_json(value) + '\n').encode('utf-8')
            if len(body) >= size:
                continue
            assert json.loads(body) == value, path
            path.write_bytes(body)
            files += 1
            saved += size - len(body)
    print(f'Compacted {files} JSON downloads, saving {saved:,} bytes')


if __name__ == '__main__':
    main()
