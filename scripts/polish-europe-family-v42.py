"""Readable Russian family copy; leave identifiers and source URLs unchanged."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/catalog.json';d=json.loads(p.read_text())
def clean(s):
    s=re.sub(r'([А-Яа-яЁё])(?=[A-Za-z0-9])',r'\1 ',s)
    s=re.sub(r'([A-Za-z0-9])(?=[А-Яа-яЁё])',r'\1 ',s)
    s=re.sub(r'([A-Za-z])(?=[0-9])',r'\1 ',s)
    return s
def prose(x):
    if isinstance(x,dict):
        for k,v in x.items():
            if k in ['id','iso','url','source','event_ids','school_ids','profile_ids','source_urls','language_mode','instruction_languages','languages','priority']:continue
            if isinstance(v,str) and not v.startswith(('http://','https://')):x[k]=clean(v)
            elif isinstance(v,(dict,list)):prose(v)
    elif isinstance(x,list):
        for v in x:
            if isinstance(v,(dict,list)):prose(v)
prose(d['europe_focus'])
for e in d['events']:
    if e['id'] in ['L'+str(n) for n in range(378,387)]:
        e['priority']=re.sub(r'^P ([0-4])',r'P\1',e['priority']);prose(e)
for s in d['schools']:
    if s['id']=='S041':prose(s)
for h in d['school_history']['results']:
    if h['id'] in ['H132','H133']:h['level']='national_other';prose(h)
e=next(e for e in d['events'] if e['id']=='C907')
url='https://wro.swiss/wp-content/uploads/2026/06/Rangliste-CH-WRO-FINAL-20.06.2026.pdf'
if not any(r['url']==url for r in e['references']):e['references'].append(dict(label='Национальный протокол: возраст, место и вид квоты',url=url))
u=json.loads((ROOT.parent/'stem-family-atlas-work/urls-europe-family-v42.json').read_text());known={s['url'] for s in d['sources']}
for key,url in u.items():
    if key not in ['sgb_primary','jis_home','robbo_faq','pu_courses','pu_planning','pu_home','sido'] and url not in known:
        d['sources'].append(dict(url=url,title='Первичный источник · '+key,evidence='Прочитан организатор / школа; ограничения и сезон указаны в карточках',checked='2026-10-02'));known.add(url)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('European family copy polished; source identifiers retained')
