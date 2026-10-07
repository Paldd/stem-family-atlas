"""Publish the evidence inventory and active research scope for the Europe pass."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'stem-family-atlas-work'
PRIMARY=WORK/'camps-primary-v75'
BASE='d7461e46b45468fec5bb26f3558bcfece2e87fa5'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text())
c=d['camp_programmes']
new_slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in {p['slug'] for p in old['camp_programmes']['profiles']}]
assert len(new_slugs)==8

def write(name,obj):
    body=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{name}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+name.replace('-','_')+'.json')).write_text(body)

checks=[
    '2450 prior events unchanged; L222 retains ID and receives directly stated July12–16/2027 date, source and packed-lunch details',
    'All314 prior dossier IDs preserved; only Aiglon/Rosenberg/CDL updated;311 other dossiers unchanged',
    'Aiglon2027 original brochure price/age tables visually read; six boarding packages and five day weeks; day7+ versus main8+ Robotics conflict visible',
    'Rosenberg general age6–18 never transferred to unknown FocusCourse minima; no age-verification submission',
    'CDL three2027 sessions coexist with explicit2026 prices; VEX AIM12+, startup10+, registration beginsNovember',
    'Helvetic own Zug detail resolves week2 to12–16July; six existing equivalent weeks reused; no assumed English instruction',
    'Babel autumn/winter/spring full/morning packages; inconsistent summer2026/27 excluded; meal inclusion unknown',
    'LittleBritish primary grade gate and Zoo3–6 maximum preserved; five campuses are variants of two courses, not ten operators',
    'Navatormes linkedPDF2026 read and table visually inspected; EUR618 is historical; tipis6–8 versus landingalbergue explicit; no2027 calendar row',
    '32 new dated catalogue rows plus one formerly undated L222;33 additional familyICS dates; all1772 prior UID/datepairs preserved',
    'Worldwide leagues/schools/results/routes unchanged;104 exhibitionICS unchanged exceptDTSTAMP; SQLite integrity/foreignkeys and bridge idempotence',
    'Canonical/publicJSON mirrors,63 scenarios,32 dossier countries,0 fullyaudited countries; worldwide goal remainsACTIVE',
    'Native browserQA: scenario59 three correct picks; Aiglon filter3 and comparison2/4; comparisonclear0; Aiglon+confirmedEN0; Babel+confirmedEN1; WebMCP L22212–16July; consoleerrors0; local comparison screenshot saved'
]
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,
    subscriptions_created=False,age_verification_submitted=False)
audit=dict(asof='2026-10-05',version=75,status='progress',
    scope='Switzerland / France / Spain detailed programme documents; all worldwide blocks and priority countries retained',
    new_dossiers=8,updated_dossiers=['aiglon','rosenberg','cdl'],corrected_legacy_event_ids=['L222'],
    new_calendar_rows=32,newly_dated_legacy_rows=1,new_family_ics=33,
    programme_dossiers=322,countries_with_dossiers=32,swiss_dossiers=53,french_dossiers=33,spanish_dossiers=27,
    official_dossier_urls=516,programme_slugs=new_slugs,findings=c['gaps'][-5:],
    calendar=dict(events=2483,learning_records=1152,family_ics=1805,exhibition_ics=104,
        managed_dated_rows=689,reused_legacy_events=64,season_windows=18),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,
    next_priority='Other Europe / Asia / North America / LATAM priority gaps,2027 contracts, exact venues and complete family budgets; current goal staysACTIVE',validation=checks)
write('europe-camp-audit-v75',audit)

# Preserve downloaded page assets locally; public site publishes facts and links,
# not the operator's brochure images or the browser's inventory/telemetry.
assetroot=Path('/var/folders/3z/n5ms27vx2z9cyvpw_wxxmy000000gn/T/browser-use/assets')
assets=[('94f343bf-d64e-4078-b940-7a00b63ec63f','740f2c1635d89a65','aiglon-vex-page4'),
    ('94f343bf-d64e-4078-b940-7a00b63ec63f','4f62919602d78605','aiglon-board-page7'),
    ('3723b262-8c85-4531-963c-5f906790a48a','5e6ea3e296d6bb63','aiglon-day-page8')]
visual=[]
for folder,aid,name in assets:
    dest=PRIMARY/(name+'.webp')
    if not dest.exists():shutil.copy2(assetroot/folder/(aid+'.webp'),dest)
    raw=dest.read_bytes()
    visual.append(dict(evidence_file=dest.name,local_research_only=True,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
receipts=[]
for path in sorted(PRIMARY.glob('receipt-*.json')):receipts+=json.loads(path.read_text())
recover=[]
for name,url in [('helvetic-robotics-native','https://www.helveticinstitute.ch/robotics-ai-and-coding/'),
        ('helvetic-zug-native','https://www.helveticinstitute.ch/summer-robotics-camp-zug/')]:
    raw=(PRIMARY/(name+'.txt')).read_bytes()
    recover.append(dict(url=url,method='native browser rendered primary page read',
        evidence_file=name+'.txt',local_research_only=True,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
        http_status_not_inferred=True))
recover.append(dict(url='https://www.aiglon.ch/summer-camp-brochure',
    final_url='https://online.fliphtml5.com/meksu/fdzd/',method='own brochure link; rendered pages4/7/8 read and pageAssets bundled',visual_evidence=visual))
old_urls={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
new_urls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-old_urls)
assert len(new_urls)==9
write('europe-camp-source-receipts-v75',dict(asof='2026-10-05',version=75,
    scope='Primary HTML/PDF and actual rendered brochure pages; failures retained separately from recovered reads',
    sources=receipts,recovered_reads=recover,verified_new_dossier_urls=new_urls,
    external_actions=external,notes=[
        'Helvetic directHTTP403 and webtimeout did not become fictitiousHTTP200; actual native primary pages subsequently loaded/read.',
        'FlipHTML full-publication download did not produce an accessiblePDF; facts came from visible original page assets read at original resolution.',
        'Navatormes own linkedPDF is titled2026 despite2027 landing; tablepage4 visually inspected; originalPDF SHA256 in receipts.',
        'No browser inventories, tracking URLs, secrets, family forms or downloaded brochure images included in public files.'
    ]))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=75:
    plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version74 native save/deploy succeeded: commit d7461e46b45468fec5bb26f3558bcfece2e87fa5; deployment appgdep_6ac3adaddb308191bd82bcdbb63419f4. Added14 dossiers,4 datedrecords/ICS. Goal ACTIVE,0 fullyaudited countries.')
plan['latest_validation']=dict(version=75,asof='2026-10-05',status='passed; native save/deploy follows',
    events=2483,camp_learning_records=1152,programme_dossiers=322,countries_with_dossiers=32,
    swiss_dossiers=53,french_dossiers=33,spanish_dossiers=27,official_dossier_urls=516,
    family_ical=1805,exhibition_ical=104,worldwide_complete=False,checks=checks)
plan['swiss_france_spain_camp_programme_audit_v75']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=322,countries=32,
    swiss=53,generated_calendar_entries=689,reused_legacy_events=64)
plan['status']=plan['native_goal_status']='active'
plan['updated']='2026-10-05'
body=json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
(ROOT/'data/research-plan.json').write_text(body)
(ROOT/'dist/downloads/STEM_research_plan.json').write_text(body)
path=ROOT/'dist/index.html'
html=path.read_text().replace('?v=74','?v=75').replace('data-ui-version="74"','data-ui-version="75"')
path.write_text(html)
path=ROOT/'dist/assets/camp-programmes.js'
js=path.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v75.json" download>Швейцария / Франция / Испания: новые программы ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v75.json" download>Документы и источники новой проверки ↓</a> · '
anchor='<a href="downloads/STEM_latam_camp_audit_v74.json"'
if link not in js:
    assert anchor in js
    js=js.replace(anchor,link+anchor,1)
path.write_text(js)
print(json.dumps(dict(dossiers=322,new_dossiers=8,new_calendar_rows=32,newly_dated_legacy_rows=1,new_family_ics=33,goal='active')))
