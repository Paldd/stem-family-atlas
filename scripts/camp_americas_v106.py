"""Selected dated American/Canadian programmes and a Spanish Mexican archive."""
CHECKED = '2026-10-05'
J = 'https://www.journeytosteam.com/'
S = 'https://steamupedu.com/'
E = 'https://explorationslearning.com/'
Z6 = 'https://www.zeffy.com/en-CA/ticketing/age-6-kindergarten-summer-camp-2027-next-year'
Z9 = 'https://www.zeffy.com/en-CA/ticketing/age-9-summer-camp-2027-next-year'
CANDIDATES = ['journey-winter-minecraft','journey-winter-robotics','journey-winter-mario','journey-winter-superheroes',
       'steamup-thanksgiving','steamup-winter','steamup-spring','kidnetix-winter','nova-mex-itclub',
       'explorations-break-tech','explorations-july-general','explorations-summer-tech']
NEW = [s for s in CANDIDATES if not s.startswith('steamup-')]

def add_americas_v106(add, src, fit, profiles):
    day = 'Дневное посещение; ночлег семьи, дорога, перелёт и семейная страховка отдельно.'
    ask = 'До поездки подтвердить конкретные места, точный возраст на старт, иностранный индивидуальный приём, язык своего преподавателя и полный счёт. Заявки и оплаты не отправлялись.'
    lang = 'Язык преподавателя прямо не установлен в прочитанной программе; английский сайт и американский/канадский адрес не заменяют доказательство EN обучения.'
    def emit(*args, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1];p['checked'] = CHECKED
        for s in p['sources']:s['checked'] = CHECKED
        return p
    def variants(p, rows):
        p['timing']['session_details'] = rows
        assert p['timing']['sessions'] == [[v['start'],v['end']] for v in rows]
    refund = 'Политика от20сентября2026: отмена до15дней — возврат минус35USD; FAQ говорит больше15дней. Ровно15дней уточнить; внутри окна/за пропуски возврата нет. Медицинское исключение по усмотрению; перенос другому участнику≥7дней и возможные сборы. Один weathercancel не возвращается; отмена организатором — полный возврат.'
    jsources = [src('Winter2026: реальные темы, часы, возраст и даты',J+'winter-break-camps'),src('FAQ: материалы, сервисный сбор, надзор',J+'faqs'),src('Договор:35USD и граница15дней',J+'refund-policy')]
    for slug, title, place, ages, themes, start, end, hours, regular, early, programme, oscar in [
        (CANDIDATES[0],'Minecraft Coders','Firstenburg Community Center · Vancouver, Washington, USA','7–11','coding,games','2026-12-21','2026-12-23','09:00–12:00',219,199,'Minecraft и код; создание проекта, проверка и финальная демонстрация семье. Точная версия/среда и распределение3дней требуют отдельного учебного плана.',fit('later','В декабре2026 Оскару5–6, минимальные7 ещё не достигнуты.')),
        (CANDIDATES[1],'Intro to Robotics: Amazing Amusement Park','Firstenburg Community Center · Vancouver, Washington, USA','6–10','robotics,coding,engineering','2026-12-28','2026-12-31','09:00–12:00',289,269,'Сборка и программирование LEGO/роботов для парка аттракционов: придумать, протестировать движение и показать результат семье. По общему campописанию робот реагирует/двигается; конкретный набор и4дневный syllabus не раскрыты.',fit('conditional','Только после6-летия к28декабря2026. Возраст5 не допускается автоматически.')),
        (CANDIDATES[2],'Super Mario Game Makers','Firstenburg Community Center · Vancouver, Washington, USA','7–12','coding,games','2026-12-28','2026-12-31','12:00–15:00',289,269,'Проектирование игры по темеSuperMario и демонстрация семье; язык кода/платформа и проект каждого ребёнка уточнить. Название игры не означает готовую международную олимпиаду.',fit('later','До7лет недоступно; в декабре2026 ещё5–6.')),
        (CANDIDATES[3],'LEGO Superheroes','Bricks & Minifigs · Beaverton, Oregon, USA','6–10','engineering','2026-12-28','2026-12-31','09:00–12:00',249,229,'Инженерные LEGO конструкции по темеSuperheroes, тестирование и показ семье. Доля именно программирования/роботов для этого трека ещё не раскрыта; не обещаем полный курс кодинга.',fit('conditional','Нужно6лет на28декабря2026; точный день рождения не известен.'))
    ]:
        p=emit(slug,'Journey to STEAM · '+title,'США','USA',place,themes,'day',ages,lang,
            programme+' Максимум20участников; внутри группы по возрасту, младшим больше помощи — собственные заявления организатора.',
            start+'–'+end+'; '+hours+' America/Los_Angeles. Это3/4коротких учебных дня, не пансион.',
            dict(year=2026,label=f'USD{regular} за курс; ранняя цена{early} до2ноября2026.',included='LEGO, роботы, Chromebooks и учебные материалы предоставляет организатор; свой ноутбук не требуется поFAQ.',extras='Зимняя страница обещает точную checkoutцену, FAQ добавляет enropsservicefee: величина неизвестна. Питание и gearнавынос не установлены; полный счёт подтвердить.',deposit=refund),day,
            fit('conditional','Возраст8–9 входит в конкретную группу; подтвердить текущий уровень, язык и наличие места.'),oscar,
            'Конкретный краткий технический маршрут на зимние каникулы; семейная пригодность зависит от возраста и языка, региональные отзывы не мировой рейтинг.',
            [ask,'Разрешить сервисный сбор и границу15дней отмены; предметный syllabus/еда/возрастной подгруппой.'],jsources,status='published_2026',priority=['technical'])
        p['timing']['sessions']=[[start,end]]
        variants(p,[dict(start=start,end=end,label=title+' · '+hours,price=f'USD{regular} / early{early} до2ноября; servicefee неизвестен',place=place,source=J+'winter-break-camps',date_scope='day_camp_window',proof='Собственная winter2026 таблица подтверждает конкретный курс/место/дни; скидочная дата не дедлайн регистрации.')])

    p=emit(CANDIDATES[7],'Kidnetix · Winter General Camp','Канада','CAN','10 Bramhurst unit13 · Brampton · Ontario','general,art,engineering','day','4–12',lang,
        'Игры, творчество, прогулки и зимние темы. Формулировка may build LEGOrobotics означает возможную опцию, не обязательный ежедневный курс роботов. Общий дневной лагерь, не технический интенсив и не независимый мировой топ.',
        '21–31декабря2026;08:30–16:30. Точные дни посещения и Christmasзакрытие не раскрыты; не обещаем все11календарных дней.',
        dict(year=2026,label='CAD175/2weeks EARLYBIRD по winterстранице; регулярный тариф/граница скидки неизвестны.',included='Программа общего лагеря; гарантированный набор robotics, еда/kit/страховка не установлены.',extras='Полный состав2weeks, care и возможные сборы уточнить; дорога/жильё отдельно.',deposit='Размер аванса и отмена не раскрыты в прочитанной странице.'),day,
        fit('conditional','Возраст8–9 входит4–12; техническую нагрузку не обещаем.'),fit('conditional','5–6 входит4–12; подтвердить подгруппу/инструкции.'),
        'Недорогой опубликованный общий кандидат для обоих рядом с Торонто; отобран по доступности и возможной LEGOопции, а не статусу лучшего лагеря.',
        [ask,'Подтвердить фактические дни/праздники, regular/earlyprice, язык и реальное расписание робототехники.'],[src('Winter2026 — программа, часы и earlyprice','https://www.kidnetixkidz.org/program/winter-camp')],status='published_2026',priority=['both','general'],sessions=[['2026-12-21','2026-12-31']])
    variants(p,[dict(start='2026-12-21',end='2026-12-31',label='Общий winter · дни уточнить',price='CAD175/2weeks earlybird; срок/regular неизвестны',place=p['place'],source=p['sources'][0]['url'],date_scope='day_camp_window',attendance_weekdays=[])])

    emit(CANDIDATES[8],'NOVA Academy México · IT Club','Мексика','MEX','Gauss12 · Chapultepec Morales / Verónica Anzúres · Miguel Hidalgo · CDMX','robotics,coding,games,engineering,art','day','8–12 /12–15; общая карточка8–15.',
        'В карточке прямо Español. Английский преподаватель не подтверждён.',
        '5тематических недель: программируемые LEGOEducationPrime, RobloxStudio, Minecraftконструирование, PixelArt, моделирование и3Dпечать; старшей группе VR/web/video. Материалы организатора, свой lunch. Учебные Minecraftсоревнования не международные награды.',
        'Основной текст ITClubdeVerano2025 с21июля, MonFri09–13 или14–18. Карточка смешивает название Invierno/EstadoMéxico с адресомCDMX; ни winter2026–27, ни summer2027 не подтверждены.',
        dict(year=2025,label='На той же странице1400зачёркнуто/1000 и1semana, но валюта/сезон цены не согласованы. Не считать1000 действительным прайсом2027 или подтверждённымиMXN.',included='Учебные материалы по описанию2025; LEGO/оборудование на вынос не обещаны.',extras='Lunch ребёнок приносит сам; дорога/жильё/новый2027счёт отдельно.',deposit='Отмена, аванс и новый сезон не установлены; формы сайта не заполнялись.'),day,
        fit('conditional','8–10 соответствует младшей8–12, но нужен новый конкретный сезон.'),fit('later','Минимум8лет; в2026–27 Оскару5–7.'),
        'Испанский технический кандидат Матвею в стране гражданства; архивный syllabus полезен для сравнения, не выдуманная будущая смена.',
        [ask,'Новые даты2026–27, город/кампус, валюта/единица тарифа, техника и refund.'],[src('Собственная карточка с архивом2025 и явнымEspañol','https://mexico.nova-academy.mx/it-camp')],status='archive_next_unannounced',priority=['technical'],confirmed=['ES'])

    erefund='Письменная отмена≥10дней минус10%admin по политике; возврат позже не обещан. Extended16–18 +60CAD/неделю или25/день; после18 +5CAD/минуту. Увольнение по трём поведенческим предупреждениям без возврата. Применимость общих правил к2027 подтвердить.'
    esources=[src('Своя registration: конкретные годы2026–27 и меню возрастов',E+'registration/'),src('Winter/Spring: технические темы и цены',E+'school-break-camps/'),src('Договор, питание и care',E+'our-policies/'),src('Rates2026: не новый2027 прайс',E+'rates/')]
    p=emit(CANDIDATES[9],'Explorations Montréal · Winter / Spring Tech','Канада','CAN','Learning Lab · 6591Somerled · NDG · Montréal','robotics,coding,games,engineering','day','Tech7–15; возраст на первый день, не возраст в календарном году.',lang,
        'Winter: Robotics +VideoGameDesign. Spring:3DPrinting +VideoGameDesign. Это два разных тематических недельных варианта. Программа arts на той же странице8+ имеет конфликт «afternoons» с полными часами: не включена как доказанный полный технический день.',
        'Winter28декабря2026–1января2027; Spring1–5марта2027 по текущейregistration. Dropoff08–09 против08:30–09 в dailycopy, pickup15:30–16; фактический режим/праздники уточнить.',
        dict(year=2027,label='SchoolbreakTech CAD485/неделю; регистрация даёт2027год, общийrates ещё2026.',included='Тематические занятия; детали robot/3Dkit и выдача вещей не установлены. Lunch/snacks свои, nut-free.',extras='Care/путь/жильё;10%2+sessions по rates2026, применимость2027 не подтверждена.',deposit=erefund),day,
        fit('conditional','Возраст8–10 входит7–15; подтвердить actualgroup и язык.'),fit('conditional','Winter2026 до7 недоступен; Spring2027 только если7лет уже на1марта.'),
        'Реальные ближайшие недельные techварианты с собственными датами; зимняя робототехника и весенняя3Dпечать разделены.',
        [ask,'Разрешить праздничные дни/dropoff/ENteacher, договор и полный счёт2027.'],esources,status='published_2026_27',priority=['technical'],sessions=[['2026-12-28','2027-01-01'],['2027-03-01','2027-03-05']])
    rows=[]
    for start,end,label in [('2026-12-28','2027-01-01','Winter ·Robotics +VideoGameDesign'),('2027-03-01','2027-03-05','Spring ·3DPrinting +VideoGameDesign')]:
        ff=dict(p['family_fit']);ff['oscar']=dict(status='later' if start.startswith('2026') else 'conditional',detail='До7лет в зимнюю смену нельзя.' if start.startswith('2026') else '7лет к1марта2027; день рождения нужен для допуска.')
        rows.append(dict(start=start,end=end,label=label,price='CAD485/неделю; careотдельно',place=p['place'],source=E+'registration/',date_scope='day_camp_window',attendance_weekdays=[],family_fit=ff,proof='Год/неделя из currentregistration, тема/485 из собственной SchoolBreak; ежедневные праздничные исключения ещё не раскрыты.'))
    variants(p,rows)

    p=emit(CANDIDATES[10],'Explorations Montréal · July General / Junior','Канада','CAN','Kells Academy · 2290Cavendish / вход6645deMaisonneuve · Montréal','general,science,engineering,art,nature','day','Age6 отдельно kindergarten/grade1completed;7/8–9/10–11 и старшие меню. Выбирать реальный возраст на первый день.',lang,
        'Разнообразная программа Kells: младшим заранее подобранные занятия/природа/творчество, старшим разные активности. СтраницаExplorer6–7 ещё2026, поэтому её coding/robotics примеры не гарантируют ежедневные роботы2027. Своё заявление о малом ratio не независимая аккредитация.',
        '5–16 и19–30июля2027 — две реальные2недельные смены. Age6kindergartenZeffy:dropoff08–08:45, pickup15:30–16, care16–18. Старые даты6–17/20–31июля2026 не переносим.',
        dict(year=2027,label='CAD785/2недели подтверждено реальными меню age6kindergarten и age9. Для6летпослеgrade1 /age7 /age10 свой тариф ещё проверить.',included='Общая дневная программа; foodприносить. ВидимыйAdd не означает бронь/наличие места.',extras='Care и fullinvoice; возможный добровольный donation наZeffy не обязательная плата, ничего не добавляли.',deposit=erefund),day,
        fit('conditional','Летом2027 возраст9–10; age9 меню785 прочитано, для10 отдельная группа/счёт.'),fit('conditional','Летом6–7; для6 kindergarten785 подтверждено, completedgrade1/7 отдельный menu. Класс не известен.'),
        'Конкретный общий научно-творческий дневной маршрут обоим с возрастной развилкой, не самостоятельный пансион.',
        [ask,'Определить actualage/grade и новое2027 расписание, instructorlanguage, meal/kit/полные возвраты.'],[esources[0],src('Реальное publicage6kindergarten меню2027',Z6),src('Реальное publicage9 меню2027',Z9),src('Explorer: старые2026 примеры и возрастные правила',E+'explorer-program-ages-6-7/'),esources[2],esources[3]],status='published_2027',priority=['both','general'],sessions=[['2027-07-05','2027-07-16'],['2027-07-19','2027-07-30']])
    variants(p,[dict(start=a,end=b,label='JulyGeneral ·2недели',price='CAD785 за2недели age6kindergarten/age9; другие группы уточнить',place=p['place'],source=Z6,date_scope='day_camp_window',attendance_weekdays=[]) for a,b in p['timing']['sessions']])

    weeks=[('2027-06-28','2027-07-02','VideoGameDesign +3DModellingPrinting',445),('2027-08-02','2027-08-06','VideoGameDesign',445),('2027-08-09','2027-08-13','VideoGameDesign',445),('2027-08-16','2027-08-20','Robots &Engineering',445),('2027-08-23','2027-08-27','3DPrinting &Engineering',545)]
    p=emit(CANDIDATES[11],'Explorations Montréal · Summer Tech Weeks','Канада','CAN','Learning Lab · 6591Somerled · NDG · Montréal','coding,games,robotics,engineering','day','Tech7–15 в общеминдексе; реальное age9 меню2027 прочитано. Другие возраста/uppergroup проверить.',lang,
        '5отдельных недель: игры/3D; две игровые; robots/engineering;3D/engineering. Тема конкретной недели важнее общего roboticsтега. ВозрастныеZeffy меню не обещают одинаковый kit/курс любому6летнему.',
        '28июня–2июля;2–6,9–13,16–20,23–27августа2027. Summerheader2026 против нового registration2027 разрешён текущим ownlinkedZeffy menu; новые даты не вычислялись по прошлому году.',
        dict(year=2027,label='Age9: CAD445 за первые4недели по отдельности, CAD545 за23–27августа. Старыйrates2026/445не заменяет реальный последний545.',included='Выбранная техническая неделя; foodсвой. Robot/3Dgearнавынос/ownlaptop не установлены.',extras='Care/fullage-specificinvoice/свойночлег. Donation добровольный, не добавлялся.',deposit=erefund),day,
        fit('conditional','Летом9–10; age9 цена подтверждена, группа10 нуждается в отдельном меню.'),fit('conditional','Только после7лет к конкретному понедельнику; до7 общий Junior, не гарантированныйTech.'),
        'Конкретные тематические недели для выбора по проекту; robotics16–20августа и3D23–27августа с разной ценой.',
        [ask,'Новый полныйsyllabus, точная площадка/часы, age7/10, язык/kit/наличие мест и полный счёт.'],[esources[0],src('Настоящее age9 publicменю2027: темы/445/545',Z9),esources[2],esources[3]],status='published_2027',priority=['technical'],sessions=[[a,b] for a,b,_,_ in weeks])
    variants(p,[dict(start=a,end=b,label=label,programme=label+'; индивидуальный проект/kitуточнить',price=f'CAD{price}/неделя дляage9; свой возраст отдельно',place=p['place'],source=Z9,date_scope='day_camp_window',attendance_weekdays=[],proof='OwnlinkedZeffy publicage9 меню прямо2027/конкретная тема/тариф; noAdd/noContinue/noform.') for a,b,label,price in weeks])

def extend_report_v106(report):
    report['shortlist'].extend([
        dict(label='США · короткие зимние технические проекты',slugs=NEW[:4],reason='Journey:21–23/28–31декабря2026,LEGOроботы и игры. Матвею подходящий возраст; Оскару6+ только после6лет,7+ недоступно зимой2026. Материалы/Chromebooks свои у лагеря; ENteacher и servicefee ещё уточнить.'),
        dict(label='США · дневные STEMканикулы без закрытых праздников',slugs=['steamup-thanksgiving','steamup-winter','steamup-spring'],reason='STEAMUPOrlando:4дняThanksgiving,6днейwinter и5днейSpring2027. Вcalendarнет24/25/31Decи1Jan. Winterреальныйдедлайн15Nov; from250неполныйсчёт зимы. Оба по5–15 подходят, ENнеустановлен.'),
        dict(label='Монреаль · выбрать общую или конкретную технику',slugs=NEW[6:],reason='JulyGeneral5–16/19–30Jul2027 с785дляage6kindergarten/9. Winterроботы,Spring3D; summerRobots16–20Aug445,3D23–27Aug545дляage9. ОскаруTechтолькопосле7, собственныйgrade/ENteacher/10-летнийтариф ещё нужны.'),
        dict(label='Мексика /Канада · честные общие и архивные кандидаты',slugs=NEW[4:6],reason='NOVAexplicitES/8+LEGOPrime/Roblox/3D, ноосновнойsyllabus2025/новые сменыunknown. Kidnetix4–12/175CADearlyза2weekswinter2026, roboticsлишьmayопция; не выделяем как гарантированныйтехническийинтенсив или мировойтоп.')
    ])
    report['gaps'].extend([
        dict(country='США',iso='USA',provider='Journey · точная сумма и возраст зимнего курса',detail='Winter2026таблица219/289/249, early−20доNov2; FAQдобавляет enropsservicefee при обещании winterexactcheckout. Refundpolicyдо15противFAQ>15;35adminодин, неповторно. 7+трек Оскару2026нельзя,6+последню рождения; город VancouverWashingtonнеCanada. ENteacherнепрямо подтверждён.',next_action='Полный счёт/границаотмены/DOB/учебный syllabus иязык; не превращатьearlyценувдедлайн.',url=J+'winter-break-camps'),
        dict(country='США',iso='USA',provider='STEAMUP · повторно подтверждённые праздники, цена и комплекты',detail='СуществующиеCP585–587 сохраненыбезповторныхкарточек/ICS. Шапка5–15противbody3–15; взят5–15. ThanksgivingзакрытNov26, winterDec24/25/31/Jan1,6attendanceдней. From250безединицызимы/осени, spring250заweekexplicit. Care84/week,late1.85/min,10%старшемусibling. WinterNov15actualregistrationdeadline; не всеобщаяшкольнаяVEXпобеда лагеря.',next_action='Общий seasoninvoice, meals/ownlaptop/kit/care/insurance/EN/численныеrefund, а не inventedпакет250.',url=S+'camp-winter-stem.php'),
        dict(country='Канада',iso='CAN',provider='Explorations · собственные годы и возрастные меню',detail='Registrationпрямо2027, footerAmiliaстарый,currentZeffyсвой. Age6kindergarten/age9по785/2weeksJuly, age9Aug23–27Tech545против445старогоrates2026. Explorerстраницаещё2026,EN/FRwebнеteacherproof. Tech7+vsjunior6gradeразвилка,dropoff08–08:45vs08–09vs08:30–09. Winterholidayattendance/новыйsyllabusещёнужны.',next_action='Свойage6completedgrade1/7/10тариф, точныйEnglish/Françaisteacher, расписание/kit/nightnotboarding/2027договор. PublicZeffyпрочитанбезAdd/Continue.',url=E+'registration/'),
        dict(country='Канада',iso='CAN',provider='Kidnetix /Envision · не гарантированные роботы и старый checkout',detail='KidnetixmayLEGOнеобязательныйrobotкурс,175CAD2weeksearlyбезdeadline/Christmasattendance. EnvisionсуществующееCP299сохранено: winterindex21–24/28–31Dec2026противproduct22–24/29–30безгода; Marchindex15–19Mar2027противproduct16–20Mar2026. Старыйproduct/timesнепереименованвновую смену.',next_action='Новые согласованныеproductdocuments иреальныеEN/младшиегруппы/прайсы/refund; дубликатыcampcardsне создавать.',url='https://envisionrobotics.com/stem-camps-for-kids-markham/'),
        dict(country='Коста-Рика /Мексика',iso='CRI',provider='FOD /NOVA /PYROX · регулярное, архивное и каникулярное',detail='FODcurrentofertaлишьучебныепилларыбезactual2027campfee/dates; ранее курсыневыданызаcamp. NOVAявныйES/8–15/архив2025сwintertitle/1000безвалютыиактуальногогода. PYROXFRC10225secondary/highschool/outreachNASAmentionsнеopencamp6/9лет2027. Noactualfee/intakeизмаркетинговогоimpact.',next_action='НовыйESканикулярныйseason/детальныеcurricula/счёты/gear/admission, продолжитьлокальныеCR/MXиLatinAmerica. Отсутствиефактоввэтихстраницахнеотсутствиевсехлагерей.',url='https://fod.ac.cr/oferta-formativa/'),
        dict(country='Мир',iso='USA',provider='v106 · полнота и переносимая база',detail='SelectedUS/Canada/MexicoнеполныйаудитАмерик. RoboThinkNexusactualHTTPтолькоJSshell; cachedsearchdatesнеconfirmedcohort. ВсеШвейцария/Франция/Испания/Европа/Азия/US/CAN/CR/MX/LATAMиschools/results/leagues/exhibitions/routesсохраняются.0полностьюпроверенныхстран. ZIPполнойSQLiteбезпотеристрочекснимаетstaticfilelimitбезсокращенияцели.',next_action='Продолжатьactualownprogrammes2026–27/general/STEM/day/boarding/ENESRU иполныеfamilyinvoices. Упаковкасверяетсяпобайтно, не удаляет программырадиразмера.',url='https://stem-family-atlas.poetic-trail-9407.chatgpt.site/#camps')
    ])
