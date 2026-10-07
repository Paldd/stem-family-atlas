"""Local reviewable delivery, source limits and retained worldwide objective."""
import collections,hashlib,json,re
from pypdf import PdfReader
from camp_nearby_v132 import ROOT,BASE,CHECKED,NEW,EVENT_IDS,POLICY,MEXPDF

P=ROOT.parent/'stem-family-atlas-work/nearby-latam-primary-v132'
d=json.loads((ROOT/'data/catalog.json').read_text())
profiles={p['slug']:p for p in d['camp_programmes']['profiles']}
sources=[]
for f in sorted(P.glob('receipt-*.json')):
    for original in json.loads(f.read_text()):
        q=dict(original,checked=CHECKED,retrieval_method='direct_public_http')
        if q.get('status')==200:
            filename=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
            body=(P/filename).read_bytes()
            assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
            q.update(raw_filename=filename,body_snapshot_retained=True,content_status='selected_pdf_clauses' if filename.endswith('.pdf') else 'selected_html_clauses')
            if q['key']=='liota-home':
                q['content_status']='javascript_shell_not_programme_clause_evidence'
                q['resolution']='Retained shell has no programme/age/price clauses; search snippet not promoted to a full current primary read.'
            elif q['key'] in ['cenfotec-courses','cenfotec-courses-page2','vex-mex-home']:
                q['content_status']='navigation_or_catalogue_discovery'
        else:
            q.update(body_snapshot_retained=False,content_status='retrieval_error_not_clause_evidence')
            q['resolution']='No challenge bypass. Existing Mexican Elementary event bodies remain inaccessible in this pass; related Middle/V5 cards do not verify Elementary places. Policy separately read through own primary reader. Three derived Academia STEM links returned 404.'
        sources.append(q)
assert len(sources)==22 and sum(q.get('status')==200 for q in sources)==14
reader=[dict(url=u,checked=CHECKED,retrieval_method='web_primary_page_reader',raw_body_snapshot_retained=False,
    content_scope=scope,limits='Selected public clauses; not live available places, authenticated application or full website audit.')
    for u,scope in [(next(e for e in d['events'] if e['id']==i)['source'],'Own Middle/V5 event category, date, venue, deadline, pricing conflict, notebook and invitation fields.') for i in EVENT_IDS]+[(POLICY,'June 1 season-end upper age caps, team counts and one-level rules; no lower age invented.')]]
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
plan=json.loads((ROOT/'data/research-plan.json').read_text())
publication=dict(plan['current_publication'],status='prepared_local_not_published',
    reason='Fresh native same-project get_site in v132 returned NOT_FOUND/project_not_found (404): Sites project not found. No source push, saved site version or deployment receipt for v132; no new project or old credentials used.',production_browser_qa=False)
blocks=collections.Counter(e['block'] for e in d['events'])
review=d['camp_programmes']['family_review']
newcamp=[e for e in d['events'] if e.get('camp_dossier_slug') in NEW]
ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text()
audit=dict(version=132,asof=CHECKED,status='progress',scope='Five selected Costa Rica/Mexico learning dossiers, one existing Makers dossier refreshed with general terms, four separately registered Mexican VEX categories; worldwide scope retained.',
    events=len(d['events']),competition_records=blocks['Соревнования'],event_records=blocks['События'],exhibition_records=blocks['События'],
    exhibition_records_unit='Mixed Events block, not a count of major company exhibitions.',camp_learning_records=blocks['Лагеря'],
    programme_dossiers=len(profiles),countries_with_dossiers=d['camp_programmes']['counts']['countries'],official_dossier_urls=d['camp_programmes']['counts']['source_urls'],
    editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=5,updated_existing_dossier_slugs=['cenfotec-makers'],new_dossier_operator_count=4,new_calendar_rows=5,new_competition_rows=4,new_dated_camp_rows=1,new_budget_scenarios=0,
    unchanged_dossiers=1078,unchanged_event_objects=3788,unchanged_budget_objects=55,dossier_ids=[profiles[s]['id'] for s in NEW],new_calendar_ids=EVENT_IDS+[e['id'] for e in newcamp],
    family_review_candidates=review['coverage']['candidates'],family_review_countries=review['coverage']['countries'],
    source_retrieval_attempts=len(sources),unique_requested_urls=len({q['url'] for q in sources}),direct_successful_retrievals=14,retrieval_errors=8,retained_body_receipts=14,
    javascript_shells_without_clauses=1,navigation_discovery_bodies=3,web_primary_clause_reads=len(reader),pdf_files=1,pdf_text_pages_extracted=len(PdfReader(P/'vex-season-pdf.pdf').pages),visual_pdf_pages_checked=[],
    family_ical=len(re.findall('BEGIN:VEVENT',ics)),new_family_ical_entries=8,old_family_ical_blocks_preserved=3001,senior_camp_rows_excluded_from_young_family_ical=1,
    exhibition_ical=104,league_profiles=len(d['league_guide']['profiles']),legacy_league_records=len(d['leagues']),new_competitive_league_profiles=0,
    goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert len(newcamp)==1 and audit['events']==3793 and audit['family_ical']==3009 and audit['pdf_text_pages_extracted']==3
for name in ['independent-check','functional-check']:
    if (P/(name+'.json')).exists():
        v=json.loads((P/(name+'.json')).read_text());assert v['status']=='passed' and v['version']==132;audit['verification'][name]=v
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('nearby-camps-audit-v132',audit)
write('nearby-camps-source-receipts-v132',dict(version=132,asof=CHECKED,sources=sources,web_primary_reader_sources=reader,external_actions=external,
    limits='22 direct requests,14 retained successful bodies,8 errors. One SPA shell has no programme clauses; three discovery pages are not full programme audits. Five additional own-page clause reads. One PDF,3 extracted text pages,0 visually checked. No full country audit or personal admission.'))
write('family-camp-selection-v132',review)
lines=['# Ближайшая база: Коста-Рика и Мексика · программы и отдельные категории VEX',
    'Локальная версия 132, проверка 6 октября 2026. По публичной ссылке эта версия ещё не опубликована: Sites сообщает «Sites project not found». Последняя подтверждённая опубликованная версия — 125.',
    'Добавлены пять досье четырёх операторов, уточнён один существующий курс и добавлены четыре отдельные категории VEX. В базе 1 084 досье в 39 странах, 58 вариантов семейного сравнения, 55 частичных смет. Это учебные треки, не число уникальных лагерей и не доказанный мировой рейтинг.',
    'Матвей 2017, Оскар 2020; EN/ES/RU. В 2026 им 8–9 и 5–6, в 2027 — 9–10 и 6–7 в зависимости от дня рождения. Возрастная рамка не подтверждает индивидуальное зачисление.',
    '## Что полезно семье сейчас',
    '- Curious Lab Minds в Heredia: регулярная робототехника с 3 лет, LEGO Education и полный учебный цикл от конструкции до испытания. Условный кандидат постоянной базы обоим; конкретная группа, язык, часы, fees и официальный соревновательный трек ещё требуют проверки.',
    '- Cerebritos в Playa del Carmen: клуб с известными вечерними часами и утренние mini camps на Semana Santa, в декабре и летом. Возраст, точные даты, язык и прайс неизвестны: запись с выдуманными каникулярными днями не создавалась.',
    '- Rocket Babies: короткие трёхчасовые workshops, CRC 33 000 с IVA, материалы/перекус/сертификат. Girls 6–13 в заголовке расходится с boys/girls в FAQ: для братьев приём пока неизвестен. Открытые CETAV workshops не равны школьным партнёрским программам.',
    '## Будущая CENFOTEC ступень',
    '- Makers Lab 10–12: прежние 7–11 декабря 2026 и L139 сохранены. Tuition с IVA USD 183.60, не вся поездка. Матвей в декабре ещё максимум 9; следующий набор после 10-летия не опубликован.',
    '- Explorador IA 14–16: 7–11 декабря 2026, 10:00–12:00, USD 122.40 с IVA. Creative generative AI и prompts, не подготовка к международному AI чемпионату. В общий каталог добавлена точная неделя, в семейный календарь младших она не попадает.',
    '- Ciberhéroes 13–15: цифровая безопасность/приватность и 10 часов. Страница печатает Monday 7 December без года, поэтому новой точной смены нет. Текущий tuition USD 122.40 не обозначен прайсом 2027.',
    '- Общие terms одновременно говорят о возврате до одного рабочего дня и семи дней до начала. Противоречие показано в досье; обещание безусловного refund не делается. Язык обучения трёх курсов явно не установлен.',
    '## Мексиканские категории отдельно от Elementary',
    '| Категория | Дата | Место | Важное условие |','|---|---|---|---|']
for ident in EVENT_IDS:
    e=next(e for e in d['events'] if e['id']==ident)
    lines.append('| ['+e['id']+' · '+e['title']+']('+e['source']+') | '+e['start']+' — '+e['end']+' | '+e['city']+' | '+e['cost']+' |')
lines += ['Отдельная категория имеет свой event code, robot/grade, состав и notebook. У Middle/V5 High опубликованы верхние пределы возраста на 1 июня 2027; нижний возраст из этих правил не выдуман. Персональный/местный допуск и готовность к задаче нужно согласовать. Основной общий старт братьев — прежде всего IQ Elementary, а не автоматический переход в новый Middle/V5 ряд.',
    'Связанные прежние Elementary C180/C513/C514/C597 сохранены, но три январско-мартовские карточки Elementary в этом проходе заново не прочитались. Другие grade categories не подтверждают их текущие места. Мексиканский PDF июня 2026 устанавливает сезон/порталы/VEX-ID, а не цену, Worlds квоту или зачисление семьи.',
    'Национальные карточки USD 0 одновременно обещают опубликовать fee на Academia STEM: ноль не полная цена. Chihuahua показывает Open Tournament вместе с Invitational, а Payment год 2026 в январских карточках расходится с датой 2027. Регистрационные дедлайны 12:00 EST переведены в 17:00 UTC / 11:00 Коста-Рика без переноса ошибочного Payment года.',
    '## Полные новые и обновлённые досье']
for slug in ['cenfotec-makers']+NEW:
    p=profiles[slug]
    lines += ['### '+p['id']+' · '+p['provider'],p['country']+' · '+p['place'],
        'Возраст: '+p['age'],'Язык: '+p['language'],'Содержание: '+p['programme'],'Даты: '+p['timing']['label'],
        'Цена: '+p['price']['label'],'Включено: '+p['price']['included'],'Доплаты: '+p['price']['extras'],'Оплата/возврат: '+p['price']['deposit'],
        'Матвей: '+p['family_fit']['matvey']['detail']+' Оскар: '+p['family_fit']['oscar']['detail'],
        'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])+'. [Досье в локальном сайте](../index.html?camp='+slug+'#camps).']
lines += ['## Проверка и границы',
    'Все 3 788 прежних событий, 1 078 не затронутых досье, 55 смет и 141 не затронутый профиль лиг/программ сохранены. Makers обновлён только выбранными terms/проверкой; VEX profile дополнен категориями. История школ/результатов, прежние маршруты и ближайший план v118 сохраняются. Истории призов Cerebritos без сезона/team ID не превращены в доказанные школьные победы.',
    'Семейный ICS — 3 009 записей: все 3 001 прежние VEVENT сохраняют байты; новые восемь — четыре категории и четыре регистрационных дедлайна. Календарь крупных выставок — прежние 104. Смешанный блок «События» содержит 196 записей; это не 196 крупных выставок.',
    '22 прямых запроса: 14 успешных сохранённых ответов / 8 ошибок. Один Liota JS shell без условий, три discovery страницы, пять дополнительных первичных web-reader прочтений. Один PDF: три страницы текста, визуального PDF-аудита нет. Это не 22 полностью изученных сайта. Сырые страницы и PDF находятся вне публичного сайта.',
    'Мировая цель активна: общие и тематические лагеря 2026–2027 EN/ES/RU, дневные/пансионные/семейные; соревнования, лиги, крупные выставки, постоянные школы, результаты 5–10 лет и инженерные/предпринимательские маршруты. Приоритет CHE/FRA/ESP/Европа, TWN/SGP/KOR/JPN, USA/CAN, CRI/MEX/Латинская Америка сохраняется. Полностью изученных стран — 0.']
(ROOT/'dist/downloads/STEM_ближайшие_программы_Коста_Рика_Мексика_v132.md').write_text('\n\n'.join(lines)+'\n')
if plan['latest_validation'].get('version')!=132:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v131:30dossiers,11calendar rows,independent/UIchecks,commit '+BASE+' and byte-verified local archive. Publication unavailable, useful primary research continues.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='5selected dossiers,1terms update,4Mexican VEX categories,58familychoices; prepared locally, not published.'
plan['nearby_camps_v132']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:
        q['evidence']='v132local:1084dossiers/39countries/1626dossierURLs;5selected CRI/MEX dossiers and1termsupdate;58familychoices/16countries,55partialbudgets. Regular learning/3h workshops/holiday curricula, age and language uncertainty distinct;0fullyauditedcountries,fullworldwidepriorityscopeactive.'
    elif q['id']=='unified_database':q['evidence']='v132local:3793events/1084dossiers/55partialbudgets in completeSQL/JSON. All3788old event objects preserved;4new VEX categories,1senior datedworkshop;1157competitionrecords,104major exhibition ICS. No push/save/deployment receipt.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=132]+[dict(version=132,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=5,new_calendar_rows=5,new_budget_scenarios=0,official_primary_retrieval_attempts=22,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=131','?v=132').replace('data-ui-version="131"','data-ui-version="132"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_ближайшие_программы_Коста_Рика_Мексика_v132.md" download>Ближайшая база · Коста-Рика и Мексика</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text().replace('downloads/STEM_лагеря_США_Канада_v131.md','downloads/STEM_ближайшие_программы_Коста_Рика_Мексика_v132.md');f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','status','events','programme_dossiers','family_review_candidates','family_ical','new_calendar_rows']}))
