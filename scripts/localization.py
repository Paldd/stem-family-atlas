"""Deterministic Spanish build helpers; inference is never run during deployment."""
import csv
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
RU = re.compile('[А-Яа-яЁё]')
TECH_OPERATORS = ['≤','≥','×','±','+','%','$','€','£','₹','₡','₩','¥','元']
PRESERVED_TERMS = ['CHF','USD','EUR','CAD','SGD','HKD','MYR','THB','JPY','KRW','MXN','CRC','CNY','TWD','SEK','NOK','NZD','AUD','INR','AED','ILS','NT$','HST','GST','VAT','LEGO','VEX','SPIKE','EV3','Scratch','Python','C++','micro:bit','Arduino','WeDo','RoboCup','RoboRAVE','MakeX','WER','RECF','TIRT','RoboFest','FLL','FRC','FTC','FIRST','Codeavour','ENJOY','CRL','VIQRC','V5RC','WRO']
URLS = re.compile(r'https?://[^\s<>"\]\)]+')
EMAILS = re.compile(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
def has_term(value,term):
    return bool(re.search(r'(?<![A-Za-z])'+re.escape(term)+r'(?![A-Za-z])',value,0 if term in {'FIRST','ENJOY','Scratch','Python'} else re.I))
@lru_cache(maxsize=131072)
def technical_facts_match(source,target):
    return (all(source.count(c)==target.count(c) for c in TECH_OPERATORS)
            and URLS.findall(source)==URLS.findall(target)
            and EMAILS.findall(source)==EMAILS.findall(target)
            and all(not has_term(source,term) or has_term(target,term) for term in PRESERVED_TERMS))
def machine_value(value):
    return bool(re.fullmatch(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',value) or
                re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*',value)
                and (any(c in value for c in '_./-') or re.fullmatch(r'[0-9a-fA-F]{12,}',value)))
# URLs, stable file names and official evidence links must remain byte-identical.
PROTECTED = re.compile(r'https?://[^\s<>"\]\)]+|(?:downloads/|assets/)[^\s<>"\']+|`[^`]+`|\]\([^\)]+\)')
FRAGMENT = re.compile(r'[^<>"\'`$\{\}\n\\]+')

def protected(value):
    return bool(re.match(r'^(?:https?://|(?:downloads/|assets/)|STEM_.*\.(?:md|json|csv|ics|zip|xlsx)$)', value))

def chunks(value):
    if protected(value):
        return
    last = 0
    for match in PROTECTED.finditer(value):
        part = value[last:match.start()].strip()
        if RU.search(part):
            yield part
        last = match.end()
    part = value[last:].strip()
    if RU.search(part):
        yield part

def translate(value, dictionary, missing=None):
    if not isinstance(value, str) or protected(value):
        return value
    if not RU.search(value):
        # English prose is also localized; names, URLs and machine enums are not.
        clean=value.strip()
        if clean not in dictionary:return value
        return value[:len(value)-len(value.lstrip())]+dictionary[clean]+value[len(value.rstrip()):]
    def one(part):
        clean = part.strip()
        if not RU.search(clean):
            return part
        result = dictionary.get(clean)
        if result is None:
            if missing is not None:
                missing.add(clean)
                return part
            raise ValueError('Missing Spanish translation: '+clean[:200])
        return part[:len(part)-len(part.lstrip())]+result+part[len(part.rstrip()):]
    pieces=[];last=0
    for match in PROTECTED.finditer(value):
        pieces.extend([one(value[last:match.start()]), match.group()]);last=match.end()
    pieces.append(one(value[last:]))
    return ''.join(pieces)

def translate_tree(value, dictionary, missing=None):
    if isinstance(value, str):
        return translate(value, dictionary, missing)
    if isinstance(value, list):
        return [translate_tree(x,dictionary,missing) for x in value]
    if isinstance(value, dict):
        return {k:translate_tree(v,dictionary,missing) for k,v in value.items()}
    return value

def collect_tree(value, pool):
    if isinstance(value,str):
        pool.update(chunks(value))
    elif isinstance(value,list):
        for v in value:collect_tree(v,pool)
    elif isinstance(value,dict):
        for v in value.values():collect_tree(v,pool)

def ui_parts(value):
    return [m.group().strip() for m in FRAGMENT.finditer(value) if RU.search(m.group()) and not protected(m.group().strip())]

def translate_markup(value,dictionary,missing=None):
    return FRAGMENT.sub(lambda m:translate(m.group(),dictionary,missing),value)

class HTMLStrings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False);self.strings=set()
    def handle_data(self,value):
        self.strings.update(chunks(html.unescape(value)))
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if value and key not in ['href','src','id','class','style']:
                self.strings.update(chunks(value))

def unfold_ics(value):
    return re.sub(r'\r?\n[ \t]','',value).splitlines()

def collect_pool():
    pool=set()
    for p in (ROOT/'dist/downloads').glob('*.json'):
        collect_tree(json.loads(p.read_text()),pool)
    collect_tree(json.loads((ROOT/'data/catalog.json').read_text()),pool)
    collect_tree(json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').rstrip(';\n')),pool)
    for p in (ROOT/'dist/downloads').glob('*.md'):
        for line in p.read_text().splitlines():pool.update(chunks(line))
    for p in (ROOT/'dist/downloads').glob('*.csv'):
        for row in csv.reader(p.open(encoding='utf-8-sig',newline='')):
            for value in row:
                if value.startswith(('[','{')):
                    try:
                        collect_tree(json.loads(value),pool)
                        continue
                    except json.JSONDecodeError:pass
                pool.update(chunks(value))
    from spanish_legacy_workbook import workbook_strings
    for p in (ROOT/'dist/downloads').glob('*.xlsx'):pool.update(workbook_strings(p))
    parser=HTMLStrings();parser.feed((ROOT/'dist/index.html').read_text());pool.update(parser.strings)
    manifest=json.loads((ROOT/'data/i18n/ui-source-tokens.json').read_text())
    for file in manifest.values():
        for token in file['tokens']:
            if token['type']=='regex':continue
            if token['type']=='template' or '<' in token['value']:
                pool.update(ui_parts(token['value']))
            else:pool.update(chunks(token['value']))
    return pool

@lru_cache(maxsize=1)
def english_pool():
    """English source-condition prose, excluding protected official names."""
    folder=ROOT/'data/i18n'
    pool=set(json.loads((folder/'en-source-strings.json').read_text()))
    names=set(json.loads((folder/'preserved-official-names.json').read_text()))
    codes=set(json.loads((folder/'preserved-source-values.json').read_text()))
    official={'name','title','provider','organizer','city','venue','place','en','url','source','registration_url','operator_key','slug','iso','event_code','id','key','filename','file_name','file','download','hash','digest','timezone','date_scope','admission_kind','participation','language_mode','evidence_level','evidence_type','source_kind','status_key','operator_identity_status'}
    prose={'age','language','summary','note','status','claim','detail','description','format','gear','proof','entry','action','limit','label','requirements','calendar','source_receipts','official_alternative','grade_level','reward'}
    def walk(value,key=''):
        if isinstance(value,str):
            if RU.search(value) or protected(value):return
            if key in official:names.add(value);return
            if machine_value(value) or 'error' in key or key.endswith(('_id','_hash','_sha256','_filename')):
                codes.add(value);return
            count=len(re.findall(r'[A-Za-z]{2,}',value))
            if (count>=3 and len(value)>=18) or (key in prose and count>=2 and len(value)>=10):pool.add(value)
        elif isinstance(value,list):
            for v in value:walk(v,key)
        elif isinstance(value,dict):
            for k,v in value.items():walk(v,k)
    for p in [ROOT/'data/catalog.json',*(ROOT/'dist/downloads').glob('*.json')]:walk(json.loads(p.read_text()))
    walk(json.loads((ROOT/'dist/assets/data.js').read_text().removeprefix('window.STEM_DATA=').rstrip(';\n')))
    return pool-names-codes

if __name__=='__main__':
    pool=collect_pool()
    target=ROOT/'data/i18n/ru-source-strings.json'
    target.write_text(json.dumps(sorted(pool),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'unique_strings':len(pool),'characters':sum(map(len,pool))}))
