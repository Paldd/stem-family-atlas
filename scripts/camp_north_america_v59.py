"""North American programmes, with public tariffs and admission gates kept separate."""
def add_north_american_programmes(add,src,fit,profiles,checked):
    def price(year,label,included,extras,deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def variants(p,rows):
        p['timing']['session_details']=rows
        p['timing']['sessions']=[[r['start'],r['end']] for r in rows]
    unconfirmed='EN преподавания/лагерной жизни прямо не установлен в прочитанных источниках; подтвердить у оператора.'
    brick='https://bricklabs.ca/over-night-camp-2026/'
    for slug,name,themes,programme,july,august in [
        ('bricklabs-robotics','Robotics','robotics,coding',
         'Intermediate/advanced LEGO: строить и программировать rescue-роботов в июле, решать ежедневные Challenge Series в августе. FLL-type задачи — учебные, не отборочный тур FLL.',
         'Natural Disaster Response','Challenge Series'),
        ('bricklabs-creative','Creative Builders','general,science',
         'Творческое конструирование: Inspired by Muskoka в июле, Macro Scale Characters в августе; outdoor-активности. Программирование роботов в этом треке не заявлено.',
         'Display Builder · Inspired by Muskoka','Macro Scale Characters')]:
        add(slug,'Brick Labs · '+name,'Канада','CAN','Rosseau Lake College / Muskoka',themes,'boarding',
            '9–13 на 01.06.2027; 8/14 только с письменным исключением',unconfirmed,
            programme,'2027: 25–30.07 и 15–20.08; Sunday–Friday.',
            price(2027,'$1 650 / ребёнок / неделя; валюту окончательного счёта подтвердить.',
                  'Coach из North York, пансион, meals/snacks, материалы и основные активности.',
                  'Перелёт/дорога до North York, страховка отдельно. Day visit $150/день не доказывает иной младший возраст.',
                  'Deposit $650 входит в $1 650; остаток $1 000 до 01.03.2027. До 31.12.2026 возврат полный; 01.01–28.02 50%; с 01.03 нет. Граничные даты уточнить.'),
            'Комнаты 2–3 ребёнка, bedding; сотрудники Brick Labs/RLC. Отъезд из North York, не проживание в Toronto.',
            fit('conditional','2017 соответствует 9–13 на 01.06.2027; нужны уровень трека, EN и готовность к пансиону.'),
            fit('later','В 2027 только 6–7, стандартный минимум 9; исключение описано лишь для 8/14.'),
            'Конкретный 2027 пансион для Матвея; технический и творческий пакеты разделены.',
            ['Подтвердить EN, валюту/налоги, страховку, уровень и места; итоговый invoice до оплаты.'],
            [src('2027: возраст на 1 июня, четыре трека, тариф, coach и отмена',brick)],
            status='published_2027',priority=['technical','boarding'] if 'robotics' in themes else ['general','boarding'])
        p=profiles[-1]
        variants(p,[dict(start=s,end=e,label=label,price='$1 650 / неделя · валюту подтвердить',place=p['place'],source=brick,
            formats=['boarding'],proof='Тело официальной страницы — 2027, хотя URL содержит 2026. Трек и цена относятся именно к выбранной неделе.')
            for s,e,label in [('2027-07-25','2027-07-30',july),('2027-08-15','2027-08-20',august)]])

    nxt='https://www.nextrobotics.ca/programs-1'
    nxtreg='https://robotics.dreamclass.io/pages/admissions-v2/form/AUZGae'
    nxtfaq='https://www.nextrobotics.ca/faq'
    add('next-robotics','Next Robotics · IQ Summer Camp','Канада','CAN','4114 MacLeod Trail SE / Calgary',
        'robotics,coding','day','Grades 3–6 в сентябре 2027; возраст в годах не заменяет класс',unconfirmed,
        'Начальный VEX IQ: сборка, программирование, управление и работа в группе. 09–16. Клубная команда — другой годовой формат Grades 4–7, с опытом/отбором; недельный лагерь не гарантирует место в ней.',
        '2027: 05–09.07, 19–23.07, 26–30.07.',
        price(2027,'Community special: $315 ($300 + GST) за неделю; цена может измениться. Валюту счёта подтвердить.',
              'Учебный комплект предоставляет клуб.',
              'Card processing +2%; питание/страховку уточнить, жильё родителей и дорога отдельно.',
              'Оплата при checkout. FAQ: возврата после регистрации нет; credit только по индивидуальному решению.'),
        'Дневной; нужен отдельный семейный быт в Calgary.',
        fit('conditional','Подходит только при Grade 3–6 в Sep 2027; текущий класс неизвестен.'),
        fit('conditional','Нужен Grade 3–6 в Sep 2027; возраст 6–7 сам по себе допуска не подтверждает.'),
        'Практический вводный VEX-кандидат с отдельным маршрутом в сезонную команду.',
        ['Подтвердить школьный класс, EN, валюту, питание, полный платёж и наличие мест.'],
        [src('Три точные недели / класс / расписание',nxt),src('Открытый пакет 2027: GST, card fee и цена',nxtreg),src('Комплект / команды / отмена',nxtfaq)],
        status='published_2027',priority=['technical'])
    p=profiles[-1]
    variants(p,[dict(start=s,end=e,label='IQ Robotics · Grades 3–6',price='$315 с GST +2% card fee',place=p['place'],
        source=nxt,formats=['day'],date_scope='day_camp_window',proof='Недели в программе; цена в открытой Introduction формы. Данные ребёнка не вводились; заявку не отправляли.')
        for s,e in [('2027-07-05','2027-07-09'),('2027-07-19','2027-07-23'),('2027-07-26','2027-07-30')]])

    yres='https://www.yorkeducation.org/camp-programs/summer-camp'
    for slug,name,themes,age,programme,mat,osc in [
        ('yres-sports-steam','Sports & STEAM Adventure','general,science,sport','5–12',
         'Шесть недельных тем: космос, secret agents, спорт, динозавры, таланты и природа. Смешанный day camp.',
         fit('conditional','Возраст соответствует; подтвердить EN, площадку и выбранную неделю.'),
         fit('conditional','Возраст соответствует; подтвердить младшую группу, EN и площадку.')),
        ('yres-ai-robotics','AI & Robotics Innovators','robotics,ai,coding','7–12',
         'Последовательные недельные проекты: робот, код, игра/app. Результат полного шестинедельного цикла не гарантирован за одну неделю.',
         fit('conditional','Возраст соответствует; подобрать уровень и подтвердить EN.'),
         fit('conditional','Только после 7-летия, если оператор не подтвердит другое правило; точная дата рождения неизвестна.'))]:
        add(slug,'YRES · '+name,'Канада','CAN','York Region / Ontario · точные площадки TBD',themes,'day',age,unconfirmed,
            programme,'Опубликовано окно 05.07–13.08.2027, шесть недель. Точные выбранные недели/праздники уточнить; это сезонное окно, не непрерывное пребывание.',
            price(2027,'Промо: $195 / 5 дней; $156 / 4-дневную civic-holiday неделю; 6-week bundle $999. После 31.10 указаны $245 / $196 / $1 399. Валюту/налоги подтвердить.',
                  'Общая базовая camp fee; применимость к AI-треку отдельно подтвердить.',
                  'Meal plan +$60/5 дней, +$48/4 дня или +$300/bundle; extended care столько же, только Richmond Hill/East Markham. После 31.10 каждая опция $100 / $80 / $500. Card processing отдельно, сумма неизвестна.',
                  'Промо до 31.10.2026; lower Key Dates ещё30.09 — расхождение. Оплата после quote; скидки второму ребёнку нет. Refund/transfer письменно; таблицу удержаний подтвердить.'),
            '08:30–16; extended 08–17. Семь районов, все Location TBD; точную school-площадку не выдаём за известную.',mat,osc,
            'Кандидат на совместную дневную поездку: общий младший и отдельный технический трек.',
            ['Подтвердить EN, адрес, выбранные недели/праздники, тариф именно трека, скидку, валюту/налоги и отмену.'],
            [src('2027: программы, возраст, окно и изображение прайса',yres)],
            status='partial_2027',priority=['both','technical'] if slug.endswith('robotics') else ['both','general'],
            sessions=[['2027-07-05','2027-08-13']])

    arates='https://camparowhon.com/programs/rates-dates/'
    amini='https://camparowhon.com/programs/mini-camp/'
    afaq='https://camparowhon.com/ourteam/faq/'
    add('arowhon-regular','Camp Arowhon · Regular Sessions','Канада','CAN','Algonquin Park / Ontario',
        'general,sport','boarding','2 недели: завершённые Grades1–5; первые заезды также Grades6–7. Полные месяцы 7–15.',unconfirmed,
        'Outdoor, canoeing, спорт и творчество; общий лагерь. Учебного robotics/AI-трека не подтверждено.',
        '2027: 01–14.07 /29.07–11.08 (2 недели); 01–27.07 /29.07–23.08; 01.07–11.08 /01.07–23.08. Длинные 6/8-недельные пакеты имеют обязательный двухночный перерыв вне лагеря.',
        price(2027,'CAD5 200/2 недели; CAD10 200/первый месяц; CAD8 800/второй; CAD13 800/6 недель; CAD14 750/всё лето. +HST.',
              'Программа, laundry, еда и пансион.',
              'Toronto/Pearson bus CAD175/направление; changeover CAD95/направление. Optional kit CAD200; medical insurance обязательна, camp option CAD200.',
              'CAD1 000 аванс в счёт пакета. Отмена: до Dec1 CAD300; Dec1–Feb1 CAD500; Feb1–May1 CAD1 000; после May1 без возврата.'),
        'Cabin-пансион. В 6/8-week пакете 27–29.07 дети покидают camp; родители организуют две ночи и дорогу отдельно.',
        fit('conditional','Выбрать допустимый класс/длительность и подтвердить EN, плавание, готовность к ночёвкам.'),
        fit('conditional','Для 2 недель нужен уже завершённый Grade1; для полного месяца минимум 7. Рассмотреть сначала Mini.'),
        'Общий канадский пансион с опубликованной стоимостью; длинный пакет требует семейной логистики перерыва.',
        ['Подтвердить EN, класс, HST/весь invoice, страхование и двухночную логистику длинного пакета.'],
        [src('2027 пакеты / HST / трансфер / changeover / отмена',arates),src('Лагерная жизнь и допуск',afaq)],
        status='published_2027',priority=['general','boarding'])
    p=profiles[-1]
    variants(p,[dict(start=s,end=e,label=label,price=fee+' +HST',place=p['place'],source=arates,formats=['boarding'],
        proof='Точные 2027 границы пакета. 6/8 недель включают двухночный перерыв вне лагеря 27–29.07; это не непрерывный пансион.',
        **({'date_scope':'programme_window_with_break'} if 'перерыв' in label else {}))
        for s,e,label,fee in [('2027-07-01','2027-07-14','Starter · 2 недели','CAD5 200'),
            ('2027-07-29','2027-08-11','Starter · 2 недели','CAD5 200'),
            ('2027-07-01','2027-07-27','First Session','CAD10 200'),
            ('2027-07-29','2027-08-23','Second Session','CAD8 800'),
            ('2027-07-01','2027-08-11','6 недель · двухночный перерыв','CAD13 800'),
            ('2027-07-01','2027-08-23','Full Summer · двухночный перерыв','CAD14 750')]])
    add('arowhon-mini','Camp Arowhon · Mini Camp','Канада','CAN','Algonquin Park / Ontario',
        'general,sport','boarding','6–9; завершённые SK–Grade 3. SEO title 6–11 не заменяет основное правило 6–9.',unconfirmed,
        'Короткое знакомство с outdoor-пансионом: canoe, water activities, climbing/crafts и cabin life с counsellors.',
        '13–16.08.2027, 3 ночи.',
        price(2027,'CAD700 / Mini Camp; налоговый итог подтвердить.',
              'Короткий camp stay; детальное включение питания/материалов подтвердить.',
              'Mini bus CAD100/направление — другой тариф, чем regular bus; страховку отдельно подтвердить.',
              'Для Mini депозит не требуется. Таблица удержаний regular camp к Mini не применяется; собственную отмену уточнить.'),
        'Деревянные cabins, counsellors живут с детьми; душевые рядом.',
        fit('conditional','Только если ещё 9 на заезд или получено письменное исключение; после 10 стандартный Mini не подходит.'),
        fit('conditional','Возраст6–7 соответствует, но нужны завершённый SK–Grade 3, EN и готовность к трём ночам.'),
        'Первый короткий самостоятельный пансион для Оскара; для совместного заезда проверить верхнюю границу Матвея.',
        ['Подтвердить EN, birthdays/classes, HST, питание, страховку и отдельную отмену Mini.'],
        [src('Mini: реальные6–9, класс, bus и cabins',amini),src('2027 дата/цена; исключение Mini из regular cancellation',arates)],
        status='published_2027',priority=['general','boarding'],sessions=[['2027-08-13','2027-08-16']])
    p=profiles[-1]
    variants(p,[dict(start='2027-08-13',end='2027-08-16',label='Mini · 3 ночи / 4 дня',price='CAD700 · налоговый итог подтвердить',
        place=p['place'],source=amini,formats=['boarding'],proof='Официальная Mini-программа; bus100 в каждую сторону и отдельные условия отмены.')])

    cprice='https://catalinaseacamp.org/dates-rates/'
    cprog='https://catalinaseacamp.org/programs/1-week-programs/'
    cfaq='https://catalinaseacamp.org/catalina-island-faqs/'
    add('catalina-sea-junior','Catalina Sea Camp · One Week','США','USA','Catalina Island / California · отправление Long Beach',
        'science,general,sport','boarding','8–13; отдельные 18-дневные пакеты12–17 не этот трек',unconfirmed,
        'Морские science labs, snorkeling, лодки, природа и adventure. Диплом scuba не гарантирован младшей недельной программой; это не robotics camp.',
        '2027: 12–18.06, 19–25.06, 26.06–02.07.',
        price(2027,'USD3 750 / 7 дней; скидка USD300 до 31.10.2026 требует проверки при записи.',
              'Программа с проживанием и meal times; точное включение boat/оборудования получить в invoice.',
              'Дорога/airport shuttle, страховка, elective fees и доплаты уточнить.',
              'USD300 невозвратный аванс входит в tuition; полная оплата до 1 мая. До 1 февраля дополнительно удерживают100, Feb1–Apr30 200; May1–14 25%, May15–31 50%, после 1 июня 100%. Базу сочетания удержаний уточнить.'),
        'Dorm-style housing; main page указывает Toyon Bay, образец расписания прибытие Fox Landing — точную площадку недели подтвердить.',
        fit('conditional','Возраст8–13 подходит; нужны EN, readiness и правила водных занятий.'),
        fit('later','В 2027 младше8.'),
        'Содержательный морской science-пансион Матвею; другой оператор, чем Catalina Island Camps.',
        ['Подтвердить EN, конкретную бухту, boat/equipment fees, водный допуск, страхование и конечный invoice.'],
        [src('2027: точные недели / цена / оплата / отмена',cprice),src('Junior marine science / lodging / расписание',cprog),src('FAQ / организация',cfaq)],
        status='published_2027',priority=['general','boarding'])
    p=profiles[-1]
    variants(p,[dict(start=s,end=e,label='One Week · ages8–13',price='USD3 750 / 7 дней',place=p['place'],source=cprice,
        formats=['boarding'],proof='Точная младшая неделя2027; скидка/места изменяемы, final venue и полный пакет отдельно.')
        for s,e in [('2027-06-12','2027-06-18'),('2027-06-19','2027-06-25'),('2027-06-26','2027-07-02')]])

    lego='https://www.lavnercampsandprograms.com/robotics-camp-los-angeles-ca-san-francisco-ca-berkeley-ca-long-island-ny-manhattan-nyc-upper-east-side-miami-fl-seattle-wa-silicon-valley-ann-arbor-mi-houston-tx-cambridge-ma/'
    vex='https://www.lavnercampsandprograms.com/vex-robotics-camp-los-angeles-ca-long-island-ny-manhattan-nyc-upper-east-side-miami-fl-seattle-wa-ann-arbor-mi-houston-tx-cambridge-ma/'
    school='https://www.lavnercampsandprograms.com/school-year-camps/'
    for slug,name,age,programme,url,mat,osc in [
        ('lavner-lego','LEGO Engineering & Coding','6–10; завершённый Kindergarten',
         'LEGO MINDSTORMS, датчики, loops/conditions, сборка и внутренний ROBOWARS по пятницам. Обновление kit2027 проверить. Турнир лагеря не победа мировой лиги.',lego,
         fit('conditional','Летом2027 будет9–10; соответствует младшему треку, класс/границу возраста проверить.'),
         fit('conditional','Возраст6–7 подходит при завершённом Kindergarten; класс семьи неизвестен.')),
        ('lavner-vex','VEX IQ','10–14; завершённый Kindergarten',
         'VEX IQ: механика, gearing, sensors и командные проекты. Заявлены block coding/Python/C++; конкретную траекторию недели уточнить. Финальный турнир внутренний, не VEX Worlds.',vex,
         fit('conditional','В 2027 только при выполнении порога10 по правилам выбранного курса; дата рождения неизвестна.'),
         fit('later','Младше10.'))]:
        add(slug,'Lavner Tech Revolution · '+name,'США','USA','Сеть университетских/школьных кампусов USA',
            'robotics,coding','day',age,unconfirmed,programme+' 09–15, early/extended отдельно.',
            'Прочитанные pages/fees ещё Summer2026. Отдельная school-year landing существует, но local Narberth page озаглавлена2025; точный будущий2026/27 календарь не установлен.',
            price(2026,'Tuition по конкретной площадке; общий тариф не опубликован. Registration fee USD79/ребёнок относится к2026, не2027.',
                  'Материалы курса; состав equipment выбранной недели уточнить.',
                  'Lunch, early08–09, extended до17:45 отдельно; некоторые университеты требуют catered lunch. Семейное жильё/дорога отдельно.',
                  'Payment ACH/card. Переносы/отмену выбранного2027 сезона подтвердить; не переносить таблицу2026 без нового документа.'),
            'Только day camp; название университета не означает его академический кредит.',mat,osc,
            'Содержательный сетевой технический кандидат; точный campus/week/EN и2027 цена ещё нужны.',
            ['Проверить2027 local calendar, класс/возраст, EN, kit, lunch requirement, полную цену и отмену.'],
            [src('Конкретный robotics course / возраст / правила',url),src('School-year направления; будущие даты отдельно',school)],
            priority=['technical'])

    # Correct prior dossiers only when new primary evidence changes a family decision.
    idp=next(p for p in profiles if p['slug']=='id-tech')
    idp['language']='Официальный FAQ: все курсы на английском; нужны базовые чтение, речь и понимание инструкции/разговора.'
    idp['confirmed_instruction_languages']=['EN']
    idp['age']+='; общий минимум курса — до 31 декабря его года, отдельные курсы строже'
    idp['family_fit']['matvey']=dict(status='conditional',detail='В 2027 исполнится10 до 31 декабря: общий course gate10 может подойти до дня рождения. Строгий курс и отдельное правило overnight10 подтвердить.')
    idp['family_fit']['oscar']=dict(status='conditional',detail='В 2027 исполнится7 до 31 декабря: общий day-course gate7 может подойти до дня рождения. Строгие курсы отдельно; overnight10 недоступен.')
    idp['editorial_reason']='Первый сетевой технический кандидат США обоим по соответствующим уровням; английский доказан, возрастное правило конкретного курса проверять.'
    idp['programme']=idp['programme'].replace('около 5 часов','около 5,5 часов за компьютером с перерывами')
    for title,url in [('Прямое подтверждение EN / международные дети','https://idtechcamps.zohodesk.com/portal/en/kb/articles/do-you-accept-international-students'),
                      ('Course age до 31 декабря / исключения','https://idtechcamps.zohodesk.com/portal/en/kb/articles/can-you-make-an-age-exception'),
                      ('Возрастные группы / Summer2027','https://idtechcamps.zohodesk.com/portal/en/kb/articles/are-your-camps-segmented-by-age-21-8-2018'),
                      ('Время за компьютером / перерывы','https://idtechcamps.zohodesk.com/portal/en/kb/articles/how-much-time-do-students-spend-on-computers-each-day-at-id-tech-camps')]:
        idp['sources'].append(dict(title=title,url=url,checked=checked))
    weekly='https://rocketcenter.com/Help/FAQ/camps/weeklong/'
    for slug in ['space-camp','space-robotics']:
        p=next(p for p in profiles if p['slug']==slug)
        p['language']='Текущий weeklong FAQ допускает иностранных детей и требует fluent conversational English; действительные въездные документы отдельно.'
        p['confirmed_instruction_languages']=['EN']
        p['price']['extras']='Airport HSV round-trip USD120; extra arrival/departure day поUSD150 при необходимости авиарасписания; страховка/личные расходы отдельно.'
        p['price']['deposit']='FAQ: при отмене за8+недель 90% оплаченного tuition минусUSD100 non-refundable registration fee; позднюю отмену и график оплаты уточнить. Один перенос бесплатный, затемUSD25; запрос минимум за2недели.'
        p['sources'].append(dict(title='Текущий weeklong FAQ: иностранцы / fluent EN / transfer / возврат',url=weekly,checked=checked))
        if slug=='space-robotics':
            p['age']='9–11; в 9 лет требуется текущий или завершённый Grade 4'
            p['programme']='VEX Robotics: инженерия, программирование и wireless control; land-робот на Challenge Table. LED flashlight из series circuit, подводный robot, симуляция полётов дронов RealFlight. 6 дней / 5 ночей, воскресенье–пятница; финальный конкурс учебный, не титул мировой лиги.'
            p['family_fit']['matvey']=dict(status='conditional',detail='9–11 подходит, но если ещё 9 на заезд — требуется текущий/завершённый Grade 4. Точный класс неизвестен.')
