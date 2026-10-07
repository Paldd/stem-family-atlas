"""Selected North American primary curricula, grade gates and project showcases."""
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '1386dca53032e0bd56d68e0acd2af423f74d633d'
CHECKED = '2026-10-06'
TORONTO = 'https://outreach.engineering.utoronto.ca/'
JR = TORONTO+'jr-deep/'
DEEP = TORONTO+'pre-university-programs/high-school-program/deep/'
RES = TORONTO+'pre-university-programs/high-school-program/summer-residence-program/'
VV = 'https://carleton.ca/vv/summercamps/'
MC = 'https://www.eng.mcmaster.ca/community/outreach-programs/summer-camp/'
SM = 'https://www.stemminds.com/'
ID = 'https://www.idtech.com/'
HELP = 'https://idtechcamps.zohodesk.com/portal/en/kb/articles/'
TECH = 'https://www.thetech.org/education/'
TC = TECH+'tech-challenge/tech-challenge-2027/'
RULES = 'https://www.thetech.org/media/42yd5cg2/ttc27_rules_english_v3.pdf'
POSTER = 'https://www.thetech.org/media/m2yoey4x/ttc27-rulesposter-1.pdf'
NEW = ['toronto-jr-robotics','toronto-jr-energy','toronto-jr-smart-systems',
       'toronto-jr-mechatronics','toronto-jr-coding','toronto-jr-cities','toronto-jr-ai',
       'toronto-deep-day-2027','toronto-deep-board-watch',
       'carleton-sprockets','carleton-explorers','carleton-nybbles','carleton-terabytes',
       'carleton-game-junior','carleton-game-senior','carleton-programming-junior',
       'carleton-programming-senior','carleton-engineering-jksk','carleton-engineering-12',
       'carleton-engineering-34','carleton-engineering-56','carleton-engineering-78',
       'mcmaster-fireball','mcmaster-flare','stemminds-junior-paused','stemminds-senior-paused',
       'id-battlebots-junior','id-battlebots-vex','id-battlebots-takehome','thetech-camp-2027']
QA = [('2026-10-20','17:00'),('2026-11-03','17:00'),('2026-11-18','19:00'),
      ('2026-12-01','17:00'),('2026-12-16','19:00')]
EVENT_IDS = ['TC2027-SHOWCASE','TC2027-REGOPEN']+['TC2027-QA-'+day.replace('-','') for day,_ in QA]
PROFILE_ID = 'tech-challenge-project'
UNKNOWN_EN = 'Английский сайт не устанавливает язык преподавания. Технический английский и приём приезжих детей необходимо подтвердить; EN пока не включён в фильтр подтверждённого обучения.'
ASK = 'Перед выбором подтвердить конкретный курс, возраст/класс, международный приём, язык занятий, места и окончательный счёт. Заявки, сообщения, аккаунты и оплаты не выполнялись.'

def add_northamerica_v131(add,src,fit,profiles):
    def emit(i,name,iso,place,themes,formats,age,language,programme,timing,price,housing,mf,of,sources,
             status='archive_next_unannounced',confirmed=None,role=None,sessions=None):
        add(NEW[i],name,{'CAN':'Канада','USA':'США'}[iso],iso,place,themes,formats,age,language,
            programme,timing,price,housing,mf,of,
            'Редакционный кандидат по собственной программе и условиям организатора. Это отдельный учебный трек, не отдельный оператор; независимый мировой рейтинг качества не установлен.',
            [ASK],sources,status=status,confirmed=confirmed,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        return p
    grade_unknown = fit('conditional','Допуск зависит от реального завершённого класса, не только от года рождения. Новый набор 2027 и международный приём пока не подтверждены.')
    jrprice=dict(year=2026,label='Архив: $490 за пятидневную неделю смешанной группы. Валюта и налоги на этой странице явно не указаны; это не прайс 2027.',
        included='Один выбранный курс, 09–16; бесплатное пребывание 08–09 и 16–17.',
        extras='Жильё семьи, дорога и питание вне опубликованного пакета отдельно. $390 относится к четырёхдневной Girls Jr. DEEP, не к курсу братьев. Bursary 10–75% заявлена только для Jr. DEEP Coding 5–6 классов и не назначена семье автоматически.',
        deposit='Отмена до 23:59 ET в воскресенье за семь дней до курса: возврат/кредит за вычетом $90; позднее возврата нет. Это политика архива 2026; условия нового набора проверить.')
    jrtracks=[
        ('Robotics at Work: Building Smart Machines','3–4','robotics,engineering','Механика, электрические цепи и управление по правилам; создание и испытание простых умных машин. Конкретный набор, контроллер и язык программирования не опубликованы.'),
        ('Power Play: Energy in Motion','3–4','science,engineering','Электрическая и механическая энергия, движение и практические конструкции. Это инженерная наука, а не отдельный соревновательный курс робототехники.'),
        ('Smart Systems: Building Gadgets That Come Alive','5–6','engineering,technology','Датчики и системы управления: транспортные и домашние устройства, проектирование взаимодействующих компонентов. Конкретная электроника и программный стек не указаны.'),
        ('Mechatronics Lab: Machines in Motion','5–6','robotics,engineering','Передачи, моторы, датчики и роботизированные механизмы/руки; итерации конструкции и управления. Платформа и программный язык не обещаны.'),
        ('Jr. DEEP Coding','5–6','coding,technology','Начальная логика и программирование. Собственная страница не устанавливает Python, Arduino либо конкретный набор; стипендиальная программа относится именно к этому треку.'),
        ('Urban Engineering: Disaster-Proofing Cities','7–8','engineering,science','Устойчивость городов, конструкции и воздействие среды. Это гражданская инженерия, не AI/robotics intensive.'),
        ('AI & Autonomous Systems','7–8','ai,technology','Данные, решения автономных систем и вопросы этики. Наличие собственного робота, платформа и языки программирования не подтверждены.')]
    for i,(title,grades,themes,programme) in enumerate(jrtracks):
        later=fit('later','Потребуется реальный завершённый '+grades+' класс. Опыт соревнований не отменяет школьный минимум.')
        emit(i,'Toronto Jr. DEEP · '+title,'CAN','University of Toronto, St. George, Toronto',themes,'day',
            'Завершённые '+grades+' классы до лагеря; не класс следующей осени',UNKNOWN_EN,programme,
            'Архив 29 июня–21 августа 2026; смешанные курсы в неделях 2, 3, 4, 5, 7, 8. Набор закрыт. Недели и программа 2027 ещё не опубликованы; архивные даты в будущий календарь не перенесены.',
            dict(jrprice),'Дневная программа. Школьный пансион DEEP senior не распространяется на Jr. DEEP.',
            grade_unknown if grades=='3–4' else later,later,[src('Конкретные смешанные курсы, завершённый класс, архивные тарифы и возврат',JR)])
    deepprice=dict(year=2026,label='Тариф 2026: $732 domestic / $1 111 international за академическую неделю. Это не цена 2027. Валюта и налоги явно не подтверждены прочитанной таблицей.',
        included='Исследовательские учебные занятия и итоговый сертификат; академических кредитов не дают.',
        extras='Обед и дорога самостоятельно, lunch break без надзора. Application fee 2027: $50 winter / $60 spring, невозвратный; точные даты раундов ещё TBA. Residence отдельно, новый прайс не опубликован.',
        deposit='Отмена до 23:59 ET в воскресенье за семь дней до курса: возврат за вычетом $135, затем нет. Bursaries приостановлены; старые льготы не включены в семейный расчёт.')
    dmf=fit('later','Старшая школа 9–12; после хотя бы одного года high school. Возможное исключение 8 класса требует уже пройденных обоих Grade 9 Math/Science и разрешения офиса; опыт младшего ребёнка не заменяет эти условия.')
    dof=fit('later','Оскар младше high school; это будущая ступень маршрута, не нынешний лагерь.')
    en='Прямо указано обучение на английском; рекомендуется Upper B2/C1. Если английский не первый язык ученика, требуется загрузить результат теста. Английский младшего Jr. DEEP этим правилом не подтверждён.'
    deepdates=[['2027-07-05','2027-07-09'],['2027-07-12','2027-07-16'],['2027-07-19','2027-07-23'],['2027-07-26','2027-07-30']]
    p=emit(7,'Toronto DEEP · дневные академические недели 2027','CAN','St. George campus, Toronto','engineering,science,technology','day',
        '9–12 классы 2026/27; завершён минимум один год high school',en,
        'Research-led курсы выпускников/исследователей инженерного факультета. Для 9–10 нужны Grade 9 Math/Science; для 11–12 Grade 11 Math/Science. Syllabus 2027 появится во втором раунде: конкретный курс AI или робототехники ещё не гарантирован.',
        '5–9, 12–16, 19–23 и 26–30 июля 2027, 09:30–15:30 ET. Один курс в неделю. Дни академических занятий подтверждены; заявки/цена/темы ещё неполные.',
        deepprice,'Дневное обучение; lunchtime без надзора. Проживание и взрослый сопровождающий отдельно.',dmf,dof,
        [src('DEEP: недели 2027, старшая школа, английский, application и тарифы с явно указанным 2026',DEEP)],
        status='partial_2027',confirmed=['EN'],role='general_instruction',sessions=deepdates)
    p['timing']['session_details']=[dict(start=a,end=b,label='Академическая неделя '+str(n),place=p['place'],source=DEEP,
        price='Цена академического курса 2027 ещё не опубликована; $1 111 international относится к 2026.',
        date_scope='day_camp_window',date_precision='published_session',proof='Собственная страница DEEP прямо перечисляет четыре недели июля 2027. Это 9–12 классы; семейный календарь младших P4 исключает.') for n,(a,b) in enumerate(deepdates,1)]
    emit(8,'Toronto DEEP · будущий пансион старшей школы','CAN','University of Toronto residence, Toronto','engineering,science,general','boarding',
        'Участники DEEP старшей школы 9–12; не Jr. DEEP',en,
        'Residence дополняет академический курс: вечерние и weekend activities, staff support и экскурсии. Не отдельный курс робототехники и не проживание младших братьев с родителями.',
        'Курс DEEP 2027 уже объявлен, но собственная residence-страница всё ещё перечисляет четыре заезда 2026: воскресенье–суббота. Заезд/выезд, комнаты и договор 2027 не опубликованы; жилищных событий в календаре нет.',
        dict(year=2026,label='Архив: $1 875 / неделю проживания дополнительно к DEEP tuition; $900 deposit за каждый session. Это не счёт 2027.',
             included='Одиночная спальня, соседние общие bathrooms, три meals и residence staff; собственное заявление о соотношении не хуже 1:10, включая ночь.',
             extras='DEEP tuition/application отдельно. Airport pickup за доплату; airport drop-off сервис не предлагается. Сотрудники не зарегистрированные медицинские специалисты; медицинская поддержка/страховка отдельно.',
             deposit='Архивные дедлайны отмены: 15/22/29 мая и 5 июня 2026, удерживают deposit $900. На 2027 не перенесены; новый договор нужен.'),
        'Старшеклассник живёт в residence, родители и другие гости в комнаты не допускаются. EN B2 и собственные правила присмотра.',dmf,dof,
        [src('Residence: архив 2026, отдельная цена, комнаты, airport и отмена; прочитано через первичный web-reader',RES),src('Академические недели 2027 не устанавливают residence-даты',DEEP)],status='partial_2027',confirmed=['EN'],role='general_instruction')
    vvprice=dict(year=2026,label='Архив: $339 за 5 дней / $295 за 4. Валюта и налоги явно не установлены выбранными страницами; новый прайс 2027 отсутствует.',
        included='Дневные занятия; $50 deposit входит в цену, не прибавляется повторно.',
        extras='Care 08–09 либо 16–17: +$25 за пятидневную / +$20 за четырёхдневную неделю; оба периода +$50 / +$40. Остаток tuition за 2 недели до старта. Питание и семейное жильё отдельно.',
        deposit='Отмена 29 января–8 июня удерживает $25; 9 июня–за неделю до старта $50; последняя неделя без возврата. В течение 24 часов после регистрации отдельное правило $15. Это даты/политика 2026, не договор 2027.')
    vvtracks=[
        ('Sprockets','JK–SK','general,science,coding','Общая младшая STEM-программа: инженерные задачи, опыты, базовые coding concepts и знакомство с техникой.'),
        ('Explorers','1–2','general,science,coding','Общий STEM: hands-on инженерия, научные опыты и начальная логика программирования; конкретный набор роботов не гарантирован.'),
        ('Nybbles','3–4','general,science,coding','Общий междисциплинарный STEM с опытами, engineering challenges и начальным coding.'),
        ('Terabytes','5–6','general,science,coding','Общий STEM для старшей начальной школы; это не отдельно обещанный интенсив AI или соревновательной робототехники.'),
        ('Game Design Junior','4–6','games,coding,art','Проектирование видеоигры: персонажи, visuals, программирование и игровой процесс. Конкретный engine/язык на этой странице не указаны.'),
        ('Game Design Senior','7–9','games,coding,art','Старшая группа создания видеоигры: характеры, визуальные материалы и программирование; инструменты не подтверждены.'),
        ('Programming Junior','3–5','coding,robotics,technology','Coding fundamentals, робототехника, электроника и разные программные инструменты. Предыдущий опыт программирования не требуется; часы каждого направления и платформы не опубликованы.'),
        ('Programming Senior','6–8','coding,robotics,technology','Старшая группа coding/robotics/electronics; предварительный coding не нужен. Язык и hardware не устанавливаются по названию.'),
        ('Engineering JK–SK','JK–SK','engineering,science','Неделя полностью без компьютеров: практическая инженерия, опыты и демонстрации. Не компьютерный coding/AI курс.'),
        ('Engineering 1–2','1–2','engineering,science','Практические конструкции, научные опыты и инженерные демонстрации; полностью без компьютеров.'),
        ('Engineering 3–4','3–4','engineering,science','Младшая инженерия полностью без компьютеров: challenges, эксперименты и демонстрации.'),
        ('Engineering 5–6','5–6','engineering,science','Инженерные задачи старшей начальной школы, эксперименты и демонстрации, полностью без компьютеров.'),
        ('Engineering 7–8','7–8','engineering,science','Практическая инженерия для 7–8 классов, полностью без компьютеров. Не обязательный курс робототехники.')]
    for i,(title,grades,themes,programme) in enumerate(vvtracks,9):
        low=grades in ['JK–SK','1–2']; high=grades in ['5–6','7–9','6–8','7–8']
        mf=fit('not_eligible','Группа младше школьного уровня Матвея.') if low else fit('later','Потребуется реальный завершённый '+grades+' класс; опыт не отменяет минимум.') if high else grade_unknown
        of=grade_unknown if low else fit('later','Потребуется завершённый '+grades+' класс. Для младшего возраста есть отдельные группы; incoming grade здесь не учитывается.')
        emit(i,'Carleton Virtual Ventures · '+title,'CAN','Carleton University, Ottawa',themes,'day',
            'Класс '+grades+', завершённый в июне года лагеря; не incoming grade',UNKNOWN_EN,programme,
            'Архив 29 июня–21 августа 2026, 09:15–15:45. Содержание одного трека повторяется между неделями: несколько одинаковых недель не новый syllabus. Расписание и Open/Full 2026 не показывают наличие мест 2027.',
            dict(vvprice),'Все перечисленные co-ed треки дневные. Optional Thursday sleepover относится только к Girls Engineering Senior, не к пансиону этих программ для братьев.',mf,of,
            [src('Конкретные треки и отдельная girls-only ночёвка',VV+'types/'),src('Завершённый класс, часы и общие условия',VV),src('Архивное расписание и повторение программы',VV+'schedule/'),src('Архивные тарифы, care, deposit и отмена',VV+'fees/')])
    for i,title in [(22,'Fireball'),(23,'Flare')]:
        emit(i,'McMaster Venture · '+title,'CAN','McMaster University, Hamilton','engineering,coding,science','day',
            'Входящие 2–8 классы следующего сентября; архив 2026',UNKNOWN_EN,
            'Hands-on coding, задачи конструирования и посещения лабораторий с undergraduate engineering staff. Fireball и Flare имеют два различных syllabus: можно выбрать одну неделю каждого без повторения содержания. Подробный hardware и расписание лабораторий не опубликованы.',
            'Архив 6 июля–20 августа 2026, семь недель, 09–16; 3 августа праздник, 21 августа занятий нет. Недели 2027 ещё не объявлены.',
            dict(year=2026,label='Tuition на прочитанной основной странице не опубликован. Цена 2027 также неизвестна; университетский лагерь не объявлен бесплатным.',
                 included='Учебная программа; точный материальный пакет и обед не установлены.',extras='Before/after care предлагается, цена неизвестна. Семейное жильё, дорога и питание отдельно.',deposit='Deposit, отмена и возврат на выбранной публичной странице не найдены; аккаунт CampBrain не создавался.'),
            'Дневной лагерь; постоянный школьный/университетский пансион не следует из места проведения.',
            fit('conditional','Категория 2–8 может подойти Матвею по реальному incoming grade; новый сезон, язык и международный приём отдельно.'),
            fit('conditional','Оскару только если в сентябре после лагеря он действительно поступает минимум во 2 класс; возраст/опыт не заменяют класс.'),
            [src('Venture: два junior syllabus, incoming grade, архивные недели и care',MC)])
    for i,label,age in [(24,'4–7','4–7'),(25,'8–14','8–14')]:
        p=emit(i,'STEM Minds · архив '+label+' · лагеря на паузе','CAN','Архив Aurora; текущий адрес King City / Boreal Farms не подтверждает там работающий лагерь',
            'robotics,coding,games,technology','day','Архивная группа '+age,UNKNOWN_EN,
            'Архивные недельные темы 3D printing, robotics, coding и game design. Текущая страница Camps прямо сообщает Camps on Pause. Старый product catalogue не подтверждает действующий набор; причина паузы не установлена.',
            'Архив 29 июня–4 сентября 2026, 09–16 либо 09–12. Сейчас лагеря на паузе; будущих сессий и событий нет.',
            dict(year=2026,label='Архивная product range $203.40–474.60 против старого index $180–420. Причина, единица пакета и налоговый состав не подтверждены; 2027 quote нет.',
                 included='Архивные занятия; взять собственные nut-free lunch и два snacks.',extras='Архив daily $100 + HST full day / $50 + HST half day. Старая care policy не устанавливает пакет возобновлённого лагеря.',
                 deposit='General class refund policy не перенесена на будущий физический лагерь. Новая работа, адрес, договор и цена требуют отдельной проверки.'),
            'Только архив дневного лагеря; текущая работа и новый адрес занятий не доказаны.',
            fit('not_eligible','Сейчас набор не предложен: Camps on Pause; архивная возрастная совместимость не означает доступный лагерь.'),
            fit('not_eligible','Сейчас набор не предложен: Camps on Pause; архивная группа не открывает регистрацию.'),
            [src('Текущая собственная страница: лагеря на паузе',SM+'camps/'),src('Старый продукт Summer Camp 2026',SM+'product/summer-camp-2026/'),src('Старая общая policy, не новый договор',SM+'policies-and-procedures/')])
        p['availability']=dict(status='closed',label='Лагеря на паузе',checked=CHECKED,reason='Camps on Pause — текущая программа приостановлена; это не вывод о закрытии организации.',source=SM+'camps/')
    iden='Собственный help centre прямо принимает иностранных учеников и говорит, что все курсы на английском: нужны базовые reading/speaking/listening. Язык подтверждён; персональный допуск и миграционные условия этим не установлены.'
    idsources=[src('Иностранный приём и английский всех курсов; первичный web-reader',HELP+'do-you-accept-international-students'),
        src('Только общий минимум возраста к 31 декабря; возможны более строгие курсы',HELP+'can-you-make-an-age-exception'),
        src('Группы 7–9/10–12/13–17 и общая политика minimum',HELP+'are-your-camps-segmented-by-age-21-8-2018'),
        src('Разные day/overnight минимумы, room/board, lunch и условия оплаты',ID+'tech-camps')]
    for i,title,age,tail,price,programme in [
        (26,'BattleBots Junior','7–9','battlebots-camp-junior',1199,'VEX IQ и VEXcode IQ block coding: механизмы, управление, работа с товарищами и внутренний BattleBots-style турнир. Не официальный VEX Worlds и не обещанный take-home робот.'),
        (27,'BattleBots with VEX Robotics','10–12','battlebots-camp-with-vex-robotics',1299,'VEX V5: programmable brain, моторы, attachments, управление и командные задачи. Это V5, не VEX IQ; внутренний BattleBots-style турнир не официальный международный титул.'),
        (28,'BattleBots · 3D Printing and Take-Home Robot','10–12','battlebots-camp-3d-printing-and-take-home-robot',1399,'Собственный iD Tech kit: motor chassis, wiring programmable brain, Arduino IDE/Bluetooth control, 3D-printed armor и attachments; итерации и внутренние игры. На этом курсе прямо обещают забрать собранного робота и напечатанные детали домой.')]:
        jr=i==26
        mf=fit('conditional','В 2027 Матвею 9–10: верхнюю границу Junior и её контрольную дату надо подтвердить. Правило 31 декабря явно относится к минимуму и не доказывает максимальный возраст.') if jr else fit('conditional','В 2027 достигает общего минимума 10 к 31 декабря. Конкретный курс может применять более строгую границу; summer admission и boarding отдельно.')
        of=fit('conditional','В 2027 Оскар достигает общего минимума 7 к 31 декабря, даже если летом ещё 6. Конкретный Junior может иметь более строгий минимум; допуск не подтверждён. Только дневной формат.') if jr else fit('later','10–12 лет, Оскар младше. Его опыт не заменяет минимальный возраст курса.')
        p=emit(i,'iD Tech · '+title,'USA','Кампус США выбирается отдельно; место университета не означает его академическое зачисление',
            'robotics,coding,engineering'+(',technology' if i==28 else ''),'day' if jr else 'day,boarding',
            age+' по карточке; общий MINIMUM к 31 декабря, maximum и исключения по конкретному курсу',iden,programme,
            'Summer 2027 объявлен; страница говорит registration opens November 8, без явного года этой даты. Недели выбранного кампуса, места и финальный тариф 2027 не установлены; 8 ноября в ICS не добавлено.',
            dict(year=None,label='На текущей карточке от $'+format(price,',')+' / неделю; год цены не указан. Это нижняя стартовая цена, не полный счёт 2027.',
                 included='Недельный course project, учебный diploma/transcript; '+('take-home робот и его 3D детали прямо заявлены в данном syllabus.' if i==28 else 'передача личного робота домой не обещана.'),
                 extras='Общая страница: room and board от $679/неделю с meals только для overnight 10–17; lunch дневным от $70/неделю. Применимость, год, taxes, campus и availability отдельно; минимумы разных страниц не сложены в готовый quote.',
                 deposit='$375 starting payment — часть/этап оплаты, не полная tuition. Общая in-person policy: до 1 марта full refund, затем не позднее 28 дней до старта удерживают $250/неделю плюс extras; ближе 28 дней возврата нет. Год/контракт конкретного набора подтвердить; правила online courses не перенесены.'),
            'Junior только днём: общая boarding граница 10–17. Для старших выбранные campuses могут иметь day/overnight; жильё родителей вне детского пакета.',mf,of,
            [src('Конкретный syllabus, hardware, возраст и стартовая цена',ID+'courses/'+tail),src('BattleBots lineup и объявление следующего сезона',ID+'bots')]+idsources,
            status='partial_2027',confirmed=['EN'],role='technical_instruction')
        p['questions'] += ['Получить campus-specific minimum/maximum age, включая контрольную дату верхней границы. Общий Dec 31 minimum не перенесён на maximum.', 'Получить конкретные недели, все extras, тариф и условия именно 2027; виртуальные/частные уроки имеют другой договор.']
    emit(29,'The Tech Interactive · CAMP · лето 2027','USA','201 S. Market St., San Jose, California','general,science,engineering,art,technology','day',
        'Incoming grades 2–6; школьный класс, не просто возраст',UNKNOWN_EN,
        'Проекты инженерного дизайна, выставочные interactive galleries, laboratories, IMAX и коллективные weekly themes в музее науки. Общий STEAM; отдельный полноценный robotics/AI intensive не обещан. Для IMAX предусмотрена альтернативная активность.',
        'Собственная страница прямо объявляет возвращение Summer 2027. Список конкретных недель, часы и tuition не опубликованы. FAQ no camp Friday July 3 относится к прежнему сезону: 3 июля 2027 — суббота, эта фраза не определяет новую смену.',
        dict(year=2027,label='Прайс 2027 не опубликован; регистрационный пакет и места не подтверждены.',
             included='Standard activities, материалы и museum experiences по FAQ.',extras='Lunch не включён, optional cafe purchase; extended care за доплату. Размер multi-week discount не указан; отдельная sibling скидка не доказана. Scholarships сейчас не предлагаются.',
             deposit='Текущий общий FAQ: письменная отмена за 60+ дней полный возврат; 30–59 дней 50%; менее 30 дней нет. Перенос без штрафа не позже двух недель при наличии места. Конкретный новый договор ещё нужен.'),
        'Дневной музейный лагерь, не пансион. Lunch и snack supervised; жильё семьи отдельно.',
        fit('conditional','Реальный incoming grade 2–6 может подойти; выбранные темы, English instruction и приём приезжей семьи ещё подтвердить.'),
        fit('conditional','Только если incoming grade минимум 2. Семейное посещение музея отдельно не даёт admission в лагерь.'),
        [src('Объявление Summer 2027, incoming grade, программа и текущий FAQ',TECH+'camp/')],status='partial_2027')

def extend_report_v131(r):
    r['version']=131;r['asof']=CHECKED
    r['shortlist'] += [dict(label='Toronto · семь junior курсов и будущий DEEP',slugs=NEW[:9],reason='Jr. DEEP требует завершённый класс; senior DEEP уже имеет четыре недели июля 2027, но школьный минимум 9–12 и цена/комнаты другого года. Пансион junior не подтверждён.'),
        dict(label='Канада · разные STEM syllabus и правила класса',slugs=NEW[9:24],reason='Carleton: 13 смешанных age/grade треков, завершённый класс, инженерные группы без компьютеров. McMaster: два разных syllabus Fireball/Flare, incoming grade. Пока архив 2026, EN teaching и иностранный junior intake не доказаны.'),
        dict(label='Канада · приостановленные программы',slugs=NEW[24:26],reason='Текущая STEM Minds Camps on Pause имеет приоритет над старым product catalogue. Архив сохраняется для сравнения, но доступные семейные варианты и будущие даты не создаются.'),
        dict(label='США · BattleBots и музейная инженерия',slugs=NEW[26:],reason='iD Tech: Junior VEX IQ 7–9, V5 10–12 и отдельный 3D take-home kit. EN/foreign intake подтверждены; minimum by Dec 31 не доказывает maximum. The Tech summer 2027 объявлен без недель/прайса и требует incoming grade 2–6.')]
    gaps=[('CAN','Toronto Jr. DEEP · junior 2027 и язык',JR,'Семь смешанных syllabus и завершённый класс проверены только в архиве 2026. Новые недели, цены, EN teaching и иностранный приём junior ещё не доказаны. Senior EN/boarding policy не перенесена на junior.'),
        ('CAN','Toronto DEEP · академия и residence разных лет',RES,'Academic weeks 2027 уже опубликованы. Tuition $732/$1111 прямо за 2026; residence $1875 и deposit $900 также 2026. Даты/договор проживания 2027 отдельно; 403 обычного HTTP разрешился только чтением первичного web-reader, не действующим аккаунтом/бронью.'),
        ('CAN','Carleton · новый набор, язык и старые места',VV,'13 co-ed grade/format tracks — один оператор. Все недели, Open/Full и fees 2026 архивные. Минимум завершённого класса, EN teaching, international grade equivalence и прайс 2027 отдельно. Girls Senior sleepover не жильё co-ed для братьев.'),
        ('CAN','McMaster · syllabus и полный quote',MC,'Incoming Grade 2–8, два junior curricula Fireball/Flare. Прайс, отмена, EN teaching, лабораторные часы и приезжий admission не найдены на выбранной публичной странице; 2027 ещё не объявлен.'),
        ('CAN','STEM Minds · текущая пауза',SM+'camps/','Текущая Camps on Pause важнее старого продукта 2026. Новый адрес не доказывает там действующий лагерь. Product range расходится со старым index; объяснение/tax inclusion не выведено из математического сходства.'),
        ('USA','iD Tech · возраст, campus и полный пакет 2027',ID+'bots','Dec 31 policy явно про MINIMUM, не maximum. Английский/foreign intake проверены через свой help centre, direct HTML — пустые JS shells. Nov 8 без явного года, недели кампуса и final prices не опубликованы. Deposit $375 не tuition, room/board отдельно; внутренний турнир не VEX Worlds.'),
        ('USA','The Tech · лагерь и проектный showcase',TECH+'camp/','CAMP Summer 2027 обещан без конкретных недель/fees/EN teaching. Отдельный Tech Challenge 2027 прямо не competition, Grades 4–12, Grade 3 нельзя; семья может быть зрителями, ticket/booking условия неизвестны. Q&A times без timezone; Test Trials registration January в events против February в FAQ.'),
        ('CAN','STEM Camp · доступ к полным первичным условиям','https://stemcamp.ca/','Selected Mississauga и Guide direct retrieval дали 403. По search snippets не создаются verified curricula/fees/даты. Emagination отдельно уже отмечен в прежнем gap: нынешний landing несвязанный; новую семейную программу на этом основании не добавили.')]
    r['gaps'] += [dict(iso=iso,country={'CAN':'Канада','USA':'США'}[iso],provider='v131 · '+title,url=url,detail=detail,
        next_action='Продолжить новые сезоны, языковые и возрастные условия всех приоритетных стран; ни одна страна не признана полностью изученной.') for iso,title,url,detail in gaps]
    additions=[('id-battlebots-junior',['technical'],'Английская младшая робототехника VEX IQ с явным foreign intake.','Оскар достигает общего минимума 7 к 31.12.2027, но курс может строже. У Матвея maximum Junior отдельно; 2027 weeks/quote ещё нет.'),
        ('id-battlebots-vex',['technical','future'],'Следующий технический курс Матвея с VEX V5 и командной инженерией.','10–12; Oscar позже. Minimum by Dec 31 не гарантия курса/boarding; внутренний турнир не международная победа.'),
        ('thetech-camp-2027',['technical','general'],'Музей, проекты и инженерные задачи в Silicon Valley.','Incoming Grade 2–6; Оскару только при реальном Grade 2. EN instruction, даты, прайс и приезжий приём не подтверждены.'),
        ('carleton-explorers',['general','technical'],'Школьная STEM-группа Оскара по завершённому классу.','Completed Grade 1–2, не incoming grade; архив 2026. EN teaching/foreign intake и 2027 quote ещё нужны; Матвей старше.'),
        ('carleton-nybbles',['general','technical'],'Общая инженерия, наука и coding Матвею по классу.','Completed Grade 3–4; младший Oscar позже. EN teaching и новый набор отдельно, архивные Open/Full не места 2027.'),
        ('carleton-programming-junior',['technical'],'Матвею сравнить coding/robotics/electronics с возрастными сверстниками.','Completed Grade 3–5, beginner-friendly; для опытного ребёнка уточнить сложность. Язык, hardware и 2027 не доказаны.'),
        ('mcmaster-fireball',['technical','general'],'Дневные проекты и лабораторное знакомство; можно чередовать Fireball/Flare.','Incoming Grade 2–8; Oscar только при реальном Grade 2. Нет публичного quote/EN teaching/приёма семьи, 2027 ещё не объявлен.')]
    review=r['family_review'];ps={p['slug']:p for p in r['profiles']};exists={q['slug'] for q in review['entries']}
    review['entries'] += [dict(slug=s,goals=g,reason=why,key_limit=limit,dossier_checked=ps[s]['checked']) for s,g,why,limit in additions if s not in exists]
    review.update(version=131,asof=CHECKED)
    review['coverage']=dict(candidates=len(review['entries']),countries=len({ps[q['slug']]['iso'] for q in review['entries']}),fully_audited_countries=0)
    r['counts']=dict(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),swiss=sum(p['iso']=='CHE' for p in r['profiles']),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))

def enrich_v131(d):
    """A regional non-competitive programme; never add its showcase as a C-record."""
    tcsrc=[dict(title=title,url=url,checked=CHECKED) for title,url in [
        ('Game On! 2027: showcase days and project',TC),('Grades, team, visitors, price and registration',TC+'faq/'),
        ('Interest/Q&A, orientation and trial dates; timezone not stated',TC+'participant-events/'),
        ('Rules and game rig',TC+'rules-and-rig/'),('English rules v3: explicitly not a competition',RULES),('Game/device dimensions poster',POSTER)]]
    grade='4–12 классы; 3 класс прямо исключён, даже при опыте; 2–6 детей и взрослый adviser'
    hardware='Физическая игра до 3 минут для 1–2 игроков; не обязательная робототехника. Purchased parts разрешены, purchased kits запрещены. Footprint 76,2×76,2 см, высота 183 см с table; player area 2,74×2,74 м. Drone/flying devices и toy guns запрещены.'
    rows=[]
    def event(eid,title,day,end,kind,scope,source,entry,note,deadline='',deadline_label=''):
        rows.append(dict(id=eid,block='События',title=title,country='США',region=next(c['region'] for c in d['countries'] if c['iso']=='USA'),
            city='Онлайн / Zoom' if kind=='organizer_information_session' else '201 S. Market St., San Jose, California',start=day,end=end,
            period=day+'–'+end,date_status='Подтверждено',deadline=deadline,deadline_label=deadline_label,
            age=('Ознакомление родителей/advisers; целевая команда '+grade) if kind=='organizer_information_session' else grade,
            mat='Семейное ознакомление; не командный допуск' if kind=='organizer_information_session' else 'Уточнить — для команды нужен реальный 4 класс; семейный зритель отдельно',
            osc='Семейное ознакомление; не командный допуск' if kind=='organizer_information_session' else 'Зритель — участие ниже 4 класса не допускается',
            format='Онлайн для родителей/advisers' if kind=='organizer_information_session' else 'Проектная команда / семейные зрители; правила различаются',
            entry=entry,gear=hardware,language='Rules English опубликованы; ES/Vietnamese coming soon. Non-EN interview accommodation по заранее согласованному запросу; язык Q&A и судейства не гарантирован.',
            cost='Early fee $150 / команда до 31.12.2026, $300 с 01.01.2027. Валюта/налоги явно не установлены; цена семейного посещения и Q&A не найдена. Это ранний тариф, не финальный registration deadline.',
            level='D — региональный инженерный проект и показ',reward='Программа прямо не competition; проект, журнал и обратная связь. Международные медали или квалификация мировых лиг не обещаны.',
            priority='P3 — дополнительный инженерный маршрут',action='Проверить реальный класс, foreign intake, конкретный слот, язык, полный счёт и правила посетителей. Онлайн-встречи доступны как ознакомление; заявки не отправлялись.',
            source=source,proof='Собственные публичные FAQ/events и English rules v3 прочитаны; clauses и PDF сохранены отдельно.',checked=CHECKED,status='Идея',note=note,
            iso=['USA'],themes=['engineering','games','technology'],scope='regional',importance_reason='Подготовка инженерного портфолио и знакомство с Tech Interactive; не международная соревновательная лига.',
            languages=[],participation='organizer_information' if kind=='organizer_information_session' else 'family_visit' if kind=='project_showcase' else 'team_registration',
            language_certainty='Rules EN; instruction/judging not guaranteed',event_kind=kind,evidence_level='program',date_scope=scope,date_precision='published_session'))
    event(EVENT_IDS[0],'The Tech Challenge 2027 · Game On! · показ инженерных проектов','2027-04-30','2027-05-01','project_showcase','festival_window',TC,
        'Grade 4–12, команда 2–6 + adviser; зарегистрированная команда резервирует отдельный showcase slot. Можно выбрать любой ОДИН день, не требуется два. FAQ приветствует младших семейных зрителей, ticket/booking условия ещё нужны.',
        'Challenge прямо не соревнование. Показ 30 апреля или 1 мая; точный slot позднее. Under-16 нельзя быть volunteer и идти с parent-volunteer, но это не запрет семейных зрителей. Grade 3 нельзя в команду. Test Trials registration opens January в events против February в FAQ.',
        deadline='2026-12-31',deadline_label='Последний день раннего командного тарифа')
    event(EVENT_IDS[1],'The Tech Challenge 2027 · объявленное открытие регистрации','2026-10-06','2026-10-06','registration_milestone','registration_open',TC+'faq/',
        'FAQ объявляет открытие 6 октября 2026; регистрационный аккаунт и форму не открывали. Объявление не доказывает фактическую доступность места.',
        'Открытие регистрации, не день турнира. Early fee до 31 декабря — граница цены; окончательный closing deadline неизвестен. Title I/public after-school waiver не назначается зарубежной семье автоматически.')
    for day,clock in QA:
        event('TC2027-QA-'+day.replace('-',''),'The Tech Challenge 2027 · ознакомительная Q&A для семьи · '+day,day,day,'organizer_information_session','workshop_window',TC+'participant-events/',
            'Interest meeting/Q&A для prospective parents и advisers по собственному расписанию Zoom. Регистрация/ссылка и язык встречи отдельно.',
            'На странице время '+clock+', но timezone не указан: в календаре только день, без предполагаемого UTC/PT. '+('20 октября presentation и Q&A recorded; ' if day=='2026-10-20' else '')+'Это знакомство с программой для семьи, не детское соревнование или выставка компаний.')
    d['events']=[e for e in d['events'] if e['id'] not in EVENT_IDS]+rows
    p=dict(id=PROFILE_ID,name='The Tech Challenge · инженерная программа и showcase',group='regional',age_summary=grade,age_tags=['9','10-12','future'],
        summary='Региональная командная инженерия и портфолио. English rules прямо говорят: challenge, не competition. Младший ребёнок может прийти семейным зрителем, но не участником команды.',
        categories=[dict(name='Game On! 2027 · физическая игра',age=grade,team='2–6 детей + взрослый adviser; division по самому старшему классу',hardware=hardware,
            age_rule='Реальный школьный класс; Grade 3 прямо исключён',entry=rows[0]['entry'],event_id=EVENT_IDS[0])],event_ids=EVENT_IDS,legacy_ids=[],
        route=['Проверить Grade 4+, собрать 2–6 детей и adviser; дети из разных школ разрешены.',
            'Познакомиться с Game On! на Q&A; часы без timezone пока не переводить.',
            'Спроектировать физическую игру детьми; ориентир организатора 15–30 часов за сезон.',
            'Вести инженерный журнал, playtest и итерации; adviser помогает, но не делает проект.',
            'Согласовать team orientation/test trials и слот одного дня showcase.',
            'Сохранить журнал, собственный вклад и обратную связь; не записывать проектный показ как международную победу.'],
        hardware=hardware,language=rows[0]['language'],importance='Дополнительная региональная инженерная программа; не международная лига и не квалификация FIRST/VEX/WRO.',
        strengths='Детский инженерный журнал, реальная проверка игры пользователями, командные роли и семейный музейный опыт.',
        requirements=['4–12 классы, 2–6 учащихся, взрослый adviser; grade самой старшей роли определяет division.',
            '4–6: tutorial до 1 минуты и минимум один documented playtest; 7–12: до 30 секунд и минимум два.',
            'Журнал PDF, интервью и работающий проект — три области обратной связи.',
            '1–2 собственные сумки 55×37×35 см для устройства; дети устанавливают проект без взрослых.'],
        nuances=['Для команды Grade 3 и младше нельзя; семейные spectators — отдельный допуск.',
            '30 апреля–1 мая 2027: выбирается один день; дополнительного showcase team fee нет.',
            'Early fee deadline 31 декабря не closing deadline; личный admission и foreign eligibility не доказаны.',
            'Orientations 14.11.2026/23.01.2027; test trials 07/13.02,03/04/17/24.04.2027; March TBD. Нужны собственные слоты. Registration January/February конфликтует между двумя страницами.',
            'Rules EN уже есть; ES/Vietnamese coming soon и advance interview accommodations не гарантируют испанское судейство.'],
        cost=rows[0]['cost'],award=rows[0]['reward'],sources=tcsrc,evidence='Selected primary programme/FAQ/PDF clauses; regional non-competitive classification explicit. Не установлен независимый ranking или personal admission.',checked=CHECKED)
    guide=d['league_guide'];guide['profiles']=[q for q in guide['profiles'] if q['id']!=PROFILE_ID]+[p]
    guide.update(version=131,checked=CHECKED)
    existing={s['url'] for s in d['sources']}
    for s in tcsrc:
        if s['url'] not in existing:
            d['sources'].append(dict(s,evidence='Первичные правила региональной инженерной программы и события; это прямо не competition.'));existing.add(s['url'])
