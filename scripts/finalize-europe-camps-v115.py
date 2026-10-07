"""Record a bounded primary audit and keep the full worldwide objective active."""
import collections
import hashlib
import json
import subprocess
from camp_europe_v115 import ROOT, BASE, CHECKED, NEW, UPDATED

P = ROOT.parent / 'stem-family-atlas-work/camp-europe-primary-v115'
d = json.loads((ROOT / 'data/catalog.json').read_text())
b = json.loads(subprocess.check_output(['git', 'show', BASE+':data/catalog.json'], cwd=ROOT))
old = {q['id']: q for q in b['events']}
now = {q['id']: q for q in d['events']}
changed = [k for k in old if old[k] != now[k]]
newids = sorted(now.keys()-old.keys())
cp = d['camp_programmes']
assert len(newids) == 53 and not changed and len(cp['profiles']) == 874
assert d['camp_planning']['offers'][:17] == b['camp_planning']['offers']
assert len(d['camp_planning']['offers']) == 24

sources = []
for f in sorted(P.glob('receipt-*.json')):
    for item in json.loads(f.read_text()):
        q = dict(item, checked=CHECKED, retrieval_method='direct_http',
                 content_scope='Selected public programme/policy clauses; not a full site or country audit.')
        if q.get('status') == 200:
            ext = 'pdf' if (P/(q['key']+'.pdf')).exists() else 'html'
            raw = (P/(q['key']+'.'+ext)).read_bytes()
            assert len(raw) == q['bytes'] and hashlib.sha256(raw).hexdigest() == q['sha256']
            scope = ('wrong_guessed_pdf_url_returned_html_not_a_pdf' if q['key']=='lamiranda-brochure'
                     else 'landing_redirect_not_the_linked_summer_programme' if q['key']=='lamiranda-camp'
                     else 'selected_pdf_clauses_and_visual_pages' if ext=='pdf'
                     else 'school_discovery_not_camp_evidence' if q['key']=='trillium-main'
                     else 'selected_html_clauses')
            q.update(raw_filename=q['key']+'.'+ext, body_snapshot_retained=True, content_status=scope)
        else:
            q.update(body_snapshot_retained=False, content_status='retrieval_error_not_content_evidence')
        sources.append(q)
assert len(sources)==38 and sum(q.get('status')==200 for q in sources)==32
assert sum(q.get('raw_filename','').endswith('.pdf') for q in sources)==8
visual = json.loads((P/'visual-review.json').read_text())
assert visual['new_visual_pdf_checks']==21 and visual['pdf_pages_text_extracted']==34
external = dict(messages_sent=False, applications_submitted=False, payments_made=False,
                accounts_created=False, subscriptions_created=False, automations_created=False, consent_accepted=False)
sm = json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text())
jm = json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
family = (ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')
expo = (ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
assert family==2760 and expo==104
blocks = collections.Counter(q['block'] for q in now.values())
country_counts = dict(collections.Counter(q['iso'] for q in cp['profiles']))
urls = len({s['url'] for p in cp['profiles'] for s in p['sources']})
assert urls==1361
checks = [
    '13 different tracks/formats under six brands; not 13 independent providers or an independently verified world ranking. All861 prior dossiers and3490 complete event objects preserved unchanged.874dossiers/39countries/1361unique URLs/207editorial scenarios/226gaps;3543events including2201camp-learning.',
    'Préfleuri Winter2027 own HTML and PDF agree Jan10–Mar19,min2weeks. Calendar keeps this a seasonal window with no fabricated exactstay. Feb6–13 ski only,no language or academic teaching. Winter groups3–6/7–10/11+ not summer groups. English15h/UK academic supported; independent AcademicIntegration price unknown,not automatically6750.',
    'Winter language2027CHF6750/2weeks through24400/9weeks; uniforms/equipment/fullboard/Swissinsurance described. Extra ski test/pocketmoney/medicalexcess sits under included heading in2027PDF,while olderweb calls itextra:fullcomposition unresolved. Different winter versus ski cancellation clauses and locked devices retained;summerphonecall times not promised for winter.',
    'SkiParis2027 three ownpublished staysFeb6–13/Feb13–20/Feb6–20. Price2500onlyfirstweek/4000two,secondseparateweekprice unknown. ParisTGV350roundtrip perchild plus programme:two-child base5000+700=5700 conditional partial arithmetic,notCostaRica fulltrip. InstructorENunknown;ski badges notSTEMworldmedals.',
    'Academicus autumnOct12–16,2026 and winterFeb15–19/Feb22–26,2027 EN5+communicative learners.785week/195day,meals/materials/publictransport/entries included. Maximum ratio7winter versus8autumn/summer,min4. Frozencreative/naturemuseumcurriculum notrobotics;Technorama visit onlysummer2026archive,notguaranteed2027theme. Spring/summer2027unannounced.',
    'friLingue AlpsWinter8–17 excludesOscar;7explicit2027startmarkers,notinferred fullstays.1200/2200/3200/4200CHF1–4weeks.12hcoursepage versus15hFAQ and exampletimetable conflict. Accommodationweek/venuechanges,privateoptions extra and separatebuildings retained. Published staffpresence not continuous24h observation guarantee.',
    'friLingue FamilyWorkation500/FamilyCamp800 CHF are adultweeklyfees,childcampprice/minage unknown.10published startmarkers each;winteradultonlyDec20,2026–Jan16,2027. ParentsPetitVélan versusmaincamp and transport/roomfees conflicts explicit. NoBraunwald age rule transferred. AdultENlesson600/1000 optional,notincludedchildinstruction. Cancelday7 overlaps80/100percent.',
    'LaMiranda three2026archive tracks. Actuallinked school119 PDF downloaded after an incomplete attempt; guessed school84 URL returns HTMLnotPDF. Juniorweb2017–19 versusPDF2018,2018,2019;Teensweb2014–16/Jun29–Jul24 versusPDF2013–15/Jun25–Jul18. No2027sessions invented. Kinder2020birthyearversusweb3–5 flagged. EN explicitly inprogramme;312external versus280Inspiredstudents;earlyMar31expired.150deposit/nonrefund/May29deadline2026only. Contractaccidentinsurance expresslyschoolstudents,externalcoverage unknown.',
    'Malherbe Oct19–23,2026 EN2–10;2–6general versus6–10confidentreading/writing,notconversation alone.500full09–16lunch/280morning09–12;twoformat variants,not10dates. ScienceFiction writingcamp notscience/AIcourse. Summer2026closedJul14archive not2027calendar.',
    'LivingSchool2026–27owncalendar9weeklyvariants eachfull/half.3–11externalpupils,ENnative teachers,bilingualcoursewithpossibleabsencewarning;Spanishonlysometimes.396full=358.40pedagogical+37.60meal,240half,87day/50halfday.10percentsecondchild base scope unclear;defaulttwo792/480before discount,752.40or756.16 conditionalfull arithmetic not invoice. School addresses differ;Jul14/attendancehours notinvented. ClosedChristmas/August. Cancellationwithoutfeeoneweek;subscriptionfees not transferred.',
    'Seven new partial two-child budget scenarios; all17previous scenarios untouched.24offers/14providerbrands/17programme dossiers. No full booking invoice asserted. Equipment,food,transport,language,intake,nightcare,medical andrefund uncertainties visible.',
    '53newcalendar records and53newtentativefamilyICS,including27explicitstartmarkers and26datedcamp/dayformat records;50seasonwindows unchangedplus2newPréfleuriwindows. All2707priorfamily UID/content preserved exceptDTSTAMP;exhibitionICS104 preserved. CompleteJSON/SQLiteZIP/CSV/filesize and UI checked separately.0fullyauditedcountries; full worldwidegoal active.',
    '38direct attempts32HTTP200 including8realPDF/24HTML;6retrievalerrors and2nonprogramme HTMLresponses distinguished. EightPDFs34pages text extracted;21selected pages visuallychecked. Noforms/messages/payments/accounts/consents/automations;documents are source material,notactioninstructions.'
]
priority = ('Continue deep Switzerland/France/Spain/Europe,Taiwan/Singapore/SouthKorea/Japan,USA/Canada,CostaRica/Mexico/LatinAmerica: all general/thematic/STEM camps2026–27,day/boarding/family and EN/ES/RU. Verify actual curriculum,teacherlanguage,foreignindividualintake,fulltwochildpricing/equipment/nightcare/insurance/refunds androutes. Preserve worldwide competitions/leagues/exhibitions/schools/results5–10years/engineeringentrepreneurjourney. Full objective remains active.')
audit = dict(version=115, asof=CHECKED, status='progress',
             scope='Selected Swiss winter/parent programmes, French English school holidays and Spanish archive contradictions; not a complete country/world audit.',
             new_dossiers=len(NEW), new_dossier_slugs=NEW, updated_dossier_slugs=UPDATED,
             new_event_ids=newids, updated_event_ids=changed, events=len(now),
             camp_learning_records=blocks['Лагеря'], programme_dossiers=874,
             countries_with_dossiers=39, official_dossier_urls=urls, editorial_scenarios=207,
             coverage_gaps=226, country_dossier_counts=country_counts, competition_records=1153,
             exhibition_records=189, league_profiles=len(d['league_guide']['profiles']),
             budget_scenarios=24, budget_providers=14, budget_programme_dossiers=17,
             new_budget_scenarios=7, family_ical=family, exhibition_ical=expo,
             new_visual_pdf_checks=21, pdf_pages_text_extracted=34, external_actions=external,
             goal='active', worldwide_complete=False, fully_audited_countries=0,
             checks=checks, next_research=priority)

def write(stem, value):
    s = json.dumps(value, ensure_ascii=False, indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(s)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)

write('europe-camps-audit-v115', audit)
write('europe-camps-source-receipts-v115', dict(version=115, asof=CHECKED, scope=audit['scope'],
      sources=sources, visual_review=visual, external_actions=external,
      primary_reader_limits='Direct public bodies retained privately; selected clauses/pages reviewed, not entire sites. Malherbe PDF letterspacing requires visual inspection. LaMiranda age/date and insurance conflicts remain unresolved. No external organizer confirmation.'))
plan = json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=115:
    plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,
     evidence='Native114 succeeded;commit '+BASE+';deployment appgdep_6ac4b37755ec819191e471a5a79f0022. Worldwide objective remains active.')
plan['latest_validation']=dict(version=115,asof=CHECKED,status='Selected primary clauses and complete portable database checks; native publication separate',
    events=3543,camp_learning_records=2201,programme_dossiers=874,countries_with_dossiers=39,
    official_dossier_urls=1361,editorial_scenarios=207,budget_scenarios=24,budget_providers=14,
    family_ical=2760,exhibition_ical=104,league_profiles=audit['league_profiles'],worldwide_complete=False,fully_audited_countries=0)
plan['europe_camp_programme_audit_v115']=audit
plan['complete_database_download']=sm
plan['complete_json_download']=jm
for q in plan['requirements']:
    if q['id']=='unified_database':
        q['evidence']='v115: 3543 cards/874 dossiers/39 countries; 13 new profiles/53 new calendar records. All3490 prior complete event objects/all861 prior complete profiles unchanged; complete JSON/SQLite ZIP without truncation.'
    elif q['id']=='camp_full_pricing':
        q['evidence']='v115: 24 partial family estimates, all17 prior offers unchanged; seven new CHF/EUR scenarios. Full invoice/intake/insurance/refund still conditional. Living discount base unresolved; LaMiranda2026 archive not2027 rates.'
    elif q['id']=='camp_calendar_2026_2027':
        q['evidence']='v115: 53 new records:27 start markers and26 dated stays/dayformat weeks. Préfleuri seasonal windows create no exactstay. FamilyICS2760/expo104; priorUID/content unchanged. No invented LaMiranda2027/Trillium camp or friLingue fullend dates.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=115]+[
    dict(version=115,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=13,updated_dossiers=0,
         new_calendar_rows=53,updated_calendar_rows=[],official_primary_retrieval_attempts=38,
         pdfs_downloaded=8,pdfs_selected_clauses_read=8,new_visual_pdf_checks=21,not_complete_worldwide=True)]
plan.update(next_research=[priority],status='active',native_goal_status='active',updated=CHECKED)
write('research-plan',plan)
p=ROOT/'dist/index.html';s=p.read_text().replace('?v=114','?v=115').replace('data-ui-version="114"','data-ui-version="115"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_europe_camps_audit_v115.json" download>Европа · зима 2027, школьные каникулы и цены на двух детей</a>'
if link not in s:
    assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
p=ROOT/'dist/assets/camp-programmes.js';s=p.read_text()
anchor='<a href="downloads/STEM_northamerica_camps_audit_v114.json"'
link='<a href="downloads/STEM_europe_camps_audit_v115.json" download>Швейцария, Франция и Испания: зимние и школьные программы ↓</a> · <a href="downloads/STEM_europe_camps_source_receipts_v115.json" download>Первичные страницы и ограничения проверки ↓</a> · '
if link not in s:
    assert anchor in s;s=s.replace(anchor,link+anchor,1)
p.write_text(s)
print(json.dumps(dict(status='progress',version=115,new_dossiers=13,new_calendar_records=53,new_budget_scenarios=7,dossiers=874,events=3543,goal='active')))
