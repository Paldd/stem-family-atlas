"""Package the complete database, verifying its bytes before removing an oversize raw export."""
import hashlib
import json
from pathlib import Path
import zipfile

STATIC_FILE_LIMIT = 26_214_400

def package_json(raw_path, max_file_bytes=STATIC_FILE_LIMIT, language='ru'):
    """Keep the complete JSON portable as it grows beyond the hosting file limit."""
    raw_path = Path(raw_path)
    body = raw_path.read_bytes()
    json.loads(body)  # Validate the actual export before packaging it.
    digest = hashlib.sha256(body).hexdigest()
    archive = raw_path.with_name(raw_path.stem + '_json.zip')
    readme = ('STEM Family Atlas — полная база JSON\n'
              'Распакуйте STEM_database.json: внутри все записи и источники.\n'
              'Сжатие не удаляет данные. SHA-256 JSON: ' + digest + '\n').encode('utf-8')
    if language == 'es':
        readme = ('STEM Family Atlas — base JSON completa en español\n'
                  'Extraiga STEM_database.json: contiene todos los registros y fuentes.\n'
                  'La compresión conserva todos los datos. SHA-256 JSON: '+digest+'\n').encode('utf-8')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, content in [(raw_path.name, body), ('README.txt', readme)]:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert z.namelist() == [raw_path.name, 'README.txt']
        assert z.read(raw_path.name) == body
    archive_body = archive.read_bytes()
    assert len(archive_body) <= STATIC_FILE_LIMIT, 'Portable JSON exceeds hosting file limit'
    available = len(body) <= max_file_bytes
    manifest = dict(schema_version=1, download=archive.name, archive_bytes=len(archive_body),
                    archive_sha256=hashlib.sha256(archive_body).hexdigest(),
                    json_entry=raw_path.name, json_bytes=len(body), json_sha256=digest,
                    raw_download_available=available, complete_database=True,
                    instructions='Распакуйте ZIP: внутри полная база JSON и README. Все записи сохранены.')
    if language == 'es':
        manifest['instructions'] = 'Extraiga el ZIP: contiene la base JSON completa y README. Se conservan todos los registros.'
        manifest['language'] = 'es'
    raw_path.with_name(raw_path.stem + '_json_download.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    if not available:
        raw_path.unlink()
    return manifest

def package_database(raw_path, max_file_bytes=STATIC_FILE_LIMIT, language='ru'):
    raw_path = Path(raw_path)
    body = raw_path.read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    archive = raw_path.with_suffix('.zip')
    readme = ('STEM Family Atlas — полная база SQLite\n'
              'Распакуйте STEM_database.sqlite и откройте его в программе для SQLite.\n'
              'Все таблицы, записи и источники сохранены; сжатие не удаляет данные.\n'
              'SHA-256 SQLite: ' + digest + '\n').encode('utf-8')
    if language == 'es':
        readme = ('STEM Family Atlas — base SQLite completa en español\n'
                  'Extraiga STEM_database.sqlite y ábrala con un lector SQLite.\n'
                  'Se conservan todas las tablas, registros y fuentes.\n'
                  'SHA-256 SQLite: '+digest+'\n').encode('utf-8')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, content in [(raw_path.name, body), ('README.txt', readme)]:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert z.namelist() == [raw_path.name, 'README.txt']
        assert z.read(raw_path.name) == body
    archive_body = archive.read_bytes()
    # Fail before deleting the raw database if the portable export itself is too big.
    assert len(archive_body) <= STATIC_FILE_LIMIT, 'Portable database exceeds hosting file limit'
    raw_available = len(body) <= max_file_bytes
    manifest = dict(schema_version=1, download=archive.name, archive_bytes=len(archive_body),
                    archive_sha256=hashlib.sha256(archive_body).hexdigest(),
                    sqlite_entry=raw_path.name, sqlite_bytes=len(body), sqlite_sha256=digest,
                    raw_download_available=raw_available, complete_database=True,
                    instructions='Распакуйте архив: внутри полная база SQLite и README. Сжатие без удаления записей.')
    if language == 'es':
        manifest['instructions'] = 'Extraiga el ZIP: contiene la base SQLite completa y README. La compresión no elimina registros.'
        manifest['language'] = 'es'
    raw_path.with_name('STEM_database_download.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    if not raw_available:
        raw_path.unlink()
    return manifest
