'Priority Latin American camps; distinguish real 2027 offers from archives.'


def add_latam(add, src, fit, profiles):
    def put(*a, **kw):
        add(*a, **kw)
        p = profiles[-1]
        p['checked'] = '2026-10-05'
        for s in p['sources']:
            s['checked'] = p['checked']
        return p

    def fee(year, label, included, extras, deposit):
        return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)

    def dated(p, days, label, price, url, scope='camp_session'):
        p['timing']['sessions'] = days
        p['timing']['session_details'] = [dict(start=a, end=b, label=label, price=price,
            source=url, place=p['place'], formats=p['formats'], date_scope=scope) for a,b in days]

    unknown = 'Язык преподавания прямо не установлен; испанский сайт не доказывает ES-группу, английская форма не доказывает EN.'
    day = 'Дневная программа; жильё семьи, дорога и время вне занятий отдельно.'
    sea = 'https://www.sailingclubpanama.com/campamentos-verano-panama/'
    seaform = 'https://forms.gle/qHJMvZZzjpid4Ns6A'
    p = put('seacamp-panama','Sailing Club Panamá · Sea Camp 2027','Панама','PAN',
        'Playa del Pueblo, Isla Saboga · Islas Perlas; Marina Flamenco — отправление ferry',
        'general,sport,science','boarding','7–16',unknown,
        'Парусный спорт, windsurf, SUP, snorkel и прогулки. Все уровни парусного опыта; робототехника не заявлена.',
        '7–10 января и 25–28 марта 2027. Февраль: основной список 19–22, ссылка и сама форма 11–14; из календаря исключён.',
        fee(2027,'USD 650 за 4 дня / 3 ночи.',
            'Ferry туда-обратно с сопровождающими, палатка с матрасом, питание/перекусы, водные и наземные занятия.',
            'USD 50 sibling либо return/multiweek, не суммируются; индивидуальный счёт и страховку уточнить. Дорога до Panamá отдельно.',
            'USD 200 аванс в счёт 650, не доплата; возможна рассрочка ACH. Отмена не раскрыта.'),
        'Палатки; заявлены 24 ч надзор и спасательные жилеты. Это не школьный пансион.',
        fit('candidate','9–10 подходит; язык, плавание, страховку и иностранный допуск согласовать.'),
        fit('conditional','Только после 7-летия к началу заезда; пока 6 минимальный возраст не достигнут.'),
        'Короткий общий пансион рядом с семейной базой; техническую подготовку организовать отдельно.',
        ['Февральское расхождение, язык инструктора, плавание, отмена, медицинская помощь и дата рождения.'],
        [src('Программа, возраст и полная базовая цена',sea),src('Февральская форма 11–14/2027, прочитана без отправки',seaform)],
        status='published_2027',priority=['general','boarding'])
    dated(p,[['2027-01-07','2027-01-10'],['2027-03-25','2027-03-28']],
        'Sea Camp · 4 дня / 3 ночи','USD 650; аванс 200 в счёт цены',sea)
    p['timing']['unresolved_sessions']=[dict(reason='19–22 February on main calendar contradicts 11–14 in form; neither interval imported.',source=sea)]

    base = 'https://pty.lallanada.com/campamento-de-verano/'
    home = 'https://pty.lallanada.com/'
    boardpdf = 'https://pty.lallanada.com/wp-content/uploads/2026/08/%F0%9F%92%9ABrochure-Sleepaway-Enero-2027-WEB.pdf'
    vallepdf = 'https://pty.lallanada.com/wp-content/uploads/2026/09/%F0%9F%92%9ABrochure-Day-Camp-El-Valle-Enero-2027.pdf'
    es = 'Основная программа 100% на испанском; EN у вожатых — помощь, не английская смена.'
    for slug,name,tail,age,housing,mat,osc in [
        ('llanada-panama-board','Sleepaway · El Valle','sleepaway-valle-de-anton/','7–16',
         'Пансион: домики 8–10 детей и 1–2 вожатых, кондиционер/санузел — по брошюре.',
         fit('candidate','Возраст 9–10 подходит; семь ночей и связь обсудить.'),
         fit('conditional','Только после 7-летия к 24 января 2027; точный день рождения неизвестен.')),
        ('llanada-panama-valle','Day Camp · El Valle','daycamp-valle-de-anton/','6–10 в PDF 2027; сайт 6–12 — расхождение',
         day,fit('candidate','9–10 подходит обеим опубликованным границам.'),
         fit('candidate','6–7 подходит; ночёвок нет.')),
        ('llanada-panama-city','Day Camp · Ciudad','daycamp-ciudad/','4–12',day,
         fit('candidate','9–10 подходит; новый городской календарь ещё нужен.'),
         fit('candidate','6–7 подходит; новый городской календарь ещё нужен.'))]:
        boarding = slug.endswith('board'); valle = slug.endswith('valle'); url=base+tail
        if boarding:
            cost=fee(2027,'USD 1 290 Early Bird до 23.10.2026 /1 352 с 24.10 за 7 ночей; 6×215 либо 4×338.',
                'Пансион, активности; дневной распорядок включает питание. PDF перечисляет shirt, фото app и транспорт туда-обратно.',
                'Скидка sibling/excamper 60 USD с ограничениями тарифа. Перелёт отдельно; страхование и итоговый договор уточнить.',
                'Все платежи до старта. Ссылка отмены озаглавлена 2026; условия 2027 не считаем подтверждёнными.')
            timing='24–31 января 2027 из новой брошюры; лето Jul–Aug на homepage только без конкретных смен.'
        elif valle:
            cost=fee(2027,'USD 400 за 25–29 января 2027,09:00–18:00.',
                'Обед, дневной перекус, shirt и фото app.',
                'Завтрак дома; родители привозят/забирают на площадке. City-bus из общего footer не переносим в El Valle. Sibling/excamper 20 USD уточнить.',
                'Заявлена рассрочка картой; применимый договор 2027 и отмену получить отдельно.')
            timing='25–29 января 2027, пн–пт 09:00–18:00; июль/август без точных смен.'
        else:
            cost=fee(None,'Прайс 2027 города не установлен; тариф El Valle 400 USD к городу не относится.',
                'Обед/дневной перекус; shirt, фото app, автобус Costa del Este/San Francisco по городским условиям.',
                'Утренний перекус свой, завтрак дома. Sibling/excamper 20 USD/нед. — условие, не подтверждённая конечная цена.',
                'Городскую отмену/прайс 2027 уточнить; доступный brochureJul–Aug 2026 не обновляет сезон.')
            timing='На homepage сезоны Jan–Feb и Jul–Aug 2027, но городской brochure и подробные даты ещё 2026.'
        p=put(slug,'La Llanada Panamá · '+name,'Панама','PAN',
            'El Valle de Antón · площадка Sleepaway' if boarding or valle else 'Club Ecuestre Castilla del Oro · дневной городской лагерь',
            'general,sport,art,science','boarding' if boarding else 'day',age,es,
            'Спорт, плавание, походы, творчество, кухня и опыты; общий отдых, инженерный курс не заявлен.'+
            (' Город:08:30–16:30, автобусные точки Costa del Este/San Francisco.' if not boarding and not valle else ''),
            timing,cost,housing,mat,osc,'Испанский прямо подтверждён; младшим доступен день, ночёвки только 7+.',
            ['Точный адрес, новые документы 2027, свободное место, иностранный допуск, связь/страхование и полный счёт.'],
            [src('Конкретный формат и язык',url),src('2027 сезоны всех форматов',home)]+
            ([src('Новая брошюра 2027: даты, возраст и прайс',boardpdf if boarding else vallepdf)] if boarding or valle else []),
            status='published_2027' if boarding or valle else 'partial_2027',confirmed=['ES'],priority=['general'])
        p['language_evidence_role']='camp_life'
        if boarding: dated(p,[['2027-01-24','2027-01-31']],'Sleepaway ·7 ночей','USD 1290/1352 по дате тарифа',boardpdf)
        elif valle: dated(p,[['2027-01-25','2027-01-29']],'Day Camp ·09:00–18:00','USD 400/неделя',vallepdf,'day_camp_window')

    sek='https://sekcostarica.com/vacaciones-activas/'
    put('sek-cr-space','SEK Costa Rica · Space Academy / Vacaciones Activas','Коста-Рика','CRI',
        'Colegio Internacional SEK Costa Rica · школьная площадка; точный сбор согласовать',
        'general,science,robotics,art,sport','day','«Все возраста», числовой допуск лагеря не опубликован',unknown,
        'Общий космический лагерь с RoboLab STEAM, опытами, спортом, творчеством и кухней; не отдельный робототехнический интенсив.',
        'Архив 29.06–10.07.2026,08:00–13:00; новый сезон 2027 не опубликован.',
        fee(2026,'CRC 142 800/2 недели либо 86 700/неделя, IVA включён; архив 2026.',
            'Занятия, обед и перекус; открыт внешним детям.',
            'Транспорт 51 980 CRC с IVA, период тарифа уточнить; периферический маршрут зависит от спроса.',
            'Архивная скидка 25% до 19 июня только на 2 недели; штраф 30% за неучастие. Новый договор отдельно.'),
        day,fit('unknown','Нужна конкретная группа 9–10, язык и программа 2027.'),
        fit('unknown','Фраза «все возраста» не подтверждает группу 6–7.'),
        'Близкий вариант общего отдыха с техническими опциями; будущий сезон и возраст ещё неизвестны.',
        ['Возрастные группы, язык RoboLab, часы робототехники, прайс/транспорт 2027.'],[src('Программа, внешние дети и архивный прайс',sek)])

    tx='https://tecnobotrix.com.mx/vj/'
    put('tecnobotrix-summer','Tecnobotrix · Robótica, IA y Videojuegos','Мексика','MEX',
        'Plaza Texcoco, Av.Fray Pedro de Gante 410, Local 14-C; San Bernardino — отдельная площадка',
        'robotics,ai,games,coding','day','С 7 лет',unknown,
        'Пять недель 2026: игры 2 D/3 D, line-following/OLED robots, электроника и промпты IA. Шесть детей в группе; проекты домой по заявлению школы.',
        'Архив 20.07–21.08.2026,10:00–13:00;2027 не опубликован.',
        fee(2026,'Тариф не раскрыт на странице; стоимость 2027 неизвестна.',
            'Предоставляются оборудование, материалы и инструменты.',
            'Жильё/дорога, питание и возможный kitfee уточнить.',
            'Зачисление только после подтверждения школы; условия оплаты не раскрыты.'),day,
        fit('candidate','Возраст подходит; для опыта 3 лет согласовать сложность вместо начального повторения.'),
        fit('conditional','После 7-летия; пока 6 этот технический трек недоступен.'),
        'Практические проекты; собственные заявления о чемпионстве не считаем независимым рейтингом.',
        ['Группа 7+, язык, учебный план/тариф 2027, площадка и реальное участие в соревнованиях.'],
        [src('Конкретная каникулярная программа',tx),src('Школа и инструменты','https://www.tecnobotrix.com.mx/')])
    punk='https://www.robotpunk.mx/cursos-de-verano/'
    put('robotpunk-summer','RobotPunk · Summer Camp','Мексика','MEX',
        'Av.Ocampo 1829 Ote., Col.Centro, Torreón, Coahuila',
        'robotics,coding,games,electronics','day','Возраст конкретного лагеря не опубликован',unknown,
        'LEGO/VEX, игры и приложения, Arduino/Raspberry,3 D печать; набор инструментов зависит от уровня. Домой заявлены 3 D модели, не все роботокомплекты.',
        'Архив 29.06–07.08.2026,10:00–14:00; новая смена 2027 не установлена.',
        fee(2026,'Тариф не опубликован; NASA-партнёрство — заявление оператора, не подтверждение качества или диплома NASA.',
            'Программные занятия; состав оборудования и стоимость материалов уточнить.',
            'Жильё/дорога/питание и kitfee неизвестны.',
            'Аванс/отмена не раскрыты.'),day,
        fit('unknown','Возраст и группа по трёхлетнему опыту нуждаются в подтверждении.'),
        fit('unknown','Минимальный возраст SummerCamp не установлен.'),
        'Техническая программа для семейной базы в Мексике; пока архивный кандидат, не бронь 2027.',
        ['Возраст, план/язык/прайс 2027, какие комплекты предоставляют и что остаётся ребёнку.'],
        [src('Летний план',punk),src('Реальный адрес','https://www.robotpunk.mx/contacto/')])

    tro='https://troonic.com/troonic-camp-2027/'
    p=put('troonic-robotics-camp','Troonic Camp 2027 · Robótica 6–11','Перу','PER',
        'Lima: Miraflores, CalleAlfonsoUgarte 309; naturetripCPRCardal,Pachacamac. Club-сайты только членам',
        'robotics,science,general','day','Camp 4–15; конкретная Robótica 6–11, LEGO 4–5, Arduino/3 D 12–15',unknown,
        'Робототехника в Lima плюс природа/гостевые лекции Pachacamac. Обещание комплект домой в общих FAQ требует подтверждения именно camp-пакета.',
        '2027: заголовки 04–07 января/01–04 февраля, но описание«04 дня пн–чт(revisar)» и пятничный bus/лекции. Полная длительность не установлена, ICS не создаём.',
        fee(2027,'USD 700 на странице, объём пакета/число недель не установлены.',
            'Заявлены занятия robotics и naturecamp; полный состав bus/food/kit нужно подтвердить.',
            'Транспорт Friday 08:30–16:00 против agenda возврата 14:30; не считаем ежедневным включённым автобусом.',
            'Аванс/отмена не раскрыты; надпись Camp не доказывает ночёвки.'),day,
        fit('candidate','9–10 подходит Robótica 6–11; новый уровень по опыту согласовать.'),
        fit('candidate','6–7 подходит Robótica 6–11; preschoolLEGO 4–5 уже не его группа.'),
        'Общий плюс технический план обоим; расписание/цена недостаточно согласованы для поездки.',
        ['Дни и полный объём 700 USD, язык, реальные Friday трансферы, комплект и открытая площадка без членства.'],
        [src('2027 страница с противоречиями',tro)],status='partial_2027')
    p['timing']['precision']='season_window'
    p['related_event_ids']=['L149','L150']

    we='https://www.wecode.edu.uy/'
    for slug,tail,name,age,cost,content,kit in [
        ('wecode-pocitos-lab','lab-pocitos','Laboratorio','Grade 2–3',5200,
         'Роботы, алгоритмы, программируемые рисунки, электричество и опыты. Четыре встречи по 2 ч, но текст предлагает дважды в неделю — полный объём уточнить.',
         'Материалы/компьютер не нужны; вариант 1 раз/неделю 2800 UYU.'),
        ('wecode-pocitos-ia','ia-pocitos','Inteligencia Artificial','Grade 4–6',2800,
         'Модели распознаваниярисунков/голоса/движения, Pictionary/BopIt;4 встречи по 2 ч. Это обучение собственных моделей, не просто пользованиечатботом.',
         'Своя laptop; онлайнплатформы. Скидка 500 UYU за комбинациюкурсов относитсяк 2026.'),
        ('wecode-pocitos-minecraft','minecraft 1-pocitos','Minecraft Coding 1','Grade 4–6',2800,
         'Координаты 3 D, переменные, loops и conditions для построек Minecraft;2 ч 1 раз/неделю.',
         'Своя laptopWindows 8+/macOS 10.15+; общая FAQ«любая laptop/online» расходитсяс конкретным требованием.')]:
        url=we+'cursos/'+tail
        p=put(slug,'WeCode Pocitos · '+name,'Уругвай','URY','JoséMartí3094, Pocitos, Montevideo',
            'robotics,coding,science' if slug.endswith('lab') else 'ai,coding' if slug.endswith('ia') else 'games,coding',
            'day',age+' по классу, который ребёнок будет проходить в 2026',unknown,content,
            'Архив Feb 2026, без конкретных новых дат 2027; homepage 3 встречи/нед. расходитсяс выбранной карточкой.',
            fee(2026,'Архив: $'+str(cost)+' за выбранный курс; ISO валюты на карточке нет, вероятно UYU — уточнить. Цена 2027 неизвестна.',
                'По карточке нет matrícula/других сборов. '+kit,
                'Питание/жильё семьи отдельно;10% annual/15% sibling из общей FAQ не гарантированы короткому summercourse.',
                'FAQ годового договора не заменяет правила короткого курса/отмену 2027.'),day,
            fit('conditional','Нужен школьный класс '+age+' и соответствие уровня; дата рождения это не доказывает.'),
            fit('conditional' if slug.endswith('lab') else 'later',
                'Нужен Grade 2–3; возраст 6–7 сам по себе недостаточен.' if slug.endswith('lab') else 'Требуется Grade 4–6, для Оскара будущая ступень.'),
            'Короткие содержательные курсы с малой группой, но 2026 архив не основание брони Feb 2027.',
            ['Класс, ES/EN, новое расписание 2027, длительность и kit/отмена; STEM.org — заявление оператора, не медаль.'],
            [src('Конкретный курс, цена и оборудование',url),src('Каникулярный сезон','https://www.wecode.edu.uy/verano')])

    bc='https://www.britishcouncil.cl/ingles/cursos-de-verano-ninos'
    for slug,name,age,mat,osc in [
        ('british-chile-young-a','Young Innovators A','6–8',fit('not_eligible','Матвей старше 8; YoungInnovatorsB.'),fit('candidate','6–7 подходит возрасту A; уровень английского отдельно.')),
        ('british-chile-young-b','Young Innovators B','9–11',fit('candidate','9–10 подходит B; английский уже известен, пользу содержания оценить.'),fit('later','Минимум 9; сейчас младшая A.'))]:
        p=put(slug,'British Council Chile · '+name,'Чили','CHL','Santiago · точный учебный кампус подтвердить',
            'languages,general','day',age,'Уроки английского с проектами; язык робототехники не применим.',
            'Английский через игры, проекты и LearningHub; robotics/engineering интенсив не заявлен.',
            'Архив 05–30 января 2026,пн–пт 09:00–13:00,20 ч/нед.;2027 не объявлен.',
            fee(2026,'CLP 259000/нед.;481740/2,660450/3,826800/4 нед., архив 2026.',
                'Английские занятия и LearningHub.',
                'Питание/материалы, жильё идорога уточнить; convenios скидки не для всех семей.',
                'Договор/отмена 2027 неизвестны.'),day,mat,osc,
            'Языковое дополнение; для ужеанглоязычных детей не первый выбор инженерной подготовки.',
            ['Новый сезон/кампус 2027, уровень английского, проекты, прайс и полный договор.'],
            [src('Возраст, уроки иархив 2026',bc)],confirmed=['EN'])
        p['language_evidence_role']='language_lessons'

    norte='https://www.chilenonorteamericano.cl/producto/curso-ingles-ninos-summer-school-2-niveles/'
    p=put('norte-chile-summer','Instituto Chileno Norteamericano · Summer School · 2 niveles','Чили','CHL',
        'Valparaíso / Viña del Mar / Quilpué — точная выбранная sede не установлена',
        'languages,general','day','7–10','Начальные уроки английского, не техническое преподавание.',
        'Два уровня по 36 clockhours, по 1 месяцу каждый; игры/проекты начального EN. Детям, уже учащимся на EN, может быть слишком просто.',
        'Начало Jan 2027; пн–чт 10:00–12:45, точный день старта/окончание не опубликованы. Прикреплённый PDF назван 2024.',
        fee(2027,'CLP 349900 на карточке 72 ч; рассрочка противоречит сама себе:12×23850 против 12×29158.',
            'Два языковых уровня; питание/материалы не уточнены.',
            'Проценты, доступ к карточной рассрочке, matrícula, жильё и дорогу согласовать.',
            'Обещание «без процентов» расходится с примечанием об interest; окончательный счёт и отмена неизвестны.'),day,
        fit('candidate','9–10 подходит; начальный EN может не приносить пользы по уровню.'),
        fit('conditional','Только после 7-летия; точную дату начала Jan 2027 ещё нужно установить.'),
        'Официальный 2027 языковой вариант; не ставим выше инженерных лагерей.',
        ['Кампус, точные даты обоих уровней, уровень, окончательная цена/рассрочка и новый PDF 2027.'],
        [src('Конкретные 72 ч, возраст и 2027 прайс',norte)],status='partial_2027',confirmed=['EN'])
    p['language_evidence_role']='language_lessons'
    p['timing']['precision']='season_window'
