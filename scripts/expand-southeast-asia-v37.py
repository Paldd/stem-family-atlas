"""Bounded primary-source SEA pass; preserve the existing worldwide inventory."""
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];W=ROOT.parent/'stem-family-atlas-work'
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1493 and d['completeness_audit']['version']==36
CHECKED='2026-10-01';new=[];profiles=[];byid={e['id']:e for e in d['events']}
for node in ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['ref','event','profile']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
YES='Условно: возраст подходит; класс, место, язык и иностранный допуск подтвердить'
NO='Нет: ниже минимального возраста этой категории'
UNKNOWN='Уточнить: возраст конкретного потока и школьная категория не установлены'
def add(*a,**k):
 e=event(*a,**k);e['region']='Азия';return e
def cat(name,age,team,hardware,entry,rule='Действующее национальное правило; новый сезон проверяется отдельно'):
 return dict(name=name,age=age,team=team,hardware=hardware,entry=entry,age_rule=rule)
def nextseason(e,past):
 e['period']='Следующий набор не датирован; '+past
 e['note']+=' '+past+' — прошедшая редакция, не будущая заявка 2027.'
my_nroc='https://nroc.sasbadi.com/competition';my_sched='https://nroc.sasbadi.com/schedule';my_nrc='https://nrc.sasbadi.com/competition'
nroc_api='https://wpsls.sasbadi.com/wp-json/wp/v2/posts/181';nroc_sched_api='https://wpsls.sasbadi.com/wp-json/wp/v2/posts/155';nrc_api='https://wpsls.sasbadi.com/wp-json/wp/v2/posts/52'
e=add('C1021','NROC Malaysia · RoboMission Junior · 14 ноября 2026','Малайзия','SEGi University · Petaling Jaya, Selangor',my_nroc,
 '7–9; дата рождения 01.01.2017–31.12.2019 по правилам 2026',YES,NO,
 'Школа Malaysia: private / international / MRSM / public. Rules: 2–3 ученика + mentor; homepage говорит 2 — состав подтвердить. Приезд иностранной гостевой команды и квота WRO не установлены.',
 'Junior Rockstars; LEGO Education / MATRIX по оператору, точный разрешённый kit и поле по игре.',start='2026-11-14',scope='national',evidence='rules',
 note='Национальный календарь даёт Junior 14 ноября 08:00–18:00; 15 ноября — старшие группы. Матвей 2017 подходит в 2026, Оскар 2020 не входит. Inline countdown сайта показывает 19 октября, но полный порядок / крайний срок заявки отдельно не прочитан, поэтому deadline не создан.')
e.update(format='2–3 ученика и mentor по правилам; состав согласовать',references=[ref('Календарь национального этапа',my_sched),ref('Содержимое правил, загружаемое официальной страницей',nroc_api),ref('Содержимое календаря официальной страницы',nroc_sched_api),ref('Оператор: школы и общий состав','https://wpsls.sasbadi.com/wp-json/wp/v2/posts/153')])
for id,name,age,mat,gear in [
 ('C1022','RoboMission Junior','7–9; DOB 2017–2019 по 2026', 'Условно в редакции 2026; в 2027 Матвей выходит из 7–9, нужна новая категория','Junior Rockstars'),
 ('C1023','RoboMission Primary · Rookie / Pro','10–12; DOB 2014–2016 по 2026','Нет в 2026; кандидат после 10-летия только по новым правилам','Robot Rockstars; Rookie / Pro — разные уровни'),
 ('C1024','Future Innovators Primary','10–12; DOB 2014–2016 по 2026','Нет в 2026; будущий проектный маршрут после новых возрастных правил','Robots Meet Culture; свой прототип и защита')]:
 e=add(id,'NRC Malaysia · '+name+' · следующий сезон','Малайзия','Национальная школьная система · площадка нового сезона неизвестна',my_nrc,age,mat,NO,
  '3 ученика + teacher mentor; максимум 5 команд школы в категории, один ребёнок в одной категории. Школьный допуск и national selection иностранной семьи не подтверждены.',gear,scope='national',evidence='rules',
  note='Малайзийская Primary здесь с 10 лет, а не глобальное WRO Elementary с 8. NRC и NROC имеют разные составы. Точный будущий календарь и международная квота нового сезона не установлены.')
 e.update(format='3 ученика + teacher mentor',period='Следующий сезон не датирован; возрастные окна приведены только по 2026',references=[ref('Правила, подгружаемые официальной страницей NRC',nrc_api)])
itex='https://itex.com.my/';itex_rules=itex+'competition/';itex_banner='https://itex.com.my/wp-content/uploads/2026/05/Web_banner_Main_Website_Desktop_2561_x_10681-scaled.jpg'
e=add('C1025','WYIE / ITEX Malaysia 2027 · Primary inventors','Малайзия','Kuala Lumpur Convention Centre',itex_rules,'Primary: 12 лет и младше по опубликованной странице; правила именно 2027 ещё подтвердить',YES,YES,
 'Показ собственной работающей invention, заявка участника / стенда. Международные участники предусмотрены; минимальный возраст, размер команды и условия школьного сопровождения 2027 не установлены.',
 'Собственная технологическая invention, демонстрация и оценка жюри; тематическую применимость robotics / AI подтвердить.',start='2027-05-27',end='2027-05-28',scope='international',evidence='rules',
 note='Первичный баннер 2027: выставка 27–28 мая 09:00–18:00; награждение 29 мая отдельно. Страница competition сохраняет старые названия / ссылки 2024–2026: Primary ≤12 — ориентир, не подтверждённый допуск нового сезона. Registration of interest прямо не является подтверждением участия. Медали выставочного конкурса не равны мировому титулу роботолиги.')
e['references']=[ref('Баннер 2027: два выставочных дня и отдельное награждение',itex_banner),ref('Главная нового выпуска',itex)]
id_wro='https://wroindonesia.org/kategori_00.html';id_wro_join='https://wroindonesia.org/infoDaftar_00.html'
for id,name,gear in [('C1026','RoboMission Elementary','Автономный робот до 250 × 250 × 250 mm; open hardware по местной странице'),('C1027','Future Innovators Elementary','Свой проект / робот, стенд 2 × 2 × 2 m и демонстрация'),('C1028','Entry Level Elementary','LEGO / Arduino-based robot; regional rules различаются по городам')]:
 e=add(id,'WRO Indonesia · '+name+' · следующий цикл','Индонезия','Surabaya / Sidoarjo / Tulungagung / Semarang / Malang',id_wro,'8–12; 1–3 участника + coach по национальной странице',YES,NO,
  'Региональный Entry Level как обязательный отбор → National Surabaya → national selection. Для иностранной команды, переноса category и международной квоты нужен отдельный допуск.',gear,scope='national',evidence='rules',
  note='Даже Entry Level на этой странице начинается с 8. Национальные Entry Level правила помечены Coming Soon; региональные документы разные. Календарь 2027 не объявлен, региональные сроки не выдуманы.')
 e.update(format='1–3 ученика + coach',references=[ref('Обязательная региональная ступень и национальная дата 2026',id_wro_join)])
 nextseason(e,'Национальный финал 2026: 12–13 сентября в Surabaya')
iyrf='https://iyra-indonesia.id/iyrc-indonesia-2026/';iyrf_poster='https://iyra-indonesia.id/wp-content/uploads/2026/03/IYRC-Indonesia-2026-1-724x1024.png'
iyrf_rows=[
 ('C1029','Kinder Mission / Brickspeed · Junior A/B/C','A: TK (kindergarten); B: Grade 1–2 SD; C: Grade 3–6 SD по протоколу 2026','Конструирование / управление роботами в соответствующей дисциплине; конкретный kit и число участников по правилам'),
 ('C1030','Coding Mission · Junior','Grade 1–6 SD / Primary по протоколу 2026','Line following / решения в лабиринте; MRT / RACERO отдельно по действующей игре'),
 ('C1031','Creative MRT · Junior','SD / Primary по протоколу 2026; точные классы нового сезона подтвердить','Своя роботизированная модель по теме, презентация и демонстрация'),
 ('C1032','Game Maker Kit · Open','Open level; числовой минимум / grade cutoff не прочитан','Своя простая игра Microsoft MakeCode Arcade по теме')]
for id,name,age,gear in iyrf_rows:
 e=add(id,'IYRC Indonesia · '+name+' · следующий выпуск','Индонезия','В 2026 Universitas YARSI · Jakarta',iyrf,age,UNKNOWN,UNKNOWN,
  'Оператор IYRF публикует национальные Junior и Open результаты. Точные школьные категории семьи, размер команды, платформа, иностранная регистрация и язык требуют действующего rulebook.',gear,
  scope='national',participation='individual_or_team',evidence='historical_program',themes=('games','coding') if id=='C1032' else ('robotics','coding'),
  note='Категории классов прочитаны в первичном протоколе результатов 2026, а не превращены в гарантированные правила 2027. Open не значит подтверждённый допуск 6 лет. Награды национального этапа не названы мировыми; поездка Korea по новому циклу не обещана.')
 e['references']=[ref('Официальный постер с датой и онлайн / очными дисциплинами',iyrf_poster)]
 nextseason(e,'Редакция 2026 прошла 17 мая')
ric='https://www.kodingnext.com/ric2026'
for id,name,age,mat,osc,gear in [('C1033','RoboExplorer','4–7','Нет: старше 7',YES,'Korbo blocks'),('C1034','Junior Builder','8–12',YES,NO,'Whalesbot AI 1s')]:
 e=add(id,'RoboNext Innovation Challenge · '+name+' · следующий набор','Индонезия','Kemayoran / Manado / Makassar / Samarinda / Medan по 2026',ric,age,mat,osc,
  'Выполнить challenge и подать собственную работу по новому набору; посещение branch, иностранное участие и язык оценивания подтвердить.',gear,scope='national',participation='individual_or_team',evidence='historical_program',
  note='Обзор hero рекламирует Beijing для 13–19, но конкретные младшие A/B действительно 4–7 и 8–12. Их приз — holiday camp voucher IDR 800 000 по 2026. Beijing top5 относится только к Senior 13–19; детям 6/9 эта поездка не обещана.')
 e['reward']='Награда младшей категории по протоколу; по 2026 voucher лагеря, не отбор в Beijing'
 nextseason(e,'Заявки и challenge 2026: 24 апреля–31 мая; результаты 1 июня')
vn_portal='https://edu.steamsolutions.com.vn/';vn_fll='https://steamsolutions.com.vn/san-choi/first-lego-league-viet-nam/';vn_gov='https://skhcn.gialai.gov.vn/Home/ChiTietTin/?tin=NjQxNA%3D%3D'
for id,name,gear in [('C1035','RoboMission Elementary','Автономный робот и mat задачи; действующий национальный rulebook и kit отдельно'),('C1036','Future Innovators Elementary','Свой роботизированный проект и защита')]:
 e=add(id,'ROBOTACON WRO Vietnam · '+name+' · следующий цикл','Вьетнам','Национальные qualifiers → финал; новая площадка неизвестна',vn_portal,
  'Elementary WRO 8–12 — ориентир международной категории; новый локальный cutoff подтвердить',YES,NO,
  'Viet Tinh Anh / STEAM Solutions; отбор national team. В 2026 были иностранные гости, но guest entry и право представлять Vietnam — разные условия.',gear,
  scope='national',evidence='historical_program',note='Правительственный отчёт: финал 22–23 августа 2026, Quy Nhon University, около 500 детей из 12 провинций и приглашённые Korean / Chinese teams, 44 Vietnamese quotas после отбора. Это не открытая квота для приезжей семьи. Конкретные младшие local boards / WeDo и даты 2027 не установлены.')
 e.update(period='Следующий сезон не датирован; национальный финал 2026 уже прошёл',references=[ref('Отчёт государственного ведомства о финале 2026 и гостях',vn_gov),ref('Описание национального оператора','https://steamsolutions.com.vn/san-choi/robotacon/')])
for id,name,age,mat,osc in [('C1037','Explore','6–9 по национальной обзорной странице','Условно: новый cutoff важен, в 2027 Матвею исполняется 10',YES),('C1038','Challenge','9–16 по национальной обзорной странице',YES,NO)]:
 e=add(id,'ROBOTACON FLL Vietnam · '+name+' · следующий сезон','Вьетнам','Viet Tinh Anh · место нового выпуска неизвестно',vn_fll,age,mat,osc,
  'Школьная / клубная команда с наставником; действующие комплект, состав, иностранная заявка и право на Vietnamese delegation не подтверждены.',
  'Explore: модель и объяснение проекта' if name=='Explore' else 'Robot Game, проект и командная работа по выбранному изданию FIRST',scope='national',evidence='historical_program',
  note='Обзор говорит January ежегодно, но свежий календарь FELTA указывает Vietnam Championship 26–29 марта 2026. Старый месяц не перенесён в January2027, а возраст обзорной страницы не объявлен новым регламентом. Английский сайт / участие гостей не доказывают EN judging.')
 e.update(period='Следующая точная дата не объявлена',references=[ref('FELTA: календарь Vietnam Championship 2026','https://felta.ph/pro/files/2026/FELTA%20SCHEDULE%20OF%20ACTIVITIES%202026_version%208.pdf')])
 if name=='Explore':e['reward']='Фестиваль / представление проекта; соревновательная победа и world quota не обещаны'
engage_manual='https://games.recf.org/engage/2.0';engage_directory='https://recfevents.org/Events/ApprovedEvents?ProgramTypeId=1&RegionId=109'
engage_rows=[
 ('C1039','Hanoi Qualifying Tournament','178','2026-10-17','2026-10-17','2026-10-10','$60 / команда; сезонная регистрация отдельно',YES,YES,'Локальный qualifying event; число spots и eligibility конкретной награды по RECF approval. Основные Dates дают 17 октября, а agenda содержит два дня — расписание перед поездкой согласовать.'),
 ('C1040','Vietnam Solo Remote · по приглашению','611','2026-10-18','2026-10-18','2026-10-15','$20 / команда; сезонная регистрация отдельно',YES,YES,'Оператор допускает рекомендации registered Engage teams из мест без очных событий. Нужны отдельная рекомендация и приглашение; открытая кнопка не заменяет приглашения. Один 30-minute slot: до 3 driving + 3 coding, собственное поле / robot / камеры. 08:00–17:00 ICT — не время Коста-Рики.'),
 ('C1041','Vietnam Open · международный Signature Event','177','2027-02-19','2027-02-21','2027-01-30','$90 / команда; сезонная регистрация, перелёт и жильё отдельно',YES,YES,'Описан приезд международных команд и confirmation letter после регистрации / оплаты. Это поддерживает guest route, но не гарантирует визу, место или world spot. Registration opens 20 октября 2026; итоговый адрес, три календарных дня vs two-day agenda и EN interview уточнить.'),
 ('C1042','Hanoi Scrimmage · Middle School only','760','2026-10-09','2026-10-09','2026-10-08','Бесплатно; сезонная регистрация отдельно','Нет для начальной школьной категории; middle-school placement не подтверждён','Нет для начальной школьной категории; middle-school placement не подтверждён','Invitational scrimmage, не qualifying. Главные Grade Levels и Eligibility — Middle School / 15U, хотя общий English overview упоминает Elementary. Использовано узкое условие, не один лишь максимум 15 лет.')]
for id,name,number,start,end,deadline,cost,mat,osc,note in engage_rows:
 url='https://recfevents.org/Events/Details/'+number
 e=add(id,'RECF Engage · '+name,'Вьетнам','Онлайн из своего помещения / Hanoi organiser' if id=='C1040' else 'Hanoi · точный адрес по final instructions' if id!='C1042' else 'American Center · 170 Phố Ngọc Khánh, Giảng Võ, Hanoi',url,
  'Middle School / 15U: ≤15 на 06.05.2027' if id=='C1042' else 'Elementary / 12U: ≤12 на 06.05.2027; Middle / 15U отдельно',mat,osc,
  'Зарегистрированная RECF команда минимум из 2 учеников; свои design / build / code / notebook; сопровождающий взрослый старше 18 и seasonal release forms. Класс и допуск конкретного этапа проверяются отдельно.',
  'Tier Takeover, поле 6 × 8 ft; разрешённые parts по manual2.0 / актуальному Q&A, driving и autonomous coding.',start=start,end=end,deadline=deadline,
  scope='international' if id in ['C1040','C1041'] else 'local',cost=cost,priority='P4 — школьная категория не подходит' if id=='C1042' else 'P2 — конкретный этап после подтверждения допуска',
  note=note+' Двуязычное описание не доказывает язык интервью. Инженерный notebook должен быть собственным; AI-generated notebook запрещён. Не каждая награда даёт выход на мировой финал.')
 e.update(references=[ref('Manual2.0: возраст, команда, взрослый и permitted parts',engage_manual),ref('Четыре опубликованных Vietnam events',engage_directory)],admission_kind='invitation' if id in ['C1040','C1042'] else 'open_application')
 if id=='C1042':e['reward']='Результат учебного scrimmage; не мировой / региональный отбор'
ph_reg='https://felta.ph/pro/files/2026/25th_PRO_Registrration-Form-2026.pdf';ph_schedule='https://felta.ph/pro/files/2026/FELTA%20SCHEDULE%20OF%20ACTIVITIES%202026_version%208.pdf'
for id,name,gear in [('C1043','RoboMission Elementary','Robot Rockstar; задачи поля'),('C1044','Future Innovators Elementary','Свой роботизированный прототип и защита')]:
 e=add(id,'Philippine Robotics Olympiad · '+name+' · следующий цикл','Филиппины','FELTA · школа / national organiser; новая площадка неизвестна',ph_reg,'8–12 по форме 25th PRO 2026',YES,NO,
  'Школьная команда и coach, подписи principal, parent consent, medical certificate и копия authenticated birth certificate. Иностранная школа / national quota не подтверждены.',gear,scope='national',evidence='historical_program',
  note='Актуальная форма и homepage расходятся по срокам / месяцам: форма June13, parent consent August–September, homepage July. Schedule version8 даёт dry run June13 и финал June22–25. Всё это прошедший 2026, не новый 2027 календарь. Возраст 8–12 взят из самой registration form.')
 e.update(period='Следующий набор не объявлен; 2026 закрыт',references=[ref('Оператор PRO','https://felta.ph/pro/'),ref('Календарь Version8 с прошедшим июньским финалом',ph_schedule)])
e=add('C1045','FIRST LEGO League Philippines · следующий национальный выпуск','Филиппины','FELTA · школу, площадку и division нового выпуска уточнить',ph_schedule,
 'Новый local division / age cutoff не опубликован в прочитанном календаре',UNKNOWN,UNKNOWN,
 'Нужны конкретный division, регламент, команда / coach и иностранный школьный допуск. 16th FLL theme launch не является открытой регистрацией детей.',
 'FIRST LEGO League по выбранному изданию; комплект и младший Explore путь подтвердить у оператора.',scope='national',evidence='historical_program',
 note='Календарь подтверждает 15th FLL 14 февраля 2026 в DLSZ Vermosa и 16th theme launch6 августа 2026. 17 октября 2026 Naga указан Student Summit, а не национальный финал; ложная competition date не создана. Возраст глобальной FIRST нельзя автоматически переносить на Philippines admission.')
e['period']='Новый конкурсный этап не датирован'
kibo='https://philsa.gov.ph/news/7th-kibo-robot-programming-challenge/'
for id,name,age,gear,prize in [('C1046','Beginner','Младше 16 / Junior High и ниже; полностью новые в coding','Int-Ball2 simulator; облегчённые правила должны выйти в October2026','Beginner победитель не участвует в ISS Final'),('C1047','Regular','Elementary–graduate school; отдельного минимума лет нет','Int-Ball2 navigation внутри ISS Kibo; собственный код / simulator','Philippine preliminary winner выходит в ISS Final; это выполнение кода, не полёт ребёнка')]:
 e=add(id,'Kibo Robot Programming Challenge · Philippines · '+name,'Филиппины','Онлайн; Philippine delegation',kibo,age,
  'Нет: требуется Filipino citizenship; заявленные паспорта семьи Mexican / Russian','Нет: требуется Filipino citizenship; заявленные паспорта семьи Mexican / Russian',
  '3–8 Filipino students в местной или зарубежной educational institution; parental consent до 18. Student / guardian / teacher может быть team leader.',gear,
  deadline='2026-10-14',scope='national',priority='P4 — гражданство семьи не соответствует Philippine track',evidence='rules',themes=('robotics','coding'),
  note='Регистрация до 14 октября 2026 22:59 Philippine Time, simulator должен стать доступен в October2026. '+prize+'. Regular включает элементарную школу, но citizenship остаётся обязательным; младший возраст сам по себе не даёт допуска. Beginner для полностью новых в coding может не соответствовать трёхлетнему опыту семьи.')
 e.update(format='3–8 студентов + team leader',period='Сезон 2026/27; будущий день preliminary / final не объявлен',reward=prize)
kn='https://www.kodingnext.com/holiday-camp';kn_home='https://www.kodingnext.com/en'
for id,name,age,mat,osc,gear,themes in [
 ('L319','RoboCare Lab','4–7','Нет: старше 7',YES,'Photon robot / Korbo / iPad; sensors и движение',('robotics','coding')),
 ('L320','BioLab','8–11',YES,NO,'Whalesbot AI 1s, sensors и биологические симуляции',('robotics','coding')),
 ('L321','SmartEye Lab','8–11',YES,NO,'PictoBlox / webcam / AI classifier; учебная имитация medical assistant',('ai','coding')),
 ('L322','Bio-Tech Engineer','8–11',YES,NO,'Scratch / CreatiCode, своя биологическая игра / симуляция',('games','coding'))]:
 e=add(id,'KodingNext Holiday Camp · '+name+' · следующий набор','Индонезия',
  'Robotics: Kemayoran / Puri / Medan / Makassar / Manado / Samarinda' if id in ['L319','L320'] else 'Точный branch / online вариант подтвердить',kn,age,mat,osc,
  'Уточнить новый поток, teacher с достаточным EN, foreign visiting child и уровень проекта после трёх лет соревнований. Онлайн: свой tablet4–7 / laptop8+; offline equipment по оператору.',gear,
  block='Лагеря',participation='day_camp',languages=('ID','EN'),language='Оператор прямо подтверждает bilingual Indonesian / English teaching; конкретный camp teacher и долю EN согласовать.',
  cost='По 2026: IDR800000 один курс /1300000 два; новый счёт и содержание подтвердить.',themes=themes,evidence='historical_program',
  note='Два дня по 3 часа, всего 6 часов на курс; beginner-friendly, не недельный пансион. Healthy Tech2026 описывает реальные программы, новые даты не опубликованы. RoboNext camps доступны только в перечисленных 6branches: Bali не обещан. AI classifier — учебная симуляция, не медицинская диагностика.')
 e.update(language_mode='bilingual',language_certainty='FAQ прямо: преподавание Indonesian+English. Camp-specific teacher / branch language остаётся условием.',period='Новый конкретный поток не объявлен; две половины дня по описанию 2026',references=[ref('FAQ: прямо указан язык обучения, оборудование и уровни',kn_home)])
hec='https://hanoienglish.com/robotics.html';hec_camp='https://hanoienglish.com/camp/'
e=add('L323','HEC Hanoi · English STEAM & Robotics · регулярная группа','Вьетнам','Đống Đa · Hanoi',hec,
 'Формальная граница группы не опубликована; описание говорит о начале в 6 лет',UNKNOWN,UNKNOWN,
 'Пробное занятие, конкретный age / level group и teacher; cohort opens после 12seats. Допуск иностранной семьи и часы уточнить.',
 'Design, build, code, defend; moving robots / sensors / реальные прототипы и защита на EN.',block='Лагеря',participation='day_camp',languages=('EN',),
 language='Программа прямо соединяет robotics и презентацию / защиту своих проектов на английском.',evidence='program',
 note='Это weekly class, не подтверждённая каникулярная смена и не международный конкурс. Возрастная рекламная фраза не заменяет enrollment cutoff. Максимум 12; технические часы и качество конкретного наставника нужны до решения о переезде.')
e.update(participation='regular',format='Регулярный STEAM / Robotics class',language_mode='primary',period='Группа формируется; конкретный график не опубликован')
e=add('L324','HEC Hanoi · all-English summer engineering · кандидат нового лета','Вьетнам','Đống Đa · Hanoi',hec_camp,
 'Формальная граница summer group не опубликована',UNKNOWN,UNKNOWN,
 'Получить будущие даты, возрастный поток, долю engineering / robotics и foreign admission. Не бронировать по витрине прошедшего camp.',
 'Строительство моделей / engineering / robotics blocks и презентации; основной лагерь также включает English curriculum.',block='Лагеря',participation='day_camp',languages=('EN',),language='Лагерь прямо назван all-English; robotics page подтверждает engineering / robotics каждый день Summer2026.',evidence='historical_program',
 note='21 campers и 40 documented days относятся к summer2026. Новых дат 2027, formal age range и стоимости именно camp нет. 210000₫ per-session на витрине не объявлены полной camp fee. Это образовательная программа, не подтверждённый международный hackathon.')
e.update(language_mode='primary',period='Кандидат следующего лета; новый календарь отсутствует',references=[ref('Engineering и robotics blocks Summer2026',hec),ref('Официальный текст витрины, загружаемый приложением','https://hanoienglish.com/camp/assets/index-D6WUE6um.js')])
e=add('L325','Hanoi Academy · NextGen Summer Camp · кандидат нового набора','Вьетнам','Hanoi Academy campus', 'https://summercamp.hanoiacademy.edu.vn/','5–16 по программе 2026',YES,YES,
 'Подтвердить конкретную STEM / robotics группу, EN teaching в техническом блоке, следующий поток и доступ visiting family.',
 'STEM & Robotics вместе с English practice, спортом и творчеством; объём самостоятельной robotics уточнить.',block='Лагеря',participation='day_camp',evidence='historical_program',
 note='Опубликованы 6 недель Mon–Fri1 июня–10 июля 2026 — уже прошли. Bilingual school / English practice не доказывают EN-преподавание technical sessions, поэтому EN language filter не включён.')
e['period']='Кандидат нового лета; даты 2027 не объявлены'
e=add('L326','Soleh Academy · 3 Days Robotics Camp','Малайзия','Конкретную площадку подтвердить','https://solehacademy.com/3-days-robotics-camp','7–17 по FAQ именно camp',YES,NO,
 'Новичкам разрешено; получить конкретные три дня, место, EN/ES teacher и foreign child admission.',
 'Arduino / circuits /3Ddesign → motors / movement /automation → integration / troubleshooting.',block='Лагеря',participation='day_camp',evidence='program',
 note='Общий operator banner4–18 не является camp возрастом: конкретный FAQ7–17. Английская страница не подтверждает английские технические занятия. Ни даты, ни стоимость camp не установлены.')
e['period']='Трёхдневная программа; конкретные даты не опубликованы'
e=add('L327','DRABOT Malaysia · robotics online intensive · будущая ступень 10+','Малайзия','Google Meet / свой робот дома','https://www.drabot.com.my/programs-workshops/drabot-robotics-holiday-camp-2026',
 'Primary10–12; Secondary / teachers по программе 2026','Нет в 9 лет; рассматривать после 10 по новому потоку',NO,
 'Новый поток и реальный EN instruction не подтверждены; собственный компьютер, базовые самостоятельные компьютерные навыки, DRABOT kit и mat.',
 'Scratch/mBlock5 и C/C++ArduinoIDE; digital I/O, PWM, serial, motors, line following, obstacle avoidance.',block='Лагеря',participation='day_camp',evidence='historical_program',
 priority='P4 — текущий возраст / язык не подходят без новых условий',cost='По 2026 promo RM99 с собственным kit или RM250 с комплектом; новый тариф неизвестен.',
 note='3–6 июня 2026,4 дня около 28 часов, live online и recordings; наборзакрывался 11 мая. Это не очный пансион. Язык EN не заявлен в прочитанной программе; прежние OS Win7/10/macOS10.12 требования не считаются безопасной современной рекомендацией.')
e.update(participation='online_camp',format='Интерактивный online intensive со своим оборудованием',period='Следующий цикл не датирован; программа 2026 уже прошла')
def exhibition(id,title,country,city,url,start,end,policy,note,highlights,gear):
 e=add(id,title,country,city,url,'18+ trade visitors' if policy=='adults_only' else 'Минимальный детский возраст не опубликован',
  'Нет: under18 запрещены' if policy=='adults_only' else 'Уточнить допуск ребёнка 9 лет',
  'Нет: under18 запрещены' if policy=='adults_only' else 'Уточнить допуск ребёнка 6 лет',
  'Предварительная регистрация и условия конкретного visitor pass; minor / guardian admission отдельно.' if policy!='adults_only' else 'Только trade / business registration, взрослый 18+; онлайн и требования к business status по оператору.',
  gear,block='События',participation='visitor',start=start,end=end,scope='international',priority='P4 — взрослый профессиональный визит' if policy=='adults_only' else 'P2 — выставка после проверки детского допуска',themes=('technology','robotics') if 'robot' in gear.lower() or 'робо' in gear.lower() else ('technology',),note=note)
 e.update(exhibition_tier='profile',visitor_policy=policy,visitor_policy_note=note,
  adult_entry='Регистрация trade visitor; допуск конкретного взрослого и билеты проверить' if policy=='adults_only' else 'Visitor registration; школа / public / foreign visitor правила проверить',
  exhibitor_note='Организаторская международная выставка; список компаний конкретного выпуска нужен отдельно. Присутствие всех мировых компаний не обещано.',highlights=highlights,exhibitor_directory_url=url)
 return e
e=exhibition('E157','ITEX Malaysia2027 · invention / technology exhibition','Малайзия','Kuala Lumpur Convention Centre',itex,'2027-05-27','2027-05-28','confirm_children',
 'Баннер 2027: public exhibition только 27–28 мая 09:00–18:00.29 мая—awards ceremony. FAQ прошлого выпуска допускает Trade/Student/Public free with registration, но минимум лет и правила детей 2027 не опубликованы: семейный допуск нужно подтвердить.',
 ['International inventions','WYIE young inventors','Технологические прототипы и образовательные проекты'],'Inventions / technology / youth projects; robotics и AI по конкретным экспонентам')
e['references']=[ref('2027: exhibition days отдельно от awards',itex_banner),ref('FAQ: audience / tickets старого выпуска',itex+'faq/')]
exhibition('E158','INATRONICS2027 · electronics / components / technology','Индонезия','JIExpo Kemayoran · Jakarta','https://www.inatronics-exhibition.net/event-fact-sheet','2027-04-21','2027-04-23','adults_only',
 'Официальный Admission: trade / professional only, visitors under18 will not be admitted. Дети 6/9 не могут пройти по опубликованному правилу.',
 ['Electronics manufacturing','Components / systems','Co-located IoT / smart-city / energy shows'],'Electronics technology, components, manufacturing and IoT; технический B2B салон')
exhibition('E159','IISMEX2027 · smart-city technology','Индонезия','NICE PIK2 · Tangerang','https://iismex.com/visitor/','2027-08-24','2027-08-26','adults_only',
 'Visitor guidelines запрещают under18. Это B2B smart-city визит только взрослым; free admission относится к qualified registered visitors.',
 ['Smart city / infrastructure','Digital management','Professional industry meetings'],'Smart-city technology / infrastructure; набор robotics booths не установлен')
exhibition('E160','Manufacturing Indonesia2026 · industrial technology','Индонезия','JIExpo Kemayoran · Jakarta','https://www.manufacturingindonesia.com/visiting/visitors-faq/','2026-12-02','2026-12-05','adults_only',
 'FAQ: business / trade visitors only; under18 запрещены. Онлайн-регистрация обязательна, onsite registration нет.2–4 декабря 10–18,5 декабря 10–17WIB.',
 ['Manufacturing technology','Industrial machinery','Business / trade visitor programme'],'Manufacturing / industrial technology; состав automation и robotics компаний 2026 смотреть в каталоге')
exhibition('E161','Vietnam ICTCOMM2027 · AI / IoT / EdTech','Вьетнам','Hall A · SECC · Ho Chi Minh City','https://ictcomm.vn/en/about-ictcomm/','2027-06-29','2027-07-01','confirm_children',
 'Основной профиль—B2B telecom/IT; Education Zone прямо включает parents/students и STEAM/coding. Возраст и caregiver pass не опубликованы, это основание уточнить семью, а не подтверждённый child ticket.',
 ['AI / IoT / Data Centers','EdTech / smart school','STEAM / coding education'],'AI, IoT, Cloud, digital infrastructure и Education Zone; конкретные экспоненты 2027 отдельно')
e=exhibition('E162','INTI Robotics & Automation Expo · следующий выпуск','Индонезия','JIExpo · Jakarta','https://robot.inti.asia/about','','','confirm_children',
 'Прочитана редакция 11–13 августа 2026—уже прошла. Нового 2027 календаря и minor policy нет. Маркетинговое число+18 не интерпретировано как запрет / разрешение детского возраста.',
 ['Industrial robotics','Automation','AI / smart manufacturing'],'Robotics / automation / AI industry exhibition; реальный список booths нового выпуска неизвестен')
e['period']='Следующий выпуск не датирован;2026 уже прошёл'
updated=['C029','C068']
e=byid['C029'];e.update(checked=CHECKED,source=engage_manual,age='Elementary12U:12 илимладше на 06.05.2027; Middle15U отдельно',
 participation='team',language='Manual на EN; язык judging национального этапа отдельно подтвердить',languages=[],
 language_certainty='Язык manual не назван автоматически языком всех интервью.',
 proof='Прочитан manual2.0 от 29.09.2026: inclusive12U /15U на 06.05.2027 и минимум 2 ученика',
 entry='RECF team минимум 2students → конкретный eligible event → approved spots; взрослый старше 18 и seasonal release forms',
 references=[ref('Vietnam directory: реальные отдельные этапы',engage_directory)],
 note=e['note']+' Уточнение 2026/27:12U включает 12 лет; это не строгий under12. Зарубежное участие, assigned region и world quota конкретного события проверяются отдельно.')
e=byid['C068'];e.update(checked=CHECKED,scope='international',languages=[],language='EN description / international rulebook links; EN judging прямо не подтверждён',
 language_certainty='Наличие international rulebook и EN сайта не гарантирует EN judging.',
 proof='Прочитана страница 2026: international participant rulebook предусмотрен, registration closed, новые даты не объявлены',
 references=[ref('Оператор: раздельные international / Malaysian / My-Robot rulebooks',e['source'])])
p=next(p for p in d['league_guide']['profiles'] if p['id']=='recf')
p.update(age_summary='Engage12U≤12 /15U≤15 на 06.05.2027; Achieve/Inspire/Launch по своим manual',language='ManualEngage на EN; язык интервью каждого этапа нужно подтвердить')
for c in p['categories']:
 if c['name']=='Engage':c.update(age='Elementary12U≤12; Middle15U≤15',age_rule='Inclusive возраст на 06.05.2027 по manual2.0; школьный division этапа отдельно',team='Минимум 2students, взрослый старше 18, release forms')
p['event_ids']+=['C1039','C1040','C1041','C1042'];p['nuances']+=['12U включает 12 лет на 06.05.2027; Elementary / Middle School конкретного этапа всё равно важны.','Remote611 требует recommendation/invitation, scrimmage760 не qualifying и Middle-only, VietnamOpen177 предусматривает foreign teams без гарантии worldspot.']
p['requirements']+=['Все участники завершают seasonal release forms; student-owned notebook и latest officialQ&A; конкретный approvalspots проверить до оплаты.']
p['sources'].append(dict(title='Engage manual2.0: точная возрастная отсечка, team и adult',url=engage_manual,checked=CHECKED))
profile('sasbadi-malaysia','Malaysia NRC / NROC · разные младшие правила','regional','Junior7–9; Primary10–12; NRC/NROC составы различаются',
 'Два национальных школьных маршрута Sasbadi / MOE. Junior2017–2019 включает Матвея в 2026, не Оскара 2020.',
 [cat('NROC Junior','7–9 / DOB2017–2019','2–3+mentor по rules;homepage2','Junior Rockstars / approved kit','Malaysian school; foreign guest / world quota не установлены'),cat('NRC Junior','7–9 / DOB2017–2019','3+teacher;max5schoolteams','Junior Rockstars','Школьный NRC допуск'),cat('NRC Primary RM / FI','10–12 / DOB2014–2016','3+teacher','Rookie/Pro mat либо project','Новый cutoff2027 отдельно')],
 ['C1021','C1022','C1023','C1024'],'Школа икатегория → national competition → отдельные правила international delegation',
 ['Проверить школьное зачисление, DOBwindow, NRCvsNROC и состав.','Уточнить foreigners / international school vs guest overseas team.'],
 ['National Primary с 10 не globalWRO с 8.','NROC Junior14 ноября,15 ноябрястаршие; countdown неполный registration rule.'],
 [('NROC rules',my_nroc),('NROC dates',my_sched),('NRC rules',my_nrc)],age_tags=('9','10-12','teen'))
profile('iyrc-asean-malaysia','IYRC ASEAN Malaysia · Foundation / Primary / Creative','regional','Foundation4–7;Lower7–9;Upper9–12;CreativeA4–9',
 'Международная младшая сетка с отдельными rulebooks для foreign participants; новый выпуск ещё неизвестен.',
 [cat('Foundation','4–7','По новому rulebook','MakerobotA /DinoEggHunter','International participant category'),cat('Lower Primary','7–9','По rulebook','CommunicationMasterIII/MakerobotB','Новый сезон и DOB cutoff'),cat('Upper Primary','9–12','По rulebook','WanderingPlanetIII/DinoDelivery','Новый сезон'),cat('Creative A','4–9','По rulebook','Свой design по правилам','Не worldquota другихли г')],
 ['C068'],'International application наконкретный выпуск → конкурсная категория → протокол результата',
 ['Не переносить closed2026 в 2027.','Проверить kit, состав, language и birthdays.'],['В 2027 Матвею 10:Lower/CreativeA можетуже неподходить.','Отдельный международный конкурс, не WRO/VEX nationalquota.'],
 [('Current international / local age categories',byid['C068']['source'])])
profile('wro-indonesia','WRO Indonesia · regional Entry → National','regional','Elementary8–12, включая EntryLevel;1–3+coach',
 'Национальная страница подтверждает обязательную региональную ступень; Entry здесь не подходит шестилетнему.',
 [cat('Elementary RM','8–12','1–3+coach','Open hardware /250mmrobot','Regional qualifier → national'),cat('Elementary FI','8–12','1–3+coach','Project /2mstand','Право сменить board / nationalentry уточнить'),cat('Entry Elementary','8–12','1–3+coach','LEGO /Arduino','Local rules по Surabaya/Sidoarjo/Tulungagung/Semarang/Malang')],
 ['C1026','C1027','C1028'],'Обязательный region → NationalSurabaya → утверждённая Indonesian delegation',
 ['Новый 2027 календарь, региональные boardrules и foreignquota.'],['Entry min8.','NationalEntryComingSoon не полноценный rulebook.'],[('Категории',id_wro),('Порядок и прошлый nationaldate',id_wro_join)],age_tags=('9','10-12','teen'))
profile('iyrf-indonesia','IYRF / IYRC Indonesia · robots, AI animation, games','regional','JuniorA TK;B Grade1–2;C Grade3–6SD;Open cutoff уточнить',
 'Национальный первичный протокол 2026 разделяет kindergarten, младшие истаршие primary; grade важнееслова Junior.',
 [cat('Kinder / BrickspeedA–C','TK;Grade1–2;Grade3–6','Состав в rules','Bricks /robot поигре','Внешний класс семьи согласовать'),cat('CodingMissionJunior','PrimarySD','В rules','Line/mazeMRT/RACERO','Nationalgame'),cat('CreativeMRTJunior','PrimarySD','В rules','Prototype /presentation','Nationalcreativejudging'),cat('GameMakerKitOpen','Минимумнепрочитан','В rules','MicrosoftMakeCodeArcade','Open не гарантирует 6 лет')],
 ['C1029','C1030','C1031','C1032'],'Выбрать grade/discpline → новый localrulebook → nationalprotocol; internationalinvite отдельно',
 ['Протокол классов 2026 не rulebook2027.','Foreignentry, язык, kit и teamrules ещёнеустановлены.'],['17 мая 2026 уже прошло.','Много Gold в creative—awardband, неодинабсолютный чемпион мира.'],[('2026 programme and organiser results',iyrf),('Official datedposter',iyrf_poster)])
profile('robotacon-vietnam','ROBOTACON Vietnam · WRO / FIRST LEGO League','regional','FLLExplore6–9 /Challenge9–16 пообзору;WROElementary8–12 ориентир',
 'Национальная система VietTinhAnh с guest teams иотбором Vietnamese delegation; quotas приезжейсемье не обещаны.',
 [cat('FLLExplore','6–9 постаромуобзору','Новый составподтвердить','Exploremodel','Показ, не Challengeworldquota'),cat('FLLChallenge','9–16 пообзору','Новый состав','Robotgame+project','Nationalregistration /quota отдельно'),cat('WROElementary','8–12 globalreference','Nationalrulebook','RM либо FI','Новый localcutoff подтвердить')],
 ['C1035','C1036','C1037','C1038'],'Национальный qualifier → finalist → quota, foreignguestroute отдельно',
 ['Прочитать новый localrulebook иязык judging.','EN/foreignguest невзаимозаменяемыс nationaleligibility.'],['FLL обзор January не March2026calendar и не January2027.','Госотчёт 2026:44quotas для Vietnamese teams, не forallvisitors.'],[('Current2026portal',vn_portal),('NationalFLLdescription',vn_fll),('Government2026finalreport',vn_gov)])
profile('felta-philippines','Philippines FELTA · PRO/WRO и FLL','regional','PROElementary8–12;новая FLLlocalcategory неподтверждена',
 'Школьный nationaloperator сконкретной PROregistrationform, документами иустаревшими конфликтующими 2026 сроками.',
 [cat('PRO RM /FIElementary','8–12','Школа+coach;размерв rules','RobotRockstar /ownprototype','Principal/parents/medical/authenticatedbirthcopy'),cat('FLL следующийвыпуск','Localdivisionage непрочитан','Школа/club поновым rules','Комплектвыбранногоиздания','StudentSummit нефинал')],
 ['C1043','C1044','C1045'],'Школа /FELTA → localnationalregistration → quota поутверждённымправилам',
 ['Новый 2027 календарьи foreignschooladmission.','Документыподписи и DOB отдельноотвозрастного fit.'],['6 летне PROElementary8–12.','Version8June22–25vsformAugust/September:прошлые conflicts неперенесенывбудущее.'],[('PROregistration2026',ph_reg),('OperatorcalendarVersion8',ph_schedule)],age_tags=('9','10-12','teen'))
profile_copy={
 'sasbadi-malaysia':dict(age_summary='Junior 7–9; Primary 10–12; NRC и NROC имеют разные составы',summary='Два национальных школьных маршрута Sasbadi / MOE. Годы рождения 2017–2019 включают Матвея в Junior 2026, а Оскара 2020 — исключают.',route='Школа и возрастная категория → национальный этап → отдельный порядок международного отбора',requirements=['Проверить школьное зачисление, окно рождения и состав команды именно NRC или NROC.','Согласовать иностранного ученика местной школы или отдельную приезжую команду.'],nuances=['Местная Primary начинается с 10, а глобальная WRO Elementary — с 8.','NROC Junior назначен на 14 ноября; 15 ноября — старшие группы. Обратный отсчёт сайта не заменяет полного порядка регистрации.']),
 'iyrc-asean-malaysia':dict(age_summary='Foundation 4–7; Lower Primary 7–9; Upper Primary 9–12; Creative A 4–9',summary='Международная младшая сетка с отдельными правилами зарубежных участников. Следующий выпуск ещё не объявлен.',route='Заявка международного участника на конкретный выпуск → дисциплина → протокол результата',requirements=['Дождаться правил и даты нового сезона.','Согласовать комплект, состав, день рождения и язык оценки.'],nuances=['В 2027 Матвею исполняется 10: Lower Primary и Creative A могут уже не подойти.','Это отдельный конкурс, его награда не даёт квоту WRO или VEX.']),
 'wro-indonesia':dict(age_summary='Elementary 8–12, включая Entry Level; 1–3 ученика и coach',summary='Национальный оператор подтверждает обязательную региональную ступень. Entry Level здесь начинается с 8 и не подходит шестилетнему.',route='Обязательный региональный Entry Level → национальный этап Surabaya → утверждённая индонезийская делегация',requirements=['Получить новый календарь, регламент своего региона и порядок допуска зарубежной команды.'],nuances=['Entry Level начинается с 8.','National Entry Rules помечены Coming Soon; это не полный национальный регламент.']),
 'iyrf-indonesia':dict(age_summary='Junior A: kindergarten; B: Grade 1–2; C: Grade 3–6; Open требует проверки',summary='Первичный национальный протокол 2026 делит kindergarten и начальные классы. Школьный класс важнее общего названия Junior.',route='Класс и дисциплина → новый регламент → национальный протокол; международное приглашение отдельно',requirements=['Категории протокола 2026 не заменяют правил 2027.','Проверить иностранный класс, язык, комплект и состав команды.'],nuances=['Редакция 17 мая 2026 уже прошла.','В Creative опубликованы несколько Gold; это наградные группы, а не один абсолютный чемпион мира.']),
 'robotacon-vietnam':dict(age_summary='FLL Explore 6–9 / Challenge 9–16 по обзору; WRO Elementary 8–12 — международный ориентир',summary='Система Viet Tinh Anh объединяет WRO и FLL. Иностранные гости подтверждены в 2026, но национальная делегация и мировые квоты имеют отдельный допуск.',route='Национальный квалификатор → финал → утверждённая квота; участие зарубежного гостя отдельно',requirements=['Получить правила нового локального сезона и язык защиты.','Уточнить иностранную команду и право представлять страну.'],nuances=['Старый FLL обзор говорит о январе; календарь 2026 указывает март. Январь 2027 не придуман.','Государственный отчёт сообщает о 44 вьетнамских квотах после отбора, а не квотах для всех приезжих.']),
 'felta-philippines':dict(age_summary='PRO Elementary 8–12; новая местная FLL категория требует проверки',summary='Школьный оператор с конкретной формой PRO и документами. Даты прошлой редакции 2026 расходятся между страницей, формой и календарём.',route='Школа и FELTA → национальная регистрация → квота по утверждённым правилам',requirements=['Получить новый календарь и допуск иностранной школы.','Согласовать документы, подписи родителя / директора и возрастной состав.'],nuances=['PRO Elementary с 8 лет, Оскар в 6 не проходит.','Version 8 даёт июньский финал; в форме есть август / сентябрь. Эти прошлые противоречия не перенесены на 2027.'])}
category_copy={
 'sasbadi-malaysia':[('NROC Junior','7–9; рождение 2017–2019','2–3 и наставник по правилам; главный обзор говорит 2','Junior Rockstars / разрешённый комплект','Малайзийская школа; зарубежный гость и квота отдельно'),('NRC Junior','7–9; рождение 2017–2019','3 и teacher; максимум 5 команд школы','Junior Rockstars','Школьный допуск NRC'),('NRC Primary RM / FI','10–12; рождение 2014–2016','3 и teacher','Rookie / Pro поле или свой проект','Новый возрастной cutoff 2027 подтвердить')],
 'iyrc-asean-malaysia':[('Foundation','4–7','По новому регламенту','Makerobot A / Dino Egg Hunter','Международная категория'),('Lower Primary','7–9','По регламенту','Communication Master III / Makerobot B','Новый сезон и дата рождения'),('Upper Primary','9–12','По регламенту','Wandering Planet III / Dino Delivery','Новый сезон'),('Creative A','4–9','По регламенту','Свой design по правилам','Отдельный международный конкурс')],
 'wro-indonesia':[('Elementary RM','8–12','1–3 и coach','Open hardware / робот 250 mm','Региональный отбор → национальный этап'),('Elementary FI','8–12','1–3 и coach','Проект / стенд 2 m','Допуск в национальную категорию отдельно'),('Entry Elementary','8–12','1–3 и coach','LEGO / Arduino','Разные региональные правила')],
 'iyrf-indonesia':[('Kinder / Brickspeed A–C','TK; Grade 1–2; Grade 3–6','По правилам дисциплины','Bricks / robot по игре','Согласовать иностранный класс'),('Coding Mission Junior','Primary / SD','По правилам','Line / maze MRT или RACERO','Национальная игра'),('Creative MRT Junior','Primary / SD','По правилам','Прототип и презентация','Национальная оценка проекта'),('Game Maker Kit Open','Минимум лет не прочитан','По правилам','Microsoft MakeCode Arcade','Open не гарантирует допуск в 6')],
 'robotacon-vietnam':[('FLL Explore','6–9 по обзорной странице','Новый состав подтвердить','Модель Explore','Показ проекта; не квота Challenge'),('FLL Challenge','9–16 по обзору','Новый состав подтвердить','Robot Game + проект','Национальная регистрация и квота отдельно'),('WRO Elementary','8–12 — международный ориентир','Национальный регламент','RoboMission или Future Innovators','Новый местный cutoff подтвердить')],
 'felta-philippines':[('PRO RM / FI Elementary','8–12','Школа и coach; размер по правилам','Robot Rockstar / свой прототип','Директор, родитель, медицинский документ и birth certificate'),('FLL следующий выпуск','Местный возраст ещё не установлен','Школа / клуб по новым правилам','Комплект выбранного издания','Student Summit не является финалом')]}
for p in profiles:
 p.update(profile_copy[p['id']]);p['strengths']=p['summary'];p['categories']=[cat(*x) for x in category_copy[p['id']]]
for e in new:
 if e['id'] in ['L323','L324']:e['language_certainty']='Оператор прямо описывает занятия / инженерную презентацию на EN; возраст и будущая группа ещё требуют проверки.'
 if e['id']=='L327':e['note']=e['note'].replace('наборзакрывался','набор закрывался')
 if e['id'] in ['C1039','C1040','C1041']:e['level']='Международный RECF этап' if e['scope']=='international' else 'Местный квалификатор RECF'
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
f=dict(version=37,checked=CHECKED,status='partial',title='Юго-Восточная Азия · возраст, язык и условия участия',heading='Четыре страны. Свой путь каждому ребёнку.',region_label='ЮГО-ВОСТОЧНАЯ АЗИЯ · ВОЗРАСТ, ЯЗЫК И ОТБОР',family=d['south_europe_focus']['family'],
 conclusion='Самый конкретный международный выезд этого прохода — Vietnam Open 19–21 февраля 2027 года: организатор предусматривает зарубежные команды, а места на мировой финал проверяются отдельно. Remote 18 октября возможен после рекомендации и приглашения. KodingNext подтверждает двуязычное обучение на индонезийском и английском, но новые даты лагерей пока неизвестны.',
 limitations='Первый ограниченный проход четырёх стран. Остальные операторы, школы, национальные квоты и язык судейства ещё требуют проверки. Английский сайт не доказывает английское преподавание, прошедшие смены не стали календарём 2027. Полный мировой охват не достигнут.',
 shortlist=[dict(title='Без перелёта · сначала приглашение',detail='Vietnam Solo Remote 18 октября 2026: зарегистрированная команда Engage, своё поле, робот и камеры. Оператор рассматривает команды из мест без очных событий; нужны рекомендация и приглашение, время согласуется отдельно.',event_ids=['C1040','C029']),dict(title='Ханой · международный зимний кандидат',detail='Vietnam Open 19–21 февраля 2027, приём открывается 20 октября. Оба ребёнка проходят максимальный возраст 12U; класс, окончательные дни программы и английское интервью ещё нужно подтвердить.',event_ids=['C1041','L323','L324']),dict(title='Каникулы и свои инженерные проекты',detail='KodingNext: Оскару RoboCare 4–7, Матвею BioLab / AI 8–11; английский преподавателя конкретной группы проверить. ITEX: выставка 27–28 мая 2027, награждение 29 мая. Детский пропуск и правила конкурса нового выпуска пока условны.',event_ids=['L319','L320','L321','E157','C1025'])],countries=[],steps=[
 dict(title='Подтвердить класс и категорию',detail='Получить школьный класс обоих, возрастную отсечку нового сезона, наставника и допуск зарубежной команды. Названия Junior и 12U не заменяют условия конкретного события.'),
 dict(title='Выбрать одну конкурсную систему',detail='Сначала пробный наставник и один проект, затем совместимый комплект. После трёх лет соревнований нужно проверить, даст ли начальный лагерь достаточно сложную задачу. Инженерный дневник и код должны оставаться работой детей.'),
 dict(title='Проверить смену отдельно от школы',detail='Запросить дату, возрастную группу, технические часы и язык именно robotics. У KodingNext курс занимает шесть часов; у HEC формальный возраст и новая летняя смена ещё неизвестны. Это пока кандидаты, а не основание переезда.'),
 dict(title='Согласовать допуск до поездки',detail='Нужны подтверждённое место, площадка, детский пропуск и итоговый тариф. Для международной награды проверить конкретный протокол и число квалификационных мест. INATRONICS, IISMEX и Manufacturing Indonesia запрещают посещение до 18 лет.')],sources=[])
country_data=[
 ('MYS','Малайзия','Матвей: школьный Junior; Оскар: отдельный младший формат',
  'NROC Junior допускает годы рождения 2017–2019 и назначен на 14 ноября 2026. IYRC имеет Foundation 4–7 и отдельные международные правила, но следующий выпуск ещё не датирован.',
  'NROC Junior подходит в 2026 после проверки школы и иностранного допуска. В 2027 Матвею исполняется 10: нужна новая Primary категория и её правила. WYIE Primary до 12 лет — условный проектный вариант.',
  'IYRC Foundation 4–7 по 2026; новый сезон неизвестен. NRC / NROC начинаются с 7, Soleh Camp — тоже с 7.',
  'Newtonshow и Embassy уже есть в базе. Soleh 7–17 не подтвердил английское техническое преподавание. DRABOT — онлайн с 10 лет, а не очный лагерь для обоих.',
  'Для постоянной базы нужна конкретная школа с младшей командой, наставником и протоколами. Нового досье с доказанным мировым лидерством этот проход не дал.',
  'Куала-Лумпур / Petaling Jaya: проба наставника, NROC и ITEX. Учебный центр My-Robot в Johor — отдельная площадка от соревнования.',
  'У ITEX прошлый FAQ предлагает бесплатный публичный / ученический вход; условия детей 2027 уточнить. Взносы NROC, комплект и школа отдельно. Цена Soleh не опубликована.',
  'Сверить точную категорию и протокол NRC / NROC. Выставочные медали WYIE не являются местом в мировой роботолиге.',
  'Ученик международной школы Малайзии и приезжая зарубежная команда имеют разные условия. NRC и NROC отличаются составом; язык судейства и мировые квоты ещё неизвестны.',
  ['C1021','C1022','C1023','C1024','C1025','C068','L189','L192','L326','L327','E157'],['sasbadi-malaysia','iyrc-asean-malaysia']),
 ('IDN','Индонезия','Двуязычное обучение подтверждено; конкурсный допуск условен',
  'KodingNext прямо подтверждает обучение на индонезийском и английском. IYRC делит младшие категории по школьным классам. WRO Elementary и Entry Level начинаются с 8.',
  'WRO 8–12 и IYRC Grade 3–6 после проверки класса. RoboNext Junior Builder 8–12 получает младший приз, а поездка Beijing относится к старшим 13–19.',
  'RoboCare 4–7; IYRC Kinder / Brickspeed после определения TK или Grade 1–2. Entry Level WRO не подходит в 6 лет.',
  'Четыре содержательных курса KodingNext: робот, AI classifier и разработка игры. Два дня по три часа. Новых дат нет; физическая робототехника только в шести названных филиалах, Bali не обещан.',
  'Протокол IYRC 2026 содержит школы и награды, но один сезон и несколько Gold в категории не доказывают мировое лидерство школы за десять лет.',
  'Jakarta / Kemayoran / Puri для лагеря; YARSI — площадка прошлого IYRC. Surabaya — национальный WRO после обязательного регионального отбора.',
  'По 2026: IDR 800 000 за один курс, 1 300 000 за два. Новый счёт нужен. Три B2B выставки доступны только взрослым; семейная поездка не рассчитана.',
  'Использовать первичный протокол IYRF с дисциплиной и уровнем награды. Gold в Creative может быть наградной группой, а не единственным победителем.',
  'Иностранный школьный класс, команда и язык оценки требуют согласования. INATRONICS, IISMEX и Manufacturing Indonesia не допускают детей до 18.',
  ['C1026','C1027','C1028','C1029','C1030','C1031','C1032','C1033','C1034','L319','L320','L321','L322','E158','E159','E160','E162'],['wro-indonesia','iyrf-indonesia']),
 ('VNM','Вьетнам','Конкретный международный Open и условный дистанционный этап',
  'Vietnam Open 19–21 февраля 2027 предусматривает приезд зарубежных команд. Hanoi 17 октября — квалификатор, Remote 18 октября — по приглашению. Это самостоятельный маршрут RECF.',
  'Engage Elementary 12U после школьной категории. WRO Elementary 8–12; FLL Challenge 9–16 по обзору национального оператора. Квота представлять Вьетнам не обещана.',
  'Максимальный возраст Engage 12U подходит, но младший школьный допуск нужно подтвердить. FLL Explore 6–9 по обзору. Scrimmage 9 октября предназначен для Middle School.',
  'HEC прямо заявляет English STEAM и all-English summer engineering; формальный возраст и будущие даты пока неизвестны. Hanoi Academy 5–16 предлагает English practice, язык технической части не доказан.',
  'До решения о переезде нужны школа, английская программа, конкретная младшая команда, наставник, часы и результаты. Этот проход нового школьного досье не добавил.',
  'Ханой: RECF и пробное занятие HEC. Ho Chi Minh City: ICTCOMM 29 июня–1 июля 2027; Education Zone включает родителей и учеников, детский билет пока нужно уточнить.',
  'RECF: Hanoi $60, Remote $20, Open $90 за команду; сезонный взнос и оборудование отдельно. 210 000₫ за занятие на витрине HEC — не полная стоимость лагеря.',
  'Государственный отчёт подтверждает финал ROBOTACON 2026, иностранных гостей и 44 вьетнамские квоты после отбора. RECF требует своего утверждённого распределения мест.',
  'Приглашение Remote нельзя заменить кнопкой заявки. Даты и двухдневная повестка Hanoi / Open расходятся; окончательное расписание и язык интервью согласовать.',
  ['C1035','C1036','C1037','C1038','C1039','C1040','C1041','C1042','L323','L324','L325','E161'],['recf','robotacon-vietnam']),
 ('PHL','Филиппины','Школьный PRO с 8 лет; Kibo требует другой паспорт',
  'Форма FELTA подтверждает PRO Elementary 8–12 и необходимые документы. Календарь 2026 содержит противоречия; будущий финал не назначен. PhilSA Kibo требует филиппинского гражданства.',
  'PRO Elementary 8–12 после допуска иностранной школы. Новая местная категория FLL ещё не установлена. Philippine Kibo не подходит по заявленному гражданству семьи.',
  'PRO начинается с 8. Конкретный новый FLL Explore или другой шестилетний конкурс в этом проходе не подтверждён. Kibo исключён по гражданству.',
  'Подтверждённый английский роботолагерь с конкретной группой 6/9 этот проход не установил. Рекламный CodeCraft пакет не заменяет возраст, язык и даты лагеря.',
  'DLSZ Vermosa указан как площадка FLL 2026. Это ещё не доказательство лучшей школы или приёма зарубежных детей; новые школьные досье не добавлены.',
  'Metro Manila / Quezon City для FELTA после проверки школы и команды. Переезд требует отдельной проверки наставника и учебной программы.',
  'Новые взносы PRO / FLL и комплект неизвестны. Денежный приз Philippine Kibo не доступен семье без требуемого гражданства.',
  'Проверять первичный протокол с точной дисциплиной, командой и наградой. Принимающая площадка FLL не становится победившей школой автоматически.',
  'Kibo требует Filipino citizenship даже для учеников зарубежных школ. PRO запрашивает медицинский документ, authenticated birth copy, подписи родителя и директора.',
  ['C1043','C1044','C1045','C1046','C1047'],['felta-philippines'])]
for iso,name,verdict,reason,mat,osc,camp,school,city,budget,results,risk,ids,pids in country_data:
 f['countries'].append(dict(iso=iso,name=name,verdict=verdict,reason=reason,mat=mat,osc=osc,camp=camp,school=school,city_route=city,budget=budget,results_check=results,risk=risk,event_ids=ids,profile_ids=pids,school_ids=[]))
d['southeast_asia_focus']=f
sources=[]
for e in new+[byid[i] for i in updated]:sources.append((e['source'],e['title']));sources.extend((r['url'],r['label']) for r in e['references'])
for p in profiles:sources.extend((r['url'],r['title']) for r in p['sources'])
known={s['url'] for s in d['sources']};fk=set()
for url,title in sources:
 if url not in known:d['sources'].append(dict(url=url,title=title,checked=CHECKED,evidence='Прочитан первичный источник; дата, возраст, язык и unknown conditions разделены.'));known.add(url)
 if url not in fk:f['sources'].append(dict(title=title,url=url,checked=CHECKED));fk.add(url)
issues=[
 ('NRC/NROC school/age/team','NROC2homepage vs2–3rules;NRC3teacher. Primarylocal10–12 не globalWRO8–12. Foreignschool/guest/worldquota нужныотдельно.',my_nroc),
 ('Vietnam RECF date/grade conflicts','Hanoi17OctDatesvs2-dayagenda;OpenFeb19–21vs2-dayagenda;ScrimmageMiddle-only приобщем ElementaryENoverview. Болееузкий grade сохранён, невыдуман extra день. Remoteinvitation обязателен.',engage_directory),
 ('RECF precise age / language','12U≤12 на 6May2027, нестрогий under12.Englishmanual не ENjudging. Команда>=2, adultover18.',engage_manual),
 ('IYRC current rules','IndonesiaJunior границывзятыпо officialresults2026, неполныйновый rulebook. IYRCMalaysia2026registrationclosed, new2027unknown.',iyrf),
 ('KodingNext Beijing reward','A4–7/B8–12campvoucher;Beijing толькос Senior13–19.Roboticsbranches6 без Bali. Bilingualteaching прямое;конкретный teacherEN нужен.',ric),
 ('HEC / Hanoi Academy camp language/age','HEC прямо all-English и engineering, но formalage и futuredate необъявлены. HanoiAcademyEnglishpractice не technicalEN.',hec),
 ('Soleh / DRABOT age','Solehcamp7–17vsoperator4–18;DRABOTonlinePrimary10–12, прошёл June2026;EN неустановлен.',byid.get('L326',next(e for e in new if e['id']=='L326'))['source']),
 ('Philippines past date conflicts','PROhomepageJuly, registrationJune13/consentAugSep, scheduleversion8June22–25.Оставлен nextcycle без ICS. A403DepEd непроцитированкакпрочитанный.',ph_schedule),
 ('PhilSA Kibo nationality and tracks','Filipinostudents обязательны;Beginnerunder16newcoding без ISSfinal, RegularElementary–graduate с ISSfinal. Не eligibleMex/Russian семье.',kibo),
 ('ITEX physical days / old policy','2027 баннер 27–28exhibition,29award. Competition/FAQ старые 2024–26fragments:2027childage/Primaryentry ещёусловны.',itex),
 ('MTE / WOCEE / FIRA unresolved','MTEApril8–10,2027—virtualsatelliteawards, не physicalexpo. WOCEE/WOSAS2026dateconflicts/406;FIRAMalaysiafetchtimeout. Неимпортированыкак confirmed2027.', 'https://www.mte.org.my/'),
 ('Philippines camps gap','CodeCraftpromo сампонебесебене age+ENcampterms. Подтверждённый ENcamp6/9 ненайденвэтомограниченномпроходе.','https://www.codecraftlearning.com/fritolay-x-codecraft')]
a=d['completeness_audit'];a['validation_previous']=a['validation'];a.update(version=37,checked=CHECKED,status='partial',scope='Malaysia / Indonesia / Vietnam / Philippines: национальные категории, RECF future dates, camp teaching language и minor exhibition admission',
 conclusion='42 новые карточки:27 соревнований/категорий,9 лагерей/учебныхкандидатов,6 выставок.6 новыхпрофилей;RECF уточнёнпо manual2.0.Все 4 страныостаютсячастичными;школьноговсемирноголидерстванеобъявлено.',
 new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=updated,updated_profile_ids=['recf'],new_school_ids=[],validation=dict(version=37,status='pending',publication='pending'))
a['source_issues'].extend(dict(name=l,status=t,official_alternative=u,checked=CHECKED) for l,t,u in issues)
a['known_backlog'].append(dict(kind='Юго-Восточная Азия',name='Оставшиеся национальные операторы, EN лагеря и school protocols',reason='Cambodia/Brunei/Myanmar/TimorLeste;Laoslocalcamps;FIRA/MTE/WOCEEnewcalendars;PhilippinesEN6/9camp;foreignquotas и ENjudging4countries',url='https://wro-association.org/'))
d['camp_focus']['validation_previous']=d['camp_focus']['validation'];d['camp_focus'].update(version=37,checked=CHECKED,carried_forward_ids=d['camp_focus']['added_ids'],added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=[],validation=dict(version=37,status='pending'))
d['camp_focus']['conclusion']='327 лагерей / учебных программ. SEA проходдобавляет 9 кандидатов:KodingNext прямое bilingualID/EN, HECEnglishengineering с unknownformalage;Soleh7–17, DRABOT10+online снеподтверждённым EN. Новыедаты past летнихсменнепридуманы;мировойохватчастичный.'
d['camp_focus']['routes'].append(dict(name='SEA · реальный язык и возраст отдельного курса',ids=['L319','L320','L321','L322','L323','L324','L325','L326','L327'],detail='KodingNext двуязычный technicalteacher, HanoiHEC прямое ENengineering после agegroup;HanoiAcademyEnglishpractice не technicalEN, Solehmin7, DRABOTmin10 и online.'))
d['expansion_log'].append(dict(version=37,checked=CHECKED,added=len(new),updated_ids=updated,new_profiles=len(profiles),new_schools=0,note='BoundedSEApass:preciseage,specificfutureEngageevents,technicalENroles,adult-onlyexhibits;globalcoveragepartial.'))
a['conclusion']='Добавлены 42 карточки: 27 соревнований / категорий, 9 лагерей / учебных кандидатов и 6 выставок; 6 новых профилей. RECF уточнён по manual 2.0. Четыре страны и мировой календарь остаются частичными.'
d['camp_focus']['conclusion']='327 лагерей / учебных программ. Добавлены 9 кандидатов Юго-Восточной Азии: двуязычный KodingNext и английский HEC с пока неизвестным формальным возрастом; Soleh с 7 и DRABOT онлайн с 10. Новые даты прошедших летних смен не придуманы; мировой охват частичный.'
d['camp_focus']['routes'][-1].update(name='Юго-Восточная Азия · язык и возраст конкретного курса',detail='KodingNext подтверждает двуязычное обучение; HEC — английскую инженерную программу после проверки возраста. English practice Hanoi Academy не доказывает технический EN. Soleh с 7, DRABOT онлайн с 10.')
rp_profile=next(p for p in d['league_guide']['profiles'] if p['id']=='recf')
for c in rp_profile['categories']:
 if c['name']=='Engage':c.update(age='Elementary 12U: 12 лет и младше; Middle 15U: 15 и младше',team='Минимум 2 ученика; взрослый старше 18 и сезонные release forms',age_rule='Возраст включительно на 6 мая 2027; школьный division конкретного этапа отдельно')
for e in new:
 if e['id']=='C1025':e['importance_reason']='Международный конкурс изобретений при ITEX; медаль выставочного жюри не является победой в мировой роботолиге.'
assert len(new)==42 and len(profiles)==6 and len(d['schools'])==32
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=[];used={u for u,_ in sources}
for folder in sorted(W.glob('sources-southeast-asia*v37')):
 if (folder/'receipt.json').exists():
  for r in json.loads((folder/'receipt.json').read_text()):
   if r['url'] in used:receipts.append({k:r[k] for k in ['name','url','status','mime','bytes','sha256','resolved','error'] if k in r})
(ROOT/'data/southeast-asia-source-receipts-v37.json').write_text(json.dumps(dict(checked=CHECKED,method='FreshprimaryHTTPpages/images/PDFsread;imagebannersvisuallyinspected;governmentreportreadwithwebreader. Rawfilesoutsidepublicrepo.',sources=receipts,web_read_primary=[dict(url=vn_gov,claim='ROBOTACON22–23Aug2026nationalfinal,foreignguestsandVietnamesequotas')]),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v37.json');r.setdefault('research_passes',[]).append(dict(version=37,checked=CHECKED,scope='SEA4countries:juniornationalroutes,actualEngagefutureevents,technicalENcampsandminoradmission',added_records=42,new_profiles=6,new_schools=0,status='partial',remaining='AllotherSEAoperators;foreignquota/ENjudging;newcampdates;PHEN6/9camp;national/schoolprotocols;worldwidecoverage'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=37,status='local_checks_pending_publication_pending');rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=37,added=len(new),profiles=len(profiles),updated=updated,world_complete=False)))
