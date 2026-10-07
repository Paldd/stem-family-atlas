"""European family boarding and English holiday programmes; scoped primary evidence."""
CHECKED = '2026-10-05'
SAN = 'https://www.internationalcamp.it/en/'
SOCKS = 'https://www.putonyoursocks.com/'
SPORT = 'https://www.englishsportcamp.it/'
MULTI = 'https://manager-cdn.srvit.biz/englishsportcamp/multimedias/fc063389-ba7c-49d6-9dde-31e25cbc42fe/o_camp-multisport.pdf'
INTENSIVE = 'https://manager-cdn.srvit.biz/englishsportcamp/multimedias/6f7593cf-06e3-4bba-8c03-6cbeecdfff10/o_camp-intensive.pdf'
AOSR = 'https://www.aosr.org/student-life/aosr-summer-program-summer-camp-in-rome'
XUK = 'https://www.xukcamps.com/'
BEDE = 'https://www.bedessummerschool.org/'
SUMMARY = BEDE+'bedes-live-2022/assets/File/2027/Bedes2027_CourseSummary_PRINT.pdf'
TERMS = BEDE+'bedes-live-2022/assets/File/2027/3580_BedesSummerSchool2027_T%26Cs_1a.pdf'
CANOPEE = 'https://www.ecolelacanopee.fr/?p=1494&lang=en'
NEW = ['sancelso-general','socks-general','englishsport-cavalese','englishsport-oclini',
       'aosr-general','xuk-activity','bede-little','bede-future','canopee-holidays']

def add_europe_v101(add, src, fit, profiles):
    def emit(*args, variants=None, role=None, **kwargs):
        add(*args, **kwargs)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        if variants:
            for v in variants:v.setdefault('place',p['place'])
            p['timing'].update(session_details=variants,variant_keyed=True,
                               sessions=[[v['start'],v['end']] for v in variants])
        return p

    emit('sancelso-general','Sancelso International Camp · Alpine English immersion',
         'Италия','ITA','Villa Sancelso · Castione della Presolana (Bergamo), Италия',
         'general,languages,sport,art,science','boarding','6–17; отдельные спортивные активности имеют собственные минимумы',
         'Английский — общий язык сотрудников/лагерной жизни. На внешних спортивных выездах инструкторы объясняют на итальянском, counsellors переводят на EN. Итальянские дети могут говорить друг с другом по-итальянски; это не обещание исключительно EN каждую минуту.',
         'Возрастные группы, спорт, театр/ролевые игры, art/craft/science/cooking, горные выходы и ночёвка в палатке/хижине. Два внешних спортивных выезда в неделю обязательны. Sailing: FAQ с8, отдельная карточка >8 — порог уточнить; paintball13+, e-bike12+. Собственного robotics/AI курса не заявлено. Оператор сообщает20–40% иностранных детей и около500 за лето; эти цифры не независимый рейтинг.',
         'Прочитанный сезон21 июня–8 августа2026: одно- и двухнедельные периоды уже прошли. Новый сезон2027/места не опубликованы; старые даты в будущий ICS не переносим.',
         dict(year=2026,label='Архив:795+обязательные60=EUR855/неделя;1550+120=1670/2недели. Двое со sibling-тарифом:1670/неделя или3280/2недели до дороги/личных расходов; цены2027 неизвестны.',
              included='Полный пансион/перекусы, основные занятия, counsellors день/ночь,24h health care, при необходимости педиатр, небольшая прачечная, liability/accident insurance. Обязательные внешние выезды оплачиваются сверх базового тарифа.',
              extras='Bus из Milan45/направление или90 return на ребёнка; двоим+180. Sailing+100 за выбранную опцию; pocket money рекомендованы50/неделя. Отдельно museums/shows/lifts/local transfers/дополнительный врач и лекарства, sleeping bag/ботинки/личная экипировка. Архивные суммы с автобусом:1850 двоим/неделя или3460/2недели до прочего.',
              deposit='Архив2026: аванс300 в счёт цены, остаток двумя платежами; даты/суммы по договору2027 ещё нужны. Sibling второй755/неделя или1490/2недели до обязательной спортдоплаты; скидки не суммируются. Текущий cancellation/refund contract не установлен.'),
         'Четырёхместные комнаты с санузлом, разделение по полу/возрасту. Counsellors на том же этаже; в младшей группе в комнате. Около1:10, младшим ещё intern. Общая комната братьям разного возраста не обещана.',
         fit('candidate','9–10 в2027 входит6–17; нужны новый сезон/уровень группы и подходящие выезды.'),
         fit('candidate','6–7 в2027 входит6–17; младшая группа/готовность к горной ночёвке и отдельные возрастные ограничения требуют согласования.'),
         'Содержательный международный общий пансион для обоих, с понятными обязательными доплатами и реальными ограничениями английской среды; кандидат после нового2027 прайса.',
         ['Точные2027 смены/итоговый счёт/отмена/места, внешняя индивидуальная заявка, ночёвка младшего и возраст Sailing, медицинская страховка для Италии и перевод внешних инструкций.'],
         [src('Возраст6–17/все национальности/английская среда',SAN+'summer-camp/'),src('Реальный архивный прайс/mandatory sport/sibling/bus',SAN+'dates-costs-and-travel/'),
          src('Язык внешних инструкторов, supervision/документы/экипировка',SAN+'faqs/'),src('Дневная структура/питание/четырёхместные комнаты',SAN+'week-program-daily-schedule/'),src('Спорт с отдельными возрастными порогами',SAN+'external-sports-activities/')],
         status='archive_next_unannounced',priority=['both','general','boarding'],confirmed=['EN'],role='camp_life')

    emit('socks-general','Put On Your Socks · English Summer Camp',
         'Италия','ITA','Cà di Gianni · Bagno di Romagna · Emilia-Romagna',
         'general,languages,art,sport','boarding','Children7–10; Tweens10–14',
         'Собственная programme page прямо EN immersion и mother-tongue English teaching: музыка, общение, игры. ПоддержкаES/RU отдельно не заявлена.',
         'Residential1–2 недели: песни, движение, игры, друзья и общение по творческому подходу Rachelle Hangsleben. Площадка с бассейном, adventure park/albering, лесом и общим Magical Room. Это общий музыкально-языковой отдых, не robotics/AI. Подробный новый посуточный syllabus/ratio и условия иностранного индивидуального приёма пока неизвестны.',
         'Dates & Prices2026 в меню, но фактический body объявляет Summer Camp2027 и открытие регистрации15 января2027. Дат смен/цен2027 пока нет; дата открытия — не заезд и не deadline.',
         dict(year=None,label='Стоимость лагеря2027 и полный пакет не опубликованы в прочитанной странице.',
              included='Заявлена residential programme; точный состав жилья/питания/активностей ещё нужен.',
              extras='Трансфер, страховка, материалы, бытовые сборы/скидка братьям и экипировка не оценены.',
              deposit='Размер аванса, график платежей и возврат/отмена не опубликованы; заявок/аккаунтов не создавали.'),
         'Residential в Cà di Gianni заявлен; число детей в комнате/ночной персонал и младший минимум конкретного заезда не раскрыты.',
         fit('candidate','9–10 в2027 подходит Children7–10; переход в Tweens по дню рождения/группе согласовать.'),
         fit('conditional','Только после7-летия в2027; до него общий минимум7 не выполнен.'),
         'Дополнительный английский творческий пансион Италии, особенно если интересна музыка; младший возраст/полный2027 пакет пока ограничивают семейный выбор.',
         ['Смены2027/цена/foreign individual intake/7лет на дату, группа обоих/комнаты/ratio, EN всех блоков, страхование/дорога/условия отмены.'],
         [src('Программа/группы7–10 и10–14/EN residential',SOCKS+'english-summer-camp'),src('Только открытие2027, пока без смен/цен',SOCKS+'dates-and-prices'),src('Фактическая площадка/бассейн/adventure park',SOCKS+'location')],
         status='partial_2027',priority=['general','boarding'],confirmed=['EN'],role='camp_life')

    for intensive in [False,True]:
        dates=[('2027-07-18','2027-07-24'),('2027-07-25','2027-07-31')] if intensive else [('2027-07-04','2027-07-09'),('2027-08-22','2027-08-27')]
        variants=[dict(start=a,end=b,variant_key=a.replace('-',''),label='Intensive /7дней' if intensive else 'English & Sport /6дней',
                       formats=['boarding'],price='EUR780 пансион' if intensive else 'EUR680 пансион; EUR340 день с обедом отдельно',source=SPORT+'informazioni',
                       proof='Собственная2027 таблица с полным месяцем и годом. Первая Cavalese строка «27–02 luglio» имеет неявный стартовый месяц и здесь не рассчитана.') for a,b in dates]
        emit('englishsport-oclini' if intensive else 'englishsport-cavalese','English Sport Camp · '+('Oclini Intensive12–16' if intensive else 'Cavalese English & Sport10–14'),
             'Италия','ITA','Passo Oclini · Aldino (BZ)' if intensive else 'Cavalese · Val di Fiemme (Trentino)',
             'general,languages,sport','boarding' if intensive else 'day,boarding','12–16' if intensive else '10–14',
             'Intensive PDF прямо full immersion: все дневные активности на английском; это camp-life EN, не только интерфейс.' if intensive else
             'Подтверждены занятия английским и вечерние Giochi in Inglese. Multisport PDF не обещает EN всем спортивным инструкторам; полный EN camp-life не установлен.',
             ('Английский утром и после обеда, ориентирование, Nordic walking, swimming, self-defence, спортивные турниры, вечерний campfire/итоговая презентация на EN.' if intensive else
              'Чередование блоков English class с mountain bike/Nordic walking, climbing/handball, swimming, командными играми и вечерними English games. Колонки ENGLAND/SCOTLAND в PDF — группы расписания в Cavalese, не страны проведения.')+
             ' PDF программы не имеет собственного нового года, поэтому это типовой план, а не гарантированное посуточное расписание2027; внутренние награды не международные соревнования.',
             '2027:18–24/25–31 июля, воскресенье–суббота.' if intensive else
             '2027:4–9 июля и22–27 августа; ещё первая строка «27–02 luglio2027», стартовый месяц неявен — не внесена точной датой. Пансион воскресенье–пятница, day08:30–18.',
             dict(year=2027,label='EUR780/7дней пансион; отдельный daytime Intensive тариф не подтверждён.' if intensive else 'EUR680/6дней пансион; dayEUR340 с обедом. Двое не проходят общий возрастной минимум.',
                  included='Hotel/full board, English course/materials, multisport или выбранный sport, leisure animation, clothing kit и организационные расходы по собственному прайсу.',
                  extras='Межсменный weekendEUR50/ночь full board, только при согласованном продолжении; число ночей уточнить. Дорога/страховка/личная экипировка/скидки не оценены. Day без dinner/ночёвки.',
                  deposit='Аванс/отмена/контракт/полная медицинская страховка не опубликованы на прочитанной странице; нужны sports non-competitive fitness certificate, health card copy и данные аллергий.'),
             'Hotel: распределение по возрасту/полу,24h supervision/medical assistance; число мест в комнате неизвестно. Multisport sample указывает Albergo Panorama в Cavalese; конкретный2027 hotel Oclini не назван.',
             fit('later' if intensive else 'conditional','Минимум12 — будущий возраст.' if intensive else 'Только после10-летия в2027; дату рождения и подходящий EN уровень согласовать.'),
             fit('later','Минимум12.' if intensive else 'Минимум10; Оскар6–7 не проходит.'),
             'Прозрачный языково-спортивный вариант с настоящими2027 ценами; Intensive — будущая ступень, не семейный лагерь обоим сейчас.',
             ['Иностранный индивидуальный приём/EN спортивных инструкций, полный счёт/страховка/аванс/отмена,2027 syllabus/hotel/ratio/места; неявный месяц первой Cavalese смены.'],
             [src('Даты2027/возрасты/680780340/пакет/меддокументы',SPORT+'informazioni'),src('Типовой визуально проверенный учебно-спортивный план',INTENSIVE if intensive else MULTI)],
             status='published_2027',confirmed=['EN'],variants=variants,role='camp_life' if intensive else 'language_lessons')

    emit('aosr-general','American Overseas School of Rome · Summer Camp',
         'Италия','ITA','AOSR · North Rome · школьный кампус',
         'general,languages,science,coding,engineering,art,sport','day','Early Years3–5; Fun & Exploration6–15; отдельные sport clinics7+/9+',
         'Own page прямо fully English-speaking programme и immersion; преподаватели школы, coaches/alumni. Внешние семьи и временные посетители Рима прямо допускаются.',
         'Balanced day programme: coding/rocket building/makerspace, science/nature, art/comic writing, Friday talent shows, swimming/field trips/sports. Tech lab в школе не означает отдельную полноценную robotics/AI смену. Basketball/soccer9–15 и cheer7–15 — отдельные2026 clinics, не автоматический доступ младшему.',
         'Архив22 июня–10 июля2026, три неделиПн–Пт08:30–16:30.2027 work in progress, подробности обещаны в марте2027; «Registrations2027 are closed» означает сейчас не принимают, а не доказанный sold-out.',
         dict(year=2026,label='Архив:EUR250/1неделя,450/2,650/3; двоим500/900/1300. Тариф2027 ещё не опубликован.',
              included='Camp activities/materials, T-shirt, off-campus admissions, snacks и lunch по собственной странице.',
              extras='Опциональный school busEUR175/неделя на ребёнка (двум+350); жильё семьи/дорога отдельно. Страховка, enrolment fee и sibling не установлены.',
              deposit='2027 intake сейчас закрыт/в разработке; аванс/сроки/отмена/места неизвестны.'),
         'Дневной08:30–16:30. Ночёвки или летний школьный пансион не предложены.',
         fit('candidate','9–10 в2027 подходит6–15; нужен новый набор/план технических блоков.'),
         fit('candidate','6–7 в2027 подходит6–15; в2026 до6-летия нужна группа3–5. Приём/группы нового сезона отдельно.'),
         'Хорошая база общего EN/STEM дня обоим во время семейной поездки в Рим: внешние временные посетители разрешены, новый сезон ещё не открыт.',
         ['Подробности2027 в марте/места/счёт/договор, возрастная группа/ratio/объём coding и оборудования, аллергии/страховка/transport.'],
         [src('Фактическая программа, иностранные временные посетители, архивный прайс и статус2027',AOSR)],
         status='partial_2027',priority=['both','general'],confirmed=['EN'],role='camp_life')

    xdates=[('2027-07-04','2027-07-11'),('2027-07-11','2027-07-18'),('2027-07-18','2027-07-25'),('2027-07-25','2027-08-01'),('2027-08-01','2027-08-08')]
    emit('xuk-activity','XUK Activity · International Multi Activity Residential Camp',
         'Великобритания','GBR','Dauntsey’s School · Devizes · Wiltshire ·SN104HE',
         'general,languages,sport,art','boarding','8–17; младшие XUK Day3–6/7–12 в Лондоне — другая программа',
         'FAQ: staff use EN during activities/games/sport/trips/everyday camp life. Activity даёт среду, structured English lessons — отдельный XUK English; optional conversation class тоже платная опция.',
         'Общий multi-activity residential с возрастными Juniors/Intermediates/Teens, играми/спортом/творчеством/поездками. XUK Excel имеет утренние electives, XUK English — language classes: их syllabus не перенесён в Activity. Оператор сообщает35–45 стран,40 в2026; это не независимая оценка качества.',
         'Пять опубликованных weekly arrival/departure окон2027:4–11/11–18/18–25 июля,25 июля–1 августа,1–8 августа. Стыки воскресных приезда/выезда, а не удвоенные учебные дни; цены ниже всё ещё озаглавлены2026.',
         dict(year=2026,label='На Dates2027 тарифный блок всё ещё Prices2026:GBP1160/неделя,Gold2695/2недели,Platinum3835/3. Не считать окончательной ценой2027.',
              included='Residential dorm1–6, три приёма пищи/fruit/drinks, основной camp и часть экскурсий. Gold/Platinum2026 включают перечисленные attraction extras/трансфер в определённые часы; ограничения возраста/мест могут оставить тот же пакетный тариф без части опций.',
              extras='Архив:conversation150,theme park95,aqua80,laser70,London199,Stonehenge65,welcome pack55; transfer99/направление,прачечная6/мешок. Страховка не включена, нужна отдельно. LIT80 только16–17. Discounts2027:75/неделя до конца января или40 до конца марта; применимость к новому тарифу уточнить.',
              deposit='Ссылка Terms PDF имеет таблицу отмены именно2026: deposit forfeited;50/75/100% по май/июнь/июль2026. Не переносим её на2027. Размер нового аванса/дата полной оплаты и актуальные условия2027 неизвестны.'),
         'Школьный пансион, комнаты1–6, распределение по возрасту; sibling room request не гарантирован. StaffDBS/references/supervision — собственные заявления оператора, независимый audit не проводили.',
         fit('candidate','9–10 в2027 входит8–17; Activity или отдельный elective выбирать по интересу.'),
         fit('later','Минимум residential8; XUK Day в Лондоне не даёт исключение здесь.'),
         'Международный английский общий пансион Матвею с конкретными2027 датами; окончательная цена и контракт2027 ещё требуют подтверждения.',
         ['Актуальный2027 all-in/terms/deposit/refund/places, конкретный Activity timetable/ratio, transfer и собственная страховка; младшему отдельный дневной лагерь, если семья едет вместе.'],
         [src('Возраст8–17 и формат Activity',XUK+'residential-camp/'),src('Точные2027 окна, тариф2026 и discount2027',XUK+'residential-camp/dates-prices/'),
          src('EN everyday camp life, питание/страховка/прачечная/foreign intake',XUK+'faq/'),src('Реальная площадка',XUK+'activity-camps/venue/'),src('PDF Terms с отменой2026, не новый контракт2027',XUK+'wp-content/uploads/2025/01/Terms-and-conditions.pdf')],
         status='partial_2027',priority=['general','boarding'],confirmed=['EN'],sessions=[list(v) for v in xdates],role='camp_life')

    for future in [False,True]:
        dates=[('2027-07-11','2027-07-17'),('2027-07-18','2027-07-24'),('2027-07-25','2027-07-31'),('2027-08-01','2027-08-07')] if future else [
              ('2027-07-04','2027-07-10'),('2027-07-11','2027-07-17'),('2027-07-18','2027-07-24'),('2027-07-25','2027-07-31'),('2027-08-01','2027-08-07'),('2027-08-08','2027-08-14')]
        variants=[dict(start=a,end=b,variant_key=a.replace('-',''),label='Residential week · '+a,formats=['boarding'],
                       price='GBP1775 /неделя пансион2027; day1125 отдельный формат',source=SUMMARY,
                       proof='Actual2027 summary PDF: конкретная отмеченная неделя/площадка/возраст/тариф. Futureweek6PDF против webendingAug7 исключена; weekly option не подтверждение свободного места.') for a,b in dates]
        emit('bede-future' if future else 'bede-little',"Bede’s Summer School · "+('Future Explorers /Burgess Hill2027' if future else 'Little Explorers /Eastbourne2027'),
             'Великобритания','GBR','Burgess Hill School · Sussex' if future else 'Bede’s Preparatory School · Eastbourne · Sussex',
             'general,languages,science,art,sport','day,boarding','8–13; A0+' if future else 'Day5–11; Residential6–11; A0+',
             'English language course плюс общий international English campus. Перечень technical subjects/отдельных external academies не превращает его в robotics intensive; поддержкаES/RU отдельно не доказана.',
             ('Новая площадка2027 Burgess Hill:18.5h English/неделя, Mission Possible team challenges, exploratory learning, outdoor/creative/экскурсии. Максимум14 в классе, A0 beginner+. Старый2026 Windlesham plan/1:4 не обещан как2027 ratio нового кампуса.' if future else
              '17.5h English/неделя: English Skills, StoryTime, Explorations(CLIL science/design/geography/art/history), затем sport/social events/экскурсии. Максимум14, уровниA0–C2. Отдельные3–4.5h academies заменяют часть общих afternoon activities, а не весь лагерь.')+
             ' Attendance certificate/report — результат обучения, не международная победа.',
             ('2027 подтверждённые совместноPDF/web недели11–17/18–24/25–31 июля,1–7 августа. PDF также отмечает8–14 августа, но webdates заканчивается7 августа: последняя неделя пока не точный календарь.' if future else
              '2027 шесть недель4 июля–14 августа, приездыВс/отъездыСб. DayПн–Пт08:30–17, ср18, пт18:45; в календаре показаны boarding windows, дневные учебные дни выбирать отдельно.')+
             ' Рекомендован минимум2 недели, но прайс содержит1 week option.',
             dict(year=2027,label='GBP1775/неделя residential или1125/day. Двое Little:3550/неделя пансион или2250/day;2недели7100/4500 до опций. Цена обоих курсов одинакова.',
                  included='Residential: tuition/materials/report/certificate, жильё/питание/snacks, basic activities/social/excursions/attraction entry, nursing access/laundry/student travel insurance/emergencyline/visa invitation, shared transfer по разрешённым дням/часам. DayLittle включает snacks/lunch; evening/weekend activities отдельно.',
                  extras='Academies:3h195–325,horse4.5h345,tennis4.5h295 по2027 таблице/кампусу/неделе; точную опцию проверить. Перелёт/pocket money/экзамены отдельно.2027terms:extra night235,irregular transfer160,late transfer95,Stansted/Luton295 one-way,adultarrivaltransfer100; не складывать альтернативные схемы без счёта.',
                  deposit='Terms2027: deposit800 boarding/400day в счёт цены; баланс56 дней до начала. Cancel≥56 дней полный возврат,29–55 deposit retained,8–28 удерживают1неделю,0–7/после начала полный тариф. FAQ29–41 устарел относительноPDF29–55. Опции имеют отдельные ограничения возврата.'),
             'Actual2027 summary:1–4 beds/room, staff day/night в boarding houses; ratio новогоBurgess не установлен.' if future else
             'Actual2027 summary:2–5 beds/room; ownEastbourne typically1:3, HouseParents/24hcare. Старый2026PDF4–8beds не перенесён на2027.',
             fit('candidate','9–10 в2027 входит8–13 новогокампуса.' if future else '9–10 в2027 входит5–11day/6–11board.'),
             fit('later' if future else 'candidate','Минимум8, Оскару6–7 рано; out-of-range исключение не гарантируется.' if future else '6–7 в2027 входит6–11пансион;5летday и6летboard разделены.'),
             'Новое английское общее обучение с фактическим2027 тарифом и договором; '+('Future — Матвею, оба ребёнка в одной программе здесь не проходят.' if future else 'Little — один из ясных EN пансионных кандидатов обоим, без обещания robotics.'),
             ['Места по nationality/language quota и возрасту, точная смена/формат/полный invoice/academies; Future8–14Aug конфликт и новыйcampusratio; siblingroom не гарантирован.'],
             [src('Actual2027 course summary, возрастаday/board, даты/прайс/rooms/academies',SUMMARY),src('Actual2027 terms: deposit/balance/cancellation/extras/medical',TERMS),
              src('Web2027 annualdates, отдельные конфликтующие поля',BEDE+'booking/dates/'),src('Новыеfees/inclusions и ссылки2027',BEDE+'booking/fees/'),
              src('СтарыйWindlesham programme не означает новыйBurgess syllabus' if future else 'Eastbourne2027 programme/dayhours/ratio/питание',BEDE+'centres/windlesham/' if future else BEDE+'centres/eastbourne/')],
             status='partial_2027' if future else 'published_2027',priority=['general','boarding'] if future else ['both','general','boarding'],confirmed=['EN'],variants=variants)

    dates=[('2026-10-19','2026-10-23','autumn',515),('2027-02-08','2027-02-12','winter',515),('2027-04-05','2027-04-09','spring',515),
           ('2027-07-01','2027-07-02','summer-short',206),('2027-07-05','2027-07-09','summer-week',515),('2027-07-12','2027-07-13','summer-extra',206)]
    variants=[dict(start=a,end=b,variant_key=k,label=k,price='EUR'+str(fee)+' /ребёнок с обедом; двое'+str(fee*2),source=CANOPEE,
                   date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'],
                   proof='Собственная таблица2026–27: полный период, duration/fee,09–17/lunch/всеактивностиEN. Два отдельных летних двухдневных окна не выданы за полные недели.') for a,b,k,fee in dates]
    emit('canopee-holidays','La Canopée Paris · English Holiday Camps',
         'Франция','FRA','Paris · La Canopée · точный адрес выбранной площадки уточнить',
         'general,languages,science,art','day','Overview3–5/6–11; подробные темы обозначают старших6–10 — upper-age discrepancy',
         'Весь09–17день полностьюEN, только собственные native-English teachers Jenni/Leah; школа прямо разрешает внешних детей. Это не просто ENlesson внутриFRдня.',
         'Младшие:Space/Planets, Dinosaurs, Community Workers, Above&BelowSea. Старшие:осеньскандинавскийfolklore/drama/costumes/performance, зимаStoneAge/tools/art, веснаAstridLindgren/pirates/friendship, летоUnderwaterKingdoms. Songs/drama, cooking/science и craft; самостоятельной robotics/AI программы не заявлено. Small groups безчисловогоratio.',
         'Шесть окон2026–27:19–23 октября;8–12 февраля;5–9 апреля;1–2,5–9,12–13 июля.09–17/lunch;12–13 июля продолжают тему5–9, но это отдельный двухдневный тариф.',
         dict(year=2027,season='2026/27',label='EUR515/5дней или206/2дня с обедом. Двоим1030 или412 соответственно. Полные12–13Jul не включены бесплатно в предыдущую неделю.',
              included='English theme day09–17, собственные школьные teachers и lunch.',
              extras='Жильё семьи/дорога отдельно; transport, snacks, enrolment fee, insurance и sibling discount не установлены.',
              deposit='Срок оплаты/аванс/возврат/contract/места не опубликованы на выбраннойprogramme page; форм не заполняли.'),
         'Только дневной: семейное жильё отдельно; school membership не обязателен.',
         fit('candidate','8–10 в2026–27 соответствует даже старшемуtheme6–10; школу/уровень группы подтвердить.'),
         fit('conditional','5лет—группа3–5, после6лет—6–10/11; exact birthday неизвестен, поэтому выбрать конкретнуюгруппу по дате.'),
         'Один из ясных французских общихENкалендарей обоим с зимой/весной/летом, собственнымиучителями и тарифом с обедом.',
         ['Группа поDOB, upper6–10vs6–11, точныйадрес/ratio/места/иностранный индивидуальныйприём, полный invoice/страховка/отмена.'],
         [src('Actual2026–27calendar/themes/all-English/dayhours/lunch/externalchildren',CANOPEE)],
         status='published_2026_27',priority=['both','general'],confirmed=['EN'],variants=variants)

def extend_report_v101(report):
    report['shortlist'] += [
        dict(label='Европа · общий английский пансион обоим',slugs=['bede-little','sancelso-general','socks-general'],
             reason='BedeLittle2027:board6–11/day5–11 с новымпрайсом/terms. Sancelso6–17, но покаархив2026; внешниеспортинструкцииITсENпереводом. Socks7+ после7летОскара; даты/цена ещёнеобъявлены. Редакционныйfamilyfit, не мировоерейтинг.'),
        dict(label='Франция / Италия · общий день в семейной поездке',slugs=['canopee-holidays','aosr-general','forest-paris-holidays'],
             reason='LaCanopée шестьокон2026–27, all-English09–17/lunch. AOSR допускаетвнешнихвременныхпосетителей, но2027подробностивмарте/регистрациясейчасзакрыта; тариф2026. Forestпокрываетлетниенеделиизимниеканикулы. Ночёвкинезаявлены.'),
        dict(label='Матвею / будущие возраста · UK и Италия',slugs=['xuk-activity','bede-future','englishsport-cavalese','englishsport-oclini'],
             reason='XUK8+ Englishcamplife/даты2027, ноценыиотмена2026. BedeFuture8–13 новыйBurgessHill1775board/1125day, последняяавгустовскаянеделяконфликтует. Cavalese10–14 после10летМатвея; Oclini12–16 позжеобоим. Общий/языково-спортивныйтрек, не roboticsintensive.')]
    report['gaps'] += [
        dict(country='Италия',iso='ITA',provider='v101 · младшие пансионы и новые сезоны',
             detail='Sancelso6–17 имеет mandatorysport+60/120, внешниеITинструкторы сENпереводом иархив2026. Socks7+ толькообъявилJan15registration2027, безсмен/прайса. AOSR2027workinprogress/March, closedintakeнеsoldout. Cavaleseперваястрока27–02luglio2027 неявностартуетвпредыдущеммесяце; точныйICSнерассчитан.',
             next_action='Новые2027 invoices/terms/dates/places, иностранныйприём/страховка/экипировка, camp-lifeвсехспортблоков иDOB/готовностьмладшегокночёвке.',url=SAN+'faqs/'),
        dict(country='Великобритания',iso='GBR',provider='v101 · Bede2027 против старых полей',
             detail='Новый2027summary:Little5–11day/6–11board,rooms2–5,1775/1125;Future8–13 теперьBurgessHill/rooms1–4. Futureweek6(8–14Aug)отмеченаPDF,webendingAug7;неICS. Terms2027cancel29–55,FAQ29–41устарел. СтарыйWindlesham2026ratio/rooms/1595неперенесены нановыйкампус.',
             next_action='ПодтвердитьFutureпоследнююнеделю/ratio/Burgesssyllabus/места/academies/invoice; сверитьdayattendance vsboardingwindow.',url=SUMMARY),
        dict(country='Великобритания',iso='GBR',provider='v101 · XUK2027 dates /2026 prices and cancellation',
             detail='Даты2027источниковые, ноPrices/Packages2026 иPDFсотменойMay–July2026. ENstaffcamplifeподтверждён;Activity/Excel/Englishразныеутренниепрограммы. Residential8–17, Day3–6/7–12вЛондоне — другаяплощадка. Owninsuranceобязательна, laundry6/bag, extras/transferотдельно.',
             next_action='Актуальный2027тариф/deposit/terms/refund/ratio/places; electivesиENlessonsпроверятькакдругиепрограммы.',url=XUK+'residential-camp/dates-prices/'),
        dict(country='Франция',iso='FRA',provider='v101 · La Canopée: младшие/старшие темы',
             detail='All-English/externalchildren/lunch/09–17/6точныхокон2026–27 подтверждены. Overviewстаршие6–11, detailedthemes6–10;выше10необещаем. Smallgroupsбезчисловогоratio, точныйадрес/invoice/refund ещёнеустановлены.',
             next_action='DOB/группа/upperage/площадка/ratio/инвойс/места/страховка/отмена; детальныйscienceblockнеподменятьrobotics.',url=CANOPEE),
        dict(country='Испания',iso='ESP',provider='v101 · Lacunza / Chester: повторная проверка без выдуманных тарифов',
             detail='Lacunzaновая1526страница2027 всёещёпоказываетplaceholder-цены«-€»/«-€/semana»,seasonJun20–Aug8, неиндивидуальныенедели. ChesterEN2027title8–17,вboardingsection8–18;datesveryshortly/PDFfeesпо-прежнему2026. Обапрежниедосьеоставленыбезновыхцен/смен,конфликтнеобъявленразрешённым.',
             next_action='Новый2027fullinvoice/конкретныеweeks/minboardingage/foreignintake/terms; подтверждение8–17vs8–18невыводитьизверхнегозаголовка.',url='https://www.lacunza.es/en/node/1526')]
