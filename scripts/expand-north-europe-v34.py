"""Bounded first-party DE/NL/BE expansion; retain all earlier country passes."""
import ast, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/catalog.json'; d=json.loads(path.read_text())
assert len(d['events'])==1346 and d['completeness_audit']['version']==32
CHECKED='2026-10-01'; new=[]; profiles=[]; byid={e['id']:e for e in d['events']}
for node in ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text()).body:
    if isinstance(node,ast.FunctionDef) and node.name in ['ref','event','profile']:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base_event=event
def add(*args,**kwargs):
    e=base_event(*args,**kwargs); e['region']='Европа'; return e
COND='Условно: возрастная ступень подходит; команду, технический язык и иностранный допуск подтвердить'
YOUNG='Нет: младше минимального возраста этой категории'
de_season='https://www.worldrobotolympiad.de/saison-2027/'
de_join='https://www.worldrobotolympiad.de/mitmachen/als-teilnehmer-im-alter-von-8-bis-19-jahren'
de_starter='https://www.worldrobotolympiad.de/world-robot-olympiad/starter-programm'
de_sumo='https://www.worldrobotolympiad.de/world-robot-olympiad/starter-sumo'
de_rm='https://www.worldrobotolympiad.de/world-robot-olympiad/robomission'
for id,name,url,age,gear,reward in [
    ('C932','Starter / Mission',de_starter,'8–19; 1–3 участника и взрослый coach','Свободный выбор робота / языка; новое поле Starter / Mission в 2027.','Оценка уровня по баллам; без рейтинга и без квалификации на German Final.'),
    ('C933','Starter / Sumo',de_sumo,'8–19; 1–3 участника и взрослый coach','В пилоте 2026 MATRIX; требования к оборудованию 2027 подтвердить.','Региональный турнир; без квалификации на German Final.'),
    ('C934','RoboMission Elementary',de_rm,'8–12; команда 2–3 и взрослый coach','Разрешены разные роботосистемы при ограничениях регламента; новый обязательный набор игровых деталей 2027.','Место в региональном протоколе; дальнейший отбор по национальным правилам, иностранная мировая квота не подтверждена.')]:
    e=add(id,'WRO Germany 2027 · '+name,'Германия','Региональные площадки; точные города / дни нового сезона уточнить',url,age,COND,YOUNG,
        'Школьная, клубная или частная команда. Регистрация с 9 ноября 2026 до 19 марта 2027; приём иностранной семейной команды и квоту уточнить.',gear,
        deadline='2027-03-19',scope='national',cost='Starter EUR 85 / команда по текущей категории; взнос RoboMission 2027 и материалы отдельно.' if id!='C934' else 'Взнос сезона 2027, робот, новое игровое поле и поездка отдельно; полную смету уточнить.',
        note='Региональные этапы ожидаются с конца апреля до начала июня 2027; список обещан к концу октября 2026. Это не точные даты этапов. Возраст считают по году рождения; старая таблица 2025 на общей странице не стала таблицей 2027. EN-судейство не подтверждено.')
    e.update(reward=reward,period='Регистрация 09.11.2026–19.03.2027; региональные дни пока не объявлены.',references=[ref('Календарь / изменения 2027',de_season),ref('Частная команда и возрастные категории',de_join)],deadline_label='Закрытие регистрации команды',deadline_note='Дедлайн регистрации сезона; точные дни регионального участия ещё уточняются.')
    if id!='C934':e['format']='1–3 участника + взрослый наставник; только региональная Starter ступень'

dach='https://www.first-lego-league.org/en/2026-27-season/bioglow'
explore='https://www.first-lego-league.org/en/divisions/explore'
challenge='https://www.first-lego-league.org/en/divisions/challenge'
future5='https://www.first-lego-league.org/en/divisions/future-edition-5'
future8='https://www.first-lego-league.org/en/divisions/future-edition-8'
e=add('C935','FIRST LEGO League DACH 2026/27 · общий финал','Германия','Paderborn · Heinz Nixdorf MuseumsForum',dach,
    'Challenge 9–16 / Future 8+ 8–16 и Grades4–10; командный отбор',COND,'Нет: финал Challenge / Future8+; Explore и Future5+ сюда не перенесены',
    'Сначала региональная квалификация в Германии / Австрии / Швейцарии. Открытая запись прямо на финал и иностранная квота не подтверждены.',
    'Challenge: прежняя LEGO платформа; Future8+: Computer Science & AI. Регламенты различаются.',start='2027-04-09',end='2027-04-10',scope='regional',
    note='Финал DACH — региональный этап трёх стран, а не мировой FIRST Championship. Проверить дисциплину, квоту, язык защиты и текущего coach; наличие даты не подтверждает приглашение семьи.')
e.update(admission_kind='qualification',references=[ref('Challenge: отдельные правила',challenge),ref('Future8+: отдельные правила',future8)])
for id,name,url,age,osc,gear,deadline,cost,reward in [
    ('C936','Explore',explore,'6–10; 2–6 детей + взрослый наставник',COND,'LEGO Education; модель и poster по сезону.','','EUR 199 программа + EUR 20 доставка в Германии; робот / festival extras отдельно.','Фестивальное представление, признание и медали участников; общего рейтинга / мирового отбора нет.'),
    ('C937','Challenge',challenge,'9–16; 2–10 детей + взрослый наставник',YOUNG,'Робот и поле Challenge; новую CS&AI платформу Future не смешивать.','2026-10-31','EUR 344 + EUR 20 доставка в Германии; робот, поездка и прочие расходы отдельно.','Региональный конкурс с возможностью отбора на DACH финал; мировой слот по правилам организатора.'),
    ('L277','Future Edition 5+',future5,'5–7 И Grades1–3; группа до24, команды до4','Условно: 6 лет подходит, но нужен класс1–3; класс Оскара неизвестен','CS&AI5+: один набор на команду до4; компьютер / tablet.','2027-03-31','Для группы8: EUR150 + EUR70 сезонные наборы + EUR20 доставка; CS&AI оборудование дополнительно.','Учебные проекты и собственное завершение группы: официальных closing events 2026/27 не предусмотрено.'),
    ('C939','Future Edition 8+',future8,'8–16 И Grades4–10; группа до24, команды до8',YOUNG,'Два CS&AI набора на команду; 8+ требует дополнительное оборудование, 11+ комплект полнее.','2026-10-31','Для группы8: EUR250 + EUR140 сезон + EUR20 доставка + EUR100 при участии в event; CS&AI оборудование дополнительно.','Учебная программа с отдельными optional конкурсными событиями; правила отбора нужно подтвердить.')]:
    mat='Нет для возрастной группы5–7' if id=='L277' else 'Условно: возраст подходит; для Future8+ обязательно Grades4–10, класс Матвея неизвестен' if id=='C939' else COND
    e=add(id,'FIRST LEGO League Germany 2026/27 · '+name,'Германия','Местная школьная / клубная / частная группа; площадку подтвердить',url,age,mat,osc,
        'Сначала группа и взрослый наставник, потом регистрация нужного division. Частные команды прямо разрешены в Explore / Challenge; Future допускает school / community group. Иностранный вход отдельно.',gear,
        block='Лагеря' if id=='L277' else 'Соревнования',deadline=deadline,scope='national',cost=cost,note='Язык немецкого сайта и EN-материалов не доказывает EN-интервью. Возраст, школьный класс, число детей, плата за оборудование и турнирный этап проверяются раздельно.')
    e.update(reward=reward,references=[ref('Сезон и DACH финал',dach)],deadline_label='Регистрация группы / команды',deadline_note='Для выбранного division; место на event и финале не гарантировано.')
    if id=='C937':e['note']+=' Overview сезона описывает Challenge как классы 5–10, отдельная division page — возраст 9–16 и частные команды. Это не разрешено молча в пользу девятилетнего: подтвердить применимость класса у организатора.'
    if id=='C936':e.update(period='Регистрация команды до4 недель перед выбранным региональным фестивалем при наличии мест; конкретный день пока неизвестен.',deadline_note='Explore:4 недели до выбранной выставки. Общий31 октября относится к Challenge / event Future8+, не Explore.')
    if id=='L277':e.update(participation='regular',format='Регулярная учебная группа; официальных событий завершения сезона нет',language_mode='unconfirmed',period='Регистрация открыта 1 октября 2026; до31 марта2027. Официального внешнего финального события сезона нет.',note=e['note']+' Future5+ — учебная ступень; не обещана рейтинговая международная медаль.')
    if id=='C939':e.update(period='До31 октября2026 для event; до31 марта2027 без event.',deadline_note='31 октября для участия в event; для группы без event опубликовано31 марта2027. Grade4–10 — дополнительное условие.')

rcj='https://robocup.de/events/junior-finale-2027'
rescue='https://robocup.de/junior/rescue/'
e=add('C940','RoboCupJunior Germany 2027 · национальный финал','Германия','Nürnberg · Messe Nürnberg',rcj,
    'Квалифицированные немецкие школьные команды; возраст по конкретной лиге',
    'Условно: национальная младшая Entry ступень возможна; возраст, класс и квалификация не подтверждены',
    'Условно только после явного младшего допуска: минимальный возраст Entry не опубликован; 6 лет не гарантированы',
    'Лучшие200 школьных команд через10 немецких региональных qualifiers. Иностранная семейная запись на национальный финал не подтверждена.',
    'Rescue / Soccer / OnStage по текущему регламенту; Entry и мировой Standard различаются.',start='2027-03-09',end='2027-03-12',scope='national',
    note='В2027 German Open однократно не проводят из-за мирового RoboCup в Германии. Этот Junior Finale — отдельный национальный финал. Более старая обзорная страница говорит о9 qualifiers и2026; текущая страница2027 говорит10. Национальная Entry не даёт мировую квалификацию.')
e.update(admission_kind='qualification',references=[ref('Rescue: LineEntry до14 / MazeEntry до16; без world qualification',rescue)])

nl_wro='https://wro-nederland.nl/Seizoen'
nl_team='https://wro-nederland.nl/Meedoen/Team'
for id,name,gear in [('C941','RoboMission','Автономный робот, поле / мат и набор игровых моделей; для nonLEGO дополнительные prototype rules.'),('C942','Future Innovators','Свой проект на любой совместимой платформе, booth / презентация и документация.')]:
    e=add(id,'WRO Netherlands · '+name+' Elementary · следующий сезон','Нидерланды','Новый календарь после2026 ещё уточняется',nl_team,
        '8–12 по опубликованной категории; 2–3 участника + coach',COND,YOUNG,
        'Организовать2–3 ребёнка и наставника. Новый набор, EN-защита, приём visiting family и национальная квота требуют подтверждения.',gear,
        scope='national',evidence='historical_program',cost='Опубликовано EUR110 / команда; формулировка о бесплатном FI project не доказывает нулевой итоговый взнос. Робот / мат / поездка отдельно.',
        note='Календарь первичного сайта относится к маю / июню2026 и уже завершён. Elementary RM был в Almelo / Delft; FI в Delft. Новый календарь2027 не придуман. Таблица годов рождения2026 не перенесена в2027. Максимум2 команды организации в возрастной группе без согласования дополнительных мест.')
    e.update(references=[ref('Реальный календарь / national categories2026',nl_wro)],format='Команда2–3 + взрослый наставник')

nl_season='https://firstlegoleague.nl/seizoen_2026_2027/'
nl_ch='https://firstlegoleague.nl/dit-seizoen/challenge/'
nl_ex='https://firstlegoleague.nl/dit-seizoen/explore/'
nl_future='https://firstlegoleague.nl/dit-seizoen/future-8-t-m-14-jaar/'
e=add('C943','FIRST LEGO League Netherlands 2026/27 · Explore','Нидерланды','Местная группа / фестиваль; точные даты уточнить',nl_ex,
    '6–10; точный размер местной команды подтвердить',COND,COND,
    'Команда и взрослый наставник, регистрация через местного партнёра. Фестиваль по выбранному региону, EN и иностранный вход отдельно.',
    'LEGO Education, модель / poster; робот оплачивается дополнительно.',scope='national',cost='EUR70 за один сезонный набор; робот и возможная местная festival fee отдельно.',
    note='Это младшая фестивальная программа без общего рейтинга; награда участия не мировой титул. Календарь региональных Challenge финалов не перенесён автоматически на Explore.')
e.update(reward='Представление проекта и признание участника, без общего рейтинга.',references=[ref('Национальный календарь: другие divisions отдельно',nl_season)])
e=add('C944','FIRST LEGO League Netherlands 2026/27 · Future Edition','Нидерланды','Местная группа; национальное событие ожидается в апреле / мае2027',nl_future,
    '8–14 в текущем нидерландском наборе; 4–8 детей и coach18+',COND,YOUNG,
    'Группа4–8, максимум2 взрослых coaches. Подтвердить местную регистрацию, язык интервью и доступ иностранцев.',
    'Два CS&AI11+ набора; маркировка оборудования11+ не повышает опубликованный возраст участников8–14.',scope='national',
    cost='EUR200 регистрация + EUR195 сезонный набор; два CS&AI робота дополнительно.',
    note='Общий международный обзор говорит Future5–14, но текущий национальный division2026/27 —8–14. Оскару6 лет Future здесь не обещан. Национальные даты / место ещё не опубликованы, апрель / май не точные даты ICS. SPIKEPrime для Future не подменяет CS&AI.')
e.update(references=[ref('Сезон: национальный Future event ещё TBD',nl_season)])

nl_dates=[
    ('2026-12-11','Zeeland · Middelburg','Joint Research Center Zeeland, Het Groene Woud1a'),
    ('2027-01-09','Helmond','Hogeschool de Kempel, Deurneseweg11'),
    ('2027-01-16','Leeuwarden','NHL Stenden, Rengerslaan10'),
    ('2027-01-21','Rivierenland · Culemborg','ORS Lek en Linge VMBO, Ina Boudier-Bakkerstraat2'),
    ('2027-01-22','Drachten','CSG Liudger Raai, Leerweg1'),
    ('2027-01-23','Midden-Brabant · Tilburg','Campus013, Stappegoorweg185'),
    ('2027-01-29','Drenthe-Zuid · Emmen','Ullevi1a'),
    ('2027-01-29','Utrecht · Amersfoort','ROC Midden Nederland, Disketteweg10'),
    ('2027-01-30','Limburg · Roermond','Wings Agora, Oranjelaan300'),
    ('2027-02-06','Groningen','Energy Academy, Rijksuniversiteit Groningen, Nijenborgh6'),
    ('2027-02-11','Zwolle','Deltion College'),
    ('2027-02-12','Appingedam','Campus Eemsdelta, Pastorielaan4'),
    ('2027-02-13','Flevoland / ’tGooi','Конкретный город / адрес пока не опубликован'),
    ('2027-02-20','Eindhoven','Fontys ICT, Rachelsmolen1, R10'),
    ('2027-02-20','West-Brabant · Breda','Avans, Hogeschoollaan1'),
    ('2027-03-06','Wageningen · национальный финал','Wageningen University & Research, Orion building103')]
for i,(start,city,venue) in enumerate(nl_dates):
    id='C'+str(945+i);final=i==15
    e=add(id,'FIRST LEGO League Netherlands 2026/27 · Challenge · '+city,'Нидерланды',city+' · '+venue,nl_season,
        '9–15; 2–10 детей; coach18+ (предпочтительно2)',COND,YOUNG,
        'Только квалифицированные команды после регионального этапа; прямой вход не подтверждён.' if final else 'Выбрать регионального партнёра и зарегистрировать команду; приём visiting family и EN-интервью подтвердить.',
        'SPIKEPrime / EV3 / NXT по текущему Challenge; CS&AI Future сюда не перенесён.',start=start,scope='national' if final else 'local',
        cost='EUR200 регистрация + EUR195 сезонный набор по national Challenge; робот, взнос конкретного этапа и поездка отдельно.',
        note='Официально опубликованный день сезона2026/27; календарь организатор помечает subject to change. Дата не подтверждает место команды / билет зрителя. Здесь Challenge9–15; младший Explore проходит по отдельной программе. Зарубежное участие не доказывает право на нидерландскую международную квоту.')
    e.update(admission_kind='qualification' if final else 'open_application',references=[ref('Возраст / команда / оборудование / fees',nl_ch)])

be_timing='https://www.voka.be/first-lego-league-be/timing'
e=add('C961','FIRST LEGO League Belgium 2026/27 · Explore','Бельгия','Местный фестиваль; точный день / площадка уточнить',be_timing,
    '6–10 по странице национального партнёра',COND,COND,
    'Сначала местная группа и партнёр Explore. Отдельно проверить дату, возрастной cutoff, EN-язык и иностранный вход.',
    'LEGO модель / poster; точный набор выбранного фестиваля подтвердить.',scope='national',
    note='Страница сезона2026/27 содержит возрастную ссылку на1 января2026 — новый cutoff нужно уточнить. Региональные contest days Challenge не выданы за фестивальные дни Explore. Explore не обещает международную рейтинговую победу.')
e.update(reward='Образовательное представление и признание участия; мировой рейтинг не установлен.')
be_dates=[('2026-11-27','Leuven'),('2027-01-16','Wallonia · город уточнить'),('2027-01-29','Kortrijk'),('2027-02-05','Gent'),('2027-02-18','Antwerpen'),('2027-02-19','Brussels · NL'),('2027-02-25','Limburg · день1'),('2027-02-26','Limburg · день2'),('2027-03-13','BeLux Championship · место уточнить')]
for i,(start,city) in enumerate(be_dates):
    id='C'+str(962+i);final=i==8
    e=add(id,'FIRST LEGO League Belgium 2026/27 · Challenge · '+city,'Бельгия',city,be_timing,
        '9–15; опубликованный cutoff1 января2026 требует уточнения для сезона2026/27',
        'Условно: возраст9 подходит сейчас, но1 января2026 ребёнку2017 было8–9; действующий cutoff / день рождения подтвердить',YOUNG,
        'Национальный BeLux финал после регионального отбора; прямой иностранный вход не подтверждён.' if final else 'Зарегистрировать команду через местного партнёра. Дата / регион опубликованы; возрастной cutoff, EN и иностранный приём подтвердить.',
        'LEGO Challenge; Future — отдельный division.',start=start,scope='regional' if final else 'local',
        note='Точный конкурсный день опубликован Voka. В Wallonia, Limburg и BeLux адрес / принимающая площадка в таблице не установлены. Английская версия сайта не доказывает EN-защиту; Brussels NL — отдельная языковая отметка региона. Участие не подтверждает право на национальную международную квоту.')
    e.update(admission_kind='qualification' if final else 'open_application')
e=add('C971','WRO Germany 2027 · национальный финал · предварительно','Германия','München · Messe München, Halle 6C · предварительно',de_season,
    'Квалифицированные RoboMission / Future Innovators; Elementary8–12',COND,YOUNG,
    'Региональная квалификация. Организатор ещё ищет финансирование финала; конкретное приглашение семьи и foreign quota не подтверждены.',
    'Платформа по категории2027; Starter сюда не квалифицируется.',scope='national',
    note='Предварительно24–25 июня2027; финансирование ещё не закрыто. Start / end оставлены пустыми, чтобы предварительная дата не стала подтверждённой в календаре. Это German Final, не WRO World Final.')
e.update(period='Планируют24–25 июня2027, München · Halle 6C; организатор прямо помечает предварительным.',date_status='Уточнить',admission_kind='qualification',related_ids=['C934'])

# Real sessions / programmes; next-year dates and English teaching are separate gates.
nt='https://newtechkids.com/en/'
for id,slot in [('L271','ранняя сессия'),('L272','поздняя сессия')]:
    e=add(id,'NewTechKids · Try It Out · '+slot,'Нидерланды','Amsterdam · Public Library near Centraal Station',nt,
        '8–12',COND,YOUNG,'Выбрать раннюю или позднюю сессию4 ноября; время, места и возможность следовать только EN уточнить.',
        'LEGO robot; работа в парах, вводная проверка подхода оператора.',block='Лагеря',start='2026-11-04',participation='holiday_workshop',
        language='Инструктор сочетает Dutch и English; полный отдельный EN поток не обещан.',languages=('EN','NL'),
        note='Главная страница прямо публикует раннюю и позднюю сессию4 ноября2026 и возраст8–12. Подробные booking shortlinks недоступны при чтении; точные часы и fee не придуманы. Для трёхлетнего опыта проверить сложность вводного занятия.')
    e.update(language_mode='bilingual',period=slot+'; точные часы уточнить')
for id in ['L132','L133','L134']:
    old=byid[id];old.update(language='Инструктор сочетает Dutch и English; участие без знания Dutch и полный EN поток подтвердить.',languages=['EN','NL'],language_mode='bilingual',checked=CHECKED,
        proof='Повторно прочитана текущая главная страница: возраст8–12, фактическое сочетание Dutch и English. Это двуязычное преподавание, не гарантированный отдельный EN поток.')
garna='https://garnaschool.com/en/summer-camp-en/'
e=add('L273','Garna School · English + Robotics · будущая летняя смена','Германия','Plötzky Adventure Park',garna,
    '7–17 по проведённой программе2026',COND,'Будущий кандидат с7 лет; день рождения и cutoff следующего сезона подтвердить',
    'Новый сезон2027 ещё не опубликован. Подтвердить иностранный приём, возраст на смену, уровень LEGO, проживание и новый тариф.',
    'LEGO Education SPIKE; Arduino указан только для12–17.',block='Лагеря',participation='day_camp',scope='international',evidence='historical_program',
    language='English: прямо заявлены все занятия, включая Robotics.',languages=('EN',),cost='Архив2026: от EUR580 за7 дней /6 ночей; тариф2027 и транспорт отдельно.',
    note='5–11 и12–18 июля2026 завершились. 15 уроков English по45 минут и Robotics5 раз в неделю; четыре места в домике, питание и snacks. Учебный сертификат не турнирная медаль. Новый набор не имеет вымышленных дат; для опытного Матвея проверить сложность.')
e.update(participation='residential',format='Пансион7 дней /6 ночей по программе2026',language_mode='primary')
tuhh='https://robotik.tuhh.de/robotikkurse-schueler/kursangebot/robotik-camp/junior-robotik-camp'
e=add('L274','TU Hamburg · Junior Robotik-Camp2026','Германия','Hamburg · TUHH',tuhh,
    'Grades4–8; LEGO / MakeCode для4–6, NXC / Python для6–8','Условно: только если соответствует классу4–6; нынешний класс и технический EN подтвердить','Нет для обычной шестилетней ступени: нужен минимум класс4',
    'Выбрать модуль при регистрации; текущий иностранный приём, EN и класс уточнить.',
    'LEGO Mindstorms / RinoLab, micro:bit MakeCode; старшие NXC и Python.',block='Лагеря',start='2026-11-21',end='2026-11-22',participation='day_camp',
    date_scope='session_days',cost='EUR50 за оба дня с питанием; жильё / поездка отдельно. Социальное снижение EUR30 только после согласования.',
    note='Два дневных учебных дня09:00–16:30, пансион не включён. Grade — требование, девятилетие само по себе не доказывает Grade4. EN / ES преподавание не заявлено; прежний отчёт об иностранных участниках2015 не текущий допуск.')
e.update(sessions=[dict(date=date,topic='Выбранный модуль Junior Robotik-Camp',start_time='09:00',end_time='16:30',timezone='Europe/Berlin',time_note='Опубликовано оператором; модуль и место подтвердить.') for date in ['2026-11-21','2026-11-22']])
isd='https://www.isdedu.de/summer-camps'
e=add('L275','ISD Düsseldorf · AI & Robotics Camp · следующий летний набор','Германия','Düsseldorf · ISD Senior School',isd,
    '9–14 по проведённой программе2026',COND,YOUNG,
    'Набор2027 откроют в январе2027; точные день открытия и смены ещё не объявлены. Оператор приглашает ISD и детей других местных школ; зарубежную гостевую семью нужно согласовать.',
    'Интерактивные роботы / smart systems, жесты и visual inputs; конкретную платформу уточнить.',block='Лагеря',participation='day_camp',evidence='historical_program',themes=('robotics','ai','coding'),
    note='Смена10–14 августа2026,09:00–14:00, уже закрыта. Общая программа предлагает practise English; это не прямое подтверждение EN именно AI module. Английский школьного curriculum не перенесён на camp. Осенние4-дневные лагеря2026 опубликованы по иным темам, AI / Robotics среди них не установлен.')
e.update(period='2027registration в январе; даты нового AI / Robotics camp неизвестны.',references=[ref('Школьный EN curriculum, отдельно от camp','https://www.isdedu.de/admissions-faqs')])
code='https://www.wintercircus.be/en/academy/ai-camp-for-kids'
e=add('L276','Wintercircus / CodeFever · AI Escape Room camp · следующий набор','Бельгия','Gent · Wintercircus',code,
    'Grades4–6 (примерно10–13); старшие допускаются','Условно: требуется Grade4–6; класс Матвея неизвестен, обычный ориентир10+','Нет для обычной шестилетней ступени: нужен минимум Grade4',
    'Сначала новая смена, соответствие классу и возможность учиться без Dutch. EN помощь прямо есть, полный EN технический поток не обещан.',
    'AI escape room project; собственная командная работа и демонстрация.',block='Лагеря',participation='day_camp',evidence='historical_program',themes=('ai','coding'),priority='P4 — будущая ступень / язык уточнить',
    language='Основное преподавание Dutch; все supervisors могут общаться на English.',languages=('NL',),
    note='6–10 июля и24–28 августа2026 завершены;2027 не объявлен. Professional teacher примерно1:5, максимум60 детей по описанию. English communication — помощь, не английский основной курс. Сертификат / показ проекта не конкурсная международная медаль.')
e.update(language_mode='support',support_languages=['EN'])

# Professional expo, qualified tournament viewing, and family museum alternatives.
machine='https://www.machineering.eu/nl/bezoeken/bezoekersprofiel/'
e=add('E146','Machineering2027 · robots / industrial technology','Бельгия','Brussels Expo',machine,
    'Professional visitors; students higher education / третий цикл technical secondary со сопровождением',
    'Младший student route9 лет не опубликован; исключение требует подтверждения','Младший student route6 лет не опубликован; исключение требует подтверждения',
    'Взрослый professional visitor pass. Школьный student route не применять к начальным классам; семейное исключение неизвестно.',
    'Промышленная робототехника, автоматизация и manufacturing.',block='События',start='2027-03-24',end='2027-03-26',scope='international',participation='visitor',priority='P3 — взрослое профессиональное посещение',themes=('robotics','ai','technology'),
    note='24 марта10–18,25 марта10–22,26 марта10–16 по организатору. Нет опубликованного универсального under18 ban; есть ограниченный student route. Наличие student admission не гарантирует вход6/9. Список компаний2025 не стал подтверждённым roster2027.')
e.update(exhibition_tier='regional',visitor_policy='confirm_children',visitor_policy_note='Для6/9 семейный вход не подтверждён; published student route старше.',adult_entry='Professional registration; актуальный visitor pass / fee подтвердить.',highlights=['Промышленная робототехника','Automation / manufacturing','Профессиональный networking'],exhibitors=[],exhibitor_note='Все компании мира не представлены; текущий каталог2027 отдельно.',exhibitor_directory_url=machine)
e=add('E147','RoboCupJunior Germany2027 · публичный просмотр','Германия','Nürnberg · Messe Nürnberg / Freizeitmesse',rcj,
    'Публика с10 марта; точный детский билет / ограничения уточнить','Условно: младший зрительский допуск и билет уточнить','Условно: младший зрительский допуск и билет уточнить',
    'Посещение через Freizeitmesse с10 марта; согласовать детские билеты и часы12 марта. Конкурсная команда регистрируется отдельно.',
    'Посмотреть автономных роботов / детские проекты; собственная конкурсная награда зрителю не обещана.',block='События',start='2027-03-10',end='2027-03-12',scope='national',participation='visitor',
    note='9 марта — начало конкурса / setup, не опубликованный день входа публики. Финалы12 марта; финальные часы и доступ к ceremony отдельно. Это школьные команды, а не выставка всех производителей.')
e.update(related_ids=['C940'])
nemo='https://www.nemosciencemuseum.nl/en/to-do'
nemo_faq='https://www.nemosciencemuseum.nl/en/plan-your-visit/frequently-asked-questions'
e=add('E148','NEMO Amsterdam · Technium / Maker Space','Нидерланды','Amsterdam · Oosterdok2',nemo,
    'Для всех возрастов; часть activities6+; до13 только со взрослым','Да по возрастной ступени; со взрослым','Да по возрастной ступени; со взрослым, ограничения отдельных activities',
    'Выбрать временной билет музея; отдельные мастерские, их язык и текущая тема по расписанию.',
    'Механизмы, технологии и практические проекты Maker Space.',block='События',participation='visitor',priority='P3 — семейное посещение при поездке',themes=('technology','coding'),
    cost='EUR21.50 / посетитель4+ по текущему FAQ; семейную итоговую цену и специальные билеты проверить.',
    note='Постоянный научный музей; дата вашей поездки не придумывается. Не торговая выставка всех robotics / AI компаний. EN-страница не доказывает английский мастер-класс. Текущий графикTue–Sun10–17:30, понедельники зависят от сезона / каникул.')
e.update(references=[ref('Возраст, сопровождение, билеты / график',nemo_faq)])
tech='https://www.technopolis.be/en/expositions/on-off/'
e=add('E149','Technopolis Mechelen · ON/OFF · robots / технологии','Бельгия','Mechelen · Technopolis',tech,
    'Рекомендовано8+; более младшие прямо приветствуются','Да по возрастной ступени; семейное посещение','Да: младшие прямо welcome; сложность8+ учитывать',
    'Обычный билет Technopolis включает ON/OFF; выбрать день и текущий режим посещения.',
    'Felix robot, holograms, eye tracking, voice changer и interactive technology.',block='События',participation='visitor',priority='P3 — семейное технологическое посещение',themes=('robotics','technology'),
    language='Информация экспозиции Dutch, English и French; это не язык технического курса.',languages=('NL','EN','FR'),
    note='Постоянная экспозиция с ориентиром8+, младшие допускаются. Отдельное Night@Technopolis18+ не детская ON/OFF поездка. Действующие экспонаты / часы уточнить; это не world competition или ярмарка всех компаний.')
e.update(language_mode='materials',references=[ref('Обычный билет / booking','https://www.technopolis.be/en/tickets-bookings/')])
hnf='https://www.hnf.de/en/permanent-exhibition/exhibition-areas/everything-goes-digital/man-robots-living-with-artificial-intelligence-and-robotics.html'
hnf_visit='https://www.hnf.de/en/visiting/general-information/opening-hours-prices-directions.html'
hnf_peter='https://www.hnf.de/en/permanent-exhibition/exhibition-areas/everything-goes-digital/man-robots-living-with-artificial-intelligence-and-robotics/robot-peter.html'
e=add('E150','Heinz Nixdorf MuseumsForum · robots / AI · постоянная экспозиция','Германия','Paderborn · HNF',hnf,
    'Дети до14 только со взрослым; правила отдельных activities уточнить','Да по музейному возрастному входу, со взрослым','Да по музейному возрастному входу, со взрослым',
    'Посещение постоянной экспозиции; технический мастер-класс требует отдельного расписания и допуска.',
    'История computing, AI и роботы; автономный guide PETER.',block='События',participation='visitor',priority='P3 — музей при поездке',themes=('robotics','ai','technology'),
    language='Для робота-guide PETER опубликованы English / German; это не EN занятия всех сотрудников.',languages=('EN','DE'),cost='Постоянная экспозиция: взрослый EUR10, reduced до18 EUR7, family ticket EUR20; состав family ticket и специальные тарифы уточнить.',
    note='Постоянная музейная экспозиция, даты поездки не заданы. Конкретные работающие роботы не гарантированы каждый день; музей и конкурсный DACH финал на той же площадке — разные посещения.')
e.update(language_mode='materials',references=[ref('PETER: English / German',hnf_peter),ref('Visitor conditions / prices',hnf_visit)],related_ids=['C935'])
gameon='https://www.nemosciencemuseum.nl/en/to-do/exhibition/game-on'
e=add('E151','NEMO Amsterdam · Game On2026','Нидерланды','Amsterdam · NEMO, Theater, Floor2',gameon,
    'Семейная выставка; до13 сопровождение взрослым по музею','Да по семейной возрастной ступени; игры / activities по возрасту','Да по семейной возрастной ступени; игры / activities по возрасту',
    'Билет NEMO с временным входом; выставка с11:00. Язык мастерской и доступ конкретных игр уточнить.',
    'История games, consoles SuperNintendo–PS5; Maker Space: собственный game level.',block='События',start='2026-07-10',end='2026-10-25',participation='visitor',priority='P3 — семейное посещение до25 октября',themes=('games','coding','technology'),
    cost='Музейный билет по текущим условиям; FAQ4+ EUR21.50 / человек, отдельную доплату проверить.',
    note='Текущая visitor page явно10 июля–25 октября2026. Более старый пресс-релиз давал11 июля–26 октября; выбран текущий календарь самой выставки. Это временная музейная экспозиция / мастерская, не хакатон и не мировой конкурс.')
e.update(references=[ref('Возраст и билеты музея',nemo_faq)],date_scope='festival_window',related_ids=['E148'])
gamescom=byid['E034'];gamescom.update(start='2027-08-26',end='2027-08-29',period='Публичные дни26–29 августа2027; неделя23–29 и business day25 августа отдельно.',date_status='Подтверждено',checked=CHECKED,
    proof='Прочитана текущая primary opening-times: public Thursday26–Sunday29 августа2027. Visitors подтверждает4–12 со взрослым,4–6 бесплатно, до4 нельзя.',
    note='Неделя gamescom23–29 августа не равна публичным дням26–29. 25 августа business / media day; ограниченные wildcard visitor tickets после13:00 не обычный семейный вход. USK отдельных игр ограничивает доступ; child pass не доступ к любому контенту.')
gamescom['references']=gamescom.get('references',[])+[ref('Публичные дни2027','https://www.gamescom.global/en/info/opening-times')]

def cat(name,age,team,hardware,age_rule,entry):return dict(name=name,age=age,team=team,hardware=hardware,age_rule=age_rule,entry=entry)
profile('wro-germany','WRO Germany · Starter / Elementary','regional','Starter8–19; RM / FI Elementary8–12',
    'Полноценный соревновательный путь Матвея через Elementary; Starter — отдельная упрощённая региональная ступень без national qualification.',
    [cat('Starter / Mission','8–19','1–3 + adult','Любой допустимый робот','По году рождения;2027field новое','Балльное признание, без общего рейтинга / German Final'),cat('Starter / Sumo','8–19','1–3 + adult','MATRIX в пилоте2026;2027rules отдельно','По году рождения','Только региональный турнир'),cat('RoboMission / Future Innovators Elementary','8–12','2–3 + adult','По2027category rules','По году рождения; таблица2025 устарела','Regional qualifier → German Final → квота по действующим правилам')],
    ['C932','C933','C934','C971'],'Найти взрослого coach и команду → зарегистрировать сезон → regional2027 → German Final только для qualifying category; Starter не квалифицирует.',
    ['Оскару2020 до8 лет ещё рано.','Школьная / клубная / частная команда разрешена; иностранное право на квоту отдельно.','Дети самостоятельно строят и объясняют код; EN-защита неизвестна.'],
    ['Старт регистрации9 ноября2026, закрытие19 марта2027.','Final24–25 июняMunich предварителен из-за финансирования.','Новое поле Starter и Creative Element Set2027; прежние правила не покупать автоматически.'],
    [('Сезон2027',de_season),('Starter',de_starter),('Участник / private team',de_join)],age_tags=('9','10-12','teen'))
profile('fll-germany','FIRST LEGO League DACH · Германия','regional','Explore6–10; Challenge9–16; Future5–7 /8–16 с Grade gates',
    'Оскару доступны младшие учебные проекты, Матвею — Challenge или Future8+ при нужном классе. Признание Explore / Future5+ не мировая рейтинговая победа.',
    [cat('Explore','6–10','2–6 + adult','LEGO / season model','Возраст и местный допуск','Festival recognition без общего рейтинга'),cat('Challenge','9–16','2–10 + adult','Прежняя Challenge platform','Возраст и regional registration','Regional → DACH final; world slot отдельно'),cat('Future5+','5–7 И Grades1–3','Группа≤24; команда≤4','CS&AI5+','Возраст И школьный класс','В2026/27 нет официальных closing events'),cat('Future8+','8–16 И Grades4–10','Группа≤24; команда≤8','Два CS&AI набора','Возраст И школьный класс','Optional events, иной gameplay')],
    ['C935','C936','C937','L277','C939'],'Младший проект Explore / Future5+ → самостоятельный Challenge или Future8+ по классу → региональный отбор → DACH финал9–10 апреля2027.',
    ['Выбрать division до покупки несовместимого оборудования.','Grade4–10 у Future8+ не заменяется достижением8/9 лет.','Explore / Challenge допускают private teams, иностранная квота и EN interview отдельно.'],
    ['Future5+ registration до31 марта2027; event Future8+ / Challenge до31 октября2026.','DACH финал в Paderborn только Challenge / Future8+.','Региональные объявления продолжения Founders не гарантия единой мировой программы после2026/27.'],
    [('Explore',explore),('Challenge',challenge),('Future5+',future5),('Future8+',future8),('DACHcalendar',dach)])
profile('robocup-germany-junior','RoboCupJunior Germany · младшие Entry и финал','regional','LineEntry≤14; MazeEntry≤16; minimum age не установлен; мировой Standard отдельно',
    'Национальные Entry дают учебную автономную робототехнику, но без мировой квалификации. Младший возраст6 лет не подтверждён одной верхней границей.',
    [cat('Rescue LineEntry','До14; minimum не опубликован','Размер команды /2027rules уточнить','Автономный line rescue','Точные2027rules нужны','Не квалифицирует на World'),cat('Rescue MazeEntry','До16; minimum не опубликован','Размер команды /2027rules уточнить','Автономный maze rescue','Точные2027rules нужны','Не квалифицирует на World')],
    ['C940','E147'],'Местная Entry группа с coach → соответствующий qualifier → Junior Final для прошедших отбор; world Standard — отдельная будущая ступень.',
    ['Национальная финальная страница описывает немецкие школьные команды.','Возрастной минимум, языки и зарубежный приём не установлены.','Стандартный международный RoboCupJunior14–19 не перенесён на Entry.'],
    ['2027final9–12 марта,Nürnberg; публичный просмотр с10 марта.','Текущая страница2027:10 qualifiers; старый2026overview:9.','German Open2027 пауза; Entry не world qualification.'],
    [('Current2027final',rcj),('Rescue Entry distinctions',rescue)])
profile('wro-netherlands','WRO Netherlands · Elementary','regional','RM / FI8–12; Junior11–15; Senior14–19',
    'Национальный маршрут Elementary для Матвея; текущая опубликованная программа2026 требует нового календаря2027. Оскару пока рано.',
    [cat('RoboMission Elementary','8–12','2–3 + coach','LEGO или prototype по правилам','Год рождения; таблица2026 не2027','Национальный этап по выбранной площадке'),cat('Future Innovators Elementary','8–12','2–3 + coach','Любой допустимый robot project','Год рождения','Проект / booth / защита')],
    ['C941','C942'],'Подтвердить2027season и foreign team → coach /2–3 children → national discipline → quota отдельно.',
    ['EN interview и иностранная world quota прямо не установлены.','Не более2 команд организации в age division без согласования дополнительных мест.','Работу выполняют дети; coaches не руководят ими во время конкурсного блока.'],
    ['2026dates завершены; будущие даты не придуманы.','RMplatform rules изменились; старый LEGO-only не универсален.','EUR110 fee и фраза о free FIproject нуждаются в уточнении итогового счёта.'],
    [('National2026programme',nl_wro),('Team / ages / fees',nl_team)],age_tags=('9','10-12','teen'))
profile('fll-netherlands','FIRST LEGO League Netherlands · сезон2026/27','regional','Explore6–10; Challenge9–15; Future8–14',
    'Чёткий национальный календарь Challenge:15 региональных дней и финал6 марта2027. Oscar Explore и Matvey Challenge / Future — разные divisions.',
    [cat('Explore','6–10','Взрослый наставник; точный размер местной группы уточнить','Season model / robot','Возраст и festivalpartner','Без общего рейтинга'),cat('Challenge','9–15','2–10, coach18+','SPIKEPrime / EV3 / NXT по сезону','Местный максимум15, не общий16','Regional → Wageningen national6March2027'),cat('Future','8–14','4–8, до2 coach18+','Два CS&AI11+','Участники8–14, kit11+ не age cutoff','National eventApr/May TBD')],
    ['C943','C944']+['C'+str(i) for i in range(945,961)],'Оскар: Explore с6 лет → будущая старшая ступень. Матвей: команда / coach → региональный Challenge → Wageningen6 марта2027; международное приглашение по национальной квоте.',
    ['Подтвердить язык интервью и foreign / resident entry.','Открытый региональный календарь не подтверждает место в команде.','Future CS&AI и Challenge старой платформы различаются.'],
    ['National Future datesApril/May неизвестны; ICS не содержит вымышленных дней.','Международный общий Future5–14 не актуальный NL rollout8–14.','Региональный календарь subject to change; подтвердить перед поездкой.'],
    [('Nationalcalendar',nl_season),('Challenge',nl_ch),('Explore',nl_ex),('Future8–14',nl_future)])
profile('fll-belgium','FIRST LEGO League Belgium / BeLux','regional','Explore6–10; Challenge9–15; актуальный cutoff требует уточнения',
    'Восемь региональных конкурсных дней Challenge и BeLux финал13 марта2027. Младший Explore фестиваль, язык EN и cutoff проверяются отдельно.',
    [cat('Explore','6–10','Группа / local rules уточнить','LEGO model','Страница сcutoffJan1,2026 требует сверки','Recognition, не общий рейтинг'),cat('Challenge','9–15','Размер команды / current local rules уточнить','LEGO Challenge','Jan1,2026 vs season2026/27: уточнить','Региональный отбор → BeLuxChampionship')],
    ['C'+str(i) for i in range(961,971)],'Explore младшим → самостоятельная Challenge команда → regional contest day → BeLux13 марта2027; foreign admission и world quota отдельно.',
    ['Матвею нужен правильный cutoff и день рождения, не только текущий возраст9.','EN-site не доказательство EN interviews.','Даты Challenge не автоматически Explore festival dates.'],
    ['Wallonia / Limburg / BeLux exact venues не установлены в timing table.','Будущая Future младшая местная регистрация не подтверждена общей международной страницей.','Объявленная дата не принятая регистрация.'],
    [('Официальный nationalpartner timing',be_timing)])

def src(title,url,claim):return dict(title=title,url=url,claim=claim,kind='school',checked=CHECKED)
school=dict(id='S029',name='International School of Düsseldorf',iso='DEU',country='Германия',region='Европа',city='Düsseldorf',school_type='private',
    curriculum='IB continuum: PYP / MYP / DP по текущему школьному FAQ; отдельно национальный High School Diploma старшей ступени.',
    ib_programmes=[dict(programme=p,status='school_report_authorized',source='https://www.isdedu.de/our-accreditations') for p in ['PYP','MYP','DP']],
    ages='Pre-K–Grade12; обычное размещение по возрасту на1 сентября:6 летGrade1,9 летGrade4. Exact birthday / placement отдельно.',instruction_languages=['EN'],
    language_note='Все предметы кроме языковых преподаются наEnglish; EAL доGrade10. Дополнительные mother tongue activities включают Russian / Spanish, не основной технический язык.',
    fit=dict(mat='candidate',osc='candidate',note='Оба возрастных школьных кандидата; placement зависит от дня рождения1 сентября и assessment, команда не гарантирована.'),
    boarding='no',boarding_note='FAQ требует проживать с компетентным родителем / родительской фигурой; одиночное проживание учащегося не принимается. Младший пансион не опубликован.',
    programme='Grades1–5: BlueBot / RuggedRobots в Grade1, 3D printing, инженерные проекты; dedicated maker space в Grade4.',
    labs='Начальный maker space и classroom robots подтверждены; недельные часы mentor / competition lab не опубликованы.',
    ai='Summer AI & Robotics9–14 проводился2026; это не доказанный ежедневный AI curriculum или EN именно лагеря.',results=[],evidence='programme',
    admissions='Иностранные семьи приветствуются; rolling admission при наличии места, для начала года рекомендуют старт к30 апреля. Минимальный German не требуется, есть EAL. Подтвердить actual grade vacancy и placement.',
    cost='Текущая полная tuition / deposits / robotics extras не установлена; запросить годовую смету.',
    questions=['Есть ли действующая FLL / WRO / VEX команда дляGrade1 иGrade4, её coach и часы?','Какие protocol / teamcodes за последние3–5 сезонов, отдельно world / national / regional?','Можно ли семейным детям приезжать вAIcamp без местной школы, каков технический язык?'],
    sources=[src('Elementary: robots / makerspace','https://www.isdedu.de/elementary-school','Grade1 coding robots иGrade4 maker space'),src('FAQ: EN / grade / admission / residence','https://www.isdedu.de/admissions-faqs','Школьный язык, возрастной cutoff и проживание с родителем'),src('School authorisation / accreditation','https://www.isdedu.de/our-accreditations','Школьное утверждениеIB; реестрIB отдельно не проверен'),src('AI camp: прошлый набор',isd,'Summer9–14; новый календарь ещё неизвестен')],
    checked=CHECKED,priority=2,research_status='partial',verification='Проверены первичные школьные программы / FAQ. Организаторских протоколов мировых побед этой школы в текущем проходе нет.')
d['schools'].append(school)
d['school_focus'].update(version=34,checked=CHECKED,conclusion='29 школьных досье. ISD Düsseldorf добавлена по доказанному EN curriculum и младшей инженерной программе; мировой рейтинг школы не установлен.')
d['school_focus']['routes'].append(dict(name='Германия · английская школа и отдельный конкурсный наставник',ids=['S029'],detail='ISD даётEnglish IB и начальные coding robots / maker space. До переезда требуется конкретный coach, junior teamcodes и протоколы; программа не доказательство мирового лидерства. Проживание с родителем требуется школьнымFAQ.'))
d['school_focus']['gaps'][0]='29 школьных досье; полный мировой и национальный школьный аудит не завершён.'

d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
source_pairs=[('WRO Germany2027',de_season),('German private teams',de_join),('WRO Starter',de_starter),('WRO Sumo',de_sumo),('WRO RoboMission',de_rm),('FLL DACHseason',dach),('FLL Explore',explore),('FLL Challenge',challenge),('FLL Future5+',future5),('FLL Future8+',future8),('RoboCup2027final',rcj),('RoboCup Entry',rescue),('WRO Netherlands2026',nl_wro),('NL WROteam',nl_team),('FLL Netherlands calendar',nl_season),('NL Challenge',nl_ch),('NL Explore',nl_ex),('NL Future8–14',nl_future),('Belgium timing',be_timing),('NewTechKids bilingual camps / sessions',nt),('Garna English Robotics',garna),('TUHH Junior2026',tuhh),('ISD summerprogrammes',isd),('CodeFever AI / Dutch with ENsupport',code),('Machineering visitor profile',machine),('NEMO exhibitions',nemo),('NEMO visitor FAQ',nemo_faq),('Technopolis ON/OFF',tech),('Technopolis tickets','https://www.technopolis.be/en/tickets-bookings/'),('HNF robots / AI',hnf),('HNF robot PETER',hnf_peter),('HNF visitor prices',hnf_visit),('NEMO current Game On dates',gameon),('gamescom2027publicdays','https://www.gamescom.global/en/info/opening-times'),('gamescomvisitorages','https://www.gamescom.global/en/info/visitors')]
source_pairs.extend((s['title'],s['url']) for s in school['sources'])
sources=[]
for title,url in source_pairs:
    if url not in {s['url'] for s in sources}:sources.append(dict(title=title,url=url,checked=CHECKED))
    if url not in {s['url'] for s in d['sources']}:d['sources'].append(dict(title=title,url=url,checked=CHECKED,evidence='Прочитан первичный источник; условия и неопределённости сохранены в карточках.'))
country_events=lambda name:[e['id'] for e in new if e['country']==name]
d['north_europe_focus']=dict(version=34,checked=CHECKED,status='partial',title='Германия / Нидерланды / Бельгия · возраст, язык и маршрут',
    family='Матвей2017 и Оскар2020: английский, испанский и русский; класс / точный день рождения неизвестны. После трёх лет опыта нужна группа по уровню, а не повтор вводного курса.',
    conclusion='Для короткой English Robotics поездки яснее всего описаны NewTechKids8–12 (English+Dutch) и Garna7–17 (English, пансион; новый сезон ещё не объявлен). Для регулярного соревновательного пути Матвею проверять WRO Elementary / FLL Challenge; Оскару Explore или немецкую Future5+ при нужном классе. Германия имеет вариант English IB школы ISD, но текущая сильная младшая команда ещё требует проверки.',
    limitations='Первый ограниченный проход этих трёх стран; все местные клубы, школы / лагеря, EN judging, foreign quotas и школьные протоколы5–10 лет не собраны. Рекомендация по языку / возрасту и доказанным программам, не общий мировой рейтинг.',
    countries=[
        dict(iso='DEU',name='Германия',verdict='Сильный выбор категорий; язык и наставник решают',reason='WRO имеет полноценную Elementary и отдельную Starter; FLL разные младшие divisions. RoboCup Entry не мировой отбор. ISD показывает доказанный English curriculum.',
            mat='WRO Elementary8–12 или FLL Challenge9–16. Future8+ требуетGrades4–10; TUHH campGrades4–8. Собрать команду и проверить foreign quota / EN.',osc='WRO пока нельзя до8. Explore6–10 или Future5–7 приGrades1–3. Garna7+ только после дня рождения / cutoff нового сезона.',
            camp='Garna English Robotics7–17: прошлый2026пансион,2027необъявлен. TUHH21–22 ноября2026:Grades4–8, ENнеподтверждён. ISD AI9–14: новый набор объявятв январе2027.',
            school='ISD Düsseldorf: English, PYP / MYP / DP по школе, coding robotsGrade1 / maker spaceGrade4. Мировые результаты конкретной младшей команды не установлены.',
            city_route='Düsseldorf — пробный школьный период после mentor / admissions. Plötzky — отдельная лагерная поездка, Hamburg — двухдневный TUHH только при нужном классе / языке. Paderborn и Nürnberg — конкретные finals / museum visits.',
            budget='StarterEUR85 / команда; TUHHcampEUR50 за2 дня; Garna архивотEUR580 за7дней. Это неполная семейная / школьная смета, тарифы следующего года отдельно.',results_check='Запросить code команды и category / stage / award за3–5 сезонов у нынешнего coach. ISD makerspace и IB не доказательство world podium.',
            risk='WROfinal24–25июня2027предварителен; Starter не квалифицируется. RCJ2027finalдля отобранных немецких школьных команд; минимум Entry и foreign admission неизвестны.',
            event_ids=country_events('Германия')+['E034'],profile_ids=['wro-germany','fll-germany','robocup-germany-junior'],school_ids=['S029']),
        dict(iso='NLD',name='Нидерланды',verdict='Прозрачный Challenge календарь; English camp для8+',reason='15 региональных Challenge дней и6 марта2027национальный финал. NewTechKids прямо сочетаетDutch / English; текущий Future8–14 не младшая5+группа.',
            mat='NewTechKids8–12, Challenge9–15 или Future8–14; WROElementary8–12 после нового сезона. EN interview / foreign team отдельно.',osc='Explore6–10 и NEMO со взрослым. NewTechKids8+ / WRO8+ / текущаяFuture8+ пока не подходят.',
            camp='NewTechKids: сохраненыосень / декабрь2026, добавленыдвеTryItOutсессии4ноября. Это bilingual instruction; полноценное участие тольконаEN подтвердить. Жильёсемьи отдельно.',school='В этом проходе новые школы с доказанной младшей roboticsкомандой / результатами не добавлены; нужен отдельный школьный поиск.',
            city_route='Amsterdam — TryItOut / NEMO и короткая проба. Для годовой команды выбирается региональныйpartner, не ближайшийкрупныйгород; национальный финалWageningen6марта.',
            budget='FLLChallenge / FutureEUR200+195season,robotextra. ExploreEUR70seasonset,robotextra. WROEUR110по2026;2027сметаотдельно.',results_check='Даты15регионовне15международныхсоревнований. Проверятьдействующуюкоманду,category / code,foreignquota иcurrentcoach.',
            risk='Future5–14 международныйобзор не NL2026/27rollout8–14. КалендарьChallengeнеExplorefestival. ENсайтнеанглийскийjudge.',
            event_ids=country_events('Нидерланды')+['L132','L133','L134'],profile_ids=['wro-netherlands','fll-netherlands'],school_ids=[]),
        dict(iso='BEL',name='Бельгия',verdict='Сначала язык и cutoff; выставки семье отдельно',reason='Опубликованы8региональныхконкурсныхдней иBeLux13марта2027. CodeFeverAIосновнойDutchсEnglishsupport; Technopolisдаётсемейнуютехнологическуюэкспозицию.',
            mat='Challenge9–15 только после уточненияcutoffJan1,2026 иbirthdate. AIcampтребуетGrade4–6; обычныйориентир10+,неавтоматически9лет.',osc='Explore6–10 после festival / cutoff. Technopolisмладшиеwelcome. CodeFeverGrade4–6 иindustrialstudentrouteMachineeringдлянего не опубликованы.',
            camp='Wintercircus / CodeFeverпрошлый2026AIcamp: Dutchinstruction,ENhelp; новыйнаборнеобъявлен. ПолныйEnglishcampдляобоихвэтомпроходенеустановлен.',school='Новые школы с первично подтверждённой текущей младшей командой и awardprotocols здесь не добавлены.',
            city_route='Gent — будущийAIcampпослеgrade / language; Mechelen—Technopolis. Challengeпоlocalpartner. BrusselsMachineeringскорееотдельнаявзрослаяprofessionalпоездка.',
            budget='ТекущиелокальныеFLLfees / schooltuition / camp2027неустановлены. TechnopolisON/OFFвключёновобычныйбилет;ценаивремяпосещенияотдельно.',results_check='BeLuxфиналрегиональный; наградаExploreиCodeFevercertificateнеworldchampionship. Школьныекоманды / protocolисториюещёнужноисследовать.',
            risk='CutoffJan1,2026 настранице2026/27противоречив; адресаWallonia / Limburg / BeLuxвтаблиценеустановлены. ENhelpнеENкурс;Machineeringprimarychildrouteнеподтверждён.',
            event_ids=country_events('Бельгия'),profile_ids=['fll-belgium'],school_ids=[])],
    steps=[dict(title='Начать с правильного division и языка',detail='Оскару6 лет: Explore илиFuture5+вГерманииприGrades1–3. Матвею9: Elementary / Challenge; Future8+иуниверситетскиелагерятребуютпроверкикласса. ПолучитьподтверждениетехническогоEN / ES / RUдооплаты.'),
        dict(title='Одна команда и самостоятельный проект',detail='Проверитьcoach, weeklylabhours,3последнихсезонанастоящихprotocolsиуровеньпослетрёхлетопыта. Выбратьоднубазовуюлигу; самостоятельныйкод,журналитераций,конструкцияипрезентациянаENважнеенакоплениясертификатовпосещения.'),
        dict(title='Гостевой вход и национальная квота',detail='Раздельноподтвердитьправоиностраннойсемейнойкомандынастарт,qualificationнафинал,языксудействаиworldquota. Необъявленныедаты2027ипредварительныйGermanFinalнебронироватькакподтверждённые.'),
        dict(title='Пробный период перед школьным переездом',detail='Сначалаvisitingcamp / schooltourисовместимыегруппыобоихдетей. ISDEnglishнепревращаетвесьAIcampвEnglish;IBимузейнеподменяютдействующегосильногоjuniorcoach. Составитьполнуюсметуtuition / equipment / travel / housing.')],sources=sources)

# Keep human-facing copy readable without altering source URLs or former passes.
replacements={'2027registration':'регистрация2027','Grades':'классы','Grade':'класс','cutoff':'возрастной cutoff','foreign quota':'квота для иностранной команды','foreignquota':'квота для иностранной команды','foreign admission':'приём иностранцев','EN interview':'интервью на английском','EN interviews':'интервью на английском','world qualification':'квалификация на мировой финал','worldquota':'мировая квота','weeklylabhours':'еженедельные часы лаборатории','awardprotocols':'протоколы наград','awardprotocol':'протокол награды','currentcoach':'нынешний наставник','juniorcoach':'наставник младших','labhours':'часы лаборатории','ENhelp':'помощь на английском','ENкурс':'английский курс','ENсайт':'английский сайт','birthdate':'дата рождения'}
def clean(v):
    import re
    if isinstance(v,str) and '://' not in v:
        for a,b in replacements.items():v=v.replace(a,b)
        v=re.sub(r'(?<=[А-Яа-яЁё])(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])(?=[А-Яа-яЁё])',' ',v)
        return v
    if isinstance(v,list):return [clean(x) for x in v]
    if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
    return v
added={e['id'] for e in new};d['events']=[clean(e) if e['id'] in added else e for e in d['events']]
d['north_europe_focus']=clean(d['north_europe_focus'])
f=d['north_europe_focus'];f['heading']='Германия, Нидерланды и Бельгия.'
f['family']='Матвей — 2017, Оскар — 2020. Дети могут учиться на английском и испанском; русский тоже подходит. Точные дни рождения и нынешние классы неизвестны. После трёх лет опыта важно проверить сложность группы.'
f['conclusion']='Матвею стоит проверить WRO Elementary и FLL Challenge. Оскару — Explore, а в Германии также Future 5+ при подходящем классе. Для каникул NewTechKids прямо сочетает английский и нидерландский, Garna проводит робототехнику на английском с проживанием; новый сезон Garna ещё не объявлен. ISD Düsseldorf — вариант школы на английском, но действующую сильную младшую команду нужно проверить отдельно.'
fc={c['iso']:c for c in f['countries']}
fc['DEU'].update(mat='WRO Elementary 8–12 или FLL Challenge 9–16. Future 8+ требует также классы 4–10; TUHH — классы 4–8. Нужно проверить нынешний класс, команду, английскую защиту и национальную квоту.',osc='WRO до 8 лет ещё рано. Explore 6–10 или Future 5–7 при классе 1–3. Garna — с 7 лет после проверки дня рождения и правил новой смены.',camp='Garna 7–17: робототехника на английском, пансион по завершённой программе 2026; даты 2027 ещё неизвестны. TUHH 21–22 ноября 2026: классы 4–8, английский не подтверждён. ISD AI 9–14: новый набор объявят в январе 2027.',school='ISD Düsseldorf: обучение на английском, PYP / MYP / DP по школе, программируемые роботы в классе 1 и мастерская в классе 4. Мировые результаты младшей команды не установлены.',city_route='Düsseldorf — пробный школьный период после проверки наставника и приёма. Plötzky — отдельная лагерная поездка. Hamburg — TUHH при нужном классе и языке. Paderborn и Nürnberg — конкретные финалы и посещения.',budget='Starter — EUR 85 за команду. TUHH — EUR 50 за два дня. Garna — архивная цена от EUR 580 за семь дней. Школьное обучение, жильё, оборудование и поездки в эту смету не входят.',results_check='Запросить код команды, категорию, этап и точную награду за 3–5 сезонов у нынешнего наставника. Мастерская ISD и IB не доказывают мировое призовое место.',risk='German Final 24–25 июня 2027 предварителен; Starter на него не квалифицируется. RoboCupJunior Final принимает команды после немецкого отбора. Минимальный возраст Entry и право зарубежной семьи не подтверждены.')
fc['NLD'].update(reason='Опубликованы 15 региональных дней Challenge и национальный финал 6 марта 2027. Другие региональные даты ещё могут появиться. NewTechKids прямо сочетает Dutch и English; текущий Future рассчитан на 8–14.',mat='NewTechKids 8–12, Challenge 9–15 или Future 8–14; WRO Elementary 8–12 после публикации нового сезона. Английский интервью и иностранную команду нужно подтвердить.',osc='Explore 6–10 и NEMO со взрослым. NewTechKids, WRO и текущая Future начинаются с 8 лет.',camp='NewTechKids: сохранены осенние и декабрьские смены 2026, добавлены ранняя и поздняя Try It Out 4 ноября. Преподаватель сочетает Dutch и English; участие только с английским нужно согласовать.',city_route='Amsterdam — короткая проба NewTechKids и NEMO. Для годовой команды сначала выбирается региональный партнёр и наставник. Национальный Challenge финал — Wageningen, 6 марта 2027.',budget='Challenge / Future — EUR 200 регистрация + EUR 195 сезонный набор, роботы дополнительно. Explore — EUR 70 за набор, робот и местное событие отдельно. WRO — EUR 110 по программе 2026; смету 2027 уточнить.',results_check='Пятнадцать региональных дат — этапы одной сети. Для выбора школы нужны действующая команда, код, категория, протокол и нынешний наставник.',risk='Общий обзор Future 5–14 не доказывает младшую группу в Нидерландах: в 2026/27 запущена 8–14. Даты Challenge не являются датами Explore. Английский сайт не подтверждает английский судейства.')
fc['BEL'].update(reason='Опубликованы восемь региональных конкурсных дней и BeLux Championship 13 марта 2027. CodeFever преподаёт AI на нидерландском с английской помощью; Technopolis даёт семейную технологическую экспозицию.',mat='Challenge 9–15 после проверки противоречивого cutoff 1 января 2026 и дня рождения. AI camp требует классы 4–6; ориентир 10–13 лет, поэтому приём девятилетнего не гарантирован.',osc='Explore 6–10 после проверки фестиваля и cutoff. Technopolis прямо допускает младших. CodeFever и student route Machineering не дают опубликованного подходящего входа шестилетнему.',camp='Wintercircus / CodeFever: AI camp 2026 завершён, новый сезон не объявлен. Основной язык — Dutch, есть английская помощь. Полный английский технический лагерь для обоих в этом проходе не установлен.',city_route='Gent — будущий AI camp после проверки класса и языка. Mechelen — Technopolis. Challenge — через местного партнёра. Brussels Machineering — отдельная профессиональная поездка взрослого.',budget='Текущие местные взносы FLL, школьная стоимость и лагерь 2027 требуют отдельной сметы. ON/OFF включён в обычный билет Technopolis; цену и режим посещения проверить.',results_check='BeLux — региональный финал. Признание Explore и учебный сертификат CodeFever не мировая конкурсная медаль. История результатов школьных команд ещё требует исследования.',risk='Страница 2026/27 использует cutoff 1 января 2026; год нельзя исправлять без ответа партнёра. Адреса Wallonia, Limburg и BeLux не опубликованы в таблице. Английская помощь не полный английский курс; Machineering не подтвердил семейный вход 6/9.')
f['steps']=[dict(title='Начать с возраста, класса и языка',detail='Оскару: Explore или Future 5+ в Германии при классе 1–3. Матвею: Elementary / Challenge; Future 8+ и TUHH требуют проверки класса. Подтвердить язык технических объяснений и защиты до оплаты.'),dict(title='Проверить наставника и самостоятельную работу',detail='Получить расписание команды, часы лаборатории и три последних протокола по её коду. После трёх лет опыта подобрать сложность. Выбрать одну основную лигу, вести журнал испытаний, код и презентацию собственного проекта.'),dict(title='Разделить старт, финал и мировую квоту',detail='Отдельно подтвердить иностранный старт, квалификацию на финал и право на национальное международное приглашение. Предварительный German Final и необъявленные смены не считать подтверждённой поездкой.'),dict(title='Сначала проба, затем переезд',detail='Проверить школу и совместимые группы обоих детей на коротком визите. Английский школьной программы ISD не подтверждает язык каждого лагеря. Нужна полная смета обучения, жилья, оборудования и поездок.')]
d['schools'][-1]=clean(d['schools'][-1]);d['league_guide']['profiles'][-6:]=clean(profiles)
c=d['camp_focus'];c['validation_previous']=c['validation'];c.update(version=34,checked=CHECKED,carried_forward_ids=c['added_ids'],added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=['L132','L133','L134'],validation=dict(version=34,status='pending'))
c['routes'].extend([
    dict(name='Германия · English пансион и проверка школьного класса',ids=['L273','L274','L275','E150','L277'],detail='Garna 7–17 прямо проводит Robotics на English; следующий набор 2027 ещё неизвестен. TUHH 21–22 ноября требует классы 4–8, English не подтверждён. ISD AI 9–14 — прошлый 2026 набор; новый откроют в январе 2027, язык модуля отдельно. Future 5+ — регулярная учебная группа для 5–7 и классов 1–3, без официальных завершающих событий сезона.'),
    dict(name='Нидерланды · bilingual Robotics8–12',ids=['L132','L133','L134','L271','L272','E148','E151'],detail='NewTechKidsсочетаетDutchиEnglish,необещаяотдельныйEnglish-onlyпоток. Сохраненыосень / декабрь2026; TryItOut4 ноябряимеетраннюю / позднююсессии. Оскару6летвэтигруппыещёрано;NEMOдаётсемейноеобразовательное посещение.'),
    dict(name='Бельгия · English помощь и семейная экспозиция',ids=['L276','E149','E146'],detail='CodeFeverAIcampGrades4–6: Dutchосновной,ENsupport,новыйсезоннеобъявлен. TechnopolisON/OFFрекомендует8+,младшиедопускаются;текстEnglishнеENкурс. Machineeringstudentrouteвышеprimary6/9.')])
c['routes'][-3:]=clean(c['routes'][-3:])
a=d['completeness_audit'];a['validation_previous']=a['validation'];a.update(version=34,checked=CHECKED,status='partial',
    scope='Ограниченный первичный проход Германии / Нидерландов / Бельгии: national / regional calendars, age / grade gates, camps, schools and family visits.',
    conclusion=f'{len(new)} новых карточек, шесть национальных профилей и школьное досье ISD. Добавлены реальные опубликованные этапы2026/27, подтверждены public days gamescom2027 и отделены язык преподавания / помощь / материалы. Мир и все местные календари пока исследованы частично.',
    new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=['E034','L132','L133','L134'],updated_profile_ids=[],new_school_ids=['S029'],validation=dict(version=34,status='pending',publication='pending'))
a['source_issues'].extend([dict(name=name,status=detail,official_alternative=url) for name,detail,url in [
    ('RoboCup Germany2027 vs old overview','Текущая финальная страница2027 говорит10 qualifiers; более старые2026страницы говорят9. GermanOpen2027пропускают; Entryнеworldqualification.',rcj),
    ('Belgium age cutoff','Таблица сезона2026/27 указывает возраст на1 января2026. Нельзя молча заменитьгодна2027; точный cutoff / деньрождения нужно подтвердить.',be_timing),
    ('Netherlands Future rollout','Текущий местный division8–14; общий обзор5–14 не доказательство местной младшей группы6 лет.',nl_future),
    ('WRO Germany final provisional','24–25 июня2027Munich ещё preliminary; финансирование не закрыто. Даты вperiod, start / end пустые.',de_season),
    ('NEMO Game On date conflict','Текущая visitorpage10 июля–25 октября2026, старыйpressrelease11 июля–26 октября. Использован актуальный календарь экспозиции.',gameon),
    ('Camp language distinctions','NewTechKids English+Dutch teaching; GarnaEnglishRobotics. CodeFeverDutchteachingсENhelp; школьныйEnglishISDнепрямоcampinstruction.',code)]])
a['known_backlog'].append(dict(kind='Европа · следующий местный проход',name='Германия / Нидерланды / Бельгия: все clubs и школьные результаты',reason='Нужны все местные camps / schoolteams,новыеWROdates2027,английскоеjudgingиforeignquota,семейныйдопускprofessionalexpo,5–10летorganizerprotocols нынешних juniorcoaches.',url=nl_season))
for row in a['continents']:
    if row['name']=='Европа':row['remaining']+=' Германия / Нидерланды / Бельгия: первый частичный проход; все местные клубы, языки, иностранные квоты и полные школьные результаты остаются открыты.'
d['expansion_log'].append(dict(version=34,checked=CHECKED,added=len(new),updated_ids=['E034','L132','L133','L134'],new_profiles=6,new_schools=1,note='Bounded DE / NL / BE primary-source expansion; preserve CHE / ESP / FRA and earlier world passes.'))
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v34.json')
r.setdefault('research_passes',[]).append(dict(version=34,checked=CHECKED,scope='DE / NL / BE primary-source pass',added_records=len(new),new_profiles=6,new_schools=1,status='partial',remaining='Local operators / schools, actual2027WROdates,ENjudging,foreignquota,and organizer schoolprotocols5–10years. World goal active.'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=34,status='local_checks_pending_publication_pending');rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=34,added=len(new),competitions=sum(e['block']=='Соревнования' for e in new),events=sum(e['block']=='События' for e in new),camps=sum(e['block']=='Лагеря' for e in new),profiles=6,schools=1,world_complete=False)))
