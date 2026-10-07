"""Selected European programme clauses; raw sources stay in private scratch."""
CHECKED = '2026-10-05'
COSMO = 'https://www.cosmorobotics.ch/en/academy'
COSMO_PDF = 'https://f71f090c-8f34-4f0e-a8c0-0f3889e5a66d.filesusr.com/ugd/ba8545_d7244217aeb74ba0a3af83181f1c1895.pdf'
CODE = 'https://en.codecampworld.ch/'
ISSH = 'https://www.issh.ch/calendar/2026-07-13/techlabs-summer-camp-2026/'
FOREST = 'https://forest-international.com/fr/stages-vacances/'
EIB = 'https://www.eibparis.com/extrascolaire/camps'
BEE = 'https://www.beelingueacademy.com/'
NEW = ['cosmo-mornings', 'cosmo-full-days', 'codecamp-spark', 'codecamp-ignite',
       'codecamp-blast', 'codecamp-web', 'codecamp-engineers', 'codecamp-masters',
       'codecamp-experts', 'codecamp-animation', 'codecamp-ai', 'issh-techlabs-robots',
       'issh-techlabs-drones', 'forest-paris-holidays', 'eib-monceau-preschool',
       'eib-monceau-science', 'beelingue-paris-autumn', 'beelingue-levallois-autumn']


def add_europe_v100(add, src, fit, profiles):
    def emit(*args, variants=None, role=None, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1]
        p['checked'] = CHECKED
        for s in p['sources']:
            s['checked'] = CHECKED
        if variants:
            for v in variants:
                v.setdefault('place', p['place'])
            p['timing'].update(session_details=variants, variant_keyed=True,
                               sessions=[[v['start'], v['end']] for v in variants])
        if role:
            p['language_evidence_role'] = role
        return p

    cosmo_dates = [('2027-02-08','2027-02-12','winter',350),
                   ('2027-03-30','2027-04-02','easter',280),
                   ('2027-07-12','2027-07-16','summer1',350),
                   ('2027-07-26','2027-07-30','summer2',350),
                   ('2027-08-09','2027-08-13','summer3',350),
                   ('2027-10-11','2027-10-15','halloween',350)]
    for full in [False, True]:
        dates = [r for r in cosmo_dates if not full or r[2].startswith('summer')]
        variants = [dict(start=a,end=b,variant_key=k,label=('Полный летний день' if full else 'Утренний курс')+' · '+k,
                         price='CHF '+str(500 if full else fee)+' / ребёнок до неизвестных бытовых доплат',
                         source=COSMO_PDF,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'],
                         proof='Конкретная таблица 2027 в PDF: даты, форматы, тариф; четыре пасхальных утра стоят280, хотя web ещё просит уточнить цену.')
                    for a,b,k,fee in dates]
        emit('cosmo-full-days' if full else 'cosmo-mornings',
             'Cosmo Robotics · '+('Summer full days' if full else 'Robotics mornings'),
             'Швейцария','CHE','Centre de Magie de la Côte · Chemin Falconnier23 ·1260 Nyon',
             'robotics,coding,engineering'+(',general,sport' if full else ''),'day',
             'Academy weekly classes с8 лет; отдельный camp minimum в PDF не установлен',
             'EN версия сайта и FR бланк не подтверждают язык преподавания лагеря. EN/ES/RU группа и помощь пока неизвестны.',
             'Программирование micro:bit, сенсоры, затем Maqueen: движение, реакции и практические миссии. '
             +('Полный день09–17: после технического утра общие активности, среда целиком в бассейне. Поэтому нельзя автоматически обещать15 часов робототехники за неделю.' if full else
               'Утро09–12: зимой/летом/осенью5 утр, на Пасху4. Конкретный syllabus по уровню, ratio и выдача набора домой не опубликованы; micro:bit в подарок относится к годовым classes, не лагерю.'),
             ('Три летние недели2027:12–16/26–30 июля,9–13 августа,09–17; full-day только летом.' if full else
              '2027:8–12 февраля,30 марта–2 апреля,12–16/26–30 июля,9–13 августа,11–15 октября,09–12.'),
             dict(year=2027,label=('CHF500 /5 полных дней; ученикам Academy450. Это не автоматическая скидка любому брату.' if full else
                  'CHF350 /5 утр; Пасха4 утраCHF280 в PDF, на web ещё price to be confirmed. Ученикам Academy315 /5 утр; пасхальная скидка отдельно не указана.'),
                  included='Техническая программа и '+('летние общие активности/день бассейна; полный бытовой пакет ещё нужен.' if full else 'утренние задания; материалы/страховка домой отдельно не обещаны.'),
                  extras='Личная страховка болезни/несчастных случаев обязательна. Обед, бассейн/транспорт, техника домой и прочие сборы требуют счёта; жильё семьи отдельно.',
                  deposit='PDF: после подтверждения вся сумма обязательна и невозвратна, оплатить не позже первого дня. При отмене оператором не позже5 дней до старта — полный возврат. Фото можно разрешить или запретить; согласий/заявки не отправляли.'),
             'Дневной центр; ночёвки не предложены.',
             fit('unknown','Матвею9–10 в2027, но возраст8+ указан для weekly Academy, не отдельного camp; EN группы и внешний приём ещё не доказаны.'),
             fit('unknown','Оскару6–7, отдельный минимум camp неизвестен. Нельзя переносить ни class8+, ни отсутствие возраста в форму как разрешение младшему.'),
             'Конкретный швейцарский робототехнический курс с шестью сезонными окнами и договорными условиями; пока язык и детский допуск требуют проверки.',
             ['Подтвердить camp age обоих, EN преподавание/уровень/ratio, иностранный индивидуальный приём, полный счёт и набор, бассейн/питание и места.'],
             [src('Микроконтроллер/робот, расписание и различие classes/camps',COSMO),src('PDF2027: точные форматы, Пасха280, страхование и невозвратность',COSMO_PDF)],
             status='published_2027',variants=variants)

    code_courses = [
        ('codecamp-spark','Spark','spark','7–12','coding,games',
         'Начальный 2D platformer в Code Camp World: блоки, переменные, события, условия, физика, тестирование. Обычно3 дня, длина зависит от площадки. Свой проект продолжает работать после лагеря.',7),
        ('codecamp-ignite','Ignite','ignite','7–12','coding,games',
         'После Spark или достаточного опыта: новый2D проект, drag-and-drop и первый блок JavaScript в конце курса. Обычно3 дня; игра запускается через общее приложение Code Camp, публикация самостоятельного приложения в магазине не обещана.',7),
        ('codecamp-blast','Blast3D','blast-3d','8–13','coding,games',
         'Текстовый JavaScript для собственной3D игры после Spark/Ignite. Нужна уверенная клавиатура; обычно3 дня с вариациями. Заявление first worldwide не независимый рейтинг.',8),
        ('codecamp-web','Web Builders','web-builders','8–13','coding',
         'Многостраничный сайт на HTML/CSS/JavaScript: структура, стили, ссылки, формы, gallery, GRID и показ проекта. Обычно3 дня, нужна уверенная клавиатура; занятия на EN ещё не подтверждены.',8),
        ('codecamp-engineers','Minecraft Engineers','minecraft-engineers','7–12','coding,engineering,games',
         'Minecraft Education: собственные американские горки, Redstone, switches, command blocks и инженерная логика. Обычно3 дня; лицензия лагеря действует только во время курса.',7),
        ('codecamp-masters','Minecraft Masters','minecraft-masters','Меню8–13; собственная course page7–12 — конфликт','coding,games',
         'Secret spy HQ: Redstone parkour, исчезающие двери/лифт, NPC, таймеры и escape room. Own course требует посещённый Engineers; общий FAQ допускает выбор по уровню — эквивалентный опыт согласовать. Шаблон Blast3D/GameOver на этой странице не её Minecraft syllabus.',None),
        ('codecamp-experts','Minecraft Experts','minecraft-experts','8–13','coding,games',
         'После как минимум одного Minecraft camp: command blocks и MakeCode, собственные инструменты, Elytra маршрут, арена, escape room и связанная adventure map. Обычно3 дня; отдельная лицензия нужна для продолжения дома. Чужое типовое3D расписание не принято за план Minecraft.',8),
        ('codecamp-animation','Animation','animation','7–10','coding,art,games',
         'Два дня stop-motion: сценарий/storyboard, LEGO персонажи, съёмка и монтаж в парах. Equipment rental включена; для продолжения дома своя app. Ни LEGO robotics, ни три дня generic3D timetable из нижнего шаблона сюда не перенесены.',7),
        ('codecamp-ai','AI Camp','ai-camp','9–13; FAQ одновременно требует аккаунт13+','ai,art',
         'Два дня: generative AI, computer vision, ограничения/мифы и comic с онлайн-инструментами. FAQ просит Microsoft account для13+, хотя camp9–13: нужен допустимый доступ для младших, возраст не меняем. Самостоятельная ML-разработка или robotics не обещаны.',9),
    ]
    ai_dates=[('2026-10-05','2026-10-06','winterthur','Winterthur · Liebestrasse Parish Hall'),
              ('2026-10-15','2026-10-16','zurich','Zürich · Greencity Maneggplatz'),
              ('2027-02-11','2027-02-12','aarau','Aarau · School Gönhard'),
              ('2027-02-11','2027-02-12','basel','Basel · Quartierzentrum Bachletten'),
              ('2027-02-16','2027-02-17','wettingen','Wettingen · School Wettingen'),
              ('2027-02-18','2027-02-19','steinhausen','Steinhausen · Chilematt Center')]
    for slug,title,path,age,themes,programme,minimum in code_courses:
        ai=slug=='codecamp-ai'; animation=slug=='codecamp-animation'; mine='Minecraft' in title
        variants=[dict(start=a,end=b,variant_key=k,label=k,place=place,source=CODE+'camps/ai-camp',
                       price='FAQ ориентирCHF120/день, не тариф выбранного AI-заезда; полный счёт неизвестен',
                       proof='Оба дня/год и конкретная площадка указаны на собственной AI course page; winter overview даёт лишь старты и не раскрывает язык этой группы.')
                  for a,b,k,place in ai_dates] if ai else None
        emit(slug,'Code Camp Switzerland · '+title,'Швейцария','CHE',
             'Швейцария · конкретный кампус выбранной смены; общая сеть также есть в Liechtenstein',themes,'day',age,
             'Own FAQ: язык зависит от конкретной смены/площадки. EN интерфейс не доказывает EN занятия; EN/ES/RU преподавание выбранного курса не установлено.',
             programme+' Внутренняя medal/graduation не международная соревновательная награда.',
             ('Шесть точных AI-заездов2026–27 в шести городах; один уже5–6 октября. Свободные места/язык не доказаны.' if ai else
              'Winter2026/27 объявлен, но конкретный '+title+' с полными датами/языком не установлен. Spring2027 registration обещана с октября2026, Summer2027 с марта2027; это сроки открытия, не смены.'),
             dict(year=None,label='Общий FAQ: околоCHF120/день; точная цена '+title+' и доплаты выбранной смены неизвестны. Voucher50–363 не цена курса.',
                  included=('Прокат устройства включён для Animation; ' if animation else '')+'надзор и учебная программа. Полный пакет зависит от смены.',
                  extras=('Для Minecraft: своё совместимое устройство, установленный Minecraft Education; лицензия только на курс. ' if mine else
                          'Для AI: устройство с webcam/браузером, допустимый аккаунт для младшего — не решён. ' if ai else
                          'Для coding: своё устройство с физической клавиатурой либо аренда с неизвестной обычной ценой. ' if not animation else '')+
                         'Lunch/snack/water свои. Late replacement менее72ч/в первый деньCHF50 по FAQ, не обычный прокат. Жильё/дорога отдельно; sibling discount есть без опубликованного размера.',
                  deposit='FAQ допускает перенос/voucher, частичный возврат после первого дня при письменном обращении; дальше нет. Точная сумма/порог не опубликованы. Terms содержит Australian law/AUD и©2018 рядом с Swiss address: текущие швейцарские условия отмены/страхование нужны отдельно.'),
             'Дневной лагерь; общая FAQ прямо исключает ночёвки.',
             fit('unknown' if minimum is None else 'conditional',
                 'Возраст9–10 в2027; '+('граница Masters расходится, нужен уровень Engineers и выбранная EN группа.' if minimum is None else
                 'для AI2026 только после9-летия, нужен допустимый аккаунт/EN группа; в2027 возраст9–10 подходит.' if ai else
                 'возраст подходит, но уровень/клавиатура/предшествующий курс и EN группа требуют согласования.')),
             fit('unknown' if minimum is None else 'conditional' if minimum==7 else 'later',
                 'Masters7–12 против8–13: допуск младшего не установлен.' if minimum is None else
                 'Только после7-летия в2027; в2026 ещё младше. EN группа/уровень и даты не подтверждены.' if minimum==7 else
                 'Минимум'+str(minimum)+'; Оскару6–7 в2027, пока будущая ступень.'),
             'Содержательный '+('AI-кандидат с датами, но нерешённым младшим аккаунтом.' if ai else
                              'технический трек с описанным итоговым проектом; язык и конкретная смена требуют проверки.'),
             ['EN выбранной группы/внешний иностранный приём, точный возраст и опыт, даты/места, полный тариф/аренда/сиблинг, действующий Swiss refund/страхование.' +
              (' Допустимый доступ к AI несовершеннолетнему без изменения возраста.' if ai else '')],
             [src('Конкретный curriculum, возраст и длительность',CODE+'camps/'+path),
              src('FAQ: язык по смене, тариф-ориентир, оборудование и питание',CODE+'faq'),
              src('Прогрессия и конфликты общего меню',CODE+'unsere-camps'),
              src('Terms с австралийскими реквизитами; применимость уточнить',CODE+'terms-conditions')],
             status='published_2026_27' if ai else 'next_unannounced',variants=variants)

    for drones in [False, True]:
        emit('issh-techlabs-drones' if drones else 'issh-techlabs-robots',
             'ISSH × TechLabs · '+('Autonomous Drones11+' if drones else 'Robotics7–10'),
             'Швейцария','CHE','ISSH · Mühlentalstrasse280 ·8200 Schaffhausen',
             'coding,engineering'+(',robotics' if not drones else ''),'day','11+' if drones else '7–10',
             'Для7–10 собственная school page прямо DE/EN-speaking environment. Это билингвальная среда, не гарантия EN всех технических инструкций; язык drone11+ отдельно не указан.',
             ('Первый деньEMPA Drone Hub, затем simulator→полёт реальным дроном indoor→код автономных миссий; утром часть дней общие выезды/активности.' if drones else
              'Сборка/программирование собственного робота, underwater mission, вулканы/сенсоры и финальное задание. Во второй половине дня выезды, включаяEMPA Drone Hub; соревнование внутри лагеря.'),
             'Архив13–17 июля2026,09–16. Новые смены2027 не объявлены в прочитанной странице; прошлый заезд не внесён в будущий ICS.',
             dict(year=2026,label='АрхивCHF650 /5 дней на ребёнка; цена2027 неизвестна.',
                  included='Учебная программа и заявленные активности; состав питания/материалов/трансфера/страхования не раскрыт.',
                  extras='Жильё семьи/дорога отдельно, подарок робота/дрона домой не обещан; equipment/lunch/экскурсионные сборы уточнить.',
                  deposit='Сроки/аванс/отмена/внешний индивидуальный приём конкретного нового лагеря не опубликованы.'),
             '09–16 дневной; постоянный school boarding programme не означает ночёвки в этом лагере.',
             fit('later' if drones else 'conditional','Для11+ только будущая ступень.' if drones else '9–10 в2027 соответствует архивному7–10; EN teaching и повторение подтвердить.'),
             fit('later' if drones else 'conditional','До11+ ещё рано.' if drones else 'Только после7-летия в2027; новый заезд/язык неизвестны.'),
             'Технически содержательная школьная программа с конкретной последовательностью проектов; дата/цена архивные, международный результат не обещан.',
             ['2027/cohort/места/внешний иностранный допуск, EN конкретной группы, доля технических часов, gear/home kit/full invoice/отмена.'],
             [src('Собственная school calendar2026, две age groups и syllabus',ISSH),src('Школьный STEM camp, не новый датированный набор','https://www.issh.ch/holiday-camps/stem-camp')],
             confirmed=['EN','DE'] if not drones else [],role='camp_life' if not drones else None)

    forest_dates=[('2026-10-19','2026-10-23',450,'10–16'),('2027-02-08','2027-02-12',450,'10–16'),
                  ('2027-04-05','2027-04-09',450,'10–16'),('2027-07-05','2027-07-09',480,'10–17'),
                  ('2027-07-12','2027-07-16',480,'10–17'),('2027-07-19','2027-07-23',480,'10–17')]
    variants=[dict(start=a,end=b,variant_key=a.replace('-',''),label='Holiday week · '+hours,
                   price='EUR'+str(fee)+' tuition +40 питание/перекусы за неделю ='+str(fee+40)+' /ребёнок; ранний/поздний сервис отдельно',
                   source=FOREST,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'],
                   proof='Own2026/27 schedule с шестью точными неделями, EN full-day/open external children, часами и сезонными ценами.')
              for a,b,fee,hours in forest_dates]
    emit('forest-paris-holidays','Forest International School Paris · Holiday Camps','Франция','FRA',
         '28 Rue de Tour d’Echelle ·78750 Mareil-Marly · запад Парижа','general,languages,science,art,sport','day','2–12, дети школы и внешние',
         'Собственная французская страница прямо заявляет дни на английском на лесном кампусе, а не только отдельный урок. EN camp-life подтверждён; специальных robotics занятий не заявлено.',
         'Природа, наблюдения/исследования, творческие проекты, игры и outdoor. Летом swimming в школьном бассейне и тихое время в лесу. Wednesday MasterClasses — отдельная услуга, сейчас только waitlist; её школьный тариф не цена лагеря.',
         'Шесть недель2026–27:19–23 октября;8–12 февраля;5–9 апреля;5–9/12–16/19–23 июля. Осень/зима/весна10–16, лето10–17.',
         dict(year=2027,season='2026/27',label='EUR450/неделя осень-зима-весна или480 лето; питание/перекусы+40 =490 /520. Двум980 /1040, до транспорта и extended hours.',
              included='Каникулярные активности и надзор в опубликованные часы; платное питание/перекусы40/неделя показаны отдельно.',
              extras='Летом приём09 и выдача18:40/день; единицу/включение обоих концов дня уточнить. Транспорт Saint-Germain/Le Pecq/Paris16 по запросу без цены; жильё семьи/перелёт отдельно.',
              deposit='Договор оплаты/аванс/отмена и места не раскрыты на выбранной programme page.'),
         'Дневной лесной школьный кампус, ночёвок нет.',
         fit('candidate','8–10 в2026–27 входит2–12; подтвердить группу по опыту и внешний иностранный приём.'),
         fit('candidate','5–7 в2026–27 входит2–12; EN уже доступен, подтвердить возрастную группу и бытовую готовность.'),
         'Один из конкретных общих английских вариантов обоим в семейной поездке во Францию, с зимними и летними датами/сметой.',
         ['Группа/места и индивидуальный приём иностранных детей, недельная тема/ratio, питание/transport/40 extended hours, страховка/contract/refund.'],
         [src('EN дни, внешние дети, все шесть недель и fees2026/27',FOREST)],
         status='published_2026_27',confirmed=['EN'],priority=['both','general'],variants=variants,role='camp_life')

    for preschool in [True, False]:
        emit('eib-monceau-preschool' if preschool else 'eib-monceau-science',
             'EIB Monceau · '+('Castle / Dragons Preschool' if preschool else 'Mystères de la Science / Coding'),
             'Франция','FRA','6 avenue Van Dyck ·75008 Paris','general,languages,art,sport' if preschool else 'general,science,coding,sport',
             'day','2,5–5; maternelle' if preschool else '6–11; primaire',
             'Собственная карточка этого лагеря прямо immersion totale en anglais. Внешние дети допускаются; постоянное зачисление в EIB не требуется.',
             ('Сказочные роли/истории, творческие задания, командные игры, спорт и маршруты в Parc Monceau.' if preschool else
              'Опыты с плавучестью, цветами и реакциями; научные наблюдения, coding и спорт. Язык/формат camp EN, но платформа/часы coding/робототехнический набор не названы.'),
             '19–23 октября2026,08:30–17; будущие смены2027 на этой странице не объявлены.',
             dict(year=2026,label='EUR650/неделя ребёнку с обедами; двое в подходящих разных/одной группе1300 до иных сборов.',
                  included='Опубликованный дневной camp и lunches.',extras='Состав snacks/gear/страхования/экскурсий, sibling/registration fee требуют итогового счёта; семейное жильё отдельно.',
                  deposit='Срок заявки/предоплата/отмена на выбранной странице не названы; регистрационный портал не заполняли.'),
             'Дневная школа, не каникулярный пансион.',
             fit('not_eligible' if preschool else 'candidate','Матвей старше5.' if preschool else '8–9 входит6–11; primaire группа/сложность coding ещё согласовать.'),
             fit('conditional','Пока5 — возрастной кандидат, после6-летия нужен primaire, не preschool.' if preschool else 'Только после6-летия и допуска в primaire; день рождения/класс неизвестны.'),
             'Конкретная английская '+('младшая группа Оскару с отдельным старшим научным вариантом для брата.' if preschool else 'научная неделя Матвею, обоим после6-летия Оскара; уровень кодинга пока неизвестен.'),
             ['День рождения/школьная категория Оскара, места и внешний иностранный приём, EN темы/coding платформа/часы, all-in и cancellation.'],
             [src('Две конкретные английские программы2026, возраст/цена/внешний приём',EIB)],
             status='published_2026',confirmed=['EN'],priority=['general'],sessions=[['2026-10-19','2026-10-23']])

    for levallois in [False, True]:
        emit('beelingue-levallois-autumn' if levallois else 'beelingue-paris-autumn',
             'BeeLingue Academy · '+('Levallois Monster Adventure' if levallois else 'Paris Autumn Magic'),
             'Франция','FRA','Playdate ·80 rue Rivay ·92300 Levallois-Perret' if levallois else '49 rue de Prony ·75017 Paris',
             'general,languages,art,sport'+('' if levallois else ',science'),'day','5–10' if levallois else '3–6 и7–10; две возрастные группы',
             ('На второй неделе подтверждён English Camp15–17; DIY14–15 и ludothèque17–18 названы отдельно, EN всей жизни/партнёрской площадки ещё уточнить.' if levallois else
              'Web/PDF прямо100% EN для тематического лагеря: утренние language/play, послеобеденные arts и theatre. Язык внешних экскурсионных операторов отдельно не установлен.'),
             ('Monster crafts14–15, English projects/roleplay15–17 и свободная ludothèque17–18. Неделя проходит у Playdate, парижский центр в эти даты camp не проводит.' if levallois else
              'English Club/Fun09–12, DIY/Art14–15, Beelingue Club15–17, свободная игра. Во вторник Musée de l’Illusion, четверг ClimbUp; спорт в паркеПн/Ср/Пт по погоде. Это общий язык/arts/science play, не robotics интенсив.'),
             '26–30 октября2026,14–18, выбор дней/недели.' if levallois else '19–23 октября2026,09–17; приём08:30, ludothèque17–18 отдельно. Выбор дней/полудня/недели.',
             dict(year=2026,label=('EUR225/5 послеобеденных дней14–18;50/день или15 за ludothèque17–18. Применимость семейного annual30 и siblingdiscount именно партнёрской недели подтвердить.' if levallois else
                  'EUR495/неделя09–17;225 за5 утр или5 послеобеденных полудней;115/день полный. Две экскурсии+25 каждая =545/ребёнок; двум1090 до annual family30/скидки. При применении второго −10% к495 и annual30:1070,50 двум, условный расчёт не счёт.'),
                  included='Выбранные английские/творческие блоки; тарифы TTC. Для Paris excursions25 включают bus и entrance, а не tuition.',
                  extras=('Личные перекусы, дополнительная опека/сервис и полный invoice партнёра ещё нужны.' if levallois else
                          'Свои lunchbox/snack. Lunch supervision12–14 отдельно15/день или75/неделя для выбранного неполного пакета; не добавлено автоматически кfull-day. Ludothèque17–18 ещё15/день или75/неделя;08:30 цена не установлена.')+
                         ' CGDV annual registration30 на семью; применимость camp и уже оплаченный год уточнить. Жильё/дорога отдельно.',
                  deposit='CGDV ateliers: отмена минимум48ч, позднее без возврата; annual30 не возвращается. Это общие workshop terms, отдельный camp contract и право раннего возврата не установлены. Фото по умолчанию могут использовать до возражения; согласий не принимали.'),
             'Дневной/послеобеденный; пансион не предложен.',
             fit('candidate','Матвею8–9, соответствующая возрастная группа; уровень/места уточнить.'),
             fit('candidate','Оскару5–6, соответствует группе; внешнее индивидуальное участие и режим уточнить.'),
             'Конкретная общая английская каникулярная программа обоим; '+('вторая площадка и роль15–17 отделены от Paris.' if levallois else 'понятный дневной/полудневный выбор и экскурсионные доплаты.'),
             ['EN всех нужных блоков, места/иностранные дети, annual30/second-child10%/excursions/extended hours в счёте и отдельный camp cancellation.'],
             [src('Конкретные две площадки/возрастные группы/режим',BEE+'autumn-camp'),
              src('PDF2026: визуальные timetable/tuition/extras/sibling',BEE+'autumn-camp/AUTUMN-CAMP-2026.pdf'),
              src('Общие CGDV ateliers, не подтверждённый отдельный camp contract',BEE+'cgdv')],
             status='published_2026',confirmed=['EN'],priority=['both','general'],
             sessions=[['2026-10-26','2026-10-30']] if levallois else [['2026-10-19','2026-10-23']],role='language_lessons' if levallois else None)


def extend_report_v100(report):
    report['shortlist'] += [
        dict(label='Франция · общий английский календарь обоим',slugs=['forest-paris-holidays','eib-monceau-science','eib-monceau-preschool','beelingue-paris-autumn','beelingue-levallois-autumn'],
             reason='Forest публикует зиму/весну/лето2027 и английские дни, включая внешних детей. EIB: Оскару preschool пока5, primary после6; BeeLingue две разные площадки/режимы. Выбор редакционный по семье; места, точный допуск и all-in ещё нужны.'),
        dict(label='Швейцария · технический проект и следующий уровень',slugs=['cosmo-mornings','cosmo-full-days','codecamp-spark','codecamp-ignite','codecamp-blast','codecamp-web','issh-techlabs-robots','issh-techlabs-drones'],
             reason='Micro:bit→Maqueen, blocks→JavaScript→3D/website и robot→autonomous drone показывают разные уровни/результаты. EN Cosmo/CodeCamp и отдельный camp age не подтверждены; ISSH2026 архив, DE/EN environment младших не гарантия всех уроковEN. Это сравнение треков, не рекомендация купить.'),
        dict(label='Швейцария · Minecraft/Animation/AI',slugs=['codecamp-engineers','codecamp-masters','codecamp-experts','codecamp-animation','codecamp-ai'],
             reason='Minecraft требует Education и временную лицензию, Animation2дня с арендой, AI2дня с точными датами и нерешённым13+account при возрасте9–13. Возраст Masters конфликтует между меню/курсом; язык каждой смены требует подтверждения. Внутренние медали не международные победы.')]
    report['gaps'] += [
        dict(country='Швейцария',iso='CHE',provider='v100 · Cosmo, Code Camp и ISSH: язык/возраст по конкретной программе',
             detail='CosmoPDF уточняет Пасху280 и невозвратные условия, но не camp minimum/EN. CodeFAQ требует13+AI account при9–13, Masters7–12 vs8–13, termsAustralian2018; public listing вернул только JS shell, course/fee/language не доказаны. ISSHroboticsDE/ENenvironment2026, droneEN/2027 не установлены.',
             next_action='Проверить EN/возраст/foreignintake каждого заезда, допустимый младший AI access, точный invoice/Swisscontract, syllabus/gear/ratio/места.',url=CODE+'faq'),
        dict(country='Швейцария',iso='CHE',provider='v100 · Florimont / Futurekids: партнёры и языковые границы',
             detail='Florimont2026: Futurekids5–14 half-days robotics/Minecraft, TechSpark9–16 и AlbertSchool15–18 EN; последний только futureage. Futurekids ownpage вернул пустой JS shell без syllabus/fee/language. Autumn19–23Oct4–9CHF810: EN интерфейс не teacherproof. Дубликат TechSpark не создан.',
             next_action='Получить programme-specific own body/EN teaching/полный2027invoice/terms/внешний допуск; AlbertSchool исследовать как будущий entrepreneurshipтрек.',url='https://www.florimont.ch/en/summer-camps/'),
        dict(country='Франция',iso='FRA',provider='v100 · Planète Sciences English и школьные недели',
             detail='Grasse Sciences in English7–12,19–23/26–30Oct2026 по190EUR; только title/details, syllabus/часы/полный пакет/boarding не опубликованы. Не объявлен top camp без этих условий. Forest/EIB/BeeLingue добавлены с собственными датами/программами; campcontract ещё нужен.',
             next_action='Подтвердить science teaching language/режим/syllabus/all-in/приём иностранцев и минимальный возраст; новые2027 смены отдельно.',url='https://www.planete-sciences.org/mediterranee/sejour-de-vacances/'),
        dict(country='Испания / Франция',iso='ESP',provider='v100 · повторная проверка архивов не создаёт новый сезон',
             detail='FAISL PDF визуально вновь не содержит ghost100%EN/grade старого скрытого слоя; прежняя осторожная карточка сохранена. StGeorge robotics2026 прайс/6–10 подтверждены selectedpage9, не2027. Lacunza толькоseason2027/6–13/триформата; ILC dates/prices без года. Все четыре досье без новых доказательств оставлены неизменными.',
             next_action='Новыеprogramme-specific2027dates/prices/teacherlanguage/fullcontracts и youngerboardingintake; не переносить oldprices/form2024/hiddenPDFtext.',url='https://www.lacunza.es/es/campamentos/lacunza-camp')]
