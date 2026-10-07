"""Selected Americas curricula; exact seasons, family stays and admission gates."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='eaef81b781f5be93ff1a177f5c2bfb235dc2a89d'
CHECKED='2026-10-06'
F='https://frostvalley.org/'
FT=F+'camps/traditional-overnight-camps/'
FD=F+'camps/day-camps/'
FF=F+'family-weekends/'
FL=F+'wp-content/uploads/2026/04/2026-27-GFR-Lodge-Participant-Rates_04-08-2026.pdf'
FW=F+'wp-content/uploads/2026/09/2026-27-Winter-Family-Camp-Rates-Sheet_09-16-2026.pdf'
FH='http://frostvalley.org/wp-content/uploads/2026/06/2026-Summer-Camp-Family-Handbook_06-17-2026_v2.pdf'
EX='https://exploracamp.com/'
CR='https://www.coderevkids.com/'
NEW=['inned-winter','frost-wawayanda','frost-sugarloaf','frost-farm-board','frost-seedlings',
     'frost-durango','frost-pathfinders','frost-lego-day','frost-inventors-day',
     'frost-family-weekends','frost-family-farm','frost-winter-family',
     'explora-kids','explora-xtreme','explora-parent-child',
     'coderev-minecraft','coderev-roblox','coderev-revrobots','cisv-mexico-village-route']
UPDATED=['envision-winter-audit']
OVERNIGHT=[['2027-06-27','2027-07-09'],['2027-07-11','2027-07-23'],
           ['2027-07-25','2027-08-06'],['2027-08-08','2027-08-20']]
DAYS=[['2027-06-28','2027-07-02'],['2027-07-05','2027-07-09'],['2027-07-12','2027-07-16'],
      ['2027-07-19','2027-07-23'],['2027-07-26','2027-07-30'],['2027-08-02','2027-08-06'],
      ['2027-08-09','2027-08-13'],['2027-08-16','2027-08-20']]
FAMILY=[('2026-10-09','2026-10-12','Indigenous Peoples: природа и культурная программа'),
        ('2026-10-16','2026-10-18','Halloween I'),('2026-10-23','2026-10-25','Halloween II'),
        ('2026-10-30','2026-11-01','Halloween III'),('2026-11-06','2026-11-08','Fall Family I'),
        ('2026-11-13','2026-11-15','Fall Family II'),('2026-12-04','2026-12-06','Winter Makers: подарки, глина, печать'),
        ('2027-01-15','2027-01-18','MLK: зимняя природа, возможен выбор двух/трёх ночей'),
        ('2027-02-12','2027-02-15','Presidents: зимний семейный заезд'),
        ('2027-03-19','2027-03-21','Maple Fest: как собирают сок и варят сироп'),
        ('2027-04-16','2027-04-18','Legends & Labyrinths: настольные истории'),
        ('2027-04-23','2027-04-25','Earth Day: экология, вода и геология'),
        ('2027-05-07','2027-05-09','Fine Arts / Mother’s Day'),
        ('2027-05-21','2027-05-23','Spring Family'),('2027-05-28','2027-05-31','Memorial: обсерватория, искусство и природа'),
        ('2027-06-04','2027-06-06','LGBTQ+ Family: открытый семейный заезд'),
        ('2027-06-11','2027-06-13','Father’s Day')]
LANG='EN/ES/RU ведущего в прочитанных материалах прямо не установлен. Язык сайта не подтверждает язык всех занятий.'
OREF=('Прайс 2027: депозит $250 для фиксации места, не возвращают; остаток до 1 марта. Отмена до 1 марта — tuition минус депозит; '
      'после 1 марта — 70% возвращаемой части tuition минус депозит; после 1 июня и при раннем отъезде возврата нет. '
      'Регистрационные сборы не возвращают. Перенос после 1 марта $50. Не подменять правилами дневных или семейных программ.')
OEX=('Дополнительно 5% registration fee от tuition; депозит $250 не складывается автоматически как ещё одна цена обучения. '
     'Bus, holdover, дорога семьи, страховка и иные выбранные опции отдельно. $ по контексту США, валюту счёта подтвердить.')
DPRICE=dict(year=2026,label='Прайс пока 2026: обычная неделя Tier A/B/C $485/400/315; specialty $495/410/325. Цена 2027 не подтверждена.',
    included='Архивный тариф занятий; по FAQ 2026 перекусы включены, обед приносит семья.',
    extras='Tier D $250/$260 только ученикам пяти перечисленных местных округов; приезжей семье не назначен. Bus $125/смена — тоже 2026. Жильё и дорога отдельно.',
    deposit='Архив 2026: депозит $50, остаток до 1 мая, после 1 мая возврата нет; это не подтверждённый договор 2027. Нужны новая цена, питание/аллергены, foreign admission и часы выдачи.')

def add_americas_v126(add,src,fit,profiles):
    countries={'USA':'США','CAN':'Канада','MEX':'Мексика'}
    grade=fit('unknown','В программе важен фактический класс на начало смены; год рождения не доказывает школьную категорию. Также подтвердить язык и приём приезжей семьи.')
    conditional=fit('conditional','По заявленному возрастному диапазону кандидат; нужны конкретная группа, язык, наличие места и условия для приезжей семьи.')
    later=fit('later','Возраст детей пока ниже этого маршрута; сохранено как будущая ступень.')
    family=fit('conditional','Заезд вместе с родителем; отдельное отправление ребёнка сюда не предусмотрено. Язык занятий, место и тариф по фактическому возрасту подтвердить.')
    def emit(i,name,iso,place,themes,formats,age,programme,price,housing,mf,of,why,
             sources,status='next_unannounced',label='Следующая конкретная смена 2026–27 не подтверждена.',sessions=None,language=LANG,confirmed=None):
        add(NEW[i],name,countries[iso],iso,place,themes,formats,age,language,programme,label,price,housing,mf,of,why,
            ['Подтвердить язык ведущего, возраст/класс, внешний приём, доступные места и полный счёт выбранной смены. Заявки и оплаты не выполнялись.'],
            sources,status=status,confirmed=confirmed,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        return p
    def dated(p,url,labels=None,scope='camp_session',variants=None):
        p['timing']['session_details']=[]
        for i,(a,b) in enumerate(p['timing']['sessions']):
            v=dict(start=a,end=b,label=labels[i] if labels else 'Опубликованная смена',place=p['place'],price=p['price']['label'],source=url,
                date_scope=scope,date_precision='published_session',proof='Даты прямо опубликованы оператором. Место, язык и личный допуск проверяются отдельно.')
            if variants:v.update(variants[i])
            p['timing']['session_details'].append(v)
    p=emit(0,'InnEd Academy × Young Engineers · Winter STEM','CAN','LOL Playlab, Whitchurch-Stouffville, Ontario',
        'robotics,coding,science,technology','day','5–12, JK – Grade 6; группы по возрасту',
        'Утром математические игры и задачи, затем движение в LOL Playlab; после обеда робототехника, код и моторизованные модели Young Engineers. '
        'Самолёт с пропеллером, ровер, ракета, кран/захват — примеры возможных сборок: набор меняется по группе и блоку, все четыре не обещаны. Новичков и внешних учеников принимают.',
        dict(year=2026,label='$240 за трёхдневный блок; оба блока $450 за одного ребёнка. Для двоих $480/один блок или $900/оба по опубликованной арифметике, валюта счёта не указана прямо.',
             included='Занятия и доступ к площадке по описанию; состав расходных материалов и обед подтвердить.',extras='Скидка $30 за шесть дней одного ребёнка, не скидка второму брату. $ по контексту Ontario; не конвертируем как подтверждённый CAD.',
             deposit='Enrollment Agreement регулирует конкретные услуги и оплату; общие monthly-class makeup/termination правила не считаем договором winter camp. Взрослый оформляет участие, отдельный waiver LOL Playlab обязателен.'),
        '09–16, только понедельник–среда; пансиона нет.',conditional,conditional,
        'Ближайшая компактная проба реальной инженерной дневной программы для обоих после подтверждения языка.',
        [src('Зимние блоки 2026, модели, цены и открытый приём','https://inned.ca/camps/'),src('Договорная иерархия и waiver','https://inned.ca/terms-of-use/')],
        status='published_2026',label='21–23 и 28–30 декабря 2026; два отдельных блока по три дня, 09–16.',sessions=[['2026-12-21','2026-12-23'],['2026-12-28','2026-12-30']]);dated(p,'https://inned.ca/camps/')
    osources=[src('Программы, школьные ступени и размещение',FT),src('Точные заезды, тарифы и отмена 2027',FT+'fees/'),
              src('Кабины, staff и медицинская помощь',FT+'faq/'),src('Архивный handbook 2026: устройства и связь, не договор 2027',FH)]
    def boardprice(a,b,c):return dict(year=2027,label=f'Tier A/B/C ${a}/{b}/{c} за ребёнка/смену + 5% registration fee. Добровольные субсидированные tiers дают ту же программу; минимальный tier не назначен семье автоматически.',
        included='Пансион, питание и выбранная программа по описанию оператора; точный пакет подтвердить.',extras=OEX,deposit=OREF)
    ohousing=('Отдельный детский пансион, родители не живут с ребёнком. Оператор описывает медперсонал и группы с вожатыми; конкретную ночную схему и международный приём подтвердить. '
              'Handbook 2026 ограничивает электронику/Yondr; unlimited детский телефон не обещан, правила 2027 ещё нужны.')
    p=emit(1,'Frost Valley YMCA · Wawayanda two-week','USA','Main Camp, Claryville, Catskills, New York','general,sport,art,science','boarding',
        'Entering Grades 2–7, класс после летних каникул',
        'Общий пансион: природа, водные активности, спорт, ремёсла, группы по школьным ступеням и самостоятельность. Это не гарантированный курс программируемых роботов. '
        'Кабины с электричеством, отоплением и санузлами; сайт описывает разные staff ratios, не универсальную персональную гарантию 1:4.',
        boardprice(3367,3199,2862),ohousing,grade,grade,
        'Крупный оператор с опубликованным летом 2027; общий пансион прежде оценить по классу, самостоятельности и языку.',osources,
        status='published_2027',label='Четыре двухнедельные смены 2027: 27.06–09.07, 11–23.07, 25.07–06.08, 08–20.08. Это интервалы оператора по 13 календарных дней.',sessions=OVERNIGHT);dated(p,FT+'fees/')
    emit(2,'Frost Valley YMCA · Sugarloaf one-week','USA','Main Camp, Claryville, New York','general,sport,art','boarding','Entering Grades 2–3',
        'Первый короткий общий пансион Wawayanda для младших: самостоятельность и обычные лагерные активности. Опция только в session 1A/1B/4A/4B; '
        'точные границы одной недели не опубликованы в прочитанных страницах и не рассчитаны делением двухнедельной смены.',
        boardprice(1852,1759,1574),ohousing,grade,grade,'Проба одной недели перед длинным пансионом, но только после подтверждения класса, дат и языка.',osources,
        label='Лето 2027: session 1A, 1B, 4A, 4B. Точные заезды/выезды ещё не подтверждены.')
    farmsources=osources+[src('Рабочая ферма, возрастные группы, юрты и Seedlings',F+'camps/farm-camp/')]
    p=emit(3,'Frost Valley YMCA · Farm Camp two-week','USA','East Valley Farm, Catskills, New York','general,nature,science','boarding','Entering Grades 2–10',
        'Рабочая ферма: животные, выращивание/сбор урожая, приготовление еды, ремёсла и традиционные активности. '
        'Юрты без отопления, электричества и водопровода; общий bathhouse, ночью сопровождение вожатого/напарника. Это природный практический трек.',
        boardprice(3781,3522,3151),ohousing+' Размещение в фермерских юртах отличается от отопленных main-camp cabins.',grade,grade,
        'Полезная самостоятельность и экологическая инженерия для подходящего школьного класса; младшему проверить комфорт ночёвок.',farmsources,
        status='published_2027',label='Четыре заезда по общему расписанию 2027: 27.06–09.07, 11–23.07, 25.07–06.08, 08–20.08.',sessions=OVERNIGHT);dated(p,FT+'fees/')
    emit(4,'Frost Valley YMCA · Seedlings one-week','USA','East Valley Farm, Catskills, New York','general,nature,science','boarding','Entering Grades 2–4; заезды различаются для boys/girls',
        'Короткий фермерский пансион. Собственная страница: 1A и 4A girls, 1B и 4B boys. Для Матвея/Оскара нельзя выбирать любую первую половину. '
        'Точные недельные даты не опубликованы; полный двухнедельный интервал не подставлен.',
        boardprice(2080,1937,1733),ohousing+' Фермерские юрты и общий bathhouse.',grade,grade,
        'Младшая ступень фермерского пансиона после проверки класса и конкретной boys-смены.',farmsources,
        label='Лето 2027: мальчики 1B/4B; календарные границы пока не подтверждены.')
    p=emit(5,'Frost Valley YMCA · Durango horsemanship','USA','Main Camp barn, Claryville, New York','general,sport,nature','boarding','Boys entering Grades 3–8 И минимум 8 лет',
        'Половина дня со своей закреплённой лошадью: верховая езда, здоровье и уход; группы по навыкам, в том числе новичков. Остальной день общие активности. '
        'На странице boys-кабины 8–10 и 11–13; школьный класс и возраст проверяются одновременно. Девичьи Mustang/EVR — другие категории.',
        boardprice(3781,3522,3151),ohousing,grade,fit('later','В 2027 Оскару 6–7, меньше заявленного минимума 8; школьный класс не снимает этот предел.'),
        'Дополнительный трек ответственности для Матвея, если подходит класс; совместная профильная смена братьев сейчас не получается.',
        osources+[src('Durango: boys, минимум 8, классы и половина дня с лошадьми',F+'camps/horse-camps/')],
        status='published_2027',label='Четыре заезда 2027 по overnight-расписанию; нужны boys-места выбранного уровня.',sessions=OVERNIGHT);dated(p,FT+'fees/')
    dsources=[src('Лето 2027: недели, классы и темы',FD),src('Прайс пока 2026, местный Tier D и условия оплаты',FD+'fees/'),src('FAQ 2026: обед, транспорт и организация',FD+'faq/')]
    p=emit(6,'Frost Valley YMCA · Pathfinders day camp','USA','Main Camp, Claryville, New York','general,sport,art,nature','day','Grades 1–5; отдельные Explorers Pre-K/K с 4 лет и toilet trained',
        'Выбор активностей, спорт, походы, ropes/archery, ремёсла, Healthy Teaching Kitchen и waterfront. Pathfinders только недели 1–8. '
        'Девятая неделя общего расписания относится к отдельным farm/pony программам; она сюда не добавлена.',
        DPRICE,'Дневная программа 09–16 по общей странице; архивные часы drop-off/pickup 2026 отличаются. Семейное жильё отдельно.',grade,grade,
        'Общий дневной вариант для семьи в Catskills; принадлежность к Grades1–5 и открытый туристический приём ещё проверить.',dsources,
        status='published_2027',label='Восемь будних недель 28.06–20.08.2027; новый тариф ещё нужен.',sessions=DAYS);dated(p,FD,scope='day_camp_window')
    p=emit(7,'Frost Valley YMCA · LEGO Masters day','USA','Main Camp, Claryville, New York','technology,general','day',
        'Неделя 1 Grades 2–3; неделя 3 Grades 3–5',
        'Конструирование LEGO, командные задания и небольшие внутренние испытания плюс обычные лагерные активности и плавание. '
        'Программирование моторов, SPIKE/VEX и подготовка к мировой LEGO-лиге в описании не обещаны.',
        DPRICE,'Дневной specialty; семья организует проживание и ежедневную дорогу.',grade,grade,
        'Инженерное знакомство через конструкцию; школьные группы двух недель различаются.',dsources,
        status='published_2027',label='Week1 28.06–02.07 Grades2–3; Week3 12–16.07.2027 Grades3–5.',sessions=[DAYS[0],DAYS[2]]);
    dated(p,FD,labels=['LEGO · Grades 2–3','LEGO · Grades 3–5'],scope='day_camp_window',variants=[dict(age='Grades 2–3'),dict(age='Grades 3–5')])
    p=emit(8,'Frost Valley YMCA · Inventor’s Workshop / Garage','USA','Main Camp, Claryville, New York','science,technology,general','day',
        'Workshop Week2 Grades4–5; Garage Week8 Grades2–3',
        'Workshop: строительные задачи, slime, egg drop и посещение Maker’s Lab. Garage: резинки, картон и крышки, мозговой штурм, прототип, испытание и презентация. '
        'Это два разных возрастных syllabus, не один робототехнический курс; часть дня общие активности.',
        DPRICE,'Дневной specialty; материалы реальных механических прототипов, собственный робот/компьютер не обещан.',grade,grade,
        'Более предметный maker-трек: выбирать Garage или Workshop по классу, а не по общему возрасту лагеря.',dsources,
        status='published_2027',label='Workshop 5–9 июля Grades4–5; Garage 16–20 августа 2027 Grades2–3.',sessions=[DAYS[1],DAYS[7]]);
    dated(p,FD,labels=['Inventor’s Workshop · Grades4–5','Inventor’s Garage · Grades2–3'],scope='day_camp_window',variants=[dict(age='Grades 4–5'),dict(age='Grades 2–3')])
    fsources=[src('Семейные темы, точные даты и отдельные специальные ретриты',FF),src('Прайс 2026–27: участники и комнаты отдельно',FL),
              src('Форматы проживания',F+'groups/lodging/'),src('Приезд и организация семейного пребывания',F+'groups/faq/')]
    p=emit(9,'Frost Valley YMCA · семейные тематические выходные','USA','Main Camp, Claryville, New York','general,nature,science,art','family','Семьи с детьми; ограничения отдельных активностей уточнять',
        '17 будущих общих семейных заездов: сезонная природа, ремёсла, Winter Makers, Maple Fest, Earth Day, обсерватория и художественные темы. '
        'Legends & Labyrinths — настольные сюжеты, не coding. Родитель сопровождает ребёнка. Одновременные Veterans/LIVESTRONG/autism/adoptive retreats имеют отдельные условия; их бесплатный тариф не перенесён на обычную семью.',
        dict(year=2027,label='Прайс 2026–27: участник $225/2 ночи или $300/3 ночи + отдельное жильё. Возраст 5 и младше без participant fee; точный возраст на приезд решает льготу.',
             included='Две ночи: 4 meals Sat breakfast–Sun breakfast; три: 7 meals Sat breakfast–Mon breakfast. Программа включена. Это не обещание любого питания с пятницы.',
             extras='Жильё 2/3 ночи: cabin $345/518; комната 4-room lodge $355/525 (весь lodge $1420/2090); Castle room $365/540; Lakeview standard $420/625, suite $555/845; hostel $80/120 может быть общим и только в отдельные выходные. Иные здания/вместимость по PDF. Валюта $ по США, итог и выбранное количество ночей подтвердить.',
             deposit='Общий family-договор отмены не установлен; детский overnight refund к семейному бронированию не применён. Memorial только 3 ночи/$300; «from225» на других длинных выходных не цена полного трёхночного пакета.'),
        'Вся семья в выбранной комнате/кабине; это не детский пансион. Общие check-in16/check-out12 отличаются от специального Winter Family.',family,family,
        'Семейный способ провести осень/зиму/весну с содержательными природными и maker-темами, прежде чем отправлять детей отдельно.',fsources,
        status='published_2026_27',label='17 опубликованных интервалов октября 2026 – июня 2027; на длинных выходных конкретное количество ночей выбирают по условиям заезда.',sessions=[[a,b] for a,b,_ in FAMILY]);dated(p,FF,labels=[c for _,_,c in FAMILY])
    p['catalog_participation']='residential'
    p['price']['unit']='participant'
    for v in p['timing']['session_details']:
        v['entry']='Семейное пребывание вместе с ответственным взрослым; это не индивидуальное отправление ребёнка в пансион.'
        if v['start'] in ['2027-05-07','2027-06-11']:
            v['extras']=p['price']['extras']+' Специальная акция Mother’s/Father’s: мама/папа бесплатно при минимум одном full-paying guest; применение, совместимость и lodging нужно подтвердить.'
    p=emit(10,'Frost Valley YMCA · семейные фермерские заезды','USA','East Valley Farm / East Valley Ranch, Catskills, New York','general,nature,science','family','Родители и дети; возрастные ограничения отдельных активностей уточнить',
        'Животные, огород, harvest/cooking, фермерские ремёсла и природа. Осень и Memorial описывают юрты; Spring May21–23 размещает гостей в East Valley Ranch в миле от фермы. '
        'Верховая езда и доступность каждой активности зависят от заезда/возраста.',
        dict(year=2026,label='Для 9–12 октября 2026 опубликовано $285/человек за 2 ночи или $380 за 3, yurt/all-inclusive. Для майских заездов 2027 отдельный тариф не опубликован в прочитанном расписании.',
             included='Осенний пакет заявлен с размещением, питанием и программой; точный состав подтвердить.',extras='Сентябрьская акция «one child free per adult» относится к другому, уже прошедшему заезду; не применена к октябрю/маю. Дорога и выбранные опции отдельно.',
             deposit='Условия конкретного семейного заезда и отмену ещё подтвердить; generic East Valley retreat price не подставлен как camp quote.'),
        'Семейное проживание, не самостоятельный детский пансион. Spring2027 — Ranch; остальные описанные — farm yurts.',family,family,
        'Практическая семейная агроэкология с разными форматами проживания; май пока без полного счёта.',fsources,
        status='published_2026_27',label='9–12 октября 2026; 21–23 и 28–31 мая 2027. Тариф 2027 неизвестен.',sessions=[['2026-10-09','2026-10-12'],['2027-05-21','2027-05-23'],['2027-05-28','2027-05-31']]);dated(p,FF)
    p['catalog_participation']='residential'
    p['price']['unit']='participant'
    for v in p['timing']['session_details']:
        v.update(place='East Valley Ranch рядом с фермой' if v['start']=='2027-05-21' else 'East Valley Farm: юрты',
                 price='Цена этого семейного заезда 2027 пока неизвестна.' if v['start']>'2027-01-01' else '$285/2 ночи или $380/3 ночи за участника, all-inclusive.',
                 entry='Только вместе с ответственным взрослым; точный пакет ночей и семейное размещение подтвердить.')
    p=emit(11,'Frost Valley YMCA · Winter Family Camp','USA','Main Camp, Claryville, New York','general,nature,sport,art','family','Семья с ответственным взрослым; participant fee бесплатно до 5 лет включительно',
        'Зимняя природа, indoor archery/climbing, ремёсла и праздник Нового года. Снег, лыжи, snow tubing и ice activities зависят от погоды; sleds привозят свои. '
        'Внутри общего периода семья выбирает приезд и 2–6 ночей, это не обязательная семидневная детская смена.',
        dict(year=2027,label='За участника 2/3/4/5/6 ночей: $225/300/385/465/545 + жильё. До 5 лет включительно participant fee бесплатен, не вся комната.',
             included='Программы и стандартное питание; ужин в день приезда 17:30–18:30 включён. Hotel/inn-style — готовые кровати и полотенца.',
             extras='Жильё за 2/3/4/5/6 ночей: Lakeview room $407/611/712/814/930; Castle room $353/530/618/706/815; cabin целиком $173/259/302/345/395; 4-room lodge camp-style room те же $173/259/302/345/395, не весь lodge. Для camp-style бельё $14/комплект опционально. Lunch на выезде $13/человека старше 5, кроме 2 января. Валюту $ и вместимость подтвердить.',
             deposit='Минимум две ночи; check-in Вс–Чт 14–20, check-out12:30. Договор отмены семейного пакета не установлен; не применён overnight camp refund.'),
        'Семейное размещение. Цена зависит от оплачиваемых участников, выбранной комнаты и количества ночей; зимняя таблица отличается от обычных weekend rates.',family,family,
        'Понятный семейный зимний отдых с отдельной опубликованной таблицей; сначала выбрать фактический приезд, возраст Оскара и тип комнаты.',
        [src('Зимний период и активности',FF),src('Специальный зимний прайс, питание, 2–6 ночей и check-in',FW)]+fsources[2:],
        status='published_2026_27',label='27 декабря 2026 – 2 января 2027: окно выбора 2–6 ночей, не фиксированная смена.',sessions=[['2026-12-27','2027-01-02']]);p['timing']['precision']='season_window'
    ep=dict(year=None,label='Цена конкретного летнего/зимнего набора 2026–27 не опубликована в прочитанных первичных страницах.',included='Оператор описывает питание, площадку и сопровождение; состав выбранного пакета ещё нужен.',
            extras='Дорога/трансфер, страховка, число ночей и возрастные опции не оценены.',deposit='Размер аванса, платёжные сроки и отмена не установлены. Не заменены агентским прайсом или сертификатами с главной.')
    es=[src('Площадки, staff и меню — заявления оператора',EX),src('На странице verano2026 уже заголовок2027, но даты без года',EX+'verano-2026.php'),
        src('Собственный список вещей: ночёвочные принадлежности и запрет electronics','https://www.exploracamp.com/pdf/lista-articulos-4.pdf')]
    elabel='«Espera las fechas para verano2027»: новый набор ещё ждут. 13–18/20–25 июля без года не выданы за подтверждённые смены2027.'
    emit(12,'Explora Campamento · Kids','MEX','El Fuerte Bambú / Quinta Margarita, Tlaltizapán, Morelos; не офис CDMX','general,nature,sport,science','boarding','6–12',
        'Общий лагерь: природа/экология, вода, спорт, игры, самостоятельность и outdoor-активности. Робототехнический syllabus не опубликован. '
        'Сайт заявляет собственные комнаты, постоянное сопровождение и максимум восемь детей на guide; независимая инспекция/сертификаты не проверены.',
        ep,'Оператор описывает проживание и питание, packing list включает pajamas/shower items. Число ночей, комнаты, ночное сопровождение и готовность младшего уточнить.',
        conditional,fit('conditional','Для Kids нужно исполниться 6 на начало: в конце2026 может быть ещё5; в2027 6–7. Язык и конкретный набор не подтверждены.'),
        'Близкий общий природный пансион в гражданской стране семьи; право жить в Мексике не гарантирует лагерное место.',
        [src('Kids: именно возраст6–12',EX+'explora-kids.php')]+es,label=elabel)
    emit(13,'Explora Campamento · Xtreme','MEX','Tlaltizapán, Morelos','general,nature,sport','boarding','13–17',
        'Старшая outdoor-ступень: приключения, команда и самостоятельность. Это отдельная возрастная категория, не младший технический лагерь.',
        ep,'Проживание на собственных площадках по описанию оператора; договор конкретной смены нужен.',later,later,
        'Будущий общий трек для подростков, не кандидат для детей2017/2020 сейчас.',[src('Правильно связанная Xtreme-страница13–17',EX+'explora-xtremo.php')]+es,label=elabel)
    emit(14,'Explora Campamento · Padres e Hijos','MEX','Tlaltizapán, Morelos','general,nature,sport','family','Родители и дети; конкретный нижний возраст не опубликован',
        'Семейное знакомство с природой, совместные приключения и укрепление команды родителей/детей. Возраст Kids6–12 автоматически на этот продукт не перенесён.',
        ep,'Родители участвуют вместе; выбранный формат размещения и количество ночей пока неизвестны.',family,family,
        'Сначала семейная проба площадки в Мексике, затем отдельный пансион после оценки языка и организации.',
        [src('Отдельная семейная программа',EX+'explora-padres-hijos.php')]+es,label='Семейная программа существует; конкретные даты2026–27 пока неизвестны.')
    cs=[src('Каталог явно 2024: учебные направления и школьные группы',CR+'tech-camps/courses.php'),src('Winter: противоречащий календарь без года',CR+'winter-camps/'),
        src('Santa Monica/Los Angeles: расписание и старый не датированный тариф',CR+'winter-camps/santa-monica-in-person-winter-camp.php'),src('Credit и возврат по условиям оператора',CR+'tech-camps/terms_of_service.php')]
    cprice=dict(year=None,label='Недатированная зимняя карточка: $125/day, $369.99/3 дня или $492.99/4 дня. Эти суммы не подтверждены для2026–27 и не применены к online/другому campus.',
        included='В описании конечный проект, рекомендации ПО и feedback/diploma; diploma участия не мировая награда.',
        extras='Конкретный campus/онлайн, техника, материалы, еда и transport требуют расчёта. $ по США, валюту счёта подтвердить.',
        deposit='Sales final: отмена не позже недели даёт credit полной суммы на один календарный год. Денежный возврат по усмотрению, обычно если credit не применим и notice≥3недели; не автоматический cash refund. Пропуски без гарантированного возврата.')
    ch='Дневной кампус или виртуальный курс по выбранному продукту; новый расписанный заезд/наличие курса на campus не подтверждены. Не пансион.'
    cl='Собственный каталог курсов озаглавлен2024. Winter homepage смешивает Dec16–Jan3/WedDec25 и таблицу Dec22–26/Dec29–Jan2; SantaMonica Dec22–24/Dec29–Jan2 без года. Не календарь2026–27.'
    emit(15,'CodeREV Kids · Minecraft Micro Code','USA','Los Angeles / California campuses или online; конкретный текущий campus подтвердить','coding,games,technology','day,online',
        'Детальная карточка6–10, Grades1–2/3–5; заголовок Micro6–9 расходится',
        'Minecraft: level design, Redstone и логика устройств, команды/код по уровню. Для level2 нужна база. Точную версию/лицензию и реальное количество часов зимней смены ещё согласовать.',
        cprice,ch,conditional,fit('conditional','С шести лет по детальному курсу; возраст на первый день, фактический класс и конкретная младшая версия решают допуск.'),
        'Архивная игровая ступень к логике и коду; действующий syllabus и новый набор ещё подтвердить.',cs,label=cl,status='archive_next_unannounced')
    emit(16,'CodeREV Kids · Roblox Studio','USA','Los Angeles / California или online','coding,games,technology','day,online','8–10, Grades3–5',
        'Roblox Studio: игровые миры и собственные механики, встроенные assets для младших, Lua по версии курса. Level2 предполагает предварительное кодирование. VR в выбранном детальном syllabus не гарантирован.',
        cprice,ch,conditional,later,'Архивный game-development трек для Матвея после новой проверки; Оскару ниже восьми пока рано.',cs,label=cl,status='archive_next_unannounced')
    emit(17,'CodeREV Kids · REV Robots','USA','California campus / virtual; фактический комплект подтвердить','robotics,coding,technology','day,online','8–10, Grades3–5',
        'Arduino: моторы, свет и датчики, блочное кодирование. Оператор допускает виртуальный симулятор ИЛИ реальный набор; физический робот каждому не гарантирован. '
        'CreatorBot опционально покупают и могут оставить, «$50 discount» — скидка, не цена набора. 140 часов curriculum access не равно140часам одной смены.',
        cprice,ch,conditional,later,'Предметная электроника/код для Матвея после проверки реальной техники и преподавателя, вместо обещания Arduino по одному названию курса.',
        cs+[src('Архив REV Robots: simulator/Arduino, optional CreatorBot и curriculum access',CR+'tech-camps/courses.php#engineering_track')],label=cl,status='archive_next_unannounced')
    p=emit(18,'CISV México · путь к международному Village','MEX','Отправляющее национальное отделение México; принимающую страну выделяют отдельно','general,languages,leadership','boarding','Village: ровно11 лет; возрастное правило выбранного приглашения подтвердить',
        'Международная образовательная village-программа 28 дней, культуры/сотрудничество. В делегации обычно2мальчика+2девочки с adult leader21+; местный chapter отбирает и готовит участников, приглашения распределены между странами. '
        'Это не свободная семейная покупка пансиона в любой стране и не международная робототехническая лига.',
        dict(year=None,label='Цена зависит от national chapter и приглашения; опубликованного полного счёта2027 для семьи нет.',
             included='CISV описывает организацию, проживание и питание в camp fee; состав национального пакета подтвердить.',extras='Международная дорога, insurance, pocket money и подготовка не оценены; Mexican citizenship не автоматическое право на приглашение.',
             deposit='Отбор, сроки, взнос, возврат и резидентский chapter определяются национальным отделением. Семья не подавала заявление.'),
        'Международный пансион с делегацией и взрослым leader, родители обычно не живут в camp. Реальная страна/даты camp пока не выделены.',later,later,
        'Будущая международная самостоятельность: Матвей достигает11 в2028, Оскар в2031; возрастной cutoff и приглашение проверяются отдельно.',
        [src('México: английский во всех международных программах, знания заранее не обязательны','https://mx.cisv.org/programas/'),src('Village11лет/28дней/делегации','https://cisv.org/programmes/village/'),src('Маршрут через отделение и родители','https://cisv.org/your-child-and-cisv/')],
        language='México прямо указывает английский как язык международных программ; предварительное владение не обязательно. Это английская camp life, не технические уроки.',confirmed=['EN'],
        label='Новый международный camp2027 не назначен; для детей семьи возрастVillage наступает только2028/2031.')
    p['language_evidence_role']='camp_life'
    p=next(x for x in profiles if x['slug']=='envision-winter-audit')
    p.update(checked=CHECKED,programme='Потоки5–8/9–13: ramp robotics, Roblox/FlowLab и3D по разным неделям. Свежий landing явно WinterDecember2026, но product/picker сохраняют иной календарь без года; нельзя гарантировать конкретный syllabus и дни по одной карточке.',
        timing=dict(status='partial_2026_27',label='Landing Winter2026:21–24/28–31декабря; product22–24/29–30 без года, picker только30декабря. Спорные смены не добавлены в календарь.',sessions=[]),
        editorial_reason='Повторная первичная проверка подтверждает конфликт страниц, поэтому единственное существующее досье обновлено без дубля/новой смены.')
    p['price']['deposit']='Camp policy: no refund; серьёзная травма/семейные чрезвычайные случаи могут дать credit за неиспользованную часть на12месяцев по усмотрению. Возможен перенос в более ранний доступный week/частная передача места по правилам. Не weekly-class makeup/refund.'
    for s in p['sources']:s['checked']=CHECKED

def extend_report_v126(r):
    r['version']=126
    r['methodology'].append('v126: североамериканские технические/общие пансионы, семейные сезоны и мексиканский chapter-маршрут проверены по выбранным страницам и PDF. $ без прямого кода валюты не стал автоматической сметой USD/CAD; будущие цены и старые договоры разделены. Ни одна страна не признана полностью изученной.')
    r['shortlist'] += [dict(label='Америка · ближайшая инженерная проба для обоих',slugs=['inned-winter','envision-winter-audit','coderev-minecraft','coderev-revrobots'],reason='InnEd даёт два точных декабрьских блока; Envision конфликтует по дням, CodeREV по годам. Для всех язык ведущего ещё нужен; старые цены не гарантируют новый набор.'),
        dict(label='США · природа, maker и первый пансион',slugs=['frost-family-weekends','frost-winter-family','frost-family-farm','frost-pathfinders','frost-inventors-day','frost-wawayanda','frost-sugarloaf'],reason='Семейный заезд с родителями, дневной camp и детский пансион имеют разные возрастные, жилищные и платёжные условия. WinterFamily выбирают2–6ночей; школьные классы не определены по одному году рождения.'),
        dict(label='Мексика · семейная проба и будущая международная самостоятельность',slugs=['explora-parent-child','explora-kids','explora-xtreme','cisv-mexico-village-route'],reason='Explora новая смена ещёTBC, Kids6–12, Xtreme13–17. CISV Village ровно11 через chapter/делегацию: будущий2028/2031маршрут, не свободное бронирование в Мексике.')]
    gaps=[('USA','Frost: недельные границы, язык, новый day quote',FT,'Sugarloaf1A/1B/4A/4B и Seedlings boys1B/4B без точных недельных дат; не вычислены. Overnight2027tiers+5%/March1 отличаются от day2026TierDlocal/May1. Семейные двух/трёхночные и зимние цены разные; самостоятельный juniorEN/foreign intake не доказан.'),
      ('USA','CodeREV: архив2024, новый заезд не датирован',CR+'winter-camps/','Owncourseheadline2024: учебные проекты сохранены как архив, не действующий syllabus2027. HeaderweekdayWedDec25 указывает другой исторический календарь, таблицаDec22 иSantaMonica иной состав дней без года. Недатированные125/369.99/492.99 не2026–27quote. REVRobots simulatorORphysical,CreatorBot$50discount неkitprice,140haccess неcampcontacthours. Другая RevEngineering имеет пустое Ages и5–8 рядом сGrades: это не доказанный возраст5–8 для Оскара.'),
      ('USA','Digital Dragon: старые наборы и 404', 'https://digitaldragon.co/','OwncampстраницыSummer2025/online2021 и зимние календарные дни других лет; guessedwinter404 не закрытие оператора. Новый2026–27детский набор не подтверждён, новое досье/цена не добавлены.'),
      ('CAN','Envision: landing и picker расходятся','https://envisionrobotics.com/product/winter-stem-camp-markham/','Свежая собственная Winter2026landing21–24/28–31Dec против product22–24/29–30 без года, pickeronlyDec30. ExistingCP299 обновлён без повторной карточки/спорной точной даты. Campno-refund/credit12months отдельно отweeklylessons.'),
      ('CAN','Holland Bloorview: медицинский admission gate','https://hollandbloorview.ca/services/programs-services/robotics-holland-bloorview/program-description','OwnWinter2027juniorJan20–Feb24,6–10,но programme требует formaldiagnosis и иногда family1:1support; возрастasofDec31. GenericCoding1018–14 противwinter9–14. Это специализированная программа, не доказанный открытый каникульный лагерь для любой семьи; здоровье детей не предполагалось.'),
      ('MEX','Explora: год дат, договор и реальная площадка',EX+'verano-2026.php','Headingwait2027 против13–18/20–25Jul без года. Даже guessedverano2027/extremounderscore200 отдаютhome, не новый syllabus. HyphenlinkedKids6–12/Xtreme13–17/family прочитаны; officeCDMX не campMorelos. Packing4days не шестидневный счёт; ESсайт не явное подтверждение языка ведущего.'),
      ('MEX','CISV: chapter, делегация и принимающая страна','https://mx.cisv.org/programas/','Village11/28days future2028/2031,Englishcamp-life подтверждён. MX — отправляющий chapter, не география всех28дневныхcamps. Национальный отбор/местные связи/приглашения/fees2027 ещё нужны; гражданство и CRПМЖ не гарантируют eligibility.'),
      ('CRI','Museo de los Niños и CISV: новый набор не найден в выбранных источниках','https://museocr.org/ninos/tu-visita/','OwnvisitaCampamentosheading,ownnews иpublicWPsearchcampamento обеихroots[]; guessedcampamentos404,cr.cisv.orgDNS. Это ограничения конкретного чтения, не отсутствие campвКостаРике. UCR2025иAmora2027 уже есть: не продублированы и не передатированы. Для нового техника/ENEScamp нужны собственная программа, возраст, смены и полный счёт.')]
    names={'USA':'США','CAN':'Канада','MEX':'Мексика','CRI':'Коста-Рика'}
    for iso,title,url,detail in gaps:r['gaps'].append(dict(iso=iso,country=names[iso],provider='v126 · '+title,url=url,detail=detail,
        next_action='Продолжить проверку следующего набора и всех приоритетных стран; worldwide goal активна. Внешних заявок/оплат не было.'))
