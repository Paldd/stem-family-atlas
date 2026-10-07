"""Record this bounded primary-source pass; the worldwide goal remains active."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'stem-family-atlas-work'
PRIMARY=WORK/'camps-primary-v77'
BASE='1207b5344138cd2d7a7d950aa5c8353f75bbece2'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in {v['slug'] for v in b['camp_programmes']['profiles']}]
new=[e for e in d['events'] if e['id'] not in {v['id'] for v in b['events']}]
assert len(slugs)==16 and len(new)==39
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False,age_verification_submitted=False)
checks=[
 'All2550 prior events,347 dossiers/stableIDs and1857 prior familyICS UID/datepairs preserved;104 exhibitionICS unchanged; all worldwide leagues/schools/routes blocks retained',
 '16 new programme dossiers,not16 independent operators/rankings;363 dossiers in33 countries,558 unique officialdossierURLs; Ecuador newly represented',
 'Olympia2027 regular andSPARK6–9 separated; Matvey only before10 forSPARK; WinaukeeRookie7+/Grade1–4/firstseason; expired30Sep/1Oct discounts excluded',
 'Eagle regular1–7week prices used; availability30Sep is a snapshot;120/125 cancellation discrepancy explicitly visible',
 'Cedar new2027 sessions but no2027 price;6–15vs7–16 age conflict;2026 payments/buses not2027; English camp-life supported separately from lessons',
 'Cuddles broadwinter22Dec–2Jan is a season window,not exactcampdays; currency unknown,2day discount20vs21 conflict; afterschoolFAQ not silently wintercontract',
 'Integem nativeexpandedFAQ directly confirms English, age/grade bands,1/2/3week robotics syllabus and kits remainoperatorproperty; no2027 fees/dates or youngerNVIDIAcertificates invented',
 'WildRoots four consistent5day periods imported; firstspring22–28Marvs5days excluded; age/currency/language unknown and swimming prerequisite retained',
 'UCR2025 andUTP2026 remain archive; one6yearold anecdote notagepolicy; UCR linked toL120 without duplicateevents; Galileo2027 weekday conflict creates noexactsession',
 'Cube Grade1/4–5 courses are8 separateSaturdaylessons/term;13Feb/22May excluded; CanadaCAD275+HST and Sept2026gradegate; conflicting Grade2/3/6 andbundleprices retained as gaps',
 'Holland diagnosis/agepolicy conflict stays a gap; nofamilyhealth/eligibility inferred; no forms/messages/subscriptions/payments',
 '39 newcalendarrows,67 newfamilyICS entries(35camp sessions+32individual lessons); bridgeidempotent; canonical/publicJSON/SQLite valid;72scenarios and0 fullyaudited countries'
]
qa=WORK/'americas-camps-v77-ui-qa.json'
if qa.exists():checks.extend(json.loads(qa.read_text())['validation'])
def write(stem,obj):
 body=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
 (ROOT/'data'/f'{stem}.json').write_text(body)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
byiso={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','PAN','ECU']}
audit=dict(asof='2026-10-05',version=77,status='progress',
 scope='USA/Canada/CostaRica/Mexico/Panama/Ecuador primaryprogramme pass; all Europe/Asia and worldwide blocks retained',
 new_dossiers=16,updated_dossiers=[],new_calendar_rows=39,new_family_ics=67,
 programme_dossiers=363,countries_with_dossiers=33,official_dossier_urls=558,country_dossier_counts=byiso,
 programme_slugs=slugs,findings=c['gaps'][-4:],
 calendar=dict(events=2589,learning_records=1258,family_ics=1924,exhibition_ics=104,managed_dated_rows=795,reused_legacy_events=65,season_windows=19),
 fully_audited_countries=0,worldwide_complete=False,external_actions=external,
 next_priority='Further Europe/Swiss/France/Spain and Asia/LatinAmerica primary2027 contracts, true instruction languages, full quotes and age/grade admission',validation=checks)
write('americas-camp-audit-v77',audit)
receipts=[v for path in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(path.read_text())]
assert len(receipts)==29 and sum(v.get('status')==200 for v in receipts)==28
evidence=[]
for filename,method in [('cuddles-pricing.png','Native rendered winter table visually read;currency absent,regular/early tiers and erroneous2day savings'),
 ('integem-faq-native.txt','Native browser expandedFAQ answers read: English,6+minimum,K–2/Grades3–5 robotics levels,kits/cancellation')]:
 raw=(PRIMARY/filename).read_bytes();evidence.append(dict(evidence_file=filename,local_research_only=True,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),method=method))
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
urls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls);assert len(urls)==26
write('americas-camp-source-receipts-v77',dict(asof='2026-10-05',version=77,
 scope='29 directprimaryfetch attempts(28successful,1errorretained),3 Olympiaofficialpages viawebreader,2nativevisual/expandedreads',
 sources=receipts,verified_new_dossier_urls=urls,local_evidence=evidence,
 webreader_primary_reads=[dict(url=u,method='Official page opened and read via webreader; rawHTTP403 not reclassified') for u in [
 'https://www.campolympia.com/summer-camps/dates-pricing-2027/',
 'https://www.campolympia.com/summer-camps/',
 'https://www.campolympia.com/summer-camps/programs/spark-week/']],
 external_actions=external,notes=[
 'Private researchHTML/screenshots remain local; publicdownloads contain facts,links,hashes,uncertainty and receipts,not providerimages/childrenphotos.',
 'English/Spanish page text and operator testimonials do not establish instructionlanguage or independentworldranking.',
 'Dollar sign withoutISO code stays unknown or explicitly geographicallyinferred; no currency conversion invented.',
 'No registrations,accounts,birthdate/medicalintake,organizer messages,bookings,subscriptions orpayments.'
 ]))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=77:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
 evidence='Version76 native save/deploy succeeded: commit1207b5344138cd2d7a7d950aa5c8353f75bbece2; deploymentappgdep_6ac3bfa4fc84819193521951d783d3d1. Added25 dossiers,67 calendarrows,52familyICS. GoalACTIVE,0fullyauditedcountries.')
plan['latest_validation']=dict(version=77,asof='2026-10-05',status='passed; native save/deploy follows',events=2589,
 camp_learning_records=1258,programme_dossiers=363,countries_with_dossiers=33,swiss_dossiers=53,french_dossiers=33,spanish_dossiers=27,
 taiwan_dossiers=21,singapore_dossiers=45,japan_dossiers=14,korea_dossiers=7,official_dossier_urls=558,
 family_ical=1924,exhibition_ical=104,worldwide_complete=False,checks=checks)
plan['americas_camp_programme_audit_v77']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=363,countries=33,swiss=53,generated_calendar_entries=795,reused_legacy_events=65)
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05'
body=json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
(ROOT/'data/research-plan.json').write_text(body);(ROOT/'dist/downloads/STEM_research_plan.json').write_text(body)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=76','?v=77').replace('data-ui-version="76"','data-ui-version="77"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v77.json" download>Америка: программы и договоры ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v77.json" download>Источники проверки Америки ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v76.json"'
if link not in s:
 assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=363,new_dossiers=16,new_calendar_rows=39,new_family_ics=67,goal='active')))
