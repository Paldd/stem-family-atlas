"""Europe: programme-specific seasons and prices; no inferred enrolment or ranking."""
CHECKED='2026-10-05'
MONT='https://www.montana-zug.ch/en/summer-camp'
MONTPDF='https://www.montana-zug.ch/hubfs/Summer%20Camp%20Presentation%202026.pdf'
EC='https://www.ecolint-camps.ch/en'
ECABOUT='https://www.ecolint-camps.ch/en/our-camps'
ECTERMS='https://www.ecolint-camps.ch/sites/camps/files/assets/10-general/cgv-camps.pdf'
SG='https://www.stgeorges.ch/camps/winter-camp'
SGOLD='https://www.stgeorges.ch/sites/school76/files/2023-05/St-Georges-Summer-Camp-TCs-002.pdf'
LPB='https://www.lespetitsbilingues.com/les-centres-les-petits-bilingues/issy-mairie/'
LPBCAL='https://www.lespetitsbilingues.com/wp-content/uploads/2026/09/Calendrier-IDF-Organisation-stages-vacances-2026-2027-v300926-Google-Sheets.pdf'
LPBTERMS='https://www.lespetitsbilingues.com/conditions-generales-de-ventes/'
SA='https://www.samiad.com/programmes/multi-activity/'
SAT='https://www.samiad.com/terms-and-conditions/'
SAFAQ='https://www.samiad.com/faqs/'
FUN='https://funtech.co.uk/camps/dates'
FUNFAQ='https://funtech.co.uk/faqs'
FUNT='https://funtech.co.uk/terms/holiday-camps'
FUNBOARD='https://funtech.co.uk/residential-kids-coding-camps'
MAD='https://ajedrezblancoynegro.com/event/campamento-de-verano-piscina-2027/'
MANGA='https://ajedrezblancoynegro.com/campamento-comic-manga-anime-madrid-2027/'

def add_europe_v78(add,src,fit,profiles):
    def fee(year,label,included,extras,deposit):return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def put(*a,**kw):
        add(*a,**kw);p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        return p
    def dates(p,rows,url,scope='camp_session'):
        p['timing']['sessions']=[[a,b] for a,b,label,cost in rows]
        p['timing']['session_details']=[dict(start=a,end=b,label=label,price=cost,source=url,
            formats=p['formats'],place=p['place'],date_scope=scope) for a,b,label,cost in rows]
    def refresh(p):
        p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
    mat=fit('candidate','Возраст соответствует; зачисление, уровень и место отдельно.')
    en_unknown='Язык конкретных занятий EN/ES/RU не доказан; английская страница сама по себе его не устанавливает.'

    p=next(p for p in profiles if p['slug']=='montana-zug')
    p.update(place='Zugerberg · Schönfels 5, 6300 Zug',
        language='Есть EN или German language track от beginner до advanced. Язык технологических workshops уточнить отдельно.',
        confirmed_instruction_languages=['EN'],language_evidence_role='language_lessons',
        programme='Языковые занятия, проекты о мире/будущем/себе, творчество, спорт и предпринимательство. В PDF встречаются разные схемы языковых часов: точный трек согласовать. Название Tech Innovation не доказывает отдельный robotics-intensive.',
        accommodation='Дневной или пансион; в PDF двухместные комнаты по возрасту/полу и house parents. Минимум две недели.',
        price=fee(2027,'2 недели: день CHF 4 800 / пансион 6 500; 3 недели: день 6 700 / пансион 8 900.',
            'В таблице PDF прямо включён транспорт в аэропорт и обратно; аэропорт, часы и применимость к day-пакету уточнить.',
            'Перелёт, страхование, карманные расходы, семья и дополнительные занятия требуют полной сметы.',
            'CHF 1 000 дополнительный возвратный депозит, не аванс в счёт цены. На странице возврат в сентябре по cancellation policy; сам действующий договор ещё нужен.'),
        questions=['Подтвердить точные day-дни/часы, технический курс и язык, оба трансфера, all-in и действующие условия отмены/депозита.'],
        sources=[dict(title=t,url=u,checked=CHECKED) for t,u in [
            ('2027 и опубликованные варианты 2/3 недели в публичной форме',MONT),
            ('PDF: filename 2026, но факты/прайс внутри 2027; таблица визуально проверена',MONTPDF)]])
    p['timing']=dict(status='published_2027',label='Публичная форма: только недели 1+2 (04–17.07.2027) либо 1+2+3 (04–24.07). Минимум две недели; произвольные недельные старты не заявлены.',sessions=[])
    dates(p,[('2027-07-04','2027-07-17','2 недели · day/boarding','CHF 4 800 / 6 500'),
             ('2027-07-04','2027-07-24','3 недели · day/boarding','CHF 6 700 / 8 900')],MONT)
    refresh(p)

    ecprice=fee(2026,'CHF 640/полная неделя; half-day CHF 370 с обедом.',
        'По договору April 2026: обед/перекусы, обучение, материалы и camp-трансферы. Это не трансфер из аэропорта или отель семьи.',
        'Семейное жильё/дорога отдельно; иностранным детям нужны Swiss health/accident и liability insurance. После 17:30 штраф CHF 50.',
        'Оплата при регистрации; booking final. При болезни/травме с медсправкой credit на год, не обычный cash refund. Отмена оператором за 3 дня из-за недобора — полный refund; французский договор имеет приоритет.')
    for slug,name,age,content,url,m,o,half in [
        ('ecolint-intro-robotics','Ecolint · Introduction to Robotics','Booking 5–7; описание 5–6 — разные границы',
         'Простые роботы, начальное coding и образовательные игры. Тип набора/объём программирования не раскрыт; трёхлетнему участнику соревнований может быть слишком просто.',
         'https://www.ecolint-camps.ch/en/camps/introduction-robotics-10?v=5416',
         fit('not_eligible','2017: старше обеих младших границ 5–6/5–7.'),fit('conditional','В октябре 2026 ребёнку 2020 года 5–6, подходит обеим таблицам; уровень после прежнего опыта отдельно.'),False),
        ('ecolint-science','Ecolint · Science','7–11',
         'Эксперименты, постановка вопросов и поиск решений, плюс outdoor. Перечень конкретных опытов/оборудования и часы научной работы не раскрыты.',
         'https://www.ecolint-camps.ch/en/camps/science-15?v=5431',mat,fit('later','В октябре 2026 ребёнок 2020 года ещё младше 7.'),False),
        ('ecolint-film','Ecolint · Film Making & Photo','9–13',
         'Фотография и создание видео на телефоне. Уточнить, чей телефон нужен, какие программы и что остаётся в портфолио; общий договор советует не приносить devices без необходимости.',
         'https://www.ecolint-camps.ch/en/camps/film-making-photo-13?v=5407',
         fit('conditional','На 19.10.2026 Матвею может быть 8 или 9; только после 9-летия.'),fit('later','Минимум 9; Оскару пока рано.'),False),
        ('ecolint-multiactivity-half','Ecolint · Multi-Activity / полдня','5–6',
         'Творчество, игры, танцы, спорт и знакомство с наукой; развитие общения/самостоятельности. Это общий half-day, не отдельный engineering camp.',
         'https://www.ecolint-camps.ch/en/camps/multi-activity-half-day-31?v=5437',
         fit('not_eligible','Матвей старше младшей группы 5–6.'),fit('candidate','Октябрь 2026:5–6 по году рождения 2020 соответствует.'),True)]:
        nations=slug in ['ecolint-science','ecolint-multiactivity-half']
        place='Campus des Nations ·11 route des Morillons, Grand-Saconnex' if nations else 'La Grande Boissière ·7 rue Marie-Thérèse-Maurette, Genève'
        p=put(slug,name,'Швейцария','CHE',place,
            'robotics,coding' if 'robotics' in slug else 'technology,art' if 'film' in slug else 'general,science,art' if half else 'science',
            'day',age,'Оператор прямо заявляет bilingual EN/FR camps и общение на предпочитаемом языке; это не гарантия English-only каждого ведущего.',
            content,'19–23.10.2026. Camp-page: deadline 16.10, 15:00, а общая страница говорит Thursday before; конкретный крайний срок согласовать. Дат 2027 ещё нет.',
            dict(ecprice,label='CHF 370/5 полудней с обедом' if half else 'CHF 640/5 полных дней'),
            '09–13 с обедом; родитель забирает после полдня.' if half else '09–17; early arrival 08–08:55 и supervision до 17:30; жильё семьи отдельно.',m,o,
            'Конкретная школьная программа с EN/FR, прайсом и договором; репутация школы не независимый рейтинг лагеря.',
            ['Уточнить точный instructor/уровень, актуальные места и дедлайн, иностранный приём, материалы и полный семейный бюджет.'],
            [src('Именно осенний поток 2026',url),src('EN/FR и адреса кампусов',EC),src('Расписание и общий дедлайн',ECABOUT),src('Договор April 2026',ECTERMS)],
            status='published_2026_27',confirmed=['EN','FR'],priority=['technical'] if 'robotics' in slug or 'science' in slug else ['general'])
        p['language_evidence_role']='bilingual'
        dates(p,[('2026-10-19','2026-10-23','Осень ·5 дней','CHF 370' if half else 'CHF 640')],url,'day_camp_window')

    for slug,name,age,cost,m in [
        ('stgeorge-winter-day','St George’s Montreux · Winter / день','8–16','CHF 1 790',mat),
        ('stgeorge-winter-board','St George’s Montreux · Winter / пансион','10–16','CHF 3 490',
         fit('conditional','Только после 10-летия к 13.02.2027; по 2017 году рождения это ещё не установлено.'))]:
        p=put(slug,name,'Швейцария','CHE','Montreux · St George’s campus; ski resorts по погоде','general,sport',
            'boarding' if slug.endswith('board') else 'day',age,en_unknown,
            'Шесть дней лыж 14–19 февраля, от beginner до advanced, snowboarding/развлечения и mountain activities. Не робототехника. Оператор допускает детей из школ по всему миру.',
            '13–20.02.2027: arrival 13 февраля 09–11; departure 20 февраля утром. День: фактические часы/посещения уточнить.',
            fee(2027,cost+' / опубликованный недельный пакет',
                'Программа, rental/pass, coaches и 3 приёма пищи; пансион/24 hcare только boarding.',
                'Departure airport transfer CHF 200; arrival transfer/early 12 февраля по запросу, цена неизвестна. Inspired 10% только своим ученикам.',
                'Действующие deposit/cancellation неизвестны: ссылка Terms ведёт на SUMMER 2023, не Winter 2027. Старые CHF 300 и refund-пороги не переносим.'),
            'Школьный пансион с 24 hstaff.' if slug.endswith('board') else 'Дневной; отдельное жильё семьи и ежедневная дорога.',m,
            fit('later','Оскар 2020 года не достигнет 8 лет кфевралю 2027.'),
            'Кандидат на зимнюю спортивную поездку Матвея; оба брата в эту программу 2027 вместе не проходят.',
            ['Подтвердить возраст на 13.02, язык инструктора, day-дни/часы, arrival-transfer, полный счёт и Winter 2027 договор.'],
            [src('Точные Winter 2027 условия',SG),src('Прикреплённые Terms фактически Summer 2023',SGOLD)],status='published_2027',priority=['general'])
        dates(p,[('2027-02-13','2027-02-20','Зима 2027',cost)],SG)

    for slug,name,age,poster,content,m,o in [
        ('lpb-issy-movers','Les Petits Bilingues Issy · Movers','3–6',
         'https://www.lespetitsbilingues.com/wp-content/uploads/2026/09/POSTER-Stage-Movers-October-2026-Four-Days.pdf',
         'Осенью: английские игры о сезонах, персонажах Halloween, еде/эмоциях, одежде и частях тела; поделки. Poster даёт 4 дня, календарь октября 5 полудней; пятый учебный блок не раскрыт.',
         fit('not_eligible','Матвей старше Movers 3–6.'),fit('conditional','2026:5–6 подходит; после 7-летия 2027 нужен Juniors.')),
        ('lpb-issy-juniors','Les Petits Bilingues Issy · Juniors','7–10',
         'https://www.lespetitsbilingues.com/wp-content/uploads/2026/09/POSTER-Stage-Juniors-October-2026-Four-Days.pdf',
         'Осенью сюжетный mystery: английское чтение/вопросы, путешествия, описания и творчество. Нет робототехнического курса. Poster 4 дня против календаря 5 полудней; программа ориентировочная.',
         mat,fit('later','В опубликованных сменах октября/декабря 2026 Оскару 5–6, нужен Movers. Juniors только после 7-летия; дат 2027 ещё нет.'))]:
        p=put(slug,name,'Франция','FRA','Issy-les-Moulineaux ·57 bis boulevard Gallieni,92130',
            'general,languages,art','day',age,'Страница прямо: тематические каникулы 100%на английском. Это языковое погружение; для свободно говорящих детей проверить нужную сложность.',
            content,'PDF календарь: 19–23/26–30 октября 2026 AM или PM; 21–24/28–31 декабря только AM. Это опубликованные реальные периоды 2026; лето/зима 2027 не объявлены.',
            fee(2026,'PDF: октябрь EUR 259/5×3 ч; декабрь 199/4×3 ч. Страница: 199/4 дня. Pack 3: PDF 699 до 31.07.2027; страница 549 до 30.04.2027 — конфликт.',
                'Выбранный полудневный ENworkshop; цены TTC по календарю.',
                'AM 09–12 /PM 14–17; lunchbox свой. Optional 12:30–14 по 15 EUR/день. Октябрь 259+5×15=334; декабрь 199+4×15=259 — наш расчёт, не all-in quote.',
                'В CGV оплата полностью при регистрации; обычная отмена родителем без refund, исключения force majeure/legitimate reason. Оператор может отменить stage за 72 ч при<5 детей; нужен договор именно центра и точный прайс.'),
            'Полдня без ночёвок; AM+PM не обещаны как один пакет. Для полной дневной смены и паузы 12–12:30 уточнить присмотр.',m,o,
            'EN вариант под семейную базу Paris/Issy; полезность для уже англоязычных детей зависит от уровня, независимый top-рейтинг не установлен.',
            ['Устранить конфликт страницы/PDF: цена, 4/5 дней, packexpiry; подобрать уровень, текущие места, full-day и питание.'],
            [src('Центр/EN/страничный прайс, проверен native',LPB),src('Датированный календарь 26/27',LPBCAL),src('Возрастной учебный план October 2026',poster),src('CGV, применимость центру подтвердить',LPBTERMS)],
            status='published_2026_27',confirmed=['EN'],priority=['general'])
        p['language_evidence_role']='primary'
        dates(p,[(a,b,label,cost) for a,b,label,cost in [
            ('2026-10-19','2026-10-23','5 полудней ·AM или PM','EUR 259 по PDF; настранице 199/4 дня'),
            ('2026-10-26','2026-10-30','5 полудней ·AM или PM','EUR 259 по PDF; настранице 199/4 дня'),
            ('2026-12-21','2026-12-24','4 полудня ·AM','EUR199'),
            ('2026-12-28','2026-12-31','4 полудня ·AM','EUR199')]],LPBCAL,'day_camp_window')

    p=put('samiad-multiactivity','Samiad · International Multi Activity /6 campuses','Великобритания','GBR',
        'RGS Surrey Hills /Oratory /Trent /Marlborough /Bromsgrove /The Leys','general,languages,sport,art','boarding','6–18',
        '15часов английского в неделю. Оператор прямо подтверждает английский как основной язык общения и приём международных детей.',
        'Английский пансион со спортом и творчеством; две экскурсии в неделю, одна с ночёвкой. Курс Robotics указан в меню, но его ссылка недоступна: новый учебный план2027 не подтверждён. Основная программа — общий отдых.',
        'Цены2027 за14ночей опубликованы. По кампусам указаны окна сезона; конкретный двухнедельный заезд ещё нужно согласовать. FAQ говорит о приезде по воскресеньям, но два окна начинаются во вторник/среду: точные смены пока не рассчитаны.',
        fee(2027,'14 ночей: Trent GBP 3 550; Oratory/Marlborough 3 650; Bromsgrove 3 750; RGS 3 850; Leys 4 000.',
            'Проживание, питание,15часов английского в неделю, активности, экскурсии и круглосуточное сопровождение. Пакет выбранного кампуса уточнить.',
            'Airport transfers отдельно; страховка по terms 10 GBP/нед., FAQ советует pocketmoney 50/нед. В campus-pages старые 3 500/3 600 против programme 3 650/3 850; новый счёт нужен.',
            'Страница договора действует с22.02.2024:50%аванс, остаток за8недель. Удержание при отмене:61+день GBP150;31–60дней400;15–30дней половина;0–14дней вся цена. Применимость к2027 и условия отказа в визе уточнить.'),
        'Школьный пансион; RGS/Oratory предлагают отдельные, двухместные и общие комнаты. Братьям не гарантирована одна комната из-за возрастных групп.',
        mat,fit('conditional','2027:6–7 соответствует 6+; самостоятельность младшего и место в возрастной группе отдельно.'),
        'Общий английский пансион для обоих с опубликованными пакетами; школа-площадка не обещает поступление или международные медали.',
        ['Выбрать campus/14 ночей, устранить старые campus-prices, получить transfer/all-in/2027 договор и младший приём.'],
        [src('MultiActivity 2027 по кампусам',SA),src('ENcommunication','https://www.samiad.com/'),src('Быт/иностранные дети',SAFAQ),src('Действующая страница договора 2024',SAT),
         src('RGS: возраст/rooms/старый прайс','https://www.samiad.com/rgs-surrey-hills/'),src('Oratory: возраст/rooms/старый прайс','https://www.samiad.com/the-oratory-school/')],
        status='partial_2027',confirmed=['EN'],priority=['both','general','boarding'])
    p['language_evidence_role']='camp_life'
    dates(p,[('2027-07-04','2027-08-22','RGS Surrey Hills ·14 ночей','GBP3 850'),
        ('2027-07-04','2027-08-01','Oratory ·14 ночей','GBP3 650'),('2027-07-04','2027-08-22','Trent ·14 ночей','GBP3 550'),
        ('2027-07-04','2027-08-01','Marlborough ·14 ночей','GBP3 650'),('2027-07-06','2027-08-03','Bromsgrove ·14 ночей','GBP3 750'),
        ('2027-07-07','2027-08-04','The Leys ·14 ночей','GBP4 000')],SA)
    p['timing'].update(precision='season_window',variant_keyed=True)
    for v,k in zip(p['timing']['session_details'],['rgs','oratory','trent','marlborough','bromsgrove','leys']):
        v['variant_key']=k;v['place']=v['label'].split(' ·')[0]
        v['label']=v['place']+' · окно сезона / пакет14ночей'

    funterms='Full-fee/EarlyBird: аванс невозвратен; 40+дней fee минус аванс, 31–39 половина минус аванс, ≤30 без refund. FlashSale невозвратен; swap до 2 нед. Minimumage на старте: day 7, board 8. Уточнить новый договор 2027.'
    for slug,name,age,content,url,m,o in [
        ('funtech-mod-day','FunTech · Minecraft Mod Developer / день','7–10',
         'MCreator: собственные блоки/предметы, события, поведения существ, рецепты, миры и итоговый modpack. Это игровые программные проекты, не сборка физического робота.',
         'https://funtech.co.uk/camp_types/v2/minecraft-with-mods',mat,fit('conditional','Только после 7-летия на старте 2027; в 6 лет не допускают.')),
        ('funtech-redstone-day','FunTech · Minecraft Redstone Engineer / день','9–12; нужны знания Minecraft',
         'Логические элементы, повторители, сравнение, память и цифровые схемы внутри Minecraft; итоговая adventuremap. Виртуальная электроника, физических компонентов нет.',
         'https://funtech.co.uk/camp_types/view/minecraft-redstone',fit('conditional','В 2027 возраст 9–10 подходит; нужны начальные знания Minecraft.'),fit('later','Минимум 9; младшему рано.'))]:
        p=put(slug,name,'Великобритания','GBR','UK · филиал 2027 пока не выбран',
            'coding,games,technology','day',age,en_unknown,
            content+' Заявлено 30 ч учебного курса за 5 дней; FridayShow&Tell 16:00.',
            'Оператор: in-person возвращается July 2027; конкретные смены/кампусы 2027 не опубликованы. Не приписываем датам общую февральскую дату открытия без года.',
            fee(None,'Текущий Standard GBP 695/5 дней с VAT по FAQ; год этой цены не указан, не подтверждён как 2027.',
                'Дневное обучение; собственный laptop или аренда. Ночёвки/питание не входят.',
                'Аренда 70/нед., установка на месте 55; early и late по 30/нед. каждое. 695+70+30+30=825 GBP — наш расчёт текущих тарифов, не оферта 2027. Lunch/snacks свои.',
                funterms),
            '09–17 Пн–Пт; 08:30/17:30 за доплату. Нужен совместимый Windows/Mac 8 GB/OpenGL 4.4; iPad/Chromebook не подходит. Конкретную спецификацию 2027 подтвердить.',m,o,
            'Практичный кандидат на игровой coding/electronics проект для портфолио; «98%recommend» не независимое место в рейтинге.',
            ['Подобрать конкретный 2027 campus/date/уровень, подтвердить EN, newprice/компьютер/лицензии и полный счёт.'],
            [src('Подробный дневной курс/техника',url),src('Статус July 2027',FUN),src('FAQ: VAT/оборудование/часы',FUNFAQ),src('Camp-specificterms',FUNT)],priority=['technical'])
    p=put('funtech-tonbridge-board','FunTech · Tonbridge coding / пансион','Великобритания','GBR','Tonbridge School · Kent',
        'coding,games,technology','boarding','8–16 по актуальным Terms; oldmodal 8–18 не используется',en_unknown,
        'Недельный coding/coursechoice и eveningactivities; компьютеры предоставляют в пансионе. Выбранный курс/сложность не установлен; весь каталог курсов не гарантируется каждому возрасту.',
        'Residentialpage ещё August 2026, в старом modal таблица 2020. Новых точных 2027 дат/price нет; общий July 2027 баннер day не доказывает boarding.',
        fee(None,'Новый пансионный 2027 прайс не опубликован в прочитанных страницах.',
            'Пансион, 3 meal/день, 24 hcare и компьютеры по описанию оператора.',
            'Airporttransfer отдельно: текущая таблица Heathrow/Gatwick 345 one-way/650 returnGBP; год не подтверждён, не новый 2027 счёт.',funterms),
        'Single/dorm, sharedbathroom; Sunday–Friday. В страницах разные check-in/out часы — welcome-pack выбранной смены нужен.',
        mat,fit('later','К лету 2027 Оскару 6–7, пансион только 8+.'),
        'Технический пансион Матвея на среднесрочный отбор; за 2027 пока доступность не доказана.',
        ['Проверить новый пансион 2027, курс как пример Redstone/Mod, EN, возраст, даты, компьютер, полный счёт/трансферы.'],
        [src('Residential: быт/архивные даты',FUNBOARD),src('Текущий FAQ',FUNFAQ),src('Актуальный agegate 8–16/terms',FUNT)],priority=['technical','boarding'])

    p=next(p for p in profiles if p['slug']=='madrid-chess-robotics')
    p['language']='Страница организатора 2027 прямо: все активности на испанском; принимают детей, приезжающих из других стран. EN сайт — справка для родителей, не English-medium.'
    p['confirmed_instruction_languages']=['ES'];p['language_evidence_role']='primary'
    p['price']['label']='Индивидуальная смета 2027 ещё не готова. Страница приблизительно EUR 300/2 недели утром без еды или 400 с обедом/длинным днём для clubmembers; не универсальная цена.'
    p['timing']['label']='Event 2027:21.06–30.07; текст этой же страницы 22.06–31.07(weekday не 2027). Главная просит ждать Feb 2027, event до March: конфликт дат, сезонное окно не превращаем в точные смены.'
    p['questions']=['Согласовать конфликт 21/22 июня и 30/31 июля, кампус/часы/уровень, испанскую robotics группу и индивидуальную 2027 смету/отмену.']
    p['sources'].append(dict(title='2027 event: ES и foreign приём, противоречивые даты/примерные цены',url=MAD,checked=CHECKED))
    refresh(p)
    p=put('madrid-manga','Blanco y Negro · Manga/Anime Workshop 2027','Испания','ESP','Madrid ·CiudadUniversitaria; кампус 2027 согласовать',
        'art,general','day','С 1ºPrimaria; особый интерес 8–14, пределы общего лагеря 5–16 не тождественны курсным',
        'Организатор заявляет все активности 2027 на испанском; внешние/приезжающие из других стран дети описаны.',
        'Создание персонажей/эскизов, сценария, панелей, линий, цвета и обложки. Нужные арт материалы включены; Ассоциация Fábula. Общий camp имеет параллельные chess/robotics: не обещаем одновременно оба workshops.',
        'Лето 2027 объявлено, но точные дни/2027 календарь спорны; примерный урок 10–12:15, потом pool. Отдельных точных смен не публикуем.',
        fee(None,'Новый прайс выбранного manga пакета 2027 не подтверждён.',
            'Все drawingmaterials включены в workshop.',
            'Более общий день/еда/earlylate, жильё и транспорт семьи отдельно; приблизительные clubmembers 300/400 EUR не полный счёт.',
            'Индивидуальный 2027 contract/refund ещё нужен.'),
        'Дневной workshop; университетские резиденции как площадки не означают ночёвки.',
        fit('conditional','Возраст 8–10 интересующей группы; реальный класс 1ºPrimaria+ и место подтвердить.'),
        fit('conditional','Только если 1ºPrimaria+; год рождения не устанавливает класс, рисовательную готовность уточнить.'),
        'Творческий проект 2027 для портфолио на испанском, можно сочетать с поездкой/другими днями robotics; не инженерная лига.',
        ['Класс/уровень, точный 2027 день/кампус, какие времена workshops совместимы, полный прайс/договор.'],
        [src('Конкретный manga учебный план 2027',MANGA),src('General 2027: ES/foreignaccess/спорные даты',MAD),src('Flexibledays/архив мест','https://www.campamentodeajedrez.com/')],
        status='partial_2027',confirmed=['ES'],priority=['general'])
    p['language_evidence_role']='primary';p['timing'].update(precision='season_window',sessions=[['2027-06-21','2027-07-30']])

def extend_report_v78(report):
    report['shortlist'].extend([
        dict(label='Женева · каникулы обоих братьев в октябре',slugs=['ecolint-intro-robotics','ecolint-science','ecolint-film','ecolint-multiactivity-half'],
            reason='19–23 октября 2026. Оскару 5–6: начальная робототехника за CHF640 или общий полдень за370. Матвею 8–9: Science7–11; фото/видео9+ только после девятилетия. Английский/французский подтверждены. Наука и робототехника проходят в разных кампусах; продумать доставку и время получения детей.'),
        dict(label='Zug · языки и проекты Матвею летом2027',slugs=['montana-zug','camp-suisse-day','tasis'],
            reason='Institut Montana:04–17 или04–24 июля, минимум две недели. Две недели день/пансион CHF4800/6500; три недели6700/8900, дополнительно возвратный депозит1000. Минимум8лет: Оскару рано. Для совместной поездки сравнить Camp Suisse Day и TASIS. Часы технических занятий Montana ещё требуют уточнения.'),
        dict(label='Швейцария · зимний спорт Матвею',slugs=['stgeorge-winter-day','stgeorge-winter-board','les-elfes'],
            reason='St George’s13–20 февраля2027: день CHF1790 с8лет, пансион3490 с10. Матвей в пансион только после десятилетия; Оскару этот лагерь рано. Английский инструктор и договор зимы2027 ещё не подтверждены. Для обоих рассмотреть отдельную возрастную программу Les Elfes.'),
        dict(label='Франция · английские тематические каникулы',slugs=['lpb-issy-movers','lpb-issy-juniors'],
            reason='Issy:100%английский, Movers3–6 для Оскара и Juniors7–10 для Матвея. В PDF октябрьские5полудней стоят EUR259, декабрьские4 —199. Страничный прайс и пакетные условия расходятся с PDF. Для уже говорящих по-английски детей сначала проверить сложность; это язык и творчество, без отдельной робототехники.'),
        dict(label='Великобритания · английский пансион и игровая инженерия',slugs=['samiad-multiactivity','funtech-mod-day','funtech-redstone-day','funtech-tonbridge-board'],
            reason='Samiad с6лет: английский пансион,14ночей GBP3550–4000 на6площадках; пока известны сезонные окна. FunTech Mod7–10 и Redstone9–12 дают программный проект; дневной тариф695 без подтверждённого года. Оскар Mod только после7лет, Матвею Redstone при опыте Minecraft. Пансион FunTech с8лет, новый сезон ещё нужен.'),
        dict(label='Мадрид · робототехника и творчество на испанском',slugs=['madrid-chess-robotics','madrid-manga'],
            reason='Организатор прямо подтверждает испанский всех активностей и приём приезжающих детей. Робототехника, manga и шахматы идут параллельно: выбрать разные дни для разных мастерских. Manga с1ºPrimaria. Точные смены/кампусы/прайсы2027 ждут обновления; расхождения дат отмечены в досье.')
    ])
    report['gaps'].extend([
        dict(country='Швейцария',iso='CHE',provider='v78: возраст, договор и техническая глубина',
            detail='Institut Montana: filename PDF2026, содержание и таблица2027; визуально сверены цены, в публичной форме только04–17/24июля. CHF1000 дополнительно, не аванс. Ecolint: booking5–7 против описания5–6, английский/французский подтверждены; конкретный дедлайн16октября15:00 расходится с общим Thursday before. St George’s Winter2027 ссылается на договор Summer2023; его аванс/отмену не переносим.',
            next_action='Точный язык ведущего, часы, возраст на начало, оба трансфера, новый договор и полный счёт до заявки. Полностью проверенных стран пока0.',url=SG),
        dict(country='Франция',iso='FRA',provider='v78: длительность и стоимость Les Petits Bilingues',
            detail='Native-страница Issy: EUR199/4дня, пакет549 до30апреля2027. Её календарь: октябрь259/5полудней, пакет699 до31июля2027; декабрь199/4полудня. Октябрьский учебный poster описывает4дня, пятый блок не раскрыт. Эти смены относятся к2026. Условия отмены и точный прайс подтвердить конкретному центру.',
            next_action='Устранить4/5дней, пакетный прайс и срок; подобрать сложность детям, новый сезон2027 и полный дневной пакет.',url=LPB),
        dict(country='Великобритания',iso='GBR',provider='v78: будущий сезон и старые страницы',
            detail='Samiad Robotics в меню ведёт на404. Multi Activity2027 — общий английский лагерь; старые campus3500/3600 расходятся с новым3650/3850. Правило Sunday arrival не объясняет Tuesday/Wednesday у двух площадок. FunTech: деньJuly2027 без смен, тариф695 без года; пансионAugust2026/таблица2020 не2027. Bede: баннер2027 против detail2026 и разных цен — новый сезон не подтверждён.',
            next_action='Новые программы/даты2027, конкретные14ночей Samiad, полный прайс, английский технического курса и договор; проверить Bede2027 prospectus.',url=FUN),
        dict(country='Испания',iso='ESP',provider='v78: Blanco y Negro2027',
            detail='Все активности на испанском и приезжающие дети подтверждены оператором. Manga с1ºPrimaria+, материалы включены; год рождения не доказывает класс. Event21июня–30июля2027 против текста22июня–31июля, обновлениеFebruary/March. Примерные EUR300/400 для club members и общего лагеря не универсальная цена robotics/manga.',
            next_action='Новый календарь и договор, возрастные уровни, сочетание параллельных мастерских и индивидуальный счёт. Продолжать остальные страны Европы, Азии и Америки.',url=MAD)
    ])
