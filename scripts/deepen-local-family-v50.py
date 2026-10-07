"""Bounded primary-source Mexico / Costa Rica junior season pass."""
import ast, copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED='2026-10-02'
p=ROOT/'data/catalog.json';d=json.loads(p.read_text())
assert d['completeness_audit']['version']==49 and len(d['events'])==1759
urls=json.loads((WORK/'urls-local-deep-v50.json').read_text())
new=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event']:
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))

sumo_conflict='Общая convocatoria от 01.09.2026: 15 см / 1 кг; связанный технический PDF от 19.05.2025: 20 см / 2 кг. Действующие пределы homologación требуется письменно уточнить: старую техническую таблицу нельзя считать правилом 2026.'
lati_note='Junior — Primaria / Secundaria; школьная справка обязательна. До 2 учеников + совершеннолетний asesor, которым может быть родитель. Смешанные школы разрешены, наивысший класс определяет дивизион. В pits входят только участники: взрослым запрещены вход и общение с ними. Самостоятельность Оскара особенно проверить. Минимум 4 команды для открытия категории. Первая jornada 9 октября; дата второй не установлена, окно 9–30 октября не превращено в непрерывный турнир. Закрытие новых команд за 5 дней: 4 октября вычислено из правила, час и отсечение подтвердить. Победитель сезона получает скидку на региональный RoboMatrix: 100% при более 5 участниках, 50% при 5 или менее; это не мировой финал.'
for number,title,gear,themes in [
 (1124,'Sumo LEGO','Автономный LEGO-робот; стартовая задержка 5 секунд. '+sumo_conflict,('robotics','coding')),
 (1125,'Seguidor de línea Kits','Автономный проход чёрной линии на белом фоне; перечислены mBot 1/2, LEGO, Zmrobo, RoboRobo. Конкретные ограничения из отдельного действующего регламента подтвердить.',('robotics','coding')),
 (1126,'Car Race','Прямая трасса 4 метра, свободная конструкция с материалами из отдельного регламента. Электроника / моторизация и действующие ограничения пока не установлены.',('technology',))]:
    e=event(f'C{number}','LATI / LTRC · Junior · '+title+' · первая jornada 2026','Мексика','Villahermosa · Universidad Olmeca',urls['lati_pdf'],
      'Primaria / Secundaria; цифровой возраст не опубликован. Нужна действующая школьная справка.',
      'Условно: подтвердить школьный класс, иностранную школу / команду и места.',
      'Условно: нужна Primaria, самостоятельная работа без взрослого в pits и допуск иностранной школы.',
      'Отдельная заявка на категорию через сайт лиги; сверить школьную справку, состав и актуальные правила до подачи.',gear,
      start='2026-10-09',deadline='2026-10-04',scope='regional',priority='P0 — ближайший кандидат; допуск и дедлайн уточнить',
      cost='MXN 300 / команда за обе jornadas сезона; это не цена поездки и не мировой взнос.',
      note=lati_note+(' '+sumo_conflict if number==1124 else ''),themes=themes,evidence='official_rules',date_scope='competition_day')
    e.update(region='Северная Америка',format='До 2 учеников + взрослый asesor; минимум учеников в convocatoria не указан.',
      deadline_label='Новые команды: расчёт 5 дней до события',deadline_basis='derived_from_official_relative_rule',
      level='Региональная лига Tabasco, связанная с RoboMatrix',reward='Сезонные очки, диплом; скидка на региональный RoboMatrix победителю при указанном количестве участников.',
      action='До поездки подтвердить иностранную школьную справку, состав, регистрацию до расчётного 4 октября и действующие технические правила. Заявка семьи не подана.')
    e['references']=[ref('Страница действующей convocatoria',urls['lati_call']),ref('Обзор дивизионов и окно сезона',urls['lati_categories'])]
    if number==1124:e['references']+=[ref('Старый технический PDF: конфликт пределов',urls['lati_sumopdf'])]

fll_cycle='2026/27 BIOGLOW: зима декабрь 2026–февраль 2027; весна февраль–апрель 2027 для государственных сетей; лето июнь 2027. Организатор назначает площадку по штату, категории и дате регистрации. Это циклы, а не точные дни турнира. Заявка только формальной командой через coach / учреждение; независимая команда и родитель-наставник допустимы в программе, но конкретный зарубежный школьный / национальный допуск подтвердить.'
fll_specs=[
 (1127,'Founders Explore','6–10','По возрасту подходит; уровень и национальную квоту подтвердить.','По возрасту подходит; команда и места не подтверждены.','SPIKE Essential либо WeDo 2.0; комплект отдельно. 10 уроков.', 'Местный размер команды сверить: текущий FAQ его не устанавливает.', 'Демонстрационная ярмарка: медаль участнику и диплом команды; выбранные команды могут пройти дальше. Общая медаль не означает соревновательное первое место.'),
 (1128,'Founders Challenge','9–16','По возрасту подходит; отдельная команда, подготовка и квота.','Нет: ниже минимального возраста 9.','SPIKE Prime либо EV3; комплект отдельно. 12 уроков, робот, инновационный проект, интервью.', 'Местный размер команды сверить: текущий FAQ его не устанавливает.', 'Награды Robot Game / Robot Design / Innovation / Core Values и общий чемпион; отбор по линии назначенного цикла.'),
 (1129,'Future · Primaria baja','6–9','Условно: сейчас 9; класс и отсечение на день события 2027 подтвердить.','По возрасту подходит; Primaria baja, команда и событие подтвердить.','LEGO Education Tecnología e IA 5+; комплект отдельно. 10 сессий.', 'Команда 4 ученика + 1–2 coach по местному FAQ.', 'В 2026/27 напрямую на национальное событие, без обещания мирового отбора. Формат младшего события ещё por confirmar.'),
 (1130,'Future · Primaria alta / secundaria','9–16','По возрасту подходит; класс, роли и место в команде подтвердить.','Нет: ниже минимального возраста 9.','LEGO Education Tecnología e IA 8+ / 11+; комплект отдельно. Для 8+ нужны дополнительные компоненты; более 16 часов, 4 сменяемые роли.', 'Рекомендуется 4–8 учеников + 1–2 coach; в classpack группы по 4.', 'В 2026/27 напрямую на национальное событие. Проект, инженерное интервью и совместные миссии 3–5 раундов; дальнейшая квота отдельно.')]
for number,title,age,mat,osc,gear,team,reward in fll_specs:
    e=event(f'C{number}','FIRST LEGO League México · '+title+' · BIOGLOW 2026/27','Мексика','Площадку и конкретный день назначает Fundación RobotiX',urls['mx_fll_faq'],
      age+' лет по местному FAQ; контрольную дату / класс и верхнюю границу на событие проверить.',mat,osc,
      'Выбрать редакцию и formal team; запросить назначенный цикл, площадку, условия и свободное место у Fundación RobotiX.',gear,
      scope='national',priority='P1 — семейная сезонная база после выбора команды' if number in [1127,1128] else 'P2 — сравнить новый формат и оборудование',
      cost='Годовой командный взнос зависит от редакции / категории; публичной суммы нет. Hardware, дорога и жильё отдельно.',
      note=fll_cycle+' '+reward+' SPIKE / EV3 Founders и новое AI-оборудование Future не взаимозаменяемы. Глобальный переход после 2026/27 и новые национальные квоты проверяются отдельно.',
      themes=('robotics','ai') if number>=1129 else ('robotics','coding'),evidence='program',date_scope='season_route')
    e.update(region='Северная Америка',period='Сезон 2026/27; конкретный день и площадка пока не назначены',format=team,reward=reward,
      level='Национальный путь FIRST México; право следующего отбора зависит от категории и цикла.',
      action='Определить категории обоих детей, состав, coaching, hardware и смету; получить назначение события и правила квоты до регистрации.')
    e['references']=[ref('Национальный оператор',urls['mx_fll'])]

e=event('C1131','Feria Maker · Concurso Ajolote 3D · 2026','Мексика','CDMX · CENART',urls['maker_ajolote'],
  'Ярмарка для всех возрастов; отдельный минимальный возраст конкурса не опубликован.',
  'Условно: детский конкурсный допуск подтвердить отдельно от семейного входа.',
  'Условно: детский конкурсный допуск и помощь взрослого при 3D-печати подтвердить.',
  'Скачать официальный Ajolote, самостоятельно персонализировать и принести физический 3D-print на конкурс в объявленный позже слот.',
  'Официальная rigid-модель ZIP / 3MF; собственная персонализация и распечатка.',
  start='2026-10-17',end='2026-10-18',scope='local',participation='individual_or_team',priority='P2 — короткая maker-проба при подходящем слоте',
  cost='Общий вход Feria бесплатный; отдельный конкурсный взнос не указан, печать / материалы отдельно.',
  note='Два дня — окно Feria, точный день / час конкурса будет объявлен. Пять лучших получают 5 /4 /3 /2 /1 filaments. Розыгрыш Bambu Lab A1 mini по QR — другая активность и не инженерная награда. Возраст ярмарки не перенесён на конкурс.',
  themes=('technology',),date_scope='festival_window')
e.update(region='Северная Америка',format='Физическая конкурсная работа; авторский / командный состав и детский допуск уточнить.',reward='Пять конкурсных мест с filament-призами; отдельно от лотереи 3D-принтера.')
e['references']=[ref('Семейные активности, fees материалов отдельно',urls['maker_activities_current'])]

for number,title,age,mat,osc in [
 (1132,'Robostarter Kinder','2026: 5–7, рождения 2019–2021','Нет для младшей категории: в 2027 исполняется 10.','Условно на 2027: исполняется 7; новые birth-year правила и школа ещё не опубликованы.'),
 (1133,'Robostarter Primaria Baja','2026: 7–9, рождения 2017–2019','Нет для 2027 при сохранении 7–9: исполняется 10; рассматривать Elementary.','Условно на 2027: исполняется 7; новая категория / birth-year cutoff ещё не объявлены.')]:
    e=event(f'C{number}','WRO México · '+title+' · следующий национальный сезон','Мексика','Местную региональную площадку 2027 ещё не объявили',urls['wro_categories'],
      age+'. Это опубликованные правила 2026, новые 2027 требуется дождаться.',mat,osc,
      'Изучить национальную младшую дорожку и дождаться регламента / расписания 2027; не подаваться в уже завершённый местный отбор 2026.',
      'Младшие Robostarter-миссии; оборудование, состав и технические правила нового сезона подтвердить.',
      scope='national',priority='P2 — младшая подготовка; правила 2027 ещё неизвестны',
      note='Одна команда и одна категория на ученика в сезон; возраст считается по календарному году соревнования. Региональные этапы 2026 были май–июль, национальные сентябрь. На уровне México младшие имеют национальное событие, но это не доказанная самостоятельная категория мирового финала WRO. Если диапазон 7–9 сохранится, Матвей 2017 в 2027 уже выше Primaria Baja, Оскар 2020 достигнет нижней границы; это условный расчёт, не правило 2027.',
      themes=('robotics','coding'),evidence='program',date_scope='season_route')
    e.update(region='Северная Америка',period='Подготовка к сезону 2027; будущие дни / новые правила не опубликованы',format='Команда; новый младший состав и размер подтвердить.',reward='Результат местного / национального Robostarter; мировой допуск не обещан.')
    e['references']=[ref('Cronograma 2026, а не будущий календарь',urls['wro_schedule']),ref('Национальный организатор',urls['wro_mx'])]

for number,title,age,mat,osc,gear in [
 (451,'Preschool','4–6','Нет: выше диапазона 4–6.','По возрасту подходит; после трёх лет опыта простота курса может не подойти.','LEGO начальные машины / простые механизмы, моторы, механика и электроника.'),
 (452,'Beginner Básico','7–8','Нет: выше диапазона 7–8.','Нет сейчас: 6 ниже 7; кандидат после достижения возраста / проверки уровня.','WeDo 1.0/2.0, Boost, SPIKE Essential, первые команды и датчики.'),
 (453,'CBRS Básico','9–11','По возрасту подходит; проверить продвинутый уровень и собственный код после трёх лет опыта.','Нет: ниже 9.','NXT / EV3, программы, сенсоры, моторы и механические сборки.')]:
    e=event(f'L{number}','Ciberbots Toluca · '+title+' · регулярный курс','Мексика','Toluca',urls['ciberbots'],age+' лет в описании школьного курса.',mat,osc,
      'Assessment, возрастная группа и текущий слот у Ciberbots. Подтвердить фактический ES / EN и доступ краткосрочной иностранной семьи.',gear,
      block='Лагеря',participation='day_camp',priority='P2 — учебная проба после проверки уровня' if number!=452 else 'P4 — будущая возрастная группа Оскара',
      note='Это постоянный школьный курс, не объявленная каникулярная смена. Возраст и hardware регулярного курса не перенесены на Navidad / Pascua / Verano. После трёх лет соревнований нужна проверка самостоятельной сборки и сложности; имя Basic не доказывает подходящий уровень. ES-текст сайта не подтверждает техническое преподавание на ES.',
      themes=('robotics','coding'),evidence='program',date_scope='regular_program')
    e.update(region='Северная Америка',participation='regular',provider='Ciberbots',format='Регулярная робототехническая группа; длительность / еженедельный слот уточнить.',period='Текущая регулярная программа; дни посещения не установлены')

e=event('E188','MEXCIR 2027 · интеллектуальные роботы · академическая конференция','Мексика','CDMX · Centro de Investigación en Computación (CIC)',urls['mexcir'],
  'Профессиональная / академическая аудитория; минимальный возраст посетителя не опубликован.',
  'Условно: детский вход / подходящий формат отдельно подтвердить.',
  'Условно: детский вход / подходящий формат отдельно подтвердить.',
  'Очное либо удалённое посещение конференции; условия несовершеннолетних и фактическую программу подтвердить.',
  'Исследовательские доклады, keynotes, tutorials / intelligent robots; программа и докладчики ещё не заполнены.',
  block='События',start='2027-05-11',end='2027-05-14',scope='international',participation='visitor',priority='P3 — прежде всего ознакомление родителя',
  cost='Очное / remote участие объявлено бесплатным; сертификат платный, сумма не опубликована.',
  note='Заголовок перечисляет 11–14 мая 2027 (четыре дня), текст описывает трёхдневную программу: точные дни занятий ещё проверить. На сайте есть шаблонные speaker / programme blocks. Это академическая конференция, а не подтверждённая крупнейшая выставка компаний и не детский лагерь. Детский вход не подтверждён.',
  themes=('robotics','ai','technology'),evidence='event_page',date_scope='festival_window')
e.update(region='Северная Америка',visitor_policy='confirm_children',visitor_policy_note='Несовершеннолетние в опубликованном приглашении отдельно не описаны; remote доступ и участника-ребёнка уточнить.',format='Академическая конференция · очно или удалённо; не выставка компаний.')
e['references']=[ref('Календарь федерации, город и месяц',urls['fmr_events'])]
d['events']+=new

updated=[]
def change(id,**fields):
    byid[id].update(**fields);updated.append(id)
change('C001',action='Проверить письменное возрастное исключение, согласие и школьную справку; выяснить, была ли сдана форма питания к уже прошедшему 30 сентября. Затем технический контроль. Публичный набор уже закрыт по предыдущему источнику.')
change('C004',checked=CHECKED,language='Язык защиты / судейства на конкретной мексиканской площадке отдельно подтвердить.',languages=[],format='Формальная команда через coach / учреждение; местный размер Explore / Challenge сверить.',period='BIOGLOW 2026/27: зимний цикл декабрь 2026–февраль 2027; конкретные дни / площадка назначаются.',note=byid['C004']['note']+' '+fll_cycle,proof='Повторно прочитан действующий национальный FAQ BIOGLOW 2026/27; новые точные дни не придуманы.')
change('C005',checked=CHECKED,participation='team',format='Primaria baja 6–9: команда 4 + 1–2 coach; 9–16: рекомендуется 4–8 + 1–2 coach.',language='Язык защиты / судейства на конкретной площадке подтвердить.',languages=[],period='2026/27: Future один раз напрямую на национальное событие; точный день назначается.',note=byid['C005']['note']+' '+fll_cycle+' Future 2026/27 напрямую на National; 6–9 формат пока por confirmar. Индивидуальные учебные задания не означают индивидуальную конкурсную регистрацию.',proof='Текущий México FAQ: формальные команды, местные 6–9 /9–16, одноразовый direct National 2026/27.')
change('C007',checked=CHECKED,source=urls['wro_categories'],language='Язык защиты / судейства конкретной площадки не подтверждён.',languages=[],proof='Прочитаны национальные категории / cronograma 2026. Новый сезон 2027 и мировая квота не установлены.',note=byid['C007']['note']+' México отдельно публикует Kinder 5–7 / Primaria Baja 7–9 в 2026. В 2027 Матвею 10, Оскару 7; новая младшая дорожка не подменяет Elementary 8–12.',references=[ref('Местный cronograma 2026',urls['wro_schedule'])])
change('C043',checked=CHECKED,source=urls['fmr_events'],city='Zacatecas · COZCyT',period='Март 2027; точные дни и правила дисциплин ещё не опубликованы.',proof='Календарь Federación Mexicana de Robótica подтверждает март 2027 / COZCyT Zacatecas; точных дней нет.',note=byid['C043']['note']+' Опубликованы месяц и национальная площадка, не точный новый детский регламент. Escuela de Invierno Veracruz декабрь 2026 — исследовательская программа без подтверждённого детского возраста; не добавлена как лагерь 6/9.')
change('C662',checked=CHECKED,priority='P4 — регистрация закончилась; младший конкурсный допуск не подтверждён',entry='Регистрация по форме закончилась 30 сентября. Прочитанные категория / приглашение не устанавливают допуск Primaria 6/9; возможность участия после срока не обещана.',note='Форма 2026 перечисляет Factory Simulation, открытые проекты, STEM posters, Forecasthon, Misión Dúrika, Autómatas, NAO, Smart Recycling Colegio, Smart Factory Universidad и Sinergia. Правила младших не получены; приглашение TEC адресовано pregrado / posgrado. Robotifest.com сейчас показывает архив 2018, не действующий регламент 2026.',action='Сохранить в каталоге как закрытый набор; детский конкурсный путь будущего сезона изучить отдельно. Посещение фестиваля — отдельная карточка E047.')
change('E047',checked=CHECKED,priority='P2 — посещение после подтверждения программы и детского входа',visitor_policy='confirm_children',visitor_policy_note='Общий исторический публичный формат не заменяет условия посетителей 2026. Конкурсная форма не билет посетителя.')
change('L139',checked=CHECKED,priority='P4 — оба ниже минимального возраста 10',action='Не планировать эту смену для детей 2017 /2020. Будущий курс после достижения 10 лет проверять по новым датам и условиям.',proof='Свежая первичная страница: presencial, пять дней 7–11 декабря 2026, 10:00–12:00, возраст 10–12. Оба ребёнка в декабре 2026 младше 10.')
change('L119',checked=CHECKED,proof='Свежая общая CS-Camp страница: Christmas декабрь / Summer январь, 2–8, внешние дети, 08:00–12:00. Точные смены 2026/27, robotics-часы и язык не объявлены.')
for id,period in [('L116','Navidad: декабрь 2026; точная смена не объявлена.'),('L117','Pascua: próxima 2027; точные дни не объявлены.'),('L118','Verano: próxima 2027; четыре недели без установленного первого дня.')]:
    change(id,checked=CHECKED,period=period,proof='Текущий Ciberbots services описывает будущий сезон, не конкретные даты; возраст / язык regular courses не перенесены на каникулы.')
change('E001',checked=CHECKED,source=urls['maker_activities_current'],proof='Текущая официальная Feria 2026: 17–18 октября / CENART, семейные активности; детали отдельных workshop ещё ожидаются.',note='Технологические активности для всех возрастов: Hebocon, электронный badge, LED Race, Robolution, autómata. Общий вход бесплатный; некоторые материалы / workshops платные. Возраст, слот и стоимость каждого занятия отдельно не объявлены. Ajolote 3D — отдельный конкурс C1131; Bambu QR — лотерея, не инженерная победа.',references=[ref('Отдельный конкурс 3D',urls['maker_ajolote']),ref('Workshop programme',urls['maker_workshops'])])

profiles=[]
def profile(id,name,summary,categories,ids,source_keys,nuances):
    q=dict(id=id,name=name,group='regional',age_summary='; '.join(c['name']+': '+c['age'] for c in categories),age_tags=['6','9','10-12'],summary=summary,categories=categories,event_ids=ids,legacy_ids=[],
      route=['Выбрать категорию каждого ребёнка','Подтвердить класс, возраст и команду','Получить текущие правила / слот / язык','Оценить самостоятельный уровень и стоимость','Местный результат и следующая квота проверяются отдельно'],
      hardware='См. категории; платформу и актуальный регламент проверить до покупки.',language='Язык занятия / защиты конкретного этапа не подтверждён; ES-сайт не является доказательством.',
      importance='Проверенный местный / национальный маршрут; международный титул не обещан.',strengths=summary,requirements=['Опубликованный возраст не подтверждает место / школьный допуск','Заявка семьи не подана','Инженерная работа детей и самостоятельная роль каждого'],nuances=nuances,
      cost='См. отдельную карточку: взнос, hardware и поездка различаются.',award='Медаль участия, местное место, национальная квалификация и мировой титул различаются.',
      sources=[dict(title='Первичный национальный источник · '+key,url=urls[key],checked=CHECKED) for key in source_keys],evidence='Прочитаны первичные страницы; существенные PDF-таблицы и ограничения осмотрены визуально.',checked=CHECKED)
    profiles.append(q);d['league_guide']['profiles'].append(q)
profile('fll-mexico-bioglow','FIRST LEGO League México · четыре маршрута BIOGLOW 2026/27',
  'Для сезонной базы: Матвею Challenge либо Future 9–16; Оскару Explore либо Future 6–9. Общая Explore-команда возможна по возрасту сейчас; классы, верхняя граница и конкретное событие отдельно.',
  [dict(name=t,age=age,team=team,hardware=gear,age_rule='Национальное отсечение / класс и день события подтвердить',entry=reward) for _,t,age,_,_,gear,team,reward in fll_specs],
  ['C004','C005','C1127','C1128','C1129','C1130'],['mx_fll_faq','mx_fll'],
  ['Future 2026/27 по исключению напрямую в National; следующие сезоны не обещаны','Future младший формат ещё por confirmar','Individual lesson challenge не индивидуальный конкурс','По FAQ один школьный event-team; независимую зарубежную семью и quota уточнить','Explore recognition не подтверждает общее первое место'])
profile('lati-tabasco-junior','LATI / LTRC Tabasco · Junior и региональный RoboMatrix',
  'Ближайшая jornada 9 октября 2026; до 2 учеников + adult advisor. Условный кандидат для обоих после подтверждения Primaria и иностранной школы, самостоятельности и технического регламента.',
  [dict(name=t,age='Primaria / Secundaria, справка',team='До 2 учеников + adult advisor',hardware=g,age_rule='Школьный уровень; наивысший класс определяет division',entry='Первая jornada 9.10.2026; новые команды за 5 дней; второй день не установлен') for t,g in [('Sumo LEGO',sumo_conflict),('Line Kits','mBot / LEGO / Zmrobo / RoboRobo'),('Car Race','Прямая 4 м; материалы по отдельным правилам')]],
  ['C1124','C1125','C1126'],['lati_call','lati_pdf','lati_sumopdf'],
  [sumo_conflict,'Взрослые не входят и не общаются с участниками в pits','Дата 4 октября вычислена из 5 дней; час уточнить','MXN 300 за обе jornadas; минимум 4 команд','RoboMatrix fee scholarship 50% если участников ≤5, 100% если >5; не мировой финал','Homepage / PDF называют региональное назначение иначе: Sureste / Península, подтвердить'])
profile('wro-mexico-junior','WRO México · Kinder / Primaria Baja / Elementary',
  'Оскару искать новые Robostarter Kinder / Primaria Baja правила 2027; Матвею Elementary. Текущий опубликованный национальный календарь — 2026 и местный отбор уже завершён.',
  [dict(name=t,age=age,team='Местный состав нового сезона подтвердить',hardware='См. регламент категории',age_rule='Возраст по календарному году; 2027 правила ещё не объявлены',entry='Регион → национальный этап; отдельная мировая категория / квота не установлены') for t,age in [('Kinder','2026:5–7 /2019–2021'),('Primaria Baja','2026:7–9 /2017–2019'),('Elementary','2026:8–12 /2014–2018')]],
  ['C007','C1132','C1133'],['wro_categories','wro_schedule','wro_mx'],
  ['Если 7–9 сохранится, Матвею в 2027 уже 10; условный расчёт не новый регламент','Оскару в 2027 исполняется 7; Elementary минимум 8 пока не подходит','Одна категория / одна команда на ученика в сезон','National младших не доказывает собственную мировую финальную категорию'])
d['league_guide'].update(version=50,checked=CHECKED)

a=d['completeness_audit'];t=a['local_focus']
t.update(version=50,checked=CHECKED,status='deeper partial audit',
  conclusion='Для постоянной подготовки я бы проверял FLL México с разными основными категориями: Матвею Challenge / Future 9–16, Оскару Explore / Future 6–9. Ближайшие даты — TecPro 8 октября, LATI 9 октября и Feria Maker 17–18 октября. Допуск и места пока не подтверждены. Каникулярные EN / ES группы рядом с домом ещё требуют конкретных смен и проверки уровня.',
  language_result='Семья может учиться на EN / ES / RU. У новых мексиканских regular / holiday candidates язык преподавания прямо не установлен, поэтому подтверждённые языковые теги не добавлены. Возраст постоянного курса не перенесён на каникулы.')
t['routes'].insert(1,dict(name='9 октября · LATI Junior в Tabasco',detail=lati_note+' '+sumo_conflict,ids=['C1124','C1125','C1126']))
t['routes'].insert(2,dict(name='2026/27 · четыре FLL México дорожки',detail='Матвею Challenge / Future 9–16; Оскару Explore / Future 6–9. Explore сейчас подходит обоим по возрасту, но после трёх лет опыта сложность проверить. '+fll_cycle+' Future по исключению сразу на National; младший формат ещё por confirmar. Цена и международная квота не опубликованы.',ids=['C1127','C1128','C1129','C1130']))
t['routes'].insert(3,dict(name='WRO México 2027 · разные младшие пути',detail='2026 публикует Kinder 5–7 /Primaria Baja 7–9 /Elementary 8–12. В 2027 Матвею 10, Оскару 7. Новые правила / дни не объявлены: Матвею планировать Elementary, Оскару проверять новую младшую национальную дорожку. Не считать прошлый national отбор открытым или обещанной мировой квотой.',ids=['C007','C1132','C1133']))
for r in t['routes']:
    if r['name'].startswith('Каникулы'):
        r['detail']='Mount View текущая общая CS-Camp страница публикует 2–8 для Christmas / Summer: Оскар подходит по возрасту, Матвей 9 выше максимума; реальные смены, технические часы и язык не объявлены. CENFOTEC 7–11 декабря, 10–12: оба не подходят. Ciberbots регулярные 4–6 / 7–8 / 9–11 — отдельно от Navidad 2026 / Pascua 2027 / Verano 2027 с неустановленными днями и языком. RoboTecnia / Cerebritos и Liota остаются кандидатами, не подтверждёнными общими сменами.'
        r['ids']+=['L116','L117','L118','L451','L452','L453']
t['routes'].append(dict(name='Посетить с семьёй / отдельно родителю',detail='Feria Maker 17–18 октября, CENART: семейный вход, мастерские и отдельный Ajolote 3D с ещё неизвестным конкурсным временем / возрастом. Robotifest 24–26 октября: младший visitor-pass и программа 2026 отдельно подтвердить, конкурсный набор закрыт. MEXCIR 11–14 мая 2027 — бесплатная академическая конференция очно /remote, детский доступ и фактические3/4 дня уточнить; не крупнейшая промышленная выставка.',ids=['E001','C1131','E047','C662','E188']))
t['family_picks_heading']='Мой выбор ближайших проверок для семьи'
t['family_picks_note']='Приоритет соответствует вашим возрастам и трём годам опыта. Это кандидаты для проверки уровня / допуска, не подтверждённые лучшие лагеря или гарантии мест и побед.'
t['family_picks']=[
 dict(kind='league',country='Мексика',title='Сезонная база · FLL с разными ролями',why='Матвею прежде всего Challenge; Оскару Explore. Future сравнить как новую AI / collaborative-среду. Одна основная лига и собственный проект полезнее набора несвязанных медалей.',gate='Команда, школа / класс, назначенное событие, оборудование, язык технических занятий и стоимость ещё подтвердить.',event_ids=['C1127','C1128','C1129','C1130'],school_ids=[],source_urls=[urls['mx_fll_faq']]),
 dict(kind='league',country='Мексика',title='Ближайший конкурс · LATI 9 октября',why='Три Junior-дисциплины и небольшой состав могут дать измеримый региональный опыт. Сезонный результат связан с RoboMatrix.',gate='Расчётный срок новых команд — 4 октября; иностранная справка, самостоятельность в 6 лет и конфликт 15 см / 1 кг против 20 см / 2 кг ещё не разрешены.',event_ids=['C1124','C1125','C1126'],school_ids=[],source_urls=[urls['lati_call']]),
 dict(kind='league',country='Мексика',title='Подготовка 2027 · WRO младшие отдельно',why='Оскару младшие Robostarter, Матвею Elementary. Так каждый получает посильную самостоятельную задачу.',gate='Правил 2027 ещё нет; Матвею 10 выйдет за текущие 7–9. Младший national не обещает мировую WRO категорию.',event_ids=['C007','C1132','C1133'],school_ids=[],source_urls=[urls['wro_categories'],urls['wro_schedule']]),
 dict(kind='camp',country='Мексика / Коста-Рика',title='Учебная проба · уровень прежде каникул',why='Ciberbots: отдельные регулярные 4–6 и 9–11 для братьев; CuriousLab — местная база. Проверять более сложную работу после трёх лет опыта.',gate='Язык, места и assessment не подтверждены. Дни каникул Ciberbots неизвестны; MountView только 2–8, CENFOTEC 10–12 сейчас исключён.',event_ids=['L451','L453','L023','L116','L117','L118','L119','L139'],school_ids=[],source_urls=[urls['ciberbots'],urls['mountview'],urls['cenfo_makers']])]
t['open_questions']+=['LATI: иностранная школьная справка, minimum team, независимость в pits, точный час закрытия и актуальные Sumo limits.','FLL México: event assignment, upper age / class cutoff, текущий взнос и квота следующего этапа.','WRO México: новые правила 2027 junior births / team rules, местные даты и отсутствие автоматически обещанной мировой категории.','Feria Maker: детский Ajolote-конкурсный допуск, слот, отдельные workshop fees; Robotifest visitor programme 2026.']
issues=[dict(name='LATI: новая convocatoria / старый Sumo PDF',status=sumo_conflict,official_alternative=urls['lati_call']),
 dict(name='LATI: segunda jornada / regional RoboMatrix',status='Первый день 9 октября подтверждён; второй день не установлен. Homepage / convocatoria называют следующий регион по-разному; географию подтвердить.',official_alternative=urls['lati_pdf']),
 dict(name='FIRST LEGO League Costa Rica: свежая страница недоступна',status='Новый запрос остановился на истёкшем SSL-сертификате. Прежние сведения не выданы за свежие подтверждённые правила.',official_alternative='https://www.firstlegoleaguecr.com/'),
 dict(name='MEXCIR2027: четыре даты / три программных дня',status='Header11–14 мая, body three-day; программа ещё содержит placeholders. Даты обозначены окном, не четырьмя установленными сессиями.',official_alternative=urls['mexcir'])]
a.update(version=50,checked=CHECKED,new_ids=[e['id']for e in new],new_profiles=[p['id']for p in profiles],updated_ids=updated,new_school_ids=[],updated_profile_ids=[],validation_previous=copy.deepcopy(a['validation']),validation=dict(version=50,status='pending',publication='pending'),conclusion='Добавлены младшие México-дорожки, национальные циклы, региональные правила и visitor conditions. Мировой инвентарь и местные аудиты остаются частичными.')
a['source_issues']+=issues
d['camp_focus'].update(version=50,checked=CHECKED,added_ids=['L451','L452','L453'],updated_ids=['L116','L117','L118','L119','L139'],conclusion='Ciberbots regular age / level paths отдельно от недатированных каникул; CENFOTEC 10–12 исключён для обоих в 2026.',validation=dict(version=50,status='pending'))
d['asof']=CHECKED;d['expansion_log'].append(dict(version=50,checked=CHECKED,scope='Priority near-home Mexico / Costa Rica junior season and camp gates',added=len(new),new_profiles=len(profiles),status='partial; worldwide objective preserved'))
known={s['url']for s in d['sources']}
for e in new+[byid[id]for id in updated]:
    for u in [e['source']]+[r['url']for r in e.get('references',[]) or []]:
        if u not in known:
            d['sources'].append(dict(url=u,title='Семейный México / Costa Rica источник',checked=CHECKED,evidence='Прочитано доступное primary programme / rules; существенные ограничения и неизвестные условия выделены.'));known.add(u)
for q in profiles:
    for s in q['sources']:
        if s['url']not in known:d['sources'].append(dict(url=s['url'],title=s['title'],checked=CHECKED,evidence='Первичный национальный источник'));known.add(s['url'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
read={'mx_fll_faq','wro_mx','wro_categories','wro_schedule','lati_call','lati_pdf','lati_sumopdf','robotifest','robotifest_form','robotifest_main','cenfo_makers','mountview','ciberbots','maker_activities_current','maker_ajolote','fmr_events','mexcir','lati_home','lati_categories'}
receipts=json.loads((WORK/'sources-local-deep-v50/receipt.json').read_text())
for row in receipts:
    row.pop('path',None);row['primary_body_read']=row['status']==200 and row['name']in read
    if row['name']in ['luva','liota']:row['limitation']='HTTP shell alone does not establish current programme content.'
(ROOT/'data/local-family-source-receipts-v50.json').write_text(json.dumps(dict(version=50,checked=CHECKED,sources=receipts,visually_inspected_pdf_pages=dict(lati_pdf=[1,2,3,4,6],lati_sumopdf=[2,3]),issues=issues),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,completeness_audit='data/audit-v50.json',latest_validation_previous=r['latest_validation'],latest_validation=dict(version=50,status='pending',publication='pending'))
r['research_passes'].append(dict(version=50,checked=CHECKED,scope='Near-home junior Mexico / Costa Rica deeper pass',status='implementation; validation pending',added=len(new),new_profiles=len(profiles),new_schools=0,new_history_results=0))
r['previous_goal_turn_classification']=dict(status='progress',evidence='v49 deployed:80 anonymous asset hashes and live UI verified; Europe 3 family scenarios,4 learning cards and 1 school delivered.',remaining='Full worldwide objective and local country audits remain active.')
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=50,added=len(new),updated_ids=updated,profiles=len(d['league_guide']['profiles']),events=len(d['events'])),ensure_ascii=False))
