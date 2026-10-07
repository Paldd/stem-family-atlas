"""Programme-specific winter dates, grade gates and instruction evidence for Asia."""


def add_asia(add, src, fit, profiles):
    def put(*args, **kw):
        add(*args, **kw)
        p = profiles[-1]
        p['checked'] = '2026-10-05'
        for s in p['sources']:
            s['checked'] = p['checked']
        return p

    def fee(year, label, included, extras, deposit):
        return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)

    def dated(p, days, label, price, url, scope='camp_session'):
        p['timing']['sessions'] = days
        p['timing']['session_details'] = [dict(start=a, end=b, label=label, price=price,
            source=url, place=p['place'], formats=p['formats'], date_scope=scope) for a, b in days]

    housing = 'Дневные занятия; жильё, перелёт и вечернее время семьи отдельно.'
    camp_url = 'https://www.computhink.com.sg/'
    mon = [['2026-11-23','2026-11-25'],['2026-11-30','2026-12-02'],
           ['2026-12-07','2026-12-09'],['2026-12-14','2026-12-16']]
    thu = [['2026-11-26','2026-11-28'],['2026-12-03','2026-12-05'],
           ['2026-12-10','2026-12-12'],['2026-12-17','2026-12-19']]
    courses = [
        ('computhink-lego','LEGO SPIKE Prime Robotics','holiday-lego-robotics-camp/',
         '7–12; максимум 8 учеников','robotics,coding',
         'Работа парами: моторы и механика, датчики и цветовые условия, затем бой роботов. Внутренний финал не является международным соревнованием.',
         thu, [('am','09:30–12:30')]),
        ('computhink-scratch','Scratch Creative Coding','holiday-scratch-coding-camp/',
         '7–11; максимум 8 учеников','coding,games,art',
         'Начальный курс: события, условия, переменные, циклы и отладка. Каждый делает игры/анимацию и сохраняет проекты.',
         [mon[1],mon[3]], [('pm','14:00–17:00')]),
        ('computhink-agent','Minecraft Agent · The Warden’s Maze','holiday-minecraft-coding-camp/',
         '7–12; максимум 8 учеников','coding,games',
         'Minecraft Education: команды агенту, циклы, условия, автоматизация и отладка лабиринта. Начальный курс, не самостоятельное обучение ИИ.',
         mon, [('am','09:30–12:30'),('pm','14:00–17:00')]),
        ('computhink-redstone','Minecraft Redstone Engineering','minecraft-holiday-workshops/',
         '7–12; максимум 8 учеников','coding,games,science',
         'Виртуальные цепи, переключатели, автоматические двери, мосты и фермы. Инженерная логика внутри Minecraft, физические роботы не заявлены.',
         thu, [('am','09:30–12:30'),('pm','14:00–17:00')])]
    for slug, name, tail, age, themes, content, days, times in courses:
        url = camp_url + tail
        p = put(slug, 'Computhink · ' + name, 'Сингапур', 'SGP',
            'Toa Payoh Library · 6 Toa Payoh Central, Singapore 319191', themes, 'day', age,
            'Язык преподавания на прочитанной странице курса явно не указан. Английский сайт не является доказательством EN-инструктора.',
            content, 'Ноябрь–декабрь 2026; отдельные трёхдневные утренние/дневные варианты ниже.',
            fee(2026,'SGD 367 за 3 дня × 3 часа, за выбранный вариант.',
                'Ноутбуки и учебное оборудование в пользование; сертификат окончания.',
                'Питание, налог в цене, дорога и отмена публично не установлены. Учебные роботы не выдаются в собственность.',
                'Правила отмены и полный счёт нужно подтвердить до оплаты.'), housing,
            fit('conditional','Возраст подходит; нужны EN-преподаватель, содержание по опыту и иностранный допуск.'),
            fit('later','В ноябре–декабре 2026 будет 5–6; минимальный возраст этого курса 7.'),
            'Короткий технический курс для Матвея; начальный уровень может повторять уже знакомое.',
            ['Подтвердить EN, продвинутые задачи, место, иностранный допуск, питание, GST и отмену.'],
            [src('Собственные даты, стоимость и программа курса',url)],
            status='published_2026',priority=['technical'])
        variants = []
        for i, (a,b) in enumerate(days,1):
            for key, clock in times:
                variants.append(dict(start=a,end=b,label='3 дня · '+clock,
                    price='SGD 367 за один вариант / 9 часов',source=url,place=p['place'],
                    formats=['day'],variant_key='w'+str(i)+'-'+key,date_scope='camp_session'))
        p['timing'].update(variant_keyed=True,sessions=[[v['start'],v['end']] for v in variants],
            session_details=variants)

    holiday = 'https://www.britishcouncil.sg/english-courses/camps/holiday'
    terms = 'https://www.britishcouncil.sg/english-courses/register/terms-conditions'
    filebase = 'https://www.britishcouncil.sg/sites/default/files/'
    pdfs = {
        'early': filebase+'2026_novdecholidaycamps_learning_outcomes_earlyyears_k1-k2_final.pdf',
        'p12': filebase+'2026_novdecholidaycamps_learning_outcomes_p1-p2_final.pdf',
        'p34': filebase+'2026_novdecholidaycamps_learning_outcomes_p3-p4_final.pdf'}
    weeks = [['2026-11-23','2026-11-27'],['2026-11-30','2026-12-04'],
             ['2026-12-07','2026-12-11'],['2026-12-14','2026-12-18']]
    for key, name, age, place, content, days, mat, osc in [
        ('early','Early Years · Where We Live','Preschool K1–K2; числовой возраст на странице смены не указан',
         'Napier Road Centre, Singapore; только этот центр и только четвёртая неделя',
         'Английский, истории о домах, растения, модели комнат и миниатюрного города. Общая творческая программа.',
         [weeks[3]],fit('not_eligible','Группа Preschool K1–K2; Матвею выбирать Primary.'),
         fit('conditional','Нужен соответствующий K1–K2 уровень; возраст 2020 года не доказывает школьную категорию.')),
        ('p12','Primary 1–2','Primary 1–2; соответствие зарубежного класса надо подтвердить',
         'Napier Road Centre / Toa Payoh Centre, Singapore; центр выбирается отдельно',
         'Темы четырёх недель: окружающий мир, дружба, животные, полёт. Проекты: путеводитель, помощь животным и выставка летающих объектов.',
         weeks,fit('conditional','Возраст сам по себе не определяет P1–2; подтвердить текущий класс.'),
         fit('conditional','Если уже в подходящем Primary-классе; K1–K2 — отдельная программа.')),
        ('p34','Primary 3–4','Primary 3–4; возраст сам по себе не определяет класс',
         'Napier Road Centre / Toa Payoh Centre, Singapore; центр выбирается отдельно',
         'Карты и аудиогид, экология и климатическая речь, проект спортивного события, животные. Командные проекты на английском.',
         weeks,fit('conditional','Подтвердить соответствие класса P3–4; это вероятный уровень, не подтверждённый допуск.'),
         fit('later','Для младшего ребёнка пока ориентир; неизвестный класс не даёт права на P3–4.'))]:
        p = put('bc-sg-'+key, 'British Council Singapore · '+name, 'Сингапур','SGP',place,
            'general,languages,science,art','day',age,
            'Английский — язык занятий; это общий языковой/project camp, не робототехнический интенсив.',
            content,'09:00–13:00; точные недели ноября–декабря 2026 ниже.',
            fee(2026,'SGD 805 за неделю; минимум одна неделя.',
                'Материалы, сертификат и 9% GST.',
                'Питание и трансфер не доказаны включёнными. Скидку «до 400» не вычитаем без личного расчёта.',
                '§5.2 допускает 75% до старта, §5.6 ограничивает возврат: требуется письменное разрешение противоречия.'),
            housing,mat,osc,'Выбирать именно класс и центр; отдельного технического трека здесь нет.',
            ['Класс, места, точный адрес, питание, иностранный допуск и разрешение конфликта возврата.'],
            [src('Недели, центры и стоимость',holiday),src('Собственный PDF выбранного уровня',pdfs[key]),
             src('Условия: camps и конфликт возврата',terms)],status='published_2026',confirmed=['EN'])
        dated(p,days,name+' · 09:00–13:00','SGD 805 / неделя',holiday,'day_camp_window')

    winter = 'https://www.britishcouncil.sg/english-courses/camps/study'
    wp = filebase+'winter_2027_camps_-_learning_outcomes_-_primary.pdf'
    p = put('bc-sg-winter-primary','British Council Singapore · Winter 2027 Primary','Сингапур','SGP',
        'Napier Road Centre, Singapore; Toa Payoh для этой зимней программы не указан',
        'general,languages,science,art','day','Программа 7–17, потоки Primary / Secondary; здесь Primary, класс подтвердить',
        'Английский. Один из двух потоков назначается после диагностики первого дня; выбирать конкретный STEM-поток свободно не обещают.',
        'Вторая неделя: комнаты либо модели американских горок; третья: профессии либо научные опыты; пятая: магазин либо немое кино. Основной курс английский.',
        '09:00–13:00; пять недель 18 января–19 февраля 2027. 1–4 и 9–12 февраля по четыре дня; 5 и 8 февраля занятий нет.',
        fee(2027,'SGD 805 / неделя по странице; цену коротких недель подтвердить, не пересчитываем автоматически.',
            'Материалы, сертификат, 9% GST.',
            'Скидка до SGD 550 зависит от пакета. Питание, перелёт и жильё отдельно.',
            '§5.2/§5.6 противоречат по возврату; до оплаты нужен конкретный договор.'),
        housing,fit('conditional','Возраст подходит; нужен Primary-класс и назначенный уровень языка.'),
        fit('conditional','Только после 7-летия к началу выбранной недели и подтверждения Primary-класса.'),
        'Точная зимняя альтернатива для семьи, но научный поток не гарантирован.',
        ['Класс, языковая диагностика, доступность STEM-потока и итог короткой недели.'],
        [src('Точные недели и закрытия 2027',winter),src('20 страниц: темы и диагностическое распределение',wp),
         src('Договор camps',terms)],status='published_2027',confirmed=['EN'],priority=['general'])
    dated(p,[['2027-01-18','2027-01-22'],['2027-01-25','2027-01-29'],
        ['2027-02-01','2027-02-04'],['2027-02-09','2027-02-12'],['2027-02-15','2027-02-19']],
        'Primary · 09:00–13:00 · поток после диагностики','SGD 805 advertised; короткую неделю подтвердить',winter,'day_camp_window')

    tw = 'https://www.britishcouncil.org.tw/en/english/young-learners/primary/winter-holiday-course'
    for slug,name,age,content,mat,osc in [
        ('bc-tw-early','Early Years','4–6',
         'История At the Zoo, драматические игры и LEGO-сцены для собственного рассказа; робототехника не заявлена.',
         fit('not_eligible','Максимум 6; Матвей старше.'),fit('conditional','Только пока Оскару 6, до 7-летия.')),
        ('bc-tw-primary','Primary Storytelling / Toontastic','6–12 и уже Grade 1 или выше',
         'Анимация Toontastic 3D, сценарий, запись озвучки и показ родителям. Не курс ИИ/роботов.',
         fit('conditional','Возраст подходит, Grade 1+ и новый набор подтвердить.'),
         fit('conditional','Возраст недостаточен без Grade 1+; текущий класс неизвестен.'))]:
        put(slug,'British Council Taiwan · Winter 2027 '+name,'Тайвань','TWN',
            'Центры Xinyi / ShiPai / Songshan / Linkou; площадка выбранной группы требует подтверждения',
            'general,languages,art','day',age,'Английский — язык творческих занятий.',content,
            'Страница уже 2027; точные даты и часы не опубликованы в прочитанном материале.',
            fee(None,'Цена нового курса не раскрыта.','Состав пакета уточнить.',
                'Жильё и дорога отдельно.','Получить текущие условия.'),housing,mat,osc,
            'Общая английская зима; выбирать возрастной поток.',
            ['Даты, цена, часы, класс, центр, питание и доступ иностранцев.'],
            [src('Актуальная программа 2027 и Grade 1+',tw)],status='partial_2027',confirmed=['EN'])

    squad = 'https://steamsquad.io/en/camps/expedition27'
    p = put('steamsquad-expedition','STEAM SQUAD · Taiwan Expedition 2027','Тайвань','TWN',
        'Beitou · No. 139, Sec. 1, Zhongyang N. Rd., Taipei','science,general,art','day',
        'Рекомендовано 8–12; 8–12 участников','Обучение на английском прямо заявлено.',
        'Полевая наука, музеи, природа, транспорт и творчество. Не робототехнический интенсив.',
        '21.01–03.02.2027, десять будних дней, 09:00–17:30. Выходные свободны; только полный курс.',
        fee(2027,'NTD 27 000 / все 10 дней; NTD 24 000 только при оплате до 05.12.2026.',
            'Программа, материалы, входы, обед/перекус и заявленная страховка несчастного случая.',
            'EasyCard примерно NTD 200/день отдельно; это ориентир, не окончательный транспортный счёт.',
            'Отмена 14+ дней:90%,7–13:50%,4–6:30%,позже:0. Недобор 8 к 05.01:полный возврат.'),
        housing,fit('candidate','Возраст 9–10 входит в рекомендуемые 8–12.'),
        fit('later','6–7 ниже рекомендуемых 8; младший допуск не обещан.'),
        'Конкретная английская научная поездка Матвею; Оскару нужен отдельный план.',
        ['Набор, опытный инструктор, транспорт, страховой объём и условия использования фотографий.'],
        [src('Собственные 10 дней, цена, включения и отмена',squad)],
        status='published_2027',confirmed=['EN'],priority=['general'])
    dated(p,[['2027-01-21','2027-02-03']],
        'Единый курс · 10 будних дней · 09:00–17:30 · выходные свободны',
        'NTD 27 000 за полный курс; early NTD 24 000 при оплате до05.12.2026',squad,'day_camp_window')

    japan = 'https://codinglab.jp/holiday-coding-tech-camp/'
    faq = 'https://codinglab.jp/faq/'
    put('codinglab-japan','Coding Lab Japan · Holiday Coding & Tech','Япония','JPN',
        'Shirokanedai · 3-14-4 TRUSTVALUE Shirokanedai 7F-A, Minato, Tokyo 108-0071; Ebisu office не classroom',
        'coding,games,robotics,ai','day','Учебные уровни 5–6 / 7–9 / 10–12 / 13–18; меню конкретной смены не подтверждено',
        'Страница holiday camp прямо заявляет all in English.',
        'Holiday и weekly версии одного модуля имеют одинаковую программу. 7–9 начинают со Scratch; Python Junior / App Inventor для 10–12. Другие треки выбирать по действующему меню.',
        'В заголовке Spring 16–31 марта 2026; в тексте winter, календарь no event found. Новые даты 2026/27 не установлены.',
        fee(None,'Цена зависит от модуля; нового holiday-прайса нет.',
            'Оборудование на занятиях предоставляется.','Вода, канцелярия, жильё и дорога семьи отдельно.',
            'Новый camp-договор ещё нужен.'),housing,
        fit('conditional','Уровень 7–9 либо 10–12 определяется возрастом на фактическую смену и модулем.'),
        fit('conditional','Переход 5–6 → 7–9 зависит от дня рождения; новые camp-даты неизвестны.'),
        'Есть доказанное EN-обучение и возрастная лестница; holiday может повторить уже пройденный weekly-модуль.',
        ['Новые дни, модуль, цена, уровень после трёх лет робототехники и иностранный допуск.'],
        [src('Holiday: язык и конфликт сезонного шаблона',japan),src('FAQ: возраст и одинаковые модули',faq)],
        confirmed=['EN'],priority=['technical'])

    seoul = 'https://lfseoul.org/en/lfs-summer-camp-2026/'
    p = put('lfs-seoul','Lycée français de Séoul · Summer Camp','Южная Корея','KOR',
        '7 Seorae-ro, Seocho-gu, Seoul 06581','general,languages,art,sport','day',
        'Архив 2026: 3–11, рождение Jan2015–Dec2022; PS–GS / CP–CM2',
        'Утром French либо English; после обеда FR/EN с корейским. Английская языковая ветка, не полностью EN STEM.',
        '09–12 языковой курс, 13–15:55 активности, выдача детей 16:00; обед включён. Робототехника не заявлена.',
        '6–16 июля 2026: 9 дней. Набор и когорты 2027 не опубликованы.',
        fee(2026,'KRW 1 040 000 / 9 дней для внешнего ученика, архив.',
            'Занятия и обед.','Доказательство daily-life liability insurance обязательно; жильё отдельно.',
            'Условия нового набора подтвердить.'),housing,
        fit('conditional','Новый возрастной набор и документы надо подтвердить.'),
        fit('conditional','Новый набор, класс и EN-ветку подтвердить; архивный birth-window не переносится.'),
        'Внешние дети допускаются, но иностранного паспорта недостаточно: требуется Alien Registration Card ребёнка и родителя.',
        ['Условия иностранной школы, parent nationality, ARC, паспорта, родство, прививки, страховка, medical form и набор2027.'],
        [src('Собственный набор: язык, цена и иностранные документы',seoul)],confirmed=['EN'])
    p['language_evidence_role'] = 'language_lessons'
