"""Programme-specific Asian camp pass; preserve language, age and venue boundaries."""
CHECKED='2026-10-05'
U='https://u-gaku.jp/'
SEE='https://seecamp.com.tw/product/'
MYOKO='https://myokoenglishexplorers.com/wp-content/uploads/2026/03/2026-EE-Adventure-Culture-Camp-overview.pdf'
SRT='https://www.srt.com.sg/'
VOCA='https://vocaacademy.co/holcamp26/'
KISAS='https://kisas.co.kr/en'
EMB='https://embassy.camp/camp-in-korea/'
NTUE='https://clec.ntue.edu.tw/p/404-1018-57247.php?Lang=zh-tw'

def add_asia_v83(add,src,fit,profiles):
    def put(slug,name,iso,place,themes,formats,age,language,programme,dates,price,housing,mat,osc,why,questions,urls,
            status='next_unannounced',role=None,priority=None,sessions=None):
        add(slug,name,{'JPN':'Япония','PHL':'Филиппины','TWN':'Тайвань','SGP':'Сингапур','KOR':'Южная Корея'}[iso],
            iso,place,themes,formats,age,language,programme,dates,price,housing,mat,osc,why,questions,
            [src(t,u) for t,u in urls],status=status,confirmed=['EN'] if role else [],priority=priority,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        if role:p['language_evidence_role']=role
        return p
    def fee(year,label,included,extras,deposit):return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def detail(p,url,**kw):
        p['timing']['session_details']=[dict(start=a,end=b,label=kw.get('label','Смена'),source=url,
            place=p['place'],formats=p['formats'],price=p['price']['label'],date_scope=kw.get('date_scope','camp_session'),
            **{k:v for k,v in kw.items() if k not in ['label','date_scope']}) for a,b in p['timing']['sessions']]

    winter=[['2026-12-26','2026-12-30']];spring=[['2027-03-28','2027-04-03']]
    uterms='Initial contract fee JPY 30 000; повторным участникам не начисляется. Общая отмена: до 90 дней и в первые 5 дней заявки без сбора; позже — contract fee; ближе 90/60/45 дней 50/70/100%. Границы пересекаются: подтвердить договор. Refund guarantee только для программ 4+ недели, к этим коротким сменам не применяется.'
    uquestions=['Подтвердить приём иностранной семьи без японского языка, школьный класс Оскара, EN общения с родителями, итоговый счёт, комнату и передачу ребёнка.']
    uurls=[('Программа и даты',U+'english-camps/'),('Договор отмены',U+'company/cancel-policy'),
           ('Ограничение refund guarantee',U+'company/refund-policy'),('Правила несовершеннолетних',U+'company/minor-policy')]
    age='Начальная и средняя школа, возраст цифрами не опубликован; иностранный класс должен быть принят организатором.'
    mat=fit('conditional','2017: подтвердить школьный класс и внешний приём; возраст сам по себе не подтверждает допуск.')
    osc=fit('conditional','2020: только если уже соответствует принятому elementary grade; kindergarten не заявлен.')
    # Different seasons use different premises; give each its own location and price.
    choices=[
      ('ugaku-nasu-winter','U-GAKU · Nasu Winter','JPN','Nasu Grand Garden, 4453-190 Takaku-ko, Nasu, Tochigi',
       'english-camps/nasu/',winter,159800,'general,languages,adventure,art,science',
       'Английская жизнь, nature/craft, командное STEAM создание и обсуждения. Конкретный robotics/AI курс не заявлен.',
       'Nasu Grand Garden; место встречи сообщают после записи. Зимнее жильё не переносим на весну.'),
      ('ugaku-nasukashi-spring','U-GAKU · Nasukashi Spring','JPN','National Nasukashi Youth Nature House, Nishigo, Fukushima',
       'english-camps/nasu/',spring,199800,'general,languages,adventure,art,science',
       'English group work, orienteering, nature hunt, craft/STEAM team creation, BBQ; итоговая английская презентация.',
       'National Nasukashi Youth Nature House, Fukushima. Встреча и выдача JR Shin-Shirakawa 11:00; это другая площадка, чем зимний Nasu.'),
      ('ugaku-chatan-winter','U-GAKU · Okinawa / Chatan Winter','JPN','3-110 Miyagi, Chatan, Okinawa',
       'english-camps/okinawa/',winter,139800,'general,languages,adventure,sport',
       'English lessons и жизнь с преподавателями, местная культура и outdoor activities; точную зимнюю программу подтвердить.',
       'Зимний адрес Chatan 3-110; весенний Pension Three Peace в Onna сюда не переносим.'),
      ('ugaku-onna-spring','U-GAKU · Okinawa / Onna Spring','JPN','Pension Three Peace, Onna, Okinawa',
       'english-camps/okinawa/',spring,199800,'general,languages,adventure,science,business',
       'English lessons, создание своего магазина, OIST English campus tour, Churaumi Aquarium, Ryukyu Village, marine activities; итоговая презентация.',
       'Pension Three Peace, Onna, арендован целиком. Встреча/выдача после записи; не зимний Chatan.'),
      ('ugaku-wakayama-spring','U-GAKU · Wakayama Spring','JPN','Prefectural Shirasaki Youth House, Wakayama',
       'english-camps/kansai/',spring,199800,'general,languages,adventure,science,art',
       '22 часа English group work, береговая экология, наблюдение звёзд, hiking, роспись кружки, готовка/BBQ; итоговая презентация.',
       'Prefectural Shirasaki Youth House; максимум 10. Meeting/transfer после записи. /wakayama/ возвращает пустую страницу, действующая programme URL /kansai/.'),
      ('ugaku-cebu-winter','U-GAKU · Cebu Winter','PHL','U-GAKU Cebu, 28 Emilio Osmeña St, Cebu City',
       'english-camps/cebu/',winter,139800,'general,languages,adventure',
       'Английские занятия, жизнь с преподавателями и культурные/морские activities. Подробный зимний itinerary подтвердить.',
       'Собственная Cebu school/residence. Сайт включает airport–camp transfer; точку передачи и международный перелёт подтвердить.'),
      ('ugaku-cebu-spring','U-GAKU · Cebu Spring','PHL','U-GAKU Cebu, 28 Emilio Osmeña St, Cebu City',
       'english-camps/cebu/',spring,199800,'general,languages,adventure',
       '14 часов one-to-one English плюс группа, island hopping, рынок/English cooking, NGO visit, итоговая презентация. Максимум 10.',
       'Собственная Cebu residence; встреча/выдача Mactan–Cebu Airport и transfer включены. Точное распределение комнат/присмотр подтвердить.'),
    ]
    for slug,name,iso,place,path,pairs,amount,themes,programme,housing in choices:
        label=('26–30 декабря 2026, 4 ночи / 5 дней.' if pairs==winter else '28 марта – 3 апреля 2027, 6 ночей / 7 дней.')
        lang='English lessons и разговор с иностранными преподавателями, питание/активности вместе; Japanese staff support. Иностранный приём без JA не установлен.'
        if 'okinawa' in path:lang+=' Раздел Target пишет intermediate+, общий header только school age: подтвердить уровень.'
        includes='Жильё, питание, уроки/материалы, основные активности и stay support; первый/последний день питание по времени заезда.'
        extras='Перелёт/дорога, личные расходы, медицинские расходы; transfer/страховку проверить.'
        if iso=='PHL':extras='Перелёт и личные расходы; аэропорт–camp включён. Оператор упоминает UM/WEG: условия по паспорту и сопровождению нужно проверить отдельно.'
        p=put(slug,name,iso,place,themes,'boarding',age,lang,programme,label,
            fee(2026 if pairs==winter else 2027,f'JPY {amount:,} + initial contract 30 000 = {amount+30000:,} для нового участника, до дороги и других расходов.',includes,extras,uterms),
            housing,mat,osc,'Небольшой EN пансион с конкретными датами; оценка под семью условная, мировой рейтинг не установлен.',uquestions,
            [('Конкретная площадка/пакет',U+path)]+uurls,status='published_2026_27',role='camp_life',priority=['general','boarding'],sessions=pairs)
        p['accommodation']+=' Spring bonus до 31 Oct: same-room friends/siblings при room 2–4 и порядке записи; разнополые siblings отдельно. Это не подтверждённое место.' if pairs==spring else ''
        detail(p,U+path)

    put('myoko-adventure-culture','Myoko English Explorers · Adventure & Culture','JPN','Buna House / Myoko, Niigata · точный адрес заселения подтвердить',
        'general,adventure,languages,sport,art','boarding','6–15 по официальной brochure 2026.',
        'Все activities на English; требуется advanced–native, не просто возможность учиться на EN.',
        'Японская культура, indigo/food crafts, kayaking/SUP, hiking/orienteering, farm tour, team projects. Это общий adventure camp.',
        'Brochure 2026: 14–18, 21–25, 28 июня – 2 июля, 5–9 июля; прошедшие смены. Новые даты/прайс 2027 не опубликованы в прочитанном документе.',
        fee(2026,'JPY 130 000 / 4 ночи, 5 дней. 2027 тариф неизвестен.',
            'Жильё, питание, activities, страхование и перевозки внутри лагеря в пакете 2026.',
            'Tokyo round-trip bullet train +20 000; family/friends discount 10% заявлен без подробных условий. Перелёт отдельно.',
            'Актуальный договор/депозит/отмена 2027 неизвестны.'),
        'Buna House в примерном itinerary; meeting Tokyo Station или Joetsu-Myoko Station. Room/night-care 2027 подтвердить.',
        fit('conditional','Возраст подходит; проверить advanced EN и новый набор.'),fit('conditional','В 2027 будет 6–7; точный возраст на старте и advanced EN.'),
        'Интересный общий японский пансион для уже уверенно говорящих детей; документ 2026 не гарантирует смену 2027.',
        ['Новый датированный пакет, English assessment, возраст младшего, проживание, итог/отмена.'],
        [('Официальный PDF: возраст, English, 2026 dates/fee',MYOKO),('Организатор','https://myokoenglishexplorers.com/')],role='primary',priority=['both','general','boarding'])

    see_age='Kindergarten senior class – Primary Grade 4; Grade 5+ только отдельное согласование, не автоматический допуск.'
    see_fit=(fit('conditional','По году рождения вероятна Primary группа; текущий класс подтвердить.'),
             fit('conditional','Нужно соответствие senior kindergarten/Primary; год рождения 2020 не доказывает класс.'))
    for slug,name,path,pairs,places,programme,price in [
      ('see-discover-japan','S.E.E. · Discover Japan, Taiwan','2027see-winter-discover-japan-2d/',
       [['2027-01-21','2027-01-22']]*2,['National Taipei University of Business, Taipei','S.E.E. English Academy, Xindian'],
       'Japanese culture: sushi, ninja/samurai games, LEGO samurai, спорт и English CLIL; всё проходит в Тайване.',
       fee(2027,'NTD 5 600 tuition +1 100 take-home LEGO =6 700. До 11.10.2026 individual5 860; группа3+5 580,6+5 300.',
           'Материалы, take-home LEGO, lunch/snack.',
           'Поздний pickup18–18:30 +100,18:30–19 +200; семейное жильё/дорога отдельно.',
           'Скидка минимум3/6 не тариф семьи из двух. Оплата/отмена и наличие места требуют подтверждения.')),
      ('see-world-games','S.E.E. · World Games','2027see-winter-world-games-5d/',
       [['2027-01-25','2027-01-29']]*2,['National Taipei University of Business, Taipei','S.E.E. English Academy, Xindian'],
       'Игры, культура и кухня France/Greece/Canada/Australia; English CLIL и командный спорт в Тайване.',
       fee(2027,'NTD 13 800 /5 дней. До 11.10.2026 individual11 730; группа3+11 040,6+10 350.',
           'Материалы, lunch/snack.',
           'Поздний pickup18–18:30 +100,18:30–19 +200; семейное жильё/дорога отдельно.',
           'Скидка минимум3/6 не тариф семьи из двух. Договор отмены/наличие места подтвердить.')),
    ]:
        url=SEE+path
        p=put(slug,name,'TWN','Taipei / Xindian · отдельные площадки',
            'general,languages,art,sport','day',see_age,'Весь programme English, native+local teacher; Chinese assistance при необходимости. Не вывод из языка сайта.',
            programme,'21–22 января 2027.' if 'japan' in slug else '25–29 января 2027. Две параллельные площадки; выбирают одну.',price,
            'Дневной09–17, приём08–08:40, pickup17:10/17:40; до18 buffer бесплатно. Parents housing отдельно.',
            *see_fit,'Общая англоязычная программа, которую можно совместить с обследованием тайваньской базы.',
            ['Класс каждого, адрес и площадка, доступность выбранной группы, внешний приём, итоговый счёт/отмена.'],
            [('Программа, площадки, grade, цена и English',url)],status='published_2027',role='primary',priority=['both','general'],sessions=pairs)
        p['timing']['variant_keyed']=True
        p['timing']['session_details']=[dict(start=a,end=b,variant_key=key,label=place,source=url,place=place,formats=['day'],
            price=price['label'],date_scope='day_camp_window',attendance_weekdays=['TH','FR'] if 'japan' in slug else ['MO','TU','WE','TH','FR'])
            for (a,b),key,place in zip(pairs,['taipei','xindian'],places)]
        p['partner_locations_unconfirmed']='Партнёрские университетские группы Coming Soon/другие прайсы не добавлены как открытые смены.'

    p=put('srt-little-elf','SRT × Kids Space · Little Elf Journey','SGP','Kids Space,16A Dempsey Road,Singapore247695',
        'general,art,languages','day','4–7; max12.',
        'English прямо указан организатором.',
        'Театр, Christmas storytelling и creative arts; выбор1–3дней.',
        '14–16 декабря 2026, Mon–Wed09–15 по конкретной SRT странице. Annual Kids Space poster пишет14–18Dec: пять дней не переносим на трёхдневный курс. Можно1,2 или3дня.',
        fee(2026,'Non-member SGD160/day или480/3дня; member130/day или390/3дня.',
            'Занятия и lunch.', 'Жильё/дорога отдельно; member price только при подтверждённом членстве.',
            'Отмена/депозит/early care неизвестны.'),
        'Дневной формат, родители забирают; пансион не заявлен.',
        fit('not_eligible','2017:8–9, выше7.'),fit('candidate','2020:5–6 соответствует4–7; внешний приём/место подтвердить.'),
        'Небольшая общая EN программа для Оскара, пока Матвей посещает старший курс.',
        ['Выбранные дни, наличие места, внешние дети, возврат/late pickup.'],
        [('Dates/English/price/lunch',SRT+'srt-kidsspace-dec'),('Annual poster с другим date range','https://www.kidsspace.sg/wp-content/uploads/2025/12/2026-CAMPS-CALENDAR.pdf')],status='published_2026',role='primary',priority=['general'],sessions=[['2026-12-14','2026-12-16']])
    detail(p,SRT+'srt-kidsspace-dec',date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE'])
    for slug,name,age,mat,osc,closed in [
      ('srt-stage-younger','SRT · English Stage Camp4–7','4–7, strict birthdate.',fit('not_eligible','Выше7.'),fit('conditional','Возраст подходит, но English week7–11Dec sold out.'),True),
      ('srt-stage-older','SRT · English Stage Camp8–12','8–12, must already turn8.',fit('candidate','8–9 подходит; сайт сообщает limited slots, это не подтверждённая бронь.'),fit('not_eligible','5–6 ниже8.'),False),
    ]:
        p=put(slug,name,'SGP','Aliwal Arts Centre,28 Aliwal Street,Singapore199918','general,art,languages','day',age,
            'English только7–11Dec.23–27Nov и30Nov–4Dec — Mandarin, не English.',
            'Legends of Europe: devised theatre, storytelling, teamwork/public speaking; Friday showcase.',
            'English7–11 декабря2026, Mon–Fri09–12. Younger sold out; older limited slots на дату чтения.',
            fee(2026,'SGD400 incl GST +6 booking =406.', 'Пятидневный театральный курс.',
                'Жильё/дорога; lunch не заявлен.10% early bird закончился4Oct; group/siblings10% условия подтвердить.',
                'Camp refund/booking fee refund неизвестны.'),'Дневной; max15. Family showcase Friday11:15–12.',mat,osc,
            'Раздельные возрастные группы и конкретный язык каждой недели.',
            ['Внешний приём, группа, доступность English, refund/итоговый счёт.'],
            [('Текущие недели, language/availability/age/fee',SRT+'stagecamp')],status='published_2026',role='primary',priority=[] if closed else ['general'],sessions=[['2026-12-07','2026-12-11']])
        detail(p,SRT+'stagecamp',date_scope='day_camp_window',availability=dict(status='closed' if closed else 'limited',
            label='English4–7 sold out' if closed else 'По сайту limited slots; реальное место не подтверждено'))

    p=put('voca-power-popstars','VOCA Academy · Power Popstars','SGP','277 Orchard Road,#04-03 Orchard Gateway,Singapore238858',
        'general,art','day','6–12.',
        'Язык всего курса не установлен: EN webpage и название Power Popstars не доказывают EN instruction.',
        'Вокальная техника/solo coaching, group dance, performance; Wednesday12:30 семейный mini-showcase и certificate.',
        '7–9 или14–16 декабря2026, Mon–Wed10–13.',
        fee(2026,'SGD450/3дня +50 registration =500. До31Oct 10% только tuition:405+50=455.',
            'Курс, VOCA bag/folder и certificate.', 'Жильё/дорога; еда не заявлена. Скидки не складываются.',
            'Full payment для регистрации; FAQ camp строго no refunds. Registration fee не считать скидочной частью.'),
        'Дневной курс у Somerset MRT; пансион не заявлен.',
        fit('conditional','Возраст подходит; подтвердить English преподавание.'),fit('conditional','Не раньше6-летия на дату смены; English нужно подтвердить.'),
        'Короткий творческий курс с ясной ценой; EN фильтр не включаем без доказательства.',
        ['Language конкретного курса, возраст на старте, место, обязательный fee/отмена.'],
        [('Курс, даты, прайс, camp FAQ',VOCA),('Company policies link','https://vocaacademy.co/faq/')],
        status='published_2026',sessions=[['2026-12-07','2026-12-09'],['2026-12-14','2026-12-16']])
    detail(p,VOCA,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE'])

    put('kisas-ai-music','KISAS · Humanities,English & AI Music','KOR','University campus,dormitory · площадка2027 TBA',
        'general,ai,art,languages,business','boarding','Grades4–9 /10–15; одновременно grade и age.',
        'English humanities lessons с native/bilingual support; язык всех AI/music и residential activities неизвестен.',
        'Собственный сюжет → English lyrics → AI melody → team performance; essay/creative journal/video/certificate. Cohort1:17 humanities+17K-pop periods; объём2027 ещё не подтверждён.',
        'January2027 только план: даты, длительность, capacity,venue и цена TBA. Прошлая cohort1 10дней/9ночей не переносится автоматически.',
        fee(2027,'TBA; pre-registration бесплатна и не резервирует место.',
            'Новый пакет ещё не установлен.', 'Все расходы/состав2027 неизвестны.',
            'Новая форма, payment/refund TBA; ничего не отправлено.'),
        'Планируется university dorm; staff ratios/insurance/24h care на сайте описывают cohort1, 2027 нужно подтвердить.',
        fit('later','January2027: только после10-летия И при Grade4+; месяц рождения/класс неизвестны.'),fit('later','До10лет/Grade4 далеко.'),
        'Перспективный creative AI трек Матвею позже; программа не является сертифицированным курсом Oxford.',
        ['Новые age/grade/date/venue/fee, English AI instruction, международный приём, staff/insurance и результат.'],
        [('Возраст, programme и next-cohort disclaimer',KISAS),('Humanities/AI curriculum cohort1',KISAS+'/program'),('Residential cohort1 boundary',KISAS+'/camp-life')],
        status='partial_2027',role='language_lessons',priority=['technical'])
    p=put('embassy-korea-spring','Embassy Camps · Korea Spring','KOR','Seoul + Busan · hotels2027 поимённо не опубликованы',
        'general,languages,adventure,art,business','boarding,family','10–19; семейный формат не отменяет child age10.',
        'English Speaking Club заявлен; английский всех экскурсионных/культурных занятий не установлен.',
        'Культурный маршрут, K-pop/taekwondo/cooking, English club, leadership/team quests; отдельная parent programme.',
        '21–30 марта2027.',
        fee(2027,'$2 780 Twin Room; валюта/единица per person/parent-child пакет требуют подтверждения.',
            '4-star hotel, только breakfast, airport/activity bus transfers, основной programme и camp kit.',
            'Lunch/dinner, перелёт и страховка не подтверждены включёнными; parent fee неизвестен. Общие terms security deposit USD200 возвращается при отсутствии ущерба.',
            'Общие terms: <45/<25/<20/<14дней штраф25/50/75/100%; refund processing USD100. Границы и применимость конкретному Korea договору подтвердить.'),
        'Seoul/Busan4-star hotels, Twin2beds. Ночной присмотр при самостоятельном участии и family room/parent tariff подтвердить.',
        fit('conditional','Только если уже10 на21.03.2027; до10-летия допуск не заявлен.'),fit('later','6–7 ниже10; parent programme не разрешает участие младшего.'),
        'Будущий cultural/English маршрут; цена Twin не означает полную стоимость семьи.',
        ['Точная DOB Матвея, child/parent quotation с валютой и meals, hotels, EN excursion и night-care.'],
        [('Korea dates/age/Twin fee/breakfast/parents',EMB),('Общие booking/cancel/security terms','https://embassy.camp/terms-and-conditions/')],
        status='published_2027',role='language_lessons',priority=['general'],sessions=[['2027-03-21','2027-03-30']])
    detail(p,EMB)

def extend_report_v83(report):
    report['shortlist'].extend([
      dict(label='Япония · небольшие EN пансионы зимой и весной',slugs=['ugaku-nasu-winter','ugaku-nasukashi-spring','ugaku-chatan-winter','ugaku-onna-spring','ugaku-wakayama-spring','myoko-adventure-culture'],
           reason='U-GAKU публикует конкретные зимние/весенние даты и initial fee; школьный класс/иностранный приём требуют проверки. Myoko6–15 advanced EN, новый2027 пока неизвестен.'),
      dict(label='Тайвань · общий English day camp обоим',slugs=['see-discover-japan','see-world-games'],
           reason='Senior kindergarten–Grade4; январь2027 в Taipei/Xindian, всё на English. DiscoverJapan остаётся в Тайване. Parents housing/класс каждого подтвердить.'),
      dict(label='Сингапур · театральные программы разным возрастам',slugs=['srt-little-elf','srt-stage-older','srt-stage-younger'],
           reason='Оскару LittleElf4–7; Матвею English Stage8–12. English Stage4–7 sold out; соседние ноябрьские смены Mandarin, их не выбираем как EN.'),
      dict(label='Корея · creative AI и культурный маршрут позже',slugs=['kisas-ai-music','embassy-korea-spring'],
           reason='Оба трека с10лет; KISAS также Grade4+. January2027 KISAS только план/TBA; KoreaSpring21–30March, только breakfast, Twin fee unit неизвестен.'),
    ])
    report['gaps'].extend([
      dict(country='Япония',iso='JPN',provider='U-GAKU / Myoko',
           detail='U-GAKU school grade и Japanese family administration требуют иностранного подтверждения; winter/spring premises различаются. /wakayama/ HTTP200 пустая, /kansai/ содержит настоящий2027camp. Общий spring news всё ещё priceTBA/NasuTochigi, новые campus pages уже price/Фукусима. MyokoPDF2026 не2027.',
           next_action='Иностранный приём, точные классы, English parents/medical support, актуальный договор и final invoice; прочитать Myoko2027 при публикации.',url=U+'english-camps/'),
      dict(country='Тайвань',iso='TWN',provider='S.E.E. / NTUE CLEC',
           detail='SEE grades, ранние individual/group discounts и отдельные площадки сохранены. PalauFamily primary недоступна: headline price range не тариф семьи. NTUE28Dec2026–8Jan2027 Mandarin6–15, NTD36000/early34000; English guide — перевод, EN занятий не доказан.1Jan нет занятий: не создан EN ICS.',
           next_action='SEE foreign grades/refund, Palau полный пакет/даты/язык; NTUE beginners/EN teaching support выяснить отдельно, не путать English guide с bilingual camp.',url=NTUE),
      dict(country='Сингапур',iso='SGP',provider='SRT / Kids Space / VOCA',
           detail='SRT язык/возраст/проданность каждой недели различаются;4–7 English Stage closed. KidsSpace annualPDF14–18Dec против конкретной SRT14–16Dec: выбраны3дня конкретного курса. AnnualPDF без полного age/price/language, весь год не размножен в ICS. VOCA EN не доказан;450+50 до скидки, non-refundable;6-летие младшего проверить.',
           next_action='Конкретная EN группа, admissions/refund, quotation и место; KidsSpace dated programme вместо годового themed poster.',url=SRT+'stagecamp'),
      dict(country='Южная Корея',iso='KOR',provider='KISAS / Embassy Korea',
           detail='KISAS next January2027 date/venue/length/fee TBA и age10/Grade4, English humanities отдельно от AI/music. KoreaSpring age10–19; Twin$2780 и breakfast only, family parent offer не допуск Оскара. Boarding school curriculum не внешняя holiday programme.',
           next_action='Матвей DOB/Grade4, English technical teaching, внешний admission и конкретный2027contract/hotel/child-parent invoice; младшие external camps продолжают исследоваться.',url=KISAS),
    ])
