"""Bounded Asian programme audit, with primary snapshots retained outside publishing."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v89'
BASE='96223ed18e24d8cbbd13a321f23b9918a22f6b0e'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
op={q['slug']:q for q in b['camp_programmes']['profiles']};old={e['id']:e for e in b['events']}
fresh=[q for q in c['profiles'] if q['slug'] not in op]
deepened=[q['slug'] for q in c['profiles'] if q['slug'] in op and q!=op[q['slug']]]
new=[e for e in d['events'] if e['id'] not in old]
assert len(fresh)==28 and len(new)==40 and deepened==['typa']
assert all(e==old[e['id']] for e in d['events'] if e['id'] in old)
assert c['counts']['dossiers']==575 and c['counts']['source_urls']==862
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==42 and sum(v.get('status')==200 for v in receipts)==40
boundaries={
 'arc-holiday':'Own autism-friendly holiday page permits Non-Pathlight participants aged7–18. Special external admission/support not fully resolved; discovery gap, no new programme dossier.',
 'korea-steam':'Own Ewha winter2027 notice: Korean heritage/language objective, Grades2–6 and minimum40. Not admitted as open English non-heritage camp.',
 'ntue-housing':'Own housing page distinguishes a separate short-course dorm arrangement from children’s camp with no housing. No family dorm promised.',
 'evergreen-info':'General camp information alongside individual programme and contract evidence; no independent operator count.',
 'irobo-camp':'Programme index read separately from five full winter2027 course pages; no duplicated index dossier.'
}
for v in receipts:
 if v.get('status')==200:
  f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
  assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
  v.update(raw_filename=f.name,body_snapshot_retained=True,content_scope=boundaries.get(v['key'],
    'Own primary body retained. Relevant curriculum, dates, ages, language evidence, fees and conditions read; dossier and audit preserve unresolved boundaries.'))
  if '-sample' in v['key']:v['content_scope']='Linked summer2026 sample timetable read; archive/sample evidence only, not an announced2027 cohort.'
images=json.loads((PRIMARY/'image-receipts.json').read_text());assert len(images)==5
for v in images:
 f=PRIMARY/(v['key']+'.png');assert v['status']==200 and hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
 v.update(raw_filename=f.name,read_scope='Original English guide page visually read; English document does not establish English teaching or support.')
visual=[]
for name,key,page,scope in [
 ('evergreen-winter-p1.png','evergreen-winter-pack',1,'Winter2026–27 two date pairs; ski all levels and snowboard enquire.'),
 ('evergreen-winter-p9.png','evergreen-winter-pack',9,'Own-phone calls only on days1/3 at17:30–18; staff phones not lent.'),
 ('evergreen-expedition-p1.png','evergreen-expedition-sample',1,'Sample2026: JA Adventure within preceding3 years; join on day5 and independent arrival at Omachi station. Not shifted to2027.'),
 ('typa-tech-p76.png','typa-magazine',78,'Printed page76: separate rising-grade curriculum, hours, lunch and NT$25000/week; not identical robotics for all.'),
 ('typa-tech-p77.png','typa-magazine',79,'Printed page77: actual Summer2026 week2 is15–18June, four days. Magazine title2026–27 does not announce Summer2027.')]:
 bb=(PRIMARY/name).read_bytes();r=next(q for q in receipts if q['key']==key)
 visual.append(dict(url=r['url'],pdf_page=page,read_scope=scope,render_sha256=hashlib.sha256(bb).hexdigest(),render_bytes=len(bb)))
oldurls={s['url'] for q in op.values() for s in q['sources']}
added=sorted({s['url'] for q in c['profiles'] for s in q['sources']}-oldurls);assert len(added)==33
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False)
learning=sum(e['block']=='Лагеря' for e in d['events'])
isos=['CHE','FRA','ESP','KEN','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','USA','CAN','CRI','MEX','BRA']
byiso={s:sum(q['iso']==s for q in c['profiles']) for s in isos}
checks=[
 '28 new programme/age/format dossiers across8 operator groups; existing TYPA deepened as a ninth group. All547 prior IDs/order retained and546 complete prior dossiers unchanged. All2997 previous events unchanged, including legacy TYPA; no calendar duplication from its curriculum themes.',
 'Evergreen White Horse:8–15,14–18Dec2026 or2–6Jan2027,5days/4nights, primary English confirmed. Base175000JPY; elementary lift24400, standard rental11220, jacket+pants6550, helmet4730 =>221900 before Tokyo/flight/insurance. Own equipment allowed; independent limited1800 season pass not guaranteed. Oscar below8; Matvey conditional. Calls only days1/3, staff supervision/medication and cancellation14-day boundary retained.',
 'Evergreen9 summer age/boarding/day variants belong to one operator. Ninja7–8; Mountain/Water/Earth9–12; Leadership13–17 versus13–16 conflict; Expedition returner prerequisite within3 years/sample day5 Omachi arrival. Prices175000/185000/259000/444000 and day87500 are2026; no fabricated2027 sessions. Day first/last days shorter than middle days. General outdoor/science programmes not promoted to robotics.',
 'GSA Tachikawa:100percent English, kindergarten3–6 versus elementary actual Grades1–6; science/art/phonics/sport, no robotics invented. Five July/August term pairs lack a year; repeated weekdays are not evidence of2026/2027. No dated calendar rows; undated55000/66000JPY and literal88:000 full-day typo/cancellation June30 retained.',
 'SOR four short tracks SPIKE Essential5+, Prime7+, Tinkercad8+, VEXGO5+. Four study hours plus lunch,200/180SGD beforeGST; credits/cancellation and extra-care fees read. Heading September8–11 versus FAQDecemberXX prevents exact current cohort. Teaching English unconfirmed; internal Bot League not established as official RECF/VEX Worlds.',
 'Computhink four older tracks: typed Roblox Lua11–16, PythonMinecraft11–16, AI App12–16 with prior coding, G3 actual Sec2–4 gates. Each467SGD/3days/9hours/max8 with provided laptop/platform;15 actual2026 slots. Both children later; all15 absent from familyICS. English website does not establish English instruction; no international medal claim.',
 'iROBO five additional winter2027 course pages independently read: mechanics/BOOST/SPIKE/Python, actual kindergarten/grade gates,20 campus/date variants including weekends,4700–7600NTD with lunch.09–16 instruction and08:30–17:30 supervision differ. Two/three-day same-theme alternatives not levels; supplied equipment versus own BOOST tablet and SPIKE Apple/iOS conflict retained. English/foreign admission unconfirmed; actual grades not inferred from birth years.',
 'NTUE overseas6–15 beginner Mandarin accepted,28Dec2026–8Jan2027 window with9 teaching days and Jan1 off. Five original English guide images plus FAQ read.36000TWD/1245USD or34000/1185 early by31Oct2026; no housing, materials/lunch/activity insurance included. English secondary support unconfirmed: ZH language lessons, not EN filter. Guide refund first half versus FAQfirst third/max15 versus FAQ8–12 discrepancies explicit.',
 'Inter-K winter14+ future, English/Korean lessons selectable,2500USD,10nights/11date span versus10day heading; weekday meals versus generic3/day and independent minor outings with consent preserved. WOLKO future English Christian Gospel/discipleship programme, Jan11–16Upcoming with age/fee/venueTBA; religious nature explicit. Ewha heritage STEAM and old Jeju school handbooks do not prove open English6–10 camps.',
 '3037 events/1706 camp-learning rows;575 dossiers/36 countries/862 dossier URLs;124 family comparisons.40 new dated catalogue rows;23 new familyICS entries = Evergreen2+iROBO20+NTUE1, with unresolved gates visible.2279 familyICS/104 exhibitionICS. Existing calendar content stable apart from DTSTAMP; publicJSON/SQLite/bridge idempotence and language filter independently checked.',
 '42 direct HTML/PDF attempts:40 HTTP200 and2 failures, including Rotary TLS mismatch and SOR terms404. Nine downloaded PDFs and five original NTUE PNGs retained;five additional PDF visual reads. Primary-page receipt is not whole-operator/country audit. All worldwide general/technical2026–27 regions, schools/results/leagues/exhibitions/routes remain active;0 fully audited countries. No external forms/messages/payments/accounts/subscriptions/automations.'
]
audit=dict(asof='2026-10-05',version=89,status='progress',
 scope='Japan real winter and archived summer English formats; Singapore curriculum/cohort conflicts; Taiwan winter2027 grade/language/contract gates; Korea future-age/heritage/religious boundaries. Worldwide work active.',
 new_dossiers=len(fresh),new_operator_groups=8,operator_groups_including_existing_deepening=9,new_calendar_rows=len(new),new_family_ics=23,updated_dossiers=deepened,corrected_existing_event_ids=[],
 programme_dossiers=len(c['profiles']),countries_with_dossiers=c['counts']['countries'],official_dossier_urls=c['counts']['source_urls'],country_dossier_counts=byiso,programme_slugs=[q['slug'] for q in fresh],findings=c['gaps'][-4:],
 calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2279,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
 fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
 next_priority='Continue USA/Canada/CostaRica/Mexico/LatinAmerica and all authorised Europe/Asia/worldwide general/technical seasonal programmes2026–27; real grades/DOB, EN/ES/RU and secondary support, foreign admission, all-in costs, places and contracts. Existing leagues, schools/history, exhibitions and family routes remain active.')
def write(stem,v):
 text=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(text)
 (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('asia-camp-audit-v89',audit)
write('asia-camp-source-receipts-v89',dict(asof='2026-10-05',version=89,
 scope='42 direct HTML/PDF attempts,40 HTTP200/2 failures;9 downloaded PDFs. Five original guide PNGs visually read and five additional PDF-page visual reads. Relevant full programme/contract bodies, not42 completed operator audits.',
 sources=receipts,image_primary_reads=images,visual_pdf_reads=visual,dossier_source_urls_added=added,external_actions=external,
 notes=['Raw HTML/PDF/images/renders retained outside public checkout. Public export contains paraphrased facts, source links, hashes and errors, without full source documents/photos.',
        'English document/site language is separate from confirmed primary teaching, bilingual teaching, secondary support, language lessons or camp life.',
        'Announced dates/fees do not establish a place, admission, final invoice or world ranking. Sample/archived summer years not shifted. Worldwide goal active.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=89:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='Version88 native publication succeeded:commit96223ed18e24d8cbbd13a321f23b9918a22f6b0e;deployment appgdep_6ac4160bf9bc8191b664e90bb530db4d.18 new dossiers/22 dated rows/7 familyICS. Worldwide goal active.')
plan['latest_validation']=dict(version=89,asof='2026-10-05',status='Independent source/preservation/calendar verification; native publication receipt separate',events=len(d['events']),camp_learning_records=learning,programme_dossiers=len(c['profiles']),countries_with_dossiers=c['counts']['countries'],official_dossier_urls=c['counts']['source_urls'],family_ical=2279,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['asia_camp_programme_audit_v89']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=len(c['profiles']),countries=c['counts']['countries'],swiss=c['counts']['swiss'],generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
 if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
  req['evidence']='v89:575 programme/venue/format dossiers in36 countries;28 new+TYPA deepened,40 new dated catalogue rows/23 familyICS,862 dossier URLs. Own Japan winter/summer sample/English/all-in fees, Singapore short-course curricula, Taiwan grade/language/2027 variants and Korea older/religious/heritage gates verified with unresolved conflicts retained. Worldwide2026–27/all priority regions active;0 fully audited countries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=88','?v=89').replace('data-ui-version="88"','data-ui-version="89"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_asia_camp_audit_v89.json" download>Япония / Тайвань / Сингапур / Корея: новая проверка ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v89.json" download>Источники и границы проверки ↓</a> · '
anchor='<a href="downloads/STEM_europe_camp_audit_v88.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=575,new_dossiers=28,deepened_dossiers=1,new_calendar_rows=40,new_family_ics=23,source_urls=862,goal='active')))
