"""Primary-source programme distinctions: ages, language, contracts and dates."""
import datetime

def add_france_spain(add, src, fit, profiles):
    def put(*a, **k):
        add(*a, **k)
        p=profiles[-1]; p['checked']='2026-10-05'
        for s in p['sources']: s['checked']=p['checked']
        return p
    def fee(year,label,included,extras,deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def dated(p, rows, source, scope='camp_session', rule=None):
        p['timing']['sessions']=[[s,e] for s,e,lab,price in rows]
        p['timing']['session_details']=[dict(start=s,end=e,label=lab,price=price,place=p['place'],source=source,formats=p['formats'],date_scope=scope) for s,e,lab,price in rows]
        if rule:
            for v in p['timing']['session_details']:
                v.update(date_precision='published_rule',date_status='Опубликованное правило · даты рассчитаны',date_rule=rule)

    kr='https://kidsrobots.fr/about/'
    windows=[('2026-10-19','2026-10-23'),('2026-10-26','2026-10-30'),('2027-02-08','2027-02-12'),('2027-02-15','2027-02-19'),('2027-04-05','2027-04-09'),('2027-04-12','2027-04-16'),('2027-07-05','2027-07-09'),('2027-08-16','2027-08-20'),('2027-08-23','2027-08-27')]
    for slug,name,age,programme,amount,mat in [
        ('kidsrobots-kids','KidsRobots · Kids-Robots 8–9','8–9; CE2 / CM1 / CM2',
         'Вводная робототехника: управление через infrared, планшет/смартфон и базовые алгоритмы. Пять утренних занятий 09:30–12:00; 12,5 часа рассчитаны из опубликованного расписания. Для детей с тремя годами опыта проверить, достаточно ли сложный курс.',250,
         fit('conditional','В 2027 только до 10-летия; требуется соответствие CE2/CM1/CM2. В октябре 2026 возможный возраст 8–9 подходит.')),
        ('kidsrobots-mini','KidsRobots · Mini-Robots 9–12','9–12; CM1 / CM2 / Collège',
         'Блочная программа управления техническими объектами и наземными/летающими роботами, алгоритмы и задачи разных уровней. Пять утренних занятий 09:30–12:00, суммарно 12,5 часа по расписанию; оборудование конкретной группы подтвердить.',300,
         fit('conditional','2027: возраст 9–10 подходит; нужен класс CM1/CM2/Collège. В октябре 2026 только после 9-летия.'))]:
        p=put(slug,name,'Франция','FRA','Montpellier · 42 rue du Faubourg Boutonnet','robotics,coding','day',age,
            'EN/ES/RU преподавания и поддержки не доказан. Французский текст сайта сам по себе не устанавливает язык занятия; иностранный EN/ES поток нужно подтвердить.',
            programme,'Опубликованы 9 окон осени 2026, зимы, весны и лета 2027. 26–30 октября прямо перечёркнуто как complet; места остальных недель не доказаны.',
            fee(2027,f'EUR {amount} / 5 половин дня по текущей странице 2026/27; окончательный счёт выбранной недели подтвердить.',
                'Пять занятий; право забрать робота/набор и включение расходников отдельно не установлено.',
                'Это утро, не полный день: жильё семьи, питание и послеобеденный присмотр отдельно.',
                'Аванс, отмена, комплект и условия иностранного ребёнка не опубликованы в прочитанной странице.'),
            'Местная дневная мастерская 09:30–12:00; собственного пансиона нет.',mat,
            fit('later','Возраст 5–6 в 2026 и 6–7 в 2027 ниже минимума '+('8' if amount==250 else '9')+'.'),
            'Техническая практика с реальными будущими датами и разными возрастными ступенями; не международный EN пансион и не независимый мировой лидер.',
            ['Подтвердить класс, язык, оборудование, подходящий после трёх лет практики уровень, свободные места и правила оплаты.'],
            [src('Возраст, содержание, даты, prix и complet',kr),src('Адрес мастерской','https://kidsrobots.fr/contact/')],status='published_2026_27',priority=['technical'])
        dated(p,[(s,e,'Пять утренних мастерских',f'EUR {amount} / 5 половин дня') for s,e in windows],kr,scope='day_camp_window')
        p['timing']['session_details'][1]['availability']=dict(status='closed',label='26–30 октября 2026: complet по официальной странице')

    ab='https://activebrainbordeaux.com/?lang=fr'
    for slug,name,age,s,e,label,morning,full,closed in [
        ('activebrain-holiday','Active Brain · Holiday Science 7–10','7–10','2026-10-20','2026-10-23','Четыре осенних дня',190,300,False),
        ('activebrain-little-holiday','Active Brain · Little Spooky 4–6','4–6','2026-10-26','2026-10-30','Пять осенних дней · мест нет',240,380,True)]:
        younger=closed
        p=put(slug,name,'Франция','FRA','Bordeaux · 17 Cité Dutrey, 33300','science,languages,art','day',age,
            'Science 10:00–12:00 прямо на EN. Отдельный Mandarin atelier 14:00–15:00 на ZH; язык свободной игры и всего дня не установлен. Это научная программа, не English-only день.',
            'Небольшая локальная группа, operator maximum 6: практические опыты с цветом, газами, водой и моделью лёгких. Утро 09:00–12:00 либо полный день 09:00–17:00 с садом и творчеством; робототехника не заявлена.',
            s+'–'+e+'. '+('Fully booked; календарь сохраняет факт закрытия, семейный .ics исключает.' if closed else 'Оператор пишет registrations open / limited; это не подтверждённое место.')+' Даты 2027 пока не опубликованы.',
            fee(2026,f'EUR {morning} утро / {full} полный день за '+('5' if closed else '4')+' дней.',
                'Материалы и выбранные занятия.', 'Обед принести с собой; жильё, дорога семьи и дополнительный присмотр не включены.',
                'FAQ: отмена более чем за 14 дней — полный возврат, за 7–13 — 50%, менее 7 — без возврата. Ровно 14 дней формулировкой не покрыто: уточнить договор, не достраивать правило.'),
            'Дневной локальный центр; гибкая передача 09:00–10:00 и 16:30–17:00, ночёвок нет.',
            fit('not_eligible' if younger else 'candidate','Матвей 8–9 в октябре 2026: '+('старше максимума 6.' if younger else 'соответствует 7–10; внешний допуск отдельно.')),
            fit('candidate' if younger else 'later','Оскар 5–6 в октябре 2026: '+('подходит 4–6, но эта группа закрыта.' if younger else 'ниже 7; возраст будущего неопубликованного лагеря не переносится на эту смену.')),
            'Прямое доказательство научного EN и понятный местный формат; возраст братьев требует разных потоков, младший осенний уже закрыт.',
            ['Проверить новый сезон, места, нужную возрастную группу и точную отмену; полный день содержит отдельный Mandarin, обед свой.'],
            [src('Science EN, расписание, цены, FAQ и real availability',ab)],status='published_2026',priority=['technical'],confirmed=['EN'])
        dated(p,[(s,e,label,f'EUR {morning} утро / {full} день')],ab,scope='day_camp_window')
        if closed:
            p['availability']=dict(status='closed',label='Осенний Little Spooky 2026 fully booked')
            p['timing']['session_details'][0]['availability']=p['availability'].copy()

    p=put('activebrain-monthly','Active Brain · Monthly Little Scientists','Франция','FRA','Bordeaux · 17 Cité Dutrey, 33300',
        'science,languages','day','4–6',
        '10:00–11:00 научная часть EN; 11:00–12:00 Mandarin ZH. Отдельные языковые части, а не два часа науки на английском.',
        'Двухчасовая научно-языковая мастерская раз в месяц; максимум 6 по заявлению оператора. Будущие темы: Static Magic, Rainbow Water Walk, Christmas Soap Lab. Это клуб, не недельный лагерь.',
        '7 октября, 4 ноября и 2 декабря 2026, 10:00–12:00. Прошлый 23 сентября не создаёт новое будущее событие; 2027 не объявлен.',
        fee(2026,'EUR 45 / одно занятие; четыре за 160, pass действует 12 месяцев.',
            'Научная часть и связанный Mandarin, материалы.', 'Присмотр и питание на остаток дня, поездка и жильё родителей отдельно.',
            'Pass non-refundable; по уведомлению за 24 часа возможен перенос. Пропуск без уведомления списывает занятие; уточнить реальную дату для переноса.'),
        'Только 10:00–12:00 в отдельные среды; пансиона нет.',
        fit('not_eligible','Матвей старше 6.'),fit('conditional','Оскару только пока 6 или младше; на будущий год после 7-летия максимум 6 уже не подходит.'),
        'Небольшой EN science опыт для Оскара во время пребывания в Бордо; явно отделён от полноценных каникул.',
        ['Проверить место, возраст, оплату разово или pass и дату переноса; отдельный Mandarin не обязателен ли для science-only варианта.'],
        [src('Monthly club: EN/ZH, три будущих даты, pass и перенос',ab)],status='published_2026',confirmed=['EN'])
    dated(p,[(s,s,l+' · 10:00–12:00 местное время','EUR 45 / 2 часа') for s,l in [('2026-10-07','Static Magic'),('2026-11-04','Rainbow Water Walk'),('2026-12-02','Christmas Soap Lab')]],ab,scope='workshop_window')

    ir='https://www.ibsofprovence-camps.com/dates-fee'
    ib='https://www.ibsofprovence-camps.com/boarding-students-ibs-summer-camp'
    for slug,name,age,url,programme,formats,price,language,confirmed,mat,osc in [
        ('ibs-mini','IBS of Provence · Mini 4–6','4–6; potty training уже завершён',
         'https://www.ibsofprovence-camps.com/bilingual-summer-camps-for-kids-4-6-year-olds',
         'Билингвальные воспитатели, игра, спорт, поделки, экскурсия и тихий час. Для внешних детей описана адаптация; дневной сон не является ночёвкой. Часы расходятся: intro до 15:50, body до 15:30; daycare 08:30–17:00.',
         'day',fee(None,'Отдельная цена Mini 4–6 не найдена. Таблица 2026 Mornings 6+ / Day Students не доказывает тариф четырёх- и пятилетним.',
                    'Mini описывает lunch/snack и материалы.', 'Early/late daycare и все доплаты согласовать; не подставлять старший тариф.', 'Условия следующего сезона и отмены неизвестны.'),
         'Прямо описаны bilingual staff и смешанная EN/FR детская среда. Это игровой билингвальный Mini, не подтверждённая техническая EN программа.',['EN','FR'],
         fit('not_eligible','Матвей старше 6.'),fit('conditional','В 2027 только до 7-летия; нужен самостоятельный туалет и допуск внешнего ребёнка.')),
        ('ibs-kids','IBS of Provence · Kids 7–8','7–8; boarding minimum 9+ не переносится вниз',
         'https://www.ibsofprovence-camps.com/kids-camps-bilingual-7-8yo',
         'F1: утренние EN/FR language classes. F3: язык + спорт/творчество; day до 15:30, daycare до 17:30. Фраза day/boarder в Kids расходится с общей таблицей и boarding-page 9+: ночёвки 7–8 не считаются доступными.',
         'day',fee(2026,'Архив: EUR 880 / 2 недели утро, 1 250 день; 1 320 / 1 875 за 3 недели. Точное применение Kids F3 и цена 2027 требуют quote.',
                    'Выбранная дневная программа; утро без обеда.', 'Daycare, Aix shuttle +50 и спортивные опции отдельно; единицу shuttle не установили.', '2027 условия, аванс и возвраты не опубликованы.'),
         'Утренние языковые уроки EN или FR подтверждены. Язык всех спорта/творчества отдельно неизвестен.',['EN','FR'],
         fit('not_eligible','В 2027 Матвей 9–10, старше Kids 7–8; выбрать 9–17.'),fit('conditional','Только после 7-летия; 6-летний ещё не соответствует Kids.')),
        ('ibs-general','IBS of Provence · General 9–17','9–17; отдельный boarding minimum 9+',
         'https://www.ibsofprovence-camps.com/copie-de-9-17ans',
         'F2: 5 часов языковых занятий без дневных активностей; F3: 3 часа языка + 2 часа спорта/творчества. Общая language programme, робототехника не доказана. Boarding: школьные residences, meals, бельё, присмотр; laundry только при 3+ неделях.',
         'day,boarding',fee(2026,'Архив: EUR 1 250 день / 1 980 пансион за 2 недели; 1 875 / 2 970 за 3 недели.',
                    'Выбранные языковые занятия; пансион включает размещение и питание по boarding описанию.',
                    'Boarding weekend +200, shuttle Aix +50; количество weekend/направлений уточнить. Football +196, tennis +300, tournament tennis +570 — опции 2026, не обязательные сборы 2027.',
                    'Прайс 2027, договор, аванс и отмена ещё неизвестны.'),
         'Курс EN/FR по выбору подтверждён; английский всех лагерных активностей и технического обучения не установлен.',['EN','FR'],
         fit('candidate','В 2027 9–10: возраст 9+ подходит; класс/пансион/следующий набор отдельно.'),fit('later','В 2027 6–7, ниже 9.'))]:
        p=put(slug,name,'Франция','FRA','Luynes / Aix-en-Provence · IBS campus','general,languages,sport,art',formats,age,language,programme,
            'Прочитан архив 2026: весна 13–24 апреля, лето 22 июня–21 августа. Все эти окна уже прошли; новые смены 2027 не опубликованы, точный будущий календарь не создаётся.',
            price,'Дневная возрастная программа.' if formats=='day' else 'Дневной либо школьный пансион с 9 лет; airport/TGV arrival slots и полный fee сверить.',mat,osc,
            'Международный школьный лагерь с отдельными младшими программами; важны фактический поток, внешнее поступление и разница day/boarding.',
            ['Получить новый календарь/прайс, конкретную группу, языковую нагрузку уже англоговорящему ребёнку, дневной режим и договор.'],
            [src('Возрастная programme',url),src('Только архив 2026 dates/fees',ir),src('Boarding minimum 9+ и residence',ib)],confirmed=confirmed,priority=['general'])
        p['language_evidence_role']='bilingual' if slug=='ibs-mini' else 'language_lessons'

    cm='https://www.cmef-monaco.fr/en/programmes/junior-summer/'
    p=put('cmef-junior','CMEF · Cap d’Ail Junior Summer','Франция','FRA','Cap d’Ail · 1 allée Jean Cocteau','general,languages,sport','boarding','12–16',
        'Header обещает French (or English) 15 ч/нед, но body называет French обязательным. Наличие EN группы 2027 противоречиво; не считаем подтверждённым английский обучения или жизни.',
        'Общий международный языковой пансион с культурой, спортом, экскурсиями, выбором afternoon activities. Оператор описывает закрытый кампус и круглосуточный надзор; самостоятельные выходы 13+ только с родительским разрешением и в группе. Это будущая подростковая ступень.',
        'HTML rates2027 содержит 18 разрешённых комбинаций старта и 1/2/3/4 недель. Вс–Сб: концовки рассчитаны по явно опубликованному правилу. Brochure/nav по-прежнему 2026, их тарифы не подменяют HTML2027.',
        fee(2027,'EUR 990 / 1 неделя только 20 июня, 25 июля и 1 августа; 2 200 / 2, 3 135 / 3, 4 180 / 4 недели в разрешённых строках.',
            'Жильё 3–4, full board, язык 15 ч/нед, основные activities, transfer Nice Airport / Monaco station; laundry с 2 недель.',
            'Перелёт, personal expenses и возможная страховка/доплаты требуют full invoice.', 'Аванс, договор и отмена 2027 не установлены.'),
        'Residential; адрес во Франции, несмотря на Monaco в брендинге.',fit('later','Матвей 9–10 в 2027, ниже 12.'),fit('later','Оскар 6–7 в 2027, ниже 12.'),
        'Будущий общий international вариант; сейчас не входит в доступный обоим маршрут и семейный .ics.',
        ['На будущее подтвердить EN поток, 2027 договор и полный счёт; возраст 12+ обязателен.'],[src('HTML2027: age, rates, arrival rule и конфликт EN/FR',cm)],status='published_2027',priority=['general'])
    rows=[]
    for s,lengths in [('2027-06-20',[1,2,3,4]),('2027-06-27',[2,3,4]),('2027-07-04',[2,3,4]),('2027-07-11',[2,3,4]),('2027-07-18',[2,3]),('2027-07-25',[1,2]),('2027-08-01',[1])]:
        for n in lengths:
            e=(datetime.date.fromisoformat(s)+datetime.timedelta(days=n*7-1)).isoformat()
            rows.append((s,e,f'CMEF · {n} нед.',f'EUR '+{1:'990',2:'2 200',3:'3 135',4:'4 180'}[n]))
    dated(p,rows,cm,rule='Таблица STAY RATE DETAILS 2027 публикует старт и разрешённое число недель; arrival Sunday / departure Saturday. Конец = старт + 7 × число недель − 1 день. Прочерки не создают смен.')

    nh='https://www.hescamps.com/campamentos-12'; nr='https://www.natukcamps.com/robotics-camp'; np='https://www.natukcamps.com/precios'
    p=put('natuk-robotics','NATUK Camps · Robotics / HES booking','Испания','ESP','Esterri d’Àneu · Pyrenees; hotel 2027 уточнить','robotics,coding,general,languages,sport','boarding,day',
        'HES 6–16 vs NATUK 6–17. Минимум совпадает; иностранный day/boarding младший допуск и возраст следующего сезона уточнить.',
        'HES прямо описывает robotics in English, но это afternoon workshop. Утро — отдельный выбираемый camp / языковые уроки. Полная EN жизнь и каждый день техники не доказаны.',
        'LEGO Mindstorms, sensors, сборка и программирование. Примеры 17 моделей не обещают 17 готовых роботов каждому. Нужно выбрать morning programme отдельно. NATUK — оператор, HES — канал одного предложения; не два независимых лагеря.',
        'NATUK catalogue2026: 28 июня–18 июля; robotics-page 29 июня–19 июля без года. Не выбираем один из вариантов и не создаём дату 2027. HES day campus для local residents не доказывает иностранный robotics day.',
        fee(None,'Числовой тариф выбранного robotics package не найден: operator /precios направляет к distributors. Неизвестный all-in, не нулевая цена.',
            'По общему операторскому списку: full board, язык, activities, базовая медицинская/accident/RC страховка; точный morning пакет согласовать.',
            'Дорога, rental, medicines, personal expenses. Brochure2026 laundry EUR 5/load, HES пишет included: расхождение. После старта смена camp +45, Adventure +75, сверх нового camp fee по /precios; не универсальный платёж каждому.',
            'После старта cancellation/withdrawal без возврата по /precios; аванс и pre-start отмена не установлены.'),
        'Boarding. HES robotics называет EuroSki****, operator brochure2026 — Trainera***: кампус 2027 неизвестен. Day вариант только после подтверждения visitor eligibility.',
        fit('conditional','9–10: возраст подходит; morning/afternoon пакет и реальный 2027 набор нужны.'),fit('conditional','6–7: младший минимум 6 по страницам; формат ночёвок, EN и независимость подтвердить.'),
        'Технический международный кандидат в Испании с прямым EN описанием; объём, отель, полный счёт и даты остаются решающими.',
        ['Подтвердить единый операторский пакет, hotel2027, afternoon tech hours/platform, иностранный day, младший boarding, EN и invoice/cancellation.'],
        [src('HES robotics EN и возраст',nh),src('NATUK programme и yearless dates',nr),src('Включения, доплаты; цены через distributors',np),src('Официальный English brochure2026','https://www.natukcamps.com/descargas/'),src('Day campus eligibility','https://www.hescamps.com/campus-en-los-pirineos')],priority=['technical','both'],confirmed=['EN'])

    cr='https://www.costablancacamp.com/en/spanish-english-robotics-summer-camp-in-spain/'
    p=put('costablanca-robotics','Costa Blanca Camp · Crea tu Mundo Robotics','Испания','ESP','Elche / Alicante · La Loma farm-school','robotics,coding,languages,general,sport','boarding',
        'Возраст и отдельный минимум ночёвок в прочитанных страницах не найдены: не обещаем допуск 6 или 9 лет.',
        'Morning EN/ES языковые занятия и EN/ES презентации проектов описаны прямо. Язык всех технических инструкций не установлен; English webpage не означает EN robotics.',
        '12 sessions в неделю распределены на четыре afternoon: remote water vehicle, sensors, stop motion и robot challenges. Количество sessions не равно 12 часам без длительности. Технический партнёр Crea tu Mundo; его лидерство — заявление оператора, не независимый рейтинг.',
        'Programme озаглавлена summer2026; будущие 2027 смены и записи не опубликованы в прочитанных источниках.',
        fee(None,'Прайс и обязательные сборы 2027 неизвестны.', 'Размещение и питание описаны на общем camp/facilities сайте; технический комплект и полноту пакета согласовать.',
            'Трансферы, insurance, materials/take-home, full technical option и personal expenses требуют quote.', 'Аванс, refund и договор неизвестны.'),
        'Cabins по 2 комнаты × 4 ребёнка, AC/bathrooms по facilities; five meals и farm/nature. Day формат не доказан.',
        fit('unknown','Возраст и night minimum не опубликованы в прочитанном источнике.'),fit('unknown','Возраст и night minimum не опубликованы в прочитанном источнике.'),
        'Предметный boarding robotics кандидат для семейного запроса: содержание известно, семейный допуск и смета ещё нет.',
        ['Получить возраст day/boarding, техчасов/инструктора EN или ES, dates2027 и all-in quote; подтвердить робототехнический объём после трёх лет опыта.'],
        [src('12 sessions и презентации EN/ES',cr),src('Facilities и общая жизнь','https://www.costablancacamp.com/en/'),src('General Spanish/English camp','https://www.costablancacamp.com/en/spanish-and-english-summer-camp-in-elche-alicante/')],priority=['technical'],confirmed=['EN','ES'])
    p['language_evidence_role']='language_lessons'

    lo='https://www.logiscool.com/en-es/programs/lego-wedo-future'
    p=put('logiscool-spain-wedo','Logiscool Spain · LEGO WeDo Future','Испания','ESP','Конкретная испанская branch не выбрана','robotics,coding,science','day','6–9; classroom, no prerequisites',
        'EN/ES преподавания конкретной branch ещё не установлен: английская страница и Испания в URL не доказывают язык занятия.',
        'Начальный LEGO WeDo курс: motors/sensors, задачи окружающей среды. Tools предоставляются, предварительная подготовка не нужна. После трёх лет robotics этот beginner уровень может быть недостаточно сложным.',
        'Будущая branch, точные camp dates2027 и текущий набор не найдены на общей programme странице.',
        fee(None,'Цена branch/смены неизвестна.', 'Инструменты обучения по programme page.', 'Жильё семьи, питание/присмотр вне занятий и возможные branch fees отдельно.', 'Branch-specific отмена и аванс неизвестны.'),
        'Classroom day programme; пансион не доказан.',fit('conditional','Только до 10-летия; подобрать уровень выше вводного.'),fit('conditional','С 6 лет по programme; выбрать живой camp branch и подходящий опытный уровень.'),
        'Локальная младшая техническая ступень, полезная для поиска branch; не подтверждённый top international residential camp.',
        ['Проверить branch, язык, реальную смену, стоимость и достаточную сложность.'],[src('Official Spain WeDo Future 6–9',lo)],priority=['technical'])

    lc='https://www.lacunza.es/en/camps/lacunza-camp'; lb='https://lacunza.com/wp-content/uploads/2025/11/Catalogo_Lacunza_EN_26.pdf'
    p=put('lacunza-general','Lacunza · International General Camp','Испания','ESP','San Sebastián · 2027 residence подтвердить; Olarain только brochure2026','general,languages,sport,art','day,boarding','6–13; minimum residential отдельно согласовать',
        'International bilingual camp; EN или ES language classes подтверждены. Язык всех activities и отдельный EN robotics не установлены.',
        'Morning 09:30–14:00, day 09:30–19:00 или full24h/weekends; языки, games/crafts, sports, arts и excursions. Robotics не найден. Brochure2026: 1,5 часа языка/день, residence Olarain; 2027 программу/кампус подтвердить.',
        'Страница публикует сезон 20 июня–8 августа 2027; отдельные недели не перечислены. Это окно выбора, не одна 50-дневная смена. Booking form всё ещё 2024: её цену не используем для2027.',
        fee(2026,'Архив PDF2026: EUR 195 morning / 455 day / 1 045 boarding за неделю. Отдельный актуальный прайс2027 пока не найден.',
            'По PDF2026: morning язык/crafts/snack; day afternoon; residence twin/private bathroom/full board.',
            'PDF2026 отдельно registration 60 и placement 50/person; morning lunch +115/week; surf90/week или135 для6–7. Применение placement к day и цены2027 подтвердить.',
            'Deposit250 и цифры old booking form2024 не переносятся на2027; нужен новый договор.'),
        'День с родительским жильём отдельно либо residential; возраст 6 из общей страницы не гарантирует каждый ночной пакет.',
        fit('candidate','9–10 соответствует6–13; формат/место подтвердить.'),fit('conditional','6–7 соответствует общей границе; residential minimum и самостоятельность отдельно.'),
        'Общий EN/ES international кандидат на совместную поездку: сезон2027 есть, но прайс и residence ещё архивные.',
        ['Получить актуальные недели/договор/прайс2027, EN/ES группу, residential minimum и all-in; старую форму2024 не заполняли.'],
        [src('Season2027, возраст, три формата',lc),src('Только архивный English catalogue2026',lb),src('Форма со старыми неделями2024','https://www.lacunza.es/en/camps/camp-enrolment')],status='partial_2027',priority=['general','both'],confirmed=['EN','ES'],sessions=[['2027-06-20','2027-08-08']])
    p['language_evidence_role']='language_lessons'

    cb='https://www.cervantes.to/barcelona/summer_programs.html'; ct='https://www.cervantes.to/barcelona/terms_and_conditions.html'
    for slug,name,formats,starts,prices,housing,osc in [
        ('cervantes-beach-board','Cervantes EI · Barcelona Beach Boarding Offer','boarding',['2027-07-04','2027-07-11','2027-07-18','2027-07-25','2027-08-01','2027-08-08'],
         'EUR 1 395 / 1 неделя; 2 495 / 2, 3 895 / 3, 4 895 / 4; extra week1 395.',
         'Residential university residence в Castelldefels, Sunday–Saturday, operator24h supervision. Конкретный camp operator/campus identity ещё не установлен.',fit('conditional','Общее описание5–15 включает6–7; отдельно подтвердить младший ночной поток и самостоятельность.')),
        ('cervantes-beach-day','Cervantes EI · Barcelona Beach Day Offer','day',['2027-07-05','2027-07-12','2027-07-19','2027-07-26','2027-08-02','2027-08-09'],
         'EUR 600 / 1 неделя; 1 200 / 2, 1 800 / 3, 2 400 / 4; extra week600.',
         'Monday–Friday09:00–20:00 с обедом. Родители живут и едут отдельно; campus residence не означает размещение семьи.',fit('candidate','6–7 входит5–15; уровень/группа и места отдельно.'))]:
        board=formats=='boarding'
        p=put(slug,name,'Испания','ESP','Castelldefels / Barcelona · Beach campus identity требует подтверждения','general,languages,sport,art',formats,
            'Beach5–15; City Center14–18 — отдельный лагерь, сюда не переносится',
            '20 EN/ES language lessons/week и English help для Spanish beginners. Это не 20 часов и не обещание EN всех activities; отдельный робототехнический курс не описан.',
            'Общий международный language/culture camp, sports, excursions. Optional sports не обязательны; можно один, при низком наборе возможна замена. Таблица Soccer16sessions/2weeks расходится с FAQ3times/week: объём уточнить.',
            'Шесть опубликованных стартов июля/августа2027; отдельные недельные окончания рассчитаны по правилу Sunday–Saturday либо Monday–Friday. Нельзя автоматически растягивать последний старт на4недели.',
            fee(2027,prices+' Enrollment35 сверх тарифа; недельный минимум '+('1 430' if board else '635')+' до выбранных опций.',
                'Языковые classes, materials, sports/activities; '+('accommodation/meals/excursions/supervision.' if board else 'lunch; weekend не обычный day пакет.'),
                'Airport95/person/oneway, bus250/2weeks bus stops, extra night95, weekend day100. Sports/2weeks: water350, tennis290, soccer290; минимальный набор и часы отдельно.',
                'Общие intermediary terms:250 credited advance, balance за2недели; это ещё не camp-specific contract. Не суммируем аванс как extra, отмену выбранного лагеря подтвердить.'),
            housing,fit('candidate','9–10 входит Beach5–15; точный поток и место отдельно.'),osc,
            'Конкретное опубликованное предложение канала бронирования; не новый независимый оператор. Может совпадать с известным Enforex campus, но точная связь не доказана и автоматически не объединяется.',
            ['Подтвердить юридического camp operator/campus, иностранный младший допуск, актуальный camp contract, availability и full invoice; language lessons не равны technical camp.'],
            [src('Beach offer2027: age, starts, prices и optional fees',cb),src('Generic booking-channel terms; camp договор отдельно',ct)],status='published_2027',priority=['general','both'],confirmed=['EN','ES'])
        p['language_evidence_role']='language_lessons'
        p['booking_channel']='Cervantes EI';p['operator_identity_status']='unconfirmed';p['possible_same_operator_as']='enforex-barcelona'
        rows=[]
        for s in starts:
            e=(datetime.date.fromisoformat(s)+datetime.timedelta(days=6 if board else 4)).isoformat()
            rows.append((s,e,'Beach · 1 неделя · '+('пансион' if board else 'день'),'EUR '+('1 395 +35' if board else '600 +35')+' enrollment; опции отдельно'))
        dated(p,rows,cb,scope='camp_session' if board else 'day_camp_window',rule='Источник публикует старты2027 и пакет1week. '+('Residential Sunday–Saturday: конец=старт+6дней.' if board else 'Day Monday–Friday: конец=старт+4дня, выходные не включены.'))

    au='https://ausiasmarch.com/cursos-de-verano-2026/'
    p=put('ausias-summer','Ausiàs March · English, Robotics & Sports','Испания','ESP','Picassent / Valencia · Colegio Ausiàs March','robotics,languages,sport','day','6–12',
        'Есть отдельные English/Spanish/robotics/PE teachers и языковые активности EN/ES; язык именно robotics instructor не установлен. EN/ES modules не доказывают английскую технику.',
        'Дневной курс с English, robotics, swimming и sports,09:15–16:00. Технологии/часов robotics и готовый проект не раскрыты подробно; уровень опытных детей уточнить.',
        'Только архив22июня–17июля2026. Даты и прайс нового2027 ещё не объявлены, будущие смены не создаются.',
        fee(2026,'EUR270/2недели либо505/месяц. Обед НЕ включён:107/2нед или159/месяц.',
            'Обучение, pool и materials по странице2026.',
            'Valencia bus116/2нед или172/месяц; Picassent55/82. Архив2нед+обед=377, сValencia bus493; месяц+обед664, сValencia bus836. Жильё/дорога семьи отдельно.',
            '2027 договор, аванс и отмена неизвестны.'),
        'Дневной школьный лагерь, ночёвок не доказано.',fit('conditional','Возраст2027 9–10 подходит6–12; новый набор/уровень подтвердить.'),fit('conditional','Возраст2027 6–7 подходит6–12; новый набор и младший уровень подтвердить.'),
        'Предметный локальный ES/EN кандидат обоим с прозрачной архивной разницей course/lunch/bus; бренд не доказывает международный рейтинг.',
        ['Получить2027 календарь, техчасов/оборудование, язык robotics и full course/lunch/bus quote.'],[src('Archive2026: возраст, timetable, отдельно lunch/bus',au)],priority=['technical','both'],confirmed=['EN','ES'])
    p['language_evidence_role']='language_lessons'

    ch='https://www.campamentodeajedrez.com/'; rt='https://www.campamentodeajedrez.com/summer-tech-camp-robotics-and-video-games/'; r4='https://robotic4kids.com/camparobotica/'
    p=put('madrid-chess-robotics','Blanco y Negro / Robotic4Kids · Madrid Tech Day','Испания','ESP','Madrid · Ciudad Universitaria; venues2026 не гарантируют2027','robotics,coding,general,sport','day','5–16 по Tech Camp; группируют по возрасту и предыдущим знаниям',
        'EN описание для visiting international families существует, но EN/ES преподавания прямо не доказан. Язык actual robotics group и bilingual support подтвердить.',
        'Robotics10:00–12:15 или wider camp07:30–17:00 с chess/pool/спортом. KitsLEGO, micro:bit/Maqueen и другие; старшим Godot/Python/GDevelop. Робототехника идёт одновременно с chess/comic/crafts: нельзя обещать всё сразу. Группы адаптируют по навыкам.',
        'Главная страница даёт сезон21июня–30июля2027, но просит ждать обновления до февраля2027. Адреса/ценовое меню всё ещё2026. Flexible days — сезонное окно, не непрерывная шестинедельная смена.',
        fee(None,'Точный2027 price для нужной дневной длительности пока неизвестен.', 'Робототехническое занятие/общий день по выбранному пакету; lunch и early/late coverage отдельно подтвердить.',
            'Жильё, дорога семьи, питание и возможные extended hours; прайс2026 не переносим.', '2027 registration/refund неизвестны.'),
        'Urban day camp; university residences как площадки не доказывают лагерь с ночёвками.',fit('conditional','9–10 по возрасту подходит; уровень, язык и новый набор2027 отдельно.'),fit('conditional','6–7 по возрасту подходит; начальный курс может быть слишком прост после трёх лет robotics.'),
        'Дневной технический кандидат с отдельным часовым блоком и настройкой по опыту; международная доступность описана, язык ещё неизвестен.',
        ['После февраля2027 сверить venues/dates/prices; подтвердить EN/ES technical language, часы, оборудование и индивидуальный уровень.'],
        [src('2027 season, обновлениеFeb2027 и архивvenues',ch),src('Age5–16 и robotics course',rt),src('Actual robotics hours и параллельные activities',r4)],status='partial_2027',priority=['technical','both'],sessions=[['2027-06-21','2027-07-30']])

def correct_garenne(profiles):
    pdf='https://www.la-garenne.ch/summer/repository/summer-conditions.pdf'
    form='https://www.la-garenne.ch/summer-camps/apply-online/'
    ps={p['slug']:p for p in profiles}
    for slug in ['la-garenne','garenne-robotics-workshop']:
        p=ps[slug]
        for title,url in [('Именно Summer2027 PDF: dates/fees/extras/contract',pdf),('Public2027 form: robotics8–12, CHF500 и3sessions',form)]:
            if url not in [s['url'] for s in p['sources']]:p['sources'].append(dict(title=title,url=url,checked='2026-10-05'))
        p['checked']='2026-10-05'
    p=ps['la-garenne']
    p['language']='Утренние EN/FR language lessons подтверждены2027 PDF; язык технического workshop и всех лагерных активностей отдельно неизвестен.'
    p['confirmed_instruction_languages']=['EN','FR'];p['language_evidence_role']='language_lessons'
    p['programme']='Общий язык/спорт/творчество/поездки. Актуальные form и summer conditions2027: Robotics8–12, три занятия заCHF500; меню всё ещё10–12, старый workshop PDF финал2sessions. Уточнить допуск8–9, часы и технический язык. Оскару6–7 доступен только общий лагерь. Это короткая опция, не двухнедельный инженерный интенсив.'
    p['timing']['label']='2027: пять boarding и пять day вариантов,2или4недели. Даты из summer conditions2027; weekday режим day включает субботу первой недели, поэтому не маркируется как обычныйПн–Пт.'
    p['price']=dict(year=2027,label='5–12: 2 недели CHF 7 200 пансион / 6 550 день; 4 недели 13 400 / 12 400. Старшие 13–16: 7 550 / 6 975 и 13 700 / 12 750 — отдельная группа.',
        included='Пансион: жильё, питание, прачечная; день: обед/snack. EN/FR уроки, activities/expeditions, transport для мероприятий, school materials, loan uniform 5–12, taxes/VAT. Детский Geneva transfer входит только в boarding в official dates/times.',
        extras='Robotics 8–12 CHF 500 / 3 занятия. Swiss medical insurance 10/day добавляется в invoice; form обязательна для non-Swiss residents, количество оплачиваемых day/student дней подтвердить. Pocket money 5–9: 30/week, 10–12: 50/week; добавляется в invoice. Off-slot Geneva 600, Zurich 900, UM 130, private language 130/week (min 2 = 260). Жильё семьи и перелёты отдельно.',
        deposit='Fees включают невозвратный CHF 500, это не extra. Место подтверждается только полной оплатой. Отмена ≥65 дней: возврат minus 500; позже без возврата. PDF deadlines: 23 апреля Session 1A/1B, 7 мая 2A/2B, 21 мая 3; для day применение deadline сверить. Extras ≤28 дней невозвратны. Sibling discount 10% второму при одной смене и одинаковом day или board; смешивать форматы братьев не разрешается. Изменение invoice CHF 25.')
    p['accommodation']='5–12 boarding: chalet rooms 4–6. Day 08:50–18:00, Пн–Сб первой / Пн–Пт второй недели; для 4 недель цикл подтвердить. Утренний путь родителями, вечером free village shuttle, нет campus pickup. Родительское посещение по appointment; жильё и трансферы взрослых не организуются.'
    p['questions']=['Подтвердить технический язык/часы, допуск 8–9 при menu 10–12, единицы дневной страховки, pocket money/скидку братьям, day Saturday schedule и итоговый счёт 2027.']
    boards=[('2027-06-27','2027-07-10','Session1A',2),('2027-07-11','2027-07-24','Session2A',2),('2027-07-25','2027-08-07','Session3',2),('2027-06-27','2027-07-24','Session1B',4),('2027-07-11','2027-08-07','Session2B',4)]
    days=[('2027-06-28','2027-07-09','Session1A',2),('2027-07-12','2027-07-23','Session2A',2),('2027-07-26','2027-08-06','Session3',2),('2027-06-28','2027-07-23','Session1B',4),('2027-07-12','2027-08-06','Session2B',4)]
    variants=[]
    for fmt,rows in [('boarding',boards),('day',days)]:
        for s,e,l,n in rows:
            variants.append(dict(start=s,end=e,label=l+' · '+str(n)+' недели · '+('пансион' if fmt=='boarding' else 'день'),
                formats=[fmt],price='CHF '+({2:'7 200',4:'13 400'}[n] if fmt=='boarding' else {2:'6 550',4:'12 400'}[n])+' базовая5–12; опции/insurance/pocketmoney отдельно',
                place=p['place'],source=pdf,date_scope='camp_session',proof='Точная строка SummerCamp2027 PDF5–12; day schedule не обычныйПн–Пт.',
                accommodation='Пансион 5–12, комнаты 4–6.' if fmt=='boarding' else 'Day 08:50–18:00; Пн–Сб первой / Пн–Пт второй недели; 4-недельный цикл подтвердить, родители живут отдельно.'))
    p['timing']['sessions']=[[v['start'],v['end']] for v in variants];p['timing']['session_details']=variants
    r=ps['garenne-robotics-workshop']
    r['age']='Form и summer conditions 2027: 8–12; menu Extras 10–12 остаётся противоречием. Для 8–9 нужно явное подтверждение оператора.'
    r['programme']='Опциональный Robotics & 3D design: VEX IQ, sensors/motors, командные задачи, Fusion360/Tinkercad и 3D printing. Актуальный summer conditions 2027 и форма: 3 занятия CHF 500. Старый workshop PDF заканчивается 2 sessions; расписание, техчасы и EN ещё уточнить. DIY Bluetooth speaker описан в PDF, состав пакета 2027 подтвердить; completion certificate не международная победа.'
    r['timing']['label']='Форма и summer conditions относятся к 2027. Отдельные даты короткого robotics workshop не опубликованы; даты общего лагеря не считаются техническими сменами.'
    r['editorial_reason']='Предметное знакомство Матвея с VEX и 3D design: опубликована опция CHF 500 / 3 занятия. Технические часы, EN, допуск 8–9 и полный пакет ещё уточняются.'
    r['price']=dict(year=2027,label='Robotics & 3D Printing CHF 500 / 3 sessions по форме и договору 2027; это опция сверх общей смены.',
        included='Три workshop занятия; точный equipment/materials/take-home пакет нужно уточнить.',extras='Базовая смена, insurance 10/day, pocket money, flights/optional transfer отдельно. Неизвестные единицы страховки и обязательные статьи оставляют all-in неполным.',deposit='Summer 2027: невозвратный credited CHF 500 внутри общего тарифа; full payment для места, основная отмена 65 дней, extras 28 дней. Условия опции и отмену технического блока подтвердить.')
    r['questions']=['Подтвердить 8–9 при menu 10–12, 3 занятия/часы, EN/ES инструктора, оборудование/материалы, наличие опции на конкретной смене и полный invoice 2027.']
    # Improve only human prose added/corrected here. Never touch IDs, dates or URLs.
    import re
    def prose(s):
        s=re.sub(r'(?<=[А-Яа-яЁё])(?=\d)|(?<=\d)(?=[А-Яа-яЁё])', ' ', s)
        s=re.sub(r'\b(CHF|PDF|Summer|summer|Winter|winter|Session|Extras)(?=\d)',r'\1 ',s)
        s=re.sub(r'\b(Beach|Center|Enrollment|Airport|bus|night|day|week|weeks|sessions|hours|camp|campus|catalogue|brochure|form|insurance|laundry|Soccer|Soccer|English|French|minimum|February|Feb)(?=\d)',r'\1 ',s)
        s=re.sub(r'(?<=[А-Яа-яЁё])(?=[A-Za-z])|(?<=[A-Za-z])(?=[А-Яа-яЁё])', ' ', s)
        return s
    for p in profiles:
        if int(p['id'][2:])>=163 or p['slug'] in ['la-garenne','garenne-robotics-workshop']:
            for k in ['age','language','programme','accommodation','editorial_reason']:p[k]=prose(p[k])
            p['timing']['label']=prose(p['timing']['label'])
            p['questions']=[prose(t) for t in p['questions']]
            for k,v in p['price'].items():
                if isinstance(v,str):p['price'][k]=prose(v)
            for f in p['family_fit'].values():f['detail']=prose(f['detail'])
            for v in p['timing'].get('session_details',[]):
                for k in ['label','price','proof','accommodation']:
                    if k in v:v[k]=prose(v[k])
