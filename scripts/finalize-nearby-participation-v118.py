"""A bounded nearby participation audit; the worldwide camp/school scope remains active."""
import collections,hashlib,json,subprocess
from nearby_participation_v118 import ROOT,BASE,CHECKED,UPDATED
P=ROOT.parent/'stem-family-atlas-work/nearby-primary-v118'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={e['id']:e for e in b['events']};now={e['id']:e for e in d['events']}
changed=[k for k in old if now[k]!=old[k]]
assert set(changed)==set(UPDATED) and now.keys()==old.keys()
assert d['camp_programmes']==b['camp_programmes'] and d['camp_planning']==b['camp_planning']
receipts=[q for f in sorted(P.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==30 and sum(q.get('status')==200 for q in receipts)==25
sources=[]
for q in receipts:
    q=dict(q,checked=CHECKED,retrieval_method='direct_public_http')
    if q.get('status')==200:
        name=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
        raw=(P/name).read_bytes();assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
        q.update(raw_filename=name,body_snapshot_retained=True,content_scope='Selected public programme/rule/price clauses; not a complete site, country or current intake audit.')
        if q['key']=='luva':q['content_scope']='HTML title and own script reference only; substantive selected clauses read in own linked bundle.'
        if q['key']=='luva-bundle':q['content_scope']='Read own public JS text:10Octubre/SumoLEGOsecundaria/InscripcionesCerradas; no code execution or form submission.'
        if q['key'] in ['mtiny-price','codey-price','mtiny-kit','mtiny-arena','mtiny-robot','codey-robot','codey-arena']:
            q['content_scope']='HTMLmetadata explicit MXN/price plus selected purchase/kit clauses. Some visible prices hidden behind information request; not current accepted2026invoice, stock not competition seats.'
    else:q.update(body_snapshot_retained=False,content_scope='Retrieval error; no primary body inferred. Guessed Inspire/Starter PDF paths rejected; actual linked English files separately recovered.')
    sources.append(q)
visual={'tecpro-rules':[5,8,9],'mtiny-rules':[2],'codey-rules':[2],'inspire-rules-linked':[7],'starter-rules-linked':[6],'lati':[2]}
blocks=collections.Counter(e['block'] for e in now.values())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2770 and expo==104
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
budget=d['family_strategy']['nearby_participation_v118']
assert len(budget['items'])==14 and len(budget['budget_scenarios'])==3 and len(budget['prices'])==7
audit=dict(version=118,asof=CHECKED,status='progress',scope='Selected nearby CRI/MEX competition entry gates and one child-specific route, with partial equipment/registration estimates. No new camp dossiers; not complete country/world audit.',
    events=len(now),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],
    programme_dossiers=890,countries_with_dossiers=39,official_dossier_urls=1398,editorial_scenarios=215,budget_scenarios=27,budget_providers=16,league_profiles=len(d['league_guide']['profiles']),
    updated_event_ids=changed,new_event_ids=[],new_dossiers=0,unchanged_event_objects=len(now)-len(changed),unchanged_dossier_objects=890,
    source_retrieval_attempts=30,direct_successful_bodies=25,retrieval_errors=5,pdfs_downloaded=6,new_visual_pdf_checks=8,
    nearby_route_candidates=14,registration_equipment_price_listings=7,partial_competition_budget_scenarios=3,new_camp_budget_scenarios=0,
    family_ical=family,exhibition_ical=expo,external_actions=external,goal='active',worldwide_complete=False,fully_audited_countries=0,
    checks=[
     'All890 camp dossier objects,27 partial camp budget offers,3555 event IDs, prior leagues/schools/worldwide requirements retained. Fifteen selected competition records corrected; no duplicate event/card or fabricated2027date.',
     'TecPro08Oct2026:6–8Artifact/9–12Game,2–4students and school-authorized adultmentor; adult verbal support only, original readyproject needed. Documentation07Oct derived fromdaybefore is not registration deadline; virtual28Sep/04Oct deadlines are separate. Birthyears2017/2020 mean8–9/5–6 in2026; exactbirthday/cutoff uncertain.',
     'LUVÁ own linked bundle saysInscripcionesCerradas andSumoLEGOsecundaria,10Oct. Publicclosedstatus does not verify Matvey exception/family admission or accepted payment.',
     'VEXMuseoAcertijo24Oct:ownwebreader24open/30capacity/FREE/Elementary/SkillsYes,physicalnotebook. Deadline24Oct00EDT=24Oct04UTC=23Oct22CostaRica; eventdayunchanged, timeddeadline corrected. Snapshotseats not reserved; directHTTP403 retained.',
     'MakeXmTiny4–6 andCodey6–9 at1Jan2026. Oscar2020 fitsmTiny; Codey onlyDOB1Jan2020. Matvey2017fitsCodey andcannotusemTinyregistration. InspireDOB2013–2020 onechild+mentor; StarterDOB2012–2020 one/twochild+one/twomentor; finalforeignintake stillunconfirmed.',
     'Seven shopHTMLmetadata prices explicitMXN. mTinyarena7499.99 alreadyincludes1registration; bundle16499.99 includes2butXIvsXII conflict. Codeyarena7999.99 excludesrobot/registration; expansion/pack404. Price metadata sometimesnotvisiblyshown, not currentinvoice. Formslinked byshop/category differ; noforms opened/submitted.',
     'Three partialcompetition scenarios:3999.98MXN registrations,14499.98Oscarrobot+arena includingregistration,5999.98Matveyrobot+registration missingrequiredexpansion. No inventedshipping/taxes/travel/refund/adultticket or doubledarena-registration.',
     'Robotifestpublicdeadline30Sep andLTRCrelative04Oct alreadypassed on06Oct; newteamroute notpresentedasopen. Robotifestfamilyvisitorneedsadmissionconfirmation, universityinvite notchildcompetitorproof. LTRCtechnical15cm1kg vsold20cm2kg conflict retained.',
     'RoboRAVEPV25–28Feb2027:8–15aMAZE,2–4team;Oscar2020in2027max7excludedfromthatchallenge. Text7challenges vs portalonlyaMAZE,60marketingcapacitynotlivecount,580USDpackageunknown. FLLExploremedaleveryparticipant notwinner; datesnextseason stillunannounced.',
     'Worldwide objective active: camps2026–27 EN/ES/RU day/boarding/family CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm; also leagues/competitions/exhibitions/schools5–10yearresults/routes. Zero fullyauditedcountries.'
    ])
def write(stem,value):
    s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('nearby-participation-audit-v118',audit)
write('nearby-participation-source-receipts-v118',dict(version=118,asof=CHECKED,scope=audit['scope'],sources=sources,visual_pdf_pages=visual,new_visual_pdf_checks=8,
    web_reader=[dict(url=now['C180']['source'],retrieval='primary_web_reader',direct_http_status=403,body_scope='Selected event metadata, agenda and notebook requirement.',observed_open_spots=24,capacity=30,free=True,deadline='24-Oct-2026 00:00EDT',snapshot_date=CHECKED)],external_actions=external))
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=118:plan['latest_validation_previous']=plan['latest_validation']
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected nearby clauses and portable database verified; native publication separate.'
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native117 succeeded; commit '+BASE+'; deployment appgdep_6ac4c6d2f9d4819198e5d82b8d4d3305. Worldwide objective active.')
plan['nearby_participation_audit_v118']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
    if q['id']=='unified_database':q['evidence']='v118:3555 records/890 dossiers/39 countries. Fifteen nearby competition gates updated;14 route candidates/7equipment price listings/3partialcompetition scenarios. Camps,27partialcamp offers unchanged; completeJSON/SQLiteZIP.'
    elif q['id']=='eligibility':q['evidence']='v118:birthyears2017/2020 notfixed9/6; TecProcutoffunknown, MakeX1JanversusDOBwindows, expiredentrydeadlines, VEXtimedlocaldeadline, OscarRoboRAVEaMAZEexcluded. Allforeignintake/places separate.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=118]+[dict(version=118,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=0,updated_event_ids=changed,new_calendar_rows=0,official_primary_retrieval_attempts=30,pdfs_downloaded=6,new_visual_pdf_checks=8,not_complete_worldwide=True)]
plan.update(updated=CHECKED,status='active',native_goal_status='active')
write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=117','?v=118').replace('data-ui-version="117"','data-ui-version="118"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_nearby_participation_audit_v118.json" download>Ближайшие старты · возраст, регистрация и техника</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps(dict(version=118,status='progress',updated_competitions=15,route_candidates=14,camp_dossiers_unchanged=890,goal='active')))
