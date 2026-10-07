"""Swiss/French/Spanish programme-specific audit; no inferred 2027 availability."""
from datetime import date,timedelta
CHECKED='2026-10-05'
ENSR='https://www.ensr.ch/summer-camp/'
ENSR_FORM='https://cdn.prod.website-files.com/6964c7b4ab6723b37f5f5366/69a572f1eb362d7af8bf982f_summer_camp_application_form_2026.pdf'
CJSA='https://camp-sport.ch/en/fr/'
FRI='https://www.frilingue.ch/en/juniors/learn-languages-switzerland-youth/braunwald/summer-camp-in-braunwald'
FRI_FAMILY='https://www.frilingue.ch/en/adults/switzerland-languages/braunwald/family-camp-family-workation'
FRI_TERMS='https://www.frilingue.ch/en/language-camps-switzerland/terms-conditions'
ALT='https://www.altitude-camps.com/'
BELL='https://www.bell-school.ch/en/'
BC='https://www.britishcouncil.fr/anglais/enfants/primaire-stages'
KID='https://en.kidooland.com/'
ES='https://www.englishsummer.com/'

def add_europe_v82(add,src,fit,profiles):
    def put(slug,name,iso,place,themes,formats,age,language,programme,dates,price,housing,mat,osc,why,questions,urls,
            status='next_unannounced',role=None,priority=None,sessions=None):
        add(slug,name,{'CHE':'Швейцария','FRA':'Франция','ESP':'Испания'}[iso],iso,place,themes,formats,age,language,
            programme,dates,price,housing,mat,osc,why,questions,[src(t,u) for t,u in urls],status=status,
            confirmed=['EN'] if role else [],priority=priority,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        return p
    def fee(year,label,included,extras,deposit):return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def detail(p,url,**kw):
        p['timing']['session_details']=[dict(start=a,end=b,label=kw.get('label','Недельная смена'),source=url,place=p['place'],
            formats=p['formats'],price=p['price']['label'],date_scope=kw.get('date_scope','camp_session'),
            **{k:v for k,v in kw.items() if k not in ['label','date_scope']}) for a,b in p['timing']['sessions']]

    ensr_dates=[['2027-07-04','2027-07-10'],['2027-07-11','2027-07-17'],['2027-07-18','2027-07-24']]
    ensr_fee=fee(2027,'CHF 2 150/1 нед.;4 300/2;6 270/3.',
        'Полный пансион, обычные активности; языковой вариант 22 периода/нед. Бельё/полотенца; стирка при проживании больше двух недель.',
        'Страховка жителей вне EU/EEA/Швейцарии 150/нед. Geneva round trip 542 для 1,345 для 2,275 для 3 студентов — единицу группового тарифа уточнить. DHL invitation 210. Europa Park 390 только 11–17 июля, минимум 10, запись за 2 месяца. Paragliding 120/полёт, tennis 80/час, court 10/час, riding 35/час. Перелёт отдельно.',
        'Сайт 2027, скачиваемая форма 2026; актуальный депозит/отмена неизвестны. Архивная форма требует страховку для всех жителей вне Швейцарии, текущий сайт — вне EU/EEA/Швейцарии; подтвердить правило.')
    for slug,name,theme,language,programme,role in [
        ('ensr-junior-languages','ENSR · Junior Languages & Sports','general,languages,sport,adventure',
         'English подтверждён на языковых уроках; язык спорта/лагерной жизни отдельно неизвестен.',
         '22 периода English/French в неделю, группы 4–7; затем спорт и вечерние игры. YLE/DELF preparation упоминает 88 уроков при трёх недельных сменах: длительность/экзамен/сертификат не обещаем.','language_lessons'),
        ('ensr-junior-multisport','ENSR · Junior Multisport','general,sport,adventure',
         'English всей Multisport программы не установлен; язык соседнего курса не доказательство.',
         'Multisport вместо языковых уроков: water/mountain activities, велосипед, climbing, tennis, riding и командные игры. Robotics/AI не заявлены.',None),
    ]:
        put(slug,name,'CHE','Hôtel Suisse, Champéry · адрес заселения подтвердить',theme,'boarding','Junior 8–11; общий лагерь 8–18 включает другую старшую группу.',language,programme,
            '4–10,11–17,18–24 июля 2027 на сайте. Linked application PDF содержит 28 июня–18 июля 2026.',ensr_fee,
            'Отель, по 2 ребёнка в комнате с личным санузлом; фактический Junior room allocation/ночной контроль подтвердить.',
            fit('conditional','9–10 подходит 8–11; язык выбранного спорта, внешний приём и договор 2027.'),fit('later','6–7 ниже 8; семейного допуска младше 8 не прочитано.'),
            'Младший Swiss пансион Матвею с опубликованной ценой 2027; два учебных выбора одного организатора.',
            ['Актуальная форма 2027, язык/курс, единица transfer fee, room, полный счёт/место и реальные условия YLE/DELF.'],
            [('Junior programme',ENSR+'summer-camp'),('Языковой план',ENSR+'language-studies-sports-and-leisure'),('Multisport',ENSR+'multisports-and-leisure'),('2027 даты/прайс',ENSR+'registration'),('Архивная форма 2026',ENSR_FORM)],
            status='published_2027',role=role,priority=['general','boarding'],sessions=ensr_dates)

    cjsa_dates=[['2027-07-04','2027-07-10'],['2027-07-11','2027-07-17'],['2027-07-18','2027-07-24'],['2027-07-25','2027-07-31'],['2027-08-08','2027-08-14'],['2027-08-15','2027-08-21']]
    cjsa_terms='CHF 250 за каждую неделю при записи, остаток за месяц. Отмена 80;50% за месяц,100% между 20-м и 11-м днями включительно, остальные границы неполны. Медицинская отмена — camp credit текущего/следующего лета. Иностранным детям medical/accident insurance обязательно; цена неизвестна.'
    for slug,name,age,price,programme,role in [
        ('cjsa-languages-sports','CJSA · Languages & Sports','Конкретный курс 9–17; общий 8–17 не снижает минимум 9.',
         'Board CHF 900/1 нед.,1800/2,2700/3,3600/4. Day 700/1,1400/2,2100/3,2800/4.',
         '15 ч English/German/French в неделю по уровню, oral practice; затем kayak/paddle, MTB, бассейн, hiking, archery/игры. Умение плавать обязательно. Группы до 12–15, staff 1:6/7.','language_lessons'),
        ('cjsa-little-fun','CJSA · Little Fun Sport','Конкретный Junior 8–10.',
         'Board CHF 750/1 нед.,1500/2,2250/3. Day 550/1,1100/2,1500/3;3-week day не 1650.',
         'Junior приключения: MTB agility, mini-golf, bouldering, labyrinth, прогулки и baking. Языковые 15 часов соседнего курса сюда не относятся.',None),
    ]:
        url=CJSA+'camps-d-ete/'+('langues-et-sports/' if role else 'little-fun-sport/')
        p=put(slug,name,'CHE','Chalet les Raffles Switzerland, Siviez,1997 Nendaz–Valais','general,languages,sport,adventure' if role else 'general,sport,adventure','day,boarding',age,
            'English подтверждён на языковых уроках; English общих активностей неизвестен.' if role else 'Язык Little Fun Sport не установлен. English в другом курсе не доказывает EN Junior.',programme,
            'Шесть недель 2027:4–10,11–17,18–24,25–31 июля;8–14,15–21 августа.1–7 августа в списке нет.',
            fee(2027,price,'Пансион: жильё, питание, активности/материалы; day без ночёвки.',
                'Bridge weekend 100. Дорога/страховка отдельно; free Sion collection только прибывающим поездом, Geneva quote неизвестен.',cjsa_terms),
            'Course rooms 6–8 против FAQ 4–8. Day FAQ 08:30–18; дни посещения подтвердить. Sunday start 17:00, Saturday departure 09–11 FAQ; course даёт более узкие окна. FAQ допускает второе здание Le Déserteur — allocation уточнить.',
            fit('conditional','9–10 соответствует курсу; English спорта, birthday и фактическая группа.'),fit('later','6–7 ниже 8/9; Junior не означает допуск 6.'),
            'Доступнее многих Swiss пансионов; сравниваем цену day/board и реальный возраст курса.',
            ['English выбранной группы, плавание, day attendance days/часы, здание, weekend/insurance invoice и границы отмены.'],
            [('Курс/шесть недель/тарифы 2027',url),('FAQ/внешняя страховка/оплата/отмена',CJSA+'faq/')],status='published_2027',role=role,priority=['general','boarding'],sessions=cjsa_dates)
        detail(p,url,label='Выбор day/boarding; дни day attendance уточнить')

    fri_pairs=[[a,(date.fromisoformat(a)+timedelta(days=6)).isoformat()] for a in ['2027-06-27','2027-07-04','2027-07-11','2027-07-18','2027-07-25','2027-08-01','2027-08-08']]
    fri_dates='Старты 27 июня;4,11,18,25 июля;1,8 августа 2027. Одна неделя Sunday–Saturday рассчитана по опубликованному правилу, не по отдельной end-date таблице. Airport departure Sunday: ночь/цену подтвердить.'
    fri_rule='Own starts 27.06/04.07/11.07/18.07/25.07/01.08/08.08.2027 плюс Sunday arrival/Saturday departure для одной недели: end=start+6. Airport Sunday return сюда не включён.'
    fri_terms='Аванс 500 в 10 дней от invoice, остаток за 30 дней. Отмена:до 30 дней 500;29–14:50%;13–7:80%;7–1:100%, день 7 пересекается. Swiss language camp перенос до 10 дней на следующие 24 месяца, repeated change 100. Страхование самостоятельно.'
    fri_extras='Coding 150/нед., minimum 3/own laptop; theatre 100/art 200/diet 100/laundry 40 при 2+неделях. Rooms 4–6 shared+150/private bath+300, double private 450, single 525/600 в неделю. Zürich airport 150/сторона Sunday arrival 10–16/departure 12–18; вне окна Sunday 400, Mon–Sat 500. UM 100/сторона, check-in help 40 до стойки. Перелёт отдельно.'
    place='Adrenalin Backpackers Hotel/Hostel, Braunwald · адрес/комнату подтвердить'
    p=put('frilingue-braunwald-language','friLingue · Braunwald Junior languages','CHE',place,'general,languages,sport,adventure,coding,art','boarding','Самостоятельный Junior 8–17; Family 6–17 отдельный формат.',
        'English/French/German 15 ч/нед. выбранной группы; EN coding отдельно подтверждён. Язык всех общих активностей неизвестен.',
        'A 1–C 2, малые языковые группы, sport/excursions/evenings. Coding — optional beginner workshop, не обязательная инженерная смена.',fri_dates,
        fee(2027,'Dorm CHF 950/1 нед.,1800/2,2700/3,3600/4; coding отдельно.',
            'Dorm/shared bathroom, full board, обычные activities/excursions,24/7 support, certificate of participation.',fri_extras,fri_terms),
        'Braunwald без автомобилей, funicular из Linthal. Saturday pickup 15:30–16 на станции экскурсии: точку сообщают в течение недели; early Friday/Saturday согласуется. Airport return Sunday отдельно.',
        fit('conditional','9–10 входит 8–17; English group/польза свободному EN и внешний приём.'),fit('later','6–7 ниже самостоятельного 8; family отдельно.'),
        'Swiss языковой пансион Матвею; можно добавить небольшой прямо подтверждённый EN coding workshop.',
        ['English уровень, реальная masterclass/minimum 3, room, airport Sunday night/стоимость, адрес выдачи и invoice.'],
        [('Braunwald2027/course/coding/transfers',FRI),('Terms/оплата/отмена',FRI_TERMS)],status='published_2027',role='language_lessons',priority=['general','boarding'],sessions=fri_pairs)
    detail(p,FRI,date_precision='published_rule',date_rule=fri_rule)
    p=put('frilingue-braunwald-coding','friLingue · optional EN Coding Workshop','CHE',place,'coding,games','boarding','Опция внутри Junior 8–17; отдельный допуск младше 8 не заявлен.',
        'Прямо English именно Coding Workshop, не вывод из языкового курса.',
        'Beginner programming/website;3 занятия Monday/Wednesday/Friday. Минимум 3 участника, собственный laptop. Это добавка к пансиону, не отдельный robotics/AI лагерь или хакатон.',
        fri_dates+' Опция привязана к базовому camp; повторный недельный ICS не создаём.',
        fee(2027,'Добавка CHF 150/нед.; base dorm 950+coding 150=1100 до других опций.',
            'Три EN workshop при открытой группе; жильё/питание принадлежат base package.',fri_extras,fri_terms),'Живут в базовом Junior camp; device/software support уточнить.',
        fit('conditional','Возраст подходит; beginner content сравнить с трёхлетним опытом.'),fit('later','Junior 8–17 не подходит 6–7; Family 6 не подтверждает coding 6.'),
        'Техническая опция с прямым EN доказательством; полноценную инженерную смену не заменяет.',
        ['Minimum 3, сложность/mentor/laptop/software, конкретный workshop, не считать Family 6 допуском на coding.'],
        [('Прямые EN/minimum 3/own laptop условия',FRI),('Базовый договор',FRI_TERMS)],status='published_2027',role='primary',priority=['technical'])
    p['parent_programme_slug']='frilingue-braunwald-language'
    p=put('frilingue-braunwald-family','friLingue · Braunwald Family / Workation','CHE',place,'general,languages,sport,adventure','family,boarding','Family page 6–17 и adults 18+; самостоятельный Junior 8–17 не отменён.',
        'EN/FR/DE для детей/взрослых; у взрослого до 3 в группе. Для 6–7 нужен конкретный детский курс; English всей жизни неизвестен.',
        'Родители/дети в одном hotel; отдых с activities, adult languages или workation. У workation activities/excursions/evenings не включены; отдельной adult activity programme нет.',fri_dates,
        fee(2027,'Adult packages:workation 500/нед., familyactivities 800,10 lessons 1400,20 lessons 1800. Это не сумма за всю семью:child/room отдельно, unit adult charge уточнить.',
            'Все adult варианты fullboard/familyroom 4–6.800 добавляет workshops/excursions/evenings;1400/1800 ещё 10/20 уроков;500 только жильё/питание/workspace/Wi-Fi.',
            'Junior page parent 1100 with transfer/800 without:сверить package. Junior child 950 не гарантирует тариф 6–7. Таблица family 800 ошибочно повторяет 1 Week возле 1600/2400/3200 — длительность не выводим.',fri_terms),
        'Один hotel/familyroom; дети с родителями или camp peers. Child room fees/оплатаобщего номера и under 8 group неизвестны.',
        fit('conditional','9–10 входит Family 6–17 и Junior 8–17; нужен adult+child счёт.'),fit('conditional','Family прямо 6–17; конкретный курс 6–7/присмотр при workation ещё неизвестен. Не самостоятельный пансионс 6.'),
        'Кандидат на альпийский отдых обоих братьев с родителями; рекламное «от 500» не семейный бюджет.',
        ['Назначенная группа 6–7/присмотр, adult unit/childfee/room, transfer/Sunday night, package иполный семейный quote.'],
        [('Family2027:age/adult packages',FRI_FAMILY),('Отдельный Junior 8–17/parent extras',FRI),('Договор',FRI_TERMS)],status='published_2027',role='language_lessons',priority=['general','family'],sessions=fri_pairs)
    detail(p,FRI_FAMILY,date_precision='published_rule',date_rule=fri_rule)

    for slug,name,fmt,age,label,housing,osc in [
        ('altitude-day-junior','Junior Day','day','Junior 6–14; booking form допускает 5.5, но год неизвестен.',
         'CHF 975/1 нед.; при 2+неделях 950/нед. — own table безгода.',
         'Monday–Friday 09–16, lunch включён; семья живёт отдельно. Marmots 3–5 — другой курс.',fit('conditional','6–7 подходит 6–14; сначала год/неделя/группа.')),
        ('altitude-residential-junior','Residential','boarding','Residential 7–14; общий day 3–14 не возрастпансиона.',
         'CHF 2950/1 нед.,5550/2,7750/3,9950/4 — own table безгода.',
         '4*private Swiss-style chalets, fullboard/24 ч, laundry 2+нед. Адрес chalet не адресофиса.',fit('conditional','Только после 7-летия к старту; до 7 пансион не подходит.')),
    ]:
        put(slug,'Altitude · '+name+' English / Mountain Adventure','CHE','Verbier ·actualmeetingpoint/chalet подтвердить','general,languages,sport,adventure',fmt,age,
            'Native qualified English teachers, классы 3–6; day прямо native EN staff. English полного Mountain Adventure подтвердить.',
            'Утром English либо mountain adventures; далее sports, nature, cooking, excursion/teamwork. Специализацию можно менять между неделями; robotics/AI не заявлены.',
            'Day 28 июня–13 августа; Residential 27 июня–31 июля, Sunday–Saturday 1–5 нед. Год own dates не указан; booking©2025/birthdate ranges. Подтверждённого 2027/ICS нет.',
            fee(None,label,'Обычные занятия/excursions; day lunch, board fullboard/chalet; точный invoice package подтвердить.',
                'Geneva return transfer от 200; golf/swim 150 час, tennis 200, language 100, paragliding 225. Insurance не предоставляется. Отдельный 5-week price не прочитан.',
                'Общие terms:20%deposit, остаток 31 мая; >30 дней full refund, within 30:50%невозврат, within 2 weeks 100%. Год/границы по новому договору.'),housing,
            fit('conditional','9–10 соответствует Junior; реальный 2027 course/год/место неизвестны.'),osc,
            'Общий EN альпийский кандидат; отделяем day 6 от boarding 7 и не приписываем датам 2027.',
            ['Новыйсезон/точные dates/полный price, birthday, EN Mountain Adventure, place/insurance/contract.'],
            [('Конкретныйформат/возраст/тарифбезгода',ALT+('day-camp/' if fmt=='day' else 'residential-camp/')),('Booking безновогогода',ALT+'booking'),('Общие terms',ALT+'terms-privacy-policy/')],role='language_lessons',priority=['general',fmt])

    bell_pairs=[['2026-10-19','2026-10-23'],['2027-02-15','2027-02-19'],['2027-04-05','2027-04-09']]
    p=put('bell-geneva-explorer','Bell Switzerland · Holiday Explorer','CHE','Bell Colombettes · 12 Chemin des Colombettes, 1202 Genève','general,languages,art,adventure','day','Holiday Explorer: 4–10 лет. Nursery и постоянная школа имеют другие возрастные категории.',
        'Английский в самой дневной программе; принимают все языковые уровни.',
        'Тематические проекты и игры, самостоятельность, творческое портфолио; максимум 12 детей. Для свободного английского проверить сложность задач. Робототехника и ИИ не заявлены.',
        'Осень: 19–23 октября 2026. Зима: 15–19 февраля 2027. Весна: 5–9 апреля 2027. Все три отдельные карточки публикуют возраст 4–10 и одинаковые тарифы.',
        fee(None,'CHF 415 / полдня; CHF 725 / полный день, за одну неделю сезона 2026/27.',
            'Английский курс и проекты; обед прямо включён. Уточнить подачу обеда в варианте половины дня.',
            'Жильё семьи, дорога, страховка и дополнительный присмотр отдельно. Оборудование в собственность ребёнку не обещано.',
            'Прочитанные Terms & Conditions регулируют использование сайта. Это не договор лагеря: аванс, возврат и внешний приём пока неизвестны.'),
        'Без ночёвки. Зима и весна: 09:00–12:30 либо 09:00–17:00. Осенняя карточка часы не указывает; их не переносим автоматически.',
        fit('conditional','Возраст 8–10 в 2026–27 подходит; проверить уровень, внешний приём и место.'),fit('conditional','Возраст 5–7 подходит; подтвердить группу, присмотр и место.'),
        'Практичный английский день для обоих братьев на осень, зиму и весну с опубликованными датами и ценой.',
        ['Часы осенней недели, обед при половине дня, уровень группы, внешний приём, договор отмены и итоговый счёт.'],
        [(k.title()+' Explorer',BELL+'courses/'+k+'-explorer/') for k in ['autumn','winter','spring']]+[('Правила сайта, не договор лагеря',BELL+'terms-conditions/')],
        status='published_2026_27',role='primary',priority=['general'],sessions=bell_pairs)
    p['price']['season']='2026/27'
    detail(p,BELL+'young-learners/holiday-camps/',date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'])
    for r,k in zip(p['timing']['session_details'],['autumn','winter','spring']):r['source']=BELL+'courses/'+k+'-explorer/';r['label']=k.title()+' Explorer'
    bc_pairs=[['2026-10-19','2026-10-23'],['2027-02-08','2027-02-12'],['2027-04-05','2027-04-09'],['2027-07-05','2027-07-09']]
    p=put('british-council-paris-primary','British Council Paris · Primary holiday projects','FRA','Paris Maubourg-Cler · 11 rue Cler, Paris 7e','general,languages,art','day','Конкретная программа: классы CE1–CM2. Общая брошюра 3–18 лет охватывает разные курсы.',
        'Проекты и игры на английском. Эквивалентность CE1–CM2 и распределение иностранного ребёнка по группам нужно подтвердить.',
        '30 учебных часов за пять дней: проекты, устная практика, игры и итоговый показ родителям. Это общий языковой курс; робототехника и международная награда не заявлены.',
        '19–23 октября 2026; 8–12 февраля, 5–9 апреля, 5–9 июля 2027. Только четыре даты младшей страницы; дополнительные недели средней школы сюда не относятся.',
        fee(None,'EUR 799 / 5 дней, 30 часов по таблице 2026/27.',
            'Учёба и проекты. Холодный обед приносить с собой. Праздничный день может менять часы и стоимость.',
            'Жильё, обед, дорога и страховка семьи отдельно. Второму и следующим детям скидка EUR80, текущая loyalty discount EUR50; не суммируются. Общая PDF пишет loyalty/sibling EUR80 под условиями — итоговую скидку подтвердить.',
            'Подтверждают после полной формы и полученного платежа. Аванс и отмена на прочитанной странице программы не раскрыты.'),
        'Понедельник–пятница 09:00–16:30. Без ночёвки и дополнительного присмотра.',
        fit('conditional','Возраст 9–10 не доказывает класс CE1–CM2; нужен текущий класс и назначенная группа.'),fit('unknown','Год рождения 2020 не доказывает CE1. До определения класса допуск не подтверждён.'),
        'Проектная английская неделя в Париже с проверенным календарём 2026/27. Оценить пользу для уже свободного английского.',
        ['Школьный класс и эквивалентность, уровень проекта, внешний приём, обед, договор отмены и итоговый счёт.'],
        [('Primary 2026/27: CE1–CM2, четыре даты и цена',BC),('Общая брошюра разных курсов 3–18','https://www.britishcouncil.fr/sites/default/files/stages_anglais_2026_2027_web.pdf')],
        status='published_2026_27',role='primary',priority=['general'],sessions=bc_pairs)
    p['price']['season']='2026/27';detail(p,BC,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'])

    kid_fee=fee(None,'Прайс лагеря 2027 не прочитан. Тарифы постоянной школы и брошюра 2024/25 не являются сметой нового лагеря.',
        'Английские тематические проекты. Состав питания и материалов в новом тарифе пока неизвестен.',
        'CGV: ежегодное членство, материалы и сборы изменения отдельно; суммы в брошюре. EUR15 за eCESU/eANCV — сбор способа оплаты, а не общий регистрационный взнос. Обед, дополнительный присмотр и жильё семьи отдельно.',
        'CGV августа2025: аванс невозвратный. Holiday refund: более60 дней100%;59–46:70%;45–31:50%;30–7:20%;менее7:0. День60 не описан. Членство/сборы удерживаются; eCESU/eANCV возвращают кредитом. Нужен актуальный счёт/договор2027.')
    for slug,name,age,mat,osc in [
        ('kidooland-activate','Activate','Французская карточка: 4–6 лет / maternelle.',fit('later','Матвей старше6; выбирать старшую группу.'),fit('conditional','Оскар6 на границе группы; после7 нужен Advance.')),
        ('kidooland-advance','Advance','Французская карточка: 6–8 лет / CP–CE1.',fit('later','В2027 Матвей9–10, старше8.'),fit('conditional','Оскар6–7 входит6–8; класс и распределение подтвердить.')),
        ('kidooland-elevate','Elevate','Французская карточка: 8–14 / CE2+. English page обычно4–12, старше12 — немного мест junior leaders.',fit('conditional','9–10 входит Elevate; проверить класс и сложность.'),fit('later','6–7 ниже8.')),
    ]:
        put(slug,'KidooLand · '+name,'FRA','Vallauris · Annexe/Loft, 1890 Chemin de St Bernard; точное помещение подтвердить','general,languages,science,art','day',age,
            'Занятия полностью на английском; французский и родной язык разрешены в свободной игре. Собственная страница прямо приветствует приезжающие международные семьи.',
            'Кулинария, театр, музыка, искусство; темы науки, космоса и природы, командные игры. STEM темы не доказывают отдельную робототехническую смену. Особый допуск3-летних через знакомую группу/пробу не относится к обычной категории4+.',
            'Есть анонс каникул2026/27, но camp brochure2027 «coming soon». Точных новых недель, тем и цен в прочитанном тексте нет. French page: неделя/3дня; English page: только недельные M–F, закрытоChristmas/частьAugust. Реальное расписание подтвердить; ICS не создан.',
            kid_fee,'English page:09:00–17:00, утренний/вечерний присмотр отдельно; без ночёвки, сон для4+ не предусмотрен. Нужны civil liability insurance, прививки и PAI при необходимости; медицинское согласование и полный родительский портал до окончательного допуска.',mat,osc,
            'Английский день на Riviera с отдыхом всей семьи; братьям нужны разные возрастные группы. Общее объявление не подтверждает открытые места на все каникулы.',
            ['Брошюра2027, точные недели/темы/цена, возраст и класс, неделя/3дня и закрытые периоды, обед/присмотр/взносы, медицинские документы иностранной семьи.'],
            [('Французские группы и анонс2026/27',KID+'stages-vacances-4-16-ans'),('English: приезжающие семьи, часы и закрытые периоды',KID+'holidays'),('Новая camp brochure покаcoming soon',KID+'brochure'),('CGV августа2025',KID+'conditions-d-inscription')],role='primary',priority=['general'])

    es_terms='Страница бронирования содержит сроки рассрочки/скидок2025, это не договор2027. Актуальные аванс, отмена, страховка и счёт пока неизвестны.'
    for slug,name,age,theme,programme,language,role,label,mat,osc,place in [
        ('englishsummer-tech','TECH Camp','8–15: LEGO WeDo8–11, Mindstorms12–15.','robotics,coding,games,languages',
         '15 часов английского в неделю утром и15 часов робототехники после обеда; преподаватели Dynamind. Строят/программируют роботов, делают игры и сайты. Минимум10 участников; робот в собственность не обещан.',
         'Уроки английского с носителями подтверждены; язык робототехнических мастерских не указан. EN/ES поддержку техники нужно уточнить.','language_lessons','В FAQ EUR905 за8дней, но год тарифа не указан. Это не подтверждённая цена2027.',
         fit('conditional','9–10 подходит WeDo8–11; проверить язык и сложность для его опыта.'),fit('later','6–7 ниже минимальных8 TECH.'),'Prades · конкретный новый заезд/корпус подтвердить'),
        ('englishsummer-multiactivity','English + Multiactivity','Конкретный общий курс5–15.','general,languages,sport,art',
         '3/4часа английского ежедневно, носители, группы10–12, Cambridge syllabus. Затем бассейн, спорт, творчество, командные игры и вечерняя жизнь. Учебный план не означает включённый официальный экзамен.',
         'Английский уроков подтверждён; язык всей лагерной жизни уточнить.','language_lessons','Точная цена2027 не прочитана.',
         fit('conditional','9–10 входит5–15; проверить конкретный campus и уровень.'),fit('conditional','6–7 входит5–15; размещение, присмотр и внешний приём.'),'Сеть Vallclara/Poblet/Tamarit/Prades · распределение2027 неизвестно'),
        ('englishsummer-alive','English Alive','Описание6–14, таблица5–14: конфликт младшей границы.','general,languages,sport,adventure',
         'Разговорный английский через практические активности, игры и командные проекты без книг и классов. Общая программа в природе, технический курс не заявлен.',
         'Носители проводят сами практические занятия на английском; язык всех общих служб уточнить.','camp_life','Точная цена2027 не прочитана.',
         fit('conditional','9–10 входит оба диапазона; подтвердить возраст конкретной недели.'),fit('conditional','6–7 после6-летия; нижнюю границу5 из таблицы не считать подтверждённым допуском.'),'Poblet или Tamarit · новая конкретная смена неизвестна'),
    ]:
        included='TECH FAQ: полный пансион, бассейн, вечера/тематические активности,15чEnglish+15чrobotics/нед.' if slug=='englishsummer-tech' else 'Пансион и программа описаны; полный состав нового тарифа неизвестен.'
        put(slug,'English Summer · '+name,'ESP',place,theme,'boarding',age,language,programme,
            'TECH: июль без года; Alive: август/сентябрь без года; общие точные даты2027 не прочитаны. Course2026/27 на главной относится к школе вожатых, не каталогу летних смен2027. Новый ICS не создан.',
            fee(None,label,included,'Трансфер, страховка, дополнительные занятия, техника и сборы по актуальному счёту. Робот в собственность не обещан.',es_terms),
            'В сети общие комнаты4/6. Конкретное здание, размещение, диету и медицинское сопровождение нового заезда подтвердить.',mat,osc,
            'Один испанский организатор с тремя разными треками: TECH8+, общий5+, разговорный Alive6+/спорный5. Новые даты не придумываем.',
            ['Каталог2027, даты, возраст смены и campus, язык технического трека, laptop/kit, полный счёт, трансфер, страховка и отмена.'],
            [('TECH: программа и FAQ EUR905 без года',ES+'campamentos-de-verano-ingles/tematicos-deportivos/tecnologico/'),('Multiactivity и Alive',ES+'campamentos-de-verano-ingles/idiomas/'),('Бронирование со сроками2025',ES+'informacion-campamentos-verano-ingles/como-reservar/')],role=role,priority=['technical'] if slug.endswith('tech') else ['general','boarding'])

def extend_report_v82(report):
    report['shortlist'].extend([
        dict(label='Швейцария · вместе двум братьям',slugs=['frilingue-braunwald-family','bell-geneva-explorer','altitude-day-junior','altitude-residential-junior'],reason='Family Braunwald6–17 требует конкретную группу6–7 и семейный счёт; самостоятельный Junior с8. Bell4–10 с тремя датами2026/27. Altitude: день6+, пансион7+, но год собственного расписания неизвестен.'),
        dict(label='Швейцария · пансион Матвею2027',slugs=['ensr-junior-languages','ensr-junior-multisport','cjsa-languages-sports','cjsa-little-fun','frilingue-braunwald-language','frilingue-braunwald-coding'],reason='ENSR8–11 CHF2150/нед.; CJSA Junior8–10 CHF750board/550day, языковой9–17 CHF900/700; Braunwald Junior950 плюс optional coding150. Английский уроков не весь спорт. Coding прямоEN/minimum3, небольшой beginner website workshop; ENSR форма ещё2026.'),
        dict(label='Франция · английские каникулы и классы',slugs=['british-council-paris-primary','kidooland-activate','kidooland-advance','kidooland-elevate'],reason='BC Primary CE1–CM2 EUR799 и четыре даты. Год рождения не доказывает школьный класс. KidooLand принимает приезжающие семьи, занятияEN; новая camp brochure, точные цены/недели неизвестны. Братьям разные группы.'),
        dict(label='Испания · общий и технический пансион',slugs=['englishsummer-tech','englishsummer-multiactivity','englishsummer-alive'],reason='TECH8–15:15чEnglish+15чrobotics. EUR905/8дней без года, язык роботов неизвестен. Общий5–15; Alive6–14 против5–14. Точных2027 нет. СвязьL006 без повторного ICS.'),
    ])
    report['gaps'].extend([
        dict(country='Швейцария',iso='CHE',provider='v82: ENSR/CJSA Junior2027',detail='ENSR сайт2027, форма2026; разные страховые правила, единица transfer fee неизвестна,22периода против88examlessons. CJSA языковой9–17, Junior8–10; шесть недель без1–7августа. Day/board тарифы, FAQ08:30–18, неполные границы отмены; English спорта неизвестен.',next_action='Договоры2027, язык выбранных групп, размещение, страховка и полные счета. Швейцария целиком не аудирована.',url=ENSR+'registration'),
        dict(country='Швейцария',iso='CHE',provider='v82: Family/Altitude/Bell',detail='Braunwald Family6–17 против Junior8–17;500workation не цена семьи, курс ребёнка6–7 неизвестен. CodingEN150/minimum3/ownlaptop без duplicate ICS. Altitude год расписания неизвестен, day6+/board7+. Bell4–10,415half/725full,три даты; web terms не договор лагеря.',next_action='Группа6–7/childfee/adultunit/room/Sundayairport для семьи; новый сезонAltitude; Autumnчасы/договорBell.',url=FRI_FAMILY),
        dict(country='Франция',iso='FRA',provider='v82: школьные классы и Kidoo2027',detail='BC четыреPrimaryдаты CE1–CM2, не вторыеsecondaryweeks/общаяbrochure3–18; текущаяloyalty50 противPDF80. Kidoo French4–6/6–8/8–14, Englishобычно4–12/немногоleaders12–16. Camp2027comingsoon, weeklyvs3days/Christmasclosure остаются расхождениями.',next_action='Классы, новое расписание/брошюра/цена с membership/supplies, закрытые периоды и иностранные медицинские документы.',url=KID+'brochure'),
        dict(country='Испания',iso='ESP',provider='v82: EnglishSummer треки и год',detail='TECH8–15/minimum10/WeDo8–11/Mindstorms12–15/15чEN+15чrobotics. FAQ905/8daysбезгода. Общий5–15;Alive6–14vs5–14. Точных2027нет,paymentdeadlines2025,L006linked; языкroboticsнеизвестен.',next_action='Каталог2027, смены/campus, EN/ESтехническихзанятий и полные счета; остальные испанские и все приоритетные страны остаются открыты.',url=ES+'campamentos-de-verano-ingles/tematicos-deportivos/tecnologico/'),
    ])
