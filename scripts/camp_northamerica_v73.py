"""Specific North American programmes; preserve unresolved operator conflicts."""


def add_northamerica(add, src, fit, profiles):
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

    day = 'Дневной лагерь; жильё, дорога и время родителей вне занятий отдельно.'
    lang = 'Язык технического преподавания явно не установлен; английский сайт не доказывает EN-группу.'
    em = 'https://www.campemerson.com/about-us/dates-fees-faqs/'
    science = 'https://www.campemerson.com/about-us/activities/science-adventure/'
    for slug, title, dates, price, content in [
        ('emerson-two-weeks', 'Two-Week General Camp',
         [['2027-06-27','2027-07-10'],['2027-07-11','2027-07-24'],['2027-07-25','2027-08-07']],
         'USD 4 800 до 1 ноября / 5 100 после за 2 недели.',
         'Общий пансион, восемь electives. Научные опции: модели ракет, CO₂-машины и опыты; полноценная робототехника не заявлена.'),
        ('emerson-awesome-week', 'Awesome Week · первый короткий заезд',
         [['2027-08-08','2027-08-14']],
         'USD 2 450 до 1 ноября / 2 600 после за 1 неделю.',
         'Короткий общий пансион: четыре electives и день специальных событий. Для первых ночёвок; технический интенсив не заявлен.')]:
        p = put(slug, 'Camp Emerson · '+title, 'США','USA','Hinsdale, Massachusetts · Berkshires',
            'general,science,sport,art','boarding','7–15; домики по завершённому школьному классу',
            'Международные дети есть, но прямое обещание языка преподавания в прочитанных материалах не найдено.',
            content,'Лето 2027; отдельные реальные заезды ниже.',
            fee(2027,price,
                'Программа пансиона; прачечная заявлена. Полный состав питания/материалов в действующем договоре ещё нужен.',
                'Автобус USD 200 в каждую сторону; stay-over между сменами USD 200 за каждый. Перелёт отдельно.',
                'Сумма аванса и правила отмены не раскрыты в прочитанных материалах; не обещаем возврат.'),
            'Ночёвки в лагере; около 10 детей в домике и 2–3 counsellors — заявление оператора.',
            fit('candidate','Возраст подходит; согласовать класс, язык и выбранные electives.'),
            fit('conditional','Только после 7-летия к началу выбранного заезда; готовность к ночёвкам отдельно.'),
            'Общий международный отдых с научными опциями; может дополнять постоянную соревновательную команду.',
            ['Язык инструктора, питание/снаряжение, полный договор, даты рождения и доступ иностранцам.'],
            [src('Смены, тарифы 2027 и FAQ',em),src('Научные активности',science),
             src('Общий пансион и международные дети','https://www.campemerson.com/about-us/')],
            status='published_2027',priority=['general','boarding'])
        dated(p,dates,title,price,em)
        if slug=='emerson-two-weeks':
            p['price']['other_packages'] = '3 недели USD 7 200/7 500; 4 — 9 350/9 700; 5 — 11 550/11 950; 6 — 13 850/14 250; 7 — 15 700/16 100 до/после 1 ноября. Доплаты stay-over отдельно.'
            p['price']['label'] += ' Другие пакеты: '+p['price']['other_packages']

    st = 'https://www.summertech.net/'
    put('summertech-python','SummerTech · Python / SUNY Purchase','США','USA',
        'Purchase College SUNY · 735 Anderson Hill Rd, Purchase, NY 10577',
        'coding,games','day,boarding','Rising 4th–12th graders; правило класса важнее возраста из старых материалов',
        lang,'Python, GitHub Codespaces и выбранный elective. Начальный Python рекомендуют младше 14; Java ориентирован на старших.',
        'Опубликован только архив лета 2026; новый календарь 2027 ещё не установлен.',
        fee(2026,'Архив: commuter USD 1 650/нед.; overnight +650, итого 2 300. Пакет 12 ночей USD 5 100; early/способ оплаты меняли тариф.',
            'Лаборатории, курс, обед и ужин; overnight также завтрак и общежитие с надзором.',
            'Перелёт/трансфер отдельно. +650 — доплата к базовой программе, не полный пансионный тариф. Цену 2027 не переносим.',
            'Общее правило: 100% до 30 апреля текущего camp year; после 1 мая максимум 50%, менее 7 дней — 0. Договор 2027 подтвердить.'),
        'День либо университетское общежитие; в архиве week A без ночёвок, B–F с ними.',
        fit('conditional','Требуется подтверждённый rising Grade 4+; текущий школьный класс неизвестен.'),
        fit('later','Минимум rising Grade 4; возраст 6–7 этого не подтверждает.'),
        'Будущий технический кандидат Матвею; история занятий не заменяет школьную категорию.',
        ['Grade 4, новый сезон/прайс, EN-преподавание, иностранный допуск и минимальный возраст общежития.'],
        [src('Текущий школьный допуск',st),src('Архивные тарифы','https://www.summertech.net/dates-pricing/'),
         src('Включения','https://www.summertech.net/whats-included/'),src('Python','https://www.summertech.net/python/'),
         src('Ночёвки','https://www.summertech.net/overnight/'),src('Отмена','https://www.summertech.net/terms-and-conditions/')])

    iv = 'https://stemschoolinventor.ca/summer-camp-laval/'
    faq = 'https://stemschoolinventor.ca/camp-faq/'
    booking = 'https://inventor-camps.jumbula.com/SUMMERLAVAL2027/'
    weeks = [['2027-06-28','2027-07-02'],['2027-07-05','2027-07-09'],
        ['2027-07-12','2027-07-16'],['2027-07-19','2027-07-23'],
        ['2027-07-26','2027-07-30'],['2027-08-02','2027-08-06'],['2027-08-09','2027-08-13']]
    courses = [
        ('inventor-laval-junior','Junior LEGO','STEMJuniorLEGODayCamp456yearsold','4.5–6 в заголовке / 4.5–7 в описании',389,
         'LEGO-конструирование, ScratchJr и опыты; отдельный набор/iPad младшим.',
         fit('not_eligible','Матвей старше верхней границы обоих вариантов.'),
         fit('conditional','В 2027 будет 6–7: до 7-летия подходит; при 7 нужен ответ по конфликту верхнего возраста.')),
        ('inventor-laval-mechanics','Junior Mechanics','STEMJuniorMechanicsDayCamp67yearsold','6–7',409,
         'Механика LEGO, анимация ScratchJr, научные опыты; утренний и дневной учебные блоки.',
         fit('not_eligible','Матвей старше 7; выбрать Middle Robotics+.'),
         fit('candidate','В 2027 возраст 6–7 подходит; EN-группа и уровень пока требуют ответа.')),
        ('inventor-laval-middle','Middle Robotics','STEMMiddleRoboticsDayCamp89yearsold','8–9',429,
         'WeDo 2.0 в парах и Minecraft Education индивидуально; инженерные и научные задания.',
         fit('conditional','Только пока Матвею 9, до 10-летия; содержание может быть начальным.'),
         fit('later','Минимум 8; Оскару в 2027 будет 6–7.')),
        ('inventor-laval-middle-plus','Middle Robotics+','STEMMiddleRoboticsDayCamp910yearsold','9–10',439,
         'LEGO SPIKE Essential, Minecraft Education и опыты. Essential отличается от Prime в старшей группе.',
         fit('candidate','Возраст 9–10 подходит; подобрать задачи по трёхлетнему опыту.'),
         fit('later','Минимум 9; младшему пока другой поток.')),
        ('inventor-laval-senior','Senior Robotics','STEMSeniorDayCamp1112yearsold','11–12 заголовок / 9–12 описание / 10–12 главный сайт',449,
         'LEGO SPIKE Prime и Minecraft; робототехника в парах. Три разных нижних возрастных границы требуют разрешения.',
         fit('conditional','9–10 попадает только в часть противоречивых правил; допуск Senior не подтверждён.'),
         fit('later','Даже самая низкая опубликованная граница 9 выше возраста Оскара.'))]
    for slug,name,tail,age,price,content,mat,osc in courses:
        url=booking+tail
        p=put(slug,'Inventor Laval · '+name,'Канада','CAN',
            'North Star Academy Laval · 950 Rue Élodie-Boucher, Laval, QC H7W 5A9',
            'robotics,coding,science,games','day',age,
            'Описания EN/FR, но язык занятий и наличие английской группы явно не обещаны.',
            content+' Темы повторяются через две недели; оператор рекомендует максимум две недели.',
            'Семь недель 28.06–13.08.2027, 09:00–16:00; реальные карточки недель прочитаны.',
            fee(2027,'CAD '+str(price)+' за неделю выбранного потока.',
                'Учебные комплекты в пользование; Junior работает индивидуально, Middle/Senior — робототехника в парах.',
                'Родители дают обед и два перекуса. Продлёнка 08:00–09:00 CAD40 / 16:00–17:00 CAD40 / обе CAD70 за неделю. Налоги и скидку sibling10% подтвердить; RL24 не гарантия льготы иностранцу.',
                '21+ дней: кредит; 10–20: кредит минус50; менее10: минус100 CAD. Возврат на способ оплаты добавляет3%; после старта нет возврата.'),
            day,mat,osc,'Разные возрастные курсы на одной площадке; полезно сравнить программу братьев и риск повторения.',
            ['EN-группа, день рождения, иностранный допуск, актуальное наполнение и окончательный счёт.'],
            [src('Возрастные уровни и 2027 прайс',iv),src('Карточка конкретного потока и смен',url),src('Работа в парах и отмена',faq)],
            status='published_2027',priority=['technical'])
        selected=weeks[:1]+weeks[2:] if slug=='inventor-laval-mechanics' else weeks
        dated(p,selected,name+' · 09:00–16:00','CAD '+str(price)+' / неделя',url,'day_camp_window')
        if slug=='inventor-laval-mechanics':
            p['timing']['label']+=' Вторая неделя: форма 6–10 июля (вт–сб), но занятия Mon–Fri; эта неделя исключена из календаря до уточнения.'
            p['timing']['unresolved_sessions']=[dict(start='2027-07-06',end='2027-07-10',
                reason='Tuesday–Saturday header contradicts Monday–Friday schedule; no corrected dates inferred.',source=url)]

    ca='https://www.canadianadventurecamp.com/dates-and-rates/'
    gen='https://www.canadianadventurecamp.com/programs/general-camp-program/'
    airport='https://www.canadianadventurecamp.com/transportation/airport-service/'
    p=put('canadventure-general','Canadian Adventure Camp · General / Adventure Island','Канада','CAN',
        'Adventure Island, Lake Temagami, Ontario; Richmond Hill в footer — офис, не лагерь',
        'general,sport,art','boarding','7–17 по заголовку программы; младшие домики 7–9',
        'Международная среда; отзывы о развитии английского не доказывают EN-инструктора каждой активности.',
        'Выбор спорта, творчества и водных активностей каждый день; младшие 7–9 также занимаются с домиком. Робототехника не заявлена.',
        '2027: четыре двухнедельных заезда, также конкретные пакеты 4/6/8 недель ниже.',
        fee(2027,'CAD 4 395/2 недели; 7 850/4; 11 025/6; 12 600/8. Налог сверх всех тарифов.',
            'Проживание, питание/перекусы, программа, инструктаж и спортивное оборудование.',
            'Транспорт отдельно; Airport Package CAD895+tax с одной ночёвкой в Торонто. Tuck CAD150 — отдельные возвратные неиспользованные карманные средства. Laundry только от4недель.',
            'Аванс возвращается до31.03.2027, остаток1апреля. Размер аванса и позднюю отмену уточнить: terms сайта не заменяют camp-contract.'),
        'Международный пансион на острове; домики обычно восемь детей и counsellor, поддержка junior/youth leader — заявление оператора.',
        fit('candidate','9–10 подходит; подтвердить язык выбранных активностей и готовность к двухнедельной разлуке.'),
        fit('conditional','Только после7-летия к началу смены; пока6 минимальный возраст не достигнут.'),
        'Общий пансион с опубликованным2027 прайсом; для иностранцев описан отдельный аэропортовый сервис.',
        ['Точная дата рождения, camp-contract, налог/трансфер, EN и правила связи. Arrival за день; обратный рейс после19:00 закрывающего воскресенья; паспорт физически у лагеря.'],
        [src('Все пакеты2027 и доплаты',ca),src('Возраст и программа',gen),
         src('Иностранные дети','https://www.canadianadventurecamp.com/international-campers/'),
         src('Аэропорт, паспорт и часы рейсов',airport),
         src('Laundry, питание и связь','https://www.canadianadventurecamp.com/faqs-prospective-families/')],
        status='published_2027',priority=['general','boarding'])
    packages=[('2027-07-05','2027-07-18',2,4395),('2027-07-19','2027-08-01',2,4395),
        ('2027-08-02','2027-08-15',2,4395),('2027-08-16','2027-08-29',2,4395),
        ('2027-07-05','2027-08-01',4,7850),('2027-08-02','2027-08-29',4,7850),
        ('2027-07-05','2027-08-15',6,11025),('2027-07-19','2027-08-29',6,11025),
        ('2027-07-05','2027-08-29',8,12600)]
    p['timing'].update(sessions=[[a,b] for a,b,n,v in packages],session_details=[dict(
        start=a,end=b,label='General · '+str(n)+' недели',price='CAD '+str(v)+' + tax; transport/tuck отдельно',
        source=ca,place=p['place'],formats=['boarding'],date_scope='camp_session') for a,b,n,v in packages])

    bs='https://www.brainstemlearning.ca/programs/winter-camp'
    bf='https://www.brainstemlearning.ca/faqs/'
    for slug,name,age,content,mat,osc,clocks in [
        ('brainstem-winter-little','Little Brains','4–6',
         'Утром VEX123 и STEM360; после обеда механика и software. Для младших два учебных блока со snack breaks.',
         fit('not_eligible','Матвей старше6; отдельная Specialists группа.'),
         fit('candidate','В декабре2026 будет5–6; подходит возраст Little Brains.'),
         [('am','09:30–12:00'),('pm','13:00–15:30'),('full','09:30–15:30')]),
        ('brainstem-winter-specialists','Specialists','7–11',
         'Утром пневматические сани, robot hockey, катапульты и магнитное движение с TinkerCAD; после обеда Gift Factory с инженерными моделями.',
         fit('candidate','В декабре2026 будет8–9; подходит возраст Specialists.'),
         fit('later','В декабре2026 будет5–6, ниже7; выбирать Little Brains.'),
         [('am','09:00–12:00'),('pm','13:00–16:00'),('full','09:00–16:00')])]:
        p=put(slug,'BrainSTEM Vancouver · Winter '+name,'Канада','CAN',
            'Marine Drive Learning Centre · 730 Marine Dr, North Vancouver, BC; unit подтвердить',
            'robotics,coding,science','day',age+'; максимум 12 участников суммарно на две возрастные группы',
            lang,content,'28–31.12.2026, четыре дня; отдельные утренний, дневной и полный варианты.',
            fee(2026,'CAD240/полдня ×4 дня; CAD528/полный день ×4 дня, GST-exempt.',
                'Четырёхдневная программа; CAD528 не равен сумме двух полудневных тарифов.',
                'Еду/напитки приносить. Optional lunch CAD48 для полного варианта; продлёнку и период этой доплаты подтвердить.',
                'В актуальном FAQ: более14дней минус15%; внутри14 только медицинское исключение. Платежи старше90дней возвращают кредитом; внизу старые формулировки отличаются.'),
            day,mat,osc,'Соседние возрастные потоки братьям на зимние каникулы; содержание и часы отличаются.',
            ['Текущие места, EN, полный счёт, адрес/unit, какой FAQ включён в договор. Оба могут прибыть09:00: младшему до09:30 свободная игра.'],
            [src('Четыре дня, темы и часы',bs),src('Отмена, кредит90дней и еда',bf)],
            status='published_2026',priority=['technical'])
        variants=[dict(start='2026-12-28',end='2026-12-31',label=name+' · '+clock,
            price='CAD '+('528' if key=='full' else '240')+' / 4дня; GST-exempt',source=bs,
            place=p['place'],formats=['day'],variant_key=key,date_scope='day_camp_window') for key,clock in clocks]
        p['timing'].update(variant_keyed=True,sessions=[[v['start'],v['end']] for v in variants],session_details=variants)

    so='https://stemotics.com/product/winter-break-camp/'
    put_sources=[src('Зимняя форма, возрастные меню и тарифные конфликты',so),
        src('Комплекты остаются у преподавателя','https://stemotics.com/faq/'),
        src('Отмена и35CAD fee','https://stemotics.com/cancellation-refund-policy/')]
    p=put('stemotics-winter','STEMOTICS Cambridge · Winter Break','Канада','CAN',
        '695 Bishop Street North, Cambridge, ON N3H 2K8','robotics,coding,science,art','day',
        '4–8 / 9–12; программу выбирают по возрасту и дню',lang,
        'Robotics: младшие WeDo/VEX GO/Indi/SPIKE Essential; старшие Prime/Arduino/EV3/VEX IQ. Coding и science — другие темы. Все перечисленные платформы за одну смену не гарантированы.',
        'Форма позволяет21–24 и28–31.12.2026; 25декабря и1января не предлагаются, хотя заголовок заканчивается01.01.2027.',
        fee(2026,'КОНФЛИКТ: week1 early149.99/regular179.99 CAD названа3днями при4днях формы; week2 early239.99 выше regular199.99 за4дня. Итог не установлен.',
            'Учебная программа; дорогие роботокомплекты остаются у преподавателя, не подарок ребёнку.',
            'Обед/перекусы приносить, nut-free. Продлёнка CAD20/20 или40CAD+HST за неделю; налог базовой цены уточнить.',
            '2+ недели: минус35CAD; внутри2:50%. Отдельная refund policy ещё вычитает35 из50%; менее3рабочихдней возврата нет. Разрешить конфликт письменно.'),
        day,fit('candidate','По возрасту подходит; в декабре2026 будет8–9, старший поток только после9-летия.'),
        fit('candidate','Возраст5–6 подходит младшему4–8; EN и конкретную тему согласовать.'),
        'Реальные зимние технические дни для обоих; сильный список оборудования требует проверки фактической программы.',
        ['Исправленный счёт week1/2, тема каждого дня, EN-инструктор, опытная группа и применимый возврат.'],
        put_sources,status='published_2026_27',priority=['technical'])
    dated(p,[['2026-12-21','2026-12-24'],['2026-12-28','2026-12-31']],
        'Зимние дни · 09:00–16:00 · тема выбирается отдельно','CAD: опубликованные тарифы противоречат; итог подтвердить',so,'day_camp_window')

    ec='https://envisionrobotics.com/stem-camps-for-kids-markham/'
    ew='https://envisionrobotics.com/product/winter-stem-camp-markham/'
    put('envision-winter-audit','Envision Robotics · Winter / конфликт действующей карточки','Канада','CAN',
        '8220 Bayview Ave, Unit10, Thornhill, ON L3T 2S2; Markham в бренде не отдельный адрес',
        'robotics,coding,games,art','day','5–8 / 9–13',lang,
        'Winter product описывает роботоподъём на рампу, Roblox/FlowLab и3D. Меню по возрасту есть, принадлежность тем зиме2026 ещё не доказана.',
        'Главная:21–24/28–31декабря2026; product:22–24/29–30 без года, picker только30декабря. Подтверждённые смены в календарь не добавляем.',
        fee(None,'Итоговая актуальная зимняя цена не установлена; летнее from200 не переносим.',
            'Состав точного зимнего пакета ещё нужен.','Питание, care, материалы и налог подтвердить.',
            'Camp Policies явно no-refund; при серьёзной травме/семейной чрезвычайной ситуации возможен кредит, не гарантированный денежный возврат.'),
        day,fit('conditional','Возраст подходит одному из потоков; год, даты, тема и места ещё расходятся.'),
        fit('conditional','Возраст подходит5–8; требуется актуальная зимняя карточка и EN.'),
        'Полезный кандидат для семейной поездки, но текущая продажа не подтверждает новый сезон.',
        ['Получить конкретную2026/27 карточку с годом, днями, тарифом, EN и правилами отмены.'],
        [src('Новый календарный анонс',ec),src('Противоречивая product-карточка и camp policies',ew)],status='partial_2026_27')

    gal='https://galileo-camps.com/our-camps/locations/irvine-1/'
    put('galileo-irvine','Camp Galileo · Irvine / Loma Ridge','США','USA',
        'Loma Ridge Elementary · 500 Tomato Springs, Irvine, CA 92618',
        'general,science,robotics,art','day','5–14 / rising K–8; потокиK–1 /2–3 /4–5 /6–8',
        lang,'Общий STEAM и outdoor; робототехнические проекты зависят от класса: Animal Bot для4–5, Remote-Control Robot для6–8 в закрытом меню.',
        'Banner Summer2027, но локальный календарь и early deadline относятся к2026, все варианты CLOSED. Новый календарь2027 не установлен.',
        fee(2026,'Архив закрытых вариантов USD480–650/нед.; K–1 500/570, grades2–5 480/550. Пакетные суммы расходятся; это не цена2027.',
            'Дневные STEAM-проекты; отдельные материалы Go-Karts100USD учтены в его650, не добавлять дважды.',
            'Архивная care:45утро/90день/110обе USD/нед.; питание и новый счёт уточнить.',
            'Скидка до28.02.2026 истекла; актуальные правила отмены и2027 enrollment нужны.'),
        day,fit('conditional','Требуется rising grade; роботAnimalBot4–5, Remote-Control6–8 младшему классу не обещается.'),
        fit('conditional','Для общего потока нужен Kindergarten/Grade1; числовой возраст не заменяет школьный класс.'),
        'Крупная сеть общего STEAM; конкретная площадка закрыта, новая рекламная шапка не доказывает даты2027.',
        ['Конкретный2027 кампус/класс, курс, EN-преподавание, текущая цена и питание.'],
        [src('Локальная карточка, закрытый календарь и цена',gal),
         src('Реальные возрастные форматы','https://galileo-camps.com/camp-galileo/')],status='partial_2027')
