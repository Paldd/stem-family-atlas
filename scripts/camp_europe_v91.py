"""Programme-level European follow-up, with visible PDF evidence and season boundaries."""
from copy import deepcopy
from camp_americas_v90 import clean_profile, readable

CHECKED = '2026-10-05'
LAS = 'https://summer.las.ch/'
IS = 'https://ischool.es/'
FAI = 'https://www.faisl.com/'
ACTION = 'https://www.action-sejours.com/'
LAS_FLYER = LAS+'fs/resource-manager/view/4766625b-d2b7-4ecd-b46d-415f7663764b'
LAS_TERMS = LAS+'fs/resource-manager/view/292d3d1a-3227-4b74-80f7-7a83f646c61c'
ACTION_CARD = ACTION+'sejour-linguistique-adolescent-et-enfant/france/american-camp-in-saint-pardoux/'
FAI_PDF = FAI+'wp-content/uploads/2026/05/TRIPTICO-CAMPAMENTO-TECNOLOGICO-2026.pdf'
FAI_FORM = FAI+'wp-content/uploads/2026/05/Documento-de-Inscripcion-2026-escuela-tecnologica-Form-1.pdf'


def add_europe_v91(add, src, fit, P):
    start = len(P)
    def fee(year, label, included, extras, deposit):
        return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)
    def source(p, title, url):
        if url not in [s['url'] for s in p['sources']]:
            p['sources'].append(dict(title=title, url=url, checked=CHECKED))

    # The existing school stay and a chosen morning intensive are alternative tracks.
    las = next(p for p in P if p['slug']=='las')
    las['checked'] = CHECKED
    las['age'] = 'Junior 9–12; Senior 13–16 — подтверждено собственным flyer Summer 2027'
    las['language'] = 'EN в общении с соседями по комнате; утром выбор English или French language track либо отдельного курса. Язык AI & Python и других предметных курсов ещё подтвердить.'
    las['confirmed_instruction_languages'] = ['EN']
    las['language_evidence_role'] = 'camp_life'
    las['programme'] = 'Один morning track на всю смену: языки EN/FR трёх уровней, Leadership (Alpine Leadership или Changemakers Launchpad), либо Enrichment (Performing Arts, Inquiry Lab, AI & Python). Flyer 2027: общий утренний блок 09–12, afternoon club 14–15:45, activities 16:15–17:45, socials 20:30–21:15. Это расписание дня, не обещанные 15 часов техники каждую неделю. AI & Python выделен отдельным вариантом, не добавлен каждому участнику общего лагеря. Family Program — группа детей с 2–3 counselors, не проживание родителей в лагере. На странице Register набор 2027 ещё Coming Soon; октябрьское обещание не подтверждает открытую регистрацию.'
    las['family_fit'] = dict(matvey=dict(status='conditional', detail='В 2027 будет 9–10: Junior 9–12 подходит по возрасту, но язык, выбранный track, его prerequisites и набор нужно подтвердить.'), oscar=dict(status='later', detail='До 9 лет младшая Junior программа недоступна; в 2027 Оскару 6–7.'))
    las['price']['included'] = 'Текущая FAQ подтверждает стандартный Geneva transfer в официальные дни при flights 09–18. Полный список room/board, instruction, computers, books, excursions, special gear и insurance есть в приложенном договоре 2026: включения сезона 2027 нужно подтвердить отдельно.'
    las['price']['extras'] = 'Leadership +CHF 500; European overnight adventure +1 500; нестандартный transfer +350 за ребёнка/направление. AI & Python отдельная доплата не указана, это не доказательство отсутствия доплаты. Договор 2026: UM +150 за каждый flight, personal expenses и dry cleaning отдельно — не подтверждённый тариф UM 2027.'
    las['price']['deposit'] = 'Страница 2027 по Booking Terms ведёт к General Booking Conditions 2026: CHF 2 000 deposit в счёт tuition, balance before 15 May 2026, все payments non-refundable; credit только по проверенным обстоятельствам (медицинское препятствие, visa denial, border closure, flight cancellation в последние 10 дней). Эти правила и дата оплаты не перенесены автоматически на 2027; нужен новый договор. Регистрация ещё Coming Soon.'
    las['accommodation'] = 'Пансион по возрасту/полу; FAQ обычно не разрешает братьям, друзьям и детям с одним родным языком жить вместе, исключения только Director. Свою стирку дети учатся делать с помощью команды; полотенца привозят. Родительский Family Camp этим названием не предложен.'
    las['questions'] = ['Подтвердить открытие набора 2027, доступность выбранного junior track, язык предметного преподавания, prerequisite level, точные учебные дни и новый договор/включения/UM/full invoice.']
    for s in las['sources']: s['checked'] = CHECKED
    for title, url in [('Morning tracks и содержание Python',LAS+'las-summer-programs/morning-program'),('Возраст / residential Families',LAS+'las-summer-programs/residential-life'),('2027 ещё Coming Soon',LAS+'register'),('Официальный flyer Summer 2027',LAS_FLYER),('По ссылке 2027 фактически договор 2026',LAS_TERMS)]: source(las,title,url)
    add('las-ai-python','Leysin American School · AI & Python: Build, Code, Create','Швейцария','CHE','Leysin · Chemin de la Source 3','coding,ai,engineering','boarding',
        las['age'], las['language'],
        'Отдельный morning Enrichment track: логика программирования, чистый код, алгоритмические задачи, инструменты разработчика и интерактивные Python applications. Итог — собственное работающее приложение с презентацией source code и решений. AI присутствует в названии, но отдельные модели ML, датасеты или часы AI не раскрыты; робототехника в этом курсе не обещана. Общий morning block 09–12 по flyer, фактические teaching days и младший уровень курса ещё неизвестны. Альтернатива general LAS track в те же даты, не дополнительная независимая поездка/другая школа.',
        las['timing']['label']+' Сам course описан на текущей morning page; junior availability требует подтверждения. Register 2027: Coming Soon.',
        deepcopy(las['price']),las['accommodation'],fit('conditional',las['family_fit']['matvey']['detail']),fit('later',las['family_fit']['oscar']['detail']),
        'Предметный кандидат Матвею: собственный код и конечный проект вместо одной демонстрации роботов; готовность младшего возраста к интенсиву ещё проверить.',
        las['questions'],[src(s['title'],s['url']) for s in las['sources']], status='published_2027',priority=['technical'],confirmed=['EN'],sessions=deepcopy(las['timing']['sessions']))
    P[-1]['language_evidence_role'] = 'camp_life'

    pre = next(p for p in P if p['slug']=='prefleuri'); pre['checked']=CHECKED
    pre['price']['label'] = 'Архив 2026, 5–14 лет: boarding 2/3/4/5/6 недель CHF 5 550 / 8 150 / 9 990 / 12 235 / 14 400; day 3 250 / 4 770 / 6 240 / 7 650 / 9 000. Скидка 10% от 4 недель уже включена; второму ребёнку 10%, но допускается только одна скидка — не складывать автоматически. Прайс 2027 не опубликован на прочитанной fee page; минимум пансиона 2 недели.'
    pre['price']['included'] = 'Пансион 2026: питание, daily laundry, форма, фото, занятия/спорт/поездки, medical/accident insurance. Day: Mon–Fri 09–18, weekends не включены; форма 2 tee-shirts + sweatshirt, уроки/спортивная техника/экскурсии. Обед day не выделен явно в day include list — подтвердить. Билингвальный Kindergarten 3–4; с 6 лет language classes EN/FR, не гарантия полного EN дня.'
    pre['price']['extras'] = 'Архив 2026: group Geneva CHF 250/направление только суббота/UM (arrivals 12–14, departures 11–13), individual CHF 600. Horse riding +300/неделю (2×2 ч, минимум 5 детей); Show Time с 8 +400, Extreme Adventure с 8 +500; Europa-Park с 10 +500, Swiss Tour с 10 +950 boarding, Expedition с 10 +600. Day родители обеспечивают страховку; опции/возраст и полный счёт 2027 нужны.'
    pre['price']['deposit'] = 'Текущие недатированные general terms: CHF 1 000 deposit в счёт цены, balance за 60 дней. Первая общая строка требует full payment для reservation, следующая подтверждает reservation с deposit — расхождение. Summer/Ski отмена за 60–45 дней: удержание 1 000; менее 45 дней требуется вся цена. Более 60 и точные границы summer не разъяснены. Winter отдельно: >60 дней удержание 1 000, <60 вся цена, ровно 60 не указано. Подтверждённая illness/travel inability/death: перенос оплаты в будущий camp, cash refund не обещан. Поздний приезд/ранний отъезд/пропуски без скидки. Для visa invitation требуют full invoice paid и passport; условия не приняты.'
    pre['accommodation'] += ' По terms устройства/часы с камерой и tracking сдают, AirTags только в багаже. Визиты родителей только по предварительному разрешению; связь по правилам, сообщаемым при booking.'
    pre['questions'] += ['Получить правила/прайс 2027: отмена summer >60 дней и точные границы, deposit vs full payment, обед day, языки всех занятий, обязательная страховка и связь.']
    for s in pre['sources']:
        if s['url'].endswith(('/summer/','/summer-fees/')):s['checked']=CHECKED
    source(pre,'General terms: summer/ski отличаются от winter','https://www.prefleuricamps.ch/en/general-terms-and-conditions/')

    # Same operator already exists. The 2026 location source resolves the country, not 2027 hotel.
    nat = next(p for p in P if p['slug']=='natuk-robotics');nat['checked']=CHECKED
    nat['price']['year']=2026
    nat['price']['label']='Найден архив HES 2026: inscription EUR 150 за booking + base 655/1 нед., 1 195/2, 1 750/3 + robotics 50 за каждую неделю + выбранное утро. С English classes (base includes) 1 неделя = EUR 855; Discovery morning +50 =>905; Active Adventure morning +125 =>980. Это расчёт по опубликованной формуле 2026, не цена 2027 и не полный счёт с дорогой/опциями.'
    nat['programme'] += ' Catalogue 2026 sample Mon–Fri robotics afternoon 16–19; это временной блок, не подтверждённые 15 часов чистой техники в 2027. Robotics age 6–16 отдельно от общего junior 6–13 / teen 14–17. При <4 participants practical guide позволяет отменить конкретный camp и заменить другим (доплата при более дорогом).'
    nat['price']['extras'] += ' Найден HES 2026: Barcelona Airport transfer 70 one-way/140 return (minimum 4 travellers; arrivals before 10:00, departure flights 15:30–19); Barcelona bus 40/80, Lleida 35/70. Gluten-free diet +30/нед., French/Spanish lessons +75/нед., optional cancellation insurance 35/45/55 за 1/2/3 недели; Port Aventura/Ferrari Land +135. HES price transport dates 29Jun–19Jul против brochure 28Jun–18Jul: транспорт будущего сезона не подтверждён.'
    nat['accommodation'] = 'HES location page и собственный catalogue 2026: Aparthotel Trainera***, Esterri d’Àneu, Lleida/Испания; EuroSki**** на robotics card расходится, не создана отдельная Андорра. Комнаты page 2–4 против brochure 3–6; состав группы/отель 2027 подтвердить. Day для местных residents 09:45–19:30 с обедом; weekend day activities доплачиваются, visitor admission неизвестен. Practical guide: родительские visits не разрешены; medication передают nurse, необходимые medicines отдельно.'
    nat['questions'] += ['Новый 2027 morning+robotics invoice/возраст, фактические дни/часы, hotel/room size, foreign day и документы, минимальная группа 4, laundry included vs 5/load, transport dates и pre-start cancellation.']
    for title,url in [('HES числовой price и формула 2026','https://www.hescamps.com/catalogos-0'),('HES location: Trainera в Испании','https://www.hescamps.com/campamentos-internacionales-en-los-pirineos'),('2026 programme/age/sample timetable','https://www.hescamps.com/sites/default/files/adjuntos/catalogo_natuk_2026.pdf'),('2026 guide: minimum group/laundry/visits','https://www.hescamps.com/sites/default/files/adjuntos/guia_practica_natuk_camps_2026.pdf')]:source(nat,title,url)

    unknown='Язык страницы ES не подтверждает ES преподавания; EN/ES/RU уроков и помощь на втором языке прямо не установлены. Иностранный приём уточнить.'
    isfee=fee(2026,'Архив Summer 2026: general public EUR 139/нед., 239 за 2 недели или 2 братьев, 335 за 3 недели или 3 братьев; четырёхдневная неделя 23–26 June 114. Affiliate/current pupil tier 125/225/320 и 100 за 4 дня только после проверки права на скидку. Прайс 2027 пока отсутствует.',
        'Обучение 25 часов/обычная неделя, early care с 08 и late pickup до 15 бесплатно. Техника и software используются на занятиях; подарок личного робота не обещан. Общий summer index заявляет ratio 10:1; programme capacity отдельно, не равна числу детей на педагога.',
        'Питание, страховка camp, foreign documents, travel и полный invoice неизвестны; жилья/пансиона нет.',
        'Общие Activity Conditions описывают annual after-school 2026–27, tuition 405/423, monthly direct debit и termination — не camp refund. Summer cancellation/deposit/media terms необходимо получить отдельно. Условия и consent не приняты.')
    isrows=[('ischool-constructors','Constructores Tech','6–8','Club Deportivo 20 bis, Logroño','robotics,coding,engineering',
        'Животные разных habitat: LEGO WeDo, Codey Rocky, Sphero Spark, Edison; возрастные игровые программы на компьютере/tablet, maker и механизмы движения. Beginners/multinivel, 12 places/turno.',
        fit('later','К 2027 Матвею 9–10: группа 6–8 уже младше него; выбрать Creadores Tech.'),fit('conditional','В 2027 6–7: возраст Constructores подходит, но язык, смена и внешний приём неизвестны.'),'constructores-tech'),
        ('ischool-creators','Creadores Tech','9+; recommended 9–12, верхний admission limit уточнить','Club Deportivo 20 bis, Logroño','robotics,coding,engineering,ai',
        'Retro videogames, LEGO Mindstorms EV3/Fischertechnik/пневматика, механика/датчики/стратегия роботов, maker и introductory AI. Внутренняя robot fighting league не является квалификатором VEX/WRO или международной медалью; 10 places/turno, beginners/experienced.',
        fit('conditional','9–10 подходит для рекомендованной группы; точный уровень, язык и новый набор нужны.'),fit('later','До 9 лет этот track недоступен.'),'creadores-tech'),
        ('ischool-minecraft','Minecraft Academy','8+, intermediate; верхний возраст не указан','Ibercaja Obra Social, Logroño; конкретный адрес не раскрыт','coding,engineering',
        'Командная 3D версия Logroño, urban planning, Redstone logic/commands и пространственное мышление; WineCraft mod моделирует виноградник/производство вина, не личное употребление алкоголя. Intermediate/уверенное владение Minecraft, 16 places/turno. Не курс физической робототехники.',
        fit('conditional','9–10 по возрасту, но intermediate Minecraft, язык и actual intake подтвердить.'),fit('later','До 8 лет этот курс недоступен.'),'minecraft-academy')]
    for slug,name,age,place,themes,programme,m,o,path in isrows:
        add(slug,'iSchool Logroño · '+name,'Испания','ESP',place,themes,'day',age,unknown,programme+' 09–14; free care 08–15. Summer page год 2026; карточка не раскрывает конкретные смены.',
            'Архив Summer 2026. Дат и полного прайса 2027 в прочитанных карточках нет; старые June/July/September не перенесены.',deepcopy(isfee),'Городской day course; проживание семьи и доставка детей отдельно.',m,o,
            'Содержательная техническая программа по возрасту; полезный оператор для семейного визита после подтверждения следующей смены и языка.',
            ['Уточнить 2027 dates, язык преподавателя/translation, возраст/уровень, precise venue, meals/insurance, стоимость для двух братьев и camp cancellation.'],
            [src('Собственная programme card и тарифный popup 2026',IS+'campamentos/'+path+'/'),src('Summer 2026, ratio и форматы',IS+'campamento-tecnologico-verano-2026/'),src('Activity Conditions: annual course, не camp refund',IS+'condiciones-de-las-actividades/'),src('FAQ/оператор, не доказательство языка',IS+'preguntas-frecuentes/')])

    tech='https://www.technomaticmalaga.com/campamentos-tecnologicos'
    add('technomatic-english-tech','Technomatic Málaga · English Creative & Tech Camp','Испания','ESP','Calle Salitre 40 Bis, 1A, 29002 Málaga','general,languages,robotics,coding,engineering','day','6–17, all English levels; B1/B2/C1 exam groups optional',
        'Own programme прямо: все creative activities на English, Robotics in English. Это EN programme 2026; будущий состав преподавателей/EN технику 2027 подтвердить.',
        'Английские творческие проекты, broadcasting, reader theatre, comics, Shark Tank pitch, debates/escape game, programming и robotics. B1/B2/C1 pull-out small groups для exam prep; общий вход all levels, B1 не обязательный порог. 10–14 half или до 17 full, project afternoon 14:30–17. Объём robotics/hardware и take-home неизвестен. Caption о regional VEX 1st place без year/category/team ID не проверенный результат школы и не summer qualifier. TOEFL-certified teachers — заявление оператора, экзамен/официальный сертификат детям не обещан.',
        'Опубликован именно Verano 2026: 27–31 July и 3–7 August; следующий 2027 ещё не объявлен.',
        fee(2026,'Half: EUR 95/1 нед.,170/2; full:125/1,215/2. Second sibling 50/нед. half или70 full: 2 ребёнка/1 нед.145/195; сочетание двухнедельного тарифа со sibling не установлено.',
            'Выбранные занятия/экзаменационная подготовка по уровню; full включает afternoon project, не подтверждённый обед.',
            'Extra afternoon для half +EUR 10/день; lunch/налоги/оборудование/страховка и итоговый счёт не раскрыты. Перелёт/семейное жильё/доставка отдельно.',
            'Camp deposit/cancellation/refund не найдены в programme page; прайс 2026 не действующее место/счёт 2027.'),
        'Day camp, без пансиона; удобен как часть семейной поездки в Málaga.',fit('conditional','Возраст подходит; новая смена 2027, реальные часы техники и место неизвестны.'),fit('conditional','6–7 входит в общий minimum6, но младший robotics cohort и новая смена требуют подтверждения.'),
        'Прямое подтверждение английской робототехники и конкретные старые цены; следующий сезон и объём техники ещё неизвестны.',
        ['Получить 2027 timetable/tech hours/platform, junior staffing/foreign admission, family fee/lunch/cancellation; подтвердить VEX результат через официальный event/team record отдельно.'],
        [src('Summer 2026: ages, English activities, dates/prices',tech)],confirmed=['EN'],sessions=[['2026-07-27','2026-07-31'],['2026-08-03','2026-08-07']])

    add('faisl-salamanca-summer','FAI SL & Rockbotic · Factoría de Inventores Tecnológicos','Испания','ESP','Calle Peña de Francia 1, 37007 Salamanca','robotics,coding,engineering,ai,science','day','Собственная web page: mayor de 6 años; включительность ровно 6 и верхний возраст уточнить',
        unknown+' PDF text extraction содержит старые 100% English / Primaria1–3 / 1July–26Aug, которых нет на видимом развороте 2026: эти строки не доказательство camp language/grade/dates. Oxford exam centre и отдельные English courses не делают этот tech camp английским.',
        'Шесть прошлых themed blocks: кино/Minions/Toy Story, Gaudí architecture, SuperMario space, ClashRoyale robot-defence, football robot/VAR scoreboard, Gulliver VR/AI decisions. Robotics/programming/3D/electronics/STEAM; на cover ещё drones, но конкретный drone block/time не обещан. PDF schedule 08–15 с tech projects12–14 и freebuilding14–15; web08–14 и robotics11:45–14 — конфликт времени. No prior programming needed, цифровой diary/video; подарок робота не установлен.',
        'Summer 2026: 25–26June,29June–3July,6–10/13–17/20–24/27–31July. Web intro ошибочно25June2025–31July2026; применяется dated2026 brochure/form. Нет новых дат 2027.',
        fee(2026,'EUR 40 за25–26June2026/2дня;70 за каждую из пяти полноценных недель. Все6блоков390 EUR за ребёнка по арифметике, не пакетная скидка. Прайс следующего лета неизвестен.',
            'Учебная программа/работа с техникой и digital journal; полный состав invoice, lunch и camp insurance не опубликованы.',
            'Жильё семьи/доставка отдельно; PDF park snack не доказывает included meal. Материалы домой/налоги/доплаты/иностранные документы уточнить.',
            'Summer2026 blank form: weekly bank direct debit/SEPA mandate, санитарное force-majeure закрытие завершает camp, refund clause не раскрыта. Form включает park crossing и media consent без time/geographic limit; не заполнено/не подписано. Web GeneralConditions регулируют website, не camp refund.'),
        'Дневной центр, без пансиона; время 14/15 требует согласования.',fit('conditional','Возраст >6 подходит, но будущий набор/язык и уровень unknown.'),fit('conditional','Только после уточнения strict >6; в2027 может быть6–7. Нет доказанного EN/ES admission или новой смены.'),
        'Подробные проекты/тариф/форма старого сезона; PDF проверен визуально, скрытый английский текст исключён из подтверждения языка.',
        ['Подтвердить age >6 / inclusive6, camp language, hours14vs15, лето2027/fee/refund/food/insurance и альтернативную оплату для иностранцев.'],
        [src('Own summer page: age, projects, hour/year conflicts',FAI+'robotica-educativa/escuela-tecnologica-en-salamanca/'),src('Видимый двухстраничный programme PDF2026',FAI_PDF),src('Blank form Summer2026: dates/fees/payment',FAI_FORM),src('Website terms, не договор camp',FAI+'condiciones-generales/')],sessions=[['2026-06-25','2026-06-26'],['2026-06-29','2026-07-03'],['2026-07-06','2026-07-10'],['2026-07-13','2026-07-17'],['2026-07-20','2026-07-24'],['2026-07-27','2026-07-31']])

    add('action-american-saint-pardoux','Action Séjours · American Camp Saint-Pardoux','Франция','FRA','Base les Chabannes, Saint-Pardoux / Compreignac, Haute-Vienne; возможная замена Meymac','general,languages,sport,art','boarding',
        'Карточка7–14, конкретная таблица October2026 только8–10 и11–14; для 7 лет конфликт, не считать допущенным',
        'Карточка прямо English от утреннего подъёма до сна; bilingual animateurs, культурные игры/творчество на EN. Новый метод без обычных language classes; не добавлено 10/16 часов из других центров.',
        'Общий immersion: Anglo-American traditions, vocabulary/tablegames, theatre/talent/karaoke, cooking/vlogs, sports/pool/ecology challenges и вечерние коллективные игры. Wizard option имеет5half-days magic/potions/runes/quest на EN, но на даты American Camp не добавлена автоматически. Робототехнического трека здесь не обещано. Старый linked PDF описывает19–25Oct2025/8–14; будущие даты берутся только из актуальной2026таблицы.',
        'Две конкретные Toussaint2026 смены18–24October и25–31October,7дней. Следующий summer/winter2027 для этого центра не объявлен.',
        fee(2026,'Числового тарифа в собственной programme table нет: personalized quote. EUR740 из агрегатора Mission Robotique не перенесены на American Camp.',
            'Полный пансион:4meal/day, packed lunch для выездов, residential staff24h. Цена transport/insurance/option неизвестна; прачечная описана для2недель, не включена автоматически в7days.',
            'Paris–Limoges train + private coach около40min предложены, включение вцену не подтверждено. Province/airport pre-transport по отдельному запросу≥2месяца; international travel/own insurance/medical costs не определены.',
            'Current flexible web offer: безairtransport отмена/изменение бесплатно до1месяца, operatorcancelrefundдо2месяцев; balanceза1месяц/no dossier fee. LinkedCGV фактически brochure baseline8April2019: holds15%≥30d/30%20–29/60%10–19/100%<10, insuranceoptional4%, без refund earlydeparture. Promo vsCGV и применимость к2026cohort/foreignpassport требуют нового письменного contract; deposit amount unknown. Ничего не принято.'),
        'Chabannes59beds, комнаты3–4, bathroomsharedмежду2комнатами; staff24h, 4meals. Карточка допускает перенос наMeymac, фактический campus и shared rooms подтвердить.',
        fit('conditional','В October2026 Матвею8–9: table8–10 по возрасту подходит; foreign intake/место/quote ещё нужны.'),fit('later','В October2026 Оскару5–6, ниже и card7 и actualtable8. В2027 до8 ещёнет.'),
        'Реальные ближайшие французские EN смены; младший возраст в конкретной таблице строже рекламной карточки, цена неизвестна.',
        ['Фактический age8vs7, campusChabannesvsMeymac, EN/cohort/foreign admission, места/quote/transport/insurance и приоритетный текущий договор отмены.'],
        [src('Own programme/table October2026',ACTION_CARD),src('Old linked programme:October2025, неcurrentdates',ACTION+'APP/mon/doc_mon/08b1b1db093cff9saint_pardoux_ac.pdf'),src('Current flexible offer/cancel/payment',ACTION+'conditions-reservation'),src('LinkedCGV,экономическаябаза2019',ACTION+'CGV%20Action%20S%C3%A9jours.pdf')],status='published_2026',confirmed=['EN'],sessions=[['2026-10-18','2026-10-24'],['2026-10-25','2026-10-31']])
    for p in P[start:]:
        p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
    for p in P[start:]+[las,pre,nat]:clean_profile(p)


def extend_report_v91(report):
    shortlist_start=len(report['shortlist']);gap_start=len(report['gaps'])
    report['shortlist'].extend([
        dict(label='Швейцария · предметный Python или общий младший лагерь',slugs=['las-ai-python','las','prefleuri','tasis','la-garenne'],reason='LAS Junior9–12 подтверждён flyer2027: Матвею предметный track после проверки prerequisites, Оскару ещё рано. RegisterComingSoon и linkedcontract2026 отдельно от2027price. Préfleuri подходит младшим, но price2026 и cancellation summer/winter разные; ENlanguageclasses не fullENcamp.'),
        dict(label='Испания · робототехника и английский без пансиона',slugs=['technomatic-english-tech','ischool-constructors','ischool-creators','ischool-minecraft','faisl-salamanca-summer','natuk-robotics'],reason='Technomatic прямо EN creative/robotics, архив2026 с siblingprices. iSchool6–8/9+ позволяет разный track обоим, но campteachinglanguageunknown; Minecraft8+ intermediate. FAI детальный2026programme/form, невидимыйEnglishtext не доказательство. NATUK найден2026base+morning+robotics855/905/980EUR1week, неfuturefee; visitor day/2027hotel уточнить.'),
        dict(label='Франция · ближайшее English immersion Матвею',slugs=['action-american-saint-pardoux','ilc','american-village','asp-paris-holiday-english'],reason='Action18–24/25–31Oct2026: actualtable8–10/11–14, Oscarрано; Englishcreativeactivitiesбезregularlessons и pricequote. ILCFUN6–9 оставлен кандидатомобоим, но его недатированныйпрайсне2027confirmation. Альтернативыразноговозрастасохранены, не утверждён мировойrank.')
    ])
    report['gaps'].extend([
        dict(country='Швейцария',iso='CHE',provider='v91 · LAS возраст, Python и год договора',detail='Прочитан flyerSummer2027:Junior9–12/Senior13–16, morning09–12. CurrentAI&Python содержит своёприложение/sourcecode, но prerequisites/точныйjunior/ENtechnicalhours иAIdepthunknown. Register2027ComingSoon, bookingterms ведут к2026PDF сbalance15May2026/nonrefund/UM150, не новыйcontract. FamilyProgram — детскаяcounselorgroup, не campдляродителей. Préfleuri2026fee/reductionsне2027; summer/Ski60–45/minus1000 vswinter60boundary, cashrefundнеобещан.',next_action='Получить реальный2027cohort/contract/invoice, languagepertrack, младшиегруппы, preciseinstructiondays и обязательныеextra. Worldauditactive.',url=LAS+'dates-and-prices'),
        dict(country='Испания',iso='ESP',provider='v91 · видимый PDF и реальная цена техники',detail='FAI2026PDF визуальнонепоказывает oldEnglish/Primaria1–3/July–Augustстроки изtextlayer; campEN/gradesнедоказаны. Web>6,08–14 vsPDF08–15, web2025intro/2026bodyconflict, blankSEPAform/refundunknown. TechnomaticENrobotics2026/dateprice not2027; VEXcaptionбезevent/yearнеschoolleaderproof. iSchool139/239/335general vs125/225/320affiliatetiers, actualcamprefundнет:termsannualcourse. NATUK2026собственныйTraineraSpain подтверждён; EuroSkioldcardнеотдельнаяАндорра, roboticsafternoon16–19/минимум4/2026priceformula855/905/980, transportdates29–19vs28–18.',next_action='Новые2027dates/techlanguage/foreignadmission/campcontracts, fullprice/room/venue иvisitorDay. Архивы не перенесены в будущий календарь.',url=FAI_PDF),
        dict(country='Франция',iso='FRA',provider='v91 · Action ближайшие смены и старые предложения',detail='AmericanSaintPardoux actualOctober2026table8–10/11–14 противcard7–14. Price personalized, ENбезtraditionalclasses, Wizard5halfdaysoptionнекаждому. LinkedprogrammePDF2025 не2026dates, CGVbaseline2019 vscurrentflexibleweb1monthoffer конфликт. Bretagne/Santec, WinterAuvergne иRoches/Chamberetownpages прямоno séjour en ce moment: не добавленыкакopen2027programmes. MissionRobotique740EURизsecondaryнеперенесён вverifiedcamp.',next_action='Camp-specificcurrentcontract/quote/age/foreigncohort, далее2027seasonoffers и прочиеFrance/Europe. Полный мировойscope/Asia/Americas/школы/лиги/выставкисохранён.',url=ACTION_CARD)
    ])
    for q in report['shortlist'][shortlist_start:]:
        for key in ['label','reason']:q[key]=readable(q[key])
    for q in report['gaps'][gap_start:]:
        for key in ['provider','detail','next_action']:q[key]=readable(q[key])
