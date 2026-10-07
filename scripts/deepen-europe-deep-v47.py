"""Bounded CHE/ESP/FRA follow-up: real 2027 camps, school evidence, podiums and visitor gates."""
import ast, copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED='2026-10-02';path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1700 and d['completeness_audit']['version']==46
urls=json.loads((WORK/'urls-europe-deep-v47.json').read_text())
new=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event']:
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 exec(compile(ast.Module(body=[node],type_ignores=[]),'event_helpers','exec'))
base_event=event
def event(*args,**kwargs):
 e=base_event(*args,**kwargs);e['region']='Европа';return e
for number,start,end in [(417,'2027-07-03','2027-07-16'),(418,'2027-07-17','2027-07-30')]:
 e=event(f'L{number}','HIF Ftan · Summer Camp 2027 · '+('Session I' if number==417 else 'Session II'),'Швейцария','Ftan · Hochalpines Institut Ftan',urls['hif'],
 '10–16 лет; Adventurers 10–13, Explorers 14–16',
 'Условно: в 2027 исполняется 10; день рождения должен быть до начала смены, точную дату проверить',
 'Нет: в 2027 исполняется 7, минимальный возраст лагеря 10',
 'Индивидуальная заявка международного ученика; подтвердить возраст на начало, доступный поток и фактические часы AI / робототехники.',
 'AI, coding, robotics и visual storytelling внутри широкой академической / outdoor программы; платформа и часы роботов не указаны.',
 block='Лагеря',start=start,end=end,participation='day_camp',scope='international',priority='P2 — будущий пансион после проверки 10-летия',
 language='English прямо указан как язык лагеря; объём конкретного технического блока подтвердить.',languages=('EN',),
 cost='CHF 4985 за 14 дней / 13 ночей; Zurich airport pickup CHF 300 дополнительно. Single-room supplements отдельно.',
 note='Пансион 14 дней / 13 ночей, international и unaccompanied minors предусмотрены. Это смешанный летний лагерь с технологиями и outdoor, не доказанный лагерь подготовки к мировому чемпионату. Место семьи не подтверждено.',evidence='program',date_scope='camp_window')
 e.update(participation='residential',format='Международный лагерь с пансионом · 14 дней / 13 ночей',language_mode='primary',provider='HIF Ftan',language_certainty='Оператор прямо указывает LANGUAGE English для этого лагеря.')
e=event('L419','Aiglon · Classic Robotics Summer Camp 2027','Швейцария','Chesières · Villars-sur-Ollon',urls['aiglon'],
 'Robotics morning: 8–16. Общий day camp с 7 не отменяет минимум 8 именно у робототехники.',
 'Условно: возраст подходит; точную robotics-неделю и язык технической группы подтвердить',
 'Нет для опубликованного robotics-трека: в 2027 исполняется 7, минимум 8; общий day camp проверить отдельно',
 'Выбрать 1 / 2 / 3 недели и Robotics morning; подтвердить даты именно этой группы, технический EN и day / boarding.',
 'Утренний Robotics focus + Alpine afternoons. English / French — другие утренние focuses; это не доказательство EN-техники.',
 block='Лагеря',participation='day_camp',scope='international',priority='P4 — конкретная robotics-смена и язык не подтверждены',
 note='Общее окно всех программ 27 июня–31 июля 2027, пять стартов. Отдельные robotics-недели не установлены и не экспортированы как непрерывный месячный лагерь. Сайт даёт общий day от 7, но Robotics focus явно 8–16. Брошюра доступна как оболочка flipbook; её цены и детали не прочитаны.',evidence='program')
e.update(participation='mixed_camp',format='Дневной или с пансионом · 1 / 2 / 3 недели',period='Общее окно 27.06–31.07.2027; выбранную robotics-неделю подтвердить',provider='Aiglon',date_scope='camp_window')
for id,key,title,lang in [('L420','eisb_robotics','Chess & Robotics',False),('L421','eisb_science','Scientific Talent · Science Camp',True)]:
 e=event(id,'EISB Sant Cugat · '+title+' · July 2027','Испания','Sant Cugat del Vallès · European International School of Barcelona',urls[key],
 'Опубликованы рождения 2012–2019 / PY1–SY2; возрастную сетку нового сезона не сдвигали предположением',
 'Условно: рождение 2017 в опубликованном диапазоне; класс и текущий набор подтвердить',
 'Нет по опубликованным рождениям: 2020 не входит в 2012–2019; возможное обновление правила только через организатора',
 'Принимаются external families по условиям записи; выбрать утро 09:00–13:00 или полный день 09:00–17:00, подтвердить недельные даты и возраст.',
 'Научные опыты с преподавателями школы; робототехника в этом science-треке не обещана.' if lang else 'Шахматы, вводное программирование / робототехника, бассейн и экскурсии; не специализированная подготовка к чемпионату.',
 block='Лагеря',participation='day_camp',priority='P2 — англоязычная science-проба Матвею после подтверждения недели' if lang else 'P4 — технический язык и точная неделя не установлены',
 themes=('science','technology') if lang else ('robotics','coding'),
 language='Оператор прямо пишет actividades en inglés guiadas por profesores del colegio.' if lang else 'Язык технического Chess & Robotics не установлен; English-сайт и школьная среда не являются подтверждением.',languages=('EN',) if lang else (),
 cost='Цена July 2027 не установлена: ссылка ведёт на таблицу 2026, а early bird указан до 01.06.2026.',
 note='Заголовок July 2027 сосуществует со старой ценовой таблицей / сроком 2026. Рождения 2012–2019 взяты буквально; обновлённый cutoff ещё не подтверждён. Точные недели не объявлены в прочитанном теле. Это дневной смешанный лагерь; одна camping-активность не делает его пансионом.',evidence='program')
 e.update(period='Июль 2027; дни конкретной недели и текущие места подтвердить',provider='European International School of Barcelona',language_mode='primary' if lang else 'unconfirmed')
 e['references']=[ref('Общие лагерные условия и старые цены',urls['eisb_camps']),ref('Таблица явно 2026, не цена 2027',urls['eisb_prices_2026'])]
e=event('L422','Logiscool Spain · LEGO WeDo Future · 6–9','Испания','Испания · участвующий филиал подтвердить',urls['logiscool'],
 '6–9 лет на дату участия; конкретный филиал и правило возраста подтвердить',
 'Условно: 9 сейчас подходит; в 2027 исполнится 10 и может выйти из диапазона',
 'Условно: 6 сейчас подходит; уровень после трёх лет опыта может быть слишком вводным',
 'Выбрать филиал, дату и язык реального занятия; опубликованная страница продукта не является датой смены.',
 'LEGO WeDo, механизмы и код; оборудование предоставляет оператор, предварительные навыки не требуются.',
 block='Лагеря',participation='day_camp',priority='P4 — даты, филиал и язык не установлены',
 note='Вводный продукт 6–9 без prerequisites. Не признан лучшим международным лагерем или соревновательной подготовкой; для опытных детей сначала тест уровня.',evidence='program')
e['provider']='Logiscool Spain'
for id,age,day,time in [('L423','8–11','среда','17:30–19:00'),('L424','12+','понедельник','18:30–20:00')]:
 older=id=='L424'
 e=event(id,'MJC Blagnac · '+('Les Cours Circuits · команда 12+' if older else 'Robotique · мастерская 8–11'),'Франция','Blagnac · 123 Vieux Chemin de Grenade',urls['mjc'],
 age+'; группы 2026/27 по текущему расписанию',
 'Нет сейчас: опубликованный минимум 12' if older else 'Условно: возраст подходит, язык и место подтвердить',
 'Нет: младше опубликованного минимума',
 'Согласовать регулярную местную группу, язык, опыт и место. Вводная мастерская не даёт автоматическое зачисление в команду.',
 'Arduino, электрика, моторы, механика и собственные инженерные проекты; готовые работы дети сохраняют.',
 block='Лагеря',participation='day_camp',priority='P4 — будущий возраст и технический язык' if older else 'P4 — EN / ES / RU обучения не установлен',
 note='Сезон 2026/27; начало регулярных занятий 14 сентября 2026 уже прошло. EN / ES / RU технического обучения не подтверждены. Команда сообщает многолетние региональные участия, но агрегатные призы не превращены в мировые школьные титулы. Клуб пишет April 2027; официальный Occitanie-этап — 27.03.2027.',evidence='program',date_scope='regular_program')
 e.update(participation='regular',format='Регулярная местная мастерская / команда',period=f'2026/27 · {day} {time}; текущую группу и места подтвердить',provider='MJC Arts Blagnac')
 e['references']=[ref('Официальный региональный день 27.03.2027',urls['occitanie_2027']),ref('Региональный результат 2026',urls['fr_regional_results'])]

def expo(id,title,country,city,key,start,end,age,policy,entry,cost,highlights,note,priority='P4 — дети не допускаются; взрослый маршрут отдельно',tier='profile'):
 no=policy=='adults_only'
 e=event(id,title,country,city,urls[key],age,'Нет: возраст ниже опубликованного порога' if no else 'Условно: детский возраст / билет и программа требуют подтверждения','Нет: возраст ниже опубликованного порога' if no else 'Условно: детский возраст / билет и программа требуют подтверждения',entry,'Не требуется',block='События',start=start,end=end,participation='visitor',scope='international',priority=priority,cost=cost,themes=('robotics','ai','technology'),note=note)
 e.update(level='Отраслевая выставка / конференция',exhibition_tier=tier,visitor_policy=policy,visitor_policy_note=age,adult_entry=entry,highlights=highlights,exhibitors=[],exhibitor_note='Тема подтверждена; полный список компаний именно будущего выпуска не проверен. Прошлые участники не гарантируют будущие демонстрации.',exhibitor_directory_url=urls[key])
 return e
e=expo('E181','Advanced Manufacturing Madrid 2026','Испания','Madrid · IFEMA · павильоны 2, 4, 6','advanced_madrid','2026-11-04','2026-11-05',
 'Для посещения требуется быть старше 16 лет. Детям 6 / 9 нельзя; это не правило 18+.', 'adults_only',
 'Предварительная профессиональная регистрация; опубликован бесплатный visitor pass. 09:30–18:00 оба дня.',
 'Бесплатная предварительная visitor-регистрация; транспорт и проживание отдельно.', ['Промышленная автоматизация','Робототехника производства','Аддитивное производство'],
 'Крупная отраслевая выставка для взрослого инженерного маршрута. Не внесена в семейный календарь; детский вход прямо исключён опубликованным порогом.')
e=expo('E182','Swiss AI Summit 2026','Швейцария','Zürich · Kunsthaus Zürich','swiss_ai','2026-11-16','2026-11-16',
 'Terms: как правило 18+. Дискреционные исключения не подтверждают допуск этой семьи.', 'adults_only',
 'Билет профессиональной конференции; сверить тариф, VAT и выбранную категорию.',
 'Executive: на странице EUR не указано, валюта CHF; показаны CHF 790 / 950, текущий тариф и VAT подтвердить.', ['AI для бизнеса','Профессиональные выступления','Деловые встречи'],
 'Это деловая AI-конференция, не большая выставка всех мировых роботопроизводителей. Дата 16.11.2026 подтверждена организатором, семейный вход не подтверждён.')
e['cost']='Executive: показаны CHF 790 / CHF 950, текущий тариф и VAT подтвердить.'
e['references']=[ref('Возраст 18+ и исключения',urls['swiss_ai_terms']),ref('Тарифы и VAT',urls['swiss_ai_tickets'])]
e=expo('E183','SIAMS 2028 · microtechnology / automation','Швейцария','Moutier · Forum de l’Arc · rue industrielle 98','siams','2028-04-04','2028-04-07',
 'Детский / семейный минимум не найден в прочитанных правилах; нужен ответ организатора.', 'confirm_children',
 'Бесплатная онлайн-регистрация посетителя; 09:00–17:30, в пятницу до 17:00.',
 'Бесплатный зарегистрированный visitor pass; поездка отдельно.', ['Микротехнологии','Мехатроника и автоматизация','Оборудование производства'],
 'Специализированная промышленная выставка; программа для детей и возрастное правило не установлены. Число экспонентов в общей странице не перенесено на будущий выпуск 2028.',priority='P3 — будущая поездка после подтверждения детей')
e['references']=[ref('Профиль организатора',urls['siams_about'])]
e=expo('E184','VivaTech 2027 · General Public Day','Франция','Paris · Expo Porte de Versailles','vivatech_b2b','2027-06-19','2027-06-19',
 '19 июня 2027 — публичный день по действующим terms; детский возраст / семейные билеты 2027 отдельно не подтверждены.', 'confirm_children',
 'Покупать категорию public-day после проверки возраста / детского билета; общий 4-day B2B pass предназначен профессионалам.',
 'Тариф public-day / детского билета 2027 не установлен.', ['AI и стартапы','Технологические демонстрации','Публичный день'],
 'Дата публичного дня 19.06.2027 прямо указана в разделе 2027 terms. General-public страница содержит старые Saturday 17 / 18 June при новом заголовке 2027; её семейная программа и прошлые экспоненты не выданы за подтверждённый детский доступ 2027.',priority='P3 — публичный день, детские билеты подтвердить',tier='global')
e.update(parent_event_id='E102',event_group='vivatech',public_days=['2027-06-19'],date_scope='public_day')
e['references']=[ref('Обзор public day с устаревшими фрагментами',urls['vivatech_public'])]
old=byid['E102'];old.update(checked=CHECKED,priority='P4 — общий профессиональный выпуск; публичный день отдельно E184',public_days=['2027-06-19'],related_ids=['E184'],event_group='vivatech',
 entry='Общий четырёхдневный B2B pass 16–19 июня 2027 — для профессиональной коммерческой деятельности. Public day 19 июня отдельной карточкой E184.',
 note='Точные дни выставки сохранены. 2027 terms подтверждают Saturday 19 June как General Public Day; B2B four-day pass профессиональный. Возраст и семейные билеты публичного дня не подтверждены из-за старых фрагментов family-страницы.',
 references=[ref('2027 B2B terms и отдельный публичный день',urls['vivatech_b2b'])])
old=byid['C918'];old['checked']=CHECKED;old['note']+=' Перепроверено: официальный день 27.03.2027 сохраняется; April 2027 в описании MJC Blagnac не заменяет дату организатора.';old['references'].append(ref('Клубное описание с April 2027',urls['mjc']))
d['events']+=new

s=next(s for s in d['schools'] if s['id']=='S009')
s.update(checked=CHECKED,language_note='Wonder Years: английский прямо назван общим языком обучения. IB registry подтверждает EN для Diploma. Язык отдельной робототехнической / летней группы ещё проверить.',
 ai='Wonder Years описывает inquiry и связь с AI / robotics; отдельный AI-курс, часы и соревновательная команда младших не установлены.')
s['programme']+=' Летний Robotics 2027 явно 8–16; общий day camp с 7 не доказывает робототехнику для Оскара.'
s['questions'][0]='Разрешить 6 / 7 лет Junior и точный Year; EN отдельного робототехнического трека проверить.'
s['sources'] += [dict(title='Wonder Years',url=urls['aiglon_wonder'],claim='Английский общий язык Wonder Years; AI / robotics inquiry, без доказанного мирового результата',kind='school',checked=CHECKED),dict(title='Summer Camp 2027',url=urls['aiglon'],claim='Отдельный robotics-трек 8–16; общий day от 7',kind='school',checked=CHECKED)]
s=dict(id='S049',name='European International School of Barcelona',iso='ESP',country='Испания',region='Европа',city='Sant Cugat del Vallès · Av. Pla del Vinyet 110',school_type='private',
 curriculum='Cambridge International Primary Programme; старшая IB Diploma. IB DP не перенесён на Primary как PYP.',ib_programmes=[dict(programme='DP',status='school_report')],ages='9 месяцев–18 лет по admissions; Primary PY1–PY6',
 instruction_languages=['EN','ES','CA'],language_note='Primary с английским погружением; школа прямо даёт PY1 65% English. Испанский / каталонский сохраняются; French с PY3. Доля других Primary-классов не установлена.',
 fit=dict(mat='candidate',osc='candidate',note='Школьный placement обоим индивидуально; запрет рождения 2020 в летнем лагере не является запретом школьного поступления.'),boarding='unknown',boarding_note='Дневная учебная база; постоянный пансион не установлен.',
 programme='Inquiry / TIC и TAC в Cambridge Primary; отдельный Chess & Robotics summer-трек. Текущий состав, код и тренировочные часы соревновательной Primary-команды не установлены.',labs='Конкретное оборудование и доступ младших к инженерной лаборатории ещё проверить.',ai='Отдельная обязательная AI-программа Primary не подтверждена.',results=[],evidence='programme',
 admissions='Заявка через admissions / OpenApply после визита и оценки; подходящий класс, места, языковую адаптацию и внешний клуб согласовать.',cost='Полный тариф 2026/27 нужных классов не установлен. Старую summer-таблицу 2026 не использовали как цену 2027.',
 questions=['Какие классы и доли EN получит каждый ребёнок?', 'Кто действующий роботонаставник Primary, сколько часов и какой код команды?', 'Можно ли тренироваться во внешней WRO / FLL команде?', 'Какой полный годовой счёт и стоимость extracurricular?'],
 sources=[dict(title=title,url=urls[key],claim=claim,kind='school',checked=CHECKED)for title,key,claim in [('Primary','eisb_primary','Cambridge Primary, inquiry / TIC / TAC'),('Школьные языки','eisb_languages','PY1 65% English; языковая модель'),('Admissions','eisb_admission','9 месяцев–18 лет, индивидуальная оценка'),('IB Diploma','eisb_ib','DP в старшей школе по отчёту школы'),('Robotics summer','eisb_robotics','Летний трек, не подтверждение школьной команды'),('English Science Camp','eisb_science','English прямо указан именно science-треку')]],
 checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны первичные школьные страницы; место, команда и мировое лидерство не подтверждены.')
d['schools'].append(s)

h=d['school_history'];h.update(version=47,checked=CHECKED)
ent={e['id']:e for e in h['entities']}
ent['FLL2026'].update(kind='community',school_id=None,note='Независимая команда детей из разных школ по собственному history; FIRST подтверждает мировые награды. Это не чемпионская награда одной установленной школы.')
# Existing canonical entity has a spelling variant; both old results and ID are retained.
for id,name,country,kind,note in [('WRO-SWISS-FIRE','Swiss Fire','Switzerland','unresolved','Национальный Elementary-победитель и world qualification по WRO Switzerland; школа и новый младший набор не установлены.'),('WRO-DOOWIT','Doowit','Switzerland','unresolved','Starter-победа национального этапа; Starter не квалифицирует на международные WRO.'),('MJC-COURS-CIRCUITS','Les Cours Circuits · MJC Blagnac','France','club','Местный внешкольный клуб; нынешняя команда 12+, отдельная мастерская 8–11. EN / ES / RU не установлены.'),('FR-ASPINUTS','Aspi’Nuts','France','unresolved','Победитель регионального Occitanie 2026. Напечатанная связь LGT Les Lombards / Lunel требует разрешения географического расхождения; школе не приписано.')]:
 assert id not in ent;h['entities'].append(dict(id=id,name=name,kind=kind,country=country,age='12+' if kind=='club' else 'unknown',school_id=None,note=note))
rows=[
 ('H138','FLL2026',2025,'FLL','Challenge','FIRST World Festival · Houston','Engineering Excellence Award Winner','world_judged','first_2025','ROBOTECH','Оценённая инженерная награда, не Champion’s Award / общий матчевый титул.'),
 ('H139','FLL2026',2025,'FLL','Challenge Robot Performance','FIRST World Festival · Houston','Robot Performance · 3rd place','world_podium','first_2025','ROBOTECH','3-е место подтверждено ordinal data-aria-posinset="3" в исходном списке FIRST; текстовый web-render ошибочно перезапускает нумерацию.'),
 ('H140','FLL2023',2025,'FLL','Challenge','FIRST World Festival · Houston','Champion’s Award Finalist','world_finalist','first_2025','FSINGENIUM Team','Финалист комплексной награды; не Winner. Школьная принадлежность не перенесена по участию отдельных старших учеников.'),
 ('H141','FLL2022',2025,'FLL','Challenge Robot Performance','FIRST World Festival · Houston','Robot Performance · 2nd place','world_podium','first_2025','Legotronic Beavers','2-е место по ordinal data-aria-posinset="2" в HTML FIRST. Канонический ID сохранён со старым вариантом Legotronics.'),
 ('H142','FLL2022',2026,'FLL','Challenge','Final Nacional · España · Burgos','Premio IngenieraSoy al ganador · 1º / ganador absoluto','national_match','fll_spain_2026','Legotronic Beavers','UBU — местный партнёр финала: общий национальный победитель. Это не мировой титул 2026.'),
 ('H143','WRO-SWISS-FIRE',2026,'WRO','RoboMission Elementary','Swiss National Final','1st place · 497 points / 234 sec','national_match','wro_swiss_results','Swiss Fire','Квалификация на World Final указана отдельно; национальное первое место не результат мирового финала.'),
 ('H144','WRO-DOOWIT',2026,'WRO','RoboMission Starter','Swiss National Final','1st place · 456 points / 318 sec','national_match','wro_swiss_results','Doowit','Местная Starter-категория не имеет международной квоты.'),
 ('H145','MJC-COURS-CIRCUITS',2026,'Coupe Junior','Junior','Occitanie · 28 March 2026','3e place','regional_podium','fr_regional_results','Les Cours Circuits','Региональный podium по организатору. Отдельные 4-е место квалификационной серии в отчёте клуба не являются 4-м итоговым местом.'),
 ('H146','FR-ASPINUTS',2026,'Coupe Junior','Junior','Occitanie · 28 March 2026','1ère place','regional_match','fr_regional_results','Aspi’Nuts','Региональная победа; школа с географическим расхождением не выбрана догадкой.')]
for id,entity,year,league,category,stage,award,level,key,team,note in rows:
 assert not any(r['id']==id for r in h['results'])
 h['results'].append(dict(id=id,entity_id=entity,year=year,league=league,category=category,stage=stage,award=award,level=level,source=urls[key],provenance='season_partner_report' if key=='fll_spain_2026' else 'organizer_protocol',team=team,team_id=None,note=note,checked=CHECKED))
h['methodology'].append('v47: 2-е / 3-е Robot Performance 2025 проверены по порядку HTML-списка FIRST; региональные призовые места не смешаны с мировыми. Агрегатная история клуба не разбита на неподтверждённые ежегодные победы.')

f=d['europe_focus'];f.update(version=47,checked=CHECKED,status='partial',limitations='Одиннадцатый ограниченный проход: 248 карточек трёх стран, 23 школьных досье. Смены / треки и публичный день не равны числу независимых фестивалей. Места, квоты и полное мировое покрытие не подтверждены.')
fc={c['iso']:c for c in f['countries']}
fc['CHE']['event_ids']+=['L417','L418','L419','E182','E183'];fc['CHE']['camp']+=' HIF Ftan: English-пансион 3–16 / 17–30 июля 2027, минимум 10; Матвею только после 10-летия, Оскару рано. Aiglon Robotics 8–16: отдельная неделя и технический EN ещё проверить; общий day с 7 не включает его автоматически.'
fc['CHE']['results_check']+=' Swiss Fire — национальный Elementary №1 2026 и мировая квота; Doowit — национальный Starter №1 без международного отбора. Школы команд не установлены.'
fc['ESP']['event_ids']+=['L420','L421','L422','E181'];fc['ESP']['school_ids'].append('S049');fc['ESP']['school']+=' EISB Sant Cugat: Cambridge Primary, PY1 65% English; позже IB Diploma. Это учебная база, мировая младшая команда не доказана.'
fc['ESP']['camp']+=' EISB July 2027: Science явно на EN; Chess & Robotics язык неизвестен. Оба публикуют рождения 2012–2019: Матвей подходит условно, 2020 Оскара исключён. Цены / early bird на странице старые 2026.'
fc['ESP']['results_check']=fc['ESP']['results_check'].replace('неизвестную школу не объявляем мировым лидером','независимую смешанную команду не приписываем одной школе')+' FIRST 2025: ROBOTECH Engineering Excellence и Robot Performance №3; FSINGENIUM Champion’s Award Finalist, Legotronic Beavers Robot Performance №2. Legotronic — общий национальный победитель Испании 2026.'
fc['FRA']['event_ids']+=['L423','L424','E184'];fc['FRA']['camp']+=' Blagnac: MJC-мастерская 8–11, соревновательная команда 12+. Матвей подходит к мастерской; EN / ES / RU не установлен. Дети не включены в команду только по общему возрасту лиги.'
fc['FRA']['results_check']+=' Les Cours Circuits — 3-е место регионального Occitanie 2026 по организатору; не мировая школьная победа.'
for c in f['evidence_cards']:
 if 'ROBOTECH' in c['detail']:c['detail']=c['detail'].replace('школу и вход новых младших детей пока не установили','ROBOTECH описывает независимый состав разных школ, у mindfactory школа неизвестна; новый младший приём не установлен')
f['evidence_cards'] += [
 dict(title='Испания · наставник мировой команды отдельно от школы',detail='ROBOTECH: Engineering Excellence и Robot Performance №3 в 2025, Champion’s Award Winner в 2026. FSINGENIUM — Finalist 2025; Legotronic Beavers — Robot Performance №2 2025 и общий национальный Winner 2026.',limit='Разные категории и уровни не сложены в единый рейтинг. Два сезона не доказывают десять лет лидерства школы; ROBOTECH — независимая команда разных школ.',event_ids=['C913'],school_ids=[],source_urls=[urls['first_2025'],urls['first_2026'],urls['robotech_history'],urls['fll_spain_2026']]),
 dict(title='Швейцария · реальный EN-пансион после 10-летия',detail='HIF Ftan: 3–16 / 17–30 июля 2027, English, 10–16, CHF 4985 за смену. Robotics / AI внутри смешанного лагеря. Aiglon Robotics 8–16, общий day с 7 — другая возрастная граница.',limit='Точный день рождения Матвея нужен перед HIF; Оскару оба robotics-трека ещё не подходят. Ни один летний лагерь не обещает мировое место.',event_ids=['L417','L418','L419'],school_ids=['S009'],source_urls=[urls['hif'],urls['aiglon']]),
 dict(title='Франция · мастерская 8–11 и команда 12+ — разные входы',detail='MJC Blagnac даёт среду 8–11 и понедельник для команды 12+. Les Cours Circuits заняли 3-е место Occitanie 2026. Официальный следующий региональный день — 27 марта 2027.',limit='Клубное April 2027 не заменяет дату организатора. EN / ES / RU не доказан; младшая мастерская не автоматический вход в призовую команду.',event_ids=['L423','L424','C918'],school_ids=[],source_urls=[urls['mjc'],urls['fr_regional_results'],urls['occitanie_2027']]),
 dict(title='Поездки на выставки · публичный день и взрослые конференции',detail='VivaTech public day — 19 июня 2027; детские билеты уточнить. Advanced Manufacturing Madrid 4–5 ноября 2026 требует возраст старше 16; Swiss AI Summit 16 ноября — обычно 18+. SIAMS — 4–7 апреля 2028, детский доступ неизвестен.',limit='У VivaTech старые семейные фрагменты 17 / 18 June не подтверждают правила 2027. Промышленная выставка и деловая AI-конференция не являются детским лагерем.',event_ids=['E181','E182','E183','E184'],school_ids=[],source_urls=[urls['vivatech_b2b'],urls['advanced_madrid'],urls['swiss_ai_terms'],urls['siams']])]
f['season_stops'] += [dict(country='Швейцария',date='03–16 / 17–30.07.2027',title='Ftan · HIF English-пансион',detail='Возраст 10–16; Матвею только после 10-летия на начало смены. Оскару ещё рано. Robotics / AI — часть смешанного лагеря.',event_ids=['L417','L418']),dict(country='Франция',date='19.06.2027',title='Paris · VivaTech public day',detail='Дата публичного дня подтверждена; детские билеты / возраст 2027 уточнить. Общий four-day B2B pass предназначен профессионалам.',event_ids=['E184'])]
for pick in f['family_picks']:
 if pick['kind']=='camp' and pick['country']=='Швейцария':
  pick['why']+=' На лето 2027 Матвею HIF Ftan на EN с пансионом после 10-летия; Оскару нужен отдельный младший дневной вариант.'
  pick['gate']+=' HIF: даты рождения и часы робототехники проверить; это смешанная программа.';pick['event_ids']+=['L417','L418'];pick['source_urls'].append(urls['hif'])
 if pick['kind']=='camp' and pick['country']=='Испания':
  pick['why']+=' EISB Science July 2027 явно EN, но опубликованные рождения исключают Оскара2020.'
  pick['gate']+=' EISB: точные недели и цены 2027 не установлены; Chess & Robotics EN неизвестен.';pick['event_ids']+=['L420','L421'];pick['source_urls'].append(urls['eisb_science'])
 if pick['kind']=='school' and pick['country']=='Испания':
  pick['why']+=' EISB Sant Cugat — ещё один Cambridge / EN-кандидат, не доказанная чемпионская школа.';pick['school_ids'].append('S049');pick['source_urls'].append(urls['eisb_primary'])
 if pick['kind']=='league' and pick['country']=='Франция':
  pick['gate']+=' MJC Blagnac: регулярная команда только 12+, младшая мастерская отдельно.';pick['event_ids']+=['L423','L424']
for b in f['base_comparison']:
 if b['iso']=='ESP':b['school_ids'].append('S049');b['school']+=' EISB Sant Cugat — Cambridge Primary / PY1 65% English, текущий младший соревновательный состав ещё проверить.'
 if b['iso']=='CHE':b['trial']+=' HIF Ftan летом 2027 на EN с пансионом — только Матвею после 10-летия, не общая смена братьям.';b['event_ids']+=['L417','L418']
 if b['iso']=='FRA':b['gate']+=' MJC Blagnac имеет мастерскую 8–11, но регулярную команду 12+; технический EN ещё не установлен.'
read_keys=[k for k in urls if k not in ['aiglon_brochure','wro_swiss_2027','vivatech_public_faq']]
known={s['url']for s in d['sources']};knownf={s['url']for s in f['sources']}
for key in read_keys:
 if urls[key]not in known:d['sources'].append(dict(url=urls[key],title='Первичный источник · '+key,checked=CHECKED,evidence='Прочитано тело первичной страницы; возраст, язык, этап и конфликты раздельно.'));known.add(urls[key])
 if urls[key]not in knownf:f['sources'].append(dict(title='Европа: углублённая проверка · '+key,url=urls[key],checked=CHECKED));knownf.add(urls[key])
issues=[dict(name=name,status=status,official_alternative=urls[key],checked=CHECKED)for name,status,key in [
 ('EISB camp year / cutoff','July2027 headers coexist with 2026 earlybird and price chart; birth2012–2019 excludes2020; exactweeks androbotics EN unknown.','eisb_robotics'),
 ('VivaTech current public day versus old family copy','2027 terms specify June19 public day; general-public body has older Saturday June17/18. Child tickets / min age 2027 unconfirmed.','vivatech_b2b'),
 ('Club month versus official regional date','MJC says April2027; organizer says March27. Official day retained; masterclass8–11 differs from team12+.','occitanie_2027'),
 ('FIRST 2025 list ordinals','RobotPerformance disjoint HTML lists carry data-aria-posinset 2/3; rendered text restarts at1. Original ordinal verified.','first_2025'),
 ('Swiss WRO participant-count inconsistency','Total and age-subcategory participant counts conflict; podium / world routing used, no invented participant total.','wro_swiss_results'),
 ('Aiglon junior / camp minimums','Junior introduction7–11 versus panel6–11 persists; overall daycamp7 differs from robotics8. WonderYears English explicit.','aiglon_junior'),
 ('WRO guessed 2027 path','Guessed saison-2027 path returned404. This is not proof that 2027 events do not exist; no dates inferred.','wro_swiss_2027')]]
a=d['completeness_audit'];a['validation_previous']=copy.deepcopy(a['validation']);a.update(version=47,checked=CHECKED,scope='CHE/ESP/FRA: actual 2027 residential / day camps, school language, bounded podiums and child admission',conclusion='12 новых карточек, одно школьное досье, 9 результатов с точными уровнями. Дата, язык, возраст и профессиональный пропуск проверены отдельно; мировой охват остаётся частичным.',new_ids=[e['id']for e in new],new_profiles=[],new_school_ids=['S049'],updated_ids=['E102','C918'],updated_profile_ids=[],validation=dict(version=47,status='pending',publication='pending'))
a['school_history']['results']=146;a['source_issues']+=issues;a['caveats'].append('v47: HIF minimum10 на начало смены; Aiglon robotics8 не общий day7; EISB summer cutoff2019 исключает2020. VivaTech отдельный public day не подтверждает детский билет. Новые podiums и национальные победы не мировой общий рейтинг школ.')
d['camp_focus'].update(version=47,checked=CHECKED,added_ids=[e['id']for e in new if e['block']=='Лагеря'],updated_ids=[],conclusion='HIF: две реальные EN-пансионные смены2027 для10–16; EISBScience EN отдельно от Chess&Robotics; остальные даты / технический язык явно не подтверждены.',validation=dict(version=47,status='pending'))
d['school_focus'].update(version=47,checked=CHECKED,conclusion='49 школьных досье. EISB — Cambridge Primary / PY1 65% English; Aiglon WonderYears EN подтверждён. Младшие мировые школьные титулы не приписаны по программе / независимой команде.')
d['asof']=CHECKED;d['expansion_log'].append(dict(version=47,checked=CHECKED,scope='CHE/ESP/FRA camps, school evidence, podiums and visit gates',added=12,new_schools=1,new_history=9,status='partial; worldwide objective preserved'))
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=[]
for name in ['receipt.json','receipt-extra.json','receipt-last.json']:
 for row in json.loads((WORK/'sources-europe-deep-v47'/name).read_text()):
  row.pop('path',None);key=row['name'];row['primary_body_read']=key in read_keys
  if key in ['vivatech_b2b','vivatech_public','fsingenium_school']:row['alternate_read']='Primary body read with web tool after local HTTP failure.'
  if key=='aiglon_brochure':row['limitation']='HTTP200 flipbook shell only; brochure contents / prices not verified.'
  if key=='eisb_prices_2026':row['alternate_read']='Image visually inspected; header explicitly2026, not reused as2027 prices.'
  receipts.append(row)
(ROOT/'data/europe-deep-source-receipts-v47.json').write_text(json.dumps(dict(version=47,checked=CHECKED,sources=receipts,issues=issues),ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r.update(updated=CHECKED,completeness_audit='data/audit-v47.json',latest_validation_previous=r['latest_validation'],latest_validation=dict(version=47,status='pending',publication='pending'))
r['research_passes'].append(dict(version=47,checked=CHECKED,scope='User-requested Switzerland / Spain / France deeper actual camp / school / results / visitor audit',status='implementation; validation pending',added=12,new_schools=1,new_history_results=9))
r['previous_goal_turn_classification']=dict(status='progress',evidence='v46 deployed; anonymous byte hashes matched all 78 static files, UI / calendars verified.',remaining='The global calendar objective remains active; country coverage partial.')
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=47,cards=len(d['events']),schools=len(d['schools']),history_results=len(h['results']),new_ids=[e['id']for e in new]),ensure_ascii=False))
