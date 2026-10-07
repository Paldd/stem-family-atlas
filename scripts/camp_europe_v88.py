"""Season-specific contracts, curricula and real autumn cohorts; no year copying."""
CHECKED = '2026-10-05'
ROSEY = 'https://www.roseysummercamps.ch/'
TASIS = 'https://summer.tasis.ch/'
ELF = 'https://www.leselfes.com/'
ELF_PDF = 'https://cdn.leselfes.com/wp-content/uploads/2026/04/'
ICS = 'https://www.icsparis.fr/student-life/ics-camps'
ALC = 'https://alcny.com/next-camp-2026'
GRANADA = 'https://granada-college.agorainternationalschool.es/en/school-life/summer-camp'

def add_europe_v88(add, src, fit, P):
    start = len(P)
    def price(year, label, included, extras, deposit):
        return dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
    def source(p,title,url):
        q=next((q for q in p['sources'] if q['url']==url),None)
        if q:q.update(title=title,checked=CHECKED)
        else:p['sources'].append(dict(title=title,url=url,checked=CHECKED))
    profiles={q['slug']:q for q in P}
    p=profiles['le-rosey']
    p['checked']=CHECKED
    p['language']='EN/FR используются ежедневно по FAQ. Выбранные языковые академии EN/FR; отдельный язык Tech & Robotics не установлен. My Mountain Adventure не предлагает традиционных уроков английского.'
    p['confirmed_instruction_languages']=['EN','FR'];p['language_evidence_role']='camp_life'
    p['programme']='Classic: одна утренняя академия на всю смену, ежедневно 2×75 минут; это 2,5 часа выбранного курса, не весь лагерный день. Tech & Robotics только 11–15: робототехнические проекты, LEGO League, CAD/3D, VR/AR и ответственное применение генеративного ИИ, максимум 20 учеников. Упоминание LEGO League не подтверждает официальный отбор FLL или международную награду. Для 8–12 есть Experimental Scientists и Life Skills; для 11–12 предпринимательство/лидерство. Лидерство и Theatre требуют EN B1; Theatre только август, Culinary Arts 13–15 только июль. Digital Creativity 13–15: Adobe, Procreate, Blender, съёмка с дрона. Выбирают также пять послеобеденных активностей; возраст/часы короткой Robotics для младших не раскрыты. Mountain 8–12: ориентирование, outdoor engineering, возобновляемая энергия, горы, ночёвки; без обычного языкового курса. My Family 8–13: две недели языковых занятий по 2×75 минут; третья — приключения без языковых уроков. Это детский пансион, родители с детьми не проживают.'
    p['price']['included']='FAQ: две недели/три недели выбранного лагеря, питание, занятия и активности, двухместная комната с санузлом, бельё/полотенца и прачечная; страхование экстренной болезни/травмы в Швейцарии. Трансфер Geneva только в официальные дни и временные окна. Состав маршрута и счёт 2027 окончательно подтвердить.'
    p['price']['extras']='Личные расходы и карманные деньги, домашний перелёт, виза и прибытие вне официального окна отдельно. В связанном финансовом PDF всё ещё SUMMER 2026: страхование отмены не включено, CHF150 удерживаются из карманных денег до отъезда; суммы/правила 2027 не объявлены этим договором.'
    p['price']['deposit']='FAQ: CHF1 000 невозвратный/непереносимый депозит в счёт тарифа. Ссылка financial-conditions.pdf явно SUMMER 2026: возврат 70% до 1 мая 2026 и отсутствие возврата позднее нельзя переносить на 1 мая 2027. Требуется новый договор; цена My Family 13 200/13 500 по-прежнему расходится.'
    p['accommodation']='Двухместные комнаты с санузлом, взрослые на жилом этаже; заявленный staff/student 1:4 относится к сопровождению, не к учебной группе. Roommate — того же возраста и пола с запросами обеих семей; братьям с разницей три года общая комната не гарантирована. Горные походы могут включать huts/glamping/camping. Родители в жилые корпуса не допускаются.'
    p['family_fit']['matvey']=dict(status='conditional',detail='В 2027 9–10 лет: основной Classic/Mountain/My Family по возрасту подходит, но утренняя Tech & Robotics с 11 пока недоступна. Рассматривать науки/outdoor или другой технический интенсив; язык и сложность уточнить.')
    p['questions']=['Получить договор и полный счёт 2027, исправленную цену My Family и состав конкретного маршрута; набор объявлен с ноября 2026, место не гарантировано.','Для Матвея подтвердить возраст, доступность/язык/часы послеобеденной Robotics и подходящую академию; для уже свободно говорящего EN языковая академия может быть неподходящей по уровню.']
    for title,url in [('Все главные даты и конфликт цены',ROSEY),('Classic: возраст академий и часы',ROSEY+'our-camps/legendary-classic/'),('Mountain: природа и отсутствие обычных уроков EN',ROSEY+'our-camps/my-mountain-adventure/'),('My Family: программа и две/три недели',ROSEY+'our-camps/my-family/'),('FAQ: языки, комнаты, трансфер и депозит',ROSEY+'faq/'),('Связанный договор только SUMMER 2026','https://www.roseycamps.ch/files/financial-conditions.pdf')]:source(p,title,url)
    # Existing seven Rosey cohorts retain dates and IDs; academy choices are not extra camps.
    for v in p['timing']['session_details']:
        if v['label']=='Legendary Classic':v['programme']='Выбор одной утренней академии, 2×75 минут; Tech & Robotics только 11–15. Матвею в 2027 ещё 9–10. Наука/Life Skills 8–12 доступны по возрасту; отдельную послеобеденную Robotics уточнить.'
        elif v['label'].startswith('My Family'):v['programme']='Две первые недели: EN/FR по 2×75 минут ежедневно; третья неделя без языковых уроков. Детский пансион, без проживания родителей.'
        else:v['programme']='Горные задачи, ориентирование, outdoor engineering и возобновляемая энергия; нет традиционных уроков английского. Походные ночёвки.'
    p=profiles['les-elfes'];p['checked']=CHECKED
    p['price']['extras']+=' ЗИМА 2026–27, отдельная форма: обязательные registration CHF150, health/accident CHF120/неделя, helmet rental CHF15/неделя; своё снаряжение и исключение из проката подтвердить. Прокат лыж/сноуборда CHF140/неделя, одежды CHF120, отмена CHF80/неделя; Geneva return CHF190. Эти зимние доплаты не перенесены на лето.'
    p['price']['deposit']+=' ЗИМА: невозвратный CHF1 000, остаток за месяц. §10 формы: со страховкой отмены документированная болезнь/травма/смерть родственника — возврат с удержанием CHF500 за неделю до 24 часов; без неё возврата нет. §2 отдельно описывает отказ в визе с доказательством; сочетание удержания с невозвратным депозитом уточнить. Дневной договор имеет другие суммы/правила.'
    p['accommodation']+=' Зимняя форма прямо описывает четырёхместные комнаты с ensuite. Отдельный зимний дневной вариант начинается с 8 лет, не с общего 6+.'
    winter_extras='Зима 2026–27: registration CHF150 + обязательная medical/accident CHF120/неделя + helmet rental CHF15/неделя по форме; использование своего шлема согласовать. Прокат skis/snowboard CHF140/неделя, одежды CHF120, cancellation CHF80/неделя, halal CHF100/неделя, личная прачечная CHF60/мешок. Geneva return CHF190. Языки EN/FR/ES/DE: 6×~50 минут CHF180 вместо après-ski либо 12×~50 минут CHF340 вместо утреннего катания; это не дополнительные часы лыж. Зимняя робототехника не заявлена.'
    for v in p['timing']['session_details']:
        if v['label']=='Зимний лыжный пансион':
            v['extras']=winter_extras
            v['programme']='Лыжи/сноуборд: уроки утром и guiding после обеда, skipass, основные активности, экскурсии, полный пансион; техника / прокат и языковые опции отдельно. Урок языка заменяет часть катания. Комнаты по четыре с санузлом; летняя робототехника не включена.'
            v['questions']=['Итоговый зимний счёт, стоимость своих/арендованных вещей, группы по уровню, условия возврата и возраст Оскара на дату приезда.']

    source(p,'Зимняя форма 2026–27: обязательные доплаты и отмена',ELF_PDF+'WINTER-REGISTRATION-FORM-DIGITAL-avec-champs.pdf')
    source(p,'Текущий FAQ: основной язык EN, поддержка и доплаты',ELF+'about-us/faq/')
    source(p,'Сезоны и тарифы — расхождение цены и форма',ELF+'dates-and-pricing/')
    p=profiles['tasis'];p['checked']=CHECKED
    p['accommodation']='CDE 7–10 с проживанием либо дневной; Minnows 4–6 только день. FAQ: комнаты по 2–4 человека одного возрастного диапазона, отдельные корпуса мальчиков/девочек; братьям и друзьям совместное размещение не разрешают. Для младшего до 7-летия семье нужно собственное жильё.'
    p['price']['deposit']='FAQ: CHF1 500 невозвратный депозит, остаток до 15 мая; после этого срока полный платёж в течение 7 дней от invoice. До 15 мая tuition может возвращаться за вычетом депозита; после — только документированные чрезвычайные исключения. Условия нового договора подтвердить.'
    p['price']['included']='CDE day: tuition и обед, только будни; boarding: программа, питание и проживание. FAQ добавляет books/laundry и health/accident для non-Swiss boarding; Swiss residents предъявляют свою страховку. Дневным страховка не включена автоматически: своя либо отдельная TASIS для non-Swiss по запросу.'
    source(p,'FAQ: комнаты, братья отдельно, страхование и оплата',TASIS+'admissions/faq')
    source(p,'Полный прайс 2027: дневные/пансионные варианты',TASIS+'dates-and-fees')
    # Real upper-age progression: formats have different inclusions and a common course choice.
    later=fit('later','В 2027 возраст ниже минимального для этой программы. Сохранено как будущая ступень; конкретный допуск/новые сезоны отдельно.')
    dates=[['2027-06-27','2027-07-17'],['2027-07-19','2027-08-08']]
    for level,ages,content in [
        ('msp','11–13','Один основной курс на всю смену, примерно 3–4 часа/день, плюс две спортивные/творческие активности. STEM: планирование/измерения, модели, простые механизмы, электроника и coding; платформа/часы роботов не раскрыты. Альтернативы — Art, EAL, French/Italian, Musical Theater, Creative Writing для native/nearly fluent (работа от руки), Digital Photography с собственной DSLR. Выбор языка не означает одновременно пройти STEM; сертификат международной лиги не заявлен.'),
        ('hsp','14–17','Один курс примерно 4 часа/день: STEM (научный метод, генетика/DNA, биохимия, эксперименты и данные Google Sheets/Tableau), Finance (инвестиции, blockchain/цифровая безопасность, VC), Lean Startup (build–measure–learn, бюджет/маркетинг, питч staff/peers), Academic Writing (эссе и этичное Gen AI), Art/Design, Architecture, Fashion, Photography, Filmmaking, Italian Cooking, EAL/French. Finance/Lean Startup/Writing требуют свой laptop, i Pad недостаточен; Photography свою DSLR. Это выбор альтернативных курсов, не один интенсив по всем направлениям. Внутренний Shark Tank не доказывает финансирование или мировой конкурс.')]:
        for board in [False,True]:
            slug='tasis-'+level+('-board' if board else '-day')
            add(slug,'TASIS Switzerland · '+level.upper()+' · '+('пансион' if board else 'дневной'),'Швейцария','CHE','Via Collina d’Oro 15,6926 Montagnola / Lugano',
                'general,languages,science,coding,art,entrepreneurship' if level=='hsp' else 'general,languages,science,coding,art','boarding' if board else 'day',ages,
                'EAL — прямо immersive English. Native/nearly fluent курс письма на EN; язык самостоятельных STEM/Finance/Startup/Art занятий не установлен. Фильтр EN относится к языковому выбору, не обещает английскую робототехнику.',
                content,'2027: 27 июня – 17 июля / 19 июля – 8 августа, полная трёхнедельная смена. Все прибывают в первый день; день и время конца дневного посещения проверить.',
                price(2027,'CHF9 200 пансион / 3 недели.' if board else 'CHF5 100 дневной / 3 недели.',
                    'Tuition, питание и dorm; по FAQ non-Swiss boarding health/accident, books/laundry. В общем описании пансиона выходные дневные экскурсии включены; дополнительные ночные поездки оплачиваются отдельно.' if board else 'Tuition, обед и большинство активностей; можно оставаться на ужин/вечер. Специальный прайс 2027 прямо исключает weekend day trips, несмотря на старый общий FAQ о семи днях и excursions.',
                    'Дополнительные sport/overnight trips отдельно, свой laptop/DSLR при соответствующем курсе. HSP French: обязательный Colmar trip дополнительно; Architecture: Basel/Vitra trip дополнительно. Перелёт, карманные деньги отдельно. '+('Своя страховка нужна Swiss residents; исключения dental/eye по FAQ.' if board else 'Своя health/accident либо платная TASIS non-Swiss по запросу, автоматически не включена. Уточнить фактические выходные дни day2027.'),
                    'FAQ: CHF1 500 невозвратный депозит, остаток до 15 мая; поздняя запись полный платёж за 7 дней. До 15 мая возможен tuition refund минус депозит; дальнейшие документированные emergency exceptions. Новую применимость подтвердить.'),
                'Dorm rooms2–4 одного возраста; мальчики/девочки отдельно. Братьям/друзьям совместную комнату не разрешают по FAQ.' if board else 'Каждая ночь с семьёй; dorm не включён. Общий FAQ MSP/HSP7days конфликтует с 2027 исключением weekenddaytrips: расписание выходных не назначено автоматически.',
                later,later,'Подробная будущая ступень науки, творчества и предпринимательства. Младшим сейчас нужны CDE/Minnows; известность школы не заменяет выбор уровня и языка конкретного курса.',
                ['Новый договор, одна выбранная академия, язык технических занятий, оборудование, обязательные поездки/спорт и итоговый счёт.','Для day подтвердить реальное расписание выходных 2027 и страховку; не переносить старое включение daytrips.'],
                [src('Возраст и полный выбор курсов',TASIS+'programs/'+level),src('Специальные цены/даты/выходные 2027',TASIS+'dates-and-fees'),src('FAQ: доплаты, комнаты и refund',TASIS+'admissions/faq')],status='published_2027',confirmed=['EN'],sessions=dates)
            P[-1]['language_evidence_role']='language_lessons'
    day_fee='CHF350 Full Day08:30–18:30 / CHF450 Extra Long08:30–21:30; форма 2026–27. Обязательная insurance CHF25/день, helmet rental CHF3/день: CHF378/478 с арендным шлемом до прочих расходов. Afternoon16:00–21:30 CHF299 только на странице, в форме его нет — подтвердить.'
    add('les-elfes-winter-day','Les Elfes International · Winter Day Camp','Швейцария','CHE','Verbier, Switzerland',
        'general,languages,sport','day','8–17 на зимней дневной странице; общий минимум пансиона 6+ не применён.','Основной EN по FAQ. Страница предлагает EN/FR/ES/DE уроки, но day-форма 2026–27 перечисляет только EN/FR; доступ ES/DE подтвердить.',
        'Лыжи/сноуборд до 6 часов, skipass4Vallées, обед/snack, après-ski; extra long добавляет ужин/вечер. Фактическое расписание катания 09–12 и 13–15:30 —5,5 часа; не шесть гарантированных часов. Языки вместо après-ski только Mon/Tue/Thu: в форме~50 минут, CHF60normal/85intensive за период; дневная страница говорит 2 часа — формат расходится. Субботы нет; робототехника не заявлена.',
        'WINTER DAY2026–2027 подтверждён формой; сезон с начала декабря до конца апреля, Sunday–Friday. Индивидуальные даты не опубликованы: непрерывную смену и 19 недель пансиона в дневной календарь не переносим.',
        price(2027,day_fee,'Основная дневная программа, skipass/обед; extra long ужин/вечер. Жильё семьи отдельно.',
            'Cancellation CHF40/день отдельно, Wednesdayexcursion CHF50, hotel dropoff CHF50oneway, оборудование/одежда и семейный отель отдельно. При позднем уходе Full Day после 18:30 добавят CHF100. Форма требует rentalhelmet; согласовать свой.',
            'Daydeposit CHF200 невозвратный, остаток за месяц. §10 без cancelinsurance: возврат минусдепозит до 60 дней; до 30 дней только medicalproof; с 29 днейнет. Со страховкой доказанная illness/death/accident до 24 часов — минусдепозит. §2 иначе описывает общий 30-дневный порог: согласовать расхождение письменно.'),
        'Ребёнок ночует с родителями; этот зимний day8+ не равен overnight6+.',fit('conditional','9–10 соответствует 8–17; проверить реальную дату, уровень, язык ski instructor и полный счёт.'),fit('later','6–7 ниже дневного минимума 8. Более ранний допуск общего пансиона не открывает этот daycamp.'),
        'Семейная зимняя база для дневной активности Матвея; обязательные доплаты и ограничение Оскара показаны прямо.',
        ['Конкретные дни и доступность afternoon, EN ski instructor, ES/DE языковых уроков, собственный шлем и страховые/отменные условия.'],
        [src('Дневной зимний возраст, часы, активности',ELF+'winter-day-camp/'),src('Форма и отдельный договор DAY2026–2027',ELF_PDF+'WINTER-DAY-CAMP-26-27-REG-FORM-DIGITAL-2026-2027.pdf'),src('Основной язык лагеря',ELF+'about-us/faq/')],status='partial_2026_27',confirmed=['EN'])
    P[-1]['price']['season']='winter2026–2027';P[-1]['language_evidence_role']='camp_life'
    add('rosey-excellence-arctic','Le Rosey · Excellence Alps & Arctic','Швейцария','CHE','Swiss Alps → Northwest Svalbard, Norway',
        'general,science,sport','boarding','13–16 на профильной странице/брошюре; один блок homepage12–16 — конфликт, исключение в 12 не обещаем.',
        'EN/FR лагерная среда Le Rosey по FAQ; язык специалистов на маршруте отдельно подтвердить.',
        'Максимум 10 подростков: Alpine hiking/climbing, glaciers/viaferrata, ночёвки huts/camping, затем перелёт из Geneva на яхту у NWcoast Svalbard. Навигация картами/электроникой, история/природа островов, командная работа. Нужна физическая готовность к сложным горам и плаванию; это outdoor/navigation, не робототехническая лига.',
        '4–19 июля 2027. На странице «2weeks», но окно включает 16 календарныхдней; не сокращено автоматически.',
        price(2027,'CHF16 300 за объявленную программу 2027.', 'Профиль говорит депозит включён. Договор 2026 описывает жильё/питание/материалы/перелёт дояхты и обратно Geneva, но его состав не гарантирует пакет 2027.',
            'Международный домашний перелёт, личные расходы, страхование за пределамиШвейцарии и маршрутный счёт 2027 подтвердить. Норвегия/Svalbard — реальная часть маршрута, не один школьный кампус.',
            'FAQ депозит CHF1000; связан SUMMER2026contract. Майский cutoff2026 не перенесён на 2027; требуется новый договор.'),
        'Горные хижины/походные ночёвки и яхта; тип кают/санузлов и сопровождение конкретного маршрута подтвердить.',later,later,
        'Будущий небольшой маршрут автономности и навигации. Не текущая поездка братьев и не обещание международной победы.',
        ['Точный minimum13/исключение 12, физическая подготовка, каюты, язык, текущий маршрут, перелёты и страховка 2027.'],
        [src('Конкретный маршрут, fitness, 13–16, даты/цена 2027',ROSEY+'our-camps/excellence-camp/'),src('Конфликт 12–16 в дублированном блоке',ROSEY),src('Контракт пока 2026','https://www.roseycamps.ch/files/financial-conditions.pdf')],status='partial_2027',confirmed=['EN','FR'],sessions=[['2027-07-04','2027-07-19']])
    P[-1]['language_evidence_role']='camp_life'
    add('rosey-chyulu-kenya','Le Rosey · Chyulu Wilderness Camp','Кения','KEN','Chyulu Hills / Tsavo, Kenya; международный маршрут через Nairobi',
        'general,science,sport','boarding','13–17; максимум 30 участников.',
        'Язык инструктажей Maasai guides/science прямо не установлен; общий EN/FR FAQ швейцарских лагерей автоматически наКению не перенесён.',
        'Adventure/conservation/volunteering: biodiversity с ботаником, safari/walking, community activities, conservation seminars, tree planting/sustainable farming. Нет традиционных ежедневных classroom lessons; глубина science зависит от программы. Недатированный sample PDF: forest hike/photography, Tsavo, conservation trust/Maasai village, lion tracking/human-wildlife conflict, trees/farm/school, reflection. Он рассчитан на семь дней, тогда как даты 2027 включают восемь: не считаем sample точным расписанием новой смены. Carbon-negative/ecolodge — собственное заявление оператора, независимая сертификация не проверена.',
        '17–24 /23–30 июля 2027. Оба опубликованных интервала включают 8 календарныхдней и пересекаются 23–24 июля; «1week» не исправляет реальные даты.',
        price(2027,'CHF5 500 в блоке 2027 и at-a-glance; FAQ той же страницы CHF5 300 — конфликт, нужен новый invoice.',
            'Блок 2027: проживание/полное питание/основные активности и воздушный Nairobi↔camptransfer. Домашний перелёт не включён.',
            'Дом↔Nairobi, промежуточные гостиницы, маршруты групповых рейсов, страхование/въездные расходы подтвердить. Старое FAQ/e TA описание не является проверкой действующих миграционных / медицинских требований.',
            'CHF1000 невозвратный/непереносимый депозит в FAQ; ссылка contract SUMMER2026, текущие условия 2027 не установлены.'),
        'Tentedlodge2–4 с ensuite, отдельные комнаты мальчиков/девочек; родителей с детьми не принимают по FAQ. ЭтоКения, не швейцарская площадка.',later,later,
        'Будущая экологическая/научная экспедиция отдельно от техники; страна фактического проживания и расхождения сохранены.',
        ['Полная смена 2027, пересечение двухгрупп, итог 5500/5300, язык, маршруты/страхование и актуальный договор.'],
        [src('Полная программа/FAQ и цена-конфликт',ROSEY+'our-camps/chyulu-camp/'),src('Общие даты/цены 2027','https://www.roseycamps.ch/files/at-a-glance.pdf'),src('Пример семидневного плана без нового года','https://www.roseycamps.ch/files/chyulu-sample-programme-camps.pdf'),src('Camp codes: правила проживания/самостоятельности','https://www.roseycamps.ch/files/chyulu-codes.pdf'),src('Договор SUMMER2026','https://www.roseycamps.ch/files/financial-conditions.pdf')],status='partial_2027',sessions=[['2027-07-17','2027-07-24'],['2027-07-23','2027-07-30']])
    # Archived summer programmes are reference dossiers, never made-up future cohorts.
    past='Опубликован только архив 2026; новый набор/даты/цены 2027 не подтверждены. В будущий календарь прошлые даты не перенесены.'
    place='ICS Paris,23 rue de Cronstadt,75015Paris'
    common_questions=['Новый сезон, внешний приём, группы/уровень, подтверждённый язык и полный счёт/отмена 2027.']
    add('ics-paris-world-summer','ICS Paris / ALCNY · Around the World','Франция','FRA',place,'general,languages,science,art,sport','day','3–12; отдельные группы по возрасту.',
        'Прямо bilingual EN/FR; сайт также говорит Americanimmersion, но полностью однородный английский поток не установлен.',
        'Творческие культуры/истории, scienceexperiments, art, filmmaking, outdoor и teamgames. 09–16, продление до 18; это 7 часов лагерного дня, не 7 часовробототехники.',
        '29 июня–3 июля /6–10 /13–17 июля 2026. '+past,
        price(2026,'EUR595/week135/day standard;695/week155/day extended2026.','Дневные занятия, сопровождение.','Lunchbox свой; семейный отель/перелёт отдельно.','Правила возврата/страховки и договор 2027 не прочитаны в этой карточке.'),
        'Дневной школьный кампус; пансион не заявлен.',fit('conditional','Возраст 3–12 подходит; новая смена и внешний приём ещё нужны.'),fit('conditional','Возраст 3–12 подходит; уровень/группа и новый сезон нужны.'),
        'Общий билингвальный городской вариант для обоих, с science/art; не технический intensive и не опубликованное лето 2027.',common_questions,[src('Полная программа/цены/билингвальность',ICS)],status='published_2026',confirmed=['EN','FR'])
    P[-1]['language_evidence_role']='bilingual'
    add('ics-paris-back-school','ICS Paris / ALCNY · Back to School Prep & Progress','Франция','FRA',place,'general,languages,science,art,sport','day','3–16; primary6–10, middle11–16.',
        'Профиль и собственный PDF: English /100%English; отдельно ESL/FSLsupport.',
        '09–12 reading/writing/grammar/vocabulary/communication поуровню; 12–16 sport/arts/STEMchallenges/групповые проекты; 16–18 optionalquietcare. Middle11–16 может только 09–12. Плакат предназначен studentsentering/returning ICS: внешний приём братьев не гарантирован.',
        '24–28 августа 2026. '+past,
        price(2026,'EUR595/week135/day; extended695/week155/day. Middlehalfdays465/week120/day: один блок HTML пишет£465, остальные/PDF€465 — расхождение сохранено.',
            'Дневной курс и supervisedlunchbreak, не сам обед.','Обед EUR9/day либо свой nut-freelunch; проживание отдельно.','Условия нового внешнего набора/возврата 2027 не установлены.'),
        'Дневная программа, без ночёвок.',fit('conditional','В 2027 9–10 входит primary6–10, но 2027 и внешний приём не установлены.'),fit('conditional','В 2027 6–7 входит primary6–10, но 2027 и внешний приём не установлены.'),
        'Английский и общие STEM проекты передшколой; STEM фото 2025 не гарантируют курс роботов 2027.',common_questions,[src('Часы, группы, обед и currencyconflict',ICS),src('Полныйплакат 2026:100%English, приём/цены','https://resources.finalsite.net/images/v1781770428/icsparisfr/rny5pqyyjbfg0uffmyhq/alcnyicscampposter2026_3.pdf')],status='published_2026',confirmed=['EN'])
    grade=fit('unknown','Требуются фактические Grades6–12. Классы детей неизвестны; год рождения не устанавливает класс. Это будущая школьная ступень, допусксейчас не подтверждён.')
    for slug,name,cost,programme,extra_sources in [
        ('ics-paris-ai-startup','ICS Paris · AI Startup Sprint / Harvard Women in Computer Science',730,'Дизайнмышление и Gen AI для startupconcept/productdevelopment за 5 дней, Harvardstudentmentors. PDF: Certificateof Participation от Harvard Womenin Computer Science. Это студенческая организация/сертификатучастия, не Harvard Universitydegree/зачисление и не победа международной лиги.',[src('Собственный плакат:организация, grade, cert, fee','https://resources.finalsite.net/images/v1777969490/icsparisfr/ja8azmnzktlftmytqnm2/AIStartupSprint.pdf')]),
        ('ics-paris-yira-leaders','ICS Paris · YIRA Young Global Leaders',630,'Полный YIRA PDF: дипломатия/публичнаяречь/debate/MUN, policywriting, Global Impact Challenge, crisisnegotiation, finalpresentations. 09–16 с breaks/lunch, пятый день schedule до 15. Certificate от Yale International Relations Association, прямо student-runorganization. Это не университетский Yale Young Global Scholars; наставники Yale Students, не автоматически преподаватели/официальные admissionguarantees. Deadline PDF20 апреля против HTML15 июня 2026 — конфликт.',[src('Полный YIRA PDF со student-run статусом, днями/сертификатом','https://drive.google.com/file/d/1rK7faz6pWZRaCs0IW0LDIrSiz6ENOO5u/view')])]:
        add(slug,name,'Франция','FRA',place,'ai,entrepreneurship' if 'ai-startup' in slug else 'general,entrepreneurship','day','Grades6–12, openforall на странице; фактический класснужен.',
            'Язык преподавания явно не указан; английский рекламный текст не доказывает английскую группу.',programme,
            '29 июня–3 июля 2026,5 дней. '+past,
            price(2026,'EUR'+str(cost)+' за программу 2026.','Курс/сертификат по описанию; оборудование/питание не раскрыты.','Полный счёт, meals, семейное жильё/перелёт и страховка отдельно проверить.','Прошлая регистрациязакрыта; новый contract/refund не установлен.'),
            'Занятия в Paris, не американский университетский пансион.',grade,grade,
            'Будущий навык предпринимательства или международной коммуникации; масштаб награды/организатор описаны точно.',common_questions,[src('Школьный хозяин, допуск/цена 2026',ICS)]+extra_sources,status='published_2026')
    # New, genuinely upcoming October programmes. Campuses are variants, not four operators.
    venues=[('lennen','Lennen · Paris7e'),('concordia','Concordia · Paris16e'),('chardin','École Bilingue Chardin · Paris'),('asp','AmericanSchoolofParis ·41ruePasteur,92210Saint-Cloud')]
    variants=[]
    for key,venue in venues:
        for n,(a,b) in enumerate([('2026-10-19','2026-10-23'),('2026-10-26','2026-10-30')],1):
            if key=='asp' and n==2:continue
            variants.append(dict(start=a,end=b,variant_key=key+'-week'+str(n),label=('HogwartsAdventures' if n==1 else 'HalloweenShadow')+' · '+venue,place=venue,price='EUR695standard /720extended за неделю; lunch+EUR9/day',source=ALC,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR']))
    add('alcny-paris-autumn-junior','ALCNY · Paris Autumn / Harry Potter','Франция','FRA','LennenParis7e /ConcordiaParis16e /ChardinParis /ASP Saint-Cloud',
        'general,languages,science,art,sport','day','3–9; группы 3–5,6–7,8–9. Общий диапазон покрывает обоих в 2026.',
        'Оператор прямо предлагает full Englishimmersion длясвоих camp; язык сложных instructions/особые запросы подтвердить.',
        'Две разные недели: science/potions, рукоделие, drama/storytelling, командные/спортивные задачи. 3–5 сенсорная игра; 6–7 эксперименты/миссии; 8–9 сложнее acting/filmmaking/performance/groupfinalproject. Присутствие 09–16, продление 16–18 для quietactivities. Daily09:30–11:30 и 13–15:30 основные activities с lunch/recess; не 7 часов техники.',
        '19–23 /26–30 октября 2026: Lennen, Concordia, Chardin обе недели; American Schoolof Paris только 19–23. Это ближайший autumn, не открытый summer2027.',
        price(2026,'EUR695/week155/day standard09–16;720/week165/day extended09–18.',
            'Дневные активности, morning/afternoonsnacks; extended сопровождение.','Lunch EUR9/day separately либо свой nut-freelunch. Семейный отель/перелёт/страховка отдельно; итог с детьми/площадкой уточнить.','Депозит/отмена/внешняя internationaleligibility на прочитанной странице не раскрыты.'),
        'Дневные школьные площадки; ночёвки ссемьёй. Адрес 7avenue Villars в footer — адресоператора, не доказательство каждой площадки.',
        fit('conditional','В октябре 2026 8–9: верхняя группа подходит. Новая бронь/место, внешний приём/язык и площадка ещё требуют подтверждения.'),fit('conditional','В октябре 2026 5–6: входит 3–9; точный birthday решает 3–5 или 6–7. Нельзя назначить 6–7 бездаты.'),
        'Ближайшее английское общее приключение дляобоих; четыре площадки не считаются четырьмя независимыми мировыми лагерями.',
        ['Конкретная площадка/адрес, возрастная группа по birthday, места для внешних детей, полный счёт и cancelpolicy.'],[src('Полная программа/реальные площадки/даты/цены',ALC)],status='published_2026_27',confirmed=['EN'],sessions=[[v['start'],v['end']] for v in variants])
    P[-1]['timing'].update(variant_keyed=True,session_details=variants)
    teens=[]
    for key,label,venue,a,b in [
        ('film-lennen','Filmmaking','Lennen ·Paris7e','2026-10-19','2026-10-23'),('style-asp','Style /Hollywood Red Carpet — названия блоков расходятся','ASP ·Saint-Cloud','2026-10-19','2026-10-23'),('broadway-concordia','BroadwayPerformance','Concordia ·Paris16e','2026-10-26','2026-10-30'),('fashion-lennen','Fashion/Design /Hollywood — альтернативу уточнить','Lennen ·Paris7e','2026-10-26','2026-10-30')]:
        teens.append(dict(start=a,end=b,variant_key=key,label=label,place=venue,price='Точный подростковый тариф не установлен; младшие 695/720 не перенесены.',source=ALC,date_scope='day_camp_window',attendance_weekdays=['MO','TU','WE','TH','FR']))
    add('alcny-paris-autumn-teens','ALCNY · Teens Master Camps / media & applied arts','Франция','FRA','LennenParis7e /ConcordiaParis16e /ASP Saint-Cloud',
        'general,languages,art,entrepreneurship','day','10–16, конкретные adolescentgroups.',
        'Общий сайтоператора: full Englishimmersion. Точный уровень и язык выбранного media модуля подтвердить.',
        'Filmmaking: idea/script/storyboard/acting/directing/camera/editing и screening. Style/Fashion: textiles/upcycling/handsewing/visualidentity/show. Broadway: voice/improvisation/ensemble/finalshow. Блоки Style/Hollywood и Fashion/Hollywood повторяются на странице: не считаемих шестью гарантированно независимыми лагерями; одна venue/week сальтернативами требует уточнения.',
        '19–23 октября 2026 Lennen Filmmaking и ASPstyle/media; 26–30 Concordia Broadway и Lennenfashion/media. Новый 2027 не объявлен.',
        price(2026,'Точный подростковый тариф не раскрыт впрочитанном блоке. Младшая программа 695/720 не приписана Teens.',
            'Недельный творческий проект; оборудование/food уточнить.','Реальные часы, lunch, gear исемейный отель отдельно.','Условия отмены/депозита неизвестны.'),
        'Дневные venues без пансиона.',fit('later','В октябре 2026 8–9, младше 10. В 2027 после 10-летия может подойти, но новая смена не объявлена.'),fit('later','В 2026 5–6 и 2027 6–7, младше 10.'),
        'Будущий творческий трек сготовым film/performance, отдельно отробототехнической подготовки.',common_questions,[src('Полный подростковый curriculum и venue/week',ALC)],status='published_2026_27',confirmed=['EN'],sessions=[[v['start'],v['end']] for v in teens])
    P[-1]['timing'].update(variant_keyed=True,session_details=teens)
    add('asp-paris-holiday-english','American School of Paris · Holiday English','Франция','FRA','41ruePasteur,92210Saint-Cloud',
        'general,languages,art,sport','day','K4–K5 /Grades1–5 /Grades6–12; фактический класс установить.',
        'Полная Englishimmersion прямо заявлена; open ASP/externalstudents и все языковыеуровни.',
        'Primary09:30–16:00 языковыеутра и afternoonarts/outdoor/culturalprojects в Possibility/Discovery Labs, auditorium/music/artrooms. Uppergroup Englishacademic/general/publicspeaking; springmorningintensive09:30–13:00. Лаборатория сама по себе не доказывает ежедневный robotics курс.',
        'На holidaypage только 21–25 окт 2024 /24–28 фев 2025 /14–18 апр 2025. Новые 2026–27camp даты не установлены, несмотря на copyright2026. Предстоящая ALCNYat ASP19–23 окт 2026 — отдельная programme, не автоматически эти старые ASP курсы.',
        price(2025,'Архив 2024–25: primary EUR725 firstchild/695second+, secondary610/580; lunch EUR45/week. Тариф 2026–27 не установлен.',
            'Указанный дневной language/activityprogramme.','Lunchoptional либо свой, семейное проживание/дорога отдельно.','Архив: fullcardpayment; cancel>30 дней удержание 25%, ≤30 днейполнаястоимостьвключая lunch; seriousmedical/familyproof admin75. Новый договор проверить.'),
        'Дневной школьный кампус; пансион не заявлен.',fit('unknown','Допуск по K/Grades; точный класс и новый сезон неизвестны.'),fit('unknown','Допуск по K/Grades; год рождения класс не доказывает.'),
        'Проверенный английскийвнешний формат, но старыйпрайс икохорты требуют обновления; годовойкурс не подменяетканикулы.',common_questions,[src('Полная holidaypage с 2024–25pricing/условиями','https://www.asparis.org/english-and-holiday-programs/holiday-camps')],confirmed=['EN'])
    for slug,name,ages,themes,lang,confirmed,role,content,mat,osc in [
        ('agora-granada-summer-fun','SummerFun','5–14','general,languages,sport','Прямо Englishlearning/reinforcement; язык всех outdoor инструктажей не установлен.',['EN'],'language_lessons','Englishreinforcement через игры/плавание и outdoorhiking, mountainbike, archery, climbingwall.',fit('conditional','9–10 в 5–14; дата/внешняя запись/уровеньнужны.'),fit('conditional','6–7 в 5–14; расписание/язык outdoor/новый сезоннужны.')),
        ('agora-granada-robotics-vr','Robotics & Virtual Reality','9–14','robotics,coding,sport','Язык Robotics прямо не указан; English страница/общая multilingual школа не подтверждают EN занятия.',[],None,'ICT/robotics и virtualreality плюс outdoorsport/pool. Платформы, конечныйпроект иобъёмкода не раскрыты.',fit('conditional','В 2027 9–10 подходит 9–14; курс/даты/язык/внешний приём неизвестны.'),fit('later','6–7 младше 9; общий Summer Fun не открывает Robotics.')),
        ('agora-granada-creative-immersion','Creative Immersion','6–14','general,languages,art,sport','Прямо английскаячасть ииспанскаячасть, bilingual.',['EN','ES'],'bilingual','Двухъязычнаяпрограмма со storytelling, workshops, sport/pool; техническая специализация не заявлена.',fit('conditional','9–10 в 6–14; год/внешний допуск/пакеттребуютуточнения.'),fit('conditional','6–7 в 6–14 на 2027; год смены иуровень неподтверждены.'))]:
        add(slug,'Agora Granada College · '+name,'Испания','ESP','UrbanizaciónLlanosdeSilva,Atarfe,Granada',themes,'day',ages,lang,content,
            'Страницабез года/текущейценысмен; Creative Immersion23–26 июнябез года. Copyright2025 не задаётгоднабору; дат 2026–27 вкалендарене создано.',
            price(None,'Ценаиактуальныйгодне опубликованы в прочитанном описании.','Основная theme программа, составоборудования/food не установлен.','Дневныечасы/gear/доставка/отельсемьинеизвестны.','Brochure кнопкаведётна inquiry, не прочитанный PDF; externaladmission/refund не установлены.'),
            'Пансионнапрограмме не заявлен; меню Boardingin Andorra не доказываетночёвкив Granada.',mat,osc,
            'Конкретный theme/age вариант; полная смета/даты не доказаны. Независимый мировой рейтингнеприписан.',common_questions,[src('Полнаястраница всехтем/возрастов/языков',GRANADA)],confirmed=confirmed)
        if role:P[-1]['language_evidence_role']=role
    add('robbo-barcelona-summer','ROBBO Club Barcelona · Summer engineering','Испания','ESP','Via Laietana45,6-2,08003Barcelona; новый сезон venue подтвердить',
        'robotics,coding,ai,science','day','6–8 /9–13, группы отдельно.',
        'Язык занятий явнонеуказан; EN/ES/Catalan/RU текстсайта не доказывает преподавание.',
        'Scratch, сенсоры/цепи, ROBBOrobot, TinkerCAD/3D. Темы недель: Mars; Smart City; electronics; voice/gesture AI; две creativeengineering. Компьютер/робот каждому на занятиях, до 8 детей на учителя; нет обещания подарить технику.',
        'Архив 22 июня–31 июля 2026,6 недель, 09–13. Первая неделя 4 дня:24 июня закрыто; страница ошибочно пишет Tuesday(фактически Wednesday). Дат 2027 нет.',
        price(2026,'EUR150/4 дня; 185/5 дней; 4 недели 634/667.','Занятия, вода/фрукты.','Свой snack, care с 08:30 по запросу, жильё семьи.','Deposit50; sibling5%/earlybird10 не комбинируются, прошлый cutoff25 мая 2026 не перенесён. Terms May2026:100%refund при уведомлении≥48 часов; позже/после старта нет, перенос только подтверждённый. Новый contract проверить.'),
        'День, без пансиона.',fit('conditional','Возраст 9–10 встаршейгруппе; новыйязык/сезоннужны.'),fit('conditional','6–7 вмладшейгруппе; новыйязык/сезоннужны.'),
        'Конкретныетехническиепроекты; независимый top-рейтингне установлен.',common_questions,
        [src('Первичная web-tool копия 2026; direct403','https://robboclub.es/barcelona/campverano26'),src('Прочитанныеусловия May2026','https://robboclub.es/barcelona/es/terms')],status='published_2026')
    prose={
        'alcny-paris-autumn-junior':dict(
            programme='Две разные недели: научные опыты, рукоделие, театр и истории, командные и спортивные задачи. 3–5 лет: сенсорная игра; 6–7: эксперименты и миссии; 8–9: более сложные актёрские, кино- и групповые проекты. День 09–16, продление 16–18 для свободных занятий под присмотром. Основные активности 09:30–11:30 и 13–15:30 с перерывами: это не семь часов техники.',
            language='Оператор прямо заявляет полное погружение в английский для своих лагерей. Уровень группы и язык сложных инструктажей подтвердить.',
            editorial_reason='Ближайший английский общий лагерь для обоих. Четыре площадки являются вариантами одной программы, а не четырьмя независимыми мировыми лагерями.'),
        'alcny-paris-autumn-teens':dict(
            programme='Выбор медиа/искусства: кино от сценария и раскадровки до съёмки, монтажа и показа; мода от тканей, ручного шитья и повторного использования вещей до образа и презентации; театр с голосом, импровизацией и финальным спектаклем. Блоки Style/Hollywood и Fashion/Hollywood повторяются: точную альтернативу на каждой площадке уточнить. Не считаем их шестью независимыми лагерями.',
            editorial_reason='Будущий творческий трек с завершённым фильмом или выступлением; конкретная техника робототехники не заявлена.'),
        'robbo-barcelona-summer':dict(
            programme='Scratch, сенсоры и цепи, робот ROBBO, TinkerCAD/3D. Недельные темы: Марс, умный город, электроника, голос/жесты и ИИ, два творческих инженерных проекта. Компьютер и робот каждому на занятиях, до 8 детей на учителя; техника домой не обещана.',
            accommodation='Дневной курс без пансиона.',
            language='Язык занятий явно не указан. EN/ES/Catalan/RU на сайте не доказывают язык преподавания.',
            editorial_reason='Конкретное содержание технических проектов; независимый мировой рейтинг не установлен.'),
        'ics-paris-yira-leaders':dict(
            programme='Полный YIRA PDF: дипломатия, публичная речь, дебаты/MUN, написание policy, Global Impact Challenge, переговоры и финальные презентации. День 09–16 с обедом/перерывами; расписание пятницы до 15. Сертификат от Yale International Relations Association, прямо студенческой организации. Это отдельная программа YIRA, не Yale Young Global Scholars. Наставники — студенты Yale; гарантия поступления и университетская степень не заявлены. Дедлайн 20 апреля в PDF расходится с 15 июня 2026 на ICS.'),
        'ics-paris-ai-startup':dict(
            programme='Дизайн-мышление, Gen AI и разработка концепции стартапа за пять дней с наставниками-студентами Harvard. Плакат обещает сертификат участия Harvard Women in Computer Science. Он не является университетской степенью, поступлением в Harvard или победой международной лиги.'),
        'agora-granada-summer-fun':dict(programme='Практика английского через игровые занятия, плавание, походы, горный велосипед, стрельбу из лука и скалодром.'),
        'agora-granada-robotics-vr':dict(programme='ICT, робототехника и виртуальная реальность, дополненные спортом и бассейном. Платформы, финальный проект, язык и часы программирования не раскрыты.'),
        'agora-granada-creative-immersion':dict(programme='Прямо английская и испанская части программы: истории, мастерские, спорт и бассейн. Самостоятельный интенсив робототехники не заявлен.')
    }
    for q in P[start:]:
        q.update(prose.get(q['slug'],{}))
        if q['slug']=='alcny-paris-autumn-junior':
            q['price']['label']='EUR695/неделя или 155/день 09–16; EUR720/неделя или 165/день 09–18.'
            q['price']['included']='Дневные активности и два перекуса; в продлённом варианте присмотр 16–18.'
            q['price']['extras']='Обед EUR9/день отдельно либо свой без орехов. Семейный отель, перелёт и страховка отдельно. Итоговый счёт подтвердить.'
        if q['slug']=='robbo-barcelona-summer':
            q['price']['deposit']='Депозит EUR50; sibling5% и earlybird EUR10 не совмещаются, срок 25 мая 2026 не перенесён. Условия мая 2026: возврат 100% при письменной отмене минимум за 48 часов; позднее/после старта возврата нет, перенос по согласованию. Новый договор проверить.'
            q['price']['extras']='Свой перекус, присмотр с 08:30 по запросу и жильё семьи отдельно.'
            q['timing']['label']='Архив 22 июня–31 июля 2026: шесть недель 09–13. Первая неделя четыре дня, 24 июня закрыто; сайт ошибочно пишет Tuesday, хотя в 2026 это Wednesday. Дат 2027 нет.'
        if q['slug'].startswith('agora-granada-'):
            q['price']['label']='Цена и актуальный год не опубликованы в прочитанном описании.'
            q['price']['included']='Тематическая программа; оборудование и питание не установлены.'
            q['price']['extras']='Дневные часы, техника, доставка и жильё семьи требуют уточнения.'
            q['price']['deposit']='Кнопка brochure ведёт на запрос, не на прочитанный PDF. Внешний приём и отмена не установлены.'
            q['timing']['label']='Описание без года и дат нового набора. Creative Immersion23–26 июня без года; copyright2025 не устанавливает сезон. Новые смены 2026–27 в календарь не внесены.'
            q['accommodation']='Пансион не заявлен. Пункт меню Boarding in Andorra не доказывает проживание в Granada.'
            q['editorial_reason']='Отдельная тема с установленным возрастом; даты, полная смета и внешний приём ещё неизвестны. Независимый мировой рейтинг не приписан.'
        q['checked']=CHECKED
        for s in q['sources']:s['checked']=CHECKED

def extend_report_v88(report):
    report['shortlist'].extend([
        dict(label='Швейцария · реальная глубина и возраст техники',slugs=['tasis','le-rosey','la-garenne','les-elfes'],reason='Для обоих сравнивать CDE/Minnows, La Garenne и общий Les Elfes. Утренняя Tech & Robotics Le Rosey с 11 лет; Матвею летом 2027 ещё 9–10. У короткой послеобеденной Robotics часы и возраст не раскрыты. Языковая академия и общий пансион не равны тренировке FLL/VEX; важны конкретный проект, язык и сложность.'),
        dict(label='Франция · ближайшая английская осень обоим',slugs=['alcny-paris-autumn-junior','ics-paris-back-school','asp-paris-holiday-english'],reason='ALCNY:19–23/26–30 октября 2026, группы 3–9; площадка ASP только в первую неделю. Это общие творческие/научные английские занятия без пансиона. ICS Back to School2026 и ASP2024–25 остаются справкой о формате, а не открытым новым набором. Подтвердить группу по дню рождения, место, внешний приём и отмену.'),
        dict(label='Испания · двуязычный общий лагерь или техника',slugs=['agora-granada-summer-fun','agora-granada-robotics-vr','agora-granada-creative-immersion','robbo-barcelona-summer'],reason='Конкретное содержание, допуск младших и языковые ограничения описаны в досье. Недатированная программа или архив 2026 не означают открытое лето 2027. В Granada английская/испанская части Creative Immersion прямо подтверждены; этот язык не перенесён на другой Robotics курс.'),
        dict(label='Позже · предпринимательство, дипломатия и автономность',slugs=['tasis-msp-day','tasis-msp-board','tasis-hsp-day','tasis-hsp-board','ics-paris-ai-startup','ics-paris-yira-leaders','rosey-excellence-arctic','rosey-chyulu-kenya','alcny-paris-autumn-teens'],reason='MSP11–13, HSP14–17 и экспедиции 13+ — будущие ступени. ICS Grades6–12 требует реального школьного класса. Сертификат студенческой организации не является университетской степенью или медалью мировой лиги. Выбор строится на навыке, проекте, уровне и языке.')
    ])
    report['gaps'].extend([
        dict(country='Швейцария',iso='CHE',provider='v88 · сезонный договор и обязательные доплаты',detail='Страницы Le Rosey2027 связаны с договором SUMMER2026; My Family CHF13 200/13 500 и Excellence13–16/12–16 расходятся. Зимняя форма Les Elfes требует registration CHF150, medical CHF120/неделю и helmet rental CHF15/неделю. Day8–17 имеет страховку CHF25/день, депозит CHF200 и отдельную отмену. На странице ES/DE и два часа языков, в дневном PDF только EN/FR и периоды~50 минут. Это другие условия, чем пансион 6+ и летняя робототехника.',next_action='Точные счета, договоры, возраст, язык и дневное расписание 2026–27. Доступные места и исправление противоречий пока не подтверждены.',url=ELF+'winter-day-camp/'),
        dict(country='Швейцария / Кения',iso='CHE',provider='v88 · TASIS форматы и международный маршрут Rosey',detail='Прайс TASIS2027 исключает weekend day trips у дневных учеников; общий FAQ ещё описывает семь дней и экскурсии. Day страховка не включается автоматически. В TASIS братья и друзья не живут вместе; Le Rosey требует одинакового возраста и пола для roommate. Chyulu находится в Кении, 13–17: CHF5 500 в блоке 2027/CHF5 300 в FAQ, периоды 17–24 и 23–30 июля пересекаются. Швейцарские EN/FR не перенесены на занятия в Кении.',next_action='Выходные day, язык выбранного курса, оборудование, комнаты, договор и маршрут 2027. Остальные сезоны и страны продолжают проверяться.',url=TASIS+'dates-and-fees'),
        dict(country='Франция',iso='FRA',provider='v88 · осенние смены и статус академических брендов',detail='ALCNY публикует ближайшую осень 2026:3–9 и Teens10–16. Повторяющиеся названия media не доказывают шесть независимых лагерей; подростковый тариф не взят у младших. YIRA: дедлайн 20 апреля в PDF против 15 июня 2026 на ICS, Grades6–12 и сертификат студенческой организации. Связанный HPAIR PDF показывает другую школу JBCN и 3/5 дней: не принят как точный план Paris2026–27. Старый ALCNY /next-camp возвращает 404, /next-camp-2026 работает. ASP holiday2024–25 не перенесён на 2027.',next_action='Классы, внешний приём, места, площадки, темы, подростковые цены и английский технических занятий. Проверять новые зиму/лето 2027.',url=ALC),
        dict(country='Испания / все приоритетные регионы',iso='ESP',provider='v88 · недатированные темы и незавершённое покрытие',detail='Agora Granada Creative23–26 июня без года/цен; Robotics9–14 без явного EN. Brochure ведёт на запрос, не на PDF. У ROBBO есть первичное web-чтение при прямом 403; ошибка дня недели 24 июня сохранена, язык не установлен. Швейцария, Франция, Испания, Европа, Тайвань, Сингапур, Корея, Япония, США, Канада, Коста-Рика, Мексика, Латинская Америка и весь мир 2026–27 остаются в активном плане. Ни одна страна не объявлена полностью проверенной.',next_action='Продолжать официальные программы, даты, счета, язык, day/boarding и классы. Рекламные заявления не заменяют независимый рейтинг.',url=GRANADA)
    ])
