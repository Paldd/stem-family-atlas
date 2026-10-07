"""Winter Japan programmes and Taiwan cohorts; Korean STEAM language exclusion."""
from collections import Counter
from pathlib import Path
from camp_planning_v108 import offer

ROOT=Path(__file__).resolve().parents[1]
BASE='bf1931dc4ba4d621b6e2a30cc2662f84f0841584'
CHECKED='2026-10-06'
ISA='https://www.isa.co.jp/'
INDEX=ISA+'lp/injapan-ps-win.html'
TERMS=ISA+'assets/domestic/generalinformation.pdf'
JW='https://www.jgroup.com.tw/%E5%86%AC%E4%BB%A4%E7%87%9F/'
MAGIC='https://www.jgroup.com.tw/%E9%AD%94%E6%B3%95%E7%87%9F/'
RAIL='https://www.jgroup.com.tw/%E5%8B%87%E8%80%85%E8%83%8C%E5%8C%85%E5%AE%A2/%E9%90%B5%E9%81%93%E5%86%92%E9%9A%AA/'
OVERSEAS='https://www.jgroup.com.tw/summer-back-in-taiwan/'
EWHA='https://kle.ewha.ac.kr/kle/notice/notice.do?articleNo=799162&mode=view'
EFORM='https://kle.ewha.ac.kr/kle/notice/notice.do?mode=download&articleNo=799162&attachNo=525005'
NEW=['isa-safari-shinagawa','isa-safari-yokohama','isa-adventure-osaka','isa-adventure-aichi','isa-kyoto-winter','isa-tgg-winter','isa-drama-shinkiba','isa-board-aichi','isa-board-hachioji','isa-board-chiba','isa-board-yokohama','isa-board-shiga','isa-board-kobe','isa-board-fukuoka','isa-hills-tohoku','isa-okinawa-homestay','jasmine-magic-winter']
ASK='Подтвердить текущий школьный класс, иностранный индивидуальный приём, место, понятное детям сопровождение и полный счёт. Заявки, аккаунты и оплаты не выполнялись.'
ISA_LANG='Занятия на английском. Иностранные преподаватели и японские/bilingual сотрудники; помощь по-японски заявлена. Английское сопровождение всех бытовых и экстренных вопросов для приезжей семьи ещё подтвердить.'
ISA_CANCEL='В связанном PDF для пансионов и большинства дневных программ: отмена с 20 дней до старта — 20%, с 7 дней — 30%, накануне — 40%, в день начала — 50%, после начала/без уведомления — 100%. Это удержание, не сумма возврата. Оплата полной суммы по счёту; минимум группы может отменить программу. Поздний приход/пропуск и отказ от включённого автобуса не дают возврата. Применимость текущей редакции и календарный расчёт уточнить.'
J_CANCEL='Зимняя страница: возврат 95% за 41+ день, 90% за 31–40, 80% за 21–30, 70% за 2–20, 50% за один день; в день начала/после начала/без уведомления нет. Применяется договор поездки; переход в другую смену возможен только при местах. Срок ранней скидки 16 октября — не окончательный срок регистрации.'

def add_asia_v136(add,src,fit,profiles):
    def emit(slug,name,place,grade,start,end,deadline,fee,programme,housing,included,extras='',country='Япония',iso='JPN',themes='general,languages,culture',formats='day',url='',lang=ISA_LANG):
        lower=grade.split('–')[0]
        mat=fit('later','Минимум 5-й класс; до подтверждения более старшего класса это будущая ступень.') if lower=='5' else fit('conditional','Нужен текущий '+grade+' класс, а не только год рождения 2017. Эквивалент зарубежного класса и индивидуальный приём ещё согласовать.')
        osc=fit('later','Минимум '+lower+'-й класс; первый класс не подходит. Класс Оскара неизвестен, этот вариант не выбран как старт младшего.')
        price=dict(year=2026 if start<'2027-01-01' else 2027,label=fee,included=included,extras=extras or 'Дорога до места сбора, жильё родителей, личные расходы, страховка/медицинское покрытие и полный счёт иностранной семье отдельно.',deposit=ISA_CANCEL)
        add(slug,name,country,iso,place,themes,formats,'Текущий '+grade+' класс; международный эквивалент подтвердить.',lang,
            programme,'Опубликовано '+start+'–'+end+'. Срок заявки '+deadline+'; места и допуск отдельно.',price,housing,mat,osc,
            'Конкретная зимняя языковая/общая программа с первичной ценой. Редакционный кандидат для семейной поездки, не независимый мировой рейтинг и не робототехническая победа.',
            [ASK],[src('Выбранная программа: возраст/класс, цена, место и даты',url),src('Зимний каталог и языковая среда',INDEX),src('Процесс, разные типы отмены и японские сотрудники',TERMS)],
            status='published_2026_27',confirmed=['EN'],sessions=[[start,end]])
        p=profiles[-1];p['checked']=CHECKED
        for s in p['sources']:s['checked']=CHECKED
        p['timing']['session_details']=[dict(start=start,end=end,label='Точная зимняя программа',price=fee,place=place,source=url,deadline=deadline,date_scope='camp_session',
            entry='Личная заявка требует аккаунт ISA и подтверждение зарубежного класса. Сам аккаунт/заявка/оплата не выполнялись.',proof='Прочитаны выбранные положения текущей собственной страницы и связанного общего PDF. Stock-loading placeholder не подтверждает место.')]
        return p
    tuition='Занятия и материалы, помещение/активности, преподаватели и сопровождающий персонал. Обед не включён.'
    safari='Один день языковых игр, миссий, творческих работ и культурных активностей. EN-инструкции и японско-английские помощники; группы по уровню и классу. Это короткая общая языковая программа, не инженерный лагерь.'
    for slug,code,place,date,deadline in [(NEW[0],'typjzs1','Tokyo · Shinagawa · ISA, 1-6-41 Konan, 10F','2026-12-26','2026-11-21'),(NEW[1],'typjzs4','Yokohama · Kanagawa Kenmin Center','2026-12-27','2026-11-22')]:
        p=emit(slug,'ISA · English Safari · '+place.split(' · ')[0],place,'2–4',date,date,deadline,'12 800 JPY за день',safari+' Сбор 09:50, конец 15:00; максимум 30, минимум 20.',
            'Дневное посещение; ночное жильё семьи отдельно.',tuition,url=ISA+'program/'+code+'_26win.html')
        p['shortlist']=['general']
    for slug,code,place,date,deadline,programme in [
        (NEW[2],'ospjza2','Osaka Science Museum · 4-2-1 Nakanoshima','2026-12-26','2026-11-21','Английские миссии в научном музее, подготовка/обсуждение увиденного. Один bilingual сотрудник примерно на 5 детей. Сбор 09:50, конец 16:00; максимум 40/минимум 30.'),
        (NEW[3],'ngpjza1','Aichi · Inuyama · Little World','2026-12-27','2026-11-22','Языковые миссии среди зданий и экспозиций культур мира, итоговое занятие. Примерно один bilingual сотрудник на 6 детей. Сбор 09:50; точный конец подтвердить; максимум 45/минимум 30.')]:
        emit(slug,'ISA · English Adventure · '+place.split(' · ')[0],place,'3–6',date,date,deadline,'11 000 JPY за день',programme+' Это экскурсионная языковая программа, не robotics интенсив.',
            'Один день, без ночёвки.',tuition,url=ISA+'program/'+code+'_26win.html')
    emit(NEW[4],'ISA · Kyoto English Camp · три дня','Kyoto JA Building · 1 Higashikujo Nishisannocho','3–6','2026-12-26','2026-12-28','2026-11-21','29 800 JPY за три дня',
        'EN-общение, игры, иностранные преподаватели и группы по уровню/классу, допускаются начинающие. Сбор 09:50, выдача 14:30 каждый день; максимум 40/минимум 20. 26–27 декабря — выходные, занятия всё равно заявлены.',
        'Три дневных посещения; семейное жильё отдельно.',tuition,url=ISA+'program/ospjze1_26win.html')
    p=emit(NEW[5],'ISA × TGG · английские миссии','Tokyo Global Gateway · 2-4-32 Aomi, Koto','3–9','2026-12-28','2026-12-28','2026-11-23','15 800 JPY при сборе в TGG; 17 800 JPY с автобусом из Shinjuku/Yokohama',
        'Группа 8 детей и один иностранный leader, практические миссии/общение/рефлексия; младшая и secondary программы различаются. TGG: 09:40–16:00; автобус Yokohama 07:40–18:00, Shinjuku 08:40–17:00. Всего до 120, минимум 60; не обещана единая группа всем точкам сбора.',
        'Один день. Автобус и часы зависят от выбранного сбора.',tuition+' Автобус только в автобусном пакете.',url=ISA+'program/typjz33_26win.html')
    p['price']['deposit']='Для ISA×TGG отдельная отмена в PDF: с 10 дней 20%, с 7 дней 30%, накануне 40%, в день начала 50%, после/без уведомления 100%. Оплата по счёту, пропуски не возвращаются. Это отличается от 20-дневного порога других программ.'
    p=emit(NEW[6],'ISA · English Drama · первая короткая ночёвка','Tokyo · Shinkiba · BumB Sports Culture Center','3–5','2027-01-04','2027-01-05','2026-11-28','44 000 JPY за два дня / одну ночь',
        'EN-фразы, ритм, песни, игры и групповое выражение. В школьном flyer были ошибочные 4–6 января/две ночи; оператор исправил на 4–5 января/одну ночь. Сбор 10:40 первого дня, конец 16:00 второго, максимум 40/минимум 20.',
        'Одна ночь, комнаты по 5 детей по полу с ванной/туалетом. Пищевая аллергия не обслуживается по странице; конкретную потребность согласовать.',
        'Занятия/материалы, проживание, преподаватели и сопровождающие; 1 завтрак, 2 обеда, 1 ужин.',formats='boarding',themes='general,languages,art',url=ISA+'program/typjbt1_26win.html')
    conflict='Срок заявки расходится внутри страницы: в заголовке 30 ноября, в подробной карточке 28 ноября 2026. Для напоминания выбран более ранний 28 ноября; действующий срок подтвердить у ISA.'
    p['timing']['label']+=' '+conflict
    p['questions'].append(conflict)
    p['timing']['session_details'][0]['proof']+=' '+conflict
    boards=[
        (NEW[7],'ngpjbj3','Aichi · Aichi Health Plaza Hotel','2026-12-25','2026-12-27','2026-11-20',59000,'4','нет'),
        (NEW[8],'typjbj9','Tokyo · Hachioji · University Seminar House','2026-12-26','2026-12-28','2026-11-21',59000,'3–4','возможно, с ограничениями'),
        (NEW[9],'typjbj1','Chiba · Alvin Sports Park','2027-01-04','2027-01-06','2026-11-30',59000,'2–6','нет'),
        (NEW[10],'typjbj0','Yokohama · Kamigo Mori no Ie','2027-01-04','2027-01-06','2026-11-30',59000,'9–14','нет'),
        (NEW[11],'ospjbj3','Shiga · Hotel Biwako Plaza','2027-01-04','2027-01-06','2026-11-30',53000,'2–3','возможно, с ограничениями'),
        (NEW[12],'ospjbj4','Kobe Seminar House','2027-01-04','2027-01-06','2026-11-30',57000,'2–3','возможно, с ограничениями'),
        (NEW[13],'fkpjbj3','Fukuoka · Manabi no Yado','2027-01-09','2027-01-11','2026-12-05',51000,'2–3','нет')]
    for slug,code,place,start,end,deadline,fee,rooms,allergy in boards:
        emit(slug,'ISA · English Boarding Camp · '+place.split(' · ')[0],place,'4–9',start,end,deadline,f'{fee:,} JPY за три дня / две ночи',
            'Групповые арт-проекты, EN-презентации и выражение своего мнения, уровни по возрасту/языку. На общей странице 100% EN, однако японские сотрудники дают поддержку. Это короткий языковой пансион, без объявленного robotics/AI курса. Дневные часы/сбор зависят от автобусного или местного прибытия.',
            'Две ночи; '+rooms+' ребёнка в комнате по полу, общие ванная/туалет. Обслуживание пищевых аллергий: '+allergy+'. Соседей можно запросить, не гарантировано.',
            'Две ночи, занятия/материалы/персонал, 2 завтрака, 3 обеда, 2 ужина; предусмотренный автобус в пакете.',formats='boarding',url=ISA+'program/'+code+'_26win.html')
    emit(NEW[14],'ISA · British Hills · будущая школьная ступень','Fukushima · Tenei · British Hills','5–12','2026-12-30','2026-12-31','2026-11-25','49 800 JPY при местном сборе/Shin-Shirakawa; 61 800 JPY от Tokyo Station',
        'EN-культурные занятия, столовый этикет, групповая презентация, предполагаемые свечи/сконы. До 20 в учебной группе; общая смена до 45/минимум 30. Программа не в Великобритании и не инженерный лагерь.',
        'Одна ночь; 2–4 в комнате по полу, общие ванная/туалет. Аллергии могут обслуживаться с ограничениями.',
        'Жильё, занятия/материалы/персонал; 1 завтрак, 2 обеда, 1 ужин. Shinkansen из Tokyo только в Tokyo пакете.',formats='boarding',url=ISA+'program/sdpjbuk_26win.html')
    p=emit(NEW[15],'ISA · Okinawa English Homestay','Okinawa · принимающая семья; вылет Haneda/Itami','4–9','2026-12-25','2026-12-28','2026-11-20','Haneda: 245 000/275 000/335 000 JPY; Itami: 195 000/225 000/285 000 JPY за ребёнка — 3–4/2/1 участник в семье по порядку',
        'Жизнь в англоязычной принимающей семье, игры/еда/культурное общение и предвыездная онлайн-ориентация. Только пакет 2 участника в семье обещает совместное размещение заранее указанных друзей/братьев; нельзя купить его одному. Братьям школьный допуск отдельно. Минимум 10/максимум 20 на аэропорт.',
        'Три ночи в принимающей семье; состав/адрес/ночное сопровождение и бытовой EN конкретного размещения подтвердить.',
        'Внутренний перелёт Японии туда-обратно в economy, аэропортовые сборы, местная организация/транспорт, homestay, питание по маршруту, стандартный багаж, сопровождающий.',
        extras='Международный прилёт в Японию, дорога до аэропорта старта, сверхнормативный багаж, личные расходы и отдельные приёмы пищи по маршруту; страховку и итоговый счёт уточнить.',formats='boarding',url=ISA+'program/typjbo4_26win.html',
        lang='Оператор описывает общение на английском в принимающих семьях, начинающие допускаются. Это языковой homestay, без гарантии количества EN-уроков или английского всех служебных сообщений.')
    p['language_evidence_role']='camp_life'

    add(NEW[16],'Jasmine Garden · AXC Magic Factory · winter','Тайвань','TWN','Taipei · National Taipei University of Education','science,makers,art,general','day','Текущий 1–4 класс на дату регистрации, не будущий класс.',
        'Задания и занятия ведут на английском; среда EN/ZH с иностранным TA и китайскоязычным сотрудником. Правила/безопасность должны быть понятны каждому. Это не весь день только EN; англоязычное объяснение сложных вопросов ещё подтвердить.',
        'Пять дней изучения изменений материалов: цвет, пропорции/порядок, пена/движение/текстура, собственный способ и повторный тест другой командой. Инструмент, работа и записи испытаний домой. 09–17: задачи/ручные студии чередуются с играми, обедом, спокойным временем, обязанностями миниобщества и физической активностью. Не робототехника и не пять полных дней лаборатории. Нагрев/огонь делает взрослый; конкретные материалы уточнить.',
        '25–29 января 2027, понедельник–пятница. Приход 08–09, занятия 09–17; поздний pickup опционально до 18:30. Early до 16 октября 2026; далее обычная цена, пока есть места.',
        dict(year=2027,label='NT$13 800 за пять дней; early NT$12 800. Двое: 27 600 /25 600 TWD до опций и поездки.',included='Обед и лагерное страхование прямо включены; состав покрытия, материалы и оборудование уточнить по счёту.',
            extras='Одежда лагеря опционально NT$300/шт., прежнюю можно использовать. Поздний pickup отдельно: тариф этой смены не установлен. Жильё/дорога/перелёт семьи отдельно.',deposit=J_CANCEL),
        'Пять дневных посещений, без зимнего пансиона. Кампус университета — площадка, оператор Jasmine Garden.',
        fit('conditional','Нужен текущий 1–4 класс; Матвею возможен общий научный трек, если класс и иностранный приём подтверждены.'),fit('conditional','Только если Оскар уже в 1–4 классе при регистрации; preschool не разрешён. 2020 год сам по себе этого не доказывает.'),
        'Короткий общий EN-led научный маршрут для обоих при подходящем классе, с точной датой и ценой; местная двуязычная среда, не международный пансионный рейтинг.',[ASK],
        [src('Конкретный научный курс, английский, даты и цена',MAGIC),src('Зимние цены, классы, сроки скидки и возвраты',JW),src('English support и Mandarin сверстников, условия зарубежной семьи',OVERSEAS)],
        status='published_2027',confirmed=['EN'],sessions=[['2027-01-25','2027-01-29']])
    p=profiles[-1];p['checked']=CHECKED;p['language_evidence_role']='bilingual'
    for s in p['sources']:s['checked']=CHECKED
    p['questions'].append('Описание расходится: общая зимняя витрина упоминает плащ, зелья и сургуч, а конкретная карточка Magic Factory — исследование материалов и прямо исключает ролевую игру. Программа здесь взята из конкретной карточки; актуальный состав перед заявкой подтвердить.')
    p['timing']['session_details']=[dict(start='2027-01-25',end='2027-01-29',label='Magic Factory · 5 дневных дней',price=p['price']['label'],source=MAGIC,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR'],place=p['place'])]

def correct_profiles_v136(profiles):
    ps={p['slug']:p for p in profiles}
    p=ps['jasmine-winter-block'];p['price']['deposit']=J_CANCEL;p['checked']=CHECKED
    p['sources'].append(dict(title='Общий зимний FAQ: фактический возврат и переход между сменами',url=JW,checked=CHECKED))
    p=ps['jasmine-nola'];p['checked']=CHECKED
    p['price']['label']=p['price']['label'].replace('Rail16800+4500=21300;', 'Rail16800 включает ночь; 4500/21300 — прежняя летняя опция городских ночей и сумма с ней, не базовый тариф и не подтверждённая зимняя доплата;')
    p['sources'] += [dict(title='Зимняя железнодорожная смена: ночёвка, grade, EN support и прайс',url=RAIL,checked=CHECKED),dict(title='Зимний набор/возврат, три разные смены',url=JW,checked=CHECKED)]
    p['timing']['label'] += ' Добавлена зима 25–29 января 2027: железнодорожный маршрут, одна ночь D4 в Ruifang.'
    p['timing']['sessions'].append(['2027-01-25','2027-01-29'])
    p['timing']['session_details'].append(dict(start='2027-01-25',end='2027-01-29',variant_key='winter-rail',label='NOLA Railway Adventure · зима',age='Текущий 3–7 класс при регистрации.',price='NT$16 800; early NT$15 800 до 16 октября 2026, одна ночь включена',
        formats=['day','boarding'],source=RAIL,place='Taipei Station · железнодорожный круг Greater Taipei · ночь D4 Ruifang',date_scope='camp_session',
        family_fit=dict(matvey=dict(status='unknown',detail='Класс 3–7 и базовый Mandarin пока не установлены; EN support не превращает NOLA в EN-курс.'),oscar=dict(status='later',detail='Минимум 3-й класс; младшему этот самостоятельный маршрут пока не выбран.')),
        programme='Пять дней: Shanjia/Yingge, Ruifang/Shifen, Keelung, старые туннели/Sandiaoling/Houtong, планирование пути маленькой командой. Маршруты меняются по погоде/железной дороге; взрослые всегда сопровождают, не самостоятельный поезд без присмотра. Сбор 08–09, день 09–16:30; D4 нет вечерней выдачи, включена одна ночь Ruifang. Конкретный hostel/комната ещё неизвестны. Нужен самостоятельно переносимый рюкзак, чемодан не используется.',
        accommodation='Дневная программа с одной включённой ночью, не пять ночей пансиона. Место ночёвки ещё не объявлено.',
        extras='EasyCard и деньги на еду/проезд готовят родители; точные суммы, остальные приёмы пищи и включения согласовать. Одна ночь уже в NT$16800, не добавлять ещё NT$4500/6000 из других летних пакетов.',
        deposit=J_CANCEL+' Отдельная железнодорожная страница требует согласовать погодную отмену; её не считать автоматически покрытой общим личным отказом.',
        questions=[ASK,'Подтвердить базовый Mandarin, английскую поддержку в группе, конкретный hostel, ночного сотрудника, еду/проезд и отмену при погоде.'],
        proof='Зима и лето — один продукт по собственной странице, но разные даты/скидки. Зимний вариант связан с существующим досье без дублирования провайдера.'))

def extend_report_v136(r):
    r.update(version=136,asof=CHECKED)
    r['shortlist'] += [dict(label='Япония · новые зимние языковые программы ISA',slugs=NEW[:16],reason='Один оператор и разные места/форматы. Класс определяет допуск; 2–4 Safari, 3+ дневные/драма, 4+ пансионы, 5+ British Hills. Английские занятия не подтверждают EN бытовой поддержки иностранцам.'),
        dict(label='Тайбэй · младший зимний научный трек',slugs=[NEW[16],'jasmine-winter-block'],reason='Magic Factory 1–4 классы 25–29 января; Physical Workshop 1–5 классы 21–22 января. EN-led, среда двуязычная, по текущему классу при регистрации. Скидка до 16 октября 2026.')]
    r['gaps'].append(dict(iso='KOR',country='Южная Корея',provider='Bright Youth / Ewha · Seoul STEAM Winter 2027',url=EWHA,
        detail='Объявление/неподписанная DOCX: 4–22 января 2027, 15 будних дней 10–16:30, grade2–6, до60/min40. Цель — корейский и идентичность корейской диаспоры; EN/ES/RU преподавание не заявлено. KRW4000000, материалы/обед/перекус/экскурсионная дорога/билеты включены; жильё не заявлено, местный guardian нужен в форме. Пять STEAM блоков без описания конкретной робототехники/AI. Не добавлен как подтверждённый англоязычный семейный лагерь или мировой конкурс.',
        next_action='Уточнить не-корейское происхождение, реальный EN перевод занятий/безопасности и содержание STEAM; до этого семье не рекомендован. DOCX только прочитана, не заполнена/подписана/отправлена.'))
    review=r['family_review']
    for slug,reason,limit in [(NEW[0],'Один дневной языковой старт Матвею в 2–4 классе, во время семейной поездки.','Оскару минимум 2-й класс; иностранный приём и бытовой EN не подтверждены.'),(NEW[16],'Общий младший EN-led научный трек для братьев, если оба в текущих 1–4 классах.','Двуязычная среда; preschool не подходит. Ранний срок 16 октября, late pickup отдельно.')]:
        assert not any(q['slug']==slug for q in review['entries'])
        review['entries'].append(dict(slug=slug,goals=['general','languages'] if slug==NEW[0] else ['general','science'],reason=reason,key_limit=limit,dossier_checked=CHECKED))
    review.update(version=136,asof=CHECKED)
    ps={p['slug']:p for p in r['profiles']};review['coverage']=dict(candidates=len(review['entries']),countries=len({ps[q['slug']]['iso'] for q in review['entries']}),fully_audited_countries=0)
    r['counts']=dict(dossiers=len(ps),countries=len({p['iso'] for p in ps.values()}),swiss=sum(p['iso']=='CHE' for p in ps.values()),by_status=dict(Counter(p['timing']['status'] for p in ps.values())),source_urls=len({s['url'] for p in ps.values() for s in p['sources']}))

def extend_planning_v136(d):
    p=d['camp_planning'];ps={q['slug']:q for q in d['camp_programmes']['profiles']};price=ps[NEW[16]]['price']
    for ident,label,base in [('jasmine-magic-winter-early','Magic Factory · двое · early до 16 октября 2026',12800),('jasmine-magic-winter-standard','Magic Factory · двое · обычная цена',13800)]:
        q=offer(ident,NEW[16],label,base,currency='TWD',price_year=2027,checked=CHECKED,format='day',sessions=[['2027-01-25','2027-01-29']],sources=[MAGIC,JW],
            gate='Оба уже в 1–4 классах на дату регистрации, зарубежный эквивалент и EN поддержка ещё согласовать. Early применяется только в объявленный срок; скидка второго ребёнка не обещана, NT800 относится к второй смене того же ребёнка и не складывается.',
            optional=[dict(id='shirts',label='Две новые футболки · 300 × 2',amount=600)],unknown_required=[dict(id='extras_total',label='Обязательные доплаты · полный счёт/поздняя выдача ещё уточнить',unit='amount',rate=1,min=0)],
            included=price['included'],deposit_note=J_CANCEL,scope='Опубликованная цена пяти дневных дней для двоих, до жилья/перелёта/мест и возможных доплат. Early 25600 либо standard27600; две новые футболки отдельно600, не обязательны всем.')
        p['offers']=[a for a in p['offers'] if a['id']!=ident]+[q]
    p.update(version=136,asof=CHECKED)
    winter=next(q for q in d['events'] if q['id']=='CP729-20270125-20270129-winter-rail')
    winter['priority']='P4 — базовый Mandarin не подтверждён; семье пока не выбран'
    winter['action']+=' Не включать в выбранный семейный маршрут до подтверждения языка.'
