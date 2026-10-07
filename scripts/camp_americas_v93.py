"""Own Americas seasonal programmes, itemised fees and unresolved curricula."""
from datetime import date, timedelta
from camp_americas_v90 import clean_profile

CHECKED = '2026-10-05'
TAM = 'https://learnspanishsummercamp.com/'
COY = 'https://www.campcoyote.mx/'
CUBE = 'https://cubestemcamps.ca/stemcamps/wintercamp2026'
ICC = 'https://www.ultracamp.com/Info/'
CIB = 'https://www.ciberbots.com.mx/services'

def add_americas_v93(add, src, fit, P):
    first = len(P)
    def fee(year, label, included, extras, terms):
        return dict(year=year, label=label, included=included, extras=extras, deposit=terms)
    def variants(p, rows):
        p['timing'].update(sessions=[[r['start'],r['end']] for r in rows], session_details=rows, variant_keyed=True)
    def row(a,z,key,label,price,url,place,**kw):
        return dict(start=a,end=z,variant_key=key,label=label,price=price,source=url,place=place,**kw)
    unknown = 'Язык EN/ES/RU конкретных занятий и сопровождения не установлен. Язык сайта или перевод интерфейса не доказывает язык преподавания.'
    both = fit('conditional','В 2027 возраст входит в опубликованный диапазон; уровень группы, иностранный приём, язык и действующее место ещё подтвердить.')
    tamplace = 'Tamarindo, Guanacaste; shuttle: Ali’s Treehouse Preschool'
    add('tamarindo-elementary','Explornatura · Learn Spanish Summer Camp Elementary','Коста-Рика','CRI',tamplace,'general,languages,sport,art','day','Elementary 5–10; соседние Pre-K и Middle School — отдельные группы',
        'Подтверждены 10 часов уроков испанского в неделю. Bilingual staff и отдельный преподаватель EN/ES упомянуты, но язык всего дня, английская поддержка конкретной группы и технические занятия на EN не подтверждены.',
        'Дневная языковая программа: 10 ч испанского в неделю, группы по возрасту/уровню, творчество, готовка, пляж и природа; один урок серфинга с доской и одна поездка в неделю. Для уже говорящих по-испански детей проверить advanced/native-speaker задачи: это отдых и языковая практика, робототехника и AI не заявлены. Elementary 10 ч, а не 16 ч соседней старшей группы.',
        'Девять явно перечисленных понедельников 2027: 14/21/28 июня, 5/12/19/26 июля, 2/9 августа. Дневной лагерь Пн–Пт 08–14; окончания по пятницам рассчитаны по этому правилу. Скрытые старые недели 2026 не перенесены.',
        fee(2027,'На текущей странице $797/ребёнок/неделя; двоим $1 594 за лагерь. Валюту, налоги и итоговый счёт подтвердить. Жильё на отдельной странице: 1-bedroom $155/ночь, Studio $170, 2-bedroom $205; минимум 6 ночей. Условный пример двое детей + 6 ночей 1-bedroom: $2 524 до неустановленных сборов и при одинаковой валюте.',
            '10 ч испанского, перечисленные занятия, один surf lesson с доской, weekly field trip, дневной перекус и обед. Не 24/7 пансион для Elementary.',
            'Жильё семьи, перелёт, airport transfer, extra surf/уроки/няня и родительские курсы отдельно. Shuttle pickup 07:40/drop14:00, стоимость не указана. Жильё 1-bedroom/Studio до 4 человек; 2-bedroom до 5. Скидки жилья 14+ ночей 15%, 28+ 30%, доступность и год тарифа подтвердить.',
            'Связанные terms действуют для набора Nov2025–сезон2026, поэтому не выданы за контракт2027. В них $100 — 50% невозвратного registration fee, а не доказанный полный сбор; 50% оплаты, остаток за8недель, cancellation200/student и разные возвраты. Текущий hold100/credit25 не принят за полный тариф или гарантированную скидку. Нужны terms2027 и финальная регистрационная сумма.'),
        'Дневной лагерь; родители живут отдельно. Жильё сайта: собственная кухня/кровати, минимум6ночей; номер kitchenette максимум2 человека не семейная комната на4. Заявления ratio5:1 и surf1:2 — сведения оператора, не независимая проверка. Under6 car seat rule не применяется автоматически к лету2027 Оскара6–7.',both,both,
        'Близкий к дому общий вариант обоим с реальными датами2027; полезность языковой части зависит от уровня их испанского.',
        ['Подтвердить advanced/native Spanish группу, поддержку EN, места, полный счёт в указанной валюте, жильё/транспорт и контракт2027.'],
        [src('Текущий Kids programme2027',TAM+'kids-summer-camp-ws'),src('Terms с явной применимостью2026',TAM+'terms623610-258659'),src('Жильё и ночные тарифы',TAM+'beachfront-lodging-options'),src('Именованные преподаватели',TAM+'our-staff'),src('Дополнительные услуги',TAM+'services')],status='published_2027',priority=['both','general','local'],confirmed=['ES'])
    P[-1]['language_evidence_role']='language_lessons'
    starts=['2027-06-14','2027-06-21','2027-06-28','2027-07-05','2027-07-12','2027-07-19','2027-07-26','2027-08-02','2027-08-09']
    variants(P[-1],[row(a,(date.fromisoformat(a)+timedelta(days=4)).isoformat(),'week-'+str(i),'Elementary · Пн–Пт 08–14','$797/неделя; валюту, registration и налоги уточнить',TAM+'kids-summer-camp-ws',tamplace,date_precision='published_rule',date_rule='Сайт явно перечисляет девять Monday starts2027 и правило Monday through Friday08–14; окончание каждой недели рассчитано как понедельник+4дня.') for i,a in enumerate(starts,1)])

    coyplace = 'Km15 Carr. Zapotlanejo–Tototlán, Zapotlanejo, Jalisco'
    coyhouse = 'Пансион в домиках glamping: заезд11:00 первого дня / выезд15:00 последнего; раздельные зоны по полу. Описание обещает4–6детей с вожатым, таблица3–4: вместимость расходится. Постель включена, но список вещей просит одеяло/спальник/подушку: уточнить комплект. Пять приёмов пищи включая2перекуса; аллергии сообщают заранее. Парамедик и сопровождение круглосуточно, больница в12минутах — заявления оператора. Телефон около1ч/день под контролем.'
    coyextra = 'Проезд/перелёт, страховку, полный состав оплаченных активностей и трансфер уточнить. Школьные private groups minimum15/возраст5–18/тариф1100+ — другой продукт. Публичные индивидуальные лагеря начинаются с6, не5.'
    coyterms = 'Аванс30% невозвратный, остаток наличными при заезде. Отмена/перенос до7дней: оплаченный сверх аванса остаток ваучером6месяцев на услуги группы, не cash refund. Медицинская справка позволяет перенос до1года. Скидки не суммируются; отдельный окончательный договор, иностранный приём и места не подтверждены.'
    coysrc=[src('Собственные сезоны, динамический прайс и раскрытый FAQ',COY)]
    coyquestion=['Подтвердить точный DOB/язык, готовность к ночёвкам, места, комнату/постель, транспорт, страховку и полный договор/счёт; сумма аванса входит в тариф.']
    fit2026m=fit('conditional','В2026 возраст8–9 входит в6–14; язык, места и ночёвки согласовать.')
    fit2026o=fit('conditional','Только после6-летия: в2026 будет5–6. Нужен точный DOB и согласование ночёвок/языка.')
    add('coyote-short','Camp Coyote · осенний и зимний короткий пансион','Мексика','MEX',coyplace,'general,sport,art','boarding','6–14; индивидуальный лагерь',unknown,
        'Autumn: природа, лошади, препятствия, костёр и квест. Winter: стрельба из лука, велосипед, лошади, творчество и готовка. Разные возрастные ротации; конкретные водные/высотные активности подтвердить. Общая программа, без заявленной робототехники.',
        '30Oct–2Nov2026:4дня3ночи; 21–23Dec2026:3дня2ночи. Собственная страница пишет cupos abiertos, это не подтверждение зачисления.',
        fee(2026,'Autumn MXN4 000/ребёнок, аванс1 200; двое братьев7 200 за семью. Winter3 300, early2 805 до20Nov; двое5 940, early двоим5 610 если применим. Winter аванс990/ребёнок. Выбирается одна скидка; earlydeadline не срок регистрации.', 'Glamping, еда и описанный отдых; состав окончательного пакета подтвердить.',coyextra,coyterms),coyhouse,fit2026m,fit2026o,
        'Короткий общий пансион рядом с Guadalajara; кандидат обоим после6-летия Оскара.',coyquestion,coysrc+[src('Read-only Autumn form',COY+'inscripcionescamp?program=oto%C3%B1o'),src('Read-only Winter form',COY+'inscripcionescamp?program=invierno')],status='published_2026',priority=['general','boarding','local'])
    variants(P[-1],[row('2026-10-30','2026-11-02','autumn','Autumn · 4дня3ночи','MXN4 000/ребёнок; двое7 200; аванс1 200 входит в цену',COY,coyplace),row('2026-12-21','2026-12-23','winter','Winter · 3дня2ночи','MXN3 300/ребёнок; early2 805 до20Nov; двое5 940 без early; аванс990',COY,coyplace)])
    add('coyote-junior','Camp Coyote · Pascua / Verano Basic','Мексика','MEX',coyplace,'general,sport,art','boarding','6–14; оба сезона6дней5ночей',unknown,
        'Pascua: игры, Easter crafts, лошади/костёр. Basic: первая ночёвка, младшие группы, lake games, препятствия и квесты. Это общий outdoor, без курса AI/робототехники.',
        'Pascua:29марта–3апреля2027 в календаре оператора. В других блоках остаются ожидание дат и пометка REF.2026: цену и открытие набора подтвердить. Basic: август2027, точных дней нет.',
        fee(None,'В текущем прайсе MXN6 500, ранний тариф5 525; Pascua двое11 700/аванс1 950 на ребёнка. На сайте встречается и5 300, а карточка Pascua сохраняет REF.2026: нужен письменный тариф2027. Для Summer скидки братьям/аванс в таблице не указаны.', 'Glamping, питание и общие активности; полный пакет подтвердить.',coyextra,coyterms),coyhouse,both,both,
        'Более длинный общий пансион обоим; отдельный вариант первой поездки, пока с листом ожидания и конфликтом тарифа.',coyquestion,coysrc,status='partial_2027',priority=['general','boarding'])
    P[-1]['availability']=dict(status='waitlist',label='На собственной странице лист ожидания; места и финальный тариф2027 не подтверждены',checked=CHECKED)
    variants(P[-1],[row('2027-03-29','2027-04-03','pascua','Pascua · 6дней5ночей','MXN6 500 / ранний5 525, но REF.2026; финальный тариф2027 неизвестен',COY,coyplace,availability=P[-1]['availability'],proof='Точная дата из собственной видимой карточки. Другие блоки ещё ждут расписания, аREF.2026/лист ожидания сохраняются; набор не объявлен открытым.')])
    add('coyote-pro','Camp Coyote · Verano Pro','Мексика','MEX',coyplace,'general,sport','boarding','9–17; 8дней7ночей',unknown,
        'Более сложные outdoor и физические командные задачи, zipline/препятствия, возрастные ротации и вечерние игры. Pro относится к приключениям; это не инженерная квалификация.',
        'Июль2027 без точных дней, лист ожидания.',fee(2027,'Текущий прайс MXN8 500, ранний7 225 без опубликованного срока; на сайте встречается и7 100. Это предварительная цена. Скидка братьям и аванс в таблице не указаны.', 'Glamping, питание и приключения; точный состав пакета подтвердить.',coyextra,coyterms),coyhouse,
        fit('conditional','В2027 будет9–10: числовой gate9+ выполняется; язык/физические активности/места ещё согласовать.'),fit('later','В2027 будет6–7, минимум9.'),
        'Отдельный старший общий трек Матвею; точное летнее расписание и договор ещё нужны.',coyquestion,coysrc,status='partial_2027',priority=['general','boarding'])
    P[-1]['availability']=dict(status='waitlist',label='Summer Pro: собственный лист ожидания, точные дни ещё не опубликованы',checked=CHECKED)

    grade=fit('unknown','Camp FAQ требует enteringGrade2 asofSeptember2026. Фактический класс неизвестен; birthyear не заменяет школьный gate. Исключение MarchBreak2026 не распространяется автоматически на Winter.')
    add('cube-winter-makers','Cube STEM · Holiday Makers & Coders','Канада','CAN','Beaches Presbyterian Church,65GlenManorDrive,Toronto','coding,engineering,science,games','day','Минимум enteringGrade2 asofSeptember2026; верхняя campграница не указана',unknown,
        '21–23Dec: зимний Scratch-platformer,3Ddesign/печать, slimechemistry с баночками, Minecraft и прогулки. Beginners; индивидуальная advancedcodingprogramme не предлагается, возможны расширения после общего урока. Отдельный VEX/AI intensive здесь не обещан.',
        '21–23December2026,3дня09–15:30. Адрес Winterpage: Beaches; footerJuly2026Wesley не перенесён как адрес зимней смены.',
        fee(2026,'CAD255+HST за3дня; пакет с обедом/перекусами275+HST. Extendedcare112.50+HST за3утра+3вечера: вместе с mealpackage387.50+HST/ребёнок, двоим775+HST до других нераскрытых сборов. HSTставка/финальныйсчёт не вычислялись.',
            'Занятия и учебные coding/roboticsmaterials. Mealpackage275 включает еду3дней. Учебная техника не обещана в подарок.',
            'Morning08–09:12.50+HST/day; PM15:30–17:25+HST/day. Отдельный mealadd-on42+HST не повторно к mealpackage275; Wednesdaypizza10+HST отдельно. Жильё/проезд семьи отдельно; без еды взять обед/2nutfreesnacks. Свои устройства запрещены, USB optional для сохранения проекта.',
            'Более20дней до начала: fullrefund минус CAD65processing; до10дней50% минус65; внутри9днейnone. Точные граничные10/20дни подтвердить. Нет возврата за пропущенные дни, перенос по наличию. Campне обеспечивает индивидуальную1:1behaviouralsupport; это описание услуги, не оценка детей.'),
        'Дневной лагерь без пансиона; взрослые доставляют/забирают. Campus зимней programme:65GlenManorDrive; другиеcampusWesley/Scarborough в общем footer не выбраны.',grade,grade,
        'Конкретная зимняя смена с прозрачными tuition/food/care; польза детям с опытом соревнований зависит от уровня группы.',
        ['Подтвердить реальный школьный класс, Winteragegate, EN преподавания, внешние места, степень сложности, адрес и полный счёт+HST.'],[src('OwnWinter2026 programme,fee,FAQ',CUBE)],status='published_2026',sessions=[['2026-12-21','2026-12-23']])

    iccplace='ICC Table Tennis Center,1507N.MilpitasBlvd,Milpitas,California95035'
    iccterms='Own RefundPolicy и FAQ открылись пустыми: политика отмены не установлена. Membershipdiscount10 требует активного членства на всю смену, sibling10 при брате в ту же неделю/центр; stacking и применение к обоим не установлены. Регистрация заканчивается10:00 первого дня, хотя camp начинается09:30: время/часовойпояс/приём в первый день уточнить. Никакие accounts/formsubmission/payment не выполнялись.'
    programmes=[
        ('drone','Drone Dynamics & Missions','engineering,coding',[(1,'2027-05-31','2027-06-04','592283'),(6,'2027-07-05','2027-07-09','592451'),(11,'2027-08-09','2027-08-13','592471')]),
        ('engineering','Engineering & Robotics','robotics,engineering',[(2,'2027-06-07','2027-06-11','592284'),(7,'2027-07-12','2027-07-16','592458')]),
        ('vex','VEX Exploration','robotics,coding',[(3,'2027-06-14','2027-06-18','592285'),(8,'2027-07-19','2027-07-23','592462')]),
        ('ai','AI Discovery','ai,coding',[(4,'2027-06-21','2027-06-25','592286'),(9,'2027-07-26','2027-07-30','592469')]),
        ('raspberry','Circuits with Raspberry Pi','engineering,coding',[(5,'2027-06-28','2027-07-02','592287'),(10,'2027-08-02','2027-08-06','592470')])]
    for slug,title,themes,cohorts in programmes:
        def url(n,i):
            return ICC+('sessionDetail.aspx?campCode=&idCamp=80&idSession='+i if n<=5 else 'sessionDetail.aspx?idCamp=80&idSession='+i+'&campCode=')
        sources=[src('Собственный списокICC2027',ICC+'upcomingsessions.aspx?campcode=&idCamp=80&lang=en-Us')]+[src('OwncourseY'+str(n),url(n,i)) for n,a,z,i in cohorts]+[src('Ownrefundpage: без условий', 'https://www.ultracamp.com/refundpolicy.aspx?campcode=&idCamp=80&lang=en-Us'),src('OwnFAQ: без ответов',ICC+'faqs.aspx?campcode=&idCamp=80&lang=en-Us')]
        add('icc-young-'+slug,'ICC Young Innovators · '+title,'США','USA',iccplace,themes,'day','5–14; объединённый диапазон, возрастные уровни не расписаны',unknown,
            'Название собственной карточки: '+title+'. Общее расписание09:30–15 обещает3ч YoungInnovators +1.5ч tabletennis/chess/art, местамиTaekwondo. Но подробный syllabus содержит Bollydance, а category — Bollywooddance. Реальные AI/VEX/drone/RaspberryPi проекты, роботонаборы, технические часы и возрастные уровни НЕ подтверждены из противоречивого текста. Не представлено как гарантированное15ч robotics или topcamp.',
            'Конкретные летние недели2027 перечислены ниже, всего11cohorts у одного оператора по5заявленным темам. Формы прочитаны только для публичных деталей. Ownavailability пишет openings, действующее место и допуск семьи не подтверждены.',
            fee(2027,'На американской карточке $429/неделя nonmember /419 member. Доплаты lunch70 +beforecare60 +aftercare99: полный выбранный набор $658/ребёнок/неделя или $1 316 двоим до неизвестных налогов/fee/скидок; валюта финального счёта подтвердить.',
                'Описанный дневной programme; фактическую техническую часть, equipment и материалы подтвердить из-за неверного dancebody. Устройства не обещаны в подарок.',
                'Вегетарианский обед70/week; утреннийcare08–09:30 60; aftercare15–18 99; после18:05 1/minlate. Жильё/проезд семьи отдельно. Указанные UIEnglish/Spanish/French/Korean не языки преподавателя.',iccterms),
            'Дневной Milpitascentre без пансиона. Возрастная группа, supervisionratio и оборудование конкретной темы пока не раскрыты.',both,both,
            'Календарный кандидат с детальным прайсом и серьёзным конфликтом syllabus; до его разрешения не рекомендован как проверенный технический интенсив.',
            ['Получить актуальный syllabus именно'+title+', язык и возрастные уровни, действующее место для иностранных детей, refundterms и полный семейный счёт; не считать danceописание технической программой.'],sources,status='published_2027')
        variants(P[-1],[row(a,z,'y'+str(n),'Y'+str(n)+' · '+title+' ·09:30–15','$429nonmember/419member; выбранные доплаты70+60+99',url(n,i),iccplace,deadline=a,proof='Даты/цена/5–14/registrationdeadline из собственной карточки. Тема подтверждена названием, подробное содержание конфликтует сBollywoodbody. Deadline10AMпервого дня против09:30начала требует уточнения.',availability=dict(status='open',label='Собственная карточка на дату проверки: openings; без гарантии места',checked=CHECKED)) for n,a,z,i in cohorts])

    c=next(p for p in P if p['slug']=='ciberbots')
    c.update(checked=CHECKED,age='Числовой campagegate не указан; регулярные уровни школы4–6/7–8/9–11/11+ не автоматически holidayintake',
        programme='Ownservices: Summer Próximo2027 —4недели механики/роботов LEGO Mindstorms,WeDo,Boost,SpikePrime/Essentials,Arduino; Pascua Próximo2027 —1неделяNXT/EV3 с тематикой яиц; Christmas Diciembre2026 —1неделя рождественских моделей/кодирования. Точный возраст, дневные часы, цена и проект каждой группы не раскрыты. Регулярные дошкольные4–6/Beginner7–8/CBRS9–11/Intermediate11+ — отдельные courses. Конкурсы доступны школьной программе по собственному примечанию, не автоматически лагерю.',
        editorial_reason='Локальная робототехника с объявленными будущими сезонами; реальный допуск обоих и уровень holidayгруппы пока неизвестны.',
        questions=['Подтвердить Christmas2026/Summer/Easter2027 exactdates, camp-specificage, язык/ENsupport, часы, роботонаборы/пары, полный тариф/отмену и путь в собственную соревновательную команду.'])
    c['timing'].update(status='partial_2026_27',label='Christmas December2026, Summer/Easter Próximo2027. Точных дней нет, календарные события не созданы.')
    for k in ['matvey','oscar']:c['family_fit'][k]=dict(status='unknown',detail='Школьный возраст сам по себе не доказывает holidaygate; конкретные campвозраст/группа/язык требуют подтверждения.')
    c['sources'].append(dict(title='Собственные будущие holidayprogrammes и отдельные школьные уровни',url=CIB,checked=CHECKED))
    for p in P[first:]:
        p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        clean_profile(p)
    clean_profile(c)

def extend_report_v93(report):
    report['shortlist'].extend([
        dict(label='Коста-Рика · лето2027 обоим',slugs=['tamarindo-elementary','cloud-forest'],reason='Tamarindo5–10 даёт9летних недель,10часов испанского/неделя,surf/поездки и отдельное жильё. Детям уже со Spanish нужен подходящий уровень. CloudForest — ранее проверенная отдельная семейная programme; цена/приём не объединены.'),
        dict(label='Мексика · короткий или длинный общий пансион',slugs=['coyote-short','coyote-junior','coyote-pro','makemake'],reason='Coyote6–14 для младших,Pro9–17 только Матвею; Short2026 только после6-летия Оскара. Basic/Pro без точных летних дней; Pascua имеет динамическую дату и ценовой конфликт. Makemake EN подтверждён ранее, но Grade2+ ограничивает младшего.'),
        dict(label='США / Канада · зимние варианты с проверкой уровня',slugs=['cube-winter-makers','star-anibots','star-robot-gaming'],reason='Cube21–23Dec с итогом tuition/meal/care доHST; требует actualGrade2asofSep2026 и beginners. StarKids — ранее записанные отдельные roboticsсмены с собственными gradegates и shortenedlastday. Birthyear не даёт автоматический класс.')])
    report['gaps'].extend([
        dict(country='Коста-Рика',iso='CRI',provider='v93 · Tamarindo: разные годы договора; Harmony и Oaktree',detail='Tamarindo текущие2027weeks подтверждены видимой страницей, hidden2026weeks не использованы; terms прямо заканчиваются сезоном2026. Lodging $155/170/205,6nightminimum отдельно, без доказанногоall-inquote. Harmonydirect403/cached2025, но реально отображённая собственная страница даётJuly5–16,2027 без цены/возраста/формата/языка: не допущен как проверенный дневной/пансион. OaktreePDFCalendar2026визуально:Christmas7–11/14–18Dec2026, Summerstart4Jan2027;1Febschoolstartнеcampend. Servicesпресchool, campage/внешнийприём/EN/цена не подтверждены, новое досье не создано.',next_action='Текущие campcontracts/язык/места/actualage и семейная смета; не подставлять regularschoolage/hours или архив2025fees. ДругиеCRoperators/2027 продолжают проверяться.',url=TAM+'kids-summer-camp-ws'),
        dict(country='Мексика',iso='MEX',provider='v93 · Coyote динамические данные / Ciberbots будущие сезоны',detail='Coyote initialHTML7100/5300/EasterTBD противrender8500/6500/29Mar–3Apr2027; уPascua осталосьREF2026/waitlist. Summerexactdaysunknown.3новых досье одного оператора, не3компании. Short4000/3300, winterearly2805until20Nov неregistrationdeadline.2siblings7200/5940,скидки не складываются;cancel30%retained/excessvoucher6mo. Room4–6versus3–4 иpackingconflict сохранены. Ciberbots ChristmasDec2026/Summer/Easter2027 объявлены без дней/цен/holidayage; regularcoursesage неcampintake, FITобоихunknown.',next_action='ТочныеDOB/ENorESteaching/места/currentseasoncontract исемейныйall-inquote; другиеMexicooperators не завершены.',url=COY),
        dict(country='США / Канада',iso='USA',provider='v93 · ICC curriculum конфликт и Cube gradegate',detail='ICC11летних карточек2027 прочитаны:5тем oneoperator,5–14,429/419,70lunch+60AM+99PM. Ownheadingtech противBollydancebody/category; technicalsyllabus невыдуман. English/Spanishportal неEN/ESteaching. Emptyrefund/FAQнеno-refundpromise. Deadline10AMfirstday против09:30campstart. CubeWinter21–23Dec2026,255/275+112.50+HST; separate42meal не доплата к275package. Grade2asofSep2026, March2026exception неWintergate. Beginnersможет быть недостаточно трёхлетнему competitionexperience.',next_action='Точныйsyllabus/язык/fullinvoice/actualgrade, потом оценка пользы и места; ICC пока не familytoptechnicalshortlist.',url=ICC+'upcomingsessions.aspx?campcode=&idCamp=80&lang=en-Us'),
        dict(country='Бразилия / Аргентина / США',iso='BRA',provider='v93 · NR контракт без базового прайса; недоступные страницы',detail='NR current/ferias HTTP200пустая оболочка и видимыйheader/footer: cachedKidsJan dates/ages не подтверждены. Legacyhomologacao selfsignedcertificate не обходился. Own2027contractPDF: DobraR$8617.50/9048.50/9257 только дополнительная2-я неделя после заезда, неinitialcampfee. Insuranceaccident10k/dental300 иforeignpassport неadmission. Refundcredit/cashretention20/50/75%,noshow100%; неfullcontractaudit. RobotikiCampURL404, SnapRoundRock403; без новых дат/цен из cachedsnippet.',next_action='Текущие прямые programmes с реальными2027days/basefee/age/language/intake; Brazil/LatAm и globalcountrycoverage остаются активной целью.',url='https://nr.com.br/ferias')])
    for q in report['shortlist'][-3:]:
        for k in ['label','reason']:
            from camp_americas_v90 import readable
            q[k]=readable(q[k])
    for q in report['gaps'][-4:]:
        for k in ['provider','detail','next_action']:q[k]=readable(q[k])
