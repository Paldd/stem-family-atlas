"""Build a complete independent Spanish edition using committed translations."""
import csv
import hashlib
import html
import json
import re
import shutil
import sqlite3
import tempfile
import zipfile
from pathlib import Path
from localization import (ROOT,RU,protected,translate,translate_tree,translate_markup,
                          unfold_ics,collect_pool,english_pool)
from database_download import package_json,package_database
from spanish_workbook import write_workbook
from spanish_calendar import localize_calendar
from spanish_legacy_workbook import translate_workbook

DIST=ROOT/'dist'; ES=DIST/'es'; OUT=ES/'downloads'
UI_VERSION=int(re.search(r'data-ui-version="(\d+)"',(DIST/'index.html').read_text()).group(1))
dictionary=json.loads((ROOT/'data/i18n/es.json').read_text())
dictionary.update(json.loads((ROOT/'data/i18n/es-reviewed.json').read_text()))
missing=(collect_pool()|english_pool())-dictionary.keys()
assert not missing, 'Spanish edition incomplete: '+str(len(missing))+' strings; '+repr(sorted(missing)[:8])
ES.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True);(ES/'assets').mkdir(exist_ok=True)

def sha(value):return hashlib.sha256(value).hexdigest()
def tr(s):return translate(s,dictionary)

# Share non-language assets; project-relative URLs work on GitHub Pages and localhost.
for p in (DIST/'assets').rglob('*'):
    if p.is_file():
        q=ES/'assets'/p.relative_to(DIST/'assets');q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)

manifest=json.loads((ROOT/'data/i18n/ui-source-tokens.json').read_text())
regexes={'/^(Да|Explore|Junior|Little Coders|Little|Codey)/i':'/^(Sí|Explore|Junior|Little Coders|Little|Codey)/i',
         '/^Нет/':'/^No/','/^Нет/i':'/^No/i',
         '/Условно|уточни|подтвер|требуе|не провер/i':'/Condicional|aclar|confirm|requie|sin verificar/i',
         '/^Условно/':'/^Condicional/',
         '/^Начало курса · /':'/^Inicio del curso · /',
         '/^(Да|Explore|Junior)/i':'/^(Sí|Explore|Junior)/i',
         '/ё/g':'/ё/g'}
for file,spec in manifest.items():
    source=(DIST/file).read_text();assert sha(source.encode())==spec['sha256'], 'Refresh UI translation tokens: '+file
    body=source.encode('utf-16-le')
    for t in sorted(spec['tokens'],key=lambda t:t['start'],reverse=True):
        if t['type']=='regex':value=regexes[t['raw']]
        elif t['type']=='template':value=translate_markup(t['raw'],dictionary).replace('`','\\`')
        else:value=json.dumps(translate_markup(t['value'],dictionary) if '<' in t['value'] else tr(t['value']),ensure_ascii=False)
        left,right=t['start']*2,t['end']*2
        assert body[left:right].decode('utf-16-le')==t['raw']
        body=body[:left]+value.encode('utf-16-le')+body[right:]
    result=body.decode('utf-16-le')
    result=result.replace("'ru-RU'","'es'").replace('"ru-RU"','"es"').replace("'ru'","'es'").replace('"ru"','"es"')
    if file=='assets/experience.js':
        result=re.sub(r"\.replace\(/ё/g,(?:'[^']*'|\"[^\"]*\")\)",'',result)
        result=result.replace("const isNo=v=>/^No/i.test(v||'');", "const isNo=v=>window.STEM_FIT_TEXT.no.includes(v||'');")
        result=result.replace("/^(Sí|Explore|Junior)/i.test(e[k]||'')", "window.STEM_FIT_TEXT.journey_yes.includes(e[k]||'')")
    if file=='assets/app.js':
        result=result.replace('PRODID:-//STEM Atlas//Family calendar//RU','PRODID:-//STEM Atlas//Family calendar//ES')
        result=re.sub(r'const yes=s=>[^\n]+;', "const yes=s=>window.STEM_FIT_TEXT.yes.includes(s), no=s=>window.STEM_FIT_TEXT.no.includes(s), maybe=s=>window.STEM_FIT_TEXT.maybe.includes(s);",result,count=1)
        result=result.replace('/^Condicional/.test(e.mat)','window.STEM_FIT_TEXT.conditional.includes(e.mat)').replace('/^Condicional/.test(e.osc)','window.STEM_FIT_TEXT.conditional.includes(e.osc)')
        old="Object.values(e).join(' ').toLocaleLowerCase('es').includes(state.query.toLocaleLowerCase('es'))"
        new="foldSearch(Object.values(e).join(' ')+' '+e.themes.map(t=>DIRECTIONS.labels[t]||t).join(' ')).includes(foldSearch(state.query))"
        assert old in result,'Refresh Spanish search adaptation'
        result=result.replace(old,new)
        fold="const foldSearch=s=>String(s).normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('es');"
        assert result.startswith("'use strict';")
        result=result.replace("'use strict';","'use strict';\n"+fold,1)
    if file=='assets/camp-planning.js':result=result.replace("JSON.stringify(p).toLocaleLowerCase('es')",'foldSearch(JSON.stringify(p))')
    if file=='assets/camp-programmes.js':result=result.replace("cs.query.toLocaleLowerCase('es')",'foldSearch(cs.query)')
    if file=='assets/schools.js':result=result.replace('JSON.stringify(s).toLocaleLowerCase().includes(filters.query.toLocaleLowerCase())','foldSearch(JSON.stringify(s)).includes(foldSearch(filters.query))')
    if file=='assets/leagues.js':result=result.replace("leagueState.query.trim().toLocaleLowerCase('es')",'foldSearch(leagueState.query.trim())').replace("JSON.stringify(g).toLocaleLowerCase('es')",'foldSearch(JSON.stringify(g))')
    (ES/file).write_text(result)

web=json.loads((DIST/'assets/data.js').read_text().removeprefix('window.STEM_DATA=').rstrip(';\n'))
translated=translate_tree(web,dictionary)
(ES/'assets/data.js').write_text('window.STEM_DATA='+json.dumps(translated,ensure_ascii=False,separators=(',',':'))+';\n')
fit_values={e[k] for e in web['events'] for k in ['mat','osc']}
fit_patterns={'yes':r'^(Да|Explore|Junior|Little Coders|Little|Codey)','no':r'^Нет','maybe':r'Условно|уточни|подтвер|требуе|не провер','conditional':r'^Условно','journey_yes':r'^(Да|Explore|Junior)'}
fit_text={k:sorted({tr(v) for v in fit_values if re.search(pattern,v,re.I if k in ['yes','maybe','journey_yes'] else 0)}) for k,pattern in fit_patterns.items()}
for v in fit_values:
    for k,pattern in fit_patterns.items():
        assert (tr(v) in fit_text[k])==bool(re.search(pattern,v,re.I if k in ['yes','maybe','journey_yes'] else 0)), 'Ambiguous translated age classification: '+repr(v)
(ES/'assets/fit-text.js').write_text('window.STEM_FIT_TEXT='+json.dumps(fit_text,ensure_ascii=False,separators=(',',':'))+';\n')

def html_tag(match):
    tag=match.group()
    def attr(m):
        name,value=m.group(1),m.group(2)
        if name in ['href','src','id','class','style'] or not RU.search(value):return m.group()
        return name+'="'+html.escape(tr(html.unescape(value)),quote=True)+'"'
    return re.sub(r'([\w-]+)="([^"]*)"',attr,tag)

page=(DIST/'index.html').read_text()
parts=re.split(r'(<[^>]+>)',page)
page=''.join(html_tag(re.match(r'[\s\S]+',p)) if p.startswith('<') else html.escape(tr(html.unescape(p)),quote=False) for p in parts if p)
page=page.replace('<html lang="ru">','<html lang="es">').replace('aria-label="Language"','aria-label="Idioma"')
page=page.replace('data-atlas-language="ru" href="./" lang="ru" aria-current="page"','data-atlas-language="ru" href="../" lang="ru" aria-current="false"')
page=page.replace('data-atlas-language="es" href="es/" lang="es" aria-current="false"','data-atlas-language="es" href="./" lang="es" aria-current="page"')
page=page.replace('<script src="assets/app.js', f'<script src="assets/fit-text.js?v={UI_VERSION}"></script>\n  <script src="assets/app.js')
page=re.sub(r'href="downloads/[^"<>]+\.xlsx"','href="downloads/STEM_atlas_es.xlsx"',page)
page=page.replace('</footer>','<p class="family-note">Edición en español de los materiales existentes: traducción automática con revisión de términos principales. La traducción no actualiza la fecha de verificación de las fuentes. Para los requisitos oficiales, consulte los enlaces del organizador.</p></footer>')
(ES/'index.html').write_text(page)

# Translate every existing public text download, retaining filenames and source URLs.
for p in sorted((DIST/'downloads').iterdir()):
    q=OUT/p.name
    if p.suffix=='.json':q.write_text(json.dumps(translate_tree(json.loads(p.read_text()),dictionary),ensure_ascii=False,indent=2)+'\n')
    elif p.suffix=='.md':
        lines=[]
        for line in p.read_text().splitlines():
            result=tr(line)
            prefix=re.match(r'^(?:#{1,6}\s+|[-*]\s+|\d+\.\s+)',line)
            if prefix and not result.startswith(prefix.group()):result=prefix.group()+re.sub(r'^(?:#{1,6}\s*|[-*]\s*|\d+\.\s*)','',result)
            lines.append(result.rstrip())
        q.write_text('\n'.join(lines).rstrip()+'\n')
    elif p.suffix=='.csv':
        def cell(value):
            if value.startswith(('[','{')):
                try:return json.dumps(translate_tree(json.loads(value),dictionary),ensure_ascii=False)
                except json.JSONDecodeError:pass
            return tr(value)
        with p.open(encoding='utf-8-sig',newline='') as inp,q.open('w',encoding='utf-8-sig',newline='') as out:
            csv.writer(out).writerows([[cell(c) for c in row] for row in csv.reader(inp)])
    elif p.suffix=='.ics':q.write_bytes(localize_calendar(p.read_text(),web,translated))
    elif p.suffix=='.xlsx':translate_workbook(p,q,dictionary)
    elif p.suffix not in ['.zip','.sqlite']:shutil.copyfile(p,q)

# Complete JSON and relational exports. Every table, source and foreign key is kept.
catalog=translate_tree(json.loads((ROOT/'data/catalog.json').read_text()),dictionary)
raw=OUT/'STEM_database.json';raw.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
json_manifest=package_json(raw,language='es')
ru_manifest=json.loads((DIST/'downloads/STEM_database_download.json').read_text())
with tempfile.TemporaryDirectory() as tmp:
    original=Path(tmp)/'source.sqlite'
    with zipfile.ZipFile(DIST/'downloads'/ru_manifest['download']) as z:original.write_bytes(z.read(ru_manifest['sqlite_entry']))
    src=sqlite3.connect(original);q=OUT/'STEM_database.sqlite';q.unlink(missing_ok=True);db=sqlite3.connect(q);src.backup(db);src.close()
    tables=[r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    for table in tables:
        columns=[r[1] for r in db.execute('PRAGMA table_info("'+table+'")')]
        rows=db.execute('SELECT rowid,* FROM "'+table+'"').fetchall()
        for row in rows:
            changed={}
            for col,value in zip(columns,row[1:]):
                if not isinstance(value,str):continue
                if col.endswith('_json') or (table=='metadata' and col=='value' and value.startswith(('{','['))):
                    replacement=json.dumps(translate_tree(json.loads(value),dictionary),ensure_ascii=False)
                elif RU.search(value) or value.strip() in dictionary:replacement=tr(value)
                else:continue
                if replacement!=value:changed[col]=replacement
            if changed:db.execute('UPDATE "'+table+'" SET '+','.join('"'+k+'"=?' for k in changed)+' WHERE rowid=?',[*changed.values(),row[0]])
    db.commit();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not db.execute('PRAGMA foreign_key_check').fetchall();db.close()
database_manifest=package_database(q,language='es')
workbook_counts=write_workbook(OUT/'STEM_atlas_es.xlsx',translated)
report=dict(language='es',source_language='ru',translation_method='local neural translation with reviewed interface and protected numeric values',
            source_research_asof=web['asof'],ui_version=UI_VERSION,source_strings=len(collect_pool()),english_prose_strings=len(english_pool()),missing_strings=0,
            complete_human_linguistic_review=False,
            events=len(web['events']),competitions=sum(e['block']=='Соревнования' for e in web['events']),
            camp_dossiers=len(web['camp_programmes']['profiles']),schools=len(web['schools']),league_profiles=len(web['league_guide']['profiles']),
            preserved_record_ids=True,original_russian_available=True,translated_downloads=len(list(OUT.iterdir())))
report['workbook_sheets']=workbook_counts
(OUT/'STEM_translation_coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/i18n/coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
