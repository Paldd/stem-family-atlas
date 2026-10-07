"""Primary-source France/Spain programme dossiers; no inferred future seasons."""
def add_europe_programmes(add,src,fit,profiles,checked):
    def price(year,label,included,extras,deposit='Полные условия оплаты и отмены выбранного сезона ещё подтвердить.'):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def variants(p,rows,keyed=False):
        p['timing']['session_details']=rows
        p['timing']['sessions']=[[v['start'],v['end']] for v in rows]
        if keyed:p['timing']['variant_keyed']=True
    def day(start,end,label,fee,place,url,**kw):
        return dict(start=start,end=end,label=label,price=fee,place=place,source=url,
                    formats=['day'],date_scope='day_camp_window',**kw)

    ermitage='https://fr.ermitage.fr/activities/holidaycamp'
    form='https://docs.google.com/forms/d/e/1FAIpQLSd5ZjWstf5pwAjF5M2bCTqpP3ZF9-JdRX-XT-i_BrOYe7F3vA/viewform?usp=dialog'
    add('ermitage-holiday','Ermitage · Holiday Camps','Франция','FRA','Maisons-Laffitte / Париж',
        'general,languages,sport','day','Текущая осенняя программа 4–10: группы 4–6 и 7–10; форма 2026/27 указывает 4–11 — границу подтвердить',
        'Осенью EN/FR билингвально. Форма предлагает English / French / без предпочтения для camp leaders; это пожелание, распределение и язык будущих смен подтвердить.',
        'Осенний Wizards Academy: тематические игры, творчество, прогулки и кулинарные опыты. Другие каникулы объявлены, но такой же сюжет или отдельная робототехника на них не гарантированы.',
        '2026: 19–23.10, 09–18. Объявлены 2027: 08–12.02, 05–09.04, летнее окно 28.06–16.07, 23–27.08. Летнее окно не одна непрерывная трёхнедельная смена.',
        price(2026,'Осень 2026: €610/неделя или €135/день. Тарифы будущих каникул 2027 не опубликованы в прочитанных источниках.',
              'Тематические занятия; обед и его включение в цену подтвердить.',
              'Жильё семьи, дорога и условия питания отдельно.'),
        'Дневной лагерь; школьный интернат Ermitage не означает ночёвки этой младшей программы.',
        fit('candidate','Возраст 9–10 подходит текущей границе; подтвердить группу будущей смены.'),
        fit('candidate','Есть младшая группа 4–6; после 7 лет другая группа. Уточнить возраст на первый день.'),
        'Кандидат на совместную семейную поездку в Париж с английским сопровождением и календарём разных каникул.',
        ['Подтвердить English leaders, возрастную группу, питание, часы и цены именно выбранной смены 2027.'],
        [src('Текущая программа и календарь каникул',ermitage),src('Публичная форма Holiday Camps 2026–2027 · прочитана без отправки',form)],
        status='partial_2026_27',priority=['both','general'],confirmed=['EN'])
    p=profiles[-1];p['language_evidence_role']='camp_life'
    rows=[]
    for start,end,label in [('2026-10-19','2026-10-23','Осень · Wizards Academy'),('2027-02-08','2027-02-12','Зимние каникулы'),('2027-04-05','2027-04-09','Весенние каникулы'),('2027-06-28','2027-07-16','Летнее окно · выбор недель уточнить'),('2027-08-23','2027-08-27','Перед учебным годом')]:
        rows.append(day(start,end,label,'€610/нед. или €135/день · осень 2026' if start.startswith('2026') else 'Тариф 2027 ещё не опубликован',p['place'],ermitage,
            accommodation='Дневной; точные часы будущей смены и семейное жильё отдельно.',
            proof='Даты опубликованы в Holiday Camp calendar 2026/27. Лето обозначает дневное окно, а не подтверждённую непрерывную смену; возраст, часы и цена будущих программ уточняются.'))
    variants(p,rows)

    wander='https://www.wanderandwonderclub.com/summer-camp'
    product='https://www.wanderandwonderclub.com/product-page/summer-nature-camp'
    holiday='https://www.wanderandwonderclub.com/holiday-camp'
    add('wander-nature','Wander & Wonder · Nature Camps','Франция','FRA','Париж / Saint-Germain-en-Laye',
        'general,languages,sport,science','day','3–12',
        'English immersion, сотрудники EN/FR; английский подтверждён для общих outdoor-активностей.',
        'Лес, наблюдение природы, укрытия, игры и творчество; дневной outdoor-отдых. Летние недели Пн–Пт 09–16; конкретную площадку выбирают при записи.',
        'Лето 2027: 05–09.07, 12–16.07, 19–23.07, 26–30.07, 23–27.08. Также 19–30.10.2026 и 08–19.02.2027. Весна напечатана как 2017: в календарь 2027 не перенесена.',
        price(2027,'Летний продукт: €380/неделю; summer-page обещает €360/нед. при двух и более неделях. Holiday: €380 за одну неделю или €720/две. Применение скидки в итоговом расчёте подтвердить.',
              'Дневные занятия и два перекуса; это указано и для летних, и для holiday-недель.',
              'Обед с собой, жильё семьи, дорога и одежда для outdoor.'),
        'Без ночёвок; Bois de Boulogne или лес Saint-Germain-en-Laye, точная точка встречи после выбора площадки.',
        fit('candidate','Соответствует 3–12; уточнить старшую группу.'),fit('candidate','Соответствует 3–12; нужна готовность к дню на природе.'),
        'Практичный общий английский day camp для обоих; подходит для каникул с семейным проживанием во Франции.',
        ['Подтвердить площадку, группировку братьев, питание, скидки и отмену; исправленный год весенней программы получить у оператора.'],
        [src('Лето 2027',wander),src('Летние недели, цена и площадки',product),src('Другие каникулы / питание / опечатка года',holiday)],
        status='published_2026_27',priority=['both','general'],confirmed=['EN'])
    p=profiles[-1];p['language_evidence_role']='camp_life'
    rows=[day(s,e,'Летняя неделя · 09–16','€380/нед.; €360/нед. при двух и более неделях · итог подтвердить',p['place'],wander) for s,e in [('2027-07-05','2027-07-09'),('2027-07-12','2027-07-16'),('2027-07-19','2027-07-23'),('2027-07-26','2027-07-30'),('2027-08-23','2027-08-27')]]
    rows += [day(s,e,label,'€380/1 нед.; €720/2 нед. · дневное окно Пн–Пт',p['place'],holiday) for s,e,label in [('2026-10-19','2026-10-30','Осеннее окно · выбрать 1/2 недели'),('2027-02-08','2027-02-19','Зимнее окно · выбрать 1/2 недели')]]
    variants(p,rows)

    ih='https://ih.fl-france.com/anglais/day-camp/'
    add('ih-holiday','International House / France Langue · English Day Camps','Франция','FRA','Париж / Ницца / Биарриц',
        'general,languages','day','8–17: группы 8–10, 11–12, 13–14, 15–17',
        'Английский — язык занятий и приключенческих миссий; это языковой лагерь.',
        'Практика английского через культурные задания и командные проекты. Пн–Пт 08:30–16:30; стандарт и premium с online-подготовкой/сопровождением. Максимум группы 12 — заявление оператора.',
        'Общая осень 19–23.10.2026; зима/весна 2027 по городам ниже. Текущая страница под тарифами 2026/27 оставляет лето 29.06–24.07.2026; поисковый снимок показывал другие даты 2027. Лето 2027 до устранения расхождения не создаём в календаре.',
        price(2027,'Учебный год 2026/27: Париж/Ницца €340 стандарт или €430 premium за неделю; Биарриц €360/€450.',
              'Языковая дневная программа; premium добавляет online-занятия, их количество в блоках страницы расходится.',
              'Холодный обед с собой, дорога и жильё семьи. Premium — отдельный тариф, не обязательная доплата.'),
        'Только днём; три городские площадки, не пансион.',
        fit('candidate','Возраст 9–10 соответствует Explorers 8–10.'),fit('later','Минимум 8 лет; Оскару в 2027 будет 6–7.'),
        'Прозрачный по языку, возрасту и цене кандидат Матвею; даты одинаковой недели разных городов сохраняются раздельно.',
        ['Подтвердить конкретный адрес, доступные места, premium-пакет и отмену. Для Оскара нужен другой оператор.'],
        [src('Программы, календарь 2026/27 и тарифы',ih)],status='published_2026_27',priority=['general'],confirmed=['EN'])
    p=profiles[-1];rows=[]
    cities=[('paris','Париж',340,430,'2027-02-08','2027-02-12','2027-04-05','2027-04-09'),('nice','Ницца',340,430,'2027-02-22','2027-02-26','2027-04-19','2027-04-23'),('biarritz','Биарриц',360,450,'2027-02-15','2027-02-19','2027-04-12','2027-04-16')]
    for key,city,standard,premium,ws,we,ss,se in cities:
        fee=f'€{standard} стандарт / €{premium} premium за неделю · тариф 2026/27'
        for start,end,season,season_key in [('2026-10-19','2026-10-23','Осень','autumn'),(ws,we,'Зима','winter'),(ss,se,'Весна','spring')]:
            rows.append(day(start,end,city+' · '+season,fee,city,ih,variant_key=key+'-'+season_key))
    variants(p,rows,keyed=True)

    petits='https://lespetitsatomes.com/categorie-produit/stages-vacances-enfants-ados-maternelle/stages-robotique-programmation/'
    add('petits-atomes-tech','Les Petits Atomes · Robotique / Programmation','Франция','FRA','Франция · конкретный город и курс выбрать',
        'robotics,coding,science','day','Техника: вводная 7–9, продвинутая 10–14; возраст общих science-программ не переносится на robotics',
        'Английский/испанский именно технического преподавания не подтверждён. Французский сайт сам по себе не доказывает язык курса.',
        'Программирование, сенсоры и механика через Scratch, micro:bit, Arduino и разные LEGO/Makeblock-платформы. Комплект зависит от курса; конкретный проект и часы нужно выбрать.',
        'Страница рекламирует осенние каникулы 2026; точные даты выбранного технического курса и прайс 2027 не проверены.',
        price(None,'Публичный тариф конкретного robotics-курса в прочитанной категории не установлен.',
              'Состав выбранного курса и выдачу оборудования уточнить.',
              'Семейное жильё, питание, материалы и техника домой — подтвердить.'),
        'Дневные тематические занятия; пансион не подтверждён.',
        fit('conditional','После 10-летия другая техническая группа; EN-преподавание сначала подтвердить.'),
        fit('conditional','Технический минимум 7: только после 7-летия и подтверждения языка.'),
        'Содержательный технический кандидат Франции, пока с существенным языковым пробелом для этой семьи.',
        ['Уточнить EN/ES, город, возраст на первый день, количество технических часов и цену конкретного курса.'],
        [src('Технические возрастные группы и инструменты',petits),src('Сезонные science-программы','https://lespetitsatomes.com/accueil/')],priority=['technical'])

    wizard='https://www.americanvillage.fr/sejour/wizard-school'
    add('american-wizard','American Village · Wizard School La Rouatière','Франция','FRA','Souilhanels / Aude · рядом с Toulouse',
        'general,languages','boarding','8–12',
        'Английский в занятиях, дневных играх и вечерних мероприятиях; native / bilingual сотрудники.',
        'Тематическая школа волшебников, творчество и командные игры; 10 часов английского за шестидневный заезд. Это языковой тематический лагерь.',
        'Прочитанный заезд 05–10.07.2026 закрыт / complet. Новые даты 2027 не опубликованы в проверенной карточке.',
        price(2026,'Архив конкретного заезда: от €779/6 дней. Это нижняя цена по выбранному городу отправления, не предложение 2027.',
              'Полный пансион, занятия и основные активности; трансфер от Toulouse station в описанном пакете без доплаты, с бронированием.',
              'Insurance pack €60, дорога из Парижа/провинции, еда в дороге и личные расходы. Состав 2027 подтвердить.'),
        'Комнаты 2–3 человека; душ/санузел на этаже.',
        fit('candidate','Возраст 9–10 подходит; ждать нового заезда и подтверждения мест.'),fit('later','Минимум 8 лет, пока недоступен.'),
        'Кандидат на первый тематический английский пансион Матвея. Закрытый прошлый заезд не отображается как ближайшая доступная смена.',
        ['Получить даты, итоговый тариф, страховку и условия отмены 2027.'],
        [src('Конкретный заезд, цена, проживание и статус',wizard),src('Концепция Wizard School','https://www.americanvillage.fr/formules/wizard-school'),src('Центр La Rouatière','https://www.americanvillage.fr/centres/american-village/la-rouatiere')],
        priority=['general','boarding'],confirmed=['EN'])

    sis='https://www.sis.ac/school-life/summer-camps'
    add('sotogrande-camps','Sotogrande International School · Junior / Mega Camps','Испания','ESP','Sotogrande / Cádiz',
        'general,science,languages,sport','day,boarding','Mega 6–7 только днём; Junior 8–12 день/пансион; Masters 13–16; Nano 4–5 только днём',
        'Основной язык лагеря английский; часть сотрудников говорит по-испански. Язык выбранного STEAM-модуля подтвердить отдельно.',
        'Junior выбирает утренний спорт и один afternoon-track на двухнедельную сессию: STEAM, публичные выступления или другой курс. Заявлены 10 часов Junior-академики в неделю, а не 10 часов робототехники. Mega — общий тематический day camp.',
        'Заголовок 2026/2027, но основное тело: 28.06–08.08.2026. Junior 28.06–11.07, 12–25.07, 26.07–08.08; Mega недельный с 29.06. Будущие даты 2027 ещё не доказаны.',
        price(2026,'Junior/Masters 2 недели: €2 375 день / €3 445 пансион. Mega 1/2/3/4/5/6 недель: €495 / 900 / 1 275 / 1 600 / 1 875 / 2 100.',
              'Занятия, питание, активности и accident/liability insurance; пансион также жильё и прачечная. Стандартный трансфер Málaga/поезд в указанные часы 10–13 по условиям пакета.',
              'Health/travel insurance, pocket money; трансфер вне расписания €150 один / €300 туда-обратно. Swimming Nano/Mega €65/нед., public speaking €125/нед.; комбинации проверить.',
              'Refund policy выдаётся с offer letter; рекламная refund protection не означает безусловный возврат.'),
        'Junior и старшие — пансион; Mega только днём, Пн–Пт. Junior day в расписании 09–19; точные часы 2027 уточнить.',
        fit('candidate','Junior 8–12; выбрать STEAM и проверить его часы/содержание.'),fit('conditional','Mega 6–7 только day camp; Junior/пансион с 8, intensive STEAM младшим не подтверждён.'),
        'Один семейный кампус с разными форматами братьев; подходит для поездки с родителями после публикации нового сезона.',
        ['Запросить даты/цены 2027, English STEAM, инструменты, питание, письменную отмену и обязательные fee.'],
        [src('Dynamic Overview / Activities / Mega / Fees / Application · прочитаны в браузере',sis)],
        status='next_unannounced',priority=['both','general','technical'],confirmed=['EN'])
    profiles[-1]['language_evidence_role']='camp_life'

    kings='https://www.madrid-soto.kingscollegeschools.org/en/summer-camps'
    add('kings-soto-camps','King’s College Soto · STEAM & Multi-Sports','Испания','ESP','Soto de Viñuelas / Madrid',
        'general,science,languages,sport,robotics','day,boarding','Core / Core+ 6–15+, пансион с 8; Nano 4–5 днём; заголовок 3+ не доказывает допуск в STEAM',
        'Сотрудники EN/ES; академический выбор языков или STEAM. Английский технического преподавания и язык Robotics lab отдельно подтвердить.',
        'Core / Core+ сочетают академический трек и спорт. Robotics lab — отдельная опция два раза в неделю, не весь основной лагерь. Выбранный учебный план, проект и часы STEAM ещё уточнить.',
        'Основная страница с заголовком 2026/2027 публикует 28.06–25.07.2026: 28.06–11.07 и 12–25.07. Старый Academics URL содержит 2025; ни один из них не переносится на 2027.',
        price(2026,'Core STEAM 2 недели: €1 350 день / €2 150 пансион; Core+ STEAM €1 770 / €2 875. Другие спорт/языковые пакеты имеют другие тарифы.',
              'Занятия, спорт, snack/lunch и accident cover; пансион жильё с ванной, все meals и прачечная. Завтрак day camp не включён.',
              'Robotics €90/нед. (два занятия), bus €120/нед., airport €130 один / €215 возврат; swimming €60/нед., horse riding €115/нед. Health/travel insurance и семейное жильё отдельно.',
              'Аванс при acceptance, остаток ожидается за 6 недель. Размер аванса и refund policy — в offer letter, публично не подтверждены.'),
        'Tenbury House, двухместные ensuite-комнаты для пансиона; до 8 лет выбранный трек только днём.',
        fit('candidate','Возраст 9–10 позволяет Core STEAM day/boarding; новый сезон подтвердить.'),fit('conditional','После 6-летия Core day; пансион с 8. Доступ Robotics для младших подтвердить.'),
        'Испанский семейный кандидат с отдельными техническими опциями и прозрачным старым прайсом; международная среда не гарантирует инженерную глубину.',
        ['Получить тарифы/даты 2027, минимальный возраст Robotics, EN технического трека и точный offer с отменой.'],
        [src('Dynamic Fees / Activities / Application / FAQ · прочитаны в браузере',kings),src('Отдельная Academics-страница · содержит прошлый сезон','https://www.madrid-soto.kingscollegeschools.org/en/academics-multi-sports')],
        priority=['both','technical'])

    tecs='https://www.tecs.es/tecs/tecs-puerto-kids/'
    add('tecs-puerto-kids','TECS Puerto Kids','Испания','ESP','El Puerto de Santa María / Cádiz',
        'general,languages,sport','boarding','7–13 на текущей странице Puerto Kids; старые Go Camp/FAQ 6–9 не означают тот же допуск',
        'Full English Immersion Plus: английский в уроках и PBL, доля Total English увеличивается постепенно.',
        'Языковые занятия/PBL, командные игры, пляж, спорт и поездки. Общий английский пансион; технический intensive robotics не установлен.',
        'В меню 2027, а даты в теле без года: 28.06–11.07, 12–25.07, 26.07–08.08. До подтверждения года не создаём датированные события 2027.',
        price(None,'На текущей странице кнопка €1 730; точный сезон, длительность и полный invoice не установлены.',
              'Основные активности включены; Jerez airport / местная station заявлены без доплаты по условиям/подтверждению оператора.',
              'Перелёты, дополнительные трансферы Madrid/Sevilla/Bilbao по quorum, страхование и личные расходы — уточнить.'),
        'Школьный пансион El Centro Inglés: общие спальни до 14 детей, 24-часовое сопровождение.',
        fit('candidate','Возраст 9–10 в 7–13.'),fit('conditional','Только после 7-летия; до этого текущий минимум не выполнен.'),
        'Кандидат на английский пансион Испании; большие спальни и возраст младшего требуют отдельного решения.',
        ['Подтвердить год дат, €1 730 за какой пакет, точную группу Оскара, insurance и отмену.'],
        [src('Возраст, размещение, дата без года и advertised price',tecs),src('FAQ: прежние категории требуют сверки','https://www.tecs.es/tecs/preguntas-frecuentes-campamentos/')],
        priority=['general','boarding'],confirmed=['EN'])
    profiles[-1]['language_evidence_role']='camp_life'

    chamberi='https://campus-chamberi.rockbotic.com/dias-sin-cole'
    add('rockbotic-chamberi','Rockbotic Chamberí · Días sin cole','Испания','ESP','Madrid · Viriato 17',
        'robotics,coding,ai','day','6–12',
        'EN/ES именно обучения не подтверждены; испаноязычный сайт не заменяет доказательство языка преподавания.',
        'Тематические технические дни: робототехника, игры, 3D/VR и программирование; инструменты меняются по теме и возрасту. Есть LEGO, micro:bit, Scratch и другие платформы.',
        'Дни без школы; точные ближайшие даты 2026/27 в прочитанной странице не установлены.',
        price(None,'€50/день или €200/неделя; год тарифов не указан.',
              'Технические занятия; часы, питание и материалы домой подтвердить.',
              'Жильё семьи и дорога. Скидки братьям/своим ученикам указаны, их совместимость не доказана.'),
        'Дневной городской формат, без проживания.',
        fit('conditional','Возраст подходит; подтвердить язык и подходящий уровень.'),fit('conditional','С 6 лет по текущей странице; язык, группа и полнодневная готовность отдельно.'),
        'Локальный технический кандидат для семейной поездки в Мадрид; полноценный международный англоязычный пансион не подтверждён.',
        ['Получить даты, EN/ES teacher, часы, оборудование, еду и отмену.'],
        [src('Программа, возраст и тариф без года',chamberi)],priority=['technical'])

    arg='https://eventos.rockbotic.com/event/1821-actividades-de-verano-en-rockbotic-2026-lunes-a-viernes-de-9-00-a-14-00-horas-luna-tic-design-s-l-arganda-6-28005-madrid-2026-06-22-2026-09-04-1821/register'
    add('rockbotic-arganzuela','Rockbotic Arganzuela · Urban Tech Camp','Испания','ESP','Madrid · Arganda 6',
        'robotics,coding,ai','day','7–12',
        'Язык технического преподавания в проверенной карточке не установлен; EN не подтверждён.',
        'Тематические игровые/робототехнические проекты; Пн–Пт 09–14. Подбирается недельная программа, а не все технологии за каждый день.',
        'Исторический набор 2026: 22.06–31.07 и 31.08–04.09; регистрация закрыта. Даты 2027 не опубликованы.',
        price(2026,'Архив 2026: €175 первая неделя, €160 последующие; условия скидок отдельно.',
              'Дневная техническая программа; питание и выдачу комплекта уточнить.',
              'Жильё семьи, дорога, продлённый день и материалы домой — уточнить.'),
        'Городской дневной лагерь, без ночёвок.',
        fit('conditional','Возраст подходит; уровень/язык ещё подтвердить.'),fit('conditional','После 7-летия и подтверждения подходящего языка/группы.'),
        'Архивный технический кандидат Мадрида с чистой официальной event-карточкой; новая смена ещё не объявлена.',
        ['Блог содержит посторонние spam-ссылки: использовать проверенную event-карточку, перед заявкой подтвердить актуальный контакт и документы оператора. Уточнить новый набор, EN/ES и отмену.'],
        [src('Официальная event-карточка · набор 2026 закрыт',arg)],priority=['technical'])

    # Deepen existing operators without multiplying programme counts or fabricating dates.
    ilc=next(p for p in profiles if p['slug']=='ilc')
    ilc.update(age='FUN 6–9; Adrenaline 10–13; подростковую границу уточнить отдельно',
        programme='Языковые занятия (FUN: 15 ч/нед.), проекты, творчество, спорт и alpine adventures. Если Матвею исполнится 10 — Adrenaline вместо FUN; Оскар FUN. Это общий языковой лагерь.',
        accommodation='Дневной 09–18 либо полный пансион в Megève; размещение конкретного трека подтвердить.')
    ilc['timing']['label']='Главная страница предлагает summer 2027, но dates/prices содержат интервалы без года. Не выдаём их за подтверждённые смены 2027.'
    ilc['price']=price(None,'Текущий недатированный прайс: FUN CHF 2 915 день / 3 995 пансион за неделю; Adrenaline CHF 3 015 / 4 095. Регистрационный fee CHF 200 за пребывание отдельно.',
        'Пакет выбранного трека/формата; окончательный состав 2027 подтвердить.',
        'Прачечная CHF 70/нед. обязательность/длительность уточнить; Geneva transfer CHF 350/направление для 1–2 детей, UM +160, ночной +60. Другие размеры группы и опции имеют свои цены.',
        'Недатированные terms: при отмене удерживается фиксированный CHF 1 000, а также перечислены удержания 5% (>60 дней), 25% (60–30), 100% (<30). Их сочетание и условия 2027 подтвердить письменно; не считаем эту cancellation fee авансом и не суммируем автоматически.')
    for title,url in [('FUN / возраст / 15 часов','https://internationallanguagecamps.com/our-camps/summer-camp/megeve-france-en/fun'),('Adrenaline','https://internationallanguagecamps.com/our-camps/summer-camp/megeve-france-en/adrenaline'),('Недатированные цены / даты','https://internationallanguagecamps.com/prices'),('Условия оплаты / отмены без нового года','https://internationallanguagecamps.com/general-terms-and-conditions-of-sale')]:
        if not any(s['url']==url for s in ilc['sources']):ilc['sources'].append(dict(title=title,url=url,checked=checked))
    ilc['questions']=['Подтвердить год даты/тарифа, группу Матвея до/после 10-летия, полный пакет для двух братьев, обязательную прачечную и письменную отмену 2027.']
    av=next(p for p in profiles if p['slug']=='american-village')
    av['programme']+=' Возраст надо проверять на конкретном центре: Aurabelle 8–15, Wizard La Rouatière 8–12; Aurabelle summer Adventure Camp 11–15 пока Матвею не подходит.'
    av['questions']=['Выбрать конкретный центр/формулу, не переносить общий минимум 8 на все Adventure-треки; получить новый календарь и итоговый прайс.']
    for title,url in [('Матрица центров и возраста','https://www.americanvillage.fr/centres'),('Aurabelle / размещение','https://www.americanvillage.fr/centres/american-village-aurabelle'),('Aurabelle / возраст конкретного Adventure-трека','https://www.americanvillage.fr/sejours/centre-greoux-les-bains'),('FAQ / английская жизнь лагеря','https://www.americanvillage.fr/informations-pratiques/foire-aux-questions')]:
        if not any(s['url']==url for s in av['sources']):av['sources'].append(dict(title=title,url=url,checked=checked))
    ct=next(p for p in profiles if p['slug']=='camp-tecnologico')
    ct['age']='По выбранному курсу: holiday camps обычно 6+/7+; общие workshop Kids & Tech 4–6 не доказывают допуск в конкретный лагерь'
    ct['timing']['label']+=' Christmas-страница сейчас озаглавлена 2024–25, не новый календарь 2026/27.'
    ct['questions']=['Подтвердить конкретный holiday-курс/площадку, минимальный возраст, ES/EN, новые даты и тариф; старое Christmas-окно не переносить на 2026/27.']
    ct['sources'].append(dict(title='Christmas: опубликован старый сезон 2024–25',url='https://camptecnologico.com/campamentos-navidad/',checked=checked))
