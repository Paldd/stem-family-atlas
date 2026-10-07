"""Primary programme-level Asia pass, preserving archive and admission boundaries."""
CHECKED = '2026-10-05'
SEE = 'https://seecamp.com.tw/product/2027see-winter-future-dreamers-5d/'
ENGINEERING = 'https://seecamp.com.tw/product/2027see-winter-esl-engineering-5d/'
SEE_POLICY = 'https://seecamp.com.tw/precautions/'
NULL = 'https://sg.nullspace.co/centre-for-robotics-learning/'
EV3 = NULL + 'lego-robotics-camp/'
AI = NULL + 'generative-ai/'
STEM = NULL + 'stem-explorer-class-7-8/'
MINECRAFT = NULL + 'minecraft-holiday-camp/'
PRINT = NULL + 'buildup-series-3d-print-design-holiday-camp/'
TEAM = NULL + 'robotics-competition-training-programme/'
POLICY = NULL + 'centre-policy/'
CONTACT = 'https://sg.nullspace.co/contact-us/'
OYIS = 'https://external.oyis.org/intensives/'
SUMMER = 'https://www.english-adventure.org/en/summer/'
IMMERSION = 'https://www.english-adventure.org/en/immersion/'
SFS = 'https://www.seoulforeign.org/camp-sfs/elementary-school-programs'
SFS_POLICY = 'https://www.seoulforeign.org/camp-sfs/on-campus-policy'
SFS_GRADE = 'https://www.seoulforeign.org/camp-sfs/grade-conversion'
SFS_ENTRY = 'https://www.seoulforeign.org/camp-sfs/eligibility'
CENTRES = {
    'rochester': 'Rochester Mall · 35 Rochester Drive #03-07, Singapore 138639',
    'kallang': 'Kallang Wave Mall · 1 Stadium Place #01-72, Singapore 397628',
    'tampines': 'SAFRA Tampines · 1A Tampines Street 92 #02-03, Singapore 528882',
}


def add_asia_v79(add, src, fit, profiles):
    def put(*args, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1]
        p['checked'] = CHECKED
        p['themes'] = [s.strip() for s in p['themes']]
        for s in p['sources']:
            s['checked'] = CHECKED
        return p

    def fee(year, label, included, extras, deposit):
        return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)

    def variants(p, rows, url, scope='day_camp_window'):
        p['timing'].update(variant_keyed=True, sessions=[[v['start'], v['end']] for v in rows], session_details=rows)
        for v in rows:
            v['variant_key'] = v.pop('key')
            v.update(source=url, formats=['day'], date_scope=scope)

    # Venue addresses and selectable variants are from the operator's own product.
    locations = [
        ('taipei', 'National Taipei University of Business · 321 Jinan Road Section 1, Zhongzheng, Taipei 100025'),
        ('xinzhuang', 'Fu Jen Catholic University · 510 Zhongzheng Road, Xinzhuang, New Taipei'),
        ('tainan', 'NCKU Green Magic School · 25 Xiaodong Road, North District, Tainan'),
    ]
    see_terms = ('Оплата в течение трёх дней; место подтверждается письмом оператора. Отмена: за 30 дней удержание NT$1 000; '
        'за 20/10/5 дней возврат 80/70/50%; за 3 дня возврата нет. Для промежуточных сроков нужен договор. '
        'При стихийном бедствии отдельные удержания; это не гарантированный полный возврат.')
    see_extras = ('Дневная travel insurance не включена по правилам. Поздний забор: после 18:00 NT$100, после 18:30 NT$200; '
        'до 18:00 льготное окно. Семейное жильё, транспорт и страховку считать отдельно. Прайс партнёрских школ отличается.')
    p = put('see-future-dreamers', 'S.E.E. · Future Dreamers', 'Тайвань', 'TWN', 'Taipei / Xinzhuang / Tainan',
        'general,languages,art,sport,entrepreneurship', 'day', 'Старшая группа детского сада – Grade 4; Grade 5+ только по согласованию.',
        'Все запланированные занятия на английском с иностранным преподавателем; китайская помощь по необходимости.',
        'Пять дней знакомства с профессиями через ролевые задания: кухня, авиация, сцена и медицина; творчество, спорт и общение. Это английский тематический лагерь, не инженерный курс.',
        '25–29 января 2027 на трёх площадках. Занятия 09:00–17:00; забор 17:10 или 17:40. Утренний приём 08:00–08:40.',
        fee(2027, 'NT$13 800 / 5 дней. До 11.10.2026: индивидуально NT$11 730; группа 3+ NT$11 040; 6+ NT$10 350.',
            'Материалы, обед, перекус; на первый день заявлена лагерная футболка.', see_extras, see_terms),
        'Только дневной лагерь; максимум 18 детей. Иностранный преподаватель, местный преподаватель и административное сопровождение.',
        fit('conditional', 'Подходит при Grade 4 или ниже; текущий класс неизвестен. Иностранный приём и содержание для свободного английского подтвердить.'),
        fit('conditional', 'Подходит только если принят в старшую дошкольную группу или выше; год 2020 не доказывает класс.'),
        'Кандидат на совместную поездку обоих в Тайвань с повседневным английским и профессиональными пробами.',
        ['Подтвердить классы, приём детей из зарубежной школы, наличие мест, точный пункт встречи и итоговую цену после скидочного срока.'],
        [src('Future Dreamers 2027: места, язык и цены', SEE), src('Оплата, отмена и дневная страховка', SEE_POLICY), src('Университет подтверждает адрес Taipei', 'https://som.ntub.edu.tw/index.php?Lang=en')],
        status='published_2027', priority=['both', 'general'], confirmed=['EN'])
    p['language_evidence_role'] = 'primary'
    variants(p, [dict(key=k, start='2027-01-25', end='2027-01-29', label='Future Dreamers · '+k, place=place,
        price='NT$13 800; индивидуальный early NT$11 730 до 11.10.2026') for k, place in locations], SEE)

    p = put('see-esl-engineering', 'S.E.E. · ESL Engineering', 'Тайвань', 'TWN', locations[1][1],
        'science,engineering,languages', 'day', 'Grades 3–6; Grades 1–2 — индивидуально при английском не ниже англоязычного Grade 2.',
        'Все занятия на английском; нужны базовые listening, speaking, reading и writing. Китайская помощь по необходимости.',
        'Дети проектируют и испытывают модели: колёса и оси, рычаги, гидравлический подъём и плавучесть. STEAM с практическими опытами; отдельная программируемая робототехника не заявлена.',
        '25–29 января 2027, только Fu Jen / Xinzhuang, 09:00–17:00; забор 17:10 или 17:40.',
        fee(2027, 'NT$16 800 / 5 дней. До 11.10.2026: индивидуально NT$14 280; 3+ NT$13 440; 6+ NT$12 600.',
            'Материалы, обед, перекус и лагерная футболка.', see_extras, see_terms),
        'Дневной университетский кампус; максимум 18 детей. Проживание университета не входит и не заявлено.',
        fit('conditional', 'Если Grade 3–6, подходит учебная категория; для Grade 1–2 нужна отдельная оценка английского.'),
        fit('conditional', 'Обычный Grade 3 минимум выше вероятного класса. Только Grade 1–2 с доказанным английским уровня Grade 2 и явным разрешением; дошкольникам допуск не заявлен.'),
        'Более содержательная инженерная альтернатива языковому лагерю для Матвея; Оскару не обещать автоматический допуск.',
        ['Получить подтверждение зарубежного класса, язык технических объяснений, оценку чтения/письма, задания по уровню и итоговую смету.'],
        [src('Engineering 2027: требования и прайс', ENGINEERING), src('Условия S.E.E.', SEE_POLICY)],
        status='published_2027', priority=['technical'], confirmed=['EN'])
    p['language_evidence_role'] = 'primary'
    variants(p, [dict(key='xinzhuang', start='2027-01-25', end='2027-01-29', label='ESL Engineering · Fu Jen',
        place=locations[1][1], price='NT$16 800; individual early NT$14 280 до 11.10.2026')], ENGINEERING)

    null_language = 'Язык конкретного технического занятия не указан в прочитанных правилах. Английский сайт не доказывает английский поток; требуется подтверждение.'
    null_terms = ('Перенос/отмена минимум за 72 часа, иначе course credit теряется; документированные медицинские исключения. '
        'Возвраты за пропуски — учебными кредитами, а не обычным денежным возвратом. После 10 минут льготного забора возможна доплата $1/мин.')
    null_sources = lambda url: [src('Собственная программа и расписание', url), src('Оборудование и правила', POLICY), src('Точные адреса центров', CONTACT)]
    nine = fit('conditional', 'Только после 9-летия; Матвею в 2026 будет 8–9. Уровень и английский поток подтвердить; места не проверены.')
    too_young = fit('later', 'До 9 лет текущий курс не подходит; будущие младшие варианты и исключения не подтверждены.')
    p = put('nullspace-ev3-holiday', 'Nullspace · EV3 Robotics Engineer', 'Сингапур', 'SGP', 'Rochester / Kallang / SAFRA Tampines',
        'robotics,coding,engineering', 'day', 'Заголовок/меню 9–12, таблица курса 9–13: верхняя граница расходится.',
        null_language, '10 часов за четыре утренних занятия: сборка EV3 и блочные программы. Ingenious и Innovate имеют разные механические модели; порядок лагерей свободный, опыт не обязателен.',
        '21–24 и 28–31 декабря 2026, 09:30–12:00; пять вариантов площадки/темы. Это четыре дня, без пятницы.',
        fee(2026, '$520 / 10 часов; страница не указывает ISO валюты. Пакеты 20/40/80 часов: $1 000 / 1 920 / 3 600; не цена одной смены.',
            'Ноутбук, оборудование и учебные материалы; робот и ноутбук домой не выдаются. Регистрационный сбор не взимается по FAQ.',
            'Обед/полный дневной присмотр не заявлены. Валюту, налоги, иностранный допуск и использование семейного пакета уточнить.', null_terms),
        'Полудневной центр; максимум пять учеников на преподавателя, пансион отсутствует.', nine, too_young,
        'Практический EV3 вариант Матвею с опубликованными декабрьскими датами; для уже опытного ребёнка проверить сложность.',
        ['Подтвердить возрастную границу, английский курс, валюту/налоги, иностранный приём и наличие места на выбранной площадке.'],
        null_sources(EV3), status='published_2026', priority=['technical'])
    rows = []
    for centre, start, end, theme in [('rochester','21','24','Ingenious'),('rochester','28','31','Innovate'),
            ('kallang','28','31','Innovate'),('tampines','21','24','Ingenious'),('tampines','28','31','Innovate')]:
        rows.append(dict(key=centre+'-'+theme.lower(),start='2026-12-'+start,end='2026-12-'+end,
            label=theme+' · 09:30–12:00 · '+centre,place=CENTRES[centre],price='$520 / 10 часов; валюта требует подтверждения',
            attendance_weekdays=['MO','TU','WE','TH']))
    variants(p, rows, EV3)

    for slug, title, programme, placements in [
        ('nullspace-ai-comic','AI Comic Story Creator','2,5 часа: сюжет, персонажи, генерация иллюстраций, редактирование и сборка цифрового комикса; самостоятельная ML-модель не заявлена.',
            [('rochester','13'),('kallang','12'),('tampines','13')]),
        ('nullspace-ai-game','AI Game Creator','2,5 часа: правила игры, AI-assisted код, тестирование, изменение механик и публикация веб-игры. Это вводная мастерская, не полноценный курс ML.',
            [('rochester','12'),('kallang','13'),('tampines','12')]),
    ]:
        p = put(slug, 'Nullspace · '+title, 'Сингапур', 'SGP', 'Rochester / Kallang / SAFRA Tampines',
            'ai,coding,games,art', 'day', '9–14; опыт программирования не обязателен.', null_language, programme,
            '12–13 октября 2026, 09:30–12:00; тема зависит от площадки. Опубликованные занятия 2 октября уже прошли.',
            fee(2026, '$137,50 / 2,5 часа; ISO валюты не указан. Каждая мастерская оплачивается отдельно или курс-пакетом.',
                'Ноутбук предоставляется; свой Windows/Mac допускается. Установка ПО не требуется.',
                'Проверить лицензии, возрастные условия AI-сервисов, способ детского доступа, публикацию проектов и налоги; обед/присмотр вне занятия не заявлены.', null_terms),
            'Короткая дневная мастерская; пять детей на преподавателя.', nine, too_young,
            'Короткая проба цифрового творчества Матвею; доступ в AI-сервис и сложность оценить до выбора.',
            ['Подтвердить 9-летие, английский язык, доступ иностранным детям, используемые сервисы и полную цену.'],
            null_sources(AI), status='published_2026', priority=['technical'])
        variants(p, [dict(key=centre+'-'+day,start='2026-10-'+day,end='2026-10-'+day,
            label=title+' · 09:30–12:00 · '+centre,place=CENTRES[centre],price='$137,50; валюта не подтверждена') for centre, day in placements], AI, 'single_workshop')

    p = put('nullspace-stem-holiday', 'Nullspace · STEM Explorer Holiday', 'Сингапур', 'SGP', 'Rochester / Kallang / SAFRA Tampines',
        'robotics,coding,science,engineering', 'day', '7–8; возраст соответствует конкретному Explorer, не общему диапазону сети.',
        null_language, 'WeDo 2.0, Scratch, 3D pen, SPIKE Essential и деревянные механические проекты. Четыре тематических набора; деревянные игрушки и цифровые проекты можно забрать, LEGO остаётся в центре.',
        'Точные новые смены не приведены в прочитанной текстовой таблице. Основной блок обещает 5×2 часа, FAQ называет четырёхдневный bootcamp: формат надо согласовать.',
        fee(None, '$550 / 10 часов в основном блоке; год тарифа и валюта не указаны. Weekly term $1 000 — отдельные 10 занятий.',
            'Необходимое оборудование/материалы; готовые деревянные проекты.',
            'На странице разные trial $60 и $100; это проба weekly class, не весь лагерь. Проверить сборы/валюту.', null_terms),
        'Дневной учебный центр, пять учеников на преподавателя.',
        fit('conditional', 'В 2026 подходит только до 9-летия; после него выбрать EV3/certificate. Новые смены неизвестны.'),
        fit('conditional', 'Только после 7-летия в 2027; пока 5–6 — другой Little Explorer. Даты и исключения не объявлены.'),
        'Лестница младшего инженерного развития; FLL Explore требует 15 или 20 занятий по разным страницам, не одну каникулярную неделю.',
        ['Новые смены, четыре или пять дней, английский поток, возраст на начало и актуальные prerequisites Explore: 15 или 20 занятий.'],
        null_sources(STEM), priority=['technical'])

    p = put('nullspace-minecraft-holiday', 'Nullspace · Minecraft Xcite / Xplore', 'Сингапур', 'SGP', 'Rochester / Kallang / SAFRA Tampines',
        'coding,games,engineering', 'day', '9–12; оператор предупреждает, что младшим может быть слишком быстро.',
        null_language, '15 часов / 5 дней: Minecraft Education, Redstone, блоки и Python; smart home либо escape room. Отдельные наборы свободного порядка, задания внутри недели усложняются.',
        'Опубликованное расписание — июнь 2026, уже прошло. Декабрь 2026 и лето 2027 на этой странице не подтверждены.',
        fee(2026, '$825 / 15 часов; валюта ISO не приведена. Многочасовые пакеты — отдельное предложение.',
            'Ноутбук предоставляется, Minecraft Education для класса.',
            'Домашняя лицензия Minecraft Education приобретается отдельно; стоимость не опубликована. Обед и продлённый присмотр не заявлены.', null_terms),
        'Дневной центр; пять детей на преподавателя.', nine, too_young,
        'Игровая инженерия Матвею при появлении новых дат; архивная летняя страница не доказывает зимний набор.',
        ['Новый сезон, английский, полная цена и набор для опытного ребёнка; обычный Minecraft не заменяет Education.'],
        null_sources(MINECRAFT), priority=['technical'])

    p = put('nullspace-3d-holiday', 'Nullspace · BuildUp 3D Print Design', 'Сингапур', 'SGP', 'Rochester / Kallang / SAFRA Tampines',
        'engineering,technology,entrepreneurship', 'day', 'Подробная таблица 9–16; меню 9–12 расходится.',
        null_language, 'Tinkercad и BambuStudio: допуски деталей, шестерни, рычаги и полезное изделие. 10 часов, печать как минимум одной модели за занятие; итог может быть готов через 1–2 дня после лагеря.',
        'Только прошедшее расписание 7–11 сентября 2026; отдельный четырёхдневный вариант 8–11.09 по 2,5 часа. Даты 2027 неизвестны.',
        fee(2026, '$550 / 10 часов; ISO валюты не указан. Это исходный прайс архивных смен, не предложение 2027.',
            'Ноутбук и работа на 3D-принтере; опубликовано минимум одно печатное изделие за занятие.',
            'Нужна доступная email-учётная запись для сохранения Tinkercad, проверить 2FA и детский доступ. Выдача изделия может потребовать ещё 1–2 дней пребывания.', null_terms),
        'Дневной центр, пять учеников на преподавателя.', nine, too_young,
        'Хороший мост от моделей роботов к проектированию реальных деталей; старое расписание не считать будущей доступностью.',
        ['Новый календарь, английский, детский Tinkercad, валюту/налоги и время выдачи. TKKYIA mentoring после курса требует отдельной подготовки и допуска.'],
        null_sources(PRINT), priority=['technical'])

    p = put('nullspace-fll-novice', 'Nullspace · FLL Challenge Novice Team', 'Сингапур', 'SGP', 'Singapore · конкретный тренировочный центр требует подтверждения',
        'robotics,coding,entrepreneurship', 'day', 'По странице тренинга 9–16; правила сезона и национальный/иностранный допуск отдельно.',
        null_language, 'Новичковая команда: 30 часов / 12 тренировок Jan–Mar, опыт не требуется. Main Team — другой путь: 45 часов / 18 занятий Nov–Mar и SPIKE Advanced prerequisite. Регистрация команды через Nullspace; нельзя представлять клуб и школу в одном соревновании.',
        'Точный график тренировок не прочитан. Страница клуба указывает qualifiers 24–25.03.2027 и final 27.03.2027; это даты соревнования, не лагерная смена и не подтверждённая квота иностранной команды.',
        fee(None, 'Стоимость сезона и соревнований не опубликована в прочитанном описании; не заменять её тарифом $520 за учебный модуль.',
            'Описана командная подготовка и регистрация клубом; точный пакет оборудования/сборов неизвестен.',
            'Регистрация, coach, tournament fee, транспорт и возможная поездка на мировой этап требуют отдельной сметы.',
            'Применимость centre policy к полному сезону/турнирным расходам должна быть подтверждена договором.'),
        'Регулярная дневная команда с несколькими месяцами подготовки; проживание семьи самостоятельно.',
        fit('conditional', 'Возраст 9–10 подходит после 9-летия, но нужны отбор, место в команде, язык и разрешённый национальный путь.'),
        fit('later', 'Challenge с 9 лет недоступен. Explore 7–9 только после 7-летия и предварительных занятий; в 2027 это зависит от дня рождения.'),
        'Практический кандидат на устойчивую команду Матвею, если семья использует Singapore как учебную базу; выход на Worlds требует реального квалификационного результата.',
        ['Подтвердить foreign eligibility, возрастные правила FLL Singapore, английский судейства/занятий, весь график, team size, смету и отбор. Explore: 15 занятий на team page против 20 на STEM page.'],
        [src('Challenge Novice/Main и Explore prerequisites', TEAM), src('Конфликт порога Explore', STEM), src('Общие правила центра', POLICY)], priority=['technical'])

    p = put('oyis-winter-intensive', 'Osaka YMCA International School · Winter Intensive', 'Япония', 'JPN',
        'Nakatsu Campus · 6-7-34 Nakatsu, Kita-ku, Osaka 531-0071', 'general,languages,science,art,sport', 'day',
        'Pre-K – Grade 6; классы распределяют по английскому уровню, числовая граница не опубликована.',
        'Полное английское погружение; тематические проекты и основной час Science/Technology/Engineering проходят на английском.',
        'Winter 2026: Survival Island и Winter Wonderland. Язык через проекты, творчество, PE, чтение и совместные задания; каждому intensive обещана экскурсия. Robotics — пример прошлых тем, не гарантированный отдельный зимний модуль.',
        '14–18 и 21–25 декабря 2026; 09:30–15:00. Открытие записи 20 октября. На 05.10.2026 подробный winter flyer ещё Coming Soon.',
        fee(None, 'Прайс Winter 2026 ещё не опубликован на прочитанной странице. Цены летнего или старого winter flyer не переносить.',
            'Описаны проекты и одна экскурсия; финансовые включения, обед и транспорт надо подтвердить.',
            'Оценка английского для elementary; сборы, материалы, lunch, bus и продление пока неизвестны.', 'Аванс и отмена Winter 2026 не опубликованы в прочитанном описании.'),
        'Дневной городской кампус. Прямо заявлены участники из Японии и других стран; пансион отсутствует.',
        fit('conditional', 'Соответствие Grade 6 или ниже и placement assessment; обычное языковое содержание может быть слишком простым.'),
        fit('conditional', 'Есть Pre-K/младшие группы; конкретный возраст, самостоятельность и placement подтвердить.'),
        'Подтверждённый международный дневной вариант для обоих в Осаке с двумя независимыми декабрьскими неделями.',
        ['После 20 октября проверить flyer, цены, age cutoffs, экскурсию, включения и подходящую группу для свободного английского. Старый winter PDF подписан 2025, но URL содержит 2024.'],
        [src('Winter 2026, English immersion и зарубежные дети', OYIS)], status='published_2026', priority=['both', 'general'], confirmed=['EN'])
    p['language_evidence_role'] = 'primary'
    variants(p, [dict(key=key,start=start,end=end,label=title+' · 09:30–15:00',place=p['place'],price='Winter 2026 цена пока неизвестна')
        for key,start,end,title in [('survival','2026-12-14','2026-12-18','Survival Island'),('wonderland','2026-12-21','2026-12-25','Winter Wonderland')]], OYIS)

    for slug, title, age, programme, mat, osc in [
        ('ea-summer-immersion-junior','Immersion · Grades 1–2','Grades 1–2 на начало смены; требуется свободный EN или JA для основного лагеря.',
         'Английский пансион: природа, озеро, командные игры, творчество; младшая Nature Inquiry и bouldering с возрастными заданиями. Свободный английский нужен для общения и правил безопасности.',
         fit('conditional','Только если реально Grade 1–2; при старшем классе выбрать Primary. Текущий класс неизвестен.'),
         fit('conditional','Только если Grade 1 или 2 на начало нового сезона и достаточно самостоятельности. Даты рождения из зимнего набора сюда не переносить.')),
        ('ea-summer-immersion-primary','Immersion · Grades 3–6','Grades 3–6 на начало смены; свободный английский для Immersion.',
         'Английский пансион с природой, творчеством и возрастными командными задачами; kayaking заявлен для Grades 3–9. Технические гаджеты отсутствуют: лагерь специально screen-free.',
         fit('conditional','Подходит при действительном Grade 3–6, свободном английском и готовности к ночёвкам; набор 2027 ещё неизвестен.'),
         fit('later','До Grade 3 эта группа не подходит; младшая программа отдельно.')),
    ]:
        p = put(slug, 'English Adventure · Summer '+title, 'Япония', 'JPN', 'Mountain Park Tsunan · Ko 1745-1, Kaminogo Ueda, Tsunan, Niigata',
            'general,languages,sport,science', 'boarding', age, 'Immersion: английская лагерная жизнь весь день. Challenge и Challenge Plus — отдельные языковые уровни.',
            programme, 'Архив Immersion 2026: 26–30.07, 03–07.08, 11–15.08, 19–23.08, по четыре ночи. Новые летние смены 2027 ещё не опубликованы.',
            fee(2026, 'Архив 2026: JPY 122 700 / 4 ночи для Grades 1–6. Это не тариф 2027.',
                'Tokyo transport туда/обратно, lodge, 4 завтрака/5 обедов/4 ужина, активности, travel insurance, сборы и налог.',
                'Nagoya +JPY 15 000; самостоятельный приезд даёт скидку JPY 7 000. Доставка багажа отдельно; братья могут иметь разные часы встречи.',
                '2026: отмена за 20–8/7–2/1 дней — удержание 20/30/40%; в день до check-in 50%, после 100%. Дополнительно 3,6% card fee от возврата. English-only policy допускает досрочный отъезд без возврата при нарушениях.'),
            'Все классы в lodge согласно текущей правке страницы. Минимум 90 детей на смену и 4 на класс с условием по полу; готовность младших к пансиону оценить отдельно.',
            mat, osc, 'Общий англоязычный пансион для будущего лета; разделён по школьной группе, без обещания робототехнических часов.',
            ['Получить расписание/прайс 2027, школьный допуск, foreign registration, минимум группы, room allocation и условия нового договора.'],
            [src('Лето 2026: группы, включения и отмена', SUMMER), src('Immersion: английская среда и требования', IMMERSION)], priority=['general', 'boarding'], confirmed=['EN'])
        p['language_evidence_role'] = 'camp_life'

    p = put('sfs-sailing', 'Camp SFS · Yacht Sailing Basics', 'Южная Корея', 'KOR', 'Seoul Foreign School · 39 Yeonhui-ro 22-gil, Seoul; занятия на воде вне кампуса',
        'general,sport,science', 'day', 'Grades 2–5; применять школьный класс, а не возраст.',
        'Elementary camp заявлен на английском; язык конкретного водного инструктажа партнёра требует подтверждения.',
        'Пять дней: безопасность на воде, ветер, управление парусами, мини-гонка; kayak и SUP. Каждый день выезд с counselors, еда на месте; партнёры Seoul Yachting Association / SMOE.',
        'Только архив 15–19 и 22–26 июня 2026. Программа/цена/площадки 2027 не объявлены.',
        fee(2026, 'Общий Elementary external tariff: KRW 680 000 early / 720 000 regular + ежегодные KRW 100 000. Применимость к sailing и отдельная доплата не подтверждены.',
            'Обед/перекусы на месте заявлены для sailing; общий Elementary включает материалы и school bus.',
            'Возможные partner fees, оборудование, трансфер к воде и страховку подтвердить. Общий bus не доказывает всех специальных включений.',
            'Условия 2026: после 22.03 обычный возврат только credit; medical/refund by operator cancellation отдельно. Change fee KRW 70 000, lost ID KRW 10 000. Не переносить условия в новый сезон.'),
        'Дневная программа с выездами; открытые места и внешний приём зависят от отбора Camp SFS.',
        fit('conditional','Возможный Grade 2–5; требуется действительный класс и английское видеоинтервью.'),
        fit('later','Для младшего возраста пока требуется Grade 2; новые исключения не опубликованы.'),
        'Полезная спортивно-практическая альтернатива Матвею; прежние даты не доказывают лето 2027.',
        ['Новый сезон, иностранный допуск, фактическая категория школы семьи, английский водного инструктажа, требования к плаванию, equipment и полный счёт.'],
        [src('Sailing curriculum / Grade 2–5', SFS), src('Квоты и EN interview', SFS_ENTRY), src('Класс по школе, а не дню рождения', SFS_GRADE), src('Архивные условия 2026', SFS_POLICY)],
        priority=['general'])
    # Do not confirm partner's English independently of the on-campus declaration.
    p['confirmed_instruction_languages'] = []

    by_slug = {p['slug']:p for p in profiles}
    p = by_slug['nullspace']
    p.update(checked=CHECKED, age='Little Explorer 5–6; STEM Explorer 7–8; SPIKE certificate 9–16; Arduino 10–16; Python 10–16 по текущему меню.',
        programme='SPIKE certificate: 60 часов / 6 уровней. FLL Main после Advanced, но Novice Team принимает без опыта: 30 часов / 12 занятий. Explore: 15 занятий на team page против 20 на STEM page; допуск уточнить. Нельзя одновременно представлять школу и Nullspace в одном турнире.',
        timing=dict(status='next_unannounced', label='Декабрьский EV3 и октябрьские AI-мастерские вынесены в отдельные карточки. Minecraft June2026 / 3D September2026 — архив; расписание 2027 не подтверждено.', sessions=[]),
        price=fee(None, '10 часов около $520 без registration/admin fee по FAQ; валюта, налог и стоимость командного сезона требуют подтверждения.',
            'Оборудование и материалы; обычные LEGO/ноутбуки не выдаются домой.', 'Полный тренировочный сезон и tournament fee считать отдельно.', null_terms),
        questions=['Подтвердить EN каждого курса, foreign eligibility, полную смету, отбор в команду и Explore threshold 15/20 занятий.'],
        sources=[dict(title=t,url=u,checked=CHECKED) for t,u in [src('Текущие уровни',NULL),src('Novice/Main/Explore',TEAM),src('Правила центра',POLICY),src('Explore prerequisites',STEM)]])
    p = by_slug['camp-sfs']
    p['checked'] = CHECKED
    p['place'] = '39 Yeonhui-ro 22-gil, Seodaemun-gu, Seoul 03723'
    p['age'] = 'Pre-K3/4; K–Grade1; Grades2–3; Grades4–5 — по зарегистрированному классу в September2026, не по возрасту.'
    p['questions'] = ['Получить season2027 и точный зарегистрированный класс. Eligibility75% SFS /25% non-English school не объясняет категорию приезжающих из другой англоязычной школы; семье нужна письменная классификация. Все внешние дети проходят EN video interview.']
    p['price']['extras'] += ' В 2026 change fee KRW70 000, replacement ID KRW10 000; bus требует местный номер +82 и фиксированный маршрут, места ограничены.'
    p['price']['deposit'] += ' Счёт оплатить за два рабочих дня /48h; пропуск срока может отменить место или early price.'
    for s in p['sources']:
        s['checked'] = CHECKED
    p['sources'].append(dict(title='Класс из школы, не возраст',url=SFS_GRADE,checked=CHECKED))
    p['sources'].append(dict(title='Автобус 2026: фиксированный маршрут и местный номер',url='https://www.seoulforeign.org/camp-sfs/transportation',checked=CHECKED))


def extend_report_v79(report):
    report['shortlist'].extend([
        dict(label='Тайвань · английская инженерия и профессии зимой',slugs=['see-esl-engineering','see-future-dreamers','steamsquad-expedition','grove-flight'],
            reason='Матвею — Engineering при Grade 3–6 или Expedition 8–12; Оскару — Future Dreamers при senior kindergarten или выше. На 25–29 января 2027 можно выбрать разные программы на Fu Jen. Требуются реальные классы, иностранный допуск и английское чтение. Скидка S.E.E. действует до 11 октября; это не последний день набора.'),
        dict(label='Сингапур · EV3 и путь в FIRST',slugs=['nullspace-ev3-holiday','nullspace-fll-novice','nullspace-stem-holiday','empire-kubo'],
            reason='Матвею после 9 лет — декабрьский EV3 или многомесячная FLL Novice Team. Оскару сейчас KUBO 4–6, Explorer только после 7 лет. Английский и иностранный допуск Nullspace пока неизвестны; для Explore страницы требуют 15 или 20 занятий. Поездку на мировой этап планировать после реального отбора команды.'),
        dict(label='Япония · декабрь вместе, летний пансион отдельно',slugs=['oyis-winter-intensive','tokyo-coding','ea-summer-immersion-junior','ea-summer-immersion-primary','english-adventure-winter'],
            reason='OYIS в Осаке: 14–18 и 21–25 декабря 2026, Pre-K–G6 и английская среда; запись открывается 20 октября, прайс ещё неизвестен. Tokyo Coding — техническая альтернатива. English Adventure summer 2026 раскрывает пансион для будущего выбора 2027; зимнюю границу рождения Оскара проверять отдельно.'),
        dict(label='Корея · английский лагерь с реальным отбором',slugs=['camp-sfs','sfs-sailing'],
            reason='Seoul Foreign School 2026: английский день, реальные школьные классы и обязательное видеоинтервью для внешних детей. Применимость квоты 75/25 к приезжающим из другой англоязычной школы не разъяснена. Sailing G2–5 — отдельный партнёрский формат; лето 2027 пока не объявлено.'),
    ])
    report['gaps'].extend([
        dict(country='Тайвань',iso='TWN',provider='v79: S.E.E.2027',
            detail='Future Dreamers: senior kindergarten–G4; Engineering: G3–6, исключение для G1–2 после оценки английского. Английский всех активностей заявлен прямо. Адрес Taipei 321 Jinan Road подтверждён университетом; партнёрские школы имеют отдельные цены. Прямой HTTP дал 403, страницы оператора прочитаны через web reader.',
            next_action='Письменный иностранный/школьный допуск, прайс после 11 октября, финальный договор и семейные расходы дневной поездки.',url=SEE),
        dict(country='Сингапур',iso='SGP',provider='v79: Nullspace course и FLL pathway',
            detail='EV3 в декабре 2026 и AI 12–13 октября имеют точные даты; Minecraft в июне и 3D в сентябре — архив. Английский не подтверждён. Валюта $ без ISO; 3D 9–16 против меню 9–12, EV3 9–13 против заголовка 9–12. STEM: 5 дней в программе против 4 в FAQ. Explore: 15 или 20 занятий. Novice: 30 часов без опыта; Main: 45 часов после Advanced.',
            next_action='Язык, иностранный допуск, валюта, новые даты, классы и национальный путь FLL. Динамический каталог Outdoor School и Myoko с HTTP 406 ещё требуют чтения конкретных программ.',url=TEAM),
        dict(country='Япония',iso='JPN',provider='v79: OYIS / English Adventure',
            detail='OYIS Winter 2026: две недели, запись с 20 октября; flyer и цена ещё неизвестны. Старый winter PDF с 2024 в URL подписан 2025 — это не текущий документ. English Adventure Summer 2026: общий английский пансион, все группы в lodge по исправлению страницы, доставка багажа отдельно. Лето 2027 не объявлено.',
            next_action='Новый зимний flyer и счёт OYIS после 20 октября, English Adventure Summer 2027; настоящие классы детей, расписание, сложность и условия ночёвок.',url=OYIS),
        dict(country='Южная Корея',iso='KOR',provider='v79: Camp SFS admission nuance',
            detail='Внешний тариф не доказывает принятие семьи. Квота 75% SFS / 25% non-English school не объясняет другие англоязычные школы. Класс определяется по школе в September 2026, без пересчёта по рождению. Sailing G2–5 и тарифы 2026 — архив; английский водного партнёра не подтверждён.',
            next_action='Проспект 2027, категория семьи, зарубежный приём, язык партнёрского курса, прайс и страховка. Продолжать Jeju, Busan и другие международные младшие лагеря.',url=SFS_ENTRY),
    ])
