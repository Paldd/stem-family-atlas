"""Bounded fourth primary-source CHE / ESP / FRA pass, keeping world inventory."""
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];W=ROOT.parent/'stem-family-atlas-work'
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1535 and d['completeness_audit']['version']==37
CHECKED='2026-10-02';new=[];profiles=[];byid={e['id']:e for e in d['events']}
for n in ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text()).body:
 if isinstance(n,ast.FunctionDef) and n.name in ['ref','event','profile']:exec(compile(ast.Module(body=[n],type_ignores=[]),'helpers','exec'))
YES='Условно: возраст подходит; класс, место, язык и иностранный приём подтвердить'
NO='Нет: ниже минимальной категории'
P4='P4 — допуск / язык не подтверждён; перед поездкой обязательна проверка'
def add(*a,**k):
 e=event(*a,**k);e['region']='Европа';return e
def cat(name,age,team,gear,entry):return dict(name=name,age=age,team=team,hardware=gear,entry=entry,age_rule='Класс, контрольную дату возраста и национальные правила проверяют отдельно')
def camp(id,title,country,city,url,age,mat,osc,gear,note,period='',cost='Новая цена и места не установлены',start='',end='',languages=(),mode='unconfirmed',priority='P2 — после проверки допуска'):
 e=add(id,title,country,city,url,age,mat,osc,'Выбрать конкретный поток; согласовать уровень после трёх лет соревнований, возраст / класс, язык и внешнюю запись.',gear,block='Лагеря',participation='day_camp',note=note,cost=cost,start=start,end=end,languages=languages,priority=priority,evidence='program',date_scope='camp_window')
 e.update(period=period,language_mode=mode)
 if languages:e.update(language='Преподавание '+ '/'.join(languages)+' прямо указано для этой программы; новый поток подтвердить',language_certainty='Язык преподавания, а не язык сайта')
 return e
lego='https://www.education.lego.com/en-us/lego-league/program-update/';first='https://www.firstinspires.org/programs/k-8'
e=add('C1048','LEGO League · новая самостоятельная программа 2027/28','Мир','Национальный оператор и этап ещё не объявлены для этой семьи',lego,'5–7 и 8–16 по глобальному анонсу; местные рамки отдельно',YES,YES,
 'Запуск с августа 2027. Подходят школа, after-school или независимый клуб; национальный оператор, отбор и сроки ещё нужны.',
 '2027/28: версии SPIKE / legacy и Computer Science & AI. С 2028/29 электроника CS & AI; LEGO bricks допустимы.',scope='international',evidence='program',priority='P3 — будущая программа, национальный вход ещё не определён',
 note='FIRST LEGO League заканчивается BIOGLOW 2026/27. Новая LEGO League и новая FIRST K–8 — разные программы. 5–7: команда 4; 8–16: минимум 4, рекомендуется 8, до 10 рекомендовано; 8+ и 11+ судят отдельно. Март–май 2027 — ориентировочное окно регистрации, не подтверждённый дедлайн / турнир. Не покупать комплект без выбора программы.')
e.update(region='Мир',iso=[],period='Анонс запуска август 2027; дата конкретного турнира отсутствует',references=[ref('Независимая будущая программа FIRST',first)])
e=add('C1049','FIRST · новая K–8 после FLL · сезон 2027/28','Мир','Название, локальные категории и этапы ещё уточняются',first,'K–8: школьная ступень; точные будущие категории ещё не опубликованы',YES,YES,
 'Следить за объявлением FIRST и местного партнёра; анонс не подтверждает регистрацию, слот или правила турнира.',
 'FIRST планирует совместимость SPIKE Prime / Essential до 2028/29; будущий список платформ уточняется.',scope='international',evidence='program',priority='P3 — будущая программа, национальный вход ещё не определён',
 note='Это отдельная от LEGO League ветка. План поддержки SPIKE FIRST до 2028/29 отличается от плана LEGO перейти на CS & AI с 2028/29. Возраст FTC / FRC не переносится на K–8. Новые правила, формат наград и национальные отборы не установлены.')
e.update(region='Мир',iso=[],period='Будущая K–8 2027/28; турниры не датированы',references=[ref('LEGO: собственная ветка',lego)])
biber='https://www.informatik-biber.ch/was-ist-der-informatik-biber/';biber26='https://www.informatik-biber.ch/vor-wettbewerb-2026/'
e=add('C1050','Informatik-Biber Schweiz · школьная информатика 2026','Швейцария','Онлайн под школьным координатором',biber26,'3–13 школьный год; примерно 8–20 по официальному описанию',
 'Условно: нужен минимум 3-й школьный год и согласованный язык; год рождения этого не подтверждает',NO,
 'Учитель / школьный координатор регистрирует детей; в 2026 первый участник может войти по QR, второй в паре — с логином.',
 '40 минут логических / вычислительных задач на компьютере или планшете; предварительное программирование не требуется.',start='2026-11-09',end='2026-11-20',scope='national',participation='individual_or_team',priority=P4,evidence='rules',themes=('coding',),
 cost='Бесплатно по описанию организатора',note='Минимум установлен по школьному году, не по возрасту 9. Допуск ученика зарубежной школы и EN/ES версия швейцарского зачёта не подтверждены. Это национальный Bebras; участие не даёт мировой титул робототехники.')
e['references']=[ref('Классы и 40 минут',biber)]
eh='https://bebras.ehu.eus/';bc='https://bebras.cat/'
e=add('C1051','Bebras EHU / España · 3º–4º Primaria · цикл 2026/27','Испания','Онлайн через школу и учителя',eh,'Младшая из пяти категорий: 3º–4º Primaria',
 'Условно: требуется именно 3º / 4º Primaria, текущий класс неизвестен',NO,
 'Учитель регистрирует класс в ViLLE и выбирает день / час; портал открывается с 9 ноября 2026, конец окна не опубликован.',
 '12–15 задач, 45–50 минут; без предварительного программирования.',scope='national',participation='individual_or_team',themes=('coding',),languages=('ES','EN'),cost='Стоимость / новая регистрация через школу уточняются',evidence='rules',
 note='Задания доступны на испанском, английском, баскском и каталанском. Пять категорий EHU не совпадают с шестью категориями Bebras CAT: начальные 1º/2º нельзя автоматически перенести в англоязычный EHU.')
e['period']='С 9 ноября 2026, учитель выбирает сеанс; конец окна не объявлен'
for id,name,age,mat,osc in [('C1052','Arrel','1º–2º Primaria; 6–8','Нет: для Матвея нужна следующая школьная категория',YES),('C1053','Branca','3º–4º Primaria; 8–10',YES,NO)]:
 e=add(id,'Bebras CAT · '+name+' · ноябрь 2026','Испания','Catalunya · онлайн через школьного координатора',bc,age,mat,osc,
  'Школьный вход; в Arrel / Branca можно индивидуально или группой до 4. Точный класс, географический приём и язык подтвердить.',
  'Интерактивные вычислительные задачи; в младших категориях нет штрафа за неправильный ответ.',start='2026-11-09',end='2026-11-13',scope='regional',participation='individual_or_team',priority=P4,evidence='rules',themes=('coding',),cost='Бесплатно',
  note='Инициатива описана как не имеющая соревновательного характера. Отдельное приглашение лучших работ не является мировой квалификацией. Для младших CAT не подтверждён EN / ES; ссылки на другие национальные порталы не доказывают одинаковый возраст и язык.')
 e.update(reward='Образовательный результат; мировой отбор / международная медаль не обещаны')
rc='https://sites.google.com/view/robocampeonesfuenlabrada/'
e=add('C1054','RoboCampeones · Soccerbot Maqueen / Nezha · Primaria','Испания','Fuenlabrada · площадка нового сезона уточняется',rc,'Primaria; точная нижняя граница и новый школьный регламент не установлены',YES,YES,
 'Участие школьным центром и наставником; запись независимой / зарубежной команды нужно подтвердить.',
 'Отдельные Soccerbot турниры Maqueen и Nezha из Código Escuela 4.0; не единый универсальный робот.',scope='regional',evidence='program',
 note='Прочитана редакция 29 апреля 2026 в Fernando Martín, 65 образовательных центров; это прошедший турнир. Новые даты 2027 не объявлены. Primaria сама по себе не подтверждает допуск каждого шестилетнего ученика.')
e['period']='Новый сезон не датирован; подтверждение программы по прошедшей редакции 2026'
robo='https://www.robolympics.ch/';roborules='https://www.robolympics.ch/wp-content/uploads/2026/06/Hauptreglement_2026.pdf'
e=add('C1055','RobOlympics OST · Rapperswil · 21 ноября 2026','Швейцария','OST · Rapperswil',robo,'Главным образом с 7-го школьного года до окончания школы; младше — только исключение',
 'Уточнить: ниже обычной школьной ступени; нужна письменная возрастная уступка','Уточнить: значительно младше обычной ступени; не планировать участие без разрешения',
 'Команда максимум 7: руководитель команды и до 6 участников. Организатор может разрешить младших; регистрация на сайте открыта с 18 мая, срок закрытия не установлен.',
 'LEGO Class и Open Class отдельно; автономный робот и собственный код. LEGO — разрешённые LEGO controllers / детали, правила дисциплины отдельно.',start='2026-11-21',scope='national',priority=P4,evidence='rules',
 note='Mentor не выполняет код / решения вместо детей. Это школьный турнир, мировой отбор не доказан. Для посещения: организатор прямо приглашает зрителей и указывает бесплатный вход; условия workshop и сопровождения ребёнка отдельно. Посещение не требует конкурсного исключения.')
e['references']=[ref('Главные правила 2026',roborules)]
castor='https://www.castor-informatique.fr/'
e=add('C1056','Castor informatique France · выпуск 2026','Франция','Онлайн в школе под контролем учителя',castor,'CM1–Terminale; возраст сам по себе не определяет категорию',
 'Условно: нужен CM1 или старше; EN французского зачёта не подтверждён',NO,
 'Учитель организует сеанс в классе; индивидуально или пара. Международный школьный / EN допуск подтвердить.',
 '45 минут, около 10 интерактивных задач четырёх уровней сложности, без предварительного программирования.',start='2026-11-08',end='2026-12-19',scope='national',participation='individual_or_team',priority=P4,evidence='rules',themes=('coding',),cost='Бесплатно',
 note='Использован календарь именно выпуска 2026: 8 ноября–19 декабря; шаблон о четырёх неделях не заменяет эти даты. Кнопка English на платформе не подтверждает EN французского национального зачёта. Диплом и оценка Castor не равны мировой олимпиадной медали.')
vu=json.loads((W/'urls-europe-confirm-v38.json').read_text());vex='https://www.techlabs.ch/vex-events-products'
rows=[('L328','Junior Robotics Lab · 7–9','Basel · Academia International School','vexclass0','7–9','17 августа–14 декабря 2026 · понедельник 16:00–17:30','CHF 648','VEX GO / Scratch','Показан лист ожидания; Матвей подходит до 10-летия, не автоматически на весь будущий цикл.'),
 ('L329','VEX IQ Robotics Lab · 9+','Basel · ELYS','vexclass1','9+','19 августа–16 декабря 2026 · среда 16:45–18:15','CHF 648','VEX IQ; для продвинутых текстовое программирование / Python','Учебная подготовка; соревновательная заявка и место отдельно.'),
 ('L330','VEX IQ Competition Lab · 9–14','Basel · ELYS','vexclass2','9–14','21 августа 2026–6 февраля 2027 · пятница 16:30–18:00','CHF 769','VEX IQ: подготовка к Alpine','Сетка сеансов указывает 2026/27; заголовок ошибочно называет February 2026. Соревновательный слот не гарантирован.'),
 ('L331','VEX IQ Competition Lab · 9–14','Zürich · Hohlstrasse 201','vexclass3','9–14','29 августа 2026–30 января 2027 · суббота 10:30–12:00','CHF 720','VEX IQ: командный design / code / testing','Сетка сеансов 2026/27 важнее заголовка February 2026. Alpine — возможный путь, национальный допуск команды отдельно.')]
for id,title,city,key,age,period,cost,gear,note in rows:
 e=camp(id,'TechLabs · '+title,'Швейцария',city,vu[key],age,YES,NO,gear,note+' EN и DE прямо указаны на странице курса. Правила Alpine исключают нешвейцарские команды; внешняя запись на курс не подтверждает национальную квоту.',period,cost,languages=('EN','DE'),mode='bilingual')
 e.update(participation='regular',format='Регулярные внешкольные занятия; не многомесячный лагерь',references=[ref('Организатор и Alpine',vex)])
nube='https://www.nube7.es/campamento-pascua/'
e=camp('L332','Nube7 / Trastobot · Pascua maker / robotics · следующий набор','Испания','Valencia',nube,'6+',YES,YES,'Моторы / переключатели, Scratch, maker / 3D и научные эксперименты',
 'Прошедшая смена 7–10 апреля 2026, 09:00–14:00; 3 блока по 80 минут, до 10 детей в группе. Учителя говорят Valencian / Castilian / English, но основной язык всей технической смены не указан. Новые даты не опубликованы.',
 'Следующий набор неизвестен; описание основано на Pascua 2026','2026: 115€ за 4 дня / 35€ день; будущая цена неизвестна',mode='support')
e.update(support_languages=['ES','EN'],language='Учителя говорят ES / EN / Valencian; весь технический поток на EN не подтверждён',language_certainty='Поддержка учителей, не обещание EN полного дня')
e=camp('L333','Robotix / COIIAS · Asturias · следующий лагерь','Испания','Asturias · площадку новой смены уточнить','https://www.coiias.es/cursos-y-jornadas/campamento-verano-2026-robotix','6–16',YES,YES,
 'Возрастные robotics проекты; Arduino / drone / 3D для старших, не обязательная программа шестилетнего.',
 'Прошедшая смена 6–10 июля 2026, 10:00–14:00. Дети 3–5 имеют другой двухчасовой поток. Внешняя семья не обязана быть семьёй инженера-члена, но иностранный приём и язык уточняются. Новые даты неизвестны.',
 'Следующий набор не датирован','2026: 110€ внешняя семья / 100€ член COIIAS; новые тарифы неизвестны')
mir='https://www.lamiranda.eu/campamentos-de-verano'
for id,title,age,mat,osc,note in [
 ('L334','Junior','6–9; Primary 1–3; 2026 рождения 2017–2019',YES,'Уточнить: 2020 нет в опубликованной таблице 2026, хотя возраст 6 есть',
  'Junior 2026 прямо перечисляет только рождения 2017–2019. Оскар 2020 не получает автоматический допуск по цифре 6. Матвею после 10-летия нужен другой поток.'),
 ('L335','Teens','Заголовок 9–12, описание 10–12 / Primary 4–6; 2026 рождения 2014–2016','Уточнить: возраст / класс конфликтуют; 2017 нет в таблице 2026',NO,
  'Заголовок и описание расходятся: 9–12 против 10–12. Матвею нужна новая таблица 2027 и подтверждённый placement.')]:
 e=camp(id,'La Miranda · '+title+' Summer · следующий набор','Испания','Barcelona',mir,age,mat,osc,'Robotics / multimedia внутри смешанного спортивно-творческого лагеря',
  note+' Весь programme на English прямо заявлен. В 2026 29 июня–24 июля, 09:00–17:00; пример расписания даёт robotics / multimedia 16:00–17:00, не полный день робототехники. Будущие даты не опубликованы.',
  'Новый набор не объявлен; подтверждённый язык и расписание относятся к 2026','2026: 312€/неделя внешняя семья, 10% Inspired discount; будущая цена неизвестна',languages=('EN',),mode='primary',priority=P4)
log='https://roboticaeducativa.logix5.com/extraescolares-escuela/'
e=camp('L336','Logix5 Madrid · регулярный maker / robotics · пробные пакеты','Испания','Madrid',log,'5+',YES,YES,'Micro:bit / Makeblock / Edison / Beduino; возрастные 3D / Arduino / Python / AI / IoT',
 '2026/27: занятия 17:30–19:00; пакеты с бронированием за 24 часа подходят для пробного периода. Уровень после 3 лет соревнований, действующую команду и язык технических занятий подтвердить.',
 'Регулярный сезон 2026/27; выбранный день по записи','На странице: 15€ разовый, 70€ / 6, 130€ / 13; 38€ новый / 34€ действующий ученик в месяц')
e.update(participation='regular',format='Регулярные занятия / пакет пробных визитов; не лагерь')
e=camp('L337','Logix5 Madrid · летняя robotics школа · следующий набор','Испания','Madrid','https://roboticaeducativa.logix5.com/escuela-de-verano/','6+; Infantil 3–6 — другой поток',YES,YES,
 'Проекты роботов, программирования и обучения AI-модели по возрасту',
 'Прошедшие недели 29 июня–3 июля, 6–10 и 13–17 июля 2026, 10:00–13:00. Новые смены не объявлены, EN / ES техническое преподавание в прочитанных условиях не указано. В 6 лет два диапазона пересекаются, нужен подходящий опытный поток.',
 'Лето нового сезона не датировано','2026: 150€ неделя / 35€ день; новый тариф неизвестен')
e=camp('L338','Agora Granada · Robotics & Virtual Reality · следующий набор','Испания','Granada','https://granada-college.agorainternationalschool.es/vida-escolar/summer-camp','9–14',YES,NO,
 'Робототехника / VR с outdoor и бассейном',
 'Язык и даты именно Robotics & VR не опубликованы в прочитанном описании. English у отдельного Summer Fun и English/Spanish у Creative Immersion не перенесены на робототехнический поток.',
 'Robotics / VR programme без подтверждённой будущей смены')
kids='https://kidsrobots.fr/about/'
for i,(start,end) in enumerate([('2026-10-19','2026-10-23'),('2027-02-08','2027-02-12'),('2027-02-15','2027-02-19'),('2027-04-05','2027-04-09'),('2027-04-12','2027-04-16'),('2027-07-05','2027-07-09'),('2027-08-16','2027-08-20'),('2027-08-23','2027-08-27')],339):
 e=camp('L'+str(i),'Kids Robots · Mini-Robots · '+start,'Франция','Montpellier · 42 rue du Faubourg Boutonnet',kids,'9–12; CM1 / CM2 / Collège',YES,NO,
  'Программируемые роботизированные модели и автоматизация; block programming',
  '09:30–12:00, пять полудней. Восемь датированных карточек — смены одного оператора. EN / ES преподавание не подтверждено; до подтверждения не включено в семейный календарь. 26–30 октября помечено complet и не предлагается как свободная смена.',
  'Пять полудней 09:30–12:00','300€/5 полудней на странице',start,end,priority=P4)
 e['references']=[ref('Адрес оператора','https://kidsrobots.fr/contact/')]
e=camp('L347','Kids Robots · Kids-Robots · 8–9 · программа','Франция','Montpellier',kids,'8–9; CE2 / CM1 / CM2',
 'Условно только до 10-летия и после школьного placement',NO,'Младшие IR / tablet robots и объяснение принципов',
 'Начальная программа отличается от Mini 9–12. Матвей с тремя годами опыта может нуждаться в более сложном Mini. Новая отдельная запись и EN / ES не подтверждены.',cost='250€ за 5 полудней на странице',period='Программа 8–9 лет; конкретная смена и свободное место ещё не выбраны',priority=P4)
for id,title,age,mat,osc,url in [
 ('L348','Robot Run · 6–9','6–9','Условно до 10-летия; при 10 годах выбрать 9–14',YES,'https://www.algora-grandouest.fr/produit/stage-robot-run-6-9-ans/'),
 ('L349','Robot Run · 9–14','9–14',YES,NO,'https://www.algora-grandouest.fr/produit/stage-robot-run-9-14-ans/')]:
 e=camp(id,'Algora · '+title,'Франция','Saint-Herblain',url,age,mat,osc,'Автономная машинка, код и собственная трасса',
  '22–24 февраля 2027, 14:00–17:00, три полудня. Итоговый внутренний конкурс / диплом не равен международной медали. EN / ES преподавание не подтверждено.',
  'Три полудня 14:00–17:00','216€ на странице','2027-02-22','2027-02-24',priority=P4)
e=camp('L350','Algora · AI initiation / intermediate · возраст уточнить','Франция','Nantes Nord','https://www.algora-grandouest.fr/produit/stage-ia-9-16-ans/',
 'Заголовок 9–16; отдельный тег 14+ — конфликт','Уточнить: 9 лет в заголовке, но есть 14+; письменный допуск обязателен',NO,
 'Обучение моделей распознавания изображения / голоса, smart objects / robot sorter',
 '19–21 апреля 2027, 09:30–12:30, три полудня. Не считать Матвея допущенным, пока оператор не разрешит конфликт 9–16 / 14+. EN / ES не подтверждены.',
 'Три полудня 09:30–12:30','229€ на странице','2027-04-19','2027-04-21',priority=P4)

def expo(id,title,country,city,url,age,note,start='',end='',family=False,tier='profile',gear='Robotics / AI / technology demos',period='',cost='Условия билета и цены нового выпуска уточнить'):
 e=add(id,title,country,city,url,age,YES if family else 'Уточнить допуск ребёнка 9 лет',YES if family else 'Уточнить допуск ребёнка 6 лет',
  'Посетительский билет / регистрация; возраст, сопровождающий и допуск к мастерским отдельно.',gear,block='События',start=start,end=end,participation='visitor',priority='P2 — семейный визит после проверки билетов' if family else P4,note=note,cost=cost)
 e.update(period=period,exhibition_tier=tier,visitor_policy='family' if family else 'confirm_children',visitor_policy_note=note,
  adult_entry='Порядок visitor registration / билет нового выпуска уточнить',exhibitor_note='Список конкретного выпуска подтверждает участников; присутствие всех мировых компаний не обещано.',highlights=list(gear.split(' / ')),exhibitor_directory_url=url)
 return e
expo('E163','Alpine Robo Games · семейные зрители VEX · Basel 2027','Швейцария','Basel',vex,'Организатор приглашает семьи; условия workshop / билета отдельно',
 '6–7 февраля 2027 — общая двухдневная программа V5 / IQ, семьи и зрители явно приглашены. Это не переносит двухдневное окно на конкретный IQ qualifying event C549 и не отменяет Swiss-team restriction для участников.',
 '2027-02-06','2027-02-07',True,'family_alternative',gear='VEX robot matches / demos / hands-on activities')
her='https://erw.hisparob.es/'
e=expo('E164','HispaRob ERW · семейная ярмарка роботов · 27 ноября 2026','Испания','Santiago de Compostela · Instituto Politécnico de Santiago',her,'Ярмарка открыта семьям и широкой публике',
 'Ярмарка только 27 ноября 17:00–19:00. Дни 26–27 содержат профессиональные / педагогические блоки; они не считаются двумя семейными днями. Старое объявление называло Cidade da Cultura; использована актуальная площадка основного ERW-сайта.',
 '2026-11-27','',True,'family_alternative',gear='Educational robots / практические демонстрации',period='27 ноября · 17:00–19:00 Europe/Madrid')
e.update(date_scope='session_days',sessions=[dict(date='2026-11-27',topic='Семейная ярмарка роботов',start_time='17:00',end_time='19:00',timezone='Europe/Madrid',time_note='Предварительная программа организатора; билет / регистрация ещё уточняются')])
expo('E165','HispaRob TechTalks · AI в роботизированной хирургии','Испания','Madrid · Singular Things, C/ Marqués de Monteagudo 22–5A',
 'https://www.hisparob.es/hisparob-techtalks-abordara-el-impacto-de-la-ia-en-la-cirugia-robotizada/',
 'Профессиональная встреча; допуск несовершеннолетних не опубликован',
 '19 ноября 2026, 19:00–21:00; ограниченный зал и предварительная регистрация. Это тематический professional panel, не большая универсальная выставка и не подтверждённый детский визит.',
 '2026-11-19',tier='regional',gear='Medical robotics / AI / professional talks',period='19:00–21:00 Europe/Madrid')
siae='https://www.siae.fr/en/general-public/'
e=expo('E166','Paris Air Show 2027 · семейные выходные и технологии','Франция','Paris · Le Bourget',siae,'Семьи и младшие посетители прямо приглашены в public programme',
 'Общий салон 14–20 июня 2027. Family programme описывает выходные, но конкретные датированные public tickets ещё не опубликованы: не превращать весь trade week в семейное окно. Условия student Friday не дают обоим детям автоматический бесплатный билет. Авиационные / drone технологии, не выставка всех производителей роботов.',
 family=True,tier='global',gear='Aerospace / drones / future aircraft / young visitor discovery',period='Общий салон 14–20 июня 2027; точные public / family дни билетов ожидаются')
e['references']=[ref('Общий календарь салона','https://www.siae.fr/'),ref('Каталог: выпуск и список 2027 проверяются отдельно','https://www.siae.fr/en/the-show/list-of-exhibitors/')]
expo('E167','tech&fest 2027 · Grenoble · deep tech / AI / industry','Франция','Alpexpo Grenoble · 2 avenue d’Innsbruck','https://www.tech-fest.fr/',
 'Предложение для collèges / lycées не подтверждает допуск Primary 6/9',
 '3–4 февраля 2027, 08:30–20:00. Tech human / planet / fab / solutions. Семейный minor policy не найден; школьный профессиональный визит старших не переносится на начальную школу.',
 '2027-02-03','2027-02-04',gear='Deep tech / AI / industrial innovation',period='3–4 февраля 2027 · 08:30–20:00')
new[-1]['references']=[ref('Practical information','https://www.tech-fest.fr/fr/content/practical-information/')]
expo('E168','Tech Show Madrid 2026 · AI / cloud / data / cyber','Испания','IFEMA Madrid · павильоны 3–5','https://www.techshowmadrid.es/',
 'Профессиональная выставка; возраст и minor admission не установлены',
 '4–5 ноября 2026. Совмещает Cloud & AI Infrastructure, Big Data & AI, Cybersecurity, Data Centre и digital-business выставки. На странице названы Oracle / Maisa AI / Zoho / Red Hat / Intel; это не подтверждение присутствия всех robot companies. Детский допуск не опубликован в прочитанном источнике.',
 '2026-11-04','2026-11-05',gear='AI / Cloud / Data / Cybersecurity')

profile('lego-league-2027','LEGO League · самостоятельная ветка с 2027/28','core','5–7 и 8–16 по глобальному анонсу',
 'Новая LEGO programme после последнего FIRST LEGO League 2026/27; местные категории и квоты ещё нужны.',
 [cat('5–7','5–7','4','Будущая LEGO CS & AI / сезонные условия','Школа или клуб; региональная процедура ещё уточняется'),cat('8+ / 11+','8–16','Минимум 4, рекомендовано 8; до 10 рекомендовано','2027/28 SPIKE / legacy или CS & AI','Возрастные судейства разделены; местное правило ещё подтвердить')],
 ['C1048'],'Выбрать национального партнёра → category / kit → команда → сезонный отбор; опубликованного этапа для семьи пока нет.',
 ['Старт август 2027; регистрации ориентировочно март–май, точный местный срок неизвестен.'],
 ['2028/29: CS & AI электроника; это не план FIRST SPIKE.','Не покупать новый kit до выбора ветки и локальной команды.'],[('Официальный анонс LEGO',lego)],age_tags=('6','9','10-12','teen'))
profile('first-k8-next','FIRST K–8 · отдельная будущая программа','core','K–8; будущие числовые категории уточняются',
 'FIRST продолжает младший инженерный маршрут после окончания FLL; это отдельная от LEGO ветка.',
 [cat('K–8 next','K–8','Новый состав команды ещё не объявлен','FIRST планирует SPIKE Prime / Essential до 2028/29','Нужны новый формат и национальные правила')],
 ['C1049'],'BIOGLOW 2026/27 → объявление FIRST 2027/28 → местная команда и hardware → новый сезон.',
 ['Название, категории и отбор нового сезона ещё нужны.'],['Нельзя переносить возраст FTC или FRC на младшую K–8.','LEGO League с 2028/29 имеет другой hardware plan.'],[('FIRST K–8',first)],age_tags=('6','9','10-12'))
profile('vex-switzerland-junior','VEX Switzerland · младшая EN / DE подготовка','regional','Junior 7–9; IQ 9+ / 9–14 по конкретным курсам',
 'Четыре регулярных TechLabs курса с явно указанными EN / DE, включая два Competition Labs.',
 [cat('Junior Robotics','7–9','Учебная группа','VEX GO / Scratch','Basel Academia, лист ожидания'),cat('IQ Competition Labs','9–14','Клубная команда; турнирный состав по event rules','VEX IQ','Basel / Zürich; местная команда и национальный gate отдельно')],
 ['C549','L328','L329','L330','L331','E163'],'Проба уровня → регулярная команда → подтверждение Swiss-team eligibility → Alpine IQ 6 февраля; 6–7 февраля общая семейная V5/IQ programme.',
 ['Оскар 6 не подходит ни одному из четырёх новых курсов.','Запись на курс не гарантирует турнир и world quota.'],['Для семьи доступно посещение; competitors и visitors имеют разные условия.','Заголовки двух курсов ошибочно говорят February 2026; даты занятий 2026/27.'],[('Host: Alpine and courses',vex),('Basel competition course',vu['vexclass2']),('Zürich competition course',vu['vexclass3'])],age_tags=('9','10-12','teen'))
profile('bebras-europe-three','Bebras / Castor · три страны, разные классы и языки','regional','CHE с 3-го года; EHU с 3º Primary; CAT с 1º; FRA с CM1',
 'Вычислительное мышление через школьного координатора; локальные порталы нельзя считать одной возрастной системой.',
 [cat('Switzerland','3–13 школьный год','Индивидуально / пара по coordinator','Онлайн, 40 минут','Язык и зарубежная школа уточняются'),cat('EHU Spain','3º/4º Primary и выше','Через учителя','ES / EN / EU / CA, 45–50 минут','С 9 ноября, конец окна неизвестен'),cat('CAT Arrel / Branca','1º/2º; 3º/4º Primary','Solo или до 4','Младшие задачи, язык EN/ES не установлен','CAT не заявляет соревновательный характер'),cat('France Castor','CM1–Terminale','Solo / пара','45 минут','CM1 обязателен; EN national entry не подтверждён')],
 ['C1050','C1051','C1052','C1053','C1056'],'Школьный класс → национальный portal / language → teacher coordinator → задачи и личный прогресс.',
 ['Возраст 9 не заменяет класс; CAT 6–8 не перенесён в EHU English.'],['Результат / диплом не равен мировому robotic championship.','Кнопка English на platform не доказывает foreign national eligibility.'],[('Swiss age / school year',biber),('Swiss 2026',biber26),('EHU categories and languages',eh),('CAT early Primary',bc),('France 2026',castor)],age_tags=('6','9','10-12','teen'))
profile('robocampeones-spain','RoboCampeones · региональный школьный путь','regional','Primaria; exact minimum и новый регламент уточняются',
 'Maqueen / Nezha Soccerbot школьных центров; дополнительный турнир, не доказанный мировой отбор.',
 [cat('Soccerbot Maqueen / Nezha','Primaria','Школьная команда по правилам нового сезона','Раздельные платформы Código Escuela 4.0','Школа / учитель; независимый и иностранный приём неизвестен')],
 ['C1054'],'Школьный клуб → актуальный регламент и teacher registration → местный этап → собственный technical report.',
 ['Будущий 2027 calendar не объявлен.'],['65 центров и дата 29 апреля относятся к прошедшему 2026.','Национальный / мировой слот не установлен.'],[('Organiser latest',rc)])
profile('robolympics-switzerland','RobOlympics OST · старшая школьная ступень','regional','Обычно с 7-го школьного года; младшим требуется исключение',
 'Школьный автономный турнир LEGO / Open Class; для 6/9 соревнование только после специального разрешения.',
 [cat('LEGO / Open','7-й школьный год и старше; разрешённые исключения','Max 7: руководитель + до 6','Autonomous LEGO / Open hardware по дисциплине','Письменная уступка возрасту, новый регистрационный слот')],
 ['C1055'],'Сейчас бесплатный зрительский визит → возрастная подготовка → собственная школьная команда → турнир.',
 ['Mentor не пишет код и не решает задачи вместо детей.'],['Не мировой отбор по прочитанным правилам.','Визит зрителя не требует того же возраста, что участие.'],[('OST tournament / free spectators',robo),('General Rules 2026',roborules)],age_tags=('10-12','teen'))

newschools=[]
def school(id,name,iso,country,city,ages,lang,program,labs,sources,cost='Текущие tuition / extras / places не установлены',school_type='private',ib=True,results=()):
 s=dict(id=id,name=name,iso=iso,country=country,region='Европа',city=city,school_type=school_type,curriculum='IB PYP по сообщению школы; авторизацию и кампус проверить' if ib else 'Государственная Primaria / Infantil, двуязычная программа',ib_programmes=[dict(programme='PYP',status='school_report')] if ib else [],ages=ages,
 instruction_languages=lang,language_note='English — основной школьный язык; дополнительные языки и язык роботокоманды отдельно' if lang==['EN'] else 'Primary: не менее трети программы на English; математика / испанский на ES, предметное распределение по классам отдельно.',
 fit=dict(mat='candidate',osc='candidate',note='Оба кандидаты начальной ступени; точный класс, места и junior team не установлены.'),boarding='unknown',boarding_note='Младший пансион на этом кампусе не подтверждён; проживание семьи отдельно.',programme=program,labs=labs,ai='Младшая непрерывная AI programme и часы самостоятельной работы не установлены.',results=list(results),evidence='other_result' if results else 'programme',
 admissions='Уточнить placement, документы, доступные места и условия пробного посещения; опубликованный сайт не подтверждает приём.',cost=cost,
 questions=['Какой текущий junior team code, наставник, часы инженерной практики и результаты за 3–5 лет?', 'Как определят класс обоим и можно ли сначала проверить уровень группы?', 'Каковы полный годовой бюджет, язык команды и национальный путь к отбору?'],
 sources=[dict(title=t,url=u,claim=c,kind='public_school' if school_type=='public' else 'school',checked=CHECKED) for t,u,c in sources],checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны первичные источники. Программа, место в школе и награда конкретной возрастной команды рассматриваются отдельно.')
 newschools.append(s);return s
iszl='https://www.iszl.ch/';iszlen='https://www.iszl.ch/news-events/news/embracing-languages-multilingualism-in-the-early-years/'
s=school('S033','International School of Zug and Luzern · Zug / Baar','CHE','Швейцария','Baar · Zug Campus','Primary 3–11; Grades 1–5', ['EN'],
 'Ideas Hub Innovation Lab — robotics / coding / LEGO / 3D / creative engineering по школьному описанию. VEX Resilience Robotics и Swiss Schools Championship связаны с Middle / High: активная команда для 6/9 отдельно не установлена.',
 'Innovation Lab и maker projects; доступ младших к соревновательной VEX-команде требует проверки.',
 [('Primary curriculum',iszl+'primary-school/academic/','PYP / English support / curriculum'),('English instruction',iszlen,'English назван основным языком школы'),('Ideas Hub and robotics',iszl+'support-iszl/support-us/','Innovation Lab / Resilience Robotics; школа сообщает программу, не мировой титул'),('Current fees',iszl+'admissions/fees/','2026/27 tuition / registration Grades 1–5'),('Admissions process',iszl+'admissions/admissions-process/','Placement / текущая заявка')],
 '2026/27 Grades 1–5: CHF 33 200/ребёнок/год + CHF 5 000 однократно. Если оба в Grades 1–5: CHF 66 400/год, первый год CHF 76 400 до lunch / transport / extras. Это расчёт по тарифу, не индивидуальный счёт.')
ecol='https://www.ecolint.ch/en/campus-des-nations/primary-school';eca='https://www.ecolint.ch/fr/file-download/download/public/2886'
s=school('S034','Ecolint · Campus des Nations Primary','CHE','Швейцария','Geneva · Pregny / Saconnex','Primary 3–11; campus placement по year group',['EN'],
 'PYP, primary instruction преимущественно English, сильный French. Общий каталог ECA включает Tiny Robotics / LEGO / Tech Lab / Junior Maker Space; каталог отдельно предупреждает о различиях по кампусам и возрастам. Нельзя гарантировать наличие каждого клуба в Nations для 6/9.',
 'STEM / maker и tech clubs по общему каталогу; расписание, оборудование и участие Nations уточняются.',
 [('Nations Primary',ecol,'3–11, преимущественно EN и French, PYP'),('School ECA catalogue',eca,'Технологические кружки; доступ зависит от кампуса и года')])
s['language_note']='Primary predominantly English, strong French прямо на странице Nations. Язык конкретного robotics club ещё уточняется.'
lor='https://www.lorcaboadilla.es/';lr=lor+'wp-content/uploads/2026/03/No52.pdf'
lresult=dict(season='2026',league='FIRST LEGO League Challenge',stage='Final; точный региональный / национальный уровень не указан',award='Second Core Values Award',team='5º / 6º Primaria',team_id=None,source=lr,provenance='school_report',limit='Первый FLL сезон по школьному отчёту. Награда Values, не роботический мировой титул; уровень финала не установлен.')
s=school('S035','CEIP Federico García Lorca · Boadilla del Monte','ESP','Испания','Boadilla del Monte · Madrid','Infantil / Primaria; точное распределение детей по классам требуется',['ES','EN'],
 'Первый FLL сезон 2026: Explore для 2º и 3º/4º, Challenge для 5º/6º. Матвей — по фактическому классу, Оскар в 1º не получает автоматический вход в школьную Explore-группу 2º.',
 'Школьные команды FLL; часы работы / kit / наставник нового сезона отдельно.',
 [('Bilingual education',lor+'planes-y-proyectos/educacion-bilingue/','Не менее трети Primary на EN; предметное распределение'),('School March 2026 newsletter',lr,'Первый FLL сезон, школьные группы и Second Values Award'),('School official',lor,'Государственная школа и собственные проекты')],
 'Государственная школа; стоимость lunches / clubs / supplies и местные правила уточняются.',school_type='public',ib=False,results=[lresult])
s['admissions']='Государственный приём через действующую школьную процедуру / адрес / наличие мест; гражданство другой страны или туристический приезд не подтверждают школьный слот.'
isn='https://www.isn-nice.com/';ir=isn+'news-and-events/news/news-details/~board/posts/post/isn-robotics-team-wins-first-place-at-globeducate-france-challenge'
iresult=dict(season='2024',league='Globeducate France Robotics Challenge',stage='France · закрытая школьная сеть · High School category',award='First place · High School category',team='Четыре ученика Grade 9',team_id=None,source=ir,provenance='school_report',limit='29 мая 2024 школьный отчёт: Python и robots, Grade 9. Это победа сетевого французского этапа, не мировой титул и не результат Primary.')
s=school('S036','International School of Nice','FRA','Франция','Nice','Primary 3–11; Grades 1–5',['EN'],
 'English primary PYP с French. Подтверждён школьный рассказ о победе Grade 9 в Globeducate France Robotics 2024. Непрерывная соревновательная robotics-команда Primary для 6/9 ещё не установлена.',
 'Robotics / Python у проверенной Grade 9 команды; доступность оборудования и клуба Primary отдельно.',
 [('Current Primary',isn+'academic-life/primary-school','3–11, PYP, EAL support'),('Current FAQ',isn+'admissions/faq','English instruction / French / school admission'),('School robotics result',ir,'First High School category, Grade 9, France school network 2024')],results=[iresult])
s['language_note']='English — язык школьного обучения; все изучают French. Primary EAL при необходимости за дополнительную плату. На странице Primary 3–11, FAQ указывает старую рамку 4–10: placement уточнить.'
d['schools'].extend(newschools)
for schoolid,year,league,category,stage,award,level,url,team,note in [
 ('S035',2026,'FIRST LEGO League','Challenge · Core Values · 5º/6º Primaria','Final; уровень не указан','Second Core Values Award','unresolved_stage',lr,'5º / 6º Primaria','Школьный отчёт о первом FLL сезоне; уровень финала не установлен, не мировой титул.'),
 ('S036',2024,'Globeducate Robotics','High School category · Grade 9','France school-network challenge','First place · High School category','network_match',ir,'Четыре ученика Grade 9','По сообщению школы; закрытая школьная сеть во Франции, не мировой финал и не результат Primary.')]:
 s=next(x for x in newschools if x['id']==schoolid)
 d['school_history']['entities'].append(dict(id=schoolid,name=s['name'],kind='school',country=s['country'],age='primary' if schoolid=='S035' else 'secondary',school_id=schoolid,note='Школа сообщила конкретную награду; уровень и возраст команды указаны в строке результата.'))
 d['school_history']['results'].append(dict(id='H'+str(len(d['school_history']['results'])+1),entity_id=schoolid,year=year,league=league,category=category,stage=stage,award=award,level=level,source=url,provenance='school_report',team=team,team_id=None,note=note,checked=CHECKED))
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
f=d['europe_focus'];f.update(version=38,checked=CHECKED,status='partial',heading='Швейцария, Испания, Франция. Свой путь каждому ребёнку.',
 conclusion='Испания — первый европейский кандидат для постоянной команды обоих на доступном семейном языке. Швейцария даёт конкретную EN/DE VEX IQ подготовку Матвею, но Оскару нужна младшая отдельная группа и бюджет выше. Франция — EN школы и двуязычные каникулы с отдельной проверкой языка соревновательной команды.',
 limitations='Четвёртый ограниченный проход. Три страны остаются частично исследованными; подтверждение места, класса, EN судейства, национальной квоты, будущих летних смен и полных 5–10-летних протоколов ещё требуется. 38 новых карточек включают 2 будущие глобальные программы, 8 смен одного французского оператора и regular / past-program candidates: это не 38 независимых турниров.')
bycountry={c['iso']:c for c in f['countries']}
for iso,ids,ss,pp in [('CHE',['C1050','C1055','L328','L329','L330','L331','E163'],['S033','S034'],['vex-switzerland-junior','robolympics-switzerland','bebras-europe-three']),('ESP',['C1051','C1052','C1053','C1054']+['L'+str(i) for i in range(332,339)]+['E164','E165','E168'],['S035'],['bebras-europe-three','robocampeones-spain']),('FRA',['C1056']+['L'+str(i) for i in range(339,351)]+['E166','E167'],['S036'],['bebras-europe-three'])]:
 c=bycountry[iso];c['event_ids'].extend(ids);c['school_ids'].extend(ss);c['profile_ids'].extend(pp)
c=bycountry['CHE'];c.update(mat=c['mat']+' TechLabs IQ competition 9–14 в Basel / Zürich на EN/DE — конкретная подготовка; team nationality gate отдельно.',osc=c['osc']+' Новые TechLabs regular начинаются с 7 или 9: шестилетнему не подходят.',
 school=c['school']+' ISZL Zug / Baar и Ecolint Nations добавлены по primary / maker programmes. У ISZL подтверждённая VEX-связь Middle/High, у Nations общий ECA каталог не гарантирует младший club.',
 budget=c['budget']+' TechLabs regular CHF 648 / 720 / 769 за опубликованные циклы 2026/27. ISZL: если оба Grades 1–5, CHF 66 400/год tuition и CHF 10 000 разовых registration до extras.',
 results_check=c['results_check']+' У новых ISZL / Nations мировой результат младшей команды не установлен.')
c=bycountry['ESP'];c.update(camp=c['camp']+' Logix5 предлагает regular 5+ и пробные пакеты; язык технической группы уточнить. La Miranda даёт весь English day, но robotics смешана с спортом / multimedia. Nube7 EN — способность учителя, не полный EN поток.',
 school=c['school']+' CEIP Federico García Lorca — государственная двуязычная Primary, первый FLL сезон 2026; 2-е Values Award на финале без установленного уровня.',
 risk=c['risk']+' Bebras EHU с 3º/4º имеет ES/EN; CAT Arrel с 1º/2º не подтверждает EN/ES и не заявляет соревновательный характер. La Miranda Junior 2026 не включает рождение 2020.',
 city_route=c['city_route']+' Madrid — проба Logix5 и школьной команды; Santiago 27 ноября — семейная ярмарка 17:00–19:00. Valencia — maker-кандидат, новый набор неизвестен.')
c=bycountry['FRA'];c.update(camp=c['camp']+' Kids Robots публикует 8 Mini-смен 9–12 на 2026/27, но EN/ES не подтверждены. Algora Robot Run 6–9 / 9–14 22–24 февраля подходит по диапазону; AI 19–21 апреля имеет конфликт 9–16 / 14+.',
 school=c['school']+' ISN Nice — EN primary PYP 3–11. Победа относится к Grade 9 и французской сети Globeducate, не к мировому турниру младшей школы.',
 risk=c['risk']+' Castor требует CM1. Kids / Algora не названы подходящими EN лагерями до подтверждения языка. Paris Air Show family tickets не дают семье весь trade week.',
 results_check=c['results_check']+' ISN 2024: First High School category, школьный рассказ о 4 учениках Grade 9; не основание считать Primary мировой командой.')
f['shortlist']=[dict(title='Испания · команда для обоих и короткая проба',detail='Матвей: WRO Elementary. Оскар: RoboBasic. Madrid Logix5 5+ позволяет проверить уровень без длинного лагеря, но язык и наличие соревновательного наставника ещё уточнить. Santiago 27 ноября 17:00–19:00 — семейная ярмарка.',event_ids=['C910','C911','L336','E164']),
 dict(title='Швейцария · Матвею VEX IQ, Оскару младшая группа',detail='В Базеле и Цюрихе Competition Labs 9–14 ведутся на EN/DE. Оскар ниже минимума новых курсов; ему WRO Starter или ранее найденный Ecolint Introduction. 6–7 февраля Alpine приглашает семьи; участникам нужна швейцарская команда.',event_ids=['L330','L331','C906','L296','E163']),
 dict(title='Франция · английская школа и двуязычные каникулы',detail='Для обоих — ранее проверенный ABI Haunted 26–30 октября. Регулярные занятия Union на английском позволяют попробовать обучение. У Kids / Algora есть новые даты, но EN/ES не подтверждены; англоязычный поток нужно согласовать.',event_ids=['L230','L300','L301','L348','L349'])]
for st in f['steps']:
 if st['title'].startswith('2027–2029'):st['detail']='Матвею: WRO Elementary / автономный робот и VEX IQ после подтверждения местной команды. Оскару: RoboBasic → Elementary с 8 лет по национальным правилам. FLL заканчивается 2026/27; с 2027/28 выбрать LEGO League или новую FIRST K–8 отдельно, с разными hardware plans на 2028/29. Добавить Python, механику, журнал экспериментов и собственный продукт; 1–2 лиги для глубины.'
f['steps'].append(dict(title='Переезд · проверить школу и команду на практике',detail='Сначала 2–4 пробных недели и один наставник для каждого ребёнка. Проверить фактические часы конструирования / кода, team code и протокол возраста, сложность для трёхлетнего опыта, язык технической защиты и полный годовой бюджет. Лаборатория / IB сами по себе не доказывают мировое лидерство.'))
sources=[]
for e in new:sources.extend([(e['source'],e['title'])]+[(r['url'],r['label']) for r in e['references']])
for s in newschools:sources.extend((r['url'],r['title']) for r in s['sources'])
for p in profiles:sources.extend((r['url'],r['title']) for r in p['sources'])
known={s['url'] for s in d['sources']};focusknown={s['url'] for s in f['sources']}
for u,t in sources:
 if u not in known:d['sources'].append(dict(url=u,title=t,checked=CHECKED,evidence='Прочитан первичный источник; исторический выпуск и неизвестные будущие условия отмечены.'));known.add(u)
 if u not in focusknown:f['sources'].append(dict(title=t,url=u,checked=CHECKED));focusknown.add(u)
issues=[('Bebras portal differences','EHU five categories starts 3º/4º, ES/EN. CAT six categories starts 1º/2º, EN/ES early category unconfirmed. Swiss grade3 and France CM1 remain separate.',eh),
 ('FLL future hardware split','Final BIOGLOW2026/27. LEGO League separate2027/28, CS&AIelectronics2028/29. FIRST plans SPIKEcompatibility through2028/29. No future local tournament date created.',lego),
 ('Source age conflicts','La Miranda Junior2026 lists2017–19; Oscar2020 not automatically accepted. Teens9–12heading vs10–12body. AlgoraAI9–16heading vs14+tag. ISNPrimary3–11 vsFAQ4–10.',mir),
 ('Past camps and language','Nube7teacher ES/EN is support. LaMiranda robotics is part of mixed day. Robotix / Logix5 / Granada current technical language unknown; past2026summer dates not2027.',nube),
 ('French dated camps','Kids / Algora future dates read; EN/ES not established, P4 excludes from familyICS. KidsOct26–30full not marketed as available.',kids),
 ('Swiss course title date conflict','Two Competition Labs titles say February2026; session tables2026/27 control. Regular cycles not continuous residential camps.',vu['vexclass2']),
 ('School award attribution','Lorca firstFLLseason2026,secondValues award at unspecified final. ISNNice Grade9 wins closed France network2024. Neither is Primary world champion or 10year school leader.',lr),
 ('Family visitor windows','ERWNov27only17–19currentInstitutoPolitécnico. Alpinefamily6–7Feb separateIQqualification6Feb. SIAEJun14–20overall,datedpublicticketwindow unknown;trade showchildren unconfirmed.',her)]
a=d['completeness_audit'];a['validation_previous']=a['validation'];a.update(version=38,checked=CHECKED,status='partial',scope='CHE / ESP / FRA: младшие школьные маршруты, EN camps versus support, даты 2026/27, primary schools and exact award levels',
 conclusion='38 новые карточки:9 соревнований / будущих программ,23 учебные карточки,6 событий.6 профилей,4 школы,2 точно ограниченных школьных результата.171 страновая карточка CHE/ESP/FRA; мировой охват частичный.',new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=[],updated_profile_ids=[],new_school_ids=[s['id'] for s in newschools],validation=dict(version=38,status='pending',publication='pending'))
a['caveats'].append('v38: 38 карточек ≠38 независимых международных мероприятий.8 дат Mini-Robots — смены одного оператора; 2 глобальных будущих programmes не подтверждают локальный отбор. Ни одна новая школа не объявлена мировым лидером по программе / локальной награде.')
a['source_issues'].extend(dict(name=n,status=t,official_alternative=u,checked=CHECKED) for n,t,u in issues)
d['camp_focus']['validation_previous']=d['camp_focus']['validation'];d['camp_focus'].update(version=38,checked=CHECKED,carried_forward_ids=d['camp_focus']['added_ids'],added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=[],validation=dict(version=38,status='pending'),conclusion='350 лагерных / учебных карточек. 23 новых CHE/ESP/FRA: 5 regular, 8 датированных смен одного French operator, другие workshops / past-program candidates. TechLabs EN/DE подтверждён, Nube7 только поддержка; French EN неизвестен.')
d['camp_focus']['routes'].append(dict(name='CHE / ESP / FRA · глубже, с реальным языком',ids=['L330','L331','L332','L334','L336','L339','L348','L349','L350'],detail='Swiss IQ9–14 EN/DE дляМатвея. Spain LaMiranda Englishmixedcamp ageconflicts;Logix5regular5+ technical language unknown. French RobotRun6–9 /9–14 hasFeb2027dates but Englishnotconfirmed;AIminageconflict.'))
d['school_focus'].update(version=38,checked=CHECKED,conclusion='36 школьных досье. ISZL / Ecolint Nations / CEIP Lorca / ISN Nice добавлены по primary curriculum и робототехническим программам. Новые награды имеют школьное происхождение и ограниченный уровень; младший мировой лидер не доказан.')
d['school_focus']['routes'].append(dict(name='CHE / ESP / FRA · начальная школа и отдельный team gate',ids=['S033','S034','S035','S036'],detail='ISZL, Nations и Nice — кандидаты для английского школьного обучения. Lorca — государственная двуязычная Primary с новой FLL-командой. Школьное место, младшая команда и национальная квота требуют отдельных подтверждений; проверить класс и действующего наставника.'))
d['school_history'].update(version=38,checked=CHECKED,conclusion=d['school_history']['conclusion']+' v38:2 новых school_report строки — LorcaValues2026 с неустановленным уровнем финала, ISNNiceGrade9/FranceNetwork2024. Полных10летних протоколов новых школ нет.')
d['expansion_log'].append(dict(version=38,checked=CHECKED,added=len(new),updated_ids=[],note='Fourth CHE/ESP/FRA pass: actual junior entry, programme transition, camp language roles, four primary school dossiers, two bounded school awards.'))
assert len(new)==38 and len(profiles)==6 and len(d['schools'])==36 and len(d['school_history']['results'])==118
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
used={u for u,t in sources};receipts=[]
for fpath in sorted((W/'sources-europe-deep-v38').glob('receipt*.json')):
 for r in json.loads(fpath.read_text()):
  if r['url'] in used:receipts.append({k:r[k] for k in ['name','url','status','mime','bytes','sha256','error','resolved'] if k in r})
(ROOT/'data/europe-deep-source-receipts-v38.json').write_text(json.dumps(dict(checked=CHECKED,method='Primary HTML/PDF read; raw downloads outside repository. Programme dates / languages / school reports scoped separately.',sources=receipts,web_read_primary=[dict(url=iszlen,claim='English main language of instruction'),dict(url=isn+'admissions/faq',claim='English instruction / French / FAQ age conflict')]),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v38.json')
evidence=dict(global_competitions='v38:1055 competition / programme cards,120 profiles; world coverage partial',camps='v38:350 camp / regular / workshop / future candidates; technical teaching language separated from support',exhibitions='v38:168 event cards; public / trade / adult and exact family dates separated',unified_database='v38:1573 records from catalog.json in web / JSON / CSV / SQLite;120 profiles,36 schools,118 bounded historical results',permanent_schools='v38:36 school dossiers,4 new CHE/ESP/FRA primary candidates; school seats / junior teams / world quota unconfirmed',school_retrospective='v38:118 bounded results;2 school reports added with exact category and unresolved / school-network stage')
for q in r['requirements']:
 if q['id'] in evidence:q['evidence']=evidence[q['id']]
r.setdefault('research_passes',[]).append(dict(version=38,checked=CHECKED,scope='Fourth CHE/ESP/FRA pass',added_records=38,new_profiles=6,new_schools=4,new_school_results=2,status='partial',remaining='Localcalendar and ENjudging / foreignquota;2027summer confirmations;5–10yearschoolprotocols;rest ofworld'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=38,status='local_checks_pending_publication_pending');rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=38,added=len(new),profiles=len(profiles),schools_added=4,history_added=2,world_complete=False)))
