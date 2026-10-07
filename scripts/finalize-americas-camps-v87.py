"""Bounded primary evidence and research progress; native publication separate."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRIMARY=ROOT.parent/'stem-family-atlas-work/camps-primary-v87'
BASE='d2451482d9480851f92ac41b9c9b48965f417adb'
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d=json.loads((ROOT/'data/catalog.json').read_text());c=d['camp_programmes']
oldslugs={p['slug'] for p in b['camp_programmes']['profiles']};oldids={e['id'] for e in b['events']}
slugs=[p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new=[e for e in d['events'] if e['id'] not in oldids]
assert len(slugs)==24 and len(new)==9 and c['counts']['dossiers']==529
receipts=[v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==44 and sum(v.get('status')==200 for v in receipts)==42
for v in receipts:
    if v.get('status')==200:
        f=next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v.update(body_snapshot_retained=True,raw_filename=f.name,
            content_scope='JavaScript shell, no full curriculum' if v['key']=='nr-home' else
            'K8 schedule matrix PDF, not full course catalogue; full catalogue is media/1461' if v['key']=='cu-catalog-full' else
            'Retained primary HTML/PDF; read depth and uncertainties in dossier/audit')
images=json.loads((PRIMARY/'image-receipts.json').read_text())
for v in images:
    assert hashlib.sha256((PRIMARY/v['file']).read_bytes()).hexdigest()==v['sha256']
    v['content_scope']='Own full poster visually inspected: seven modules/age/hours or address and operator claims; not independent accreditation'
visual=[]
for file,url,page,note in [
    ('cu-robots-page4.png','https://www.colorado.edu/sciencediscovery/media/1461',4,'Read Grade2–3 Robot Playground USD330, platforms/activities and early Friday release; archive2026.'),
    ('cu-ai-page8.png','https://www.colorado.edu/sciencediscovery/media/1461',8,'Read Grade7–8 AI330/Arduino370, TeachableMachine/microbit and take-homeGroveKit; archive2026.'),
    ('waterloo-robotics-page3.png','https://uwaterloo.ca/engineering-outreach/sites/default/files/uploads/documents/discovery-b-2026-sneak-peek.pdf',3,'Read teamLEGO SPIKEPrime, TinkerCAD, shortweek exclusions; curricula not every-hour robotics.'),
    ('sloane-day-refunds-page23.png','https://campsloane.org/client_media/files/pdf/2027%20DC%20Handbook.pdf',23,'Read dayMar1 finalbalance/nonrefundabledeposit, medical exception, insurance not included. Filename2027 not assumed all undated clauses newly issued.')]:
    bb=(PRIMARY/file).read_bytes();visual.append(dict(url=url,page=page,method=note,render_sha256=hashlib.sha256(bb).hexdigest(),render_bytes=len(bb)))
oldurls={s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls=sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==33 and c['counts']['source_urls']==804
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False,automations_created=False)
learning=sum(e['block']=='Лагеря' for e in d['events'])
byiso={s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','USA','CAN','CRI','MEX','BRA']}
checks=[
    'All2966 previous events and505 complete dossiers/IDs preserved;24 new programme/format dossiers across7 operators in USA/Canada/Mexico, not24 unique globally ranked camps. Four new family comparison scenarios, no general world-completion claim.',
    'Berkeley own course pages: Grades1/2/3–4 engineering day1295USD/fortnight2026; actual grades unknown. NanoG7–9 and AIG10–12 day1550 plus optionalboard1350=2900;boardingonlyeligibleweeks/course,1:10residential/1:12instruction,noairporttransport. NanoJuly9 vs residentialJuly10 discrepancy retained.2027 dates/prices not guessed.',
    'CU actual13page2026 catalogue media1461 read, media1460 onlymatrix. K–2 rockets595, G2–3robot330,G5–6Scratch330/short265,G7–8AI330/Arduino370,G9–12XRP1270. GroveArduino/XRPtakehome onlyexplicitcourses;Fridayearlyrelease/ownlunch/5yearminimum retained. SeparatecurrentVEXcampnotconfirmed,2027announcementDecember2026. Spanishparentmanual not Spanishinstruction.',
    'Waterloo gradegroups2–3/4–5/6–7/8–9 Fall2026; junior5 ownPDFs/seniorcurriculum read. SPIKEPrime/Ozobot/microbit/Python/solder/Arduino/3D projects vary;B/C/A repeatedweeks do not create newtopics. 362CADfive/290fourdays, pizza2.5+HST, care5each/week, cancellation25/50/fullwithinweek archivepolicy. English/foreignadmission still unconfirmed.',
    'Western SK–G1/G2–3/G4–6 samegrade2026;4themes twice plusbestof repeats,325/275CAD, structured9–16 vs supervision8:30–16:30, care25each optional.80percentrefund≥14days,no laterrefund. Not automatically specializedrobotics/boarding/English.',
    'Sloane2027 four fortnightboarding27Jun–10Jul/11–24Jul/25Jul–7Aug/8–21Aug,3045/2795/2545USD tiers;dayfourfortnights28Jun–9Jul/12–23Jul/26Jul–6Aug/9–20Aug+23–27Aug.Gradebasedeligibility unknown,ENcamp_life/internationalwelcome explicit. Dayprice1115/1040/965 and560/520/480 conflicts1085/1010/935 and545/505/465;nofinalpricechosen. OneweekJune4–July10error excluded, not repaired.',
    'SloanePDF2027filename parenthandbooks read:weekdaydayattendance, tentsadultcounselors, refundabledeposit500board/250dayuntilMar1, finalMar1day/May1board, medical exception/insuranceextra/JFKLGAtransportfeeunknown. Bothday/boardgeneraloutdoor, notrobotics;ES/RUwebsite translation not campinstruction.',
    'MexRoboticsstore2026ownlargeposters visuallyread sevenmodules/3–16/8–13/Jul20–Aug14;streetneighbourhoodconflict/price/language gaps retained. Robotitos8–14 summer vsgeneric6–14/5–7, $3000/$5100withoutyearcurrency;no2027datesguessed. FreshRobotiXFAQ noindividual/nochildsummerprogrammes;404oldtalleres not admitted as camp. BrazilNRstagingTLSfail/productionJSshell not completeauditedprogramme.',
    '2975events/1644learningrecords,529dossiers/35countries/804dossierURLs,115familycomparison scenarios;9newdatedrows/9familyICS,2249familyICS/104exhibitionICS. AllpreviousUID/content/datepairs preserved, SQLite/publicJSON/bridgeidempotence verified. No source snapshots/photos copied to public checkout.',
    'All worldwide authorised regions/general+technical26–27camps/schools/leagues/results/exhibitions/routes remain active,0fullyauditedcountries;not all programmeadmissions/prices/languages fullyconfirmed. Noapplications/messages/payments/accounts/automations.'
]
audit=dict(asof='2026-10-05',version=87,status='progress',scope='USA/Canada university technical curriculum and day formats;Sloane general day/boarding2027;Mexico technicallocal;Brazil/CRI incompletelead safeguards;worldwide work active',
    new_dossiers=24,operators_covered=7,new_calendar_rows=9,new_family_ics=9,updated_dossiers=[],programme_dossiers=529,countries_with_dossiers=35,official_dossier_urls=804,country_dossier_counts=byiso,programme_slugs=slugs,findings=c['gaps'][-4:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2249,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='All worldwide general/technical26–27 programmes:Switzerland/France/Spain/Europe,Taiwan/Singapore/Korea/Japan,USA/Canada/CRI/Mexico/LatAm;actualage/grade,EN/ES/RU/secondarylanguageproof,foreignadmission,allfees,boarding/day/family,seasons;schools/historicalresults/leagues/exhibitions/familyroutes remain in goal')
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(t)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('americas-camp-audit-v87',audit)
write('americas-camp-source-receipts-v87',dict(asof='2026-10-05',version=87,
    scope='44directHTML/PDFattempts,42HTTP200 inclNRJSshell;1HTTP404and1TLSfailure.2ownfullposters and4PDFvisualreads retained. These are not44 complete programmeaudits.',
    sources=receipts,image_sources=images,visual_primary_reads=visual,dossier_source_urls_added=newurls,external_actions=external,
    notes=['Primary snapshots/largePDF/posterimages/renders retained outside public checkout;paraphrased programme facts and hashes/errors only published.',
        'Currentprice/dates do not establish places/admission/finalinvoice/globalranking. OfficialPDFfilename2027 not proof all undated policyclauses newlydated.',
        'Universitygrade/English/foreignadmission pending, Sloaneprice/date discrepancies preserved;full worldwide scope active.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=87:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',evidence='Version86 native publication succeeded: commitd2451482d9480851f92ac41b9c9b48965f417adb;deployment appgdep_6ac407a2776c819195541d711497bde6.18newdossiers/7datedrows/7familyICS. Worldwidegoal active.')
plan['latest_validation']=dict(version=87,asof='2026-10-05',status='Independent source/preservation/calendar verification;native publication receipt separate',events=len(d['events']),camp_learning_records=learning,programme_dossiers=529,countries_with_dossiers=35,official_dossier_urls=804,family_ical=2249,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['americas_camp_programme_audit_v87']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=529,countries=35,swiss=78,generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v87:529 programme/venue/format dossiers in35countries,24new across7operators,9datedrows/9familyICS,804officialdossierURLs. Detailed universitycurriculum/fees/grades, Sloane2027generalday/boardpriceconflicts and Mexicoarchivalposter modules verified;all priorityregions/full worldwide26–27general+technicalcamps active,0fullyauditedcountries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=86','?v=87').replace('data-ui-version="86"','data-ui-version="87"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_americas_camp_audit_v87.json" download>США / Канада / Мексика: программы и ограничения ↓</a> · <a href="downloads/STEM_americas_camp_source_receipts_v87.json" download>Источники нового прохода ↓</a> · '
anchor='<a href="downloads/STEM_asia_camp_audit_v86.json"'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=529,new_dossiers=24,new_calendar_rows=9,new_family_ics=9,source_urls=804,goal='active')))
