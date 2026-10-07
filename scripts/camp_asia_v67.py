"""Asia programme evidence: current intake, real attendance and language roles."""
def add_deep_asia(add, src, fit, profiles):
    def put(*a, **k):
        add(*a, **k)
        p=profiles[-1];p['checked']='2026-10-05'
        for s in p['sources']:s['checked']=p['checked']
        return p
    def fee(year,label,included,extras,deposit,season=None):
        x=dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
        if season:x['season']=season
        return x
    def dates(p, rows):
        p['timing']['session_details']=rows
        p['timing']['sessions']=[[r['start'],r['end']] for r in rows]

    koa='https://www.wintercamp.jp/ski'
    files=['d3e2ad_04cd7ef58524422da2d07206e95b04f3.pdf','d3e2ad_5ce0179e110a4b75bd77bf4fb616368b.pdf','d3e2ad_691dc544e4c74dc09b3e4cb2150140f5.pdf']
    cancel='FAQ оператора: без штрафа до 17:00 за 21 день; затем до 17:00 за 8 дней — 20%; до 17:00 за 2 дня — 30%; до 17:00 накануне — 40%; позже — 100%. Это опубликованные условия оператора; окончательный договор и часовой пояс подтвердить. PDF: набор минимум 15, дедлайн за 2 недели; максимум 70 не означает наличие мест.'
    for i,(slug,title,amount,level,content,role) in enumerate([
        ('koa-classic','Classic Winter',98000,'Все уровни, включая новичков',
         'Общий зимний пансион с английской лагерной средой, снежными играми, творческим проектом и лыжами/сноубордом. PDF даёт уроки утром и днём на 2-й и 3-й день; первый/последний день — другие активности. Веб-фраза one session per day расходится с четырьмя уроками в PDF; не считать четыре полных дня ski.', 'camp_life'),
        ('koa-aire','SKI PLUS · AIRE',117000,'Минимум Alpine / Lower Intermediate по собственной шкале KOA',
         'Больше катания с AIRE Ski School: опубликованы занятия в каждый из четырёх дней, но первый/последний укорочены дорогой. В PDF видны шесть блоков, поэтому обещание twice a day не означает восемь полных уроков. Нужны уверенные связные повороты на простом склоне по шкале KOA.', 'camp_life'),
        ('koa-english-ski','SKI PLUS · KOA English',125000,'Минимум Black Diamond / Intermediate по собственной шкале KOA',
         'Английское ski-преподавание прямо указано для этого отдельного пакета. Уроки во все четыре дня, в PDF шесть блоков с укороченным первым/последним днём. Black Diamond здесь название ступени KOA с контролируемыми поворотами; это не требование кататься по любой чёрной трассе.', 'primary')]):
        pdf='https://www.wintercamp.jp/_files/ugd/'+files[i]
        p=put(slug,'KOA Japan · '+title,'Япония','JPN','Kitashiga / Ryuoo Ski Park · Hotel Alpine, 11700-26 Yomase, Yamanouchi, Nagano',
            'general,languages,sport','boarding','FAQ 6–15; PDF Grades 1–9; '+level,
            'Лагерная среда EN, японская поддержка. FAQ прямо говорит, что ski/snowboard lessons на JP; '+('отдельный KOA English Ski явно устанавливает исключение и EN на склоне.' if i==2 else 'английскую жизнь лагеря не переносить на лыжные уроки AIRE/Classic.'),
            content+' Международные игры, японская культура и снежные проекты; робототехника/ИИ не заявлены.',
            '26–29 декабря 2026 и 3–6 января 2027: 4 дня / 3 ночи. Отправление Shibuya 07:20, возвращение 18:00. Возраст FAQ 6–15 не отменяет школьный минимум Grade 1 в PDF.',
            fee(2026,f'JPY {amount:,} с налогом / 4 дня 3 ночи. KOA Member {amount-5000:,}; членство семьи не установлено.',
                'Автобус Shibuya ↔ курорт, 3 ночи, 4 обеда / 3 ужина / 3 завтрака, lift ticket, уроки, местные активности, страхование по PDF. Покрытие страхования уточнить.',
                'Прокат gear JPY 5 500 и одежды 5 500 за 4 дня каждый; night ski 5 500 за один вечер. Перчатки, шапка, очки не выдаются в прокате. Шлем и его стоимость не установлены. Билеты до Японии, жильё семьи и дорога к Shibuya отдельно.',cancel,season='2026/27'),
            'Hotel Alpine: 4–6 детей в комнате, разделение по полу; санузел/ванная в комнате по PDF, также общая купальня на странице. Пансион 3 ночи; родительское размещение не включено.',
            fit('conditional','Матвею возраст подходит; Grade 1–9 и '+level.lower()+' надо подтвердить. Лыжный опыт семьи неизвестен.'),
            fit('conditional','Оскару нужен уже исполненный 6-й день рождения на дату смены и Grade 1; FAQ 6+ сам по себе не подтверждает дошкольный допуск. '+('Новичку подходит Classic, внешний допуск отдельно.' if i==0 else 'Также обязателен '+level+'; не считать опыт робототехники лыжным уровнем.')),
            'Конкретный зимний вариант общего английского отдыха с разными лыжными требованиями; не технический лагерь и не турнир.',
            ['Подтвердить возраст/класс, лыжную ступень, язык инструктора выбранного пакета, места, шлем, договор/страхование и итоговый счёт.'],
            [src('Пакеты, даты, языковой FAQ и отмена',koa),src('PDF своего пакета: тариф, часы, включения, комнаты и классы',pdf)],
            status='published_2026_27',priority=['general','boarding'],confirmed=['EN'])
        p['language_evidence_role']=role
        dates(p,[dict(start=s,end=e,label=title+' · 4 дня / 3 ночи',price=f'JPY {amount:,} с налогом',place=p['place'],source=pdf,formats=['boarding'],date_scope='camp_session') for s,e in [('2026-12-26','2026-12-29'),('2027-01-03','2027-01-06')]])

    ayla='https://www.aylais.com/camp-ayla'
    p=put('ayla-tokyo','Camp Ayla · общие дневные каникулы','Япония','JPN','Tokyo · 5-13-28-102 Shirokanedai, Minato-ku',
        'general,art,sport,languages','day','3–9 по каждому сезонному body; SEO-заголовок 3–6 устарел относительно основного текста',
        'Camp назван bilingual, а школьная homepage устанавливает EN/JP. Это поддерживает гипотезу пары EN/JP, но язык лагерной смены и доля EN отдельно прямо не установлены; пока вне фильтра подтверждённого EN. Англоязычная страница сама по себе не доказывает EN преподавание.',
        'Тематические игры, искусство, культурные активности, спорт и поделки: Space, Pirate, Ninja, Bakery и другие темы. Это общий отдых, не подтверждённый robotics/STEM интенсив. Часы Regular 09–13, Extended 09–15, Super Extended 09–17, Super Duper Extended 09–18.',
        '23 названные недели осени/зимы 2026, весны, Golden Week, лета, осени/зимы 2027. 11 летних недель 7 июня – 20 августа, но 20–23 июля начинается во вторник, 11 августа no school. Неделя 9–13 августа разделена на два отрезка без среды: 24 календарных строки. У Winter 2027 heading опечатка 20267; год взят из двух явных Winter 2027 Calendar и соответствующих им дат/дней недели.',
        fee(2027,'JPY 8 000 / 10 000 / 12 000 / 13 000 за день по четырём часам +10% tax: 8 800 / 11 000 / 13 200 / 14 300. Extended 5 дней = 55 000, 4 = 44 000, 3 = 33 000; это расчёт, не отдельный пакет.',
            'Выбранный учебно-игровой день; включение питания/материалов не доказано.',
            'Месяц 4 последовательные недели: Extended 200 000 / Super 220 000 до налога. Только дольше 4 недель: registration 30 000 + processing 20 000, применение налога к этим сборам подтвердить. Дополнительные 30 минут 990, итоговый налог уточнить. Трансфера нет; жильё семьи отдельно.',
            'Все уплаченные сборы оператор объявляет non-refundable / non-transferable. Перед оплатой проверить итоговый договор и дни посещения.',season='2026/27'),
        'Дневная школа; собственного лагерного пансиона и транспорта не заявлено. Семья организует жильё и сопровождение.',
        fit('conditional','Матвею только пока не исполнилось 10; конкретная дата рождения определяет доступность каждой недели 2027. В октябре 2026 возраст подходит.'),
        fit('candidate','Оскару 5–6 в 2026 и 6–7 в 2027: соответствует 3–9, зачисление и язык отдельно.'),
        'Календарь общего отдыха вокруг семейного пребывания в Токио; для техники сочетать с отдельным Tokyo Coding / Elev8, а не считать тематические поделки робототехникой.',
        ['Подтвердить язык смены, интересность Матвею с прежним опытом, дату 10-летия, иностранное зачисление, питание, материалы, выходные/праздники и полный счёт.'],
        [src('Каждая неделя 2026/27, no school, часы, налог и возвраты',ayla),src('Школьная пара EN/JP; не прямое доказательство camp instruction','https://www.aylais.com/')],
        status='published_2026_27',priority=['both','general'])
    weeks=[('2026-10-13','2026-10-16','Karate',4),('2026-10-19','2026-10-23','Zombie',5),('2026-12-07','2026-12-11','Jurassic',5),('2026-12-14','2026-12-18','Winter Traditions',5),('2027-03-15','2027-03-19','Bakery',5),('2027-03-23','2027-03-26','Farmer',4),('2027-03-29','2027-04-02','Space',5),('2027-04-26','2027-04-28','Golden Week',3),('2027-06-07','2027-06-11','Picnic',5),('2027-06-14','2027-06-18','Safari',5),('2027-06-21','2027-06-25','Outback',5),('2027-06-28','2027-07-02','Pirate',5),('2027-07-05','2027-07-09','Superhero',5),('2027-07-12','2027-07-16','Jungle',5),('2027-07-20','2027-07-23','Grocery',4),('2027-07-26','2027-07-30','Glamour',5),('2027-08-02','2027-08-06','Ninja',5),('2027-08-09','2027-08-10','Matsuri · первая часть',2),('2027-08-12','2027-08-13','Matsuri · вторая часть',2),('2027-08-16','2027-08-20','Magic',5),('2027-10-12','2027-10-15','Autumn · неделя 1',4),('2027-10-18','2027-10-22','Autumn · неделя 2',5),('2027-12-06','2027-12-10','Winter · неделя 1',5),('2027-12-13','2027-12-17','Winter · неделя 2',5)]
    rows=[]
    for s,e,label,n in weeks:
        v=dict(start=s,end=e,label=label+f' · {n} дневных посещений',price=f'Extended 09–15: JPY {n*11000:,} с 10% tax, расчёт из тарифа за день',place=p['place'],source=ayla,formats=['day'],date_scope='day_camp_window',proof='Опубликованная тематическая неделя и фактические дни без no school; не обещание свободного места.')
        if s in ['2027-08-09','2027-08-12']:
            v.update(date_precision='published_rule',date_status='Опубликованное правило · даты рассчитаны',date_rule='В неделе Matsuri 9–13 августа 2027 среда 11 августа прямо no school. Понедельник–вторник и четверг–пятница разделены на два двухдневных отрезка; закрытая среда не входит в посещение.')
        if s.startswith('2027-12'):
            v['proof']='Winter 2027 Calendar явно даёт эти недели и дни Mon–Fri; heading 20267 — отмеченное расхождение, не перенесённый 2026 сезон.'
        rows.append(v)
    dates(p,rows)

    sh='https://www.shhkca.com.sg/yearendcamp2026'
    p=put('shhk-spike-claw','SHHK Cultural Academy / The Lab · SPIKE Claw Machine','Сингапур','SGP','Sennett / Toa Payoh · две разные площадки',
        'robotics,coding','day','7–12, Primary 1–6; обе границы подтвердить',
        'EN/ES/RU преподавания не установлен. Английская страница и партнёр The Lab не доказывают язык этой группы; название Hokkien также само по себе не доказывает язык занятия.',
        'Двухдневная сборка автоматического claw machine на LEGO SPIKE Prime: моторы, датчики, циклы, условия, тестирование, исправления и собственная демонстрация. Часы 09–17; внутренний финальный challenge не международное соревнование.',
        'Sennett 30 ноября – 1 декабря 2026; Toa Payoh 2–3 декабря 2026. Календарь 2027 не опубликован.',
        fee(2026,'SGD 420 с GST за 2 дня. Early bird минус 20 до 20 ноября = 400 при выполнении условий; наличие мест не установлено.',
            'Оператор пишет материалы включены; право забрать SPIKE-набор/модель не установлено.',
            'Обед и питание, late pickup, оборудование домой, жильё семьи и дорога отдельно уточняются.',
            'Цена/дедлайн скидки есть, camp refund/deposit не найден. Два PDF в footer — privacy и whistleblowing, не лагерная отмена.'),
        'Дневные 09–17, 5 Sennett Road 466781 или 397 Lorong 2 Toa Payoh 319639. Ночёвок нет.',
        fit('conditional','Матвей 8–9 в конце 2026 соответствует 7–12; Primary 1–6 и нужный уровень подтвердить.'),
        fit('later','Оскар в 2026 только 5–6, ниже 7. Возможный возраст 7 в 2027 не создаёт допуск к этой смене 2026.'),
        'Конкретный ближайший проект Матвею вместо общего обещания robotics camp; язык и детали питания требуют подтверждения.',
        ['Подтвердить язык, класс, места, уровень после трёх лет опыта, обед/полный день, использование/возврат набора и правила отмены.'],
        [src('Две площадки, SPIKE, возраст, часы и тариф с GST',sh)],status='published_2026',priority=['technical'])
    dates(p,[dict(start=s,end=e,label=title+' · 09–17 / 2 дня',price='SGD 420 с GST; условный early bird 400 до 20.11',place=place,source=sh,formats=['day'],date_scope='day_camp_window') for s,e,title,place in [('2026-11-30','2026-12-01','Sennett','5 Sennett Road, Singapore 466781'),('2026-12-02','2026-12-03','Toa Payoh','397 Lorong 2 Toa Payoh, Singapore 319639')]])

    uw='https://sites.google.com/gapps.uwcsea.edu.sg/holiday-activities-programme/'
    uc=uw+'activity-description/coding';us=uw+'activity-schedule';uf=uw+'faq';ur=uw+'registration'
    sheet='https://drive.google.com/open?id=1HwsOLLLpjHxWVa5geH_X-z6moZmzN2BAw1tRRdBUFGU'
    tracks=[
        ('codequest','CodeQuest Robotics & Adventure','K1–G1','robotics,coding','Dash, Bee-Bot, ScratchJr и алгоритмы; вводный младший уровень.',[],None,None),
        ('robospace','Mission Robospace','K1–G1','robotics,coding,science','Космос, простые алгоритмы, программируемые rover, задачи и игры.',[],None,None),
        ('sciencecraft','Science Craft','K1–G1','science','Screen-free модели и опыты с силами, светом, воздухом и гравитацией.',[['2026-10-12','2026-10-16']],395,'09–12'),
        ('buildverse','AI Buildverse','G2–G5','ai,coding','Введение в generative AI, детские проекты с изображениями/музыкой, приватность и ответственное использование. Это не продвинутый ML исследовательский интенсив.',[],None,None),
        ('scratch-ai','AI with Scratch','G2–G5','ai,coding','Rule-based AI и ML, распознавание изображений/речи/текста и проект с моделями в Scratch.',[],None,None),
        ('python-ml','Create AI with Python','G5–G8','ai,coding','Практические ML/rule-based модели, приложения на Python, распознавание. Предыдущих навыков сайт не требует, но школьный класс обязателен.',[['2026-10-19','2026-10-23']],395,'09–12'),
        ('minecraft','Minecraft ThinkLab','G3–G7','coding','Minecraft Education, цифровые 3D-миры, планирование ресурсов и программируемый Agent; логика и блочное кодирование.',[['2026-10-12','2026-10-16'],['2026-10-19','2026-10-23']],395,'13–16'),
        ('python','Python Bootcamp','G5–G8','coding','Переменные, строки, структуры данных, условия, циклы и функции; проекты и game development для начинающих/уточнения навыков.',[],None,None),
        ('speedtech','SpeedTech Race Car','G2–G5','robotics,coding,science','Аэродинамика, механика, электроника и программирование гоночной машины. Только этот course write-up прямо обещает забрать собственную машину домой.',[],None,None)
    ]
    for slug,title,grade,themes,programme,sessions,amount,hours in tracks:
        infant=grade=='K1–G1';future=grade=='G5–G8';active=bool(sessions)
        p=put('uwc-dover-'+slug,'UWCSEA Dover / Create Lab · '+title,'Сингапур','SGP','Singapore · UWCSEA Dover, точку входа подтверждает организатор; текущие выбранные курсы MATH 206',
            themes,'day',grade+'; год рождения не заменяет текущий школьный класс',
            'Технический EN/ES/RU непосредственно не указан в прочитанных camp description/FAQ/schedule. Международная EN школа и английская страница — контекст, не подтверждение языка конкретной группы.',
            programme+' Create Lab выдаёт digital certificate участия, не международную награду.',
            ('Текущая открытая таблица набора подтверждает '+('12–16 октября 2026, 09–12.' if slug=='sciencecraft' else '19–23 октября 2026, 09–12.' if slug=='python-ml' else '12–16 и 19–23 октября 2026, 13–16.')+' Даты 2027 не объявлены.' if active else 'Course write-up содержит октябрьские недели 2026, но в текущей таблице Programme Offerings этого курса нет. Это описание, а не подтверждённое предложение мест; точная календарная строка не создаётся. Следующий набор 2027 неизвестен.'),
            fee(2026 if active else None,'Таблица: $395 за 5 полудней для своих +10% non-UWCSEA = $434.50 внешнему, рассчитано. Валюта/окончательный налоговый счёт отдельно подтвердить.' if active else 'Тариф этого отсутствующего в актуальной таблице курса не установлен; $395 других Create Lab курсов не переносится.',
                'Выбранная программа '+(hours+', 5 × 3 часа = 15 часов по расписанию.' if hours else 'при появлении реального набора.')+' Комплект/расходники отдельно согласовать.',
                'Full day состоит из двух оплачиваемых программ. Для K1–G8 lunch/supervision 12–13 обязателен, таблица $65 за неделю +10% external = $71.50; столовая закрыта, Sodexo указан в таблице. Снэк/вода свои, автобус/жильё семьи не включены. Для одного полудня присмотр на остаток дня не предоставляется.',
                'FAQ: нет sibling/group/earlybird скидок и prorating; travel/change of mind не возвращают. Болезнь/травма — уведомление вовремя и medical certificate. Внешним CAP parent account и подтверждённая allocation; если не оплатить в срок, место снимают. September dates в timeline относятся к октябрю; footer 8 June и ссылка current grade 2025/26 выглядят остатками другого сезона, не дедлайн семьи.'),
            'Только дневной школьный кампус. Внешним выдаётся activity pass, но вход родителя в место занятий запрещён. После полудня нужно покинуть кампус, если не оплачены второе занятие и lunch/supervision.',
            fit('unknown' if infant else 'later' if future else 'conditional',
                'Для Матвея нужен '+grade+'. '+('Младшая ступень K1–G1, класс Матвея неизвестен; не рекомендовать автоматически по 8–9 годам.' if infant else 'Оба ребёнка пока младше обычной Grade 5; сохранено как будущая ступень, ускоренный допуск не обещан.' if future else 'Точный текущий класс неизвестен; зачисление по школьной ступени и наличию мест, не по одному году рождения.')),
            fit('conditional' if infant else 'later',
                'Оскару '+('только при соответствии K1–G1; класс неизвестен, внешний набор допускается условно.' if infant else 'нужно достигнуть '+grade+'; возраст 5–6 в октябре 2026 сам по себе не подтверждает эту ступень.')),
            ('Ближайший опубликованный школьный '+('научный' if slug=='sciencecraft' else 'технический')+' полудень; открытый внешний набор подтверждён, язык и фактическое место отдельно.' if active else 'Полезная ступень учебного каталога, но отсутствует в текущем расписании предложения; в shortlist не выдаётся за свободную смену.'),
            ['Внешним доступны оставшиеся места после Dover, first-come по времени interest form; своим приоритет. Подтвердить класс/язык, появление именно курса в таблице, allocation обоим в одинаковые часы и полный счёт. Ссылка формы не означает зачисление; ничего не отправлялось.'],
            [src('Содержание и классы конкретных courses',uc),src('Текущие предлагаемые courses, часы и external surcharge',us),src('Открытая таблица школы',sheet),src('Внешний допуск, lunch, возвраты и скидки',uf),src('Октябрьский процесс allocation и несогласованный footer',ur)],
            status='published_2026' if active else 'next_unannounced',priority=['technical'] if active else [])
        p['intake_evidence']='offered_in_current_schedule' if active else 'description_only_absent_from_current_schedule'
        dates(p,[dict(start=s,end=e,label=title+' · '+hours+' / 5 полудней',price='$434.50 external по расчёту 395 +10%; окончательную валюту/налоги подтвердить',place=p['place'],source=us,formats=['day'],date_scope='day_camp_window') for s,e in sessions])

    ish='https://www.iis.kh.edu.tw/teaching/international-summer-camp'
    news='https://www.iis.kh.edu.tw/news/2026-Summer-Taiwan-en'
    p=put('ishou-international','I-Shou International School · Languages / STEM / Culture','Тайвань','TWN','Kaohsiung · 6 Xuecheng Road, Section 1, Dashu District',
        'general,languages,robotics,coding,science,sport','boarding','10–16 в announcement 2026; минимум/максимум нового 2027 ещё проверить',
        'Camp detail прямо пишет full English interaction с bilingual teachers и USA assistants. Это EN лагерная коммуникация; язык именно VEX / robotics / game design не установлен.',
        'В 2026 отдельно перечислены VEX Robotics Design & Challenges, Robotics Automation, Coding & Interactive Game Design, китайский/английский, культура и поездки. Elite fencing/golf/equestrian. В разделе Coming Soon 2027 — будущая смешанная programme concept, не гарантированная VEX смена или турнирная школа.',
        'Официально Coming Soon in 2027, но дат/смен/тарифа 2027 нет. История 2023–26 показывает maker/robotics развитие; старые активности не автоматически план каждого дня 2027.',
        fee(None,'Тариф 2027 и стоимость технических/Elite модулей не опубликованы.',
            'Состав будущего пакета ещё неизвестен.',
            'Роботы/владение набором, Elite, поездки, питание, трансферы, insurance и родительское проживание отдельно получить в quote.',
            'Нет опубликованного в прочитанных страницах договора оплаты/отмены и 2027 availability.'),
        'В 2026 прямо заявлена ночёвка в aquarium и забота 24/7; в campus tour виден Boarding House. Это доказывает ночной элемент, но не полный гостиничный/школьный пансион каждой ночи: длительность, комнаты и цена 2027 ещё не установлены.',
        fit('conditional','Только после 10-летия и сохранения 10–16 в 2027. В 2026 8–9 ниже минимума, текущий старый набор не подходит.'),
        fit('later','До 10 лет ниже опубликованной категории; не переносить возраст Primary школы на summer camp.'),
        'Перспективная тайваньская школьная инженерная среда Матвею после 10 лет; это ожидаемый 2027 набор без даты, не готовая бронируемая летняя смена.',
        ['Получить опубликованный 2027 календарь, возраст, технический EN, объём проектов/часов, foreign intake и полный boarding/Elite invoice до выбора поездки.'],
        [src('История robotics и coming soon 2027, EN interaction',ish),src('Международный состав, 10–16, ночёвка и 24/7 — сезон 2026',news)],status='partial_2027',priority=['technical'],confirmed=['EN'])
    p['language_evidence_role']='camp_life'

    ci='https://cistw.com/english-camp-in-taiwan/'
    for slug,title,grade,place,formats,housing,extra in [
        ('citop-day','CiTOP / CiStudy · English Day Network','Entering Grades 2–7','Hsinchu NEHS / Zhubei Walden / Tainan Xinjin / Yilan NIU','day',
         'Дневные 08–16:30, семья размещается отдельно. 20–25 детей, Walden 15–25; 1 native EN teacher + 1 class manager. Точный campus/programme выбирать отдельно.',
         'Питание не включено явно; daily transport/жильё семьи отдельно. Цена price-explainer является общей статьёй рынка, а не тарифом выбранного кампуса.'),
        ('citop-uch','CiTOP / CiStudy · UCH Residential','Entering Grades 3–9','Zhongli / Taoyuan · Chien Hsin University of Science and Technology','boarding',
         'UCH student dormitories, 3–4 ребёнка в комнате; дневной режим 08–21:30, 10–16 в классе. 1 native EN teacher + 1 manager; weekend ведут director/managers, не гарантированный native teacher каждую минуту.',
         'Meal supplement TWD 1 500 сверх ещё неизвестного camp fee; личная дорога до/после лагеря отдельно. Shuttle Taoyuan HSR ↔ UCH прямо бесплатный.'),
        ('citop-eda','CiTOP / CiStudy · E-Da Residential','Entering Grades 3–9','Kaohsiung · E-Da World / E-Da Skylark Hotel','boarding',
         'E-Da Skylark Hotel, 2–4 ребёнка в комнате; 08–21:30, 10–16 в классе, 1 native EN teacher + 1 manager. Указаны уже зарегистрированные японские школьники 2026, не доказанные участники 2027.',
         'Meal supplement TWD 1 000 сверх ещё неизвестного camp fee. E-Da shuttle рекомендован, бесплатность не доказана. Личная дорога до/после отдельно.')]:
        board=formats=='boarding'
        p=put(slug,title,'Тайвань','TWN',place,'general,languages,art,science','boarding' if board else 'day',grade,
            'Оператор прямо описывает 100% English environment и native-speaking teachers, full-English thematic camp. Это общий коммуникативный PBL лагерь; специализированная робототехника не доказана.',
            'Миссии, командные проекты, общение, презентации и культурный опыт. Day network содержит разные кампусы и темы: Walden — art/design, Xinjin — board game design, NEHS/NIU — общая английская программа. Робототехнический набор/лига не заявлены. Статистика оператора 80 000/100 000 выпускников имеет разные периоды и не заменяет независимую оценку качества.',
            'Прочитанная страница описывает Summer 2026; новые даты/цены 2027 ещё не опубликованы. Общие 3–5 дней не устанавливают точную длительность UCH с weekend. Private group 15+ может заказать свои даты — это не готовая открытая индивидуальная смена.',
            fee(None,'Основная цена выбранной программы не установлена; 2027 прайса нет.',
                'Материалы/страхование по странице. '+('Жильё, внутренние поездки/входные билеты; '+('28 meals по описанию UCH с отдельным supplement.' if slug=='citop-uch' else 'завтраки buffet, 5 обедов, 4 ужина и snacks с отдельным supplement.') if board else 'Включение обеда не установлено.'),
                extra,'Оплата, refundable deposit и условия отмены конкретной программы неизвестны; не подставлять общую рыночную статью вместо quote.'),
            housing,fit('conditional','Матвею нужен '+grade+' именно при входе в выбранную смену; текущий класс неизвестен. Сохранение правила и нового набора 2027 отдельно.'),
            fit('later','Оскару нужно уже '+grade+'. Возраст 6–7 в 2027 не доказывает Grade '+('3' if board else '2')+'; не применять sibling exception без отдельного решения оператора.'),
            'Общий английский '+('пансион' if board else 'дневной вариант')+' с прямым приглашением иностранных семей; возрастная ступень/цена не превращаются в подтверждённый допуск обоих.',
            ['Подтвердить новый набор, входной класс, конкретный curriculum, дату/длительность, комнаты/питание, договор и весь invoice. Не считать 15+ private group доступной двум детям индивидуально.'],
            [src('English immersion, foreign families, отдельные grades/форматы/доплаты',ci),src('Общая статья о цене рынка — не прайс лагеря','https://cistw.com/campcost/')],priority=['general','boarding'] if board else ['general'],confirmed=['EN'])

    cj='https://cistw.com/jeju-camp/'
    p=put('cistudy-jeju-seoul','CiStudy booking · Jeju / Seoul English & Culture','Южная Корея','KOR','Jeju + Seoul · точные принимающие школы и места проживания не установлены',
        'general,languages,art,sport','boarding','10–18 в Summer 2026; границы нового сезона неизвестны',
        'EN speaking занятия ведут native teachers; язык каждой экскурсии/K-pop/всей среды не установлен. Это отдельные уроки EN и культурная программа, не доказанный technical EN лагерь.',
        'Практическая английская речь, корейская культура, K-pop, природа, местные мастерские/походы и продление поездки до Сеула. Robotics/AI не заявлены. CiStudy — тайваньский booking channel; принимающий оператор/школа ещё не подтверждены.',
        'Архив 2026: 5–15 июля и 19–31 июля. Следующий 2027 не объявлен; прошедшие даты не создают будущие строки календаря.',
        fee(2026,'Архив: Plan A USD 2 200, Plan B 2 600. Оба без международных билетов; B включает внутренний корейский перелёт. Какой план/длительность каждому старту — отдельно подтвердить.',
            'Объявлены питание, местный airport/school transfer и shared dorm/hotel проживание; контракт и точный состав A/B не опубликованы в текстовом summary.',
            'Международный перелёт, родительская поездка, личные расходы, domestic flight для A и возможные сборы отдельно.',
            'Агент описывает group сопровождение и страхование; это не подтверждение персонального покрытия иностранного ребёнка и не договор отмены.'),
        'Activity-centre dorms и hotels в общих многоместных комнатах; точные названия/количество ночей неизвестны.',
        fit('conditional','2026 Матвей младше 10; только после 10-летия и при появлении нового 2027 набора с теми же условиями.'),
        fit('later','До 10 лет не подходит.'),
        'Будущий общий языковой маршрут; не установленный camp Branksome/Chadwick и не робототехнический пансион сейчас.',
        ['Установить принимающего оператора и школы, новый сезон, приём семьи вне тайваньской group tour, языки, длительность A/B, комнату, договор и полный счёт.'],
        [src('Официальная страница booking channel: даты/возраст/планы Summer 2026',cj)],confirmed=['EN'])
    p.update(language_evidence_role='language_lessons',booking_channel='CiStudy',operator_identity_status='unconfirmed')
