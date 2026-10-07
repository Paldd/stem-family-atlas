"""Selected programme audit, publication links and the unchanged worldwide scope."""
import collections,hashlib,json,subprocess
from camp_latam_v117 import ROOT,BASE,CHECKED,NEW,UPDATED
P=ROOT.parent/'stem-family-atlas-work/camp-latam-primary-v117'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
old={q['id']:q for q in b['events']};now={q['id']:q for q in d['events']}
newids=sorted(now.keys()-old.keys());changed=[k for k in old if old[k]!=now[k]]
cp=d['camp_programmes'];offers=d['camp_planning']['offers'];blocks=collections.Counter(q['block'] for q in now.values())
assert not changed and len(newids)==2 and len(cp['profiles'])==890
assert offers==b['camp_planning']['offers'] and len(offers)==27
sources=[]
for f in sorted(P.glob('receipt-*.json')):
 for item in json.loads(f.read_text()):
  q=dict(item,checked=CHECKED,retrieval_method='direct_http',content_scope='Selected public programme and policy clauses, not an entire site or country audit.')
  if q.get('status')==200:
   ext='pdf' if (P/(q['key']+'.pdf')).exists() else 'html'
   raw=(P/(q['key']+'.'+ext)).read_bytes()
   assert len(raw)==q['bytes'] and hashlib.sha256(raw).hexdigest()==q['sha256']
   q.update(raw_filename=q['key']+'.'+ext,body_snapshot_retained=True,content_status='selected_pdf_clauses_and_visual_pages' if ext=='pdf' else 'selected_html_clauses')
   if q['key']=='mustakis-call':q['content_status']='article_title_only_no_full_programme_body'
  else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
  sources.append(q)
assert len(sources)==39 and sum(q.get('status')==200 for q in sources)==29
images=json.loads((P/'gapper-image-receipt.json').read_text())+[json.loads((P/'image-receipt.json').read_text())]
for q in images:
 raw=(P/(q['key']+'.png')).read_bytes();assert hashlib.sha256(raw).hexdigest()==q['sha256'] and len(raw)==q['bytes']
visual=dict(pdf_pages_text_extracted=17,new_visual_pdf_checks=6,rendered_pages={'mustakis-faq':[2,3,8,9],'ymca-news':[5],'camohmila-rules':[1]},
           image_checks=['rukamalon-rates','gapper-level'],image_non_evidence=['gapper-venue'],images=images,
           scope='Three PDF documents, selected programme/policy clauses; six visual PDF pages and two substantive images. Venue icon not programme evidence.')
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
family=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT');expo=(ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')
urls=len({s['url'] for p in cp['profiles'] for s in p['sources']})
assert family==2770 and expo==104 and urls==1398
sm=json.loads((ROOT/'dist/downloads/STEM_database_download.json').read_text());jm=json.loads((ROOT/'dist/downloads/STEM_database_json_download.json').read_text())
checks=[
 'Seven programme dossiers under six brands; two YMCA formats share one operator. No independent world ranking. All883 previous dossier objects,3553 events and27 partial budget offers unchanged. 890 dossiers /39 countries /1398 programme URLs /215 editorial scenarios /240 gaps. 3555 events:1153 competitions,189 exhibitions,2213 camp-learning.',
 'MET Panama Camp Corotu: ages3–5/6–8/9–13, non-MET students accepted, LEGO WeDo2.0 and Mindstorms named. Fourweeks Mo–Fr08–14 without dates/year. ENpage $275 non-MET /250 MET and50 weekly transport; ESpage says feessoon. Currency/year not asserted, no exact2027 session or budget invoice. Meals/materials/excursiontransport included by programme, homecamp transport separate; English website not instruction proof.',
 'YMCA Camohmila: traditional spring/summer/winter camps versus separate familyweekends/DayPass; 1counselor/10 statement not nightcare guarantee. Cabins8–22 for groups or2–5 for families. Primary newsletter2025 not2027; linkedrules2020 applicability conditional, reading not consent. No camp age/fee inferred from $40/month YMCA minors template or6600MXN charitable CasaBecarios monthlyfunding.',
 'Mustakis science/technology12–17 andFAQ2025 grade7basic throughgrade3secondary, aftergrade6. Freeonlyselected, materialsprovided, noelectronicsrequired, individualselection/motivation, first-sessionabsence losesplace, localtravelselfarranged, guardianoutsideclassroom, commitmentnextsemester. Landing2026 includesclosed/staledate templates; no2027 calendar invented. Bothchildrenlater; sevenvenues one dossier.',
 'ITSTEP Tijuana archive: headlineSummer2025, age7–16 narrative versusFAQ/card8–15, yearlessJuly8–12week sequence. Strict8–15 used: Matveyconditional/Oscarlater; ownFAQexternalstudents, lunch/snackextra, robots/game/Blender/VR topics but kit/hours/ownership unclear. $2350/2200pesos notcurrent2027 quote; adultpassport/online FAQ notchildentry evidence.',
 'Rukamalon artistic archiveJan5–23,2026 ages6–12; roboticsbonus1.5h for3+days versusmorethan3text conflict. Visualprices47400/92900/136900/179200/210000/380000 $, codeunconfirmed;3visit12h and5visit19h conflictwith3.5h/day. Mealsbringown, tablet/appandpossiblyinstrumentown; refundboundary7daysambiguous, new2027language/fees notinvented. Notfullroboticsintensive.',
 'Gapper homepageAugust2027:23–25Aug10:00/14:00 and25–27Aug18:00/15:00, age9–12/13–17, A2iconvisual,3dayfullEnglishimmersion andindividualentry explicit. Twoexactfuturecalendarrows, onlyMatveyconditional/Oscarlater. Lodging/nightstaff/fullinvoice unknown, formatunknown retained; no boarding promise or robotics/AI course inferred. Footer2026 andunreadableDrivebrochure distinguished.',
 'MuseoCR programmeforgroups notindividualcamp intake; ordinarymuseumticket notcampfee. STRI owncachedsearchsummary2024–26 notfullprimaryprogramme body: direct403/webopenRejected. Manque ownwebreader Jan4–10,2027 membershipManque/IFM-SEI; announcementEN/ES notteacher, individualnonmemberage/price/housingunknown, notreadyfamilydossier. METInnovation9–13 discoverynotCorotu fee/age and guessedURL404 retainedasgap.',
 '39 directretrievalattempts29HTTP200 bodies (26HTML3PDF),tenerrors. ThreePDFs17pages text-extracted;sixselectedvisualPDFpages+two substantiveimages. Noforms/messages/accounts/consents/bookings/payments/automations. Complete worldwide objective active,zero fullyauditedcountries; previousEuropeAsiaAmericas,leagues,exhibitions,schools androutes retained.'
]
priority='Продолжить подробный аудит Швейцарии, Франции, Испании и Европы; Тайваня, Сингапура, Южной Кореи и Японии; США, Канады, Коста-Рики, Мексики и Латинской Америки. Все общие, тематические и STEM лагеря 2026–27, день/пансион/семья, EN/ES/RU: содержание, язык преподавателя, индивидуальный приём, возраст/класс, полный счёт с техникой, ночное сопровождение, страхование и отмена. Сохранить мировой календарь соревнований, лиг, выставок, школы и результаты 5–10 лет, инженерно-предпринимательские маршруты. Общая цель активна.'
audit=dict(version=117,asof=CHECKED,status='progress',scope='Selected programmes in Panama, Mexico, Chile and Argentina, with CostaRica and blocked-primary discovery gaps; not a complete country/world audit.',
 new_dossiers=7,new_dossier_slugs=NEW,updated_dossier_slugs=UPDATED,new_event_ids=newids,updated_event_ids=changed,
 events=len(now),camp_learning_records=blocks['Лагеря'],programme_dossiers=len(cp['profiles']),countries_with_dossiers=39,official_dossier_urls=urls,
 editorial_scenarios=len(cp['shortlist']),coverage_gaps=len(cp['gaps']),country_dossier_counts=dict(collections.Counter(p['iso'] for p in cp['profiles'])),competition_records=1153,exhibition_records=189,
 league_profiles=len(d['league_guide']['profiles']),budget_scenarios=27,budget_providers=16,budget_programme_dossiers=19,new_budget_scenarios=0,
 family_ical=family,exhibition_ical=expo,new_visual_pdf_checks=6,substantive_image_checks=2,pdf_pages_text_extracted=17,external_actions=external,
 goal='active',worldwide_complete=False,fully_audited_countries=0,checks=checks,next_research=priority)
def write(stem,value):
 s=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(s);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(s)
write('latam-camps-audit-v117',audit)
write('latam-camps-source-receipts-v117',dict(version=117,asof=CHECKED,scope=audit['scope'],sources=sources,visual_review=visual,
 external_actions=external,web_reader=[dict(url='https://www.manquechile.cl/2026/08/29/inscribete-y-participa-en-el-campamento-internacional-verano-2027-manque-chile-international-summer-camp-2027-manque-chile/',status='selected_body_read',direct_http_status=403),dict(url='https://stri.si.edu/es/noticia/eventos-especiales-de-stri-feb-2026',status='cached_search_summary_only_open_rejected',direct_http_status=403)],
 primary_reader_limits='Selected public bodies and clauses retained privately. Cached summaries, old PDF dates, guessed404s and title-only pages not full newprogramme proof. No organizer intake/fullinvoice confirmation.'))
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=117:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='Native116 succeeded; commit '+BASE+'; deployment appgdep_6ac4c1c2c494819180abe19b7e3bf6d8. Worldwide objective active.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','budget_providers','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected primary clauses and complete portable database verified; native publication separate.'
plan['latam_camp_programme_audit_v117']=audit;plan['complete_database_download']=sm;plan['complete_json_download']=jm
for q in plan['requirements']:
 if q['id']=='unified_database':q['evidence']='v117: 3555 records /890 dossiers /39 countries. Seven new programme dossiers and two calendar rows; all3553 prior event objects and883 profiles unchanged. Complete JSON/SQLite ZIP.'
 elif q['id']=='camp_full_pricing':q['evidence']='v117: all27 partial budget estimates preserved. Current confirmed-currency invoices absent in new programmes; no new price scenario manufactured from old prices, symbol$ or socialfunding.'
 elif q['id']=='camp_calendar_2026_2027':q['evidence']='v117: Gapper twoAug2027 rows,Matveyconditional/Oscarlater; lodgingunknown. No inferred2027 dates fromMETfourweeks/YMCA2025/ITSTEPstaleweeks/Mustakisclosed/Rukamalonarchive. FamilyICS2770/expo104, allpriorUID/content preserved.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=117]+[dict(version=117,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=7,updated_dossiers=0,new_calendar_rows=2,updated_calendar_rows=[],official_primary_retrieval_attempts=39,pdfs_downloaded=3,pdfs_selected_clauses_read=3,new_visual_pdf_checks=6,substantive_image_checks=2,not_complete_worldwide=True)]
plan.update(next_research=[priority],status='active',native_goal_status='active',updated=CHECKED);write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=116','?v=117').replace('data-ui-version="116"','data-ui-version="117"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_latam_camps_audit_v117.json" download>Латинская Америка · программы, возраст, семья и условия</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text();anchor='<a href="downloads/STEM_asia_camps_audit_v116.json"'
link='<a href="downloads/STEM_latam_camps_audit_v117.json" download>Латинская Америка: дневные, пансионные и семейные программы ↓</a> · <a href="downloads/STEM_latam_camps_source_receipts_v117.json" download>Первичные источники и ограничения проверки ↓</a> · '
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps(dict(version=117,status='progress',new_dossiers=7,new_calendar_records=2,events=len(now),dossiers=len(cp['profiles']),budget_scenarios=27,goal='active')))
