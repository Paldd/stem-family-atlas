"""Fail release on a missing translation, dropped record, broken link or changed fact."""
import hashlib
import json
import re
import sqlite3
import tempfile
import zipfile
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from localization import ROOT,RU,protected,collect_pool,english_pool,unfold_ics,translate,technical_facts_match,machine_value

DIST=ROOT/'dist';ES=DIST/'es'
dictionary=json.loads((ROOT/'data/i18n/es.json').read_text())
dictionary.update(json.loads((ROOT/'data/i18n/es-reviewed.json').read_text()))
missing=(collect_pool()|english_pool())-dictionary.keys();assert not missing,repr(sorted(missing)[:10])
read=lambda base:json.loads((base/'assets/data.js').read_text().removeprefix('window.STEM_DATA=').rstrip(';\n'))
ru=read(DIST);es=read(ES)
assert ru.keys()==es.keys()
numeric=re.compile(r'\d+(?:[.,]\d+)*')
for source,target in dictionary.items():
    assert not RU.search(target), 'Untranslated dictionary value: '+source[:120]
    assert numeric.findall(source)==numeric.findall(target), 'Dictionary numeric mismatch: '+repr((source,target))
    assert technical_facts_match(source,target), 'Dictionary technical condition mismatch: '+repr((source,target))
    assert len(target)<=len(source)*4+150, 'Abnormally long translation: '+source
preserved=0;translated=0
def compare(a,b,path=''):
    global preserved,translated
    assert type(a)==type(b),path
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for k,v in a.items():compare(v,b[k],path+'/'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(v,w) in enumerate(zip(a,b)):compare(v,w,path+'/'+str(i))
    elif isinstance(a,str):
        if not RU.search(a) and (machine_value(a) or re.fullmatch(r'[a-z][a-z0-9_./-]*',a)):assert a==b,path+' changed a machine identifier'
        if (not RU.search(a) and a.strip() not in dictionary) or protected(a):assert a==b,path;preserved+=1
        else:
            assert not RU.search(b),path+' contains untranslated Cyrillic'
            assert numeric.findall(a)==numeric.findall(b),path+' changed numeric facts: '+repr((a,b))
            assert technical_facts_match(a,b),path+' changed a technical condition'
            translated+=1
    else:assert a==b,path
compare(ru,es)
for block in ['events','schools']:
    assert [e['id'] for e in ru[block]]==[e['id'] for e in es[block]]
for original,localized in zip(ru['events'],es['events']):
    assert re.match(r'^P\d',original['priority']).group()==re.match(r'^P\d',localized['priority']).group(),original['id']+' changed priority code'
assert [p['id'] for p in ru['league_guide']['profiles']]==[p['id'] for p in es['league_guide']['profiles']]
assert [p['slug'] for p in ru['camp_programmes']['profiles']]==[p['slug'] for p in es['camp_programmes']['profiles']]

class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.text=[];self.lang=None
    def handle_data(self,text):
        if RU.search(text):self.text.append(text.strip())
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='html':self.lang=attrs.get('lang')
        if 'id' in attrs:self.ids.add(attrs['id'])
        for key,value in attrs.items():
            if key not in ['href','src']:continue
            url=urlsplit(value)
            if url.scheme or url.netloc or not url.path:continue
            target=(ES/unquote(url.path)).resolve()
            assert target.is_relative_to(DIST.resolve()),value
            if target.is_dir():target=target/'index.html'
            assert target.is_file(),value
# Original page IDs are the inventory; its links have a different relative base.
ru_ids=set(re.findall(r'\bid="([^"]+)"',(DIST/'index.html').read_text()))
page=Page();page.feed((ES/'index.html').read_text())
assert page.lang=='es' and not page.text,repr(page.text)
assert ru_ids==page.ids,'A section or control was dropped'

out=ES/'downloads'
for kind in ['json','sqlite']:
    name='STEM_database_json_download.json' if kind=='json' else 'STEM_database_download.json'
    manifest=json.loads((out/name).read_text());archive=out/manifest['download']
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==manifest['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        data=z.read(manifest[kind+'_entry'])
        assert not RU.search(z.read('README.txt').decode())
    assert hashlib.sha256(data).hexdigest()==manifest[kind+'_sha256']
    if kind=='json':
        export=json.loads(data);compare(json.loads((ROOT/'data/catalog.json').read_text()),export,'full-export')
    else:
        with tempfile.TemporaryDirectory() as tmp:
            p=ROOT/Path(tmp)/'export.sqlite';p.write_bytes(data)
            con=sqlite3.connect(p)
            assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
            assert not con.execute('PRAGMA foreign_key_check').fetchall()
            assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==len(es['events'])
            assert con.execute('SELECT COUNT(*) FROM camp_programmes').fetchone()[0]==len(es['camp_programmes']['profiles'])
            original_manifest=json.loads((DIST/'downloads/STEM_database_download.json').read_text())
            original_path=Path(tmp)/'original.sqlite'
            with zipfile.ZipFile(DIST/'downloads'/original_manifest['download']) as z:
                original_path.write_bytes(z.read(original_manifest['sqlite_entry']))
            original=sqlite3.connect(original_path)
            tables=original.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
            assert tables==con.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
            for table,schema in tables:
                columns=[row[1] for row in original.execute('PRAGMA table_info("'+table+'")')]
                old=original.execute('SELECT * FROM "'+table+'" ORDER BY rowid').fetchall()
                new=con.execute('SELECT * FROM "'+table+'" ORDER BY rowid').fetchall()
                assert len(old)==len(new),'SQLite rows lost: '+table
                for i,(a,b) in enumerate(zip(old,new)):
                    for key,v,w in zip(columns,a,b):
                        if key.endswith('_json') or (table=='metadata' and key=='value' and v.startswith(('{','['))):
                            compare(json.loads(v),json.loads(w),'SQLite/'+table+'/'+str(i)+'/'+key)
                        else:compare(v,w,'SQLite/'+table+'/'+str(i)+'/'+key)
            original.close()
            con.close()
with zipfile.ZipFile(out/'STEM_atlas_es.xlsx') as z:
    assert z.testzip() is None
    ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    first=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    ids=[r.find('x:c/x:is/x:t',ns).text for r in first.findall('x:sheetData/x:row',ns)][1:]
    assert ids==[e['id'] for e in es['events'] if e['block']=='Competiciones']
    for name in z.namelist():ET.fromstring(z.read(name))
for p in (DIST/'downloads').glob('*.xlsx'):
    with zipfile.ZipFile(p) as original,zipfile.ZipFile(out/p.name) as localized:
        assert original.namelist()==localized.namelist(),p.name+' dropped workbook components'
        sheets=ET.fromstring(original.read('xl/workbook.xml')).findall('{*}sheets/{*}sheet')
        names={s.attrib['name']:translate(s.attrib['name'],dictionary) for s in sheets}
        for file in original.namelist():
            if not file.endswith('.xml'):assert original.read(file)==localized.read(file);continue
            a=ET.fromstring(original.read(file));b=ET.fromstring(localized.read(file))
            old=list(a.iter());new=list(b.iter());assert len(old)==len(new),p.name+'/'+file
            for x,y in zip(old,new):
                assert x.tag==y.tag,p.name+'/'+file
                if x.tag.split('}')[-1] in ['f','definedName']:
                    formula=x.text or ''
                    for old_name,new_name in names.items():formula=formula.replace("'"+old_name+"'!", "'"+new_name+"'!")
                    assert formula==(y.text or ''),p.name+' changed a formula'
                elif x.text is not None:compare(x.text,y.text,p.name+'/'+file)
                assert x.attrib.keys()==y.attrib.keys(),p.name+'/'+file
                for key,value in x.attrib.items():
                    if key=='location':
                        for old_name,new_name in names.items():value=value.replace("'"+old_name+"'!", "'"+new_name+"'!")
                        assert value==y.attrib[key],p.name+' changed a cell link'
                    else:compare(value,y.attrib[key],p.name+'/'+file+'/'+key)
for p in (DIST/'downloads').glob('*.csv'):
    old=list(csv.reader(p.open(encoding='utf-8-sig',newline='')))
    new=list(csv.reader((out/p.name).open(encoding='utf-8-sig',newline='')))
    assert len(old)==len(new),p.name
    assert all(len(a)==len(b) for a,b in zip(old,new)),p.name
for p in (DIST/'downloads').glob('*.md'):
    old=p.read_text();new=(out/p.name).read_text()
    assert len(re.findall(r'^#{1,6}\s',old,re.M))==len(re.findall(r'^#{1,6}\s',new,re.M)),p.name+' lost headings'
    urls=lambda text:set(re.findall(r'https?://[^\s<>"\]\)]+',text))
    assert urls(old)==urls(new),p.name+' changed source links'
for p in (DIST/'downloads').glob('*.ics'):
    old=unfold_ics(p.read_text());new=unfold_ics((out/p.name).read_text())
    assert len(old)==len(new),p.name+' changed calendar structure'
    for a,b in zip(old,new):
        key=a.partition(':')[0]
        if key in ['SUMMARY','DESCRIPTION','LOCATION','X-WR-CALNAME']:
            assert key==b.partition(':')[0],p.name+' changed property type'
            assert not RU.search(b),p.name+' contains untranslated calendar text'
            assert numeric.findall(a)==numeric.findall(b),p.name+' changed calendar numeric facts: '+repr((a[:200],b[:200]))
        elif key=='PRODID':assert b==a.removesuffix('//RU')+'//ES'
        else:assert a==b,p.name+' changed scheduling property '+key
report=dict(language='es',missing_translations=0,events=len(es['events']),competitions=sum(e['block']=='Competiciones' for e in es['events']),
            camps=len(es['camp_programmes']['profiles']),schools=len(es['schools']),league_profiles=len(es['league_guide']['profiles']),
            preserved_values_checked=preserved,translated_values_checked=translated,all_sections_preserved=True,
            numeric_values_and_technical_operators_preserved=True,complete_exports_verified=True)
print(json.dumps(report))
