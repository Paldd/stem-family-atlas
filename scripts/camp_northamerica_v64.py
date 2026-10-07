"""North American stays: official 2027 tables, grade gates and unresolved contracts."""
def add_deep_northamerica(add, src, fit, profiles):
    def put(*a,**k):
        a=list(a);a[5]=a[5].replace(' ','');a[6]=a[6].replace(' ','')
        add(*a,**k); p=profiles[-1]; p['checked']='2026-10-05'
        for s in p['sources']: s['checked']=p['checked']
        return p
    def price(year, label, included, extras, deposit): return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)
    def dates(p, rows, source):
        p['timing']['sessions']=[[s, e] for s, e, lab, fee in rows]
        p['timing']['session_details']=[dict(start=s, end=e, label=lab, price=fee, place=p['place'], source=source, formats=p['formats']) for s, e, lab, fee in rows]
    ar='https://astrocamp.org/camp-dates-rates/'
    aj='https://astrocamp.org/camp-overview/one-week-sessions/'
    ag='https://astrocamp.org/parent-guide/'
    at='https://astrocamp.org/travel/'
    p=put('astrocamp-junior','AstroCamp · One-Week Discovery','США','USA','Idyllwild, California · 26800 Saunders Meadow Rd',
        'general, science, sport','boarding','Минимум 7. Rates/header: 7–13; карточка At a Glance/Parent Guide: 7–12 — верхний предел расходится.',
        'Прямого утверждения об английском всех занятий и приёме иностранного ребёнка в прочитанных FAQ нет; английский сайт не считается доказательством.',
        '7 дней / 6 ночей: наука и STEM-активности вместе с outdoors, творчеством, кулинарией и выборными занятиями. Родительский гид 2027 прямо описывает STEM как часть общего лагеря. Не отдельный робототехнический интенсив; школьные лаборатории нельзя автоматически обещать каждому summer camper.',
        'Непротиворечивые смены 2027: 12–18 июня, 19–25 июня, 25–31 июля. Август: rates 1–7 августа, At a Glance 2–7 — день приезда уточнить; спорная смена не добавлена в точный календарь. Старый astrocampsummer.org остаётся на 2026/8+.',
        price(2027,'USD 2 900 / неделя; на rates скидка USD 250 до 31 октября. Применение к выбранной заявке подтвердить.',
            'Проживание, питание, основные активности и оборудование; Junior FAQ не заявляет дополнительных обязательных program fees.',
            'Перелёт, страховка и ONT transfer USD 60 в каждую сторону по без указания года travel-page; итог 2027 подтвердить. LAX transfer не предлагается; вне разрешённых flight slots возможна доплата.',
            'USD 300 невозвратный аванс в счёт цены; balance May 1. До Feb 1 ещё USD 100 cancellation fee, Feb–Apr USD 200; May 1–14 удержание 25%, May 15–31 50%, после June 1 100%. Оператор допускает регулируемую надбавку до USD 150 с возможностью отказаться. Отдельное исключение financial aid не распространяем на обычную заявку.'),
        'Пансион; готовность к ночёвкам, bedding и присмотр проверить в пакете 2027.',
        fit('candidate','9–10 в 2027: входит в обе опубликованные младшие границы; язык и иностранный допуск ещё нужны.'),
        fit('conditional','Только после 7-летия к первому дню; в 6 лет не допускается.'),
        'Научно-приключенческий короткий пансион с реальными датами и прозрачным базовым тарифом; допуск обоих зависит от дня рождения младшего.',
        ['Подтвердить EN занятий, международный допуск, точный августовский старт, возраст на дату и окончательный transfer/insurance пакет.'],
        [src('2027: смены, тарифы, оплата и отмена', ar), src('Junior: включения и расхождения дат/возраста', aj), src('Гид родителей именно 2027', ag), src('ONT transfer и допустимые flight slots', at)], status='published_2027', priority=['general','boarding'])
    dates(p,[('2027-06-12','2027-06-18','Junior · 7 дней / 6 ночей','USD 2 900'),('2027-06-19','2027-06-25','Junior · 7 дней / 6 ночей','USD 2 900'),('2027-07-25','2027-07-31','Junior · 7 дней / 6 ночей','USD 2 900')], ar)

    fr='https://frenchwoods.com/dates-and-rates.htm'; fh='https://frenchwoods.com/'
    fi='https://frenchwoods.com/international-campers.htm'; fp='https://frenchwoods.com/program-french-woods.htm'
    ft='https://frenchwoods.com/transportation.htm'; fw='https://frenchwoods.com/session5.htm'
    en='EN-погружение прямо описано: общение в домиках и выбранных активностях весь день с native speakers. Это общий/творческий лагерь, не отдельные ESL lessons или английская робототехника.'
    extra='Перелёт, UM/baggage fees, camp airport/bus transfer, страховка и остальные обязательные сборы в полном договоре уточнить. Подтверждённый прайс transfer не найден; международным детям предоставляются bedding/towels и еженедельная прачечная.'
    pay='Early rate до Dec 1; общий аванс USD 1 750 на ребёнка. До Dec 1 2026 возврат минус 550, до Mar 1 2027 минус 800; возвраты не выдаются до May 1 2027. Условия поздней отмены и under-nine special programme нужны отдельно.'
    p=put('frenchwoods-regular','French Woods Festival · Performing Arts Boarding','США','USA','Hancock, New York · 199 Bouchoux Brook Rd',
        'general, art, sport','boarding','7–17; отдельные условия программы under nine уточнить', en,
        'Музыка, театр, танец, цирк, изобразительное искусство, спорт и другие electives. Шесть периодов: три постоянных majors и три ежедневных minors. Конкретное меню меняется по смене. Финальные спектакли/показы — лагерная практика, не международная победа.',
        '2027: четыре базовые 3-недельные смены 6–27 июня / 27 июня–18 июля / 18 июля–8 августа / 8–29 августа; сочетания 6/9/12 недель тоже опубликованы.',
        price(2027,'3 недели early USD 6 700 / 8 000 / 8 800 / 6 700. После Dec 1: 6 900 / 8 400 / 8 400 / 7 100. Session 3 early выше late — расхождение не исправляем догадкой.',
            'Пансионная программа и выбранные активности; конкретный полный состав, платные опции и исключения подтвердить.', extra, pay),
        'Пансион; иностранные campers прямо принимаются. Прилёт EWR, staff встречает ребёнка; международная страница описывает встречу после Customs.',
        fit('candidate','Возраст 9–10 подходит; выбрать программу и готовность к 3+ неделям.'), fit('conditional','После 7-летия; условия under-nine programme и ночёвок уточнить.'),
        'Содержательный общий творческий пансион с прямым доказательством английской лагерной жизни и международного состава.',
        ['Сверить Session 3 тариф, under-nine условия, полный счёт и перенос/отмену; availability конкретных majors не обещана.'],
        [src('Возраст и международный состав', fh), src('Точная таблица 2027', fr), src('EN-погружение и иностранные campers', fi), src('Majors/minors и меняющееся меню', fp), src('Трансфер и EWR', ft)], status='published_2027', priority=['general','boarding','both'], confirmed=['EN'])
    p['language_evidence_role']='camp_life'
    rows=[('2027-06-06','2027-06-27','Session 1 · 3 недели','USD 6 700 / после Dec 1 6 900'),('2027-06-27','2027-07-18','Session 2 · 3 недели','USD 8 000 / после Dec 1 8 400'),('2027-07-18','2027-08-08','Session 3 · 3 недели','USD 8 800 / после Dec 1 8 400 · подтвердить'),('2027-08-08','2027-08-29','Session 4 · 3 недели','USD 6 700 / после Dec 1 7 100')]
    rows += [(s, e, lab,'USD '+fee) for s, e, lab, fee in [('2027-06-06','2027-07-18','Sessions 1–2 · 6 недель','11 800 / 12 000'),('2027-06-27','2027-08-08','Sessions 2–3 · 6 недель','12 600 / 12 800'),('2027-07-18','2027-08-29','Sessions 3–4 · 6 недель','11 800 / 12 000'),('2027-06-06','2027-08-08','Sessions 1–3 · 9 недель','14 600 / 14 800'),('2027-06-27','2027-08-29','Sessions 2–4 · 9 недель','14 600 / 14 800'),('2027-06-06','2027-08-29','Sessions 1–4 · 12 недель','16 700 / 16 900')]]
    dates(p, rows, fr)
    p=put('frenchwoods-trial','French Woods Festival · One-Week Trial','США','USA','Hancock, New York · 199 Bouchoux Brook Rd',
        'general, art, sport','boarding','Основной лагерь 7–17; пробная неделя для новых campers; under nine согласовать', en,
        'Короткое знакомство с тем же выбором творческих majors/minors. Пробная страница также упоминает возвращающихся, но таблица 2027 называет Session 5 для новых campers: eligibility подтвердить. Большинство уезжает после субботнего показа; таблица тарифов задаёт конец в воскресенье.',
        '30 августа–5 сентября 2027 по rates; фактический день отъезда в конце пробной недели выбрать отдельно.',
        price(2027,'USD 2 000 early / USD 2 400 после Dec 1.',
            'Пробная пансионная творческая программа; полный состав тарифа подтвердить.', extra,
            'Пробная без указания года-page говорит USD 250 deposit, общая таблица 2027 USD 1 750: применимый trial аванс/возвраты ещё неизвестны. Не складываем оба взноса.'),
        'Пансион 1 неделя; короткий формат не отменяет минимальный возраст и согласование under-nine.', fit('candidate','9–10: кандидат на первую короткую творческую смену.'), fit('conditional','Только после 7-летия; письменный допуск under nine и готовность к ночёвкам нужны.'),
        'Более мягкая проба общего международного пансиона перед длинными сменами; явная цена отдельного формата.',
        ['Подтвердить минимальный возраст именно Trial, допуск новых / возвращающихся детей, аванс и окончательный день вывоза/transfer.'],
        [src('2027: отдельная пробная цена и даты', fr), src('Пробная программа и другой deposit', fw), src('Возраст основного лагеря', fh), src('Английская лагерная жизнь', fi), src('EWR и перевозка', ft)], status='published_2027', priority=['general','boarding','both'], confirmed=['EN'])
    p['language_evidence_role']='camp_life'
    dates(p,[('2027-08-30','2027-09-05','Session 5 · new campers / Trial','USD 2 000 / после Dec 1 2 400')], fr)

    tq='https://ticcamp.com/faqs'; tr='https://ticcamp.com/robotics'; tc='https://ticcamp.com/tic-dc'; tt='https://ticcamp.com/technology'
    put('tic-robotics','TIC · Robotics & Athletics','США','USA','Washington DC / Maryland / Virginia · кампус курса выбрать',
        'robotics, coding, sport','day','7–15 и завершённый 1-й класс. DC/MD Junior rising 2–5, VA rising 2–4; Senior границы различаются.',
        'Язык полного преподавания прямо не установлен в прочитанных FAQ; EN-сайт и названия кода не доказательство.',
        'Половина дня техника, половина активность. LEGO EV3 — парные/групповые механические задачи; VEX электроника и более сложный код, LEGO прежде рекомендован. Доступ именно VEX младшему отдельно проверить. Страница называет Robot C graphical — фактическую версию ПО уточнить. Два ребёнка делят компьютер, обучение по уровню; ratio4:1 — заявление оператора.',
        'Текущие кампусные страницы описывают 2026; точных смен и прайса 2027 в прочитанном нет.',
        price(None,'Точный базовый тариф выбранного кампуса и следующей смены пока не доказан.',
            'Technology + athletics, конкретные equipment/licences и питание требуют campus confirmation.',
            'Extended Day 15–17:30 и Athletics Specials отдельные опции; обед/перекусы и жильё семьи согласовать. Mutual Aid описан как 1% каждого registration; отдельную обязательную надбавку без invoice не прибавляем.',
            'Применимые registration fee, cancellation и refund terms следующего сезона запросить перед оплатой.'),
        'Дневной лагерь; DC drop-off8–8:30, pickup15:00. Жильё семьи отдельно.',
        fit('conditional','Возраст подходит; rising grade, campus и LEGO/VEX menu2027 подтвердить.'), fit('conditional','Только после 7-летия, завершения Grade 1 и при минимальном чтении; один возраст 7 недостаточен.'),
        'Робототехническая практика с проектами и спортом; полноценный grade gate для младшего и LEGO→VEX переход.',
        ['Подтвердить сезон 2027, классы, EN, тариф и доступ конкретного VEX/LEGO курса на одном кампусе.'],
        [src('Возраст, классы, чтение и сборы', tq), src('LEGO/VEX содержание', tr), src('DC: часы и Junior grade range2026', tc), src('Парная работа и индивидуализация', tt)], priority=['technical'])

    pr='https://ponacka.com/rates-dates/'; pp='https://ponacka.com/wp-content/uploads/2026/09/26-1620-Camp-Ponacka-Info-sheet-2027.pdf'
    pq='https://ponacka.com/frequently-asked-questions/'; ps='https://ponacka.com/our-staff/'
    language='Иностранные campers, в том числе из Мексики, описаны оператором. Прямого обещания полного EN-преподавания / лагерной жизни или ES поддержки в прочитанном нет; языковой допуск подтвердить.'
    programme='Общий outdoor лагерь для мальчиков: плавание, каноэ, парус, спорт, лошади и самостоятельный выбор активностей. Это отдых без устройств, а не робототехника; плавание и неделя каноэ обязательны по описанию оператора.'
    included='Пансион и основная общая программа; состав питания/оснащения подтвердить в invoice.'
    extras='HST сверх базового тарифа; transport, tuck shop и riding lessons не включены в PDF2027. Transfer Pearson возможен по согласованным датам; цену подтвердить. Перелёт/страховка отдельно.'
    deposit='CAD 1 000 аванс, внутри него 300 non-refundable admin fee. До Mar15 возврат 700; Mar15–May1 аванс не возвращают,700 можно зачесть 2028; после May1 возврата fees нет. Balance May1 для July/June1 для August. Аванс повторно к базовой цене не прибавлять.'
    sources=[src('2027: сроки и session eligibility', pr), src('2027PDF: grade gate, fee, доплаты/возвраты', pp), src('Младшее размещение, обязательные активности', pq), src('Международные campers: прежнее подтверждение состава', ps)]
    commonplace='Highland Grove, Ontario · 376 Ponacka Rd · Lake Baptiste'
    p=put('ponacka-oneweek','Camp Ponacka · First Grade One Week','Канада','CAN', commonplace,'general, sport','boarding','Новые мальчики, учившиеся в Grade 1 уже в сентябре 2026; FAQ cabins6–10 не заменяет этот grade gate.', language, programme,
        'Шесть недельных смен 2027: 30 июня–6 июля / 7–13 июля / 14–20 июля / 1–7 августа / 8–14 августа / 15–21 августа.',
        price(2027,'CAD 1 865 + HST / неделя.', included, extras, deposit),
        'Младшие 6–10 в cabins с bunkbeds; showers отдельно, рядом outdoor toilets. Родительского проживания в тарифе нет.',
        fit('unknown','Недельная программа привязана к Grade 1 осенью 2026; класс Матвея неизвестен. Возраст 9–10 не доказывает этот допуск.'), fit('conditional','Кандидат только если уже Grade 1 в сентябре 2026; возраст 6–7 не заменяет класс.'),
        'Короткая проба общего пансиона для младшего с точным школьным условием и документом 2027.',
        ['Подтвердить фактический Grade 1, EN/международный допуск, полный счёт с налогом/transfer и готовность к бытовому формату.'], sources, status='published_2027', priority=['general','boarding'])
    dates(p,[(s, e,'First Grade · 1 неделя','CAD 1 865 + HST') for s, e in [('2027-06-30','2027-07-06'),('2027-07-07','2027-07-13'),('2027-07-14','2027-07-20'),('2027-08-01','2027-08-07'),('2027-08-08','2027-08-14'),('2027-08-15','2027-08-21')]], pr)
    p=put('ponacka-twoweek','Camp Ponacka · Junior Two Weeks','Канада','CAN', commonplace,'general, sport','boarding','Мальчики 7–9 на 1 июля 2027; в 10 лет только впервые записывающиеся', language, programme,
        '30 июня–13 июля / 14–27 июля / 1–14 августа / 15–28 августа 2027. Возраст на 1 июля применяется и к августовским сменам.',
        price(2027,'CAD 3 850 + HST / 2 недели.', included, extras, deposit),'Младшие cabins; отдельные showers и outdoor toilets.',
        fit('conditional','9 лет подходит; если на 1 июля уже 10 — только ребёнок, впервые приезжающий в лагерь.'), fit('conditional','На 1 июля должно уже быть 7; день рождения позднее 1 июля не делает августовский junior автоматически доступным.'),
        'Двухнедельный общий junior с возрастной датой, которую легко упустить при выборе августа.',
        ['Сверить рождения на 1 июля , first-time статус 10-летнего, EN, налог и transport.'], sources, status='published_2027', priority=['general','boarding'])
    dates(p,[(s, e,'Junior · 2 недели','CAD 3 850 + HST') for s, e in [('2027-06-30','2027-07-13'),('2027-07-14','2027-07-27'),('2027-08-01','2027-08-14'),('2027-08-15','2027-08-28')]], pr)
    p=put('ponacka-fourweek','Camp Ponacka · Four-Week Outdoor','Канада','CAN', commonplace,'general, sport','boarding','Мальчики 8–15', language, programme,
        '30 июня–27 июля / 1–28 августа 2027; четырёхнедельный формат — отдельный выбор от младшей группы и пробной недели.',
        price(2027,'CAD 6 550 + HST / 4 недели.', included, extras, deposit),'В 9–10cabins; в 11 и 12–15platform tents. Срок 4 недели требует отдельной готовности.',
        fit('candidate','9–10 в 2027 по возрасту подходит; длительность и язык согласовать.'), fit('later','Минимум 8; в 2027 будет 6–7.'),
        'Длинная ступень самостоятельности после короткого пансиона; здесь нет technical electives.',
        ['Проверить готовность к 4 неделиелям, размещение, EN, полную цену и условия связи.'], sources, status='published_2027', priority=['general','boarding'])
    dates(p,[('2027-06-30','2027-07-27','Outdoor · 4 недели','CAD 6 550 + HST'),('2027-08-01','2027-08-28','Outdoor · 4 недели','CAD 6 550 + HST')], pr)

    dh='https://www.destination-canada.com/'; dr='https://www.destination-canada.com/dates-and-pricing/'
    dc='https://www.destination-canada.com/english-classes/'; df='https://www.destination-canada.com/facilities/'; da='https://www.destination-canada.com/administration/'
    p=put('destination-canada','Destination Canada · International English Summer','Канада','CAN','Ottawa · Carleton University',
        'general, languages, sport','boarding','10–17 по официальному основному описанию',
        'EN прямо и на уроках, и во всех interactions activity teacher со students. Отдельно заявлены 5 часов English instruction / day.',
        'Общий языковой университетский пансион: письмо, разговор, презентации, дебаты, спорт и supervised поездки. Международный speech competition — активность оператора; уровень награды отдельно проверять. Это не robotics/AI курс.',
        '2027: две недели 10–24 или 17–31 июля; три недели 10–31 июля или 17 июля–7 августа; четыре недели 10 июля–7 августа.',
        price(2027,'USD 3 910 / 2 недели;5 425 / 3 недели;6 625 / 4 недели. Валюта USD, не CAD.',
            'Программа; общая facilities/admin описывают residence, питание 3 раза, присмотр, airport transfers и medical insurance CAD 100 000. Эти включения не датированы — закрепить в пакете 2027.',
            'Laundry и отдельные off-campus activities CAD25–50 / week исключены из rates. Optional tours USD175Adventure/595TorontoNiagara/225MontTremblant; extra day USD200. Общая admin обещает regular туры выходного дня в 3/4 недели: сверить с платными 2027, не считать все tours бесплатными.',
            'USD 500 аванс, balance June1. Rates говорит 100%refundable для всех payments, но сроки/исключения полного договора проверить; это не доказанная безусловная страховка отмены.'),
        'University residence:2 студента / room, communal washrooms, supervised. Размещение семьи отдельно.',
        fit('conditional','Только если к выбранному приезду уже 10; в 9 ещё младше минимума.'), fit('later','Минимум 10; в 2027 ещё 6–7.'),
        'Для Матвея после 10 лет: общий английский пансион с точными сроками 2027, ценой в USD и явно платными экскурсиями.',
        ['Подтвердить 10-летие, включения, страховку и трансфер 2027, возвраты и нагрузку 5 часов в день для уже англоязычного ребёнка.'],
        [src('Возраст и язык активностей', dh), src('2027: даты, USD цены, опции и refund statement', dr), src('Пять часов EN и уровни', dc), src('Carleton housing/food', df), src('Общая package/insurance: год не указан', da)], status='published_2027', priority=['general','boarding'], confirmed=['EN'])
    dates(p,[(s, e, lab, fee) for s, e, lab, fee in [('2027-07-10','2027-07-24','2 недели','USD 3 910'),('2027-07-17','2027-07-31','2 недели','USD 3 910'),('2027-07-10','2027-07-31','3 недели','USD 5 425'),('2027-07-17','2027-08-07','3 недели','USD 5 425'),('2027-07-10','2027-08-07','4 недели','USD 6 625')]], dr)

    sw='https://www.cisscanada.com/swallowdale-camp/'; ct='https://www.cisscanada.com/programmes/summer-programmes/city-residential-programmes/ciss-toronto/'
    ce='https://www.cisscanada.com/programmes/summer-programmes/leaership-skills-courses/future-entrepreneurs/'; cb='https://www.cisscanada.com/programmes/summer-programmes/city-residential-programmes/ciss-at-trinity/'
    ch='https://www.cisscanada.com/'; cf='https://www.cisscanada.com/knowledge-base/how-do-i-find-your-dates-and-fees/'
    cprice=price(None,'Прайс 2027 не найден на прочитанных официальных страницах; полного счёта пока нет.',
        'Программа, присмотр, проживание и питание описаны; окончательный пакет, трансфер и страховку уточнить.',
        'Перелёт, прачечная, платные активности, аэропортовые сборы, страховка, налог и регистрационный сбор требуют расчёта.',
        'Ссылка помощи с тарифами показывает статью How do I register? 2022. Новый договор, аванс и условия возврата пока неизвестны.' )
    p=put('swallowdale-forest','CISS Swallowdale · Forest School & Activities','Канада','CAN','Muskoka · Rosseau Lake College · Lake Rosseau',
        'general,science,sport','boarding','8–14; Leader-in-Training 15–16 — отдельная старшая программа',
        'Forest School прямо указывает допуск всех уровней английского. Это занятия на природе. Старые 10 часов ESL в скрытом блоке не подтверждают языковой курс 2027.',
        '10 часов природных занятий и 15 часов других активностей в неделю: экология, местная география, навыки походной жизни, спорт, вода и творчество. Forest School обязателен для 8–14; помощь персоналу в Leader-in-Training только для 15–16.',
        'Общее окно 11–31 июля 2027; заявлены 2–3 недели. Точные даты двухнедельных заездов не показаны; окно не превращаем в одну 21-дневную смену.',
        dict(cprice), '1–4 ребёнка в комнате по возрасту и полу; персонал живёт рядом и обеспечивает круглосуточный присмотр. Три приёма пищи и перекус в день; полотенце и средства гигиены свои.',
        fit('candidate','9–10 подходит; выбрать реальную двух- или трёхнедельную смену и полный пакет 2027.'), fit('later','Минимум 8; в 2027 ещё 6–7.'),
        'Общий международный пансион на природе с окном 2027 и младшей группой с 8 лет; цена и точные двухнедельные заезды ещё неизвестны.',
        ['Получить точную смену, полный тариф и договор, иностранный допуск и язык лагерной жизни.'],[src('Forest School: окно 2027 и жильё', sw), src('Международная политика оператора', ch), src('Ссылка тарифов показывает старую статью регистрации', cf)], status='partial_2027', priority=['general','boarding'], confirmed=['EN'], sessions=[['2027-07-11','2027-07-31']])
    p=put('ciss-ai-lab','CISS Toronto · AI Future Skills Lab','Канада','CAN','Toronto · University of Toronto · городской residence',
        'ai, entrepreneurship','boarding','12–16',
        'Нужен средний или продвинутый английский, эквивалент IELTS 4.0+. Обычные 15 часов английского — другая опция.',
        'Новый курс 2027: 20 часов в неделю, инструменты AI, технологии и командные задачи. Финальный Future Lab Challenge: проблема, решение с помощью AI и презентация. Языки кода, часы программирования/ML и конкретное оборудование не указаны; международный хакатон и продвинутый ML не заявлены.',
        '4–17 июля / 25 июля–7 августа 2027, две недели. Future-Ready Series 2026 с Circuit Stream и IELTS 5.0+ — другая программа.',
        dict(cprice),'Университетское общежитие с присмотром; постельное бельё. Три приёма пищи понедельник–суббота, поздний завтрак и ужин в воскресенье; прачечная платная.',
        fit('later','В 2027 будет 9–10; минимум 12.'), fit('later','В 2027 будет 6–7; минимум 12.'),
        'Будущая англоязычная AI / product ступень, отдельная от нынешних junior лагерей и общего ESL.',
        ['Подтвердить техническую глубину, ноутбук, отбор и полный тариф 2027; сейчас оба младше.'],[src('AI 2027: возраст, EN, две смены, 20 часов', ct), src('Международные программы оператора', ch), src('Полный прайс не найден', cf)], status='published_2027', priority=['technical'], confirmed=['EN'])
    dates(p,[('2027-07-04','2027-07-17','AI Future Lab ·2 недели','2027 цена уточняется'),('2027-07-25','2027-08-07','AI Future Lab ·2 недели','2027 цена уточняется')], ct)
    p=put('ciss-entrepreneurs','CISS at Trinity · Future Entrepreneurs','Канада','CAN','Toronto · Trinity College, University of Toronto',
        'entrepreneurship','boarding','14–18',
        'Средний или продвинутый английский, эквивалент IELTS 4.0+; 20 часов в неделю. Общий английский и Academic & Career Prep с 16 лет — другие опции.',
        'Выявление потребностей, идея, решение и бизнес-план, критическое мышление и проекты. Общение и презентации на английском; результат собственного стартапа или международная победа не обещаны.',
        '4–17 июля 2027, две недели; общее окно Trinity 27 июня–7 августа не заменяет даты Entrepreneurs.',
        dict(cprice),'Один или два ребёнка в комнате, персонал в общежитии, общие санузлы. Три приёма пищи понедельник–суббота, поздний завтрак и ужин в воскресенье; часть экскурсий включена, дополнительные активности платные.',
        fit('later','В 2027 ещё 9–10; минимум 14.'), fit('later','В 2027 ещё 6–7; минимум 14.'),
        'Будущая предпринимательская ступень после инженерной базы; условия отдельного курса показаны явно.',
        ['Подтвердить тариф 2027, глубину проектов, отбор и условия возврата.'],[src('Entrepreneurs 2027: возраст, EN, даты', ce), src('Trinity: часы, жильё, питание, доплаты', cb), src('Новый прайс пока не найден', cf)], status='published_2027', priority=['boarding'], confirmed=['EN'])
    dates(p,[('2027-07-04','2027-07-17','Future Entrepreneurs ·2 недели','2027 цена уточняется')], ce)
