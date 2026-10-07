"""Record bounded winter evidence and preserve the full worldwide objective."""
import collections,hashlib,json,subprocess
from camp_asia_v136 import ROOT,BASE,CHECKED,NEW,INDEX,TERMS,JW,MAGIC,RAIL,EWHA,EFORM,J_CANCEL
P=ROOT.parent/'stem-family-atlas-work/camp-eastasia-primary-v136'
d=json.loads((ROOT/'data/catalog.json').read_text());ps={q['slug']:q for q in d['camp_programmes']['profiles']}
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
oe={q['id']:q for q in b['events']};ne={q['id']:q for q in d['events']}
sources=[]
for name in ['initial','programme','jasmine']:
    for r in json.loads((P/(name+'-receipts.json')).read_text()):
        q={k:v for k,v in r.items() if k not in ['links','path','text_path']}
        q.update(retrieval_method='direct_public_http',body_snapshot_retained='path' in r)
        if 'path' in r:
            path=__import__('pathlib').Path(r['path']);raw=path.read_bytes()
            assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
            q['raw_filename']=path.name
            q['content_status']='selected_programme_clauses_not_whole_website'
            if q['key']=='ewha-application':q['content_status']='blank_docx_read_only_language_fee_and_unresolved_refund_boundaries_no_form_submission'
            if q['key']=='ewha-brochure':q['content_status']='primary_png_visually_read_no_English_claim'
            if q['key']=='isa-terms':q['content_status']='four_pdf_pages_retained_selected_enrolment_support_and_cancellation_clauses_read'
            if q['key']=='isa-index':q['content_status']='provider_navigation_and_grade_language_catalogue'
        sources.append(q)
assert len(sources)==27 and sum(q.get('http_status')==200 for q in sources)==25
plan=json.loads((ROOT/'data/research-plan.json').read_text())
publication=dict(plan['current_publication'],status='prepared_local_not_published',reason='Fresh v136 native get_site for the unchanged project_id returned NOT_FOUND/project_not_found404. No source push, saved version, deployment or replacement project.',production_browser_qa=False)
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
counts=collections.Counter(q['block'] for q in d['events']);added=set(ne)-set(oe);changed=[i for i in oe if oe[i]!=ne[i]]
audit=dict(version=136,asof=CHECKED,status='progress',scope='16 selected ISA winter programmes, one new Taiwan AXC science programme, winter NOLA variant linked to an existing dossier, refund clarification of the existing junior workshop, and a Korean STEAM language/heritage exclusion. Worldwide scope retained.',
    events=len(ne),competition_records=counts['Соревнования'],event_records=counts['События'],exhibition_records=counts['События'],exhibition_records_unit='Mixed Events block, not number of major world company exhibitions.',camp_learning_records=counts['Лагеря'],
    programme_dossiers=len(ps),countries_with_dossiers=d['camp_programmes']['counts']['countries'],official_dossier_urls=d['camp_programmes']['counts']['source_urls'],editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=len(NEW),new_dossier_operator_count=2,new_operators_in_catalogue=1,updated_dossier_slugs=['jasmine-nola','jasmine-winter-block'],unchanged_dossiers=1100,new_calendar_rows=len(added),new_budget_scenarios=2,
    unchanged_event_objects=len(oe)-len(changed),updated_event_ids=changed,updated_event_scope='Only six CP729/CP730 records: checked date/references/overall period, and the actual CP730 refund note. Existing dates, UIDs, ages and numerical prices preserved.',
    dossier_ids=[ps[s]['id'] for s in NEW],new_calendar_ids=sorted(added),family_review_candidates=d['camp_programmes']['family_review']['coverage']['candidates'],family_review_countries=d['camp_programmes']['family_review']['coverage']['countries'],
    source_retrieval_attempts=len(sources),direct_http200_bodies=25,retrieval_errors=2,retained_body_receipts=25,pdf_files=1,pdf_pages_retained=4,blank_docx_files_read=1,primary_png_files_visually_read=1,
    family_ical=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text().count('BEGIN:VEVENT'),new_family_ical_entries=31,old_family_ical_blocks_byte_identical=3027,old_family_ical_updated_blocks=6,
    excluded_new_family_rows=['CP729-20270125-20270129-winter-rail',next(q['id'] for q in ne.values() if q.get('camp_dossier_slug')=='isa-hills-tohoku')],exhibition_ical=104,league_profiles=len(d['league_guide']['profiles']),
    ui_changes='School grade text no longer receives a years suffix; session-specific programme, accommodation, extras, cancellation and questions are visible within the variant details. General NOLA tariff distinguishes the included night from an older optional summer package.',
    goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert audit['events']==3847 and audit['programme_dossiers']==1119 and len(added)==18 and len(changed)==6 and audit['family_ical']==3064
for name in ['independent-check','functional-check']:
    f=P/(name+'.json')
    if f.exists():
        q=json.loads(f.read_text());assert q['version']==136 and q['status']=='passed';audit['verification'][name]=q
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(body);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('asia-camps-audit-v136',audit)
write('asia-camps-source-receipts-v136',dict(version=136,asof=CHECKED,sources=sources,external_actions=external,limits='25 retained bodies from 27 attempts; 22 HTML, one four-page PDF, one unfilled DOCX and one primary programme PNG. Selected programme/contract clauses, not 25 complete websites/country audits. Eduko connection failed. Raw bodies, blank form and instructor/public contact data remain private outside the repository. No camp enrolment or consent.'))
write('family-camp-selection-v136',d['camp_programmes']['family_review'])
ISA_PLACEHOLDER=ps[NEW[0]]['sources'][0]['url']
ISA_KYOTO_PLACEHOLDER=ps[NEW[4]]['sources'][0]['url']
lines=['# Зима 2026–2027: Япония, Тайвань и ограничение корейского STEAM',
    'Локальная версия 136 · проверено 6 октября 2026. Новая редакция не опубликована: Sites возвращает «Sites project not found». Последняя подтверждённая публикация — 125.',
    'Добавлены 17 досье (16 разных программ/площадок ISA, одна AXC) и 18 календарных вариантов. NOLA winter связан с прежним досье; новые программы одного оператора не считаются разными независимыми лагерями. Итого 1 119 досье в 39 странах, 3 847 календарных/учебных записей и 59 частичных смет. Это не мировой рейтинг и не завершённый мировой переписной аудит.',
    'Матвей 2017 / Оскар 2020, EN/ES/RU: в 2026 возраст 8–9 /5–6, в 2027 — 9–10 /6–7. Класс при регистрации, точный день рождения и принятая заявка — разные проверки.',
    '## Выбор для семьи',
    'Тайбэй: [Magic Factory]('+MAGIC+') 25–29 января, EN-led science, текущие 1–4 классы. Для обоих только после подтверждения класса. Учебный результат — собственный способ, инструмент и записи испытаний; не робототехническая медаль. [Physical Workshop](https://www.jgroup.com.tw/%E9%BA%A5%E5%A1%8A%E7%87%9F/%E5%AF%A6%E9%AB%94%E5%B7%A5%E5%9D%8A/) 21–22 января уже был собран; уточнены возвраты. Компьютерное название Minecraft здесь означает ручные постройки, не кодирование.',
    'Япония: [ISA Safari Shinagawa]('+ISA_PLACEHOLDER+') 26 декабря — короткий старт Матвею при 2–4 классе; [Kyoto]('+ISA_KYOTO_PLACEHOLDER+') 26–28 декабря — три дневных посещения при 3–6 классе. Большинство пансионов ниже требуют 4-й класс, British Hills — 5-й. Оскару эти ISA варианты не назначены как текущий маршрут; для младшего нужны другие уже собранные программы или отдельное согласование.',
    'Инженерный Harrow Appi 13–19 декабря уже присутствует в атласе: новый дубль не создан. Эта проверка добавляет общие и языковые зимние альтернативы, сохраняет все прежние технические лагеря, лиги и соревнования.',
    '## Новые японские программы',
    '| Программа | Дата | Класс | Цена за ребёнка | Источник |\n|---|---|---|---|---|']
table=[lines.pop()]
for slug in NEW[:16]:
    p=ps[slug];v=p['timing']['session_details'][0]
    table.append('| '+p['provider']+' | '+v['start']+'—'+v['end']+' | '+p['age']+' | '+p['price']['label']+' | [Организатор]('+v['source']+') |')
lines.append('\n'.join(table))
lines += ['Английские занятия/общение описаны оператором; японские сотрудники тоже присутствуют. Иностранный ребёнок с сильным EN не получает автоматического допуска: класс, бытовое сопровождение, аккаунт/оплата и местная организация ещё согласуются. Подгрузка остатка мест не доказывает наличие места. [Зимний каталог]('+INDEX+'), [процесс и условия]('+TERMS+').',
    'Дневные Safari/Kyoto/Adventure/TGG не включают обед. Трёхдневные пансионы: две ночи, 2 завтрака, 3 обеда, 2 ужина; комнаты зависят от площадки. В Yokohama 9–14 детей в комнате, в других выбранных местах 2–6. Ряд площадок прямо не обслуживает пищевые аллергии; смотрите своё досье. Программа Shiga помечена организатором как состоится, но личное место не подтверждено.',
    'Drama Shinkiba: исправление организатора — 4–5 января/одна ночь, ошибочные 4–6 января из школьного flyer не использованы. Срок заявки внутри страницы расходится: заголовок 30 ноября, подробная карточка 28 ноября; более ранняя дата используется для напоминания с явным предупреждением. TGG цены различаются по точке сбора. Okinawa — шесть тарифов по аэропорту и размеру размещения; внутренний перелёт Японии включён, международный перелёт семьи нет. Цена общего каталога «от 155000» не назначена текущему зимнему homestay.',
    'Отмена в [PDF ISA]('+TERMS+'): для большинства выбранных программ удержание начинается с 20-дневного порога; у ISA×TGG отдельный 10-дневный порог. 20/30/40/50/100% — удержания, а не возврат. Полная оплата по счёту, минимум группы и применимость текущего договора ещё проверяются. Скидка повторного участника не применена семье автоматически.',
    '## Тайбэй: научный день и одна ночь железнодорожного маршрута',
    'Magic Factory: пять дневных дней 09–17, приход 08–09; 30 мест — объявленный предел, не остаток. Задачи/ручная студия чередуются с играми, обедом и физической активностью. Английские инструкции с EN/ZH поддержкой, без обещания EN сверстников. Нагрев/огонь делает взрослый; материалы и страховое покрытие ещё уточнить. Общая зимняя витрина описывает плащ, зелья и сургуч, конкретная карточка — исследования материалов и исключает ролевую игру. Состав взят из конкретной карточки, расхождение отмечено для подтверждения перед заявкой.',
    'Двое: NT$25600 early до 16 октября либо NT$27600 обычно; две новые футболки опционально +600. Это цена программы до перелёта, жилья семьи и возможной поздней выдачи. Скидка 800 относится к дополнительной смене того же ребёнка, не ко второму брату, и не складывается с early. [Курс]('+MAGIC+'), [зимний прайс и возвраты]('+JW+').',
    'В существующий NOLA добавлены 25–29 января, текущие 3–7 классы, 16800/early15800, одна ночь D4 в Ruifang уже включена. Летом 26–30 июля тот же продукт остаётся отдельно. EasyCard/еда и точный hostel ещё согласуются. Mandarin-first с English support; этот вариант исключён из нового выбранного семейного ICS до подтверждения языка. [Конкретный маршрут]('+RAIL+').',
    J_CANCEL,
    '## Seoul STEAM: почему пока не рекомендован',
    '[Ewha notice]('+EWHA+') и [неподписанная DOCX]('+EFORM+'): 4–22 января, 15 будних дней 10–16:30, классы 2–6, максимум 60/минимум 40. Bright Youth — оператор, Ewha Korean Language Education — партнёр/кампус. Утром Korean, днём культура/музыка/театр/экскурсии; пять блоков STEAM без конкретной robotics/AI программы. Цель — корейская диаспора; не-корейский приём и EN/ES/RU преподавание не доказаны.',
    'В DOCX KRW4000000, материалы, обед/перекусы, экскурсионная дорога/билеты и активности; требуется местный guardian для выдачи детей, жильё не заявлено. Оплата в течение 48 часов после счёта. Таблица возвратов 21/14/7 дней содержит неясные интервалы и пересечение на седьмом дне; не превращена в расчёт гарантированного возврата. Форма только прочитана, фото/данные/согласия не заполнены. Это запись ограничения исследования, не подтверждённый EN лагерь для семьи.',
    '## Проверка и пределы',
    'Сохранены без изменений 3823 прежние карточки как JSON-объекты, 1100 досье, все 57 прежних смет, школы, история результатов, маршруты и 144 профиля лиг/программ. Шесть прежних строк NOLA/workshop обновлены по источникам, даты/возраст/числовые цены сохранены. Досье без источника сезона не получили новые даты.',
    'Семейный ICS: 3064 записи, 31 новая (15 дат ISA, 15 сроков заявок, одна AXC). Сохранены 3027 VEVENT побайтно; у шести обновлены пояснения при прежних UID/датах. Grade5 British Hills и Mandarin NOLA winter не включены. ICS 104 крупных выставок прежний; 207 смешанных событий не означают 207 крупнейших выставок.',
    'Интерфейс: школьный класс больше не помечается как возраст в годах. У вариантов с собственными условиями показаны программа, проживание, доплаты, отмена и вопросы; зимняя NOLA не теряется за летним общим описанием. Пройдены 12 функциональных проверок карточек, смет, фильтров и ссылки на текущий разбор; консоль без ошибок. Снимок и мобильная визуальная проверка не подтверждены: встроенный браузер возвращает нулевую ширину для screenshot. Проверка полной SQLite/JSON и сохранности прежних данных пройдена отдельно.',
    'Получены 25 первичных ответов из 27 попыток: 22 HTML, PDF на четыре страницы, одна пустая DOCX и один PNG, визуально прочитанный. Это выборочные условия программ, не 25 полностью изученных сайтов. Eduko недоступен прямому чтению; кампусная публикация и её вложения прочитаны. Сырые материалы сохранены приватно вне атласа.',
    'Мировая цель активна: все общие/тематические/технические лагеря 2026–27 с EN/ES/RU, день/пансион/семья; соревнования/лиги/крупные выставки; постоянные школы, история 5–10 лет и инженерные/предпринимательские маршруты. Европа, Азия, Северная и Латинская Америка остаются в полном объёме. Полностью проверенных стран — 0; эта локальная версия ещё не публикация по семейной ссылке.']
lines=[s.replace('ISA_PLACEHOLDER',ps[NEW[0]]['sources'][0]['url']).replace('ISA_KYOTO_PLACEHOLDER',ps[NEW[4]]['sources'][0]['url']) for s in lines]
(ROOT/'dist/downloads/STEM_лагеря_Япония_Тайвань_зима_v136.md').write_text('\n\n'.join(lines)+'\n')
if plan['latest_validation'].get('version')!=136:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v135:21 cards, two local profiles, exact TMR host dates, eight UI checks, complete databases, commit '+BASE+' and verified local ZIP. Current research can progress despite publication outage.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected winter additions and Korean exclusion, prepared locally, not published.'
plan['asia_camps_v136']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:q['evidence']='v136 local:1119 dossiers/39 countries/1669 URLs; winter ISA/AXC/NOLA age-language-contract gates,66 editorial family selections,59 partial budgets. Korean STEAM title excluded as English proof.0 fully audited countries; full world scope active.'
    if q['id']=='unified_database':q['evidence']='v136 local:3847 records,1119 dossiers,59 partial budgets; complete SQLite/JSON ZIP and3064 family ICS. All competitions, schools and routes preserved. No push/save/deployment.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=136]+[dict(version=136,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=17,new_calendar_rows=18,new_budget_scenarios=2,official_primary_retrieval_attempts=27,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=135','?v=136').replace('data-ui-version="135"','data-ui-version="136"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_лагеря_Япония_Тайвань_зима_v136.md" download>Япония и Тайвань · зимние программы и цены</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';f.write_text(f.read_text().replace('downloads/STEM_лагеря_Сингапур_Япония_v134.md','downloads/STEM_лагеря_Япония_Тайвань_зима_v136.md'))
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','new_calendar_rows','family_ical','goal']}))
