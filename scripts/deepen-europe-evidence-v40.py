"""CHE / ESP / FRA: verify the route from current teaching to actual team results."""
import ast, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT.parent / 'stem-family-atlas-work'
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert len(d['events']) == 1576 and d['completeness_audit']['version'] == 39
CHECKED = '2026-10-02'
new = []
byid = {e['id']: e for e in d['events']}
for node in ast.parse((ROOT / 'scripts/expand-oceania-v29.py').read_text()).body:
    if isinstance(node, ast.FunctionDef) and node.name in ['ref', 'event']:
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'helpers', 'exec'))
u = json.loads((W / 'urls-europe-evidence-v40.json').read_text())
u.update(json.loads((W / 'urls-europe-evidence-extra-v40.json').read_text()))
u.update(json.loads((W / 'urls-europe-camp-v40.json').read_text()))
u.update(json.loads((W / 'urls-europe-stage-v40.json').read_text()))

def learning(id, title, country, city, source, age, mat, osc, entry, gear, cost, note, languages=(), mode='unconfirmed'):
    e = event(id, title, country, city, source, age, mat, osc, entry, gear,
        block='Лагеря', participation='day_camp', evidence='program',
        cost=cost, note=note, languages=languages,
        priority='P2 — проба после проверки группы' if 'EN' in languages else 'P4 — язык / допуск группы уточнить')
    e.update(region='Европа', participation='regular', format='Регулярная внешкольная программа',
        language_mode=mode, period='Учебный цикл 2026/27; точный доступный слот и позднюю запись подтвердить')
    if languages:
        e['language']='Опубликованы '+ '/'.join(languages) + '; язык выбранного потока и возможность учиться без французского отдельно подтвердить.'
        e['language_certainty']='Язык подтверждён в описании именно этой программы; свободное место не подтверждено.'
    return e

e=learning('L354','Robo Matik · Sport-Robotik · подготовка WRO / FLL 9–15',
    'Швейцария','Ennetbaden · Baden',u['robomatik_sport'],'9–15; продвинутый уровень',
    'Условно: подходит по возрасту; нужен assessment уровня и язык группы','Нет: минимум 9 лет',
    'Текущий план 2026/27: RoboSport в понедельник / четверг; Teams Time по субботам. Условия включения в команду отдельно.',
    'LEGO EV3 / SPIKE / Robot Inventor, Python, алгоритмы, тестирование и командная работа.',
    'Текущая стоимость соревновательной подготовки не установлена',
    'BFH подтверждает первое место Robomatik Titans в Elementary на региональном этапе Biel2025. Это не мировой титул и не подтверждение школы или языка клуба.')
e['references']=[ref('Текущее расписание',u['robomatik_hours']),ref('Организатор регионального этапа Biel2025',u['biel_2025'])]
e=learning('L355','Robo Matik Schule · младшая регулярная робототехника',
    'Швейцария','Ennetbaden · Baden',u['robomatik_faq'],'FAQ: 6–9 для младших; текущий Modul0 отдельно 4–5',
    'Условно: выбрать модуль по уровню и текущему расписанию','Условно: 6 лет по FAQ; Modul0 для 4–5 не подходит',
    'Учебные годовые модули; группы 4–12. Точную текущую возрастную границу выбранного модуля и язык подтвердить.',
    'Младшие WeDo2.0, далее EV3 / SPIKE / Arduino; самостоятельная сборка и код.',
    'Цена выбранного модуля не установлена',
    'FAQ включает Modul0 в 6–9, а его новая страница2026/27 указывает 4–5. Это расхождение сохранено; вводный курс может быть слишком прост после трёх лет опыта.')
e['references']=[ref('Modul0: актуальные 4–5',u['robomatik_zero']),ref('Расписание2026/27',u['robomatik_hours'])]

e=learning('L356','Tech Kids Academy · 5–6 · двуязычные регулярные занятия 2026/27',
    'Франция','Paris15 · 6 rue Valentin Haüy',u['kids5'],'5–6; GSM / CP',
    'Нет: отдельная группа 7–9','Условно: возраст подходит; класс и сложность проверить',
    '27 занятий по 60 минут; публичная запись. Старт цикла уже прошёл; поздний вход и возможность следовать на EN уточнить.',
    'Роботы Botzee / Tale-bot, логика, анимация и графика; вводный уровень.',
    'EUR640/год + EUR45 за заказ; опубликованная скидка второго ребёнка 5%, итог уточнить',
    'Именно bilingual FR/EN, а не обещание отдельного полного EN-потока. Сертификат участия не является наградой соревнований.',('FR','EN'),'bilingual')
e=learning('L357','Tech Kids Academy · 7–9 · регулярный технический поток EN / FR 2026/27',
    'Франция','Paris15 / Saint-Germain-en-Laye',u['kids7'],'7–9; CE1 / CE2 по описанию',
    'Условно: возраст9 подходит, класс CE1/CE2 и уровень отдельно','Нет: 6 ниже минимума7',
    '27 занятий по 90 минут; программа предлагается на FR и EN. Выбрать именно EN-поток, подтвердить расписание и класс.',
    'Scratch, LEGO WeDo2.0 / Ozobot, LittleBits, micro:bit и 3D-дизайн.',
    'От EUR775/год + EUR45 за заказ; скидки / конкретный поток уточнить',
    'Вводная программа; для опытного Матвея нужна проверка сложности. EN этого годового курса не перенесён на каникулярный лагерь того же оператора.',('EN','FR'),'primary')

for id,title,age,mat,osc,gear in [
    ('L358','Robótica I','5–7; рядом опубликованы годы2018–2019', 'Нет по диапазону5–7', 'Условно: возраст6 подходит; рождение2020 отсутствует в опубликованных годах', 'LEGO, простые моторы / сенсоры и код.'),
    ('L359','Robótica II','7–9; рядом годы2016/2017', 'Условно: возраст9 / рождение2017; группа и уровень отдельно', 'Нет: ниже7', 'Прототипы, исследование, командная работа; на этой ступени формируют группы FLL / WRO.'),
    ('L360','Robótica de Competición','10–16; рядом годы2009/2015', 'Будущая ступень после10-летия2027; новый набор неизвестен', 'Нет: ниже10', 'LEGO-роботы и подготовка FIRST LEGO League / WRO.')]:
    e=learning(id,'TECNISTEM Cáceres · '+title+' · регулярная программа',
        'Испания','Cáceres',u['tecnistem_regular'],age,mat,osc,
        '90 минут один день в неделю. До записи согласовать текущие birth-year / grade условия, технический ES и foreign-family приём.',
        gear,'EUR30 matrícula + EUR65/месяц на странице; число платных месяцев и турнирные расходы уточнить',
        'Возраст и годы рождения на странице не полностью согласованы с2026/27. ES не подтверждён отдельно от языка сайта. Академия — внешкольный клуб, не общеобразовательная школа.')
    e['references']=[ref('Команды / собственное описание результатов',u['tecnistem_results']),ref('Национальный протокол2026',u['spain_results'])]

for id,start,end in [('L361','2026-10-19','2026-10-20'),('L362','2026-10-21','2026-10-22')]:
    e=event(id,'MPT Saint-Ismier · Multi Robots · '+start,
        'Франция','Saint-Ismier · salle Grand Pic, bâtiment Belledonne',u['mpt_camps'],'9–12 лет',
        'Условно: возраст9 подходит; EN / ES и уровень неизвестны','Нет: минимум9',
        'Два дня09:00–16:30; публичная запись HelloAsso, до7 детей; visiting-family и язык уточнить.',
        'Сборка и программирование четырёх роботов; компьютер / набор предоставляются.',
        block='Лагеря',participation='day_camp',start=start,end=end,date_scope='camp_window',
        priority='P4 — EN / ES не установлены',cost='EUR165 за двухдневную смену; холодный обед с собой',
        note='Две даты — две смены одного оператора. На странице ошибочно осталось слово juillet, но обе явные даты относятся к октябрю2026; четырёхдневное окно не выдано за одну смену.')
    e['region']='Европа'

for id,start,end in [('L363','2026-10-19','2026-10-23'),('L364','2026-10-26','2026-10-30')]:
    e=event(id,'Tech Kids Academy · LEGO / Ozobot · Toussaint · '+start,
        'Франция','Paris15 / Saint-Germain-en-Laye · выбрать площадку',u['kids_stage'],'7–10; мотивированным CP предлагается отдельно обратиться',
        'По возрасту подходит; курс начальный и идёт на FR','Ниже обычного7; исключение CP не является подтверждённым приёмом',
        'Пять полудней13:30–16:00; публичная запись. Компьютер и набор предоставляются.',
        'WeDo2.0 / Ozobot: моторы, сенсоры и собственный финальный проект.',
        block='Лагеря',participation='day_camp',start=start,end=end,date_scope='camp_window',languages=('FR',),
        language='В карточке именно этого лагеря указан Français; EN не заявлен.',
        priority='P4 — французский; EN группы не подтверждены',cost='От EUR215; вариант / итоговый тариф уточнить',
        note='Две смены, каждая доступна на двух площадках. Регулярный EN-курс этого оператора не доказывает EN-лагерь; начинающий формат требует проверки уровня.')
    e.update(region='Европа',language_mode='primary',language_certainty='FR прямо указан у этой смены; EN не подразумевается.')

e=byid['C085']
e.update(checked=CHECKED,city='Craon · точная площадка2027 требует подтверждения',
    age='Глобальный a-MAZE-ing8–15; host: collège / lycée, младший день CM1–CM2 /6e местной Pays de Craon',
    mat='Не подтверждено: возраст сам по себе недостаточен; нужны класс и исключение местного ограничения младшего дня',
    osc='Нет по обычному a-MAZE-ing8–15 и младшей школьной ступени; отдельное исключение не подтверждено',
    format='Команда; младший местный день описан для4 детей; общий формат2027 ещё подтвердить',
    entry='Международный портал объявил3июня2027; host пока описывает2026. Основной турнир открыт миру для collège / lycée. Доступ зарубежной Primary-команды согласовать.',
    language='Host описывает English presentation; это не обещание всех судейских коммуникаций на EN.',
    proof='Прочитаны международная дата2027 и конкретные школьные / местные условия принимающего организатора; правила2026 не названы новыми правилами2027.',
    note='Исправлен прежний вывод «Матвею да по возрасту». Primary-день описан для местных CM1–CM2 и6e; будущий иностранный Primary-допуск неизвестен. Международный Open не является мировым финалом.')
e['references'] += [ref('Организатор: реальная школьная ступень и English presentation',u['roborave_host'])]

def school(id,name,iso,country,city,ages,programme,sources,**extra):
    s=dict(id=id,name=name,iso=iso,country=country,region='Европа',city=city,school_type='private',
        curriculum='',ib_programmes=[],ages=ages,instruction_languages=['EN'],language_note='EN школьное обучение подтверждено; язык конкретной robotics-команды отдельно.',
        fit=dict(mat='candidate',osc='candidate',note='Точные классы, места и действующий младший наставник не установлены.'),
        boarding='unknown',boarding_note='Младший пансион6/9 не подтверждён; семейное проживание отдельно.',
        programme=programme,labs='',ai='Конкретный постоянный младший AI-трек не установлен.',results=[],evidence='programme',
        admissions='Проверить класс, документы, оценку уровня и места; опубликованная программа не подтверждает приём.',
        cost='Текущую цену и полный бюджет уточнить',questions=['Какой team code и наставник именно6/9, часы работы и протоколы последних3–5сезонов?','Можно ли сначала проверить уровень и место каждому ребёнку?'],
        sources=[dict(title=title,url=url,claim=claim,kind='school',checked=CHECKED) for title,url,claim in sources],checked=CHECKED,priority=2,
        research_status='partial',verification='Первичные школьные источники; самостоятельная программа младших и результат старших разделены.')
    s.update(extra);d['schools'].append(s);return s
s=school('S037','TASIS · The American School in Switzerland','CHE','Швейцария','Montagnola · Lugano',
    'Pre-K с3лет – Grade5; placement обоим подтвердить',
    'English Elementary; у школьной Middle School команды1828A подтверждён школьный отчёт о национальной VEX IQ награде и квалификации2026.',
    [('English Elementary',u['tasis_elementary'],'EN,Pre-K3–Grade5'),('VEX IQ2026',u['tasis_result'],'1828A,Robot Skills Champion,выход на Worlds'),('Tuition2026/27',u['tasis_fees'],'CHF34000/K–G5')],
    curriculum='Американская начальная Core Knowledge; AP / IB старших не перенесены на Primary.',
    labs='Две science laboratories в Elementary; текущий доступ к robotics6/9 и нагрузку кружка подтвердить.',
    evidence='national_result',cost='2026/27: K–Grade5 CHF34000/ребёнок/год. Если оба на этой ступени: CHF68000 tuition. Application CHF1250/ребёнок, enrollment depositCHF3000/ребёнок; campus fundCHF5000 сGrade1. Не складывать deposit с tuition без правил зачёта.')
s['results']=[dict(season='2026',league='VEX IQ',stage='Swiss qualifier · Basel · Middle School',award='Robot Skills Champion; квалификация на World Championship',team='TASIS Tigers',team_id='1828A',source=u['tasis_result'],provenance='school_report',limit='Рассказ школы о7–8февраля2026; участие / квалификация не названы мировой победой. Младшая Elementary-команда этим результатом не доказана.')]
s=school('S038','Marymount International School Paris','FRA','Франция','Neuilly-sur-Seine',
    'Early Learners2–6; Elementary7–11 / Grades1–5',
    'English education и FabLab. STEM ASA2026/27: T1 Grades4–6; T2 Grades2–3. LEGO Workshop отдельно Kindergarten–Grade1.',
    [('English school',u['marymount_services'],'EN основной язык'),('Early Learners',u['marymount_early'],'2–6,EN'),('Elementary',u['marymount_elementary_current'],'7–11,EN'),('Digital / FabLab',u['marymount_fablab'],'fabrication / robotics'),('Current ASA',u['marymount_asa'],'конкретные классы и триместры')],
    curriculum='Международный AERO / американские стандарты; IB-авторизация не установлена.',
    labs='FabLab с электроникой,3D,laser cutting и robotics по описанию школы; доступ младших и часы отдельно.',
    cost='ASA2026/27 EUR200 за триместр; это не school tuition. Полная школьная плата в прочитанных источниках не установлена.')
s['fit']['note']='Матвею подходит Elementary по возрасту. Оскару Early Learners2–6; класс Kindergarten / Grade1 и STEM-ступень нельзя вывести только из рождения2020.'
s['questions'].append('Какой exactgrade и ASAтриместр дадут каждому? Инженерная LEGO-мастерская не равна мировому соревновательному клубу.')

h=d['school_history']
entities=[
    dict(id='S037',name='TASIS',kind='school',country='Швейцария',age='secondary',school_id='S037',note='Проверенный результат относится к Middle School, не Elementary.'),
    dict(id='CHE-ROBOMATIK',name='Robomatik · клуб / команды',kind='club',country='Швейцария',age='primary',school_id=None,note='Связь с общеобразовательной школой не установлена; конкретные результаты по названиям команд.'),
    dict(id='CHE-SWISSFIRE',name='Swiss Fire',kind='unresolved',country='Швейцария',age='primary',school_id=None,note='Команда национального Elementary; школа / клуб неизвестны.'),
    dict(id='ESP-TECHNOBROS',name='TECHNOBROS',kind='unresolved',country='Испания',age='primary',school_id=None,note='Национальный результат; название не является названием школы.'),
    dict(id='ESP-CRABGIRLS',name='CRABGIRLSCLUB',kind='unresolved',country='Испания',age='primary',school_id=None,note='Не приписана Colegio Aldovea только потому, что школа организовала местный этап.'),
    dict(id='ESP-TECNISTEM',name='TECNISTEM · Cáceres',kind='club',country='Испания',age='mixed',school_id=None,note='Внешкольная академия; Junior / RoboSports результаты старших не доказательство допуска6/9.')]
h['entities'].extend(entities)
for id,entity,year,league,category,stage,award,level,source,team,team_id,provenance,note in [
    ('H119','S037',2026,'VEX','IQ Middle School','Swiss qualifier · Basel','Robot Skills Champion; Worlds qualification','national_skills',u['tasis_result'],'TASIS Tigers','1828A','school_report','Школьный отчёт; qualification не мировой титул и не результат Elementary.'),
    ('H120','CHE-ROBOMATIK',2025,'WRO','RoboMission Elementary','Biel regional','1-е место; выход в Swiss Final','regional_match',u['biel_2025'],'Robomatik Titans',None,'organizer_protocol','BFH как принимающий организатор; не нац./мировая победа.'),
    ('H121','CHE-SWISSFIRE',2026,'WRO','RoboMission Elementary','Swiss National Final','1-е место; квалификация на International Final','national_match',u['swiss_results'],'Swiss Fire',None,'organizer_protocol','497points. Школа / клуб не указаны; Worlds ещё впереди.'),
    ('H122','ESP-TECHNOBROS',2026,'WRO','RoboMission Elementary','Spain National Final','1-е место','national_match',u['spain_results'],'TECHNOBROS',None,'organizer_protocol','Организатор подтверждает место, аффилиация школы / клуба не установлена.'),
    ('H123','ESP-CRABGIRLS',2026,'WRO','Future Innovators Elementary','Spain National Final','1-е место','national_match',u['spain_results'],'CRABGIRLSCLUB',None,'organizer_protocol','Host местного турнира не является доказательством школы команды.'),
    ('H124','ESP-TECNISTEM',2026,'WRO','RoboBasic','Spain National Final','3-е место','national_match',u['spain_results'],'SNAKE BOTS T-STEM',None,'organizer_protocol','Собственная страница клуба связывает SnakeBots сTECNISTEM; местное1-е и национальное3-е — разные этапы.'),
    ('H125','ESP-TECNISTEM',2026,'WRO','Future Innovators Junior','Spain National Final','1-е место','national_match',u['spain_results'],'ARQUEOPIXELS T-STEM',None,'organizer_protocol','Связь академии по собственному рассказу; Junior — отдельная старшая категория.'),
    ('H126','ESP-TECNISTEM',2026,'WRO','RoboSports','Spain National Final','1-е место','national_match',u['spain_results'],'PIXEL SPORTS T-STEM',None,'organizer_protocol','Связь академии по собственному рассказу; не младшая Elementary категория.')]:
    h['results'].append(dict(id=id,entity_id=entity,year=year,league=league,category=category,stage=stage,award=award,level=level,source=source,team=team,team_id=team_id,provenance=provenance,note=note,checked=CHECKED))
h.update(version=40,checked=CHECKED,conclusion='126 отдельных результатов. Новые CHE / ESP протоколы точно разделяют региональный / национальный этапы, Middle School / Elementary и qualification / мировой титул. Полный5–10летний рейтинг школ трёх стран не установлен.')
h['gaps'].append('v40 CHE/ESP/FRA: школы SwissFire,TECHNOBROS,CRABGIRLSCLUB неизвестны; RoboRAVE Primary foreign entry не подтверждён. Нет полного5–10летнего младшего школьного рейтинга.')

f=d['europe_focus'];f.update(version=40,checked=CHECKED)
f['evidence_cards']=[
    dict(title='Испания · реальные национальные Elementary-лидеры2026',detail='TECHNOBROS — RoboMission; CRABGIRLSCLUB — Future Innovators. Названия подтверждены организатором; школу / нынешнего наставника ещё установить.',limit='Национальный результат не мировой титул. Colegio Aldovea как host не доказывает школу CRABGIRLSCLUB.',event_ids=['C911'],school_ids=[],source_urls=[u['spain_results']]),
    dict(title='Испания · клуб вместо смены школы вслепую',detail='TECNISTEM: национальное3-е RoboBasic и первые Junior / RoboSports2026. Есть младшие учебные группы; возрастные годы на странице расходятся.',limit='Нужен пробный урок и подтверждение ES. Академия не постоянная общеобразовательная школа.',event_ids=['L358','L359','L360'],school_ids=[],source_urls=[u['tecnistem_regular'],u['spain_results']]),
    dict(title='Швейцария · сильная команда ещё не означает младший доступ',detail='TASIS1828A получил Robot Skills Champion на швейцарском отборе2026 и квалификацию на Worlds, по рассказу школы. Робоматика Titans — региональный Elementary победитель Biel2025.',limit='TASIS результат Middle School. У Robomatik EN/ES не установлен. SwissFire выиграл национальный Elementary2026, школа неизвестна.',event_ids=['L354','L355'],school_ids=['S037'],source_urls=[u['tasis_result'],u['biel_2025'],u['swiss_results']]),
    dict(title='Франция · годовой EN-курс и FR-каникулы различаются',detail='Tech Kids5–6: bilingualFR/EN;7–9: отдельныеFR/ENпотоки. Каникулярный LEGO/Ozobot7–10 прямо указан на французском.',limit='Для опытных детей проверить уровень. Английский годового курса не перенесён на лагерь; Оскар ниже обычного7лет.',event_ids=['L356','L357','L363','L364'],school_ids=[],source_urls=[u['kids5'],u['kids7'],u['kids_stage']]),
    dict(title='Франция · English школа и точные STEM-классы',detail='Marymount: EN, FabLab; STEMтриместр1 дляGrades4–6, триместр2 дляGrades2–3. Младший LEGO отдельноKindergarten–Grade1.',limit='Лаборатория — подтверждённая программа; мировой результат команды6/9 не установлен. Класс и место проверить до выбора школы.',event_ids=[],school_ids=['S038'],source_urls=[u['marymount_elementary_current'],u['marymount_asa']])]
countries={c['iso']:c for c in f['countries']}
for iso,ids in [('CHE',['L354','L355']),('ESP',['L358','L359','L360']),('FRA',['L356','L357','L361','L362','L363','L364'])]:countries[iso]['event_ids']+=ids
countries['CHE']['school_ids'].append('S037');countries['FRA']['school_ids'].append('S038')
countries['CHE']['school']+=' TASIS Lugano: English Elementary; опубликована Middle School VEX IQ1828A qualification2026, младшая команда6/9 отдельно.'
countries['CHE']['city_route']+=' Ennetbaden / Baden: Robo Matik9–15для Матвея и младший модуль для Оскара, EN/ES неизвестны. Lugano: TASIS семейный day-кандидат.'
countries['CHE']['budget']+=' TASIS K–Grade5: CHF68000tuition/год за двоих; application, deposit и campus fund отдельно, правила зачёта deposit неизвестны.'
countries['CHE']['results_check']+=' SwissFire —1-е Elementary2026, школа неизвестна. Robomatik Titans —1-е ElementaryBiel2025, региональный этап.'
countries['ESP']['city_route']+=' Cáceres: пробаTECNISTEM, затем выбрать школу по семье; результаты Junior/RoboSports не переносить на6/9.'
countries['ESP']['results_check']+=' Национальные Elementary2026: TECHNOBROS(RM),CRABGIRLSCLUB(FI); школа/клуб не установлены. TECNISTEMSnakeBots3-е RoboBasic, а местное1-е относится к другому этапу.'
countries['ESP']['risk']+=' TECNISTEM: возраст5–7 не совпадает с годами2018–2019; рождение2020 Оскара требует прямого подтверждения.'
countries['FRA']['camp']+=' Tech Kids Academy добавлен как year-round bilingual5–6 /EN7–9; лагеряLEGO7–10наFR. MPT Saint-Ismier9–12:19–20/21–22октября,EN/ES неизвестен.'
countries['FRA']['school']+=' Marymount Neuilly:EN EarlyLearners2–6/Elementary7–11,FabLab и классовыеASA2026/27; младший мировой титул не установлен.'
countries['FRA']['risk']+=' RoboRAVE Craon2027: дата есть, но младший день host2026 описан для местныхCM1–CM2/6e; возраст8–15 не даёт свободный Primary-допуск.'
f['limitations']='Шестой ограниченный проход CHE/ESP/FRA:185 карточек, включая регулярные курсы и разные смены операторов;16 школьных досье. Проверены новые первичные протоколы2025/26 и реальные языковые / классовые условия. Все национальные календари и5–10летний рейтинг младших школ не установлены.'
f['conclusion']='Для семьи первый европейский кандидат базы остаётся Испания: выбирать наставника Elementary и младшую дорожку Оскара. Швейцария даёт конкретную подготовку VEX на английском и новый школьный кандидат TASIS, но сильный результат средней школы не гарантирует младший доступ. Во Франции есть подтверждённые английские и двуязычные регулярные программы и школы; язык и класс выбранного лагеря проверяются отдельно.'

for key in ['sources']:
    existing={s['url']:s for s in d[key]}
    for name,url in u.items():
        if name in ['robomatik_module0','marymount_elementary','marymount_fees','palencia','palencia_retry']:continue
        if url in existing:existing[url]['checked']=CHECKED
        else:d[key].append(dict(url=url,title=name,checked=CHECKED,evidence='Прочитан первичный источник; текущий возраст / язык, школьный отчёт и организаторский протокол разделены.'))
for name in ['roborave_host','swiss_results','robomatik_sport','robomatik_hours','biel_2025','tasis_result','tasis_elementary','tasis_fees','spain_results','tecnistem_regular','marymount_services','marymount_elementary_current','marymount_asa','kids5','kids7','kids_stage','mpt_camps']:
    if u[name] not in {s['url'] for s in f['sources']}:f['sources'].append(dict(title=name,url=u[name],checked=CHECKED))
d['events'].extend(new)
d['school_focus'].update(version=40,checked=CHECKED,conclusion='38 школьных досье. Добавлены TASIS: английская начальная школа и VEX-квалификация команды средней школы; Marymount: английское обучение, FabLab и STEM по конкретным классам. Мировые результаты младших команд этих школ не установлены.')
d['school_focus']['routes'].append(dict(name='Швейцария / Франция · EN база и отдельный младший наставник',ids=['S037','S038'],detail='TASIS: действующая VEX Middle School команда, младший доступ отдельно. Marymount:FabLab и STEMпо классу/триместру, подтверждённых мировых наград6/9 нет.'))
a=d['completeness_audit'];a['validation_previous']=a['validation']
a.update(version=40,checked=CHECKED,status='partial',scope='CHE/ESP/FRA: реальные команды и первичные результаты, языковые / классовые ограничения младших',
    conclusion='11 дополнительных учебных карточек,2школы,8конкретных результатов; исправлен условный допускRoboRAVEFrance.185карточек трёх стран; мировой охват частичный.',
    new_ids=[e['id'] for e in new],new_profiles=[],updated_ids=['C085'],updated_profile_ids=[],new_school_ids=['S037','S038'],validation=dict(version=40,status='pending',publication='pending'))
a['source_issues'].append(dict(name='RoboRAVE host / course-language / birth-year conflicts',status='Craon Primary locally gated; TechKids EN regular versus FR camp; TECNISTEM ages conflict with published birth years; Robomatik FAQ versus current Modul0 age retained.',official_alternative=u['roborave_host'],checked=CHECKED))
d['camp_focus']['validation_previous']=d['camp_focus']['validation']
d['camp_focus'].update(version=40,checked=CHECKED,added_ids=[e['id'] for e in new],updated_ids=[],validation=dict(version=40,status='pending'),conclusion='364 лагерных и учебных карточки. Добавлено 11 программ Швейцарии, Испании и Франции: семь регулярных и четыре короткие смены с датами. Английский подтверждён у двух регулярных программ Tech Kids; их язык не перенесён на французский лагерь.')
d['expansion_log'].append(dict(version=40,checked=CHECKED,added=11,updated_ids=['C085'],note='CHE/ESP/FRA junior routes: actual school-stage gates, two EN schools, eight bounded results and provider-specific camp language.'))
def readable(value):
    if isinstance(value, dict):
        return {key: item if key in ['id','entity_id','school_id','team_id','source','url','source_urls','event_ids','school_ids','profile_ids','related_ids'] else readable(item) for key,item in value.items()}
    if isinstance(value, list): return [readable(item) for item in value]
    if not isinstance(value, str) or value.startswith('http'): return value
    value=re.sub(r'(?<=[А-Яа-я])(?=[A-Za-z0-9])',' ',value)
    value=re.sub(r'(?<=[A-Za-z0-9])(?=[А-Яа-я])',' ',value)
    value=re.sub(r'(?<=[A-Za-z])(?=20\d{2})',' ',value)
    value=re.sub(r'([,;])(?=[^\s\d])',r'\1 ',value)
    for before,after in [('ENElementary','EN Elementary'),('EnglishElementary','English Elementary'),('ENPrimary','EN Primary'),('MiddleSchool','Middle School'),('EarlyLearners','Early Learners'),('SchoolVEX','School VEX'),('bilingualFR','bilingual FR'),('ElementaryBiel','Elementary Biel'),('TechKids','Tech Kids'),('5–10лет','5–10 лет'),('6/9лет','6/9 лет'),('CHF34000','CHF 34 000'),('CHF68000','CHF 68 000'),('CHF5000','CHF 5 000'),('CHF3000','CHF 3 000'),('CHF1250','CHF 1 250')]:value=value.replace(before,after)
    return value
new_ids={e['id'] for e in new}
d['events']=[readable(e) if e['id'] in new_ids or e['id']=='C085' else e for e in d['events']]
d['schools']=[readable(s) if s['id'] in ['S037','S038'] else s for s in d['schools']]
d['school_history']['results']=[readable(r) if int(r['id'][1:])>=119 else r for r in h['results']]
d['europe_focus']=readable(f)
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=[]
for file in ['receipt.json','receipt-extra.json','receipt-camps.json','receipt-stage.json']:
    rows+=json.loads((W/'sources-europe-evidence-v40'/file).read_text())
(ROOT/'data/europe-evidence-source-receipts-v40.json').write_text(json.dumps(dict(checked=CHECKED,method='Primary HTML read; raw material outside repo. Failed guesses retained as fetch gaps, not confirmed sources.',sources=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in rows]),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v40.json')
r.setdefault('research_passes',[]).append(dict(version=40,checked=CHECKED,scope='CHE/ESP/FRA school-age and language gates with bounded primary results',added_records=11,new_profiles=0,new_schools=2,new_school_results=8,status='partial',remaining='Exactgrades,birthdays,teamplaces,foreignquota,allnationalcalendarsand5–10yearschoolranking;fullworldcoverage'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=40,status='local_checks_pending_publication_pending')
for requirement in r['requirements']:
    if requirement['id']=='unified_database':requirement['evidence']='v40: 1587 records; 120 league profiles, 38 schools, 126 history results. CHE/ESP/FRA: 185 records and 5 interactive evidence cards.'
    if requirement['id']=='camps':requirement['evidence']='v40: 364 camp/learning records. Seven new regular programmes and four dated French sessions; EN regular courses are distinguished from FR holiday camps.'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=40,added=11,total=len(d['events']),schools=len(d['schools']),history=len(h['results']),world_complete=False)))
