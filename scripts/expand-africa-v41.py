"""Primary-source African routes; retain full worldwide scope and prior inventory."""
import ast, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1587 and d['completeness_audit']['version']==40
CHECKED='2026-10-02';new=[];profiles=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event','profile']:
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(ROOT/'scripts/expand-oceania-v29.py'),'exec'))
base_event=event
used=set()
urls=json.loads((WORK/'urls-africa-v41.json').read_text())
urls.update(json.loads((WORK/'urls-africa-extra-v41.json').read_text()))
def u(name):
    used.add(name);return urls[name]
def event(*args,**kwargs):
    mode=kwargs.get('participation','team')
    if mode in ['regular','online']:kwargs['participation']='day_camp'
    if mode=='individual':kwargs['participation']='individual_or_team'
    e=base_event(*args,**kwargs);e['region']='Африка'
    if mode in ['regular','online']:
        e['participation']=mode;e['format']='Регулярные занятия; не каникулярная смена' if mode=='regular' else 'Онлайн-программа; расписание и часовой пояс подтвердить'
    if mode=='individual':e['participation']='individual';e['format']='Индивидуально; guardian для несовершеннолетнего'
    if e['languages']:e['language_certainty']='Язык прямо указан у этой программы; язык других продуктов оператора отдельно.'
    return e

# Kenya: the live registration page is more current than the incomplete calendar.
kw=u('ke_wro_reg');kc=u('ke_wro_cat');ks=u('ke_comp')
e=event('C1057','WRO Kenya · RoboMission Elementary / следующий сезон','Кения','Nairobi и региональные площадки',kc,'Elementary 8–12 по возрасту в календарном году',
 'Условно: 2017 подходит по возрасту; школьная команда и иностранный вход отдельно','Нет: 2020 ниже Elementary; местная Rookie 6–9 отдельно',
 '2–3 ученика и coach; форма требует школу. С 2027 нужен минимум один региональный турнир до Nationals.',
 'Автономный робот, поле; любая разрешённая сборная платформа по местной странице, действующий technical pack обязателен.',scope='national',evidence='program',
 note='Новый национальный финал 2027 не датирован. Открытый национальный сайт не доказывает иностранный приём или право кенийской мировой квоты.')
e['references']=[ref('Регистрация, школьные поля и изменение 2027',kw),ref('Действующий местный календарь',ks)]
for id,title,date,deadline,venue in [('C1058','Nairobi','2026-11-14','2026-11-08','Potterhouse Senior School'),('C1059','Mombasa','2026-11-21','2026-11-15','Oshwal Academy Mombasa')]:
    e=event(id,'WRO Kenya RoboStarter 2026 · '+title,'Кения',title+' · '+venue,kw,
     'Rookie 6–9; Elementary 8–12 по местному обзору. Точные RoboStarter правила потока запросить.',
     'Условно: по году рождения подходит Rookie / Elementary; категорию и уровень подтвердить','Условно: Rookie 6–9 подходит по году рождения; иностранный школьный вход не подтверждён',
     '2–3 ученика + coach; форма запрашивает школу, материалы и consent. Страница ограничивает команду одним турниром: не планировать обе даты одной командой без разрешения.',
     'Собственный робот и laptop; поле / mission bricks на площадке. Нужны именно правила RoboStarter, а не автоматическое применение мирового RoboMission.',
     start=date,deadline=deadline,scope='regional',note='Регистрация опубликована как Open; заполненная форма не означает место. На tournament page ноябрьские этапы отсутствуют, но они есть в live registration и на сайте организатора. Countdown и демонстрационный unsaved draft не использованы как срок или состояние заявки семьи.',
     cost='Rookie KES 12 000 / команда с coach; дополнительный coach KES 3 000. Тариф других категорий отдельно.')
    e['references']=[ref('Возрастные диапазоны местного обзора',kc),ref('Организатор подтверждает ноябрьские этапы',ks)]
e=event('C1060','WRO National Kenya 2026 · архив национального финала','Кения','Nova Pioneer · Tatu City',kw,
 'RoboMission Elementary 8–12; Junior / Senior старше; FI в этом финале только Junior / Senior',
 'Архив: возраст Elementary подходит, но приём завершён','Нет: ниже Elementary; Rookie не заявлена в этом финале',
 'Школьная команда 2–3 + coach; уже завершённый национальный отбор.',
 'RoboMission / FI по конкретным категориям; результаты для поиска действующего наставника.',
 start='2026-06-26',end='2026-06-27',scope='national',priority='P4 — прошедший этап; искать следующий набор',evidence='historical_program',
 note='Архив отделён от ноябрьской RoboStarter. Team ISS 1-е Elementary, 200 баллов. Квота на Worlds не является правом иностранной семьи.',cost='Архив: RM KES 27 000, новые команды 35 000; FI 27 000 по форме.')
e['references']=[ref('Официальный протокол 2026',u('ke_wro_results')),ref('Связь команды со школой: сообщение организатора',u('ke_results_school'))]

# Nigeria: an introductory pathway is not an age-certified world qualifier.
nw=u('ng_categories');ns=u('ng_starter');nc=u('ng_season')
e=event('C1061','WRO Nigeria · основные категории / следующий национальный сезон','Нигерия','Lagos · Arc-Lights Foundation; следующий venue неизвестен',nw,
 'Местный обзор 8–19; детальная возрастная категория и сезонное отсечение отдельно',
 'Условно: общий диапазон 8–19 подходит; Elementary и действующий набор подтвердить','Нет для основных категорий: ниже общего минимума 8; RoboStarter отдельно',
 'Связаться с национальным организатором для действующего local pack, команды, иностранных участников и квот.',
 'RoboMission / Future Innovators / RoboSports / Future Engineers: это разные требования и возрасты.',scope='national',evidence='program',
 note='Страница сезона 2026 описывает тему, но не даёт в прочитанном тексте следующую дату. Диапазон 8–19 не подтверждает допуск девятилетнего во все четыре дисциплины.')
e['references']=[ref('Сезонный обзор',nc)]
e=event('C1062','WRO Nigeria RoboStarter · младший вводный маршрут','Нигерия','Lagos · условия местного запуска уточнить',ns,
 'Вводная программа; точные local ages не опубликованы в прочитанном описании',
 'Условно: после трёх лет соревнований проверить полезность начального уровня','Условно: младший формат заявлен, но возраст 6 местными правилами не подтверждён',
 'Через Arc-Lights; запросить текущую группу / событие и правила возраста, не записываться по общему слову Kids.',
 'Sumo, line-following Training, Innovators и Kids как вводные варианты.',scope='local',evidence='program',
 note='На странице остаётся фраза про новые варианты в 2025; это описание программы, не подтверждённый турнир 2026/27. Всемирный финал для этой вводной программы не обещан.')
nr=u('ng_robotchallenge_reg');nf=u('ng_robotchallenge_faq')
for id,city,start,end in [('C1063','Abuja','2026-05-20','2026-05-21'),('C1064','Lagos','2026-05-28','2026-05-29')]:
    e=event(id,'RobotChallenge Nigeria 2026 · '+city+' · архив','Нигерия',city+(' · Nile University по FAQ' if city=='Abuja' else ' · точная площадка не установлена'),nr,
     'Школьный Primary 7–11; Independent Teams 9–18 на форме. Категория / состав команды отдельно.',
     'Архив: 9 подходит общему диапазону; действующий foreign вход не подтверждён','Нет по опубликованному Primary минимуму 7; не переносить в отдельный online RC.CODE',
     'Команда несовершеннолетних с coach; институция / штат / DOB в форме. Следующее издание пока не объявлено.',
     'Sumo, drones, line following, maze, Freestyle и другие категории: регламент каждого робота отдельно.',
     start=start,end=end,scope='national',priority='P4 — прошедшее издание',evidence='historical_program',
     note='Registration различает Abuja и Lagos; FAQ только Abuja и hackathon 22 мая. Статичная форма с оплатой не принята за открытый новый сезон. Утверждение об отборе China / Greece / Romania — заявление организатора, конкретная квота семье не доказана.')
    e['references']=[ref('FAQ: primary / independent teams, minor coach',nf)]
e=event('C1065','RobotChallenge Nigeria RC.CODE · онлайн-программирование / следующий набор','Нигерия','Онлайн; местный оператор RobotKraftAfrica',u('ng_rccode'),
 'Primary school и independent young coders; числовой минимум / возрастные категории не опубликованы',
 'Условно: Primary Scratch / CREATiCODE; подтвердить следующий срок и foreign eligibility','Условно: числовой минимум не установлен, школьную ступень и детский допуск подтвердить',
 'Индивидуальная регистрация с DOB и guardian для minors; язык задания, дата и международный вход требуют подтверждения.',
 'Scratch, CREATiCODE; Python / C++ для других уровней. Проект и rubric текущего потока неизвестны.',
 scope='national',participation='individual',themes=('coding','games'),cost='NGN 10 000 / участник на странице; платёж семьи не выполнен.',
 note='Название World Championship на форме не доказывает масштаб проведённого финала или открытую международную квоту. В footer шаблонный телефон; не считать его подтверждённым контактом. Без текущей даты не экспортируется как будущий этап.')

# Ghana: international camp access is explicit, teaching language is a separate fact.
ge=u('gh_enjoy')
e=event('C1066','ENJOY AI African Open Ghana 2026 · опубликованная программа','Гана','Accra · точный venue / даты не установлены',ge,
 'Общая сеть 3–22; конкретный challenge и возрастная группа по event technical pack',
 'Условно: нужна разрешённая категория, технический пакет и иностранная делегация','Условно: общий 3–22 не доказывает доступ шестилетнему в каждую дисциплину',
 'Организатор допускает школы / country coordinators и международные делегации через координацию; применимость к семье из Мексики / Коста-Рики уточнить.',
 'Ancient Civilizations, Battle of Stars, Skyline, Drone Cup и другие challenge; финальный event pack пока обещан.',
 scope='international',note='Заявлено два дня, но точных дат в прочитанном тексте нет. Отсутствующую дату не заменяет footer 2026. Некоторые прикреплённые файлы с названием 2025; разрешённый technical pack нужно подтвердить. Континентальное Open не тождественно мировому финалу.')
e=event('C1067','Robofest Ghana / GRAF · путь к сезону 2027','Гана','Accra · Ghana Robotics Academy Foundation',u('gh_graf'),
 'Мировой 2027: Explorer 1–4 классы; Junior Game / Exhibition 5–8 весной 2027. Local qualifier отдельно.',
 'Условно: класс неизвестен; RoboParade Explorer вероятнее Junior Game по школьной ступени','Условно: требуется класс 1–4 для Explorer; шестилетний возраст сам по себе не допуск',
 'Уточнить действующий Ghana Director, local selection и иностранное представительство. Member-country команды проходят через Director, включая Open.',
 'Автономные robots; RoboParade Fun and Games — отдельная младшая категория; Game / Exhibition требуют qualifier.',
 scope='national',note='Календарь Ghana 2027 не найден в прочитанном наборе. APEX3718-1 выиграла мировой Junior Game 2026; это не подтверждение младшей школы или доступности её наставника. Мировые tentative даты не перенесены в Ghana calendar.')
e['references']=[ref('LTU: опубликованные General Rules 2027',u('robofest_2027_rules')),ref('LTU: мировой протокол 2026',u('robofest_2026_awards'))]
e=event('C1068','Creativity Lab Robotics Challenge Rwanda · архив первого финала','Руанда','Kigali · местный национальный проектный конкурс',u('rw_challenge'),
 '8–11; Primary или отдельные дети; до 3 в группе по rules первой редакции',
 'Архив: 9 подходит, но заявка закрыта; следующий сезон неизвестен','Нет: ниже опубликованного 8; младшие курсы отдельно',
 'Самостоятельный проект ребёнка / до 3; video selection и national final. Foreign admission не установлен.',
 'SDG3: инженерное решение против переноса микробов; robot code / research / presentation, coach не делает проект.',
 start='2025-02-14',scope='national',participation='individual_or_team',priority='P4 — архив 2024/25; новый набор не объявлен',evidence='historical_program',
 note='Подача была до 29 ноября 2024, отбор 13 декабря 2024, финал 14 февраля 2025. Footer 2026 не обновляет сезон. Регулярный курс EN не доказывает язык судейства этого конкурса.')
e['references']=[ref('Полный архивный регламент',u('rw_rules'))]

for id,name,start,end,key,price,topic in [('L365','December','2026-12-07','2026-12-12','ke_growth_dec','12 000','Coding, robotics, digital design и content creation'),('L366','November','2026-11-16','2026-11-28','ke_growth_nov','24 000','Public speaking / leadership / digital literacy; робототехника конкретно в этой смене не обещана')]:
    e=event(id,'Growthfluential · '+name+' Kids & Youth Camp 2026','Кения','Nairobi · Garden Estate / Google Meet',u(key),'8–18',
     'Условно: 9 подходит; нагрузку, EN и foreign access подтвердить','Нет: младше 8',
     'Очные полудни или online option, Monday–Saturday 09–12 по местному времени. Проверить одинаков ли учебный набор online и очно.',
     topic,block='Лагеря',start=start,end=end,participation='day_camp',cost='KES '+price+' / ребёнок; materials included. Deposit 50% входит в стоимость, не добавлен повторно.',
     themes=('robotics','coding','technology') if id=='L365' else ('technology',),note='Это полудневная программа, пансион не заявлен. English website не доказывает язык занятий. Online расписание в Nairobi UTC+3 = 00:00–03:00 Costa Rica, поэтому семье удобнее очное посещение; часовой пояс подтвердить. В November робототехника не перенесена из December.')
    e['references']=[ref('Две разные смены и архив',u('ke_growth_programs'))]
for id,title,key,age,mat,osc,gear,mode in [
 ('L367','CodeAugs Summer Camp · Explorer', 'gh_codeaugs','6–9','Условно: 9 подходит Explorer; robotics camp Builder начинается с 10','Условно: 6 подходит Explorer; места / язык отдельно','Scratch / creative coding; робототехнический Builder 10–13 не перенесён на младшую группу','day_camp'),
 ('L368','CodeAugs · Coding Fundamentals', 'gh_code_courses','6–9; 12 недель','Условно: возраст подходит; начинающий уровень проверить','Условно: возраст подходит; язык / foreign доступ отдельно','Логика кода и проекты; это регулярный учебный курс','regular'),
 ('L369','CodeAugs · Robotics & Electronics', 'gh_code_courses','9–17; 12 недель','Условно: с 9 по странице; технический уровень / язык отдельно','Нет: ниже 9','Собственные robotics projects; набор / частота уроков не установлены','regular'),
 ('L370','Coasted Code · Explorers Creative Coding & Robotics', 'gh_coasted_explore','6–9; 12 недель','Условно: возраст подходит; начинающий уровень после 3 лет соревнований проверить','Условно: возраст подходит; фактический набор / язык уточнить','ScratchJr / Blockly, beginner robotics, story AI и игры','regular'),
 ('L371','Coasted Code · Online Summer School', 'gh_coast_online','6–17; 6 недель','Условно: подтвердить текущую age-matched группу и EN','Условно: 6 входит в общий диапазон; отдельный младший трек и EN уточнить','Live online projects: coding / robotics / AI; optional robot kit','online')]:
    e=event(id,title,'Гана','Accra / online · конкретный формат и площадку выбрать',u(key),age,mat,osc,
     'Выбрать действующий поток и техническую программу; следующие даты не опубликованы.',gear,block='Лагеря',participation=mode,
     themes=('coding','games') if id in ['L367','L368'] else ('robotics','coding','ai') if id in ['L370','L371'] else ('robotics','coding'),
     note='Язык сайта не принят за EN-преподавание; точный иностранный доступ, время и место уточнить. Это программа для планирования, не принятая семейная заявка.')
    if id in ['L370','L371']:
        e['note']='Оператор прямо пишет open to families worldwide. Это подтверждает опубликованный международный канал, но не язык уроков, дату cohort или место семье. Сертификат курса не соревновательная победа; заявленная STEM.org аккредитация не оценка мирового рейтинга.'
        e['entry']='Есть открытый международный online маршрут; выбрать actual cohort, язык и расписание. Очный визит согласовать отдельно.'
        e['cost']='Для Ghana-прайса GHS 650 enrolment + 200 / месяц; международный market тариф уточнить' if id=='L370' else 'Ghana-прайс GHS 1 000 за 6 недель; это один programme fee, не плюс enrolment; international market отдельно'
e=event('L372','Ghana International School · Summer Day Camp 2026 · архив Adventure','Гана','Accra · Infant / Secondary school campuses',u('gh_gis_faq'),
 'Adventure & Enrichment 6–15; Little Explorers только 4–5, не для Оскара 6',
 'Архив: 9 подходит группе Adventure; следующий набор не объявлен','Архив: 6 подходит Adventure, а не Little Explorers4–5',
 'FAQ прямо допускает детей других школ locally / internationally. Сезон 2026 закончился; новый cohort и camp teaching language отдельно.',
 'Coding / robotics, web / games, Mini-Bot Builders и drones как часть смешанной программы.',
 block='Лагеря',start='2026-07-06',end='2026-07-31',participation='day_camp',priority='P4 — архив; ждать новый набор',evidence='historical_program',
 cost='Архив GHS 2 000 / неделя; день 08:30 arrival, activities09:00–14:50.',
 note='FAQ сообщает 2025:140детей,34школы,7стран — операторский отчёт, не международная награда. EN основной школы не перенесён на язык технического camp. Пансион и ежедневный объем робототехники не установлены.')
e['references']=[ref('6–15 и STEM-подпрограмма',u('gh_gis_adventure')),ref('Little Explorers4–5',u('gh_gis_little'))]
for id,name,key,age,hours,mat,osc,gear in [('L373','Intermediate','rw_intermediate','9–11','10 занятий / 20 часов','Условно: возраст 9 подходит; набор / иностранный ребёнок отдельно','Нет: ниже 9','Arduino Uno, micro:bit, robotics / MakeCode, circuits и игры'),('L374','Junior','rw_junior','7–8','8 занятий / 16 часов','Нет по группе7–8 для текущего9','Будущий вариант: с 7; до дня рождения2027 не подходит','Электрические цепи, motors / pumps, making и визуальный код')]:
    e=event(id,'Creativity Lab Rwanda · '+name+' · регулярный курс на английском','Руанда','Kigali · Gikondo, GBC building',u(key),age,mat,osc,
     'Заявка на учебную группу; даты, цена, иностранные дети и требования уровня не опубликованы.',gear,block='Лагеря',participation='regular',
     languages=('EN',),language='Teaching language English прямо указан в overview именно этого уровня.',
     note=hours+'. Это регулярный курс; EN не перенесён на недатированный Children Bootcamp или архивный конкурс.',priority='P2 — подготовка Матвея после проверки' if id=='L373' else 'P3 — будущая ступень Оскара')
    e['language_mode']='primary'
e=event('L375','LogicLabs Kenya · восьминедельный Coding & Robotics Bootcamp 2026','Кения','Nairobi · South C / формат и площадку уточнить',u('ke_logic'),'7–16',
 'Условно: 9 подходит, но full-stack сложность и учебный поток проверить','Нет: младше7',
 'Оператор публикует окно26октября–24декабря. Точные дни, перерывы, часы и in-person/remote не установлены.',
 'Python / Scratch, micro:bit, UI, SQL / APIs / IoT и portfolio hackathon как учебный финал.',
 block='Лагеря',participation='day_camp',themes=('coding','robotics','games','ai'),cost='KES 6 000 за всю длительность по странице; комплект / число часов уточнить.',
 note='Это учебный hackathon, не независимый международный турнир. Восьминедельное описание и календарное окно не определяют ежедневное расписание. Названия partner schools — заявление оператора, не доказательство их результатов.',date_scope='holiday_window')
e['period']='26 октября – 24 декабря 2026: опубликованное окно; отдельные учебные дни не установлены'
e['holiday_window']={'start':'2026-10-26','end':'2026-12-24','note':'Окно программы не экспортируется как ежедневный лагерь без actual sessions.'}
e=event('L376','Creativity Lab Rwanda · Children STEM Bootcamps / следующий набор','Руанда','Kigali · точную площадку смены уточнить',u('rw_bootcamp'),
 'Children; числовой возраст / младшая группа не опубликованы',
 'Условно: детский формат, но возраст9 / technical track не подтверждены','Условно: слово Children не подтверждает6-летний допуск',
 'Запросить nextcohort, childage, EN-преподавание и технику именно лагеря.',
 'Детские STEM-активности; robotics / AI подробно описаны у youth и teacher bootcamps и не перенесены автоматически на childcamp.',block='Лагеря',participation='day_camp',themes=('technology',),priority='P3 — кандидат с неизвестными условиями',
 note='English regular Intermediate / Junior — отдельные продукты. У Children Bootcamp не установлены dates / ages / цена / язык технических уроков.')
e=event('L377','Sheen Academy · Festive workshops / следующий подтверждённый набор','Южная Африка','Cape Town · Century City',u('za_sheen'),
 'Festive workshops9+ на главной; точный возраст отдельного потока уточнить',
 'Условно:9 подходит общему анонсу; новая дата не опубликована','Нет для опубликованного Festive9+; старые junior смены отдельно',
 'Проверить новую festive detailpage: текущий workshop index всё ещё рекламирует Spring29сентября–1октября.',
 'Coding / robotics по главной; фактическую тему и число часов новой смены уточнить.',block='Лагеря',participation='holiday_workshop',cost='ZAR750 / workshop на главной; SpringR650 — другой поток.',
 note='Не перенесены даты December2025 на December2026. Главная Festive и индекс прошедшей Spring различаются; будущая дата остаётся неизвестной.')
e['references']=[ref('Индекс смен и архив: текущие детали Spring',u('za_workshops'))]

for id,title,country,city,key,start,end,gear,major in [
 ('E169','World Drone & Robotics Show Nigeria 2027','Нигерия','Abuja · H.E. Bola Ahmed Tinubu ICC','ng_drone','2027-03-23','2027-03-25','Autonomous drones / robots / AIhardware; professional exhibition / demo zones',True),
 ('E170','GITEX Nigeria 2027','Нигерия','Lagos; venue нового выпуска подтвердить','ng_gitex','2027-09-28','2027-09-30','AI, cloud, cybersecurity, digital infrastructure, fintech / startups',True),
 ('E171','Africa Tech Summit Nairobi 2027','Кения','Nairobi · Sarit Expo Centre','ke_techsummit','2027-02-10','2027-02-11','Tech / AI / fintech / startup conference с expo opportunities; не большая промышленная robot show',False),
 ('E172','Sheen Academy Open Day · попробовать robotics и coding','Южная Африка','Cape Town · Century City campus','za_sheen','2026-10-03','2026-10-03','Robotics, coding, drones,3D printing и laser engraving; учебная проба',False)]:
    e=event(id,title,country,city,u(key),'Возраст посетителя6/9 прямо не установлен' if id!='E172' else 'Семейный open day; регулярные занятия академии6–18',
     'Условно: детский посетитель требует подтверждения' if id!='E172' else 'Условно: учебный возраст9 подходит; программа open day / доступ подтвердить',
     'Условно: детский посетитель требует подтверждения' if id!='E172' else 'Условно: учебный возраст6 подходит; программа open day / доступ подтвердить',
     'Выбрать visitor badge / публичный день и получить ответ про детей6/9; student badge не автоматический детский билет.' if id!='E172' else 'Опубликован walk-in:10–13или15–17, бесплатно, no booking needed. Поездку семьи / конкретное занятие согласовать.',
     gear,block='События',start=start,end=end,scope='international' if id!='E172' else 'local',participation='visitor',
     priority='P3 — взрослое посещение; детей уточнить' if id!='E172' else 'P3 — близкая дата, только при удобной поездке',themes=('robotics','ai','technology') if id=='E169' else ('ai','technology') if id!='E172' else ('robotics','coding','technology'),
     note='Дата подтверждена объявлением организатора; отдельное право входа и реестр нынешних экспонентов не установлены. Посещение не даёт детям соревновательную победу.' if id!='E172' else 'Это местный день знакомства, не мировой турнир / большая выставка. EN-уроки не подтверждены названием сайта.',cost='Билет выбранной категории и дополнительные сессии проверить' if id!='E172' else 'Бесплатно по анонсу')
    e.update(visitor_policy='confirm_children',visitor_policy_note='Числовое правило детей6/9 не опубликовано в прочитанных условиях.',adult_entry=e['entry'],highlights=[gear],exhibitor_note='Следующий список компаний не проверен; логотип или sponsorship2026 не гарантирует экспонента2027.',exhibitor_directory_url=e['source'])
    if major:e['exhibition_tier']='regional_major';e['level']='Крупная региональная профессиональная tech-площадка по редакционной оценке'
    if id=='E169':
        e['references']=[ref('Badge policy: visitor / student без числового возраста',u('ng_drone_admission')),ref('Описание exhibitors и demo',u('ng_drone_exhibitors'))]
        e['note']+=' Слова global / state-backed — позиционирование организатора; мировой масштаб и конкретные компании не подтверждены независимым протоколом.'
    if id=='E170':e['note']+=' Header / новый блок дают28–30сентября2027; hero и sponsor lists всё ещё2026. Старые даты31августа–3сентября2026 не выданы за новый выпуск.'
    if id=='E171':e['references']=[ref('Регистрация и Founders Day9февраля отдельно',u('ke_tech_register'))]

# Remove language candidate tags that would appear as confirmed instruction.
updated=['L037','L038','L088','E082']
for id in updated[:3]:
    e=byid[id];e.update(checked=CHECKED,languages=[],language_mode='unconfirmed',language='Язык конкретных технических занятий прямо не подтверждён; EN-сайт не доказательство.',language_certainty='Повторно прочитан primarysource: обещание English-medium не найдено; кандидат EN снят с фильтра подтверждённого языка.')
byid['E082'].update(checked=CHECKED,proof='Повторно прочитан FAQ: trade/business18+,16–17 только со школой; даты2027 не найдены.',references=[ref('Future Manufacturing & Robotics track',u('gitex_morocco'))])

# Two permanent-school candidates, with exact evidence types.
def school(id,name,iso,country,city,curriculum,ages,langs,programme,results,sources,note):
    s=dict(id=id,name=name,iso=iso,country=country,region='Африка',city=city,school_type='private',curriculum=curriculum,ib_programmes=[],ages=ages,instruction_languages=langs,
     language_note='Английский язык школы прямо подтверждён; язык robotics team и camp отдельно.' if langs else 'English как предмет не доказывает язык всех уроков; languageofinstruction и robotics отдельно.',
     fit=dict(mat='candidate',osc='candidate',note=note),boarding='unknown',boarding_note='Возрастной пансион6/9 не установлен; семейное проживание отдельно.',
     programme=programme,labs='Точный juniorlab доступ и технические часы не установлены.',ai='Постоянный juniorAItrack не установлен.',results=results,evidence='national_result' if results else 'programme',
     admissions='Есть публичный канал enquiry; foreign admission, class assessment и места не подтверждены.',cost='Текущая полная школьная смета не установлена; лагерь отдельно.',
     questions=['Код действующей juniorteam, наставник, технические часы и протоколы последних3–5сезонов?','Какой класс и язык technicalteam получат дети2017/2020?','Есть ли trial, foreign admissions и полная смета?'],sources=sources,checked=CHECKED,priority=2,research_status='partial',verification='Первичные школа / организатор; juniorдоступ, worldaward и место семье отдельно.')
    d['schools'].append(s);return s
def ss(title,key,claim,kind='school'):return dict(title=title,url=u(key),claim=claim,kind=kind,checked=CHECKED)
result=dict(league='WRO',season=2026,category='RoboMission Elementary',stage='Kenya National',award='1-е место;200баллов',source=u('ke_wro_results'),provenance='organizer_protocol',team='Team ISS',note='Школа Kigwa Ridge указана отдельным опубликованным сообщением организатора; мировой титул не заявлен.',limit='Национальный результат одной команды, не мировой титул; младший наставник и место семье отдельно.')
school('S039','Kigwa Ridge School & Montessori Centre','KEN','Кения','Nairobi · Runda','Montessori EarlyYears / CambridgeInternational доYear9; IBне установлен','KeyStage1:Years1–2 /5–7; KeyStage2:Years3–6',[],
 'Действующий школьный Elementary результат2026 по WROKenya; класс6лет и младшая roboticsgroup отдельно.',[result],
 [ss('Школа и2026/27intake','kigwa','Montessori/Cambridge'),ss('KeyStage1','ke_kigwa_ks1','Years1–2,5–7'),ss('KeyStage2','ke_kigwa_ks2','Years3–6'),ss('Национальный протокол','ke_wro_results','TeamISS200баллов','organizer'),ss('Связь ISSсо школой','ke_results_school','Kigwa RidgeSchool','organizer')],
 'Для Оскара KeyStage1 по возрасту; Матвею classplacement. Победа школьной Elementaryteam не означает свободное место, текущего coach или иностранную worldquota.')
school('S040','Ghana International School','GHA','Гана','Accra · Cantonments','Cambridge / EnglishNationalCurriculum; младшие ступени; IBне установлен','Infant3–7; JuniorYears3–6 /7–11',['EN'],
 'JuniorSchool прямо включает coding / robotics / digital literacy. Летняя mixedSTEMprogramme отдельно, campage6–15.',[],
 [ss('Язык обучения','gh_gis_about','Englishlanguageofinstruction'),ss('InfantSchool','gh_gis_infant','3–7,classes1–2'),ss('JuniorSchool','gh_gis_junior','7–11,codingrobotics')],
 'Оскару Infant3–7; Матвею Junior7–11. Младшая лаборатория, действующая отборная команда и мировые результаты не установлены; иностранных детей лагеря не приравнивать к школьному admission.')

entities=[dict(id='S039',name='Kigwa Ridge School',kind='school',country='Кения',age='primary',school_id='S039',note='Связь ISSорганизатором; currentcoach иforeignentry отдельно.'),dict(id='KEN-MURAMATI',name='Muramati Comprehensive',kind='school',country='Кения',age='primary',school_id=None,note='Кампус / admissionsне изучены; связь по организатору.'),dict(id='KEN-CITAM',name='Citam Schools · campus unknown',kind='school',country='Кения',age='primary',school_id=None,note='Название сети без установленного кампуса; не досье постоянной школы.'),dict(id='GHA-APEX',name='APEX · Accra',kind='unresolved',country='Гана',age='junior',school_id=None,note='3718-1; школа не установлена; мировой результат команды не приписан GIS.'),dict(id='GHA-AURORA',name='Aurora · Old Akrade',kind='unresolved',country='Гана',age='secondary',school_id=None,note='6777-1; Senior, не младший школьный результат.')]
d['school_history']['entities'].extend(entities)
for id,entity,team,place,score in [('H127','S039','Team ISS',1,200),('H128','KEN-MURAMATI','THE CROP TOPPERS',2,195),('H129','KEN-CITAM','Galaxy Coders',3,180)]:
    d['school_history']['results'].append(dict(id=id,entity_id=entity,year=2026,league='WRO',category='RoboMission Elementary',stage='Kenya National Final',award=str(place)+'-е место; '+str(score)+'баллов',level='national_match',source=u('ke_wro_results'),team=team,team_id=None,provenance='organizer_protocol',note='Schoolaffiliation из отдельного сообщения организатора; мировой титул не заявлен.',checked=CHECKED))
for id,entity,team,code,category,place in [('H130','GHA-APEX','APEX','3718-1','Junior Game',1),('H131','GHA-AURORA','Aurora','6777-1','Senior Game',2)]:
    d['school_history']['results'].append(dict(id=id,entity_id=entity,year=2026,league='Robofest',category=category,stage='World Championship 2026 · Building Bridges',award=str(place)+'-е место',level='world_match',source=u('robofest_2026_awards'),team=team,team_id=code,provenance='organizer_protocol',note='Точная worldкатегория подтверждена LTU; нынешняя школа и junioradmission семьи не установлены.',checked=CHECKED))
d['school_history'].update(version=41,checked=CHECKED,conclusion='131 отдельных результатов; добавлены три национальных Elementary результата Kenya и два мировых Robofest2026 из Ghana. Schoolaffiliation / старшая категория и мировой титул разделены; полный5–10летний мировой рейтинг школ не установлен.')

profile('wro-kenya','WRO Kenya · Elementary / Rookie RoboStarter','regional','Местная Rookie6–9; Elementary8–12; возраст по календарному году',
 'Ноябрьская Rookie дает отдельный младший кандидат обоим; страна и право worldqualification требуют отдельного допуска.',
 [dict(name='RoboStarterRookie',age='6–9 в местном обзоре',team='2–3 +coach',hardware='Технический пакет RoboStarterотдельно',age_rule='Календарный год; точные условия потока подтвердить',entry='Ноябрь2026Nairobi/Mombasa;schoolfields и foreigngate'),dict(name='RoboMissionElementary',age='8–12',team='2–3 +coach',hardware='Автономный сборный robot',age_rule='Возраст в календарном году',entry='С2027 regionalrequired→national→worldquota')],
 ['C1057','C1058','C1059','C1060'],'Выбрать категорию → подтвердить иностранную schoolteam → местный этап; national / internationalквота отдельно.',
 ['Schoolfields в форме не заменяют отдельный foreignдопуск.','Coachне строит и не программирует за детей.','Одной команде по форме разрешён только один турнир; обе ноябрьские даты не автоматический двойной вход.'],
 ['Registrationновее неполного tournamentsoverview.','Национальный2026закрыт, будущий2027финал не датирован.'],[('Регистрация',kw),('Категории',kc),('Организатор',ks)])
profile('wro-nigeria','WRO Nigeria / Arc-Lights · основные категории и RoboStarter','regional','Основной обзор8–19; exactRoboStarterminunknown',
 'Канал национального организатора с отдельным вводным youngerмаршрутом; текущие даты и иностранные квоты не установлены.',
 [dict(name='Основные WROкатегории',age='Общий8–19, возраст конкретной discipline отдельно',team='Текущий localpack',hardware='По RoboMission/FI/RoboSports/FE',age_rule='Детальный seasonalcutoff подтвердить',entry='Arc-Lightsнациональныйорганизатор'),dict(name='RoboStarter',age='Младший вводный, ageне опубликован',team='Localprogrammeуточнить',hardware='Sumo/Training/Innovators/Kids',age_rule='Возраст6не доказан словомKids',entry='Настоящий набор или этап отдельно')],
 ['C1061','C1062'],'Найти действующий localpack и наставника → подтверждение age / foreignteam → qualifyingevent, если объявлен.',
 ['Общий8–19не означает доступ9во все дисциплины.','Нет текущих дат в прочитанном наборе.'],['RoboStarterвводный, не обещанныйworldfinal.'],[('Категории',nw),('RoboStarter',ns),('Сезон',nc)])
profile('robotchallenge-nigeria','RobotChallenge Nigeria / RC.CODE','regional','Primary7–11, Independent9–18; onlineRC.CODEnumericminunknown',
 'Роботы командой и onlinecoding индивидуально имеют разные формы и возрастные требования.',
 [dict(name='Nationalrobotics',age='Primary7–11/Independent9–18',team='Командаminorсcoach',hardware='Правила каждойdisciplineотдельно',age_rule='DOBвформе, следующаяредакциянеизвестна',entry='2026архивAbuja/Lagos'),dict(name='OnlineRC.CODE',age='Primaryschool; числовойminimumне опубликован',team='Индивидуально',hardware='Scratch/CREATiCODE; другиеязыкипоуровню',age_rule='Schoolstage и guardian',entry='Следующуюдату, foreigneligible и languageподтвердить')],
 ['C1063','C1064','C1065'],'Выбрать роботнуюdisciplineилиonlinecoding → текущийregulationиdate → minorconsent / foreignentry.',
 ['Шестилетнийне подходитPrimary7–11автоматически.','RC.CODEonlineне наследуетчисловойвозрастrobotteam.'],['Worldbrandingне доказываетмировоймасштабилиforeignquota.','Формаплатежанеподтверждает новыйнабор.'],[('Robotregistration',nr),('FAQ',nf),('Onlinecoding',u('ng_rccode'))])
profile('enjoy-africa','ENJOY AI African Open Ghana','regional','Общее3–22; categoriesпоfinaltechnicalpack',
 'Континентальный Open с международными делегациями через координаторов; точные дни и technicalageне установлены.',
 [dict(name='AfricanOpenchallenge',age='Согласованная approvedageband',team='По challengepack; coach/chaperone',hardware='Challengeplatformпоразрешённойкатегории',age_rule='Общий3–22не заменяетcategoryrules',entry='Schools/countrycoordinators/approvedinternationaldelegations')],
 ['C1066'],'Localtraining→organizercoordination→approvedcategory→continentalOpen; globalfinalqualificationотдельно.',
 ['Нужен окончательныйtechnicalpack, некоторыеlinkedPDFназваны2025.','Два заявленныхднябездатне календарнаябронь.'],['Mexico/CostaRicafamilyentryнеподтверждён.','AfricaOpenнеравенglobalworldfinal.'],[('AfricanOpen',ge)])
profile('creativity-rwanda','Creativity Lab Rwanda · project challenge / EN courses','regional','Архивchallenge8–11; ENcourses7–8и9–11',
 'Архивныйнациональныйproject и нынешниестраницыEnglishcoursesотделены от будущихbootcamps.',
 [dict(name='Projectchallenge',age='8–11архив2024/25',team='Soloилидо3',hardware='СобственныйSDG3solution',age_rule='Старыйнаборзакрыт',entry='Новыйсезоннеобъявлен'),dict(name='УчебныйIntermediate',age='9–11',team='Регулярныйкурс',hardware='Arduino/micro:bit/MakeCode',age_rule='Возрастучебнойгруппы',entry='Foreignchildиactualcohortподтвердить')],
 ['C1068','L373','L374','L376'],'ВозрастнойENкурс→самостоятельныйпроект→новаяобъявленнаяконкурснаязаявка, если появится.',
 ['Junior7–8пока не дляОскара6; Intermediate9–11дляМатвеяпо возрасту.','Englishcoursesне доказываютязыкcampилиjudge.'],['Финал14февраля2025не выдан за2026.'],[('Challenge',u('rw_challenge')),('EnglishIntermediate',u('rw_intermediate')),('EnglishJunior',u('rw_junior'))])

# Readable prose; protect source URLs, IDs and dictionary keys.
import re
def readable(v,key=''):
    if isinstance(v,dict):return {k:readable(x,k) for k,x in v.items()}
    if isinstance(v,list):return [readable(x,key) for x in v]
    if not isinstance(v,str) or key in ['id','entity_id','team_id','iso','school_id','event_id'] or v.startswith('http'):return v
    v=re.sub(r'(?<=[А-Яа-яЁё])(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])(?=[А-Яа-яЁё])',' ',v)
    return re.sub(r'(?<=\d)(?=[A-Za-zА-Яа-яЁё])|(?<=[А-Яа-яЁё])(?=\d)',' ',v)
new=[readable(e) for e in new];profiles=[readable(p) for p in profiles]
for s in d['schools'][-2:]:s.update(readable(s))
for r in d['school_history']['results'][-5:]:r.update(readable(r))
for r in d['school_history']['entities'][-5:]:r.update(readable(r))

country_rows=[
 ('KEN','Кения','Ближайшие младшие старты','Nairobi14ноября / Mombasa21ноября: Rookie6–9; school / foreigngateотдельно.','Rookie / Elementaryпо возрасту; national2027региональныйотбор обязателен.','Rookie6–9; договориться с teammate / schoolentry.','GrowthfluentialDecember8–18 — толькоМатвей; ENunknown. LogicLabs7–16, точныеsessiondays неизвестны.','KigwaRidge: национальныйElementarywinner2026; languageofinstructionи currentcoachнеустановлены.','Nairobi:schoolvisitиRookie; Mombasa — самостоятельный этап.','RookieKES12000/команда; GrowthDec12000/ребёнок. Транспорт / жильёотдельно.','ISS200, CropToppers195, GalaxyCoders180поофициальномупротоколу; schoollinkпоорганизатору.', ['C1057','C1058','C1059','C1060','L365','L366','L375','E171'],['wro-kenya'],['S039']),
 ('GHA','Гана','Роботные соревнования и международные учебные каналы','ENJOYAfricanOpenобщий3–22, categorypack / dateunknown; GRAFпутьRobofestпо школьномуклассу.','ENJOYapprovedcategory; RobofestExplorer1–4илиJunior5–8весной2027послекласса.','ENJOYcategoryнеподтверждена; CoastedExplorers6–9; GIScampследующегодатированногонабора пока нет.','Coastedявнопринимаетfamiliesworldwide,ENнеустановлен. GISстарыйcamp6–15иforeignadmissionдоказаны, даты2027необъявлены.','GIS: Englishinstruction, Juniorcoding/robotics; мировойтитулэтойшколы неустановлен.','Accra: internationalcamp/onlineпробаилиapproveddelegation, непоездка безdate.','GISархивGHS2000/неделя; Coastedрынковыйтарифотдельно, summerGhanaGHS1000за6недель.','APEX3718-1worldJuniorGame1st; Aurora6777-1worldSeniorGame2nd; schoolaffiliationнеизвестна.', ['C1066','C1067','L367','L368','L369','L370','L371','L372'],['enjoy-africa','robofest'],['S040']),
 ('NGA','Нигерия','Национальные и индивидуальные пути с разными gates','WROArc-Lightsи RobotChallenge — самостоятельныеорганизаторы; localrobotics и onlineRC.CODEне смешаны.','WROобщий8–19; RobotChallengePrimary7–11; actualnextseason/foreignentryуточнить.','WROосновной8+неподходит; RoboStarterageнеустановлен. RC.CODEPrimaryчисловойminunknown.','ДетскийEN/EScamp с датой и подтверждённым foreignдопуском в этомпроходе не установлен.','Новая постояннаяшколасдоказанным младшимрезультатом / foreignadmission неустановлена.','Lagos / Abujaтолькопослеactualcall; онлайнcodingальтернативабезtravelприforeigneligible.','RC.CODENGN10000individual; robotfeesпоdiscipline; expoвзрослыебилетыотдельно.','Worldbrandingнаregistrationнепротоколпобеды. СтарыеMay2026неближайшиеэтапы.', ['C1061','C1062','C1063','C1064','C1065','E169','E170'],['wro-nigeria','robotchallenge-nigeria'],[]),
 ('RWA','Руанда','Прямо подтверждённое английское обучение','CreativityLabIntermediate9–11:ENуказан; archivedchallenge8–11неоткрытый2026набор.','IntermediateENArduino/micro:bit20часов; группа / foreignchildдопуск отдельно.','JuniorEN7–8покараньше7неподходит; ChildBootcampageunknown.','Childrenbootcampбезновыхdates/age/EN; regularEnglishнеперенесён.','Постояннаямладшаяшколасworldresultв этомпроходе не установлена.','Kigali:GikondoрегулярнаяучебнаяпробаМатвею; Оскарус7последнярождения.','20часовIntermediate /16часовJunior; цена / новыеcohortsнеопубликованы.','Challengefinal14февраля2025:архив, не нынешний сезон; Worldawardнезаявлен.', ['C1068','L373','L374','L376'],['creativity-rwanda'],[]),
 ('ZAF','ЮАР','Сохранённые маршруты и повторная языковая проверка','WROSA,STEMLabSumoи SheenFIRST уже в базе; новыйOpenDay3октября и Festivecandidateотдельно.','FLLChallenge9–16 / Sumo9–11; nextcamp9+толькопоследопуска.','FLLExplore6–10 / Sumo6–8; Exploreпризнаниепроекта, не рейтинговаямедаль.','STEMLab28сентября–2октябряпоследнийдень; новыеDecember/2027datesнеобъявлены. У3учебныхкарточексняткандидатныйENтег.','Досьес подтверждённым младшимworldresultвэтойстране ещёне установлено.','CapeTownCenturyCity:OpenDay10–13или15–17,freeno booking; не основание срочнойдалекойпоездки.','SheenregularZAR280/урок; FestiveZAR750пообщемуанонсу; деталиnextgroupunknown.','СвоиFIRSTteamsи тренировочныезанятия отдельноот протоколовworldwins.', ['C715','C751','C752','C753','C756','C757','L037','L038','L088','L377','E100','E101','E172'],[],[]),
 ('MAR','Марокко','Крупная выставка для взрослых','GITEXAfricaимеетrobotics/AItrack; next2027datesв текущемFAQне найдены.','Нет: опубликовано18+; exception16–17только сошколой.','Нет: ниже18; familyexception6/9не заявлено.','ПодтверждённыйдетскийEN/ESrobotcampновогосезона в этомпроходе неустановлен.','Младшиешколыисторическиеprotocolsнеисследованыдостаточно.','Marrakech:взрослаяпрофпоездкапослеобъявленияdates, детейнепланироватьпоoldFAQ.','Nextticketfeeнеустановлен.','Профессиональнаявыставка, не соревнование детей.', ['E082'],[],[])]
cs=[]
for iso,name,verdict,reason,mat,osc,camp,school_text,city,budget,results,ids,pids,sids in country_rows:
    cs.append(dict(iso=iso,name=name,verdict=verdict,reason=reason,mat=mat,osc=osc,camp=camp,school=school_text,city_route=city,budget=budget,results_check=results,event_ids=ids,profile_ids=pids,school_ids=sids,risk='Наличие страницы и возрастной диапазон не подтверждают место семье, язык занятий / защиты, право иностранной мировой квоты или новые даты.'))
f=dict(version=41,checked=CHECKED,title='Африка: возрастные пути, каникулы и выставки',region_label='АФРИКА · МЛАДШИЕ ПУТИ И ПОДТВЕРЖДЁННЫЕ УСЛОВИЯ',heading='Новые страны. Отдельный маршрут каждому ребёнку.',family='Матвей2017,Оскар2020; английский / испанский / русский доступны; классы и дни рождения неизвестны.',
 conclusion='Для отдельной поездки сначала проверить NovemberRookieKenyaиactualforeignentry; для обученияМатвеяRwandaимеетявноеEN. Ghanaдаётpublishedinternationalonline/campканалы. Этиданные не меняютосновнойприоритетCostaRica/Mexicoи не доказываютвсехмероприятийАфрики.',countries=cs,
 shortlist=[dict(title='Ближайшие младшие турниры',detail='Nairobi14ноября(deadline8ноября),Mombasa21ноября(deadline15ноября). Rookie6–9пообзору; правилапотока / foreignschoolentry отдельно.',event_ids=['C1058','C1059']),dict(title='Матвею: EN обучение и Decemberкандидат',detail='RwandaIntermediate9–11прямоEN; GrowthDecember7–12декабря8–18с неизвестнымязыком. Оскарещёнепроходитниодиниз этихдиапазонов.',event_ids=['L373','L365']),dict(title='Большие tech-площадки',detail='NigeriaWDRS23–25марта2027/GITEX28–30сентября2027; childaccessunknown. MoroccoGITEX18+, nextdateunknown.',event_ids=['E169','E170','E082'])],
 evidence_cards=[dict(title='Кения · национальный результат школы',detail='ISS / KigwaRidge —1-еElementary2026,200баллов. Организаторпубликуетпротоколиотдельноschoolaffiliation.',limit='Currentcoach, младшаягруппаОскара,ENinstructionиforeignquotaнеподтверждены.',event_ids=['C1060'],school_ids=['S039'],source_urls=[u('ke_wro_results'),u('ke_results_school')]),dict(title='Гана · мировая победа команды',detail='APEX3718-1—1-еJuniorGameRobofest2026; Aurora6777-1—2-еSeniorGame. ПротоколLTU, не маркетинговоеWorldназвание.',limit='Не установленаcurrentK12schoolAPEX; Seniorawardне доказательство6/9juniorдоступа. Не приписанGIS.',event_ids=['C1067'],school_ids=[],source_urls=[u('robofest_2026_awards')]),dict(title='Гана · иностранный канал и язык раздельно',detail='GIScampFAQ прямоlocal/internationalstudents; Coastedopenfamiliesworldwide. GISEnglishschool имеетcoding/robotics вJunior.',limit='GIScamp2026закончился; ENшколы не перенесённаcamp. Coastedteachinglanguageнеустановлен.',event_ids=['L370','L371','L372'],school_ids=['S040'],source_urls=[u('gh_gis_faq'),u('gh_coasted_explore'),u('gh_gis_junior')]),dict(title='Руанда · точный Englishcourse',detail='Intermediate9–11:10занятий/20часов; Junior7–8:8занятий/16часов. ENуказанименнонастраницахуровней.',limit='Это регулярныекурсы; датированнаяENcampсменаилиforeignplaceнеподтверждены.',event_ids=['L373','L374','L376'],school_ids=[],source_urls=[u('rw_intermediate'),u('rw_junior')])],
 steps=[dict(title='Подтвердить actualentry',detail='Указатьобаyearofbirth,class,foreignschool иопыт3года; запроситьcurrentpack, teammate / coach, язык иправонаграды/qualification.'),dict(title='Сначала короткаяпроба',detail='Выбратьregulartrialилиdayprogramme среальнымEN/ESответом. Дляbeginnercurriculumпосле3летсоревнований проверитьпользууровня.'),dict(title='Разделитьfamily/adultvisits',detail='Studentbadgeилиpublicexhibitionне подтверждаетchild6/9. Купитьticketпослеchildpolicy выбранногоиздания; все adultgatesоставленывидимыми.')],
 limitations='Проход охватываетшестьнаправленийчастично. Egypt,Tunisia,Uganda,SenegalиостальныестраныАфрикисохраняютсявмировойбазе; полныйконтинентальныйкалендарь,allschoolsи5–10летрезультатовещёнеустановлены.',sources=[])
d['africa_focus']=readable(f)
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
known={s['url'] for s in d['sources']}
for key in sorted(used):
    url=urls[key]
    if url not in known:
        d['sources'].append(dict(url=url,title=key,checked=CHECKED,evidence='Прочитан первичный источник; actualevent / archivedseason / язык и foreignadmission разделены.'));known.add(url)
    d['africa_focus']['sources'].append(dict(title=key,url=url,checked=CHECKED))
d['asof']=CHECKED;d['expansion_log'].append(dict(version=41,checked=CHECKED,scope='Africa: Kenya / Ghana / Nigeria / Rwanda; ZA language recheck and MAR adult gate',added=len(new),new_profiles=len(profiles),new_schools=2,history_added=5,status='partial; worldwide goal active'))
a=d['completeness_audit'];a['validation_previous']=a.get('validation',{})
a.update(version=41,checked=CHECKED,status='Исследование продолжается',conclusion='Добавлено29карточек Африки,5профилей,2школьныхдосье и5результатовкоманд. Три candidateENтега сняты; exactdatesиforeignentryразделены. Мировойохватостаётсячастичным.',new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=updated,new_school_ids=['S039','S040'],updated_profile_ids=[],validation=dict(version=41,status='pending',publication='pending'))
d['camp_focus']['validation_previous']=d['camp_focus'].get('validation',{})
d['camp_focus'].update(version=41,checked=CHECKED,added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=updated[:3],conclusion='377 лагерных иучебныхкарточек. ДобавленпрямойENregularRwanda9–11,международныеGhanaканалы иKenyaNovember/Decemberprogramme; неизвестныйязыкнепревращёнвподтверждённый.',validation=dict(version=41,status='pending'))
d['school_focus'].update(version=41,checked=CHECKED,conclusion='40досье: новыеKigwaRidgeснациональнымElementaryпротоколом иEnglishGISсcoding/roboticsprogramme. Juniorcoach, admissionисметаотдельно; полныймировойрейтингнеустановлен.')
for obj in [a,d['camp_focus'],d['school_focus']]:
    obj['conclusion']=readable(obj['conclusion'])
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=[]
for name in ['receipt.json','receipt-extra.json']:
    rows.extend(json.loads((WORK/'sources-africa-v41'/name).read_text()))
# These sources were opened by web.run despite direct HTTP 406. Preserve both facts.
web_opened=['rw_intermediate','rw_junior','rw_challenge','rw_bootcamp','gh_gis_about','gh_gis_infant','gh_gis_junior']
receipt=dict(version=41,checked=CHECKED,scope='Africa primary sources',fetches=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in rows],used_names=sorted(used),alternate_web_opened=[dict(name=k,url=urls[k],read_via='web.run open / click; direct HTTP406 retained') for k in web_opened],remaining='Actualforeignadmission, campinstruction/cohorts, restofAfrica andworldremainincomplete.')
(ROOT/'data/africa-source-receipts-v41.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r['updated']=CHECKED
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=41,status='local_checks_pending_publication_pending');r['completeness_audit']='data/audit-v41.json'
r['research_passes'].append(dict(version=41,checked=CHECKED,scope='Africa current junior entry / camp language / adult exhibition gate',added_records=len(new),new_profiles=len(profiles),new_schools=2,history_added=5,status='partial',remaining='Allworldcoverage, restofAfrica, actualforeignentry andcohortlanguage/placesremain.'))
r['previous_goal_turn_classification']=dict(version=40,classification='progress',evidence='Published v40 commit3c12ea252fd967853a9d8acc857b722a3a7d9bc9; liveanonymousQAand37assethashesmatched.')
for req in r['requirements']:
    if req['id']=='unified_database':req['evidence']='v41:1616records;125profiles;40schools;131historyresults. Africaoverview / portableDB; worldwidepartial.'
    elif req['id']=='camps':req['evidence']='v41:377learning/camprecords; RwandaexplicitENcourses separatefromunknowncamp;3ZA candidateENtagsremoved.'
    elif req['id']=='exhibitions':req['evidence']='v41:172eventcards;2newregionalmajorexpos andconference/open-day; currentagegates/venueconfirmed separately.'
    elif req['id']=='permanent_schools':req['evidence']='v41:40schooldossiers;KigwaRidge2026nationalElementaryandEnglishGISprogramme;futurefamilyadmissionunknown.'
    elif req['id']=='school_retrospective':req['evidence']='v41:131boundedresults;KenyanElementarynationalandGhanaRobofestworldstage;5–10yearworldrankingpartial.'
r['next_research'].insert(0,'Africa v41: KenyaRookieforeignschoolteam / currenttechnicalpack; GhanaENJOYexactdatesandnonAfricafamilyentry; GRAF2027localcalls / Explorergrade; RwandaactualEnglishcohort / childbootcamp; NigeriaactualRC.CODEcalendar / foreigneligibility; ZAnewDecembercohorts andinstruction; Morocco2027newpolicy/date. AllotherAfricacountries andworldauditcontinue.')
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=41,added=len(new),profiles_added=len(profiles),schools_added=2,history_added=5,records=len(d['events']),updated_ids=updated,world_complete=False)))
