"""Save bounded primary evidence and progress; deployment is a separate receipt."""
import hashlib, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT.parent/'stem-family-atlas-work/camps-primary-v86'
BASE = '3585725a3011b0e34d825786540ed906be4cce35'
b = json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
d = json.loads((ROOT/'data/catalog.json').read_text())
c = d['camp_programmes']
oldslugs = {p['slug'] for p in b['camp_programmes']['profiles']}
oldids = {e['id'] for e in b['events']}
slugs = [p['slug'] for p in c['profiles'] if p['slug'] not in oldslugs]
new = [e for e in d['events'] if e['id'] not in oldids]
assert len(slugs)==18 and len(new)==7 and c['counts']['dossiers']==505
receipts = [v for f in sorted(PRIMARY.glob('receipt-*.json')) for v in json.loads(f.read_text())]
assert len(receipts)==41 and sum(v.get('status')==200 for v in receipts)==40
for v in receipts:
    if v.get('status')==200:
        f = next(PRIMARY/(v['key']+ext) for ext in ['.html','.pdf'] if (PRIMARY/(v['key']+ext)).exists())
        assert hashlib.sha256(f.read_bytes()).hexdigest()==v['sha256']
        v.update(body_snapshot_retained=True,raw_filename=f.name,
                 content_scope='JavaScript shell only: title, no full programme body' if v['key']=='tyas-camp-details' else
                 'Payment form with undated/inconsistent packages, no current curriculum' if v['key']=='nishimachi-summer' else
                 'Primary HTML/PDF snapshot retained; read depth and programme limits specified in audit')
images = json.loads((PRIMARY/'image-receipts.json').read_text())
for v in images:
    assert hashlib.sha256((PRIMARY/v['file']).read_bytes()).hexdigest()==v['sha256']
    v['content_scope'] = 'School photographs visually inspected; not programme/date/price evidence'
visual = []
for file,url,page,note in [
    ('gep-guardian-page3.png','https://thegep.com/wp-content/uploads/2026/05/01-EN_May-2026-GEP-Terms-and-Conditions.pdf',3,
     'Visually read May2026 contract: parent abroad requires local guardian/3-hour availability; conditional service RM800/day; force-majeure credit rather than cash refund.'),
    ('gep-cancellation-page7.png','https://thegep.com/wp-content/uploads/2026/05/01-EN_May-2026-GEP-Terms-and-Conditions.pdf',7,
     'Visually read cancellation cutoff of more than60 business days, RM1000 charge, later conditional credit; separate flight terms.'),
    ('minecraft-age-page1.png','https://mccup.jp/pdf/minecraftcup_guidelines_2026.pdf',1,
     'Visually read official8thCup organiser and age cutoff1Apr2027, junior includes preschool/1–40members. Training provider cutoff1Apr2026 not copied into official eligibility.')]:
    bb=(PRIMARY/file).read_bytes()
    visual.append(dict(url=url,page=page,method=note,render_sha256=hashlib.sha256(bb).hexdigest(),render_bytes=len(bb)))
oldurls = {s['url'] for p in b['camp_programmes']['profiles'] for s in p['sources']}
newurls = sorted({s['url'] for p in c['profiles'] for s in p['sources']}-oldurls)
assert len(newurls)==22 and c['counts']['source_urls']==771
external = dict(messages_sent=False,applications_submitted=False,payments_made=False,subscriptions_created=False,automations_created=False)
checks = [
    'All2959 previous events and487 complete dossier records/IDs preserved;18 new programme/format dossiers across5 operators/4 countries, not18 independently ranked camps. Korean/TYAS/Nishimachi incomplete leads retained as gaps, not verified2027 cohorts.',
    'CanadianAcademy5 own2026 programme pages: ExperiencePreK–G6/VEX elective/English communication/JPY75000week140000fortnight+3500registration;DiscoveryPreK–G12/no language requirement/PreKownstudents only/118000+8000lunch+3500registration. Two-child sums independently checked. Schoolboarding not inherited by summerdaycourses.',
    'CAInspiritAI G6–12 USD1200;JapaneseAIFromScratch G8–12 JPY60000 with explicitENtranslation, not childrenScratch. IBMathG9–11/G10–11 and3.5teachinghours/day. Birthyears2017/2020 do not establish schoolgrades; grade-limited eligibility unknown until actualgrade supplied. No2027 dates guessed from account pre-registration.',
    'TAIS own2027 forms read without submission:junior8–11/G1–5,2or3weeks35000/58000NTD preliminary+2000deposit,no dates;2026body8–12/G1–6 retained. Teen12–17 provisional1week25000/2week48000/4week70000,3week62,00 typo not silently repaired. TeenFridayhome not continuous7-dayboarding;dayPuli/Yuchi,vegetarianmeals/ownmattress,creditclassownstudents.',
    'CodingLab course-specific GST/format/equipment/ratio verified:Scratch474.15/528.65/921.05;App/Python512.30/866.55/942.85SGD.10/17.5learningformat vs12/21fulldaypresence not all codinghours. Juniorpartnerpreschool-only;6yoScratchPrimary1 condition andPythonplacement alternative preserved. No Englishinstruction assumed from website language, no invented holidaycohorts.',
    'Graphite Roblox6+ body:Nov23–25/Dec7–9 withoutyear,Septemberheading/comingsoon and1.5h vs09:30–12 conflict retained;noICS. Operatorclaims/participationcertificates/internalhackathons not internationalcompetition/results.',
    'Minecraft official2026PDF independently read:DigitalManufacturingCouncil organiser,agecutoff1Apr2027/1–40juniorinclpreschool/overseasblock,Sep7entryclosed/finalFeb14,2027. CodingLabtrainingpackage975.55SGD GST/18coachinghours/ownstudents/prereqs and cutoff1Apr2026 differ;not officialentryrestriction or futureopen camp. Historical awards remain operatorclaims pending primaryresults.',
    'GEPWinter2027 independently parsed boarding10000/10000/20000 vsday9100/9100/18200RM,Jan10–22/Jan22–Feb3/combined25days. SpringMar26–Apr2,9–16,7326RM. Matveyagefits9minimum/Oscarbelow9;all7calendar/ICS additions currentfamilyconditional,day3 rows labelledwindow without invented weekdays.',
    'GEPMay2026 contract guardian3hours/RM800dayconditional,60businessdaycancellation/RM1000,force-majeureyearcredit and BSS-specific2000deposit retained. Contract2027/currentfullinvoice not obtained. Springlaptop vsgenericdevicepolicy unresolved. EpsomownaddressBandarEnstek notKLcentre. WildMinds11–17/B1,soldout2026/9400RM/internalflightincluded/externalflightnotincluded;no2027cohorts.',
    'ENtranslation is separate confirmed_support_languages;pureENinstruction filter excludes JAprimaryAIFromScratch,EN-support includes it;RUinstruction option restored. Concrete filter cases verified in Node, JavaScript syntax checked.',
    '2966events/1635camp-learningrecords,505dossiers/35countries/771dossierURLs,111family scenarios,2240familyICS/104exhibitionICS.7newdatedrows/7ICS;all priorUID/dates preserved,SQLite/publicJSON agreement and bridgeidempotence.0 fullyauditedcountries;worldwidegoal and all priorityregions remain active.'
]
byiso = {s:sum(p['iso']==s for p in c['profiles']) for s in ['CHE','FRA','ESP','GBR','DEU','AUT','NLD','TWN','SGP','JPN','KOR','MYS','USA','CAN','CRI','MEX','COL']}
learning = sum(e['block']=='Лагеря' for e in d['events'])
audit = dict(asof='2026-10-05',version=86,status='progress',
    scope='Japan/Taiwan/Singapore primary programme/price/grade/language/format audit;Malaysia winter/spring2027 and AIentrepreneurship;Korea incomplete leads;all authorised regions/worldwide work active',
    new_dossiers=18,operators_covered=5,updated_dossiers=[],new_calendar_rows=7,new_family_ics=7,
    future_age_rows_excluded_from_family_ics=0,reused_existing_calendar_rows=0,
    programme_dossiers=505,countries_with_dossiers=35,official_dossier_urls=771,country_dossier_counts=byiso,programme_slugs=slugs,findings=c['gaps'][-5:],
    calendar=dict(events=len(d['events']),learning_records=learning,family_ics=2240,exhibition_ics=104,managed_dated_rows=len(c['generated_event_ids']),
        reused_legacy_events=c['integration']['reused_legacy_events'],season_windows=c['integration']['seasonal_windows']),
    fully_audited_countries=0,worldwide_complete=False,external_actions=external,validation=checks,
    next_priority='Continue Switzerland/France/Spain/Europe,Taiwan/Singapore/Korea/Japan,USA/Canada/CostaRica/Mexico/LatinAmerica and remaining world:all top general/technical26–27 seasonal camps,day/boarding/family,realEN/ES/RU/secondarysupport,fullfees,ages/grades/foreignadmission;schools/results/routes/leagues/exhibitions remain in scope')
def write(stem,v):
    t=json.dumps(v,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(t)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(t)
write('asia-camp-audit-v86',audit)
write('asia-camp-source-receipts-v86',dict(asof='2026-10-05',version=86,
    scope='41directHTML/PDF attempts:40HTTP200 incloneJSshell andoneundatedpaymentform;one404 retained.ThreePDFvisualreads andthreephotoinspections,not44 complete camp audits.',
    sources=receipts,image_sources=images,visual_primary_reads=visual,dossier_source_urls_added=newurls,external_actions=external,
    notes=['RawHTML/PDF/providerphotos/renderedpages remain outside public checkout;public paraphrased facts/provenance/errors only.',
        'Publicforms read only;noapplications/bookings/payments/messages/subscriptions/automations.',
        'Publishedprice/date notguaranteedplace/admission/fullinvoice or globalranking;worldwide goal active.']))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=86:
    plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof='2026-10-05',
    evidence='Version85 native publication succeeded: commit3585725a3011b0e34d825786540ed906be4cce35;deployment appgdep_6ac401208dc081918407d140936870d5.23new dossiers/136calendar rows/84familyICS. Full worldwide scope remains active.')
plan['latest_validation']=dict(version=86,asof='2026-10-05',status='Independent source/preservation/languagefilter/calendar verification;nativepublication tracked separately',
    events=len(d['events']),camp_learning_records=learning,programme_dossiers=505,countries_with_dossiers=35,official_dossier_urls=771,
    family_ical=2240,exhibition_ical=104,worldwide_complete=False,checks=checks,country_dossier_counts=byiso)
plan['asia_camp_programme_audit_v86']=audit
plan['camp_catalog_integration'].update(asof='2026-10-05',dossiers=505,countries=35,swiss=78,
    generated_calendar_entries=len(c['generated_event_ids']),reused_legacy_events=c['integration']['reused_legacy_events'])
for req in plan['requirements']:
    if req['id'] in ['camps','family_top_picks','camp_calendar_2026_2027','camp_full_pricing']:
        req['evidence']='v86:505programme/venue/formatdossiers in35countries;18new across5operators,7datedrows/7familyICS,771dossierURLs. CA/Taiwan/Singapore/Malaysia primarycurriculum/fees/grades/languages/secondaryEN/guardian and archive/currentseason boundaries verified;all priorityregions/fullworldwide26–27general+technicalcamps active,0fullyauditedcountries.'
plan['status']=plan['native_goal_status']='active';plan['updated']='2026-10-05';write('research-plan',plan)
p=ROOT/'dist/index.html';p.write_text(p.read_text().replace('?v=85','?v=86').replace('data-ui-version="85"','data-ui-version="86"'))
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
link='<a href="downloads/STEM_asia_camp_audit_v86.json" download>Азия: программы, языки и полная смета ↓</a> · <a href="downloads/STEM_asia_camp_source_receipts_v86.json" download>Источники проверки Азии ↓</a> · '
anchor='<a href="downloads/STEM_europe_camp_audit_v85.json"'
if link not in s:
    assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(dossiers=505,new_dossiers=18,new_calendar_rows=7,new_family_ics=7,source_urls=771,goal='active')))
