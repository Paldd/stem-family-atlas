"""Primary curriculum, seasonal contracts and family gates; no inferred camp year."""
CHECKED='2026-10-05'
EVER='https://www.evergreen-hakuba.com/'
GSA='https://school.gsacademy.com/en/season_en/'
SOR='https://www.sor.com.sg/september-holiday-program-2026'
CT='https://www.computhink.com.sg/'
IRO='https://www.irobo.com.tw/'
NTUE='https://clec.ntue.edu.tw/p/404-1018-57247.php?Lang=zh-tw'

def add_asia_v89(add,src,fit,P):
    start=len(P)
    def price(year,label,included,extras,deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def later(text):return fit('later',text)
    def detail(p,rows):
        p['timing'].update(sessions=[[r['start'],r['end']] for r in rows],session_details=rows,variant_keyed=True)
    def row(a,z,key,label,cost,url,place,scope='camp_session',weekdays=None):
        q=dict(start=a,end=z,variant_key=key,label=label,price=cost,source=url,place=place,date_scope=scope)
        if weekdays is not None:q['attendance_weekdays']=weekdays
        return q
    # Preserve the existing Tech dossier and its legacy relation; the magazine is 2026, not summer2027.
    p=next(p for p in P if p['slug']=='typa');p['checked']=CHECKED
    p['programme']='Atomic × TYPA Summer Tech 2026: rising Grades1–2 Curious Explorers — лёд, движение/материалы, простые механизмы/электрические цепи, безопасные реакции. Grades3–4 Creative Problem Solvers — строить/программировать простых роботов, датчики/моторы/свет, экосистемы/энергия. Themes Arctic Explorers, Time Travellers, Sorcery School чередуются по классу / неделе. Grades5–8 Confident Young Engineers — открытые инженерные проекты, собственные машины/механика, физика и safety logic; Future Machines, Fantastic Contraptions, Amusement Park Engineering. Это разные возрастные задания, не одинаковый робототехнический интенсив для всех. 09–16 понедельник–пятница, обед; вторая неделя 15–18 июня, четыре дня. Требуются членство и иностранный паспорт; TAS/Tiger Tots имеют приоритет. 2027 ещё не объявлен.'
    p['sources'].append(dict(title='Собственный журнал 2026–27: Tech curriculum и именно Summer2026, страницы 76–77',url='https://www.typa.org.tw/wp-content/uploads/2026/03/TYPA-2026-27-Magazine_20260319-update.pdf',checked=CHECKED))
    p['questions'].append('Журнал 2026–27 содержит Summer2026; новая летняя матрица 2027/класс/часы конкретного robotics-проекта и язык ещё нужны. Week2 архива 15–18 июня — четыре дня по тому же недельному прайсу.')

    eplace='The Alps View Hotel, Tsugaike / Otari, Hakuba Valley, Nagano, Japan'
    elang='FAQ: общение, организация и работа лагерей на EN; летом возможна JA-помощь и двуязычное объяснение безопасности, не постоянный перевод. Зимой EN требуется для активного участия. Это основной язык общего/outdoor лагеря.'
    ehouse='Alps View Hotel только для campers, до 4 детей в комнате с санузлом, круглосуточное сопровождение. Братьев/друзей одного пола стараются разместить вместе, но не гарантируют. На маршрутах с ночёвкой часть проживания в палатках или mountain huts.'
    ecancel='Собственный camp contract: за 0–6 дней удержание 100%, за 7–13 дней 50%; более 2 недель JPY15 000/person. Граница ровно 14 дней сформулирована неоднозначно. Перенос: более 2 недель 10 000, за 7–14 дней 20%, за 0–6 дней 50%, только тот же сезон/места; более дешёвый вариант без возврата разницы. Дополнительные услуги за 0–3 дня невозвратны. Ранний отъезд/опоздание без возврата; при отмене оператором возвращают camp fee, не сопутствующие расходы.'
    equestions=['Подтвердить набор, места, возраст на начало, уровень самостоятельности/велосипеда/водных активностей и аллергию.','Получить полный счёт с трансфером, страховкой/своим оборудованием и точную границу отмены 14 дней. Не переносить расписание/цену 2026 на 2027.']
    winter='evergreen-hakuba-winter'
    add(winter,'Evergreen Hakuba · White Horse Winter Snowsports','Япония','JPN',eplace,'general,sport','boarding','8–15',elang,
        'Пять дней/четыре ночи лыж или snowboard, снежные прогулки, igloo, командные игры и вечерние активности. Лыжи для всех уровней; наличие snowboard-группы нужно запросить. Образец дня:09:30–12 и 13–15:30 катание, остальное питание/перерывы/игры. Welcome Pack26–27: звонок родителям 17:30–18 только в 1-й и 3-й день; остальное время устройства хранят staff. Для обычных звонков нужен свой телефон, сотрудники свой не дают; экстренная связь через management. Лекарства передают staff с EN-инструкцией, не самостоятельный приём. Робототехника не заявлена.',
        '14–18 декабря 2026 или 2–6 января 2027. Даты одинаково подтверждены страницей и Welcome Pack26–27.',
        price('2026–27','JPY175 000 база/5 дней. С обычным elementary lift pass24 400:199 400; со standard rental11 220, jacket+pants6 550 и helmet4 730:221 900/ребёнок до 13 лет до трансфера/прочего. Свой шлем разрешён.',
              '4 ночи, питание, программа/уроки, местные перемещения и помещения. Не путать локальный транспорт с дорогой из Tokyo.',
              '4-дневный lift: elementary24 400, middle-school+34 800. Прокат ski/snowboard+boots(+poles): до 13 лет standard11 220/premium13 560, 14+17 300/21 975; jacket или pants до 13 лет 3 275/item, 14+7 015; helmet4 730 либо свой. Gloves/goggles не сдаются в аренду. Tokyo chaperonedbus отдельно, сумма не раскрыта; родители в нём не едут. Перелёт, travel insurance/въездные документы отдельно. Независимый KidsSeasonPass1 800 для 7–12 ограничен и оформляется отдельно; не принят как гарантированная скидка.',ecancel),
        ehouse,fit('conditional','8–10 лет зимой 26–27: возраст 8–15 подходит; лыжная группа, место и готовность жить без родителей ещё нужны.'),later('Зимой 26–27 будет 6–7, ниже 8 лет даже после 7-летия.'),
        'Подробно проверенный общий английский зимний пансион для Матвея; для Оскара пока нужен другой формат. Часы и итоговая стоимость прозрачнее базовой рекламной цены.',equestions,
        [src('Даты, возраст и отдельные зимние доплаты',EVER+'winter-kids-camps/'),src('Welcome Pack26–27: даты, связь и бытовые правила',EVER+'wp-content/uploads/Winter-Camp-Welcome-Pack-26_27.pdf'),src('FAQ: EN и комнаты',EVER+'faq/'),src('Camp contract: отмена/перенос/иностранные участники',EVER+'terms-and-conditions/')],status='published_2026_27',confirmed=['EN'],sessions=[['2026-12-14','2026-12-18'],['2027-01-02','2027-01-06']])
    P[-1]['language_evidence_role']='primary'
    for i,(a,z) in enumerate(P[-1]['timing']['sessions'],1):
        P[-1]['timing'].setdefault('session_details',[]).append(row(a,z,'winter'+str(i),'5 дней/4 ночи · лыжи, snowboard запросить','JPY175 000 база; elementarypass24 400 и прокат/дорога отдельно',EVER+'winter-kids-camps/',eplace))
    summer=[
        ('ninja','Nagano Ninjas','7–8','Походы, canoeing/SUP/lake rafting, велосипед, творчество, slackline и задачи команды. Образец: первый день river walk, далее trail/canoe, treasure hunt/lake rafting, crafts/SUP, затем bike и итог.','175 000','NN_5_Day_Timetable_2026.pdf','29Jun–3Jul;13–17Jul;20–24Jul;3–7Aug;10–14Aug;17–21Aug',False),
        ('mountain','Mountain Masters','9–12','Экосистемы гор/леса, велосипед, ориентирование, tree climbing. Пример 5 дней: lake rafting/SUP, mountainbike, Tsugaike nature hike/bouldering, campfire/quiz.','175 000','MM_5_Day_Timetable_2026.pdf','29Jun–3Jul;20–24Jul;3–7Aug',False),
        ('water','Water Wizards','9–12','Озёрные/речные исследования, canoe/SUP/raft building, походы, river rafting, campfire. Пример: lake rafting, Shionomichi hike, речной rafting, SUP/истоки Himekawa.','175 000','WW_5_Day_Timetable_2026.pdf','13–17Jul;27–31Jul;10–14Aug;17–21Aug',False),
        ('earth','Earth Explorers','9–12','Природа/экология и outdoor craft: установка палаток, укрытие, огонь и готовка; bicycle/riverrafting/SUP/treeclimbing. Одна ночёвка в палатке+3 в отеле, не 5 ночей.','175 000','EE_5_Day_Timetable_2026.pdf','20–24Jul;17–21Aug',False),
        ('leader','Japan Alps Adventure Leadership','13–17 в описании; 13–16 в Details — конфликт','SUP, canyoning, mountainbike и речная экспедиция с одной палаточной ночёвкой; совместная готовка/лидерство. Базовая ступень перед Japan Alps Expedition.','185 000','JA_5_Days_Time_Table_2026.pdf','29Jun–3Jul;13–17Jul;27–31Jul',True),
        ('expedition','Japan Alps Expedition','13–17','Продолжение для уже прошедших 5/10-dayLeadership: отдельная 8-dayextension или объединённые 12 дней/11 ночей. Трёхдневный alpine trek/mountain huts, climbing/abseiling, mountainbike, командное планирование. Sample2026 допускает joining day5 после JA Adventure в последние 3 года, самостоятельное прибытие Omachi station; перенос этих условий на 2027 отдельно подтвердить. Смена 12 дней включает базовый Leadership, не 12+5 дней.','259 000/8 дней extension; 444 000/12 дней combined','JA_12_Days_Time_Table_2026.pdf','31Jul–7Aug extension;27Jul–7Aug combined',True),
    ]
    for slug,name,ages,content,cost,pdf,dates,future in summer:
        mat=later('Будущая ступень 13+; оба ребёнка ниже минимального возраста.') if future or slug=='ninja' else fit('conditional','В 2027 будет 9–10, подходит 9–12; новое лето 2027, место и самостоятельность ещё нужны.')
        if slug=='ninja':mat=later('В 2027 будет 9–10: выше группы 7–8; сравнивать 9–12.')
        osc=later('Ниже 9/13 лет этой группы.') if slug!='ninja' else fit('conditional','Летом 2027 будет 6–7: только после 7-летия, точная дата рождения нужна; новые смены ещё не объявлены.')
        add('evergreen-hakuba-'+slug+'-board','Evergreen Hakuba · '+name+' · пансион','Япония','JPN',eplace,'general,science,sport','boarding',ages,elang,content,
            'Текущая летняя страница и связанные образцы 2026: '+dates+'. Это архивные/образцовые периоды; лето 2027 не объявлено, в календарь 2027 не скопированы.',
            price(2026,'JPY'+cost+' / выбранная летняя программа 2026; цена 2027 не объявлена.',
                  'Для 5 дней:4 ночёвки, питание, основные активности/местные перемещения и учебное оборудование. Expedition и палаточные ночёвки по выбранному маршруту.',
                  'Tokyo chaperonedtrain/bus отдельно для всех смен; Nagoya только указанные 3–5. Стоимость дороги не опубликована. Собственная travelinsurance, перелёт, дополнительные вещи и карманные деньги отдельно; наборами техники в подарок не является.',ecancel),
            ehouse,mat,osc,'Проверенный общий английский outdoor-кандидат: содержание и прогрессия по возрасту, без заявления мирового рейтинга/соревновательной робототехники.',equestions,
            [src('Возраст/содержание/летние тарифы',EVER+'summer-camps/'),src('Связанный образец расписания 2026, не гарантированный 2027',EVER+'wp-content/uploads/'+pdf),src('FAQ: основной EN, самостоятельность и размещение',EVER+'faq/'),src('Camp contract, отдельно от условий tours',EVER+'terms-and-conditions/')],status='published_2026',confirmed=['EN'])
        P[-1]['language_evidence_role']='primary'
    for slug,name,ages,periods in [('ninja','Nagano Ninjas','7–8','3–7 и 10–14 августа'),('mountain','Mountain Masters','9–12','3–7 августа'),('water','Water Wizards','9–12','10–14 августа')]:
        add('evergreen-hakuba-'+slug+'-day','Evergreen Hakuba · '+name+' · дневной','Япония','JPN',eplace,'general,science,sport','day',ages,elang,
            'Английский дневной outdoor вариант того же возрастного содержания, без ночёвок. Sample day PDF: первый день доставляют к Hakuba station11:45, обычные дни 08:30–16:30 у hotel; в последний день забирают у station13:00. Точные часы нового набора подтвердить; не все пять дней полные. Дневная Ninja отличается от пансиона 7–8.',
            'Опубликованный летний план 2026: '+periods+'. Только перечисленные программы/периоды. Новых дат 2027 нет.',
            price(2026,'JPY87 500/5 дневных посещений, не пансион. Для двоих 175 000 до поездки/жилья; разные группы должны совпасть по неделе/возрасту.',
                  'Дневные активности и питание по summerpage/sample.', 'Жильё семьи/перелёт, доставка/забор детей, страховка отдельно; overnight/Tokyochaperonedservice в day fee не обещаны.',ecancel),
            'Без проживания; подходит семейной поездке с собственным жильём.',
            later('В 2027 выше группы 7–8.') if slug=='ninja' else fit('conditional','В 2027 подходит 9–12; язык EN есть, но набор 2027 и уровень активности ещё нужны.'),
            fit('conditional','Только после 7-летия в 2027; до него не подходит, нужна дата рождения.') if slug=='ninja' else later('В 2027 максимум 7, ниже 9.'),
            'Дневная альтернатива первому самостоятельному пансиону. Для обоих возможно только совпадение Ninja/Mountain либо Water в новом расписании после 7-летия Оскара.',equestions,
            [src('Дневные форматы, периоды и цена',EVER+'summer-camps/'),src('Sample day schedules: неполные 1/5 дни',EVER+'wp-content/uploads/Day-Camps-Timetables.pdf'),src('EN и бытовые требования',EVER+'faq/'),src('Camp contract',EVER+'terms-and-conditions/')],status='published_2026',confirmed=['EN'])
        P[-1]['language_evidence_role']='primary'

    gplace='GSA International School,6-14-26 Shibasaki-cho,Tachikawa,Tokyo'
    for slug,kind in [('gsa-tachikawa-elementary',False),('gsa-tachikawa-kindergarten',True)]:
        url=GSA+('tachikawa_k_en/' if kind else 'tachikawa_e_en/')
        add(slug,'Global Step Academy Tachikawa · '+('Kindergarten' if kind else 'Elementary Summer School'),'Япония','JPN',gplace,
            'general,languages,science,art,sport','day','3–6; 24 ученика/class' if kind else 'Grades1–6; это классы, не 6 лет',
            'Seasonalhub прямо 100%EN; Kindergarten специальные предметы all taught inEnglish, Elementary experiencednativeEnglishspeakers. Основной EN подтверждён.',
            'Kindergarten: IEYC inquiry/play, phonicsJolly, 45 мин science/socialstudies, outdoor/art/music/dance. 09–14:30; продление до 18 отдельно, отсутствует Term3. Elementary: наука/иллюзии/насекомые, грамотность/истории, art/crafts и спорт; 09:30–10:30science, 1 час art. Обычный 09–14:30 или full09–18 со studyhall/sport/ENwriting; продление не дополнительная робототехника. Не технический codingintensive.',
            'Пять блоков 21–24/27–31 июля, 3–7/17–21/24–28 августа, без года. TuesdayJuly21/June30 не доказывает 2026: такой календарь повторяется. Новые даты 2027, зима/весна не объявлены подробной страницей.',
            price(None,'Недатированный прайс: JPY55 000/4 дня, 66 000/5 дней; Elementary full75 000 или буквально 88:000(типографическое расхождение, счёт уточнить).',
                  'Основной дневной курс выбранного term; питание платное.',
                  'Kindergarten lunch4 000/4 дня либо 5 000/5; extension1 000/30min, кроме Term3. Elementary lunch4 000/5 дней, цена 4-дневного обеда отдельно неизвестна. Communitydiscount10% лишь eligiblemembers, Kindergartenownstudents20%; семье по умолчанию не назначено. Жильё/дорога отдельно.',
                  'Нет возврата после June30Tuesday, но год не указан. Для 2026/27 нужен новый договор; старый дедлайн не перенесён.'),
            'Городской дневной курс. Пансион школы/летней программы не заявлен.',
            later('В 2027 выше 3–6.') if kind else fit('conditional','Нужен фактический Grade1–6 и новый сезон. Год рождения не заменяет класс.'),
            fit('conditional','В 2027 только пока 6 лет; после 7-летия —Elementary по реальному классу.') if kind else fit('conditional','Нужен фактический Grade1–6; допуск по возрасту 6 сам по себе не установлен.'),
            'Понятный городской общий английский вариант с science/art для семейной поездки; год и новый прайс требуют подтверждения.',
            ['Год/даты/цена/актуальная отмена и EN уровень; внешний иностранный приём, место и реальный класс.','Уточнить длительность/налоги/обед, 4-дневный тариф, расширенный день и верхнюю границу возраста.'],
            [src('Подробный возраст/программа/расписание/тариф, год не указан',url),src('Прямое 100%EN и сезонный формат',GSA)],confirmed=['EN'])
        P[-1]['language_evidence_role']='primary'

    splace='SOR Bukit Timah170UpperBukitTimah#B2-15/16;AngMoKio5AMKCentral2#02-01/02;Katong112EastCoast#04-07'
    for slug,name,ages,content,branches in [
        ('sor-rescue','Rescue Squad','5+','SPIKE Essential: двигатели/сенсоры, blockcoding, спасательные машины, проверка/улучшение механизмов.','Все 3 центра'),
        ('sor-rumble','Robo Rumble','7+','SPIKE Prime: построить/программировать battle robot, robosumo и защита PowerCore. Внутренние игры не официальный международный квалификатор. Страница ошибочно предваряет этот блок Tuesday3Dprinting7+.','Все 3 центра'),
        ('sor-spin','3D Spin Strikers','8+','Tinkercad3D модели волчка/Beyblade, баланс/вес/форма, BambuStudio, slicing и BambuLabP1S. Два посещения day1/day2 имеют одинаковое содержание, не второй уровень.','Все 3 центра'),
        ('sor-vexgo','VEX GO Bot League','5+','Конструкция VEXGO и дистанционное управление RoboSoccer, инженерные игровые миссии. Слово League не подтверждает участие RECF/VEXWorlds.','Только Bukit Timah / Ang Mo Kio, без Katong')]:
        add(slug,'School of Robotics Singapore · '+name,'Сингапур','SGP',splace,'robotics,coding' if slug!='sor-spin' else 'design,technology','day',ages,
            'Язык самих занятий EN/ES/RU или вторичной помощи не установлен в прочитанной собственной странице. Язык сайта не подтверждает язык занятий.',
            content+' '+branches+'. 10:30–15:30 с 1 часом обеда:4 часа учебных блоков, не 5 часов робототехники. VEXGOdeviceprovided; остальные курсы разрешают принести свой tablet/laptop(3D laptop). Письменно уточнить выдачу device для остальных треков.',
            'Заголовок 8–11September2026, FAQDecember2026 с незаполненным поле XXDecember2026. Расписание всех филиалов не подтверждено: новый декабрьский / 2027 набор не внесён как точный calendarcohort.',
            price(2026,'SGD200/day при 1–2 днях или 180/day при 3–4 днях, GST сверх. Условия credits приводят пример 3 дня 540 — можно разделить среди разных детей, скидка братьям / сёстрам автоматически не назначена.',
                  'Две 2-часовые сессии и обед; собственный обед разрешён после предупреждения, снижение цены не обещано.',
                  'GST ставка/итоговый invoice проверить; pre/post5SGD каждые 15 минут до GST, жильё/дорога отдельно. Роботы/3D принтер в пользование, kit в подарок не обещан.',
                  'Credits после оплаты невозвратны / непередаваемы, нет topup, истекают в конце периода каникул. Перенос ≥48 часов при наличии мест; при отмене организатором предлагают другие даты / классы, cashrefund не обещан. Требования к медицинской информации/photoconsent есть.'),
            'Дневной городской центр, проживания нет.',fit('conditional','Возраст подходит; нужны подтверждённые EN занятия, даты, место и сложностьпо 3-летнему опыту.'),
            fit('conditional','5+позволяет возраст; язык / место / даты уточнить.') if ages=='5+' else later('В конце 2026 ещё 5–6, в 2027 до 7; 7+только после 7-летия, 8+позже.'),
            'Проверенная структура коротких технических занятий; пока кандидат для наблюдения кандидат из-за языка/конфликтадат, не семейная рекомендация с гарантированным EN.',
            ['Исправленный календарь конкретного филиала и EN группа/иностранный допуск.','Итог с GST, предоставление девайса, возврат/credits и подходящие сложные задачи.'],
            [src('Все 4 курса/возраст/тариф/обед/условия/расхождения в датах',SOR)],status='partial_2026')

    cplace='Computhink@ToaPayohLibrary,6ToaPayohCentral,Singapore319191'
    ctdata=[
        ('computhink-roblox-teens','Roblox Defenders of Magic','11–16','holiday-roblox-game-developer-coding-camp/',
         '3 дня: дизайн мира/первые Lua события; spells, monsters/spawnAI, UI, variables/functions; затем прогресс игрока, playtest/debug/polish. Своя игра RobloxStudio, не участие в международном хакатоне.',True),
        ('computhink-python-minecraft-teens','Python Minecraft','11–16','holiday-python-minecraft-coding-camp/',
         'TypedPython в GitHubCodespaces, запуск в MinecraftEducation. День 1syntax/variables/strings/numbers; 2forloops/автоматизация Agent/build; 3ifconditions, missions/debugging и finalbuild. Beginner-friendly переход от блочного coding.',False),
        ('computhink-ai-app-teens','AI App Building','12–16; нужен опыт coding','ai-coding-camp-for-teens/',
         'Startup-подобный 3-дневный sprint: идея/планирование/prompts, построить webapp с выбранным организатором AItool, проверка/итерации; затем готовое приложение/презентация родителям. Название AItool не раскрыто; собственный проект, нет обещания обучения ML или официального конкурса.',False),
        ('computhink-g3-python','G3 Computing Python','Sec3–4; Sec2 только подтверждённый предмет G3','holiday-o-level-computing/',
         'Академический catch-up для учащихся G3Computing, курс вторичной школы. Variables/I-O/typeconversion/forloops, ifelse/while/inputvalidation/debug, lists/listmethods и exam-style refinement/debug/development. Название экзамена / дисциплины передано по описанию оператора, требования экзамена отдельным регулятором в этом проходе не проверялись.',False)]
    weeks=[('2026-11-23','2026-11-25'),('2026-11-30','2026-12-02'),('2026-12-07','2026-12-09'),('2026-12-14','2026-12-16')]
    for slug,name,ages,path,content,october in ctdata:
        url=CT+path
        add(slug,'Computhink · '+name,'Сингапур','SGP',cplace,'ai,coding,entrepreneurship' if '-ai-' in slug else 'games,coding' if 'g3' not in slug else 'coding,science','day',ages,
            'Язык преподавания EN не подтверждён прямым утверждением собственной странице курса. Названия/laptop/platformEnglish не достаточны для подтверждения EN-инструктора.',
            content+' Каждый вариант 3 дня×3 часа=9 часов, максимум 8 учеников; laptops/платформы дают на курс, StudentPortal/levelassessment. Completioncertificate не международная медаль.',
            'Конкретные 2026 октябрь/ноябрь/декабрьские 3-дневныедаты ниже. Нет цен / дат 2027.',
            price(2026,'SGD467 за один 3-дневный/9-часовой вариант.',
                  'Laptops, нужная учебная платформа/оборудование, занятия, StudentPortal; AItool выбирается организатором.',
                  'GST в цене/питание/лицензии после курса и срок доступа публично не установлены; дорожные расходы/жильё отдельно.',
                  'Полный invoice / условия отмены / переноса и внешний приём ещё нужны; слоты/доступная ёмкость не гарантированы.'),
            'Дневной курс по 3 часа; пансион/обед не заявлены.',
            later('Текущий возраст ниже 11/12; академический G3Sec2–4—будущий трек, реальный класс не подменён возрастом.'),
            later('Младший возраст ниже 11/12; G3 средняя школа—будущий трек.'),
            'Будущая лестница textcoding/game/app и экзамена, со своим полным 3-дневным содержанием. Эти 4 трека—один оператор, не 4 независимых мировых топ-лагеря.',
            ['Подтвердить EN, приём/возраст или Sec предмет, материалы/GST/отмену и новые 2027 наборы.'],
            [src('Собственный полный курс/слоты/возраст/оборудование/прайс',url),src('Восемь курсов организатора, классы/оборудование',CT+'holiday-coding-camps-for-kids/')],status='published_2026')
        use=[weeks[0],weeks[2]] if 'g3' in slug else weeks
        rows=[]
        if october:rows.append(row('2026-10-12','2026-10-14','oct-am','3 дня 09:30–12:30','SGD467/9 часов',url,cplace,'day_camp_window',['MO','TU','WE']))
        for i,(a,z) in enumerate(use,1):
            time='14–17' if october or 'g3' in slug else '09:30–12:30'
            rows.append(row(a,z,'w'+str(i),'3 дня'+time,'SGD467/9 часов',url,cplace,'day_camp_window',['MO','TU','WE']))
        detail(P[-1],rows)

    ip='Banqiao,SiweiRoad177Lane4Alley20 / Taichung,Xitun,FulinRoad61'
    for slug,name,ages,path,content,fee2,fee3,cohorts in [
        ('irobo-speed-mechanics','Speed Mechanics','Старшая дошкольная группа(大班) или Grades1–3','spm-camp-theme2',
         'LEGO Simple&PoweredMachines: шестерни/шкивы/моторы, ускорение/передача, трение/сила, кинетическая / потенциальная энергия, 3D пространство; тестирование быстрых устойчивых моделей. Без заявленного coding / AI интенсива.',4700,6800,
         [('banqiao','2027-01-21','2027-01-22'),('banqiao','2027-01-25','2027-01-27'),('banqiao','2027-01-30','2027-01-31'),('taichung','2027-01-21','2027-01-22'),('taichung','2027-01-25','2027-01-27')]),
        ('irobo-boost-ice','BOOST Ice Adventure','Grades1–3','boost-camp',
         'LEGOBOOST оригинальный kit+app, блочные инструкции / последовательности, моторы / сенсоры, логика / управление; ледяные миссии, тест/исправление. Курс для начинающих.',5200,7400,
         [('banqiao','2027-01-21','2027-01-22'),('banqiao','2027-01-25','2027-01-27'),('taichung','2027-01-21','2027-01-22'),('taichung','2027-01-25','2027-01-27')]),
        ('irobo-boost-treasure','BOOST Treasure Hunters','Grades1–3','boost-camp-theme2',
         'LEGOBOOST конструкции/моторы / сенсоры, appblockcoding/правила, problem-solving. Заголовок TreasureHunters, вводнаяфраза GalaxyRescue: смешение названий, не ещё один самостоятельный лагерь.',5200,7400,
         [('banqiao','2027-01-28','2027-01-29'),('banqiao','2027-02-01','2027-02-03'),('taichung','2027-01-28','2027-01-29'),('taichung','2027-02-01','2027-02-03')]),
        ('irobo-star-voyager','SPIKE/EV3 Star Voyager','Grades3–9; верхняя начальная/middle вописании, границу Grade3 уточнить','spike-ev3-camp',
         'SPIKE/EV3 компьютер / сенсоры, конструкция/блочная программа, командные миссии/remotecontrol; логика / разбор задач. Внутренние командные игры — это не официальный турнир VEX/FLL.',5400,7600,
         [('banqiao','2027-01-21','2027-01-22'),('banqiao','2027-01-25','2027-01-27'),('taichung','2027-01-25','2027-01-27')]),
        ('irobo-python-basic','Python Foundations','HeadlineGrades5–highschool, bodyGrade5/middle/high; grade6 явно не перечислен','python-basic-camp',
         '2 дня pure-softwarePython: переменные / условия / циклы/functions, логика / практика / разбор задач. Упомянутые PythonAIRobotInventor и C++Arduino—отдельные следующие курсы, не включены в эти тариф / даты.',5600,None,
         [('banqiao','2027-01-23','2027-01-24'),('banqiao','2027-01-30','2027-01-31'),('taichung','2027-01-21','2027-01-22'),('taichung','2027-01-30','2027-01-31')])]:
        url=IRO+path
        fees='NT$'+str(fee2)+'/2 дня'+(' или'+str(fee3)+'/3 дня' if fee3 else '')
        devices='Учебное оборудование дают в пользование, не kit домой.'
        if 'boost' in slug:devices+=' Нужен свой Android/Appletablet или phone с Bluetooth и USB кабелем.'
        if slug=='irobo-star-voyager':devices+=' Основной laptop предоставляют; отдельный mobile experience разрешает Android/Apple в одной фразе, следующая исключает iOS. Уточнить, дополнительный Android не основное оборудование.'
        add(slug,'iROBO Taiwan · '+name,'Тайвань','TWN',ip,'robotics,coding' if slug!='irobo-speed-mechanics' and slug!='irobo-python-basic' else 'science,technology' if slug=='irobo-speed-mechanics' else 'coding','day',ages,
            'EN/ES/RU инструкция или вторичная помощь не подтверждены. Китайская страница и английское название не доказывают иностранную английскую группу; пока кандидат для наблюдения.',
            content+' '+devices+' 09–16, приём 08:30–17:30 со staff; после 16:00 свободная игра / уборка, не 9 часов робототехники. 2/3-дневные варианты одной темы альтернативны, рекомендуется выбрать один; 5 дней можно собрать из разных тем.',
            'Конкретные январь/февраль 2027 варианты по кампусам ниже; места не подтверждены.',
            price(2027,fees+' с обедом; early bird/gifts не оценены как гарантированная скидка.',
                  'Выбранный 2/3-дневныйкурс, обед, учебное LEGO оборудование; передача набора в собственность не обещана.',
                  'Mobile для BOOST/optionalSPIKE, проживание, дорога и столовые приборы отдельно. Итоговая ранняя цена / налоги и иностранный приём публично не установлены.',
                  'После onlineapplication ждут paymentnotice и confirmation. Полный договор с точными сроками отмены ещё не получен; weatherclosure перенос/допзанятияпо ownFAQ, не cashrefund. Формы не отправляли.'),
            'Дневной курс, ночёвок нет; детей забирают родители.',
            fit('unknown','Допуск зависит от реального школьного класса, не от года рождения. Проверить разрешённую группу/уровень и EN.') if slug=='irobo-python-basic' else fit('conditional','Реальный Grade нужен:Grades1–3 либо 3–9 для темы; язык/место / сложность ещё не подтверждены.'),
            fit('conditional','Проверить реальную старшую дошкольную группу/Grade1–3 и EN.') if slug=='irobo-speed-mechanics' or 'boost' in slug else fit('unknown','Нужен реальный Grade3+ либо Grade5+; год рожденияне заменяет класс, младший допуск не гарантирован.'),
            'Конкретный технический зимний кандидат 2027 с расписанием / ценой. До ответа о EN/внешнем приёме не попадает в рекомендации подтверждённого английского лагеря.',
            ['Получить подтверждение EN инструктора/второй языковой помощи, реального класса, иностранного приёма и места.','Новый счёт/возврат, продвинутые задачи, device/налоги; одинаковые темы 2/3 дней не бронировать как самостоятельные уровни.'],
            [src('Собственная полная зимняя 2027 программа, варианты/цены/FAQ',url)],status='published_2027')
        rows=[]
        for campus,a,z in cohorts:
            days=2 if int(z[-2:])-int(a[-2:])==1 else 3
            place='Banqiao,SiweiRoad177Lane4Alley20' if campus=='banqiao' else 'Taichung,Xitun,FulinRoad61'
            rows.append(row(a,z,campus+'-'+a.replace('-',''),str(days)+'дня 09–16, приём 08:30–17:30','NT$'+str(fee2 if days==2 else fee3)+' с обедом',url,place,'camp_session'))
        detail(P[-1],rows)

    add('ntue-mandarin-winter','NTUE CLEC · Mandarin Winter Camp','Тайвань','TWN','National Taipei University of Education,134Sec2HepingEastRoad,Da-an,Taipei',
        'general,languages,science,art','day','6–15; max15 по guide, FAQ примерно 8–12',
        'Цель/предмет—китайский Mandarin. Английские документы прочитаны целиком, но EN как вторичная помощь/инструктаж не обещаны; в фильтр подтверждённого EN не включён.',
        '9 учебных дней за 2 недели:утром Mandarinconversation, входной тест / группы по уровню / возрасту, после обеда diabolo/DIY/inkpainting/martialarts/языковое закрепление; 31Dec поездка в NationalTaiwanScienceEducationCenter и ScienceDIY.01Jan праздник, занятий нет; суббота/воскресенье вне программы.09–15:30, привоз 08:50+, забор до 15:40. Приглашают overseasstudents, начинающие Mandarin допускаются; родители не остаются на занятиях / экскурсиях. Сертификат окончания не является соревновательной наградой.',
        '28 декабря 2026–8 января 2027; единое окно двухнедельной смены, 9 учебных дней. Новый год 1 января без занятий.',
        price('2026–27','NT$36 000 / US$1 245; early bird до 31Oct2026 NT$34 000 / US$1 185. За двоих NT$68 000early либо 72 000 обычно; два участника group 35 000/person не выгоднее early и не складывается.',
              'Регистрация/форма/backpack/посуда/workbook/культурные материалы, обед/перекусы, экскурсионные дорога/билеты/питание; activityaccidentinsurance.FAQ:1 000 000NTDaccident+100 000medical, не универсальная туристическая страховка.',
              'Жильё не предоставляется; перелёт, жильё семьи / доставка детей, вечера / выходные, банковские расходы отдельно. Группы 3/4/5/6+ стоят 34/33/32/31 тыс/person, совместные оплаты; не складываются с early/returning.',
              'Оплата в течение 7 рабочих дней после admission notice. Guide:до начала 90%tuition, в первой половине 50%, позже нет; registration невозвратна. FAQ говорит 1/3, а не 1/2 — конфликт, сумма registration не раскрыта. Возврат банком около 1 месяца; болезнь/force-majeureclosure без подневного возврата/компенсации.'),
        'Дневной, размещение с родителями/родственниками; hotel рекомендации по запросу не являются оплаченным пансионом.',
        fit('conditional','Возраст 6–15 подходит; Mandarin новичок допустим, но не подтверждена EN помощь и это общий языковой, не robotics camp.'),
        fit('conditional','На 28Dec2026 будет 6 только если день рождения уже прошёл; точная дата/готовность без родителей/EN помощь ещё нужны.'),
        'Культурно-языковой тайваньский зимний вариант с science экскурсией. Сохранён с ограничением EN, не выдаётся за английский технический intensive.',
        ['Письменно подтвердить EN помощь/язык scienceDIY, возраст Оскара, место/уровень.','Устранить 1/3vs1/2refund, сумму registration/страховое покрытие и итоговый invoice; семейного общежития нет.'],
        [src('Winter2027:даты/overseas допуск',NTUE),src('FAQ:нулевой Mandarin/нет родителей/возврат 1/3', 'https://clec.ntue.edu.tw/p/404-1018-57259.php?Lang=zh-tw')],status='published_2026_27',confirmed=['ZH'],sessions=[['2026-12-28','2027-01-08']])
    P[-1]['language_evidence_role']='language_lessons'
    P[-1]['timing']['session_details']=[row('2026-12-28','2027-01-08','winter','Единая смена:9 дней 09–15:30, 01Jan выходной','NT$36 000; 34 000early до 31Oct2026, жильё отдельно',NTUE,P[-1]['place'],'day_camp_window',['MO','TU','WE','TH','FR'])]

    ik='https://www.intercamp-korea.com/programs/winter-language-camp-in-seoul'
    add('intercamp-seoul-winter','Inter-K · Seoul Winter Language Camp','Южная Корея','KOR','Seoul, studentresidence; название партнёрского университета не установлено',
        'general,languages,art','boarding','FAQ14–18, 18–25, 25–35; для нынешних детей позже',
        'Выбор одного языка EN либо KO:уроки 09–12 на заявленном целевом языке, certifiednative-speakingteachers; общая языковая поддержка RU не подтверждена наличием русского сайта.',
        'Языковой / культурный маршрут:29–31Dec и 4–6Jan утренние уроки, музеи/дворец/город, taekwondo/hiphop, конференция о поступлении в университеты, выезд за город; 01Janfree, 02JanLotteWorld, 03Janexcursion. Beginner/AdvancedEnglish; оба направления сразу не изучают. Coursecompletioncertificate университета заявлен оператором, название выдавшего учреждения не установлено:не академическая степень / соревновательный диплом.',
        '28Dec2026–7Jan2027:11 календарных дат/10 ночей, заголовок 10days/10nights. Расхождение продолжительности сохранено.',
        price('2026–27','USD2 500/программа; валюта доллара/финальный счёт проверить.',
              'Уроки/двухместная studentresidence/24hcoordinators, билеты/экскурсии, сим/transportcard, roundtripairporttransfer. Three meals/day в общем блоке, детальное included уточняет только понедельник–пятница.',
              'Питание в выходные, перелёт/страховка/виза/допрасходы и конкретный universitycertificate ещё проверить.',
              'Отмена/аванс/полная смета 2027 не раскрыты в прочитанной программе; foreigncitizenswelcomed, invitation не является визой.'),
        'Двухместные дуплексные комнаты: санузел/kitchenette/laundry. Для несовершеннолетних curfew22:30; самостоятельный выход в город возможен с parentconsent, не предполагает обязательного сопровождения каждого выхода 24 часа в сутки.',
        later('Минимальная возрастная группа FAQ14+:Матвей пока ниже.'),later('Минимальная группа 14+:Оскар пока ниже.'),
        'Будущий международный языковой/culture маршрут, не поездка для 6/9 лет. EN подтверждён для уроков, но возраст не позволяет детям семьи участвовать сейчас.',
        ['Возраст/комнаты/кураторство/трансферы / питание в выходные/выдающий университет и договор.'],
        [src('Полный winter2027 план/питание/проживание/EN',ik),src('OwnFAQ:14+ и любая страна/curfew/parentconsent','https://www.intercamp-korea.com/')],status='published_2026_27',confirmed=['EN','KO'],sessions=[['2026-12-28','2027-01-07']])
    P[-1]['language_evidence_role']='language_lessons'
    add('wolko-winter-english','Word of Life Korea · Winter English Camp','Южная Корея','KOR','Pyeongtaek(WOLKOCentre); точное место когорты ещё TBA',
        'general,languages','boarding','Общий English CampGrades6–9/11–15; возраст конкретной winter2027 когорты TBA.',
        'Большинство программы на EN, жизнь с native-speaking staff; общий English Camp подтверждён, новые детали зимнего потока пока не объявлены.',
        'Христианский лагерь с Gospel/evangelism/discipleship, Библией, общением/активностями. Религиозное содержание существенно и явно указано оператором; нет основания называть техническим/secular. Общий English Camp11–15; Jeju отдельный highschool15–18, не перенесён на этот набор.',
        'Заявлен 11–16Jan2027, 5 ночей/6 дней, max40. Регистрация ещё Upcoming/OpeningSoon, дата начала не объявлена; цена/возраст/точное место TBA.',
        price(2027,'Не опубликовано/TBA; не подставлен старый или Jeju тариф.', 'Жилой формат 5 ночей заявлен, полные детальные включения ещё не названы.', 'Питание/трансферы/страховка/иностранный приём/итоговый invoice ещё нужны.', 'Аванс/отмена ещё не опубликованы.'),
        'Пять ночей заявлены, комнаты/сопровождение в конкретном договоре 2027 ещё уточнить.',
        later('Общий поток 11+позже; конкретный winter2027 возраст ещё не объявлен.'),later('Общий поток 11+позже; конкретный winter2027 возраст ещё не объявлен.'),
        'Сохранён как будущий английский религиозный вариант с объявленным окном. Не включён в приоритетную светскую / техническую подборку для семьи.',
        ['Возраст/иностранный допуск/уровень EN/отношение к содержанию, место/прайс/договор; регистрация ещё не открыта.'],
        [src('Own2027 зимний набор:Upcoming/TBA','https://wolko.org/camp-register/'),src('Owncamp содержание / EN / общий возраст, Jeju отдельно','https://wolko.org/camp/')],status='partial_2027',confirmed=['EN'],sessions=[['2027-01-11','2027-01-16']])
    P[-1]['language_evidence_role']='camp_life'
    for p in P[start:]:
        p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED

def extend_report_v89(report):
    report['shortlist'].extend([
        dict(label='Япония · английский зимний пансион Матвею',slugs=['evergreen-hakuba-winter','english-adventure-winter','koa-english-ski'],reason='Evergreen8–15:14–18Dec2026/2–6Jan2027, 175000JPY база, типичный elementarypass+standardgear итог 221900 до Tokyo/перелёта. Оскар пока ниже 8; независимые сезонные пакеты/уровень сравнивать по досье, места не гарантированы.'),
        dict(label='Япония · летний EN outdoor с разными возрастами',slugs=['evergreen-hakuba-ninja-board','evergreen-hakuba-mountain-board','evergreen-hakuba-water-board','evergreen-hakuba-earth-board','evergreen-hakuba-ninja-day','evergreen-hakuba-mountain-day','evergreen-hakuba-water-day'],reason='Matvey9–12, Oscar7–8 лишь после 7-летия. Летние 175000JPY пансион/87500 день — архив 2026, новые когорты 2027 не объявлены. Совместная семейная поездка дневными треками для разных возрастов зависит от совпадения недель; это общие/природные, не технические интенсивы.'),
        dict(label='Тайвань · зимние проекты с языковым барьером',slugs=['irobo-speed-mechanics','irobo-boost-ice','irobo-boost-treasure','irobo-star-voyager','irobo-frozen','ntue-mandarin-winter'],reason='Есть реальные winter2027 даты, курсы/стоимость/оборудование. EN инструктаж/второй язык не подтверждён:это кандидат для наблюдения, подтверждения английского пока нет. Для iROBO нужен реальный Grade; NTUE6–15—Mandarin/culture без пансиона, refund1/3vs1/2 расходится.'),
        dict(label='Токио · городской английский общий лагерь',slugs=['gsa-tachikawa-elementary','gsa-tachikawa-kindergarten','canadian-academy-summer-experience','asij-chofu'],reason='GSA явно EN, science/art/sport; возраст/класс определяют разные потоки. GSA не указывает год летних term, поэтому нет придуманных дат 2027. CanadianAcademy/ASIJ свои сезонные условия, это отдельные регистрации/кампус.'),
        dict(label='Сингапур · короткая техника сейчас и coding позже',slugs=['sor-rescue','sor-rumble','sor-spin','sor-vexgo','computhink-roblox-teens','computhink-python-minecraft-teens','computhink-ai-app-teens','computhink-g3-python'],reason='SOR5+/7+/8+короткие 4 часа учёбы+обед, конфликт September/DecemberXX и EN не установлены. ComputhinktypedLua/Python11+, AI12+, G3Sec2–4—позже; 467SGD/9h и 2026 слоты проверены, не 14 независимых топ-лагерей/мировых хакатонов.')
    ])
    report['gaps'].extend([
        dict(country='Япония',iso='JPN',provider='v89 · реальные зимние и архивные летние форматы',detail='EvergreenWhiteHorse8–15, 26–27 даты/EN/175000JPYbase проверены; lift/gear/Tokyoextras обязательны по ситуации. Summer9 отдельных возрастных / форматных досье—один оператор, не 9 мировыхтопов; 2027 не объявлен, Leadership13–17/13–16 конфликт. GSA100%EN, но summerdates/deadline без года/88:000price, не превращены в 2027. Первый/последний день Evergreenday короче; nightphone ограничен.',next_action='Новые 2027 летние даты/счета, точные DOB/grade, совпадение недель двух возрастов, самостоятельность, отмена 14 дней/допуски.',url=EVER+'summer-camps/'),
        dict(country='Тайвань',iso='TWN',provider='v89 · язык и документы не равнозначны',detail='iROBO ещё 5winter2027 тем с реальными датами по кампусам/fees:SPM大班/G1–3, BOOSTG1–3, SPIKEG3–9, PythonG5+; EN не обещан. NTUEforeign6–15, 28Dec–8Jan9 днейбез 01Jan, 34000/36000TWD с lunch/materials/insurance без housing; Englishguide невыполняет ENsupportproof. Refundguide1/2vsFAQ1/3 и max15vsFAQ8–12. TYPA журнал 2026–27—Summer2026, не 2027; одна матрица возрастных тем, нет календарного размножения 24 тем.',next_action='Реальный класс/день рождения, EN инструктаж/поддержка, иностранный допуск/места, новые договоры/счета/отмена и TYPA2027.',url=NTUE),
        dict(country='Сингапур',iso='SGP',provider='v89 · конфликт набора и особый внешний допуск',detail='SOR заголовок 8–11Sep2026 но FAQDecemberXX; не получены точные декабрьские слоты/EN. Computhink4 новых futuretracks11+/12+/Sec2–4, 15 реальных 2026 вариантов, EN неявен. ARCautism-friendly2026holidaycourses страница говорит Non-Pathlight7–18allowed, поэтому запрет внешним детям не приписан; специальные admission/support/grade/language условия ещё нужны, новые курсы пока gap.',next_action='Исправленные SOR когорты/EN/GST; полный прайс/отмена Computhink/реальные уровни; прочесть специальные условия внешнего приёма ARC без предположений о детях семьи.',url=SOR),
        dict(country='Южная Корея',iso='KOR',provider='v89 · возраст, heritage и религиозная программа',detail='Inter-Kwinter2027EN/KO09–12, foreigncitizens, 2500$, 10nights/11dates; общий FAQ14+, детям 6/9 не подходит, питание weekdaysonlyvs общий 3/day блок. WOLKO11–16Jan2027Upcoming, age/priceTBA, общий English11–15:религиозный Gospel/discipleship ясно отмечен, не bestsecularSTEM. EwhaSeoulSTEAM4–22Jan2027G2–6aimsKoreanheritage/корейский, min40, не подтверждён foreignnonheritageEN допуск; JEINS/SJAcamp не подтверждён старым школьным handbook.',next_action='Искать новые открытые английские программы 6–10 с учётом внешнего приёма, не подменять camp постоянным schoolcurriculum или universitybrand; сохранять весь мировой план active.',url='https://kle.ewha.ac.kr/kle/notice/notice.do?articleNo=799162&mode=view')
    ])
