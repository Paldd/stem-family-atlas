"""Keep the worldwide research scope active and publish the Asia evidence inventory."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'stem-family-atlas-work'
PRIMARY=WORK/'camps-primary-v76'
BASE='4916e69c616e19d5c70d550723c73ba8374de1c6'
old=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
old_slugs={p['slug'] for p in old['camp_programmes']['profiles']}
new_slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in old_slugs]
new=[e for e in d['events'] if e['id'] not in {v['id'] for v in old['events']}]
assert len(new_slugs)==25 and len(new)==67

def write(name,obj):
    body=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{name}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+name.replace('-','_')+'.json')).write_text(body)

checks=[
 'All 322 prior dossiers and stable IDs unchanged; all 2482 other prior events unchanged; L143 receives directly published grade, address and early-tariff condition without changing dates',
 '25 new programme dossiers across Taiwan/Singapore/Japan/Korea; counts are programmes, not 25 operators or independent rankings',
 'Empire new primary page directly states English-medium, ten age-banded courses and five Mon-Fri weeks; own JSON-LD confirms SGD; 12.5h single course versus two-course full day and device rental kept separate',
 'October Post-PSLE is a separate three-day product; 4 October early-bird expired; non-PSLE foreign admission and English instruction unknown; regular fees used',
 'The Lab two AI projects have non-member prices and concrete Nov/Dec2026 dates; 4h versus 9h; English/currency/GST unknown; disputed Jurong excluded from exact calendar',
 'Grove L143 reused once; primary elementary grade and submission-based early price updated; no payment/deposit required for early tariff; Wenzao drama all-English versus separate language lessons',
 'Brown Grade1-3 upper gate and bilingual showcase versus unconfirmed instruction; iROBO Grade3-9, three date/campus variants, supplied laptop, conflicting iOS device advice',
 'ASIJ/Aoba summer2026 and KRW museum2026 prices remain archival without new2027 events; Japanese-grade rule/foreign fees/Meguro conflict and elementary museum grade gates visible',
 'Aoba own PDF2026 text read and price table visually inspected; 120000+11000 first-time external fee, optional food/bus/after-school kept separate; no2024 robotics transferred',
 'Seoul Science Institute local EducationOffice Grade4-6/Middle1 restriction prevents treating it as an open international younger camp',
 '67 new calendar rows; 52 new family ICS entries, 15 both-later teen course rows excluded; all1805 prior UID/date pairs and104 exhibition ICS preserved',
 'Canonical/public JSON, SQLite integrity/foreignkeys, bridge idempotence; 67 family scenarios,32 dossier countries,0 fully audited; worldwide goal ACTIVE'
]
qa=WORK/'asia-camps-v76-ui-qa.json'
if qa.exists():checks.extend(json.loads(qa.read_text())['validation'])
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,
 subscriptions_created=False,age_verification_submitted=False)
audit=dict(asof='2026-10-05',version=76,status='progress',
 scope='Detailed Taiwan/Singapore/Japan/Korea programme pass; Europe, North America, CostaRica/Mexico/LATAM and all worldwide blocks retained',
 new_dossiers=25,updated_dossiers=[],corrected_legacy_event_ids=['L143'],new_calendar_rows=67,new_family_ics=52,
 programme_dossiers=347,countries_with_dossiers=32,swiss_dossiers=53,french_dossiers=33,spanish_dossiers=27,
 taiwan_dossiers=21,singapore_dossiers=45,japan_dossiers=14,korea_dossiers=7,official_dossier_urls=532,
 programme_slugs=new_slugs,findings=c['gaps'][-5:],
 calendar=dict(events=2550,learning_records=1219,family_ics=1857,exhibition_ics=104,
 managed_dated_rows=756,reused_legacy_events=65,season_windows=18),
 fully_audited_countries=0,worldwide_complete=False,external_actions=external,
 next_priority='Other Europe / USA / Canada / CostaRica / Mexico / LATAM; dated2027 contracts, exact locations, actual EN/ES/RU instruction and complete family quotes',validation=checks)
write('asia-camp-audit-v76',audit)
receipts=[]
for path in sorted(PRIMARY.glob('receipt-*.json')):receipts+=json.loads(path.read_text())
raw=(PRIMARY/'aoba-fees.png').read_bytes()
visual=dict(evidence_file='aoba-fees.png',local_research_only=True,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
 method='Own EnglishPDF2026 page3 rendered and visually read: external tuition/registration/lunch/bus/after-school and nonrefundable clause')
old_urls={s['url'] for p in old['camp_programmes']['profiles'] for s in p['sources']}
new_urls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-old_urls)
assert len(new_urls)==16
write('asia-camp-source-receipts-v76',dict(asof='2026-10-05',version=76,
 scope='Direct primary HTML/PDF reads and native rendered new Empire page; errors retained without inventing successful reads',
 sources=receipts,verified_new_dossier_urls=new_urls,visual_evidence=[visual],
 native_rendered_reads=[dict(url='https://empirecode.co/december-holiday-camps-singapore/',method='Native browser public page observed: current2026/27 five weeks, age bands, English-medium and pricing visible',no_registration=True)],
 external_actions=external,notes=[
 'Empire new page ownJSON-LD saysSGD430/500, and programme table gives five distinct weeks. Broad structured-data23Nov–8Jan was not converted into one continuous session.',
 'Empire oldyear-end page retained as separate contradictory2025 product; testimonials do not prove programme language or international results.',
 'Labterms ownlink returned404; refund/currency/English were left unknown. RawHTTP succeeded for museum/institute pages after webtool failures; primary content actually read.',
 'Aoba original EN/JP PDFs downloaded; ENpage3 fee table visually inspected. Operators brochure images and children data are not included in public downloads.',
 'No form filling, GoogleForms submission, accounts, messages, bookings, subscriptions or payments.'
 ]))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=76:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
 evidence='Version75 native save/deploy succeeded: commit4916e69c616e19d5c70d550723c73ba8374de1c6; deploymentappgdep_6ac3b5afa8508191961a4b0fca870871. Added8 dossiers,32 new calendarrows and one newly dated L222,33 familyICS. Goal ACTIVE,0 fullyaudited countries.')
plan['latest_validation']=dict(version=76,asof='2026-10-05',status='passed; native save/deploy follows',events=2550,
 camp_learning_records=1219,programme_dossiers=347,countries_with_dossiers=32,swiss_dossiers=53,
 french_dossiers=33,spanish_dossiers=27,taiwan_dossiers=21,singapore_dossiers=45,japan_dossiers=14,korea_dossiers=7,
 official_dossier_urls=532,family_ical=1857,exhibition_ical=104,worldwide_complete=False,checks=checks)
plan['asian_camp_programme_audit_v76']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=347,countries=32,swiss=53,
 generated_calendar_entries=756,reused_legacy_events=65)
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05'
body=json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
(ROOT/'data/research-plan.json').write_text(body);(ROOT/'dist/downloads/STEM_research_plan.json').write_text(body)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=75','?v=76').replace('data-ui-version="75"','data-ui-version="76"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_asia_camp_audit_v76.json" download>Азия: программы, классы и цены ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v76.json" download>Источники проверки Азии ↓</a> · '
anchor='<a href="downloads/STEM_europe_camp_audit_v75.json"'
if link not in s:
 assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=347,new_dossiers=25,new_calendar_rows=67,new_family_ics=52,goal='active')))
