"""Programme-level primary pass: Americas, winter 2026/27 and summer 2027."""
from datetime import date, timedelta

CHECKED = '2026-10-05'
MUSK = 'https://www.campmuskoka.com/summercamp/2027-dates-rates'
MUSK_EXP = 'https://www.campmuskoka.com/summercamp/the-experience'
WOODS = 'https://muskokawoods.com/'
WOODS_RATES = WOODS + 'rates-and-dates-for-overnight-summer-camp-in-ontario/'
WOODS_FAQ = WOODS + 'frequently-asked-questions/'
WOODS_TERMS = WOODS + 'terms-and-conditions/'
ROBIN = 'https://www.camprobinhood.ca/'
ROBIN_RATES = ROBIN + 'rates-apply/'
ROBIN_IMAGE = ROBIN + 'wp-content/uploads/2027-REG-RATES-Oct-1-819x1024.png'
VGC = 'https://vgc.ca/english-programs-and-schedule/the-camps-junior-program/'
VGC_FAMILY = 'https://vgc.ca/english-programs-and-schedule/family-program/'
VGC_PDF = 'https://vgc.ca/wp-content/uploads/2026-General-Price-Book-FINAL.pdf'
ROBOT = 'https://robot-academy.com/summer-camps-columbus/'
ROBOT_WEST = 'https://robot-academy.com/westerville-summer-robotics-camp-page/'
ROBOT_LEWIS = 'https://robot-academy.com/lewis-center-delaware-camp-page/'
STEM = 'https://www.stem4kids.co/'
STEM_SPRING = STEM + 'camps/robotics?location=cupertino-ca&season=spring-camp-2027#season'
YMCA = 'https://ymcacolombia.org/campamento-en-ingles-para-ninos-y-jovenes/'
YMCA_26 = 'https://experiencias.ymcacolombia.org/InscripcioncampamentosColombia2026'
LINCOLN = 'https://www.lincoln.ed.cr/es/innovacion/campamento-de-verano'


def add_americas_v80(add, src, fit, profiles):
    def put(*args, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1]
        p['checked'] = CHECKED
        for s in p['sources']:
            s['checked'] = CHECKED
        return p

    def fee(year, label, included, extras, deposit):
        return dict(year=year, label=label, included=included, extras=extras, deposit=deposit)

    def variants(p, rows, url, formats, scope):
        for row in rows:
            row.update(source=url, formats=formats, date_scope=scope)
        p['timing'].update(variant_keyed=True, sessions=[[r['start'], r['end']] for r in rows], session_details=rows)

    def weeks(start, n, end_days=6):
        day = date.fromisoformat(start)
        return [[(day+timedelta(days=7*i)).isoformat(), (day+timedelta(days=7*i+end_days)).isoformat()] for i in range(n)]

    en_unknown = 'Язык ведущего и лагерной жизни прямо не установлен прочитанными правилами. Английский сайт не доказывает англоязычное обучение; подтвердить до оплаты.'
    boarding_fit = lambda who: fit('conditional', 'Возрастная категория подходит; готовность к ночёвкам, язык и международный приём подтвердить. ' + who)
    p = put('camp-muskoka-general', 'Camp Muskoka · недельный пансион', 'Канада', 'CAN', 'Muskoka / Ontario',
        'general,sport,art,music,adventure', 'boarding', '6–16; Leadership 14–16 — отдельный продукт.', en_unknown,
        'Общий приключенческий лагерь: выбор из 50+ активностей разного уровня, вода, спорт, творчество, музыка и mountain biking. Feature programs входят; шесть specialty options оплачиваются отдельно. Полноценная робототехника/ИИ не заявлены.',
        'Восемь смен: 4–10 / 11–17 / 18–24 / 25–31 июля; 1–7 / 8–14 / 15–21 / 22–28 августа 2027. Семь дней / шесть ночей.',
        fee(2027, 'CAD 1 695 за неделю плюс налог; одинаковый тариф восьми смен.',
            'Проживание в cabin/cottage, питание, обычная программа и feature activities.',
            'Specialty activities, дорога, страховка и налоги отдельно; полный размер налога и трансфер запросить.',
            'Отмена до/включительно 15 апреля: удержание CAD 150 + HST за ребёнка за неделю. После — без возврата, кроме медицинского случая; по справке 50% пропорционального остатка. Перенос смены без штрафа при наличии места; предоплата на странице не раскрыта.'),
        'Комнаты с кондиционером и внутренними санузлами; заявлены 24/7 healthcare и 4 ребёнка на counselor. Возраст на дату старта уточнить.',
        boarding_fit('Матвею в 2027 будет 9–10.'), boarding_fit('Оскару в 2027 будет 6–7.'),
        'Кандидат на первую общую недельную смену обоим; сравнивать с отдельной технической неделей.',
        ['Подтвердить английский, возрастную дату отсечения, иностранный допуск, сборы specialty, налоги, трансфер, договор и самостоятельность Оскара.'],
        [src('Смены, CAD и отмена 2027', MUSK), src('Активности, включённое и жильё', MUSK_EXP), src('Возраст и сопровождение', 'https://www.campmuskoka.com/')],
        status='published_2027', priority=['both','general','boarding'], sessions=weeks('2027-07-04',8))

    # Explicit birth-year cohorts, not an inferred school grade. Never merge these two operators.
    for slug, provider, page, age, mat, osc, prices, programme in [
        ('muskoka-woods-wild', 'Muskoka Woods · WILD', 'wild-overnight-summer-camp-for-kids-aged-6-8/',
            '6–8; на Summer2027 сайт прямо относит сюда рождение 2019–2021.',
            fit('not_eligible','Матвей 2017 не относится к WILD2027; ему Venture.'),
            fit('conditional','Оскар 2020 относится к опубликованной группе WILD2027. Язык, приём и ночёвки подтвердить.'),
            [1695,1850,1850,1850,1850,1750,1750,1695],
            'Первый пансион: маленькие группы, поддержка при тоске по дому, отдых в середине дня; вода, beginner ropes, творчество и игры. Взрослые ведут группу между активностями.'),
        ('muskoka-woods-venture', 'Muskoka Woods · Venture', 'venture-overnight-summer-camp-for-kids-ages-9-10/',
            '9–10; Summer2027: рождение 2017–2018.',
            fit('conditional','Матвей 2017 относится к опубликованному Venture2027; язык и зачисление подтвердить.'),
            fit('not_eligible','Оскар 2020 не относится к Venture2027; ему WILD.'),
            [1995,2300,2300,2300,2300,2200,2200,1995],
            'Общий outdoor пансион с большей самостоятельностью: вода, ropes, искусство, вечерние игры. Venture Quest Card — ежедневные задания про дружбу, активность и ответственность, не международное соревнование.'),
    ]:
        p = put(slug,provider,'Канада','CAN','4585 Highway 141, Rosseau, Ontario P0C 1J0',
            'general,sport,art,adventure','boarding',age,en_unknown,programme,
            'Восемь недель 4 июля – 28 августа 2027, воскресенье–суббота. Classic 29 августа – 3 сентября только 13–16, не эти программы.',
            fee(2027, '$'+str(min(prices))+'–'+str(max(prices))+' / неделя + HST. Тариф каждой недели ниже; ISO валюты на прочитанном прайсе не указан, подтвердить CAD.',
                'Питание, жильё, 16–18 активностей, вечерние программы и персонал.',
                'One-way coach $195, Pearson airport service $700, laundry $60 при нескольких неделях; опции slide $70 / combo $110 / laser tag $80, всё + HST. FAQ рекомендует store budget $70–90. Страховка/медицинские расходы иностранца отдельно.',
                'Невозвратный аванс $400/ребёнок/неделя; остаток 15.04.2027. До 15 апреля удерживается аванс; после и за 30+ дней — 50%, менее 30 дней — 100%; медицинские исключения по договору. Отмена транспорта: FAQ 14 дней против договора 15 — подтвердить.'),
            'Пансион с кондиционером/HEPA. Христианская youth-организация, принимает разные вероисповедания: WILD/Venture участвуют в Cabin Chat. Международному гостю нужен местный взрослый, способный забрать ребёнка за 6 часов; equivalent medical insurance обязательна.',
            mat,osc,'Можно выбрать одну неделю обоим, но группы/тарифы разные. Язык пока не подтверждён; ночёвки не заменяют STEM курс.',
            ['Подтвердить язык, валюту/HST, наличие мест и готовность к ночёвкам; предусмотреть взрослого для забора за 6 часов. Братьев не обещают поселить вместе.'],
            [src('Конкретная возрастная программа',WOODS+page), src('Годы рождения 2027',WOODS), src('Тарифы, опции и смены',WOODS_RATES),src('FAQ / Cabin Chat',WOODS_FAQ),src('Договор 2027 / международные гости',WOODS_TERMS)],
            status='published_2027',priority=['general','boarding'])
        variants(p,[dict(variant_key='week-'+str(i+1),start=a,end=b,label='Неделя '+str(i+1),price='$'+str(prices[i])+' + HST; валюту подтвердить',place=p['place']) for i,(a,b) in enumerate(weeks('2027-07-04',8))],WOODS_RATES,['boarding'],'camp_session')

    robin_fee = fee(2027, '$1 855 / 2 недели; короткая Session3 $1 680 / 9 учебных дней. 2/3/4 sessions: $3 195 /4 430 /5 375. Это early для новых семей при записи 1–31.10.2026; валюту подтвердить.',
        'Занятия, футболка, backpack, cabin photo, towel service, угощение/сок; pizza lunch только по пятницам.',
        'Neighbourhood bus $190 или door-to-door $280/ребёнок/session + HST. Дневной camp fee HST exempt. Второму ребёнку 5% на лагерь и транспорт; полноценный обед остальных дней/страховку/жильё семьи уточнить.',
        '$500 аванс/ребёнок; остаток равными платежами 1 марта/1 апреля/1 мая. Oct/Nov отмена $0; Dec/Jan $250; Feb/Mar $500; April/May 50%; после 1 июня возврата нет. Условия сокращения отличаются; карта +2,4%.')
    p = put('robin-hood-day', 'Camp Robin Hood Canada · Day Camp', 'Канада','CAN','10243 Reesor Road, Markham, Ontario L6B 1A8',
        'general,sport,art,adventure','day','С 4 лет на первый день; FAQ 4–12, до завершённого Grade7; верхнюю возрастную границу уточнить.',en_unknown,
        'Общий дневной outdoor лагерь с плаванием и творчеством. Группы по завершённому классу, минимум два counselor на cabin. Sports Academy — отдельный выбор; не смешивать с одноимённым американским пансионом.',
        '2027: 5–16 июля, 19–30 июля, 3–13 августа (9 учебных дней), 16–27 августа. Таблица цен — изображение оператора, визуально прочитано. Приём заявок с 1 октября; наличие мест не доказано.',
        robin_fee,'Дневной формат; проживание семьи отдельно. Братья разного класса могут быть в разных cabin.',
        fit('conditional','Возраст подходит; определить завершённый класс, язык и внешний приём.'),fit('conditional','Возраст подходит; определить завершённый класс, язык и внешний приём.'),
        'Общий летний кандидат обоим с реальными сменами и текущим октябрьским early прайсом.',
        ['Подтвердить ISO валюты, English, внешний приём, конечную группу/смету, обычный обед и отличие табличных/обычных цен после 31 октября.'],
        [src('Смены и текущие условия',ROBIN_RATES),src('Изображение прайса2027',ROBIN_IMAGE),src('Возраст и оплата/возврат',ROBIN+'apply_now/'),src('FAQ',ROBIN+'faq/')],
        status='published_2027',priority=['both','general'],sessions=[['2027-07-05','2027-07-16'],['2027-07-19','2027-07-30'],['2027-08-03','2027-08-13'],['2027-08-16','2027-08-27']])
    p = put('robin-hood-home-away', 'Robin Hood / Camp Walden · Home & Away', 'Канада','CAN','Markham / Camp Walden, Ontario',
        'general,sport,adventure','day,boarding','Только завершённые Grades2–4.',en_unknown,
        'Комбинация дневного Robin Hood и трёх ночей Walden: Tue–Thu дневной лагерь, Fri–Mon Walden, затем Tue–Fri дневной. Первый пробный пансион; полная робототехника не заявлена.',
        'Только Session3: 3–13 августа 2027. Ночная часть 6–9 августа следует из опубликованного недельного расписания; время/переезд нужно подтвердить.',
        fee(2027,'$2 625 при записи до 31.10.2026; с 1 ноября $2 725. Валюту и применимость HST подтвердить.',
            'Трёхночная часть и дневной лагерь заявлены как единая программа; точный пакет еды/перевозки запросить.',
            'Семейное жильё для дневной части, дорога и страховка отдельно; bus и sibling discount конкретного пакета уточнить.',
            'Общие правила Robin Hood не объясняют все расходы Walden; нужен договор конкретного hybrid пакета, сроки оплаты и отмены.'),
        'Три ночи отдельно от родителей плюс дневные дни. Место ночёвок и передача ребёнка между площадками должны быть подтверждены.',
        fit('conditional','Подходит только при завершённом Grade2,3 или4; рождение2017 не доказывает класс.'),fit('later','Завершённые Grades2–4 выше вероятного класса Оскара; возрастное исключение не заявлено.'),
        'Промежуточный путь Матвея к пансиону; Оскару — обычный Day Camp, если допуск подтверждён.',
        ['Проверить реальный завершённый класс, язык обеих площадок, точный ночной график, транспорт и отдельный договор.'],
        [src('Home & Away2027 / классы и стоимость',ROBIN_RATES),src('Общие правила, не отдельный hybrid-договор',ROBIN+'apply_now/')],
        status='published_2027',priority=['general','boarding'],sessions=[['2027-08-03','2027-08-13']])

    p = put('vgc-junior-family', 'VGC · Junior Camp с взрослым / Family option', 'Канада','CAN','Vancouver · зимой Downtown; летний школьный кампус уточнить',
        'general,languages,art,sport','day,family','Junior9–12; взрослый обязателен для приезжающего Junior. Family adult stream30+; Teen13–17 отдельно.',
        'Прямо объявлена English-only среда и международные ученики; не технический лагерь.',
        'Английский, практическое применение языка, культура/активности; Junior25 часов/нед., 09:00–15:30 Mon–Fri. Adult17 часов и отдельные уроки. Для уже свободно говорящего Матвея проверить пользу уровня.',
        'Winter2027: 4 января–5 февраля, старты4/11/18/25 января. Summer2027: 5 июля–6 августа, старты5/12/19/26 июля. Минимум2, максимум5 недель; это два окна сезона, не две непрерывные поездки/ICS.',
        fee(2027,'Junior2/3/4/5 недель: CAD2 845 /4 080 /5 315 /6 550 без homestay; CAD4 585 /6 270 /7 955 /9 640 с homestay. Summer/Winter2027 одинаковы по страницам8–9 PDF. Семейный тариф по запросу.',
            'Учёба, registration/material/activity/facility fees и medical insurance Junior; homestay-пакет также full board, placement, custodian letter и оба airport transfers.',
            'Взрослый не включён: его2–5 недель CAD2 135–4 775 без жилья /3 625–7 465 с homestay. Optional afternoon/weekend activities дополнительно; extra transfer CAD150/person/way, extra homestay night100. Family suite/Оскар без Junior допуска — отдельный расчёт.',
            'Включённые registration CAD200, homestay placement390 и custodian150 названы non-refundable. Полный договор/отмена и комплект ночей ещё не проверены; из названия файла2026 не выводить старый тариф — внутри обе страницы2027.'),
        'Homestay с сопровождающим взрослым, три приёма пищи; Family homestay рассчитан на adult+child, квартира отдельно. Это не самостоятельный детский пансион. Unaccompanied-minor fee из общей таблицы не отменяет обязательного взрослого Junior.',
        fit('conditional','9–10 в2027 подходит, но ехать только с взрослым. Для свободного English оценить сложность/пользу.'),fit('later','6–7 ниже Junior9. Наличие семейного пакета не доказывает учебную программу Оскару.'),
        'Проверенный английский семейный маршрут Матвею на зиму/лето2027; не подходит как лагерь обоим без отдельного решения для Оскара.',
        ['Подтвердить дату возраста, уровень, взрослый пакет, точный campus, число ночей/даты заселения, optional активности, договор и занятия Оскару.'],
        [src('Junior: English-only и обязательный взрослый',VGC),src('Family: даты/условия жилья',VGC_FAMILY),src('Прайс PDF: страницы8–9 действительно2027',VGC_PDF),src('Страница прайса названа2026', 'https://vgc.ca/price-list/')],
        status='published_2027',priority=['general'],confirmed=['EN'],sessions=[['2027-01-04','2027-02-05'],['2027-07-05','2027-08-06']])
    p['language_evidence_role']='primary'
    p['timing']['precision']='season_window'

    p = put('robot-academy-full-day', 'Robot Academy · LEGO Robot & 3D Printing', 'США','USA','Westerville / Powell–Lewis Center–Delaware, Ohio · точный campus уточнить',
        'robotics,coding,engineering,art','day','Раздельные группы4–7 и8–13; beginner и advanced задания.',en_unknown,
        'Утром CAD/3D детали и LEGO challenges, затем собственная сборка/код с моторами и сенсорами. 3D работы домой; Take-Home Robot опционален. Медали лагерных игр не являются наградой мировой лиги.',
        'Главный календарь2027: Westerville21–25 июня; Powell/Lewis Center/Delaware12–16 июля. Общий список имеет и другие места, но их конкретный full-day продукт здесь не утверждается.',
        fee(None,'Полный тариф2027 и доплата Take-Home Robot в прочитанных страницах не раскрыты. $10 — advertised initial deposit, не стоимость лагеря.',
            'Supervised lunch/recess при полном дне или сочетании AM+PM; воду и обед приносить. 3D работы домой.',
            'Стоимость робота, total tuition, налоги, страховку и поездку семьи уточнить.',
            'Бесплатный перенос до начала при наличии места. 100% возврат в течение4 недель после регистрации; позже credit/reschedule. В день старта/no-show credit нет. Срок после регистрации отличается от срока до смены.'),
        'Дневной формат. Lewis AM09:30–12:30, PM13:30–16:30, полный09:30–16:30; Westerville часы уточнить. Заявлен teacher:student1:6.',
        fit('conditional','Матвей9–10 подходит8–13; сложности/английский и внешний приём проверить.'),fit('conditional','Оскар6–7 подходит4–7; самостоятельность чтения и язык проверить.'),
        'Технический кандидат обоим с разными заданиями; собственные обещания чемпионских coach не считаем независимым школьным рейтингом.',
        ['Уточнить exact venue/time, текущий полный прайс, английский, иностранный приём и комплект домой.'],
        [src('Летний календарь2027 / группы / отмена',ROBOT),src('Westerville: подробная full-day программа',ROBOT_WEST),src('Lewis: часы/содержание/robot option',ROBOT_LEWIS)],
        status='published_2027',priority=['technical','both'])
    variants(p,[dict(variant_key='westerville',start='2027-06-21',end='2027-06-25',label='Westerville · full-day programme подтвердить',place='Westerville, Ohio',price='Тариф2027 ещё не установлен'),dict(variant_key='lewis-center',start='2027-07-12',end='2027-07-16',label='Powell/Lewis Center/Delaware · место уточнить',place='Powell / Lewis Center / Delaware, Ohio',price='Тариф2027 ещё не установлен')],ROBOT,['day'],'day_camp_window')

    # Every dated campus/course variant appears in its own public product table.
    for slug, title, path, age, programme, mat, osc, n in [
        ('stem4-builders','LEGO Robotics · Builders','lego-robotics-builders','6–9',
            'SPIKE Essential, icon blocks: моторы, передачи, color/distance sensors, две сборки/день. Уровень подбирают по опыту; пятничная демонстрация семьям.',
            fit('conditional','Весной2027 Матвею9–10: только до выхода из6–9; дата отсечения неизвестна. Старшие альтернативы Challengers/Engineers.'),fit('conditional','Оскар6–7 подходит. Проверить фактическое чтение, язык и самостоятельность.'),10),
        ('stem4-challengers','LEGO Robotics · Challengers','lego-robotics-challengers','9–14',
            'SPIKE Prime + Expansion Set: семь уроков про точное движение, механизмы, линии/сенсоры и FLL-style миссии. Loops/conditionals/variables, debugging; локальные финальные robot challenges.',
            fit('conditional','Матвей9–10 подходит; для трёхлетнего опыта просить advanced задания.'),fit('later','До9 лет выбранный Challengers не подходит.'),9),
        ('stem4-engineers','VEX Robotics · Engineers','vex-robotics-engineers','9–13',
            'VEX IQ, intake/lifts/gearboxes, Distance/Bumper/Optical/Gyro, автономные программы и alliance challenge. Команды2–4, равное driving time; это подготовка, не отбор в VEX Worlds.',
            fit('conditional','Матвей9–10 подходит; спросить продвинутый проект и сезонную команду.'),fit('later','До9 лет Engineers не подходит.'),9),
        ('stem4-rookies','VEX Robotics · Rookies','vex-robotics-rookies','7–9',
            'VEX GO/VEXcode GO: собрать, управлять и программировать; передачи/моторы/сенсоры/attachments. Дети работают парами; дальше отдельный IQ курс Engineers.',
            fit('conditional','Матвей только пока9; advanced содержание и возраст на старт подтвердить.'),fit('conditional','Оскар2020 только после7-летия. До дня рождения7 порог не выполнен; исключение не заявлено.'),9),
    ]:
        url=STEM+'camps/'+path
        p=put(slug,'STEM4Kids · '+title,'США','USA','Cupertino / San José–Los Gatos, California',
            'robotics,coding,engineering','day',age,en_unknown,programme,
            'Spring2027:12–16 апреля только Cupertino. Summer2027: weekly starts7 июня–'+('9 августа' if n==10 else '2 августа')+', две площадки. В таблице одновременно Open и Opens Nov1; бронирование/места не проверены.',
            fee(2027,'$524 regular/$474 early до1 марта за full week; half-day$374/$324. Single full day$120; ISO валюты/налоги подтвердить.',
                'Общие kits/materials и присмотр. Робот/комплект остаётся в лагере; результат — программа, фото/демонстрация.',
                'Обед и два snacks с собой или optional hot lunch. Extended care от$65/нед.,08:30–09:00/16:00–18:00. 2–3 недели скидка$50;4–6$120;7+$250/ребёнок, sibling$20; порядок применения/налоги уточнить.',
                'Полная оплата при бронировании, аванса нет. Summer: до10 мая удержание$25/нед.; после за3+недели —25%, менее3 недель —без возврата. Spring: до31 марта$25/нед., после возврата нет. Отмена оператора — полный возврат; перенос при местах бесплатный.'),
            'Дневной09–16 Mon–Fri; half09–12/13–16. До14 детей на преподавателя. Cupertino:20900 Stevens Creek Blvd; San José:15040 Union Ave. Общая programme page не заменяет договор.',
            mat,osc,'Выбирать по конкретной платформе и возрасту; опубликованные недели полезны для семейной технической поездки, язык ещё проверить.',
            ['Подтвердить возраст на старт, английский, иностранный приём, статус записи с1 ноября, ISO валюты/налоги, holidays, продвинутый уровень и полный счёт.'],
            [src('Конкретный курс / расписание / возраст',url),src('Весна2027: четыре курса, даты и прайс',STEM_SPRING),src('Полная оплата и отмена',STEM+'policies'),src('Оборудование, обед и формат',STEM+'faq')],
            status='published_2027',priority=['technical'])
        rows=[dict(variant_key='cupertino-spring',start='2027-04-12',end='2027-04-16',label='Spring · Cupertino',place='20900 Stevens Creek Blvd, Cupertino, CA95014',price='$474 early/$524 regular; ISO/налоги подтвердить')]
        for i,(a,b) in enumerate(weeks('2027-06-07',n,4)):
            for key,place in [('cupertino','20900 Stevens Creek Blvd, Cupertino, CA95014'),('san-jose','15040 Union Ave, San Jose, CA95124')]:
                rows.append(dict(variant_key=key+'-week-'+str(i+1),start=a,end=b,label='Summer · '+key+' · неделя'+str(i+1),place=place,price='$474 early/$524 regular; ISO/налоги подтвердить'))
        variants(p,rows,url,['day'],'day_camp_window')
        p['availability']=dict(status='unknown',label='Таблица одновременно Open / Opens Nov1; фактическое зачисление и свободные места не проверены.')

    p=put('ymca-colombia-ycamp','YMCA Colombia · YCAMP Junior','Колумбия','COL','YMCA Campamento Bochica, Santandercito / Cundinamarca',
        'general,languages,sport,art,science,leadership','boarding','YCAMP8–13; YTAC14–17 отдельно. Общая booking page8–17 не отменяет младшую группу.',
        'Прямо заявлено100% English immersion по уровням и английский каждой активности. Не доказан отдельный STEM на испанском.',
        'Шесть дней/пять ночей: спорт, театр, музыка, творчество, природа и научные challenges; самостоятельность и лидерство. Программируемый robotics/AI курс не заявлен.',
        'Ближайшая полная смена29 ноября–4 декабря2026. October4–9 уже началась5 октября; возможность позднего входа не доказана. Summer2027 только лист уведомления, дат ещё нет. Старый список LaVega отличается от текущих площадок.',
        fee(2026,'COP1 950 000 /6 дней5 ночей, без повышения к2025; абон отCOP300 000. Это цена2026, не2027.',
            'Многоместное проживание с индивидуальной кроватью,3 приёма пищи2 snacks/день, kit/materials/activities, insurance и transport от установленной встречи туда-обратно.',
            'Перелёт/дорога до встречи, страховые условия и возможный языковой placement уточнить; семейное проживание не включено.',
            'Минимальный платёж300 000. Programme policy упомянута, её текст в прочитанном landing не доступен; конкретный возврат/невозвратность абона не установлены. Запросить договор.'),
        'Проживание с круглосуточным сопровождением, заявлены медицинская/сестринская помощь. Контакт с ребёнком по лагерному режиму, не свободные звонки; иностранный детский приём уточнить.',
        fit('conditional','Матвей8–9 в2026 подходитYCAMP8–13; английский среда подтверждена, зачисление и готовность к5 ночам отдельно.'),fit('later','Оскару5–6; до8 лет YCAMP не подходит.'),
        'Ближайший общий английский пансион в Латинской Америке для Матвея, с конкретной площадкой/ценой. Оскару нужен другой формат.',
        ['Подтвердить международный приём, место/часы встречи, языковую сложность, договор отмены, страховой пакет и свободные места.'],
        [src('YCAMP/ YTAC / питание / транспорт',YMCA),src('Текущий сезон2026, COP и английский',YMCA_26)],
        status='published_2026',priority=['general','boarding'],confirmed=['EN'],sessions=[['2026-11-29','2026-12-04']])
    p['language_evidence_role']='camp_life'

    p=put('lincoln-epic-archive','Lincoln School · Ingenious Lab / EPIC','Коста-Рика','CRI','Lincoln Innovation Center, Costa Rica',
        'entrepreneurship,general,technology','day','Только Grades8–12; это не младший детский лагерь.',
        'Оператор прямо называет испанский и английский; долю занятий/потоки уточнить.',
        'Архивный двухнедельный предпринимательский курс: создание продукта/услуги, общественная польза и экономическая ценность, университетские innovation visits, встречи с экспертами, final pitch предпринимателям.',
        '5–16 января2026 уже прошли. Новая смена/прайс2027 не объявлены в прочитанном первичном источнике; будущие календарные даты не создаём.',
        fee(2026,'$570 архив2026, налоги включены; ISO валюты подтвердить. Новая цена2027 неизвестна.',
            'Материалы, футболка и snacks по архивному объявлению.',
            'Обед, транспорт, посещения, страховка и жильё семьи отдельно проверить для нового сезона.',
            'Аванс/отмена/приём зарубежных школьников не установлены.'),
        'Дневной innovation center; пансион не заявлен. Будущая старшая ступень, не предложение детям6/9 сегодня.',
        fit('later','ДоGrade8 ещё рано; сохранить как будущий local entrepreneurship маршрут.'),fit('later','ДоGrade8 ещё рано; младший вариант не объявлен.'),
        'Полезный будущий предпринимательский ориентир на постоянной базе; архив не превращаем в доступный лагерь2027.',
        ['Ждать нового сезона, младших вариантов, языковых часов, exact campus и полного прайса; сейчас не подавать как подходящее6/9.'],
        [src('EPIC: классы, языки, архивный прайс',LINCOLN)],status='next_unannounced',confirmed=['ES','EN'])
    p['language_evidence_role']='bilingual'


def extend_report_v80(report):
    report['shortlist'].extend([
        dict(label='Канада 2027 · одна поездка, разные возрастные группы',slugs=['camp-muskoka-general','muskoka-woods-wild','muskoka-woods-venture','robin-hood-day','robin-hood-home-away'],reason='Camp Muskoka и Muskoka Woods — разные операторы. Woods относит Оскара 2020 в WILD, Матвея 2017 в Venture, но язык ещё подтвердить; нужен взрослый в шести часах для экстренного забора. Robin Hood — дневной вариант обоим; три ночи Walden только при завершённом Grade 2–4.'),
        dict(label='Калифорния 2027 · платформы и два кампуса',slugs=['stem4-builders','stem4-challengers','stem4-engineers','stem4-rookies'],reason='SPIKE Essential 6–9 / Prime 9–14 / VEX GO 7–9 / IQ 9–13. Оскар до семилетия — только Builders; Матвей после десятилетия — Challengers или Engineers. Весенние и летние недели опубликованы; запись с 1 ноября и язык требуют подтверждения. Робот домой не включён.'),
        dict(label='Ближайшая Латинская Америка · английский пансион Матвею',slugs=['ymca-colombia-ycamp','liota-winter','cloud-forest','lincoln-epic-archive'],reason='YMCA 29.11–04.12.2026: 8–13, COP 1 950 000, английский 100%, пять ночей. Оскару до восьми лет не подходит. Liota: 19 календарных дней названы четырьмя неделями, зимний возраст и язык неизвестны. Cloud Forest — локальные научные дневные смены; Lincoln только Grades 8–12, архив 2026.'),
        dict(label='Северная Америка · семейная языковая и техническая поездка',slugs=['vgc-junior-family','robot-academy-full-day','id-tech','integem-junior','integem-young'],reason='VGC Junior 9–12 только с взрослым; семейная цена отдельно и у Оскара нет Junior допуска. PDF с 2026 в названии содержит прайсы Winter/Summer 2027. Robot Academy: группы 4–7 / 8–13; полную смету, язык и точную площадку ещё получить. Внутренние медали не мировые победы.'),
    ])
    report['gaps'].extend([
        dict(country='Канада',iso='CAN',provider='v80: первичный прайс и условия 2027',detail='Muskoka Woods: WILD 2019–21 / Venture 2017–18; язык не подтверждён. Международному ребёнку обязателен взрослый, забирающий за шесть часов. Проверить HST, ISO валюты и 14 против 15 дней отмены транспорта. Robin Hood: изображение прайса 2027 содержит 1855/1680; текущий bus 280/190 против старых 265/180 в поиске. Early до 31 октября — не крайний срок приёма.',next_action='Подтвердить язык, валюту/налог, внешний допуск, готовность Оскара и итоговый счёт. Остальные запрошенные страны остаются в работе.',url=WOODS_TERMS),
        dict(country='США',iso='USA',provider='v80: STEM4Kids / Robot Academy',detail='78 вариантов курса/кампуса STEM4Kids 2027, а не 78 операторов. Таблица Open / Opens Nov1 не доказывает свободное место. Учебные платформы, возраст и комплект в лагере подтверждены; язык неизвестен. Robot Academy: календарь 2027 при некоторых ссылках регистрации 2026, полная цена неизвестна. Лагерные награды не являются мировыми победами.',next_action='Проверить договор, язык/возраст, цену/оборудование/праздники, конкретную площадку и задания опытным детям; продолжать остальные USA/CAN программы.',url=STEM+'camps/robotics'),
        dict(country='Канада',iso='CAN',provider='v80: VGC 2027 внутри PDF 2026',detail='Визуально прочитаны страницы 8–9: Summer/Winter 2027; Junior CAD 2845–6550 без жилья / 4585–9640 homestay. Это индивидуальные тарифы; семейный расчёт отдельно. Junior 9–12 обязательно с взрослым; unaccompanied-minor fee не исключение. Окна сезона и еженедельные старты не превращены в непрерывную смену.',next_action='Проверить пользу языка для свободного английского, даты ночей/заезда, семейное жильё/прайс, договор и детскую программу Оскару.',url=VGC_PDF),
        dict(country='Коста-Рика / Мексика / Колумбия',iso='CRI',provider='v80: будущие даты и настоящий адрес',detail='YMCA FinAño 2026 проходит в Bochica/Santandercito; старый общий список La Vega не текущая площадка. COP и 100% EN указаны прямо; Summer 2027 пока лист уведомления. Lincoln EPIC января 2026 только Grades 8–12. Liota Winter: 17 декабря–4 января против четырёх недель; летний FAQ не доказывает зимний допуск. Camp Hope — поездка команды волонтёров; Heredia января 2026 — архив.',next_action='Найти новые зимние младшие смены CRI/MEX, прочитать договор YMCA и цены новых LATAM сезонов. Формы, сообщения и платежи не отправляли.',url=YMCA_26),
    ])
