"""Official North American intake, boarding costs and actual workshop gates."""
def add_northamerica_intake(add, src, fit, profiles):
    def put(*a, **k):
        add(*a, **k)
        p=profiles[-1];p['checked']='2026-10-05'
        for s in p['sources']:s['checked']=p['checked']
        return p
    def fee(year,label,included,extras,deposit,season=None):
        d=dict(year=year,label=label,included=included,extras=extras,deposit=deposit)
        if season:d['season']=season
        return d
    def dated(p,rows):
        p['timing']['session_details']=rows
        p['timing']['sessions']=[[r['start'],r['end']] for r in rows]
    def row(p,s,e,label,price,url,**kw):
        return dict(start=s,end=e,label=label,price=price,source=url,place=p['place'],formats=p['formats'],date_scope='camp_session',**kw)

    cody='https://campcody.com/dates-tuition/'
    p=put('cody-general','Camp Cody · общий пансион','США','USA','Freedom, New Hampshire · 9 Cody Road, NH 03836',
        'general,sport,art,science,languages','boarding','7–15: Pioneers 7–9, Juniors 10–11, Inters 12–13, Seniors 14–15; Leadership 16–17 — отдельная ступень',
        'ESL-страница прямо описывает английское погружение лагеря. EN — лагерная среда; дополнительные ESL-уроки оплачиваются отдельно. У ESL преподавателей названы ES и RU среди языков поддержки, но это не испанская/русская смена и не гарантия конкретного сотрудника 2027.',
        'Спорт, озеро, outdoor, искусство, дерево/металл, научные эксперименты и выбор интересов. Pioneers выбирают две активности в день, получают дополнительную бытовую поддержку Camp Moms. Science — опция общего лагеря; подтверждённого курса robotics/AI нет. Личные игровые/электронные устройства запрещены.',
        '2027: четыре двухнедельных и три четырёхнедельных заезда с 20 июня по 14 августа. Возрастные группы и наличие мест подтверждаются отдельно. Текст формы Request Availability всё ещё называет Summer 2026 — он не отменяет явные таблицы 2027 и не доказывает свободные места.',
        fee(2027,'$5 750 / 2 недели; $10 300 / 4 недели. Символ $ на американском сайте; валюту окончательного счёта подтвердить.',
            'Основная пансионная программа; weekly laundry, обычные активности и поездки по описанию term fee. Полный состав питания/страхования закрепить в договоре.',
            'ESL/математика/чтение $800 / 2 недели, $1 600 / 4. Equestrian 675/1 350; tennis и golf 565/1 130 каждый; scuba 455/910; crew 325/650. Round trip: NY/CT 535, Boston Logan для unaccompanied 430, Newton MA 295. Карта +3%. International package (бельё/поездки) указан без цены; перелёты отдельно.',
            '$750 deposit; FAQ также называет $750 Winter Payment. Зачёт этих платежей в tuition и их сроки явно не установлен — не прибавлять их автоматически и не обещать итог. FAQ: оба возвращаются до 31 января; tuition до 1 мая минус $1 500; отмена после 31 января также $300 admin. Год/договор и правила после 1 мая уточнить.'),
        'Cabin около 7 детей и 3 вожатых, электричество, собственный санузел. Возрастные комнаты; совместная комната братьев разного возраста не гарантирована.',
        fit('candidate','В 2027 Матвею 9–10: Pioneers или Juniors по дате рождения. Подходит основной программе; не робототехнический интенсив.'),
        fit('conditional','Только после исполнения 7 лет к заезду; ребёнок 2020 года летом 2027 может ещё быть шестилетним.'),
        'Кандидат на английский общий отдых и самостоятельность, с понятным младшим подразделением. Техническую подготовку планировать отдельно.',
        ['Подтвердить возраст на приезд, внешнее зачисление, комнату, страхование, international package, зачёт deposit/Winter Payment и полный invoice.'],
        [src('Таблицы 2027, все доплаты и отмена',cody),src('Младшая группа 7–9','https://campcody.com/future-families/our-programs/pioneers-ages-7-9/'),src('EN immersion и ES/RU поддержка ESL','https://campcody.com/future-families/activities/academic-offerings/esl-tutoring/'),src('Комнаты и правило устройств','https://campcody.com/future-families/bunk-life/'),src('Реальные electives; science не robotics','https://campcody.com/future-families/activities/')],
        status='published_2027',priority=['general','boarding'],confirmed=['EN'])
    p['language_evidence_role']='camp_life'
    dated(p,[row(p,s,e,f'{n} недели · общий пансион',f'${v:,} базовый tuition',cody) for s,e,n,v in [
        ('2027-06-20','2027-07-03',2,5750),('2027-07-04','2027-07-17',2,5750),('2027-07-18','2027-07-31',2,5750),('2027-08-01','2027-08-14',2,5750),
        ('2027-06-20','2027-07-17',4,10300),('2027-07-04','2027-07-31',4,10300),('2027-07-18','2027-08-14',4,10300)]])

    birch='https://campbirchhill.com/dates-rates-2/'
    p=put('birch-hill','Camp Birch Hill · общий пансион','США','USA','New Durham, New Hampshire · 333C Birch Hill Road, NH 03855',
        'general,sport,art','boarding','6–16 по About; комнаты по возрасту',
        'Международные дети, включая Испанию/Францию, прямо подтверждены. Язык ежедневного обучения и EN support отдельно не назван: английский сайт не считается доказательством EN instruction.',
        'Самостоятельный выбор из спортивных, водных, творческих и outdoor занятий, театр, музыка, фотография и nature study. Свыше 50 electives — заявление оператора; robotics/AI в прочитанном перечне не заявлены.',
        '2027: три смены по 2 недели, две по 4 и одна на 6 недель, 27 июня – 7 августа. Даты комбинаций опубликованы отдельно; не считать их шестью разными лагерями.',
        fee(2027,'$3 850 / 2 недели; $7 000 / 4; $8 350 / 6. Валюту $ подтвердить в американском invoice.',
            'Tuition, laundry, camp T-shirt, все обычные camp activities и trips. Quick Facts описывает три buffet meals и комнаты; окончательные включения питания закрепить в договоре.',
            'Airport pickup $200 и drop off $200 за ребёнка; bedding $60 за enrolled session для прилетающих. Карта +2.75%. New early discount $200 до 1 декабря 2026; returning $300 до 1 ноября только для бывших участников. Дополнительный sibling $300; сочетание скидок неизвестно. Перелёты и жильё родителей отдельно.',
            'В total входят deposit $700 / $1 000 / $1 200 по длительности; повторно его к цене не прибавлять. Остаток до 1 июня 2027. Deposit non-refundable; до 1 мая возврат остального. Позднюю отмену и final terms уточнить.'),
        '8–10 детей одного возраста и два вожатых в cabin, санузел, горячая вода, электричество; laundry раз в неделю. Nurse available 24h по Quick Facts; это не гарантия медицинского страхового покрытия.',
        fit('candidate','9–10 лет в 2027 входит в 6–16; язык/интерес и готовность к ночёвкам проверить.'),
        fit('candidate','6–7 лет входит в 6–16. Это один из новых общих пансионов с минимумом 6; зачисление отдельно.'),
        'Возрастно возможный общий пансион для обоих; сравнивать по среде и активности. Международный состав сам по себе не устанавливает учебный язык.',
        ['Подтвердить EN и языковую помощь, места для обоих, иностранное зачисление, питание/страхование, скидки и итоговую смету.'],
        [src('2027: даты, tuition, deposit и доплаты',birch),src('Возраст 6–16','https://campbirchhill.com/about/camp-birch-hill/'),src('Иностранцы, комнаты и питание','https://campbirchhill.com/quick-facts/'),src('Реальные activities','https://campbirchhill.com/campers/activities/')],
        status='published_2027',priority=['both','general','boarding'])
    dated(p,[row(p,s,e,f'{n} недели · общий пансион',f'${v:,} total, deposit внутри',birch) for s,e,n,v in [
        ('2027-06-27','2027-07-10',2,3850),('2027-07-11','2027-07-24',2,3850),('2027-07-25','2027-08-07',2,3850),
        ('2027-06-27','2027-07-24',4,7000),('2027-07-11','2027-08-07',4,7000),('2027-06-27','2027-08-07',6,8350)]])

    weeq='https://www.weequahic.com/summer-camp-experience/camp-dates-fees/'
    arts='https://www.weequahic.com/summer-camp-experience/summer-camp-activities/creative-fine-arts/'
    p=put('weequahic-general','Camp Weequahic · пансион с STEM electives','США','USA','Lakewood / Wayne County, Pennsylvania · точный адрес прибытия подтвердить',
        'general,sport,art,robotics,science','boarding','7–16; возрастной допуск конкретного Robotics elective отдельно не опубликован',
        'FAQ подтверждает международных детей, включая Мексику. EN как язык занятия Robotics отдельно не установлен; англоязычный сайт и международный состав не заменяют это подтверждение.',
        'Общий пансион с индивидуальным расписанием sports, arts, water/outdoor и STEM. Robotics использует LEGO Mindstorm и другие системы; опытным предлагают индивидуальные/командные внутренние RoboCup серии. Название RoboCup здесь не доказательство участия в официальной мировой лиге RoboCupJunior и не обещание международной награды. Технические часы/инструктор 2027 неизвестны.',
        '2027: Tribal 26 июня – 17 июля; Olympic 19 июля – 8 августа; Super Six 26 июня – 8 августа как отдельный опубликованный полный пакет. Условия двух промежуточных ночей полного пакета уточнить. SEO intro ещё упоминает цену 2026, таблица явно 2027.',
        fee(2027,'Tribal/Olympic $8 100 + обязательный Camper Account $300 = $8 400. Super Six $14 000 + $450 = $14 450. Валюту $ подтвердить в invoice.',
            'Обычные занятия/trips; FAQ три meals и snacks. Camper Account: четыре обязательные T-shirts, towel service, meeting-point transport, spending/tickets, canteen и weekly laundry.',
            'Карта +3%. Early enrollment до 1 сентября 2026 уже истёк. Перелёты, airport transfer вне meeting points, bedding/страхование и возможные older overnight trips уточнить. Не считать Camper Account депозитом, который возвращается автоматически.',
            'Размер/зачёт deposit, payment deadlines и refunds текущего набора публично не установлены в прочитанных страницах.'),
        'До 11 детей одного возраста/пола и три вожатых в bunk; санузел, горячая вода, электричество. Разные возрастные комнаты братьев. Doctor/nurses заявлены в FAQ, страховой счёт отдельно.',
        fit('conditional','Основной возраст подходит. Объём Robotics, возраст elective и EN подтвердить; общий пансион не заменит сезонную команду.'),
        fit('conditional','Пансион только после 7-летия; Robotics elective не подтверждён для младшей группы.'),
        'Интересное сочетание общего отдыха и опциональной робототехники Матвея. Выбор основан на опубликованных возможностях, не на независимом рейтинге результатов.',
        ['Подтвердить Robotics 2027, часы/язык/возраст, доступ братьев, точный адрес, airport costs, полный пакет Super Six и отмену.'],
        [src('2027 dates и обязательный Camper Account',weeq),src('Robotics и внутренние challenges',arts),src('Иностранные дети, комнаты и питание','https://www.weequahic.com/summer-camp-experience/faqs/'),src('Разница короткого и полного пакета','https://www.weequahic.com/summer-camp-experience/our-sessions/')],
        status='published_2027',priority=['general','boarding'])
    dated(p,[row(p,s,e,label,price,weeq) for s,e,label,price in [('2027-06-26','2027-07-17','Tribal · общая смена','$8,400 с Camper Account'),('2027-07-19','2027-08-08','Olympic · общая смена','$8,400 с Camper Account'),('2027-06-26','2027-08-08','Super Six · полный пакет','$14,450 с Camper Account')]])

    man='https://www.manitoucamp.com/future-families/rates-dates/'
    msrc=[src('2027: даты, birth-year gates, HST и доплаты',man),src('EN camp life, ES поддержка и иностранцы','https://www.manitoucamp.com/future-families/international-campers/'),src('Возраст/Grade 1 и адрес лагеря','https://www.manitoucamp.com/future-families/faq/'),src('Выбор общих занятий','https://www.manitoucamp.com/future-families/activity-choice/')]
    mextra='Все charges +13% HST по оператору. Toronto/airport round trip CAD 425; международный пакет детям вне США/Канады CAD 450 (medical insurance/bedding etc). Точную единицу, покрытие и применимость к Rookie Day проверить. Карта +3%; перелёты отдельно. Прибытие семьи из Коста-Рики/Мексики не освобождает от international package.'
    mterms='Плата за отмену/сокращение: CAD 500 до 30 ноября; 750 с 1 декабря до 31 января; 1 500 с 1 февраля до 30 апреля. С 1 мая невозвратно, тогда же срок оплаты. Это условия оператора; год/договор, deposit и смену категории уточнить.'
    for slug,name,age,mat,osc,sessions in [
        ('manitou-long','обычный пансион','FAQ 7–16, Grade 1 и выше',fit('conditional','Возраст подходит; класс и зачисление подтвердить.'),fit('conditional','Нужны 7 лет и Grade 1 по FAQ; short birth-year наборы имеют собственные правила.'),[('2027-07-01','2027-07-27','1st',10800),('2027-07-27','2027-08-19','2nd',7700),('2027-07-01','2027-08-19','Full',15500),('2027-07-01','2027-08-11','6 Week',14350)]),
        ('manitou-first-short','1st Short · только 2019–2020','Первый приезд; только рождённые в 2019 или 2020. FAQ 7–16 / Grade 1 требует согласования',fit('not_eligible','Матвей 2017 года не входит в birth-year 2019–2020 независимо от опыта и возраста.'),fit('conditional','2020 входит в годовую категорию, но общий FAQ 7+ / Grade 1 расходится с возможными шестилетними: требуется явный допуск.'),[('2027-07-01','2027-07-15','1st Short',5400)]),
        ('manitou-second-short','2nd Short · первый приезд обоих','Первый приезд; рождённые 2013–2020; FAQ 7+ / Grade 1 отдельно',fit('conditional','2017 входит в годовую категорию; только first-time camper, класс подтвердить.'),fit('conditional','2020 входит, но возраст 6/7 и Grade 1 нужно согласовать с оператором.'),[('2027-07-27','2027-08-11','2nd Short',5300)]),
        ('manitou-rookie-day','Rookie Day · знакомство с лагерем','Рождённые 2019–2021; отдельный однодневный пробный формат',fit('not_eligible','2017 год не соответствует 2019–2021.'),fit('conditional','2020 входит; допуск иностранного ребёнка, участие/плата родителя и время дня уточнить.'),[('2027-07-17','2027-07-17','Rookie Day',150)])]:
        rookie=slug=='manitou-rookie-day'
        p=put(slug,'Camp Manitou Ontario · '+name,'Канада','CAN','McKellar, Ontario · 10 Camp Road, P2A 0B4; Toronto — зимний офис',
            'general,sport,art,languages','day' if rookie else 'boarding',age,
            'Оператор прямо описывает преимущественно EN жизнь лагеря и сотрудников для ES помощи. Это английское погружение через игры, без школьных language books; ES поддержка не испанский учебный поток.',
            'Спорт, water/outdoor, искусство, музыка, woodwork, фото/видео; выбор интересов, у младших более структурированное расписание. Robotics/AI не подтверждены. '+('Пробный день — знакомство, не двухнедельная школа и не пансион.' if rookie else 'Разные длительности и first-time категории не объединяются в один стандартный допуск.'),
            'Явные заезды 2027. Текущая rates-page объявляет Summer 2027 и Rookie Day registration now open; старую будущую дату открытия из других снимков не использовать как дедлайн. Наличие места не доказано.',
            fee(2027,('CAD 150 +13% =169.50 за ребёнка/день, до иных charges.' if rookie else 'CAD '+('10 800 / 7 700 / 15 500 / 14 350 для четырёх обычных пакетов, до HST.' if slug=='manitou-long' else '5 400 +13% =6 102 за 1st Short, до других charges.' if slug=='manitou-first-short' else '5 300 +13% =5 989 за 2nd Short, до других charges.')),
                'Пробный день; питание/родительское участие не установлено.' if rookie else 'Основной пансион, camp activities и питание по international/activities description; пакет страхования/белья дополнительный.',mextra,mterms),
            'Дневной визит; ночёвка и проживание родителей не включены.' if rookie else 'Cabin 6–14 детей и 2–3 вожатых, sinks/toilets/showers, электричество. Англоязычную cabin можно согласовать; братья могут быть в разных возрастных группах.',
            mat,osc,'Конкретный EN/ES-support кандидат с редкими birth-year правилами. Это другой Manitou, чем оператор manitoucamp.org в Whitefish Falls.',
            ['Подтвердить age/class/birth-year и first-time условия, итог HST/international/transport, цену за родителя Rookie Day, места, комнаты и договор.'],msrc,
            status='published_2027',priority=['general'] if not rookie else ['oscar'],confirmed=['EN'])
        p['language_evidence_role']='camp_life'
        p['eligibility_birth_years']=list(range(2019,2021)) if slug=='manitou-first-short' else list(range(2013,2021)) if slug=='manitou-second-short' else list(range(2019,2022)) if rookie else []
        dated(p,[row(p,s,e,label,f'CAD {v:,} +13% HST; обязательные доплаты отдельно',man) for s,e,label,v in sessions])

    ow='https://discoveropenworld.com/'
    oprice='https://discoveropenworld.com/register/registration-tuition/'
    ofaq='https://discoveropenworld.com/faq/'
    obill='https://discoveropenworld.com/register/billing-and-refund-policies/'
    courses=[
        ('openworld-explore-robotics','Exploring Robotics and Engineering','6–8','robotics,coding,science','exploring-robotics-and-engineering',899,'Физическое/визуальное программирование, робот с условными решениями, конструкции, движение и материалы; пример химического проекта — slime polymer.'),
        ('openworld-explore-games','Exploring Sci-Fi Game Development','6–8','coding,science','exploring-scifi-game-development',899,'MakeCode Arcade, GameGo, sci-fi игровой мир и инженерные задачи; собственная игра на handheld console для дальнейшего использования. Архивная 4-дневная Session 1B стоила $799 вместо $899.'),
        ('openworld-vehicle','Creating an Autonomous Vehicle','9–13','robotics,coding','designing-an-autonomous-vehicle',999,'Arduino-based robot car, датчики, самостоятельные решения, line following/cliff detection. Текст описывает visual coding, technologies перечисляет Arduino IDE / Arduino C; долю текстового кода уточнить.'),
        ('openworld-robots','Building Robots with Friends','9–13','robotics,coding','designing-and-creating-robotics',999,'Visual scripting и Thames & Kosmos Smart Machines; torque/speed, механизм, итерации. Примеры all-terrain vehicle/conveyor; собственный робот для продолжения дома.'),
        ('openworld-game-jam','Creative Game Jam','9–13','coding,art','creative-game-jam',899,'Четырёхдневная разработка игры в RPG Maker MZ: идея, уровень, прототип, storytelling и итерации. Это учебный game jam; международный конкурс/медаль не заявлен.'),
        ('openworld-python','Python Programming Unlocked','9–13','coding','coding-in-python',999,'Python / Visual Studio Community: решения, данные, интерактивность, псевдокод, inheritance и file I/O. Пример text game / penguin identification; упоминание Python в AI не доказывает полноценный AI/ML курс.')]
    for slug,name,age,themes,path,amount,content in courses:
        url='https://discoveropenworld.com/workshops/'+path+'/'
        young=age=='6–8'
        p=put(slug,'Open World by DigiPen · '+name,'США','USA','Washington · Redmond / Bothell и отдельные school campuses по курсу; площадки 2027 не подтверждены',
            themes,'day',age+' на дату workshop по FAQ; выход за возрастной диапазон не обещан',
            'Язык technical teaching EN/ES/RU прямо не установлен в прочитанных course/FAQ; американский университет и английская страница не заменяют подтверждение.',
            content+' Это дневные workshops, не университетское зачисление и не пансион. Курс разработан Open World с консультациями DigiPen faculty; преподаватель-профессор на каждом занятии не обещан.',
            'Homepage уже рекламирует earliest bird 2027 $659/week, но course pages и общий tuition/schedule ещё Summer 2026. Возобновление именно этого курса, точные 2027 даты, кампус и условия акции не установлены; календарных дат 2027 не создано. '+('Game Jam июня 2026 помечен FULL.' if slug=='openworld-game-jam' else 'Старые июнь–август даты 2026 не перенесены вперёд.'),
            fee(2026,f'Архив своего курса: ${amount:,} за '+('4 дня' if slug=='openworld-game-jam' else '1 неделю')+'. Общая реклама 2027 $659/week не считается подтверждённой ценой этого курса.',
                'Общий tuition включает материалы, kits и take-home projects; точное право забрать hardware своего курса и редакцию 2027 подтвердить.',
                'Архив 2026 extended day $75/неделю, $150/2 недели; food, transfer, налоги/регистрационные charges отдельно не установлены. Tuition page sibling $200 и 50% second-workshop требуют года/совместимости; St. Thomas / Open Window site registrations исключены из Open World promotions. Семья оплачивает жильё и дорогу.',
                'Earliest Bird deposit $200 обозначен refundable; general deposit $200 non-refundable. Остальные сроки оплаты/возврата на странице привязаны к 1 июня 2026, поэтому не переносить на 2027. Точный новый договор и зачёт deposit подтвердить.'),
            'Только daily drop-off/pick-up; sleepaway отсутствует. FAQ адрес Redmond 9931 Willows Road NE и Cascadia Bothell 18345 Campus Way NE; свой campus на 2027 неизвестен.',
            fit('not_eligible' if young else 'candidate','Матвею 9–10 в 2027: выше 6–8; опыт не отменяет age gate.' if young else '9–10 входит в 9–13. После подтверждения нового набора/языка можно выбирать инженерный или coding результат.'),
            fit('candidate' if young else 'later','Оскару 6–7 в 2027: соответствует 6–8; новый набор/язык подтвердить.' if young else 'В 2027 6–7, минимальная группа 9–13 пока недоступна.'),
            'Полезная ступень для '+('Оскара' if young else 'Матвея')+' с конкретным проектом. Совпадающие даты/кампусы братьев в 2027 пока не доказаны.',
            ['Подтвердить наличие своего курса в 2027, возраст на начало, EN teaching, campus/часы, применимость $659, take-home kit, food и итоговый договор.'],
            [src('Своя программа и архивный тариф',url),src('Новый общий баннер 2027; не собственная смена',ow),src('Tuition: архив 2026, материалы и скидки',oprice),src('Возраст на дату и day-only',ofaq),src('Различие deposits и устаревшие payment deadlines',obill),src('DigiPen Academy направляет младшие workshops в Open World','https://academy.digipen.edu/')],
            status='partial_2027',priority=['technical'])
        p['intake_evidence']='operator_2027_promotion_course_dates_still_2026'

    rf='https://www.robotfunacademy.com/camps'
    p=put('robotfun-camps','Robotfun Academy · LEGO/VEX camps','США','USA','Massachusetts · точный адрес выбранной camp площадки не установлен',
        'robotics,coding','day','Возраст именно camp не установлен. Отдельные regular courses: LEGO Essential G1–2, VEX GO G2–3, LEGO Prime G3–6, VEX IQ G4–8; это не доказанный camp admission',
        'EN/ES/RU teaching конкретной camp группы не установлен. Не выводить язык из отзывов или англоязычной страницы.',
        'Week-long LEGO/VEX, building/coding/problem solving, Foundation → Advanced Engineering для подготовки к сезону 2026/27. Обещание Competition READY не означает отбор в Worlds. Обычный G4–8 VEX IQ Foundation включает driver/autonomous challenges и sensors; он описывает учебную базу, а не гарантированную летнюю смену.',
        'Camp page: 2026 Summer Camps / See you in 2027. Точные даты, grade gates и новая базовая цена 2027 не опубликованы. Архивный camp день 09–16.',
        fee(2026,'Базовый summer tuition не найден; 2027 не установлен.',
            'Включение набора/hardware, материалов, мероприятий и страховки не установлено.',
            'На странице 2026: extension 08–09 / 16–17 по $25/час; lunch/snacks $100/неделю. Валюту $, налог и применимость в 2027 подтвердить. Дневной формат требует жилья/транспорта семьи.',
            'Публичный Enrollment Agreement содержит waiver/privacy/media terms, но не найден актуальный camp refund/payment schedule; не выдавать этот документ за подтверждение возврата.'),
        'Дневной формат; собственного пансиона на странице camps нет.',fit('unknown','Опыт подходит для подбора уровня, но возраст/класс именно будущей смены не установлен.'),fit('unknown','Regular LEGO G1–2 может быть ориентиром, однако camp минимум и дошкольный допуск не доказаны.'),
        'Технический кандидат для проверки практической глубины и связи с командой; без точной смены не использовать для бронирования поездки.',
        ['Подтвердить свои camp class gates, адрес, EN, новый tuition, оборудование, lunch/extension, refund terms и отдельные правила competition team.'],
        [src('Camp часы и архивные доплаты',rf),src('Regular LEGO; не camp admission','https://www.robotfunacademy.com/lego'),src('Regular VEX IQ учебная база','https://www.robotfunacademy.com/vex-iq'),src('Agreement не заменяет camp refunds','https://www.robotfunacademy.com/program-enrollment-policy')],priority=['technical'])

    rns='https://www.rns.cc/camps/rns-camps'
    for slug,name,age,programme,mat,osc in [
        ('rns-steam','S.T.E.A.M.','Entering G1–G6; Junior G1–3 / Senior G4–6','Эксперименты, engineering challenges, outdoor exploration и игры; 4 дня, максимум 20 в каждой группе. Robotics как гарантированный модуль именно STEAM не заявлен.',fit('conditional','Нужно сопоставление entering grade; вероятный возраст не заменяет школьный допуск.'),fit('conditional','Только entering Grade 1 или выше; дошкольный допуск не подтверждён.')),
        ('rns-junior-coding','Junior Coding','Entering G1–G3','Четырёхдневная сборка/программирование роботов: movement, colour и touch sensors, игровые задачи. Coding ограничен 18 детьми с работой в парах; hardware brand и take-home kit не установлены.',fit('conditional','Нужен entering G1–3; если уже G4 — сравнивать Senior, а не переносить возраст младшей группы.'),fit('conditional','Нужно entering G1–3; kindergarten не соответствует.')),
        ('rns-senior-coding','Senior Coding','Entering G4–G6','Та же опубликованная robotics/coding программа, но старший class gate и отдельная смена. Страница не доказывает более сложный curriculum или индивидуального робота для каждого.',fit('conditional','Только если entering G4–6; год рождения не определяет класс иностранной школы.'),fit('later','В ближайшей возрастной ступени G4–6 обычно недоступно; класс не установлен.'))]:
        p=put(slug,'Rothesay Netherwood School · '+name,'Канада','CAN','Rothesay, New Brunswick · RNS campus',
            'science,art' if slug=='rns-steam' else 'robotics,coding','day',age,
            'EN camp instruction прямо не указан; школьный English/IB/boarding статус не доказывает язык конкретной летней группы и внешний иностранный допуск.',
            programme+' Все camp дни 09–16. Это day camps в школе-пансионе, а не подтверждённое летнее проживание.',
            'Прочитан только Summer 2026: STEAM 6–9 июля, Junior Coding 27–30 июля, Senior Coding 31 августа – 3 сентября; все помечены camp full / waitlist. Набор 2027 ещё не объявлен, старые даты не перенесены.',
            fee(2026,'Архив: $260 / ребёнок / 4-дневный STEAM или Coding camp. Валюту $ и taxes итогового счёта подтвердить; цена 2027 неизвестна.',
                'Hot lunch, два snacks и camp swag; право на hardware не установлено.',
                'Трансфер, страховка, extension и семейное жильё неизвестны/отдельно; школьный пансион не включён.',
                '2026 page: full refund лишь при отмене за 2 недели до первого дня; поздние условия и новая редакция 2027 не установлены.'),
            'RNS campus днём; ночёвка не заявлена. Семья организует проживание и сопровождение.',mat,osc,
            'Понятная робототехническая/STEAM программа по школьным категориям; будущая смена и EN требуют подтверждения, школьная репутация не рейтинг camp.',
            ['Подтвердить 2027 даты, entering grade, EN, иностранных внешних детей, реальный kit/curriculum и полный счёт.'],[src('Camp-specific grades, content, 2026 full и включения',rns)],priority=['technical'])

    sn='https://www.sciencenorth.ca/school-break-camps'
    policy='Отмена ≥14 рабочих дней: возврат минус $10 + applicable taxes; до 2 рабочих дней: service charge $20 + taxes; менее 2 рабочих дней — без возврата. Минимум 4 участников, при отмене оператором возврат, уведомление за 2 недели; обычная регистрация закрывается за 3 дня. Подтвердить договор выбранного года.'
    for slug,title,place,dates in [
        ('science-north-sudbury','Sudbury · зимние и школьные каникулы','Sudbury · Science North, 100 Ramsey Lake Road',[
            ('2026-10-26','2026-10-26','Spooky Science',57),('2026-12-21','2026-12-23','Micro Explorers',114),('2026-12-29','2026-12-31','Let’s Build It',114),('2027-02-01','2027-02-01','Dinos and Discoveries',57),('2027-03-15','2027-03-19','March Break Madness',258.75),('2027-04-23','2027-04-23','Record-Breaking Science',57),('2027-06-11','2027-06-11','Beat the Heat',57)]),
        ('science-north-thunder','Thunder Bay · зимние и школьные каникулы','Thunder Bay · Boys and Girls Club, 270 Windsor Street',[
            ('2026-10-26','2026-10-26','Spooky Science',57),('2026-12-21','2026-12-23','Micro Explorers',114),('2026-12-29','2026-12-31','Let’s Build It · содержание уточнить',114),('2027-01-29','2027-01-29','Motion Masters',57),('2027-02-26','2027-02-26','Dinos and Discoveries',57),('2027-03-15','2027-03-19','March Break Madness',258.75),('2027-04-30','2027-04-30','Record-Breaking Science',57),('2027-06-11','2027-06-11','Beat the Heat',57)])]:
        tb=slug=='science-north-thunder'
        p=put(slug,'Science North · '+title,'Канада','CAN',place,'science,general','day','Группы 4–5 / 6–8 / 9–11. Старшие Robo Builders, TechLab, Circuit Builders 12–13 — отдельные программы',
            'Выбран EN поток: Sudbury предлагает EN/FR раздельно; Thunder Bay прямо English only. Полный EN technical/science day, а не лишь перевод сайта.',
            '09–16: chemistry, микроскопия, инженерные конструкции, биология/физика и научные игры по собственной теме. Robotics 12–13 не переносится в младшие 4–11. '+('У Thunder Bay Let’s Build It body описывает динозавров: тема/содержание расходятся, инженерный curriculum этой смены не обещан. ' if tb else '')+'Название Record-Breaking Science — учебная тема, не запись официального мирового рекорда.',
            'Явные даты каникул 2026/27; запись Dec2026–Jun2027 обозначена opening soon. Календарь показывает опубликованную смену, не свободное место и не уже открытую регистрацию. Nov Robo Ready проверяется отдельным досье из-за расхождения группы 9–11.',
            fee(2026,'Public: $57 / PA day; $114 / 3 зимних дня; $258.75 / 5 дней March Break. Member $51.50 / $103 / $232.88. Валюту $, tax inclusion и финальный invoice подтвердить.',
                'Выбранные дневные scientific activities; food/kit ownership не доказаны.',
                'Обычный drop-off 08:30–09, pick-up 16–16:30. Extension платный, тариф не указан. Sudbury 07:30–17:45; Thunder Bay location intro даёт то же время, FAQ 08–17:30 — конфликт. Lunch/snacks принести, варианты питания на самой Science North уточнить; жильё семьи отдельно.',policy,season='2026/27'),
            'Дневной science centre/club, без пансиона; проживание/transport семьи отдельно.',
            fit('candidate','В 2026 8–9, в 2027 9–10: выбрать соответствующую возрастную группу; братья могут учиться отдельно.'),
            fit('conditional','В 2026 5–6: группа 4–5 или 6–8 зависит от дня рождения. '+('Thunder Bay Oct26 4–5 Sold Out; при возрасте 5 эту дату не считать доступной. ' if tb else '')+'В 2027 6–7 подходит 6–8; зачисление внешнего гостя отдельно.'),
            'Конкретные зимние/весенние STEM дни для семейного пребывания в Канаде; выгодно сравнивать с отдельными тематическими intensives. Готовность регистрации и curriculum проверяются по смене.',
            ['Подтвердить внешних иностранных детей, свой EN age group, opening/места, точную тему, tax, еду, extension часы/цену и местный транспорт.'],
            [src('Даты 2026/27, площадки, языки и refund policy',sn),src('Возрастные карточки и список actual intake','https://www.sciencenorth.ca/camps/communities')],
            status='published_2026_27',priority=['both','technical'],confirmed=['EN'])
        dated(p,[row(p,s,e,label,f'${v:,.2f} public; tax inclusion подтвердить',sn,date_precision='published_session') for s,e,label,v in dates])
        for v in p['timing']['session_details']:v['date_scope']='day_camp_window'

    ticket='https://order.sciencenorth.ca/183345/183380'
    p=put('science-north-robo-ready','Science North · Robo Ready 6–8','Канада','CAN','Sudbury · Science North, 100 Ramsey Lake Road',
        'robotics,coding','day','6–8; отдельная группа, не вся линейка 4–11',
        'Билетная карточка прямо называет English; выбран именно EN поток.',
        'Однодневное знакомство с coding и разными robots: движения, решения и задачи через игры/creative challenges. Hardware brand, глубина и take-home kit не установлены; для опытных детей проверить сложность. 09–16.',
        '20 ноября 2026. Группа 6–8: title, Date, Description и English согласуются. У соседней 9–11 карточки Date Nov20, но Name/heading Spooky Science Oct26 — она не создана как подтверждённый Robotics camp. Thunder Bay Nov27 из списка не подменяет Sudbury Nov20.',
        fee(2026,'Non-Member Child $57 на actual ticket; tax inclusion/валюту подтвердить.',
            'День курса; питание/kit не установлены.',
            'Extension и food как в School Break; конкретные charges не известны. На странице есть member early-access notice и public price option: это не подтверждённое свободное место/зачисление.',policy),
        'Дневной курс; семья организует проживание/дорогу.',
        fit('conditional','Подходит только если Матвею ещё 8 на 20 ноября 2026; в 9 лет нужна отдельная 9–11 группа, её название противоречиво.'),
        fit('conditional','Нужны уже исполненные 6 лет на 20 ноября; если ещё 5, эта группа не подходит.'),
        'Проверенная конкретная EN robotics карточка с точной ценой; возраст и сложность важнее общего бренда.',
        ['Подтвердить дни рождения, доступ иностранцам и public intake, kit/сложность, еду/extension; для Матвея 9 лет исправленную 9–11 карточку.'],
        [src('Actual ticket: 6–8 / EN / Nov20 / $57',ticket),src('Часы, место и общие условия',sn),src('Противоречивый 9–11 ticket','https://order.sciencenorth.ca/183346/183381')],
        status='published_2026',priority=['technical'],confirmed=['EN'])
    dated(p,[row(p,'2026-11-20','2026-11-20','Robo Ready 6–8 · 09–16','$57 public; tax inclusion уточнить',ticket)])

    for slug,title,url,age,mat,osc in [
        ('science-north-beebots','Homeschool Bee-Bot','https://order.sciencenorth.ca/180578/180586','Grades 1–3 и Ages 6–8 по собственному ticket',fit('conditional','Только если ещё 8 и Grades1–3; 9-летнему эта ticket категория не подходит. Сейчас Sold Out.'),fit('conditional','Нужны уже 6 лет и Grade1–3; дошкольный допуск не доказан. Сейчас Sold Out.')),
        ('science-north-cubetto','Homeschool Code with Cubetto','https://order.sciencenorth.ca/180578/180585','JK/SK и Ages 4–5 по собственному ticket',fit('not_eligible','Выше дошкольной категории 4–5.'),fit('conditional','Только если на 19 октября ещё 5 и JK/SK; в 6 лет выше ticket категории. Сейчас Sold Out.'))]:
        p=put(slug,'Science North · '+title,'Канада','CAN','Sudbury · Science North, адрес комнаты workshop подтвердить','robotics,coding','day',age,
            'Actual ticket прямо English; FR соседний ticket — другой поток.',
            'Короткая homeschooling мастерская по указанной системе, начало 10:00. Конец, food, hardware ownership и подробные learning outcomes не опубликованы в карточке. Это не доказанный полный camp day.',
            '19 октября 2026, обе actual EN tickets Sold Out. Другие даты Homeschool2026/27 принадлежат другим темам и не перенесены сюда как повтор Bee-Bot/Cubetto.',
            fee(None,'Цена закрытой workshop карточки не показана. PA-day $57 и summer weekly fees сюда не перенесены.','Подробные включения не установлены.','Жильё/дорога семьи; участие/оплата взрослого и session-specific charges не установлены.','Общие School Break refunds не считаются автоматически договором Homeschool; свои условия уточнить.'),
            'Дневная мастерская, пансиона нет; длительность неизвестна.',mat,osc,
            'Полезный ориентир школьных/дошкольных EN workshops, но эта конкретная дата уже недоступна.',
            ['Новый открытый набор, свой возраст/класс, foreign/homeschool eligibility, duration, food, стоимость и adult accompaniment.'],
            [src('Actual ticket: age/class/EN и Sold Out',url),src('Отдельные темы Homeschool 2026/27','https://www.sciencenorth.ca/camps/communities')],
            status='published_2026',confirmed=['EN'])
        v=row(p,'2026-10-19','2026-10-19','10:00 · workshop, конец неизвестен','Цена не опубликована · SOLD OUT',url,availability=dict(status='closed',label='Actual ticket Sold Out'),proof='Самостоятельная workshop карточка, начало 10:00; sold out, не включается в семейный календарь доступных дат.')
        v['date_scope']='workshop_window';dated(p,[v])

    robo='https://www.sciencenorth.ca/robokids'
    p=put('science-north-robokids','Science North · RoboKids after-school','Канада','CAN','Sudbury · TechLab, Science North',
        'robotics,coding,science','day','8–12',
        'EN/ES/RU teaching своего after-school курса не установлен; EN подтверждение PA camps не переносится на RoboKids автоматически.',
        '8-недельный after-school курс LEGO SPIKE: природные бедствия, robotic first responders, programming, тестирование и rescue missions. Это регулярные занятия, не восьминедельное непрерывное проживание.',
        'Страница просит ждать даты программы 2026; точных upcoming занятий и нового набора 2027 нет. Calendar rows не создавались.',
        fee(2026,'8 недель: Non-Member $300 + HST; Member $250 + HST. Ставка HST на этой странице не названа; полный счёт/валюту уточнить.',
            'Восьминедельная программа; hardware ownership не доказано.',
            'Транспорт, еда, длительность каждого занятия, членство и язык отдельно. Налоги Manitou не переносятся на чужой invoice.',
            'Конкретные after-school payment/refund terms не установлены.'),
        'TechLab после школы, без ночёвок.',fit('candidate','8–10 лет соответствует; нужны реальные upcoming даты и подходящая сложность.'),fit('later','В 2027 6–7 ниже минимума 8.'),
        'База для регулярного инженерного проекта Матвея при жизни/длительном пребывании в Ontario; не замена летнего пансиона.',
        ['Подтвердить даты/часы, EN, внешний иностранный доступ, уровень, kit, счёт и регулярное присутствие 8 недель.'],
        [src('8–12, LEGO SPIKE, 8 недель и прайс',robo)],priority=['technical'])
