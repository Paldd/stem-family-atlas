"""Evidence-led Switzerland / Spain / France pass; retain the world inventory."""
import ast, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1260 and d['completeness_audit']['version']==29
CHECKED='2026-10-01';new=[];profiles=[];byid={e['id']:e for e in d['events']}
# Reuse only pure helpers, never execute a previous migration.
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['ref','event','profile']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base_event=event
def add(*args,**kwargs):
 e=base_event(*args,**kwargs);e['region']='Европа';return e
CONDITIONAL='Условно: возраст подходит; язык, иностранный допуск и место подтвердить'
NO_YOUNG='Нет: младше опубликованного минимального возраста'

# Swiss learning: published 2027 tables are separated from ambiguous rows.
hel='https://www.helveticinstitute.ch/robotics-ai-and-coding/'
hel_overview='https://www.helveticinstitute.ch/kids-camps/'
for id,season,start,finish,age,hours,cost in [
 ('L217','Winter · 6–9','2027-01-06','2027-04-14','6–9 лет','16:30–18:00','CHF650 + CHF75 materials'),
 ('L218','Winter · 9+','2027-01-06','2027-04-14','9+ лет','14:45–16:15','CHF650 + CHF75 materials'),
 ('L219','Spring · 6–9','2027-05-05','2027-06-30','6–9 лет','16:30–18:00','CHF450 + CHF75 materials'),
 ('L220','Spring · 9+','2027-05-05','2027-06-30','9+ лет','14:45–16:15','CHF450 + CHF75 materials')]:
 e=add(id,'Helvetic Institute · Robotics / AI / Coding · '+season,'Швейцария','Zug · точный учебный адрес подтвердить',hel,age,
  CONDITIONAL,NO_YOUNG if '9+' in age else CONDITIONAL,
  'Запись на еженедельный курс, не каникулярную смену. Подтвердить язык технического преподавателя и учебный календарь.',
  'LEGO robotics, coding, AI в названии курса; конкретный уровень AI для возраста уточнить.',
  block='Лагеря',start=start,participation='day_camp',cost=cost,evidence='program',date_scope='activity_start',themes=('robotics','coding','ai'),
  note='Таблица оператора 2027: занятия по средам '+hours+'. В календарь вынесено только начало курса; весь период не изображён непрерывным лагерем. Язык English / German / bilingual описан для общего лагеря, но не доказан для этой robotics-группы. В общем intro указано 7+, в таблице младшей группы 6–9 — Оскару нужно прямое подтверждение.')
 e.update(participation='regular',format='Регулярный курс по средам; проживание семьи отдельно',period=f'{start} — {finish}; среды {hours}, Europe/Zurich',references=[ref('Обзор языковых вариантов: не доказательство EN robotics',hel_overview)])
summer=[('L221','Zug','2027-07-05','2027-07-09'),('L222','Zug','2027-07-13','2027-07-16'),('L223','Zug','2027-08-09','2027-08-13'),('L224','Zürich · Römerhof','2027-07-19','2027-07-23'),('L225','Zürich · Römerhof','2027-07-26','2027-07-30'),('L226','Zürich · Römerhof','2027-08-16','2027-08-20')]
for id,city,start,end in summer:
 bad=id=='L222'
 e=add(id,'Helvetic Institute · Robotics Summer 2027 · '+city+' · '+start[5:],'Швейцария',city,hel,
  '4–12 лет в summer table; общий intro курса 7+ — младшую группу подтвердить',CONDITIONAL,CONDITIONAL,
  'Дневная смена; выбрать именно Robotics & Coding и подтвердить язык, возрастной поток и даты письменно.',
  'Robotics / coding hands-on; точную платформу и сложность проверить.',block='Лагеря',start='' if bad else start,end='' if bad else end,
  participation='day_camp',cost='CHF730 / опубликованная неделя; питание и материалы уточнить.',evidence='program',date_scope='camp_window',
  note='09:00–16:00. На robotics-странице таблица подписана Summer2027, рядом сохраняется «dates coming soon»; общий camps overview ещё содержит Summer2026. EN / DE / bilingual доступны в общем лагере, но язык выбранной robotics-группы не подтверждён. Это смены одного оператора, не отдельные международные лагеря.'+(' Строка 13–16 июля2027 названа Monday–Friday, хотя это вторник–пятница. Дата не признана подтверждённой и не экспортируется в календарь.' if bad else ''))
 e['references']=[ref('Общий camp overview с прежним годом и языковыми опциями',hel_overview)]
 if bad:e.update(period='В таблице: 13–16 июля2027; weekday / длительность противоречат — уточнить',date_status='Уточнить')

# Spain: actual robotics in English, not just English lessons in a camp.
hes='https://www.hescamps.com/campamentos-12'
for id,day in [('L227',False),('L228',True)]:
 e=add(id,'NATUK / HES · Robotics in English · '+('Day Camp' if day else 'проживание в отеле'),'Испания','Esterri d’Àneu · Pirineos de Lleida',hes,
  '6–16 лет в описании Robotics camp; следующий набор / условия младшей группы уточнить',CONDITIONAL,CONDITIONAL,
  'Следующий набор после закрытого лета2026. '+('Day Camp рассчитан на жителей района; visiting family и доступ robotics afternoon подтвердить.' if day else 'Проверить hotel residential для6лет, rooming, supervision и реальный технический уровень.'),
  'Robotics afternoon на английском; утром отдельный выбранный camp / языковые занятия.',block='Лагеря',participation='day_camp',
  language='Оператор прямо называет robotics camp на английском; утренний модуль выбирается отдельно.',languages=('EN',),evidence='program',date_scope='camp_window',
  note='Прочитанные даты28июня–18июля относятся к2026 (Fechas2026 / каталог2026). Даты2027 не опубликованы и не перенесены из прошлого года. Residential и day — два формата одной программы, не два независимых лагеря.')
 e.update(language_mode='primary',participation='day_camp' if day else 'residential',format='Дневной camp, ночёвка семьи отдельно' if day else 'Residential · Hotel Trainera; возраст пансиона подтвердить',references=[ref('Day формат и местный resident scope' if day else 'Hotel Trainera: residential infrastructure','https://www.hescamps.com/campus-en-los-pirineos' if day else 'https://www.hescamps.com/campamentos-internacionales-en-los-pirineos')])

# France: the linked public forms identify the year, real price and languages.
abi='https://abischool.fr/holiday-workshops'
forms={
 'L229':'https://docs.google.com/forms/d/e/1FAIpQLSdAcSOgAQsU0mEoMJMjYEzOqPsGJ9OSDJ-m2jlrBdkm8dnbXQ/viewform?usp=header',
 'L230':'https://docs.google.com/forms/d/e/1FAIpQLSfQnlO-xclspypTx6a76X4ZOAWR7cQYj82XDeutOsS6RXZ77w/viewform',
 'L231':'https://docs.google.com/forms/d/e/1FAIpQLSdoq-85ALkX5NPPb-jpoGV1R7GUeEudrT3Vit63ZEIs2c_sOQ/viewform?usp=header'}
for id,name,start,end,age,gear,cost in [
 ('L229','Ocean Lab','2026-10-19','2026-10-23','5–12 в прежнем ABI workshop; возраст именно Ocean Lab в форме не указан','STEAM shared underwater research station; степень robotics / code уточнить','EUR490 / неделя; EUR110 / отдельный день. Early-bird450 до15сентября уже истёк.'),
 ('L230','Haunted STEAM Lab','2026-10-26','2026-10-30','Explorer5–8; Inventor9–12 — прямо в текущей форме','Общий проект haunted house: действующие электрические цепи, механизмы и код','EUR490 / неделя; EUR110 / день. Early-bird450 до22сентября уже истёк.'),
 ('L231','Winter Invention Lab','2026-12-21','2026-12-23','Возраст текущей смены не указан; прежний ABI workshop5–12 не заменяет допуск','Miniature Winter Village: действующие lights / mechanisms; robot contest не обещан','EUR300 /3дня; EUR270 до1декабря2026; EUR110 / отдельный день.')]:
 e=add(id,'ABI School Paris · '+name,'Франция','Paris17 ·12rueClaudePouillet',forms[id],age,CONDITIONAL,CONDITIONAL,
  'Дневной билингвальный workshop; запросить наличие мест и приём visiting child; возрастную группу согласовать.',gear,
  block='Лагеря',start=start,end=end,participation='day_camp',language='Прямо подтверждено bilingual English / French в форме конкретной смены.',languages=('EN','FR'),cost=cost,evidence='program',date_scope='camp_window',
  themes=('technology','coding') if id=='L230' else ('technology','science'),
  note='09:00–16:30 Europe/Paris; меньше10детей в группе; проживание семьи отдельно. Прочитана публичная форма, никаких данных семьи не отправлено. Учебный проект не является международной олимпиадной наградой.'+(' Обе возрастные дорожки опубликованы для этой конкретной смены.' if id=='L230' else ' Нижнюю возрастную границу этого потока нужно подтвердить.'))
 e.update(language_mode='bilingual',references=[ref('Организатор: holiday workshops',abi)])

tinker='https://fr.tinkerrobotlabs.com/stages-vacances'
for id,name,start,end in [('L232','программа для принимающих центров','',''),('L233','Winter2027 ·22–26февраля','2027-02-22','2027-02-26'),('L234','Winter2027 ·1–5марта','2027-03-01','2027-03-05'),('L235','Spring2027 ·26–30апреля','2027-04-26','2027-04-30')]:
 e=add(id,'Tinker Robot Labs · '+name,'Франция','Paris / Lille · конкретный принимающий центр не выбран',tinker,
  'Числовой возраст не опубликован; уровень Arduino и допуска младшей группы уточнить',
  'Условно: возраст / партнёрский центр / поток не установлены','Условно: возраст / партнёрский центр / поток не установлены',
  'B2B: оператор предлагает провести программу в образовательном / youth centre. Открытое семейное место и реальный адрес не опубликованы.',
  'Arduino, industrial robotics,3Dprinting; максимум20участников; полдня, Mon–Fri.',block='Лагеря',start=start,end=end,participation='day_camp',
  language='Оператор прямо предлагает delivery French / English / Spanish; язык и преподаватель согласуются с принимающим центром.',languages=('EN','ES','FR'),cost='EUR250 / participant с материалами в предложении центрам; семейный счёт не установлен.',
  priority='P4 — предложение центрам, семейная запись не подтверждена',evidence='program',date_scope='workshop_window',
  note='Даты обозначают доступные окна поставщика для заказчика-центра; не доказанное существование открытой смены. Autumn2026 sold out. Summer2027 table содержит2026внутри строк — летние даты не исправлены предположением. В семейный календарь предложения P4 не включены.')
 e.update(language_mode='primary',admission_kind='school',registration_status='Нет выбранного принимающего центра / открытой семейной регистрации.')

# Swiss national WRO: birth-year rules do not create a foreign world quota.
wros='https://wro.swiss/en/information-on/categories-and-age-groups/'
starter='https://wro.swiss/informationen/kategorien-und-altersklassen/wro-starter/'
swterms='https://wro.swiss/teilnahmebedingungen/'
for id,category,age,osc in [('C906','Starter','6–10; в2026 birth2016–2020',CONDITIONAL),('C907','RoboMission / Future Innovators Elementary','8–12; в2026 birth2014–2018',NO_YOUNG)]:
 e=add(id,'WRO Switzerland · '+category+' · следующий сезон','Швейцария','Региональный этап / Swiss final ещё не объявлен',starter if id=='C906' else wros,age,CONDITIONAL,osc,
  'Команда2–3детей и coach18+; календарь / birth table нового сезона и допуск иностранной семьи подтвердить у WRO Switzerland.',
  'Starter LEGO + picture blocks; Elementary автономный robot / robotics research project по категории.',scope='national',
  note='Прочитаны условия2026; регистрация до15марта2026 закрыта. Даты2027 не придуманы. Starter — бесплатный младший локальный путь, не заявленная квота на world final. Swiss world qualification на главной странице относится к RoboMission / Future Innovators, требует отдельного национального допуска.',cost='Starter курс и конкурс бесплатно по странице2026; будущие условия / Elementary взнос уточнить.',evidence='rules')
 e['references']=[ref('Возраст по году рождения: таблица2026',wros),ref('Team / coach / registration2026',swterms)]

fllch='https://www.first-lego-league.org/en/2026-27-season/bioglow'
for id,category,age,osc,url,cost,deadline in [
 ('C908','Explore','6–10; team2–6 + adult facilitator',CONDITIONAL,'https://www.first-lego-league.org/en/divisions/explore','EUR199 + EUR42 shipping CHE; robot дополнительно.',''),
 ('C909','Challenge · Founders Edition','9–16; team2–10 + adult mentor',NO_YOUNG,'https://www.first-lego-league.org/en/divisions/challenge','EUR344 + EUR42 shipping CHE; robot / travel дополнительно.','2026-10-31')]:
 e=add(id,'FIRST LEGO League Switzerland · BIOGLOW2026/27 · '+category,'Швейцария','Швейцарская площадка и конкретная дата уточняются',url,age,CONDITIONAL,osc,
  'School / club / library / private family team разрешены; выбрать Swiss location, проверить foreign registration и язык judging.',
  'Explore: SPIKEEssential / WeDo2.0; Challenge: SPIKEPrime / EV3 / NXT по division page.',scope='national',deadline=deadline,cost=cost,evidence='rules',
  note='Explore — showcase с признанием каждой команды; не общая таблица победителей Challenge. Challenge local→Swiss qualifier→DACH final; точные Swiss даты в динамической регистрации ещё не получены. Общая схема «grades1–4 /5–10» не заменяет прямое возрастное правило division page. International slots2026/27 ещё отдельно подтверждать.')
 e.update(admission_kind='open_application',references=[ref('BIOGLOW: 2редакции / сроки регистрации',fllch),ref('Текущие locations','https://www.first-lego-league.org/en/2026-27-season/locations')])
 if id=='C908':e['reward']='Признание / medal Explore; не победа в соревновательном Challenge'

# Spain explicitly has non-school teams, RoboBasic6+ and two FLL editions.
wroe='https://www.wroboto.es/competicion/'
for id,category,age,osc in [('C910','RoboBasic','6–12; возраст, который исполняется в календарном году',CONDITIONAL),('C911','RoboMission / Future Innovators Elementary','8–12; возраст по календарному году',NO_YOUNG)]:
 e=add(id,'WRO Spain · '+category+' · следующий местный этап','Испания','Турнир2027 / регион уточняются',wroe,age,CONDITIONAL,osc,
  '2–3участника и coach. FAQ разрешает независимые нешкольные команды. Проверить foreign eligibility и слот страны; выбрать локальный этап, предлагающий нужную категорию.',
  'RoboBasic — teledriven robot до25cm; Elementary — автономный robot / innovators project. Hardware свободный, кроме готовых compact robots.',scope='national',cost='EUR60 / team по participation page; hardware, lodging и international fee отдельно.',evidence='rules',
  note='Локальный→national→international только для соответствующей категории и национальной квоты. Не все местные турниры предлагают все категории. Закрытие местного приёма15дней до даты или раньше при заполнении; неизвестная дата не превращена в выдуманный дедлайн. RoboBasic не назван world-final category; инженерная практика младших отделена от мирового титула.')
 e['references']=[ref('RoboBasic6–12 / hardware','https://www.wroboto.es/robobasic/'),ref('FAQ: independent teams / deadlines','https://www.wroboto.es/faqs/'),ref('Текущий календарь содержит2026, не2027','https://www.wroboto.es/torneos/')]
flles='https://firstlegoleague.soy/inscripciones-bioglow/'
for id,category,age,team,gear,mat,osc,competitive in [
 ('C912','Explore · Founders','6–9','2–6','SPIKEEssential / WeDo',CONDITIONAL,CONDITIONAL,False),
 ('C913','Challenge · Founders','10–16','2–10','Classic educational robot + Challenge kit','Условно: 2017год достигает10в2027; возрастную контрольную дату сезона подтвердить',NO_YOUNG,True),
 ('C914','K5 · Future Edition','5–7','2–4','Новое LEGOComputationalThinking&AI5+',NO_YOUNG,CONDITIONAL,False),
 ('C915','K8 · Future Edition','8–16','4–10','2новых LEGOComputationalThinking&AI robots на команду',CONDITIONAL,NO_YOUNG,True)]:
 e=add(id,'FIRST LEGO League Spain · BIOGLOW2026/27 · '+category,'Испания','Local host / dates уточняются',flles,age+'лет; '+team+'участников',mat,osc,
  'Registration2026/27 у Ingeniera.soy; школы / академии / associations / independent groups. Подтвердить конкретный event, foreign admission и возрастную контрольную дату.',gear,
  scope='national',evidence='rules',note='В текущей регистрации две аппаратно разные редакции. K8 — конкурентная уже с8лет; это реальная возрастная альтернатива Матвею9лет. Она требует4–10детей и2новыхроботов, братьев вдвоём недостаточно. Explore / K5 не конкурентные. Discover на2026/27 прямо недоступен, несмотря на старую главную страницу. Classpack на общем сайте не даёт event slot; нужен правильный event registration.')
 e['references']=[ref('Classic ages / team / kit','https://firstlegoleague.soy/'+('explore/' if id=='C912' else 'challenge/'))]
 e['reward']='Конкурентный результат / judging awards конкретного этапа; международный отбор подтвердить' if competitive else 'Некомпетитивное признание проекта; не победа Challenge / K8'

fllfr='https://firstlegoleaguefrance.fr/lafllenquelquesmots'
e=add('C916','FIRST LEGO League France · BIOGLOW2026/27 · Founders / новый формат','Франция','Местный partenaire / следующий этап уточнить',fllfr,
 '9–16 на общей Challenge-page; возраст и оборудование Future Edition проверить отдельно',CONDITIONAL,NO_YOUNG,
 'WestSideRobotLab / местный partenaire; текущая регистрация открыта, но точные этапы, foreign team и English judging не установлены.',
 'Founders classic LEGOrobot и research; новая BIOGLOW FutureEdition имеет4роли и другое wirelesshardware.',scope='national',evidence='program',
 note='General Challenge page всё ещё описывает Mindstorms. Текущие ресурсы BIOGLOW отдельно содержат Future Edition и Founders; возраст9–16 нельзя автоматически переносить на новую редакцию. French resources подтверждены, EN интервью не доказано. Подходит Матвею по старому возрастному диапазону условно; Оскару этот Challenge пока рано.')
e['references']=[ref('BIOGLOWcurrent resources / hardware differences','https://firstlegoleaguefrance.fr/ressources/bioglow-saison/'),ref('Current registration / operator','https://firstlegoleaguefrance.fr/')]

junior='https://www.coupederobotique.fr/participer-a-la-coupe-junior/'
for id,region,city,date,url in [
 ('C917','AuvergneRhôneAlpes','Vaulx-en-Velin','2027-02-13','https://www.coupederobotique.fr/event/coupe-de-robotique-junior-rencontre-auvergne-rhone-alpes-2027/'),
 ('C918','Occitanie','Toulouse · Cité de l’espace','2027-03-27','https://www.coupederobotique.fr/event/coupe-de-france-de-robotique-junior-rencontre-occitanie-2027/'),
 ('C919','Île-de-France','Savigny-le-Temple · LeMillénaire','2027-04-17','https://www.coupederobotique.fr/event/coupe-de-france-de-robotique-junior-rencontre-ile-de-france-2027/'),
 ('C920','National Final','LaRoche-sur-Yon · точные Juniorдни уточняются','','https://www.coupederobotique.fr/calendrier/')]:
 e=add(id,'Coupe de France de Robotique Junior2027 · '+region,'Франция',city,url,
  '8–18 по current participation page; older presentation7–18 противоречит',CONDITIONAL,NO_YOUNG,
  'Команда через PlanèteSciences / местную delegation; national final после местного отбора. Foreign delegation, школьный статус и язык проверить.',
  'Дети строят robot filoguidé / управляемый по Juniorrules; обязательный presentationposter. Не путать с senior autonomous Eurobot.',start=date,scope='national',evidence='rules',
  cost='Structure membership EUR50; Juniorregistration бесплатно по прочитанной странице. Robot / trip отдельно.',
  note='Страницы смешивают2027calendar и старые2026registration/nationalfinal; закрытие31декабря2025 не перенесено на2027. Текущая participation-page8–18 приоритетнее старого описания7–18; Оскар6лет ниже обоих. Localpodium→national→EurobotJunior, новый internationalfinal не датирован.'+(' Общий фестиваль указан5–8мая2027, но конкретные Junior final дни не получены: start оставлен пустым.' if id=='C920' else ''))
 e['references']=[ref('Возраст / membership / routing и прежние дедлайны',junior),ref('Старое описание7–18: противоречие','https://www.coupederobotique.fr/levenement/la-coupe-junior/')]
 e['admission_kind']='qualifier' if id=='C920' else 'open_application'
 if id=='C920':e['period']='Общий фестиваль5–8мая2027; конкретные Juniorfinalдни / invitation уточнить'

# Professional exhibitions: no child admission inferred from youth marketing.
for id,title,country,city,source,start,end,tier,cost in [
 ('E140','Swiss Robotics Day2026','Швейцария','Zürich · StageOne','https://swissroboticsday.ch/','2026-11-13','2026-11-13','profile','CHF400 Seniorprofessionals>35; CHF250 Youngprofessionals<35; CHF100 PhD/MSc/BScstudent с studentcard. Детского тарифа не найдено.'),
 ('E141','Global Industrie Lyon2027','Франция','Lyon / Chassieu · Eurexpo','https://www.global-industrie.com/','2027-03-15','2027-03-18','global','Badge и условия organiser; childprice не подтверждён.'),
 ('E142','SIDO Lyon2027 · IoT / AI / Robotics / XR','Франция','Lyon / Chassieu · Eurexpo','https://www.sido-lyon.com/','2027-09-15','2027-09-16','regional','Professionalbadge / registration; childprice не подтверждён.')]:
 e=add(id,title,country,city,source,'Профессиональное событие; минимальный возраст visitor не установлен',
  'Условно:6/9 childentry не подтверждён','Условно:6/9 childentry не подтверждён',
  'Взрослый professionalregistration; до семейной поездки получить прямой ответ о6/9лет и сопровождающем.',
  'Expo компаний / университетов, технологии / demonstrations; не детская соревновательная заявка.',block='События',start=start,end=end,participation='visitor',scope='international' if tier=='global' else 'national',cost=cost,themes=('robotics','ai','technology'),
  note='Профиль / масштаб не означает присутствие всех мировых компаний. Опубликованный перечень экспонентов нужно проверить для конкретного года. Открытая professionalregistration и студенческая категория не доказывают вход детей6/9; семейная регистрация не сделана.')
 e.update(exhibition_tier=tier,visitor_policy='confirm_children',visitor_note='Детский допуск не найден в прочитанном актуальном источнике; уточнить до семейной поездки.',company_scope='Индустрия / research / technology; полный roster зависит от издания.')
 if id=='E140':e['references']=[ref('Прочитан professional / university-student tariff','https://swissroboticsday.ch/registration/')]
mwc=byid['E017'];mwc.update(start='2027-03-01',end='2027-03-04',date_status='Подтверждено',period='1–4марта2027 · FiraGranVia',checked=CHECKED,
 proof='MWC27 Location & Venue: exact1–4March; footer прямо подтверждает возвращение2027.',
 note=mwc['note']+' v30: даты1–4марта2027 проверены на текущей venue-page. Прежняя under16policy сохранена как последний прочитанный регламент; venue-page не заменяет проверку новых eventguidelines2027.')
mwc.setdefault('references',[]).append(ref('MWC27 venue / exact dates','https://www.mwcbarcelona.com/about/location-venue'))

# Four national path profiles, not four new global league brands.
profile('wro-switzerland','WRO Switzerland · Starter / Elementary','regional','Starter6–10; Elementary8–12; birth-year rules',
 'Для Оскара — Starter. Для Матвея — Elementary с национальным / мировым отбором после подтверждения допуска.',
 [dict(name='Starter',age='6–10',team='2–3 + coach18+',hardware='LEGO / blocks',age_rule='Таблица2026 birth2016–2020;2027подтвердить',entry='Startercourse/competition, free по2026page'),dict(name='Elementary',age='8–12',team='2–3 + coach18+',hardware='RoboMission / FutureInnovators',age_rule='Таблица2026 birth2014–2018;2027подтвердить',entry='Swissregional→national→worldquota отдельно')],
 ['C906','C907'],'Starter practice / local recognition → independent Elementary team → Swissqualifier only with nationaleligibility → internationalquota.',
 ['No one-child+adult team.','Birth-year—not birthday on event day.','Даты иforeigneligibility нового сезона пока неизвестны.'],
 ['Starter не заявлен как world-finalcategory.','Существование бесплатных beginnerworkshops не гарантирует нужный уровень детям с3годами опыта.'],
 [('Swissages2026',wros),('Startercourse/competition',starter),('Participationconditions',swterms)])
profile('wro-spain','WRO Spain · RoboBasic6+ / Elementary','regional','RoboBasic6–12; Elementary8–12',
 'Практичный семейный национальный маршрут с нешкольными командами; Elementary для Матвея и младшая ступень для Оскара.',
 [dict(name='RoboBasic',age='6–12',team='2–3 + coach',hardware='Teledriven;25cm; non-compact',age_rule='Возраст исполняется в calendar year',entry='Independentteamallowed; worldqualification этой категории не заявлена'),dict(name='Elementary',age='8–12',team='2–3 + coach',hardware='RoboMission autonomous / FutureInnovators',age_rule='Возраст исполняется в calendar year',entry='Выбрать localhost нужной категории;national/worldeligibility отдельно')],
 ['C910','C911'],'Independentteam + rightcategory → localtournament → nationalfinal → eligibleinternationalcategory/quota.',
 ['EUR60 excludesrobot/travel/internationalfee.','Localdeadline15дней доevent или раньшеприfullcapacity.','Foreigneligibility не установлена.'],
 ['Не каждый tournament предлагает всеcategories.','RoboBasic practice/result не назван мировой победой.'],[('Participation/age/hardware',wroe),('FAQindependentteam','https://www.wroboto.es/faqs/'),('RoboBasic','https://www.wroboto.es/robobasic/')])
profile('fll-europe-three','FIRST LEGO League · Switzerland / Spain / France','regional','Разные национальные возраста и2редакцииBIOGLOW',
 'Матвей: SwissChallenge9+ или SpanishK8 8+; Oscar: SwissExplore6–10 / SpanishExplore6–9 либоK5. FranceChallenge9+ с языковым барьером.',
 [dict(name='Spain Founders',age='Explore6–9 / Challenge10–16',team='Explore2–6 / Challenge2–10',hardware='ClassicSPIKE / WeDo versusChallengekit',age_rule='Seasoncutoffпроверить;2017неавтоматически10до2027',entry='Independentgroupsallowed;classpackнеeventslot'),dict(name='Spain Future',age='K5:5–7 / K8:8–16',team='K5:2–4 / K8:4–10',hardware='NewComputationalThinking&AI;K8needs2robots',age_rule='Current26/27registration—not genericoldhomepage',entry='K5noncompetitive / K8competitive;Discovernotavailable'),dict(name='SwissFounders',age='Explore6–10 / Challenge9–16',team='Explore2–6 / Challenge2–10',hardware='ClassicLEGOsets',age_rule='Gradeoverviewнеединственноеageправило',entry='Privatefamilysettingallowed;foreigngate+languageunknown'),dict(name='France',age='GeneralChallenge9–16;Futurecutoffнеполучен',team='Currentlocalrulesподтвердить',hardware='Founders/Futureпоразнымdocuments',age_rule='GeneralMindstormspageнепереноситсянаFuture',entry='Localpartner→national→international;ENjudgingнеподтверждено')],
 ['C908','C909','C912','C913','C914','C915','C916'],'Выбратьcountry + edition + hardware → correcteventregistration → teamproject/judging → qualifyingquota конкретнойcountry/edition.',
 ['Explore/K5 recognition≠competitivewin.','ИспанскаяK8 требуетминимум4детей;братьеввдвоёмнедостаточно.','SwissChallengedeadline31октября2026;Swisslocaldateunresolved.'],
 ['Futurehardware иFoundershardware не взаимозаменяемы.','ENwebsite≠ENjudging.','Международный слот нового сезона подтверждается отдельно.'],[('Spain26/27registration',flles),('SwissBIOGLOW',fllch),('SwissExplore','https://www.first-lego-league.org/en/divisions/explore'),('SwissChallenge','https://www.first-lego-league.org/en/divisions/challenge'),('Francecurrentresources','https://firstlegoleaguefrance.fr/ressources/bioglow-saison/')])
profile('eurobot-junior-fr','Coupe de France de Robotique Junior / Eurobot Junior','regional','8–18 на currententrypage;7–18 наolderpresentation',
 'Собственный управляемый робот, длинный инженерный проект и региональный отбор; подходящая возрастная ступень Матвею, Оскару рано.',
 [dict(name='Junior',age='Current8–18; conflict7–18resolve',team='Детская команда+принимающаяstructure / delegation',hardware='Robotfiloguidé;poster;annualrules',age_rule='Currententryminimum8;older7неиспользовандляadmission',entry='Localpodium→national→EurobotJunior;foreigndelegationunknown')],
 ['C917','C918','C919','C920'],'6–8месяцев собственногопроекта → localqualifier → nationalpodium → EurobotJunior поcurrentrules.',
 ['EUR50structuremembership;robot/travelдополнительно.','2027deadlineнеполучен;старый31Dec2025непереносить.','ENjudge/foreigndelegationпроверить.'],
 ['УправляемыйJunior отличаетсяотautonomousSeniorEurobot.','Общие5–8May2027непризнаныконкретнымиJuniorfinalднями.'],[('Currentparticipation',junior),('2027calendar','https://www.coupederobotique.fr/calendrier/'),('Presentationageconflict','https://www.coupederobotique.fr/levenement/la-coupe-junior/')],age_tags=('9','10-12','teen'))

# Schools: school-reported national awards are not organizer world results.
def school_source(title,url,claim):return dict(title=title,url=url,claim=claim,kind='school',checked=CHECKED)
basel='https://www.isbasel.ch/learn/overview/robotics'
baselworld='https://www.isbasel.ch/connect/news/news-post/~board/isb-public-news/post/isb-robotics-team-qualifies-for-vex-robotics-world-championship'
baselaward='https://www.isbasel.ch/connect/news/news-post/~board/isb-public-news/post/isb-robotics-teams-shine-at-alpine-robo-games-2026'
schools=[dict(id='S023',name='International School Basel',iso='CHE',country='Швейцария',region='Европа',city='Basel area · Aesch / Fiechten / Reinach',school_type='private',
 curriculum='English language not-for-profit International School; IBPYP/MYP/DP по сообщению школы.',ib_programmes=[dict(programme=p,status='school_report_authorized') for p in ['PYP','MYP','DP']],
 ages='3–18 school; roboticsJunior Grades3–5; VEXIQGrades7–8; VEXV5Senior; классы детей неизвестны.',instruction_languages=['EN'],language_note='ENschool прямо подтверждена; конкретного тренера и язык Juniorrobotics отдельно подтвердить.',
 fit=dict(mat='candidate',osc='candidate',note='Оба по возрасту могут быть schoolcandidates. ДляМатвея проверитьGrade3–5; Juniorrobotics нижеGrade3 не доказана, Оскаруteamentryнеобещан.'),boarding='unknown',boarding_note='Школа сообщает Junior/Middle/Senior; пансион не установлен. Планировать семейное проживание.',
 programme='JuniorGrades3–5:optionalpaidexternalrobotics; MiddleVEXIQcourse иcompetitiongroupпланируется; SeniorVEXV5team.',labs='LEGOintro/SPIKE иAI-enabledkitsJunior; VEXIQMiddle / VEXV5Senior.',ai='AI-enabledkitsвописанииJunior; полноценныйAIcurriculumдля6лет не доказан.',
 results=[dict(season='2026',league='VEXV5',stage='AlpineRoboGames · nationalqualifier',award='SigmaBots:4thoverall;2ndOffensivePowerRating;DesignNotebookAward. Limbo:InnovateAward.',source=baselaward,provenance='school_report',note='OPR2ndне2ndoverall; Grade11—notprimary.'),dict(season='2026',league='VEXV5',stage='WorldChampionshipqualification',award='Первый ISBteamqualifiedforWorlds; worldprizeнеустановлен.',source=baselworld,provenance='school_report',note='Qualification story написана доWorlds. Общаяroboticspageназываетnational2nd; конкретныйAlpineотчёт4thoverall/OPR2nd — не сведено в единое место.')],
 evidence='national_result',admissions='Rollingadmissionssubjecttospaceandentryrequirements; Englishassessment, gradeplacement, juniorrobotcoach/teamplaceподтвердить.',cost='Schoolfees иoptionalroboticsнужногогода не установлены; проверитьполнуюсмету.',
 questions=['CurrentGrade3–5 coach, hours/week, teamcode итриrecentseasonresults?','КакаяtechnicalgroupдоступнаОскару6лет?','Разрешитьnational2ndvs4thoverall/OPR2nd; получитьorganizerprotocol.'],sources=[school_source('Roboticsvertical / age / ENschool',basel,'Текущий programme поgrade; старшийteamнепереноситсянаjunior'),school_source('Alpine2026schoolreport',baselaward,'4thoverall,2ndOPR,DesignNotebook/Innovate'),school_source('Worldqualificationreport',baselworld,'ПервыйworldqualifierGrade11;worldawardнеподтверждён')]),
 dict(id='S024',name="St PETER’S School Barcelona",iso='ESP',country='Испания',region='Европа',city='Barcelona',school_type='private',
 curriculum='English IBContinuum; PYP/MYP/DP по сообщению школы;1–18.',ib_programmes=[dict(programme=p,status='school_report_authorized') for p in ['PYP','MYP','DP']],ages='1–18school; AfterSchoolHub2025/26RoboticsY1–Y2; VRY3–Y5. Текущий2026/27наборпроверить.',
 instruction_languages=['EN'],language_note='ENschoolпрямо заявлена; языкextracurricularrobotics отдельно не установлен.',fit=dict(mat='candidate',osc='candidate',note='Schoolageобоимподходитусловно. RoboticsY1–Y2вероятнеедляОскара; дляМатвеяY3–Y5впоследнемPDFтолькоVR. Currentcompetitionteamнеподтверждена.'),
 boarding='unknown',boarding_note='Residential/boardingнеустановлен; семьяживётотдельно.',programme='2025/26paidRoboticsY1–Y2. FLLRoboSparksclasses6/9 в2018 — historicalparticipation, неcurrentwinningteam.',labs='ThinkersHub:Robotics иVirtualReality; nurseryScienceLabвописаниишколы.',ai='SchoolAIpositioning—неподтверждение соревновательногоAIкурсамладших.',results=[],evidence='programme',
 admissions='Admissions/gradeplacement/ENassessment; отдельноroboticsY1–2agefit идействующуюкомандудля9лет.',cost='Robotics/VR EUR670/semester по2025/26HubPDF; schooltuition/2026/27неустановлены.',questions=['Какаяroboticsgroupдля2017годаестьв2026/27?','ЕстьлиcurrentFLLteamcode/mentor/results?','Currentcourseage/language/feeдля2020года?'],
 sources=[school_source('Schooloverview','https://stpeters.es/','EN,IBContinuum,1–18поschoolreport'),school_source('AfterSchoolHub2025/26PDF','https://stpeters.es/wp-content/uploads/2025/07/After-School-Hub-25-26.pdf','RoboticsY1–2,VRY3–5,EUR670/semester;не2026/27'),school_source('FLL2018RoboSparks','https://stpeters.es/first-lego-league/','Historicalparticipationclasses6/9;награданеобъявлена')]),
 dict(id='S025',name='ABI · Alliance Bilingual International School',iso='FRA',country='Франция',region='Европа',city='Paris17',school_type='private',curriculum='FR/ENbilingualpreschool/primary,ages2–12;STEAMholidayprojects. IBнеустановлен.',ib_programmes=[],ages='2–12school; HauntedSTEAMLab5–8/9–12.',instruction_languages=['EN','FR'],language_note='FR/ENschoolиFR/ENименноHauntedtechnicalworkshopпрямо подтверждены. EN-onlyschooldayнеобещан.',fit=dict(mat='candidate',osc='candidate',note='SchoolageиHauntedgroupsподходятобоимпоage;admission,assessment,placesнеподтверждены.'),boarding='unknown',boarding_note='Дневныеworkshops09–16:30;школьныйпансионнеустановлен.',programme='Билингвальнаяначальнаяшкола;currentholidaycircuits/mechanisms/code/sharedproject. Currentselectivecompetitionteamнеустановлена.',labs='STEAMprojectdelivery;переченьschoolrobotkits/labcapacityнеполучен.',ai='ВозрастнойAIcourseнеподтверждён.',results=[],evidence='programme',admissions='Welcomesexpatfamiliesпоschooloverview;admissionprocess/gradeplacement/FRsupportиteammentorподтвердить.',cost='Schooltuitionнеустановлена;camp490/week(Oct2026)неравенannualschooltuition.',questions=['Какова доляENвschooldayиroboticscourse?','ЕстьлиcurrentFLL/WROteam,registeredcodeиmentor?','Какподдерживают6/9летбезFR?'],sources=[school_source('Schoolages / expatriates','https://abischool.fr/','2–12,bilingualFR/EN;неleagueleaderproof'),school_source('Currentholidayworkshops',abi,'Техническиепроекты'),school_source('HauntedSTEAMLab2026form',forms['L230'],'5–8/9–12,circuits/code,EN/FR,dates/price')])]
for s in schools:s.update(checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны первичные programme / schoolreports; admissions и teamplace семьёй не подтверждены.')
d['schools'].extend(schools)
d['school_focus'].update(version=30,checked=CHECKED,conclusion='25школьныхдосье. v30:Basel,StPETER’SBarcelona,ABIParis; возрастjunior,язык и результатыteamразделены. Общего рейтинга лучших школмира не заявлено.')
d['school_focus']['routes'].append(dict(name='Европа · три разных младших пути',ids=['S023','S024','S025','S009','S010','S011'],detail='ISBasel:реальнаяgradevertical,старшиенациональныенаграды;StPETER’S:EN/IBноRoboticsPDFтолькоY1–2;ABI:FR/ENprimaryиcurrentSTEAMcamps,winningteamнепоказана. Aiglon/Ermitage/Brainsостаютсякандидатами,panсион и командыотдельно.'))
d['school_focus']['gaps'][0]='25школв15странах;249страни территорий. Полностьюпроаудированныхстранпошколам:0.'

# A dedicated public comparison keeps recommendations and evidence together.
f=dict(version=30,checked=CHECKED,status='partial',title='Швейцария, Испания, Франция · семейный STEM-маршрут',
 family='Матвей2017 / Оскар2020; английский / испанский для полного дня, русский также допустим. Точные классы и дни рождения неизвестны.',
 conclusion='Для европейской учебной базы первым проверял бы Испанию: языковой вход проще, есть независимые WROкоманды и реальные младшие/FutureFLLкатегории. Швейцарию — как ENшкольнуюбазу после проверкиjuniorcoachи полнойсметы. Францию — для конкретныхбилингвальныхканикул; постоянныйсоревновательныйпутьтребуетFRилипрямогоподтвержденияENкоманды.',
 limitations='Редакционная рекомендация по возрасту, языку и проверенным программам, не официальный рейтинг стран/школ. Места, admissions, foreignqualification, полный бюджет и все локальныеоператоры ещё не подтверждены.',
 countries=[dict(iso='ESP',name='Испания',verdict='Первый кандидат европейской базы',reason='ES уже доступен обоим;WROindependentteams,младшийRoboBasic6+ иFLLдвухредакций.',mat='WROElementary8–12;FLLFutureK8 8–16 уже подходитпоage. FoundersChallenge10–16 — cutoffна2027подтвердить.',osc='WRO RoboBasic6–12;FLLExplore6–9 либоK5 5–7. RecognitionExplore/K5 не конкурентнаяпобеда.',camp='NATUK/HESRoboticsнаEN,6–16;residential/day. Набор2027ещё не датирован.',school='BrainsLaMoraleja иStPETER’SBarcelona:проверитьcurrentjuniorrobotics/mentor,невыбирать поодномуIBлоготипу.',school_ids=['S011','S024'],event_ids=['C910','C911','C912','C913','C914','C915','L227','L228','E017'],profile_ids=['wro-spain','fll-europe-three'],risk='Независимаякоманда≠foreignworldquota. K8минимум4детей+2новыхробота;расходы и internationalrouteпроверить.'),
 dict(iso='CHE',name='Швейцария',verdict='Сильный ENшкольный кандидат с возрастными условиями',reason='SwissStarter6–10,Elementary8–12,FLLExplore6–10/Challenge9–16;Baselс конкретнойroboticsvertical.',mat='WROElementary / FLLChallenge9+. ВBaselJuniorroboticsGrades3–5;егоgradeplacement неизвестен.',osc='WROStarter6–10 / FLLExplore6–10. Schooladmission6лет не гарантируетjuniorroboticsдоGrade3.',camp='Helvetic2027опубликоваллетние/termтаблицы;ENroboticsнеподтверждён. С10летв2027можнорассмотретьBrillantmontTech,точный birthday/groupотдельно.',school='Basel:S023;Aiglon:S009. СтаршийVEXqualificationBaselнеявляетсямировойпобедоймладшего.',school_ids=['S023','S009'],event_ids=['C906','C907','C908','C909','L217','L221','L224','L222','L168','E140'],profile_ids=['wro-switzerland','fll-europe-three'],risk='Starterнеworldfinalquota;foreigneligibility/Swisslocaldatesunknown. ENroboticscamp и juniorclassпроверить. SRDprofessionalstudentticketнеchildticket.'),
 dict(iso='FRA',name='Франция',verdict='Конкретные билингвальные каникулы, школьный путь с языковой проверкой',reason='CurrentABIEnglish/FrenchSTEAM;PlanèteSciencesJunior2027qualifiers;FLLFrance9+поgeneralChallenge.',mat='CoupeJunior8–18:3qualifiers2027;FLLChallenge9+Foundersусловно;ENjudging/foreignteamнеподтверждены.',osc='ABIHauntedExplorer5–8. Juniorcompetitionminimum8;старое7–18тоже6летнепокрывает.',camp='ABI19–23/26–30Oct,21–23Dec2026. Haunted5–8/9–12прямо;возрастдругихпотоковподтвердить. TinkerEN/ES—B2Bчерезhostcentre.',school='ErmitageS010 + ABIS025:FR/ENprimary;нетдоказательствмировоголидерстваробокоманды. ПансионErmitage11+необа6/9.',school_ids=['S010','S025'],event_ids=['C916','C917','C918','C919','C920','L229','L230','L231','L233','E141','E142','E102','E104'],profile_ids=['fll-europe-three','eurobot-junior-fr'],risk='FRcompetitionlanguageнеавтоматическиEN. Juniorage7/8conflict. Tinker—availableproviderwindow,неоткрытыйfamilycamp;общиеMayfestivaldatesнеJuniorfinalschedule.')],
 steps=[dict(title='Осень2026 · проверить одну действующую команду',detail='Не покупатьновыйFLLkitдо выбораedition. Испания:K8можетдатьМатвеюageentryсейчас,нонужны4–10участников. ОскаротдельноExplore/K5либоRoboBasic. SwissChallengeприёмдо31октября2026;местныйhost/foreigngateпроверить.'),dict(title='Каникулы · технический пробный поток',detail='ИздатированныхEN/FRкандидатовсамыйпонятныйпообоимвозрастамABIHaunted26–30октября2026. Формыдают5–8и9–12,circuits/mechanisms/code. Это обучение, неinternationalprize. Согласоватьуровеньдля3годовопыта.'),dict(title='2027–2029 · одна инженерная лига и собственный продукт',detail='Матвей:WROElementary+собственнаяautonomoussystem либоконкретнаяFLLedition;Оскар:младшийcompetitiveRoboBasicилиExploreпроекты→Elementaryпосле8поnationalbirthrules. ДобавитьPython/механизмы/журналэкспериментов,демонстрациюнаEN/ES и продуктдляреальногопользователя;1–2лиги,небесконечнаясменаплатформ.'),dict(title='К10–12лет · отбор и доказательства вклада',detail='Currentmentor/нагрузка/свойкод/engineeringnotebook→localresult→nationalquota→worldevent. Проверятьjudgedawardvsperformancevsучастие. Переездрешатьпослепробноготриместраиувиденнойработыteam,а не schoolmarketing.')],
 sources=[dict(title=t,url=u,checked=CHECKED) for t,u in [('WROSpainages/independentroute',wroe),('FLLSpain26/27twoeditions',flles),('WROSwissStarter',starter),('SwissFLLages','https://www.first-lego-league.org/en/divisions/challenge'),('ABIcurrentHauntedform',forms['L230']),('BaselJunior/Seniorrobotics',basel),('FranceJuniorcurrententry',junior),('Helveticpublishedtables',hel)]])
d['europe_focus']=f
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
for pid,text,urls in [('wro','v30:SpainRoboBasic6–12иSwissStarter6–10—младшиенациональныепути;нетавтоматическойworldquota. См.профилиwro-spain/wro-switzerland.',[(wroe,'Spainages'),(starter,'SwissStarter')]),('first','v30:FLLSpain2026/27FoundersChallenge10–16vsFutureK8 8–16,4–10participants/2newrobots;Discoverнедоступен. SwitzerlandChallenge9–16;возрастаиhardwareразделенывfll-europe-three.',[(flles,'Spainactual26/27registration'),(fllch,'SwissBIOGLOW')])]:
 p=next(p for p in d['league_guide']['profiles'] if p['id']==pid);p['nuances'].append(text);p['sources'].extend(dict(title=t,url=u,checked=CHECKED) for u,t in urls)
known={s['url'] for s in d['sources']}
for url,title in [(e['source'],e['title']) for e in new]+[(r['url'],r['label']) for e in new+[mwc] for r in e['references']]+[(s['url'],s['title']) for sch in schools for s in sch['sources']]+[(s['url'],s['title']) for s in f['sources']]:
 if url not in known:d['sources'].append(dict(url=url,title=title,checked=CHECKED,evidence='Первичныйисточникпрочитан;scope/неизвестныеусловияотмеченывдосье.'));known.add(url)
a=d['completeness_audit'];a.update(version=30,checked=CHECKED,status='partial',scope='Углублённый проходШвейцария/Испания/Франция:лагеря,национальныевозрастныепути,школыиprofessionalexpos. Мироваяцельпродолжается.',
 conclusion='Частичный мировой каталог. v30:37новыхкарточек,4национальныхпрофиля,3школыиотдельноеевропейскоесравнение. Датыстарыхсмен,языквебсайта,schoolclaims иforeignworldquota не смешаны.',new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=['E017'],new_school_ids=[s['id'] for s in schools])
a['caveats'].append('v30:19новыхучебныхкарточек — смены/курсы4операторов (Helvetic,NATUK/HES,ABI,Tinker),не19независимыхмеждународныхлагерей. TinkerB2Bнеfamilybooking;unknowncamp/competitionlanguagesнеподтвержденыязыкомсайта. Тристраныпроверенычастично.')
issues=[dict(name='FLLSpaincurrentregistrationversusgeneralhomepage',status='2026/27Discoverнедоступен;FoundersChallenge10–16;FutureK8 8–16competitive,4–10детей/2новыхробота. Приоритетcurrentseasonregistration.',official_alternative=flles),dict(name='Helvetic2027tables/dateandageconflicts',status='Roboticspage2027vsобщийoverview2026/datescomingsoon;13–16July2027namedMon–FriпротиворечитTue–Fri. L222startпустой. Intro7+vs6–9groupsи4–12camp;ENroboticsнеподтверждён. ПозднейшиеповторныеHTTPзапросы403/timeout,перваяуспешнаяwebвыгрузкапрочитана.',official_alternative=hel),dict(name='FranceJunior7or8minimum / olddeadline',status='Currentparticipation8–18,olderpresentation7–18. Старый31Dec2025deadlineиMay2026final не перенесенына2027;known2027regionaldatesсохранены.',official_alternative=junior),dict(name='BaselrankversusOPRandworldqualification',status='Roboticsoverviewnational2nd;конкретныйAlpine2026report4thoverall/2ndOPR. Worldqualificationreportпубликуетfirstqualificationстарших,неworldprize. Organizerprotocolещёнеполучен.',official_alternative=baselaward),dict(name='Tinkerconsumeradmission / Summer2027wrongrowyear',status='Сервисдляцентров,непрямойfamilycamp. Currentwinter/spring2027providerwindowsпоказаныP4;летниестроки2026под2027headingнеисправлены.',official_alternative=tinker)]
a['source_issues'].extend(issues)
eu=next(x for x in a['continents'] if x['name']=='Европа');eu['remaining']='v30углубилCHE/ESP/FRA,нонеполныйобзорлагерей/школ/локальныхqualifiers. Foreignadmission,ENjudging,currentjuniorcoach,полнаясмета,Swissdynamiclocations,FRмладшиеRCJиschoolprotocolsостаются.'
a['validation']=dict(version=30,status='pending',previous_version=29)
c=d['camp_focus'];c.update(version=30,checked=CHECKED,conclusion='EN/ES/RUсемейныеязыки. v30:ABIcurrentFR/ENtechnicalworkshops,NATUKRoboticsнаENследующийнабор,Helvetic2027снеподтверждённымENrobotics,TinkerEN/ESчерезhostcentre. Датыиagegatesразделены.',added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=[])
c['routes'].extend([dict(name='Европа · младшие EN/ESканикулы',detail='ABIHaunted5–8/9–12,26–30Oct2026FR/ENcircuits/code;NATUKRobotics6–16ENresidential/dayдат2027нет;Helveticлето2027ENименноroboticsнеподтверждён.',ids=['L230','L229','L231','L227','L228','L221','L224']),dict(name='Европа · регулярные курсы и партнёрские окна',detail='Helveticwinter/springпоWednesday —неcontinuousholidaycamp. TinkerдоступеннаEN/ESпозаказуцентра,неоткрытаяfamilyregistration;age/actualhostнеполучены.',ids=['L217','L218','L219','L220','L232','L233','L234','L235'])]);c['source_issues'].extend(issues)
d['expansion_log'].append(dict(version=30,checked=CHECKED,added=len(new),updated_ids=['E017'],new_profiles=4,new_schools=3,note='CHE/ESP/FRAcountrycomparison,actual26/27nationalgates,2027tablesandprofessionalexpos;worldcoveragepartial.'))
assert len(new)==37 and len(profiles)==4
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v30.json');r.setdefault('research_passes',[]).append(dict(version=30,scope='DeepCHE/ESP/FRA',added_records=len(new),new_profiles=4,new_schools=3,status='partial',remaining=eu['remaining']+' Othercountriesworldwidecontinuing.'));rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=30,added=len(new),profiles=4,schools=3,world_complete=False)))
