"""Record the bounded European primary-source pass; retain the global active goal."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT.parent/'stem-family-atlas-work'
PRIMARY=WORK/'camps-primary-v78';BASE='d40d30c58c0a1fa34cd02a443cef2d1eea67bfcf'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldslugs={p['slug'] for p in b['camp_programmes']['profiles']}
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in {v['id'] for v in b['events']}]
assert len(slugs)==13 and len(new)==15
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False,age_verification_submitted=False)
checks=[
 'All2589 prior events and363 stable dossierIDs retained;361 dossiers unchanged,onlyMontanaZug/MadridES details explicitly deepened. Worldwide leagues/schools/routes andAmerica/Asia retained.',
 '13 new programme dossiers,not13 independent operators/rankings;376 dossiers in33 countries and587 unique officialdossierURLs.',
 'Montana PDF filename2026 contains2027 facts andfees;price table visually read. Public blankform permitsonly04–17or04–24July/minimum2weeks;2calendarrows. CHF1000 additionalreturnabledeposit separatefromtuition.',
 'Ecolint bilingualEN/FR policy read directly;Introduction5–7booking/body5–6 linkedtoexistingL296 withoutduplicate. Science7–11,Film9–13 andMultiActivityHalf5–6 separated;MatveyFilm requires9birthday inOct2026.',
 'Ecolint camp-specific16Oct15:00vs genericThursday deadline retained;April2026Frenchcontract governs,credits forillness notordinarycashrefund,foreigninsurance required.',
 'StGeorge13–20Feb2027 exactday8+/1790CHF andboard10+/3490. Matveyboardingonlyafter10birthday;Oscarunder8. LinkedTerms areSummer2023,notWinter2027;English notinferred.',
 'LPB Issy nativepage199/4days/pack549 conflictslinkedcalendarOctober259/5half-days/pack699;December199/4half-days. Calendar visuallyread;4dayposter not proof fifthdaycancelled. JuniorOscar5–6 in2026 markedlater.',
 'SamiadENcamp-life/MultiActivity6+/2027fees3550–4000GBP;6 campus seasonwindows never14night confirmedsessions. CampusoldfeesandTue/WedwindowvsSundayFAQ conflictsretained;Roboticsmenu404 not2027 roboticscourse.',
 'FunTechdayMod7–10/Redstone9–12 andboard8–16 separated;695GBP/yearunknown,ownlaptop/rental70/setup55/extended30+30. BoardAugust2026/modal2020 not2027;noexactdates orEnglishconfirmationinvented.',
 'Madridoperator directlystatesallactivitiesSpanish andforeignchildren. Roboticsdossier updatedES;Manga1ºPrimaria+ andmaterials ownproduct. Date21Jun–30Julvs22Jun–31Jul andFeb/Marchrefresh preventexactsessioncreation.',
 '15 newcalendarrows/familyICS;1924 prior UID/datepairs preserved,104 exhibitioncalendarunchanged. Bridgeidempotent,canonical/publicJSON/SQLite agree;78familyscenarios and0fullyauditedcountries.'
]
qa=WORK/'europe-camps-v78-ui-qa.json'
if qa.exists():checks.extend(json.loads(qa.read_text())['validation'])
def write(stem,obj):
 body=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
 (ROOT/'data'/f'{stem}.json').write_text(body)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
byiso={iso:sum(p['iso']==iso for p in c['profiles']) for iso in ['CHE','FRA','ESP','GBR','TWN','SGP','JPN','KOR','USA','CAN','CRI','MEX','PAN','ECU']}
learning=sum(e['block']=='Лагеря' for e in d['events'])
audit=dict(asof='2026-10-05',version=78,status='progress',scope='Switzerland/France/Spain/UK programme-specific primary pass; every prior worldwide block retained',
 new_dossiers=13,updated_dossiers=['montana-zug','madrid-chess-robotics'],new_calendar_rows=15,new_family_ics=15,
 programme_dossiers=376,countries_with_dossiers=33,official_dossier_urls=587,country_dossier_counts=byiso,
 programme_slugs=slugs,findings=c['gaps'][-4:],
 calendar=dict(events=len(d['events']),learning_records=learning,family_ics=1939,exhibition_ics=104,
  managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
 fully_audited_countries=0,worldwide_complete=False,external_actions=external,
 next_priority='Continue deeperEurope2027contracts andTaiwan/Singapore/Korea/Japan/USA/Canada/LatinAmerica; exactinstructionlanguage/fullquotes/age-grade gates',validation=checks)
write('europe-camp-audit-v78',audit)
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==43 and sum(v.get('status')==200 for v in receipts)==42
evidence=[]
for filename,method in [('montana-price-05.png','Poppler rendering visually read:2/3weeks day/boarding prices and2027date;filename2026 notseasonproof'),
 ('lpb-calendar-render-1.png','Poppler rendering visually read:IssyAM/PM,October5half-days259,December4half-days199,pack699/July2027expiry')]:
 raw=(PRIMARY/filename).read_bytes();evidence.append(dict(evidence_file=filename,local_research_only=True,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),method=method))
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
urls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls);assert len(urls)==29
write('europe-camp-source-receipts-v78',dict(asof='2026-10-05',version=78,
 scope='43 directprimaryfetch attempts:42successful,1Robotics404 retained;2PDFtables visually read;Montana publicform andIssy nativepage read without submission',
 sources=receipts,verified_new_dossier_urls=urls,local_evidence=evidence,
 native_observations=[dict(url='https://www.montana-zug.ch/en/summer-camp',
  method='Blank public form:minimum2weeks,Week1+2(4–17July2027)orWeek1+2+3(4–24July);no personalfieldsfilled/noagreementaccepted'),
  dict(url='https://www.lespetitsbilingues.com/les-centres-les-petits-bilingues/issy-mairie/',
  method='NativeAX:3–10years199EUR/4x3h;pack549/useby30Apr2027;100%English andIssy57bisGallieni. Conflictswithowncalendar retained')],
 external_actions=external,notes=[
 'Private providerHTML/PDF/screenshots remain local; publicdata containfacts/links/hashes/uncertainty,not copiedproviderimages orchildrenphotos.',
 'Programmewindows do not guaranteechosen sessions,places orforeignadmission;unknown2027rates remainunknown. Noautomaticcurrencyconversion.',
 'Englishcamp-life/language-lessons/bilingual policy distinguishedfromcourse-specificEnglishinstruction;websiteEnglish notproof.',
 'Editorialcountry/theme shortlist isnot independently verifiedworldranking;newdossiers maybelongtosameoperator.'
 ]))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=78:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
 evidence='Version77 native save/deploy succeeded:commitd40d30c58c0a1fa34cd02a443cef2d1eea67bfcf;deploymentappgdep_6ac3c8273cdc8191991a5ce40363e37b.16newdossiers/39calendarrows/67familyICS. GoalACTIVE,0fullyauditedcountries.')
plan['latest_validation']=dict(version=78,asof='2026-10-05',status='passed; native save/deploy follows',events=len(d['events']),
 camp_learning_records=learning,programme_dossiers=376,countries_with_dossiers=33,swiss_dossiers=59,french_dossiers=35,spanish_dossiers=28,
 uk_dossiers=5,taiwan_dossiers=21,singapore_dossiers=45,japan_dossiers=14,korea_dossiers=7,official_dossier_urls=587,
 family_ical=1939,exhibition_ical=104,worldwide_complete=False,checks=checks)
plan['europe_camp_programme_audit_v78']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=376,countries=33,swiss=59,
 generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05'
plan['latest_scope_update']='Подробно проверить общие, тематические и технические лагеря/пансионы2026–27 по всем странам. Приоритет:Швейцария/Франция/Испания/Европа,Тайвань/Сингапур/Корея/Япония,США/Канада/Коста-Рика/Мексика/ЛатинскаяАмерика. Читать собственные программы/договоры, разделять EN/ES/RU обучение/языковыеуроки, точный возраст/класс, даты, оборудование, all-in/отмену, доступность и редакционныйотбор. Сохранять соревнования/выставки/школы/маршруты.'
body=json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
(ROOT/'data/research-plan.json').write_text(body);(ROOT/'dist/downloads/STEM_research_plan.json').write_text(body)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=77','?v=78').replace('data-ui-version="77"','data-ui-version="78"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_europe_camp_audit_v78.json" download>Европа: подробная проверка программ ↓</a> · <a href="downloads/STEM_europe_camp_source_receipts_v78.json" download>Источники проверки Европы ↓</a> · '
anchor='<a href="downloads/STEM_americas_camp_audit_v77.json"'
if link not in s:
 assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=376,new_dossiers=13,new_calendar_rows=15,new_family_ics=15,goal='active')))
