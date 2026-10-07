"""Swiss younger programmes, real winter availability and optional engineering."""
import datetime
import re

def add_deep_swiss(add, src, fit, profiles):
    def put(*a, **k):
        add(*a, **k)
        p=profiles[-1]; p['checked']='2026-10-05'
        for s in p['sources']: s['checked']=p['checked']
        return p
    def fee(year, label, included, extras, deposit, season=None):
        d=dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
        if season: d['season']=season
        return d
    def dates(p, rows, source, day=False, rule=None):
        p['timing']['sessions']=[[s,e] for s,e,lab,price in rows]
        p['timing']['session_details']=[dict(start=s,end=e,label=lab,price=price,place=p['place'],source=source,formats=p['formats']) for s,e,lab,price in rows]
        for v in p['timing']['session_details']:
            if day: v['date_scope']='day_camp_window'
            if rule:
                v.update(date_precision='published_rule',date_status='Опубликованное правило · даты рассчитаны',date_rule=rule)

    nano='https://www.nordangliaeducation.com/college-du-leman/camps/nano-camp'
    p=put('cdl-nano','Collège du Léman · Nano 4–7','Швейцария','CHE','Versoix / Geneva · Collège du Léman',
        'general,art,sport','day','4–7; отдельная младшая программа, старший Summer 8–18 не переносится сюда',
        'English and French spoken прямо указано. Билингвальная лагерная среда; отдельный EN-only поток и английская робототехника не заявлены.',
        'Неделя игр, готовки, творчества, treasure hunts и экскурсии. Осень — Mythical Creatures. Дополнительное летнее плавание: 30 минут три раза в неделю. Это общий младший отдых; курсы робототехники старшего лагеря не включены.',
        'Пн–Пт: 12–16 октября 2026; 5–9 апреля, 28 июня–2 июля, 5–9 июля и 12–16 июля 2027.',
        fee(2027,'Прайс 2026/27: CHF 735 / 1 неделя; 1 365 / 2 летние; 1 970 / 3 летние. CDL Family 700 / 1 300 / 1 880 — только при соответствующем статусе.',
            'Дневная программа, обед и afternoon snack.',
            'Nursery до 18:00: CHF 115 / 230 / 345. Летнее плавание: 115 / 230 / 345. Неделя с обеими опциями 965 до дороги и жилья семьи.',
            'Аванс, отмена и внешнее зачисление по договору выбранной недели; текущая карточка не публикует их полностью.',season='2026/27'),
        'Дневной 09:00–17:00, nursery до 18:00 за доплату. Жильё родителей и трансфер отдельно.',
        fit('not_eligible','В 2026–2027 Матвей старше максимума 7; выбрать старший Discovery/Summer.'),
        fit('candidate','В 2026 будет 5–6, в 2027 6–7: младшая категория подходит; зачисление и поддержка EN уточняются.'),
        'Полезный дневной вариант Оскару во время семейной поездки в Женеву; возраст, недели и опции опубликованы отдельно.',
        ['Согласовать внешнюю запись, точную EN/FR организацию группы, место, отмену и выбранные платные опции.'],
        [src('Nano: возраст, языки, недели, полный прайс опций',nano),src('Тот же Nano на французском','https://www.nordangliaeducation.com/fr/college-du-leman/camps/nano-camp')],
        status='published_2026_27',priority=['general'],confirmed=['EN','FR'])
    p['language_evidence_role']='bilingual'
    dates(p,[(s,e,l,'CHF 735 / неделя; опции отдельно') for s,e,l in [('2026-10-12','2026-10-16','Осень · Mythical Creatures'),('2027-04-05','2027-04-09','Весна · Nano'),('2027-06-28','2027-07-02','Лето · неделя 1'),('2027-07-05','2027-07-09','Лето · неделя 2'),('2027-07-12','2027-07-16','Лето · неделя 3')]],nano,day=True)

    ls='https://lovellcamps.ch/summer-camp/'
    lw='https://lovellcamps.ch/winter-camp/'
    lp='https://lovellcamps.ch/wp-content/uploads/2026/08/Session-Application-202627.pdf'
    p=put('lovell-summer','Lovell Camps · Junior Summer','Швейцария','CHE','Saanen / Gstaad · Rübeldorfstrasse 5',
        'general,languages,sport,art','day,boarding','Junior: вводный блок 5–10, подробный 5/6–10/11; общий приём Junior/Senior 5–15. Точную возрастную группу подтвердить.',
        'Total immersion English прямо описан для летнего лагеря. Французский — отдельный изучаемый язык; не доказательство французского всех активностей.',
        'Плавание, outdoors, спорт, творчество, cooking и выбор двух interest groups, экскурсии и альпийские походы с ночёвкой. Tennis, golf и riding оплачиваются отдельно. Лагерные awards только при 3+ неделях; это внутренняя практика, не международные победы. Самостоятельного робототехнического курса не найдено.',
        '2027: 4–24 июля и 25 июля–14 августа, по 3 недели. Недельные варианты существуют в общем окне 4 июля–14 августа, но отдельные даты/воскресные доплаты надо подтвердить.',
        fee(2027,'3 недели: CHF 6 700 пансион / 4 300 дневной. Недельный вариант 2 600 / 1 800. Registration/extras deposit сверх: CHF 100/нед пансион, 50/нед день.',
            'Уроки, основные программы, оборудование, экскурсии; пансион — room/board, день — обед; camp T-shirt.',
            'Tennis, golf, riding, медицинская страховка, transport, hats, German, личные расходы. После объявленного registration/extras deposit минимум 7 000 / 4 450 за 3 недели до прочих расходов; часть deposit расходуется на pocket money/admin/special programmes, не считать её второй раз.',
            'Registration/extras deposit невозвратный. Дополнительный booking аванс, возвраты и правила summer2027 нужны отдельно; зимний CHF 1 000 сюда автоматически не переносится.'),
        'Junior день или пансион. Day Пн–Пт 08:40–17:45; пансион Вс–Сб, выходные и ночные походы включают отдельную outdoor готовность.',
        fit('candidate','9–10: соответствует Junior; сверить старшую границу и группу.'),
        fit('candidate','6–7: соответствует Junior; отдельно оценить длительность, ночёвки и прогулки.'),
        'Общий EN лагерь для обоих с конкретным 2027 прайсом и длинным пансионным либо дневным форматом.',
        ['Выбрать день/пансион, Junior возраст и походы; уточнить короткую неделю, воскресную доплату, летний договор и весь счёт.'],
        [src('Summer2027: возраст, EN, режим и тарифы',ls)],status='published_2027',priority=['both','general','boarding'],confirmed=['EN'])
    p['language_evidence_role']='camp_life'
    dates(p,[('2027-07-04','2027-07-24','Summer Session 1 · 3 недели','Пансион CHF 6 700 / день 4 300 + registration/extras deposit'),('2027-07-25','2027-08-14','Summer Session 2 · 3 недели','Пансион CHF 6 700 / день 4 300 + registration/extras deposit')],ls)

    winter_en='PDF2026/27 включает языковые уроки на выбор EN или FR. Язык жизни, ski instruction и всех остальных занятий отдельно не установлен; EN summer immersion не переносится на winter.'
    winter_programme='Лыжи/сноуборд, ski pass, плавание, climbing, спорт и экскурсии; примерно до 25 часов на склоне по веб-описанию. Уровни от начинающих до опытных. Afternoon language lessons выбираются вместо альтернативных afternoon activities; не обещаем оба одновременно. Робототехники в winter не найдено.'
    winter_in='Уроки лыж/сноуборда и ski pass; EN/FR lessons на выбор; afternoon programme, питание, supplies, поездки и transport к склону/на экскурсии. Room/board для пансиона, lunches для day.'
    winter_extra='Ски/сноуборд rental и личное оснащение, страховка, airport и door bus, German, pocket money. PDF исключает camp shirts/hats, хотя веб-footer обещает T-shirt: контракт конкретной смены приоритетен. Цены этих статей не опубликованы полностью; all-in итог неизвестен.'
    winter_pay='CHF 1 000 аванс в счёт цены; не прибавляется повторно. Возврат по письменной отмене минимум за 30 дней, balance/extras и медсправка за 30 дней. Невозвратный registration: CHF 100/нед пансион или 50/нед день; часть используется на pocket money при нескольких сменах. Withdrawal/absence не уменьшают fee по PDF; полный договор сверить.'
    winter_sources=[src('Winter2026/27: программа и разница веб-часов',lw),src('Именно Winter2026/27 PDF: 14 недель, цены, закрытые boarding места и состав',lp)]
    weeks=[('2026-12-13','2026-12-19'),('2026-12-20','2026-12-26'),('2026-12-27','2027-01-02'),('2027-01-03','2027-01-09'),('2027-01-10','2027-01-16'),('2027-01-17','2027-01-23'),('2027-01-24','2027-01-30'),('2027-01-31','2027-02-06'),('2027-02-07','2027-02-13'),('2027-02-14','2027-02-20'),('2027-02-21','2027-02-27'),('2027-02-28','2027-03-06'),('2027-03-07','2027-03-13'),('2027-03-14','2027-03-20')]
    for slug,name,formats,label,housing in [('lovell-winter-board','Lovell Camps · Winter Boarding','boarding','CHF 2 600 + 100 registration / неделя','Вс–Сб, комнаты 2–4 ребёнка с санузлом. В PDF для 10–30 января нет boarding spaces; day не закрыт этой пометкой.'),('lovell-winter-day','Lovell Camps · Winter Day','day','CHF 1 900 + 50 registration / неделя','PDF: Пн–Пт 09:00–17:00; веб-страница до 17:30 — часы подтвердить. Жильё родителей, путь и weekend extras отдельно.')]:
        p=put(slug,name,'Швейцария','CHE','Saanen / Gstaad · Rübeldorfstrasse 5','general,languages,sport',formats,
            'PDF2026/27: 5–16, все национальности; boarding веб-блок 5–15. Для 6–10 младшая граница совпадает; старшую уточнить.',
            winter_en,winter_programme,'14 недель 13 декабря 2026–20 марта 2027; пансион Вс–Сб, день Пн–Пт. Для board weeks5–7 прямо отмечено отсутствие мест, в семейный .ics они не входят.',
            fee(2027,label,winter_in,winter_extra,winter_pay,season='2026/27'),housing,
            fit('candidate','9–10: возраст подходит; язык лыжного инструктора и конкретную неделю подтвердить.'),fit('candidate','6–7: возраст подходит; младшая группа, сопровождение и готовность к зимнему формату отдельно.'),
            'Зимний кандидат с настоящей таблицей 2026/27 и открыто отмеченными ограничениями пансиона; EN доказан только для language lessons.',
            ['Проверить возраст/уровень, EN на склоне, физическую готовность, места, rental, insurance/transfer и окончательный winter invoice.'],
            winter_sources,status='published_2026_27',priority=['both','general'],confirmed=['EN','FR'])
        p['language_evidence_role']='language_lessons'
        if formats=='boarding':
            dates(p,[(s,e,'Winter · неделя '+str(i),label) for i,(s,e) in enumerate(weeks,1)],lp)
            for i in [4,5,6]: p['timing']['session_details'][i]['availability']=dict(status='closed',label='Пансион: мест нет по PDF2026/27; дневной формат проверять отдельно')
        else:
            rule='PDF2026/27 публикует 14 недель Вс–Сб и attendance day campers Пн–Пт. Начало day рассчитано как понедельник, конец как пятница каждой опубликованной недели; выходные не включены.'
            rows=[((datetime.date.fromisoformat(s)+datetime.timedelta(days=1)).isoformat(),(datetime.date.fromisoformat(e)-datetime.timedelta(days=1)).isoformat(),'Winter Day · неделя '+str(i),label) for i,(s,e) in enumerate(weeks,1)]
            dates(p,rows,lp,day=True,rule=rule)

    sh='https://www.campsuisse.com/front-page/'
    sp='https://www.campsuisse.com/summer-camp/'
    sr='https://www.campsuisse.com/register-online/dates-and-prices/'
    sq='https://www.campsuisse.com/summer-camp/faq/'
    sl='https://www.campsuisse.com/activities/languages-at-camp-suisse/'
    sd='https://www.campsuisse.com/summer-day-camp/'
    sdr='https://www.campsuisse.com/day-camp-dates-prices/'
    language='EN camp life подтверждён FAQ и Languages: English-speaking camp. FR широко используется. ES/FR/EN — отдельные language courses, не доказательство испанского всей программы. Объём language-page расходится: 15 и 18 часов за 2 недели; summer-page минимум18 — точные часы2027 согласовать.'
    programme='Общий outdoor и языковой лагерь: mountain biking, climbing, archery, glacier, Lake Geneva и культура. За две недели заявлены пять full-day excursions. Группы по возрасту. Самостоятельный курс робототехники не найден; award certificate языка не международная медаль.'
    p=put('camp-suisse-board','Camp Suisse · International Boarding','Швейцария','CHE','Les Crosets · The Télécabine, Route des Crosets 69',
        'general,languages,sport','boarding','7–17 по homepage; точную возрастную группу и дату расчёта подтвердить',language,programme,
        '2027: 19 июня–3 июля; 3–17 июля; 17–31 июля; 31 июля–14 августа. Custom1/3/4 недели возможны, но их отдельный прайс/места не подтверждены.',
        fee(2027,'CHF 4 400 / 2 недели; extra day CHF 320 по актуальной таблице2027.',
            'Full board, 3 meals/snack, activities/admissions/equipment, language classes, bedding, laundry1раз/2нед, care, camper insurance/financial protection и детский Geneva/Aigle transfer в допустимые дни/часы.',
            'Перелёт и transfer вне preferred slots за доплату. Прилёт Geneva09–16, обратный рейс11–17 в FAQ. Parent transfer CHF100/adult описан Geneva→camp→Aigle, не airport round trip. Опциональная профессиональная фотография; применимость страховки к резидентам CR/гражданам MX/RF и исключения подтвердить.',
            'CHF500 невозвратный аванс в счёт цены, balance за4недели. Downloads содержит старые Terms2018; текущие cancellation и insurance policy2027 нужны до оплаты.'),
        'Международный пансион с возрастными группами, house parents и staff; родительское жильё отдельно в Les Crosets/Champéry.',
        fit('candidate','9–10: минимальный возраст подходит; группа и места отдельно.'),fit('conditional','Только после 7-летия; в6лет boarding7+ не допускается. До него есть отдельный day5+.'),
        'Общий EN пансион с опубликованными2027 датами и широким базовым пакетом; младшему важен день рождения.',
        ['Уточнить возраст на старт, language timetable15/18, свободные места, flight slots, страховку по семейному резидентству и актуальный договор.'],
        [src('Возраст7–17','https://www.campsuisse.com/'),src('2027:4смены, цена и включения',sr),src('Программа и excursions',sp),src('EN, трансферы, аванс и страховка',sq),src('EN camp life и конфликт language hours',sl)],
        status='published_2027',priority=['general','boarding','both'],confirmed=['EN'])
    p['language_evidence_role']='camp_life'
    dates(p,[(s,e,'Summer · Session '+str(i),'CHF 4 400 / 2 недели') for i,(s,e) in enumerate([('2027-06-19','2027-07-03'),('2027-07-03','2027-07-17'),('2027-07-17','2027-07-31'),('2027-07-31','2027-08-14')],1)],sr)
    p=put('camp-suisse-day','Camp Suisse · Day 5–17','Швейцария','CHE','Les Crosets · The Télécabine, Route des Crosets 69',
        'general,languages,sport','day','5–17 по отдельной day-page. Мин.7 пансиона не переносится на day.',language,programme+' Наличие и объём отдельных language classes именно в day package подтвердить.',
        'Дневной сезон21июня–13августа2027: можно выбрать день,5дней или custom dates. Это окно доступных вариантов, не единая длинная смена; конкретные дни нужно забронировать.',
        fee(2027,'CHF200/день или1000/5дней. Return minibus CHF20/день; пятидневный пакет+ежедневный bus1100.',
            '08:30–17:30, обед, alpine activities и excursions.',
            'Return minibus из Champéry/Val d’Illiez/Monthey20/день; родители жильё/дорога/питание отдельно. Overnight option120/night включает dinner/evening/bedding/breakfast, но допуск5–6лет к ночёвке не установлен.',
            'Условия day deposit/cancellation и insurance уточнить отдельно: boarding FAQ500 не переносится автоматически на дневной пакет.'),
        'Дневной,08:30–17:30; overnight опцию без подтверждённого младшего допуска не считаем обычным пансионом.',
        fit('candidate','9–10: day5–17 подходит по возрасту.'),fit('candidate','6–7: day5–17 подходит, boarding7+ до дня рождения не подходит.'),
        'Общий EN дневной кандидат для обоих во время альпийской семейной поездки; понятный базовый пакет и сезон2027.',
        ['Выбрать реальные дни, уточнить места, language lessons в day, insurance и возраст ночёвки; посчитать жильё/транспорт всей семьи.'],
        [src('Day: отдельный возраст5–17',sd),src('2027: окно, цены и overnight',sdr),src('EN среда и бытовые правила',sq),src('Язык лагеря и language courses',sl)],
        status='published_2027',priority=['both','general'],confirmed=['EN'],sessions=[['2027-06-21','2027-08-13']])
    p['language_evidence_role']='camp_life'

    gw='https://www.la-garenne.ch/winter-camps/'
    summer='https://www.la-garenne.ch/summer-camps/'
    robotics='https://www.la-garenne.ch/summer/repository/summer_robotics_workshop.pdf'
    extras='Прайс от; rental/equipment, transfer, insurance, optional activities и другие обязательные fee в прочитанной winter-page не раскрыты. Получить полный camp quote; annual school conditions не заменяют winter contract.'
    deposit='Winter deposit/cancellation и полные General Conditions выдаются Admissions; точный аванс и возвраты пока неизвестны.'
    p=put('garenne-super-ski','La Garenne · Super Ski','Швейцария','CHE','Chesières / Villars-sur-Ollon · Chemin des Chavasses 23',
        'general,sport','day,boarding','8–14; минимум intermediate: безопасно и уверенно проходить Swiss red runs',
        'Язык ski instruction и camp life прямо не установлен winter-page; английский сайта не является доказательством.',
        '5 полных лыжных дней в неделю; минимум1неделя. Intermediate red-run gate обязателен именно Super Ski, его не переносим на другие программы школы.',
        '2027:10–16,17–23,24–30января;11–20февраля с+CHF1200;21–27февраля;7–13марта. У Session4/7 начало ошибочно2026 при конце2027: обе спорные строки исключены из точного календаря.',
        fee(2027,'От CHF3 750 дневной /4 400 пансион за1неделю; special11–20февраля +CHF1 200, точное применение к формату подтвердить.',
            'Super Ski programme; полный состав room/board, lift pass и rentals подтвердить.',extras,deposit),
        'Пансион всю неделю; день Пн–Пт09:00–16:00. Special11–20февраля длится10календарных дней, не обычная семидневная смена.',
        fit('conditional','9–10: возраст подходит только при уверенном intermediate red-run skiing.'),fit('later','6–7 в2027: ниже минимума8, даже при лыжном опыте.'),
        'Настоящий спортивный интенсив Матвею при нужном уровне; возраст, ошибочные даты и special supplement показаны явно.',
        ['Подтвердить red-run уровень, EN инструктора, цены/места special, правильный год Session4/7 и all-in winter quote.'],
        [src('Winter2027: Super Ski, skill gate и противоречивые даты',gw)],status='published_2027',priority=['general'])
    dates(p,[(s,e,'Super Ski · '+lab,'От CHF3 750 day /4 400 board'+(' +CHF1 200; применимость уточнить' if s=='2027-02-11' else '')) for s,e,lab in [('2027-01-10','2027-01-16','Session1'),('2027-01-17','2027-01-23','Session2'),('2027-01-24','2027-01-30','Session3'),('2027-02-11','2027-02-20','Session5 · special10дней'),('2027-02-21','2027-02-27','Session6'),('2027-03-07','2027-03-13','Session8')]],gw)
    two=[('2027-01-10','2027-01-23'),('2027-01-24','2027-02-06'),('2027-02-07','2027-02-20'),('2027-02-21','2027-03-06'),('2027-03-07','2027-03-19')]
    for slug,name,age,language,programme,housing,mat,osc,why in [
        ('garenne-english-ski','La Garenne · English + Ski','8–14; минимум2недели; ski groups по уровню, Super Ski red-run gate здесь не заявлен',
         'Подтверждены утренние EN lessons/immersion, но язык лыжных инструкторов и жизни отдельно не установлен.',
         'Малые группы английского утром;4лыжных afternoon +1полный ski day в неделю. Для7–19марта2027 вторая неделя БЕЗЛЫЖ прямо отмечена. Не робототехнический intensive.',
         'День Пн–Пт08:00–16:00; пансион full-time. Минимум2недели, продление4/6/8/10 по запросу.',
         fit('candidate','9–10: возраст подходит; полезность курса EN уже англоговорящему ребёнку оценить отдельно.'),fit('later','6–7: ниже минимума8.'),
         'Зимний язык+спорт для Матвея; последняя мартовская смена имеет меньше лыж, чем другие.'),
        ('garenne-integration','La Garenne · Winter School Integration','5–14; минимум2недели; класс, академическая группа и внешний допуск отдельно',
         'Язык конкретной школьной секции и всех занятий не установлен winter programme; EN/FR summer lessons не доказывают зимний academic stream.',
         'Проба постоянной международной школы: ребёнок входит в regular classes и школьное расписание, плюс минимум2ski sessions/нед. Для7–19марта вторая неделя БЕЗЛЫЖ. Это школьная интеграция, не полностью каникулярная программа и не подтверждённое зачисление на учебный год.',
         'День Пн–Пт08:30–16:00; пансион full-time, минимум2недели.',
         fit('conditional','9–10: возраст подходит; нужен класс, уровень и приём в regular classes.'),fit('conditional','6–7: возраст подходит; младший класс/язык/boarding readiness подтвердить.'),
         'Вариант проверки новой школы для семьи, рассматривающей переезд; учебная нагрузка и цель отличаются от обычного лагеря.')]:
        p=put(slug,name,'Швейцария','CHE','Chesières / Villars-sur-Ollon · Chemin des Chavasses 23','general,languages,sport','day,boarding',age,language,programme,
            '2027:10–23января;24января–6февраля;7–20февраля;21февраля–6марта;7–19марта. Последняя смена13календарных дней, вторая неделя без ski.',
            fee(2027,'От CHF7 500 день /7 950 пансион за2недели; мартовский короткий вариант и полный invoice подтвердить.',
                'Выбранная English+Ski либо Integration programme; детальный состав тарифа не раскрыт.',extras,deposit),housing,mat,osc,why,
            ['Подтвердить программу, внешний допуск, уровень/класс, EN на склоне и в группе, отсутствие skiing во второй мартовской неделе и полный quote.'],
            [src('Winter2027: отдельные программы, тарифы и март без ski',gw)],status='published_2027',priority=['general'],confirmed=['EN'] if slug=='garenne-english-ski' else [])
        if slug=='garenne-english-ski': p['language_evidence_role']='language_lessons'
        dates(p,[(s,e,'Session'+str(i)+(' · вторая неделя без ski' if i==5 else ''),'От CHF7 500 day /7 950 board · точный пакет уточнить') for i,(s,e) in enumerate(two,1)],gw)

    p=put('garenne-robotics-workshop','La Garenne · Robotics Workshop Option','Швейцария','CHE','Chesières / Villars-sur-Ollon · летний лагерь La Garenne',
        'robotics,coding,science','day,boarding','PDF:8–12; menu Summer2027: Extras10–12. Допуск8–9 противоречивый, требует подтверждения.',
        'Утренние языковые уроки EN/FR не доказывают английский robotics workshop; преподаватель и поток технических занятий ещё не подтверждены.',
        'Дополнительный workshop: VEX IQ, sensors/motors, командные задачи; Fusion360/Tinkercad и Bambu3Dprinting. VEXV5 — только по возрасту/опыту; наличие Arduino в комнате не обещает отдельный Arduino курс. Python game дан как пример темы. Итог — DIYBluetooth speaker с печатным корпусом и circuit board. Completion certificate не международная награда. Заголовок PDF и меню говорят3sessions, финал PDF2: часы/объём ещё уточнить.',
        'Опция связана с меню Summer2027; PDF без года. Отдельные даты workshop не опубликованы и не копируются с дат общей смены.',
        fee(None,'Стоимость технической опции неизвестна; базовая цена общего лагеря не равна полной цене robotics.',
            'Содержание из PDF; включение equipment, материалов/готового speaker и certificate в доплату уточнить.',
            'Базовый летний лагерь, дополнительный workshop, transfer/insurance и другие опции считать отдельно по quote2027.',
            'Точные payment/refund terms summer2027 для выбранного пакета и workshop нужны отдельно.'),
        'Короткая опция внутри day/boarding общего лагеря; самостоятельный недельный инженерный пансион не подтверждён.',
        fit('conditional','До10-летия PDF допускает8–9, но menu10+ — нужно письменное подтверждение. После10-летия обе границы подходят.'),
        fit('later','6–7в2027 ниже обоих опубликованных минимумов8/10.'),
        'Предметное знакомство Матвея с VEX и 3D-дизайном; объём короткий и условия8–9/EN/цены ещё открыты.',
        ['Уточнить возраст8–9, year/current syllabus,3или2sessions и часы, ENtechnical instruction, точные workshop dates, доплату и project materials.'],
        [src('Summer2027: menu Extras10–12 и ссылка PDF',summer),src('Workshop PDF:8–12, VEX,3D/Python и противоречивое число занятий',robotics)],status='partial_2027',priority=['technical'])

    # Correct one existing claim using the new official PDF; do not pretend 8–9 is settled.
    old=next(q for q in profiles if q['slug']=='la-garenne')
    old['programme']='Языки, спорт, творчество и поездки. Robotics & 3D Design — короткая опция: menu2027 Extras10–12, связанный PDF8–12. Допуск8–9 требует подтверждения. Заголовок/меню3sessions, финалPDF2; часы неизвестны. Не двухнедельный инженерный интенсив.'
    old['questions'].append('Сверить расхождение возраста8–12/10–12 и объёма3/2sessions; технический workshop EN не подтверждён.')
    old['sources'].append(dict(title='Workshop PDF: возраст/объём расходятся с menu',url=robotics,checked='2026-10-05'))
    old['checked']='2026-10-05'

    # Space human-readable values only; never modify URLs, dates, enums or CSV themes.
    def prose(s):
        s=re.sub(r'(?<=\d)(?=[А-Яа-яЁё])|(?<=[А-Яа-яЁё])(?=\d)', ' ', s)
        s=re.sub(r'\b(CHF|PDF|Summer|summer|Winter|winter|Session|Extras)(?=\d)',r'\1 ',s)
        return s.replace('VEXV5','VEX V5').replace('DIYBluetooth','DIY Bluetooth').replace('БЕЗЛЫЖ','без лыж')
    for q in [x for x in profiles if x['id']>='CP153']+[old]:
        for k in ['age','language','programme','accommodation','editorial_reason']:q[k]=prose(q[k])
        q['timing']['label']=prose(q['timing']['label'])
        for k in ['label','included','extras','deposit']:q['price'][k]=prose(q['price'][k])
        q['questions']=[prose(s) for s in q['questions']]
        for f in q['family_fit'].values():f['detail']=prose(f['detail'])
        for v in q['timing'].get('session_details',[]):
            for k in ['label','price','date_rule']: 
                if k in v:v[k]=prose(v[k])
