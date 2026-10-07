"""A second bounded CHE/ESP/FRA audit, with explicit junior and language gates."""
import ast, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1317 and d['completeness_audit']['version']==31
CHECKED='2026-10-01';new=[];profiles=[];byid={e['id']:e for e in d['events']}
for node in ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text()).body:
    if isinstance(node,ast.FunctionDef) and node.name in ['ref','event','profile']:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base_event=event
def add(*args,**kwargs):
    e=base_event(*args,**kwargs);e['region']='Европа';return e
COND='Условно: возрастная ступень подходит; место, технический язык и иностранный приём подтвердить'
YOUNG='Нет: младше минимального возраста этой технической группы'
lg='https://www.la-garenne.ch/summer-camps/'
lgform='https://www.la-garenne.ch/summer-camps/apply-online/'
lgrobot='https://www.la-garenne.ch/summer/repository/summer_robotics_workshop.pdf'

# Published camp windows, not a claim of two weeks of daily robotics.
for id,mode,start,end in [
    ('L249','residential','2027-06-27','2027-07-10'),
    ('L250','residential','2027-07-11','2027-07-24'),
    ('L251','residential','2027-07-25','2027-08-07'),
    ('L252','day_camp','2027-06-28','2027-07-09'),
    ('L253','day_camp','2027-07-12','2027-07-23'),
    ('L254','day_camp','2027-07-26','2027-08-06')]:
    boarding=mode=='residential'
    e=add(id,'La Garenne 2027 · Robotics option · '+('пансион' if boarding else 'дневная смена')+' · '+start[5:],
        'Швейцария','Villars-sur-Ollon',lgform,'Robotics 8–12; общий лагерь 5–16',COND,
        'Нет: в лето 2027 ребёнку 2020 года только 6–7, а Robotics начинается с 8',
        'Выбрать Robotics как дополнительную опцию; иностранная application предусмотрена, принятие и слот не подтверждены.',
        'VEX IQ, Python, CAD / 3D-печать; старший V5 по уровню.',block='Лагеря',start=start,end=end,
        participation='day_camp',scope='international',date_scope='camp_window',evidence='program',
        cost=('Пансион от CHF 7 200 / 2 недели' if boarding else 'Day от CHF 6 550 / 2 недели')+' + Robotics CHF 500; страховка non-Swiss CHF 10 / день, поездка отдельно.',
        note='Это языковой / adventure лагерь с короткой технической опцией. Утренний EN/FR не доказывает EN именно Robotics. Сайт описывает 3 занятия; финал PDF говорит о 2 — число и часы уточнить. В общей программе ребёнок с 5 лет не получает автоматически Robotics 8+; учебный сертификат не турнирная награда.')
    e.update(participation=mode,format='Пансион; полное размещение' if boarding else 'Дневная смена; семейное жильё отдельно',
        admission_kind='foreign_application',references=[ref('Основная программа 2027: стоимость / включения',lg),ref('Технический модуль 8–12',lgrobot)],
        language='Утренние классы EN или FR опубликованы; язык отдельного технического модуля не установлен.',languages=[],language_mode='unconfirmed')
    if id in ['L249','L252']:e['note']+=' Форма предлагает также продление до 24/23 июля; четыре недели не отдельная независимая смена.'
    if id in ['L250','L253']:e['note']+=' Форма предлагает также продление до 7/6 августа; четыре недели не отдельная независимая смена.'

swkids='https://wro.swiss/en/courses/courses-for-kids/'
swde='https://wro.swiss/kurse/kurse-fuer-kinder-und-jugendliche/'
for id,city,start in [('L255','Winterthur','2026-10-24'),('L256','Yverdon','')]:
    e=add(id,'WRO Switzerland · семейный SPIKE Prime workshop · '+city,'Швейцария',city,swkids,
        'С родителем: младший минимум не указан; без родителя только 10+ по согласованию',
        'Условно: с родителем, минимальный возраст и уровень подтвердить',
        'Условно: с родителем; минимум 6 лет прямо не опубликован',
        'Семейная группа 1–2 взрослых и 1–2 детей; конкретный младший допуск и EN уточнить.',
        'SPIKE Prime, сенсоры, циклы и автономный line follower.',block='Лагеря',start=start,participation='holiday_workshop',
        cost='CHF 100 / семья; без родителя 10+ по договорённости CHF 65.',date_scope='activity_start',
        note='Учебная встреча родителей и детей, не команда турнира WRO и не квалификация. Для опытных детей проверить сложность; семейная мастерская не подтверждает право на швейцарскую мировую квоту.')
    e.update(references=[ref('Немецкая версия расписания',swde)],start_time='13:30',end_time='16:30',timezone='Europe/Zurich')
    if not start:e.update(period='Предложено 29 ноября 2026, 13:30–16:30; обе страницы называют день субботой, но календарно это воскресенье.',date_status='Уточнить',note=e['note']+' Из-за противоречия даты / дня недели запись не включена в подтверждённый ICS.')

epfl='https://www.epfl.ch/education/education-and-science-outreach/fr/jeunepublic/camps/'
e=add('L257','EPFL Lausanne · Mon robot est malin · будущая ступень','Швейцария','Lausanne · EPFL',epfl,
    '11–13 лет; возрастные границы обязательны',YOUNG,YOUNG,
    'Новый набор 2027 планируют открыть в марте; конкретный день не объявлен. Нужны 11 лет, язык и иностранный допуск.',
    'Роботы, лабиринты, сенсоры, задания FLL и знакомство с университетом.',block='Лагеря',participation='day_camp',priority='P4 — будущая возрастная ступень',
    cost='CHF 50 регистрация / перекусы по текущей программе; CHF 500 — субсидируемая себестоимость, не семейный счёт.',
    note='Октябрьская смена 19–23 октября 2026 и waitlist уже полные. Даты смен 2027 не придуманы; март — окно открытия регистрации. EN / ES занятия не подтверждены. Один лагерь на ребёнка в год; пансиона нет.')
e.update(period='Кандидат после 11 лет; регистрация 2027 ожидается в марте, даты лагерей пока не объявлены.')

unicaja='https://www.fundacionunicaja.com/blog/fundacion-unicaja-abre-las-inscripciones-de-sus-campus-2026/'
evad='https://evadformacion.com/segunda-edicion-del-campamento-techplay-con-fundacion-unicaja/'
e=add('L258','Fundación Unicaja / EVAD · Tech&Play · следующий летний набор','Испания','Ronda · Colonia Las Delicias',unicaja,
    '7–16 по программе 2026; минимум следующего набора подтвердить',COND,'Будущий кандидат с 7 лет; день рождения и правила следующего набора подтвердить',
    'Робототехника / games / AI в летней программе; уточнить новый сезон, техническую долю EN, уровень и иностранное место.',
    'Технологические проекты, игры и AI; платформу и часы младшей группы уточнить.',block='Лагеря',participation='day_camp',scope='national',evidence='historical_program',
    note='Смена 16–23 августа 2026 завершена; новый летний календарь не опубликован. Оператор прямо заявляет английскую языковую иммерсию, но 100% EN каждого технического урока не установлены. Общий отчёт сети о 18 национальностях не подтверждает место семьи именно Tech&Play.')
e.update(participation='residential',format='Летняя программа с проживанием; новый тариф уточнить',language_mode='support',languages=[],support_languages=['EN'],
    language='English immersion заявлена для этой программы; язык всех технических объяснений и ES-поддержку подтвердить.',references=[ref('Партнёр EVAD: программа 2026',evad),ref('Проживание / реально проведённая смена','https://www.fundacionunicaja.com/campus/2026/08/17/vuelve-la-aventura-mas-tecnologica-del-verano-arranca-techplay-2026/')])

ct='https://camptecnologico.com/talleres-tecnologicos-para-ninos/'
e=add('L259','Camp Tecnológico · регулярная робототехника 2026/27','Испания','Basauri / Bilbao / Vitoria · выбранную sede подтвердить',ct,
    'Оператор 5–17; точная регулярная младшая группа не опубликована',COND,COND,
    'Открыта регистрация регулярных групп по возрасту и уровню; выбрать sede и подтвердить ES вместо другого местного языка.',
    'Robotics / coding; точное оборудование зависит от группы.',block='Лагеря',participation='day_camp',date_scope='activity_start',
    note='Октябрь 2026–июнь 2027, один час в неделю, будние слоты 17:30 или 18:30. Это учебный курс, не девятимесячный лагерь. Дата первого занятия неизвестна, поэтому годовой интервал не экспортирован в ICS. ES / EN преподавание прямо не установлены; испанская страница сама по себе не доказательство.')
e.update(participation='regular',format='Регулярные очные занятия · 1 час / неделя',period='Октябрь 2026–июнь 2027; конкретный день / место / младшая группа уточнить')
for id,name,age,mat,osc,url in [
    ('L260','Junior','6–9; младшие 5–6 только если умеют читать',COND,'Условно: в 6 лет обязательна способность читать; язык чтения / набор подтвердить','https://camptecnologico.com/talleres-junior-verano/'),
    ('L261','Genius','9–12',COND,YOUNG,'https://camptecnologico.com/taller-genius-verano/')]:
    e=add(id,'Camp Tecnológico · '+name+' · отдельный технический трек','Испания','Madrid / Bilbao / другие опубликованные sedes; следующий набор уточнить',url,age,mat,osc,
        'Выбрать новую местную смену; опубликованное описание трека не является местом в будущем лагере.',
        'Роботы, micro:bit и программирование Minecraft.',block='Лагеря',participation='day_camp',evidence='program',date_scope='camp_window',
        note='Самостоятельные возрастные треки одного оператора, связаны с обзорной L002. Новый каникулярный календарь не объявлен. Для детей с трёхлетним опытом вводные испытания могут быть простыми; попросить собственный проект и сложность по уровню. ES / EN именно в выбранной sede уточнить.')
    e['related_ids']=['L002','L259']
old=byid['L002'];old.update(checked=CHECKED,age='Отдельные треки: Junior6–9 (5–6 только с чтением), Genius9–12; площадка / смена отдельно',
    proof='Повторно прочитаны страницы Junior / Genius. Уточнены возраст, возможность для шестилетнего при чтении и неподтверждённый язык конкретной группы.')
old.update(**{'mat': 'Условно: Junior 6–9 или Genius 9–12; конкретный уровень, язык и иностранный приём подтвердить', 'osc': 'Условно: Junior 6–9; в 6 лет обязательно уметь читать, язык чтения и место подтвердить', 'language': 'Технический язык конкретной площадки ES / EN нужно подтвердить; язык сайта не доказывает язык занятия.', 'languages': [], 'language_mode': 'unconfirmed'})
old['references']=old.get('references',[])+[ref('Junior: чтение для младших','https://camptecnologico.com/talleres-junior-verano/'),ref('Genius9–12','https://camptecnologico.com/taller-genius-verano/')]

mai='https://www.magicmakers.fr/products/explore-le-monde-des-intelligences-artificielles-primaires'
mmc='https://www.magicmakers.fr/products/concois-tes-jeux-dans-lunivers-minecraft'
for id,name,city,period,age,url,cost,gear,mode in [
    ('L262','AI Junior · онлайн · Toussaint','Онлайн · французский часовой пояс','26–30 октября текущего набора; 13:30–16:00','CE2–CM2; для младших читать / писать',mai,'EUR 250','AI: правила, данные, критическое мышление и свой мини-проект.','online'),
    ('L263','AI Junior · онлайн · Noël','Онлайн · французский часовой пояс','21–24 декабря текущего набора; 09:30–12:00','CE2–CM2; для младших читать / писать',mai,'EUR 215','AI: правила, данные, критическое мышление и свой мини-проект.','online'),
    ('L264','AI Junior · Paris · Noël','Paris7 · Saint-Thomas-d’Aquin, 44 rue de Grenelle','21–23 декабря текущего набора; первые два дня 09:30–16:00, среда 09:30–12:00','CE2–CM2; для младших читать / писать',mai,'EUR 265','AI: правила, данные, критическое мышление и свой мини-проект.','day_camp'),
    ('L265','Minecraft Junior · Paris · Toussaint','Paris16 · École Pascal','19–23 октября текущего набора; 09:30–12:00','CE2 опытные / CM1–CM2 начинающие и опытные',mmc,'EUR 265','Minecraft Education: код блоками и свой мини-game.','day_camp')]:
    e=add(id,'Magic Makers · '+name,'Франция',city,url,age,
        'Условно: требуется соответствие французскому классу; класс Матвея и EN подтвердить',
        'Нет для обычной шестилетней школьной ступени: нужен CE2 или выше; индивидуальный допуск не установлен',
        'Публичная форма выбранного трека; подтвердить год, класс, технический EN и свободное место.',gear,
        block='Лагеря',participation='day_camp',cost=cost,evidence='program',date_scope='camp_window',
        note='В расписании указаны день / месяц и будни, но нет явного года. Текущий сайт 2026/27 указывает на осень / декабрь 2026; это вывод по контексту, а не отдельная дата организатора. Поэтому start/end пустые и записи не в подтверждённом ICS. Embedded variants available=true на дату проверки; это не бронь. Технический EN / ES не опубликован.')
    e.update(participation=mode,format='Онлайн · собственный компьютер / camera / headset' if mode=='online' else 'Очная дневная программа; оборудование предоставляется',period=period+' · год и доступ подтвердить',date_status='Уточнить')

cite='https://origine.cite-sciences.fr/fr/au-programme/lieux-ressources/bibliotheque/thematiques/enfants-familles/activites/ateliers-robotique'
for id,start in [('L266','2026-10-23'),('L267','2026-10-30')]:
    e=add(id,'Cité des sciences · Un robot en balade · '+start[5:],'Франция','Paris19 · библиотека Cité des sciences',cite,
        '9–11',COND,YOUNG,'Полудневный stage; выбрать дату, подтвердить язык занятия и доступность.',
        'LEGO / программируемый робот; вводная практика.',block='Лагеря',start=start,participation='holiday_workshop',date_scope='activity_start',cost='EUR 45 / ребёнок; EUR 35 abonnes по опубликованному тарифу.',
        note='10:00–13:30, не полный день и не пансион. EN / ES техническое обучение не заявлено. Для опытного ребёнка проверить уровень; диплом не соревновательная награда.')
    e.update(start_time='10:00',end_time='13:30',timezone='Europe/Paris')
for id,name,age,osc,gear in [('L268','Les défis de Photon','6–9',COND,'Photon: последовательность команд и задачи.'),('L269','Electro-Robot','9–12',YOUNG,'LittleBits и Sphero RVR; сенсоры и программирование.')]:
    e=add(id,'Cité des sciences · '+name+' · семейная робототехника','Франция','Paris19 · библиотека Cité des sciences',cite,
        age,COND,osc,'Билет ребёнку и сопровождающему 16+; будущую дату / часы / EN уточнить.',gear,
        block='Лагеря',participation='holiday_workshop',cost='EUR 15 / человек, EUR 10 abonnes; платят и ребёнок, и сопровождающий.',
        note='На ребёнка максимум 2 сопровождающих, на одного взрослого максимум 2 ребёнка. Даты основной страницы не опубликованы; не добавлено фиктивное ежедневное событие. Уроки EN / ES не подтверждены. Учебная семейная мастерская, не турнир.')
clubs='https://origine.cite-sciences.fr/fr/au-programme/activites-spectacles/ateliers-stages-clubs/les-clubs-de-science'
e=add('L270','Cité des sciences · Club Robotique niveau2 · курс 2026/27','Франция','Paris19',clubs,
    '9–14',COND,YOUNG,'Уточнить место после старта годового курса, требуемый уровень и EN / ES.',
    'Годовой проект углублённой робототехники; точный набор уточнить.',block='Лагеря',participation='day_camp',date_scope='activity_start',
    note='Опубликованный период 23 сентября 2026–16 июня 2027; занятия по средам 2 часа во время учебных недель. Даты уже начавшегося курса не превращены в непрерывный лагерь. EN / ES не установлены.')
e.update(participation='regular',format='Регулярный годовой club · 2 часа / учебная среда',period='23 сентября 2026–16 июня 2027 · учебные среды; место после начала курса уточнить')

rcj='https://www.robocup.fr/onstage'
rcjevent='https://www.robocup.org/events/82'
e=add('C928','RoboCupJunior France · Discovery · младший проектный маршрут','Франция','Местный этап / national следующего сезона пока не объявлен',rcj,
    'Обзор: maternelle / CP–CE2; ниже на той же странице Cycle1–3. OpenFrance2026:5–10. Правила нового этапа уточнить.',
    'Условно: возраст 9 / начальная школа; из-за расхождения классов конкретный этап подтвердить',
    'Условно: младшая школьная группа; семейную команду иностранцев и язык не установлены',
    'Проект школьной / детской группы; размер команды, самостоятельную family team и иностранный приём подтвердить.',
    'Своё роботизированное выступление / демонстрация.',scope='national',
    note='Discovery не имеет общего рейтинга, хотя специальные отличия возможны. Прямо не соответствует наднациональной лиге; через неё не получают мировой слот RCJ. OpenFrance30–31 мая 2026 прошёл, даты 2027 не перенесены. Мировые правила 14+ не запрет для этой отдельной младшей демонстрации.',cost='OpenFrance2026:EUR 100 / team; Discovery-specific и новый тариф уточнить.')
e.update(reward='Презентация / возможное специальное отличие; общего рейтинга и мирового отбора Discovery нет.',references=[ref('Федерация: прошедший Open France 2026 и Discovery5–10',rcjevent)])
e=add('C929','RoboCupJunior France · OnStage Entry · будущая ступень','Франция','Новый местный этап не датирован',rcj,
    '10–13 на французской странице; актуальный cutoff / правила 2027 подтвердить',
    'Будущий кандидат с 10 лет: для 2017 года нужен cutoff конкретного сезона',YOUNG,
    'Выбрать local Entry event и подтвердить новые правила, team size, иностранный вход и EN judging.',
    'Автономные физические роботы, техническое объяснение и выступление.',scope='national',priority='P4 — будущий возраст / новый регламент',
    note='На текущей странице правила Standard 2026, а правила Entry 2025: это разные редакции. Entry для младших не гарантирует право участия в мировом Standard. Французский сайт не доказывает язык EN-интервью.')

rm='https://www.wroboto.es/robomission/'
for id,name,age,mat in [('C930','Start','8–12',COND),('C931','Rookie','11–15','Будущий кандидат после 11 лет; новый календарный cutoff подтвердить')]:
    e=add(id,'WRO Spain · RoboMission '+name+' · упрощённая автономная ступень','Испания','Выбранный местный организатор / следующий сезон не объявлен',rm,age,mat,YOUNG,
        'Команда 2–3 + coach по национальным условиям; выбрать tournament именно Start / Rookie и проверить допуск иностранцев.',
        'Автономный робот до 25×25×25 см; hardware свободный, компактные коммерческие robots исключены; technical sheet.',scope='national',
        priority='P2 — младший автономный маршрут после проверки' if id=='C930' else 'P4 — будущая возрастная ступень',
        note='Start использует Elementary board с упрощёнными правилами; Rookie — Junior board. Они имеют отдельные национальные результаты, но в опубликованной мировой квоте Spain2026 Start / Rookie не указаны. Это не RoboBasic с 6 лет и не мировой слот Elementary. Training прямо не официальная категория.')
    e['references']=[ref('Национальные результаты и мировые slots2026','https://www.wroboto.es/torneos/'),ref('Training — практика, не официальная категория','https://www.wroboto.es/training/')]
wp=next(p for p in d['league_guide']['profiles'] if p['id']=='wro-spain')
wp['categories'].extend([dict(name='RoboMission '+name,age=age,team='2–3 + coach',hardware='Автономный робот / соответствующий board',age_rule='Возраст исполняется в календарном году по общим правилам; новый season cutoff проверить',entry='Упрощённая национальная ступень; нет заявленного мирового Start / Rookie slot') for name,age in [('Start','8–12'),('Rookie','11–15')]])
wp['event_ids'].extend(['C930','C931']);wp['nuances'].extend(['Training — учебное упражнение, прямо не официальная соревновательная категория.','Spain2026: RoboMission Elementary2worldslots, FutureInnovators Elementary1; квоты 2027 и национальный допуск семьи не установлены.']);wp['sources'].extend([dict(title=t,url=u,checked=CHECKED) for t,u in [('Start/Rookie ages and hardware',rm),('National results versus world quota','https://www.wroboto.es/torneos/'),('Noncompetitive Training','https://www.wroboto.es/training/')]])
profile('robocup-france-junior','RoboCupJunior France · Discovery / OnStage Entry','regional','Младшая Discovery по классу; Entry 10–13; мировой Standard отдельно',
    'Даёт проектную младшую ступень и будущую соревновательную Entry. Discovery не мировой отбор и не рейтинговая победа.',
    [dict(name='Discovery',age='Cycle1–3 в теле страницы; обзор до CE2; Open2026:5–10',team='Школьная / детская группа; размер и вход иностранцев уточнить',hardware='Свой роботизированный проект',age_rule='Конкретный event rule важнее несовпадающих общих описаний',entry='Без общего рейтинга; международного аналога нет'),dict(name='OnStage Entry',age='10–13',team='Подтвердить новый local rule',hardware='Автономные роботы + выступление',age_rule='Cutoff2027 не опубликован в прочитанном источнике',entry='Младшая национальная Entry, мировой Standard отдельно')],
    ['C928','C929'],'Discovery: представить свой проект → Entry после возраста / языка → Standard и национальный отбор по актуальным международным правилам.',
    ['Дети самостоятельно объясняют свою механику / код.','EN judging, семейную команду иностранцев и сезон 2027 пока не подтверждены.','Название RoboCup не делает любое отличие мировой медалью.'],
    ['Discovery age / grade descriptions расходятся.','Entry rules2025 не выданы за обновлённый регламент 2027.','Даты OpenFrance2026 прошли.'],[('French OnStage / junior levels',rcj),('Federation: Open2026 Discovery',rcjevent)])

tech='https://www.live.technorama.ch/en/visit/faq'
e=add('E143','Technorama Winterthur · семейный центр экспериментов','Швейцария','Winterthur · Technorama',tech,
    'Младшие дети приветствуются; до 12 лет обязательно взрослый',COND,COND,
    'Выбрать день посещения; отдельную возрастную мастерскую и EN-ведущего бронировать только после подтверждения.',
    'Экспериментальные станции и конструирование; не промышленная выставка всех брендов.',block='События',participation='visitor',
    language='Тексты станций DE / FR / IT / EN; стандартные shows / workshops на DE. Иной язык — по запросу.',languages=('EN','DE','FR','IT'),
    note='Постоянная семейная площадка; конкретная поездка не датирована. English signage не равно английскому ведущему. Подходит для семейного hands-on посещения после проверки выбранных мастерских.')
e.update(exhibition_tier='family_alternative',visitor_policy='family',visitor_policy_note='Дети младше 12 только с взрослым; отдельный workshop может иметь собственный возраст.',
    adult_entry='Обычный visitor ticket; текущий тариф проверить.',highlights=['Hands-on эксперименты','Tinkering Lab','EN-тексты'],exhibitor_note='Постоянный science centre, не trade show и не перечень всех компаний.',exhibitor_directory_url='https://www.live.technorama.ch/en/home',language_mode='materials')
robots='https://www.cite-sciences.fr/fr/au-programme/expos-permanentes/les-expositions/robots'
access='https://www.cite-sciences.fr/fr/ma-cite-accessible/expositions-permanentes/robots'
e=add('E144','Cité des sciences Paris · постоянная экспозиция Robots','Франция','Paris19 · Cité des sciences',robots,
    'Accessibility presentation: от 11 лет; исключение / младший сопровождаемый вход уточнить',
    'Условно: младше указанной 11+ аудитории; сопровождаемый допуск подтвердить',
    'Условно: младше указанной 11+ аудитории; лучше сначала Photon6–9',
    'Проверить доступ именно 6/9 лет и язык; обычный билет Expositions не доказательство подходящего workshop.',
    'Действующие роботы, автономность, социальные вопросы и роботизированная инсталляция.',block='События',participation='visitor',
    note='Это постоянный музейный маршрут, не международная выставка всех производителей. Презентация accessibility указывает 11+; формальный запрет младшим в прочитанном тексте не установлен, исключение не обещано. Отдельные L268/L269 имеют подтверждённые младшие возрастные группы.',priority='P3 — младший доступ уточнить')
e.update(exhibition_tier='family_alternative',visitor_policy='confirm_children',visitor_policy_note='Публикуется 11+ аудитория; допуск 6/9 сродителем требуется подтвердить.',adult_entry='Билет Expositions; тариф выбранного дня отдельно.',
    highlights=['Реальные роботы','Автономность и сенсоры','TROBO'],exhibitor_note='Museum exhibition; roster промышленных компаний не заявлен.',exhibitor_directory_url=robots,references=[ref('Возраст 11+ в accessibility presentation',access)],related_ids=['L268','L269','L266','L267'])
af='https://www.advancedfactories.com/en/'
faq='https://www.advancedfactories.com/en/visit/faqs/'
e=add('E145','Advanced Factories Barcelona 2027 · automation / robotics / AI','Испания','Barcelona · Fira Gran Via',af,
    'Professional event; studentroute: final-year undergraduate / master, не дети 6/9',
    'Нет опубликованного младшего входа; возможное исключение требует письменного ответа',
    'Нет опубликованного младшего входа; возможное исключение требует письменного ответа',
    'Взрослый professional pass. Семейное исключение не подтверждено; student route не применять к начальной школе.',
    'Industrial robots, automation, AI, Industry4.0 и manufacturing.',block='События',start='2027-03-31',end='2027-04-02',scope='international',participation='visitor',priority='P3 — профессиональное посещение взрослым',
    note='FAQ прямо называет мероприятие исключительно professional. Student access: только finalday2 апреля 2027 с 13:30, профильные graduates / masters и priorapproval. Полный exhibitor list обещан примерно за месяц; прежние logos не выданы за подтверждённый roster2027.')
e.update(exhibition_tier='profile',visitor_policy='confirm_children',visitor_policy_note='Детский вход 6/9 не опубликован; обычная студенческая схема им не подходит.',adult_entry='Professional registration / badge; выбранный тариф проверить.',
    highlights=['Industrial robotics','Automation','AI / Industry4.0'],exhibitor_note='Актуальный roster2027 ещё не опубликован: FAQ обещает примерно за месяц.',exhibitor_directory_url=faq,references=[ref('Student eligibility / exhibitor publication',faq)])

def src(title,url,claim,kind='school'):return dict(title=title,url=url,claim=claim,kind=kind,checked=CHECKED)
high='https://www.highlandssevilla.es/realmente-conectados/'
highprimary='https://www.highlandssevilla.es/colegio-privado-sevilla/'
highresult='https://www.dipusevilla.es/comunicacion/noticias/Los-participantes-en-la-competicion-de-Robotica-WRO-demuestran-su-destreza-y-competitividad/'
lar='https://colegiolar.es/'
larresult='https://colegiolar.es/el-colegio-lar-se-convierte-en-el-epicentro-de-la-robotica-con-la-wro-vigo-2026/'
bis='https://www.bordeaux-school.com/learning/primary'
biscode='https://www.magicmakers.fr/products/bordeaux-bordeaux-international-school'
schools=[dict(id='S026',name='Highlands School Sevilla',iso='ESP',country='Испания',region='Европа',city='Montequinto / Sevilla',school_type='private',
    curriculum='Испанская школьная траектория и bilingüe / Cambridge positioning по школе; IB не установлен.',ib_programmes=[],ages='Primaria6–12; робототехнический уровень и конкретная команда по классу отдельно.',instruction_languages=[],
    language_note='Школа заявляет bilingual profile; предметные доли ES/EN и язык младшей Robotics группы не установлены.',
    fit=dict(mat='candidate',osc='candidate',note='Школьная возрастная ступень подходит условно; конкретные robotgroup / приём иностранцев не доказаны.'),boarding='unknown',boarding_note='Пансион не установлен; планировать проживание семьи.',
    programme='Realmente Conectados: от computational thinking в Infantil к анализу данных и технологическим проектам в Primaria. Есть внешний региональный результат FI.',labs='Конкретные младшие robotkits и lab hours не опубликованы в прочитанных страницах.',ai='В Primary описываются данные / цифровая компетентность; отдельный AI engineering course6 лет не подтверждён.',
    results=[dict(season='2024',league='WRO Future Innovators',stage='Местный отбор Sevilla',award='Farmbites — первое место местной категории; проход в national.',source=highresult,provenance='organizer_protocol',note='Публикация организатора Diputación / INPRO. Не мировой титул и не доказанная победа primary team; школу не смешивать с CEIP El Pinar Olivares.')],
    evidence='other_result',admissions='Gradeplacement, языковая оценка, juniormentor / часы / команда и новые результаты уточнить.',cost='Тариф учебного года и отдельной Robotics группы не установлен.',
    questions=['Какая группа и текущий код команды доступны детям 2017/2020?','Покажите результаты 2024–2026 именно младшей команды и текущего наставника.','Какие предметы и robotjudging проходят на ES / EN?'],
    sources=[src('Primaria6–12 и bilingual school',highprimary,'Школьная ступень, не мировое лидерство'),src('Realmente Conectados',high,'Технологическая программа по этапам'),src('Региональный результат 2024',highresult,'Farmbites local first / national qualification',kind='organizer')]),
    dict(id='S027',name='Colegio Lar',iso='ESP',country='Испания',region='Европа',city='Mos / Vigo · Camino Eido de San Antonio3',school_type='private',curriculum='Infantil / Primaria / ESO / Bachillerato; IB не установлен.',ib_programmes=[],ages='Школьные ступени от Infantil до Bachillerato; текущая робототехника Primary требует проверки класса.',instruction_languages=[],
    language_note='Язык общей школы / младшей Robotics и доля ES / Galician / EN не подтверждены прямым расписанием.',fit=dict(mat='candidate',osc='candidate',note='Возраст соответствует школьному поиску; турнирный допуск 6 лет и робототехническое место не обещаны.'),boarding='unknown',boarding_note='Размещение / пансион не установлен; семья живёт отдельно.',
    programme='Школа принимала WRO Vigo2026; опубликован полный Elementary podium школы. Проверить регулярный mentor / primary team и отдельную RoboBasic группу.',labs='Оборудование и недельные lab hours не установлены.',ai='Самостоятельный AI curriculum младших не доказан.',
    results=[dict(season='2026',league='WRO RoboMission',stage='Региональный Vigo',award='Школа сообщает 1–3 место Elementary и 2 место Junior.',source=larresult,provenance='school_report',note='Три Elementary winners у WRO: Las Princesas, La Vaca Lola, Girls Legolar. School ownership указан школой; национальное / мировое место этим не доказано.')],evidence='other_result',
    admissions='Подтвердить класс, язык, приём иностранцев, младшую RoboBasic группу и командный слот.',cost='Школьная стоимость / robotics extras текущего года не установлены.',
    questions=['Кто тренирует Elementary2026 в 2026/27 и сколько часов?','Есть ли отдельная группа 6 лет и регулярная RoboBasic?','Есть ли национальные / мировые протоколы последних 5 лет для этих teamcodes?'],
    sources=[src('Школа и ступени',lar,'Private school / уровни обучения'),src('WRO Vigo2026: собственный отчёт',larresult,'1–3 места Elementary, Junior2'),src('WROSpain: published winners','https://www.wroboto.es/torneos/','Vigo winning teamnames; worldquota отдельно',kind='organizer')]),
    dict(id='S028',name='Bordeaux International School',iso='FRA',country='Франция',region='Европа',city='Bordeaux',school_type='private',curriculum='Primary bilingual FR/EN; выше Cambridge IGCSE / International A Level. IB не подтверждён.',ib_programmes=[],ages='Primary 6–10; Magic Makers конкретный трек по классу CE1–CE2 / CE2–CM1 и далее.',instruction_languages=['EN','FR'],
    language_note='Primary прямо двуязычная. Язык отдельного Magic Makers coding и возможность учиться технический день только на EN не установлены.',fit=dict(mat='candidate',osc='candidate',note='Оба по возрастной школьной ступени кандидаты; coding дляОскара только при подходящем CE1/CE2, не автоматически в 6 лет.'),boarding='unknown',boarding_note='Пансион младших не установлен; host families старшей ступени не перенесены на 6/9 лет.',
    programme='School partnership с Magic Makers: Scratch / Minecraft junior, старшие coding / games / AI; постоянная competitionrobotteam не установлена.',labs='Coding courses по grade; специализированный robotics lab не подтверждён.',ai='AI присутствует у старшего DeveloperCM2–5ème; не обещано Оскару.',results=[],evidence='programme',
    admissions='Школа приветствует local / international families; grade, поддержка без FR и уровень кодинга / EN инструктор требуют оценки.',cost='Отдельная операторская coding страница показывает EUR 695, другие варианты различаются; tuition и тариф именно группы не установлены.',
    questions=['Сколько FR нужно новичкам 6/9 и какая ежедневная поддержка?','Можно ли Coding проходить на EN и какие возрастные группы по классу доступны детям?','Есть ли текущая league team с mentor / code / national results?'],
    sources=[src('Primary 6–10 и bilingual learning',bis,'Школьная Primary'),src('Current partner coding by grade',biscode,'Scratch / Minecraft и старшие tracks; не worldresult',kind='school_operator'),src('School overview','https://www.bordeaux-school.com/','International families / Cambridge upper path')])]
for s in schools:
    s.update(checked=CHECKED,priority=2,research_status='partial',verification='Первичные программы и конкретные отчёты прочитаны. Место, приём и новая младшая команда не подтверждены.')
    for r in s['results']:
        r.update(team='Farmbites' if s['id']=='S026' else 'Las Princesas / La Vaca Lola / Girls Legolar; имя Junior отдельно',team_id='',limit=r['note'])
        if s['id']=='S026':r['provenance']='organizer_report'
d['schools'].extend(schools)
d['school_focus'].update(version=32,checked=CHECKED,conclusion='28 школьных досье. Для CHE/ESP/FRA сохранены языковые и возрастные ограничения; региональные результаты не превращены в мировое лидерство.')
d['school_focus']['routes'].append(dict(name='Европа · реальные младшие результаты и двуязычный вход',ids=['S026','S027','S028','S023','S024','S025'],detail='Lar:Elementary podium2026 по сообщению школы, organizerteamnames отдельно. Highlands:местное первое место FI в 2024 по организатору. Bordeaux:FR/ENPrimary и партнёр по кодингу, выигравшая league team не установлена. Basel остаётся кандидатом школы на английском; старшие результаты не доказывают силу младшего наставника.'))
d['school_focus']['gaps'][0]='28 школьных досье; полный мировой и национальный школьный аудит не завершён.'

f=d['europe_focus'];f.update(version=32,checked=CHECKED,status='partial',
    conclusion='Из этих трёх стран первым проверял бы Испанию для регулярного семейного соревновательного пути. Швейцарию — после проверки английской младшей команды и полной сметы; известный пансион сам по себе не даёт ежедневную инженерную подготовку. Франция подходит для конкретных младших проектов и двуязычной школы, но текущие технические EN / ES группы нужно подтвердить.',
    limitations='Редакционная рекомендация по вашим возрастам / языкам и прочитанным программам, не мировой рейтинг. Исследование трёх стран частичное: все муниципальные клубы, foreign quotas, school admission, новые местные даты и протоколы 5–10 лет ещё не собраны.')
fc={c['iso']:c for c in f['countries']}
fc['CHE'].update(camp='La Garenne 2027: пансион / day, Robotics 8–12 как короткая допопция; Матвею возможно, Оскару рано. WROfamily24 октября 2026Winterthur:оба только после подтверждения минимального возраста / EN. EPFLrobotics11–13 пока не подходит обоим.',
    city_route='Пробный путь: Basel при выборе школы на английском / Juniormentor; Winterthur для семейная мастерская и Technorama. Villars — краткий лагерный опыт, не доказанная соревновательная база.',
    budget='La Garenne: от CHF 7 200 пансион или CHF 6 550 дневной формат / 2 недели +CHF 500Robotics +страховка nonSwissCHF 10/день. Технические часы уточнить; это не две недели ежедневной Robotics.',
    results_check='ISBasel:проверять текущего наставника младших отдельно от наград Grade11. Получить teamcode, точный протокол и реальный вклад ребёнка.',
    risk=fc['CHE']['risk']+' Yverdon29 ноября назван субботой, хотя это воскресенье: не подтверждённый ICS. EN тексты Technorama не означают английский мастер-класс.')
fc['CHE']['event_ids'].extend(['L249','L252','L255','L256','L257','E143']);
fc['ESP'].update(camp='Camp Tecnológico имеет отдельные Junior6–9 собязательным чтением для 6 лет и Genius9–12, плюс regular2026/27. Tech&Play7–16 пансион / английская языковая иммерсия — будущий набор, технический EN-only не установлен. NATUK6–16ENRobotics остаётся кандидатом для обоих.',
    school='К прежним Brains / StPETER’S добавлены HighlandsSevilla и ColegioLarVigo. Lar сообщает 1–3 места Elementary в Vigo2026; Highlands имеет первое место местного Future Innovators 2024, подтверждённое организатором. Ни один результат не назван общим мировым титулом школы.',
    city_route='Пробный соревновательный маршрут: искать Elementarycoach по конкретным результатам в Vigo / Madrid / Sevilla. Bilbao / Basauri / Vitoria имеют регулярного оператора, но язык группы проверить. Город выбирается после наставника и совместимых групп 6/9.',
    budget='WRO общий EUR 60 неполная годовая смета. Camp Tecnológico1 час/неделя — дополнение; нужна отдельная регулярная работа команды. Новый Tech&Play2027 тариф пока не опубликован.',
    results_check='Spain2026 официально публикуетместные / национальные победители и мировые квоты Elementary: 2 RoboMission и 1 FI. Название winningteam ещё нужно связать с фактической школой / клубом / нынешним наставником.',
    risk=fc['ESP']['risk']+' RoboMissionStart 8–12 и Rookie 11–15 имеют упрощённые local/national правила, но не заявлен мировой слот этих названий. Training неофициальная практика. AdvancedFactories studentpass недляначальнойшколы.')
fc['ESP']['event_ids'].extend(['C930','C931','L258','L259','L260','L261','E145']);fc['ESP']['school_ids'].extend(['S026','S027'])
fc['FRA'].update(osc='ABI5–8 и Cité Photon 6–9 дают младший технический формат. RoboCupDiscovery допускает младших по классу, но без общего рейтинга / мирового отбора. Для 6 лет не обещаны CE2AIcamp или пансион 11+.',
    camp='Cité:23/30 октября 2026stage9–11 дляМатвея; Photon6–9 сродителемдляОскара. Magic Makers AI по CE2–CM2 и MinecraftCE2+ — EN/ES неустановлены, год дат подтвердить. ABI HauntedFR/EN дляобоих остаётся наиболее ясно описанным ближайшим двуязычным набором.',
    school='ABI / Ermitage и новый BordeauxInternationalSchool: FR/ENPrimary. Bordeaux имеет партнёр по кодингу по классу; постоянная выигравшая roboticteam не найдена. Нужен отдельный mentor / leaguepath.',
    city_route='Paris — короткая проба ABI и семейных Citéworkshops. Bordeaux — проба двуязычной Primary / партнёр по кодингу и выяснение местный маршрут RoboCup. Переезд оправдан только после проверки адаптации без FR и действующей команды.',
    budget='Мастерская CitéEUR 45, familyworkshopEUR 15 накаждого, включая сопровождающего. Magic Makers AI варианты EUR 215–265; это отдельные занятия, не tuition / pan сион. Годовой тариф школы не установлен.',
    results_check='Отличие Discovery не рейтинговая медаль. Entry 10–13 неравна worldStandard; публикация правила 2025 неподтверждает season2027. Для школ нужны именно organizerprotocols последнего наставника.',
    risk=fc['FRA']['risk']+' Robotsmuseum публикует 11+аудиторию; вход 6/9 сродителемнеустановлен. MagicMakers название Primary неозначаетприёмлюбого 6 летнего.')
fc['FRA']['event_ids'].extend(['C928','C929','L262','L264','L265','L266','L267','L268','L269','L270','E144']);fc['FRA']['profile_ids'].append('robocup-france-junior');fc['FRA']['school_ids'].append('S028')
f['steps'].append(dict(title='Пробный триместр · школа и команда проверяются отдельно',detail='Попроситьтри последних сезона одной команды: код, категория, местный / национальный / мировой этап, точная награда, протокол организатора и часы тренера. Отдельно проверить группу Оскара 6 лет и сложность Матвею после трёх лет опыта. Бренд школы / IB / пансионнеподменяютдействующего mentor и инженерныйвклад детей.'))
for title,url in [('La Garenne 2027windows / fees',lg),('La GarenneRobotics 8–12',lgrobot),('Swissfamilyworkshops',swkids),('EPFLrobotics11–13',epfl),('SpainactualStart/Rookie',rm),('Spainnationalresults / quotas','https://www.wroboto.es/torneos/'),('FranceDiscovery / Entry',rcj),('Citéactualjuniorworkshops',cite),('TechPlay2026 / английская языковая иммерсия',unicaja),('AdvancedFactoriesprofessional/studentgate',faq),('TechnoramaENmaterials / DEshows',tech),('LarElementary2026 сообщению школы',larresult),('BordeauxPrimary',bis)]:
    if url not in {s['url'] for s in f['sources']}:f['sources'].append(dict(title=title,url=url,checked=CHECKED))

d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
issues=[dict(name=name,status=detail,official_alternative=url) for name,detail,url in [
    ('La Garenne: общий лагерь и Robotics','Общий лагерь с 5 лет не допускает Robotics 8+; утренний английский не английский технического занятия;3/2 занятия расходятся.',lgrobot),
    ('SwissWRO Yverdon weekday','29Nov2026 в обеихверсиях Saturday; календарно Sunday. Подтверждённая дата не экспортирована.',swkids),
    ('EPFL младший возраст / места','Robotics11–13;October2026 и waitlist полные;2027registration ожидаетсяв March безточногодня.',epfl),
    ('MagicMakers year / language','Деньмесяцбезгода;26/27 контекстпомеченкакинференция;EN неподтверждён;available=true небронь.',mai),
    ('RoboCupFranceDiscovery grades','Overviewmaternelle/CP–CE2vsbodyCycle1–3vsOpen2026age5–10;eventrule уточнить;нет worldroute.',rcj),
    ('WROSpainStarternames / quotas','Start 8–12,Rookie 11–15 не RoboBasic с 6 лет;Training — неофициальная практика;quota2026 не quota2027.',rm),
    ('AdvancedFactoriesstudent','Studentroutegraduates/masters, finalday13:30approval;не child6/9;roster2027 будетзаоколо 1 месяц.',faq),
    ('Wrong / unavailable candidates','Complubotfetchtimeout;guessCité/Technorama404;bisfrance.com оказался businesssite. Неиспользованокак schoolevidence. Реальный schooldomainbordeaux-school.com прочитан.',bis)]]
a=d['completeness_audit'];a['validation_previous']=a['validation'];a.update(version=32,checked=CHECKED,status='partial',
    scope='Второй углублённый проход Швейцарии / Испании / Франции: младшие gates, реальные программы, школы и посещение.',
    conclusion='29 новых карточек, один профиль младшего маршрута и три школы. Проверены возрастные ступени, технические опции лагерей, роль языка, школьные классы и уровень результатов. Мировой аудит остаётся незавершённым.',
    new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=['L002'],updated_profile_ids=['wro-spain'],new_school_ids=[s['id'] for s in schools],
    validation=dict(version=32,status='pending',publication='pending'))
a['source_issues'].extend(issues)
a['known_backlog'].append(dict(kind='Европа · повторный проход',name='Все местные команды и 5–10 лет школьных результатов',reason='CHE/ESP/FRA stillpartial:национальные квоты для иностранцев,учебныеязыкикаждой sede,new2027cohorts,municipalclubs и organizerschoolresultprotocols всех 5–10 летнеполучены.',url='https://www.wroboto.es/torneos/'))
for row in a['continents']:
    if row['name']=='Европа':row['remaining']='CHE/ESP/FRA углублены повторно. Не закрыты все местные лиги, новые qualifiers2027, преподавание на английском / испанском, иностранные квоты, текущие juniormentors и полные школьные протоколы 5–10 лет.'
c=d['camp_focus'];c['validation_previous']=c['validation'];c.update(version=32,checked=CHECKED,added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=['L002'],carried_forward_ids=c['added_ids'],validation=dict(version=32,status='pending'))
c['routes'].extend([
    dict(name='Швейцария · модуль 8+ и семейная мастерская',ids=['L249','L250','L251','L252','L253','L254','L255','L256','L257','E143'],detail='La Garenne 2027 имеетшесть опубликованных окон смен и короткую опцию Robotics 8–12:Матвеюусловно,Оскарурановлето 2027. WROfamilyWinterthur24 октября 2026:младший age/EN уточнить. Yverdonweekdayconflict не ICS. EPFL11–13 позже. TechnoramaENsignage,DEshows.'),
    dict(name='Испания · разные группы для обоих',ids=['L258','L259','L260','L261','C930','C931'],detail='Junior6–9 требуетчтениев 6 лет;Genius9–12 дляМатвея. RegularCamp Tecnológico1 час/неделя,не campwindow. TechPlay7–16 английская языковая иммерсия:новыйсезон/полныйанглийский технического занятияуточнить. Start 8–12 автономный,не RoboBasic с 6 лет;Training — неофициальная практика.'),
    dict(name='Франция · младший проект и возрастной AI',ids=['L262','L263','L264','L265','L266','L267','L268','L269','L270','C928','C929'],detail='Cité Photon 6–9 сродителем;23/30 октября stage9–11. Magic Makers AI требует CE2–CM2;год дат и английский язык не подтверждены. Discovery младшийбезобщего ranking;OnStageEntry 10–13 будущее. ABI Haunted остаётсядатированным FR/EN вариантомдляобоих.')])
c['source_issues'].extend(issues);c['gaps'].append('Повторный CHE/ESP/FRA: собственные занятия детей 3 года не делают вводный courseadvanced. TechnicalEN, новый foreignslot, exactgrade и адекватнуюсложностьподтвердить увыбранной группы.')
known={s['url'] for s in d['sources']}
for obj in new+[byid['L002']]:
    for url,title in [(obj['source'],obj['title'])]+[(r['url'],r['label']) for r in obj['references']]:
        if url not in known:d['sources'].append(dict(url=url,title=title,checked=CHECKED,evidence='Первичный источник прочитан; ограничения и выводы отмечены.'));known.add(url)
for s in schools:
    for r in s['sources']:
        if r['url'] not in known:d['sources'].append(dict(url=r['url'],title=r['title'],checked=CHECKED,evidence=r['claim']));known.add(r['url'])
assert len(new)==29 and len(profiles)==1 and len(schools)==3
def polish_family_text(data):
    """Keep the family-facing conclusion readable, independently of source notation."""
    c={x['iso']:x for x in data['europe_focus']['countries']}
    c['ESP'].update(
        camp='Camp Tecnológico: Junior 6–9, с обязательным чтением для шестилетних, и Genius 9–12. Есть регулярный курс 2026/27. Tech&Play 7–16 с проживанием и английской иммерсией — кандидат следующего летнего набора; язык каждого технического урока уточняется. NATUK предлагает Robotics на английском для 6–16.',
        city_route='Для пробного периода искать наставника Elementary в Vigo, Madrid или Sevilla по результатам его команды. Bilbao, Basauri и Vitoria имеют регулярные занятия оператора, но язык группы нужно проверить. Город выбирать после знакомства с тренером и группами для обоих детей.',
        budget='Взнос WRO EUR 60 не покрывает год подготовки, оборудование и поездки. Один час Camp Tecnológico в неделю — дополнение к работе команды. Цена Tech&Play 2027 пока не опубликована.',
        results_check='WRO Spain публикует местных и национальных победителей. В 2026 для мирового финала указаны две квоты RoboMission Elementary и одна Future Innovators Elementary. Это квоты сезона, а не подтверждение допуска вашей семьи. Нужно установить школу или клуб команды и нынешнего наставника.',
        risk='Независимая команда не гарантирует испанскую мировую квоту. FLL K8 требует 4–10 детей и два робота. RoboMission Start 8–12 и Rookie 11–15 — упрощённые ступени; мировой слот этих категорий не заявлен. Training — практика вне официального турнира. Студенческая схема Advanced Factories не предназначена для начальной школы.')
    c['CHE'].update(
        camp='La Garenne 2027: пансион или дневные смены; Robotics 8–12 — короткая дополнительная опция. Матвей подходит по возрастной ступени, Оскару летом 2027 ещё рано. WRO Winterthur 24 октября 2026 предлагает семейную мастерскую; минимум возраста и английский нужно подтвердить. EPFL Robotics 11–13 пока не подходит обоим.',
        city_route='Basel — проба школы на английском и наставника младшей робототехники. Winterthur — семейная мастерская и Technorama. Villars — краткий лагерный опыт; постоянная сильная соревновательная команда там не установлена.',
        budget='La Garenne: пансион от CHF 7 200 или дневная программа от CHF 6 550 за две недели, плюс CHF 500 за Robotics. Для нерезидентов Швейцарии форма указывает страховку CHF 10 в день. Число технических занятий уточняется; это не две недели ежедневной робототехники.',
        results_check='У International School Basel нужно проверить текущего младшего наставника отдельно от наград старшей команды Grade 11. Запросить код команды, протокол организатора, часы работы и самостоятельный вклад детей.',
        risk='Starter не заявлен как категория мирового финала. Иностранный допуск, местные даты FLL и язык ряда лагерей ещё уточняются. Студенческие билеты Swiss Robotics Day относятся к университетским ступеням. Yverdon 29 ноября назван субботой, хотя это воскресенье: дата не включена в подтверждённый календарь. Английские тексты Technorama не означают мастер-классы на английском.')
    c['FRA'].update(
        osc='ABI предлагает группу 5–8; Cité Photon — семейную мастерскую 6–9. RoboCup Discovery допускает младших по школьной ступени, но не имеет общего рейтинга и мирового отбора. CE2 в AI-лагере не означает приём любого шестилетнего ребёнка.',
        camp='Cité: 23 и 30 октября 2026 — мастерская 9–11 для Матвея; Photon 6–9 с родителем — кандидат для Оскара, конкретные даты уточняются. Magic Makers AI требует CE2–CM2, Minecraft — опытного CE2 или CM1–CM2. Язык EN/ES и год дат нужно подтвердить. ABI Haunted остаётся ближайшей ясно описанной двуязычной сменой для обоих.',
        school='ABI, Ermitage и Bordeaux International School имеют двуязычные младшие программы. У Bordeaux есть партнёр по кодингу с группами по классам; действующая команда с робототехническими победами не установлена. Пансион Ermitage 11+ пока не подходит обоим.',
        city_route='Paris — короткая проба ABI и семейных мастерских Cité. Bordeaux — проба двуязычной начальной школы, кодинга и местного маршрута RoboCup. Переезд рассматривать после проверки адаптации детей без французского и работы действующего наставника.',
        budget='Мастерская Cité стоит EUR 45; семейное занятие — EUR 15 за каждого, включая сопровождающего. Варианты Magic Makers AI стоят EUR 215–265. Это цены отдельных занятий, а не стоимость школы или пансиона; годовые школьные тарифы ещё нужны.',
        results_check='Отличие Discovery — признание проекта, а не рейтинговая медаль. Entry 10–13 отличается от мирового Standard; правила Entry 2025 не подтверждают сезон 2027. Для выбора школы нужны протоколы последних команд и сведения о нынешнем наставнике.',
        risk='Французские материалы не доказывают судейство на английском. В Coupe Junior сохраняется расхождение минимума 7 / 8 лет. Tinker предлагает окна принимающим центрам, открытая семейная смена не подтверждена. Музей Robots публикует аудиторию 11+; сопровождаемый вход 6/9 нужно уточнить.')
    data['europe_focus']['steps'][-1]['detail']='Запросить три последних сезона одной команды: код, категорию, этап, точную награду, протокол организатора и часы наставника. Отдельно проверить группу Оскара 6 лет и сложность для Матвея после трёх лет опыта. Бренд школы, IB и пансион не заменяют тренера и самостоятельную инженерную работу детей.'
    data['camp_focus']['routes'][-3]['detail']='La Garenne публикует шесть окон смен 2027; короткая опция Robotics 8–12 подходит Матвею по возрастной ступени, Оскару ещё рано. В Winterthur 24 октября 2026 есть семейная мастерская: младший возраст и английский уточняются. Дата Yverdon противоречива. EPFL 11–13 — будущая ступень. В Technorama английские тексты, стандартные шоу на немецком.'
    data['camp_focus']['routes'][-2]['detail']='Junior 6–9 требует умения читать в 6 лет; Genius 9–12 — кандидат Матвею. Регулярный Camp Tecnológico занимает один час в неделю. Tech&Play 7–16 предлагает английскую иммерсию, но новый набор и технический язык ещё нужны. Start 8–12 — автономная ступень; RoboBasic начинается с 6. Training не официальная категория.'
    data['camp_focus']['routes'][-1]['detail']='Photon 6–9 проходит с родителем; мастерские 23 и 30 октября рассчитаны на 9–11. Magic Makers AI требует CE2–CM2; год опубликованных дат и английский язык уточняются. Discovery — младшая проектная ступень без общего рейтинга; OnStage Entry 10–13 — будущий маршрут. ABI Haunted — датированный двуязычный вариант для обоих.'
    replacements={'pan сион':'пансион','sobe':'sobe','robotgroup':'группа робототехники','teamcode':'код команды','foreign admission':'приём иностранцев','Juniormentor':'наставник младших','Elementarycoach':'наставник Elementary','current':'текущий','worldStandard':'мировой Standard','season2027':'сезон 2027','robotkits':'робототехнические наборы','lab hours':'часы лаборатории','School ownership':'Принадлежность к школе','Junior name':'имя Junior','campwindow':'окно лагеря','available=true':'available=true','неустановлен':'не установлен','дляМатвея':'для Матвея','дляОскара':'для Оскара','дляОскара':'для Оскара','сродителем':'с родителем','дляобоих':'для обоих','накаждого':'на каждого','всемировые':'все мировые'}
    def clean(v):
        if isinstance(v,str) and '://' not in v:
            for a,b in replacements.items():v=v.replace(a,b)
            return v
        if isinstance(v,list):return [clean(x) for x in v]
        if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
        return v
    added=set(data['completeness_audit']['new_ids'])
    data['events']=[clean(e) if e['id'] in added else e for e in data['events']]
    data['schools']=[clean(s) if s['id'] in ['S026','S027','S028'] else s for s in data['schools']]
polish_family_text(d)
d['expansion_log'].append(dict(version=32,checked=CHECKED,added=29,updated_ids=['L002'],new_profiles=1,new_schools=3,note='Second CHE/ESP/FRA audit; junior / grade / language / professional gates; world incomplete.'))
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v32.json')
r.setdefault('research_passes',[]).append(dict(version=32,checked=CHECKED,scope='CHE / ESP / FRA: second deeper primary-source pass',added_records=29,new_profiles=1,new_schools=3,status='partial',remaining='Все localoperators,new2027dates,foreignquota,английский технического занятия/ES,schoolprotocols5–10 лет; мировая цель active.'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=32,status='local_checks_pending_publication_pending');rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=32,added=29,profiles=1,schools=3,world_complete=False)))
