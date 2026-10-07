"""Reviewable local North American delivery, source receipts and retained scope."""
import collections, hashlib, json
from urllib.parse import urldefrag
from pypdf import PdfReader
from camp_northamerica_v131 import ROOT, BASE, CHECKED, NEW, EVENT_IDS, PROFILE_ID, HELP, RES

P=ROOT.parent/'stem-family-atlas-work/camp-northamerica-primary-v131'
d=json.loads((ROOT/'data/catalog.json').read_text())
profiles={p['slug']:p for p in d['camp_programmes']['profiles']}
sources=[]
shells={'id-age','id-groups','id-english'}
discovery={'carleton-home','carleton-events','carleton-clubs','stemminds-camps','stemminds-programs'}
for f in sorted(P.glob('receipt-*.json')):
    for original in json.loads(f.read_text()):
        q=dict(original,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected programme/price/grade/contract clauses or source discovery; not a full website audit.')
        if q.get('status')==200:
            filename=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
            body=(P/filename).read_bytes()
            assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
            q.update(raw_filename=filename,body_snapshot_retained=True)
            q['content_status']='selected_pdf_clauses' if filename.endswith('.pdf') else 'selected_html_clauses'
            if q['key'] in shells:
                assert not (P/(q['key']+'.txt')).read_text().strip()
                q['content_status']='javascript_shell_not_programme_clause_evidence'
                q['resolution']='Clauses separately read with web primary-page reader; retained HTTP shell does not contain those clauses.'
            elif q['key']=='tech-details':
                q['content_status']='same_page_fragment_discovery_duplicate'
                q['resolution']='Own #details anchor retrieves the same camp page, not another independently read site.'
            elif q['key'] in discovery:
                q['content_status']='navigation_or_archive_discovery'
        else:
            q.update(body_snapshot_retained=False,content_status='retrieval_error_not_clause_evidence')
            q['resolution']='HTTP 403 retained as a retrieval limitation, without challenge bypass. Toronto residence separately read in own web-reader; STEM Camp and weekend pages do not establish verified programmes.'
        sources.append(q)
assert len(sources)==35 and sum(q.get('status')==200 for q in sources)==31
reader_sources=[dict(url=url,checked=CHECKED,retrieval_method='web_primary_page_reader',raw_body_snapshot_retained=False,
    content_scope=content,limits='Read own-page clauses; not authenticated admission, form submission or full website audit.') for url,content in [
    (RES,'Residence archive2026 price/deposit/room/meals/English/airport/cancellation.'),
    (HELP+'do-you-accept-international-students','Foreign students welcome; all courses English, basic reading/speaking/listening. No visa claim adopted.'),
    (HELP+'can-you-make-an-age-exception','General MINIMUM by December31; certain courses stricter, exceptions case-specific. No maximum cut-off inferred.'),
    (HELP+'are-your-camps-segmented-by-age-21-8-2018','7–9/10–12/13–17 age bands; general minimum policy, mixed lab cohorts possible.')]]
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
publication=dict(status='prepared_local_not_published',project_id='appgprj_6abd44bca1348191809b7260dcb46d87',
    reason='Fresh native same-project get_site in v131 returned NOT_FOUND/project_not_found: Sites project not found. Versions126–131 have no source-push/save/deployment receipt; no older credential or new site used.',
    last_confirmed_published_version=125,last_confirmed_deployment_id='appgdep_6ac4ff3f3c7481918fe3d668d24574b0',last_confirmed_success_at='2026-10-06T14:02:09.803197+00:00',production_browser_qa=False)
blocks=collections.Counter(e['block'] for e in d['events'])
review=d['camp_programmes']['family_review']
newcamp=[e for e in d['events'] if e.get('camp_dossier_slug') in NEW]
audit=dict(version=131,asof=CHECKED,status='progress',scope='30selected USA/Canada course dossiers across six operators, seven regional Tech project/Q&A/milestone events and one explicitly non-competitive programme profile. Worldwide priority scope preserved.',
    events=len(d['events']),competition_records=blocks['Соревнования'],event_records=blocks['События'],exhibition_records=blocks['События'],
    exhibition_records_unit='All records in mixed Events block; not196major company exhibitions.',camp_learning_records=blocks['Лагеря'],
    programme_dossiers=len(profiles),countries_with_dossiers=39,official_dossier_urls=d['camp_programmes']['counts']['source_urls'],editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=30,new_calendar_rows=len(newcamp)+len(EVENT_IDS),new_dated_camp_rows=len(newcamp),new_noncompetitive_event_rows=len(EVENT_IDS),new_budget_scenarios=0,
    unchanged_dossiers=1049,unchanged_event_objects=3777,unchanged_budget_objects=55,new_profile_id=PROFILE_ID,new_competitive_league_profiles=0,
    dossier_ids=[profiles[s]['id'] for s in NEW],new_calendar_ids=[e['id'] for e in newcamp]+EVENT_IDS,
    family_review_candidates=57,family_review_countries=16,operators_represented_in_new_dossiers=6,new_dossiers_are_not_unique_operator_count=True,
    source_retrieval_attempts=35,unique_requested_urls=len({q['url'] for q in sources}),unique_page_urls_without_fragment=len({urldefrag(q['url'])[0] for q in sources}),
    direct_successful_retrievals=31,retrieval_errors=4,retained_body_receipts=31,javascript_shells_without_clauses=3,same_page_fragment_duplicates=1,
    web_primary_clause_reads=4,pdf_files=2,pdf_text_pages_extracted=sum(len(PdfReader(f).pages) for f in P.glob('*.pdf')),
    visual_pdf_pages_checked=['Tech rules page10: challenge explicitly not competition','Tech rules page6: device and player area geometry'],
    family_ical=3001,new_family_ical_entries=8,old_family_ical_blocks_preserved=2993,
    senior_grade_camp_rows_excluded_from_young_family_ical=4,exhibition_ical=104,league_profiles=142,league_profiles_unit='League-and-programme profiles, including new non-competitive regional programme.',legacy_league_records=46,
    goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert len(newcamp)==4 and audit['pdf_text_pages_extracted']==14
for name in ['independent-check','functional-check']:
    if (P/(name+'.json')).exists():
        v=json.loads((P/(name+'.json')).read_text());assert v['status']=='passed' and v['version']==131;audit['verification'][name]=v
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(body)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('northamerica-camps-audit-v131',audit)
write('northamerica-camps-source-receipts-v131',dict(version=131,asof=CHECKED,sources=sources,web_primary_reader_sources=reader_sources,external_actions=external,
    pdf_text_pages_extracted=14,visual_pdf_pages_checked=audit['visual_pdf_pages_checked'],
    limits='35direct attempts/31retainedHTTP200 bodies/4errors;3retained JS shells have no programme text, one #details anchor is same-page duplicate. Four own-page web-reader clause reads,2PDFs14textpages/2visuallycheckedpages. Selected clauses, not35fullyauditedsites. No country complete, independent quality ranking or personal admission certified.'))
write('family-camp-selection-v131',review)
lines=['# Лагеря США и Канады: программы, классы и маршрут 2026–2027',
    'Подготовлено локально 6 октября 2026, версия 131. Публикация не выполнена: свежая проверка Sites сообщает «Sites project not found». Последняя подтверждённая опубликованная версия — 125.',
    'Добавлены 30 досье учебных треков шести операторов и семь событий отдельной инженерной программы The Tech Challenge. В базе теперь 1 079 досье в 39 странах, 57 вариантов семейного сравнения и 55 частичных смет. Это число программ, не уникальных лагерей и не мировой рейтинг.',
    'Матвей 2017, Оскар 2020; английский, испанский и русский. В 2027 им 9–10 и 6–7. Предварительная совместимость по возрасту или классу не подтверждает персональное зачисление.',
    '## Что меняет выбор для братьев',
    '- iD Tech: Junior 7–9 использует VEX IQ и block coding; курс 10–12 использует VEX V5; отдельный 3D printing курс обещает take-home робот. Английский и приём иностранных учеников подтверждены. Общий минимум возраста — к 31 декабря, но отдельный курс может быть строже. Это потенциальный путь Оскара летом 2027 и Матвея к V5, требующий проверки конкретного курса.',
    '- У Junior верхняя граница Матвея ещё требует собственной контрольной даты: правило minimum by December 31 не устанавливает maximum. Junior — дневной формат; общий boarding минимум 10 лет. Опубликованные starting prices и deposit не заменяют полный счёт выбранного campus 2027.',
    '- Toronto Jr. DEEP: семь смешанных учебных курсов, от Robotics at Work до AI & Autonomous Systems, разделены по завершённым 3–4, 5–6 и 7–8 классам. Это архив 2026; английский преподавания junior ещё не доказан.',
    '- Carleton Virtual Ventures: общий STEM, game design, programming с robotics/electronics и инженерия полностью без компьютеров. Здесь используют класс, завершённый в июне; у McMaster Fireball/Flare — класс следующей осени. Опыт соревнований не заменяет школьный минимум.',
    '- Toronto DEEP senior уже объявляет 5–9, 12–16, 19–23 и 26–30 июля 2027. Это 9–12 классы, будущая ступень. Tuition и пансион на прочитанных страницах относятся к 2026. Четыре академические недели есть в базе, но исключены из календаря нынешнего возраста братьев.',
    '- STEM Minds сейчас пишет Camps on Pause. Старые продукты сохранены как архив с явной паузой; их нет в семейной рекомендации или будущем календаре.',
    '- The Tech Interactive объявил CAMP Summer 2027 для incoming Grades 2–6: музей, инженерный дизайн и совместные проекты. Точных недель, цены и подтверждённого языка преподавания ещё нет. Семейный визит в музей и допуск в лагерь — разные условия.',
    '## The Tech Challenge 2027: проектная программа',
    'Собственный English rules v3 прямо определяет challenge как программу, не competition. Это физическая игра, инженерный журнал и обратная связь; международная медаль или выход в мировые лиги не обещаны.',
    'Команда 2–6 учеников 4–12 классов и взрослый adviser, division по старшему классу. Grade 3 прямо исключён. Матвею нужен реальный Grade 4; Оскар может быть семейным зрителем. Условия билета/резерва для зрителей пока неизвестны.',
    'Showcase 30 апреля или 1 мая 2027 в The Tech Interactive, San Jose: команда выбирает один день и отдельный слот, без дополнительного showcase team fee. FAQ объявляет открытие регистрации 6 октября 2026; actual form/account не проверялись. Early fee $150 за команду до 31 декабря, затем $300. 31 декабря — граница цены, не окончательный дедлайн регистрации.',
    'Q&A для prospective родителей/advisers: 20 октября, 3 и 18 ноября, 1 и 16 декабря 2026. Время на сайте 17:00 либо 19:00 без timezone; в семейном календаре только день. Январь/февраль открытия Test Trials регистрации расходятся между events и FAQ.',
    'Rules на английском опубликованы; ES/Vietnamese обозначены coming soon. Другой язык интервью согласуют заранее. Это не гарантия испанского судейства. Purchased parts допускаются, purchased kits запрещены; работа проекта должна принадлежать детям.',
    'Источники: [программа 2027](https://www.thetech.org/education/tech-challenge/tech-challenge-2027/), [FAQ](https://www.thetech.org/education/tech-challenge/tech-challenge-2027/faq/), [встречи и trials](https://www.thetech.org/education/tech-challenge/tech-challenge-2027/participant-events/), [English rules v3](https://www.thetech.org/media/42yd5cg2/ttc27_rules_english_v3.pdf).',
    '## Новые подробные досье']
for iso in ['CAN','USA']:
    pp=[profiles[s] for s in NEW if profiles[s]['iso']==iso]
    lines+=['### '+pp[0]['country']]
    for p in pp:
        lines += ['**'+p['id']+' · '+p['provider']+'**',
            'Возраст/класс: '+p['age']+' Язык: '+p['language'],
            'Программа: '+p['programme'],'Когда: '+p['timing']['label'],
            'Цена: '+p['price']['label'],'Включено: '+p['price']['included']+' Доплаты: '+p['price']['extras'],
            'Оплата/отмена: '+p['price']['deposit'],'Проживание: '+p['accommodation'],
            'Матвей: '+p['family_fit']['matvey']['detail']+' Оскар: '+p['family_fit']['oscar']['detail'],
            'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])+'. [Досье в локальном сайте](../index.html?camp='+p['slug']+'#camps).']
lines+=['## Пробелы и границы',*['- '+g['provider']+': '+g['detail'] for g in d['camp_programmes']['gaps'][-8:]],
    '35 прямых запросов: 31 успешный ответ сохранён, четыре 403. Три HTML ответа help centre — пустые JS shells; английский и minimum clauses прочитаны отдельно первичным web-reader. Один #details URL повторяет страницу лагеря. Из двух PDF извлечён текст 14 страниц; визуально проверены две страницы. Это не 35 полностью изученных сайтов.',
    'Все 3 777 прежних событий, 1 049 прежних досье, 55 смет и 141 профиль лиг/программ сохраняются. Добавлены четыре академические недели старшей школы и семь событий The Tech. Конкурентных лиг и соревнований в этом проходе не добавляли: их счётчик не увеличен за счёт проекта или Q&A.',
    'Семейный ICS: 3 001 записи, все 2 993 прежних VEVENT сохраняют исходные байты. Восемь новых — семь событий The Tech и срок ранней цены; старшая DEEP исключена по возрасту. Календарь крупных выставок прежний: 104 записи. Сырые страницы, PDF и browser snapshots находятся вне публичного сайта.',
    'Мировая цель активна: общие и тематические лагеря 2026–2027 на EN/ES/RU, дневные/пансионные/семейные; соревнования, лиги, крупные выставки, постоянные школы, результаты 5–10 лет, инженерные и предпринимательские маршруты. Приоритет CHE/FRA/ESP/Европа, TWN/SGP/KOR/JPN, USA/CAN, CRI/MEX/Латинская Америка сохраняется. Полностью изученных стран — 0.']
(ROOT/'dist/downloads/STEM_лагеря_США_Канада_v131.md').write_text('\n\n'.join(lines)+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=131:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v130:15verified local dossiers,2datedrows,2partial budgets,50familychoices,independent/UIchecks,commit '+BASE+' and byte-verified local archive. Publication unavailable, meaningful primary research continues.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='30selected course dossiers,11datedrows,57familychoices; Tech programme explicitly non-competitive; prepared locally, not published.'
plan['northamerica_camps_v131']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:
        q['evidence']='v131local:1079dossiers/39countries/1618dossierURLs;30selectedcourse dossiers across6USA/CANoperators;57familychoices/16countries,55partialbudgets. Grade/age/currency/teaching/contract years distinguished;0fullyauditedcountries,fullworldwidepriorityscopeactive.'
    elif q['id']=='unified_database':q['evidence']='v131local:3788events/1079dossiers/55partialbudgets in completeSQL/JSON;all3777old events/1049oldprofiles preserved. Tech project events in Events, competitioncount1153 unchanged. No push/save/deployment receipt.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=131]+[dict(version=131,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=30,new_calendar_rows=11,new_budget_scenarios=0,official_primary_retrieval_attempts=35,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=130','?v=131').replace('data-ui-version="130"','data-ui-version="131"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_лагеря_США_Канада_v131.md" download>Лагеря · США и Канада · классы и программы</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text().replace('downloads/STEM_лагеря_Европа_Канада_v130.md','downloads/STEM_лагеря_США_Канада_v131.md')
if "E(p.availability?.label||" not in s:s=s.replace("E(p.availability?.status==='closed'?", "E(p.availability?.label||p.availability?.status==='closed'?")
# Parenthesise the fallback so a custom label is rendered rather than treated as a boolean.
s=s.replace("E(p.availability?.label||p.availability?.status==='closed'?'Набор закрыт':p.availability?.status==='not_open_yet'?'Набор ещё не открыт':p.availability?.status==='waitlist'?'Лист ожидания':statusLabels[p.timing.status])", "E(p.availability?.label||(p.availability?.status==='closed'?'Набор закрыт':p.availability?.status==='not_open_yet'?'Набор ещё не открыт':p.availability?.status==='waitlist'?'Лист ожидания':statusLabels[p.timing.status]))")
f.write_text(s)
print(json.dumps(dict(version=131,status='progress',new_dossiers=30,new_calendar_rows=11,family_review=57,source_attempts=35,publication=publication['status'])))
