"""Read programme-specific 2027 documents; keep unresolved ages and years explicit."""

CHECKED = '2026-10-05'
AIGLON = 'https://www.aiglon.ch/2027-summer-camp'
BROCHURE = 'https://online.fliphtml5.com/meksu/fdzd/'
HEL = 'https://www.helveticinstitute.ch/robotics-ai-and-coding/'
ZUG = 'https://www.helveticinstitute.ch/summer-robotics-camp-zug/'
BABEL = 'https://www.babelschool.fr/stages-vacances-anglais/'
LB = 'https://littlebritishschools.com/stages-de-vacances/summer/'
NAV = 'https://respiraocio.com/campamentos-de-verano/campamentos-de-verano-ingles-gredos/'
NAVPDF = 'https://respiraocio.com/wp-content/uploads/2024/05/NAVATORMES-RESPIRA-HOJA-INFORMATIVA.pdf'


def add_europe(add, src, fit, profiles):
    def put(*args, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1]
        p['checked'] = CHECKED
        for s in p['sources']: s['checked'] = CHECKED
        return p

    def fee(year, label, included, extras, deposit):
        return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)

    def dates(p, rows, source, formats, scope='camp_session'):
        p['timing']['sessions'] = [[a,b] for a,b,label,price in rows]
        p['timing']['session_details'] = [dict(start=a,end=b,label=label,price=price,
            place=p['place'],source=source,formats=formats,date_scope=scope)
            for a,b,label,price in rows]

    no_en = 'Язык VEX-преподавания не подтверждён; английская брошюра и отдельный урок English не доказывают английскую робототехнику.'
    programme = ('Classic: утренний VEX Robotics, сборка, программирование и задачи; затем общие альпийские активности. '
        'Каждая программа длится одну неделю; в двух- и трёхнедельных пакетах выбирают несколько программ. '
        'Не обещаем робототехнику на протяжении всего многонедельного проживания или подготовку к официальному турниру.')
    place = 'Avenue Centrale 61, Chesières / Villars-sur-Ollon'
    q = ['Подтвердить язык инструктора, платформу VEX, часы/сложность после трёх лет соревнований, выбор недель и полный расчёт с трансфером/страховкой.']
    p = put('aiglon-classic-board','Aiglon · Classic VEX / пансион','Швейцария','CHE',place,
        'robotics,general,sport','boarding','Пансион и Robotics: 8–16',no_en,programme,
        'Шесть опубликованных пакетов A–F в брошюре 2027; даты и цены привязаны к каждому пакету.',
        fee(2027,'CHF 4 600 / 1 неделя; 8 200 / 2 недели; 12 000 / 3 недели.',
            'Пакет школьного пансиона и выбранных программ; окончательный состав питания/материалов/страховки сверить по договору.',
            'Трансфер, личные расходы, комплект домой и возможные дополнительные услуги не установлены.',
            'Аванс и отмена пока не проверены; опубликованный тариф не равен итоговому счёту.'),
        'Школьный пансион; возрастной минимум 8.',fit('candidate','Возраст Robotics подходит; язык и недельный выбор ещё согласовать.'),
        fit('later','В 2027 будет 6–7, пансион и Robotics в boarding-таблице с 8.'),
        'Предметный вариант VEX для Матвея с опубликованными пакетами; технический объём ограничен утренним недельным курсом.',
        q,[src('Программа 2027',AIGLON),src('Брошюра: VEX стр.4 / пансион стр.7',BROCHURE)],status='published_2027',priority=['technical','boarding'])
    dates(p,[('2027-06-27','2027-07-03','A · 1 неделя','CHF 4 600'),
        ('2027-06-27','2027-07-10','B · 2 недели / несколько программ','CHF 8 200'),
        ('2027-06-27','2027-07-17','C · 3 недели / несколько программ','CHF 12 000'),
        ('2027-07-04','2027-07-17','D · 2 недели / несколько программ','CHF 8 200'),
        ('2027-07-18','2027-07-31','E · 2 недели / несколько программ','CHF 8 200'),
        ('2027-07-25','2027-07-31','F · 1 неделя','CHF 4 600')],BROCHURE,['boarding'])

    p = put('aiglon-classic-day','Aiglon · Classic VEX / дневные недели','Швейцария','CHE',place,
        'robotics,general,sport','day','Дневная таблица: Robotics 7–16; описание Classic / главная страница: 8–16 — конфликт младшего допуска.',
        no_en,programme+' Дневной режим пн–пт 08:00–17:00; отдельные вечера можно остаться дольше.',
        'Пять дневных недель 28.06–30.07.2027; каждая пн–пт, без автоматических ночёвок.',
        fee(2027,'CHF 2 500 за каждую дневную неделю.',
            'Дневная программа; полный состав питания и материалов подтвердить.',
            'Субботняя экскурсия CHF 500; жильё семьи, дорога/трансфер и личные расходы отдельно.',
            'Аванс/отмена неизвестны; никакая заявка или age verification не отправлена.'),
        'Дневное посещение; семья организует собственное жильё. Ночёвки в экспедициях описаны для Adventure / Ride / Survival, не переносим на Classic VEX.',
        fit('candidate','Подходит обеим возрастным версиям; выбрать техническую неделю и язык.'),
        fit('conditional','Только после 7-летия и прямого разрешения на Robotics: day-таблица 7+, основное описание 8+.'),
        'Позволяет семейную поездку без пансиона; возраст Оскара требует разрешения именно на Robotics.',q+[ 'Разрешить расхождение Robotics 7–16 в day-таблице и 8–16 в описании.' ],
        [src('Основной возраст 8–16',AIGLON),src('Дневные недели / 7–16 / тариф, стр.8',BROCHURE)],status='published_2027',priority=['technical'])
    dates(p,[(a,b,'Дневная неделя '+str(i),'CHF 2 500') for i,(a,b) in enumerate([
        ('2027-06-28','2027-07-02'),('2027-07-05','2027-07-09'),('2027-07-12','2027-07-16'),
        ('2027-07-19','2027-07-23'),('2027-07-26','2027-07-30')],1)],BROCHURE,['day'],'day_camp_window')

    p = put('helvetic-zug-summer','Helvetic · Robotics, AI & Coding / Zug','Швейцария','CHE','Zug; точную площадку летней смены подтвердить',
        'robotics,coding,ai,general','day','Обзорная summer-таблица 4–12; подробный курс рассчитан на 6–11; общее вступление 7+.',
        'Английский/немецкий/билингвальный общий лагерь не доказывает язык именно технического курса; EN Robotics ещё уточнить.',
        'Утром: сборка роботов, block coding / Scratch, AI digital modelling рисунка в 3D. После обеда экскурсии/активности. Не весь день робототехника.',
        '2027: 05–09.07, 12–16.07, 09–13.08; пакет первых двух недель 05–16.07. Подробная карточка прямо указывает 12–16, обзорная таблица ошибочно 13–16.',
        fee(2027,'CHF 730 / неделя, CHF 1 460 / две недели.',
            'Технические занятия, экскурсии и общие активности по карточке.',
            'Обед и воду принести с собой; жильё семьи и транспорт отдельно. Обязательный materials fee именно summer не установлен, школьный term fee не переносим.',
            'Порядок оплаты, отмена и extended care требуют отдельного расчёта.'),
        'Дневной 09:00–16:00 пн–пт, без пансиона.',fit('candidate','9–10 входит в подробное описание 6–11; нужна сложность для опытного участника.'),
        fit('conditional','Подробный курс доступен шестилетним, но вступление 7+: подтвердить конкретную группу и дату рождения.'),
        'Полезный технический кандидат для семейной поездки: содержание и исправленная вторая неделя подтверждены отдельной карточкой.',
        ['Подтвердить EN, возрастную группу, точный адрес, оборудование и проект домой; подробная карточка разрешает дату 12–16 июля, не предполагаем её из календаря.'],
        [src('Конкретный Summer Camp Zug',ZUG),src('Обзорная таблица с расхождениями',HEL)],status='published_2027',priority=['technical'])
    dates(p,[('2027-07-05','2027-07-09','Неделя 1','CHF 730'),('2027-07-12','2027-07-16','Неделя 2 · подробная карточка','CHF 730'),
        ('2027-08-09','2027-08-13','Неделя 3','CHF 730'),('2027-07-05','2027-07-16','Двухнедельный пакет','CHF 1 460')],ZUG,['day'],'day_camp_window')

    p = put('helvetic-zurich-summer','Helvetic · Robotics / Zürich Römerhof','Швейцария','CHE','Zürich · Römerhof; адрес и возрастной технический поток подтвердить',
        'robotics,coding,ai','day','Summer-таблица 4–12; вступление технического курса 7+. Группа и возраст Zug не автоматически действуют в Zürich.',
        'Язык технической группы не установлен; английский сайт не является доказательством EN.',
        'Robotics, AI & Coding по обзорной таблице. Подробный учебный план/AI-модуль Цуга не автоматически обещается другой площадке.',
        '2027: 19–23.07, 26–30.07, 16–20.08; опубликован двухнедельный пакет 19–30.07.',
        fee(2027,'CHF 730 / неделя, CHF 1 460 / две недели.',
            'Опубликованный пакет курса; питание, материалы и экскурсии для Zürich подтвердить.',
            'Семейное жильё/дорога и возможные материалы отдельно.', 'Отмена, аванс и фактическое наличие мест неизвестны.'),
        'Дневной 09:00–16:00 пн–пт; пансион не описан.',fit('candidate','Возраст 9–10 соответствует таблице; уровень и группа неизвестны.'),
        fit('conditional','4–12 в таблице против общего 7+; до подтверждения не обещаем Robotics в 6 лет.'),
        'Дополнительная швейцарская площадка с реальными датами; учебные условия и язык ещё требуют уточнения.',
        ['Получить точный адрес, возраст технического потока, EN, питание/материалы и curriculum Zürich.'],[src('Summer 2027 · Zürich',HEL)],status='published_2027',priority=['technical'])
    dates(p,[('2027-07-19','2027-07-23','Неделя 1','CHF 730'),('2027-07-26','2027-07-30','Неделя 2','CHF 730'),
        ('2027-08-16','2027-08-20','Неделя 3','CHF 730'),('2027-07-19','2027-07-30','Двухнедельный пакет','CHF 1 460')],HEL,['day'],'day_camp_window')

    p = put('babel-holiday-english','Babel School · English holiday camps','Франция','FRA','Toulouse · Tournefeuille; точный адрес подтвердить',
        'languages,general,science,art','day','PS–CM2, группы 3–8 детей по уровню; школьный класс уточнить, числовой возраст не опубликован.',
        'Все занятия 100% на английском, преподаватели англоязычные; прямо заявлено для этих holiday stages.',
        'Культурные темы, песни/игры, творчество, готовка, сад; зимой pancake workshop и science experiments. Общие английские каникулы, не инженерный интенсив.',
        '19–23.10.2026, 08–12.02.2027, 05–09.04.2027. Летний заголовок 05–09.07.2027 против текста 2026: лето исключено из точного календаря.',
        fee(None,'2026/27: EUR 350 / неделя 09:00–17:00 или EUR 160 / неделя 10:00–12:00.',
            'Занятия выбранного полного или утреннего пакета.',
            'Жильё, транспорт и питание уточнить: «еда на месте» не подтверждает её включение.',
            'Во spring-блоке 10% второму ребёнку; распространение на другие сезоны и суммирование с CE Air France не предполагаем. Отмена не проверена.'),
        'Дневной/утренний формат; без пансиона.',fit('conditional','Предварительно начальная школа, но требуется текущий класс PS–CM2.'),
        fit('conditional','Есть младшие школьные группы; точный класс и уровень подтвердить.'),
        'Понятная английская программа зимой и весной для семейной поездки; детям с хорошим EN оценить пользу языкового содержания.',
        ['Подтвердить класс/уровень, питание, адрес, условия отмены и исправленный год summer.'],[src('Даты, уровни, 100% English и тарифы',BABEL)],
        status='published_2026_27',priority=['both','general'],confirmed=['EN'])
    p['language_evidence_role']='camp_life'
    p['price']['season']='2026/27'
    variants=[]
    for a,b in [('2026-10-19','2026-10-23'),('2027-02-08','2027-02-12'),('2027-04-05','2027-04-09')]:
        for key,hours,price in [('full','09:00–17:00','EUR 350'),('morning','10:00–12:00','EUR 160')]:
            variants.append(dict(start=a,end=b,label=hours,variant_key=key+'-'+a.replace('-',''),price=price,
                place=p['place'],source=BABEL,formats=['day'],date_scope='day_camp_window',accommodation='Дневной '+hours+'; без ночёвок.'))
    p['timing'].update(variant_keyed=True,sessions=[[v['start'],v['end']] for v in variants],session_details=variants)

    campuses=[('paris6','Paris 6 · 59 rue Notre-Dame des Champs'),('paris7','Paris 7 · 115 rue Saint-Dominique'),
        ('paris16','Paris 16 · 72 bis rue de la Tour'),('paris17','Paris 17 · 70 rue de Lévis'),('meudon','Meudon · 3 rue du Ponceau')]
    for slug,name,course,age,content,start,end,mat,osc,hours in [
        ('littlebritish-boost','Little British · English Boost / Primaire','english-boost-camp-summer-2027/',
         'Primaire (начальная школа); точный числовой возраст не указан.',
         'Устная речь, слушание, чтение/письмо, грамматика, словарь, role play; пять коротких уроков, 12,5 часов.',
         '2027-07-05','2027-07-09',fit('conditional','Требуется класс Primaire; для сильного EN уточнить, нужен ли этот языковой уровень.'),
         fit('conditional','После начала начальной школы; не обещаем допуск по одному году рождения.'),'14:00–16:30'),
        ('littlebritish-zoo','Little British · Off to the Zoo / младшие','off-to-the-zoo/',
         '3–6 лет по конкретному planning; после 7-летия уже другая программа.',
         'На английском: животные, творчество, science experiments, игры/театр. Тема Zoo не обещает настоящую экскурсию в зоопарк.',
         '2027-07-12','2027-07-16',fit('not_eligible','9–10 лет вне конкретной группы 3–6.'),
         fit('conditional','Если ещё 6 на начало; после 7-летия выбрать Primaire. Точный день рождения неизвестен.'),
         '09:30–12:00 или 14:00–16:30; Meudon в таблице только утро')]:
        url=LB+course
        p=put(slug,name,'Франция','FRA','Paris 6 / 7 / 16 / 17 и Meudon',
            'languages,general,science' if slug.endswith('zoo') else 'languages,general','day',age,
            'Английский — содержание и язык занятий; это отдельное языковое занятие, не обещание полного дня или EN робототехники.',
            content,'Лето 2027: '+start+'–'+end+'; отдельные площадки, не пять разных операторов.',
            fee(2027,'EUR 300 / неделя, 2,5 часа в день × 5.',
                'Выбранная половина дня, всего 12,5 часа.',
                'Жильё/дорога/питание; не считаем две половины дня включёнными в один тариф.',
                'Скидки, отказ и уровень входа не установлены.'),'Только короткий дневной языковой формат: '+hours+'.',mat,osc,
            'Вариант городской семейной поездки, оценивать языковую пользу отдельно от технических лагерей.',
            ['Подтвердить класс/точный возраст, уровень, выбранные часы/площадку и отмену; зимняя реклама в footer не подтверждает этот летний курс зимой.'],
            [src('Конкретный летний курс 2027',url)],status='published_2027',confirmed=['EN'])
        p['language_evidence_role']='language_lessons'
        variants=[dict(start=start,end=end,label=address,variant_key=key,price='EUR 300 / 12,5 часа',place=address,
            source=url,formats=['day'],date_scope='day_camp_window') for key,address in campuses]
        p['timing'].update(variant_keyed=True,sessions=[[v['start'],v['end']] for v in variants],session_details=variants)

    p=put('navatormes-english','Respira · Navatormes English Camp','Испания','ESP','Navatormes / Navarredonda de Gredos, Ávila',
        'general,languages,sport,outdoor','boarding','7–17, группы по возрасту; иностранный внешний допуск отдельно подтвердить.',
        'В PDF 2026 прямо: английский во всех активностях и общении, instructors C1+. Это доказательство лагерной жизни прошлого сезона, не подтверждение staff 2027.',
        'Горные маршруты, конный/верёвочный парк, стрельба из лука, природные бассейны, квесты, ночи vivac. Языковая immersion через активности без обычных уроков; не робототехника.',
        'Landing «Próximamente 2027», но её собственный PDF озаглавлен Campamento 2026, даты 02–14 июля. Не переносим архив в календарь 2027.',
        fee(2026,'Архив EUR 618 / 13 дней; тот же тариф на landing без надёжного нового года.',
            'Питание, tipis с двухъярусными кроватями, основные активности/материалы, staff 24h, RC/accident insurance по PDF.',
            'Madrid bus EUR 50, cancellation insurance 20, hoodie 20; donation 5 добровольно. Условиe бесплатной hoodie первым 100 не гарантируем.',
            'Договор/отмена 2027 не подтверждены; PDF 2026 не переносится на новый набор.'),
        'PDF: tipis на 6–8 человек. FAQ landing говорит albergue: точный housing 2027 подтвердить; не обозначать как школьный пансион.',
        fit('candidate','Возраст подходит общему лагерю; новый сезон и иностранный допуск ещё неизвестны.'),
        fit('conditional','После 7-летия; до него не подходит.'),
        'Более доступный английский приключенческий вариант Испании; архив подробно изучен, новый набор ещё не подтверждён.',
        ['Получить датированный прайс/договор 2027, иностранный допуск, EN staff и точный тип жилья.'],
        [src('Landing с новым заголовком',NAV),src('Собственный информационный PDF 2026',NAVPDF)],confirmed=['EN'],priority=['general'])
    p['language_evidence_role']='camp_life'


def correct_profiles(profiles):
    p={x['slug']:x for x in profiles}
    a=p['aiglon']
    a['age']='Пансион Robotics 8–16; дневная таблица Robotics 7–16 против описания 8–16. Entrepreneurship / Leadership 13–16.'
    a['programme']='Classic: утренний VEX Robotics и общие активности; каждая программа одна неделя, многонедельный пакет выбирает несколько. Signature — отдельные полнодневные академии. Подробные дневные/пансионные пакеты вынесены в отдельные досье.'
    a['price']['label']='Брошюра 2027: пансион CHF 4 600 / 1 нед., 8 200 / 2 нед., 12 000 / 3 нед.; дневной CHF 2 500 / нед.'
    a['price']['extras']='Дневная субботняя экскурсия CHF 500; трансферы, питание/материалы точного пакета и отмена требуют проверки.'
    a['family_fit']['oscar']['detail']='После 7-летия дневной общий формат; Robotics 7–16 в day-таблице против 8–16 на основной странице, нужен прямой допуск.'
    a['questions']=['Подтвердить EN Robotics, часы/платформу/сложность, полный расчёт и расхождение возрастов дневной группы.']
    a['sources'].append(dict(title='Подробная брошюра 2027: VEX / цены / day age conflict',url=BROCHURE,checked=CHECKED))
    a['editorial_reason']='VEX-кандидат для Матвея; опубликованы дневные и пансионные цены. Для Оскара нужен возрастной допуск именно на Robotics.'
    r=p['rosenberg']
    r['age']='Общий camp 6–18, минимум 6 к первому дню; минимум конкретного Robotics / Coding / AI Focus Course пока неизвестен.'
    r['programme'] += ' Robotics & Engineering: недельный проект computer/robot; Coding: сайт/app/game; AI Agentic Enterprise: агенты и творческие бизнес-задачи. Общий возраст 6–18 не автоматически действует для каждого Focus Course.'
    r['sources'].append(dict(title='Общий возраст 6–18 и 6 лет к приезду',url='https://rosenbergcamps.ch/application/age-verification/',checked=CHECKED))
    for child in ['matvey','oscar']:
        r['family_fit'][child]=dict(status='conditional',detail='Возраст общего camp подходит 6–18; возраст/EN конкретного технического Focus Course ещё не подтверждены.')
    c=p['cdl']
    c['age']='Основной Summer Camp 8–18; afternoon AI Robotics VEX AIM 12+, startup/future leaders 10+, drones 11+; Robot Mash-up отдельно подтвердить.'
    c['programme']='Выбор четырёх активностей за две недели: утро и день каждую неделю. Утренний Robot Mash-up VEX GO/IQ / BattleBot; afternoon AI Robotics VEX AIM только 12+. Coding, Science Lab; startup 10+. По средам после обеда pool party. Не весь день VEX/ИИ.'
    c['timing'].update(status='partial_2027',label='2027: 27.06–10.07, 11–24.07, 25.07–07.08; регистрация 2027 открывается в ноябре. Прайс на той же странице явно ещё 2026.',sessions=[['2027-06-27','2027-07-10'],['2027-07-11','2027-07-24'],['2027-07-25','2027-08-07']])
    c['price']['label']='Архив 2026: CHF 6 830 пансион / 3 360 день за 2 недели. Цены 2027 ещё не опубликованы.'
    c['price']['extras']='Премиальные afternoon activities на странице CHF 800 / нед.; этот архивный тариф не переносится в 2027.'
    c['accommodation']='Дневной пн–пт 09:00–17:00 с обедом; boarding — отдельные villas, питание/вечера/выходные и airport transfer по описанию; состав нового тарифа подтвердить.'
    c['family_fit']['matvey']['detail']='Основной возраст подходит; Robot Mash-up проверить отдельно, AI Robotics VEX AIM с 12 пока недоступен.'
    c['editorial_reason']='VEX GO/IQ кандидат для Матвея с новыми датами 2027; AI VEX AIM 12+ пока будущая ступень. Цена и технический язык ещё нужны.'
    c['questions']=['Подтвердить Robot Mash-up для 9–10 лет, EN, прайс/обязательные доплаты 2027 и выбранные модули; VEX AIM до 12 не обещать.']
    for a,b in c['timing']['sessions']:
        c['timing'].setdefault('session_details',[]).append(dict(start=a,end=b,label='Основная смена / выбор возрастных модулей',price='Тариф 2027 не опубликован; архив 2026 в досье',
            place=c['place'],source=c['sources'][0]['url'],formats=['day','boarding']))
    for slug in ['aiglon','rosenberg','cdl']:
        p[slug]['checked']=CHECKED
        for s in p[slug]['sources']:s['checked']=CHECKED


def correct_catalog(catalog):
    """Resolve the formerly undated week from the actual linked camp detail page."""
    row=next(e for e in catalog['events'] if e['id']=='L222')
    row.update(title='Helvetic Institute · Robotics Summer 2027 · Zug · 07-12',
        start='2027-07-12',end='2027-07-16',source=ZUG,checked=CHECKED,
        period='Подробная карточка: 12–16 июля 2027; week 2, пн–пт.',date_status='Подтверждено',
        age='Подробный курс рассчитан на 6–11; обзорная summer-таблица 4–12, общий intro 7+ — младший допуск подтвердить.',
        cost='2027 · CHF 730 / неделя; экскурсии включены, packed lunch с собой; materials fee уточнить.',
        gear='Утром робототехника / block coding или Scratch / AI digital modelling; после обеда экскурсии и активности.',
        proof='Подробная собственная карточка Summer Robotics Camp Zug прямо указывает Week 2: July 12th–16th 2027; прочитана в браузере.',
        note='Дата 12–16 июля подтверждена конкретной карточкой, без самостоятельного исправления 13–16 из обзорной таблицы. 09:00–16:00 пн–пт; обед/воду принести с собой. Язык технического курса и младший возрастной допуск ещё неизвестны.',
        references=[dict(label='Обзорная таблица с ошибкой 13–16',url=HEL),dict(label='Подробный Summer Camp Zug: 12–16',url=ZUG)],
        date_scope='day_camp_window',date_precision='published_session',attendance_weekdays=['MO','TU','WE','TH','FR'])


def extend_report(report):
    report['shortlist'].extend([
        dict(label='Швейцария · VEX с понятными пакетами',slugs=['aiglon-classic-day','aiglon-classic-board','cdl'],reason='Aiglon: дневные недели CHF 2 500, пансион 4 600/8 200/12 000; Robotics утром, при длинном проживании несколько программ. CDL уже имеет три смены 2027, но прайс 2026. Матвею VEX GO/IQ; VEX AIM с 12. Оскару Aiglon только после 7 и согласования расхождения 7+/8+.'),
        dict(label='Швейцария · робототехника в семейной поездке',slugs=['helvetic-zug-summer','helvetic-zurich-summer'],reason='CHF 730 / неделя, отдельные Zug / Zürich даты. В Zug подробная карточка исправляет вторую неделю на 12–16 июля; утро техника, день экскурсии, packed lunch. Язык курса и младший допуск ещё уточнить.'),
        dict(label='Франция · зимние и весенние английские каникулы',slugs=['babel-holiday-english'],reason='Tournefeuille: полные дни EUR 350 или утро EUR 160; 19–23 октября, 8–12 февраля, 5–9 апреля. 100% EN, группы PS–CM2. Летний конфликт 2026/27 не включён в календарь.'),
        dict(label='Франция / Испания · языковые форматы разной длительности',slugs=['littlebritish-boost','littlebritish-zoo','navatormes-english'],reason='Paris/Meudon: 12,5 часа за EUR 300, не полный день; Primaire по классу, Zoo 3–6 до 7-летия. Navatormes: 13-дневный английский приключенческий лагерь в tipis, но собственный PDF/прайс пока 2026. Не технические интенсивы.')])
    report['gaps'].extend([
        dict(country='Швейцария',iso='CHE',provider='Aiglon · младший Robotics и недельные программы',detail='Брошюра 2027 прочитана визуально: пансион 8–16; дневная таблица Robotics 7–16, а описание и основная страница 8–16. Пять day-недель и шесть boarding-пакетов имеют собственные тарифы. Каждый курс одна неделя; длинные пакеты выбирают несколько программ, а не гарантируют три недели VEX.',next_action='Подтвердить младший допуск, язык, часы/уровень VEX и полный пакет; переносить среднюю цену на другую программу нельзя.',url=AIGLON),
        dict(country='Швейцария',iso='CHE',provider='Helvetic · подробная карточка против overview',detail='Summer Zug прямо 12–16 июля 2027 вместо ошибочных 13–16 в overview; CHF 730/неделя, 1 460/2 недели; packed lunch. Технический intro 7+, summer overview 4–12, подробный Zug рассчитан на 6–11. Язык общего camp не доказательство EN Robotics; условия Zug не переносим на Zürich.',next_action='Получить точный летний адрес, EN/DE группу, минимальный возраст, materials fee и отмену. L222 обновлена из недатированной спорной записи; другие старые записи сохранены и связаны без повторов.',url=ZUG),
        dict(country='Швейцария',iso='CHE',provider='Rosenberg / College du Léman · возраст курса и тарифный год',detail='Rosenberg age form подтверждает только общий camp 6–18 и 6 лет к приезду, не минимум Robotics / AI. CDL публикует три смены 2027, регистрацию с ноября, но цену явно 2026. Afternoon VEX AIM 12+; startup 10+, drones 11+. Разные modules и pool-party Wednesday влияют на техчасов.',next_action='Проверить EN/минимум выбранного курса и полный прайс/договор 2027; age verification не выполнялась.',url='https://rosenbergcamps.ch/application/age-verification/'),
        dict(country='Франция',iso='FRA',provider='Babel / Little British · летний год и класс',detail='Babel летний заголовок 2027 против body 2026, поэтому summer исключён. Little British Boost 5–9 июля2027 требует Primaire; Zoo12–16 июля2027 группа3–6. British POP по-прежнему 13–17 июля2026; соседняя реклама зимы2027 не обновляет его. Пять площадок не пять операторов, 2,5 часа не полный день.',next_action='Подтвердить классы/уровни детей, утро/день, питание, скидки/отмену и исправление summer Babel.',url=BABEL),
        dict(country='Испания',iso='ESP',provider='Navatormes / Costa Blanca · жильё, язык и архив',detail='Navatormes landing «Próximamente2027», собственный PDF2026 подтверждает EUR618,2–14июля,7–17,tipis6–8 и EN всех активностей. FAQ говорит albergue: housing/2027 ещё нужны; нет новых точных дат. Costa Blanca описывает12 sessions, не12 часов, и презентации EN/ES, не весь технический инструктаж; ещё summer2026.',next_action='Датированные 2027 документы, иностранный допуск и полные расходы; не называть tipis школьным пансионом и не выдавать английскую презентацию за EN Robotics.',url=NAV)])
