"""Publish scoped evidence and retain every requirement of the active world goal."""
import hashlib,json,subprocess
from pathlib import Path
from opportunities_v107 import ROOT,BASE,CHECKED,NEW_IDS,UPDATED
PRIMARY=ROOT.parent/'stem-family-atlas-work/opportunities-primary-v107'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
ev={e['id']:e for e in d['events']};old={e['id']:e for e in b['events']}
assert set(ev)-set(old)==set(NEW_IDS)
assert {k for k,v in old.items() if ev[k]!=v}==set(UPDATED)
assert d['camp_programmes']==b['camp_programmes'] and len(d['events'])==3348
scopes={
 'luva-home':'HTTP200 only1692byte shell; no specific current programme clauses. Not proof of current closure, fees or young-child intake.',
 'roborave-pv':'ActualFeb25–28 2027/PuertoVallarta/580USD button with unknown unit/inclusions/60team advertised capacity not remaining places; existingC082 reused.',
 'roborave-events':'Current event index used for discovery; same events not duplicated and index/detail scale conflicts retained.',
 'roborave-challenges':'404; guessed path supplied no rules; actual programme route later recovered.',
 'roborave-home':'Actual network/ID invitation; freeRRID not free participation nor automaticWorld qualification.',
 'roborave-korea':'Actual Korea partner page; old8/23 and linked2026 rules not copied as complete2027 WRL rules.',
 'robofest-main':'Actual season index; existingWorld/US/video categories retained, no duplicate event.',
 'robofest-host':'Actual ownKwangWoon Augustannouncement says28–31May2027 confirmed; newer internationalSep25V1 stillTENTATIVE; conflict retained.',
 'waicy-2026':'ActualSep30page6–18/worldwide/remote/individual or team/four tracks; notification invitation not proven open registration.',
 'tmr-events':'Actual FMR2027 calendar reviewed; existingMexican competition/event entries reused, no invented new dates.',
 'roborave-beijing':'Actual existingFeb16 2027 event; no duplicate card/calendar row.',
 'roborave-guanajuato':'Actual21–22May2027 header butbody tentative/NATIONAL2027 vsInternationalheader; no confirmed datedICS.',
 'roborave-taiwan':'Actual existingJul27–28 2027 event reused; no duplicate card.',
 'roborave-houston':'ActualNov5–7 2027/venuePorconfirmar/no fresh fee. CorrectOscar2020birth:maximum7 in2027, noteligible aMAZE8–15.',
 'roborave-allchallenges':'404; no usable challenge body.',
 'worldrobotleague-home':'ActualFeb2027/day venue registration feesTBA/9events29divisions/foreign registrationEN promised/history roster not2027 confirmed countries.',
 'worldrobotleague-rules':'Actual rule directory; individual rules separately read; plannedAI Othello not current remotecontrolOthello.',
 'robofest-general':'Actual50pageGeneral2027.pdf V1Sep25; selected timeline/grade/fees/video clauses; May28–31TENTATIVE/Explorer1–4/Game5–8. Not full50page rule audit.',
 'waicy-guide':'Original Python SSLcertificate failure; no body in this attempt. Same URL recovered with ordinary verifiedTLS curl; separate successful receipt retained.',
 'beijing-robot-marathon':'Actual municipal Aug24announcement forApr18 2027/Yizhuang/global engineering teams. Family tickets/children unknown; race not counted as company tradeexpo.',
 'wrl-roborave-rules':'Actual English selected aMAZE/Line/Sumo/SoccerBot clauses; ownKorea800mmring overridesglobal100cm. ESgrade does not establish minimumage or foreign admission.',
 'wrl-othello-rules':'Actual U12 explicitly12orunder/1:1or2:2/500g/25cmcube/11.7V; AI plannedTBA; minimumage/cutoff unknown.',
 'wrl-soccer-rules':'Actual summary Junior5–13/2–3players2–4robots/allLEGO; linkedThai rules authoritative; MRC/KRL differences/finalrules≥50days before event.',
 'wrl-humanoid-relay':'Actual allages/allnationalities; robot/team/mission/scoringcomingsoon. Not confirmed ready child competition.',
 'roborave-amaze':'Actual8–15years/2–4students/ES8–11/2min/maze/noexternalmazesensors. Global lowerage not waived by unnumberedlocalES label.',
 'mrc-lego':'Actual ThaiMRC2026/Junior5–13/AllLEGO/2–3players2–4robots/20cm1000g/2minhalves; allLEGO junior amendmentFeb13 2026. Not confirmedKorea2027 final rulebook.',
 'mrc-open':'Actual ThaiMRC2026 openhardware rules as linked byWRL; not automatic2027 roster/pricing.',
 'waicy-guide-curl':'VerifiedTLS curl recovered actual30page2026Guidebook. SelectedArt/Video/LLM2026deadlineNov29 17ET; allgrades/VideoENorENsubtitles/LLMolder-target noage subdivisions. p2/p3/p5/p29 retain2025/finaldate conflicts. Seven PDF visual pages total across2documents; not entire30page audit.'
}
receipts=[q for f in sorted(PRIMARY.glob('receipt-*.json')) for q in json.loads(f.read_text())]
assert len(receipts)==28 and sum(q.get('status')==200 for q in receipts)==25
assert set(scopes)=={q['key'] for q in receipts}
for q in receipts:
    q.update(checked=CHECKED,content_scope=scopes[q['key']],retrieval_method=q.get('retrieval_method','direct_http'))
    if q.get('status')==200:
        f=PRIMARY/(q['key']+('.pdf' if q['key'] in ['robofest-general','waicy-guide-curl'] else '.html'))
        assert len(f.read_bytes())==q['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==q['sha256']
        q.update(raw_filename=f.name,body_snapshot_retained=True,content_status='non_specific_shell' if q['key']=='luva-home' else 'selected_pdf_clauses' if f.suffix=='.pdf' else 'selected_html_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
cal=dict(events=3348,competitions=1153,visitor_events=189,camp_learning_records=2006,family_ics=2593,exhibition_ics=104,league_profiles=141)
assert (ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT')==2593
sql=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text())
js=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
checks=[
 '10newcompetition categories/1newvisitor race/5updatedoldcards/1newleague profile. Existing3337cards preserved except specified5; all778campdossiers/2006learningcards/schools/results/routes unchanged.',
 'RoboRAVE Oscar2020 maximum7 throughout2027: aMAZE8–15 excluded; otherdiscipline routes not automatically excluded. ExistingPV/Taiwan/Beijing/Guanajuato/Houston reused;Guanajuato tentative/no fabricatedICS.',
 'WRL Korea Feb2027TBA/7category cards;Othello≤12/MRCSoccerJunior5–13/grade-basedRoboRAVE/Relaycomingsoon. EN/ESrules not proven judge/teachinglanguage; no independenttop-worldranking.',
 'WAICY3additionaltracks/one sharedNov29 2026 17ET deadlineICS=22UTC/16CostaRica; separate2026deadline clauses verified. Showcaseold2025/final4–6vs5–7conflicts retained; no fabricatedfinaldaycalendar. LLMolder-target/alllevels/noagegroups visible.',
 'Robofest ownhost confirmsMay28–31 vs newerinternationalV1stillTENTATIVE; dates remainblank/Explorergrade1–4 separateGamegrade5–8. Nationalqualifying routes not automaticopenWorld admission.',
 'BeijingrobotmarathonApr18 2027 visitorcandidate only; childtickets/priceunknown. Not countedas majorcompanyexpo;104expoICS unchanged.',
 '28retrievalattempts/25actualbodies:23HTMLincluding1nonspecificshell and2PDFs/3originalerrors. FailedPDFcert attempt retained and separateordinaryTLS curlsuccess. Selected7PDFpages visually checked, no entirecountry/website audit.',
 'FullSQLite andJSONZIP verify original bytes/hash/README; no records removed for static filelimits. DataJS/world scope preserved;0fullyauditedcountries.'
]
next_priority='Continue deep top general/thematic/STEM camps2026–27/day/boarding/family EN/ES/RU in CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm. Read actual programmes/full invoices/nightcare/foreign intake/teacher language/refunds/gear/current places and expose child-specific shortlist. Balance leagues/competitions/exhibitions and permanent schools/results5–10years/family routes; resolve WRLdates/finalrules, WAICYyear/finals, Robofesthost-vs-internationaldate conflict. All world requirements stay active;0fullyauditedcountries; never truncate records tofitstaticlimits.'
audit=dict(version=107,asof=CHECKED,status='progress',scope='Selected2026–27 competition/category/visitor opportunities; not completecamp/country/world audit.',new_event_ids=NEW_IDS,updated_event_ids=UPDATED,new_competitions=10,new_visitor_events=1,new_league_profiles=1,new_family_ics=2,new_deadline_ics=1,new_exhibition_ics=0,calendar=cal,programme_dossiers=778,countries_with_dossiers=39,official_dossier_urls=1215,worldwide_complete=False,fully_audited_countries=0,primary_retrievals=dict(attempts=28,http200=25,selected_html_bodies=22,non_specific_shells=1,actual_pdfs=2,retrieval_errors=3,selected_visual_page_checks=7),external_actions=external,validation=checks,next_priority=next_priority,complete_database_download=sql,complete_json_download=js)
def write(stem,value):
    s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('opportunities-audit-v107',audit)
write('opportunities-source-receipts-v107',dict(version=107,asof=CHECKED,scope='Selected clauses only; raw bodies retained privately, no whole-site/country audit.',sources=receipts,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=107:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication106 succeeded;commit '+BASE+';deployment appgdep_6ac47e3972308191a285460051db93b0. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=107,asof=CHECKED,status='Independent selected-source/preservation/category/calendar/completeZIP verification; nativepublication receipt separate',events=3348,camp_learning_records=2006,programme_dossiers=778,countries_with_dossiers=39,official_dossier_urls=1215,family_ical=2593,exhibition_ical=104,league_profiles=141,worldwide_complete=False,checks=checks,country_dossier_counts=plan['latest_validation_previous']['country_dossier_counts'])
plan['opportunities_audit_v107']=audit
plan['complete_database_download']=sql;plan['complete_json_download']=js
for q in plan['requirements']:
    if q['id'] in ['global_competitions','eligibility']:q['evidence']='v107:selected10newcompetitioncategories/5correctedoldcards/WRLprofile/WAICYdeadline; grade/age andunknown dates separated. Fullworldresearch remainsactive.'
    elif q['id']=='unified_database':q['evidence']='v107:completeJSON/SQLite portableZIP verified without reducing world/camp/schoolcoverage;3348cards/778campdossiers.'
entry=dict(version=107,asof=CHECKED,status='progress',scope=audit['scope'],new_competition_cards=10,new_visitor_cards=1,new_league_profiles=1,new_family_ics=2,new_deadline_ics=1,new_dossiers=0,corrected_existing_calendar_rows=5,official_primary_retrieval_attempts=28,unique_actual_pdfs=2,selected_visual_page_checks=7,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=107]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=106','?v=107').replace('data-ui-version="106"','data-ui-version="107"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_opportunities_audit_v107.json" download>Новые категории и уточнения допуска · JSON</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',calendar=cal,source_attempts=28,actual_primary_bodies=25,goal='active')))
