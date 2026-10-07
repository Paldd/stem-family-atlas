"""Record a bounded primary-source increment while retaining the global goal."""
import collections,hashlib,json,re
from nearby_robotics_v135 import ROOT,BASE,CHECKED,NEW_IDS,RL_IDS,GUIDES,GOV,RL,GENERAL,PARADE,RUBRIC,DRONE,FOOTBALL,BAJA,ARMADO,SUMO,MAKER

P=ROOT.parent/'stem-family-atlas-work/robotics-nearby-primary-v135'
d=json.loads((ROOT/'data/catalog.json').read_text());ev={e['id']:e for e in d['events']}
plan=json.loads((ROOT/'data/research-plan.json').read_text())
sources=[]
shells={'baja-home','bebras-home','bebras-agenda'}
public_json={'maker-workshops-public-json','bebras-agenda-public-api','bebras-home-public-api','bebras-rules-public-api'}
for name in ['receipt.json','extra-receipt.json','manuals-receipt.json','rules-receipt.json']:
    for r in json.loads((P/name).read_text()):
        q=dict(r,retrieval_method='direct_public_http',body_snapshot_retained=bool(r.get('raw_filename')))
        if q.get('raw_filename'):
            body=(P/q['raw_filename']).read_bytes();assert len(body)==q['bytes'] and hashlib.sha256(body).hexdigest()==q['sha256']
        q['content_status']='selected_primary_clauses_not_complete_site_audit'
        if q['key'] in shells:q['content_status']='javascript_shell_no_programme_clauses'
        elif q['key']=='maker-workshops':q['content_status']='dynamic_workshop_page_navigation_and_observed_public_catalog_endpoint'
        elif q['key'] in public_json:q['content_status']='public_json_used_by_own_page_selected_programme_fields'
        elif q['key'].endswith('public-bundle'):q['content_status']='public_source_bundle_read_for_document_links_or_read_api_no_execution_or_secret_config'
        elif q['key'] in ['first-mx-faq','first-k8-recheck','fmr-calendar','maker-ajolote']:q['content_status']='existing_source_recheck_no_duplicate_calendar_card'
        elif q['key']=='rl-about':q['content_status']='older_unspecified_edition_not_2026_venue'
        elif q['key']=='rl-host-bulletin':q['content_status']='http404_error_body_not_venue_evidence'
        elif q.get('error'):q['content_status']='retrieval_failed_no_direct_programme_body'
        sources.append(q)
assert len(sources)==30
reader=json.loads((P/'primary-reader-observations.json').read_text())
native=json.loads((P/'native-site-check.json').read_text());assert native['isError'] and native['structuredContent']['error_data']['code']==404
publication=dict(plan['current_publication'],status='prepared_local_not_published',reason='Fresh v135 native get_site for manifest project returned NOT_FOUND/project_not_found404. No source push, saved version or deployment; existing project/audience retained.',production_browser_qa=False)
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(e['block'] for e in d['events']);ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text()
audit=dict(version=135,asof=CHECKED,status='progress',scope='Exact host-announced TMR2027 dates, current Bebras grade/deadline discrepancy, ten RobofestLATAM discipline watches, two BajaBot grade scenarios and nine FeriaMaker workshops. Worldwide scope retained.',
    events=len(ev),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],event_records=blocks['События'],exhibition_records_unit='Mixed Events block, not number of major world company exhibitions.',camp_learning_records=blocks['Лагеря'],
    programme_dossiers=d['camp_programmes']['counts']['dossiers'],countries_with_dossiers=d['camp_programmes']['counts']['countries'],official_dossier_urls=d['camp_programmes']['counts']['source_urls'],editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=0,new_calendar_rows=len(NEW_IDS),new_competition_rows=11,new_event_rows=10,new_dated_workshop_windows=8,new_undated_rule_watches=12,new_undated_workshop_rows=1,
    updated_event_ids=['C043','C064'],unchanged_event_objects=3806,new_calendar_ids=NEW_IDS,
    unchanged_dossiers=1102,unchanged_budget_objects=57,unchanged_family_review_candidates=64,family_review_countries=16,
    league_profiles=len(d['league_guide']['profiles']),new_league_profiles=GUIDES,updated_guide_ids=['tmr','robofest'],unchanged_guide_profiles=140,
    source_retrieval_attempts=len(sources),direct_http200_bodies=sum(q.get('status')==200 for q in sources),http_error_bodies=sum(bool(q.get('raw_filename')) and q.get('status')!=200 for q in sources),
    direct_timeouts=sum('timed out' in q.get('error','') for q in sources),retained_body_receipts=sum(q['body_snapshot_retained'] for q in sources),
    pdf_files=sum(bool(q.get('pdf_pages')) for q in sources),pdf_pages_retained=sum(q.get('pdf_pages',0) for q in sources),presentation_files=1,presentation_slides_retained=16,
    source_limits='Seven PDF files/80pages and one16slide presentation retained; selected age/team/hardware/awards clauses read. Not80 independently audited pages or30 complete organiser sites. Two TMR timeouts supplemented by full web primary reader; Pachuca bulletin404. Three HTML JS shells not programme evidence. Public JSON is served content, not live acceptance/availability.',
    family_ical=ics.count('BEGIN:VEVENT'),new_family_ical_entries=8,old_family_ical_blocks_byte_identical=3023,old_bebras_ical_blocks_updated_check_date=2,exhibition_ical=104,
    mobile_qa=False,production_browser_qa=False,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert len(ev)==3829 and audit['family_ical']==3033 and blocks==dict(Соревнования=1168,События=207,Лагеря=2454)
for name in ['independent-check','functional-check']:
    f=P/(name+'.json')
    if f.exists():
        q=json.loads(f.read_text());assert q['version']==135 and q['status']=='passed';audit['verification'][name]=q
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(body);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('nearby-robotics-audit-v135',audit)
write('nearby-robotics-source-receipts-v135',dict(version=135,asof=CHECKED,sources=sources,primary_reader_observations=reader,external_actions=external,limits=audit['source_limits'],raw_evidence_in_repository=False))
f=ROOT/'dist/downloads/STEM_соревнования_Мексика_мастерские_v135.md'
lines=['# Мексика и Коста-Рика: младшие дисциплины, точные даты и ближайшие мастерские',
    'Локальная версия135 · проверено6 октября2026. Новая редакция не опубликована: сервис Sites возвращает «Sites project not found». Последняя подтверждённая публикация125; существующий сайт и его аудитория сохранены.',
    'Добавлены21 карточка:11 соревновательных дисциплин и10 учебных/посещаемых событий. Из них12 вариантов без нового календаря,8 окон мастерских с датой и1 короткая мастерская без дня. Обновлены две прежние записи. Всего3 829 записей,144 профиля лиг/программ; лагеря1 102 досье/39 стран и57 частичных смет прежние. Эти количества не мировой рейтинг и не число уникальных организаторов.',
    'Матвей2017 / Оскар2020: в2027 возраст9–10 /6–7 в зависимости от дня рождения. Школьный класс, редакция сезона и реальная самостоятельность важнее соответствия цифре6/9.',
    '## Что сделать семье первым',d['family_strategy']['nearby_participation_v135']['conclusion'],
    '**Bebras Costa Rica:** срок16 октября, тест9–13 ноября,45 минут в школе. На отображённой главной есть Pre-Ecolier2.º; собственный регламент требует3–6 классы и школуCosta Rica. Перепроверка не разрешила расхождение. Для Матвея — подтвердить класс и регистрацию школы; для Оскара1-й класс регламентом не разрешён,2-й требует разъяснения. [Agenda](https://cangurocr.org/bebras/agenda),[правила](https://cangurocr.org/bebras/reglamento),[главная](https://cangurocr.org/bebras/).',
    '**TMR2027:**3–6 марта,Palacio de Convenciones,Zacatecas. Это точные дни из [объявления принимающей стороны]('+GOV+') от18 июня2026, согласованные по месяцу с[FMR](https://femexrobotica.org/fmr/eventos/). Детские категории, cutoff, deadline, fees и отбор пока неизвестны.23 категории/300 команд/1200 участников — прогноз, не протокол.',
    '## Robofest LATAM: локальные правила не равны LTU World2027',
    'Прочитанный [General PDF2026]('+GENERAL+') даёт Junior6–14 для Game/Exhibition,BottleSumo,UMC,RoboArts,RoboMed. [Overview]('+RL+'desafios) задаёт grade5–8. Файл смешивает footer2025 и положения2026. Новый LATAM2027 не объявлен: прошлые20–21 марта2026 не превращены в даты2027. Grade/age конфликт требует новой редакции и ответа организатора.',
    '| Дисциплина2026 | Команда | Для братьев / ограничения |\n|---|---|---|\n| Game / Exhibition | до5 + coach | Условный local6–14; автономный собственный проект, unknown factors |\n| BottleSumo Junior | до3 + coach | LEGO NXT/EV3/SPIKE/RobotInventor илиVEX IQ; неRC сумо |\n| UMC Junior | до4 + coach | Те же kit рамки; полностью неизвестная задача |\n| RoboArts / RoboMed Junior | до5 + coach | Собственный проект и отдельная защита; не автоматический World |\n| RoboParade |1–5 + coach | Local6–14; подходит для подготовки обоих после проверки следующего сезона |\n| DronesW193 |1–2 + coach | PDF9–14, HTML10–12; для Матвея допуск неоднозначен, Оскар младше обеих групп |\n| Football3v3W193 | до6 по формулировке PDF + coach18+ | Junior8–14; Матвей условно, Оскар младше; три собственных робота |\n| VCC | до5 + coach | Senior15–19; будущая ступень |',
    'RoboParade имеет реальную [рубрику]('+RUBRIC+'): самостоятельность10%, teamwork10%, объяснение скорости7%, математика3%, плюс тест/дизайн/парад. Solo разрешён, но teamwork получает1–2 из5. [Презентация]('+PARADE+') требует автономной линии в обе стороны, остановки перед соседом и показанной скорости7–16 см/с. У LTU World2027 отдельный Explorer1–4 классы и темаFun and Games; локальные правила2026 не заменяют его правила.',
    'В [дроновом PDF]('+DRONE+') и [футболе]('+FOOTBALL+') мировой путь названW193,HongKongJuly2026. Это прошлое локальное заявление, внешний допуск/квоты не проверены. У дронов конфликт возрастов и неполные правила числа команд; у футбола формулировка двух первых мест одновременно перечисляет1/2/3. Не смешивать сLTU.',
    'Старый localGeneralp31–35 допускает при<3 команд аккредитацию от80% без призового места, отдельно национальные квоты иUSD100+10 за прошлое мировое оформление. USD90 вp27 — US local, неMexico fee. Тарифы2027 и полный семейный бюджет неизвестны.',
    '## BajaBot: школьный класс и различие результатов',
    '[Convocatoria2026]('+BAJA+') и [Armado manual]('+ARMADO+'):1–3 классы,2–3 ребёнка и взрослый. Музей даёт временный LEGO kit; демонстрация, participation diploma. Ноmanualp8 перечисляет поощрения — противоречие сохранено, соревновательный титул не обещан. Самостоятельные/межшкольные команды возможны при школьных подтверждениях. Это вариант первого опыта, если класс подходит.',
    '[Mini Sumo LEGO]('+SUMO+'):4–6 классы,2–3 ученика и взрослый, собственный автономный LEGO,NXT/EV3/SPIKE/51515.20см куб,2кг; Bluetooth/Wi-Fi off,USB upload,5секунд задержки,ring77см. Матвей кандидат только при4–6 классе. Вmanual есть шаблонная secundaria и15151/51515 — комплект подтвердить. Старт17 мая2026/дедлайн8 мая завершены;2027 не объявлен. Взнос неизвестен, мировая квота не установлена.',
    '## Feria Maker17–18 октября: отдельные мастерские',
    'Изучены выбранные записи публичного JSON, который загружает [собственная страница]('+MAKER+'). В нём28 занятий; в атлас добавлены9 тематических вариантов. День, часы, capacity и цена относятся к конкретному занятию, не гарантированному месту. EN/ES teaching прямо не заявлен. Числовая цена без кода валюты не объявлена подтверждённойMXN.',
    '| Мастерская | День / время | Возраст | Цена занятия |\n|---|---|---|---|\n'+ '\n'.join('| '+ev[id]['title'].replace('Feria Maker · ','')+' | '+(ev[id]['start']+'—'+ev[id]['end'] if ev[id]['start'] else 'День не задан')+' | '+ev[id]['age']+' | '+ev[id]['cost']+' |' for id in ['E'+str(i) for i in range(192,201)]),
    'Картонный robot12+ — позже; emotional monster не подтверждает наличие электроники. Craft брелокrobot — дерево и ручные инструменты. OctoStudio0 иmonster0 относятся кзанятию; общий вход/поездка отдельно. Для0.2/0.25часа коротких сессий длительность не превращена в полный день. Пустое поле датыClicker не заменено днями всей ярмарки.',
    '## Полные карточки и ссылки']
for ident in NEW_IDS:
    e=ev[ident];lines+=['### '+ident+' · '+e['title'],e['country']+' · '+e['city'],'Когда: '+(e['start']+' — '+e['end'] if e['start'] else e['period']),
        'Возраст: '+e['age'],'Матвей: '+e['mat'],'Оскар: '+e['osc'],'Команда/формат: '+e['format'],'Оборудование/содержание: '+e['gear'],'Язык: '+e['language'],
        'Цена: '+e['cost'],'Результат: '+e['reward'],'Условия: '+e['note'],'Следующий шаг: '+e['action'],
        'Источник: [первичный документ]('+e['source']+'). '+', '.join('['+r['label']+']('+r['url']+')' for r in e['references'])+'.']
lines+=['## Проверка и оставшийся мировой охват',
    'Сохранены3 806 прежних событий, все1 102 camp dossiers,57 смет,64 семейных выбора лагеря, школы, история5–10 лет, длинные маршруты и140 прежних профилей. TMR/C064 и два связанных профиля изменены по описанным источникам. Два новых профиля — местные, не мировой рейтинг.',
    'Семейный ICS3 033: добавлены8 записей сдатами, прежние3 023VEVENT побайтно сохранены;2Bebras сохраняютUID/даты, обновлена отметка проверки. Техническая мастерская12+ не включена в семейный ICS.104крупные выставки в отдельномICS прежние. Undated watches не экспортированы как вымышленные дни.',
    audit['source_limits'],
    'Публикация этой редакции пока недоступна. Локальный сайт/полные ZIPSQLite иJSON проверяются отдельно от живой ссылки. Сырые документы, пустые формы и браузерные снимки остаются приватно вне репозитория. Сообщения, заявки, платежи и consent не выполнялись.',
    'Мировая цель активна: все уровни соревнований/лиг, крупные компании/выставки и допуск семьи; топовые общие иSTEM лагеря2026–2027,EN/ES/RU,пансионы/дневные/семейные программы; постоянные школы и история результатов; инженерные и предпринимательские маршруты. Европа/Швейцария/Франция/Испания,Азия/Тайвань/Сингапур/Корея/Япония/Китай,США/Канада,Коста-Рика/Мексика/Латинская Америка и прочий мировой охват сохранены. Полностью изученных стран0.']
from nearby_robotics_v135 import polish
body='\n\n'.join(polish(s) for s in lines)+'\n'
body=body.replace(': **',':** ').replace(',[',', [')
body=re.sub(r'([^\d]),(?=\d)',r'\1, ',body)
f.write_text(body)
if plan['latest_validation'].get('version')!=135:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v134:fourselectedSingapore dossiers/twodatedcamp rows/onebudget and Ayla tariff correction; independent/UIchecks,commit '+BASE+' and byte-verified archive. Meaningful research continues despite same-project hosting404.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected nearby primary categories/workshops; local preparation only, no global completeness or publication.'
plan['nearby_robotics_v135']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['global_competitions','eligibility']:q['evidence']='v135local:1168competitionrecords/144profiles. LocalLATAM2026age/team/hardware conflicts separatedfromLTU2027/W193. Baja grade1–3demo/4–6Sumo, TMR2027March3–6 exacthostdates, BebrasOctober16deadline/gradeconflict.0fullyauditedcountries;worldobjectiveactive.'
    elif q['id']=='unified_database':q['evidence']='v135local:3829records/1102campdossiers/57partialbudgets,21newrows/twoupdated,completeSQLite/JSONZIP.3033familyICS/104majorICS;unchangedcamps/schools/routes. No push/save/deployment.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=135]+[dict(version=135,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=0,new_calendar_rows=21,updated_event_ids=['C043','C064'],new_guide_ids=GUIDES,primary_http_attempts=30,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
html=ROOT/'dist/index.html';s=html.read_text().replace('?v=134','?v=135').replace('data-ui-version="134"','data-ui-version="135"')
s=s.replace('src="assets/leagues.js"','src="assets/leagues.js?v=135"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_соревнования_Мексика_мастерские_v135.md" download>Мексика · младшие дисциплины и мастерские</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
html.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','league_profiles','new_calendar_rows','family_ical','direct_http200_bodies','pdf_pages_retained','goal']}))
