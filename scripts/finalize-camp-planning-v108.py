"""Retain worldwide scope while recording a bounded planning and price pass."""
import hashlib,json,subprocess
from pathlib import Path
from camp_planning_v108 import ROOT,BASE,CHECKED
P=ROOT.parent/'stem-family-atlas-work/camp-planning-primary-v108'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
assert {k:v for k,v in d.items() if k!='camp_planning'}==b
assert len(d['camp_planning']['offers'])==9
scopes={
 'garenne-main':'Selected current Summer2027 age/parents-nearby format clauses; not whole-site audit.',
 'garenne-contract':'Actual nine-page Summer2027 PDF; selected fee, 5–12 programme, 8–12 extras, insurance, pocket money, sibling and refund clauses. Five selected pages visually inspected.',
 'garenne-form':'Read-only public page: mandatory insurance and conditions; no form filled or submitted.',
 'leselfes-summer':'Selected current general camp age and 2027 programme clauses; EN camp life does not prove EN technical teaching.',
 'leselfes-contract':'Actual two-page Summer2027 PDF; both pages visually inspected. Base, compulsory registration/medical fees, single workshop age, transfers and refund conditions.',
 'tasis-fees':'Actual2027 two three-week sessions; CDE7–10/day/boarding and Minnows4–6/day standard/extended tariffs.',
 'tasis-faq':'Selected age-on-first-day, insurance day-vs-board, sibling rooming, deposits/refunds and non-included expenses.',
 'ermitage-camp':'Actual autumn2026 bilingual Wizards/4–10/day/610EUR week. This fee is not carried into2027; meals and cancellation pricing remain unknown.',
 'kings-soto':'HTTP200 2813-byte shell; web reader also has zero programme lines. No programme or current2027 price established.',
 'helvetic-camps':'Direct403 retained; separate web reader recovered actual own page still showing2026, conflicting age labels. No730CHF price assigned to2027.'}
r=json.loads((P/'receipt-1.json').read_text());assert len(r)==10
for q in r:
    q.update(checked=CHECKED,content_scope=scopes[q['key']],retrieval_method='direct_http')
    if q.get('status')==200:
        f=P/(q['key']+('.pdf' if 'contract' in q['key'] else '.html'))
        body=f.read_bytes();assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
        q.update(raw_filename=f.name,body_snapshot_retained=True,content_status='non_specific_shell' if q['key']=='kings-soto' else 'selected_pdf_clauses' if f.suffix=='.pdf' else 'selected_html_clauses')
    else:q.update(body_snapshot_retained=False,content_status='retrieval_error_no_body')
w=P/'primary-web-reader.json';wb=w.read_bytes()
fallback=dict(retrieval_method='web_primary_reader',urls=json.loads(wb)['urls'],sha256=hashlib.sha256(wb).hexdigest(),bytes=len(wb),actual_programme_bodies=1,empty_responses=1,scope='OwnHelvetic2026 programme recovered; ownKingSoto zero-line response. Raw response retained privately; no fresh2027 offer from either.')
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
sql=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text())
js=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
checks=[
 'All3348 event cards,778 programme dossiers,182 editorial scenarios,141 league profiles,schools/results/routes and old SQL rows retained; only camp_planning metadata added. No new dates or deadlines.',
 'Month intersection, source-date sorting, age-candidate ordering, retained old filters, direct dossier links, and shareable URL filters. An age ordering is not a world quality ranking.',
 'Nine two-child estimates from four providers in CHE/FRA. LesElfesJune10760/July13780CHF compulsory camp components; Robotics180 onlyMatvey after10. Not a full travel invoice.',
 'LaGarenne5–12 familybase12445day/13680boardCHF; second-child10percent on base only, same session/format; insurance10/child-day requires confirmed billed days; pocketmoney120/160 dependsMatvey9/10. Deposits not charged twice.',
 'TASIS8000/9000day scenarios and18400boardCHF. OscarMinnows4–6/day vs CDE7–10/board gated on first-day age. Day insurance price unknown, sibling rooming restricted. Ermitage1220EUR belongsOct2026 only; meals not assumed free.',
 'Blank or invalid mandatory/trip expenses remain missing; entered estimates separate from published components; no currency conversion or automatic complete invoice.',
 'Ten direct attempts/nine200 bodies: six usableHTML, one shell, twoPDF; one403 retained. Separate primary reader one actual2026 body/one empty. Seven selected PDF pages visually checked; no whole-country audit.',
 'Complete portable JSON/SQLite ZIP entries/hash/README and unchanged old CSV/ICS entries verified; all static assets below per-file limit. Worldwide scope active, zero fully audited countries.'
]
next_priority='Continue deep general/thematic/STEM camps2026–27/day/boarding/family EN/ES/RU in CHE/FRA/ESP/Europe/TWN/SGP/KOR/JPN/USA/CAN/CRI/MEX/LatAm: actual cohort programme, EN technical teacher, foreign intake, full invoice/nightcare/gear/refunds/current places and child-specific shortlist. Expand verified family cost scenarios and transparent editorial quality criteria without inventing a world ranking. Preserve competitions/leagues/exhibitions/permanent schools/5–10year results/family routes; resolve existing source/date conflicts. Worldwide objective active;0 fully audited countries.'
audit=dict(version=108,asof=CHECKED,status='progress',scope='Camp planning UX and selected Swiss/French family price components; not all programmes or full country audit.',new_event_ids=[],new_dossiers=0,budget_scenarios=9,budget_providers=4,budget_countries=['CHE','FRA'],events=3348,camp_learning_records=2006,programme_dossiers=778,countries_with_dossiers=39,official_dossier_urls=1215,family_ics=2593,exhibition_ics=104,league_profiles=141,worldwide_complete=False,fully_audited_countries=0,primary_retrievals=dict(direct_attempts=10,http200=9,usable_html=6,non_specific_shells=1,pdfs=2,errors=1,web_reader_actual_bodies=1,web_reader_empty=1,selected_visual_page_checks=7),external_actions=external,validation=checks,next_priority=next_priority,complete_database_download=sql,complete_json_download=js)
def write(stem,v):
    s=json.dumps(v,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('camp-planning-audit-v108',audit)
write('camp-planning-source-receipts-v108',dict(version=108,asof=CHECKED,scope=audit['scope'],sources=r,primary_reader=fallback,external_actions=external))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=108:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Research/nativepublication107 succeeded;commit '+BASE+';deployment appgdep_6ac483498dcc81919cb3f73ff9aa42db. Fullworldobjective unchanged.')
plan['latest_validation']=dict(version=108,asof=CHECKED,status='Selected primary fees/contract, old-record preservation, budget/filter/DOM and portable-export verification; native publication receipt separate',events=3348,camp_learning_records=2006,programme_dossiers=778,countries_with_dossiers=39,official_dossier_urls=1215,budget_scenarios=9,budget_providers=4,family_ical=2593,exhibition_ical=104,league_profiles=141,worldwide_complete=False,checks=checks,country_dossier_counts=plan['latest_validation_previous']['country_dossier_counts'])
plan['camp_planning_audit_v108']=audit;plan['complete_database_download']=sql;plan['complete_json_download']=js
for q in plan['requirements']:
    if q['id']=='camp_planning_ux':q.update(status='implemented_partial_research_active',evidence='v108:month/age-order/shareable filters above map/scenarios; compact182-scenario selector;9 family budget estimates. All778 dossiers retained. Full budget/duration/global quality ranking still incomplete.')
    elif q['id']=='camp_full_pricing':q['evidence']='v108:selected9 estimates/4providers/CHE-FRA verified from primary2027 tariffs/contracts and autumn2026. Mandatory unknowns, deposits, sibling conditions and age thresholds explicit; no fullworld invoice coverage.'
    elif q['id']=='camp_calendar_2026_2027':q['evidence']='v108:24-month overlap filter and nearest published-date ordering; exact dates/season windows retain distinction. 2593 familyICS unchanged; dates not invented.'
    elif q['id']=='unified_database':q['evidence']='v108:3348cards/778dossiers plus camp_planning metadata in complete JSON/SQLite portable ZIP; no truncation for static limits.'
    elif q['id']=='web':q['evidence']='v108:camp filters/cards before map and182 editorial scenarios; monthly selection, link sharing and partial family budget. Real headless offline DOM checks reported separately; research active.'
entry=dict(version=108,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=0,new_calendar_rows=0,budget_scenarios=9,budget_providers=4,official_primary_retrieval_attempts=10,actual_pdfs=2,selected_visual_page_checks=7,not_complete_worldwide=True)
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=108]+[entry]
plan['next_research']=[next_priority];plan['status']=plan['native_goal_status']='active';plan['updated']=CHECKED
write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=107','?v=108').replace('data-ui-version="107"','data-ui-version="108"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_camp_planning_audit_v108.json" download>Проверка семейных смет и выбора каникул · JSON</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=108,events=3348,camp_dossiers=778,budget_scenarios=9,goal='active')))
