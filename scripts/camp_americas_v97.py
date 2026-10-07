"""Bounded first-party America programme audit, not admissions or a world ranking."""
CHECKED = '2026-10-05'
NEW = ['pali-general','pali-mini','pali-robotics','wenonah-regular','wenonah-one','wenonah-five','wenonah-wee',
       'sciencequest-kinder','sciencequest-junior','sciencequest-engineering','sciencequest-robotics',
       'sfu-elite-engineers','sfu-brick-builders','sfu-digital-defenders','sfu-wattson',
       'calgary-early-engineering','calgary-early-technology','calgary-engineering101','calgary-winter']
UPDATED = []
PALI = 'https://paliadventures.com/'
W = 'https://campwenonah.com/'
Q = 'https://sciencequest.ca/'
SFU = 'https://sciencealive.ca/'
UC = 'https://activelivingportal.ucalgary.ca/'

def add_americas_v97(add, src, fit, profiles):
    def emit(*args, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1];p['checked'] = CHECKED
        for s in p['sources']:s['checked'] = CHECKED
        return p
    day = 'Дневной лагерь; семейное жильё, международная дорога и ежедневное сопровождение отдельно.'
    grade = fit('unknown','Допуск по фактическому классу. Класс ребёнка не известен; год рождения и опыт соревнований не заменяют школьное условие.')
    en_unknown = 'Язык преподавания, минимальный английский и индивидуальный иностранный приём не установлены по прочитанным страницам. Английский сайт не доказывает английского преподавателя.'
    currency = 'Символ $ на странице; валюта лагерного счёта прямо не названа в прочитанных условиях и требует подтверждения.'
    unknown_terms = 'Аванс, отмена, налоги, медицинские условия, места и итоговый договор выбранной смены ещё неизвестны. Формы не отправлялись.'

    regular = [['2027-06-13','2027-06-19'],['2027-06-20','2027-06-26'],['2027-06-27','2027-07-03'],['2027-07-04','2027-07-10'],['2027-07-11','2027-07-17'],['2027-07-18','2027-07-24'],['2027-07-25','2027-07-31'],['2027-08-01','2027-08-07'],['2027-08-08','2027-08-14']]
    mini = [['2027-06-13','2027-06-16'],['2027-06-20','2027-06-23'],['2027-06-27','2027-06-30'],['2027-07-04','2027-07-07'],['2027-07-11','2027-07-14'],['2027-07-18','2027-07-21'],['2027-07-25','2027-07-28'],['2027-08-01','2027-08-04'],['2027-08-08','2027-08-11']]
    pali_lang = ('Иностранные семьи приветствуются. Связанные ES/RU страницы описывают лето 2023 и практику английского с детьми, не обучение на испанском/русском. '
                 'Прямое актуальное подтверждение языка преподавания каждого трека 2027 и минимального уровня английского пока отсутствует.')
    pali_terms = ('FAQ 2027: cancellation insurance $150 / неделю / ребёнка только при записи. С ним отмена до 01.02.2027 — 100%, до 01.03 — 75%, до 01.04 — 50%; после 01.04 возврата нет. '
                  'Без этой страховки FAQ допускает возврат только при её покупке; смену можно поменять при наличии места. Граничный день 1 апреля, страховой договор, аванс/баланс и применимость к Mini отдельно подтвердить.')
    p_sources = [src('Девять общих смен 2027 и состав пакета',PALI+'dates-enrollment/'),src('Сезон 2027 и отдельные даты Mini',PALI+'whats-new/'),src('Возраст, жильё, питание и отмена 2027',PALI+'about/faqs/'),src('Иностранные семьи',PALI+'about/international-families/'),src('ES описание всё ещё 2023',PALI+'about/international-families/spanish/'),src('RU описание всё ещё 2023',PALI+'about/international-families/russian/')]
    p = emit('pali-general','Pali Adventures · General / выбор специальности','США','USA','Running Springs · San Bernardino, California',
        'general,sport,art','boarding','Основной camp 8–16; широкий homepage 6–16 включает отдельный Mini',pali_lang,
        'Утром одна выбранная specialty, после обеда разные electives, вечером общие игры. Темы недели — оформление отдыха, не самостоятельные инженерные курсы. Robotics 8–16 разобран отдельно: доступность выбранного трека на нужной неделе не подтверждена.',
        'Девять смен 2027: 13–19 / 20–26 июня / 27 июня–3 июля; 4–10 / 11–17 / 18–24 / 25–31 июля; 1–7 / 8–14 августа. Семь дней, шесть ночей.',
        dict(year=2027,label='Текущий Fall Promo $2 750 / обычную смену; не цена Mini. '+currency,
            included='По общей странице: активности, питание, проживание и программа; electives/specialties без добавочного сбора.',
            extras='Страховка отмены $150 / неделю / ребёнка: условно $2 900 с ней до неизвестных налогов/трансфера/дороги/личных покупок. Скидка siblings без конкретного размера. Header: до 23 октября без года; это не точный регистрационный deadline. Early Bird до 28 сентября в news уже истёк.',deposit=pali_terms),
        'Пансион; FAQ: десять детей и два сотрудника в комнате, душ/санузел, отопление. Это заявление оператора. Для основных участников звонки/визиты не рекомендуются, письма разрешены.',
        fit('candidate','В 2027 будет 9–10, входит в основной 8–16; готовность к самостоятельному пансиону и выбранный трек отдельно.'),fit('later','В 2027 будет 6–7, ниже основного 8; отдельный Mini 6–8, без автоматического допуска к обычному лагерю.'),
        'Общий многопрофильный пансион Матвею; одна площадка с отдельной младшей программой Оскару.',
        ['Прайс и валюта 2027, язык teachers, доступность специальности, международный приём, аэропорт и политика контактов/отмены.'],p_sources,
        status='published_2027',priority=['general','boarding'],sessions=regular)
    p['timing']['session_details']=[dict(start=a,end=z,label='Обычная смена · семь дней / шесть ночей',price='$2 750 текущий promo обычной смены, валюта/договор подтвердить',place=p['place'],source=PALI+'dates-enrollment/') for a,z in regular]
    emit('pali-mini','Pali Adventures · Mini first sleepaway','США','USA','Running Springs · California',
        'general,sport,art','boarding','6–8',pali_lang,
        'Короткое первое знакомство с пансионом: природа, вода, творчество, кулинария, магия и отдельные научные опыты. Четыре блока в образце дня; полноценная выбранная specialty Robotics не обещана. До 50 детей; заявлены три сотрудника на девять детей в комнате, не независимая оценка качества.',
        '2027 подтверждён разделом What’s New: Mini во всех девяти сессиях. 13–16 / 20–23 / 27–30 июня; 4–7 / 11–14 / 18–21 / 25–28 июля; 1–4 / 8–11 августа. Четыре дня / три ночи.',
        dict(year=2027,label='Отдельный тариф Mini не найден. $2 750 общей недельной программы не применён к четырём дням.',included='Есть образец дня с питанием и ночёвкой, но состав оплаченного Mini-пакета ещё подтвердить.',extras='Трансфер, налоги, страховка, международная дорога и личные расходы неизвестны.',deposit='Условия общего FAQ не приняты автоматически за договор Mini: '+pali_terms),
        'Отдельная младшая программа и персонал; три ночи, поддержка при первом расставании с родителями по описанию оператора.',
        fit('not_eligible','В 2027 будет 9–10, старше максимума Mini 8; смотреть основной camp.'),fit('candidate','В 2027 будет 6–7, входит в Mini 6–8; самостоятельность, язык и приём подтвердить.'),
        'Короткий первый пансион Оскару, пока Матвей может быть в общей программе с другим сроком забора.',
        ['Получить именно Mini-счёт/договор/язык, ночной надзор, родительскую связь и аэропорт; согласовать разные даты окончания с Матвеем.'],
        [src('Младший возраст, содержание и девять интервалов',PALI+'mini-camp/')]+p_sources,status='published_2027',priority=['general','boarding'],sessions=mini)
    emit('pali-robotics','Pali Adventures · Robotics morning specialty','США','USA','Running Springs · California',
        'robotics,coding,technology','boarding','8–16',pali_lang,
        'Отдельная утренняя специальность внутри общего лагеря: механика/шестерни/моторы, sumo, робот-футбол, VEXcode, датчики цвета/расстояния, автономный лабиринт и итоговая rescue mission. Часы, точная VEX-платформа, язык блоки/text, входной уровень и вынос техники не опубликованы. Внутренние задачи не результат официальной мировой лиги.',
        'Общие смены Pali 2027 известны, но недельная доступность Robotics не опубликована в прочитанной странице. Девять общих дат не продублированы как гарантированные Robotics-смены.',
        dict(year=2027,label='Специальности входят в общую стоимость; базовый текущий promo $2 750 требует подтверждения выбранной Robotics-недели. '+currency,included='Нет добавочного сбора за specialty по общей странице; остальной день общелагерный, не непрерывный курс робототехники.',extras='Те же неизвестные налоги/дорога/трансфер и $150 страхования отмены; технику домой не обещают.',deposit=pali_terms),
        'Общий Pali-пансион, не отдельный технический кампус.',fit('candidate','9–10 в 2027 входит в Robotics 8–16; проверить подходящую учебную подгруппу с учётом прежнего опыта.'),fit('later','6–7 в 2027 ниже Robotics 8; Mini не даёт автоматического допуска.'),
        'Содержательный инженерный кандидат Матвею с международной семейной поездкой, если подтвердят неделю и язык преподавателя.',
        ['Доступные Robotics-недели 2027, часы, VEX-платформа, язык, уровень группы/учителя, проект и сезонный счёт.'],
        [src('Прямой syllabus Robotics и возраст',PALI+'specialty/robotics/'),src('Реестр специальностей',PALI+'camp-programs/specialties/')]+p_sources,priority=['robotics'])

    wenonah_lang = 'Прямо подтверждено: вся лагерная жизнь и всё преподавание на английском; ребёнок должен комфортно понимать базовый английский. Французский/испанский у отдельных людей возможен, но оператор его не обещает.'
    wterms = ('Regular: остаток до 1 апреля 2027; аванс внутри стоимости, не доплата. Priority требовал полную оплату до 1 октября 2026 и уже не применён. '
              'Отмена до 30 января 2027: удержание $75 / неделю / ребёнка; 1 февраля–1 апреля: $150 / неделю; после 1 апреля возврата нет. Граница 30–31 января не описана. '
              'Ранний отъезд/опоздание/тоска по дому без возврата; болезнь/травма в лагере — пропорциональный кредит следующего сезона. Card/eCheck processing fee без суммы, правила коротких смен отдельно подтвердить.')
    wextras = ('13% HST добавляется к лагерной цене. Расчёт с HST не полный бюджет: есть processing fee, опциональный camp bus/покупки/международная дорога/страхование. '
               'Для приезжающих из-за границы заявлен бесплатный трансфер из Toronto Pearson и возможность приехать на день раньше; цену ранней ночи, обратную дорогу и условия коротких смен уточнить. Airline unaccompanied-minor fee лагерь не оплачивает.')
    wsources=[src('Таблица 2027, возраст на 31 декабря, налоги и отмена',W+'2027-dates-fees/'),src('Прямой английский и иностранные участники',W+'welcome-international-campers/'),src('Содержание и выбор занятий',W+'activities/'),src('Надзор, комнаты и распорядок',W+'faq/'),src('Различающиеся возрастные формулировки homepage',W)]
    for slug,name,age,programme,dates,fee,total,deposit,mat,osc,extraurl in [
        ('wenonah-regular','One Month / Two Weeks','9–15 на 31.12.2027; homepage body 8–15 расходится с таблицей 2027','Природа, вода, canoe/sailing, спорт, искусство и выбор личных PIC-занятий. 25+ активностей по заявлению оператора; робототехника/AI не объявлены.',[['2027-07-04','2027-07-31'],['2027-08-01','2027-08-28'],['2027-07-04','2027-07-17'],['2027-07-18','2027-07-31'],['2027-08-01','2027-08-14'],['2027-08-15','2027-08-28']],'$6 350 / месяц или $3 650 / две недели','$7 175,50 / месяц или $4 124,50 / две недели','$1 600 / месяц, $800 / две недели',fit('candidate','2017 даёт 10 лет к 31.12.2027, входит в 9–15.'),fit('later','2020 даёт 7 к 31.12.2027, ниже 9; посмотреть Period Five/WEEnonah.'),None),
        ('wenonah-one','Wenonah One','8–12 на 31.12.2027','Короткое общее знакомство: outdoor, вода, искусство, спорт и друзья. Не технический интенсив; фактический выбор PIC зависит от introductory period, не переносим весь месячный выбор на неделю.',[['2027-07-04','2027-07-10'],['2027-07-11','2027-07-17'],['2027-08-01','2027-08-07'],['2027-08-08','2027-08-14']],'$1 960 / семь дней / шесть ночей','$2 214,80','$400',fit('candidate','2017 → 10 на конец 2027, входит в 8–12.'),fit('later','2020 → 7, ниже 8; не обычная недельная программа.'),None),
        ('wenonah-five','Period Five','7–12 на 31.12.2027','Пять дней / четыре ночи знакомства с общим лагерем: природа, игры, вода, arts/crafts и любимые активности в группе. Робототехника не заявлена.',[['2027-08-30','2027-09-03']],'$1 300 / пять дней','$1 469 ребёнку; $2 938 двум','$400',fit('candidate','2017 → 10 к 31.12.2027, входит в 7–12.'),fit('candidate','2020 → 7 к 31.12.2027, соответствует явному правилу года даже при шести в августе. Индивидуальный допуск отдельно.'),'odyssey-period-five/'),
        ('wenonah-wee','WEEnonah','5–7 на 31.12.2027 и минимум 5 в начале; homepage body 5–6 расходится с таблицей 5–7','Первый короткий пансион: три дня / две ночи, canoe, arts/crafts, archery, костры и игры в младшей группе. Не курс роботов.',[['2027-08-30','2027-09-01']],'$500 / три дня','$565','Таблица $100, Registration Policies $75 — явное расхождение',fit('not_eligible','2017 → 10 к 31.12.2027, выше 7.'),fit('candidate','2020 → 7 к 31.12.2027 и уже старше 5 в августе, входит в текущую таблицу.'),'weenonah/')]:
        p=emit(slug,'Camp Wenonah · '+name,'Канада','CAN','Muskoka · Bracebridge, Ontario','general,sport,art','boarding',age,wenonah_lang,programme,
            'Сезон 2027: '+'; '.join(a+' — '+z for a,z in dates)+'. Даты подтверждены, место не удерживается без заявки/аванса.',
            dict(year=2027,label='Regular: '+fee+'. С обязательным HST: '+total+'. '+currency,
                included='Лагерная программа; Tuck Shop snacks/drinks и framed cabin photo по fee page. Прачечная только для двух недель/месяца. Полный состав питания/медицинского пакета выбранного краткого трека подтвердить.',
                extras=wextras,deposit='Аванс: '+deposit+'. '+wterms),
            'Пансион. Общий FAQ: 8–10 детей с двумя сотрудниками в комнате, ratio 5:1 по заявлению оператора; точный надзор младших треков уточнить. Разница рождения детей три года не соответствует cabinmate request ≤18 месяцев, одну комнату не обещают.',mat,osc,
            'Английский общий пансион с прямым иностранным приёмом; короткие ступени дают выбор по возрасту, а не только по бренду.',
            ['Подтвердить валюту, итог с HST/processing fee, аванс, места, короткий международный трансфер/раннюю ночь/обратную дорогу, питание/страхование и ночной надзор.'],
            wsources+([src('Отдельная младшая/короткая программа',W+extraurl)] if extraurl else []),status='published_2027',priority=['general','boarding'],confirmed=['EN'],sessions=dates)
        p['timing']['session_details']=[dict(start=a,end=z,label='Четыре недели' if slug=='wenonah-regular' and i<2 else 'Две недели' if slug=='wenonah-regular' else name,price=('$6 350 + 13% HST = $7 175,50' if i<2 else '$3 650 + 13% HST = $4 124,50') if slug=='wenonah-regular' else fee+'; с HST '+total,place=p['place'],source=W+'2027-dates-fees/') for i,(a,z) in enumerate(dates)]

    qdates=[['2026-06-29','2026-07-03'],['2026-08-03','2026-08-07']]
    qterms=('Архив 2026: $100 невозвратного аванса внутри платы за каждую неделю; остаток до первого дня. Отмена >5 рабочих дней — возврат без аванса; <5 дней — полная плата, кроме случая по решению оператора; <24 часов без возврата. '
            'Граница пяти дней/разница business days и days не уточнена. При отмене оператором — полный возврат с авансом или кредит, смена недели без сбора при местах. Не договор 2027.')
    for slug,name,age,programme,fee,shortfee in [
        ('sciencequest-kinder','Kinder Creators','SK–Grade 1','Научные эксперименты начального уровня; coding и алгоритмы через физические игры, без программирования за компьютером.',350,280),
        ('sciencequest-junior','Junior Thinkers','Grades 2–3','Наука и инженерия через задания, связь с реальным миром; алгоритмы руками, компьютерного coding младшего трека не обещают.',350,280),
        ('sciencequest-engineering','Engineering Science & Tech','Grades 4–8','Инженерный цикл, проверка гипотез, эксперименты, часть работы в computer lab. Отдельная Robotics содержит больше времени с кодом/роботами.',330,264),
        ('sciencequest-robotics','Robotics','Grades 4–8','Конструирование, код и энергия роботов: Jade, LEGO Mindstorms/EV3, Sphero, Ozobot и MicroBit. Выбор платформы/часы/продвинутый уровень и технику домой не гарантируют.',365,292)]:
        p=emit(slug,'Science Quest · Queen’s · '+name,'Канада','CAN','Queen’s University · Kingston, Ontario','science,technology'+(',robotics,coding' if slug=='sciencequest-robotics' else ',coding' if slug=='sciencequest-engineering' else ''),'day',age,en_unknown,
            programme+' Четыре повторяющиеся темы Space/City/Ocean/Spy, задачи меняются по уровню. Темы не четыре независимых международных лагеря. Университетская площадка не обещает профессоров или университетский зачёт.',
            'Сайт прямо называет 2026 завершённым, обновления 2027 ожидаются. Две архивные четырёхдневные недели: 29 июня–3 июля без Canada Day и 3–7 августа без Civic Holiday. День 09–16, продление 08–09 / 16–17; новые недели не выдуманы.',
            dict(year=2026,label=f'Архив 2026: ${fee} / обычную неделю, ${shortfee} / четырёхдневную. Не цена 2027. '+currency,
                included='Обучение/занятия; полный список материалов, налоги и дальнейший проект подтвердить.',
                extras='Обычная неделя: before или after $25, оба $40; четырёхдневная $20 каждое / оба $35. Hot lunch отдельно у Grocery Checkout, заказ до полуночи предыдущей субботы; цена неизвестна. Жильё семьи/дорога отдельно.',deposit=qterms),day,grade,grade,
            'Разные реальные школьные ступени одного STEM-оператора; лето 2027 и подходящий класс ещё установить.',
            ['Сезон 2027: даты/цены, фактический класс, язык учителя, иностранные дети, содержание/часовые нагрузки и договор.'],
            [src('Собственная программа, завершённый сезон, возрастные классы и тарифы',Q+'summer-camp-2/'),src('FAQ и архивные условия',Q+'policies-faqs/')],status='archive_next_unannounced',priority=['robotics'] if slug=='sciencequest-robotics' else [],sessions=qdates)
        p['timing']['session_details']=[dict(start=a,end=z,label='Архив: четырёхдневная неделя, праздник без посещения',price=f'2026: ${shortfee}, не тариф 2027',place=p['place'],source=Q+'summer-camp-2/') for a,z in qdates]

    for slug,name,age,programme,dates in [
        ('sfu-elite-engineers','Elite Engineers','Grade 1','Инженерный цикл, проектирование и базовые конструкции.', [['2026-07-20','2026-07-24'],['2026-08-17','2026-08-21']]),
        ('sfu-brick-builders','Brick Builders Lab','Grades 2–3','Engineering и coding; конкретный robot kit и точные часы не названы.',[['2026-07-13','2026-07-17'],['2026-08-10','2026-08-14']]),
        ('sfu-digital-defenders','Digital Defenders','Grades 4–5','Разработка игр и код; робототехника в этом треке не заявлена.',[['2026-07-13','2026-07-17'],['2026-08-10','2026-08-14']]),
        ('sfu-wattson','Wattson’s Wonderland','Grades 6–8','C/C++ programming; требуемый начальный уровень и продвинутая программа не опубликованы.',[['2026-07-20','2026-07-24'],['2026-08-17','2026-08-21']])]:
        emit(slug,'SFU Science AL!VE · Burnaby · '+name,'Канада','CAN','SFU · Burnaby, British Columbia','technology'+(',coding,games' if slug=='sfu-digital-defenders' else ',coding' if slug in ['sfu-wattson','sfu-brick-builders'] else ',science'),'day',age+' — класс поступления в 2026/27',en_unknown,
            programme+' FAQ запрещает запись выше текущего учебного уровня; опыт олимпиад не исключение. Не переносим классы/полудневный режим Surrey на Burnaby.',
            'Архив 2026: '+'; '.join(a+' — '+z for a,z in dates)+'. Burnaby 09–15:30. Даты 2027 не объявлены; похожую тему второй раз за лето FAQ не рекомендует.',
            dict(year=2026,label='Burnaby от $322 / неделю, не точная цена выбранного курса и не 2027. $186 Surrey не применяется. '+currency,
                included='Дневные STEM-занятия; материалы и итоговый проект выбранного трека уточнить.',
                extras='Before 07:45–09 и after 15:30–17 по $15 / день каждое: пять дней оба +$150, условный минимум $472 до неизвестных налогов/поездки. Обед, перекусы и воду приносят сами.',
                deposit='Отмена более недели до старта — возврат без $35 / camp; менее недели — без возврата. Ровно неделю страница не разъясняет. Отмена оператором — полный возврат, перенос между неделями $10. Аванс/сезонные условия 2027 неизвестны.'),day,grade,grade,
            'Канадская STEM-площадка с раздельными школьными треками; выбор только после подтверждения класса, языка и сезона.',
            ['Новые даты/цена Burnaby 2027, допустимый класс, язык teaching, индивидуальный иностранный приём, учебные часы/уровень и договор.'],
            [src('Таблица Burnaby: темы, классы и прошлые недели',SFU+'sfu-summer-camps'),src('Grade gate, еда, продление и отмена',SFU+'summer-academy-faqs')],status='archive_next_unannounced',sessions=dates)

    for slug,name,age,programme,identifier in [
        ('calgary-early-engineering','Early Engineering','Grades 1–2','Design challenges, простые машины/физика, химические эксперименты и программирование робота. Платформа/часы не названы.', '2603'),
        ('calgary-early-technology','Early Technology','Grades 1–2','Электрические компоненты/цепи, colour-coded управление роботами и практические задания.', '2604'),
        ('calgary-engineering101','Engineering 101','Grades 3–9','Инженерный цикл, LEGO SPIKE coding, 3D printing, VR и химия/материалы. LEGO прямо не спонсирует и не подтверждает эту программу.', '1778')]:
        emit(slug,'University of Calgary · '+name,'Канада','CAN','University of Calgary · Calgary, Alberta','technology,robotics,coding','day',age+' — класс, в который ребёнок идёт осенью',en_unknown,
            programme+' Оператор предупреждает: перечисленные занятия примеры и могут измениться. Разбивка группы, полноценный syllabus, часы/платформа, уровень наставников и техника домой неизвестны.',
            'Текущая собственная programme page прямо сообщает отсутствие offerings. Недельные фильтры 2027 общего каталога не доказательство доступных смен этого курса.',
            dict(year=None,label='Стоимость и сезонные даты выбранной программы не опубликованы в доступном предложении.',included='Лагерный пакет неизвестен.',extras='Еда, продление, материалы, налоги, семейное жильё и дорога уточнить.',deposit=unknown_terms),day,grade,grade,
            'Содержательная инженерная ступень по классу; наблюдаемый curriculum без объявленного набора — идея для следующего сезона.',
            ['Новый конкретный набор/даты/счёт, действующий класс, язык teacher, иностранный приём, платформы/часы/продвинутые уровни.'],
            [src('Собственная страница курса и отсутствие offerings',UC+'Program/'+identifier+'?path=All_Camps'),src('Общий каталог — фильтр не регистрация курса',UC+'Browse/All/Camps')],priority=['robotics'] if slug=='calgary-engineering101' else [])
    p=emit('calgary-winter','University of Calgary · Mini U Winter Break','Канада','CAN','University of Calgary · Calgary, Alberta','general,science,sport,art','day',
        'Выбранная текущая смена Gr. 3–5; боковой entering-grade filter 4/5/6 расходится с class label',en_unknown,
        'Общие зимние занятия: indoor games, спорт, LEGO building, творчество, active gaming, наука, ракеточные виды/гимнастика и бассейн. Обязателен swim test, жилеты доступны. Это не отдельный курс программирования роботов; примеры активностей могут меняться.',
        '21–23 декабря 2026, 08:30–16:30. Собственный код F26YMWB301, 13 мест на момент чтения — снимок, не гарантия. Кнопка Add to Cart не нажималась.',
        dict(year=2026,label='$260 / три дня. '+currency,included='Текущая дневная программа; еду/материалы/налоги и точный доступ в бассейн подтвердить.',extras='Обед, продление, жильё семьи, перелёт, ежедневный транспорт и страховка неизвестны.',deposit=unknown_terms),day,grade,grade,
        'Ближайшие каникулы в канадской семейной поездке, если оператор подтвердит фактический класс и язык.',
        ['Устранить конфликт Gr.3–5 и entering4/5/6, получить счёт/договор/язык/foreign intake/питание и места.'],
        [src('Датированная class card 2026, цена и противоречие фильтра',UC+'Program/miniuwinterbreakcamp?path=All_Camps')],status='published_2026',priority=['general'],sessions=[['2026-12-21','2026-12-23']])
    p['timing']['session_details']=[dict(start='2026-12-21',end='2026-12-23',label='Mini U Winter Break · F26YMWB301',price='$260 / три дня; валюта/налоги подтвердить',place=p['place'],source=UC+'Program/miniuwinterbreakcamp?path=All_Camps')]

def extend_report_v97(report):
    report['shortlist'].extend([
        dict(label='Канада · общий пансион обоим в конце лета 2027',slugs=['wenonah-five','wenonah-wee','wenonah-one','wenonah-regular'],reason='Period Five 30.08–03.09: 7–12 на 31.12.2027, обоим возраст подходит по явному правилу года. $1 300 + HST13% = $1 469 ребёнку/$2 938 двум до processing fee/дороги. WEEnonah 30.08–01.09: 5–7, короткая ступень Оскару $500+HST=$565; аванс $75/100 расходится. Это outdoor/общий английский отдых, робототехника не заявлена.'),
        dict(label='США · два возраста на одной площадке',slugs=['pali-general','pali-mini','pali-robotics'],reason='Pali 2027: Матвею общий 8–16, Оскару Mini6–8 четыре дня/три ночи. Девять интервалов каждого; окончания различаются. Общий promo$2 750 не цена Mini. Robotics8–16/VEXcode/сенсоры/лабиринт — выбранная утренняя specialty без опубликованной недельной доступности. ES/RU страницы всё ещё2023, язык учителя2027 не подтверждён.'),
        dict(label='Канада · реальные STEM-ступени по классу',slugs=['sciencequest-kinder','sciencequest-junior','sciencequest-robotics','sciencequest-engineering','sfu-elite-engineers','sfu-brick-builders','sfu-digital-defenders','sfu-wattson'],reason='Queen’s: SK–G1/G2–3/G4–8; старший Robotics с несколькими robot platforms, младшие coding только физическими играми. SFU Burnaby: G1engineering/G2–3coding/G4–5games/G6–8C++; не Surrey. Это архив2026, даты/тарифы/язык2027 ещё нужны. Классы детей неизвестны, из года рождения допуск не выведен.'),
        dict(label='Канада · ближайшая зима и инженерные идеи',slugs=['calgary-winter','calgary-early-engineering','calgary-early-technology','calgary-engineering101'],reason='UCalgary21–23.12.2026/$260: общий зимний MiniU, карточкаGr3–5 против фильтраentering4/5/6. Engineering101G3–9/LEGO SPIKE/3D/VR и EarlyG1–2 имеют syllabus, но noofferings. Общий фильтр2027 не фактическая смена. Для всех язык преподавания/foreign intake и реальный класс ещё проверить.')
    ])
    report['gaps'].extend([
        dict(country='Канада',iso='CAN',provider='v97 · Wenonah: возраст на конец года и полный сезонный счёт',detail='12futurevariants2027:6regular/4One/1Five/1Wee. Возраст31Dec2027; Wee такжеminimum5настарте. Явный teachingEnglish/international intake, Spanishнеобещан. Regularprices6350/3650/1960/1300/500 плюсHST13%;priorityOct1истёк. Fee currencyнепрописана, processingfeeнеизвестен. Wee75/100авансconflict;homepagebody8–15/5–6vs2027table9–15/5–7. Siblings3годаapartнеsamecabinrequest18months.',next_action='Валюта/счёт/processingfee, краткие трансферы/ранняя ночь, ночной надзор/питание/медицинские условия и отмена на пограничные даты.',url=W+'2027-dates-fees/'),
        dict(country='США',iso='USA',provider='v97 · Pali: Mini, общий лагерь и Robotics — разные условия',detail='18futurevariants2027изdates/news/Mini. General8–16семьдней6ночей;Mini6–8четыредня3ночи, отдельныйfeeunknown. RoboticsVEXcode8–16спецтрекбезspecificweeks. Promo2750perregularsessionнеMini;October23безгода,September28expired. FAQinsurance150/нед/ребёнок/отмена2027,неавтоматическийMinicontract. ПереведённыеES/RUстраницысаминазывают2023,неcurrentteachingSpanish/Russian.',next_action='Сезонный счёт обоих форматов, Roboticsдаты/часы/платформа/язык, internationaltransport и готовность к разным окончаниям/пансиону.',url=PALI+'mini-camp/'),
        dict(country='Канада',iso='CAN',provider='v97 · Queen’s / SFU / Calgary: класс, язык и год важнее интерфейса',detail='Queen’s4/SFU4досье и16pastvariants2026небудущиеICS. SFUforbidsoldergrade, Burnaby322fromнеSurrey186. Calgary3engineeringnoofferings; generic2027filterнеweekproof. MiniUexact21–23Dec2026/260/classGr3–5vsentering4/5/6. Actualfamilygradesunknown; Englishwebsiteнетeacherproof, полноценныйcurrentinvoiceвездеещёнужен.',next_action='Даты/цены2027, actualgrade/individualforeignintake/teachinglanguage, advancedsyllabus и полный договор; wintergradeconflict.',url=UC+'Browse/All/Camps'),
        dict(country='Латинская Америка',iso='BRA',provider='v97 · повторная проверка: тариф уже был внесён; shell/403 не новый syllabus',detail='EnglishCampBrazilKidsOctoberpromoянварь2027совпалсCP101,досье/календарьнепродублированы. LiotaHTTP200лишьJSshellбезпрочитаннойprogrammebody;AlbertaDiscoverEdirect403,неновыйverifieddossier. ПоCostaRica/Mexico/LatinAmericaобщийаудитостаётсяактивным,неполноепокрытие.',next_action='Новые сезонные страницы/счета для2027,EN/ES/RUteaching и иностранный индивидуальный приём; не подменять сайт поисковым сниппетом.',url='https://www.englishcamp.com.br/programas/kids/')
    ])
