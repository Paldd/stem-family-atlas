"""Publish a bounded Asia audit while retaining the complete worldwide research plan."""
import collections,hashlib,json,subprocess
from camp_asia_v116 import ROOT,BASE,CHECKED,NEW,UPDATED

P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v116'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
newids=sorted(now.keys()-old.keys());changed=[k for k in old if old[k]!=now[k]]
cp=d['camp_programmes'];offers=d['camp_planning']['offers'];blocks=collections.Counter(q['block'] for q in now.values())
assert not changed and len(newids)==10 and len(cp['profiles'])==883
assert offers[:24]==b['camp_planning']['offers'] and len(offers)==27
sources=[]
for f in sorted(P.glob('receipt-*.json')):
    for item in json.loads(f.read_text()):
        q=dict(item,checked=CHECKED,retrieval_method='direct_http',
               content_scope='Selected public programme/policy clauses; not an entire site or country audit.')
        if q.get('status')==200:
            ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html'
            raw=(P/(q['key']+'.'+ext)).read_bytes()
            assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
            q.update(raw_filename=q['key']+'.'+ext,body_snapshot_retained=True,
                content_status='selected_pdf_clauses_and_visual_pages' if ext=='pdf'
                else 'school_discovery_not_new_camp_evidence' if q['key'] in ['nishimachi','tis-summer','daewon','daewon-programme']
                else 'selected_html_clauses')
        else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
        sources.append(q)
assert len(sources)==36 and sum(q.get('status')==200 for q in sources)==32
assert sum(q.get('raw_filename','').endswith('.pdf') for q in sources)==3
visual=json.loads((P/'visual-review.json').read_text())
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,
              subscriptions_created=False,automations_created=False,consent_accepted=False)
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text())
jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2768 and expo==104
urls=len({s['url'] for p in cp['profiles'] for s in p['sources']});assert urls==1380
checks=[
    'Nine programme dossiers under five brands, not nine providers or an independently verified world ranking. All 874 prior complete dossiers, 3543 prior complete event objects and 24 budget offers unchanged. 883 dossiers / 39 countries / 1380 unique programme source URLs / 211 editorial scenarios / 233 gaps. 3553 catalogue records: 1153 competitions, 189 exhibitions, 2211 camp-learning.',
    'Camp Beaumont NLCS Singapore Magic 5–7 / Active 8–12: real booking dates December 14–18, 21–24, 28–31 in 2026. Marketing page incorrectly ends week two December 25; booking view omits that day. SGD 110/day, 550/5-day week, 440/4-day week. English communication requirement is camp-life evidence, not 20 academic lesson hours; Nexus English in Action has 20h and 5–12 but future dates/prices unannounced.',
    'Singapore winter meals not included by summer-only promise. Linked Singapore contract is named 2025; applicability to 2026 remains conditional. Non-FLEX nonrefundable; FLEX 20/day or100/week per child, cancellation fee3.5% plus retained FLEX, seven days in PDF versus seven working days FAQ. Optional family FLEX arithmetic200/160 uses daily rate; exact short-week quote still unknown. Promotions not automatically applied.',
    'D.CAMPS direct winter2027 posts: Daewon Jan11–15 and18–22 day09–14:30, grades1–6, KRW989000. SNU Jan4–8 four nights, grades4–6, KRW1790000. September18 early rates expired. Current general curricula: CTEB robotics/micro:bit/LEGO grades1–3, AI grades4–6; exact cohort-module availability conditional. Korean safety explanations explicitly disclosed. Birthyear alone not a grade equivalence, Oscar preschool intake not proved. SNU night medical coverage/2-person rooms/food stated; university credit or world medals not inferred.',
    'Gamja direct primary response says winter2027 although web-open cache showed2025. Jeju Jan5–24/Jan27–Feb15 each20 inclusive days versus label4weeks. KRW3900000, grade3 throughmiddle2; ESL English confirmed but AI/STEAM/math/nightcare English unproven. Grade/intake/insurance/refund conflict retained; Oscar too young for ordinarygrade3.',
    'UWC ISAK Summer2027 Jul18–31 English residential ages13–14, published DOBJuly2012–June2014; applicationsDec7–Jan31, decisionMar16, USD3850 orJPY600000 alternative currencies. Refund FAQ has2027/2026 contradiction. Winter2026 Dec26–30 ages12–13, USD1380 overseas orJPY200000 resident plusJPY2000 applicationfee, deadlineOct13 versusoldOct21 banner/portal2025 link. Both children later; future programmes not present family ICS or automatic UWC school admission. Winter accommodation nearby differs from summer campus dorms.',
    'MIT English Taiwan summer2026 archive: Chinese morning, at least3h English afternoon, grades1–6 or assessedsenior-kindergarten; branch-dependentSTEAM/LEGO/coding. RenaiJuly/August PDF visually checked. NTD12500/12000/11500 weekly tiers and5%sibling onlytwo+weeks;2027 not invented. CARES PDF halfoneweek withprocedure contradicts simplistic100%satisfaction interpretation; typhooncredit notcash. Winterownpage explicitlyChineseinstructors, noyear/dates/price/confirmedEN; no summer language or fee transferred. MITuniversity affiliation not claimed.',
    'TokyoInternationalSchool owncancelled summer2026 and proposedreturn2027, noexactdates/ages/prices/campEnglishcurriculum. Nishimachi stalepaymentform and2024resources do notprove2027camp. DaewonAt知 productnotD.CAMPS and noverifiedreadableage/language/dates. DulwichSeoul/Branksome/NLCSJeju discovery incomplete; not asserted nonexistent.',
    '36 directretrievalattempts,32HTTP200 bodies:29HTML+3PDF;fourerrors distinguished (406, TLS hostname mismatch, two guessed404s). ThreePDFs13pages text-extracted,eightselectedpages visuallyreviewed. Noforms/accounts/consents/messages/bookings/payments/automations. Fullglobalobjective active,zero fullyauditedcountries. PriorSwiss/French/Spanish,Americas,schools/leagues/exhibitions/routes preserved.'
]
priority=('Продолжить подробный аудит Швейцарии, Франции, Испании и Европы; Тайваня, Сингапура, Южной Кореи и Японии; США, Канады, Коста-Рики, Мексики и Латинской Америки. Все общие, тематические и STEM лагеря 2026–27, день/пансион/семья, EN/ES/RU: реальные программы, язык преподавателя, приём иностранных детей, возраст/класс, полный счёт с техникой, ночное сопровождение, страхование и отмена. Сохранить мировые соревнования, лиги, выставки, школы/результаты 5–10 лет и инженерно-предпринимательский маршрут. Общая цель остаётся активной.')
audit=dict(version=116,asof=CHECKED,status='progress',scope='Selected Singapore, Korea, Japan and Taiwan programmes and contract distinctions; not a complete country/world audit.',
    new_dossiers=len(NEW),new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=changed,
    events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,
    official_dossier_urls=urls,editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),
    country_dossier_counts=dict(collections.Counter(p['iso'] for p in cp['profiles'])),competition_records=blocks['Соревнования'],
    exhibition_records=blocks['События'],league_profiles=len(d['league_guide']['profiles']),budget_scenarios=27,
    budget_providers=16,budget_programme_dossiers=19,new_budget_scenarios=3,family_ical=family,exhibition_ical=expo,
    new_visual_pdf_checks=8,pdf_pages_text_extracted=13,external_actions=external,goal='active',worldwide_complete=False,
    fully_audited_countries=0,checks=checks,next_research=priority)
def write(stem,value):
    s=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(s)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('asia-camps-audit-v116',audit)
write('asia-camps-source-receipts-v116',dict(version=116,asof=CHECKED,scope=audit['scope'],sources=sources,visual_review=visual,
    external_actions=external,primary_reader_limits='Direct public bodies retained privately; selected programme/contract clauses and pages read. No external organizer intake or invoice confirmation. Web cached Gamja 2025 distinguished from direct2027 response.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=116:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,
    evidence='Native115 succeeded; commit '+BASE+'; deployment appgdep_6ac4bb7820948191a8a9c2c1508bf14e. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected primary clauses and complete portable database verified; native publication separate.'
plan['asia_camp_programme_audit_v116']=audit
plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
    if q['id']=='unified_database':q['evidence']='v116: 3553 records / 883 dossiers / 39 countries. Nine new dossiers and ten calendar records. All prior 3543 complete event objects and874 profiles unchanged; complete JSON/SQLite ZIP without truncation.'
    elif q['id']=='camp_full_pricing':q['evidence']='v116: 27 partial estimates, all24 prior offers unchanged. Singapore two-child bases1100/880SGD; Daewon onlyMatvey989000KRW. Contractapplicability/FLEX/meals/intake/equipment/fullinvoice still conditional. No freeOscar assumed.'
    elif q['id']=='camp_calendar_2026_2027':q['evidence']='v116: ten dated Asian rows, eight new familyICS; UWC futureage excluded from familyICS. NLCSreal21–24Dec dates, D.CAMPSgradegates, Gamja20days/4weeks conflict visible. No inventedMITsummer2027/Nexus/TIS/Nishimachidays. FamilyICS2768/expo104; priorUID/content preserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=116]+[dict(version=116,asof=CHECKED,
    status='progress',scope=audit['scope'],new_dossiers=9,updated_dossiers=0,new_calendar_rows=10,updated_calendar_rows=[],
    official_primary_retrieval_attempts=36,pdfs_downloaded=3,pdfs_selected_clauses_read=3,new_visual_pdf_checks=8,not_complete_worldwide=True)]
plan.update(next_research=[priority],status='active',native_goal_status='active',updated=CHECKED)
write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=115','?v=116').replace('data-ui-version="115"','data-ui-version="116"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_asia_camps_audit_v116.json" download>Азия · зима 2026–27, английский и пансионы по возрасту</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_europe_camps_audit_v115.json"'
link='<a href="downloads/STEM_asia_camps_audit_v116.json" download>Сингапур, Корея, Япония и Тайвань: смены, языки и пансионы ↓</a> · <a href="downloads/STEM_asia_camps_source_receipts_v116.json" download>Первичные источники и ограничения проверки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps(dict(version=116,status='progress',new_dossiers=9,new_calendar_records=10,events=len(now),dossiers=len(cp['profiles']),budget_scenarios=27,goal='active')))
