"""Programme-specific European language/general camps: current primary 2027 documents."""
from copy import deepcopy
import re

CHECKED = '2026-10-05'
AL = 'https://www.alpadia.com/'
CH = 'https://chantemerle.ch/'
EC = 'https://english-camp.ch/'
EN = 'https://www.enforex.com/en/summer-camps/'
EPDF = 'https://download.enforex.com/pdf/enforex-summercamps.pdf'

# Exactly the dots in the independently rendered 2027 price/date table (page 33).
# A weekly tariff does not establish that every start is available at every campus.
ONE = [('2027-06-27','2027-07-03'),('2027-07-04','2027-07-10'),
       ('2027-07-11','2027-07-17'),('2027-07-18','2027-07-24'),
       ('2027-07-25','2027-07-31'),('2027-08-01','2027-08-07'),
       ('2027-08-08','2027-08-14'),('2027-08-15','2027-08-21'),
       ('2027-08-22','2027-08-28')]
TWO = [('2027-07-04','2027-07-17'),('2027-07-18','2027-07-31'),
       ('2027-08-01','2027-08-14'),('2027-08-15','2027-08-28')]
STARTS = {
    'madrid': ONE[:7]+TWO[:3], 'marbella-elviria': ONE+TWO,
    'salamanca': ONE[:5]+TWO[:2], 'barcelona': ONE[1:8]+TWO[:3],
    'alicante': ONE[:7]+TWO[:3], 'malaga': ONE[:7]+TWO[:3],
    'barcelona-centro': ONE[5:]+TWO,
    'marbella-centro': ONE+TWO,
    'valencia': [ONE[i] for i in [0,5,6,7,8]]+TWO,
}

def readable(t):
    """Space editorial facts without touching URLs, IDs, source data or old records."""
    replacements={'3Dprinting':'3D-печать','3D printing':'3D-печать','one-way':'в одну сторону',
        'privatebath':'с собственной ванной','sharedbath':'общая ванная','shareddouble':'двухместная',
        'sharedroom':'общая комната','singleroom':'одноместная комната','nightcare':'ночной присмотр',
        'agegroup':'возрастная группа','fullboard':'полный пансион','baseprice':'базовая цена',
        'all-ininvoice':'полный счёт','fullinvoice':'полный счёт','teacherhours':'часы преподавателя',
        'campminimum':'минимальный возраст лагеря','language-only':'только языковые занятия',
        'twochildren':'двое детей','Singlebedroom':'одноместная комната','Tripleroom':'трёхместная комната',
        'Double':'двухместная','Primary':'основной','currentinvoice':'актуальный счёт',
        'campuscolumnpage':'столбец кампуса на странице','two-week':'двухнедельная',
        'minimum9':'минимальный возраст 9','YoungAdults':'Young Adults','InternationalSummerCamps':'International Summer Camps',
        'MonFri':'пн–пт','whole-camp':'весь лагерь','camp life':'повседневная жизнь лагеря',
        'camplife':'повседневная жизнь лагеря','life-skills':'жизненные навыки',
        'Private-bath':'С собственной ванной','Single-room':'Одноместная','course-only':'только языковой курс',
        'application':'регистрация','weekendactivities':'занятия выходного дня','private-bath':'с собственной ванной'}
    for a,b in replacements.items():t=t.replace(a,b)
    t=re.sub(r'(?<=[А-Яа-яЁё])(?=[A-Za-z0-9])|(?<=[A-Za-z0-9])(?=[А-Яа-яЁё])',' ',t)
    t=re.sub(r'(?<=[a-z])(?=[A-Z])',' ',t)
    t=re.sub(r'(?<=[A-Za-zА-Яа-яЁё])(?=\d)|(?<=\d)(?=[A-Za-zА-Яа-яЁё])',' ',t)
    t=t.replace('3 D-печать','3D-печать')
    t=re.sub(r'([,;:])(?=\S)',r'\1 ',t)
    return t

def polish(p):
    for key in ['age','language','programme','accommodation','editorial_reason']:
        p[key]=readable(p[key])
    p['questions']=[readable(s) for s in p['questions']]
    p['timing']['label']=readable(p['timing']['label'])
    for v in p['timing'].get('session_details',[]):
        for key in ['label','price','age','entry','attendance_weekdays']:
            if key in v and isinstance(v[key],str):v[key]=readable(v[key])
    for v in p['family_fit'].values():v['detail']=readable(v['detail'])
    for key in ['label','included','extras','deposit']:p['price'][key]=readable(p['price'][key])
    for s in p['sources']:s['title']=readable(s['title'])

def add_europe_v85(add, src, fit, profiles):
    def put(slug, name, iso, place, themes, formats, age, language, programme, dates,
            price, housing, mat, osc, why, questions, urls, status='partial_2027',
            sessions=None, confirmed=None, role=None, priority=None, window=False):
        add(slug,name,{'CHE':'Швейцария','FRA':'Франция','ESP':'Испания'}[iso],iso,
            place,themes,formats,age,language,programme,dates,price,housing,mat,osc,why,
            questions,[src(t,u) for t,u in urls],status=status,sessions=sessions,
            confirmed=confirmed or [],priority=priority or [])
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        if window:p['timing']['precision']='season_window'
        return p
    def fee(year,label,included,extras,deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def details(p,url,records=None):
        p['timing']['session_details']=records or [dict(start=a,end=b,label='Смена',
            source=url,place=p['place'],price=p['price']['label'],formats=p['formats'])
            for a,b in p['timing']['sessions']]

    alterms=AL+'en/terms-and-conditions'
    aldep='Прочитанные условия ещё устанавливают цены и сборы 2026 года: аванс CHF/EUR 300 в счёт курса, остаток за 4 недели. Регистрация CHF125 в Швейцарии / EUR90 во Франции, однако пакет лагеря прямо включает регистрацию: повторно не прибавляем. При отмене за22 и более дней удерживаются перечисленные сборы и опции; менее чем за21 день возврата нет. Ровно21 день не описан. Нужен договор2027.'
    alang='Можно выбрать английский языковой курс. Английский подтверждён для уроков; язык спортивных занятий, экскурсий и общения в пансионе нужно уточнить.'
    for slug,name,iso,place,age,url,pairs,dates,priceextra,housing,mat,osc in [
        ('alpadia-leysin','Alpadia Leysin · Spring / Summer','CHE','Le Central Résidence & Spa, Route du Belvédère, 1854 Leysin','8–17',AL+'en/language-camps/switzerland/leysin',
         [['2027-03-29','2027-04-16'],['2027-06-21','2027-08-06']],
         'Весеннее окно 29 марта – 16 апреля, летнее 21 июня – 6 августа 2027. Это даты работы Mon–Fri; проживание Sunday–Saturday по общему правилу. Конкретная смена/начало для уровня ещё не подтверждены.',
         '2027 EN page: one-way CHF100 местный bus, CHF210 Geneva airport, CHF230 Geneva train. Premium cooking 8–14 CHF140/week; riding/fitness/adrenalin13+ CHF230/week. Старые FR2026 Geneva200/UM40/private300 не новые тарифы.',
         'Отель, комнаты с ванной; all meals, 24/7 support и общие activities. Родители живут отдельно.',
         fit('candidate','В 2027 9–10: минимум8 подходит; языковой уровень/место подтвердить.'),fit('later','В 2027 6–7; минимум8, не подходит младшему.')),
        ('alpadia-engelberg','Alpadia Engelberg · English / German','CHE','Benediktinerkloster 5, 6390 Engelberg','10–17',AL+'en/language-camps/switzerland/engelberg',
         [['2027-06-28','2027-07-30']],
         'Летнее окно 28 июня – 30 июля 2027. Opening dates курса, не единая обязательная пяти-недельная смена. Проживание Sunday–Saturday; точные выбранные недели подтвердить.',
         'Zurich airport CHF160 one-way по текущей EN page; premiums и insurance в окончательной смете. Сборы Terms2026 не гарантированы для2027.',
         'Резиденция монастырского кампуса, single/twin с общими ванными; all meals, 24/7 support.',
         fit('conditional','Только после 10-летия к выбранному началу: ребёнок2017 может быть ещё9.'),fit('later','Младше10 в2027.')),
        ('alpadia-paris-passy','Alpadia Paris–Passy · English / French','FRA','La Salle Passy Buzenval, 50 avenue Otis Mygatt, 92500 Rueil-Malmaison','13–17',AL+'en/language-camps/french/france/paris-passy',
         [['2027-06-28','2027-08-06']],
         'Летнее окно 28 июня – 6 августа 2027; точные недельные заезды и availability не установлены. Sunday–Saturday accommodation не даёт автоматический календарь всех понедельников.',
         'One-way: EUR120 Gare de Lyon / de l’Est / du Nord, EUR80 ORY, EUR90 CDG. Base weekly price не виден в прочитанном camp price section.',
         'Single-bedroom residence, все meals, 24/7 support, sports и поездки по Парижу.',
         fit('later','Минимум13, будущая подростковая ступень.'),fit('later','Минимум13, не лагерь6–7.')),
    ]:
        p=put(slug,name,iso,place,'general,languages,sport,art','boarding',age,alang,
            'Standard20: 20 уроков×45 минут =15 часов/нед.; Intensive25:18ч45м, не18.45 десятичных часа. Все уровни, максимум15 в группе. Язык, speaking/listening, collaborative projects, sport/culture; полноценного robotics/AI курса нет.',
            dates,fee(None,'Базовая стоимость2027 в прочитанных страницах не раскрыта; цены опций не полная цена лагеря.',
                'Camp package включает enrolment, tuition, accommodation, meals и основные activities; материалы, assessment, certificate и language portfolio.',
                priceextra+' Mandatory medical/accident insurance по Terms; current2027 cover/цена неизвестны.',aldep),
            housing,mat,osc,'Языковой пансион с EN course; минимальный возраст и цена нуждаются в отдельной проверке выбранного набора.',
            ['Полный прайс/договор2027, конкретная смена, whole-camp EN support, room/food, insurance, optional sport и допуск внешнего ребёнка.'],
            [('Конкретный camp: возраст/курс/окно2027',url),('Terms: сезон цен2026 и accommodation rule',alterms),('Brochure page пока2026',AL+'en/brochure')],
            sessions=pairs,confirmed=['EN'],role='language_lessons',window=True,
            priority=['general','boarding'] if iso=='CHE' else [])
        details(p,url)
    put('alpadia-paris-igny','Alpadia Paris–Igny · English / French','FRA','Igny / Paris · точный campus address до поездки подтвердить',
        'general,languages,sport','boarding','13–17',alang,
        'English/French course в зелёном пятигектарном кампусе, classroom/project language practice и культурные поездки в Париж; это языковой, не robotics camp.',
        'Own page всё ещё Summer28June–08August2026. Не перенесено в2027 и не создано будущих календарных смен.',
        fee(None,'Тариф следующего2027 набора неизвестен.','Пакет включает tuition/enrolment/accommodation/meals/activities по странице.',
            'Трансфер, insurance, premiums и обязательные сборы2027 уточнить.',aldep),
        'Резиденция, meals и24/7support; конкретный room allocation нового сезона неизвестен.',
        fit('later','13+; в2027 пока9–10.'),fit('later','13+; пока6–7.'),
        'Будущий EN вариант Парижа; соседнийPassy2027 не доказывает новыйIgny набор.',
        ['Новый Igny calendar/price, язык всей camp life, внешний приём и договор.'],
        [('Igny own page: EN choice,13–17,2026',AL+'en/language-camps/french/france/paris-igny'),('Terms',alterms)],
        status='published_2026',confirmed=['EN'],role='language_lessons')

    churls=[('Own Summer2027 PDF: ages6–11/12–16, dates/fees',CH+'documents/summer-camp-2027-brochure.pdf'),
            ('Full2027 price and cancellation',CH+'en/fees/'),('Morning tracks and languages',CH+'en/summer-camp-switzerland/language-camps/'),
            ('Activities: outdoor/art/3D printing',CH+'en/summer-camp-switzerland/activities/')]
    chdep='Первый платёж CHF800 невозвратный, покрывает регистрацию и закрепляет место. Из текста неясно, включён ли он полностью в базовую цену или является дополнительным сбором: нужен счёт. Остаток за30 дней. Отмена более чем за60 дней: возврат минус первый платёж; за31–60 дней:50% стоимости программы, первый платёж удерживается; за30 дней и менее: возврата нет. Болезнь, тоска по дому и ранний отъезд не дают возврат за неиспользованные услуги. CHF1600 относится к учебному году, не к летнему лагерю.'
    chlang='Speak Up: языковые занятия на выбранном английском, французском или немецком. Английские уроки подтверждены. Для детей, уже говорящих по-английски, нужно выбрать подходящий уровень; язык остальных занятий и общения в пансионе уточняется отдельно.'
    for slug,name,fmt,label,inc,extra,house in [
        ('chantemerle-junior-board','Chantemerle · Junior Residential','boarding','CHF4950/2нед.,6250/3,7500/4,8900/5. Fees также1нед.2800, но brochure рекламирует минимум2: one-week admission уточнить.',
         'Full board, academic courses/materials20h/week,24/7care, activities/excursions,2-day Europa-Park и airport transfers10–18 включены.',
         'Medical insurance CHF8/day; sport academy600/5days, full-day tennis/golf800 — indicative. Family2kids/2weeks base9900 +medical224; registration800 treatment, adult lodging/flights/optional sports неизвестны.',
         'Пансион семейной школы вBlonay, общий заявленный максимум65; room/counselor/night care младших подтвердить.'),
        ('chantemerle-junior-day','Chantemerle · Junior Full Day','day','CHF1600/week за ребёнка. Два ребёнка2недели: baseCHF6400 до extras/registration и жилья родителей.',
         'Academic programme, lunch/evening meal, excursions и activities; это полный дневной пакет без проживания.',
         'Airport CHF200return, medical CHF8/day, Europa-Park CHF300, optional academies600/800indicative. Adults hotel и local transport отдельно.',
         'Дети возвращаются к родителям; жильё семьи и точные часы передачи детей отдельно.'),
        ('chantemerle-junior-halfday','Chantemerle · Junior Academic Half Day','day','CHF1100/week за ребёнка; два ребёнка2недели baseCHF4400 до extras/registration.',
         'Только academic courses и lunch. Afternoon activities/экскурсии не входят; не полная дневная программа.',
         'Airport CHF200return, insurance CHF8/day и отдельные options по invoice; жильё родителей/after-lunch childcare отдельно.',
         'Без проживания и afternoon activities; родители отвечают за оставшуюся часть дня.'),
    ]:
        p=put(slug,name,'CHE','Chemin de Chantemerle 7, 1807 Blonay','general,languages,art,sport,adventure',fmt,
            'Junior6–11 по конкретному2027 PDF. SEO/page header8–17 не отменяет первичную junior category6–11.',chlang,
            'Утренний языковой SpeakUp и hands-on projects. Full/day boarding дополнены nature/sport/arts. 3Dprinting есть в activities, но часы/возраст/EN не установлены: не обещаем полноценный курсrobotics/AI.',
            'Окно27июня–1августа2027, advertised2–5week stays. Конкретные заезды/недельное меню не установлены; это seasonal availability window, не единая35-дневная смена.',
            fee(2027,label,inc,extra,chdep),house,
            fit('candidate','9–10 входит в junior6–11; выбранный поток/место подтвердить.'),
            fit('candidate','6–7 входит в junior6–11 после6-летия; готовность к пансиону оценить отдельно.'),
            'Одно из совместных младших направлений с первично подтверждёнными2027 ценами; day/half-day/boarding отличаются по составу.',
            ['Конкретная смена, English camp life и advanced language benefit, комнатный/night-care план, CHF800 inclusion, all-in invoice, Europa-Park dates и возраст options.'],
            churls,status='published_2027',sessions=[['2027-06-27','2027-08-01']],confirmed=['EN'],role='language_lessons',
            priority=['both','general']+(['boarding'] if fmt=='boarding' else []),window=True)
        details(p,CH+'en/fees/')
    p=put('chantemerle-leadership','Chantemerle · Make It Count','CHE','Chemin de Chantemerle 7, 1807 Blonay',
        'general,entrepreneurship,science,adventure','boarding','Teens12–16 по2027 brochure; конкретный age gate MakeItCount подтвердить.',
        'MakeItCount прямо in English; English workshops подтверждены, не только EN website.',
        'Двухнедельные life skills: culinary/team project, TEDx-style debate, SafeWaterCube engineering water fountain и survival challenge. TEDx-style не officialTEDx и не международное соревнование.',
        '18июля–1августа2027, конкретный двухнедельный MakeItCount блок.',
        fee(2027,'Общий двухнедельный campCHF4950; включён лиMakeItCount без course surcharge — нужен invoice.',
            'Общий boarding package20h/week/fullboard/activities/excursions поfees; особенности конкретногоtrack подтвердить.',
            'Insurance8/day, optional sport, track surcharge неизвестен; взрослые/перелёт отдельно.',chdep),
        'Школьный пансион; teen group, room/care зависит от выбранного course.',
        fit('later','12+; future engineering/life-skills track.'),fit('later','12+, неjunior6–11.'),
        'Будущая ступень самостоятельности и инженерных/предпринимательских навыков; не текущая младшая смена.',
        ['Age MakeItCount, course inclusion/fee, конкретные projects/teacher hours, admission и полный пакет.'],
        churls,status='published_2027',sessions=[['2027-07-18','2027-08-01']],confirmed=['EN'],role='primary')
    details(p,CH+'en/summer-camp-switzerland/language-camps/')
    p=put('chantemerle-maths-physics','Chantemerle · Maths / Physics Revision','CHE','Chemin de Chantemerle 7, 1807 Blonay',
        'science,engineering,general','boarding','Course page14–17, brochure camps teens12–16: допуск17-летних требует отдельного подтверждения.',
        'English илиFrench для Maths/Physics по course page; English lessons подтверждены.',
        'Повторение maths/physics с преподавателями, описанными оператором как EPFL engineers, и visitEPFL. Это описание Chantemerle; официальная EPFL academic accreditation/partnership не проверена.',
        '«2-week programme available June27–July18 2027»: трёхнедельное окно выбора двух недель, не21-дневная смена. Конкретные cohort dates неизвестны.',
        fee(2027,'Общий2-week tariffCHF4950; включениеrevision/surcharge и17-летний допуск уточнить.',
            'Общий fullboard/academic package поfees; track-specific состав и visitEPFL требуется подтвердить.',
            'Insurance8/day, optional sport/course fees и travel отдельно.',chdep),
        'Пансион; конкретная дата/комната неизвестны.',fit('later','Минимум14.'),fit('later','Минимум14.'),
        'Будущий physics/engineering маршрут, конкретный доступ ещё не полностью определён.',
        ['Две конкретные недели, допуск17 приbrochure12–16, EN teacher/team, visit/fee и invoice.'],
        churls,sessions=[['2027-06-27','2027-07-18']],confirmed=['EN'],role='language_lessons',window=True)
    details(p,CH+'en/summer-camp-switzerland/language-camps/')

    ecurls=[('2027: четыре точные недели иage9–15',EC+'infos/infos-fuer-eltern/daten-2027'),
            ('2026&2027: собственная price table/terms',EC+'infos/preise'),('English small-group lessons и programme',EC)]
    ecdep='Административный сбор CHF50 на счёт невозвратный. Счёт оплачивается за30 дней после подтверждения. При отмене:70% до30 дней,30% за30–10 дней,10% менее чем за10 дней. Граница ровно30 дней в тексте пересекается — нужно уточнить договор. При раннем отъезде или болезни возврата нет. Старый перенос из-за COVID2020 в лагеря2022/23 не считаем условиями2027.'
    for slug,name,place,pairs in [
        ('englishcamp-switzerland-spring','English Camp Switzerland · Spring','Ritterhaus Ürikon / Zürichsee',
         [['2027-04-18','2027-04-24'],['2027-04-25','2027-05-01']]),
        ('englishcamp-switzerland-summer','English Camp Switzerland · Summer','Burg Mariastein-Rotberg, near Basel',
         [['2027-07-11','2027-07-17'],['2027-07-18','2027-07-24']]),
    ]:
        p=put(slug,name,'CHE',place,'general,languages,art,adventure','boarding','9–15 поDATEN2027; sibling discount не отменяетminimum9.',
            'EN lessons5×3h/week, малые группы5–7. English practice днём/вечером; для beginners упомянута German assistance. English-only foreign family/admin support подтвердить.',
            'Общий языковой residential programme, trips, две workshop days (film/photography и др.), outdoor activities. Robotics/AI интенсив не заявлен.',
            'Две конкретные Sun–Sat недели2027; можно1/2weeks. Тарифы3/4weeks есть, но3/4week cohorts2027 не опубликованы; календарь их не выдумывает.',
            fee(2027,'RegularCHF1380/1week,2430/2 +50/invoice =1430 или2480 для одногоMatvey. Early/BringFriend1290/2290, sibling1150/2150 только eligible children; discount deadline/rules неизвестны.',
                'Пансион,3meals/snacks,15h EN,3excursions,2workshop days. SundayEuropaPark/Rulantica для2–4week programme.',
                'Transfer/insurance/flight не раскрыты. Family sibling rate не рассчитан дляOscar: младший ниже9. 3/4week regular3380/4300 не подтверждённые3/4week dates.',ecdep),
            'Ritterhaus/castle residential; room/nightcare/foreign admission подтвердить.',
            fit('candidate','В2027 9–10:9–15 подходит, EN level/место отдельно.'),fit('later','6–7 меньше9; sibling tariff не admission.'),
            'Более короткий общий English пансион Матвею с точными2027 неделями; Oscar пока не проходит.',
            ['English/German dependence, место, all-in invoice, early conditions, transfer/insurance и точный cancellation boundary.'],
            ecurls,status='published_2027',sessions=pairs,confirmed=['EN'],role='language_lessons',priority=['general','boarding'])
        details(p,EC+'infos/infos-fuer-eltern/daten-2027',records=[dict(start=a,end=b,label='One week',
            source=EC+'infos/infos-fuer-eltern/daten-2027',place=place,formats=['boarding'],
            price='CHF1380 +CHF50/admin per invoice; одногоMatvey regularCHF1430') for a,b in pairs])

    # One shared official 2027 PDF carries the exact campus/age/date/format differences.
    # Read-only investigation: course-only is quoted separately, never as a full camp.
    enlang='Английский или испанский языковой курс:20 уроков по45 минут, то есть15 часов в неделю. Уровни A1–C2, группы8–16. Английский вариант подтверждён каталогом2027; язык спорта и повседневного общения уточняется отдельно.'
    enextra='Регистрация EUR35 один раз на участника. Аэропорт или местный вокзал EUR95 на человека в одну сторону; автобус дневного лагеря EUR250 за2 недели там, где доступен. Выходной день EUR100, дополнительная ночь суббота–воскресенье EUR125, форма EUR130. Дополнительная гарантия отмены EUR300 в неделю. Спорт за2 недели: теннис/падел EUR290, верховая езда400, гольф500; возраст и доступность каждой опции уточняются. Жильё родителей и перелёты отдельно.'
    endep='Особые условия детского лагеря: при записи за4 недели или менее счёт оплачивается целиком сразу. Отмена в последние4 недели — штраф EUR850; за2 недели и менее или после приезда возврата нет. В общих условиях также указаны невозвратный депозит EUR250 и остаток за4 недели: применимость депозита к выбранному лагерю нужно подтвердить, повторно к tuition не прибавляем. Гарантия отмены EUR300 в неделю добровольная, с отдельными исключениями.'
    def en_fee(board_cost):
        return fee(2027,f'Пансион EUR{board_cost[0]}/1 неделю,{board_cost[1]}/2,{board_cost[2]}/3,{board_cost[3]}/4. Дневной600/1200/1800/2400 за1–4 недели. Только язык300/600/900/1200. Плюс EUR35 регистрации на ребёнка.',
            'Пансион:20 языковых уроков, материалы, общая комната, питание, мастерские, спорт, занятия, экскурсии, медицинская страховка и круглосуточный присмотр. Дневной формат пн–пт09–20: уроки, материалы, обед и занятия, без ночёвки. Только язык пн–пт09–12:30:20 уроков с перерывом, без полной лагерной программы.',
            enextra,endep)
    def en_records(p,campus,fmt,cost):
        records=[]
        for a,b in STARTS[campus]:
            weeks=1 if (a,b) in ONE else 2
            tuition=cost[weeks-1] if fmt=='boarding' else 600*weeks
            records.append(dict(start=a,end=b,label=f'{weeks} week · '+('Residential' if fmt=='boarding' else 'Day camp'),
                source=EPDF,place=p['place'],formats=[fmt],price=f'EUR{tuition} tuition +35/person application = EUR{tuition+35}; extras отдельно',
                date_precision='exact',date_scope='day_camp_window' if fmt=='day' else 'camp_session',
                entry='Опубликованная смена2027; место, admission/room и final invoice подтверждает оператор. Никакой заявки не отправлено.'))
            if fmt=='day':records[-1]['attendance_weekdays']=['MO','TU','WE','TH','FR']
        return records
    family_campuses=[
        ('madrid','Madrid','Wynwood University Residence Complex / Madrid',(1395,2495,3895,4895),
         'Private-bath double rooms, optionalsingle +EUR210/week; 4meals/day. OwnPDF campus15minfromcenter, не гарантированный адресизобщегоHQ.',
         'Pool/sportfields, language/culture, creative activities, excursions;180capacity,50%international/50%Spanish поoperator.'),
        ('marbella-elviria','Marbella Elviria','German High School / Deutsche Schule, Marbella Elviria',(1195,2095,3295,3995),
         'Sharedrooms:older4–6,younger6–12;single неavailable.4meals/day. Для6–7 важныnight-care, counselor ratio иготовностьксамостоятельномупансиону.',
         'Schoolcampus/gardens/beach/sport,200capacity,50%international/50%Spanish. Этообщий языковойcamp, отдельныйroboticscourse не заявлен.'),
        ('salamanca','Salamanca','Colegio Calasanz, Salamanca',(1195,2095,3295,3995),
         'Schoolresidence single/double, singleswithoutfee сsharedbath;4meals/day. Homestay14+ не вариантдлядетей6–10.',
         'Историческийгород,language/sport/creativeactivities,150capacity,70%international/30%Spanish. Ночёвки по возрастнымгруппам.'),
    ]
    for campus,name,place,cost,house,programme in family_campuses:
        for fmt,suffix in [('boarding','Residential'),('day','Day Camp')]:
            p=put('enforex-'+campus+'-'+('board' if fmt=='boarding' else 'day'),'Enforex '+name+' · '+suffix,'ESP',place,
                'general,languages,sport,art',fmt,'Kids/Teens programme5–18 поpage33. Общаяdestinationpage может включатьYoungAdultsдо21; это другойпродукт.',
                enlang,programme+' '+('Residential24hcare иovernight, неhomestay.' if fmt=='boarding' else 'DayMonFri09–20, lunch; родителизабираюткаждыйвечер.'),
                f'2027, {len(STARTS[campus])} явноотмеченных1/2week cohorts поcampuscolumnpage33. 3/4week tariffs есть; конкретные3/4week combinations/availability неустановлены, отдельнонеразмножены.',
                en_fee(cost),house if fmt=='boarding' else 'Безпроживания;семьяживётотдельно,weekendactivitiesoptional.',
                fit('candidate','9–10 входит5–18;group/level/местоотдельно.'),fit('candidate','6–7 входит5–18;minimum5 не гарантияготовностикпансиону.'),
                'Оба по возрасту могутрассматриватьобщийиспанскийcamp;разницаday/boarding иroomsizeсущественна.',
                ['ТочныеDOB/agegroup, ENилиESadvancedcourse дляbilingualдетей, место, nightcare, food, sports/transfer, deposit и полныйсемейныйinvoice.'],
                [('Official2027 PDF:campus-specificdates/ages/prices/terms',EPDF),('Owncamp webpage пока2026',EN+campus)],
                status='published_2027',sessions=[list(x) for x in STARTS[campus]],confirmed=['EN','ES'],role='language_lessons',priority=['both','general'])
            details(p,EPDF,records=en_records(p,campus,fmt,cost))
            if fmt=='boarding':
                p['price']['extras']+=f' Дваchild2weeks base+application EUR{2*(cost[1]+35)}; twochildren airportreturn EUR380 сверху еслинужен;flight/adultstay/otheroptions отдельно.'

    # Refresh the existing CP018 instead of counting Barcelona Beach twice.
    beach=next(p for p in profiles if p['slug']=='enforex-barcelona')
    historical=deepcopy({k:beach[k] for k in ['age','programme','timing','price','sources','checked']})
    beach['previous_seasons']=[dict(season=2026,record=historical)]
    beach.update(age='Kids5–16 по2027PDFpage22/33; стараяwebcategory5–15 неcurrent2027.',
        language=enlang,language_evidence_role='language_lessons',checked=CHECKED,
        programme='UPC universityresidence Castelldefels, beach/sport/language/culture,180capacity,80%international/20%Spanish поoperator. Day,boarding иcourse-only имеютразныйсостав. Campgamesroom неcomputerengineeringcourse.',
        accommodation='Private-bath shareddouble rooms, airconditioning,4meals/day;optional single +EUR350/week. Homestay14+ нельзяавтоматическиназначитьмладшим.',
        timing=dict(status='published_2027',label='4июля–21августа2027. Вpage33:7one-week и3two-week cohorts; July1weekstarts есть, unlikeBarcelonaCentro. Необъявлена2-week Aug15–28 дляBeach.',sessions=[],variant_keyed=True),
        price=en_fee((1395,2495,3895,4895)),
        questions=['Конкретныйday/boardingcohort, EN/ESlevel, room/food/nightcare, transport/options и полный2027invoice.'],
        sources=[dict(title='Official2027 PDF:Beachage5–16/starts/fees/terms',url=EPDF,checked=CHECKED),
                 dict(title='OwnBeachwebpage всёещё2026',url=EN+'barcelona',checked=CHECKED)])
    variants=[]
    for fmt in ['boarding','day']:
        for i,v in enumerate(en_records(beach,'barcelona',fmt,(1395,2495,3895,4895)),1):
            v['variant_key']=fmt+'-'+str(i);variants.append(v)
    beach['timing']['session_details']=variants
    beach['timing']['sessions']=[[v['start'],v['end']] for v in variants]
    beach['price']['extras']+=' Дваchildren2week residential+application EUR5060;dayEUR2470;language-onlyEUR1270. Эторазныепродукты;hotel/flights/extras сверху.'

    for campus,name,place,age,cost,house,programme in [
        ('alicante','Alicante','University of Alicante residence','12–18',(1395,2495,3895,4895),
         'Privatebath double/single(add210/week),airconditioning;3meals/day.', 'Universitycampus,pool/gym,water/sailingoptions.105capacity;broader12–21heading combinesYoungAdults.'),
        ('malaga','Málaga','Residencia Universitaria Teatinos / RUT, Málaga','12–18',(1395,2495,3895,4895),
         'Singlebedroomwithoutfee;each2rooms sharebath,3meals/day. Facilitiesparagraph saysprivatebath butaccommodationclarifiesshared — roomconfirm.', 'Universitydistrict,pool/sport,cultural/beachactivities.210capacity;YoungAdults12–21overalllabel notjunior21.'),
        ('barcelona-centro','Barcelona Centro','The Lofttown residence, Gràcia / Barcelona','14–18',(1395,2495,3895,4895),
         'Single/doubleprivatebath,airconditioning,3meals/day;singleadd350/week.', 'Citycamp/independence,culture/sport,180capacity. Videogamesroom isamenity,notcodingmodule.'),
        ('marbella-centro','Marbella Centro','Marbella Centro · exactcampusaddressconfirm','14–18',(1395,2495,3895,4895),
         'Triple/quadprivatebath,airconditioning,3meals/day;singleadd350/week.', 'City/beach/pool/sport,cultureandteenindependence,180capacity. Destination14–21overallnotkids5–18.'),
        ('valencia','Valencia Beach','Colegio Mayor Galileo Galilei / University of Valencia','12–18',(1195,2095,3295,3995),
         'Tripleroomprivatebath,airconditioning,3meals/day;singleadd210/week.', 'Language/culture/beachandwater/sailing,250capacity;ITlabamenityisnotAIcamp.'),
    ]:
        p=put('enforex-'+campus+'-teen','Enforex '+name+' · Teen Residential','ESP',place,'general,languages,sport','boarding',
            age+' дляInternationalSummerCamps;YoungAdults16–21отдельныйпродуктс50%supervision.',enlang,
            programme,'2027: '+str(len(STARTS[campus]))+' явных1/2weekcohorts(page33). Weeklytariff неозначаетвседаты:CentroимеетJulyтолько2weeks,ValenciaJulyтолько2weeks.',
            en_fee(cost),house,fit('later','Пока9–10, нижеcampminimum.'),fit('later','Пока6–7, нижеcampminimum.'),
            'Будущаявозрастнаяступеньобщихмеждународныхканикул;доступJuniorMadrid/Elviria не переноситсянаэтуdestination.',
            ['Точныеagegroup, language/level,admission,room, specific sports иcurrentinvoice/terms.'],
            [('Own2027 PDF:campus-specific table/body',EPDF),('Campuswebpage,seasoncheck',EN+campus)],
            status='published_2027',sessions=[list(x) for x in STARTS[campus]],confirmed=['EN','ES'],role='language_lessons')
        details(p,EPDF,records=en_records(p,campus,'boarding',cost))
    p=put('enforex-madrid-leadership','Enforex Madrid · Leaders of Tomorrow','ESP','Universidad Francisco de Vitoria / Madrid',
        'entrepreneurship,general,languages','boarding','14–21 отдельногоLeadershipcourse;неjunior5–18camp.',
        'Entrepreneurship&Leadership option allinEnglish по2027PDF. Spanishlessons —альтернативныйвыбор,необязательныйsecondcourseвтойжепрограмме.',
        'Двухнедельныеconferences/workshops,team projects,presentation/leadership. 20lessonsSpanishИЛИEntrepreneurship&Leadership,одновременнооба необещаны.',
        '4–17июля2027,однаконкретнаяLeadershipсмена.',
        fee(2027,'EUR3950/2weeks +application35=3985/person.',
            'Selected20lessons/materials,conferences/workshops,singleroom,3meals/day,sports/activities/excursions,healthinsurance,24hcare.',
            enextra,endep),
        'Single-room universityresidence,отдельныйотjuniorWynwoodcampus;transportquoteдлянего подтвердить.',
        fit('later','Минимум14.'),fit('later','Минимум14.'),
        'БудущаяEnglishentrepreneurshipступень;неcurrentfamilycampи неinternationalawardprogramme.',
        ['Coursechoice/teacherhours,admission, campus/transfer и all-ininvoice/terms.'],
        [('Official2027 Leadershippage32/34',EPDF)],status='published_2027',sessions=[['2027-07-04','2027-07-17']],confirmed=['EN'],role='primary')
    details(p,EPDF)
    for p in profiles:
        if int(p['id'][2:])>=465 or p['slug']=='enforex-barcelona':polish(p)

def extend_report_v85(report):
    report['shortlist'].extend([
        dict(label='Швейцария · Chantemerle для обоих,6–11 лет',slugs=['chantemerle-junior-board','chantemerle-junior-day','chantemerle-junior-halfday'],
             reason='Каталог2027 подтверждает младшую группу6–11. Пансион CHF4950 на ребёнка за2 недели; дневной CHF1600 в неделю; полдня CHF1100. Оба подходят по возрасту, можно выбрать английские уроки. Нужно уточнить конкретный заезд, уровень для уже англоязычных детей, язык остальных занятий и включение CHF800. 3D-печать в перечне занятий не является полным курсом робототехники.'),
        dict(label='Швейцария · короткийEnglishМатвею',slugs=['englishcamp-switzerland-spring','englishcamp-switzerland-summer','alpadia-leysin','alpadia-engelberg'],
             reason='English Camp принимает9–15 лет:18–24 апреля,25 апреля–1 мая,11–17 и18–24 июля2027. Обычная недельная цена для одного Матвея CHF1430 с административным сбором. Alpadia Leysin с8, Engelberg с10 после дня рождения; у них пока сезонные окна без полной базовой цены. Оскар6–7 лет не проходит эти минимумы. Для ребёнка, уже говорящего по-английски, важна польза выбранного языкового уровня.'),
        dict(label='Испания · Enforex обоим,dayилипансион',slugs=['enforex-madrid-board','enforex-madrid-day','enforex-marbella-elviria-board','enforex-marbella-elviria-day','enforex-salamanca-board','enforex-salamanca-day','enforex-barcelona'],
             reason='Каталог2027: Мадрид, Elviria и Саламанка5–18 лет, Barcelona Beach5–16. Английский или испанский,20 уроков по45 минут. Для двоих детей за2 недели с регистрацией: пансион EUR5060 в Мадриде/Beach или4260 в Elviria/Саламанке; дневной EUR2470. Перелёты, жильё родителей и опции сверху. В Elviria младшие живут по6–12 в комнате, в Мадриде/Beach — по двое; готовность к ночёвкам оценивается отдельно.'),
        dict(label='Будущие ступени · English leadership иинженерия',slugs=['chantemerle-leadership','chantemerle-maths-physics','enforex-madrid-leadership','alpadia-paris-passy','alpadia-paris-igny'],
             reason='Будущие ступени: Chantemerle Make It Count с12 лет,18 июля–1 августа; математика/физика с14, две недели внутри окна27 июня–18 июля. Enforex Leadership с14,4–17 июля, EUR3985 с регистрацией. Alpadia в Париже с13: Passy уже2027, Igny ещё2026. Эти программы рассчитаны на более поздний возраст; участие само по себе не даёт международной победы.')
    ])
    report['gaps'].extend([
        dict(country='Швейцария / Франция',iso='CHE',provider='v85 · Alpadia: окно/язык/год договора',
             detail='EnglishLeysin/Engelberg/Passy2027 противFrenchLeysin2026 иbrochure/terms2026; baseprice неотрендерен. Сборenrolmentвключёнвpackage,125/90нельзямеханическидобавлять. 20lessons15h/25lessons18h45m. Openingwindow некаждаянедельнаясмена. IgnyEnglishcourseесть,датыпока2026;Nice/Biarritzпрочитаны,толькоFrenchcourseнеподтверждаетENsupport.',
             next_action='Полныедоговоры2027,точныеcohorts/places/ENcamplifeиall-ininvoice. Nice/Biarritz невключенывподтверждённыйENfamilyshortlist.',url=AL+'en/language-camps/switzerland/leysin'),
        dict(country='Швейцария',iso='CHE',provider='v85 · Chantemerle: младшие/формат/длительность',
             detail='Own2027PDF6–11/12–16,Jun27–Aug1,2–5weeks,4950/6250/7500/8900CHF. Fees1week2800противadvertisedmin2;halfday1100безactivities,day1600. Initial800nonrefundableinclusionнеясно. Maths14–17противcampteen12–16,2weeksavailableJune27–July18не21days;3Dprintingactivityнеroboticsintensive.',
             next_action='Точныйcohort/nightcare/ENcamplifeиуровень,invoice800/sports/insurance,Maths17лет,visitEPFL. Life-skillsfuturecourseнеofficialTEDx/competition.',url=CH+'en/fees/'),
        dict(country='Швейцария',iso='CHE',provider='v85 · EnglishCamp иStGeorge: primarybodyнеравенполнойпроверке',
             detail='EnglishCamp2027age9–15:4weeksдатированы;currentpricepageявно2026&2027сimagefilename2024. Siblingprice1150неразрешаетOscarbelow9. 3/4weektariffбезcohortsнеразмножен. StGeorgeSummerHTML200толькоJSshell;ownbundleсодержит2026defaultsиразныеcampcards. Суммы/agesизdefaultsбезrenderedcampcontentнепринятыкакпроверенная2027программа.',
             next_action='EnglishCampforeignlanguage/admin/transfer/earlydeadline и cancellationboundary;StGeorgerenderedcurrentprogramme/brochure отдельно. Noforms/messages/subscriptions.',url=EC+'infos/preise'),
        dict(country='Испания',iso='ESP',provider='v85 · Enforex: официальный2027 PDF важнеестарогоweb2026',
             detail='Page33визуальнопрочитан:9juniorcampcolumnsсразнымиages/dots. Madrid/Elviria/Salamanca5–18,Beach5–16;Centro14–18,другие12–18. JulyoneweekнетCentro/Valencia;BeachAug15–28двухнедельнаясменанепоказана. Day600/week,course-only300 непансион;application35extra,airport95oneway. Camp-specific850penalty/refund≤2weeksприменяютсяотдельноотgenericterms. YoungAdults50%supervisionнеjunior24hcare.',
             next_action='Конкретноеместо/agegroup/campus/ENилиESadvancedlevel,room/nightcareиfullinvoice/cancellation. Соревнования,выставки,школы/история/маршрутыиоставшиесяприоритетныестранывработе;0полностьюпроверенныхстран.',url=EPDF)
    ])
    for s in report['shortlist'][-4:]:
        s['label']=readable(s['label']);s['reason']=readable(s['reason'])
    for s in report['gaps'][-4:]:
        for k in ['provider','detail','next_action']:s[k]=readable(s[k])
