"""Asian camp curricula, course-specific schedules and complete mandatory fee arithmetic."""
from pathlib import Path
from camp_europe_v127 import readable
from camp_planning_v108 import offer
ROOT=Path(__file__).resolve().parents[1]
BASE='a0ccbe5b08d9a772ef7e560ddd7a637dd180f523'
CHECKED='2026-10-06'
C='https://www.coboacademy.com/'
CT=C+'tnp/index.asp'
O='https://owis.org/jp/admissions/events-and-webinars/owis-winter-camp/'
OA='https://owis.org/jp/specified-commercial-transactions-act/'
K='https://www.kas.tw/dragoncamp/'
KP='https://www.kas.tw/wp-content/uploads/2026/03/Dragon-Camp-2026-Schedule.pdf'
KT='https://docs.google.com/document/d/17Hn0ju1a1IQz2TkdFf0hluH3DiDXjZI0k1DZ9-R6Y0Y/edit?usp=sharing'
H='https://images.headstartphuket.com/en/additional-programmes/summer-camp'
HP='https://images.headstartphuket.com/downloads/2924'
B='https://brightoncollege.ac.th/vibhavadi/july-camp'
BP='https://brightoncollege.ac.th/assets/files/uploads/a4t-summer-camp-2026-final-1.pdf'
BS='https://brightoncollege.ac.th/file/48/1778145303/brighton-camp-schedules-6-12yo-stem-artscrafts.pdf'
BD='https://brightoncollege.ac.th/file/49/1778145330/description-of-camp-activities-for-marketing.pdf'
BI='https://brightoncollege.ac.th/assets/img/resized/text-image--mobile/july-camp-social-final-wel-a-02.jpg'
NEW=['cobo-wedo-junior','cobo-spike-junior','cobo-spike-senior','cobo-vex-senior','cobo-arcade-junior','cobo-arcade-senior','cobo-ai-junior','cobo-ai-senior','cobo-hackathon-principal',
     'owis-osaka-winter','kas-global-plate','kas-future-city','headstart-activity','headstart-around-world','headstart-discovery','headstart-adventure','headstart-english-focus','brighton-vibha-general','brighton-vibha-ai']
NEW_IDS=['owis-winter-both-external','cobo-vex-matvey','cobo-spike-oscar']
COBO_IDS=[3,210,211,186,223,224,189,190,237]
COBO_DATED={1:('10:00','12:00','WAN CHAI'),2:('14:00','16:00','WAN CHAI'),3:('14:00','16:00','WAN CHAI'),6:('10:00','12:00','HKPC Building'),8:('10:00','12:00','WAN CHAI')}
COBO_TERMS='Общие условия: полная оплата минимум за 3 недели; после подтверждённой регистрации платежи невозвратны. Holiday Camps не имеют make-up. Typhoon8/black rain/public-health cancellation без refund/make-up. Правила term credits не обещают возврат пропуска camp. Приём в продвинутую группу может потребовать assessment; до/после 2-часового занятия сопровождение семьи.'

def add_asia_v128(add,src,fit,profiles):
    names={'HKG':'Гонконг','JPN':'Япония','TWN':'Тайвань','THA':'Таиланд'}
    def emit(i,name,iso,place,themes,age,language,programme,label,price,housing,mf,of,sources,status='next_unannounced',confirmed=None,role=None,sessions=None):
        add(NEW[i],name,names[iso],iso,place,themes,'day',age,language,programme,label,price,housing,mf,of,
            'Редакционный кандидат по собственному учебному плану и условиям. Независимый мировой рейтинг качества и результаты соревнований этим лагерем не доказаны.',
            ['До записи подтвердить места, конкретную группу, приём приезжей семьи и полный счёт. Заявки, аккаунты и оплаты не выполнялись.'],sources,status=status,confirmed=confirmed,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        return p
    junior_m=fit('conditional','Матвей2017 в октябре2026 имеет8–9лет: Junior6–8 только до9-летия; после нужен Senior9–11. Это не автоматический перевод между группами.')
    junior_o=fit('conditional','Оскар2020 в октябре2026 имеет5–6лет: Junior6–8 только после6-летия. Требования курса и приём приезжей семьи отдельно.')
    senior_m=fit('conditional','Senior9–11 для Матвея только после9-летия к первому занятию. Опыт трёх лет не заменяет возраст и prerequisite.')
    senior_o=fit('later','Оскар младше минимума9; старшая группа пока будущий маршрут.')
    courses=[
      ('LEGO WeDo · Junior','robotics,science','6–8','Датчики и моторы, события и циклы, чтение сборочных инструкций. Дети строят и программируют модели по темам механики, биологии и природных явлений. Вводное блочное программирование; набор домой не обещан.',junior_m,junior_o),
      ('LEGO SPIKE Prime · Junior','robotics,coding','6–8','Инженерный цикл: модели протезов, сейфов с датчиками и моторами, автономных автомобилей. Проектирование, испытания, поиск ошибок и улучшение конструкции. Нужен предыдущий опыт LEGO WeDo 2.0 и Scratch; свой ноутбук PC/Mac/Chromebook с зарядкой. Покупка набора SPIKE домой в карточке не указана.',junior_m,junior_o),
      ('LEGO SPIKE Prime · Senior','robotics,coding','9–11','Модели протезов, защищённых механизмов и автономных автомобилей, программирование и повторные испытания. Предыдущий опыт WeDo 2.0 и Scratch обязателен; свой ноутбук PC/Mac/Chromebook с зарядкой. Senior имеет отдельную возрастную группу и расписание.',senior_m,senior_o),
      ('VEX IQ · Senior','robotics,coding,technology','9–11','Механика, передачи, датчики и моторы, инженерный цикл. Blocks/C++/Python указаны как возможности платформы; 15+ сборок — общее описание курса, их не обещают все за восемь часов. Учебное оборудование предоставляет оператор; нужны ноутбук PC/Mac/Chromebook или iPad, зарядка и VEXCode IQ. Сертификация преподавателей заявлена самим оператором; это не квалификация на VEX Worlds.',senior_m,senior_o),
      ('MakeCode Arcade · Junior','games,coding','Заголовок6–8, основной syllabus говорит8+: конфликт для6–7лет','Спрайты и анимация, события, циклы, условия и переменные; дети создают собственные аркадные игры. Портативную консоль забирают домой. Нужны свой PC/Mac, зарядка и USB-C адаптер. Сбор за консоль HKD 400 помечен inclusive; включение этих 400 в общий тариф требует уточнения.',fit('conditional','Если Матвею ещё8, совпадают Junior6–8 и текст8+; после9 нуженSenior. Конкретных дат этой карточки нет.'),fit('unknown','ЗаголовокJunior6–8 расходится с текстом8+. Оскару5–6, доступность после6 не подтверждена.')),
      ('MakeCode Arcade · Senior','games,coding','9–11; основной syllabus8+','Блочное программирование MakeCode, спрайты, уровни и правила собственных игр. Портативную консоль забирают домой; PC/Mac, зарядку и USB-C адаптер приносит семья. Сбор HKD 400 помечен inclusive; включение в основной тариф должен подтвердить итоговый счёт.',senior_m,senior_o),
      ('AI Fundamentals · Junior','ai,coding','6–8','Блочные программы, компьютерное зрение, распознавание текста, речи и лиц; дети собирают изображения для обучения модели в Teachable Machine. Предыдущий опыт программирования обязателен; новичкам сначала предлагают Scratch. Нужны собственный PC/Mac и зарядка.',junior_m,junior_o),
      ('AI Fundamentals · Senior','ai,coding','9–11','Распознавание объектов, речи и изображений, алгоритмы, данные для обучения и модель Teachable Machine. Нужны собственный PC/Mac и зарядка. Обязательный начальный опыт указан у Junior; в карточке Senior такое требование отдельно не опубликовано.',senior_m,senior_o),
      ('Vibe Coding Hackathon · Principal','ai,coding,entrepreneurship','12–14','Дизайн интерфейсов в Figma и создание приложения с помощью AI в Base44: идея, прототип, работающий сайт и финальная презентация. Дети получают приложение и дизайн-портфолио; награды относятся к внутреннему лагерному показу. Предыдущий опыт кода не требуется; нужен ноутбук с зарядкой. Общее описание пяти дней расходится с точным октябрьским расписанием: четыре урока, восемь часов.',fit('later','Матвей ещё8–9, минимум12 не достигнут. Будущий путь к app/pitch; не текущая международная лига.'),fit('later','Оскар ниже12; внутренний Hackathon не отменяет возраст.'))]
    for i,(title,themes,age,programme,mf,of) in enumerate(courses):
        u=C+'camp_detail/index.asp?CourseID='+str(COBO_IDS[i]);dated=i in COBO_DATED
        time=COBO_DATED.get(i);place=('Wan Chai · 23ThomsonRoad,6/F' if not time or time[2]=='WAN CHAI' else 'HKPC Building ·78TatCheeAvenue,KowloonTong')
        price=dict(year=2026,label='HKD3600 за4 занятия/8часов, по конкретному расписанию.' if dated else 'Общий October menu: HKD3600/4дня или4500/5дней. У этого курса собственная текущая строка расписания/счёт не опубликована.',
            included='Одно 2-часовое занятие в день; typical class4–8 по оператору. Набор робота домой не обещан; только Arcade прямо включает переносную консоль домой.',
            extras='Laptop+charger по syllabus приносит семья; daycare между/вне уроков, питание, travel и lodging отдельно. Early-bird до30сентября уже истёк; Buddyextra10% не применён без условий. Для Arcade material fee400(inclusive) требует уточнения счёта.',deposit=COBO_TERMS)
        p=emit(i,'Cobo Academy · '+title,'HKG',place,themes,age,'Medium of Instruction:English прямо в каждой собственной карточке; не вывод из языка сайта.',programme,
            '20–23октября2026,Вт–Пт, '+time[0]+'–'+time[1]+',8часов; место и late-registration отдельно.' if dated else 'October2026menu опубликован, но Schedule именно этого курса пуст. Не переносим все4недели общих camps на этот конкретный syllabus.',
            price,'Короткий дневной курс, пансиона и полного дня нет. Родитель организует поездку, проживание и pickup; KowloonTong бывает selected classes по запросу.',mf,of,
            [src('Конкретный syllabus, age, prerequisites и Schedule',u),src('Общие текущие октябрьские недели и expired early-bird',C+'holiday-camps/'),src('Enrollment, оплата, weather и сопровождение',CT)],
            status='published_2026' if dated else 'partial_2026',confirmed=['EN'],role='primary',sessions=[['2026-10-20','2026-10-23']] if dated else [])
        if dated:
            p['timing']['session_details']=[dict(start='2026-10-20',end='2026-10-23',label=title,price=price['label'],place=place,source=u,date_scope='session_days',date_precision='published_session',
                proof='Именно собственная строка курса показывает4даты,Tue–Fri,один2hслот,venue иHKD3600.',sessions=[dict(date='2026-10-'+str(n),start_time=time[0],end_time=time[1],timezone='Asia/Hong_Kong',ical_timed=True,topic=title) for n in range(20,24)])]
    both=fit('conditional','Возраст 4–16 подходит обоим, внешние ученики прямо допускаются. Места и окончательные условия подтвердить; на странице регистрация пока помечена как не открытая.')
    p=emit(9,'OWIS Osaka · Winter Camp 2026','JPN','3-1-39Shariji,Ikuno-ku,Osaka544-0022','general,languages,art,sport,science','4–16',
        'Зимняя страница прямо заявляет английскую среду с международными преподавателями. Английский используется в общих активностях; отдельный интенсив робототехники не обещан.',
        'Творческие проекты, спорт, выезды и приглашённые преподаватели; подробный план 2026 ещё разрабатывается. Лепка арктических животных, покадровые мультфильмы, кулинария и поездка в Mt. Rokko Snow Park приведены как примеры прошлой программы. Они не стали гарантированными занятиями 2026. Робототехнические лаборатории школы не означают наличие зимнего курса робототехники.',
        '14–18 декабря 2026. Приход 08:30–08:45, занятия с 09:00, забирать 15:30–16:00; выезды могут изменить часы. Даты опубликованы, но на странице регистрация пока не открыта: предлагают проверить в октябре.',
        dict(year=2026,label='Новый внешний участник: JPY 70 000 обучение + 5 000 материалы + 15 000 первая регистрация = 90 000 до налога; с 10% налогом JPY 99 000. Двое впервые: JPY 198 000. Расчёт по опубликованным компонентам.',
            included='Недельная программа. Включение обеда 2026 ещё подтвердить: горячие обеды приведены как часть прошлой программы.',
            extras='У бывшего участника сезонного лагеря без первой регистрации расчёт JPY 82 500 с налогом. Школьный тариф JPY 60 000 семье не назначен. Дорога, жильё, страховка и возможная стоимость обеда ещё требуют сметы. Школьного автобуса и пансиона нет.',
            deposit='Зимняя карточка не публикует шкалу отмены. Документ в подвале относится к Tsukuba и говорит о включённом налоге; Osaka Winter прямо добавляет 10%. Общие условия сайта относятся к Singapore и не заменяют договор лагеря Osaka.'),
        'Дневной лагерь: пансиона нет, школьный автобус не работает. Семья организует жильё и ежедневный транспорт. Кнопка расписания не содержит ссылки; подробный текущий PDF не получен.',both,both,
        [src('Собственная WinterCamp2026: допуск, часы и компонентный прайс',O),src('FooterAct: Tsukuba, не готовый договор OsakaWinter',OA)],status='published_2026',confirmed=['EN'],role='camp_life',sessions=[['2026-12-14','2026-12-18']])
    p['timing']['session_details']=[dict(start='2026-12-14',end='2026-12-18',label='WinterCamp2026',price=p['price']['label'],place=p['place'],source=O,date_scope='day_camp_window',date_precision='published_session',proof='OwnWinter2026 card shows14–18December; admission external4–16 and noovernight/no schoolbus directly stated.')]
    kg=fit('unknown','Обязательная категория: PK–G5 и обучение в школе с английским преподаванием. Фактический класс и тип школы неизвестны. Владение английским само по себе не подтверждает этот допуск.')
    for i,title,programme in [(10,'The Global Plate','Кулинарные культуры и исследования пути продуктов от фермы до стола, последовательности действий, письмо и исследования. В расписании есть Makerspace и физкультура. Отдельный курс робототехники не заявлен.'),(11,'Future City Builders','Архитектура и устойчивый город, техническая грамотность, аргументация идей и правила сообщества. Дети переходят от эскизов к объёмным моделям; 3D-печать, роботы и AI отдельно не заявлены.')]:
        emit(i,'Kaohsiung American School · '+title,'TWN','889CueihuaRoad,ZuoyingDistrict,Kaohsiung813035','general,science,technology,art','PK–G5 из English-basedschools',
            'Допускаются ученики школ с обучением на английском. Язык всего лагеря и Makerspace отдельно не установлен; английский сайт и школьная категория не стали подтверждением языка занятий.',programme,
            'Архив 2026: Global Plate 13–17 июля, Future City 20–24 июля по PDF. В договоре первая смена ошибочно 13–20 июля. Набор 2026 закрыт, даты 2027 не объявлены; новые будущие заезды не добавлены.',
            dict(year=2026,label='Архив договора от 19 марта 2026: NTD 16 500 обычный тариф или 15 500 ранний за смену. Цена 2027 неизвестна; ранняя скидка прошлого сезона не считается текущей.',
                included='Ежедневный обед прямо включён в договор 2026; полный день 09–15, физкультура и Makerspace по примерному расписанию.',extras='Дорога, жильё родителей, трансфер, страховка и возможная стоимость материалов отдельно не раскрыты. Завтрак и пансион не обещаны.',
                deposit='Архив договора 2026: полная оплата в течение двух недель после регистрации. До 25 мая полный возврат, после — 50%, менее 15 рабочих дней до начала возврата по личным причинам нет, кроме серьёзного заболевания или травмы со справкой больницы. При закрытии из-за тайфуна 50% дневного тарифа, за часть дня возврата нет. Минимум 10 в классе против таблицы PK: два преподавателя на девять детей — конфликт.'),
            'Дневной лагерь 09–15, приход с 08:45. В примерном плане 2026 родители приглашены на показ 17/24 июля в 14–15. Школьная категория и будущий договор должны быть подтверждены отдельно.',kg,kg,
            [src('Две темы и школьный admission gate',K),src('Полный draft2026 двухнедельного расписания',KP),src('Публичный собственный campcontract2026: цена, еда, отмена',KT)])
    hs_rows=[
      (12,'Activity','4–5','general,art,music','Игровое обучение, искусство, музыка, движение и английская лексика. Младший поток не выбирает отдельную робототехнику или программирование.',fit('not_eligible','Матвей старше максимума5.'),fit('not_eligible','В будущем сезоне2027Оскар6–7, старшеActivity4–5; нуженAroundtheWorld. Прошлый2026возраст на 1июля отдельно.')),
      (13,'Around the World','6–7','general,art,science,robotics','Культуры мира, рассказы, исследования, спорт и выезды. VEX-робототехника доступна только на неделях 3–5: три выбранных блока в неделю. Программирование для группы 6–7 отдельно не перечислено.',fit('not_eligible','Матвей старше6–7; нужнаDiscovery8–9 илиAdventure10–11.'),fit('conditional','Оскар6–7 в2027 подходит по возрасту, но новые даты/тариф и правилоageafter1July ещё нужны.')),
      (14,'Discovery','8–9','general,science,coding,robotics','Наука, кулинария, творчество и спорт. Опция VEX — недели 3–5, программирование CYBERone — недели 3–6: визуальный код, игры и Roblox. Ссылку на созданную игру присылают родителям. Одна выбранная опция занимает три блока в неделю.',fit('conditional','Матвей9–10 в2027:Discoveryтолько если ещё9 по campcutoff; после10Adventure. Новая2027таблица ещё не опубликована.'),fit('later','Оскар ниже8; в2027не подходит.')),
      (15,'Adventure','10–14, Junior10–11 / Senior12–14','general,science,coding,robotics','Командная работа, самостоятельность, научные опыты и островные выезды; группы 10–11 и 12–14 разделены. VEX доступен на неделях 3–5, CYBERone coding — 3–6, только в трёх выбранных блоках в неделю. Приборы домой не обещаны.',fit('conditional','Матвей должен достичь10 к применимомуcutoff. Нынешнее правило2026ageafter1July нельзя автоматически назначать2027.'),fit('later','Оскар младше10.')),
      (16,'English Focus','8–14, группы8–9/10–11/12–14','languages,general,coding,robotics','Для начального и среднего английского: четыре дня в неделю по три языковых урока плюс общая лагерная программа. Робототехника или код — три выбранных блока в неделю. Для детей с хорошим английским сравнивать с более интенсивным техническим курсом.',fit('conditional','Матвей входит в опубликованные 8–14 лет. Языковой уровень, даты 2027 и выбранную опцию сверить отдельно.'),fit('later','Оскар ниже8; отдельныйAroundtheWorld.'))]
    for i,title,age,themes,programme,mf,of in hs_rows:
        emit(i,'HeadStart Phuket · '+title,'THA','Chaofah City Campus ·39/99Moo4,VichitsongkramRd,Vichit,Phuket83000',themes,age,
            'В собственной информации лагеря прямо указано: все уроки, инструкции и активности на английском. Принимают любой уровень английского, предлагают языковую поддержку.',programme,
            'Архив 2026: шесть недель 29 июня – 7 августа. Робототехника на неделях 3–5, то есть 13–31 июля; код на неделях 3–6, 13 июля – 7 августа. Эти даты не перенесены на 2027.',
            dict(year=2026,label='Архив2026:Activity18 000THB/нед,остальные потоки20 000THB/нед. Новая цена 2027не подтверждена.',
                included='Обед, два перекуса, экскурсии, основные активности, учебные материалы, футболка и базовая accident insurance. Выбранная опция VEX или coding входит в тариф: три блока в неделю, отдельно от платных занятий после лагеря.',
                extras='Архив 2026: продлённый день на неделях 3–6 — THB 3000 за неделю или 750 за день. Автобус THB 2000 за ребёнка в неделю только при четырёх и более детях одного маршрута; двое братьев не обеспечивают маршрут. Accident insurance только в часы лагеря, лимит THB 40 000. Другая страховка, дорога и жильё отдельно.',
                deposit='Архив 2026: 80% возврата при отмене более чем за 14 дней; менее чем за 14 дней возврата нет. Ровно 14 дней не разъяснено. Болезнь и исключение не компенсируют. Скидка 10% за три и более недели в одной записи; школьная 25% семье не назначена. Место подтверждается после проверки оплаты; аккаунт не создавали.'),
            'Дневной лагерь, жильё семьи HeadStart не предоставляет и не организует. Площадка Chaofah City; другой кампус Cherngtalay не считается лагерной площадкой автоматически. Группа минимум шесть, максимум 24. При будущей записи нужны паспорта родителя и ребёнка, фото ребёнка; документы не передавали.',mf,of,
            [src('Own2026 programmes, language, food, bus, price and cancellation',H),src('Полный OptionsPDF: точные weeks, VEX иCYBERone',HP)],confirmed=['EN'],role='primary')
        if i==12:
            profiles[-1]['price']['label']='Архив 2026: THB 18 000 за неделю Activity 4–5. Цена 2027 ещё не подтверждена.'
            profiles[-1]['price']['included']='Обед, два перекуса, основные занятия и выезды, учебные материалы, футболка и базовая accident insurance. В этом младшем потоке нет выбора Robotics/Coding Option.'
        else:profiles[-1]['price']['label']='Архив 2026: THB 20 000 за неделю выбранного потока. Цена 2027 ещё не подтверждена.'
    for i,title,themes,programme in [(17,'Let’s Play, Create & Explore','general,languages,art,science,sport','Английский 09–12; спорт, искусство и простые STEM-проекты 13–15. В примерном плане 6–12: испытание защиты яйца при падении, полимеры, мосты на нагрузку, воздушные змеи и творчество. Общий исследовательский лагерь.'),(18,'Let’s Create with AI','languages,ai,coding,robotics,technology','Английский 09–12; AI, машинное обучение, код и робототехника 13–15. Проекты: башни, треки, мосты, логика, данные и стратегия; распознавание объектов и речи, безопасное поведение в цифровой среде. Конкретный робот, личное оборудование и язык технических ведущих отдельно не опубликованы.')]:
        emit(i,'Brighton College Bangkok Vibhavadi · '+title,'THA','Vibhavadi campus ·998/1VibhavadiRangsitRoad,LadYao,Chatuchak,Bangkok10900',themes,'3–12; уAотдельные3–5и6–12, уBплакаттоже3–12',
            'Утренние уроки английского подтверждены. Язык послеобеденных технических занятий отдельно не назван; полностью английская техническая программа не обещана.',programme,
            'Архив 29 июня – 17 июля 2026: три недели, понедельник–пятница 09–15. Набор 2027 не опубликован. Vibhavadi/Tesoltree/Cubic Creative имеет другую площадку и программу, чем Krungthep Kreetha In House Camp.',
            dict(year=2026,label='Архив 2026: Option A — THB 18 000 / 32 000 / 45 000 за одну / две / три недели; Option B — 21 000 / 40 000 / 55 000. Это разные программы и тарифы; не цены 2027.',
                included='Утренний английский и один выбранный послеобеденный поток. Брошюра подтверждает три часа английского и два часа активностей в день. Включение обеда 12–13 не разъяснено.',extras='Обед, перекусы, страховка, трансфер, покупка оборудования домой и включение VAT не разъяснены. Они не считаются бесплатными.',
                deposit='Оплата, возврат, минимум группы и приём приезжих внешних семей в выбранных страницах не раскрыты. Актуальный договор ещё нужен.'),
            'Дневной лагерь 09–15; пансион в карточке не заявлен. Родители организуют поездку и жильё отдельно; школьное поступление не следует из записи в camp.',
            fit('conditional','Матвей входит в 3–12. Новый сезон, места, приём внешних семей и английский технических занятий ещё подтвердить.'),fit('conditional','Оскар входит в 3–12. Собственный плакат Option B тоже указывает 3–12; содержание AI для самых младших отдельно не разъяснено.'),
            [src('A/B fees, dates and campus',B),src('Полная9-page2026 brochure',BP),src('A6–12 sampleSTEMschedule',BS),src('Полныйcraft/scienceactivitydescription',BD),src('Bплакатпрямоуказывает3–12',BI)],confirmed=['EN'],role='language_lessons')
    profiles[-len(NEW):]=readable(profiles[-len(NEW):])

def extend_report_v128(r):
    r['version']=128
    r['methodology'].append('v128: course-specificCoboScheduleсохраняет2часа/деньивыбраннуюплощадку,не всеобщиеweeks. OWISmandatorymaterials/registration/taxсчитаныявно;previouswinteractivitiesне обещаны2026. KASEnglish-schooladmissionне доказательствоязыкавсехcampзанятий;архив2026не стал2027.')
    r['shortlist'] += readable([
      dict(label='Гонконг · инженерия и AI по отдельным английским курсам',slugs=NEW[:9],reason='Cobo: пять точных курсов 20–23 октября, четыре занятия по два часа, HKD 3600. Junior 6–8 / Senior 9–11 с требованиями к опыту. У Arcade Junior конфликт 6–8 против 8+, у четырёх карточек нет собственного расписания. Внутренний Hackathon 12–14 — будущий путь к приложению и презентации.'),
      dict(label='Япония · общая английская зима для обоих',slugs=[NEW[9]],reason='OWIS Osaka: 14–18 декабря 2026, английский дневной лагерь 4–16 для внешних учеников. Двое новых участников JPY 198 000 с материалами, регистрацией и налогом. Пансиона и автобуса нет; включение питания, договор и открытие регистрации ещё нужны.'),
      dict(label='Тайвань и Таиланд · подробные летние кандидаты следующего набора',slugs=NEW[10:],reason='KAS: Future City / Global Plate с grade + English-school gate; HeadStart: полный EN и VEX/Coding options только три блока в неделю; Brighton: утро EN и два разных afternoon paths. Все эти публикации — архив 2026, новый набор 2027 ещё нужен.')])
    gaps=[('HKG','Cobo · возраст, ценаconsole, invoice',C+'holiday-camps/','Найдено5собственныхOct20–23Schedule,не20вымышленныхcourseweeks. ArcadeJunior6–8против8+;400inclusiveне ясноinsidefee. WeDo/Arcade/AI SeniorScheduleпуст;нетновыхdates. Полнаяоплата3weeksзаранее vsближайшийкурс14days:late-entryне гарантирован;4–8typicalнеpre-bookingproof.'),
      ('JPN','OWIS · winterregistration иcampcontract',O,'Winter2026date/price/EN/external4–16подтверждены. Bannernotyetopen/checkOctober,Schedulebuttonбезhref. PreviousprogrammeSnowPark/film/foodнеобещает2026. ActTsukubataxincludedне winterOsakaexcludes10;websitestermsSingaporeнеcampcontract. Нужны lunch/insurance/refund/актуальныйsyllabus.'),
      ('TWN','KAS · договор ианглийский technical instruction',KT,'КонтрактSession1July13–20противSchedule13–17;PKratio2:9противmin10class. AdmissionPK–G5English-basedschoolsне простоfluency. Языкcampвselectedsourcesне explicit. Closed2026неfuture2027closed;NTD16500/15500иrefundMarch19архив.'),
      ('THA','HeadStart · будущаясмена икласс',H,'OwnallcampEnglish,feeincludesVEX/Codingoption3/weekнеextension;2026толькогруппы/датапосле1July. Bus≥4same-routeнеguaranteeдлядвухsiblings. По2027нужнынедели,agecutoff,тариф,optionshours/kit. CherngtalayнефактическийChaofahcamp.'),
      ('THA','BrightonVibhavadi · age3–12не AIdepthгарантия',B,'Bплакат3–12подтверждёнвизуально;A6–12sampleSTEMещёнеBage6+. УтроEnglishнеexplicitafternoonAIEnglish. Кит/еда/tax/refund/externaladmissionнеполучены;archive3weeks2026не будущий2027. Другойcampusнеобъединён.'),
      ('KOR','YoungHoon/Gangbuk · локальнаяшкольнаякатегория','https://www.younghoon.org/2026-gangbuk-education-camp','Ownfive-dayJuly27–31,2026ZootopiaEnglishcooperationG1–6только Gangbukarea. Tourist/foreignchildrenправоне доказано;price/boardingнепрочитаны. Не добавленкакготовыймеждународныйпансион. BranksomeCanadaTorontocampне переноситсявBranksomeHallAsiaJeju.'),
      ('TWN','NTNU · Mandarinwinterне EnglishSTEM','https://ntnucamp.sce.ntnu.edu.tw/mandarincamp/intro.php','OwnJan4–15,2027Mandarinprogramme37000+1000registration. ENSTEMинструкциянедоказана;этакитайскаяязыковаяопцияне пополнилафильтрEnglishrobotics. Сначалаподтвердитьреальныйязыковойпотокисодержание.')]
    names={'HKG':'Гонконг','JPN':'Япония','TWN':'Тайвань','THA':'Таиланд','KOR':'Южная Корея'}
    for iso,title,url,detail in gaps:r['gaps'].append(readable(dict(iso=iso,country=names[iso],provider='v128 · '+title,url=url,detail=detail,next_action='Продолжитьпервичнуюпроверку следующего набора и всех приоритетных стран. Мировойаудит остаётся активен;0стран полностью изучены.')))

def extend_planning_v128(d):
    m=d['camp_planning'];m['offers']=[q for q in m['offers'] if q['id'] not in NEW_IDS]
    m['offers'] += [
      offer(NEW_IDS[0],NEW[9],'OWIS Osaka · оба впервые · 14–18 декабря 2026',70000,currency='JPY',price_year=2026,format='day',checked=CHECKED,sessions=[['2026-12-14','2026-12-18']],sources=[O],
        required=[dict(id='materials',label='Materials5000×2',amount=10000),dict(id='registration',label='Первыйseasonalcampregistration15000×2',amount=30000),dict(id='tax',label='10%consumptiontaxна 180000первыйсезоноба',amount=18000)],
        unknown_required=[dict(id='lunch',label='Lunch2026 ·включение/итоговыйсчётподтвердить',unit='amount',rate=1,min=0)],
        gate='Возраст 4–16, внешние ученики. Смета для двух детей, которые не учатся в OWIS и впервые идут в сезонный лагерь. Даты опубликованы; регистрация на странице пока не открыта. Место отдельно подтвердить.',
        included='Недельный лагерь. Материалы, первая регистрация и налог учтены отдельно. Школьного автобуса и пансиона нет.',deposit_note='ОтдельныйOsakaWinterrefundcontractне опубликован;TsukubaActиSingaporewebsiteTermsnotspecificcampterms.',scope='JPY 198 000 за двоих новых внешних участников. Питание, страховка, дорога и жильё родителей ещё не оценены. Для бывшего участника лагеря нужен другой расчёт регистрации и налога.'),
      offer(NEW_IDS[1],NEW[3],'Cobo VEX IQ · только Матвей · 20–23 октября 2026',3600,currency='HKD',price_year=2026,children=['matvey'],base_by_child={'matvey':3600},format='day',checked=CHECKED,sessions=[['2026-10-20','2026-10-23']],sources=[C+'camp_detail/index.asp?CourseID=186',CT],
        gate='ТолькоеслиМатвеюуже9на 20Oct. 14–16WanChai,4×2h=8hours,неполныйdaycare. PC/Mac/Chromebook/iPadсcharger+VEXCodeIQсвой;hardwareдаётоператор. Late-entry/publicminimum3weekspayотдельноподтвердить.',
        included='Четыредвухчасовыхурока,учебныйVEXIQhardware. Kitдомойне обещан.',deposit_note=COBO_TERMS,scope='HKD 3600 за одного участника и восемь часов занятий. Оскар в Senior не допускается. Это не оплата двоих детей и не полный недельный уход.'),
      offer(NEW_IDS[2],NEW[1],'Cobo SPIKE Prime · только Оскар · 20–23 октября 2026',3600,currency='HKD',price_year=2026,children=['oscar'],base_by_child={'oscar':3600},format='day',checked=CHECKED,sessions=[['2026-10-20','2026-10-23']],sources=[C+'camp_detail/index.asp?CourseID=210',CT],
        gate='ТолькоеслиОскару исполнилось6к20OctиестьWeDo2.0+Scratch. 10–12WanChai,4×2h=8hours. СвойLaptop+charger;переходнаJuniorне подтверждён одним годом рождения/трёхлетним опытом.',
        included='Четыредвухчасовыхурока. Неутверждёнkitpurchase/takehome.',deposit_note=COBO_TERMS,scope='HKD 3600 только за Оскара, при подтверждённых возрасте и опыте. Матвей в Senior занимается 14–16; разные часы не обеспечивают общий полный день.')]
    m['offers'][-len(NEW_IDS):]=readable(m['offers'][-len(NEW_IDS):]);m.update(version=128,asof=CHECKED)
