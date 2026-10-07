"""Add bounded South Asia research; keep the prior world inventory intact."""
import ast, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1297 and d['completeness_audit']['version']==30
CHECKED='2026-10-01';new=[];profiles=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['ref','event','profile']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
base_event=event
def add(*args,**kwargs):
 e=base_event(*args,**kwargs);e['region']='Азия';return e
COND='Условно: возраст подходит; конкретный набор, EN, иностранный приём и место подтвердить'
YOUNG='Нет: младше опубликованного минимального возраста'
GLOBAL='https://wro-association.org/competition/categories/'
DIRECTORY='https://wro-association.org/about-wro/association/member-countries/'
india='https://wroindia.org/season-2026/'
pak='https://www.linkedin.com/company/wro-pak/'
sri='https://www.burhani.edu.lk/world-robot-olympiad-sri-lanka-nationals-2026/'
bdro='https://bdro.org/'

# National membership is not permission to claim another country's world quota.
for id,category in [('C921','RoboMission Elementary'),('C922','Future Innovators Elementary')]:
 mission=id=='C921'
 e=add(id,'WRO India · '+category+' · следующий сезон','Индия','Площадка нового сезона не объявлена',india,
  'Elementary 8–12 по национальному описанию 2026; возрастную таблицу нового сезона проверить',
  'Условно: 2017 год подходит по возрастной ступени; национальный / иностранный допуск не подтверждён',YOUNG,
  'Команда 2–3 и взрослый coach. '+('В 2026 RoboMission входил сразу в national; regional отбора не было.' if mission else 'В 2026 Future Innovators: virtual → regional → national; прямой вход в national не обещан.'),
  'Свободный выбор hardware / software в описании 2026; автономный робот до 25 × 25 × 25 см.' if mission else 'Роботизированный проект по теме сезона; прототип, презентация, инженерия и предпринимательская часть.',
  scope='national',evidence='rules',
  cost='RoboMission 2026: INR20 000 / team; тариф нового сезона не объявлен.' if mission else 'В 2026 одна бесплатная FI-команда на школу; это не общий бесплатный вход иностранной семьи.',
  note='National 26–28 августа 2026 в Hyderabad уже завершён; даты 2027 не перенесены из 2026. Нужны национальные условия для иностранной команды, язык защиты и новые правила. Медаль за 1–3 место, процентный badge, участие и world qualification — разные результаты.')
 e['references']=[ref('Глобальные категории и возрастные ступени',GLOBAL),ref('Национальный организатор',DIRECTORY)]
 e['admission_kind']='national_qualification'

e=add('C923','WRO Pakistan · Future Innovators Elementary · следующий сезон','Пакистан','Следующий национальный этап не датирован',pak,
 'Глобальная Elementary 8–12; местный cutoff нового сезона пока не подтверждён',
 'Условно: возрастная ступень подходит; местные правила / иностранная команда не подтверждены',YOUNG,
 'Подтвердить у PSSEC новую регистрацию, школьный / национальный статус команды, coach и язык judging.',
 'Роботизированный проект Future Innovators; local equipment rules нового сезона уточнить.',scope='national',evidence='organizer_report',
 note='Организатор сообщил об Elementary победителях national 4–5 сентября 2026 в Aitchison College, Lahore. Эта дата прошла. Старое руководство 2025 противоречит само себе: 2–3 участника в Composition и обязательные 3 в Coaching; новый размер команды не выведен догадкой. Маркетинговое 6–25 на LinkedIn не заменяет возраст Elementary. Зарубежный world slot семьи не установлен.',
 cost='2025: PKR80 000 / team; это архивный тариф, не цена 2026/27.')
e.update(admission_kind='national_qualification',references=[ref('PSSEC: национальный организатор','https://pssecm2m.com/team/'),ref('Архив 2025 и конфликт team size','https://pssecm2m.com/wro-2025/'),ref('Глобальные категории',GLOBAL),ref('Каталог национальных организаторов',DIRECTORY)])

e=add('C924','WRO Sri Lanka · младший проектный маршрут Elementary','Шри-Ланка','Следующая площадка / дата не объявлены',sri,
 'Elementary опубликована в местных результатах; глобальная FI 8–12, местный cutoff нового сезона уточнить',
 'Условно: возрастная ступень подходит; local category и иностранный / национальный допуск проверить',YOUNG,
 'У Burhani Serendib School уточнить правила национального входа, младший проектный поток и выбор сезона.',
 'Проектный робот, описание решения и демонстрация; числовые local hardware / team правила не получены.',scope='national',evidence='organizer_report',
 note='Сообщение организатора от 6 апреля 2026 описывает завершённый national и Elementary проекты. Syncro-Rise (Leeds International School Matara) указан среди пяти команд на международные соревнования. Это сообщение об отборе, не мировой приз и не многолетний рейтинг школы. Следующие даты и международный допуск приезжей семьи неизвестны.')
e.update(admission_kind='national_qualification',references=[ref('Burhani: действующая robotics-программа','https://www.burhani.edu.lk/robotics/'),ref('Глобальная возрастная ступень',GLOBAL),ref('Национальный организатор',DIRECTORY)])

# Bangladesh's local school condition and the non-qualifying quiz are explicit.
for id,category,url,gear in [
 ('C925','Creative Junior','https://bdro.org/rules/creative-category/','Роботизированное решение по теме; production plan и демонстрация.'),
 ('C926','Physical Computing Junior','https://bdro.org/rules/physical-computing/','Действующий робот + animation story в общей block-coding среде; production plan и файлы проекта.'),
 ('C927','Robotics Quiz Junior','https://bdro.org/rules/robotics-quiz/','Индивидуальные вопросы по робототехнике, электронике, сенсорам и основам программирования.')]:
 quiz=id=='C927'
 e=add(id,'Bangladesh Robot Olympiad · '+category+' · следующий набор','Бангладеш','Online qualifier → Dhaka national; новый сезон не объявлен',url,
  'Junior: Grades1–6 по правилам 2026; требуется документ класса. Год рождения не заменяет класс.',
  'Нет для нынешнего школьного маршрута семьи: главная страница требует обучение в образовательном учреждении Бангладеш',
  'Нет для нынешнего школьного маршрута семьи: требуется обучение в учреждении Бангладеш и подходящий класс',
  'Проверить национальное школьное условие. '+('Индивидуально; обязательный online qualifier.' if quiz else '1–3 участника из одной grade-группы; возможна команда из одного ребёнка; online qualifier обязателен.'),
  gear,scope='national',participation='individual_or_team',priority='P4 — национальное школьное условие не выполнено',evidence='rules',
  note='Online qualifier 28–29 августа и national 11–12 сентября 2026 прошли; даты нового набора неизвестны. '+('Правила прямо исключают Quiz из IRO: его победитель не получает через Quiz право участия в международном IRO.' if quiz else 'National победа даёт доступ к дополнительному international team selection camp; только последующий отбор определяет сборную. Взносы разных этапов и международная поездка оплачиваются отдельно.'),
  language='Quiz: вопросы национального тура прямо предлагаются на Bangla и English.' if quiz else 'Для Physical Computing: все online selection tasks прямо требуют English; язык живой защиты отдельно.' if id=='C926' else 'Полный язык живого judging не установлен; EN-текст правил не является доказательством.',
  languages=('EN','BN') if quiz else ('EN',) if id=='C926' else ())
 e.update(admission_kind='national_school',format='Индивидуальный quiz' if quiz else 'Индивидуально / команда 1–3 одной grade-группы',references=[ref('Национальное школьное условие',bdro)])
 e['reward']='Медаль местного Quiz по результату; международный отбор IRO через Quiz исключён.' if quiz else 'National achievement medal по результату; international selection отдельно. Участие даёт отдельный сертификат.'

# Archived summer curricula are programme candidates, never invented future dates.
robog='https://robog.in/camps'
pdf='https://img1.wsimg.com/blobby/go/894a109f-5da6-4b3f-808b-e8331a5533e4/downloads/78040afb-d0b4-474f-b6f2-971201189d51/SummerCamp2026_ROBO-G_RJ_June_July.pdf?ver=1781801176927'
for id,name,age,mat,osc,gear,cost in [
 ('L236','LEGO Early Robotics','5,5–7 лет','Нет: 9 лет выше максимального возраста 7 этой группы',COND,'Построить и запрограммировать работающую LEGO-модель; вводный уровень.','Архив 2026: INR3 600 за 6 занятий по 1 часу; новая цена неизвестна.'),
 ('L237','Science in Motion with LEGO','7–10 лет',COND,YOUNG,'Конструирование и код интерактивных LEGO-моделей, механика и сенсорные задачи; вводный уровень.','Архив 2026: INR7 500 за 6 занятий; новая цена неизвестна.')]:
 e=add(id,'ROBO-G North Bangalore · '+name+' · кандидат следующего набора','Индия','North Bengaluru · Jakkur; конкретный учебный адрес подтвердить',pdf,age,mat,osc,
  'Следующий holiday набор после закрытого июня–июля 2026. До поездки подтвердить EN, уровень при трёхлетнем опыте детей, иностранный приём и расписание.',gear,
  block='Лагеря',participation='day_camp',priority='P3 — вводная программа, новый набор не подтверждён',cost=cost,evidence='historical_program',date_scope='camp_window',
  note='Брошюра прямо подписана Summer2026; все четыре опубликованных набора прошли. Даты 2027 не придуманы. Два трека одного оператора, не два международных пансиона. Английский в брошюре не подтверждает EN преподавание. Жильё семьи отдельно; сертификат завершения — не соревнование.')
 e['references']=[ref('Оператор: AY2026/27 лагерные направления',robog)]

foundation='https://robog.in/foundation-program'
e=add('L238','ROBO-G · Foundation Program for Robotics Olympiads','Индия','North Bengaluru · Jakkur',foundation,
 '9–15 лет',COND,YOUNG,
 'Очная подготовка WRO / Indian Robotics Olympiad; новый поток, EN и иностранный приём подтвердить.',
 'SPIKE Prime предоставляется; свой laptop. Gyro / line following, My Blocks, debugging, digital LEGO design.',block='Лагеря',participation='day_camp',evidence='program',date_scope='activity_start',
 note='45–50 часов; kit/student1:1, coach/student1:8 по оператору. Прочитанные даты March–May не содержат явного года и не подходят для будущего календаря. В Courses есть отдельное слово Online, но конкретная Foundation-страница говорит In-Person: онлайн-место не обещано. Учебная подготовка не даёт автоматическую квоту WRO.')
e.update(participation='regular',format='Очный учебный курс; размещение семьи отдельно',references=[ref('Обзор курсов: отдельные онлайн / очные предложения','https://robog.in/courses')])

rancho='https://www.rancholabs.com/post/summer-camp-in-noida-2026-give-your-child-a-summer-that-actually-builds-something'
for id,name,gear in [('L239','Robotics','Электроника, Arduino, CAD / 3D-design и собственные демонстрируемые проекты.'),('L240','Game Development','Визуальное программирование, игровые механики и собственная игра; конкретную платформу младшего потока уточнить.')]:
 e=add(id,'Rancho Labs Noida · '+name+' · младший summer-кандидат','Индия','Noida · Sector75, Spectrum Metro Mall, TowerA, 5th floor, Unit504/506',rancho,
  'Grade2–12 в конкретной статье Noida2026; junior поток и school equivalence подтвердить',
  'Условно: только при Grade2+; класс семьи, EN и новый поток подтвердить',
  'Условно: только при Grade2+; 6 лет сами по себе не доказывают этот класс',
  'Очный Noida поток: даты следующего набора, младший grade-track, EN и foreign enrolment уточнить.',gear,
  block='Лагеря',participation='day_camp',priority='P3 — следующий набор и язык не подтверждены',evidence='historical_program',date_scope='camp_window',
  note='Статья относится к лету2026. Общий каталог пишет Grade2–12, но прочитанные ссылки online Robotics / GameDev ведут на Senior6–12. Младший online-допуск не подтверждён. Заявление IIT-backed / certificate опубликовано оператором; независимый документ аккредитации не получен. Сертификат обучения не записан как международная победа.')
 e['references']=[ref('Текущий каталог и разные grade-track ссылки','https://home.rancholabs.com/summer-camps-for-kids-and-teens')]

isa='https://isa.summercamp.indiaspaceweek.org/'
e=add('L241','India Space Academy · Space / AI / Robotics online camp · следующий набор','Индия','Онлайн; timezone / зарубежный доступ и kit delivery уточнить',isa,
 'Classes3–12',
 'Условно: только при Class3+; полный EN поток и новый набор подтвердить',
 'Позже: программа начинается с Class3; класс и младший поток не подтверждены',
 'Следующий онлайн набор после закрытого летнего приёма 2026; запросить English-only либо достаточную EN поддержку в смешанной группе.',
 'Space, AI, robotics, IoT и предпринимательство; live sessions и DIY kits по описанию.',block='Лагеря',participation='day_camp',evidence='historical_program',date_scope='camp_window',
 language='Прямо заявлены Hindi и English; полноценный отдельный EN поток не установлен.',languages=('EN','HI'),
 cost='На странице отдельные workshops INR150; это не доказанная цена полного camp / международной доставки.',
 note='Регистрация 1апреля–20мая2026 закончилась. Будущие даты не опубликованы. Название Space Academy не доказывает государственную / ISRO аккредитацию; это программа названного оператора. Сертификат загрузки проекта отдельно от олимпиадной награды.',themes=('robotics','ai','technology','coding'))
e.update(language_mode='bilingual',participation='online',format='Онлайн программа; проживание отсутствует',language_certainty='HI/EN указаны прямо; объём EN и способность учиться без Hindi нужно подтвердить.')

pssec='https://pk.linkedin.com/company/pssecm2m'
e=add('L242','PSSEC · Mission to Mars · robotics / rover programme','Пакистан','Karachi · DHA Phase6; реальную площадку подтвердить',pssec,
 'Grades3–11 в профиле самого оператора',
 'Условно: только при Grade3+; язык, актуальное расписание и foreign enrolment уточнить',
 'Позже: младшая группа ниже Grade3 не опубликована; точный класс Оскара неизвестен',
 'Регулярная / проектная программа: запросить новый конкретный поток, EN и уровень самостоятельной rover-инженерии.',
 'Rover engineering, robotics, 3D-printing и space-science curriculum по оператору; kit / длительность потока неизвестны.',
 block='Лагеря',participation='day_camp',evidence='program',date_scope='activity_start',
 note='Главный сайт описывает Mission to Mars, но адрес Olympus Mons / Red Planet — часть бренда, не адрес для поездки. В карточке использована реальная локация Karachi из профиля оператора. Дата 2025 Global Mission не перенесена на 2026/27. EN не выведен из языка страницы.')
e.update(participation='regular',format='Проектное обучение; формат и новое расписание подтвердить',references=[ref('Сам оператор: Mission to Mars','https://pssecm2m.com/')])

bbt='https://bbt.edu.pk/kids/'
e=add('L243','BBT Kids Lahore · STEM Robotics · механическая инженерия','Пакистан','Lahore · 444-Q DHA Phase2; адрес потока уточнить',bbt,
 '6–15 лет: STEM Robotics прямо от6, другие BBT курсы не от6',COND,COND,
 'Следующий набор и EN подтвердить; сверить сложность с трёхлетним соревновательным опытом детей.',
 '12 hands-on build sessions; kits на площадке. FAQ прямо говорит mechanical rather than programmed.',
 block='Лагеря',participation='day_camp',priority='P3 — вводная механика, не соревнование',evidence='program',date_scope='camp_window',
 note='Описание Summer2026 не содержит точной даты будущего набора. Длительность два месяца не изображена как непрерывный лагерь. Spoken English — отдельный курс, не доказательство EN robotics. Это mechanical STEM, не полноценная программа автономного кода / AI.',themes=('robotics','technology'))
e['period']='Два месяца, 12 build sessions; следующий старт неизвестен'
e=add('L244','BBT Kids Lahore · AI for Kids / Entrepreneurship · будущая ступень','Пакистан','Lahore · конкретный поток уточнить',bbt,
 '12+ по конкретному FAQ; общий баннер 6–15 не заменяет этот порог',YOUNG,YOUNG,
 'Вернуться к направлению после12лет; для нынешних6/9 прямой младший допуск не заявлен.',
 'No-code / low-code AI и предпринимательский проект; отдельные курсы, не младшая Robotics группа.',
 block='Лагеря',participation='day_camp',priority='P4 — обоим пока младше12',evidence='program',date_scope='camp_window',
 note='FAQ ограничивает AI, entrepreneurship, math и Spoken English возрастом12+. Табличная отметка6–15 относится к общему camp. Подготовка проекта / pitch не названа внешней конкурсной победой; EN технического курса не подтверждён.',themes=('ai','technology'))

meeti='https://www.meeti.lk/admissions'
e=add('L245','M.E.E.T.I. · младший Robotics Technology · иностранная заявка','Шри-Ланка','Sri Lanka · площадку / online формат подтвердить',meeti,
 'ICKRCT: Grades4–5; возраст в годах не опубликован',
 'Условно: только при Grade4–5; форма прямо предусмотрена для иностранных детей, EN и текущий набор неизвестны',
 'Позже: курс Grade4–5; класс, эквивалентность и младшая программа не подтверждены',
 'Использовать General Application route для foreign / international-school students; сначала подтвердить класс, EN, расписание и полный тариф.',
 'Учебный robotics technology course; платформу и junior syllabus подтвердить. Advanced IHDRCE-проекты не приписаны Grade4–5.',
 block='Лагеря',participation='day_camp',evidence='program',date_scope='activity_start',
 note='Admissions2026 прямо выделяет иностранные заявки. Это возможность подать документы, не зачисление семьи. Название International Certificate и пометка For Edu Purposes не доказывают университетский диплом или world award. Учебный курс отделён от бесплатной схемы для government schools.')
e.update(participation='regular',format='Учебный курс; место, длительность и текущий поток уточнить',admission_kind='foreign_application')
e=add('L246','M.E.E.T.I. · бесплатная robotics scholarship · школьное ограничение','Шри-Ланка','Sri Lanka · отдельная схема для government schools',meeti,
 'Grades3–9, только ученики государственных школ Sinhala / English medium',
 'Нет для нынешнего школьного маршрута: опубликовано government-school условие',
 'Нет для нынешнего школьного маршрута: government-school условие и Grade3–9',
 'Бесплатный трёхмесячный курс с robot kit только для указанной школьной группы; не общий foreign-family camp.',
 'Mobile Robot Kit предоставляется по admissions page; syllabus и обучение на EN отдельно.',
 block='Лагеря',participation='day_camp',priority='P4 — требуется местная государственная школа',cost='No course fees / free robot kit по специальной схеме; другие расходы не описаны.',evidence='rules',date_scope='activity_start',
 note='English-medium школа — условие школьного статуса, не доказательство EN преподавания на курсе. Отдельная General Application форма для foreigners не отменяет узкое условие этой стипендии.')
e.update(participation='regular',format='Трёхмесячный курс; national school scholarship',admission_kind='national_school')

dolex='https://dolex.lk/'
e=add('L247','Dolex Global Academy · English robotics / coding · старшая школьная ступень','Шри-Ланка','Kirindiwela · Gampaha',dolex,
 'Grades6–11; эквивалентность классов подтверждается отдельно',
 'Позже: Grade6–11; нынешний класс семьи не подтверждён',
 'Позже: Grade6–11; младшая robotics группа не заявлена',
 'Вернуться при подходящем классе; запросить уровень проектов, иностранный приём и конкретное расписание.',
 'Robotics / engineering и coding от Scratch к Python по программе оператора.',
 block='Лагеря',participation='day_camp',priority='P4 — старшая grade-ступень, не младший camp',evidence='program',date_scope='activity_start',
 language='Прямо заявлены 100% English medium, every subject / every session.',languages=('EN',),
 note='EN технической программы подтверждён текстом, но возрастная ступень старше текущего семейного маршрута. Demo Day / orientation на странице рядом с OpenDay2025 не использованы как будущие даты. Vendor отзывы / world-class формулировки не доказательство мирового лидерства.')
e.update(language_mode='primary',participation='regular',format='After-school курс Grades6–11; проживание семьи отдельно')

cad='https://bdro.org/event/3d-modeling-cad-workshop-for-absolute-beginners/'
e=add('L248','BdRO / BdOSN · 3D Modeling CAD Workshop · 9 октября2026','Бангладеш','Dhaka · Dhanmondi, 758 Satmasjid Road',cad,
 'Grades4–12; без опыта CAD / 3D modeling',
 'Условно: только при Grade4+; класс, EN и иностранный приём подтвердить',
 'Позже: workshop начинается с Grade4; возраст6 не подтверждает этот класс',
 'Запись до6октября; school ID / birth certificate для проверки. Иностранный доступ и EN instructor не подтверждены.',
 'CAD workspace, sketches / extrusions / assemblies и подготовка 3D-print модели; laptop + mouse желательны.',
 block='Лагеря',start='2026-10-09',deadline='2026-10-06',participation='holiday_workshop',evidence='event_page',date_scope='session_days',
 cost='BDT1500; bKash при записи. Организатор указывает non-refundable / нельзя отменить.',
 note='10:00–17:00 Asia/Dhaka; питание не предоставляется, можно принести своё. Без laptop оператор предлагает совместную практику. Сертификат завершения — учебный, не международная олимпиадная победа. Очень короткий срок для поездки из Коста-Рики; не рекомендация бронировать без grade / EN допуска.',themes=('technology','robotics'))
e['sessions']=[dict(date='2026-10-09',start_time='10:00',end_time='17:00',timezone='Asia/Dhaka',topic='3D Modeling / CAD',time_note='Опубликованный workshop slot; место семьи не подтверждено.')]

def category(name,age,team,hardware,entry,rule='Правила прочитанного сезона; новый набор проверяется отдельно'):
 return dict(name=name,age=age,team=team,hardware=hardware,entry=entry,age_rule=rule)
profile('wro-india','WRO India · национальные маршруты','regional','Elementary8–12; Junior11–15; Senior14–19; FE14–22',
 'RoboMission и Future Innovators имеют разные точки входа. Индийский national slot не подтверждает право иностранной команды на world quota.',
 [category('RoboMission Elementary','8–12','2–3 + coach','Свободный выбор по правилам2026','В2026 сразу national; без regionals'),category('Future Innovators Elementary','8–12','2–3 + coach','Проектный робот / prototype','В2026 virtual → regional → national')],
 ['C921','C922'],'Новый сезон / иностранный team status → выбранная категория → national → отдельная международная квота.',
 ['Возраст, национальный team status, coach и новый регламент.','Прямой national вход RoboMission не отменяет правила допуска и ограничение мест.'],
 ['National2026 уже завершён; даты2027 не выдуманы.','Одна бесплатная FI-команда на школу — узкое предложение.','Badge за процент баллов не равен медали за место.'],
 [('WRO India2026: categories / progression',india),('Глобальные категории',GLOBAL)],age_tags=('9','10-12','teen'))
profile('wro-pakistan','WRO Pakistan / PSSEC','regional','Elementary: глобальная ступень8–12; local cutoff нового сезона уточнить',
 'Национальный FI Elementary существует и имеет объявленных победителей2026. Новый иностранный вход / world quota семьи неизвестны.',
 [category('Future Innovators Elementary','Глобальная8–12; местный новый cutoff неизвестен','Новый team size уточнить; старый текст противоречив','Проектный робот','У PSSEC подтвердить local / foreign registration')],
 ['C923'],'Local rules и team status → national → международный отбор отдельным решением.',
 ['Не переносить общий баннер6–25 в категорию Elementary.','Coach обязателен в архивном local guide; новые условия проверить.'],
 ['2026national4–5сентября прошёл.','Архив2025:2–3 versus обязательные3 участника; правило не выбрано догадкой.','Национальные победы школ не записаны как мировые.'],
 [('WRO Pakistan: сообщения самого организатора',pak),('PSSEC: национальный organizer','https://pssecm2m.com/team/'),('Архив local guide2025','https://pssecm2m.com/wro-2025/'),('Глобальные категории',GLOBAL)],age_tags=('9','10-12','teen'))
profile('wro-srilanka','WRO Sri Lanka / Burhani Serendib School','regional','Elementary в local result; глобальная8–12, местное правило проверить',
 'Опубликован младший проектный national result2026 и international selection. Не установлены новый календарь и foreign-family admission.',
 [category('Elementary project route','Local cutoff не получен; глобальная FI8–12','Местные team правила нового сезона уточнить','Роботизированное решение и показ проекта','National organizer Burhani; foreign entry неизвестен')],
 ['C924'],'Подтвердить новый сезон, категорию и team status → national → отдельный international selection.',
 ['Возраст и класс отдельно.','Протокол local / world результата и название конкретной награды отдельно.'],
 ['Перечисленные Elementary школы — кандидаты на дальнейший школьный аудит.','Сообщение про international selection не доказывает international prize.'],
 [('Burhani: national2026 results',sri),('Школьная robotics programme','https://www.burhani.edu.lk/robotics/'),('Глобальные категории',GLOBAL)],age_tags=('9','10-12','teen'))
profile('bdro','Bangladesh Robot Olympiad / IRO Bangladesh Open','regional','JuniorGrades1–6; Senior7–12; обучение в учреждении Бангладеш',
 'Два инженерных Junior маршрута и отдельный индивидуальный Quiz. Название Open не отменяет местное школьное условие.',
 [category('Creative Junior','Grades1–6','1–3 одной grade-группы','Проектный робот','Online qualifier → national → selection camp'),category('Physical Computing Junior','Grades1–6','1–3 одной grade-группы','Робот + animation в block-coding среде','Online qualifier → national → selection camp'),category('Robotics Quiz Junior','Grades1–6','Индивидуально','Written quiz Bangla / English','Online qualifier → national; НЕ ведёт в IRO')],
 ['C925','C926','C927'],'Школьный допуск → mandatory online qualifier → national; Creative / Physical ещё проходят международный selection camp.',
 ['Документ grade с датой выдачи; максимальный класс в году сезона.','Члены одной команды должны быть в одной Junior / Senior группе.','Формальное принятие команды предшествует оплате; взносы этапов отдельные.'],
 ['Quiz прямо не является категорией международного IRO.','Национальная победа не гарантирует выбор в сборную.','EN online tasks Physical подтверждены; это не доказательство EN camp instructor.','Даты нового сезона неизвестны.'],
 [('Школьный допуск',bdro),('Creative правила','https://bdro.org/rules/creative-category/'),('Physical Computing правила','https://bdro.org/rules/physical-computing/'),('Quiz правила: no IRO selection','https://bdro.org/rules/robotics-quiz/')])
for p in profiles:
 p['language']='См. конкретный этап; EN-сайт не доказывает EN judging. BdRO Physical online tasks требуют EN; Quiz предоставляет вопросы BN/EN.' if p['id']=='bdro' else 'Язык национальной защиты / judging не подтверждён; уточнить отдельно.'
import re
def polish(value,key=''):
 if isinstance(value,str) and key not in ['id','source','url','start','end','deadline','checked'] and not value.startswith('http'):
  value=re.sub(r'\b(Grade|Grades|Class|Classes|Elementary|Junior|Senior|Summer|OpenDay)(?=\d)',r'\1 ',value)
  value=re.sub(r'\b(до|от)(?=\d)',r'\1 ',value)
  value=re.sub(r'(\d)(?=октября|сентября|апреля|мая|ноября|лет\b)',r'\1 ',value)
  value=re.sub(r'\b(202[567])(?=[A-Za-zА-Яа-я])',r'\1 ',value)
  return value
 if isinstance(value,list):return [polish(v,key) for v in value]
 if isinstance(value,dict):return {k:polish(v,k) for k,v in value.items()}
 return value
new=[polish(e) for e in new];profiles=[polish(p) for p in profiles]
assert len(new)==20 and len(profiles)==4
assert not ({p['id'] for p in profiles}&{p['id'] for p in d['league_guide']['profiles']})
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide'].update(version=31,checked=CHECKED)
sources={e['source'] for e in new}
sources.update(r['url'] for e in new for r in e.get('references',[]))
sources.update(s['url'] for p in profiles for s in p['sources'])
existing={s['url'] for s in d['sources']}
for url in sorted(sources-existing):
 d['sources'].append(dict(url=url,title='Южная Азия: первичная программа / правила / сообщение организатора',checked=CHECKED,evidence='Прочитан первичный источник; допуск, новый набор, язык и архивные условия разделены.'))
issues=[
 dict(name='BdRO: Open и международный путь',detail='Локальный школьный gate сохраняется; Quiz не ведёт к IRO, national medal не гарантирует выбор в сборную.',url=bdro),
 dict(name='Pakistan: current result / archived rules',detail='Сообщения2026 подтверждают national; local2025 guide имеет конфликт team size и устаревшую цену. Новый допуск не выведен из маркетингового6–25.',url=pak),
 dict(name='Sri Lanka: national selection ≠ world prize',detail='Школьные names в national2026 не использованы как независимый мировой рейтинг.',url=sri),
 dict(name='ROBO-G: лето2026 и Foundation',detail='Летние даты прошли; Foundation-даты без явного года не вынесены в future calendar. EN instruction не подтверждён.',url=robog),
 dict(name='Rancho: junior banner / senior online links',detail='Junior2–12 указан для summer / Noida; прочитанные online ссылки — senior6–12. Доступ младших online не обещан.',url='https://home.rancholabs.com/summer-camps-for-kids-and-teens'),
 dict(name='BBT: возраст разных курсов',detail='Robotics от6 механическая; AI / entrepreneurship от12 по FAQ. Баннер6–15 не расширяет AI admission.',url=bbt),
 dict(name='M.E.E.T.I.: две разные формы',detail='Foreign General Application существует; бесплатная government-school scholarship не становится открытым иностранным camp. Junior4–5 отдельно от advanced-after-O/L syllabus.',url=meeti),
 dict(name='India Space Academy: смешанный язык',detail='HI/EN указаны прямо, English-only поток не установлен; INR150 относится к workshop, не всему camp.',url=isa),
 dict(name='Dolex: EN и старшая ступень',detail='EN technical instruction подтверждён; Grade6–11 и даты рядом сOpenDay2025 не превращены в младший future camp.',url=dolex),
 dict(name='Coral / RoboSticks: устаревшая поисковая карточка',detail='Прочитанный нынешний сайт содержит preschool / clubs, но не подтверждает найденный в поиске summer robotics offer. Лагерная карточка не добавлена.',url='https://corallearning.net/')]
issues=[dict(name=s['name'],status=s['detail'],official_alternative=s['url']) for s in issues]
a=d['completeness_audit'];a['validation_previous']=a['validation'];a.update(version=31,checked=CHECKED,status='partial',
 scope='Ограниченный первичный аудит Южной Азии: Индия, Пакистан, Бангладеш и Шри-Ланка; национальные маршруты и camp / learning кандидаты. Мировое исследование продолжается.',
 conclusion='Добавлены 20 карточек и 4 национальных профиля. Подтверждён foreign application route M.E.E.T.I.; явно отмечены grade / national school gates, смешанный EN/HI, старшие ступени и закрытое лето2026. Полный мировой и страновой аудит не завершён.',
 new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=[],new_school_ids=[],
 validation=dict(version=31,status='pending',publication='pending'))
a['source_issues'].extend(issues)
a['known_backlog'].append(dict(kind='Южная Азия',name='Новые наборы, иностранный допуск и младший EN',reason='Полные country calendars, Bangladesh WRO / local camps, Pakistan / Sri Lanka actual6+English programmes, India2027 cohorts, junior online Rancho, текущие команды и school award protocols остаются не закрытыми.',url=india))
for item in a['known_backlog']:
 if item['name']=='Постоянные школы и junior команды':item['reason']='25 школьных досье; страны и кампусы покрыты частично. Нужен более широкий аудит текущих команд, национальных / мировых протоколов, языка и иностранного приёма.'
for row in a['continents']:
 if row['name']=='Азия':row['remaining']='Добавлены India camp candidates и первые Pakistan / Bangladesh / Sri Lanka маршруты. Не все national qualifiers, языки и иностранный приём закрыты; другие страны Азии исследованы частично.'
c=d['camp_focus'];c['validation_previous']=c['validation'];c.update(version=31,checked=CHECKED,added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=[],carried_forward_ids=c['added_ids'],validation=dict(version=31,status='pending'))
c['routes'].extend([
 dict(name='Индия · уровень для каждого ребёнка',detail='Оскар: ROBO-G Early Robotics5,5–7. Матвей: Science in Motion7–10 / Foundation9–15. Это кандидаты нового набора: English, класс, календарь и иностранный приём ещё проверяются; уровень вводных групп может быть слишком простым после трёх лет соревнований.',ids=['L236','L237','L238','L239','L240','L241']),
 dict(name='Пакистан · механика отдельно от AI',detail='PSSEC Mission to Mars требуетGrade3–11; BBT Robotics6+ механическая, AI12+. Прочитанное описание не подтверждает EN занятия или новое лагерное расписание.',ids=['L242','L243','L244']),
 dict(name='Шри-Ланка · foreign application и школьные gates',detail='M.E.E.T.I. принимает General Application от иностранцев; младшая RoboticsGrade4–5, EN неизвестен. Бесплатная схема только government schools. Dolex100%EN robotics начинается сGrade6–11.',ids=['L245','L246','L247']),
 dict(name='Бангладеш · CAD и реальные границы допуска',detail='CAD9октября2026, запись до6октября,Grade4–12, BDT1500; EN / foreign admission неизвестны. BdRO JuniorGrades1–6 национальный, требуется местная школа; Quiz не ведёт к IRO.',ids=['L248','C925','C926','C927'])])
c['source_issues'].extend(issues)
c['gaps'].append('Южная Азияv31: только часть операторов и национальных маршрутов. Нет подтверждённого открытого EN-пансиона для обоих6/9; India2027 / Pakistan / Sri Lanka младшие EN cohorts и Bangladesh local camp foreign admission ещё нужны.')
d['expansion_log'].append(dict(version=31,checked=CHECKED,added=len(new),updated_ids=[],new_profiles=4,new_schools=0,note='South Asia: age / grade / local school gates; archived camps without invented dates; foreign application and EN evidence labelled; worldwide incomplete.'))
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v31.json')
r.setdefault('research_passes',[]).append(dict(version=31,checked=CHECKED,scope='South Asia: India / Pakistan / Bangladesh / Sri Lanka',added_records=20,new_profiles=4,new_schools=0,status='partial',remaining='Новые наборы и полные country calendars, grade / birthday, EN-only teaching и foreign admission; мировая цель остаётся активной.'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=31,status='local_checks_pending_publication_pending')
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=31,added=20,profiles=4,world_complete=False)))
