"""Retain primary receipts and report bounded Asian progress against published v82."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v83'
BASE='94063c00ad38953ac234e75f35ddb0d17654c176'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldslugs={p['slug'] for p in b['camp_programmes']['profiles']};oldids={e['id'] for e in b['events']}
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in oldids]
assert len(slugs)==16 and len(new)==17 and len(c['profiles'])==448
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==31 and sum(v.get('status')==200 for v in receipts)==22
for v in receipts:
    if v.get('status')==200:
        f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v.update(body_snapshot_retained=True,raw_filename=f.name)
images=json.loads((PRIMARY/'ntue-guide-receipt.json').read_text())
for v in images:assert hashlib.sha256((PRIMARY/v['file']).read_bytes()).hexdigest()==v['sha256']
web=[]
for file,url,note in [
    ('see-home-web.txt','https://seecamp.com.tw/','Own web reader: homepage. Direct HTTP403 retained.'),
    ('see-japan-web.txt','https://seecamp.com.tw/product/2027see-winter-discover-japan-2d/','Own web reader: complete programme/grade/price/locations. Direct HTTP403 retained.'),
    ('see-products-web.txt','https://seecamp.com.tw/product/2027see-winter-world-games-5d/','Own web reader: complete World Games. Same response retains Palau cache miss; no Palau programme added.'),
    ('srt-stage-web.txt','https://www.srt.com.sg/stagecamp','Own web reader independently agrees with retained direct200 source; week/age/language-specific availability.')]:
    bb=(PRIMARY/file).read_bytes();web.append(dict(url=url,method=note,snapshot_sha256=hashlib.sha256(bb).hexdigest(),snapshot_bytes=len(bb)))
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==22 and c['counts']['source_urls']==703
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False)
checks=[
    'All 2780 previous events and 432 programme dossiers retain their IDs and content. 16 new programme/season/age dossiers cover 7 operators, including an existing Taiwan operator and an Embassy network already in the legacy calendar; not 16 independent camps.',
    'U-GAKU 7 specific winter/spring boarding packages. School-grade eligibility retained, foreign/English-only family admission unknown. Winter Nasu/Chatan and spring Fukushima/Onna are separate venues; Wakayama uses /kansai/, while /wakayama/ is an HTTP200 empty listing.',
    'U-GAKU base139800/159800/199800 +30000 first contract fee, repeats waived. Short camps do not meet 4+week refund-guarantee condition. Cancellation thresholds overlap, not simplified to free cancellation. Spring/news TBA/NasuTochigi conflicts with current campus fee/Fukushima preserved.',
    'Myoko own2026 brochure visually read: 6–15, advanced–native English,130000/5days4nights,Tokyo rail+20000. Four2026 sessions are historical; no invented2027 dates or copied future price. Accommodation Buna House in sample itinerary, future contract/room/night-care unknown.',
    'SEE DiscoverJapan2days and WorldGames5days are in Taiwan, senior kindergarten–Grade4, two parallel Taipei/Xindian campuses, fullEnglish confirmed. Grade5+ enquiry and foreign-grade equivalence retained. Regular/individual/3+/6+ early fees separated; two children do not receive automatic group3+ discount.',
    'SRT LittleElf specific programme14–16Dec differs from annual KidsSpace poster14–18Dec: use3days, optional1–3attendance, English4–7/max12/lunch, member prices separate. Yearlyposter alone not multiplied into fullyverified calendar programmes.',
    'SRT Stage: November Mandarin,7–11Dec English. Younger4–7 sold out, excluded from family ICS; older8–12 limited according to source, real seat not confirmed.400+6booking and expired4Oct early bird retained, no fake English-November sessions.',
    'VOCA two3day dates,6–12,450+50registration,10% tuition-only early total455 and no stacking/no refunds. Whole-course English unknown: not placed in confirmed EN filter, younger6birthday conditional.',
    'KISAS Grade4–9 and age10–15, nextJanuary2027 dates/length/venue/fee TBA. Cohort1 10days/9nights/staff/insurance are not verified2027 commitments. English humanities direct proof, full AI/music/residence English unknown, not an Oxford-certified course.',
    'Embassy Korea21–30Mar2027 age10–19 and parent programme; Matvey conditional10birthday, Oscar below minimum. Twin$2780 currency/unit/parent fee unresolved, only breakfast included. General USD200security/refundUSD100 and cancellation thresholds require current Korea contract confirmation.',
    'NTUE English guide visually read: Mandarin programme28Dec2026–8Jan2027,1Jan no class,NTD36000/early34000. English translation does not prove English teaching; no EN dossier/ICS added. Palau primary403/cache miss kept as gap, no homepage-price guess.',
    '17 new calendar rows and16 new family ICS entries; all previous2112family UID/datepairs and104exhibition entries preserved. SQLite/publicJSON agree, bridge idempotent,98family scenarios,0fullyaudited countries; complete worldwide goal remains active.'
]
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','PHL','USA','CAN','CRI','MEX','COL']}
learning=sum(e['block']=='Лагеря' for e in d['events'])
audit=dict(asof='2026-10-05',version=83,status='progress',scope='Programme-specific Japan/Taiwan/Singapore/Korea and Cebu packages; all priority regions and full worldwide goal remain active',
    new_dossiers=16,operators_covered=7,updated_dossiers=[],new_calendar_rows=17,new_family_ics=16,reused_existing_calendar_rows=0,
    programme_dossiers=448,countries_with_dossiers=34,official_dossier_urls=703,country_dossier_counts=byiso,programme_slugs=slugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2128,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),
        reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue Swiss/French/Spanish/Europe,USA/Canada/CostaRica/Mexico/LatinAmerica and Asian junior/general/technical2026–27 day/boarding/family programmes, full prices/languages/grade/admission/availability, plus schools/results/routes and worldwide leagues/exhibitions')
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('asia-camp-audit-v83',audit)
write('asia-camp-source-receipts-v83',dict(asof='2026-10-05',version=83,
    scope='31 directHTML/PDF attempts:22successful bodies retained/9HTTPerrors. Four NTUE guide images independently downloaded/hashed/visually read. Four retained own web-reader snapshots; HTTP403 and Palau cache miss not relabelled as successful programme reads.',
    sources=receipts,image_sources=images,web_reader_sources=web,dossier_source_urls_added=newurls,
    visual_primary_reads=[dict(url='https://myokoenglishexplorers.com/wp-content/uploads/2026/03/2026-EE-Adventure-Culture-Camp-overview.pdf',pages=[3,5],method='Poppler rendered and read age/English and dates/price table'),
        dict(url='https://www.kidsspace.sg/wp-content/uploads/2025/12/2026-CAMPS-CALENDAR.pdf',pages=[1],method='Poppler rendered and read year/theme/date poster; no full programme age/fee proof'),
        dict(url='https://clec.ntue.edu.tw/p/404-1018-57247.php?Lang=zh-tw',method='Four linked English guide images visually read; translation does not establish EN teaching')],
    external_actions=external,notes=['RawHTML/PDF/provider child photographs, rendered images and web-reader bodies stay outside public repository; public facts/provenance/errors only.',
        'A sourced date is not a confirmed place, booked course, accepted foreign grade or whole-family quote.',
        'No applications, bookings, payments, organizer messages or new automations.',
        'Full worldwide authorised scope preserved;0fullyaudited countries.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=83:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version82 native publication succeeded: commit 94063c00ad38953ac234e75f35ddb0d17654c176; deployment appgdep_6ac3edcce8d08191b38640807f6abce9.17new dossiers/39calendar rows. Goal active; worldwide coverage incomplete.')
plan['latest_validation']=dict(version=83,asof='2026-10-05',status='Independent source/preservation/calendar verification; native publication tracked separately',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=448,countries_with_dossiers=34,official_dossier_urls=703,
    family_ical=2128,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['asia_camp_programme_audit_v83']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=448,countries=34,swiss=69,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v83:448 programme/age/format dossiers in34countries;16new dossiers/17calendar rows/16familyICS,703dossierURLs. Grade/language/foreign/year/price/venue/availability boundaries retained; all priority regions and worldwide blocks remain active,0fullyaudited countries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=82','?v=83').replace('data-ui-version="82"','data-ui-version="83"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_asia_camp_audit_v83.json" download>Азия: программы, возраст и условия ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v83.json" download>Источники проверки азиатских программ ↓</a> · '
anchor='<a href="downloads/STEM_europe_camp_audit_v82.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=448,new_dossiers=16,new_calendar_rows=17,new_family_ics=16,source_urls=703,goal='active')))
