"""Primary programme/grade/price pass for general American camps and Spanish immersion."""
CHECKED = '2026-10-05'
WALT = 'https://www.campwalt.com/'
CH = 'https://campchampions.com/'
WA = 'https://www.campwalden.ca/rates-and-dates/'
NO = 'https://nominingue.com/'
ICO = 'https://www.icomexico.com/'
IN = 'https://interculturacostarica.com/'

def add_americas_v84(add, src, fit, profiles):
    def put(slug, name, iso, place, themes, formats, age, language, programme, dates, price,
            housing, mat, osc, why, questions, urls, status='next_unannounced', confirmed=None,
            role=None, priority=None, sessions=None):
        add(slug, name, {'USA':'США','CAN':'Канада','CRI':'Коста-Рика','MEX':'Мексика'}[iso], iso,
            place, themes, formats, age, language, programme, dates, price, housing, mat, osc, why,
            questions, [src(t,u) for t,u in urls], status=status, confirmed=confirmed or [],
            priority=priority or [], sessions=sessions)
        p = profiles[-1]; p['checked'] = CHECKED
        for s in p['sources']: s['checked'] = CHECKED
        if role: p['language_evidence_role'] = role
        return p
    def fee(year, label, included, extras, deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def details(p, url, records=None, **kw):
        label = kw.pop('label','Смена')
        p['timing']['session_details'] = records or [dict(start=a,end=b,label=label,
            source=url,place=p['place'],price=p['price']['label'],formats=p['formats'],**kw)
            for a,b in p['timing']['sessions']]
    en_unknown = 'Сайт и материалы на английском, но прямого указания языка всей программы в прочитанных текущих страницах нет. EN instruction и поддержку иностранной семьи подтвердить; в фильтр подтверждённого EN не включён.'
    usd_note = 'На странице знак $; USD следует из американского оператора, валюту счёта подтвердить.'
    wurls = [('Даты и тарифы 2027',WALT+'current-families/preparing/'),('Текущие grade/short-session условия',WALT+'about/faqs/')]
    p = put('walt-whitman-pioneer','Camp Walt Whitman · Pioneer','USA','1000 Cape Moonshine Road, Piermont, New Hampshire 03779',
        'general,adventure,sport,art','boarding','Только заканчивающие Grade 1 или Grade 2; возраст цифрами на странице не установлен.',
        en_unknown,'Вводная неделя самостоятельного лагеря: canoe, swimming, climbing, sports, craft, campfire; полноценный robotics/AI курс не заявлен.',
        '25–31 июля 2027; один конкретный Pioneer набор, не две прошлые смены 2026.',
        fee(2027,'USD 2 000 за смену (валюту счёта подтвердить).','Программа и пребывание в лагере; полный состав питания/услуг в цене требует договора.',
            'Дорога, optional activities и все обязательные сборы 2027 не раскрыты в конкретной карточке. '+usd_note,
            'Депозит и отмена 2027 неизвестны; handbook 2026 не новый договор.'),
        'Пансион; опытные counselors живут с детьми. Night-care/питание и room allocation 2027 подтвердить.',
        fit('conditional','2017: вероятно старше типичного Grade 1–2; допустим только при фактическом завершённом классе 1/2. Возраст 9–10 не даёт допуск.'),
        fit('conditional','2020: только после завершения Grade 1 или 2; kindergarten не заявлен, нужен фактический класс.'),
        'Короткая проба пансиона с точным grade gate; подходит не каждому ребёнку этого возраста.',
        ['Завершённый класс каждого, English, внешний приём, питание, трансфер, fees и отмена 2027.'],
        [('Pioneer: grade, дата и цена',WALT+'pioneer-camp/')]+wurls,status='published_2027',sessions=[['2027-07-25','2027-07-31']])
    details(p,WALT+'pioneer-camp/')
    p = put('walt-whitman-regular','Camp Walt Whitman · Regular / Short Sessions','USA','1000 Cape Moonshine Road, Piermont, New Hampshire 03779',
        'general,adventure,sport,art','boarding','FAQ: half/full cabins для текущих Grades 2–3; finishing Grades 4–7 short-session места ограничены. Полный возрастной диапазон не установлен этими страницами.',
        en_unknown,'Спорт, outdoor adventure, creative arts, групповые активности; обычный самостоятельный пансион. Продолжительность и cabin eligibility согласуются отдельно.',
        '2027: Full 27 июня – 12 августа; First 27 июня – 24 июля; Second 25 июля – 12 августа. Second опубликована отдельно, хотя общий FAQ говорит о four-week option.',
        fee(2027,'Full USD 17 600; First 12 150; Second 9 400. Валюту счёта подтвердить.',
            'Пансион и обычная программа; исчерпывающий состав пакета/питания 2027 не раскрыт на rates странице.',
            'Трансфер/спецкурсы/страховка и обязательные сборы требуют текущего расчёта. '+usd_note,
            'Депозит, финальный платёж и договор отмены 2027 в прочитанных страницах не установлены.'),
        'Дети живут с двумя full-time college-age counselors в cabin по FAQ; окончательные cabin/питание/трансфер подтвердить.',
        fit('conditional','2017: сверить класс; для finishing Grades 4–7 short option ограничена местами и cabin configuration.'),
        fit('conditional','2020: regular Grade 2–3 только при соответствующем классе; нельзя переносить Pioneer допуск на regular.'),
        'Известный общий пансион с прозрачными session prices; пригодность семье требует grade и English проверки.',
        ['Классы, конкретная короткая смена/место, язык, все обязательные fees, питание и договор 2027.'],wurls,
        status='published_2027',sessions=[['2027-06-27','2027-08-12'],['2027-06-27','2027-07-24'],['2027-07-25','2027-08-12']])
    details(p,WALT+'current-families/preparing/',records=[dict(start=a,end=b,label=label,source=WALT+'current-families/preparing/',
        place=p['place'],formats=['boarding'],price=price,age=p['age']) for (a,b),label,price in zip(p['timing']['sessions'],
        ['Full Session','First Session','Second Session'],['USD 17 600','USD 12 150','USD 9 400'])])
    p = put('walt-whitman-family','Camp Walt Whitman · Family Camp','USA','1000 Cape Moonshine Road, Piermont, New Hampshire 03779',
        'general,adventure,sport,art','family,boarding','Для всей семьи; детский тариф 4–17, до 3 лет бесплатно. Отдельные активности могут иметь свои ограничения.',
        en_unknown,'Взрослые и дети вместе: water sports, archery, climbing, tennis, craft, hiking и evening games. Семейный отдых, не самостоятельный детский пансион и не международное соревнование.',
        '16–20 августа 2027, 5 дней.',
        fee(2027,'Взрослый USD 1 000; ребёнок 4–17 USD 500; до 3 лет бесплатно. Два взрослых + два ребёнка 4–17 = USD 3 000 до неизвестных доплат.',
            'Семейная cabin и camp programme описаны; исчерпывающий список услуг в тарифе не опубликован.',
            'Перелёт/дорога; включение питания, taxes, трансфера и иные fees подтвердить. '+usd_note,
            'Семейные deposit/refund условия 2027 не опубликованы в прочитанной странице.'),
        'Отдельная семейная cabin с горячей водой, душем и электричеством; родители участвуют и остаются вместе с детьми.',
        fit('conditional','Детский тариф 4–17 соответствует; язык/активности и семейную cabin подтвердить.'),
        fit('conditional','Детский тариф 4–17 соответствует; взрослые остаются с ребёнком, язык и отдельные активности подтвердить.'),
        'Практичный семейный вариант знакомства с пансионом; сумма 3 000 — арифметика опубликованных тарифов, не полный подтверждённый счёт.',
        ['English, питание и supervision детей, полная family quotation, доступная cabin, отмена/перенос.'],
        [('Family Camp 2027, ages/fee/cabin',WALT+'family-camp/')],status='published_2027',priority=['both','general'],sessions=[['2027-08-16','2027-08-20']])
    details(p,WALT+'family-camp/')

    churls=[('Даты, completed grades, fees и cancellation 2027',CH+'dates-rates'),
        ('Cabins, activities и FAQ',CH+'prospective-families/first-time-families/your-first-summer/parent-camper-faqs'),
        ('Международные семьи, в том числе Мексика',CH+'prospective-families/what-makes-cc-special/camper-life-and-traditions/international-community'),
        ('Current-family fees: смешанные 2027/2026 инструкции',CH+'current-families')]
    chinclude='Основные activities/programming, laundry (для longer-than-one-week), uniform (shorts +2 shirts), yearbook и weekly Champ credits. Cabins с counselors; состав питания подтвердить в договоре.'
    chextras='Airport transport за отдельную плату, spirit packs/Surprise Sack, extra Champ credits. Rates называют Campanion optional, current-families — automatic opt-out fee; сумма/отключение требуют подтверждения. Current-families header 2027, текст/resources 2026: transport суммы не перенесены как доказанный прайс 2027.'
    chcancel='Депозит полностью возвратный до 1 декабря, наполовину до 1 февраля; после 1 февраля только rollover на следующее лето, не sibling transfer. Возврат tuition-less-deposit: 91+ дней 75%, 61–90 дней 50%, 31–60 дней 25%, менее 30 дней 0%. Для ровно 30 дней правило не указано: подтвердить. Ранний отъезд/поздний приезд без скидки.'
    place='775 Camp Road, Marble Falls, Texas 78654'
    cpairs=[['2027-06-13','2027-06-19'],['2027-06-20','2027-06-26'],['2027-06-27','2027-07-03'],['2027-07-25','2027-07-31'],['2027-08-01','2027-08-07']]
    p=put('champions-one-week','Camp Champions · One Week','USA',place,'general,sport,adventure,art','boarding',
        'Single 1/2: finishing Grade 3 or younger; Single 3/4/5: finishing Grade 8 or younger. Нижнюю границу one-week уточнить; только для 2/4 weeks явно finishing Kindergarten.',
        en_unknown,'Шесть activity periods в день, более 40 выборов; спорт, water activities, outdoor skills, arts, evening traditions. Tech-free общий пансион, не robotics camp.',
        '2027: 13–19 июня; 20–26 июня; 27 июня – 3 июля; 25–31 июля; 1–7 августа. Grade maximum различается по смене.',
        fee(2027,'USD 2 450 / неделя; USD 400 deposit в счёт курса. Валюту счёта подтвердить.',chinclude,chextras+' '+usd_note,chcancel),
        'Cabin 8–12 детей одного completed grade с 2–3 counselors. Parent visits/phone calls до последнего дня не предусмотрены по FAQ.',
        fit('conditional','2017: Single 1/2 только при completed Grade ≤3; остальные ≤8. Фактический класс неизвестен, EN ещё не доказан.'),
        fit('conditional','2020: minimum one-week grade на rates странице не указан; finishing Kindergarten из 2/4 weeks не переносим автоматически.'),
        'Проба общего пансиона с реальными 2027 датами; grade каждого важнее оценки по возрасту.',
        ['Минимальный completed grade one-week, English, доступность именно выбранной смены, питание, Campanion fee, total и отмена.'],churls,
        status='published_2027',priority=['general'],sessions=cpairs)
    details(p,CH+'dates-rates',records=[dict(start=a,end=b,label=f'Single {i+1}',source=CH+'dates-rates',place=place,formats=['boarding'],
        price='USD 2 450; deposit 400 в счёт tuition',age='Finishing Grade 3 or younger' if i<2 else 'Finishing Grade 8 or younger',
        family_fit=dict(matvey=dict(status='conditional',detail='Completed Grade ≤3 для Single 1/2, ≤8 для остальных; класс/English подтвердить.'),
        oscar=dict(status='conditional',detail='Minimum one-week grade неизвестен; отдельно подтвердить допуск младшего.')),
        availability=dict(status='open',label='Rates показывает Open на дату чтения; конкретное место не подтверждено.')) for i,(a,b) in enumerate(cpairs)])
    regular=[('Double 1','2027-05-30','2027-06-12',4750,'Kindergarten–Grade 11'),('Double 2','2027-06-13','2027-06-26',4750,'Kindergarten–Grade 11'),
        ('Double 3','2027-06-27','2027-07-10',4750,'Kindergarten–Grade 11'),('Double 4','2027-07-11','2027-07-24',4750,'Kindergarten–Grade 11'),
        ('Double 5','2027-07-25','2027-08-07',4750,'Kindergarten–Grade 11'),('Combo D1+D2','2027-05-30','2027-06-26',7250,'Kindergarten–Grade 11'),
        ('Combo D2+D3','2027-06-13','2027-07-10',7250,'Kindergarten–Grade 11'),('Combo D3+D4','2027-06-27','2027-07-24',7250,'Kindergarten–Grade 11'),
        ('Combo D4+D5','2027-07-11','2027-08-07',7250,'Kindergarten–Grade 11'),('Triple Play','2027-07-04','2027-07-24',6350,'Grade 2–11'),
        ('Combo 5','2027-07-04','2027-08-07',8995,'Grade 2–11')]
    p=put('champions-regular','Camp Champions · Two / Four / Longer Weeks','USA',place,'general,sport,adventure,art','boarding',
        '2/4 недели: finishing Kindergarten–Grade 11. Triple Play (3), Combo 5 и six-week: finishing Grades 2–11. Completed grade перед летом, не вывод из года рождения.',
        en_unknown,'Тот же общий tech-free пансион, longer stays с возрастными cabins, water/land sports, art и outdoor experiences. Длины смен — варианты одной программы.',
        '11 явно датированных вариантов 2027. Six weeks: combine any three 2-week sessions, но конкретную комбинацию/непрерывность согласуют; отдельные даты на основе догадки не созданы.',
        fee(2027,'2 недели USD 4 750; 4 недели 7 250; Triple Play 6 350; 5 недель 8 995; 6 недель 10 500. Deposit 800 в счёт курса.',
            chinclude,chextras+' '+usd_note,chcancel),
        'Cabins по completed grade с counselors, родители живут отдельно; longer stays включают weekly laundry.',
        fit('conditional','2017: вероятно grade подходит, но подтвердить фактический completed grade и EN; Grade 2+ для 3/5/6 weeks.'),
        fit('conditional','2020: 2/4 недели только после Kindergarten; 3/5/6 недели только Grade 2+, не по возрасту 6–7.'),
        'Один из вариантов для обоих после проверки grades; 4 недели оценивать по готовности младшего к самостоятельному пансиону.',
        ['Completed grade каждого, язык всей программы, конкретная комбинация, место, питание/Campanion/transfer и полный договор.'],churls,
        status='published_2027',priority=['both','general','boarding'],sessions=[[a,b] for _,a,b,_,_ in regular])
    details(p,CH+'dates-rates',records=[dict(start=a,end=b,label=label,source=CH+'dates-rates',place=place,formats=['boarding'],
        price=f'USD {amount:,}; deposit 800 в счёт tuition',age='Finishing '+grades,
        family_fit=dict(matvey=dict(status='conditional',detail='Completed '+grades+' и English подтвердить.'),
            oscar=dict(status='conditional',detail='Completed '+grades+' обязателен; год рождения не доказывает класс.')),
        availability=dict(status='open',label='Open по опубликованной rates таблице; не подтверждённое место.')) for label,a,b,amount,grades in regular])
    put('champions-family','Camp Champions · Family Weekend','USA',place,'general,adventure,sport,art','family,boarding,day',
        'Семейный формат: 0–3 бесплатно, 4–6 отдельный тариф, 7+ включая взрослых. Оба ребёнка могут быть с родителями; activities имеют свои ограничения.',
        en_unknown,'Семейные water/land activities, creative arts, вечерние camp traditions и общение с directors. Пансион, дневные и off-site варианты.',
        '25–27 сентября 2026 уже прошли; registration deadline 18 сентября. Новые 2027 даты и тарифы не объявлены в этой странице.',
        fee(2026,'Полный weekend/cabin: 4–6 USD 118.06, 7+ 214.40. Saturday/Sunday cabin: 96.34/176.26; Saturday only 63.75/111.56; daily off-site 90.31/170.00. Taxes included; 2027 неизвестен.',
            'Пакет зависит от attendance/housing; опубликован meal/activity schedule. Уточнить полный состав будущего пакета.',
            'Резерв целой cabin только при группе 6+: deposit 499.50 плюс per-person registration price; семья из 4 не получает отдельную cabin автоматически. Своё постельное бельё/полотенца и дорога.',
            'Для 2026 deposit 50/person, 25 для 4–6; включение/зачёт и отмену будущего набора подтвердить.'),
        'Family cabin либо off-site/day посещение; private cabin для четырёх не доказана. Родители остаются с детьми.',
        fit('conditional','Возрастной тариф 7+; новый набор/English неизвестны.'),fit('conditional','Тариф по возрасту на дату будущей смены; новый набор/English неизвестны.'),
        'Короткая семейная проба; архив 2026 не считается открытым набором 2027.',
        ['Новые даты 2027, private/shared cabin для 4, fee/deposit/food, English и отмена.'],
        [('Family Camp: явно 2026, attendance/age prices',CH+'prospective-families/first-time-families/meet-us-in-person/family-camp')],priority=['both','general'])

    walden_lang='Язык всей программы прямо не установлен прочитанной rates страницей; Ontario/English сайт сами по себе не подтверждают EN instruction.'
    waextra='Плюс 13% HST и 3% processing при credit card. Special travel, dental/orthodontics и medical beyond camp health centre отдельно. Foreign rate для семей вне Canada/US может отличаться: не считать гарантированной CAD ценой семьи из Коста-Рики/Мексики.'
    wadeposit='General deposit $ 2 000 в счёт цены; FAQ явно исключает Long Weekend: там full payment. Далее 4 платежа 1 марта/1 апреля/1 мая/1 июня; всё + taxes оплачено к 1 июня. Refund до Oct 1 (уже прошёл), далее до Feb 1 charge 1 000, Feb 1–start 2 000 (1 000 credit). Есть конфликт: поздний CRS paragraph говорит deposits non-refundable for any reason — нужен актуальный договор. HST на cancellation fees.'
    wainclude='Пансион, weekly laundry, t-shirt, baggage handling, tuck и trips; return bus Toronto/Ottawa/Montreal в стандартные opening/closing дни. Special travel отдельно.'
    for slug,name,age,pairs,prices,mat,osc in [
        ('walden-regular','Camp Walden Ontario · Regular','Завершённый Grade 2–10 для July/full; Grade 2–5 для 6-week. Не day camp: декоративный DAY 1 не означает дневной формат.',
            [['2027-07-02','2027-07-29'],['2027-07-02','2027-08-12'],['2027-07-02','2027-08-19']],
            [('July (4 weeks)',10850,'Grade 2–10'),('Six weeks',14150,'Grade 2–5'),('Full (7 weeks)',15400,'Grade 2–10')],
            fit('conditional','2017: проверить completed Grade 2–10/2–5 и waitlist; не гарантировать по возрасту.'),
            fit('conditional','2020: обычный маршрут источника Grade 1 — Long Weekend; regular только если действительно завершён Grade 2+.')),
        ('walden-explorer','Camp Walden Ontario · Explorer','Только заканчивающие Grade 2, не все младшие 7–10 лет.',
            [['2027-07-02','2027-07-15']],[('Explorer (2 weeks)',5425,'Grade 2 only')],
            fit('conditional','2017: при типичном более старшем классе Explorer не подходит; нужен фактический completed Grade 2.'),
            fit('conditional','2020: только completed Grade 2; семейный год рождения не подтверждает допуск.')),
        ('walden-long-weekend','Camp Walden Ontario · Long Weekend','Только заканчивающие Grade 1; finishing Senior Kindergarten пока не допускается.',
            [['2027-07-30','2027-08-02']],[('Long Weekend',1000,'Grade 1 only')],
            fit('conditional','2017: только completed Grade 1; типичный класс старше, не возрастной лагерь 6–10.'),
            fit('conditional','2020: source journey показывает birth2020/Grade1, но фактический Grade1 должен быть подтверждён, не вывод из года.')),
    ]:
        p=put(slug,name,'CAN','Ontario · точный cabin/campus address до поездки подтвердить',
            'general,adventure,sport,art','boarding',age,walden_lang,'Общий overnight camp: уверенность, outdoor experiences, trips, friendships. Короткие входные программы зависят от completed grade.',
            'Summer 2027; registration CLOSED, новым семьям предлагается waitlist. '+('30 июля – 2 августа: rates label «3 days», journey «4 days»; сохраняем даты, не меняем конец.' if 'weekend' in slug else 'Даты отдельных смен указаны в календаре.'),
            fee(2027,'; '.join(f'{label}: $ {amount:,}' for label,amount,_ in prices)+'. CAN/USD и отдельный foreign tariff требуют quotation.',
                wainclude,waextra+' Sibling 5% второму ребёнку только same parents/residence; pay-in-full Sep10 истёк, не применён.',wadeposit),
            'Самостоятельный пансион. Доступность, cabin, питание и внешние admissions требуют подтверждения; мест на сайте не обещают.',
            mat,osc,'Grade-specific общий пансион; важны waitlist, foreign rate и неоднозначный договор отмены.',
            ['Фактический completed grade, admission с waitlist, EN, campus, валюта/foreign fee/taxes, deposit исключение и договор отмены.'],
            [('Summer 2027 dates/rates/grades/waitlist/terms',WA)],status='published_2027',sessions=pairs)
        details(p,WA,records=[dict(start=a,end=b,label=label,source=WA,place=p['place'],formats=['boarding'],
            price=f'$ {amount:,} +13% HST; currency/foreign rate confirm',age='Completed '+grade,
            entry='Регистрация закрыта; новым семьям только waitlist. Место, иностранный допуск и тариф подтвердить у оператора.',
            availability=dict(status='closed',label='Registration Closed; новым семьям только waitlist, место не подтверждено.'))
            for (a,b),(label,amount,grade) in zip(pairs,prices)])

    nourls=[('Sessions: age/grade/price, year not labelled',NO+'sessions-rates-dates/'),
        ('FAQ: camp operates in English, French opportunity',NO+'faq/'),('Calendar header explicitly 2026',NO+'summer-calendar/'),
        ('Own summer 2026 PDF',NO+'wp-content/uploads/2026/03/summer-2026.pdf')]
    nolang='Camp Nominingue operates in English прямо в FAQ. Anglophone дети могут практиковать French с tent-mates/counselor; это возможность общения, не обязательные French lessons.'
    noextra='Валюта/налоги и действующий сезон rates не указаны. Tuck deposit отдельный, остаток возвращается; travel и insurance quote для иностранцев. FAQ insurance $3.50/day относится к 2018 — не прайс 2027.'
    for slug,name,age,programme,label,price in [
        ('nominingue-junior','Camp Nominingue · Junior / Discovery 8 Days','Мальчики 7–10, до Grade 4 по rates; FAQ старее описывает 8-day для 7–9 — конфликт верхней границы надо подтвердить.',
            'Восемь дней tent life, outdoor skills, canoe, campfire cooking и overnight canoe introduction для младших.',
            'На undated rates: 27 июня – 4 июля; 4–11 июля; 25 июля – 1 августа; 1–8 августа. Own calendar явно 2026, не 2027.',
            '$ 1 875 / 8 дней; валюта и новый тариф 2027 неизвестны.'),
        ('nominingue-regular','Camp Nominingue · Regular 12–26 Days','Мальчики: 12 days 7–12/Grade ≤6; 15/19/26 days 7–15/Grade ≤9. Возраст и класс проверяются вместе.',
            'Outdoor instruction, жизнь в tents и canoe trips по возрасту/опыту. 12 days — одна неделя выбора skills; длинные смены дают больше instruction и trip possibilities.',
            'Rates dates без года; calendar 2026. 12 days 11–22 июля/8–19 августа; 15 days 27 июня – 11 июля/25 июля – 8 августа; 19 days 4–22 июля/1–19 августа; 26 days 27 июня – 22 июля/25 июля – 19 августа. Не перенесены в 2027 ICS.',
            '$ 3 090/12 days; 3 690/15; 4 600/19; 5 750/26. Long 40/43/54 days 8 000/8 500/10 500. Валюта/сезон не установлены.'),
    ]:
        put(slug,name,'CAN','1889 Ch. Des Mésanges, Nominingue, Québec J0W 1R0','general,adventure,sport,languages','boarding',
            age,nolang,programme,label,
            fee(None,price,'Программа/жизнь в tents; weekly laundry и feather shield по FAQ, meals описаны. Полный current package подтвердить.',
                noextra,'Текущие deposit/отмена/налоги/финальный платёж не установлены прочитанными страницами.'),
            'Tents; младшие обычно 5 детей с counselor +junior counselor по FAQ. Конкретное распределение/food/trip 2027 подтвердить.',
            fit('conditional','2017: в 2027 будет 9–10; проверить фактический возраст/Grade и конфликт junior9/10, новый набор ещё не опубликован.'),
            fit('conditional','2020: только после 7-летия на начало смены и при подходящем Grade; 6-летний не допускается в boys programme.'),
            'Подтверждённая английская camp life с French exposure; не обещаем уже опубликованное лето 2027.',
            ['Новый датированный 2027 brochure/price, валюта и налог, junior age, класс, foreign admission/insurance, полный договор.'],
            nourls,confirmed=['EN'],role='camp_life',priority=['general','boarding'])
    put('nominingue-family','Camp Nominingue · Family Camp','CAN','1889 Ch. Des Mésanges, Nominingue, Québec J0W 1R0',
        'general,adventure,sport','family,boarding','Семейный формат; adult/child rates, до 3 лет бесплатно. Boys camp minimum 7 не переносится автоматически на family формат.',
        'Boys programme работает на EN по FAQ; отдельная family-page язык activities не подтверждает. Family English/French support согласовать.',
        'Вся семья вместе: canoe excursions, cooking/banquet, evening activities и жизнь в tents; можно часть пребывания.',
        '19–23 августа 2026 по Family странице/own calendar, уже прошли; 2027 dates неизвестны.',
        fee(2026,'Adult $150/day или 520/full; child $100/day или 350/full; до 3 бесплатно. 2 adults+2 children>=4 full = $1 740, валюта/налоги не прописаны.',
            'Tents, meals приготовлены chef; evening snack описан. Состав future package подтвердить.',
            'Дорога/трансфер, taxes и final currency; child cutoff кроме free≤3 уточнить.',
            'Депозит/отмена 2027 неизвестны; 2026 тариф не будущая quotation.'),
        'Семьи живут в tents; full period 4 ночи, родители остаются с детьми.',
        fit('conditional','Family child tariff подходит, но новые даты/язык неизвестны.'),
        fit('conditional','Family children могут быть младше 7; минимальные ages отдельных activities и язык уточнить.'),
        'Семейная альтернатива самостоятельному boys camp; архивный семейный тариф отделён от 2027.',
        ['2027 date/price/currency/taxes, family English, accommodation и отмена.'],
        [('Family 2026 dates/fee/meals/tents',NO+'family-camp/'),('English boys programme scope',NO+'faq/')],priority=['both','general'])

    put('ico-oaxaca-kids','Instituto Cultural Oaxaca · Kids Spanish Summer Camp','MEX','Av. Juárez 909, Centro, Oaxaca, México',
        'general,languages,art','day','5–12; группы 5 лет / 6–8 / 9–12, по Spanish level; до 6 детей в конкретном Kids programme.',
        '100% Spanish, native teachers; все уровни, включая heritage speakers. EN сайта не язык лагеря.',
        'Языковая практика через crafts/music/games, piñatas, mask making и natural dyes; parents adult class в параллельные часы. Для уже Spanish-speaking детей уточнить пользу advanced/heritage curriculum.',
        '1 июня – 21 августа 2026, weekly Mon–Fri 09–13 (20 часов). Уже прошедший сезон; 2027 dates неизвестны, общий FAQ Monday start не доказывает 52 camp weeks.',
        fee(2026,'USD 300/1 week; 560/2; 780/3; 960/4. После 5-й недели указан USD 200/дополнительную, но цена самой 5-й недели не дана.',
            '20 часов/неделя, Spanish games/cultural workshops, все материалы.',
            'Parent tuition, семейное жильё, дорога/food отдельно или неизвестны. Цена 5-й недели требует quote; general FAQ class cap8 не переносится на Kids cap6.',
            'USD 55 deposit/student; balance в первый день. General FAQ: deposit refund до 14 дней до arrival, позже credit на online/future lessons. Применимость к Kids 2027, зачёт в tuition и остальные refunds подтвердить.'),
        'Дневной 09–13; housing семьи и transfer не входят в опубликованный Kids пакет. Родители могут учиться отдельно.',
        fit('candidate','Группа 9–12 по будущему возрасту; новый сезон и level/heritage программу проверить.'),
        fit('candidate','Будет 6–7, подходит группа 6–8; новый сезон и испанский уровень подтвердить.'),
        'Понятный cultural day camp в Мексике для обоих; не technical track и не пансион.',
        ['2027 weekly dates/price, группа/level, 5-я неделя, deposit credit/refund, food и family housing.'],
        [('Конкретный Kids camp: ages/100%ES/2026/cap6/fees',ICO+'kids-spanish-summer-camp'),
         ('General FAQ: deposits и Monday modules',ICO+'frequently-asked-questions'),('Calendar не доказательство Kids 2027',ICO+'calendar')],
        confirmed=['ES'],role='primary',priority=['both','general'])

    inurls=[('Детский camp-style curriculum, age и housing',IN+'family-spanish-immersion-program/'),
        ('Price page: separate2026/2027',IN+'prices/'),('Официальный 2027 price PDF',IN+'wp-content/uploads/2026/06/2027-Price-List-Intercultura-Costa-Rica.pdf'),
        ('Terms2026–7: schedules/payment/refunds',IN+'terms-and-conditions/'),('Heredia apartment under8 restriction',IN+'student-apartments/')]
    ideposit='Standard: USD 150/person classes only, USD 250/person classes+school lodging, в счёт услуги; non-refundable/non-transferable. High season Jan–Mar/Jun–Jul: due8weeks, остальные 4weeks; balance start. Full prearrival cancellation: eligible70% total минус deposit/processing или eligible credit до 1 года; после начала no refund/credit. Kids group сохраняет 20 часов даже при единственном student, adult lone-level hours могут уменьшиться.'
    for slug,city,amount,adult,schedule in [('intercultura-heredia-kids','Heredia',365,345,'Фиксированный AM08:30–12:30 либо PM13:30–17:30; назначает school, morning не гарантирован.'),
        ('intercultura-samara-kids','Playa Sámara',380,365,'MWF08–12/TuTh13–17 либо наоборот. Parent/child same-schedule priority; не обещание неизменного утреннего курса.')]:
        put(slug,'Intercultura · '+city+' Family Kids', 'CRI',city+' campus · точный адрес/room assignment подтвердить',
            'general,languages,art,adventure','day','8–12 (отдельно teens13–17). Placement по возрасту, maturity и Spanish level; школьный Grade не критерий.',
            'Spanish immersion: дети говорят/слышат Spanish в activities/classes. Уроки английского/португальского другого подразделения не язык этого camps-style курса.',
            '20 часов/неделя, 4 часа Mon–Fri: storytelling, games, sports, crafts, treasure hunts, environmental hikes. In-water activities не включены; field trips с transport/entry могут быть доплатой. '+schedule,
            'Прайс 2027 опубликован; weekly course availability требует подтверждения. Точные holiday camp cohorts 2027 не названы, повторяющиеся недели в календарь не выдуманы. Family page ещё показывает 2026 starting price.',
            fee(2027,f'USD {amount}/week ребёнок (20ч). Adult1–4weeks USD{adult}/week отдельно. 3+ family members studying одновременно10%, условия и состав счёта подтвердить.',
                'Kids/teen group20 часов, материалы; общие cultural activities зависят от campus. 20 часов включают два 15 минутных breaks/day.',
                'Parent tuition, housing/food, поездки/transport, insurance отдельно. Homestay private breakfast+dinner+laundry 2027: Heredia245/Sámara265 USD/week. Это не цена размещения всей семьи. Heredia school apartments не допускают детей младше 8, Oscar сюда не подходит.',
                ideposit),
            'Дневной формат с родителями, family lodging отдельно. Heredia student apartment under8 restriction исключает совместное размещение с Оскаром; hotel/Airbnb искать отдельно.',
            fit('candidate','2017:9–10 соответствует 8–12; проверить advanced/heritage Spanish пользу, availability и schedule.'),
            fit('not_eligible','2020:6–7 ниже 8. Общая цена private lessons не подтверждает отдельный camp admission младшего.'),
            'Местный cultural/Spanish вариант для Матвея; не общий лагерь обоим и не робототехника.',
            ['Подтверждённая неделя/advanced level, schedule рядом с parent, total 2027/discount, food/housing отдельно, возраст младшего и refundable amount.'],
            inurls,status='partial_2027',confirmed=['ES'],role='primary',priority=['local','general'])
    put('intercultura-teen-adventure','Intercultura · Teen Spanish & Adventure','CRI','Playa Sámara + excursions · residential placement подтвердить',
        'general,languages,adventure','boarding','13–17 по конкретной Teen Summer programme; детям 6–10 пока недоступно.',
        'Spanish immersion по programme; EN поддержки и язык каждого excursion отдельно подтвердить.',
        'Две недели Spanish, local cultural activities и adventure excursions. Только будущий подростковый маршрут; price alone не подтверждает текущую смену.',
        '2027 price опубликована, dates пока не установлены. Teen page всё ещё 12–26July/26July–9August 2026; не скопированы на 2027.',
        fee(2027,'USD 3 650/2weeks all-inclusive по 2027 price list. Programme page 2026 и PDF 2026 дают разные прежние суммы, новые 2027 terms/date уточнить.',
            'Заявлен all-inclusive пакет, исчерпывающий состав residence/food/transfer/экскурсий на 2027 требует договора.',
            'Flights/insurance и личные расходы подтвердить; families не получают допуск younger child к teen programme.',
            'Group/teen:20% non-refundable deposit due2months; balance2weeks. До deposit no penalty; после deposit/до 2weeks20% удерживается; менее 2weeks full payment/no refund. Не стандартный USD 150 deposit.'),
        'Самостоятельный residential/homestay teen формат; размещение/round-the-clock care конкретного 2027 набора согласовать.',
        fit('later','После 13-летия; ни 2026, ни 2027 возраст не подходит.'),fit('later','Только после 13-летия.'),
        'Будущий Spanish/adventure трек в своей стране проживания; отделён от junior family classes.',
        ['2027 dates/адрес/состав all-inclusive, EN support, foreign admission, contract и emergency/night-care.'],
        [('Teen age/programme: dates2026',IN+'spanish-summer-camp/')]+inurls[:4],status='partial_2027',confirmed=['ES'],role='language_lessons')

def extend_report_v84(report):
    report['shortlist'].extend([
        dict(label='США · самостоятельный общий пансион: сначала completed grade',slugs=['walt-whitman-pioneer','walt-whitman-regular','champions-one-week','champions-regular'],
            reason='2027 даты/стоимость опубликованы. Pioneer только Grade1/2; Champions one-week maximum меняется, 2/4weeks после Kindergarten, longer Grade2+. EN полного курса и иностранный допуск нужно подтвердить.'),
        dict(label='Семья вместе · cabin/tent лагеря Америки',slugs=['walt-whitman-family','champions-family','nominingue-family'],
            reason='Whitman16–20Aug 2027,2adults+2children>=4 =USD 3000 до неизвестных extras/food. Champions/Nominingue family pages пока 2026; не открытые 2027 смены. Family EN и private cabin/tents проверять отдельно.'),
        dict(label='Канада · grade gates, English proof и waitlist',slugs=['walden-regular','walden-explorer','walden-long-weekend','nominingue-junior','nominingue-regular'],
            reason='Walden 2027 только waitlist, foreign rate/CANUSD и EN требуют quotation; Explorer только Grade2, weekend только Grade1. Nominingue English прямо подтверждён, но calendar 2026/undated rates не доказывают 2027.'),
        dict(label='Коста-Рика / Мексика · cultural day camps на Spanish',slugs=['ico-oaxaca-kids','intercultura-heredia-kids','intercultura-samara-kids','intercultura-teen-adventure'],
            reason='Oaxaca5–12 обоим, 2026 архив/новые 2027 dates неизвестны. Intercultura8–12 толькоМатвей,2027 price365/380 USD, adult/lodging отдельно. Teen13–17 позже; не technical лагеря.'),
    ])
    report['gaps'].extend([
        dict(country='США',iso='USA',provider='Whitman / Camp Champions: grade и язык',
            detail='Даты 2027 первично подтверждены, но EN сайтов не доказательство whole-course EN. Grade1/2 Pioneer, one-week Champions maxGrade3/8 и lower-bound unknown;2/4weeks K–11,3/5/6weeks Grade2+. Current-family header 2027 с текстом 2026/Campanion automatic против rates optional.',
            next_action='Текущий invoice/English, actual completed grades, питание, app fee/airport costs и cancellation contract; внешние сообщения не отправлены.',url=CH+'dates-rates'),
        dict(country='Канада',iso='CAN',provider='Walden / Nominingue: закрытая регистрация и год программы',
            detail='Walden Summer 2027 RegistrationClosed/waitlist; 13%HST/3%card, outsideCanada/US tariff mayvary, CAN/US accepted. LongWeekend full-payment exception,3days vs4days labels; refundtiers vs blanketnon-refundable contradiction. Nominingue English confirmed, SummerCalendar explicitly 2026 and rates unlabelled:2027 dates/fees не придуманы.',
            next_action='Реальный admission/English/final foreign quote Walden; датированный 2027 brochure Nominingue и current currency/tax/insurance/cancellation.',url=WA),
        dict(country='Коста-Рика / Мексика',iso='CRI',provider='Intercultura / ICO: прайс не дата и не пансион',
            detail='Intercultura 2027 PDF365/380 USD kids,8–12;Oscar ниже 8/Heredia apartments under8 запрещены. Family page ещё 2026 prices; fixedHeredia/alternatingSamara, deposit150/250 vsTeen20%, adult/housing отдельно. ICO 2026 JuneAug5–12/cap6/100%ES,5thweekpricegap;55deposit/refundgeneralFAQ применимость проверить.',
            next_action='Польза детям с уверенным Spanish, реальные 2027 availability/campdates, quotedrefund/total и жильёсемьи; не генерировать 52weeks без фактических campcohorts.',url=IN+'family-spanish-immersion-program/'),
        dict(country='Бразилия / Чили / Мексика',iso='BRA',provider='Timbalaia / Acampark и повторная сверка существующих операторов',
            detail='Timbalaia Jan 2027 age6–17 и packsBRL2940/2450/5130 прочитаны ownwebreader, прямой 403 сохранён; school-languagegroups не доказывают EN holidaycamp. Acampark Jan17–23/17–20 2027 age5–16, board/5meals/busSãoPaulo/terms primary, но EN/ES и цена неизвестны: не добавлен в ENshortlist. WildRoots/Makemake уже существуют; новыедубликаты не созданы.',
            next_action='Текущая международная EN/ES holiday cohort, stafflanguage/total вместо вывода из PT сайта или schoolgroups; другие LatinAmerica/Europe/Asia приоритеты продолжаются.',url='https://edutretenimento.acampark.com.br/acampamento-de-ferias'),
    ])
