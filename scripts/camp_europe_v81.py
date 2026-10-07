"""Read programme-specific 2027 European pages and preserve admission conflicts."""
CHECKED = '2026-10-05'
SALEM = 'https://www.schule-schloss-salem.de/de/summer-camps/salem-kids-camp/'
LAND = 'https://www.landheim-ammersee.de/en/summer-schools/international-summer-camp'
LAND_FORM = 'https://www.landheim-ammersee.de/sites/default/files/media/downloads/Anmeldung_Summer%20Camp_2027_EN_Formular_0.pdf'
LAND_AI = 'https://www.landheim-ammersee.de/en/summer-schools/ai-summer-campus-ammersee'
STGIS = 'https://www.stgis.at/camps/'
YOYO = 'https://www.yoyocamps.de/'
BAC = 'https://bookacamp.de/de/booking/form/view-by-date/162c63b16e6cec45f83ae6ac3227808f/'
NEWTECH = 'https://newtechkids.com/en/'


def add_europe_v81(add, src, fit, profiles):
    def put(*args, **kwargs):
        add(*args, **kwargs)
        p = profiles[-1]
        p['checked'] = CHECKED
        for s in p['sources']:
            s['checked'] = CHECKED
        return p

    def fee(year, label, included, extras, deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)

    def detail(p, a, b, label, url, formats, **extra):
        row = dict(start=a,end=b,label=label,source=url,place=p['place'],formats=formats,
                   price=p['price']['label'],date_scope='day_camp_window' if formats==['day'] else 'camp_session')
        row.update(extra)
        p['timing'].setdefault('session_details',[]).append(row)

    p = put('salem-kids-2027','Salem · Kids Camp','Германия','DEU','Schlossbezirk 1, 88682 Salem',
        'general,languages,science,art,music,sport,adventure','boarding','9–11; Junior12–14 и Senior14–16 отдельно.',
        'Есть Basic English и Deutsch als Fremdsprache. Basic English требует минимум год школьного английского; это не доказательство EN всех занятий. History требует хороший немецкий; язык Mini Uni и всей лагерной жизни подтвердить.',
        'Утром 08:15–10:15 выбирают одну академическую группу: прикладная математика, Basic English, Deutsch, History, Mini Uni (наука/техника), DaF. Затем искусство, музыка, сцена, лес или цирк; после обеда спорт, bushcraft и другие практические активности. Mini Uni не заявлена как курс сборки/программирования роботов.',
        '24 июля – 7 августа 2027. Запись для Kids открывается 1 ноября 2026; новичкам приоритет, повторные участники на waiting list с решением в мае.',
        fee(2027,'EUR 3 650 / весь двухнедельный пансион.',
            'Занятия, круглосуточные Betreuung/поддержка, жильё, все приёмы пищи, активности и экскурсии прямо включены.',
            'Дорога, аэропортовый трансфер, страховка и личные расходы не раскрыты как включённые; запросить итоговую смету.',
            'Аванс, сроки остатка и договор отмены 2027 не прочитаны; открытие формы не означает место.'),
        'Проба жизни в интернате с 24/7 сопровождением. Конкретная комната/корпус, лекарства и иностранный допуск требуют договора.',
        fit('conditional','9–10 в 2027 соответствует Kids; английский всей программы, требование школьного EN и выбранный курс подтвердить.'),
        fit('later','6–7 ниже минимума 9.'),
        'Общий академический пансион Матвею с настоящим прайсом 2027. Выбирать Mini Uni можно после проверки языка и содержания; это не робототехническая лига.',
        ['Подтвердить английский Mini Uni/лагерной жизни, фактическую группу, иностранный приём, корпус, трансфер/страховку и договор отмены.'],
        [src('Kids2027: возраст, цена, открытие записи и выбранные занятия',SALEM),src('Общие даты и другие возрастные лагеря','https://www.schule-schloss-salem.de/de/summer-camps/')],
        status='published_2027',confirmed=['EN'],priority=['general','boarding'],sessions=[['2027-07-24','2027-08-07']])
    p['language_evidence_role']='language_lessons'

    p = put('landheim-general-2027','Landheim Ammersee · International Summer Camp','Германия','DEU','Landheim 1, 86938 Schondorf am Ammersee',
        'general,languages,sport,art,adventure,robotics,ai','boarding','Форма2027 и текущий сайт:9–14; brochure с2026 в имени/теле:9–13 — архив.',
        'Текущий сайт предлагает English/German с носителями. Форма2027 прямо пишет: все international students посещают German course. EN занятий robotics/AI и EN-only участие иностранца не подтверждены; не обещать английский пансион.',
        'Общий языково-приключенческий пансион. Каждую из двух недель выбирают одну послеобеденную активность (четыре приоритета в форме): спорт, искусство/ремёсла, LEGO robotics, no-code/low-code AI agents, металлообработка и другое. Наличие Robotics/AI в форме не гарантирует группу/место или обе технические недели. Экскурсии выбирают по возрасту/подготовке; младший hut weekend9–11, сложный AlpineIII12–13, water overnight требует очень хорошего плавания.',
        '31 июля – 14 августа 2027: текущая страница и форма совпадают. Ссылка brochure всё ещё открывает Summer Camp2026 1–15 августа; эти старые даты не перенесены.',
        fee(2027,'EUR 2 750 за Summer Camp2027 по странице3 формы; Munich transfer включён.',
            'Форма прямо включает трансфер из/в Munich airport/main station. Основная программа и пансион описаны на сайте; полный пакет питания/материалов запросить в счёте.',
            'Дорога до Munich, страховка, карманные деньги, выбор технических опций и возможные сборы подтвердить; гаджеты/робот в собственность не обещаны.',
            'После заполненной формы присылают folder, договор и invoice. Зачисление только после полной оплаты и подписанного договора; размер аванса/отмена пока неизвестны. Форма нами не отправлялась.'),
        'Пансион на Ammersee плюс возможная ночёвка mountain hut/под палаткой на выбранной экскурсии. Страхование, комната и медицинские требования по договору.',
        fit('conditional','Возраст9–10 подходит, но international students German rule делает EN-only вариант неподтверждённым. Нужна конкретная языковая/техническая группа.'),
        fit('later','6–7 ниже минимума9.'),
        'Интересное сочетание общего лагеря и опциональных LEGO/AI для Матвея; языковой конфликт важнее маркетингового EN текста.',
        ['Разрешить international/German правило; подтвердить язык Robotics/AI, реальное выделение курса, плавание/экскурсию и полный договор/счёт2027.'],
        [src('Текущая программа и даты2027',LAND),src('Форма2027: возраст, язык иностранца, LEGO/AI, EUR2750 и трансфер',LAND_FORM),src('Архивная brochure2026, не новые условия','https://www.landheim-ammersee.de/sites/default/files/media/downloads/landheim-ammersee-international-summer-camp-2026-de-en.pdf')],
        status='published_2027',priority=['general','boarding'],sessions=[['2027-07-31','2027-08-14']])

    put('landheim-ai-future','Landheim Ammersee · AI & English Summer Campus','Германия','DEU','Landheim 1, 86938 Schondorf am Ammersee',
        'ai,coding,art,languages,sport','boarding','14–17.',
        'Утром AI ИЛИ English/Cambridge preparation. Native speakers явно относятся к English module; язык AI module не установлен. Английский курс не доказывает английский ИИ.',
        'Десятидневная будущая ступень: AI agents, AI film production, policy simulation games; альтернативный English module. После обеда водный спорт, столярная/металлическая мастерская, art, theatre/team sports; вечером общение и career orientation.',
        'Страница анонсирует август2027 и обещает новые документы1 октября2026, но доступные ссылки всё ещё brochure/application2026. Точных новых дат/прайса не прочитано; ICS не создан.',
        fee(None,'Прайс2027 неизвестен; цену общего лагеря EUR2750 сюда не переносить.',
            'Учёба, campus activities и пансион описаны; состав будущего тарифа не опубликован в прочитанном тексте.',
            'Дорога, трансфер, страховка, оборудование/аккаунты и опции по будущему договору.',
            'Приём/оплата/отмена2027 требуют актуальной формы; обещанная дата публикации не доказала выход документов.'),
        'Проба интернатной жизни; комната/питание и международный допуск нового сезона уточнить.',
        fit('later','До14 лет рано; не детский вариант2027.'),fit('later','До14 лет рано.'),
        'Сохранить как старшую AI/предпринимательскую ступень; нельзя смешивать с9–14 общим лагерем.',
        ['Ждать действующие документы2027, точные смены, полный прайс и язык AI, а не только English module.'],
        [src('Собственная старшая AI программа и несовпадение обещанных/доступных документов',LAND_AI)],status='next_unannounced')

    stfee = fee(2027,'EUR 4 180 / две недели; focused afternoon options имеют доплаты.',
        'Пансион, buffet meals/несколько ресторанных приёмов, обычные Outdoor Adventures; complimentary Salzburg airport/train collections на границах смен.',
        'Sailing CampI +EUR200; Golf CampII/III +500; Horse Riding CampIII +900, riding examinations отдельно. Дорога до Salzburg, страхование, внештатные transfer/extra nights и taxes подтвердить.',
        'Ссылка application2027 при прямом чтении404; brochure2027 ведёт в файл2026. Договор/депозит/отмену2026 не переносим на2027; наличие мест неизвестно.')
    p = put('stgis-general-2027','St. Gilgen · English / Creative Arts & Outdoor','Австрия','AUT','Ischlerstraße 13, 5340 St. Gilgen',
        'general,languages,art,sport,adventure','boarding','10–15; Robotics отдельный12–15 трек.',
        'CampI: English/German A1–B2 или Sustainability (EnglishB1/GermanB2). CampII: Creative Arts. Полный English поток Arts/всей жизни не установлен; подтвердить для опытного англоязычного ребёнка.',
        'Утро15 часов/нед.: CampI языки или Sustainability; CampII painting/drawing/ceramics/sculpture/portfolio. После обеда Outdoor Adventures (small groups max8) либо focused sailing/golf. Не все morning options доступны во всех трёх сменах. Максимум40 международных участников/смена, заявлен staff-to-camper1:2, телефоны днём собраны, вечером20:30–21:30.',
        'CampI10–23 июля2027; CampII24 июля–6 августа2027. Robotics only CampIII8–21 августа вынесен отдельно. Общая цена/даты текущего сайта прочитаны; application2027 пока404.',
        stfee,'En-suite double/triple rooms, по возрасту/полу; buffet meals и учёт диеты. Сбор Salzburg complimentary на старте/финише, окна/UM ещё подтвердить.',
        fit('conditional','Только после10-летия к старту. Для свободного EN проверить пользу language course и английский Creative Arts.'),fit('later','До10 лет не подходит.'),
        'Альпийский общий пансион Матвею после10-летия; курсы и спортивные доплаты привязаны к конкретной смене.',
        ['Действующая форма/договор2027, день рождения, английский CreativeArts, утренний трек, полный invoice/transfer/места.'],
        [src('Текущие смены2027, возраст и конкретные morning/afternoon options',STGIS),src('Ссылка новой формы:404 при проверке','https://www.stgis.at/summer-camp-application-2027/')],
        status='published_2027',confirmed=['EN'],priority=['general','boarding'],sessions=[['2027-07-10','2027-07-23'],['2027-07-24','2027-08-06']])
    p['language_evidence_role']='language_lessons'
    detail(p,'2027-07-10','2027-07-23','CampI · языки или Sustainability',STGIS,['boarding'])
    detail(p,'2027-07-24','2027-08-06','CampII · Creative Arts',STGIS,['boarding'])
    p = put('stgis-robotics-ai-2027','St. Gilgen · Robotics, Coding & AI','Австрия','AUT','Ischlerstraße 13, 5340 St. Gilgen',
        'robotics,coding,ai,games,science','boarding','Конкретный Robotics track:12–15, английский минимумB2; общий лагерь10–15 не отменяет это правило.',
        'Прямое требование минимумB2 English именно Robotics, Coding & AI. Beginners/advanced welcome по coding; B2 языковой порог остаётся.',
        'Design/build/program robot challenges; AI/ML, beginner-friendly apps/games и STEM engineering. Утро15 часов/нед.; после обеда Outdoor Adventure, Golf или Horse Riding. Sailing CampI не опция этого заезда. Конкретные platforms, device/account и take-home robot не раскрыты.',
        'Только CampIII8–21 августа2027. Общие школьные даты/возраст не применяем вместо условий этого трека.',
        fee(2027,'EUR 4 580 = базовые4 180 + Robotics surcharge400 / две недели.',
            stfee['included'],'Golf ещё +EUR500 (итог5080) или Horse Riding +900 (5480), examination fees отдельно; '+stfee['extras'],stfee['deposit']),
        p['accommodation'],fit('later','Матвею9–10, ниже12 в2027; минимум10 общего лагеря не достаточен.'),fit('later','Оскару6–7, ниже12.'),
        'Будущая инженерная ступень с ясным EnglishB2 и собственным возрастным порогом; не готовый technical camp детям сегодня.',
        ['Форма/договор2027, B2 подтверждение, выбранная afternoon option, platform/device и полноценная смета.'],
        [src('Конкретный Robotics12–15/B2/CampIII/+400',STGIS),src('Новая форма пока404','https://www.stgis.at/summer-camp-application-2027/')],
        status='published_2027',confirmed=['EN'],sessions=[['2027-08-08','2027-08-21']])
    p['language_evidence_role']='primary'

    dayfee = lambda label: fee(2027,label,
        '09–16 дневная программа, тёплый lunch и вода; creative projects/игры. Snack можно принести с собой.',
        'Жильё семьи, дорога, страховка и early/late care отдельно. Таблица показывает «от», FAQ описывает Soli ±EUR15 для day camp; получить обычный полный тариф и sibling discount.',
        'AGB Jan2026: авансEUR25 в14 дней от invoice, остаток около3 недель до лагеря. Отмена:60+ дней EUR15;30+/15+ дней20%/50%; менее15 дней90%; со старта возврата нет. День15 описан двумя строками — подтвердить границу. Optional Rücktrittsgarantie EUR25 с другими условиями; минимум12 детей.')
    for slug,name,key,dates,age,label,mat,osc,programme in [
        ('yoyo-fez-july','YoYo · FEZ English & Climbing · июль','7',['2027-07-19','2027-07-23'],'Конкретная неделя6–12; общий текст6–14 шире.','От EUR429 /5 дней.',fit('candidate','9–10 входит6–12; внешний приём/место подтвердить.'),fit('conditional','6–7 входит6–12 только при6-летии; конкретная неделя July.'),'Английская общая игровая/спортивно-творческая неделя; climbing forest (высокий parcours от130cm, младшим Zwergenparcours), lake/outdoor и небольшие проекты. Robotics не заявлена.'),
        ('yoyo-fez-august','YoYo · FEZ English & Climbing · август','7',['2027-08-02','2027-08-06'],'Конкретная неделя8–13; общий текст6–14 не допуск младшего.','От EUR429 /5 дней.',fit('candidate','9–10 входит8–13; место/приём подтвердить.'),fit('not_eligible','6–7 ниже конкретного минимума8, несмотря на общую6–14 карточку.'),'Те же общие English games, climbing и творческие проекты, но другая возрастная неделя. Для двух братьев одновременно выбирать July, а не этотAugust вариант.'),
        ('yoyo-steglitz-2027','YoYo · Berlin-Steglitz English','86',['2027-08-02','2027-08-06'],'В датированной таблице8–12; общая карточка6–14 расходится.','От EUR419 /5 дней.',fit('candidate','9–10 подходит8–12; внешний приём и место подтвердить.'),fit('not_eligible','6–7 ниже опубликованной группы8–12 конкретной недели.'),'English games, спорт, drawing/craft projects и возможный afternoon pool. В Kinder- und Jugendhaus Immenweg; школьный/библиотечный театр и спортплощадка, полноценная техника не заявлена.'),
    ]:
        course = 'fun-action-camp-berlin-steglitz' if key=='86' else 'fun-action-camp-fez-berlin'
        place = 'Kinder- und Jugendhaus Immenweg · Immenweg10,12169 Berlin' if key=='86' else 'FEZ-Berlin · Straße zum FEZ2,12459 Berlin'
        p=put(slug,name,'Германия','DEU',place,'general,languages,art,sport,adventure','day',age,
            'Оператор прямо заявляет английский общения/проектов с ведущими; дети между собой могут говорить по-немецки. Уроков языка нет, learning by doing.',
            programme,dates[0]+'–'+dates[1]+'; своя Bookacamp table: «Bald buchbar». Показанные10+ не подтверждают уже доступную запись/место; homepage обещает booking концаOctober/началаNovember.',
            dayfee(label),'Без ночёвок; drop-off08:30–09:00 / pick-up15:30–16:00. Жильё/вечера семьи отдельно.',mat,osc,
            'Младший доступный EN общий вариант после проверки конкретной недели; не путать общий рекламный возраст и фактическую таблицу.',
            ['Обычная цена без Soli, точная возрастная группа, открытие записи/место, внешний допуск, высота/плавание, страховка и договор.'],
            [src('Конкретная программа',YOYO+'camps/'+course),src('Своя встроенная датированная таблица',BAC+key),src('FAQ / Soli и группы',YOYO+'infos'),src('AGB Jan2026 / оплата и отмена',YOYO+'agb')],
            status='published_2027',confirmed=['EN'],priority=['general']+(['both'] if slug=='yoyo-fez-july' else []),sessions=[dates])
        p['language_evidence_role']='camp_life'
        detail(p,*dates,'Конкретная возрастная неделя',BAC+key,['day'])

    boardprice=lambda year,label: fee(year,label,
        'Программа, supervision24/7, multi-bed комнатa с собственным WC/shower и три приёма пищи/день; напитки/диету учесть.',
        'Дорога, страховка, индивидуальный трансфер/личные расходы отдельно; «от» может быть Soli, FAQ для overnight±EUR25. Полный обычный счёт уточнить.',
        'AGB Jan2026: авансEUR50 в14 дней, остаток около3 недель до старта; стандартные отмены EUR15/20%/50%/90% по60/30/15-дневным срокам, после старта0refund; спорную границу15 дней уточнить. Optional RücktrittsgarantieEUR50; minimum12детей.')
    p=put('yoyo-ruppin-autumn','YoYo · Ruppiner See English Autumn','Германия','DEU','Jugenddorf · Gutsstraße23,16818 Neuruppin OT Gnewikow',
        'general,languages,sport,art,adventure','boarding','8–15.',
        'Ведущие исключительно на английском; дети друг с другом могут говорить по-немецки. Языковых уроков нет.',
        'Autumn creative projects/English games, climb tower и indoor pool excursions, campfire/night walk/disco/film. Это общий приключенческий пансион, не robotics курс.',
        '18–24 октября2026; текущая встроенная таблица «Ausgebucht» — заполнено. Даты сохранены как опубликованная смена, доступной рекомендацией не считаем.',
        boardprice(2026,'От EUR699 / неделя; набор заполнен по прочитанной таблице.'),
        'Multi-bed комнаты с собственным санузлом, круглосуточная ответственность. Autumn startsSun16:00, Saturday show11:30/забордо12:00; общийFAQ Sun–Fri не отменяет конкретныйSaturday.',
        fit('conditional','Возраст9 подходит, но опубликованная смена заполнена; только отдельное подтверждение/освободившееся место.'),fit('later','6 ниже8.'),
        'Показать настоящий статус ближайшего пансиона, чтобы семья не строила поездку по полной смене.',
        ['Не покупать билеты по заполненной карточке; новый набор/место, английский внешний приём, полный счёт/трансфер.'],
        [src('Autumn8–15 и конкретныйSaturday departure',YOYO+'camps/herbst-camp-im-jugenddorf-am-ruppiner-see'),src('Даты/прайс и sold out',BAC+'82'),src('Общие условия',YOYO+'agb')],
        status='published_2026',confirmed=['EN'],sessions=[['2026-10-18','2026-10-24']])
    p['language_evidence_role']='camp_life'
    p['availability']=dict(status='closed',label='Ausgebucht: заполнено на проверке05.10.2026; отменившееся место не доказано')
    detail(p,'2026-10-18','2026-10-24','Autumn · заполнено',BAC+'82',['boarding'],availability=p['availability'])

    p=put('yoyo-ruppin-spanish','YoYo · Ruppiner See Club Español','Германия','DEU','Jugenddorf · Gutsstraße23,16818 Neuruppin OT Gnewikow',
        'general,languages,sport,art,adventure','boarding','Датированная смена12–14; общий текст11–15 не допуск11-летнего.',
        'Испанский в своей группе; общие активности с другимиYoYo на английском, ведущий сохраняетES focus. Дети могут общаться по-немецки; немецкий не заявлен как обязательный входной язык.',
        'Испанское погружение через игры, творческие проекты, canoe/dragonboat и climbing, evening campfire/night walk/disco. Для свободно говорящегоES цель — самостоятельность/общение, а не начальный языковой курс.',
        '8–13 августа2027, Sun–Fri; таблица «Bald buchbar», показанные4female/4male не доказательство открытой записи или гарантированного места.',
        boardprice(2027,'От EUR659 /6 дней,5 ночей; обычный полный тариф подтвердить.'),
        'Multi-bed en-suite rooms; check-inSun15:30/start16:00, Frifinish15:30/забордо16:00. Родительский/airport transport неизвестен.',
        fit('later','9–10 ниже конкретного12-летнего минимума.'),fit('later','6–7 ниже12.'),
        'Будущий общийES/EN пансион; испанский вариант существует за пределами Испании, но в2027 обоим рано.',
        ['Возраст12–14 конкретной смены, польза дляnativeES, opening/места, внешний приём и полный счёт/transport/договор.'],
        [src('Испанская программа11–15 в общем тексте',YOYO+'camps/spanisch-camp-im-jugenddorf-am-ruppiner-see'),src('Смена2027:12–14 и ценаот659',BAC+'78'),src('Договор',YOYO+'agb')],
        status='published_2027',confirmed=['ES','EN'],sessions=[['2027-08-08','2027-08-13']])
    p['language_evidence_role']='bilingual'

    for slug,name,a,b,programme,legacy in [
        ('newtech-autumn-art','NewTechKids · Autumn robots & art','2026-10-12','2026-10-16','Изобретают роботизированные sculpture/music/drawing проекты; вычислительное мышление, обсуждение и prototype/test. Уровень образовательного введения, не обещание подготовки мирового чемпиона.','L132'),
        ('newtech-christmas-film','NewTechKids · Before Christmas film robots','2026-12-21','2026-12-24','Смотрят/обсуждают film clips, изобретают роботов для воображаемого фильма: Charlie and the Chocolate Factory, How to Train Your Dragon, WALL-E. Детский invention/design подход, не профессиональныйVFX.','L133'),
        ('newtech-christmas-art','NewTechKids · After Christmas robots & art','2026-12-28','2026-12-31','Роботы как art/sculpture, рисование и music-performing machines. Computational thinking/design/playful invention; образовательная программа не официальная соревновательная победа.','L134'),
    ]:
        p=put(slug,name,'Нидерланды','NLD','Amsterdam Public Library near Centraal Station · точную аудиторию подтвердить',
            'robotics,coding,art','day','Конкретные bootcamps8–12.',
            'Прямо Dutch/English combination by instructor; EN-only группа не обещана. Полное понимание ребёнком безNL подтвердить; Vocabularycomputer science преимущественноEnglish.',
            programme,a+'–'+b+'; собственная страница перечисляет этот конкретныйbootcamp. Часы/места не установлены.',
            fee(None,'Цена выбранногоbootcamp не опубликована в прочитанной основной карточке; короткиеregistrationlinks403.',
                'Instructor/programme по описанию; оборудование/питание/часы по конкретному договору.',
                'Stadspas subsidy только отдельнымeligible местным детям, не бесплатныйinternationalcamp. Lunch/transport/семейное жильё и robottake-home неизвестны.',
                'Депозит, оплата/отмена и внешний приём не прочитаны; регистрационные формы не отправляли.'),
            'Дневнойlibrarybootcamp, ночёвок нет; evening supervision/жильё родителей отдельно.',
            fit('conditional','Матвей8–9 в2026 подходит; проверить двуязычную поддержку безNL и задания для его опыта.'),fit('later','Оскар5–6 ниже8.'),
            'Ближайшие осенние/рождественские короткиеtechnical дни Матвею; существующая строка'+legacy+' связана без дублирования календаря.',
            ['EN-supportбезNL, точноадрес/часы, иностранныйдопуск, программа/kit, food, полноценныйпрайс/место/отмена.'],
            [src('Собственные конкретные8–12 даты и bilingual teaching',NEWTECH)],
            status='published_2026',confirmed=['EN','NL'],priority=['technical'],sessions=[[a,b]])
        p['language_evidence_role']='bilingual'


def extend_report_v81(report):
    report['shortlist'].extend([
        dict(label='Германия2027 · общие пансионы Матвею',slugs=['salem-kids-2027','landheim-general-2027','landheim-ai-future'],reason='Salem9–11 EUR3650 и Landheim9–14 EUR2750 сMunichtransfer; EN всей жизни/техники не доказан. LandheimforeignstudentsGermanrule нужно разрешить, LEGO/AI — выбор, не гарантия. СтаршийAI14–17 отдельно.'),
        dict(label='Берлин2027 · английский общий день двум братьям',slugs=['yoyo-fez-july','yoyo-fez-august','yoyo-steglitz-2027','yoyo-ruppin-autumn','yoyo-ruppin-spanish'],reason='КонкретнаяJulyFEZ6–12 подходит обоим по возрасту; AugustFEZ8–13/Steglitz8–12 — толькоМатвею. Общаякарточка6–14 не отменяет возрастнедели. Autumnsoldout, Spanish12–14 рано; ценыот иBald buchbar не место.'),
        dict(label='Австрия2027 · возраст и цена каждого трека',slugs=['stgis-general-2027','stgis-robotics-ai-2027','village-austria'],reason='StGISобщийс10 EUR4180, Roboticsтолькос12/B2English EUR4580; Matveyтолькоgeneralпоследесятилетия. Golf/Horseещё500/900. Form2027сейчас404, договор2026 не переносим.'),
        dict(label='Amsterdam2026 · ближайшийtechnicalbootcampМатвею',slugs=['newtech-autumn-art','newtech-christmas-film','newtech-christmas-art','bricks-robots-nl'],reason='NewTechKids8–12, Dutch/English; три существующихкалендарныхстроки связаны, не новыеивенты. Oscarдо8неподходит. Полныеprice/hours/foreignaccess/ENonlyнеизвестны; Stadspasнеобщаяльгота.'),
    ])
    report['gaps'].extend([
        dict(country='Германия',iso='DEU',provider='v81: Salem/Landheim младшие пансионы',detail='SalemKids2027 9–11 EUR3650, запись1November; BasicEnglishнеязыкMiniUni. Landheim2027form9–14/EUR2750/transfer; brochureпо-прежнему2026/9–13. ForeignstudentsGermanrule конфликтует сENвыбором; Robotics/AIопциональны. AIcamp14–17August2027 безновыхexactdates.',next_action='Язык конкретнойscience/robot/AI и foreignEnglishgates, назначенныйкурс/комната/договор/смета; Swiss/France/Spain и прочиеpriorityстраны остаются открыты.',url=LAND_FORM),
        dict(country='Германия',iso='DEU',provider='v81: YoYo возраст датированной недели и soldout',detail='ВстроеннаяоператоромBookacampFEZJuly6–12 противAugust8–13; Steglitz8–12 противgeneral6–14; Spanish12–14 противgeneral11–15. От429/419/659 иBaldbuchbarнеготовоебронирование. Autumn18–24Oct2026от699soldout, конкретныйSaturdaydeparture противgeneralFAQFriday. AGBJan2026ясны, граница15днейдвусмысленна.',next_action='ПодтвердитьобычныйSoliпрайс, familyforeignadmission/места/страховку, birthday/cohort, сборысемьи/transport иrefundграницу; считать конкретную группу первичной.',url=YOYO+'agb'),
        dict(country='Австрия',iso='AUT',provider='v81: StGIS конкретныйRoboticsgate2027',detail='Общий10–15 не минимумRobotics12–15/B2. MorningoptionsпривязаныCampI/II/III. EUR4180base+400Robotics, focusedafternoon+200/500/900 поотдельнымсменам. Application2027сейчас404; ссылкаbrochure2027остаётсяPDF2026. Персоналworkvisaразделнеусловиедопускадетей.',next_action='Актуальная2027форма/договор/ценаexactoption, английскийArts/всяжизнь, internationalchildaccess и birthday10; продолжаемallpriorityстраны.',url=STGIS),
        dict(country='Нидерланды',iso='NLD',provider='v81: NewTechKids multilingualrobotics',detail='3bootcamps2026linkedL132–134безduplicateICS; programme8–12 Dutch+English, не отдельныйENпоток. Короткиeregistrationlinks403, цена/часы/kit неизвестны; subsidyStadspasнеобщийтарифдлязарубежнойсемьи.',next_action='Прочитатьконкретнуюдоступнуюprice/termscard, внешнийдопуск/ENsupport, точныйaddress/time и новый2027набор. AdultAIeducationevent не добавленкакcampдетям.',url=NEWTECH),
    ])
