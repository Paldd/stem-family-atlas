"""Reviewable selected primary evidence and local delivery, with world scope intact."""
import collections,hashlib,json,re
from pypdf import PdfReader
from camp_europe_v133 import ROOT,BASE,CHECKED,NEW,EVENT_ID,TOLEDO,COOLEST

P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v133'
d=json.loads((ROOT/'data/catalog.json').read_text());ps={p['slug']:p for p in d['camp_programmes']['profiles']}
sources=[]
discovery=['sanpatricio-home','codelearn-home','codelearn-camps','silc-fr-list','kids-es-funweeks']
for f in sorted(P.glob('receipt-*.json')):
    for original in json.loads(f.read_text()):
        q=dict(original,checked=CHECKED,retrieval_method='direct_public_http')
        if q.get('status')==200:
            filename=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html');body=(P/filename).read_bytes()
            assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
            q.update(raw_filename=filename,body_snapshot_retained=True,content_status='selected_pdf_clauses' if filename.endswith('.pdf') else 'selected_html_clauses')
            if q['key']=='sanpatricio-camps':q['content_status']='javascript_shell_without_programme_clauses';q['resolution']='Programme tabs separately read in live own page; HTTP shell is not clause evidence.'
            elif q['key']=='sanpatricio-bundle':q['content_status']='javascript_source_bundle_discovery_not_full_programme_read';q['resolution']='Generic demonstration programme objects are not published Toledo fees/ages. Live page tabs used; no remote code was executed in the repository.'
            elif q['key'] in discovery:q['content_status']='navigation_or_network_catalogue_discovery'
            elif q['key']=='sanpatricio-archive-pdf':q['content_status']='selected_historical_2024_pdf_clauses_not_current_2027_terms'
        else:q.update(body_snapshot_retained=False,content_status='retrieval_error_not_clause_evidence')
        sources.append(q)
assert len(sources)==25 and all(q.get('status')==200 for q in sources)
native=[dict(url=TOLEDO,checked=CHECKED,retrieval_method='native_browser_own_page',raw_browser_snapshot_retained=False,
    selected_panes=['Overview','Activities','Activities/Robotics','Fees & Add-ons','Stay','FAQs','Safety'],
    limits='Selected visible programme clauses; no Application/Staff audit, no live place confirmation or registration. Generic bundle demo cards not used.')]
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
plan=json.loads((ROOT/'data/research-plan.json').read_text())
publication=dict(plan['current_publication'],status='prepared_local_not_published',reason='Fresh native same-project get_site in v133 returned NOT_FOUND/project_not_found404: Sites project not found. No source push, saved site version or deployment receipt for v133; no new project or old credentials used.',production_browser_qa=False)
blocks=collections.Counter(e['block'] for e in d['events']);review=d['camp_programmes']['family_review'];ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text()
newcamp=[e for e in d['events'] if e.get('camp_dossier_slug') in NEW]
audit=dict(version=133,asof=CHECKED,status='progress',scope='14 selected programme dossiers from four operators in France/Spain,12 dated camp variants,one youth showcase visitor card,one partial budget; full worldwide objective retained.',
    events=len(d['events']),competition_records=blocks['Соревнования'],event_records=blocks['События'],exhibition_records=blocks['События'],exhibition_records_unit='Mixed Events block, not major company exhibition count.',camp_learning_records=blocks['Лагеря'],
    programme_dossiers=len(ps),countries_with_dossiers=d['camp_programmes']['counts']['countries'],official_dossier_urls=d['camp_programmes']['counts']['source_urls'],editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=14,new_dossier_operator_count=4,new_calendar_rows=13,new_dated_camp_rows=12,new_showcase_rows=1,new_competition_rows=0,new_budget_scenarios=1,unchanged_dossiers=1084,unchanged_event_objects=3793,unchanged_budget_objects=55,
    dossier_ids=[ps[s]['id'] for s in NEW],new_calendar_ids=[e['id'] for e in newcamp]+[EVENT_ID],
    family_review_candidates=review['coverage']['candidates'],family_review_countries=review['coverage']['countries'],source_retrieval_attempts=25,unique_requested_urls=len({s['url'] for s in sources}),direct_successful_retrievals=25,retrieval_errors=0,retained_body_receipts=25,
    javascript_shells_without_clauses=1,javascript_bundles_for_discovery=1,native_own_page_clause_reads=1,pdf_files=3,pdf_text_pages_extracted=sum(len(PdfReader(f).pages) for f in P.glob('*.pdf')),visual_pdf_pages_checked=['Mega2026filename:page1 grid STEAM/engineering/hours','Robotics2026filename:page1 grid language/robotics'],
    family_ical=ics.count('BEGIN:VEVENT'),new_family_ical_entries=13,old_family_ical_blocks_preserved=3009,exhibition_ical=104,league_profiles=len(d['league_guide']['profiles']),legacy_league_records=len(d['leagues']),new_competitive_league_profiles=0,updated_guide_profiles=['coolest'],
    goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert len(newcamp)==12 and audit['events']==3806 and audit['family_ical']==3022 and audit['pdf_text_pages_extracted']==11
for name in ['independent-check','functional-check']:
    f=P/(name+'.json')
    if f.exists():
        q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==133;audit['verification'][name]=q
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(body);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('europe-camps-audit-v133',audit)
write('europe-camps-source-receipts-v133',dict(version=133,asof=CHECKED,sources=sources,native_browser_sources=native,external_actions=external,
    limits='25 retained HTTP200 bodies include one SPA shell, one source bundle and catalogue/navigation pages. One own live page with selected tabs. Three PDFs11pages text extracted,2pages visually reviewed; historical2024brochure not current2027 evidence. No full website/country audit or personal admission. Raw pages/PDF remain private outside repo.'))
write('family-camp-selection-v133',review)
lines=['# Франция и Испания: ближайшие английские недели и будущие технические программы',
    'Локальная версия 133 · проверено 6 октября 2026. Эта версия ещё не опубликована: Sites возвращает «Sites project not found». Последняя подтверждённая публикация — 125.',
    'Добавлены 14 досье программ четырёх операторов, 12 датированных вариантов лагерей, одна карточка семейного посещения и одна частичная смета. Теперь в атласе 1 098 досье в 39 странах и 3 806 записей календаря/учебных направлений. Досье, варианты смен и независимые лагерные организации — разные единицы; это не мировой рейтинг.',
    'Матвей — 2017, Оскар — 2020; EN/ES/RU. В 2026 им 8–9 и 5–6, в 2027 — 9–10 и 6–7 в зависимости от дня рождения. Возрастная рамка не подтверждает зачисление.',
    '## Ближайшие недели английского',
    '| Место | Даты 2026 | Возраст и формат | Подтверждённая цена |','|---|---|---|---|',
    '| [Barcelona Eixample Dreta]('+ps[NEW[0]]['sources'][0]['url']+') | 26–30 октября | 3–10; часы центра уточнить | Не опубликована |',
    '| [Paris 5]('+ps[NEW[1]]['sources'][0]['url']+') | 19–23 и 26–30 октября | 3–10; есть половина/полный день, часы уточнить | Не опубликована |',
    '| [Paris 11]('+ps[NEW[2]]['sources'][0]['url']+') | 19–23 и 26–30 октября | Утро 3–10; полный день первой недели только 5–8 | Не опубликована |',
    '| [Angers Centre / Nord]('+ps[NEW[3]]['sources'][0]['url']+') | Centre 19–23; Nord 26–30 октября | Утро 3–10; полный Centre 5–10, своя еда | Не опубликована |',
    '| [Rueil-Malmaison]('+ps[NEW[4]]['sources'][0]['url']+') | 19–23 октября | 3–12, English 09–13 | €285 / ребёнок / неделю |',
    'FunWeeks — общие английские программы с играми, историями и творчеством. Приём неучеников опубликован, но это ещё не подтверждение места для приезжей семьи. В Paris 11 Матвей подходит к полному дню только пока ему 8; в 9 лет остаётся утро 3–10. Вторую неделю полного дня центр не обещает.',
    'Rueil: €285 × 2 = €570 только за English mornings. Полный день English + AMK’ART стоит €495 за ребёнка плюс €30/week материалов с неясной единицей начисления. Язык ART не установлен. Смета €570 не включает жильё, дорогу, питание и непроверенные доплаты; аванс/возврат неизвестны.',
    '## Техническая Испания и пансион во Франции',
    '- Codelearn: отдельные syllabus для создания игр/роботов, Futbots Robobol и Godot/GDScript. Название Campus «6–7» — мем, а не возраст 6–7. Общая сеть пишет 7–18, но возраст каждого курса, язык, даты и цена ещё нужны. Декабрьские 22–24 и February tournament не содержат года: точные смены не созданы.',
    '- San Patricio Toledo: Main Robotics & Computing 10–16 с EN/ES, Godot, MakeCode Arcade, microcontrollers/sensors и 3D. Есть дневной и пансионный форматы. Mega 6–9 — общая программа; приложенный timetable показывает один час STEAM во вторник и один час engineering в четверг. Это короткое знакомство, не полный robotics intensive.',
    '- Mega timetable: arrival 08:45, programme 09–16; общий Main FAQ 09–19 сюда не перенесён. Fees Mega €280 за одну неделю; при 2/3/4 неделях €275/270/265 за каждую неделю. Overview связывает €265 с half-day, Fees — с четырьмя неделями: договор должен разрешить расхождение.',
    '- Toledo title 2026/2027 не подтверждает смены 2027: body без года, linked filenames timetables прямо 2026. Main €1180 day / €1925 boarding за две недели в таблице, но pathway day range €1180–1700: конкретный robotics invoice ещё нужен. Transfer Madrid €380 return / €200 one-way; accident/liability cover не personal health/travel insurance.',
    '- SILC Normandy: собственная вариация 18–23 июля 2027, 10–15, English activities, full board и сопровождаемый поезд из Paris, €1150. Онлайн-покупка недоступна; причина неизвестна. Матвей только после 10-летия, Оскар младше. Programme и детские CPV 2026 расходятся о включении €100 dossier; новый договор 2027 ещё нужен.',
    '- SILC One-to-One: 10–17, English A1/A2, 10 частных уроков по 55 минут в неделю, full-board homestay у англоязычной семьи во Франции. Нужна самостоятельность в свободное время; это не школьный пансион или непрерывная 24/7 лагерная программа. От €1130/week без подтверждённого года прайса; доступных точных недель нет.',
    '## Семейный технологический ивент',
    '[Coolest Projects Spain в Gavà]('+COOLEST+') — 24 октября 2026, La Casa Gran, 09–14; семьи посещают стенды 11:30–13:30. Посещение и подача проектов бесплатны. Для проектов возраст 12–18, срок подачи 8 октября; братья младше и этот срок к ним как посетителям не относится. Допуск младших посетителей уточнить отдельно.',
    'Жюри выдаёт тематические упоминания, участникам — дипломы и Raspberry Pi Pico kit; предусмотрен розыгрыш. Это признание проектов в местном showcase, не титул чемпиона мира и не крупная выставка всех технологических компаний. Посетитель не получает автоматически подарки участников.',
    '## Полные новые досье']
for slug in NEW:
    p=ps[slug]
    lines+=['### '+p['id']+' · '+p['provider'],p['country']+' · '+p['place'],
        'Возраст: '+p['age'],'Язык: '+p['language'],'Программа: '+p['programme'],'Когда: '+p['timing']['label'],
        'Стоимость: '+p['price']['label'],'Включено: '+p['price']['included'],'Доплаты: '+p['price']['extras'],'Оплата/возврат: '+p['price']['deposit'],
        'Проживание: '+p['accommodation'],'Матвей: '+p['family_fit']['matvey']['detail']+' Оскар: '+p['family_fit']['oscar']['detail'],
        'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])+'. [Открыть досье в локальном сайте](../index.html?camp='+slug+'#camps).']
    for v in p['timing'].get('session_details',[]):
        text=v['label']+' · '+v['start']+' — '+v['end']+' · '+v['price']
        if v.get('family_fit'):text+=' Матвей: '+v['family_fit']['matvey']['detail']+' Оскар: '+v['family_fit']['oscar']['detail']
        lines.append(text)
lines+=['## Проверка и границы',
    'Сохранены все 3 793 прежних события, 1 084 досье, 55 прежних смет, школы, история результатов, инженерные маршруты и семейная стратегия. Дополнен только существующий обзор Coolest Projects отдельной испанской редакцией. Остальные 141 профиль лиг/программ сохранены.',
    'Семейный ICS — 3 022 записи: 3 009 прежних VEVENT сохранены побайтно; 12 новых датированных вариантов и одно семейное посещение добавлены. 104 записи календаря крупных выставок прежние. Блок «События» содержит 197 смешанных ивентов, а не 197 крупных выставок.',
    '25 прямых HTTP-запросов сохранили ответы: среди них JS shell без условий, JS bundle для навигации и общие catalogue pages. У Toledo выбраны видимые tabs; демонстрационные объекты bundle не стали прайсом лагеря. Три PDF, 11 страниц извлечённого текста, две страницы расписаний визуально проверены. Старый brochure 2024 не договор 2027. Это не 25 полностью изученных сайтов.',
    'Мировая цель остаётся активной: все общие и тематические лагеря 2026–2027 EN/ES/RU, дневные/пансионные/семейные; соревнования, лиги, крупные выставки, постоянные школы, результаты за 5–10 лет и инженерные/предпринимательские маршруты. Приоритет CHE/FRA/ESP/Europe, TWN/SGP/KOR/JPN, USA/CAN, CRI/MEX/Латинская Америка сохраняется. Полностью изученных стран — 0.']
(ROOT/'dist/downloads/STEM_лагеря_Франция_Испания_v133.md').write_text('\n\n'.join(lines)+'\n')
if plan['latest_validation'].get('version')!=133:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v132:5dossiers,4VEXcategories,independent/UIchecks,commit '+BASE+' and byte-verified local archive. Primary worldwide research continues despite hosting outage.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='14 selected dossiers,12datedcampvariants,1visitorcard,1budget and62familychoices; prepared locally, not published.'
plan['europe_camps_v133']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:q['evidence']='v133local:1098dossiers/39countries/1642dossierURLs,14selectedFranceSpaindossiers;62familychoices/16countries,56partialbudgets. CurrentEnglishweeks,age-specificfull-day,Englishmorning-onlyart,ambiguousToledo2027andNormandyunavailableonlineexplicit.0fullyauditedcountries;fullworldscopeactive.'
    elif q['id']=='unified_database':q['evidence']='v133local:3806events/1098dossiers/56partialbudgets in fullSQL/JSON.3793old event objects preserved;12newcampvariants and1visitorcard;104major exhibition ICS. No push/save/deployment receipt.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=133]+[dict(version=133,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=14,new_calendar_rows=13,new_budget_scenarios=1,official_primary_retrieval_attempts=25,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=132','?v=133').replace('data-ui-version="132"','data-ui-version="133"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_лагеря_Франция_Испания_v133.md" download>Франция и Испания · ближайшие недели и будущие программы</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text().replace('downloads/STEM_ближайшие_программы_Коста_Рика_Мексика_v132.md','downloads/STEM_лагеря_Франция_Испания_v133.md');f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','family_review_candidates','family_ical','new_calendar_rows','goal']}))
