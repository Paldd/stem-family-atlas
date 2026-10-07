"""Deep European programme review: dated courses, boarding gates and archival fees."""
import json
from pathlib import Path

def add_deep_europe(add,src,fit,profiles):
    checked='2026-10-05'
    def put(*args,**kwargs):
        add(*args,**kwargs);p=profiles[-1];p['checked']=checked
        for s in p['sources']:s['checked']=checked
        return p
    def price(year,label,included,extras,deposit):return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def variants(p,rows,keyed=False):
        p['timing']['session_details']=rows;p['timing']['sessions']=[[r['start'],r['end']] for r in rows]
        if keyed:p['timing']['variant_keyed']=True
    day='Дневной лагерь; семейное жильё и сопровождение вне лагеря.'
    ts='https://techsparkacademy.ch/in-person-camps/'
    tt='https://techsparkacademy.ch/terms-conditions/'
    tr='https://online.techsparkacademy.ch/robotics-course/'
    campus=json.loads((Path(__file__).resolve().parents[1]/'data/techspark-sessions-v63.json').read_text())
    tech_sources=[src('Английский преподавания, оборудование и питание',ts),src('Правила именно In-Person Programs',tt)]+[src('Смены и конкретные курсы: '+r['label'].split(' · ')[0],r['source']) for r in campus if r['start'] in ['2026-10-12','2026-10-19','2026-10-06','2027-04-19']]
    payment='In-Person: отмена до 14 дней даёт voucher за вычетом 3.5%, не гарантированный денежный возврат; ближе 14 дней отмена недоступна. При отмене оператором — возврат или voucher. Проверить применяемую редакцию договора.'
    common='Английский — основной язык технического преподавания; EN/FR или EN/DE помощь. Достаточное понимание английских инструкций обязательно.'
    p=put('techspark-games','TechSpark · Animation & Game Design Junior','Швейцария','CHE','Pully / Petit-Lancy / Zürich / Zug',
        'coding','day','В меню 7–10; в датированных сменах 7+. Верхний предел выбранной группы уточнить.',common,
        'Scratch: анимации, интерактивные истории и игры. Задачи адаптируют по уровню, обычно 3–6 участников в группе; финальный показ родителям. Это программирование, отдельный LEGO-курс не входит автоматически.',
        '25 точных смен осени 2026 и весны/лета/осени 2027 в четырёх городах. 22 уже были в календаре; досье связывает их по конкретной площадке.',
        price(2027,'Junior: CHF 645 / 3 дня; 790 / 4 дня; 890 / 5 дней. Цена конкретной площадки показана в смене.',
            'Занятия, ПО, присмотр, перекусы; обед включён в Pully и Petit-Lancy.','В Zürich/Zug — ланч с собой. Ноутбуки доступны на большинстве junior-площадок по выбору при записи; возможную плату подтвердить.',payment),
        day,fit('candidate','В 2027 будет 9–10; подходит меню 7–10. Подтвердить верхнюю границу группы.'),fit('conditional','Только после 7-летия к первому дню; в 2026 ещё младше 7.'),
        'Технический маршрут на английском с конкретными датами, адресами и ценами; удобнее общего пансиона для ежедневного программирования.',
        ['Подтвердить места, верхний возраст, ноутбук и итог выбранной площадки; питание отличается по городам.'],tech_sources,status='published_2026_27',priority=['technical'],confirmed=['EN'])
    rows=[]
    for c in campus:
        r={k:v for k,v in c.items() if k not in ['python_offered','python_closed','lunch_included']}
        r.update(age=p['age'],programme=p['programme'],proof='Animation & Game Design прямо указан в Junior Course Info данной смены; время '+c['hours']+'; '+('обед включён.' if c['lunch_included'] else 'ланч с собой.'))
        if c['start']<'2027-01-01':r['family_fit']=dict(matvey=p['family_fit']['matvey'],oscar=dict(status='later',detail='В 2026 ещё младше минимальных 7.'))
        rows.append(r)
    variants(p,rows,True)
    p=put('techspark-python','TechSpark · Code in Python Junior','Швейцария','CHE','Pully / Petit-Lancy / Zürich / Zug',
        'coding','day','Junior 10+; точный верхний предел выбранного курса уточнить',common,
        'Текстовое программирование Python: индивидуальные проекты с задачами по уровню, исходная проверка готовности. Не путать с подростковыми Beginner/Advanced или AI/Startup 13+.',
        '24 датированных предложения 2026–2027. В Zürich 11–14 октября 2027 Junior Python не указан: эту смену сюда не переносим. 6–9 октября 2026 junior Python sold out.',
        price(2027,'Junior: CHF 645 / 3 дня; 790 / 4; 890 / 5. Цены именно junior, без подростковых тарифов.',
            'Занятия, ПО, присмотр, перекусы; Pully/Petit-Lancy также обед.','Ланч Zürich/Zug, доступность/аренда junior-ноутбука и семейная поездка отдельно.',payment),
        day,fit('conditional','В 2027 только после 10-летия; в сменах 2026 ещё не подходит.'),fit('later','Минимум 10; в 2027 будет 6–7.'),
        'Следующая ступень Матвея от Scratch к текстовому коду; публичное расписание позволяет планировать год.',
        ['Проверить 10-летие к первому дню, готовность к Python, ноутбук и места.'],tech_sources,status='published_2026_27',priority=['technical'],confirmed=['EN'])
    rows=[]
    for c in campus:
        if not c['python_offered']:continue
        r={k:v for k,v in c.items() if k not in ['python_offered','python_closed','legacy_event_ids','lunch_included']}
        r.update(age=p['age'],programme=p['programme'],proof='Python Junior прямо указан в Junior Course Info этой площадки и смены; '+c['hours']+'.')
        if c['start']<'2027-01-01':r['family_fit']=dict(matvey=dict(status='later',detail='Рождён в 2017; в 2026 ещё не достигает 10.'),oscar=p['family_fit']['oscar'])
        if c['python_closed']:r['availability']=dict(status='closed',label='Junior Python sold out')
        rows.append(r)
    variants(p,rows,True)
    put('techspark-lego','TechSpark · Robotics with LEGO Junior','Швейцария','CHE','Площадку конкретного LEGO-заезда согласовать',
        'robotics,coding','day','6+ в описании LEGO Junior; Arduino — отдельный курс 12+',common,
        'LEGO SPIKE: двигатели, сборка, программирование и ежедневные задачи. Страница курса подтверждает 6+ и отсутствие требований к опыту; общий календарь городов не доказывает наличие LEGO в каждой смене.',
        'Даты лагерей показаны как learning options, но в прочитанных датированных меню Junior перечислены Scratch/Python, а не LEGO. Подтверждённой смены именно LEGO 2027 пока нет.',
        price(None,'Итог именно LEGO неизвестен. Общие junior-тарифы CHF 645–890 не считаем подтверждённой LEGO-ценой.',
            'Свои устройства для Junior LEGO не требуются.','Питание, набор, итоговая цена и площадка согласовать. CHF 100 hardware surcharge относится к Arduino, не к LEGO.',payment),
        day,fit('conditional','Возраст подходит; ещё нужен реально доступный LEGO-заезд.'),fit('conditional','После 6-летия по опубликованному порогу; смена ещё не доказана.'),
        'Возрастной робототехнический кандидат для обоих; не создаём фиктивные LEGO-смены из общего расписания.',
        ['Подтвердить LEGO, даты, площадку, EN-преподавание конкретной группы и стоимость.'],[src('LEGO 6+ / Arduino 12+, оборудование',tr),src('Язык дневных курсов',ts),src('In-Person cancellation',tt)],priority=['technical','both'],confirmed=['EN'])

    lb='https://www.lyceum-alpinum.ch/en/summer-camps/boarding-camp/'
    lj='https://www.lyceum-alpinum.ch/en/summer-camps/junior-day-camp/'
    lp='https://www.lyceum-alpinum.ch/wp-content/uploads/2026/09/Flyer-International-Summer-Camp-2027.pdf'
    ld='https://www.lyceum-alpinum.ch/wp-content/uploads/2026/09/Factsheet-Digital-Skills.pdf'
    p=put('lyceum-board','Lyceum Alpinum Zuoz · Digital Skills Boarding','Швейцария','CHE','Zuoz · Lyceum Alpinum',
        'robotics,coding,ai,entrepreneurship,sport','boarding','10–17; допуск конкретного цифрового курса согласовать',
        'Digital Skills 2027 прямо taught in English; инструкторы EN/FR. Языковой курс EN/FR/DE — альтернатива утреннему Digital Skills.',
        '9 утренних занятий по 3.25 часа, выбор одного из четырёх треков: AI & Innovation/Lean Startup, Python games, Arduino robotics, cybersecurity. Свой ноутбук, зарядка и адаптер; предпочтительно RAM 8GB+. Короткая оценка уровня; все уровни допустимы. После обеда спорт, футбол, кино или гольф.',
        '4–16 и 18–30 июля 2027; можно оба лагеря с промежуточными выходными. Регистрация объявлена на октябрь.',
        price(2027,'CHF 6 200 / один лагерь; CHF 12 800 / оба. Страница отдельно называет CHF 400 за промежуточные выходные: полный итог четырёх недель подтвердить.',
            '29 часов курса, пансион, питание, присмотр 24/7, материалы, прачечная, активности и групповой Zurich Airport transfer.','Перелёт, медицинская/accident/liability страховка семьи; гольф-набор CHF 450/лагерь. Собственный ноутбук. Не прибавляем CHF 400 автоматически поверх 12 800 без расчёта.',
            'Отмена до 30 дней без затрат; 29–15 дней — 50%; ближе 15 дней — без возврата. Связанная cancellation insurance PDF 2026 не считается договором 2027.'),
        'Пансион в single/double комнатах; два лагеря соединяются с присмотром Fri–Sun.',fit('conditional','Только если к приезду уже 10; готовность к курсу и допуск проверить.'),fit('later','Минимум 10; в 2027 будет 6–7. Есть отдельный дневной Junior.'),
        'Сильный кандидат Матвею после 10-летия: доказан английский именно цифрового преподавания и объём занятий.',
        ['Подтвердить возраст и выбранный модуль, hardware fee Arduino, окончательный итог двух лагерей и transfer slots.'],[src('2027: даты, цены, включения и правила',lb),src('Брошюра лагеря 2027',lp),src('Digital Skills 2027: EN, часы и техника',ld)],status='published_2027',priority=['technical','boarding'],confirmed=['EN'])
    variants(p,[dict(start=s,end=e,label=lab,price=fee,place=p['place'],source=lb,formats=['boarding']) for s,e,lab,fee in [('2027-07-04','2027-07-16','Camp 1 · Digital Skills по выбору','CHF 6 200'),('2027-07-18','2027-07-30','Camp 2 · Digital Skills по выбору','CHF 6 200'),('2027-07-04','2027-07-30','Оба лагеря · промежуточные выходные','CHF 12 800; статус CHF 400 уточнить')]])
    p=put('lyceum-junior','Lyceum Alpinum Zuoz · Junior Day Camp','Швейцария','CHE','Zuoz · Lyceum Alpinum',
        'general,languages,sport','day','6–9',
        'Английский или немецкий: уроки и общение на выбранном языке в обед/активностях, прямо описано на странице.',
        '16 языковых lessons в неделю, утром 08:30–11:45; после обеда природа, спорт, творчество, экскурсии. Присмотр до 16:00. Это общий языковой лагерь: Digital Skills/Arduino старшего пансиона сюда не входят.',
        '5–9 / 12–16 / 19–23 / 26–30 июля 2027, понедельник–пятница; можно 1–2 недели.',
        price(2027,'CHF 1 000 / неделя.',
            'Материалы, обед, занятия и активности. Страница включает pick-up, но также предлагает with/without: выбранную комплектацию подтвердить.','Жильё семьи, страховка, дорога; маршрут pick-up до St. Moritz / Madulain.',
            'До 30 дней отмена без затрат; 29–15 дней — возврат 50%; ближе 15 дней без возврата.'),
        day,fit('conditional','Только пока ещё 9; после 10-летия этот Junior недоступен.'),fit('candidate','В 2027 возраст 6–7 подходит; выбрать английскую группу.'),
        'Практичный общий английский вариант Оскару рядом с возможным техническим пансионом старшего.',
        ['Сверить даты рождения обоих и маршрут/включение автобуса; это дневной общий лагерь.'],[src('Программа, возраст, тариф и условия',lj),src('Одностраничный Junior flyer 2027','https://www.lyceum-alpinum.ch/wp-content/uploads/2026/09/Flyer-Junior-Day-Camp-2027.pdf')],status='published_2027',priority=['general','both'],confirmed=['EN'])
    variants(p,[dict(start=s,end=e,label='Junior · английский по выбору',price='CHF 1 000',place=p['place'],source=lj,formats=['day'],date_scope='day_camp_window') for s,e in [('2027-07-05','2027-07-09'),('2027-07-12','2027-07-16'),('2027-07-19','2027-07-23'),('2027-07-26','2027-07-30')]])
    ch='https://www.nordangliaeducation.com/champittet/camps/summer-leadership-camp'
    p=put('champittet-leadership','Collège Champittet · Summer Leadership Camp','Швейцария','CHE','Pully · Collège Champittet',
        'general,entrepreneurship,sport','day,boarding','Junior 11–13; Senior 14–17',
        'Английский — язык лагеря и leadership workshops; достаточно базового everyday English.',
        'Коммуникация, команда, принятие решений, уверенность и outdoors. Партнёрские IMD/EHL/IOC-сессии разделены по Junior/Senior: участие 11-летнего во всех старших IMD workshops не обещается. TechSpark на этом кампусе — другая программа.',
        '5–18 июля и 19 июля–1 августа 2027; двухнедельный дневной или residential пакет.',
        price(2027,'CHF 6 900 / residential 2 недели; CHF 3 950 / day 2 недели.',
            'Residential-пансион и программа; Geneva transfer в дни смен: прилёт 08–18, вылет 09–20.','Перелёт и трансферы в другое время/дату отдельно; точный day-пакет и страхование подтвердить.',
            'CHF 1 000 первоначальный взнос невозвратный. Отмена за 60+ дней — fee 50%, 59 и меньше — без возврата; зачёт первого взноса в санкцию уточнить.'),
        'Школьный пансион или дневной пакет; возраст 11+ относится к обоим.',fit('later','В 2027 будет 9–10; минимум 11.'),fit('later','В 2027 будет 6–7; минимум 11.'),
        'Будущая международная ступень лидерства; не подходящий сейчас младший robotics-пансион.',
        ['Уточнить содержание Junior, итог пакета и договор отмены 2027.'],[src('2027: возрастные группы, EN, цены, FAQ',ch)],status='published_2027',priority=['boarding'],confirmed=['EN'])
    variants(p,[dict(start=s,end=e,label='Leadership · Junior/Senior',price='CHF 6 900 boarding / 3 950 day',place=p['place'],source=ch,formats=['day','boarding']) for s,e in [('2027-07-05','2027-07-18'),('2027-07-19','2027-08-01')]])
    sc='https://www.saint-charles.ch/summer-camp'
    put('saintcharles-camp','Saint-Charles · Language & Adventure Camp','Швейцария','CHE','Porrentruy · Route de Belfort 10',
        'general,languages,science,sport','boarding','Старая страница 2026: 10–15. Новая страница не устанавливает возраст сезона 2027.',
        'EN/FR языковые уроки подтверждены; английский STEM и лагерной жизни отдельно не доказан.',
        'Языки утром, STEM/творчество/спорт после обеда, поездки, швейцарские ремесленные workshops. STEM — опция общей программы; не объявлен полный робототехнический интенсив.',
        'Текущая страница не даёт дат нового сезона. Старый 27 июня–25 июля 2026 уже завершён; не переносим его в 2027.',
        price(None,'На новой странице без года: CHF 3 900 / 1 нед.; 6 900 / 2; 9 900 / 3; 11 900 / 4. Не подтверждённый прайс 2027.',
            'Питание, языковые материалы, основные активности, housekeeping/laundry, health insurance, welcome pack.','Airport transfers, Big Sundays, watch/knife workshops отдельно. Прежние Basel CHF 400 / Zurich 600 — только старый 2026 источник.',
            'Старый 2026 аванс CHF 1 000 в течение 15 дней, balance May 30. Новый договор/возвраты пока не известны.'),
        'Пансион; family concierge не включает проживание родителей.',fit('unknown','Прежний минимум 10; для 2027 возраст ещё подтвердить.'),fit('later','Прежняя основная группа с 10; младший не подходит, новый возраст неизвестен.'),
        'Дополнительный швейцарский общий пансион с подробным составом; новая страница сохраняет цены, но не сезон/возраст.',
        ['Подтвердить новый сезон, возраст, EN жизни/тематики и полный тариф с трансфером.'],[src('Новая официальная программа',sc),src('Архив 2026 и прежний возраст','https://www.saint-charles.ch/en/Summer-Camp/Summer-Camp.html')])

    rd='https://www.ecoledesroches.com/en/summer-camp/'
    rp='https://www.ecoledesroches.com/wp-content/uploads/2026/04/SummerCamp2026Brochure-EDR.pdf'
    put('roches-ai','École des Roches / JMA · AI Boarding Camp','Франция','FRA','Verneuil-sur-Avre · École des Roches',
        'robotics,coding,ai','boarding','11–14 и 15–17; общий French Classic 9+ — другой курс',
        'Именно AI Camp прямо English; French Classic и Elite Sports не переносятся в EN-технический фильтр.',
        '2026: первый модуль robotics/AI с AlphAI/mBot/LEGO SPIKE для 11–14; второй — CyberLab. Для 15–17 Python/ML и perceptron. Можно один или оба модуля; общий шестинедельный спорт-пакет не доступен как шестинедельный AI.',
        'Архив 2026: учебные модули 28 июня–11 июля и 12–25 июля; boarding-таблица заканчивает их 12/26 июля. 2027 ещё не объявлен.',
        price(2026,'EUR 4 850 / 2 недели; 8 550 / оба модуля (4 недели). Не тариф 2027.',
            'Уроки, пансион/питание, активности, 2 экскурсии в неделю, standard CDG transfers, присмотр.','Возвратный security deposit EUR 300 отдельно; медицинские расходы/нестандартный transfer могут удерживаться из него; перелёт отдельно.',
            'EUR 2 000 аванс в счёт цены, balance 1 May 2026. До 1 June 2026 возврат минус 500; после — нет. На 2027 не переносить.'),
        'Shared boarding rooms, supervision 24/7.',fit('later','В 2027 будет 9–10; AI минимум 11.'),fit('later','Минимум 11; ещё будущая ступень.'),
        'Проверенный английский тематический пансион для будущего возраста; техническое содержание сильнее общей рекламной метки STEM.',
        ['Дождаться сезона 2027, возрастного допуска и нового прайса; проверить реальные дни проживания.'],[src('Содержание и AI возраст',rd),src('2026 brochure: программы, тарифы и условия',rp),src('Партнёр Jeannine Manuel Academy','https://www.jmacademy.org/ai-tech-camp-at-ecole-des-roches')])
    jm='https://www.jmacademy.org/summer-camps'
    for slug,title,age,programme,mat,osc in [
        ('jm-juniors','Juniors','5–7','Творчество, театр, музыка и спорт; группы до 12. Научно-робототехнический Scientists сюда не входит.',fit('not_eligible','Старше максимума 7.'),fit('candidate','В 2027 будет 6–7; младшая группа подходит.')),
        ('jm-campers','Campers','8–9 на текущем сайте оператора; школьная страница ещё пишет 7–9','Fun Science & Makers Lab, искусство, спорт, музыка/театр; ротация занятий, финальный показ. Не робототехнический Scientists.',fit('conditional','Только пока ещё 9; после 10 лет перейти в Scientists.'),fit('later','В 2027 ещё младше текущего минимума 8.')),
        ('jm-scientists','Scientists','10–12','Coding & Robotics, Makers Lab, Fun Science, спорт и музыка; Science Fair и итоговый показ.',fit('conditional','После 10-летия к смене; младше 10 выбрать Campers.'),fit('later','Минимум 10; в 2027 ещё 6–7.'))]:
        put(slug,'Jeannine Manuel Academy Paris · '+title,'Франция','FRA','Paris · 115 avenue Émile Zola, 75015',
            'robotics,coding,science' if slug=='jm-scientists' else 'general,science' if slug=='jm-campers' else 'general','day',age,
            'Все занятия и общение с командой проводятся на английском; все уровни, без языкового теста.',
            programme+' Дневной распорядок: двери 08:30, занятия 09–17; без дневного сна.',
            'Оператор анонсирует открытие Summer Camp 2027 applications в мае 2027; точные даты/прайс ещё отсутствуют. Список недель и FAQ с 6/13 июля относится к 2026.',
            price(2026,'Архив: EUR 900 / 5 дней; 13–17 июля 2026 EUR 720 / 4 дня (14 июля выходной). 2027 не опубликован.',
                'Уроки/активности, обед и extracurricular insurance.','Перекус и вода с собой; жильё/дорога семьи отдельно.',
                'Архив 2026: до 1 July возврат с удержанием 20% deposit; после без возврата. Размер deposit и новый договор проверить.'),
            day,mat,osc,'Английский дневной вариант Парижа; младший общий трек и старший science/robotics разделены по реальному возрасту.',
            ['Уточнить даты 2027, возрастную группу и прайс. Оператор требует vaccination proof для детей из зарубежных школ; точный перечень и альтернативы согласовать, его формулировку не считаем проверкой законодательства.'],
            [src('Текущие возрастные треки, 2027 interest и архив 2026',jm),src('Школа: EN и допуск детей всех школ','https://ecolejeanninemanuel.org/summer-et-science-camp/')],status='partial_2027',priority=['technical'] if slug=='jm-scientists' else ['general'],confirmed=['EN'])
    sd='https://www.saint-denis.net/fr/article/english-summer-camps-44.html'
    put('saintdenis-kids','Saint Martin–Saint Denis · Kid’s English Camp','Франция','FRA','Loches · 19 avenue du Général de Gaulle',
        'general,languages','day','Maternelle–6ème; точный возраст и формат младшего нового заезда неизвестны',
        'Описана полная английская иммерсия; новый сезон не подтверждён.',
        'Игры, искусство и английский, прежние 1–2 недели. Painting Camp для 4ème–Terminale — другой старший курс; пансион его не переносим к Kid’s.',
        'На странице прямо: English Summer Camps летом 2026 НЕ проводились. 2027 не объявлен; это наблюдение за возможным возобновлением.',
        price(None,'Новый прайс неизвестен.','Состав пакета ещё не опубликован.','Жильё, питание и поездки пока не установлены.','Нового договора нет.'),
        'Формат Kid’s подтвердить; общий школьный internat не доказывает младший camp boarding.',fit('unknown','Школьная категория может подойти; нового набора нет.'),fit('unknown','Нужны класс, возраст и возобновлённая смена.'),
        'Закрывает пробел по французским школам; не предлагаем как подтверждённый работающий лагерь.',
        ['Проверить возобновление 2027, младшую категорию и условия.'],[src('Отмена 2026 и разделение Kid’s/Painting',sd),src('Внешние ученики и общий школьный формат','https://www.saint-denis.net/fr/categorie/cours-de-vacances-summer-camps-7.html')])

    life='https://lifeschool.es/life-tech-camp/'
    put('life-tech','LIFE International School · VEX EXP Tech Camp','Испания','ESP','Tres Cantos · LIFE International School',
        'robotics,coding','day','10–14',
        '100% English Immersion; полный robotics programme in English прямо указан, не только английские уроки.',
        'VEX EXP STEM Labs: сборка basebot, автоматизация, claw/cup challenges, maze и математические escape-room задачи. До 16 мест в неделю; четверг — бассейн/общие outdoor-активности.',
        'Три опубликованные недели июня/июля 2026 завершены. EN нижний блок пишет до 17 июля, ES до 10 июля: четвертую неделю не выводим. 2027 ещё неизвестен.',
        price(2026,'EUR 280 / неделя; прежняя скидка outsiders 15% до 1 June — архив.',
            'Робототехника EN, обед/перекус, бассейн.','Жильё и дорога семьи; своё оборудование и судьбу робота уточнить.','Публичные правила оплаты/возврата конкретного нового заезда неизвестны.'),
        day,fit('conditional','В 2027 только после 10-летия и при повторении курса.'),fit('later','Минимум 10; будущая ступень.'),
        'Испанская школа с явно английской именно VEX-практикой; outsiders прямо допускаются, но текущей будущей смены нет.',
        ['Подтвердить 2027, возраст на старте, даты, технику, отмену и наличие мест.'],[src('VEX EXP, EN, возраст и цена',life),src('Испанский источник: расхождение конечной даты','https://lifeschool.es/es/tech-summer-camp/')],priority=['technical'],confirmed=['EN'])
    sg='https://www.stgeorgebarcelona.com/en/news-events/summer-school-barcelona'
    sb='https://www.stgeorgebarcelona.com/IB%20-%20St%20George%20Barcelona/Download%20%26%20policies/SGB_SummerCamp2026_Brochure_v3.pdf'
    put('stgeorge-barcelona','St George Barcelona / Ignite · Robotics Summer School','Испания','ESP','Barcelona · Passeig de la Reina Elisenda de Montcada 18 bis',
        'robotics,coding','day','6–10; общий English Camp 3–10 — другой выбор',
        'Официальная страница прямо Robotics Summer Camp in English; общий брошюрный EN immersion не заменяет отдельное подтверждение robotics.',
        'Robotics, programming, 3D design, Minecraft coding и еженедельные новые задания с Ignite. Платформу/набор, часы реального robotics и ноутбук подтвердить.',
        '6–31 июля 2026 — архив. Страница без года раскрыта брошюрой 2026; 2027 пока не объявлен.',
        price(2026,'EUR 330 / 1 нед.; 645 / 2; 950 / 3; 1 240 / 4. Брошюра robotics имеет отдельную таблицу; 5-недельный общий пакет не переносим.',
            'Дневной лагерь 09–16, обед/перекусы указаны в общем пакете; robotics-комплектацию подтвердить.','Early service 08–09: EUR 15/день или 60/нед.; жильё/транспорт отдельно.',
            'EUR 200 registration fee вычитается из total, не добавляется второй раз; бронирование минимум за 2 недели. Отмену уточнить.'),
        day,fit('candidate','В 2027 будет 9–10; текущий возрастный диапазон подходит, при повторении.'),fit('conditional','С 6 лет к первому дню; новая смена ещё неизвестна.'),
        'Английская техническая программа обоим в одной школе; ясный архивный прайс без обещаний 2027.',
        ['Проверить 2027, платформу и оборудование, питание именно robotics, возвраты.'],[src('Робототехника EN и внешние ученики',sg),src('Полный brochure 2026: отдельный robotics прайс',sb),src('Robotics / Minecraft flyer 2026','https://www.stgeorgebarcelona.com/IB%20-%20St%20George%20Barcelona/Pdf/Robotics%20summer%20camp%202026.pdf')],priority=['technical','both'],confirmed=['EN'])
    cc='https://www.chestercollege.org/en/camps/chester-international-english-summer-camp/'
    put('chester-english','Chester College · International English Summer Camp','Испания','ESP','Teo / Santiago de Compostela · Travesía de Montouto 2',
        'general,languages,sport','day,boarding','8–18; Juniors 8–12, Teens 13+','English immersion: daily English, public speaking, music/drama with native specialist teachers.',
        'Общая английская программа, спектакли/musical, спорт и поездки; optional Trinity exams для full camp. Это не робототехническая смена. День 09:15–18:30, иногда позже; субботние trips.',
        'Анонсирован 2027, запись с 1 December 2026; точные даты пока обещаны shortly. Ссылки fees ведут в файлы 2026 — не 2027.',
        price(2026,'Архив fee PDFs: boarding EUR 2 225 / session, 3 865 / full; day 1 150 / session, 1 950 / full. Новый 2027 прайс не опубликован.',
            'Boarding: комнаты с dorm parents, полное питание, уроки/активности; day: обед/перекусы, материалы и trips.','Trinity exam fees отдельно; архив shuttle train EUR 30 и airport 60 one-way. Day bus 70/session, 140/full; early breakfast 50/session,100/full — сверить 2027.',
            'Архив registration EUR 750 в счёт цены. Текущая страница balance by 1 May 2027; отмена и новый аванс ещё неизвестны.'),
        'Day или boarding: separate boys/girls premises с dorm parents.',fit('candidate','В 2027 будет 9–10, junior подходит; точные даты неизвестны.'),fit('later','Минимум 8; в 2027 будет 6–7.'),
        'Общий международный английский пансион Испании для старшего; понятный резерв без подмены тематическим STEM.',
        ['Дождаться 2027 dates/fees и договора, уточнить transfer/экзамены.'],[src('2027, возраст, программа и регистрация',cc),src('Boarding fee flyer 2026','https://www.chestercollege.org/wp-content/uploads/2026/02/en-boarding-chester-english-summer-camp-2026.pdf'),src('Day fee flyer: ссылка 2026, год внутри не указан','https://www.chestercollege.org/wp-content/uploads/2026/02/en-day-chester-english-summer-camp-2026.pdf')],status='partial_2027',priority=['general','boarding'],confirmed=['EN'])
    ac='https://aikidsclub.org/en/ai-summer-camp-alicante'
    put('ai-alicante','AI Kids Club Alicante · Project & Demo Camp','Испания','ESP','Alicante · MiCampus 2026; площадка 2027 ещё не подтверждена',
        'ai,coding,entrepreneurship','day','2026 mixed group 8–12; FAQ также вспоминает 7-летних. 2027 возраст объявят вместе с датами.',
        '2026: English с Spanish support; язык преподавания 2027 оператор обещает подтвердить с расписанием.',
        'Собственный проект с AI-инструментами: от идеи и прототипа к демонстрации семье. Начинают с основ, нужны собственный ноутбук и проверка совместимости. Маркетинговое сравнение с robotics не считаем рейтингом качества.',
        'Summer 2027 прямо анонсирован; dates/price/venue/ages/timetable ещё не опубликованы.',
        price(2026,'EUR 250 / неделю в 2026 (20 часов); цена 2027 неизвестна.',
            'Обучение AI, материалы и Demo Day по описанию 2026.','Свой ноутбук, перекус/вода, жильё/дорога семьи. 09:30–13:30 без обеда в 2026; часы 2027 ещё не известны.',
            'Публичные условия аванса/отмены ещё не проверены.'),
        day,fit('conditional','Предыдущая 8–12 подходит; возраст/язык новой смены подтвердить.'),fit('unknown','Упоминание прежних 7-летних не устанавливает возраст 2027; нужен конкретный допуск.'),
        'Небольшой проектный AI-кандидат с семейным Demo Day; не доказанный лидер международного рынка.',
        ['Дождаться дат, прайса, возраста и EN/ES, адреса и правил инструментов/родительского согласия.'],[src('2027 анонс и честно отделённый архив 2026',ac)],status='partial_2027',priority=['technical'],confirmed=['EN'])
