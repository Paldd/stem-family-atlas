"""Concrete Asian holiday programmes with source conflicts kept explicit."""
def add_asia_programmes(add,src,fit,profiles,checked):
    def price(year,label,included,extras,deposit='Оплату и отмену выбранного сезона подтвердить.'):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def variants(p,rows):
        p['timing']['session_details']=rows
        p['timing']['sessions']=[[r['start'],r['end']] for r in rows]
    faq='https://www.campasia.asia/about-us/faqs.html'
    availability='https://www.campasia.asia/book-a-camp'
    terms='https://www.campasia.asia/about-us/terms-and-conditions.html'
    common_price=price(None,'Текущий тариф SGD 725 за 5 дней; цены 2027 не установлены.',
        'Программа, lunch, два перекуса и T-shirt; комплект курса предоставляется.',
        'Bus — опция; жильё семьи/дорога отдельно, страхование уточнить.',
        'Предоплата; опубликованные terms не предусматривают отмену/возврат. Изменение курса минимум за 10 дней при наличии мест; доплатить разницу более дорогого курса.')
    rows=[
        ('campasia-robotics','Robotics Makerspace','robotics,coding','6–8 / 9–12',
         'LEGO и VEX: конструкция, блоковый код и ежедневные задачи. Набор младших WeDo/SPIKE/VEX GO; старших SPIKE/VEX. В примерном расписании есть legacy EV3 — фактический комплект уточнить.',
         'https://www.campasia.asia/holiday-camps/tech-savvy/robotics-makerspace.html',
         fit('conditional','Общий курс 9–12 подходит, но в ближайшем октябрьском наборе этой группы нет.'),
         fit('conditional','Октябрьская группа 6–8: должно исполниться 6 к началу; точный день рождения неизвестен.')),
        ('campasia-coding','Creative Coding','coding','6–8 / 9–12',
         'Scratch/GDevelop: интерактивные истории и игры, собственный итоговый проект; ноутбук лагеря, свой приносить не требуется.',
         'https://www.campasia.asia/holiday-camps/tech-savvy/creative-coding.html',
         fit('conditional','Возраст 9–12 подходит; конкретный новый набор и язык подтвердить.'),
         fit('conditional','С 6 лет; подобрать младшую группу и язык.')),
        ('campasia-electronics','Electronic Makerspace','science,coding','6–9 на странице курса; landing 6–11 расходится',
         'Электрические цепи, LED, моторы, картонные конструкции и игровые устройства. Малые maker-проекты; состав конкретной недели уточнить.',
         'https://www.campasia.asia/holiday-camps/tech-savvy/electronic-makerspace.html',
         fit('conditional','Только до 10-летия по странице курса; расширенную границу landing не используем как разрешение.'),
         fit('conditional','6–9 соответствует после 6-летия; язык и набор подтвердить.')),
        ('campasia-stem','STEM Explorers','science,coding','9–12',
         'Смешанные инженерные, научные и программные проекты; примерное расписание перечисляет разные устройства/платформы. Их наличие в каждой неделе не гарантировано.',
         'https://www.campasia.asia/holiday-camps/multi-activity/multi-stem.html',
         fit('conditional','9–12 соответствует; проверить учебный план недели и язык.'),
         fit('later','Минимум 9 лет.')),
    ]
    for slug,name,themes,age,programme,url,mat,osc in rows:
        add(slug,'Camp Asia · '+name,'Сингапур','SGP','Singapore · кампус выбранной недели',
            themes,'day',age,
            'EN преподавания прямо не подтверждён в прочитанной программе/FAQ. Международная школа и английский сайт не заменяют подтверждение языка.',
            programme+' Пн–Пт 09–15.',
            'Общие страницы показывают баннер 19–23.10.2026. Текущий booking board подтверждает только Robotics 6–8; остальные три технических трека и Robotics 9–12 в этом наборе не перечислены. Лето 2027 не объявлено.',
            common_price.copy(),'Только дневной; Stamford / Australian International School по конкретной неделе.',mat,osc,
            'Содержательный городской технический кандидат; FAQ прямо допускает детей разных школ, стран и национальностей.',
            ['Подтвердить EN учителя, конкретный набор/возраст, полный тариф bus и оборудование; места проверять перед оплатой.'],
            [src('Конкретная программа / возраст / цена',url),src('Фактические предложения ближайшего набора',availability),src('Внешние дети / FAQ',faq),src('Условия изменения / отмены',terms)],
            status='partial_2026_27' if slug=='campasia-robotics' else 'next_unannounced',priority=['technical'])
        if slug=='campasia-robotics':
            p=profiles[-1];p['price']['year']=2026
            variants(p,[dict(start='2026-10-19',end='2026-10-23',label='Fantastic Fall · только Robotics 6–8',
                age='6–8',price='SGD 725 / 5 дней',place='Stamford American International School · Singapore',source=availability,
                formats=['day'],date_scope='day_camp_window',family_fit=dict(
                    matvey=dict(status='later',detail='Для этой смены максимум 8, Матвею 9. Общая группа 9–12 сейчас не выставлена.'),
                    oscar=dict(status='conditional',detail='Нужно 6–8 лет на начало и подтверждение языка/места.')),
                proof='В актуальном October board есть Robotics 6–8, Available; статус прочитан 04.10 и может измениться. Баннер других курсов не является их отдельным набором.')])

    family='https://www.camptaiwan.com.tw/family-camps'
    add('camp-taiwan-family','Camp Taiwan · Family Weekends','Тайвань','TWN','Wanli / New Taipei',
        'general,sport','family','Родители и дети разных возрастов; ограничения отдельных активностей уточнить',
        'Язык сопровождения именно семейного заезда не установлен. English летнего детского лагеря не переносится автоматически.',
        'Семейные outdoor-выходные. Обычный private booking: 10–17 семей, минимум 40 человек; отдельная семья не может считать каждую открытую дату собственным билетом.',
        'Индивидуальные семьи допускаются в special weekends. Октябрь 2026: текст 16–18.10, таблица 17–18.10; приезд/длительность расходятся. До уточнения не создаём точный календарный заезд. Даты 2027 не опубликованы.',
        price(2026,'Публичный полный семейный тариф в прочитанной странице не установлен.',
              'Состав питания/занятий и возрастные цены подтвердить.',
              'Трансфер, страховка и размещение по выбранному пакету.'),
        'Семейное пребывание; тип жилья и nights выбранного weekend подтвердить.',
        fit('conditional','Вместе с родителями; ограничения активностей и special booking подтвердить.'),
        fit('conditional','Вместе с родителями; это другой формат, чем летний самостоятельный лагерь 7+.'),
        'Кандидат на знакомство с camp life без самостоятельного пансиона младшего; цена, язык и дата пока требуют ответа.',
        ['Получить точные arrival/departure special weekend, EN, семейную смету, размещение и отмену.'],
        [src('Семейные / групповые правила и конфликт дат',family)],status='partial_2026_27',priority=['both','general'])

    camping='https://campingtaiwan.com/en/summer-camp'
    campingfaq='https://campingtaiwan.com/en/faq'
    add('camping-taiwan','Camping Taiwan · English Adventure','Тайвань','TWN','Восточное побережье · поезд из Taipei Songshan',
        'general,science,sport','boarding','6–15 и завершённый Grade 1; младше — только индивидуальное рассмотрение',
        'FAQ прямо подтверждает почти исключительно английский в camp life; общий adventure, без технического курса.',
        'Океан/реки, kayaking, snorkelling, экология и outdoor-практика. Оператор заявляет максимум 8 детей / 2 guides; это не независимая оценка качества.',
        '2026: летние пятидневные смены июнь–август уже прошли. Будущие зимние/летние даты 2027 в прочитанных страницах не объявлены.',
        price(2026,'Пакет 5 дней / 4 ночи: $24 000; валюту в окончательной смете подтвердить (тайваньский оператор).',
              'В FAQ registration $4 000 + tuition $20 000 составляют тот же пакет, а не дополнительные $4 000.',
              'Перелёты, страховка и точное включение поездов/оборудования подтвердить.',
              'Registration не возвращается; tuition refund 61–90 дней 90%, 31–60 70%, 8–30 50%, 0–7 без возврата. При отмене оператором из-за тайфуна — credit будущей смены; условия 2027 проверить.'),
        'Подвесные tree tents, общие outdoor-удобства, guides рядом; точное место выдаётся семьям оператором.',
        fit('conditional','Нужны завершённый Grade 1, готовность к outdoor-пансиону и новый набор.'),
        fit('conditional','Одного возраста 6–7 недостаточно: требуется уже законченный Grade 1 или письменное исключение.'),
        'Небольшой английский adventure-кандидат Тайваня; не путать с отдельным оператором Camp Taiwan.',
        ['Подтвердить новый год, валюту/включения, Grade 1, страховку, погодную замену и размещение.'],
        [src('2026 adventure / длительность / цена',camping),src('Язык / класс / проживание / отмена',campingfaq)],
        priority=['general','boarding'],confirmed=['EN'])
    profiles[-1]['language_evidence_role']='camp_life'

    winter='https://www.english-adventure.org/en/winter/'
    add('english-adventure-winter','English Adventure · Winter Holiday','Япония','JPN','Mountain Park Tsunan / Niigata',
        'general,languages,sport','boarding','Japanese Grades 1–9; младшая группа: рождение 02.04.2014–01.04.2020',
        'English Immersion: английский весь день, включая лыжи; обязательна свободная речь на EN или JA.',
        'Лыжи, игры и пансион; при недостатке снега другие активности.',
        '26–30.12.2026 (4 ночи); 03–06.01.2027 (3 ночи).',
        price(2027,'Grades 1–6: JPY 137 250 декабрь / 120 800 январь за ребёнка; не общий тариф всех возрастов.',
              'Tokyo transfer, жильё, meals, основные активности, ski lessons/lifts/helmet при катании, travel insurance и tax.',
              'Ski set +9 000, одежда +6 000; luggage shipping отдельно; Nagoya +15 000; приезжающим самим скидка 7 000.',
              'Полная оплата; отмена 20–8/7–2/1 дней: 20/30/40%, в день до check-in 50%, позже 100%. От возврата дополнительно 3,6% card fee; опции входят в базу удержаний.'),
        'Residential lodge; минимум 90 участников на смену и 4 в школьной группе, включая условие по полу.',
        fit('conditional','2017 входит в birth range; нужен соответствующий класс, fluent EN и готовность к пансиону.'),
        fit('conditional','2020 подходит только при рождении не позднее 01.04.2020; также Grade 1+. Позже этой даты текущий winter набор не подходит.'),
        'Английский зимний пансион с точной границей рождения младшего.',
        ['Подтвердить день рождения/класс, English Immersion, места и полную смету.'],
        [src('Текущий winter 2026/27: даты, birthday cutoff, цена, язык и отмена',winter)],
        status='published_2026_27',priority=['general','boarding'],confirmed=['EN'])
    p=profiles[-1];p['language_evidence_role']='camp_life';p['price']['season']='2026/27'
    variants(p,[dict(start=s,end=e,label=label,price=fee,place=p['place'],source=winter,formats=['boarding'],
        proof='Официальный сезон December2026 / January2027. Только категория Grades1–6 и birth02.04.2014–01.04.2020; English Immersion, admission/места отдельно.')
        for s,e,label,fee in [('2026-12-26','2026-12-30','English Immersion · 4 ночи / 5 дней','JPY 137 250 · Grades 1–6'),
                             ('2027-01-03','2027-01-06','English Immersion · 3 ночи / 4 дня','JPY 120 800 · Grades 1–6')]])

    hakuba='https://www.hakuba-is.jp/summer-program'
    add('hakuba-summer','Hakuba International School · Summer School','Япония','JPN','Hakuba / Nagano',
        'general,science','boarding','Школьные классы 6–9; это не возраст 6–9 лет',
        'Язык летней программы прямо не установлен; английский основной школы не доказывает язык summer course.',
        'Sustainability, science/art, systems thinking и проекты на природе. Собственный laptop рекомендуется.',
        'Заголовок Summer School 2027: details coming soon. Тело ещё 06–17.07.2026, 2 недели; вводный one-week текст расходится. Новые даты не переносим из архива.',
        price(2026,'Исторический двухнедельный пакет JPY 575 000; цены 2027 не опубликованы.',
              'Пансион, meals, linen/laundry и local medical/accident insurance по старому пакету.',
              'Дорога до Hakuba отдельно; pickup местной station по описанному пакету без доплаты.'),
        'Mont Bien / Miyama dorm; до 3 детей в комнате по описанию прошлой программы.',
        fit('later','Классы 6–9 — будущая ступень; текущий школьный класс семьи неизвестен.'),
        fit('later','Не младшая программа; классы 6–9.'),
        'Долгосрочный science/adventure-кандидат, пока исключён из текущего возрастного shortlist.',
        ['Ждать полного 2027 brochure; подтвердить класс, EN, длительность, прайс и новую отмену.'],
        [src('2027 heading / ещё старый programme body',hakuba)])

    portal='https://portal.lcclcoding.com/camps'
    lcclterms='https://www.lcclcoding.com/holidays/terms/'
    dates=[('2026-10-12','2026-10-16'),('2026-10-19','2026-10-23'),('2026-10-26','2026-10-30'),('2026-11-23','2026-11-27'),('2026-11-30','2026-12-04'),('2026-12-07','2026-12-11'),('2026-12-14','2026-12-18')]
    for slug,name,url,age,programme,mat,osc in [
        ('lccl-early','Early Creators','https://www.lcclcoding.com/holidays/early-creators/',
         '5–7 в программе/terms; портал 5–8 — верхнюю границу подтвердить',
         'Блоковый код для начинающих: последовательности, циклы, события; собственная анимация/мини-игра и презентация.',
         fit('later','В 9 лет выше обеих опубликованных границ; другой трек.'),
         fit('conditional','5–7 соответствует; прежде подтвердить EN и конкретную группу.')),
        ('lccl-fundamentals','Coding Fundamentals','https://www.lcclcoding.com/holidays/coding-fundamentals/',
         '8–11 в программе/terms; портал 7–12 — расширенный допуск не подтверждён',
         'Scratch: циклы, переменные, условия и события; 4–6 проектов и собственная игра. Опыт оценивают в первый день.',
         fit('conditional','9–10 соответствует обеим границам; уровень после трёх лет опыта согласовать.'),
         fit('conditional','2027 будет 6–7; по terms пока рано. Указание портала 7+ требует письменного допуска.')),
    ]:
        add(slug,'LCCL · '+name,'Сингапур','SGP','Singapore · 583 Orchard Road, #13-01',
            'coding','day',age,'EN технического преподавания в прочитанных страницах прямо не установлен; подтвердить учителя.',
            programme+' Пять afternoon-дней 14:30–17:30, 15 контактных часов; максимум 6 в группе — заявление оператора.',
            'Семь будущих недель Oct–Dec2026 опубликованы на странице конкретного курса. Портал показывает семь batches, но требует данные ребёнка для выбора; даты будущего лета 2027 не объявлены.',
            price(2026,'SGD 600 regular / 570 при записи минимум за 14 дней; скидка не означает текущую цену любого набора.',
                  'Материалы/software и laptops; GST по условиям.',
                  'Питание и уход вне учебных часов не заявлены; жильё семьи/дорога отдельно.',
                  'Полная оплата; cash refund нет, перенос только внутри того же Sep2026–Jan2027 сезона при наличии мест.'),
            'Короткий дневной курс, ночёвок и ухода вне учебных часов не заявлено.',mat,osc,
            'Разные возрастные треки братьев идут одновременно; язык, места и спорные возрастные границы ещё согласовать.',
            ['Подтвердить EN и age range, конкретную неделю, уровень, итоговую скидку и правила переноса.'],
            [src('Конкретный курс / published batches',url),src('Terms 2026/27 / возраст / pricing',lcclterms),src('Портал: другие age ranges · без ввода данных детей',portal)],
            status='partial_2026_27',priority=['technical'])
        p=profiles[-1]
        variants(p,[dict(start=s,end=e,label=name+' · 14:30–17:30',price='SGD 600 regular / 570 при записи за 14+ дней',place=p['place'],source=url,
            formats=['day'],date_scope='day_camp_window',proof='Даты перечислены на странице данного курса, не выведены из общего seasonal window. Места, EN и расширенная граница портала не подтверждены.') for s,e in dates])

    # Existing IDs stay stable; summer and family formats are now separate dossiers.
    taiwan=next(p for p in profiles if p['slug']=='camp-taiwan')
    taiwan['formats']=['boarding']
    taiwan['language']='FAQ прямо подтверждает English для инструкций, общения, песен и активностей летнего residential camp; Mandarin-speaking counsellor помогает каждой команде. Это общий outdoor, не уроки языка/robotics.'
    taiwan['language_evidence_role']='camp_life'
    taiwan['accommodation']='Safari tents на деревянной платформе, электричество и кровати; обычно 4–6 детей, общий bath-house. Counselors рядом; собственная подушка. По FAQ братья не могут выбрать друг друга tentmate.'
    taiwan['questions']=['Получить 2027 dates/price, возраст Оскара 7+ на начало, полный пакет и возврат; не рассчитывать на совместную палатку братьев. Семейные weekends — отдельное досье.']
    taiwan['price']['label']='2026: Youth 7–12 NT$23 000 / 6 дней 5 ночей; 2–5 детей NT$22 000 каждый. Teen13–16 NT$25 000. Новый прайс 2027 не опубликован.'
    taiwan['price']['deposit']='На летней странице есть notice о невозвратных fee; точную разбивку и актуальные условия 2027 получить отдельно.'
    for title,url in [('Summer: возраст / price / старые смены','https://www.camptaiwan.com.tw/summer-camp'),('FAQ: English / палатки / братья','https://www.camptaiwan.com.tw/faq')]:
        if not any(s['url']==url for s in taiwan['sources']):taiwan['sources'].append(dict(title=title,url=url,checked=checked))
    sfs=next(p for p in profiles if p['slug']=='camp-sfs')
    sfs['questions']=['Получить summer2027 и grade conversion. Eligibility делит Elementary acceptance75%/25% по школьной/языковой категории; это не личная вероятность приёма и не гарантия места внешней семье. Обязательно EN video interview.']
    sfs['language_evidence_role']='camp_life'
