"""Own seasonal programmes and contracts; no inferred teaching language or grade."""
CHECKED='2026-10-05'
import re
STAR='https://www.starkidsafterschool.org/'
RISE='https://stemrise.ai/en/'
SNAP='https://www.snapology.com/north-carolina-greensboro/blog/day-camp-2026-teacher-work-day-holidays/'
SANTA='https://www.campsantaursula.com/'
RM='https://frmclinicsavanza.com/'
MAKE='https://www.campmakemake.com/'

def readable(text):
    """Space compact evidence notation only in prose, never in IDs, URLs or dates."""
    text=re.sub(r'([А-Яа-яёЁ])([A-Za-z0-9])',r'\1 \2',text)
    text=re.sub(r'([A-Za-z0-9])([А-Яа-яёЁ])',r'\1 \2',text)
    text=re.sub(r'([0-9])([A-Za-z])',r'\1 \2',text)
    text=re.sub(r'([a-z])([A-Z])',r'\1 \2',text)
    text=re.sub(r'([,;:])(?=[А-Яа-яёЁA-Za-z])',r'\1 ',text)
    replacements={
        'необъявлен':'не объявлен','неподтверждён':'не подтверждён','неподтверждены':'не подтверждены',
        'неопубликованы':'не опубликованы','неподставлены':'не подставлены','неподразумеваются':'не подразумеваются',
        'необещана':'не обещана','необещан':'не обещан','необещаны':'не обещаны','неустановлены':'не установлены',
        'неустановлен':'не установлен','неразъяснено':'не разъяснено','нетолько':'не только','другихоператоров':'других операторов',
        'уточнитьдля':'уточнить для','полнаяцена':'полная цена','точныедни':'точные дни','точныечасы':'точные часы',
        'точногособытия':'точного события','точныйконец':'точный конец','прочитанным':'прочитанным',
        'пятьдней':'пять дней','шестидневный':'шестидневный','соседниепрограммы':'соседние программы',
        'этотлагерь':'этот лагерь','историческийрезультат':'исторический результат','старшаяшкола':'старшая школа',
        'основнойпрайс':'основной прайс','телефонытольковебсообщения':'телефоны: только веб-сообщения',
        'действующаядоступность':'действующая доступность','полныймировой':'полный мировой',
        'активностикаждому':'активности каждому','внешнийприём':'внешний приём','реальныедни':'реальные дни',
        'родителинаблюдают':'родители наблюдают','родителям':'родителям','каждоймалойгруппе':'каждой малой группе',
        'старшийподросток':'старший подросток','самостоятельнойдоставке':'самостоятельной доставке',
        'техникинедостаточно':'техники недостаточно','последниедни':'последние дни',
    }
    for a,z in replacements.items():text=text.replace(a,z)
    return text

def clean_profile(p):
    for k in ['provider','place','age','language','programme','accommodation','editorial_reason']:p[k]=readable(p[k])
    p['timing']['label']=readable(p['timing']['label'])
    for k in ['label','included','extras','deposit']:p['price'][k]=readable(p['price'][k])
    p['questions']=[readable(q) for q in p['questions']]
    for q in p['family_fit'].values():q['detail']=readable(q['detail'])
    for q in p.get('timing',{}).get('session_details',[]):
        for k in ['label','price','place']:
            if k in q:q[k]=readable(q[k])
    for q in p['sources']:q['title']=readable(q['title'])

def add_americas_v90(add,src,fit,P):
    start=len(P)
    def fee(year,label,included,extras,terms):
        return dict(year=year,label=label,included=included,extras=extras,deposit=terms)
    def detail(p,rows):
        p['timing'].update(sessions=[[q['start'],q['end']] for q in rows],session_details=rows,variant_keyed=True)
    def row(a,z,key,label,price,url,place,**kwargs):
        return dict(start=a,end=z,variant_key=key,label=label,price=price,source=url,place=place,**kwargs)
    unknown_language='Язык страницы не доказывает язык преподавания. Основной EN/ES/RU, помощь на втором языке и иностранный допуск конкретной смены пока не подтверждены.'
    gradefit=fit('unknown','Нужен фактический школьный класс, а не возраст из года рождения; подтвердить внешний/иностранный приём и язык.')
    owntravel='Перелёт, жильё семьи и местная доставка/забор детей отдельно; без пансиона. Место и итоговый счёт не подтверждены.'

    # One academy, five themes; BattleBots has an unresolved end date.
    stplace='10181 Finch Ave, Cupertino, California 95014, USA'
    stcost=fee('2026–27','USD399.75 / 461.25 / 563.75 / 666.25 за выбранную смену: цена390/450/550/650 + ticket fee9.75/11.25/13.75/16.25. Это четыре ступени, не гарантированная доступность самой дешёвой.',
        'Учебная программа и работа с роботами. StarCode связывает блоки с Python/C++/Java; это знакомство, не подтверждённое овладение всеми тремя языками. Учебная техника не обещана в подарок.',
        'Свой обед, перекус/вода: camp terms прямо не предусматривают еду. Жильё/дорога отдельно. Опоздание после 5-минутной льготы1USD/min. Возможную доплату/налог и часы последнего дня подтвердить.',
        'August2026 terms: camps/classes отдельно от after-school subscription. Общий cash refund не обещан; исключение first-day try требует письменного запроса в первый день и вычета35USD, processing и части за посещённое. Перенос оплаченной стоимости в течение1года, минимум7дней; позднее50USD. Место только после оплаты; итоговая цена checkout. After-school1100/750USD/month и75USD enrolment не camp price. Условия включают media permission, не приняты от имени семьи.')
    strows=[
        ('star-anibots','ANIBOTS Christmas','anibots-christmas','2026-12-21','2026-12-24',
         'Роботизированные головы/руки, выразительная механика и двуногие модели; датчики, интерактивность, знакомство с AI/ML. Beginners/intermediate, новые и возвращающиеся. Body явно начинает примечание HalfDay24Dec; Time&Location заканчивается12:00, общий teaser09–15. Для24декабря рассчитывать на короткий день, подтвердить точные часы.',True),
        ('star-robot-gaming','Robot Gaming3.0','robot-gaming-3-0','2026-12-28','2026-12-31',
         'Создание и кодирование игровых роботов: световые датчики laser-tag, цветовые ускорения/зоны MarioKart, арену с препятствиями и стратегией. Темы игр используются как учебная механика, не официальные турниры этих брендов. Time&Location заканчивается31Dec12:00, teaser обещает09–15; время последнего дня расходится.',True),
        ('star-carbots','Carbots2.0','carbots-2-0','2027-02-15','2027-02-19',
         'Датчики, препятствия/парковка/waypoints, sensor fusion и адаптивное управление; проектирование и3Dпечать кузова, steering/speed. Сравнение с Waymo/Tesla — заявление оператора об учебной теме, не участие компаний/официальная квалификация инженера autonomous vehicle.',False),
        ('star-ecobots','Ecobots2.0','ecobots-2-0','2027-04-12','2027-04-16',
         'Агро-/экологическая робототехника, датчики и автоматизация. Recycling/color sorting, strawberry rover, XYZwatering/seeding и solar tracker описаны как прошлый EcoBots1.0: не гарантированный список проектов2027. Новый2.0 обещает более сложные задачи; точный проект по возрасту запросить.',False),
        ('star-battlebots','BattleBots2.0','battlebots-2-0',None,None,
         'Механика устойчивости/скорости, кодирование роботов для внутренней арены, SUMO/autonomous challenge/BattleRoyale. Это учебные внутренние игры, не официальный мировой BattleBots/SUMO medal. Teaser23–26Nov2026 против Event/Time&Location23–27Nov: конец смены конфликтует, точного события пока не создано.',False),
    ]
    for slug,name,path,a,z,content,holiday in strows:
        add(slug,'Star Kids Academy · '+name,'США','USA',stplace,'robotics,coding,engineering'+(',ai' if slug=='star-anibots' else ''),'day','Grades1–2 или3–6; школьный класс, не числовой возраст',
            unknown_language+' StarCode собственная страница подтверждает EN/ES/RU интерфейс и Tutor среди22языков; это язык приложения, не педагогов/лагеря.',content+' В открытом HTML описание заканчивается ShowMore; подробное раскрытие не удалось из-за перенаправления browser в blocked-page. Скрытая часть не объявлена прочитанной. Общий camp index: восемь тем с разными роботами и внутренним challenge, точное содержание своей группы ещё нужно.',
            ('21–24Dec2026,09–15 кроме короткого24Dec.' if slug=='star-anibots' else '28–31Dec2026; конец31Dec12:00 против teaser15:00.' if slug=='star-robot-gaming' else a+'–'+z+',09–15,пять дней.' if a else 'Thanksgiving2026:23–26 против23–27Nov; точный конец не установлен.'),stcost,
            'Дневной городской лагерь; комнаты/пансион не предложены. Camp terms: food not served, свой lunch; camps без off-site field trips, classroom max26 не равно26:1staffratio.',gradefit,gradefit,
            'Конкретный технический кандидат с датами/сборами и проектами; фактический класс, язык, полный план и места ещё нужны.',
            ['Подтвердить фактический класс обоих, язык/иностранный приём, возрастную сложность и свой набор роботов.','Получить полное описание за ShowMore, последний день/закрытие Thanksgiving, итоговый тариф/место и camp terms.'],
            [src('Собственная карточка смены:даты/видимые проекты/четыре цены',STAR+'event-details/'+path),src('Camp index и группы',STAR+'camps'),src('Camp terms August2026', 'https://starkidsacademydocs.netlify.app/terms.html'),src('Языки приложения, не доказательство языка урока','https://starcoderobot.com/')],
            status='published_2026_27' if a else 'next_unannounced',sessions=[[a,z]] if a else [])
    # Same curriculum and dates, three specifically named camp venues; not three operators.
    rburl='https://www.robolabs.org/camps'
    add('robolabs-holiday','RoboLabs · Holiday Robotics','США','USA','Dublin / Fremont / San Jose, California','robotics,coding,engineering','day','Grades1–12; BattleRobots K–7 относится к другому недатированному summer2025 описанию',unknown_language,
        'Каждый ребёнок строит/программирует/тестирует физического робота; mechanical design/gears/friction и совместные задачи. VEXIQ/FLLLEGO/VEXV5 по уровню; brandplatform не обещает участие в официальном Worlds/qualifier. Beginners welcome; advanced level оценивается индивидуально, максимум8/instructor. Full09–15:30 включает30минобед+10минперерывы, half09–12 либо12:30–15:30. Отдельный BattleRobotsK–7 не переносится на эти даты.',
        'Thanksgiving23–25Nov2026, Christmas21–24 или28–31Dec2026. Summer2026 архив; реальные даты2027 ещё не опубликованы.',
        fee(2026,'3дня full417USD/half237;4дня full556/half316. Summer2026 five-day695/395 — архив, не тариф2027.',
            'Техника/учебная программа по уровню; ноутбук/robot take-home отдельно подтвердить.',
            'Свои lunch/snacks/water; extended15:30–18 по20USD/hour =50USD/day за все2.5h, не included robotics. '+owntravel,
            'Отмена/transfer/deposit/foreign admission для holiday cohorts в прочитанной camp page не раскрыты. Получить договор до оплаты.'),
        'Без проживания; только три camp venues из FAQ.',gradefit,gradefit,'Младшая робототехника с прозрачными дневными ценами/нагрузкой; реальный Grade1 нужен, K-onlyBattleBots не подменяет допуск.',
        ['Фактический Grade, beginner/advanced hardware, основной язык/foreign admission, точный кампус/место и camp refund.'],[src('Полная Holidaycamp page, fees,3venues/FAQ',rburl)],status='published_2026',sessions=[])
    rr=[]
    for place,key in [('6500 Dublin Blvd SuiteC,Dublin,CA','dublin'),('37120 Fremont Blvd SuiteQ,Fremont,CA','fremont'),('4140 Stevens Creek Blvd,San Jose,CA','san-jose')]:
        for a,z,label,cost in [('2026-11-23','2026-11-25','Thanksgiving3дня','full417USD/half237;extended20/hour'),('2026-12-21','2026-12-24','Christmas4дня','full556USD/half316;extended20/hour'),('2026-12-28','2026-12-31','NewYear4дня','full556USD/half316;extended20/hour')]:
            rr.append(row(a,z,key+'-'+a,label+' · '+key,cost,rburl,place))
    detail(P[-1],rr)

    snplace='Urban Air Adventure Park,4640 West Market Street,Greensboro,NC27407'
    snterms='Оплата полностью при регистрации. Отмена >4недель: возврат минус10USD;2–4недели50%;<2недель0. Medical written physician excuse:минус10; при отмене оператором возврат. WaiverUrbanAir обязателен до check-in, не подписан. Staff не может давать лекарства/помогать туалету; родитель приезжает для лекарства. Latepickup1USD/min после окна.'
    snextra='Свой lunch/snacks/water, без refrigeration/heating; никаких личных игрушек/электроники. Extended включает UrbanAir16–17, не лишний час робототехники. '+owntravel
    for slug,name,dates,cost,content in [
        ('snap-greensboro-school-holidays','School Holiday / Workday',[], '60USD/full09–16 или85/extended08–17 за день', 'Один день=утренняя+дневная тема, не вся мировая STEMпрограмма. HalloweenSPIKE, AttackBot/SPIKE, RobotSport/MegaMachines, Roblox, science и mechanicalbuilding; точная пара в календарной карточке.'),
        ('snap-greensboro-winter','Winter Holiday', [['2026-12-21','2026-12-23'],['2026-12-28','2026-12-30']], '3дня150USD/full или225/extended до26Oct2026;с27Oct175/275', 'Week1EscapeWinter+HolidayRoboticsSPIKEPrime;Week2STEAMSurvivor+CombatRobots. Таблица дважды прямо3campdays; вводный абзац Four-day противоречит таблице, четвёртый день не добавлен.'),
        ('snap-greensboro-spring','Spring Break', [['2027-03-22','2027-03-26']], '5дней224USD/full или324/extended до15Feb2027;с16Feb249/349', 'Minecraft-inspired конструирование + real-world robotics наSPIKEPrime, coding/engineering/teamwork, пять дней. Не официальный Minecraftтурнир или FLLqualifier.'),
    ]:
        add(slug,'Snapology Greensboro · '+name,'США','USA',snplace,'robotics,coding,engineering,science','day','Currently enrolled AND attending Kindergarten through age14; самостоятельный туалет',unknown_language,
            content+' Full09–16,drop08:30–09,pick16–16:30;extended08–17,drop07:30–08,pick17–17:30. Это окна передачи, не дополнительные учебные часы. English curriculum ещё не установлен. Ownbrand прямо отрицает LEGO endorsement.',
            'Собственная таблица SchoolYear2026–27: точные дни/смены, до2027May31. Без переноса на новое лето.',fee('2026–27',cost,'Программа/LEGOmaterials и extendedUrbanAir по пакету; следующая20%visitcoupon не бесплатный независимый парк.',snextra,snterms),
            'Дневной формат, без пансиона. Самостоятельный туалет обязателен; staff не даёт медикаменты.',gradefit,gradefit,'Точная локальная техника для школьных каникул, с доступными day/week fees и существенными бытовыми gates.',
            ['Подтвердить посещаемый Kindergarten/grade, языки, внешний приём, места, age-specific учебный план и final taxes/fee.'],[src('Официальная таблица/FAQ: браузером прочитаны раскрытые условия',SNAP)],status='published_2026_27',sessions=dates)
        if slug=='snap-greensboro-school-holidays':
            days=[('2026-09-07','BrickCity + E2/E3Engineers'),('2026-09-21','MovieMania + ScienceSlime'),('2026-10-30','EscapeHalloween + SPIKEHalloween'),('2026-11-03','FidgetSpinner + Roblox'),('2026-11-11','AttackBotSPIKE + Escape'),('2027-01-18','RobotSportSPIKE + MegaMachinesSPIKE'),('2027-01-25','MovieMania + EmmettAdventures'),('2027-02-15','RobotChallenge + Roblox'),('2027-03-05','PrehistoricSPIKE + Scientists'),('2027-05-31','MiniFigure + E2/E3Engineers')]
            detail(P[-1],[row(a,a,'day-'+a,label,cost,SNAP,snplace) for a,label in days])

    steam='https://steamupedu.com/'
    for slug,path,label,a,z,content,scope,weekdays in [
        ('steamup-thanksgiving','camp-thanksgiving-robotics-and-engineering-stem.php','Thanksgiving','2026-11-23','2026-11-27','Robotics/engineering/scienceexperiments и командные задачи;26NovThursday закрыто, четыре actualdays.', 'day_camp_window',['MO','TU','WE','FR']),
        ('steamup-winter','camp-winter-stem.php','Winter','2026-12-21','2027-01-01','Наука/инженерия/роботы: закрыты24/25/31Dec и01Jan, поэтому только21/22/23/28/29/30Dec — шесть посещений, не12полных дней. Bookingdeadline15Nov2026.', 'day_camp_window',['MO','TU','WE']),
        ('steamup-spring','camp-spring-stem.php','Spring','2027-03-15','2027-03-19','Конкретные K–5направления:RoboAdventurers,CodeExplorers,CyberScouts,GizmoGurus — простая механика/роботы, gaming/coding, onlinesafety/mechatronics. Для6–8Grade отдельные TechTinkerers/RoboArchitects/CodeQuest/CyberGuardians. Это варианты/описания, выбор ежедневного timetable ещё не опубликован; все восемь курсов каждому не обещаны.', 'camp_session',None),
    ]:
        place='2000 N.Orange Ave,Orlando,Florida32804'
        add(slug,'STEAMUP Academy · '+label,'США','USA',place,'robotics,coding,engineering,science','day','Таблица5–15 против текста3–15; Spring конкретные K–5 / Grade6–8',unknown_language,
            content+' Обычный09–17,extended08–18. Школьная VEXIQteam в отдельном меню не подтверждает camp qualification/международную победу.',a+'–'+z+'; '+('точные5дней' if scope=='camp_session' else 'окно лагеря с закрытыми днями, не гарантированный ежедневный заезд'),
            fee('2026–27','От250USD'+('/неделю прямо на Springpage' if slug=='steamup-spring' else '; период/пакет из Startingat250 не раскрыт'),
                'Тематические занятия. Полный почасовой план, hardware/lunch/insurance/все обязательные сборы запросить.',
                'Early/latecare84USD/week, lateafter18:1.85USD/min; sibling10% только oldestchild/однаскидка. '+owntravel,
                'Camp refund/deposit не раскрыты в прочитанных страницах; рекламные250USD не finalall-in invoice.'),
            'Без проживания; питание и ownershipоборудования не подтверждены.',fit('conditional','Возраст5–15 подходит; фактический K–5/Grade, уровень, EN/foreign admission ещё нужны.'),fit('conditional','Возраст5–15 подходит, но нужны grade, язык/самостоятельность и внешний приём.'),
            'Тематический кандидат: реально исключены holidays, grade-specific проекты и приписывание дешёвой базовой цены всем дням.',
            ['Подтвердить grade/свой трек, язык и foreign intake, actual посещения/оплачиваемую единицу, full invoice и refund.'],[src('Собственная сезонная programmepage',steam+path)],status='published_2026_27',sessions=[[a,z]])
        q=row(a,z,slug,label,P[-1]['price']['label'],steam+path,place,date_scope=scope)
        if slug=='steamup-winter':q['deadline']='2026-11-15'
        if weekdays:
            import datetime
            dd=datetime.date.fromisoformat(a);last=datetime.date.fromisoformat(z)
            mapping=['MO','TU','WE','TH','FR','SA','SU'];actual=[]
            while dd<=last:
                if mapping[dd.weekday()] in weekdays:actual.append(dd.isoformat())
                dd+=datetime.timedelta(days=1)
            q.update(date_scope='session_days',sessions=[dict(date=d,start_time='09:00',end_time='17:00',timezone='America/New_York',topic='STEAMUP '+label+' · обычный дневной лагерь',time_note='Extended08–18 оплачивается отдельно; весь пакет и места уточнить.') for d in actual])
        detail(P[-1],[q])

    for slug,name,age,content,mat,osc in [
        ('stemrise-winter-roblox','Roblox+3D','7–13','Python/Lua,RobloxStudio/3Dprinting, проектирование/сборка, teamdemo и внутренний award.','conditional','conditional'),
        ('stemrise-winter-ai','Coding+AI','9–16','Python/WebAIassistant/app, исходный Gitrepo и презентация проекта; уровень/часовой объём ещё уточнить.','conditional','later'),
        ('stemrise-winter-research','ResearchPortfolio','12–18','Исследовательский project/datacodeportfolio/recommendationletter, обещание оператора:не университетский диплом/поступление и не подтверждённая международная победа.','later','later'),
    ]:
        add(slug,'STEMRise · Winter '+name,'Канада','CAN','Markham,Ontario — точный wintercampaddress ещё запросить','coding,games'+(',ai' if slug!='stemrise-winter-roblox' else ',engineering'),'day','Wintercourse '+age,unknown_language,
            content+' Winter page: только Markham onsite; NorthYork/RichmondHill/Scarborough onlineonly, несмотря на общийhome4campusbanner. Не созданы четыре очных кампуса. Расписание/размерcampgroup/своя техника не опубликованы. Общаяcourseprogression Scratch→Python→Java/Roblox→USACO/CCC не доказывает результаты школы.',
            '20Dec2026–10Jan2027 — seasonalwindow, не расписание по дням/полная смена. Christmas/NewYearweekdays не подразумеваются.',
            fee('2026–27','Camp price только quote. Trial9.9CAD не зимний тариф; referral25CAD и early/sibling акции не вычтены без подтверждения.',
                'Выбранный curriculum; software/devices/lunch/формат и реальная длительность неизвестны.',
                owntravel+' Homepage/FAQ/refund расходятся по stacking/платежам; цену со скидками не считать подтверждённой.',
                'Camp sectionEnglishpolicy:до30дней удержание5%;внутри30дней доначала20%;послестарта при<20%completion pro-rataнепосещённое минус25%;после20%обычно no refund/transfer90дней. Registrationfee отдельноневозвратный/сумманеизвестна, discountedrefundпоstandardprice. Chineseversionprevails — английский summary не подтверждает совпадение с договором. Generalcourseflat50/100CADFAQ не camp rule.'),
            'OnsiteMarkhamбезпансиона; другие перечисленные cities только onlinewinter.',
            fit(mat,'По возрасту'+('9–10 соответствует' if mat!='later' else ' ниже12; будущаяступень')+'; реальные даты/приём/язык и grade/уровень уточнить.'),
            fit(osc,'7–13 только после7-летия:кJan10,2027 нужен уже7-летний возраст; точная DOB нужна.' if osc=='conditional' else 'Ниже9/12, будущийвозраст.'),
            'Канадский сезонный кандидат с различием onsite/online и уровня; camp slots/EN/full invoice не объявлены установленными.',
            ['Полное расписание и адресMarkham, точная дата рождения/уровень, EN/foreign admission, campus/online, договорZH/EN и finalprice.'],
            [src('Конкретная winter2026–27coursepage',RISE+'camps/winter'),src('Camprefund отдельно от generalcourses',RISE+'refund-policy'),src('FAQ:уровни/общие правила, не подтверждённая статистика побед',RISE+'faq')],status='published_2026_27',sessions=[['2026-12-20','2027-01-10']])
        P[-1]['timing']['precision']='season_window'

    suplace='Camino a Portezuelo s/n,Planta del Carmen,Cerro de San Pedro,San Luis Potosí,México'
    add('santa-ursula-general','Camp Santa Úrsula · Verano','Мексика','MEX',suplace,'general,sport,science,art','boarding','Именно summer7–15; общий activityrule minimum6 не отменяет7-летний допуск',
        'Основной ES/EN/RU и постоянная помощь конкретной группе не подтверждены. Собственный internationalblog прямо различает иностранных campers и bilingualimmersion; исторический международный состав не ENcurriculum.',
        'Общий outdoorпансион:команды/спорт, велосипеды/kayak/плавание/horse,forest/biodiversity,practicalworkshops иnightgames. Робототехника/AI/coding не заявлены. Каждая команда instructor+assistant, ночью instructor скомандой. Medicalservice24h; summerpage amenities не гарантирует всем детям каждую attraction — age/safetyrules. Поreglamento сон обычно22:30; дневныеактивности10–22 с break, не12hуроков. Телефоны сдают доотъезда, сообщения родителей только websystem; обычные звонки ребёнку не обещаны.',
        'Датированные2027pricecards:10–16July;17–23July;10–23Julyextended. Старыйhero11–24July2026 иhome16–23July расходятся; используется конкретная2027card, подтверждение письменно нужно.',
        fee(2027,'MXN51 700/7дней за10–16 или17–23July;98 500/14дней за10–23July. Две отдельныеweeks103 400, extended дешевлена4 900; пакетная разница, не дополнительная акция.',
            'Проживание/foodsnacks, facilities/equipment/instruction иmaintenancequota. Summerpage24hmedical; собственный contract: accident policy до150 000MXN на участника, действует только до выхода из лагеря.',
            'Дорога/transfer не обещаны. Расходы сверх150 000MXN и исключения полиса оплачивают родители; заболевания/предсуществующие расходы полис не покрывает; medicalservice24h не allmedicalexpensecoverage. Состав текущих activities может заменяться. Длядвух7days103 400 илиextended197 000 до дороги/прочего, еслиOscarуже7.',
            'Contract:обычнаяотмена≥15дней, health/safety исключение≥3дней; варианты transferдругому участнику/credit1год/50%cashrefund. Другаястрока ≤3дней вообще0 — ровно3дня конфликтуют. Latearrival/earlydeparture0. Operatorforce-majeure переносдо1года, затемrefundесли невозможен; посленачалаsuspension0. Тарифможетизменятьсясуведомлением/acceptance, fullpaydeadline нужен; не подписано.'),
        'Пансион вPuebloVaquero/traincarrooms, instructorночуетскомандой. Requests совместногожилья максимум3campers, не гарантия отдельнойдвухместнойкомнаты. Securitypage говоритnooffsiteexcursions.',
        fit('conditional','Летом2027 будет9–10:summer7–15по возрасту подходит; место, языки и готовностькпансиону подтвердить.'),fit('conditional','Летом2027будет6–7:только после7-летия, нужно точное DOB. Minimum6 вactivityreglamento не допускsummer.'),
        'Мексиканский общий пансион среальными2027датами/ценами и прочитаннымcontract; не подтверждённый топробототехники/билингвальныйлагерь.',
        ['DOBОскара/язык, точная17Julyграница, cohort/inclusions иfullinvoice; отмена ровно3дня, transfer, medical policy/лимит покрытия иcontactrule.'],
        [src('Конкретные Summer2027age/date/pricecards',SANTA+'campamentos-de-verano'),src('Contract/cancel/medicaldeductible',SANTA+'terminos-y-condiciones-campamento-de-verano'),src('Behaviour/phones/activityage, не summeradmission',SANTA+'reglamento'),src('Internationalcommunity не languageimmersion',SANTA+'post/un-campamento-con-experiencia-internacional-sin-salir-de-mexico'),src('Security/nooffsite',SANTA+'seguridad')],status='published_2027',sessions=[])
    detail(P[-1],[row(a,z,'summer-'+a+'-'+z,label,cost,SANTA+'campamentos-de-verano',suplace) for a,z,label,cost in [('2027-07-10','2027-07-16','Verano1 ·7дней','51 700MXN'),('2027-07-17','2027-07-23','Verano2 ·7дней','51 700MXN'),('2027-07-10','2027-07-23','Extendido ·14дней','98 500MXN')]])

    rmplace='GSD International School,C.Guácima,Guácima Abajo,Alajuela20105,Costa Rica'
    add('avanza-real-madrid-cr','Avanza · Fundación Real Madrid FootballClinics','Коста-Рика','CRI',rmplace,'general,sport','day','Собственная2027card5–17 vs FAQ6–17/born2010–2021; подтвердить дляOscar',
        unknown_language+' Испанские тренеры/ESстраница не доказательство языкаинструкций; ENвариантсайта тоже не ENcourse.',
        'Дневная футбольнаяclinicдляplayers/goalkeepersвсехуровней:техника/тактика, игровыеrole/командныеценности. Owncard1coach:14players иtechnicaldirector:72; не2Spanishcoachesвкаждоймалойгруппе.08–14пятьдней, родителинаблюдаютизотдельнойзоны. Completioncertificate не medal/академияRealMadrid; MadridExperienceнеавтоматическое продолжениеCR, FAQссылаетсянаUSparticipants. Робототехникинет.',
        '11–15 или18–22January2027 по собственным2027cards иhub; GSDфактическиGuácima/Alajuela, а маркетингSanJosé.',
        fee(2027,'Основнойпрайснепоказанвпрочитанных2027cards; first30registrations75USDoff не гарантированная цена. Sibling10%2/3ребёнку не автоматическиstacked.',
            'Футбольныйcourse/equipmentиsmallgroups; lunchFAQ говоритincluded дляfull-day, bringlistодновременноownlunch — конфликт. Diplomascompletion.',
            'ОбязательнаяAdidasформаshirt/shorts/socks покупаетсяотдельноSoccer.comпослерегистрации; прайснепоказан. Shoes/shinguards/water/sunscreen, личныемедрасходывышеpolicy, жильё/дорога отдельно.',
            'Отмена>90dayshold95USD,90–60days50%,последние60days0. Operatorcancelrefundwithin30days безtravelcoverage; weather/force-majeureafterstartrefundнеобещан. Instalmentsнеполнаяоплата; medical/mediawaiverчитан, не принят.'),
        'Дневнаяsportsclinic, безпансиона;familylogistics и фактическийязык нужны.',fit('conditional','Возраст5/6–17 подходит, место/язык/полнаяцена ещё нужны.'),fit('conditional','ВJan2027будет6–7;возрастcard/FAQрасходится, письменныйдопуск поDOB нужен.'),
        'Ближайший общий спортивный выбор с международнымбрендом; не STEMleague/teamadmission.',
        ['Письменныйage/language/foreignintake, полныйcampfee+mandatoryuniform, lunchconflict, места/contractточнойнедели.'],
        [src('2027hub/даты',RM),src('Week1точныйvenue/age/ratio',RM+'info-30-san-jose-2027'),src('Week2',RM+'info-31-san-jose-2027'),src('FAQuniform/meal/age/sibling',RM+'faq'),src('Legalcancel/medical/media',RM+'legal')],status='published_2027',sessions=[['2027-01-11','2027-01-15'],['2027-01-18','2027-01-22']])
    add('woods-amora-dominicalito','Woods of the World × Amora · NatureSummer','Коста-Рика','CRI','На территорииAmora,Dominicalito,CostaBallena','general,science,art','family','Campageнеобъявлен; USschool3–13 иCorcovado10–13/10–15/5–15 не допускDominicalito',unknown_language,
        'Конкретнаяcamp page:дети/семьи, outdoorlearningмеждуcanopy/river/shore,play/discovery/stories/exploration. SampledayWoods:math/language/outdoor/art/music/handcrafts/olderprojects, не обещаниеточногоcamp2027timetable. Corcovado3monthresearchи4dayfamilytour — разные соседниепрограммы, неJanuaryDominicalito. Roboticsнеобещана.',
        '4January–6February2027 подтверждаютWoodsиAmora; timeTobeset. Это seasonalwindow, неизвестныднипосещения/пакеты; не35daysпоследовательногоchildboarding.',
        fee(2027,'Fee/часовойplan/оплачиваемаядлительность не опубликованы. WaitlistAmoraдляпокупкидомов не campregistration/места.',
            'Структураinclusiveprogramme/pитания/оборудования/страховкипока неизвестна.',
            'Семейноежильё/доставка/дорога/parentparticipationрасходы не установленыпакетом.',
            'Camprefund/депозит/foreignintake/Englishsupport/DOB/graдeтребования ещё не опубликованы.'),
        'Familiesпрямо указаны, детскийпансион/ночнойsupervisionнепредложены; не подставлятьлоджCorcovado.',gradefit,gradefit,
        'Местный naturecandidateдляисследования; датыесть, пригодностьобоим/EN/стоимостьпоканеустановлены.',
        ['Возраст/DOB/реальныедни/часы, EN/ESпедагогов, fullfee/housing/parentpresence, campadmissionвместодомовойwaitlist.'],
        [src('WoodsотдельнаяDominicalitopage','https://www.woodsoftheworld.net/dominicalito'),src('КонкретныйAmoracamp/eventwindow','https://amora.cr/event/woods-of-the-world-summer-camp/'),src('Sampleday, не конкретныйtimеtable','https://www.woodsoftheworld.net/costa-rica/a-day-in-the-life'),src('Corcovadoотдельныйresearch/tour, смешанныевозраста','https://www.woodsoftheworld.net/costa-rica')],status='published_2027',sessions=[['2027-01-04','2027-02-06']])
    P[-1]['timing']['precision']='season_window'

    # Existing Classic preserved dates/ID; deepen transport, staff and cancellation.
    p=next(q for q in P if q['slug']=='makemake');p['checked']=CHECKED
    p['language_evidence_role']='primary'
    p['programme']+=' ClassicGrade7–8автоматическиLIT, не отдельнаяпокупка. Датированныйpage24/7supervisionratio1:4/residentnurse, English-speakingcounselors, teamgames/leadership. FAQforeigncampersисторическивтомчислеMexico/US/Canada; exactpassportintakeещёнеподтверждён. Teen/JuniorCounselorGrade9–11 отдельныеформаты, не младшимпообщему6–17age.'
    p['price']['included']='535 000CLP/6дней incVAT:camp/foodsnacks, activities/safetyequipment, tents, shirt/photos и round-tripprivatebusизSantiago прямоincluded.Оператор указывает круглосуточное сопровождение и ratio1:4. CurrentratesbusstopAv.FranciscoBilbao8000LasCondes; FAQLaReinaстарее/расходится. Автобусныхместменьшеcampplaces, место вbusподтвердить. Departurefirstday13:00/returnlastday13:00 поrates.'
    p['price']['deposit']='Refund2027:до20Dec2026 возвратминус21%tax/bank;после20Decтолькоseriousillness/injury/familyemergencyминус30%, илизаменаcampers. Ровно20Decнеразъяснено. Operatorcancelbeforestartfullrefund, emergencyearlyendпосленачала0/futurediscount0. Месторезервируюттолькопослеформы+payment, Страница говорит, что обычных скидок нет; отдельно опубликован вычет20 000CLP при самостоятельной доставке в обе стороны — исключение нужно согласовать.'
    p['questions'].append('Уточнитьbusместо/точныйstopLaReinavsLasCondes, границу20Decemberrefund иforeignдокументы; онлайнcampplacesнепредставлятькакгарантированнуюбронь.')
    p['sources'].append(dict(title='Конкретная2027refundpolicy',url=MAKE+'refund-policy',checked=CHECKED))
    add('makemake-teen','Camp Mákemáke · TeenCamp','Чили','CHL','Pelarco/Maule,Chile','general,languages,sport','boarding','Entering Iº–IIIºMedio / currentlyGrades9–11, не общий6–17',
        'DatedTeen2027page прямоEnglish-speaking; FAQallactivitiesEN/translationifneeded/allENlevels. ОсновнойEN, переводпо необходимости; отдельныйESteachingcurriculumнеобещан.',
        'Шестидневный outdoorleadership:походы,kayak/SUP/river tubing,farm,archery,teamchallenges,crafts/campfire/outdoorcooking/wildernessskills. ЭтоgeneralENprogramme,неrobotics/AI. ОтдельныйJuniorCounselorExperience предназначенreturnersGrades9–11; его FULL10–15Janне statusTeenCamp.',
        'Teen2027:17–22January и31January–5February. Отдельные20camp/busplaces; показанные16/15небронь.',
        fee(2027,'CLP535 000/6дней incVAT, тотжеlistedTeenpriceкакClassic; не независимыйпредполагаемыймировойrank.',p['price']['included'],p['price']['extras'],p['price']['deposit']),
        p['accommodation'],fit('later','Grades9–11—будущаясредняя/старшаяшкола; фактическийgradeпонадобится.'),fit('later','СтаршийteenGrade9–11, будущаяступень.'),
        'Английскаябудущаяleadershipступеньс собственнымage-grade/датами, не увеличивает список подходящихнынешнему6/9лету.',
        ['РеальныйGrade9–11, самостоятельность/English/foreignintake, campиbusplace, kit/refundточнойсмены.'],
        [src('DatedTeen2027dates/fee/inclusions',MAKE+'dates-and-rates'),src('English/foreignhistory/life',MAKE+'everything-you-need-to-know'),src('2027refundpolicy',MAKE+'refund-policy')],status='published_2027',confirmed=['EN'],sessions=[['2027-01-17','2027-01-22'],['2027-01-31','2027-02-05']])
    P[-1]['language_evidence_role']='primary'
    for p in P[start:]:
        p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        clean_profile(p)
    classic=next(q for q in P if q['slug']=='makemake')
    classic['programme']=readable(classic['programme'])
    for k in ['included','deposit']:classic['price'][k]=readable(classic['price'][k])
    classic['questions'][-1]=readable(classic['questions'][-1])

def extend_report_v90(report):
    shortlist_start=len(report['shortlist']);gap_start=len(report['gaps'])
    report['shortlist'].extend([
        dict(label='США · собственные роботы и точные2027смены',slugs=['star-carbots','star-ecobots','star-anibots','star-robot-gaming','robolabs-holiday'],reason='Датированные localrobotics/curriculum/прайс, реальныеgradegates. StarCodeEN/ES/RU не доказываетcampEN; USD399.75/461.25 ужес ticketfee. RoboLabs417/556fullили237/316half, threevenuesoneoperator. НуженGrade/язык/foreignintake, не обещаннаямеждународнаямедаль.'),
        dict(label='США · зимние и весенние школьные каникулы',slugs=['snap-greensboro-winter','snap-greensboro-spring','snap-greensboro-school-holidays','steamup-thanksgiving','steamup-winter','steamup-spring'],reason='SnapWinter3днянесмотряfour-dayintro,150/175USDfull;Spring5дней224/249. Kindergartenattending/selftoileting и staffcannotmedicate. STEAMUPwinter6actualdays, закрытыholidays,250startingнеall-in. EN/foreignadmissionпокаunknown; этоcitydayprogrammesнепансионы.'),
        dict(label='Коста-Рика · рядом с домом, разные цели',slugs=['woods-amora-dominicalito','avanza-real-madrid-cr','cloud-forest','wonder-camp','mount-view-camps','cenfotec-makers'],reason='AmoraNature4Jan–6Febwindowfamily,age/EN/feeещёнет; рядомCorcovadoresearch/tourнеэтотcamp. Avanzafootball11–15/18–22JanGSDAlajuela,формаотдельно/priceunknown/ageconflict; generalспортнеSTEM. СтарыеRoboticsкандидатысохранены, UCRinstructorcallнеchildregistration.'),
        dict(label='Латинская Америка · общий пансион2027',slugs=['santa-ursula-general','makemake','makemake-teen','replago-general','international-camp-br'],reason='SantaÚrsula7–15,51 700MXN7days/98 50014;Oscarтолькопосле7,EN не установлен; medical policy до150 000MXN, исключения отдельно. MákemákeEnglishClassicGrade2–8,535 000CLP6daysbusincluded/21%cancelhold; Oscargradeещёнужен. TeenGrade9–11будущий. Brazilсвойязык/даты/availabilityвдосье, нетобщего мировогоrank.'),
        dict(label='Канада · зимний coding по уровню',slugs=['stemrise-winter-roblox','stemrise-winter-ai','stemrise-winter-research','brainstem-winter-little','stemotics-winter','envision-winter-audit'],reason='STEMRiseRoblox7–13,AI9–16,Research12+;20Dec–10Janлишьseasonwindow, onsiteтолькоMarkham. Ценаquote/ENunknown/Chinesecontractprevails. ДляOscarпосле7-летия, Researchfuture. Существующиеwinterconflictsдругихоператоровсохранены.')
    ])
    report['gaps'].extend([
        dict(country='Канада / США',iso='CAN',provider='v90 · Tamwood / ILAC действующая доступность',detail='КэшпоискапродолжаетпредлагатьTamwoodSummer2027. Прямойтекущийtamwood.com/camps/перенаправляетнаilac.comсownnoticeceasedoperationseffectiveimmediately/allclassesandprogrammingcancelled/KPMGappointed/bankruptcyprotectionFridaySeptember18. Годвbodynoticeненапечатан, не добавленпо догадке. ILAC/Tamwoodдосье/событийвтекущейбазенет; новые2027кандидатыисключеныиз-заоперационногоnotice, не закрытдругойодноимённыйлагерь.',next_action='Не считатькэшнабором; проверятьобъявленияcurrentoperator/administrator. FunWithBotswinterClosed/HTTP406,Qwanoes/Kamin403не доказательство открытогонабора2027. Worldwideauditactive.',url='https://ilac.com/'),
        dict(country='США',iso='USA',provider='v90 · учебная тема, grade и настоящий язык',detail='Star5темoneacademy;Battle23–26vs23–27Novнетточногоevent,RobotGaming31Dec12vs15часовконфликт. Видимыйcurriculum/tickets/termsпрочитаны, ShowMorebrowserredirectblockedнеполныйплан. StarCode22languagesнеcampteaching. RoboLabs3venuesне3operators, BattleK–7summer2025неGrades1–12holidayadmission. Snap3daysvsfour-dayintro,kindergartencurrentlyattending/selftoileting/no staffmedication. STEAMUP5–15vs3–15,feesstarting/holidayclosures, VEXschoolменюнеcampmedal.',next_action='Настоящиеgrades/DOB/ENinstructors/foreignadmission, fullcurriculum/dayend, invoice/lunch/contract. Fullcountrycoverageнеутверждается.',url=STAR+'camps'),
        dict(country='Канада',iso='CAN',provider='v90 · STEMRise winterwindow и договор',detail='20Dec26–10Jan27seasonwindowнеежедневныйschedule,3возрастныхtracksодногооператора. ТолькоMarkhamonsite;3другихcitieswinteronline. Feequote/9.9trialнеcampfee, EnglishwebsiteнеENteaching. Camprefund5/20/25%условный, Chineseversionprevails; generalcourse50/100FAQнеcamp. MarketingUSACO/CCCrouteнеисторическийрезультат/Harvardadmission.',next_action='Фактическийcampcohort/address/язык/primaryChinesecontract/обязательныесборы, уровнии7/9/12agegate.',url=RISE+'camps/winter'),
        dict(country='Мексика / Чили',iso='MEX',provider='v90 · generalпансион2027 и язык/пакет',detail='Santa7–15andMXN51 700/98 500datedcards; home16–23vs17–23 иold2026heroнеподставлены. Internationalblogнетbilingualimmersion, medical24hнерасходывсёвключено:accident policy до150 000MXN, illnesses excluded. Cancel3dayboundaryconflict, телефонытольковебсообщения. MákemákeClassicGrade2–8приоритетнад6–17homepage, TeenGrade9–11future;Englishиbusincluded535 000CLPдоказаны,refundminus21%before20Dec26/30%limitedafter/20Decboundaryunknown.',next_action='DOBOscar/grade, языкSanta, окончательный invoice/transport/campplaces/contractграницы. Никакого универсального международногоrankнеприсвоено.',url=SANTA+'campamentos-de-verano'),
        dict(country='Коста-Рика',iso='CRI',provider='v90 · Amora Nature, футбол и UCRinstructorcall',detail='Amora/WoodsNature4Jan–6Feb27familieswindowtimeTBA; campage/EN/priceunknown. HomeUSschool3–13неcampage, соседнийCorcovado3month10–13/10–15/5–15и4dayfamilytourнеJanuarycohort. RealMadridAvanzaGSDGuácimaAlajuela11–15/18–22Jan27;page5–17vsFAQ6–17, fullpriceunknown/Adidasuniformотдельно, lunchincludedvsbringlunch. LanguagefromSpanishcoachesневыведен. UCR1Oct26ED-3331callfor2027instructorsнеchildcampregistration.',next_action='Новыеlocaltechnicalwinter/programmesдля6/9, реальныеgrades/DOB/EN/ES/foreignприём/fee/contract; весьмировойплан,Europe/Asia/школы/лиги/выставки/маршрутыactive.',url='https://amora.cr/event/woods-of-the-world-summer-camp/')
    ])
    for q in report['shortlist'][shortlist_start:]:
        q['label']=readable(q['label']);q['reason']=readable(q['reason'])
    for q in report['gaps'][gap_start:]:
        for k in ['provider','detail','next_action']:q[k]=readable(q[k])
