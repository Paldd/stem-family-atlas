"""CHE/ESP/FRA: family choices, source conflicts and actual junior access."""
import ast
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED = '2026-10-02'
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert len(d['events']) == 1689 and d['completeness_audit']['version'] == 45
urls = json.loads((WORK / 'urls-europe-choice-v46.json').read_text())
byid = {e['id']: e for e in d['events']}
new = []
tree = ast.parse((ROOT / 'scripts/expand-oceania-v29.py').read_text())
for name in ['ref', 'event']:
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'event_helpers', 'exec'))
base_event = event
def event(*args, **kwargs):
    e = base_event(*args, **kwargs)
    e['region'] = 'Европа'
    return e

# The English page explicitly gives dates, but never establishes English teaching.
for number, title, start, end, cost in [
    (407, 'регулярная Academy 8+', '', '', 'CHF 390 / 12 часов за semester; CHF 690 / 24 часа за год'),
    (408, 'Winter · 8–12 февраля 2027', '2027-02-08', '2027-02-12', 'CHF 350 за пять утренних занятий'),
    (409, 'Easter · 30 марта–2 апреля 2027', '2027-03-30', '2027-04-02', 'Цена четырёх утренних занятий ещё не объявлена'),
    (410, 'Summer · 12–16 июля 2027', '2027-07-12', '2027-07-16', 'Общий тариф: CHF 350 утро / CHF 500 полный день; пакет смены подтвердить'),
    (411, 'Summer · 26–30 июля 2027', '2027-07-26', '2027-07-30', 'Общий тариф: CHF 350 утро / CHF 500 полный день; пакет смены подтвердить'),
    (412, 'Summer · 9–13 августа 2027', '2027-08-09', '2027-08-13', 'Общий тариф: CHF 350 утро / CHF 500 полный день; пакет смены подтвердить'),
    (413, 'Halloween · 11–15 октября 2027', '2027-10-11', '2027-10-15', 'CHF 350 за пять утренних занятий'),
]:
    e = event(f'L{number}', 'Cosmo Robotics Nyon · ' + title, 'Швейцария',
        'Nyon · Centre de Magie de la Côte, Falconnier 23', urls['cosmo'],
        'Academy прямо 8+; отдельный возраст лагерной группы не указан',
        'Academy подходит по диапазону; лагерь после подтверждения группы и языка',
        'Academy пока не подходит: в 2027 исполняется 7. Возраст лагеря отдельно',
        'Нужно подтвердить возраст лагеря, язык техники и текущий набор; публичная дата не подтверждает место.',
        'micro:bit, Maqueen, датчики, моторы и практические проекты', block='Лагеря',
        start=start, end=end, participation='day_camp', priority='P4 — язык и лагерный возраст не установлены',
        cost=cost, date_scope='camp_window' if start else 'regular_program',
        note='Технический EN / ES / RU не подтверждён. Утро 09:00–12:00; полный день 09:00–17:00 с отдыхом и бассейном в среду. Не весь полный день отведён робототехнике.')
    if number == 407:
        e.update(participation='regular', format='Регулярные занятия; один час в неделю',
            note='До декабря 2026: вторник 17:00–18:00. С января 2027 также среда 13:30–14:30 / 14:45–15:45. Включён micro:bit; язык и текущий состав неизвестны.')

e = event('L414', 'Costa Blanca Camp · Robotics · кандидат следующего лета', 'Испания',
    'Elche / Alicante · La Loma farm-school', urls['costa'],
    'Возраст конкретной robotics-группы в прочитанных страницах не указан',
    'Кандидат: возраст, сложность и долю технического EN / ES подтвердить',
    'Кандидат: младшую robotics-группу и готовность к пансиону подтвердить',
    'Новый сезон 2027 не объявлен; возраст, даты, стоимость и текущие места отдельно.',
    'Моторы, водный управляемый аппарат, датчики, stop-motion и проекты роботов',
    block='Лагеря', participation='day_camp', priority='P4 — будущий набор и возраст неизвестны',
    language='Языковые занятия EN / ES утром; технические презентации на EN / ES. Полный язык преподавания робототехники не установлен.',
    note='Архив 2026: технический трек занимает четыре дня второй половины дня. Robotics-page пишет 12 sessions, homepage — 12 hours: длительность согласовать. Пансион в домиках с питанием подтверждён; сертификат и внутренний robot battle не мировой отбор.')
e.update(participation='residential', format='Пансион с полным питанием; наличие day-варианта не установлено',
    language_mode='support', support_languages=['EN','ES'],
    references=[ref('Техника и языковые занятия', urls['costa_home']), ref('Пансион и питание', urls['costa_facility'])])
e = event('L415', 'Robots School Segovia · TecnoCamp · следующий набор', 'Испания',
    'Segovia', urls['robotschool'], 'Последний набор 2026: 5–16 лет',
    'По прежнему возрасту подходит; новую группу и уровень подтвердить',
    'По прежнему возрасту подходит; новую группу подтвердить',
    'Даты 2027 не объявлены; уточнить язык техники, группу и место.',
    'LEGO, Minecraft, Roblox, программирование, робототехника и AI',
    block='Лагеря', participation='day_camp', priority='P4 — новый сезон и язык неизвестны',
    note='Архив 2026: 25 июня–21 августа, рабочие дни 09:00–14:00. English-Techy — отдельная страница 2025: язык + базовые цифровые навыки; её даты и EN не перенесены на TecnoCamp.',
    evidence='historical_program')
e['references'] = [ref('Отдельная устаревшая English-Techy программа', urls['techy'])]
e = event('L416', 'ICS Paris · AI Startup Sprint · будущая старшая ступень', 'Франция',
    'Paris 15 · 23 rue de Cronstadt', urls['ics_camps'], 'Последняя AI-программа 2026: Grades 6–12',
    'Будущая ступень только после поступления в Grade 6 и нового набора',
    'Пока не подходит: программа начинается с Grade 6',
    'Последний AI-поток открыт внешним школьникам; новый сезон и язык занятий подтвердить.',
    'Design thinking, generative AI и разработка концепции продукта', block='Лагеря',
    participation='day_camp', priority='P4 — старшая ступень; новых дат нет', themes=['ai','coding','technology'],
    cost='Архив 2026: EUR 730 за пять дней; на 2027 цена не установлена', evidence='historical_program',
    note='29 июня–3 июля 2026 завершены. Вела студенческая Harvard Women in Computer Science; это не поступление в Harvard и не университетская степень. Начальные творческие ICS camps 3–12 — другая программа, их возраст не применён к AI Startup Sprint.')
e = event('C1105', 'Globeducate Robotics Challenge · следующий школьный цикл', 'Франция',
    'Paris / гибридный формат; площадка нового сезона не объявлена', urls['ics_robotics'],
    'Архив 2026: Primary / Middle / High School; точные классы будущей команды неизвестны',
    'Кандидат через школьную Primary-команду; состав подтвердить',
    'Младшая Primary-группа не установлена; одного возраста школы недостаточно',
    'Школьная сеть Globeducate; свободный вход независимой иностранной команды не подтверждён.',
    'LEGO SPIKE, матчи по заданиям и командная работа', scope='international',
    priority='P4 — школьный доступ; новый календарь не объявлен',
    note='Пятый цикл 19 мая 2026: France / Spain / Italy / Morocco / Canada, host EIB Monceau. Следующий цикл ожидается в 2027, но дата не опубликована. Международное сетевое событие не подменяет мировой финал FLL / WRO / VEX.')
e['related_school_ids'] = ['S047','S036']
assert len(new) == 11
d['events'] += new

# Keep the LEGO Junior programme undated rather than multiplying a catalogue course by all camps.
byid['L131']['references'] += [ref('Robotics catalogue', urls['techspark_robotics']),
    ref('Zürich: опубликованный выбор конкретных курсов', urls['zurich_camps']),
    ref('Lausanne: опубликованный выбор конкретных курсов', urls['lausanne_camps'])]
byid['L131']['proof'] = '02.10.2026 перепроверены каталог и конкретные меню: LEGO 6+ есть в каталоге, но в датированных сменах Zürich / Lausanne не перечислен.'
byid['L179']['related_school_ids'] = ['S048']

def sources(items):
    return [dict(title=t,url=urls[k],claim=c,kind='school',checked=CHECKED) for t,k,c in items]
ics = dict(id='S047', name='ICS Paris · International School', iso='FRA',country='Франция',region='Европа',
    city='Paris 15 · 23 rue de Cronstadt',school_type='private',
    curriculum='IB PYP: Primary Grades 1–5, 6–11 лет; английская программа с французским как отдельным языком.',
    ib_programmes=[dict(programme='PYP',status='school_report'),dict(programme='DP',status='school_report')],
    ages='Nursery–Grade 12; Primary 6–11. Класс и место по индивидуальному зачислению.',instruction_languages=['EN','FR'],
    language_note='Primary: предметы на английском, французский четыре часа в неделю. BML support включён в tuition; язык команды уточнить.',
    fit=dict(mat='candidate',osc='candidate',note='Primary подходит по общему возрасту обоим. Текущий состав соревновательной команды отдельно.'),
    boarding='unknown',boarding_note='Дневная школа; пансион для младших не подтверждён.',
    programme='Primary: LEGO Education / AI / Space Programme и Innovation Centre. Участие в Globeducate Robotics Challenge 2026 подтверждено, приз / команда конкретного класса не установлены.',
    labs='FabLab с 3D-принтером и лазерным резаком прямо для Grades 6–9. Доступ детям 6/9 к этим инструментам не обещан.',
    ai='AI / coding / robotics заявлены; AI Startup Sprint 2026 только Grades 6–12, не младшая программа.',results=[],evidence='programme',
    admissions='По досье и свободным местам, возможен приём в течение года. FAQ не требует вступительного экзамена; grade placement и текущую команду подтвердить.',
    cost='2026/27 при обоих Grades 1–5: tuition EUR 49518/год за двоих. Новым +15000 application / registration / development fund; итого EUR 64518 до питания и дополнительных услуг. Lunch supervision с собственным обедом +3354 за двоих; hot lunch +5730 включает supervision. School development fund со второго года EUR 1000 каждому, не разовый навсегда. Grade 5 iPad deposit EUR 400 отдельно, если применимо.',
    questions=['Какие конкретные классы и часы LEGO / AI получит каждый?', 'Какие коды, наставник и результаты текущей Primary-команды?',
        'Можно ли после трёх лет опыта участвовать в внешнем FLL / WRO?', 'Какой полный счёт с питанием, ECA и языковыми услугами?'],
    sources=sources([('Primary','ics_primary','EN, 6–11, PYP и четыре часа французского'),('STEAM и FabLab','ics_steam','FabLab Grades 6–9; младший доступ отдельно'),
        ('Сетевой турнир 2026','ics_robotics','Участие школы; общего мирового титула не установлено'),('Тариф 2026/27','ics_fees','Tuition, фонд и обязательное сопровождение обеда'),
        ('Admission FAQ','ics_faq','Приём по досье / месту'),('Разные лагерные программы','ics_camps','AI только Grades 6–12')]),
    checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны первичные школьные страницы; приём и младший мировой результат не подтверждены.')
asv = dict(id='S048',name='American School of Valencia',iso='ESP',country='Испания',region='Европа',
    city='Puçol · Los Monasterios · Avenida Sierra Calderona 29',school_type='private',
    curriculum='Американская Elementary Grades 1–5; старшая IB Diploma. PYP не приписан American Primary.',
    ib_programmes=[dict(programme='DP',status='school_report')],ages='Early Childhood–Grade 12; Elementary Grades 1–5',
    instruction_languages=['EN','ES'],language_note='Английская школьная программа, Spanish / Valencian отдельно. ASV+ прямо на английском; перечень STEM-групп по возрастам подтвердить.',
    fit=dict(mat='candidate',osc='candidate',note='Обоим возможна Elementary по placement; клуб робототехники и текущая команда ещё не установлены.'),
    boarding='unknown',boarding_note='Дневная школа; пансион не установлен.',
    programme='Технология в учебных предметах; ASV+ STEM по возрастным группам. Летний STEAM Summerland 2026 с робототехникой — подтверждённая учебная программа, новый набор не объявлен.',
    labs='Конкретный младший набор, технические часы и действующая лаборатория требуют подтверждения.',
    ai='Обязательный младший AI-трек отдельно не установлен.',results=[],evidence='programme',
    admissions='Официальный процесс через OpenApply; класс, оценки английского и место отдельно. Заявка семьи не подана.',
    cost='HTML-тариф 2026/27: Elementary EUR 7878 tuition/год с lunch. За двоих EUR 15756. При non-shareholder модели: +2500 annual enrollment, +3000 capital и +300 application, пример первого года EUR 21556 до materials, bus и extras. Модель shareholder с ASV Share EUR 2500 не смешана с non-shareholder; полный расчёт подтвердить.',
    questions=['Есть ли нынешняя Elementary-команда WRO / FLL / VEX и кто наставник?', 'Какие ASV+ STEM-группы доступны каждому и сколько часов?',
        'Какой полный счёт при выбранной shareholder / non-shareholder модели?', 'Можно ли сочетать школу с независимой соревновательной командой?'],
    sources=sources([('Elementary','asv_primary','Grades 1–5 и интеграция технологии'),('ASV+','asv_cocurricular','Занятия прямо на EN; доступ по возрастам'),
        ('Школа и IB DP','asv','Американская школа и старший DP'),('Тариф 2026/27','asv_fees_live','Tuition включает lunch, модели оплаты отдельно'),
        ('Admission','asv_admission','Индивидуальное зачисление'),('Летний STEAM','asv_summer','Робототехнический трек 2026')]),
    checked=CHECKED,priority=2,research_status='partial',verification='Язык и тариф первично подтверждены; чемпионская младшая команда не установлена.')
d['schools'] += [ics,asv]

h = d['school_history']; old = next(x for x in h['results'] if x['id']=='H107')
old.update(source=urls['first_world'],provenance='organizer_protocol',checked=CHECKED,
    note='FIRST прямо подтверждает Champion’s Award Winner ROBOTECH 2026. Это комплексная награда; Robot Performance в опубликованном списке шестое место. Школьная принадлежность неизвестна.')
h['entities'].append(dict(id='FLL-MINDFACTORY',name='mindfactory',kind='unresolved',country='Switzerland',age='unknown',school_id=None,
    note='FIRST подтверждает Aargau и мировой результат команды; школа и открытый младший набор не установлены.'))
h['results'].append(dict(id='H137',entity_id='FLL-MINDFACTORY',year=2026,league='FLL',category='Challenge',stage='FIRST World Festival · Houston',
    award='Champion’s Award Finalist',level='world_finalist',source=urls['first_world'],provenance='organizer_protocol',team='mindfactory',team_id=None,
    note='Финалист главной комплексной награды по FIRST; не Winner и не отдельная победа Robot Performance. Школьная принадлежность неизвестна.',checked=CHECKED))
for c in h['coverage']:
    if c['id']=='FLL':
        c['years']['2026']='protocol'
        c['detail']='Champion’s Award 2022–2026: 2022–2024 и 2026 протоколы организатора, 2025 отчёт SESI-SP. Добавлен Swiss finalist 2026. Полные ранние годы, все финалисты и школьные связи ещё не собраны.'
        c['sources'].append(urls['first_world'])
h.update(version=46,checked=CHECKED,conclusion='137 отдельных результатов. ROBOTECH 2026 теперь подтверждён FIRST; mindfactory добавлен как мировой финалист. Школы этих команд не установлены. Полный рейтинг школ за 5–10 лет остаётся частичным.')

f=d['europe_focus']; f.update(version=46,checked=CHECKED,
    heading='Испания для команды. Швейцария для VEX. Франция для английской пробы.',
    conclusion='Мой выбор для вашей семьи: сначала Испания и действующий наставник Elementary, рядом отдельная дорожка Оскару. Швейцария интересна для VEX IQ / английской школы при подходящем бюджете. Франция — конкретный английский Primary и двуязычная проба; французский язык соревнований ещё согласовать.',
    limitations='Десятый ограниченный проход: 236 карточек трёх стран, 22 школьных досье. Новый календарь не заменяет подтверждение места и национальной квоты. Все страны остаются частично исследованными; мировой рейтинг школ не установлен.')
fc={x['iso']:x for x in f['countries']}
fc['CHE']['event_ids'] += [f'L{x}' for x in range(407,414)]
fc['CHE']['camp'] += ' Cosmo Nyon: шесть лагерных окон 2027; технический EN и возраст именно лагеря неизвестны, Academy с 8.'
fc['CHE']['results_check'] += ' FIRST World Festival 2026: mindfactory — Champion’s Award Finalist; школа / текущий младший набор не установлены.'
fc['ESP']['school_ids'].append('S048');fc['ESP']['event_ids'] += ['L414','L415']
fc['ESP']['school'] += ' ASV Valencia: American Elementary и ASV+ на EN; младшая чемпионская команда не установлена.'
fc['ESP']['camp'] += ' Costa Blanca: пансион и EN/ES-презентации, но технический язык и возраст ещё проверить. TecnoCamp Segovia 5–16: следующий набор без дат.'
fc['ESP']['results_check'] += ' ROBOTECH — мировой Champion’s Award 2026 по FIRST; неизвестную школу не объявляем мировым лидером.'
fc['FRA']['school_ids'].append('S047');fc['FRA']['event_ids'] += ['C1105','L416']
fc['FRA']['school'] += ' ICS Paris: EN Primary 6–11 / PYP, участие в сетевом Globeducate 2026. FabLab Grades 6–9 и AI Startup Grades 6–12 не младшие программы.'
fc['FRA']['budget'] += ' ICS Paris при обоих Grades 1–5: EUR 49518 tuition/год; первый приём EUR 64518 до питания и extras. Полный счёт и выбранные классы отдельно.'
f['family_picks_note']='Это мой выбор по возрасту, языку, уровню опыта и документам вашей семьи. Школы ниже подходят как учебные базы; мировой титул их младших команд не установлен. Набор на курс не гарантирует место в команде.'
f['family_picks'] = [
    dict(kind='league',country='Испания',title='Основная соревновательная дорожка: WRO',
        why='Матвею Elementary: автономный робот или собственный инженерный продукт. Оскару RoboBasic; сейчас разные категории лучше сохраняют глубину подготовки старшего.',
        gate='Команды 2–3. Младший Elementary по действующему правилу календарного возраста — с сезона 2028; допуск национальной квоты отдельно.',event_ids=['C910','C911'],school_ids=[],source_urls=[urls['wro_spain']]),
    dict(kind='league',country='Швейцария',title='Для Матвея: VEX IQ с наставником',
        why='TechLabs Competition Lab 9–14 на EN/DE даёт конкретную командную практику. Оскару отдельная младшая группа / WRO Starter.',
        gate='Курс не гарантирует команду: Alpine 2027 принимает швейцарские команды. Starter не даёт мирового отбора.',event_ids=['L330','L331','C549','C906'],school_ids=[],source_urls=[urls['robotlabsch'],urls['wro_ch']]),
    dict(kind='league',country='Франция',title='FLL / Coupe Junior после языковой проверки',
        why='Матвею национальный FLL 9–16 или Coupe Junior 8–18. Оскару проектный Explore / Discovery; признание проекта не мировая рейтинговая победа.',
        gate='Локальный Nantes начинает с 11: общий минимум 9 не отменяет его правило. EN-защита и иностранное продвижение не установлены.',event_ids=['C916','C918','C1102','C1103'],school_ids=[],source_urls=[]),
    dict(kind='camp',country='Франция',title='Лучший конкретный общий старт: ABI Paris',
        why='Haunted STEAM 26–30 октября 2026: Explorer 5–8 и Inventor 9–12, двуязычная работа над механизмами, схемами и кодом.',
        gate='EUR 980 за двоих за неделю без проживания. Наличие места и более сложную задачу Матвею после трёх лет опыта подтвердить.',event_ids=['L230'],school_ids=['S025'],source_urls=[urls['abi']]),
    dict(kind='camp',country='Швейцария',title='Две группы: Ecolint и TechLabs',
        why='Оскару Ecolint Introduction 19–23 октября; Матвею TechLabs VEX IQ. Это отдельные возрастные группы, а не обещанная общая смена.',
        gate='Ecolint вводный уровень: после трёх лет опыта может быть простым. LEGO 6+ TechSpark есть в каталоге, конкретная смена не установлена.',event_ids=['L296','L292','L293','L131'],school_ids=[],source_urls=[urls['ecolint'],urls['techspark_robotics'],urls['zurich_camps']]),
    dict(kind='camp',country='Испания',title='EN-проба сейчас; пансион после нового объявления',
        why='Tecnoeduka Pamplona имеет отдельные EN-группы по рождениям обоих. Это регулярный часовой курс. NATUK и Costa Blanca — лагерные кандидаты.',
        gate='У лагерей нет подтверждённого нового набора для обоих. Costa Blanca: язык занятий и 12 sessions / 12 hours расходятся.',event_ids=['L396','L397','L227','L414'],school_ids=[],source_urls=[urls['natuk'],urls['costa'],urls['costa_home']]),
    dict(kind='school',country='Испания',title='Школа + внешняя команда',
        why='ASV Valencia — EN/ES учебная база; Colegio Lar — проверяемый кейс местных Elementary-результатов. Город выбирать по доступному сильному наставнику.',
        gate='ASV+: технический EN подтверждён, конкретная младшая команда неизвестна. Lar: местные результаты не общий мировой титул.',event_ids=['L179','C911'],school_ids=['S048','S027'],source_urls=[urls['asv_cocurricular'],urls['lar']]),
    dict(kind='school',country='Швейцария',title='Basel для команды; ISZL для EN Primary',
        why='IS Basel имеет соревновательную связь; ISZL — английскую Primary. Нужны текущие младшие составы, часы и наставники.',
        gate='Награды старшей / Middle School команды не доказывают сильную команду детям 6/9. Сравнивать полный годовой бюджет.',event_ids=['L330'],school_ids=['S023','S033'],source_urls=[urls['isbasel']]),
    dict(kind='school',country='Франция',title='ICS Paris / ABI для английского Primary',
        why='ICS Primary прямо на EN, PYP / LEGO / Innovation Centre; ABI — двуязычная школьная и каникулярная проба.',
        gate='ICS сетевое участие подтверждено, младший мировой приз нет. FabLab 6–9 означает Grades 6–9, а не возраст 6–9.',event_ids=['C1105','L230','L416'],school_ids=['S047','S025'],source_urls=[urls['ics_primary'],urls['ics_steam'],urls['ics_robotics']]),
]
f['evidence_cards'] += [dict(title='Испания / Швейцария · первичный мировой протокол FLL 2026',
    detail='ROBOTECH — Champion’s Award Winner; mindfactory — Champion’s Award Finalist. FIRST подтверждает обе команды; школу и вход новых младших детей пока не установили.',
    limit='Winner и Finalist — разные результаты. Нельзя перенести награду на школу по месту проведения / городу.',event_ids=['C913','C909'],school_ids=[],source_urls=[urls['first_world']]),
    dict(title='Франция · английский Primary не даёт автоматический доступ к старшему FabLab',
    detail='ICS Paris: 6–11 лет в Primary на EN. FabLab — Grades 6–9; AI Startup — Grades 6–12.',
    limit='Американский Grade 6 — школьная ступень, не шестилетний возраст. Сетевое участие не World Championship.',event_ids=['C1105','L416'],school_ids=['S047'],source_urls=[urls['ics_primary'],urls['ics_steam'],urls['ics_camps']])]
for b in f['base_comparison']:
    if b['iso']=='ESP':b['school_ids'].append('S048')
    if b['iso']=='FRA':b['school_ids'].append('S047')
for k in ['cosmo','costa','costa_home','costa_facility','robotschool','techy','first_world','ics_primary','ics_steam','ics_fees','ics_camps','ics_robotics','asv_primary','asv_cocurricular','asv_fees_live']:
    f['sources'].append(dict(title='Углублённая проверка · '+k,url=urls[k],checked=CHECKED))

d['asof']=CHECKED
d['expansion_log'].append(dict(version=46,checked=CHECKED,scope='CHE/ESP/FRA family decisions and source conflicts',added=11,new_schools=2,new_history=1,status='partial; worldwide objective preserved'))
a=d['completeness_audit'];a['validation_previous']=copy.deepcopy(a.get('validation',{}))
a.update(version=46,checked=CHECKED,scope='CHE/ESP/FRA: конкретный семейный выбор, младшие школы и перепроверка первичных результатов',
    conclusion='11 новых карточек, два школьных досье, мировой финалист и усиленный протокол ROBOTECH. Языковые, возрастные и сезонные пробелы обозначены; остальной мир сохранён.',
    new_ids=[e['id']for e in new],new_profiles=[],new_school_ids=['S047','S048'],updated_ids=['L131','L179'],updated_profile_ids=[],
    validation=dict(version=46,status='pending',publication='pending'))
a['school_history']['results']=137
d['camp_focus'].update(version=46,checked=CHECKED,added_ids=[e['id']for e in new if e['block']=='Лагеря'],updated_ids=['L131','L179'],
    conclusion='Новые Nyon окна 2027 с неподтверждённым языком, два испанских кандидата и старший AI-трек ICS. Архивные сроки не перенесены в 2027.',validation=dict(version=46,status='pending'))
d['school_focus'].update(version=46,checked=CHECKED,conclusion='48 школьных досье. ICS Paris / ASV добавлены как англоязычные учебные базы, без выдуманных мировых младших титулов.')
known={s['url']for s in d['sources']}
for key in ['cosmo','costa','costa_home','costa_facility','robotschool','techy','first_world','ics_primary','ics_steam','ics_faq','ics_fees','ics_camps','ics_robotics','asv','asv_primary','asv_cocurricular','asv_fees_live','asv_admission','asv_summer']:
    if urls[key]not in known:d['sources'].append(dict(url=urls[key],title='Первичный источник · '+key,checked=CHECKED,evidence='Прочитаны конкретные условия; пробелы отдельно.'));known.add(urls[key])
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=[]
for filename in ['receipt.json','receipt-extra.json','receipt-last.json','receipt-summer.json']:
    receipts += json.loads((WORK/'sources-europe-choice-v46'/filename).read_text())
out=dict(version=46,checked=CHECKED,status='partial',sources=[{k:v for k,v in row.items()if k!='path'}for row in receipts],
    unresolved=['Cosmo: EN website does not establish teaching language or separate camp age.', 'TechSpark LEGO 6+ absent from dated Zurich/Lausanne course menus.',
        'Costa Blanca 12 sessions / 12 hours conflict; teaching language not established.', 'English-Techy is 2025; no 2027 TecnoCamp dates.',
        'School affiliation and current junior intake of ROBOTECH / mindfactory unresolved.', 'ICS FabLab Grades 6–9 not ages 6–9.'])
(ROOT/'data/europe-choice-source-receipts-v46.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r['updated']=CHECKED;r['completeness_audit']='data/audit-v46.json';r['latest_validation_previous']=r.get('latest_validation',{})
r['latest_validation']=dict(version=46,status='pending',publication='pending')
r['research_passes'].append(dict(version=46,scope='Requested deeper Switzerland / Spain / France family analysis',status='implementation; validation pending',added=11,new_schools=2,new_history_results=1))
r['previous_goal_turn_classification']=dict(status='progress',evidence='v45 deployed and all 78 static assets anonymously hash-verified; 23 cards and two schools delivered.',remaining='The global calendar objective remains active; country coverage partial.')
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=46,cards=len(d['events']),schools=len(d['schools']),history_results=len(h['results']),new_ids=[e['id']for e in new]),ensure_ascii=False))
