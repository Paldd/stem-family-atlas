"""Bounded CHE/ESP/FRA pass: current teaching, family visits and school evidence."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED = '2026-10-02'
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert len(d['events']) == 1658 and d['completeness_audit']['version'] == 43
urls = json.loads((WORK / 'urls-europe-practical-v44.json').read_text())
new = []
byid = {e['id']: e for e in d['events']}
tree = ast.parse((ROOT / 'scripts/expand-oceania-v29.py').read_text())
for name in ['ref', 'event']:
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'event_helpers', 'exec'))
base_event = event


def learning(id, title, country, city, source, age, mat, osc, gear, note,
             cost='Текущую стоимость подтвердить', start='', end='', mode='unconfirmed', languages=(),
             regular=False, residential=False, priority='P2 — после проверки места и уровня'):
    e = base_event(id, title, country, city, source, age, mat, osc,
                   'Выбрать конкретную группу; подтвердить место, язык, уровень и допуск до записи.', gear,
                   block='Лагеря', participation='day_camp' if regular or residential else 'holiday_workshop',
                   note=note, cost=cost, start=start, end=end, priority=priority,
                   languages=languages, date_scope='camp_window', evidence='program' if regular else 'event_page')
    e.update(region='Европа', language_mode=mode)
    if regular:
        e.update(participation='regular', format='Регулярный курс; жильё семьи отдельно',
                 date_scope='season_window', period='Сентябрь 2026 — июнь 2027; поздний вход и слот подтвердить')
    if residential:
        e.update(participation='residential', format='Пансионный лагерь; условия проживания 2027 подтвердить')
    return e


# The current courses explicitly match the children's birth years and teach in English.
for id, title, source, age, mat, osc, gear, group_size in [
    ('L396', 'Tecnoeduka Pamplona · EN-робототехника · 1º–2º Primaria', urls['tecno_junior'],
     'Рождения 2019–2020; 1º–2º Primaria', 'Нет для штатной группы этого года рождения',
     'Условно: рождение 2020 подходит; класс и уровень отдельно', 'Scratch Jr, Dash & Dot', 8),
    ('L397', 'Tecnoeduka Pamplona · EN-робототехника · 3º–4º Primaria', urls['tecno_primary'],
     'Рождения 2017–2018; 3º–4º Primaria', 'Условно: рождение 2017 подходит; сложность после трёх лет опыта проверить',
     'Нет для штатной группы этого года рождения', 'Scratch, Tinkercad, LEGO WeDo / SPIKE Essential', 10),
]:
    e = learning(id, title, 'Испания', 'Pamplona · Tecnoeduka', source, age, mat, osc, gear,
                 f'Курс 2026/27 прямо указан на английском. Один час в неделю, до {group_size} детей. '
                 'Наличие мест меняется; недельный курс не гарантирует соревновательную команду.',
                 cost='EUR 50/месяц при квартальной оплате или 54 при помесячной; matrícula 30. '
                      'Сентябрь / июнь 25; скидка братьям 5%. Субсидия до 30 сентября уже истекла.',
                 regular=True, mode='primary', languages=('EN',))
    e.update(language='Английский прямо указан для этой технической группы 2026/27',
             language_certainty='Язык конкретного курса подтверждён; уровень и место отдельно.',
             references=[ref('Возрастные потоки 2026/27', urls['tecno_index']),
                         ref('Местная FLL-группа начинается с рождения 2014 и старше', urls['tecno_fll'])])

# Date pages now show 2027; an older cached web view showed the 2026 edition.
# The technical language is not established by an English website or an old parent booklet.
for id, start, end in [('L398', '2027-07-04', '2027-07-17'), ('L399', '2027-07-18', '2027-07-31')]:
    e = learning(id, 'Village Camps Leysin · STEM & Robotics · ' + start,
                 'Швейцария', 'Leysin · Village Camps', urls['village_current'], '10–17 лет',
                 'Только после 10-летия; точный день рождения и cutoff неизвестны', 'Нет: минимум 10 лет',
                 'LEGO SPIKE, механика, датчики и собственный робот',
                 'Первичная страница 2027 публикует две июльские смены. Внутренний Robot Wars — лагерный проект, '
                 'не WRO / VEX квалификация. Язык именно робототехники и пакет проживания 2027 ещё подтвердить.',
                 cost='CHF 5500 на ребёнка за опубликованную двухнедельную смену; включения и extras проверить',
                 start=start, end=end, residential=True, priority='P4 — нужны 10-летие и технический язык')
    e.update(language='Техническое EN / ES / RU не подтверждено; английский сайт не заменяет язык курса',
             references=[ref('Родительская информация; связанный PDF имеет metadata 2026', urls['village_booklet'])])

# These are genuine dated robotics workshops; no EN instruction is asserted.
for id, day in [('L400', '2026-10-23'), ('L401', '2026-10-30')]:
    e = learning(id, 'Cité des sciences · Un robot en balade · ' + day,
                 'Франция', 'Paris · Cité des sciences, bibliothèque', urls['cite_workshops'], '9–11 лет',
                 'Условно: нужно уже исполненных 9; язык занятия отдельно', 'Нет: минимум 9 лет',
                 'Робот и программирование; мастер-класс 10:00–13:30',
                 'Отдельный каникулярный мастер-класс, не недельный лагерь. EN / ES преподавание не установлено.',
                 cost='EUR 45; абонентам 35 при наличии мест', start=day, end=day,
                 priority='P4 — подходящий технический язык не подтверждён')
    e.update(language='EN / ES / RU не подтверждены в текущем описании', date_scope='event',
             format='Однодневный каникулярный мастер-класс 10:00–13:30')

for id, title, source, city, start, end, age, mat, osc, gear, note, cost in [
    ('E177', 'Festival des Technologies · Colomiers · семейные AI / роботы / игры', urls['toulouse_tech'],
     'Colomiers · Salle Gascogne, Toulouse Métropole', '2026-10-17', '2026-10-17',
     'Открыт всем; возраст отдельных занятий уточнить', 'Да для семейного посещения; задания по возрасту',
     'Да для семейного посещения; задания по возрасту', 'Мини-роботы, AI photobooth, AI-инициация, аркадные игры',
     '13:30–17:30. Муниципальный семейный фестиваль; международный отраслевой масштаб не заявлен.', 'Бесплатно'),
    ('E178', 'Lumières sur le Quai 2026 · семейный maker / digital festival', urls['toulouse_lights'],
     'Toulouse · Quai des Savoirs и площадки фестиваля', '2026-10-17', '2026-11-01',
     'Семейная программа; maker 7+, CNES-конференция 9+, Quai des Petits 2–7',
     'Условно: maker 7+; конференция 20 октября с 9 лет',
     'Семейные экспозиции и Quai des Petits; maker 7+ сейчас не подходит',
     'Цифровые инсталляции, 3D / DIY / maker и космическая инженерия',
     'Даты — окно фестиваля, не расписание ежедневных мастер-классов. '
     'Семейные активности имеют разные возрастные границы; язык технических занятий отдельно.',
     'Тариф зависит от активности; XYZT бесплатно 30 октября после 19:00 и 31 октября — 1 ноября'),
]:
    e = base_event(id, title, 'Франция', city, source, age, mat, osc,
                   'Посещение с родителем; для выбранного занятия сверить возраст, язык, билет и расписание.',
                   gear, block='События', participation='visitor', start=start, end=end, note=note, cost=cost,
                   themes=('robotics', 'ai', 'games', 'technology'), priority='P2 — семейный визит после проверки программы')
    e.update(region='Европа', exhibition_tier='family_alternative', visitor_policy='family',
             visitor_policy_note='Семейное посещение прямо заявлено; возраст отдельного занятия проверяется отдельно.',
             adult_entry='Родительское сопровождение; тариф выбранного занятия отдельно.',
             highlights=[gear], exhibitor_note='Это семейный научный / технологический фестиваль; участие всех мировых компаний не заявлено.',
             exhibitor_directory_url=source)
    if id=='E178':
        e['themes']=['technology','makers']

# School programmes, teen results and access to a junior team are different findings.
school = dict(id='S044', name='International School of Lausanne (ISL)', iso='CHE', country='Швейцария',
              region='Европа', city='Le Mont-sur-Lausanne', school_type='private',
              curriculum='IB PYP 5–11; MYP / DP дальше. Билингвальный EN / FR поток Year 3–6 по сообщению школы.',
              ib_programmes=[dict(programme=p, status='school_report') for p in ['PYP', 'MYP', 'DP']],
              ages='Primary 5–11; полная школа 3–18', instruction_languages=['EN', 'FR'],
              language_note='EN / FR Primary прямо описан; языковой assessment обязателен для билингвального потока. '
                            'Нужный английский поток и язык младшего кружка подтвердить отдельно.',
              fit=dict(mat='candidate', osc='candidate', note='Возраст Primary подходит обоим; класс, язык, место и младшая команда отдельно.'),
              boarding='unknown', boarding_note='Рассматривается дневная школа; младший пансион не установлен.',
              programme='Robotics, coding и SciTech в общем каталоге. Impact Hub: Year 5 Mission Zero и проекты с EPFL. '
                        'VEX-команда в публикации 2024 приглашает Years 10–12; это не младший набор.',
              labs='Младшее оборудование, часы и доступ к инженерным пространствам ещё проверить.',
              ai='Impact Hub описывает AI и предпринимательские workshops; обязательный AI-трек 6/9 не установлен.',
              results=[dict(league='VEX', season='2024', stage='Swiss National Final', award='Team A: 2-е место Robot Skills',
                            team='Five Rings · Team A', source=urls['isl_results'], provenance='school_report',
                            limit='Старшая команда; школа также сообщает участие в Worlds без мирового титула. Результат 6/9 не установлен.')],
              evidence='national_result',
              admissions='Нужно школьное и языковое распределение. Зачисление не гарантирует доступ в соревновательный состав.',
              cost='PDF 2026/27: Year 1–6 CHF 29300 в год каждому. За двоих tuition CHF 58600; при одновременном первом '
                   'зачислении acceptance CHF 5000 + 2500, итого CHF 66100 до OARF, питания, транспорта и optional activities. '
                   'Sibling tuition discount начинается с третьего ребёнка. Тариф 2027/28 не опубликован.',
              questions=['Есть ли нужный английский Primary-поток и места обоим?',
                         'Какой младший team code, наставник, часы, платформа и результаты 2024–2026?',
                         'Можно ли Матвею заниматься в соревновательной группе после трёх лет опыта?',
                         'Какой полный счёт для конкретных Year и нового зачисления посреди года?'],
              sources=[dict(title=t, url=urls[k], claim=c, kind='school', checked=CHECKED) for t,k,c in [
                  ('Primary', 'isl_primary', 'PYP 5–11'), ('Языковой поток', 'isl_bilingual', 'EN / FR Year 3–6 и assessment'),
                  ('Клубы', 'isl_clubs', 'Robotics / coding без возраста конкретной группы'),
                  ('Impact Hub', 'isl_hub', 'Year 5 Mission Zero; сотрудничество с EPFL'),
                  ('Результат 2024', 'isl_results', 'Старшая Skills 2-я и участие Worlds, без мирового титула'),
                  ('Тариф 2026/27', 'isl_fee_pdf', 'Year 1–6 и acceptance; дополнительные сборы отдельно')]],
              checked=CHECKED, priority=2, research_status='partial',
              verification='Первичные школьные материалы и обе страницы тарифного PDF прочитаны. Младший командный допуск не подтверждён.')
d['schools'].append(school)
h = d['school_history']
h['entities'].append(dict(id='CHE-ISL-FIVERINGS', name='ISL · Five Rings Robotics', kind='school',
                          country='Швейцария', age='teen', school_id='S044',
                          note='Публикация 2024 приглашает Years 10–12; к младшим детям не отнесена.'))
h['results'].append(dict(id='H136', entity_id='CHE-ISL-FIVERINGS', year=2024, league='VEX',
                         category='Robot Skills · старшая команда', stage='Swiss National Final · Basel',
                         award='Team A: 2-е место', level='national_skills', source=urls['isl_results'],
                         team='Five Rings Team A', team_id=None, provenance='school_report', checked=CHECKED,
                         note='School report, не независимый протокол. Участие в Worlds также сообщено, но мировой титул не заявлен.'))
h.update(version=44, checked=CHECKED,
         conclusion='136 отдельных результатов. Новый ISL Skills-результат — национальный и старший; мировой младший титул не установлен. Полный рейтинг 5–10 лет остаётся частичным.')

# Recheck existing data without inventing dates from generic programme pages.
byid['L131'].update(checked=CHECKED, priority='P3 — конкретная LEGO-смена не подтверждена',
                    action='Получить подтверждение именно LEGO Junior 6+; не бронировать смену Game Design как робототехнику.')
for id in ['C916', 'C928', 'C929']:
    byid[id]['checked'] = CHECKED
byid['C916']['references'].append(ref('FIRST: сезон 2026/27 и переход после 2027', urls['first_transition']))
profile_by_id = {p['id']:p for p in d['league_guide']['profiles']}
p = profile_by_id['fll-europe-three']
p.update(checked=CHECKED,
         summary='Сезон 2026/27: Swiss Challenge 9–16; Испания Explore 6–9, Founders Challenge 10–16, Future K 5 / K 8. '
                 'Французский текущий возраст / редакцию и язык судейства проверять у местного партнёра.',
         strengths='Одна основная команда на сезон, собственный робот и проект. Младшее демонстрационное признание отдельно от рейтинговой победы.')
for c in p['categories']:
    if c['name'] == 'Spain Founders':
        c.update(team='Explore 2–6; Challenge 2–10', hardware='Explore: WeDo / SPIKE; Challenge: допустимый текущий набор',
                 age_rule='Подтвердить контрольную дату сезона; 2017 год не означает уже исполненных 10',
                 entry='Независимая группа допустима; учебный Class Pack не равен месту на событии')
    elif c['name'] == 'Spain Future':
        c.update(hardware='Computer Science & AI; K 8 требует два робота',
                 age_rule='Возраст текущей регистрации 2026/27', entry='K 5 — учебная демонстрация; K 8 — соревновательный формат')
    elif c['name'] == 'Swiss Founders':
        c.update(age='Explore: FAQ 6–9 / страница division 6–10; Challenge 9–16', team='Explore 2–6; Challenge 2–10',
                 hardware='Допустимые LEGO-наборы текущей редакции', age_rule='Верхняя граница Explore 9 / 10 требует подтверждения',
                 entry='Иностранное участие допустимо; проход дальше только для команды страны события. Судейство обычно на местном официальном языке.')
    elif c['name'] == 'France':
        c.update(age='Общий Challenge 9–16; текущие Future-категории уточнить', team='Текущий местный регламент',
                 hardware='Founders / Future по документам выбранного потока',
                 age_rule='Общий старый возраст не заменяет новый локальный регламент',
                 entry='Местный этап → национальный → международный по квоте; EN-судейство не подтверждено')
p['nuances'] = [
    'Founders и Future 2026/27 используют разные наборы.',
    'FAQ Explore 6–9 и division 6–10 расходятся; возраст на конкретную дату важен.',
    'В Швейцарии иностранное участие и национальная квалификация — отдельные права.',
    'FIRST объявляет 2026/27 последним сезоном FIRST LEGO League. В 2027/28 планируются новые K–8 программы; '
    'совместимость SPIKE заявлена до 2028/29, названия / правила / местный отбор ещё уточняются.',
]
p['sources'].append(dict(title='FIRST K–8 после 2027 · обновление 27 августа 2026', url=urls['first_transition'], checked=CHECKED))
swiss = profile_by_id['fll-swiss-junior']
swiss['nuances'] = [s.replace('Future 5+ не имеет официального события 2026/27',
                            'FAQ допускает лишь несколько либо отсутствие официальных Future 5+ событий 2026/27; конкретный швейцарский день не установлен')
                    for s in swiss['nuances']]
swiss['sources'].append(dict(title='Повторная проверка FAQ', url=urls['swiss_fll'], checked=CHECKED))
swiss['checked'] = CHECKED
wp = profile_by_id['wro-spain']
wp['checked'] = CHECKED
wp['categories'][0]['entry'] = 'Независимая команда допустима; мировой отбор RoboBasic не заявлен'
wp['categories'][1]['entry'] = 'Местный этап нужной категории; национальная / мировая квота отдельно'
wp['sources'].append(dict(title='Повторная проверка независимых команд и сборов', url=urls['spain_wro'], checked=CHECKED))

d['events'] += new
f = d['europe_focus']
f.update(version=44, checked=CHECKED,
         conclusion='Для вашей семьи первым проверять Испанию: общий язык и независимый WRO-маршрут. '
                    'Швейцарию — как дорогую школьную / лагерную пробу с отдельной младшей командой. '
                    'Францию — через конкретный EN-поток и семейные поездки; французскую техническую защиту ещё подтвердить.',
         limitations='Восьмой ограниченный проход трёх стран: 202 карточки и 18 школьных досье. '
                     'Проверены действующие EN-группы, семейные фестивали, пансионные возрастные ограничения, '
                     'ISL и тариф 2026/27. Полные национальные календари и мировой рейтинг школ не установлены.')
countries = {c['iso']:c for c in f['countries']}
for iso, country in [('ESP','Испания'), ('CHE','Швейцария'), ('FRA','Франция')]:
    countries[iso]['event_ids'] += [e['id'] for e in new if e['country'] == country]
countries['CHE']['school_ids'].append('S044')
countries['ESP']['camp'] = ('Для обоих: текущие отдельные EN-группы Tecnoeduka в Pamplona по рождениям 2020 / 2017. '
    'Один час в неделю — языковая / проектная проба; их FLL-курс начинается с рождения 2014 и старше. '
    'Camp Tecnológico / Logix 5 — проверить язык и уровень. St George EN-роботолагерь подтверждён прошлому лету; '
    'ROBBO ждёт зимние подробности. NATUK / Tech&Play — новый сезон и язык именно техники отдельно.')
countries['ESP']['city_route'] += ' Pamplona добавлена для двух EN-групп; выбирать город для переезда всё равно по доступной соревновательной команде.'
countries['CHE']['camp'] = ('Сейчас: Ecolint для младшего и TechLabs по доступной возрастной группе; TechSpark Game Design 7+ — другой курс. '
    'LEGO Junior 6+ есть в общем каталоге TechSpark, но не в списках конкретных датированных смен. '
    'Village Camps Leysin 4–17 / 18–31 июля 2027 с 10 лет: только Матвею после 10-летия, язык и пакет отдельно.')
countries['CHE']['school'] += ' ISL Lausanne добавлен: Primary / Impact Hub; старшая VEX-команда участвовала в Worlds 2024. Младший состав 6/9 не подтверждён.'
countries['CHE']['budget'] += ' ISL: CHF 58600 tuition за двоих в Year 1–6; первый одновременный приём +7500, до OARF и optional services.'
countries['FRA']['camp'] += ' Cité 23 / 30 октября: робототехнический workshop 9–11, EN / ES не подтверждены; это отдельные короткие занятия.'
countries['FRA']['city_route'] += ' Toulouse / Colomiers: 17 октября семейный технологический фестиваль; Lumières sur le Quai 17 октября — 1 ноября с возрастами отдельных активностей.'
f['shortlist'].insert(1, dict(title='Испания · два действующих технических EN-потока в Pamplona',
                            detail='Оскар: рождения 2019–2020, до 8 детей. Матвей: 2017–2018, до 10. '
                                   'Недельные курсы; местная FLL-команда старше обоих. Для Матвея проверить сложность после трёх лет опыта.',
                            event_ids=['L396','L397']))
f['shortlist'].append(dict(title='Франция · семейная технологическая поездка в Toulouse',
                          detail='Colomiers 17 октября бесплатно и открыто всем. В Lumières sur le Quai maker с 7, '
                                 'CNES-конференция с 9, Quai des Petits 2–7; это семейные фестивали с разными возрастными занятиями.',
                          event_ids=['E177','E178']))
f['evidence_cards'] += [
    dict(title='Швейцария · школьная среда и младший состав',
         detail='ISL: национальное 2-е Robot Skills старшей команды и участие Worlds 2024 по сообщению школы. '
                'Primary и Impact Hub есть; нынешний младший соревновательный набор отдельно.',
         limit='Не мировой титул и не результат команды детей 6/9.', event_ids=[], school_ids=['S044'], source_urls=[urls['isl_results'],urls['isl_hub']]),
    dict(title='Сезон 2027/28 · новая FIRST-программа',
         detail='FIRST LEGO League завершится после 2026/27; FIRST планирует новые K–8 программы и совместимость SPIKE до 2028/29.',
         limit='Будущие названия и национальные условия не гарантированы. Выбирать наставника и инженерную практику, сверяя сезон ежегодно.',
         event_ids=['C916'], school_ids=[], source_urls=[urls['first_transition']]),
]
for b in f['base_comparison']:
    if b['iso']=='ESP':
        b['trial'] += ' Альтернатива: две текущие EN-группы Tecnoeduka в Pamplona.'
        b['event_ids'] += ['L396','L397']
    elif b['iso']=='CHE':
        b['school'] += ' ISL Lausanne: школьная кандидатура; старший Worlds-опыт не доказывает младшую команду.'
        b['school_ids'].append('S044')
    else:
        b['trial'] += ' Семейная поездка в Toulouse / Colomiers 17 октября — 1 ноября.'
        b['event_ids'] += ['E177','E178']
for key in ['tecno_junior','tecno_primary','tecno_fll','isl_results','isl_fee_pdf','village_current','toulouse_tech','toulouse_lights','cite_workshops','first_transition']:
    f['sources'].append(dict(title='Первичный источник · ' + key, url=urls[key], checked=CHECKED))

d['asof'] = CHECKED
d['expansion_log'].append(dict(version=44, checked=CHECKED, scope='CHE/ESP/FRA practical teaching and family visits',
                               added=8, new_schools=1, history_added=1, status='partial; worldwide scope preserved'))
a = d['completeness_audit']; a['validation_previous'] = a.get('validation', {})
a.update(version=44, checked=CHECKED, status='Исследование продолжается',
         scope='CHE/ESP/FRA: текущие группы, семейные события, школьный результат и будущие возрастные условия',
         conclusion='Восемь новых карточек, одно досье ISL и один национальный Skills-результат. '
                    'Текущая учебная группа отделена от команды; EN-сайт от технического языка. Остальные регионы сохранены, мировой охват частичный.',
         new_ids=[e['id'] for e in new], new_profiles=[], new_school_ids=['S044'],
         updated_ids=['L131','C916','C928','C929'], updated_profile_ids=['fll-europe-three','fll-swiss-junior','wro-spain'],
         validation=dict(version=44, status='pending', publication='pending'))
d['camp_focus'].update(version=44, checked=CHECKED, added_ids=[e['id'] for e in new if e['block']=='Лагеря'],
                       updated_ids=['L131'], conclusion='401 учебная и лагерная карточка. '
                       'Текущие EN-группы, будущий пансион 10+ и workshops с неизвестным техническим языком разделены.',
                       validation=dict(version=44,status='pending'))
d['school_focus'].update(version=44, checked=CHECKED,
                         conclusion='44 досье. ISL имеет национальный старший Skills-результат и Worlds-опыт; младший состав и полный личный счёт ещё нужны.')
known = {s['url'] for s in d['sources']}
for key in ['tecno_junior','tecno_primary','tecno_index','tecno_fll','isl_primary','isl_bilingual','isl_clubs','isl_hub','isl_results','isl_fee_pdf',
            'village_current','village_booklet','toulouse_tech','toulouse_lights','cite_workshops','first_transition']:
    if urls[key] not in known:
        d['sources'].append(dict(url=urls[key],title='Первичный источник · '+key,checked=CHECKED,
                                 evidence='Прочитан организатор / школа; сезон и ограничения указаны в карточке.'))
        known.add(urls[key])
path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

rows = json.loads((WORK/'sources-europe-practical-v44/receipt.json').read_text())
rows += json.loads((WORK/'sources-europe-practical-v44/receipt-pdf.json').read_text())
receipt = dict(version=44, checked=CHECKED, scope='CHE/ESP/FRA practical family pass',
               fetches=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in rows],
               conflicts=['Village cached web view showed 2026; current direct HTTP and canonical page show 2027.',
                          'Village linked parent booklet metadata names 2026; not used as full 2027 technical-language conditions.',
                          'TechSpark generic LEGO course vs dated session course lists.',
                          'Tecnoeduka FLL cached overview 2025/26 vs current body 2026/27; birth cutoff 2014 persists.'],
               pdf_checks='ISL two pages visually checked; Village booklet cover and relevant text read.',
               remaining='Exact birthdays/classes, technical language, junior team places, foreign quotas and world coverage.')
(ROOT/'data/europe-practical-source-receipts-v44.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
rp = ROOT/'data/research-plan.json'; r = json.loads(rp.read_text())
r.update(updated=CHECKED, status='active', completeness_audit='data/audit-v44.json')
r['latest_validation_previous'] = r['latest_validation']
r['latest_validation'] = dict(version=44,status='local_checks_pending_publication_pending')
r['previous_goal_turn_classification'] = dict(version=43,classification='progress',
    evidence='Published 752f9f0f2d1fc548fc64dab61edb00b4cca5df12; anonymous live QA and all 78 asset hashes matched. Four-country Middle East pass delivered; full-world objective continues.')
r['research_passes'].append(dict(version=44,checked=CHECKED,scope='CHE/ESP/FRA teaching / school / family pass',
                                added_records=8,new_schools=1,history_added=1,status='partial',
                                remaining='Current junior coach/places, foreign quotas, future language and worldwide scope'))
r['next_research'].insert(0,'CHE/ESP/FRA v44: текущий младший наставник и места; чужая национальная квота; EN-робототехника Village / Cité, 10-летие Матвея; будущие лагеря и национальные полные календари. Остальной мировой аудит сохраняется.')
for req in r['requirements']:
    if req['id']=='unified_database':req['evidence']='v44: 1666 cards / 129 profiles / 44 schools / 136 bounded results; world partial.'
    elif req['id']=='camps':req['evidence']='v44: 401 learning/camp cards; actual Tecnoeduka EN cohorts and strict future/unknown-language gates.'
    elif req['id']=='permanent_schools':req['evidence']='v44: 44 dossiers; ISL national teen Skills and fees; junior access not established.'
    elif req['id']=='school_retrospective':req['evidence']='v44: 136 bounded results; national Skills separated from Worlds participation; full school ranking partial.'
    elif req['id']=='global_competitions':req['evidence']='v44: 1087 competition/programme cards, 129 profiles; worldwide coverage partial.'
    elif req['id']=='exhibitions':req['evidence']='v44: 178 event cards; two current French family alternatives distinct from major professional fairs.'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=44,added=8,school_added=1,history_added=1,records=len(d['events']),world_complete=False)))
