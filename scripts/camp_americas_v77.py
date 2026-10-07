"""Primary-site Americas pass: actual sessions, term classes and unresolved contracts."""
CHECKED='2026-10-05'
OLY='https://www.campolympia.com/summer-camps/dates-pricing-2027/'
SPARK='https://www.campolympia.com/summer-camps/programs/spark-week/'
WIN='https://winaukee.com/dates-rates'
WINFAQ='https://winaukee.com/the-winaukee-way/faqs'
EAGLE='https://campeagleridge.com/dates-rates/'
EAGLEFAQ='https://campeagleridge.com/about-camp-eagle-ridge/frequently-asked-questions/'
CEDAR='https://cedarridgecamp.ca/dates-rates/'
CEDAREN='https://cedarridgecamp.ca/international-campers/'
CUD='https://www.cuddleskidz.com/winter-camp'
INT='https://camp.integem.com/faq'
INTCU='https://camp.integem.com/register/summer-camps-in-cupertino-san-jose-sunnyvale-us-ca'
WILD='https://www.wildrootsworldschool.com/camp-info'
WILDTERMS='https://www.wildrootsworldschool.com/terms-and-conditions'
UCR='https://srp.ucr.ac.cr/noticia/ucr-sede-del-pacifico-realizo-con-exito-su-primer-campamento-de-robotica-para-ninos-y-ninas/'
UTP='https://sostenible.utp.ac.pa/noticia/actividad-tecno-camp-2026-utp'
GAL='https://cegalileo.com/escuela-de-robotica-educativa/'
CUBE='https://cubestemcamps.ca/classes'
HOLLAND='https://hollandbloorview.ca/services/programs-services/robotics-holland-bloorview/program-description'

def add_americas_v77(add,src,fit,profiles):
    def put(*a,**kw):
        add(*a,**kw);p=profiles[-1];p['checked']=CHECKED
        p['themes']=[t.strip() for t in p['themes']]
        for s in p['sources']:s['checked']=CHECKED
        return p
    def fee(y,label,included,extras,deposit):return dict(year=y,label=label,included=included,extras=extras,deposit=deposit)
    def sessions(p,rows,url,scope='camp_session'):
        p['timing']['sessions']=[[a,b] for a,b,label,cost in rows]
        p['timing']['session_details']=[dict(start=a,end=b,label=label,price=cost,source=url,
            formats=p['formats'],place=p['place'],date_scope=scope) for a,b,label,cost in rows]
    en_unknown='Язык занятий и иностранный приём уточнить: английский сайт сам по себе не доказательство English-medium.'
    seven=fit('conditional','Только после 7-летия на начало смены; в 2027 Оскару может быть ещё 6. Нужна готовность к ночёвкам.')
    mat=fit('candidate','9–10 соответствует основной возрастной группе; уровень и зачисление отдельно.')
    both_unknown=fit('unknown','Числовой возрастной допуск конкретной программы не опубликован; требуется подтверждение.')
    # All prices below are the regular published rate; expired early prices are not offers.
    for slug,name,age,rows,m,o,extra in [
        ('olympia-regular','Camp Olympia · обычный пансион','7–16',[
            ('2027-05-30','2027-06-12','Term1','$4 825'),('2027-06-13','2027-06-26','Term2','$4 825'),
            ('2027-06-27','2027-07-10','Term3','$4 825'),('2027-07-11','2027-07-24','Term4','$4 825'),
            ('2027-07-25','2027-08-06','Term5 · 13 дней','$4 480')],mat,seven,
         'Term5 заканчивается 6 августа по таблице, хотя общая фраза страницы говорит о субботних окончаниях.'),
        ('olympia-spark','Camp Olympia · SPARK / первая неделя','6–9; впервые в лагере',[
            ('2027-05-30','2027-06-05','SPARK1','$2 450'),('2027-07-25','2027-07-31','SPARK2','$2 450')],
         fit('conditional','Только до 10-летия и при соответствии условию первого лагеря; прежние поездки уточнить.'),
         fit('candidate','6–7 по возрасту подходит; готовность к первой самостоятельной ночёвке проверить.'),'18 возрастных активностей; не инженерная академия.')]:
        p=put(slug,name,'США','USA','Trinity, Texas · Lake Livingston','general,sport,art','boarding',age,en_unknown,
            'Спорт, вода, лошади, скалолазание и творчество. Робототехника/AI не заявлены. '+extra,
            'Опубликованы смены 2027; конкретные даты в календаре.',
            fee(2027,'$4 825/14 дней; $4 480/Term5' if slug.endswith('regular') else '$2 450/7 дней',
                'Пансион и основная программа; валюта USD предполагается по американскому оператору, подтвердить в счёте.',
                'Карта +3%; перелёт, трансфер и дополнительные покупки уточнить. Второму ребёнку заявлено 5%; совместимость льгот неизвестна.',
                '$500 аванс в счёт цены: $250 невозвратны сразу, остальные до 01.01.2027; баланс 01.04.2027. Отмена 31+ дней: минус аванс,14–30: половина минус аванс,<14: без возврата.'),
            'Детские cabins, мальчики и девочки отдельно; возрастные группы.',m,o,
            'Кандидат на общий пансион с опубликованным 2027 контрактом; ACA/соотношение сотрудников заявляет оператор, независимого рейтинга нет.',
            ['Подтвердить EN, валюту, полный пакет, младший допуск/первый лагерь, места и трансфер.'],
            [src('Тарифы и условия 2027',OLY),src('Основная программа','https://www.campolympia.com/summer-camps/'),src('Отдельный SPARK',SPARK)],
            status='published_2027',priority=['general','boarding'])
        sessions(p,rows,OLY)

    for slug,name,age,rows,o in [
        ('winaukee-regular','Winaukee · sports sleepaway','Мальчики 7–15; Mainland7–12 / Island13–15',[
            ('2027-06-23','2027-07-17','Session1','$10 150'),('2027-07-18','2027-08-07','Session2','$8 050'),
            ('2027-06-23','2027-08-07','Full summer','$16 400')],seven),
        ('winaukee-rookie','Winaukee · Rookie / Winaukee in2','Мальчики 7–15 общая граница; Rookie только первый сезон, Grades1–4',[
            ('2027-06-23','2027-07-06','Первый двухнедельный опыт','$5 500')],
         fit('conditional','Нужно 7-летие, Grade1+ и первый сезон. По одному году рождения допуск не установлен.'))]:
        p=put(slug,name,'США','USA','Lake Winnipesaukee, New Hampshire','general,sport,art','boarding',age,en_unknown,
            'Спортивная и творческая программа W.A.A.M.; устройства запрещены. Технического coding/robotics курса не подтверждено.',
            '23 июня — 7 августа 2027; отдельные пакеты в календаре.',
            fee(2027,'Regular: $10 150 /8 050 /16 400' if slug.endswith('regular') else '$5 500 /2 недели',
                'Выбранный пансион; долларовая валюта и состав all-in требуют счёта.',
                'Логотипная одежда обязательна частично и отдельно; транспорт/карманные расходы уточнить. Early-bird закончился 01.10.2026.',
                'Депозит и cancellation не установлены в прочитанных страницах; не переносить чужую политику.'),
            'Пансион для мальчиков; Mainland для младших.',mat if slug.endswith('regular') else fit('conditional','Grade1–4 и первый сезон; фактический класс неизвестен.'),o,
            'Общий спортивный лагерь с ясными пакетами; рекламное «best» не независимый мировой рейтинг.',
            ['Получить EN/admission, класс, договор отмены, транспорт и стоимость обязательной одежды.'],
            [src('Dates & Rates 2027',WIN),src('Одежда, техника и транспорт',WINFAQ),src('Возраст/площадки','https://winaukee.com/')],status='published_2027',priority=['general','boarding'])
        sessions(p,rows,WIN)

    p=put('eagle-ridge-leadership','Camp Eagle Ridge · leadership & outdoor','США','USA',
        'Mellen, Wisconsin · 75392 Lake Galilee Road','general,sport,entrepreneurship','boarding','7–17',en_unknown,
        'Лидерство, самостоятельность и outdoor; cabin6–12 с сотрудниками. Три приёма пищи, еженедельная прачечная при длинной смене. Без интернета/телефонов; robotics не заявлена.',
        'Лето 2027,1–7 недель; места на сайте — снимок 30.09.2026.',
        fee(2027,'Обычные $1 595/нед.; 2 недели3 190 /3нед.4 785 /4нед.6 380 /5нед.7 975 /6нед.9 570 /7нед.11 165.',
            'Пансион и основная программа; валюту/налоги подтвердить.',
            'Early-bird30.09.2026 истёк; автобус/авиавстреча/магазин и optional trips отдельно. Sibling6% второму,15% третьему,20% четвёртому по странице.',
            'До15.05.2027 refund минус$120/нед.,16–31мая половина минус$125/нед.: суммы120/125 расходятся. После31мая возврата нет; правила автобуса отдельные.'),
        'Обычный детский пансион; международные дети перечислены в FAQ.',mat,seven,
        'Может быть полезен для самостоятельности и лидерства; иностранный состав доказан, английский язык преподавания отдельно не установлен.',
        ['Разрешить противоречие120/125, EN, полный транспортный счёт, возраст и текущие места.'],
        [src('Все смены и regular fees',EAGLE),src('Быт/иностранные участники',EAGLEFAQ),src('Активности','https://campeagleridge.com/activities/list-of-activities/')],status='published_2027',priority=['general','boarding'])
    sessions(p,[(a,b,label,'$'+price) for a,b,label,price in [
        ('2027-06-20','2027-06-26','1 неделя','1 595'),('2027-06-27','2027-07-10','2 неделиA','3 190'),
        ('2027-07-11','2027-07-24','2 неделиB','3 190'),('2027-07-25','2027-08-07','2 неделиC','3 190'),
        ('2027-06-20','2027-07-10','3 недели','4 785'),('2027-06-27','2027-07-24','4 неделиA','6 380'),
        ('2027-07-11','2027-08-07','4 неделиB','6 380'),('2027-06-20','2027-07-24','5 недель','7 975'),
        ('2027-06-27','2027-08-07','6 недель','9 570'),('2027-06-20','2027-08-07','7 недель','11 165')]],EAGLE)

    for slug,name,age,rows,m,o in [
        ('cedar-regular','Cedar Ridge · overnight outdoor','Таблица2027:6–15; homepage7–16 — конфликт',[
            ('2027-07-03','2027-07-16','A'),('2027-07-17','2027-07-30','B'),
            ('2027-08-02','2027-08-14','C'),('2027-07-03','2027-07-30','D · месяц')],mat,
         fit('conditional','Таблица разрешает6,главная с7; младший допуск нужно подтвердить.')),
        ('cedar-mini','Cedar Ridge · Mini Camp','6–9',[
            ('2027-07-03','2027-07-09','Mini1'),('2027-07-10','2027-07-16','Mini2'),
            ('2027-07-17','2027-07-23','Mini3'),('2027-07-24','2027-07-30','Mini4'),
            ('2027-08-02','2027-08-08','Mini5'),('2027-08-08','2027-08-14','Mini6')],
         fit('conditional','Только до10-летия; затем общий лагерь.'),fit('candidate','6–7 соответствует Mini; ночёвки/приём подтвердить.'))]:
        p=put(slug,name,'Канада','CAN','McArthurs Mills, Ontario ·57 Cemetery Road','general,languages,sport','boarding',age,
            'Английская среда camp-life подтверждена страницей для иностранных детей; это не формальный ESL или EN-robotics курс.',
            'Природа, озеро, спорт и лагерный быт. Пансион светский, OCA по оператору; техническая программа не установлена.',
            'Смены2027 опубликованы; регистрация с ноября2026 без точного дня. Цена2027 отсутствует.',
            fee(None,'Прайс2027 ещё пуст; +13%HST по странице.',
                'Пакет питания/жилья и занятий должен быть подтверждён новым счётом.',
                'YYZ140+HST/направление без сезона; Toronto80/Ottawa65+HST относятся к автобусам2026. Не используем их как договор2027. Магазин/printed email отдельно.',
                'Депозит100 и апрельские сроки страницы ещё2026; правила оплаты/отмены2027 неизвестны.'),
            'Пансион; свой approved PFD по packing list, форму и трансфер уточнить.',m,o,
            'Английская международная среда с датами, но бюджет ещё не готов; не бронировать поездку по старому прайсу.',
            ['Уточнить возраст6/7, новый прайс2027, трансфер/отмену и полный счёт.'],
            [src('Dates2027 / устаревшие условия2026',CEDAR),src('Международные дети и English',CEDAREN),src('Быт/packlist','https://cedarridgecamp.ca/faq/'),src('Возраст homepage','https://cedarridgecamp.ca/')],
            status='partial_2027',confirmed=['EN'],priority=['general','boarding'])
        p['language_evidence_role']='camp_life'
        sessions(p,[(a,b,label,'Цена2027 не опубликована;13%HST') for a,b,label in rows],CEDAR)

    p=put('cuddles-winter','Cuddles Learning · winter STEAM','Канада','CAN',
        'Markham · Lincoln Alexander P.S.,38 Hillmount Road; winter venue подтвердить','robotics,coding,games,art','day','5–13',en_unknown,
        'Minecraft Education, pixel art, robotics/coding и outdoor. Объём технических занятий и комплект домой не раскрыты.',
        'Верх страницы:22.12.2026–02.01.2027; фактические рабочие дни/праздничные закрытия неизвестны. Широкое окно не точная смена.',
        fee(None,'Regular: $99/1день,179/2,249/3,399/5; early79/158/219/339 без крайнего срока; ISO-валюта неизвестна.',
            'Учебная программа; питание/оборудование полного winter-пакета не подтверждены.',
            'Свой lunch/snacks/water; extended-care отдельно. Табличная скидка2дня заявлена20, фактически179−158=21.',
            'Общий afterschool FAQ:7+дней полный refund,позжеcredit,после старта нет; применимость к winter2026/27 подтвердить.'),
        'Дневной; адрес из общего FAQ, не гарантия winter-campus.',mat,
        fit('candidate','6–7 подходит по общей группе5–13; отдельный winter-приём уточнить.'),
        'Кандидат для обоих с видимым тарифом, но валюта, язык и рабочие дни ещё не установлены.',
        ['Точные camp-дни, EN, ISO-валюта/налоги, winter-address, техника, итог с extendedcare и отмена.'],
        [src('Winter и таблица цен',CUD),src('Общий FAQ, не winter-контракт','https://www.cuddleskidz.com/faqs')],status='partial_2026_27')
    p['timing']['precision']='season_window';p['price']['season']='2026/27'
    p['timing']['sessions']=[['2026-12-22','2027-01-02']]

    for slug,name,age,content,m,o in [
        ('integem-junior','Integem · Junior AI Robotics','Grades K–2, 6–8 лет',
         '1 неделя Intro: мотор, ESP32 и дополненная реальность. 2 недели Engineering: сенсоры, ультразвук и движение по линии. 3 недели Advanced: три системы и автономные задачи.',
         fit('not_eligible','В 9–10 лет группа Junior 6–8 уже не подходит; выбирать Young.'),
         fit('conditional','Возраст 6–7 подходит, нужны классы K–2 и самостоятельное понимание EN.')),
        ('integem-young','Integem · Young AI Robotics','Grades 3–5, 8–11 лет; другая общая таблица указывает 8–10',
         'Intro: ESP32, сенсоры и дополненная реальность. Engineering добавляет MechaArm, Raspberry Pi Pico, WiFi 6 и колёса Mecanum. Advanced развивает робота Mecha и AR.',
         fit('conditional','Возраст 9–10 подходит, но нужны Grades 3–5; класс и сложность продвинутого курса подтвердить.'),
         fit('later','Для Young нужно минимум 8 лет и Grade 3; младшему подходит Junior.'))]:
        p=put(slug,name,'США','USA','Cupertino · St Joseph School, 10120 N De Anza Blvd; площадку 2027 подтвердить',
            'robotics,coding,ai,technology','day',age,
            'FAQ прямо: все лагеря на английском; ребёнок понимает/отвечает самостоятельно. English подтверждён, не только интерфейс.',
            content+' Наборы включены для класса, остаются собственностью школы; домой робот не входит. Новичкам можно, опытным нужна диагностика.',
            'Лето 2026 закрыто; сайт собирает интерес к 2027, конкретных дат/цен ещё нет. Подписка семьи не создана.',
            fee(None,'Стоимость 2027 не опубликована в прочитанных страницах.',
                'Классные robotics kits включены по FAQ; собственный домашний kit не покупать по этому описанию.',
                'Питание, устройство/лицензии, присмотр и поездка требуют нового пакета 2027.',
                'Текущий FAQ: отмена21+дней минусregistration+$150/нед. илиvoucher,позже безrefund; правило24ч имеет условия. Новый договор 2027 ещё нужен.'),
            'Дневной курс на 1, 2 или 3 недели, ночёвки не объявлены.',m,o,
            'Содержательный английский инженерный вариант для раздельных возрастных треков; сертификаты/конкурсы старшей школы не переносятся младшим.',
            ['Даты и цены 2027, школьный класс, площадка, выбор уровня и полный счёт с условиями отмены.'],
            [src('Раскрытые ответы FAQ: curriculum/English/kit',INT),src('Cupertino:2026closed/2027updates',INTCU),src('Общие курсы','https://camp.integem.com/summercamp')],confirmed=['EN'],priority=['technical'])
        p['language_evidence_role']='primary'

    p=put('wildroots-marine','Wild Roots · Marine Biology Camp','Мексика','MEX','Playa del Carmen / Akumal','science,general,art','day',
        'Числовой возраст не найден; плавание и уверенность в воде обязательны.',en_unknown,
        'Пять дней marine biology/conservation: snorkel, наблюдения, beach-cleanup, творчество и cenote. Погода меняет программу; робототехника не заявлена.',
        'Зима28.12–01.01,04–08.01,11–15.01.2027; весна29.03–02.04. Первый весенний22–28марта расходится с5днями — исключён из точного календаря.',
        fee(None,'$400/ребёнок,50 sibling-discount; валюта не указана. Не считать автоматическиUSD илиMXN.',
            'Питание и основные guided activities по camp-page.',
            'Жильё родителей, страховка, ежедневный семейный транспорт и дополнительные parent/sibling trips отдельно; экскурсионный van уточнить.',
            'В пределах120дней до старта безrefund, кроме отмены оператором. Старшая winter-смена уже внутри этого срока на05.10.2026; вывод по календарю. Семья ничего не бронировала.'),
        'Drop-off09–14,семья живёт отдельно; некоторые совместные экскурсии за доплату.',both_unknown,both_unknown,
        'Местная прикладная наука на зимние каникулы; возраст/EN/валюта остаются решающими вопросами.',
        ['Минимальный возраст, EN/ES, ISO-валюта, плавание, транспорт, точные spring-дни и письменная отмена.'],
        [src('Планы и пакеты',WILD),src('Возврат/транспорт',WILDTERMS),src('CDMX — другая программа','https://www.wildrootsworldschool.com/')],status='partial_2026_27',priority=['general'])
    p['price']['season']='2026/27'
    sessions(p,[(a,b,'5 дней marine biology','$400, ISO-валюта уточнить') for a,b in [
        ('2026-12-28','2027-01-01'),('2027-01-04','2027-01-08'),('2027-01-11','2027-01-15'),('2027-03-29','2027-04-02')]],WILD,'day_camp_window')

    for slug,name,country,iso,place,age,content,label,url,m,o in [
        ('ucr-pacific-archive','UCR Pacífico · robotics / новый сезон ждать','Коста-Рика','CRI','Puntarenas · UCR Sede del Pacífico','Архив2025:5–14',
         'Электричество/солнечная энергия, механика/гидравлика, circuit-lab и3Dшестерни;44участника.',
         '08–16.07.2025,статья07.08.2025; это не2026/27.',UCR,mat,fit('candidate','Архивная группа5–14 подходит, новый допуск ещё не объявлен.')),
        ('utp-tecnocamp-archive','UTP · TecnoCamp / новый сезон ждать','Панама','PAN','Panama City · Campus Dr Víctor Levi Sasso','Архив:участники8–13; один6летний не правило приёма',
         'Робототехника/3Dдизайн вместе со спортом,культурой и cooking; не полный robotics-intensive.',
         '19–27.01.2026,статья19.01.2026;2027не объявлен.',UTP,mat,fit('unknown','Один шестилетний в отчёте не устанавливает минимальный возраст6.'))]:
        p=put(slug,name,country,iso,place,'robotics,science,technology,general','day',age,
            'Страница на испанском; фактический язык преподавания EN/ES/RU и иностранный приём не доказаны.',content,label,
            fee(None,'Новый прайс2026/27 не опубликован в прочитанном источнике.','Есть подтверждение прошедшей программы, не новая оферта.',
                'Часы/материалы, питание, оборудование и возрастные группы нового сезона неизвестны.','Новый договор, оплата/отмена неизвестны.'),
            'Дневной архив; новый календарь и сопровождение уточнить.',m,o,
            'Реальная региональная инженерная программа; прошлый отчёт не прогноз будущих дат.',
            ['Дождаться нового объявления, прайса, языка, школьных/возрастных условий и допуска внешних детей.'],[src('Первичный отчёт фактического года',url)])

    p=put('galileo-cuenca','Galileo Cuenca · robotics vacacional / даты спорны','Эквадор','ECU',
        'Cuenca · Av.del Estadio4-35 y Roberto Crespo,Edificio El Estadio,PB','robotics,coding,science','day','Vacacional от5; распределение групп уточнить.',
        'Испанская страница; основной язык уроков/EN-помощь не подтверждены.',
        'LEGOWeDo2.0/EV3,blocks,circuits и творческие активности. Время09–12/14:30–17:30; постоянная школа и каникулы имеют разные тарифы.',
        'Написано2027,но29июня/27июля названы понедельниками,24июля/21августа пятницами: календарь2027 не совпадает. Субботние даты тоже воскресенья2027. Точные смены не создаём.',
        fee(None,'Vacacional: $85/$155 в месяц,IVAвключён; валюта, пакет и год тарифа уточнить.',
            'Материалы/лаборатория явно включены в постоянном курсе; не доказаны для vacacional.',
            'Постоянные тарифы52/63/70/76 относятся к2–5ч/нед., не лагерю. Не складываем разные продукты.',
            'Отмена/приём иностранных детей и новое расписание требуют подтверждения.'),
        'Дневной курс; пансион не объявлен.',mat,fit('candidate','Общийvacacional5+ подходит; язык и возрастной курс уточнить.'),
        'Региональный robotics-кандидат, но несовместимые weekday/year не основание для поездки.',
        ['Новый календарь2027, exact-package85/155, валюта, EN/ES, оборудование и cancellation.'],[src('Собственная школа и vacacional',GAL)],status='partial_2027')

    # Weekly courses are represented as actual lesson days, never as a continuous camp.
    for slug,name,age,content,m,o,time in [
        ('cube-grade1','Cube STEM · RoboBuilders Junior / Grade1','Grade 1 на сентябрь 2026',
         'Зима: робототехника, электроника и блочное программирование. Весна: Scratch. Два разных курса по восемь занятий.',
         fit('not_eligible','Возраст 9–10 обычно выше Grade 1; ориентир — реальный класс, не год рождения.'),
         fit('conditional','Только Grade 1 на сентябрь 2026; дошкольник автоматически не зачисляется.'),('10:00','11:15')),
        ('cube-grade45','Cube STEM · STEMSquad / Grades4–5','Grades 4–5 на сентябрь 2026',
         'Зима: SPIKE Prime, миссии и навесные механизмы. Весна: Python. Участие в лиге этим курсом не обещано.',
         fit('conditional','Только если Grade 4/5 на сентябрь 2026; Grade 3 не входит в этот конкретный курс.'),
         fit('not_eligible','Младший пока не в Grades 4/5.'),('15:15','16:30'))]:
        p=put(slug,name,'Канада','CAN','Toronto · Beaches Presbyterian Church; точный classroom уточнить',
            'robotics,coding,technology','day',age,en_unknown,content,
            'Субботы 09.01–06.03.2027, кроме 13.02; 10.04–05.06, кроме 22.05. Каждый курс: 8 занятий по 75 минут. Это еженедельный кружок.',
            fee(2027,'CA$275 + HST за 8 уроков одного семестра; CAD прямо указан на сайте.',
                'Один курс из восьми занятий; оборудование/лицензии и итоговый проект уточнить.',
                'Пакет 675 до 15.10.2026 указан в заголовке, но товарная карточка показывает 645 с уже истёкшим сроком 01.09. Пакетный прайс требует уточнения.',
                'Уточнить отмену, пропуски, приём иностранных детей и тариф выбранного семестра 2027.'),
            '75 минут один раз в неделю; жилья/присмотра на каникулы нет.',m,o,
            'Полезен при длительной базе в Toronto; не повод лететь на восьминедельный «лагерь».',
            ['Школьный класс на сентябрь 2026, EN, стоимость одного term, оборудование и режим пропусков.'],
            [src('Timetable2026/27 / классы и исключённые субботы',CUBE),src('Собственный оператор','https://cubestemcamps.ca/')],status='published_2027',priority=['technical'])
        sessions(p,[('2027-01-09','2027-03-06','Winter ·8 уроков','CA$275+HST'),
            ('2027-04-10','2027-06-05','Spring ·8 уроков','CA$275+HST')],CUBE,'session_days')
        from datetime import date,timedelta
        for v in p['timing']['session_details']:
            first=date.fromisoformat(v['start']);last=date.fromisoformat(v['end']);days=[]
            while first<=last:
                if first.isoformat() not in ['2027-02-13','2027-05-22']:
                    days.append(dict(date=first.isoformat(),topic=v['label'],start_time=time[0],end_time=time[1],timezone='America/Toronto',time_note='Очное занятие; время Toronto.'))
                first+=timedelta(days=7)
            assert len(days)==8
            v['sessions']=days

def extend_report_v77(report):
    report['shortlist'].extend([
        dict(label='США · первый короткий пансион',slugs=['olympia-spark','olympia-regular','winaukee-rookie','eagle-ridge-leadership'],reason='Olympia SPARK: 6–9 лет, $2450 за неделю; Матвею только до 10-летия. Winaukee Rookie: 7+ и Grades 1–4; Eagle: 7+. Основные направления — общий отдых и спорт. Английский и полную стоимость с транспортом нужно подтвердить.'),
        dict(label='Канада · английская среда и короткий Mini',slugs=['cedar-mini','cedar-regular'],reason='Cedar Mini: шесть смен 2027 для 6–9 лет. Основной лагерь указывает 6–15, а главная страница — 7–16. Английская среда подтверждена; прайс 2027 пока пуст. Старые условия депозита и автобусов относятся к 2026.'),
        dict(label='США · английский robotics по отдельным уровням',slugs=['integem-junior','integem-young'],reason='Оскару — Junior 6–8 лет, K–2; Матвею — Young 8–11 лет, Grades 3–5. ESP32, сенсоры, дополненная реальность и MechaArm. Учебный комплект остаётся организатору. Английский прямо подтверждён; даты и цены 2027 ещё ждём.'),
        dict(label='Ближе к дому · science и реальные региональные robotics',slugs=['wildroots-marine','ucr-pacific-archive','utp-tecnocamp-archive','galileo-cuenca'],reason='В Playa del Carmen четыре согласованных периода по пять дней; возраст, валюта и английский ещё неизвестны, требуется уверенность в воде. UCR 2025 и UTP 2026 — архив. У Galileo даты не совпадают с названными днями недели 2027. Эти варианты требуют новых документов перед поездкой.'),
        dict(label='Toronto · занятия при длительной базе',slugs=['cube-grade1','cube-grade45','cuddles-winter'],reason='Cube: восемь субботних уроков за CA$275 + HST, допуск по классу на сентябрь 2026. Cuddles: 5–13 лет, $399 за пять дней; валюта и конкретные зимние дни неизвестны. Английский у обоих ещё не подтверждён.')])
    report['gaps'].extend([
        dict(country='США / Канада',iso='USA',provider='v77: новые пансионы — возраст, валюта и контракт',detail='Olympia2027SPARK6–9 закрывается Матвею после10; WinaukeeRookie требуетGrade1–4 и первого сезона. Eagle120/125cancel-conflict. Cedar2027datesбезцены,6–15vs7–16; payment/busещё2026. Истёкшие30Sep/1Oct скидки не текущие.',next_action='Новые all-inquotes/EN/internationaladmission и возраст на конкретный старт; источники не равно подтверждённому месту.',url=CEDAR),
        dict(country='Канада',iso='CAN',provider='v77: Cuddles/Cube — другой продукт и точность',detail='Cuddleswinter-window22Dec–2Jan не список рабочих дней; ISO-валюта отсутствует и скидка2дня ошибочна. Cubeweekly8×75мин с двумя пропущенными субботами,не пансион/лагерь; Grade3winter имеет конфликт2026/2027,Grade2end иGrade6time также спорны, не добавлены точно.',next_action='Уточнить реальные уроки/рабочие camp-дни, валюту,EN,оборудование и договор выбранного продукта.',url=CUBE),
        dict(country='Канада',iso='CAN',provider='v77: Holland Bloorview — специальная доступность',detail='March15–19.03.2027,$475+HST; заголовок9–14vseligibility8–14. Program-description требуетformaldiagnosisдо старта; March-page формулирует иначе. Juniorwinter6–10 есть, но правила не доказывают обычный международный приём. Не выводим диагноз/допуск для семьи.',next_action='Уточнить операторскую доступность/agepolicy без передачи медицинских данных; не включать как обычную открытую семейную оферту.',url=HOLLAND),
        dict(country='Коста-Рика / Панама / Мексика / Эквадор',iso='CRI',provider='v77: архив и конфликтующие обещания',detail='UCRробототехника08–16Jul2025 не2027; UTP19–27Jan2026 с одним6летним не возрастная политика. WildRootsspring22–28Mar2027 vs5дней, валюта/возраст не заданы;CDMX23–27Nov2026 отдельный продукт. Galileoweekdayне совпадаютс2027. EN/ES/RUинтерфейса не язык обучения.',next_action='Новые2027 первичные договоры/подробности; первая спорная веснаGalileo/WildRoots исключена из точных дат. Мировой сбор продолжается, полностью проверенных стран0.',url=GAL)])
