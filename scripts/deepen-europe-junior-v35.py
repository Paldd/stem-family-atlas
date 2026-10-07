"""Third CHE/ESP/FRA pass: concrete sessions, language roles and qualification gates."""
import ast, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
W=ROOT.parent/'stem-family-atlas-work'
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert d['completeness_audit']['version']==34 and len(d['events'])==1398
CHECKED='2026-10-01';new=[];profiles=[];byid={e['id']:e for e in d['events']}
for node in ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text()).body:
    if isinstance(node,ast.FunctionDef) and node.name in ['ref','event','profile']:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
def add(*a,**k):
    e=event(*a,**k);e['region']='Европа';return e
COND='Условно: возраст подходит; подтвердить уровень, место и приём иностранной семьи'
YOUNG='Нет: младше минимума этой группы'
def regular(e,period):
    e.update(participation='regular',format='Регулярная учебная программа; не каникулярный лагерь',period=period)
faq='https://www.first-lego-league.org/en/faq'
f8='https://www.first-lego-league.org/en/divisions/future-edition-8'
f5='https://www.first-lego-league.org/en/divisions/future-edition-5'
e=add('C972','FIRST LEGO League Switzerland · Future Edition 8+ · BIOGLOW 2026/27','Швейцария','Swiss regional event через JOIN; дата не получена',f8,
    '8–16 и Grades 4–10; класс Матвея неизвестен',
    'Условно: 9 лет входит в диапазон; проверить Grade 4–10 и командную категорию',YOUNG,
    'School / community group до 24; отдельная команда до 8 и 1–2 coaches на группу. Иностранная команда может участвовать, но не проходит дальше через чужую страну.',
    'Два новых Computer Science & AI 8+ / 11+ комплекта на команду; SPIKE / EV3 не совместимы. Для 8+ нужен дополнительный hardware.',
    deadline='2026-10-31',scope='national',cost='Для группы 8: EUR250 + season set EUR140 + CH logistics EUR42 + event EUR100 / team; два robot kits отдельно.',
    note='Опубликован прямой маршрут regional → DACH Final для местных Future-команд; это не обещанная квота FIRST Worlds. Местные даты в динамическом JOIN ещё не получены. Регистрация без event до 31 марта 2027 — другой маршрут. Язык защиты обычно официальный язык страны; EN нужно согласовать.',evidence='rules')
e.update(references=[ref('Иностранные команды / квалификация / язык',faq)],deadline_label='Регистрация с участием в event',deadline_note='31 октября 2026; точный час не указан. Место семьи не подтверждено.')
e=add('L278','FIRST LEGO League Switzerland · Future Edition 5+ · учебная группа','Швейцария','Школа / клуб / собственная группа',f5,
    '5–7 и Grades 1–3; точное соответствие класса подтвердить','Нет: старше диапазона 5–7',COND,
    'Учебная группа до 24 детей, команды до 4, 1–2 coaches. В сезоне 2026/27 официальных завершающих events нет.',
    'Один новый Computer Science & AI 5+ комплект на четыре ребёнка; планшет / ноутбук. Старый SPIKE не совместим.',block='Лагеря',participation='day_camp',deadline='2027-03-31',evidence='program',
    cost='Группа 8: EUR150 programme + EUR70 season sets + EUR42 CH logistics; robot kits отдельно.',
    note='Регистрация и задания с 1 октября 2026. Это программа для обучения с собственным школьным / клубным показом; официальной конкурентной медали или мирового отбора нет. EN материалы не доказывают EN преподавание.')
regular(e,'Сезон 2026/27; свою группу и расписание нужно организовать')
e['deadline_label']='Регистрация учебной группы без официального event'

# Concrete branch menus control the course, not the generic Robotics course calendar.
tsa='https://online.techsparkacademy.ch/robotics-course/'
gen='https://leman.techsparkacademy.ch/geneva-day-camps/'
lau='https://leman.techsparkacademy.ch/lausanne-camps/'
tsas=[('Genève · Institut Florimont',gen,[('2026-10-19','2026-10-23',890),('2027-03-29','2027-04-01',790),('2027-07-12','2027-07-16',890),('2027-07-19','2027-07-23',890),('2027-08-17','2027-08-20',790),('2027-10-26','2027-10-29',790)]),
      ('Lausanne / Pully · Collège Champittet',lau,[('2026-10-12','2026-10-16',890),('2027-03-30','2027-04-02',790),('2027-07-12','2027-07-16',890),('2027-07-19','2027-07-23',890),('2027-08-16','2027-08-19',790),('2027-10-12','2027-10-15',790),('2027-10-18','2027-10-21',790)])]
i=279
for city,url,dates in tsas:
    for start,end,cost in dates:
        e=add('L'+str(i),'TechSpark · Animation & Game Design Junior · '+city+' · '+start,'Швейцария',city,url,
            'Junior от 7 лет в конкретной смене; общий course catalog 7–10',COND,
            YOUNG if start.startswith('2026') else 'Условно только после 7-летия; дата рождения и граница выбранной смены неизвестны',
            'Публичная регистрация конкретной смены; выбрать Animation & Game Design. Иностранное место, уровень и возраст на день начала подтвердить.',
            'Animation / game creation; отдельный LEGO Robotics в меню этих смен не перечислен.',block='Лагеря',start=start,end=end,participation='day_camp',date_scope='camp_window',
            cost=f'Junior CHF{cost} / смена; lunch включён по branch page, жильё и поездка отдельно.',themes=('games','coding'),languages=('EN','FR'),
            language='Все инструкторы этой площадки bilingual English/French по конкретной branch page.',
            note='09:30–15:00. Это датированные смены одной учебной программы в двух городах, не независимые международные лагеря. Python Junior начинается с 10, AI / cybersecurity — с 13: эти пороги не перенесены на Game Design. При трёхлетнем опыте согласовать сложность собственного проекта.')
        e.update(language_mode='bilingual',start_time='09:30',end_time='15:00',timezone='Europe/Zurich',language_certainty='EN/FR прямо указаны для инструкторов конкретной площадки; место и состав группы не подтверждены.')
        i+=1
assert i==292
details=json.loads((W/'urls-europe-junior-details-v35.json').read_text())
for index,(start,end) in enumerate([('2026-10-05','2026-10-09'),('2026-10-12','2026-10-16')]):
    url=details['techlabs_battle'+str(index)]
    e=add('L'+str(292+index),'TechLabs Zürich · Battle Bots VEX IQ · '+start,'Швейцария','Zürich · Hohlstrasse201',url,
        'Заголовок 8–14, поле Age9+; в 8 лет допуск нельзя обещать',COND,YOUNG,
        'Enrollment open to all students; согласовать EN-помощь, final age rule и наличие места. Внутрилагерный турнир не равен VEX Worlds qualifier.',
        'VEX IQ, VEXcode, сенсоры, механика, CAD / 3D-печать и итерации.',block='Лагеря',start=start,end=end,participation='day_camp',date_scope='camp_window',
        cost='CHF525 полдня09–12:30 или CHF990 полный день09–17; поездка / семейное жильё отдельно.',evidence='program',
        note='Course Language: EN & FR supported. Это явно помощь на EN/FR; основной язык курса не установлен. На 5–9 октября есть противоречие: Available places8 и кнопка waiting list. На 12–16 октября указаны5 мест и Register now. Эти числа — снимок, не бронь; перед поездкой проверить доступ.')
    e.update(language_mode='support',support_languages=['EN','FR'],language='EN / FR supported; основной технический язык не установлен.',references=[ref('Основная программа Battle Bots',json.loads((W/'urls-europe-junior-final-v35.json').read_text())['techlabs_battle'])])
for index,(start,end) in enumerate([('2026-10-05','2026-10-09'),('2026-10-12','2026-10-16')]):
    e=add('L'+str(294+index),'TechLabs Zürich · Junior STEM Inventors · '+start,'Швейцария','Zürich · Hohlstrasse201',details['techlabs_invent'+str(index)],
        'Booking Ages5–9; описание6–8 → границу 9 лет уточнить',
        'Условно: 9 лет указан в booking, но выше6–8 в описании; подтверждение нужно',COND,
        'Обе смены показывают waiting list, несмотря на Available places8; сначала выяснить реальный статус и верхний возраст.',
        'LEGO / VEX / micro:bit / Neuron; механизмы, сенсоры, 3D-печать и свой проект.',block='Лагеря',start=start,end=end,participation='day_camp',date_scope='camp_window',
        cost='CHF525 полдня09–12:30 или CHF990 полный день09–17; custom schedule отдельный счёт.',languages=('EN','DE'),language='Course Language прямо English & German.',evidence='program',
        note='Не открытый набор по одному счётчику мест: кнопка требует waiting list. Индекс выдаёт 09:00–09:15, но детальная страница даёт реальные варианты полдня / полного дня; использована подробная страница. Короткая инженерная подготовка, не мировая лига и не подтверждённый международный лидер.')
    e.update(language_mode='bilingual',language_certainty='EN/DE опубликованы как Course Language конкретной смены; место ещё не получено.')
ec='https://www.ecolint-camps.ch/en/camps/introduction-robotics-10'
ech='https://www.ecolint-camps.ch/en'
e=add('L296','Ecolint Genève · Introduction to Robotics · осень2026','Швейцария','Genève · La Grande Boissière',ec,
    'Booking5–7; body5–6; Оскар6 входит в оба диапазона','Нет: 9 лет выше обеих границ',COND,
    'Публичная регистрация до16 октября15:00; уточнить EN-группу, свободные места и иностранный приём. School admission отдельно.',
    'Простые роботы и основы coding; уровень начальный, после трёх лет опыта может быть простым.',block='Лагеря',start='2026-10-19',end='2026-10-23',deadline='2026-10-16',participation='day_camp',date_scope='camp_window',
    cost='CHF640 / неделя; 09–17, семейное жильё отдельно.',languages=('EN','FR'),language='Оператор прямо обещает bilingual EN/FR coaching и общение на предпочитаемом языке ребёнка.',
    note='Сайт допускает5–7 в booking, описание5–6: не обещан семилетний допуск. Летнюю смену29июня–3июля2026 не выдали за будущую. Общий сайт bilingual относится к лагерям; точного распределения инструкторов этой группы нет.')
e.update(language_mode='bilingual',references=[ref('Язык camps и preferred language',ech)],deadline_label='Регистрация лагеря',deadline_note='16 октября2026,15:00 по странице booking; timezone отдельно подтвердить.')
e=add('L297','Ecolint · Robotics EV3 8–13 · кандидат следующего набора','Швейцария','Campus des Nations · Genève; следующую площадку подтвердить',
    'https://www.ecolint-camps.ch/fr/camps/robotique-10','8–13 по опубликованной технической группе',COND,YOUNG,
    'Ждать нового конкретного EV3-потока; старые даты30июня–4июля2025 не повторять в2027.',
    'LEGO EV3 и Space Challenge; уровни от beginner до advanced.',block='Лагеря',participation='day_camp',evidence='historical_program',languages=('EN','FR'),
    language='Общая политика Ecolint camps EN/FR; язык нового EV3-потока и наличие англоязычного наставника подтвердить.',
    note='Это архив конкретного Robotics8–13, а не подтверждённая осенняя смена2026. В актуальном индексном календаре19–23октября прочитан только младший Introduction, поэтому второй семейный robot slot не обещан.')
e.update(language_mode='bilingual',references=[ref('Общая языковая политика camps',ech)],period='Следующая датированная робототехническая смена не установлена')
td='https://www.tandem-ims.ch/hubfs/Flyer_ASC_A4_STEAM%2020252026.pdf'
e=add('L298','Tandem IMS / TechLabs · VEX IQ STEAM6–9 · регулярный клуб','Швейцария','Zürich · Seefeldstrasse111',td,
    '6–9 в PDF2025/26; новый возрастной срез подтвердить',COND,COND,
    'Курс нужно бронировать на весь semester; минимум5 детей. Приём внешних учеников и сезон2026/27 не установлен.',
    'VEX IQ, конструирование и робототехнические состязания в конце семестра.',block='Лагеря',participation='day_camp',evidence='historical_program',
    cost='CHF45 /75мин;18 занятийCHF810 или15CHF675 по2025/26. Новый тариф не объявлен.',languages=('EN','DE'),language='PDF конкретного клуба: bilingual English / German.',
    note='Mix and Match и указанные Mondays относятся к2025/26. Локальные состязания курса не являются автоматически официальной мировой квалификацией. Название Center of Excellence — самоописание, не подтверждённый школьный мировой титул.')
e['language_mode']='bilingual';regular(e,'Понедельники16:00–17:15 по2025/26; текущий semester и места подтвердить')
issh='https://www.issh.ch/calendar/2026-07-13/techlabs-summer-camp-2026/'
e=add('L299','IS Schaffhausen / TechLabs · robotics7–10 · следующий набор','Швейцария','Schaffhausen · школаISSH',issh,
    '7–10 для младшего Robotics; Drone group11+ отдельно',COND,'Кандидат только после7лет; летом2027 день рождения и возрастную границу подтвердить',
    'Узнать новый календарь и открытость внешним международным детям; школьная запись и camp booking разные.',
    'Свой робот, сенсоры, underwater missions; визит Drone Hub, но полёты / автономные дроны11+ — другой трек.',block='Лагеря',participation='day_camp',evidence='historical_program',
    cost='CHF650 /5 дней по2026; новый тариф неизвестен.',languages=('EN','DE'),language='Принимающая школа прямо German- and English-speaking environment.',
    note='Прошедшая смена13–17июля2026,09–16. Новый2027набор не объявлен. Публикация школы даёт реальный junior content, но не league wins и не гарантированное место семьи.')
e.update(language_mode='bilingual',period='Кандидат следующего лета; новых дат нет')

un='https://unionschool.paris/en/academy/'
unfr='https://unionschool.paris/fr/activites/'
unhome='https://unionschool.paris/en/'
e=add('L300','Union School Paris · English Coding / LEGO для младших','Франция','Paris16 ·27rue de La Faisanderie',un,
    'ENpage3–7, FRpage4–7;6лет подходит обоим','Нет: старше7лет',COND,
    'Academy открыта детям других школ. Подтвердить подключение в середине года и сложность для опытного ребёнка.',
    '45мин screen-free coding с Hayo и75мин LEGOmechanics; блок yoga отдельно.',block='Лагеря',participation='day_camp',evidence='program',themes=('coding','robotics','technology'),
    languages=('EN',),language='Все три workshops прямо на английском; школа отдельно двуязычная.',cost='EUR2100 /32 Wednesday-пакета coding+yoga+LEGO; не цена32технических полных дней.',
    note='С16сентября2026,13:30–16:30. Coding45мин и LEGO75мин, yoga45мин / паузы отдельно; не три часа программирования. Min8 детей / max12. Точная длительность доступного остатка semester не установлена.')
regular(e,'Среды учебного2026/27 с16сентября; текущий вход и остаток semester уточнить');e.update(language_mode='primary',references=[ref('Другой нижний возраст FRpage',unfr),ref('Academy доступна детям других школ',unhome)])
e=add('L301','Union School Paris · English Scratch / Python / AI7–11','Франция','Paris16 ·27rue de La Faisanderie',un,
    '7–11',COND,YOUNG,
    'Academy открыта детям других школ; выбрать coding+sports-пакет и подтвердить старт / mentor / устройство.',
    'Scratch, затем Python games и вводные creative AI; собственный проект по уровню.',block='Лагеря',participation='day_camp',evidence='program',themes=('coding','games','ai'),
    languages=('EN',),language='Coding1.5часа прямо на английском.',cost='EUR2100 за опубликованный Wednesday-пакет; остаток года / оборудование / условия уточнить.',
    note='Среды13–17 с16сентября2026, но code13–14:30; затем snack, прогулка, real tennis и squash. Это не четыре часа AI и не турнирная школа. Указано10мест, наличие конкретного места не установлено.')
regular(e,'Среды2026/27;1.5часа coding в4часовом пакете');e.update(language_mode='primary',references=[ref('Внешние ученики и английский Academy',unhome)])
petit='https://lespetitsatomes.com/produit/stage-coding-robotique-pour-enfants/'
e=add('L302','Les Petits Atomes · Robotics / coding10–14 · будущая ступень','Франция','Paris16 / Vincennes / Versailles-LeChesnay',petit,
    '10–14 именно Robotics', 'Кандидат после10лет; в2026ещё9',YOUNG,
    'Достичь10лет, выбрать точный поток, технический EN/ES и иностранный допуск подтвердить.',
    'Роботы, сенсоры, блоковый код; C++ при освоении задач, отдельные AIинструменты.',block='Лагеря',participation='day_camp',priority='P4 — будущая возрастная ступень',evidence='program',
    note='Общий sciences6–12 не означает Robotics с6лет. Robotics14–17 или combo09–17 с sciences утром; lunchbox свой. ЯзыкEN/ES не опубликован. Даты выбранной смены ещё не установлены.')
e['period']='Каникулы; конкретные новые дни и место не установлены'

asti='https://astichallenge.com/'
e=add('C973','ASTI Robotics Challenge2027 · национальная финальная ступень старших','Испания','Burgos · финал; semifinals5городов',asti,
    '3º/4ºESO, Bachillerato, FP и university; начальная школа не входит','Нет: начальная ступень не входит в правило','Нет: начальная ступень не входит в правило',
    'Команда2–4 по школьной категории, взрослый mentor для minors; отбор через Marchsemifinals. Иностранный национальный допуск отдельно.',
    'Mobile robotics, электроника, программирование и техническая презентация.',start='2027-04-17',scope='national',priority='P4 — старшая школьная ступень',
    cost='Участие заявлено бесплатным; hardware и поездка отдельно.',note='RegistrationSep–Dec2026 — только месяцы, точный день закрытия не объявлен. ProjectDec2026–Feb2027; semifinalMarchвMadrid/Málaga/Valencia/Valladolid/Zaragoza. Это маршрут на будущее, не текущий турнир для6/9, поэтому не семейныйICS.')
asc='https://alsalirdelcole.es/first-lego-league-intercoles-challenge-asc/'
e=add('L303','Al Salir del Cole · FLL Intercoles · подготовка2026/27','Испания','Colmenar Viejo · через местные colegios',asc,
    'Primaria6–11; категории по классу, не только году рождения',
    'Условно при местной школьной категории; текущий класс и приём проверить','Условно приPrimaria и местном colegio;6лет не заменяет нужный класс',
    'Набор по colegios ColmenarViejo, еженедельная подготовка. Для туристической / внешней семейной команды доступ не установлен.',
    'FLL робот, seasonal mat, проект и командная защита; точную edition и аппаратную платформу подтвердить.',block='Лагеря',participation='day_camp',evidence='program',
    note='Заголовок2026/27, но gradeусловия ссылаются на25/26, а турнир на странице одновременно делится на2и3категории. Не выдано за универсальный новый nationalregламент. ТехническийES/EN прямо не указан; язык сайта не стал фильтром преподавания.')
regular(e,'Субботы с октября2026; полный календарь группы и тариф не опубликованы')

smart='https://www.smartcityexpo.com/exhibitor-faqs/'
e=add('E152','Smart City Expo World Congress2026 · технологии / AI / urban systems','Испания','Barcelona · FiraGranVia',smart,
    'Professional expo; minors обычно не допускаются, есть исключение для young children с родителем',
    'Условно: попросить письменное подтверждение исключения для9лет','Условно: попросить письменное подтверждение исключения для6лет',
    'Adult visitor pass; для детей запросить исключение заранее и оформить MinorResponsibilityForm на accessdesk. Монтаж / демонтаж детям запрещён.',
    'AI, smartcitysystems, digitaltwins и прикладные технологии; это не выставка всех мировых роботокомпаний.',block='События',start='2026-11-03',end='2026-11-05',participation='visitor',scope='international',priority='P3 — профессиональное посещение с детским исключением',themes=('ai','technology','robotics'),
    note='Организатор публикует3–5ноября2026;3/4ноября09–19,5ноября09–17. Youngchildren не определено числом лет: нельзя гарантировать6/9. Семейный ticket и workshopENне установлены; adultpass и childadmission отдельные условия.')
e.update(exhibition_tier='global',visitor_policy='confirm_children',visitor_policy_note='Официальное исключение сопровождаемых youngchildren;6/9иформа требуют подтверждения.',
    adult_entry='Visitorpass по актуальной registration; тариф выбранного пакета уточнить.',highlights=['ПрикладнойAI','Digitaltwins / города','Профессиональные компании и проекты'],exhibitors=[],exhibitor_note='Каталог участников конкретного сезона; все компании мира не обещаны.',exhibitor_directory_url='https://www.smartcityexpo.com/',references=[ref('Технологический трек2026','https://www.smartcityexpo.com/tracks-scewc/enabling-technologies/')])
coupe='https://www.coupederobotique.fr/event/coupe-de-france-de-robotique-2027/'
access='https://www.coupederobotique.fr/horaires-et-acces/'
e=add('E153','Coupe de France de Robotique2027 · семейный просмотр / WE R TECH','Франция','LaRoche-sur-Yon · ParcExpoLesOudairies',coupe,
    'Зрители; младшие workshops3+ опубликованы для2026, условия2027ещёнеустановлены',COND,COND,
    'Ждать расписания publicdays2027;2026допуск посетителей и workshops не является билетом2027. Командная заявка отдельная.',
    'Автономные / junior robots и возможные hands-onprojects; не универсальная выставка производителей.',block='События',participation='visitor',scope='national',themes=('robotics','coding','games','technology'),
    note='Competitionwindow5–8мая2027 опубликован. Но accessbody всё ещё13–16мая2026 и publicdays14–16мая2026. Эти дни нельзя автоматически перенести на2027. WE R TECHописание / иллюстрации2026: бесплатные ateliers3+, mini-robots/3D/code; новый familyprogramme не подтверждён.')
e.update(period='Конкурс5–8мая2027; точные дни посетителей ещёнеобъявлены',date_status='Уточнить',published_start='2027-05-05',published_end='2027-05-08',references=[ref('Accesspage с прошлогодними publicdays',access),ref('WE R TECH: архив детских ateliers','https://www.coupederobotique.fr/we-r-tech/')])

# Correct concrete old records without erasing prior country and world research.
updated=['C549','C908','C909','L131']
e=byid['C549'];e.update(checked=CHECKED,priority='P4 — нешвейцарская команда не допускается',
    mat='Нет для нешвейцарской команды; после перехода в Swiss team допуск отдельно',osc='Нет для нешвейцарской команды; после перехода в Swiss team допуск отдельно',
    entry='Прямой запрет Non-Swiss teams в GeneralInfo. После реального входа в швейцарскую команду проверить её region, возраст, notebook и право на Worlds.',
    deadline='2027-01-08',deadline_note='Registration8Jan2027,00:00EST; Payment1Jan2027раньше. Уточнить обе процедуры уeventpartner.',
    deadline_utc='2027-01-08T05:00:00Z',cost='EUR110 / team поprimarypage;USD127.66альтернатива. Lunchпредзаказ отдельно.',
    registration_status='Снимок:16мест, только Swiss teams. Место семьи и teamregion не подтверждены.',
    proof='Повторно прочитана полная официальная eventpage черезwebreader; directHTTP403 не использован как отсутствие правила.',
    note=e['note']+' Новый факт:Non-Swiss teams explicitly barred. IQдата6февраля2027; при большем количестве команд agendaдопускает расширение на2дня, но конецнепередвинут предположением.')
e=byid['C908'];e.update(checked=CHECKED,age='FAQ2026/27:6–9; divisionpage6–10 — верхнюю границу9/10подтвердить',
    mat='Условно:9лет сейчас; кevent2027можетбыть10 — точный cutoffирасхождение FAQподтвердить',
    entry='Privateinitiatives разрешены. Иностранная команда может участвовать вDACH-events, но не проходит дальше в чужой стране. Exploreне имеет общей победной таблицы.',
    language='Судейство / презентация обычно наофициальномязыке страны;ENисключение согласовать.',
    proof='Повторно прочитан currentFAQ:иностранный вход,локальная квалификация,язык,Explore6–9. Противоречие division6–10 отмечено.')
e['references'].append(ref('ТекущийFAQ ирасхождениеExplore',faq))
e=byid['C909'];e.update(checked=CHECKED,deadline='2026-10-31',deadline_label='Регистрация Challenge',
    entry='School / club / privatefamilyteam допустимы. Foreignteam может участвовать, но progressionвSwissqualifier доступен только команде изШвейцарии.',
    language='Judgingиpresentationобычнонаофициальномязыке страны;ENнужно согласовать.',
    proof='ТекущийFAQподтверждаетdeadline31October2026,foreigneventвходбезчужойквотыиофициальныйязыкзащиты.')
e['references'].append(ref('FAQ:registration/foreignqualification/language',faq))
e=byid['L131'];e.update(checked=CHECKED,language_mode='primary',
    note=e['note']+' Повторно прочитаныGeneva/Lausanne/Zug:вдатированныхjuniorменютожеGameDesign7+иPython10+,неLEGO6+. НиодномуRobotics6+неприписаначужаяcampдата.',
    proof='Проверены общий Roboticscourse и текущие конкретныеbranchmenus;датыGameDesignнеперенесенынаRobotics.')
e['references'].extend([ref('Geneva:actualmenu',gen),ref('Lausanne:actualmenu',lau),ref('Zug:actualmenu','https://zurich.techsparkacademy.ch/zug-day-camps/')])
p=next(p for p in d['league_guide']['profiles'] if p['id']=='fll-europe-three')
cat=next(c for c in p['categories'] if c['name']=='Swiss Founders');cat.update(age='ExploreFAQ6–9vsdivision6–10;Challenge9–16',
    entry='Foreigneventвходразрешён;progressionтолькокомандеизстраныevent. Языкобычноофициальныйместный.',age_rule='Exploreверхнийcutoff9/10неразрешён;birthdayнадату2027уточнить')
p['sources'].append(dict(title='DACHFAQ:age/foreignteams/language',url=faq,checked=CHECKED))
p['nuances'].append('SwissFAQ6–9иExploredivision6–10расходятся;дляМатвея2017точныйcutoffважен. DACHчужаястранадаётучастиебезprogression.')
profile('fll-swiss-junior','FIRST LEGO League Switzerland · четыре младших маршрута2026/27','regional',
    '5+:5–7;ExploreFAQ6–9/division6–10;8+:8–16Grades4–10;Challenge9–16',
    'Короткий выбор длясемьи:ОскарExploreлибоучебнаяFuture5+;МатвейChallengeилиFuture8+приправильномклассе. Иностранныйтурнирныйвизитне даётSwissquota.',
    [dict(name='Future5+',age='5–7Grades1–3',team='До4,groupдо24',hardware='CS&AI5+,1kit/team',age_rule='Schoolgradeотдельно',entry='Учебнаяпрограмма;официальногоevent2026/27нет'),
     dict(name='Explore',age='FAQ6–9vsdivision6–10',team='До6',hardware='Founderskit',age_rule='Birthday/cutoffверхнего возрастаподтвердить',entry='Каждаякомандаполучаетrecognition;непобедаврейтинге'),
     dict(name='Future8+',age='8–16Grades4–10',team='До8,groupдо24',hardware='2новыхCS&AIkits;SPIKEнеподходит',age_rule='Возрастикласс',entry='Regional→DACHfinalтолькокомандеизстраныevent'),
     dict(name='Challenge',age='9–16',team='Точныйместныйteamlimitподтвердить',hardware='FoundersSPIKE/EV3поrules',age_rule='Возрастнаcontrol date',entry='Regional→Swissqualifier→DACHfinal;internationalquotaотдельно')],
    ['C908','C909','C972','L278'],['Определитьвозрастикласс','Выбратьedition/команду/наставника','Подтвердитьместныйjudgingязык','Registration31Octevent/31Marучебнаяgroup','Localresult→допустимыйотбор'],
    ['Толькоchildren-ownwork','Не покупатьновыйkitдовыбораedition','Foreigneventvisit≠Swissqualification'],
    ['Future5+неcompetitiveevent','ТочныйSwissregionalcalendarвJOINнеполучен','Regionalpromises2027/28непревращенывгарантиюглобальнойFIRSTструктуры'],
    [('DACHFAQ',faq),('Future8+rules/cost',f8),('Future5+teaching',f5)])

admit='https://unionschool.paris/en/information-request/'
s=dict(id='S030',name='Union School Paris',iso='FRA',country='Франция',region='Европа',city='Paris16',school_type='private',
    curriculum='Двуязычная Nursery / Primary: French national programme + English National Curriculum. IB не подтверждён.',ib_programmes=[],
    ages='Nurseryс2летдоYear6;точныйplacement6/9черезоценку. Academyмладшие3/4–7,старшиеcoding7–11.',instruction_languages=['EN','FR'],
    language_note='ШколаFR/EN;WednesdayAcademyпрямоEnglish-only. Полностьюанглийскийшкольныйденьнеобещан.',
    fit=dict(mat='candidate',osc='candidate',note='Начальнаяступеньподходитусловно;English/French/mathsassessment,schoolseatиcodingместаотдельно.'),
    boarding='unknown',boarding_note='Описана дневнаяшкола;младшийпансионнеустановлен.',
    programme='Codingвходитвschoolfeesпоadmissionspage;Academyоткрытавнешнимученикам. Для6летcoding45мин+LEGO75минвWednesdayпакете;7–11coding1.5часаScratch/Python/creativeAI.',
    labs='LEGOмеханика/codingоборудованиепрограммы;отдельнаяробототехническаялабораторияикомандаотборовнеподтверждены.',ai='CreativeAIвAcademy7–11;это не доказанныйкурсMLengineeringилиOlympiadteam.',
    results=[],evidence='programme',
    admissions='TasterdayиassessmentEN/FR/maths;решениепослеоценки. LanguageIntensiveLABпредлагаетсясYear1;FRsupportдлясемьиуточнить.',
    cost='Admissions2026/27показываетEUR21700/24700вшкольных/LABтарифах:пакетопределить;registrationEUR1550,insurance30,питание/материалыотдельно. AcademyEUR2100неannualtuition.',
    questions=['КакойFRsupportиclassplacementдля6/9безфранцузского?','Есть лифизическаяroboticsкоманда,кодлиги,наставникипротоколы?','Сколькоcode/engineeringчасоввшкольномднеиподходитлиуровеньпослетрёхлетсоревнований?'],
    sources=[dict(title='Школа/curriculum/внешняяAcademy',url=unhome,claim='FR/ENprimaryиоткрытаяEnglishAcademy',kind='school',checked=CHECKED),dict(title='Конкретныеcodingгруппы2026/27',url=un,claim='Язык/возраст/техническиечасы;несоревновательныенаграды',kind='school',checked=CHECKED),dict(title='Admissionsassessment/fees',url=admit,claim='EN/FR/mathsassessmentиотдельныешкольныетарифы',kind='school',checked=CHECKED)],
    checked=CHECKED,priority=2,research_status='partial',verification='Первичныестраницышколыпрочитаны;соревновательныепобеды,приёмиместанеустановлены.')
d['schools'].append(s);d['school_focus'].update(version=35,checked=CHECKED,conclusion='30 школьных досье. Добавлена Union Paris как двуязычная начальная школа с английским coding; мировое робототехническое лидерство не доказано.')
d['school_focus']['routes'].append(dict(name='Париж · проба английского coding до выбора школы',ids=['S030','S025','S028'],detail='Union Academy допускает внешних учеников, поэтому школьный переезд не обязателен для знакомства с Englishcoding. ШколаFR/EN,assessmentиcompetitionmentorтребуютотдельнойпроверки. ABIиBordeauxсохранены.'))
d['school_focus']['gaps'][0]='30 школьных досье; полный мировой и национальный школьный аудит не завершён.'
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles)
f=d['europe_focus'];f.update(version=35,checked=CHECKED,heading='Три страны. Конкретные шаги для семьи.',
    conclusion='Для регулярного соревнования на доступном языке первым проверял бы Испанию и действующего наставника WRO/FLL. Швейцария стала конкретнее по младшим EN/FR/DE лагерям, но иностранный турнирный визит не даёт швейцарскую квалификацию. Франция имеет подтверждённый Englishcoding и двуязычные каникулы; для школьного переезда нужно проверить поддержку без французского и сильную команду.',
    limitations='Третий первичный проход, а не полный реестр трёх стран или рейтинг школ. Локальные календари JOIN, новые летние2027наборы,foreignquotasвИспании/Франции,школьныеместаипротоколы5–10летостаютсянеполными.')
fc={c['iso']:c for c in f['countries']}
fc['CHE'].update(reason='ЕстьStarter6–10/Elementary8–12WROиFLLChallenge9–16. ВDACHforeignteamможетучаствовать,нонепроходитдальшечерезчужуюстрану;AlpineVEX2027вообщетолькоSwissteams.',
    mat='WROElementary/Challenge;Future8+ещёпроверитьGrade4–10. ExploreFAQ6–9vsdivision6–10:в2027деньрожденияважен. AlpineVEXтолькопослереальногоSwissteamдопуска.',
    osc='WROStarter;FLLExploreилиучебнаяFuture5+приправильномклассе. EcolintIntroduction5–6/7иTechLabsInventors5–9подходятпо6лет;местоотдельно.',
    camp='Geneva:19–23октября2026EcolintRoboticsдляОскара;дляМатвеяTechSparkGameDesign7+,EN/FR. Добавлены13GameDesignсменGeneva/Lausanne2026–27. ZürichTechLabsInventorsEN/DEпоказываетwaitinglist;BattleBotsдляМатвеяимеетENsupport,а неENосновной. LaGarenneRobotics8+сохранён.',
    budget='EcolintCHF640/неделя;TechSparkCHF790–890/смена. TechLabsCHF525полдня/990полныйдень. TandemVEX75мин/неделяпостаромуPDFCHF45:неинтенсив. LaGarenne2недели+краткийRoboticsмодульсущественнодороже.',
    city_route='Geneva—параразныхвозрастныхпрограмм,безгарантиимест. Zürich—пробамладшегоVEX/STEAMиликлубаTandem. Basel—школа/mentorиSwissteamrouteпослеотдельногодопуска. Campbookingнеравеншкольномуприёму.',
    risk='FLLязыкзащитыобычноофициальныйместный,ENисключениеподтвердить. ForeignFLLвходнеравенSwissprogression. VEXAlpineNon-Swissteambarred. TechLabswaitinglistсчётчикнебронь;Exploreверхняяграница9/10расходится;Tandem2025/26недействующий2026/27календарь.')
fc['CHE']['event_ids'].extend(['C549','C972']+['L'+str(i) for i in range(278,300)]);fc['CHE']['profile_ids'].append('fll-swiss-junior')
fc['ESP'].update(risk=fc['ESP']['risk']+' ASTI2027толькоESO3/4истарше,не6/9. IntercolesColmenarViejoчерезместныеcolegiosсрасхождениемклассов25/26. SmartCityExpoобычноprofessional;youngchildrenтолькопоисключениюиMinorForm.',
    camp=fc['ESP']['camp']+' ДобавленапроверяемаярегулярнаяFLLподготовкаASC:входпоcolegio/классу,неуниверсальныйлагерьдлятуриста.',
    city_route=fc['ESP']['city_route']+' ColmenarViejoрассматриватьтолькопоследопускачерезместнуюшколу;публичнаястраницасама нерегистрируетдетей.')
fc['ESP']['event_ids'].extend(['C973','L303','E152'])
fc['FRA'].update(camp=fc['FRA']['camp']+' UnionParis:English-onlyWednesdayAcademyдлявнешнихучеников,младшаягруппа3/4–7истаршаяcoding7–11. LesPetitsAtomesRobotics10–14покане6/9.',
    school=fc['FRA']['school']+' ДобавленаUnionParis:FR/ENdoublecurriculumиEnglishcoding;сильнаясоревновательнаякомандаилимировыепобедынеустановлены.',
    budget=fc['FRA']['budget']+' UnionAcademyEUR2100заWednesdayпакет;code45минумладших/90минустарших,остальноеLEGO/yoga/sport. Этоотдельноотschooltuition.',
    risk=fc['FRA']['risk']+' Coupe2027competition5–8мая,ноaccessиfamilyprogrammeвсёещё2026:publicdays2027невыдуманы.',
    city_route='Paris—пробаABIканикулярнойсменыилиUnionEnglishAcademyдлявнешнихдетейдообязательногошкольногопереезда. Bordeaux—FR/ENprimary+coding. СоревновательныйmentorиадаптациябезFRпроверяютсяотдельно.')
fc['FRA']['event_ids'].extend(['L300','L301','L302','E153']);fc['FRA']['school_ids'].append('S030')
f['shortlist']=[dict(title='Испания · постоянная команда для обоих',detail='Матвей:WROElementaryлибоFLLK8;Оскар:RoboBasic/Explore. Сначалапоказательныетренировкиснаставникомидействующийteamcode,затемрешениеошколе. ЛетниеNATUKдатыследующегосезонапоканеобъявлены.',event_ids=['C910','C911','C912','C915','L227']),
    dict(title='Швейцария · проверить конкретный осенний slot',detail='19–23октября:EcolintIntroductionдляОскара;TechSparkGenevaGameDesignдляМатвея. Разныеплощадки/программы,местаиуровеньподтвердить. ВZürich12–16октябряBattleBotsпоказываетregister,Inventors—waitinglist.',event_ids=['L296','L279','L293','L295']),
    dict(title='Франция · короткая проба английского',detail='ABIHaunted26–30октябряимеетгруппыдляобоих. UnionWednesdayAcademyнаENдоступнавнешнимученикам,нонеоднонедельныйлагерь. SchoolassessmentпотребуеттакжеFRиmaths;roboticsleaguewinsнеустановлены.',event_ids=['L230','L300','L301'])]
f['steps'].insert(1,dict(title='Swissвход · командный регион и язык',detail='ForeignteamможетприехатьвFLLDACH,нопереходвSwissqualifierтребуеткомандыизШвейцарии. VEXAlpine2027вообщенедопускаетNon-Swiss. Передпереездомнуженпроверяемыйпланвходавреальнуюместнуюкоманду;паспортсампосебеэтогонеустанавливает.'))
sources=[]
for e in new+[byid[i] for i in updated]:
    sources.append((e['source'],e['title']))
    sources.extend((r['url'],r['label']) for r in e.get('references',[]))
sources.extend((r['url'],r['title']) for r in s['sources'])
known={r['url'] for r in d['sources']};focus_known={r['url'] for r in f['sources']}
for url,title in sources:
    if url not in known:d['sources'].append(dict(url=url,title=title,checked=CHECKED,evidence='Первичныйисточникпрочитан;возраст/язык/даты/допускотмеченысограничениями.'));known.add(url)
    if url not in focus_known:f['sources'].append(dict(title=title,url=url,checked=CHECKED));focus_known.add(url)
issues=[('TechSparkcourse/calendar','LEGO6+общийкурснеперечисленвдатированныхbranchmenus;13новыхсменвнесеныкакGameDesign7+,неRobotics.',tsa),
    ('DACHforeignentry','FLLforeignteamentryразрешён,progressionтолькоhomecountry. Judgingобычноофициальныйместныйязык.',faq),
    ('Exploreageconflict','CurrentFAQ6–9vsdivision6–10;Матвей2017можетвыйтиза9леткevent2027.',faq),
    ('SwissVEXAlpine','Полнаяprimaryeventpage:Non-Swiss teamsне допускаются. DirectHTTP403,webreaderпрочитан.',byid['C549']['source']),
    ('TechLabsInventors','Body6–8vsbooking5–9;waitinglistнесмотряAvailableplaces8;index09–09:15заменёнподробнымиhalf/fullschedule.',details['techlabs_invent1']),
    ('TechLabsBattle','Header8–14vsAge9+;EN&FRsupportedнеосновнойEN;5–9Octwaitinglistнесмотря8places.',details['techlabs_battle0']),
    ('Ecolintarchive/current','2026Introduction5–7bookingvs5–6body;olderEV38–13page2025несталосенней2026сменой.',ec),
    ('Unionmixedpackage','ВAcademy45/90минcoding,остальноеmechanics/yoga/sport;внешниеученикидопустимы,schoolFRassessmentотдельно.',un),
    ('Francevisitorcalendar','Coupeheader2027,accessbody/publicdays2026иWERTTECH2026;неподтверждённыйpublicICS.',access),
    ('Spainprimarygates','ASTIстаршиеESO3/4;ASCIntercolesместныеcolegiosипротиворечивыеклассы25/26;неуниверсальныйnationalrule.',asc),
    ('SmartCityminors','Professionalminorsbanсyoungchildrenисключением;числовойвозрастнеопределён,MinorFormтребуется.',smart),
    ('TechLabsFAQtemplate','FAQсодержитtemplatequestions;неиспользованкакправиловозраста/языка/приёма. Детальныеbookingpagesпрочитаны.','https://www.techlabs.ch/faqs')]
a=d['completeness_audit'];a['validation_previous']=a['validation'];a.update(version=35,checked=CHECKED,status='partial',scope='Третий глубокий CHE/ESP/FRAпроход:младшиепрограммы,реальныйязык,национальнаяквалификация,школаипосещение.',
    conclusion='30новыхкарточек,1профильмладшихSwissFLLмаршрутови1школьноедосье. Исправленыусловия4старыхкарточекиSwissчастипрофиля. Мировойкалендарьостаётсячастичным.',
    new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=updated,updated_profile_ids=['fll-europe-three'],new_school_ids=['S030'],validation=dict(version=35,status='pending',publication='pending'))
a['source_issues'].extend(dict(name=l,status=t,official_alternative=u,checked=CHECKED) for l,t,u in issues)
d['camp_focus']['validation_previous']=d['camp_focus']['validation'];d['camp_focus'].update(version=35,checked=CHECKED,carried_forward_ids=d['camp_focus']['added_ids'],added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=['L131'],validation=dict(version=35,status='pending'))
d['camp_focus']['routes'].extend([dict(name='Geneva/Lausanne · реальные bilingualсмены',ids=['L296','L279','L280','L285','L286'],detail='EcolintRobotics6лет19–23Oct;TechSparkGameDesign7+EN/FR,неRobotics6+. Oscarв2027толькопосле7-летия;grade/birthdayисвободныеместаотдельно.'),dict(name='Paris · подтверждённый Englishcoding',ids=['L230','L300','L301'],detail='ABIканикулынаEN/FRдляобоих;UnionрегулярныйEnglish-onlyclubдлявнешнихдетей. Языкфранцузскойшколыотдельныйбарьер;мироваясоревновательнаяпобеданеобещана.')])
d['expansion_log'].append(dict(version=35,checked=CHECKED,added=30,updated_ids=updated,new_profiles=1,new_schools=1,note='CHE/ESP/FRAthirdpass;sourceconflicts,languageinstruction/supportandnationalqualificationgates;worldpartial.'))
assert len(new)==30 and len(profiles)==1 and len(d['schools'])==30
# Keep the public comparison readable; codes and compact source notes stay in data.
fc['CHE'].update(
    reason='Есть WRO Starter 6–10 и Elementary 8–12, а также FLL Challenge 9–16. В FLL иностранная команда может участвовать, но проходит дальше только через свою страну. Alpine VEX 2027 принимает только швейцарские команды.',
    mat='WRO Elementary или FLL Challenge. Для Future 8+ нужно проверить класс 4–10. У Explore расходятся границы 6–9 и 6–10: день рождения к событию 2027 важен. Для Alpine VEX требуется допуск швейцарской команды.',
    osc='WRO Starter, FLL Explore или учебная Future 5+ при подходящем классе. Ecolint Introduction и TechLabs Inventors подходят шестилетнему по возрасту; место и уровень нужно подтвердить.',
    camp='19–23 октября 2026: Ecolint Robotics в Женеве для Оскара, TechSpark Game Design на EN/FR для Матвея. Добавлены 13 датированных смен Game Design в Женеве и Лозанне на 2026–2027 годы. TechLabs Inventors на EN/DE показывает лист ожидания; Battle Bots предлагает помощь на EN/FR. La Garenne Robotics с 8 лет сохранён.',
    budget='Ecolint: CHF 640 за неделю. TechSpark: CHF 790–890 за смену. TechLabs: CHF 525 за полдня или 990 за полный день. Старый курс Tandem: CHF 45 за 75 минут в неделю. Жильё семьи и поездки отдельно; краткий модуль La Garenne нельзя сравнивать с ежедневной робототехникой.',
    city_route='Женева — проба разных возрастных программ без гарантии мест. Цюрих — младший STEAM/VEX и проверка клуба Tandem. Базель — школа, наставник и вход в местную команду. Запись в лагерь и приём в школу — отдельные процедуры.',
    risk='FLL обычно судит на официальном языке страны: английское исключение согласовать. Иностранное участие не даёт швейцарскую квалификацию. Alpine VEX запрещает нешвейцарские команды. У TechLabs лист ожидания и счётчик мест расходятся. PDF Tandem 2025/26 не подтверждает нынешний набор.')
fc['ESP'].update(
    risk='Независимая команда не гарантирует испанскую мировую квоту. FLL K8 требует 4–10 детей и новое оборудование. ASTI начинается со старших классов ESO, детям 6/9 рано. Intercoles в Colmenar Viejo идёт через местные школы; правила классов на странице противоречивы. Smart City Expo — профессиональная выставка, детям нужно отдельное исключение и форма ответственности.',
    camp='Camp Tecnológico: Junior 6–9 с обязательным чтением для шестилетних, Genius 9–12 и регулярные занятия. NATUK заявляет Robotics на английском для 6–16, но новые летние даты ещё нужны. Tech&Play с проживанием — от 7, английская иммерсия не доказывает язык каждого технического занятия. ASC добавлен как местная школьная подготовка FLL.',
    city_route='Vigo, Madrid или Sevilla: выбирать действующего наставника Elementary по результатам его команды. Bilbao, Basauri и Vitoria имеют регулярного оператора; язык группы проверить. Colmenar Viejo — только после подтверждения входа через местную школу.')
fc['FRA'].update(
    camp='ABI предлагает ближайшие двуязычные смены для обоих. Union Paris: регулярная Academy на английском для внешних учеников, младшая группа 3/4–7 и coding 7–11. У Cité и Magic Makers конкретные возрастные/школьные категории и неподтверждённый EN. Les Petits Atomes Robotics начинается с 10 лет.',
    school='ABI, Ermitage и Bordeaux имеют двуязычные младшие программы. Добавлена Union Paris с французской и английской программами и coding. Действующая команда с мировыми победами у Union не установлена; Ermitage boarding с 11 лет пока не подходит обоим.',
    budget='Union Academy: EUR 2 100 за пакет сред по опубликованной странице. Coding занимает 45 минут у младших или 90 минут у старших; остальное — LEGO, yoga или спорт. Это отдельно от школьной платы. Cité и Magic Makers дешевле как отдельные мастерские, но технический EN нужно подтвердить.',
    risk='Без французского язык защиты и школьная адаптация требуют проверки. Discovery признаёт проект, не даёт рейтинговой медали. Coupe 2027 объявлен на 5–8 мая, но страница входа и детских мастерских ещё описывает 2026: дни посетителей 2027 не выдуманы.',
    city_route='Париж — проба ABI на каникулах или Union Academy на английском для внешних детей. Бордо — двуязычная начальная школа и coding. До переезда проверить адаптацию без французского и работу действующего соревновательного наставника.')
f['limitations']='Третий проход по первичным источникам. Реестр трёх стран остаётся частичным: местные даты FLL в JOIN, новые лагеря 2027, национальные квоты, школьные места и протоколы команд за 5–10 лет ещё собраны не полностью.'
f['shortlist']=[
 dict(title='Испания · постоянная команда для обоих',detail='Матвей: WRO Elementary или FLL K8. Оскар: RoboBasic или Explore. Сначала пробные тренировки с наставником и действующий код команды, затем выбор школы. Новые летние даты NATUK пока не объявлены.',event_ids=['C910','C911','C912','C915','L227']),
 dict(title='Швейцария · конкретная осенняя смена',detail='19–23 октября: Ecolint Introduction для Оскара и TechSpark Game Design для Матвея в Женеве. Разные площадки: согласовать места и транспорт. В Цюрихе Battle Bots 12–16 октября показывает регистрацию, Inventors — лист ожидания.',event_ids=['L296','L279','L293','L295']),
 dict(title='Франция · проба английского без смены школы',detail='ABI Haunted 26–30 октября имеет группы для обоих. Union Academy на английском допускает внешних учеников, но это регулярный курс. Школьная оценка включает французский и математику; соревновательную команду нужно искать отдельно.',event_ids=['L230','L300','L301'])]
f['steps'][1]=dict(title='Швейцарский отбор · команда и язык',detail='Иностранная команда может приехать на FLL, но переход в швейцарский отбор требует команды из Швейцарии. Alpine VEX 2027 иностранные команды не принимает. Нужен проверяемый план входа в местную команду; паспорт сам по себе её регион не устанавливает.')
s.update(curriculum='Двуязычная Nursery / Primary: французская национальная программа и English National Curriculum. IB не подтверждён.',
 ages='От 2 лет до Year 6. Класс детей 6/9 определят при приёме. Academy: младшие 3/4–7, старшие coding 7–11.',
 language_note='Школа на FR/EN, Wednesday Academy на английском. Полностью английский школьный день не обещан.',
 fit=dict(mat='candidate',osc='candidate',note='Возраст начальной школы подходит условно. Нужны оценка английского, французского и математики, школьное место и отдельное место в Academy.'),
 boarding_note='Описана дневная школа; младший пансион не установлен.',
 programme='Coding включён в школьную плату по странице приёма. Academy открыта внешним ученикам. Младшим: 45 минут coding и 75 минут LEGO внутри пакета. Для 7–11: 90 минут Scratch, затем Python и creative AI.',
 labs='LEGO-механика и оборудование coding-программы. Отдельная робототехническая лаборатория и отборная команда не подтверждены.',
 ai='Creative AI в Academy 7–11. Курс машинного обучения или олимпиадная команда не установлены.',
 admissions='Пробный день и оценка EN/FR/математики. Language Intensive LAB с Year 1; поддержку без французского уточнить.',
 cost='Страница 2026/27 показывает EUR 21 700 / 24 700 в школьных и LAB-тарифах: определить свой пакет. Вступительный взнос EUR 1 550, страховка 30, питание и материалы отдельно. Academy EUR 2 100 — отдельный тариф.',
 questions=['Как поддержат детей 6/9 без французского и определят классы?','Есть ли команда робототехники: код лиги, наставник и протоколы?','Сколько инженерных часов в школьном дне и как адаптируют задания после трёх лет соревнований?'],
 verification='Первичные страницы школы прочитаны. Соревновательные победы, приём и места не подтверждены.')
# Spacing around technical names in card text; URLs, dates, IDs and schema stay exact.
import re
def readable(v):
    if isinstance(v,str):
        if v.startswith('http'):return v
        v=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])',r'\1 \2',v)
        v=re.sub(r'([A-Za-z0-9])([А-Яа-яЁё])',r'\1 \2',v)
        v=re.sub(r'([,;:])(?=\S)',r'\1 ',v)
        return v
    if isinstance(v,list):return [readable(x) for x in v]
    if isinstance(v,dict):return {k:readable(x) for k,x in v.items()}
    return v
keys=['title','city','age','mat','osc','entry','gear','language','cost','note','period','proof','registration_status','deadline_note','format','language_certainty','visitor_policy_note','adult_entry','exhibitor_note']
for e in new:
    for k in keys:
        if k in e:e[k]=readable(e[k])
for node in ast.parse((ROOT/'scripts/polish-europe-junior-v35.py').read_text()).body:
    if isinstance(node,ast.FunctionDef): exec(compile(ast.Module(body=[node],type_ignores=[]),'polish','exec'))
polish(d)
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=[]
for folder in W.glob('sources-europe-junior*v35'):
    if (folder/'receipt.json').exists():
        for r in json.loads((folder/'receipt.json').read_text()):
            if r['url'] in {u for u,_ in sources}:
                receipts.append({k:r[k] for k in ('name','url','status','mime','bytes','sha256','resolved','error') if k in r})
(ROOT/'data/europe-junior-source-receipts-v35.json').write_text(json.dumps(dict(checked=CHECKED,method='Primarypagesreadviawebandlocalsnapshot;rawHTMLkeptoutsidepublishedsite.',sources=receipts,web_read_primary=[dict(url=byid['C549']['source'],claim='Non-Swissteambarred;EUR110;registration8Jan2027;payment1Jan2027')]),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v35.json');r.setdefault('research_passes',[]).append(dict(version=35,checked=CHECKED,scope='CHE/ESP/FRAthirdjunior/language/qualificationpass',added_records=30,new_profiles=1,new_schools=1,status='partial',remaining='SwisslocalFLLdates;Spain/Franceforeignquota;new2027camps;schoolsandprotocols5–10years'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=35,status='local_checks_pending_publication_pending');rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=35,added=30,updated=updated,profiles=1,schools=1,world_complete=False)))
