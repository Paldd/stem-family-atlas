"""Current European programme separation and season-specific family costs."""
from copy import deepcopy

CHECKED = '2026-10-05'
ELFES = 'https://cdn.leselfes.com/wp-content/uploads/2026/07/2027-Summer-Camp-Registration-Form_Digital_avec-champs.pdf'
VC = 'https://www.villagecamps.com/'
G = 'https://www.la-garenne.ch/'
ILC = 'https://internationallanguagecamps.com/'
TECS = 'https://www.tecs.es/tecs/'
UPDATED = ['les-elfes', 'village-leysin', 'la-garenne', 'garenne-robotics-workshop', 'ilc', 'tecs-puerto-kids']


def add_europe_v94(add, src, fit, profiles):
    by_slug = {p['slug']: p for p in profiles}

    def source(p, title, url):
        s = next((s for s in p['sources'] if s['url'] == url), None)
        if s:
            s.update(title=title, checked=CHECKED)
        else:
            p['sources'].append(dict(title=title, url=url, checked=CHECKED))

    # The Summer2027 contract has a different cancellation deduction from Winter.
    # Preserve each old winter/spring note rather than applying new summer terms.
    p = by_slug['les-elfes']
    previous_deposit = p['price']['deposit']
    previous_extras = p['price']['extras']
    summer_extras = ('ЛЕТО 2027: обязательные registration CHF 150/ребёнок и medical/accident CHF 120/неделя. '
        'Один half-day workshop за смену обязателен, но Shelter Building 6+ включён: платный workshop не обязателен. '
        'Robotics 10+ CHF 180, Arts/Theatre 6–11 CHF 190, Cooking 6–11 CHF 210, Etiquette 6–11 CHF 180. '
        'Cancellation insurance CHF 80/неделя optional; одежда laundry CHF 60/мешок, фото CHF 50, halal CHF 100/неделя. '
        'Geneva return CHF 190, Martigny return CHF 80; трансфер в другие даты CHF 170 one-way. Единицу тарифа трансфера подтвердить. '
        'Языки EN/FR/ES/DE/CN: 8×~50 минут в неделю CHF 200 или 12×~50 CHF 350; период начисления суммы уточнить, не умножаем автоматически на две недели. '
        'Можно выбрать без языкового курса; тогда в эти часы обязательны onsite sports. '
        'Четыре недели подряд: CHF 1 000 скидка, это не sibling discount. Нестандартные даты могут добавить 10% service charge.')
    summer_terms = ('ТОЛЬКО ЛЕТО 2027: невозвратный CHF 1 000 — часть цены, не extra; остаток за 30 дней, '
        'при регистрации менее чем за 30 дней сразу полная сумма. Optional cancellation policy CHF 80/неделя: '
        'документированная болезнь/травма/смерть близкого до 24 часов перед заездом — возврат camp fee минус CHF 1 000 аванса. '
        'Без этой policy обычный возврат не обещан; §2 отдельно допускает полный возврат при подтверждённом отказе Swiss consulate в визе. '
        'Неиспользованные дни обычно не возвращаются, медицинский ранний выезд требует врача/страховой. '
        'Medical покрывает Швейцарию и период лагеря, не pre-existing conditions. CHF 1 000 liability deductible '
        'по AXA civil responsibility — условие страхового случая, не второй аванс или обязательная доплата. '
        'Зима и весна имеют отдельные условия; этот summer deduction не переносится на них.')
    p['price']['included'] = ('ЛЕТО: четыре места с ensuite, полный пансион/напитки, уборка и смена белья/linen laundry раз в неделю, '
        'большинство sports и экскурсии частным автобусом. Linen laundry не означает бесплатную стирку одежды. '
        'Shelter Building 6+ доступен как включённый обязательный workshop. Зима/весна — отдельные сезонные пакеты.')
    p['price']['extras'] = summer_extras + ' ЗИМА: обязательные registration 150, medical 120/неделя и helmet rental 15/неделя по отдельной зимней форме; остальные зимние статьи в карточках смен.'
    p['price']['deposit'] = summer_terms
    p['price']['label'] += (' Летний пример 15–28.08: 4 750 + 150 + 2×120 = CHF 5 140/ребёнок; '
        'двое CHF 10 280 с включённым Shelter Building, до дороги, трансфера и платных опций. '
        'Аванс 1 000 не прибавляется повторно. При согласованном 10+ Robotics Матвею ещё 180; цена полного invoice неизвестна.')
    p['questions'] = ['Подтвердить точные DOB/места, часы и язык Robotics, summer transfer unit, начисление языка, laundry и финальный семейный счёт. Для зимы/весны нужен их собственный договор.']
    source(p, 'Летняя форма именно 2027: цены, обязательные сборы и summer contract', ELFES)
    source(p, 'Официальная страница летней формы', 'https://www.leselfes.com/summer-camp/enrol/')
    for v in p['timing']['session_details']:
        v['deposit'] = previous_deposit
        if 'extras' not in v:
            v['extras'] = previous_extras
        if v['label'].startswith('Летний'):
            v.update(extras=summer_extras, deposit=summer_terms, source=ELFES,
                proof='Шесть точных смен и базовых тарифов из собственной Summer2027 registration PDF; mandatory fees/workshop и сезонная отмена проверены отдельно. Выбор платного workshop не обязателен.')

    # Retain CP051 and its four IDs, but narrow it to the actual Junior programme.
    # STEM's two July dates belong to a separate 10+ programme, not the June/August Junior dates.
    p = by_slug['village-leysin']
    p.update(provider='Village Camps · Leysin Junior Adventure', themes=['general', 'sport'],
        age='Junior Adventure 7–9; отдельный STEM начинается с 10',
        programme='Общий Junior Adventure для первого пансиона: возрастные игры, outdoor и спорт, заявленный оператором ratio 1:4; staff CPR/First Aid и health specialists. STEM, языковые курсы 10+ и Tennis — другие программы, не содержание каждой Junior смены.',
        accommodation='Swiss Alpine Centre Leysin: комнаты 3–4, большинство с ensuite; распределение по возрасту/полу. Три приёма пищи; special diet заранее согласовать. Junior page перечисляет Geneva/Lausanne/chocolate factory/Aigle, окончательный маршрут меняется. Booklet с metadata2026: до12 лет сопровождение на экскурсиях, но в activity parks counsellors находятся у разных attractions; это не обещание непрерывного 1:1.',
        editorial_reason='Общий пансион для Оскара только после 7-летия, Матвею только пока ему 9. После его 10-летия рассматривать отдельный STEM; EN обоих треков ещё не доказан.',
        shortlist=['general', 'boarding'])
    p['family_fit'] = dict(matvey=dict(status='conditional', detail='Junior только в возрасте 7–9 на заезд. После 10-летия нужен отдельный STEM/другой 10+ трек, не эта Junior карточка.'),
        oscar=dict(status='conditional', detail='Junior только после 7-летия; точный DOB и готовность к пансиону ещё подтвердить.'))
    p['language'] = 'Язык Junior не указан прямо на прочитанных programme/guide; английская форма и international staff не доказывают EN преподавание. Отдельный English Language Camp 10+ не является уроком Junior.'
    transfer = ('Travel PDF без года: Geneva CHF 100 one-way / 200 return, arrivals09–19/departures11–19; '
        'Lausanne train CHF 55/110,08–18. Extra night CHF 215/ребёнок, только заранее согласованные случаи. '
        'Текущая public form: optional accident/illness CHF 140/ребёнок/смена. '
        'Metadata booking conditions и Leysin booklet — 2026; применимость всех contract/transfer статей к 2027 подтвердить. '
        'Loyalty относится к household и числу разных лет, не числу детей/смен: первый summer ещё без скидки; '
        'после одного summer CHF 200/camper при следующей booking до конца ноября, затем другие tiers. Team применяет скидку вручную, не автоматическое уменьшение первой цены.')
    terms = ('Публично связанный PDF имеет metadata Parent Guide2026, не доказанный контракт2027: '
        'CHF 1 000 невозвратный депозит в счёт цены в течение48ч; balance May1, послеMay1 full payment за48ч. '
        'Отмена доMay1 удерживает deposit, May1–31 удержание50%total fees paid, June1–start100%; после начала без возврата. '
        'При отмене specialist programme по недостатку участников альтернатива или возврат этого programme, не автоматически всей поездки. '
        'Возможны card fees неизвестного размера. Travel submission: PDF одновременноMay1 иMay15, форма≥30дней — конфликт, это не registration deadline. '
        'Применимость к конкретной смене2027, invoice и возможное суммирование удержаний нужно подтвердить.')
    p['price'] = dict(year=2027, label='Junior: CHF 5 200 / 5 500 / 5 500 / 5 100 за две недели по порядку четырёх смен. Последняя смена двоим CHF 10 200 за лагерь; при условном Geneva return200/ребёнок и optional insurance140/ребёнок CHF 10 880 до прочих расходов. Transfer/contract2027 ещё не подтверждены, это пример расчёта.',
        included='Пансион, три приёма пищи, Junior activities; описанные admission fees на экскурсиях по Switzerland overview. Окончательный пакет2027 и pocket money/laundry уточнить.', extras=transfer, deposit=terms)
    p['timing']['label'] = 'Junior 2027: 20.06–03.07, 04–17.07, 18–31.07, 01–14.08. Эти четыре строки только Junior, не четыре STEM смены.'
    p['timing']['session_details'] = [dict(start=a, end=z, place=p['place'], label='Junior Adventure · 7–9 · пансион', price='CHF '+str(price)+' / две недели; transfer/optional insurance отдельно', source=VC+'junior-programme-summer-school-camp-in-leysin-switzerland',
        proof='Собственная Junior page явно печатает возраст7–9, точные даты2027 и цену данной смены. STEM10+ хранится в отдельном досье.')
        for (a,z),price in zip(p['timing']['sessions'], [5200,5500,5500,5100])]
    p['questions'] = ['Подтвердить возраст каждого на заезд, EN Junior/STEM, одновременное размещение разных треков, контракт2027, итоговый invoice/transfer/laundry/pocket money и срок travel form при конфликте May1/May15/30дней.']
    for title,url in [('Junior: возраст и четыре собственных смены2027',VC+'junior-programme-summer-school-camp-in-leysin-switzerland'),
        ('Даты и цены текущих программ2027',VC+'dates-and-prices-parent-guide'),('Текущее проживание и трёхчасовые утренние основные занятия',VC+'summer-camp-programmes-in-leysin-switzerland'),
        ('Own Parent Guide со ссылками на PDF',VC+'summer-camp-parent-guide'),('Public form: optional medical140 и travel≥30дней',VC+'sign-up?lang=eng'),
        ('Travel PDF: тарифы/времена и конфликт May1/May15',VC+'pdf/Travel-Information.pdf'),('Booking conditions: metadata2026, финальный2027 контракт нужен',VC+'pdf/booking-conditions.pdf?1775656204='),
        ('Leysin booklet: metadata2026, сопровождение/medical',VC+'pdf/Campinformation_Leysin.pdf?v=1534565998'),('Family loyalty: household years, не sibling discount',VC+'vc-loyalty-programme')]:source(p,title,url)

    add('village-leysin-stem','Village Camps · Leysin STEM & Robotics','Швейцария','CHE','Leysin / Swiss Alpine Centre','robotics,coding,engineering','boarding','10–17; все уровни от новичков до experienced',
        'EN технического преподавания прямо не установлен. Английская programme/форма и вопрос English proficiency не подтверждают язык инструктора.',
        'LEGO Education SPIKE: gearing, sensors/motors, programming и decision structures; сначала guided concepts, затем собственный робот и командные задачи. Robot Wars — внутренний финал лагеря, не международная медаль FLL/VEX. Morning main programme3ч из общего расписания, не гарантированные30технических часов: выходные/экскурсии и часы инструктора уточнить. Kits, компьютеры, iPad и software предоставляются и остаются в лагере.',
        'Только две собственные смены2027: 04–17.07 и18–31.07. June/August Junior dates не STEM.',
        dict(year=2027,label='CHF 5 500/ребёнок/две недели. Оскар6–7 ниже10+; его отдельный Junior в июльскую смену тоже5 500 только после7-летия. Условная пара STEM+Junior11 000; при Geneva return200каждому и optional insurance140каждому11 680 до прочих расходов и подтверждения тарифов/договора2027.',
            included='Пансион/три приёма пищи, STEM programme, учебные kits/устройства; оборудование остаётся в лагере. Полный пакет2027 ещё подтвердить.',extras=transfer,deposit=terms),
        'Swiss Alpine Centre, комнаты3–4, большинство ensuite. Собственная STEM page ошибочно перечисляет Salzburg/Sigmund Thun Klam/Welten Museum и Austria link рядом с жильём Leysin: это конфликт сайта, австрийские экскурсии не включены как обещанный швейцарский маршрут.',
        fit('conditional','Только после фактического10-летия к заезду. Три года соревнований требуют advanced-level задач; конкретный уровень и EN не установлены.'),
        fit('later','В2027 будет6–7, минимум10. Отдельный Junior7–9 только после7-летия, не STEM.'),
        'Двухнедельная робототехника для Матвея после10-летия; для Оскара отдельноJuniorпосле7-летия. Английский преподавателя, сложность и фактический возраст на заезд ещё проверить.',
        ['Подтвердить DOB10+, EN технического инструктора, advanced tasks/реальные часы, Swiss excursion itinerary, одновременный Junior для брата7+ и полный договор/счёт2027.'],
        [src('Собственная STEM programme: возраст, даты, kits и site conflict',VC+'STEM-robotics-summer-school-camp-in-leysin-switzerland')]+[src(s['title'],s['url']) for s in p['sources'] if s['url']!=VC+'STEM-robotics-summer-school-camp-in-leysin-switzerland'],
        status='published_2027',priority=['technical','boarding'],sessions=[['2027-07-04','2027-07-17'],['2027-07-18','2027-07-31']])

    # Current menu now includes Robotics under5–9; explicit form/PDF8–12 still governs.
    p = by_slug['la-garenne']
    p['programme'] = ('Общий язык/спорт/творчество/поездки. Текущие summer menu теперь показывают Robotics в5–9 и10–12; прежнее menu10+ расхождение снято. '
        'Но конкретные form и contract2027 задают8–12, три занятия заCHF500: это не допуск Оскара6–7. '
        'Workshop PDF содержит VEX IQ/V5, Python/3D design; финальная фраза two sessions расходится с заголовком Three Sessions и текущим договором3. '
        'Расписание/часы/технический EN неизвестны; короткая опция, не двухнедельный инженерный интенсив.')
    p['questions'] = ['Подтвердить EN/часы/уровень workshop8–12, единицы day insurance, pocket money и sibling discount, Saturday day schedule, места и итоговый семейный счёт2027.']
    p['price']['extras'] += ' Семейная база при одной смене/одном формате и10%второму: CHF12 445 day или13 680 boarding; одна Robotics опция+500. Дополнительно2×10×число оплачиваемых insurance days и pocket money по возрасту; количество дней пока не подставляем.'
    for title,url in [('Текущий menu2027: Robotics уже есть в5–9 и10–12',G+'summer-camps/'),('Workshop PDF:8–12, заголовок3/finalphrase2, уровень и проекты',G+'summer/repository/summer_robotics_workshop.pdf'),('Summer2027 conditions:9страниц, relevant extras/cancellation',G+'summer/repository/summer-conditions.pdf'),('Read-only form: конкретные8–12/500/3',G+'summer-camps/apply-online/')]:source(p,title,url)
    p = by_slug['garenne-robotics-workshop']
    p['age'] = '8–12 по public form и summer conditions2027; menu теперь также содержит Robotics в5–9, но не расширяет конкретный8+ gate.'
    p['family_fit']['matvey']['detail'] = 'Летом2027 возраст9–10 входит в8–12; прежнее menu10+ расхождение снято. Уровень группы, EN, часы и реальное место в опции ещё согласовать.'
    p['family_fit']['oscar']['detail'] = 'В2027 возраст6–7 ниже конкретного8+ gate. Robotics в menu5–9 не отменяет возраст8–12 формы/договора.'
    p['programme'] = ('Опциональный workshop8–12: VEX IQ, sensors/motors, VEXcode blocks; более опытным VEX V5 по возрасту/опыту. '
        'Fusion360/Tinkercad, BambuLab3D printing, Tinkercad circuits, Python basics/input/output/variables/loops для игры. '
        'Это перечень возможных проектов, не обещание прохождения всех за3занятия. Текущие form/contract2027:3занятияCHF500; PDF на одной странице говорит Three Sessions, в конце two sessions — числовой конфликт остаётся. '
        'PDF описывает take-home Bluetooth speaker в3Dкорпусе и completion certificate; текущий комплект2027 подтвердить. Certificate не международная победа, EN не следует из утренних language lessons.')
    p['questions'] = ['Подтвердить технический EN/ES, actual hours трёх занятий, advanced tasks, kit/materials/take-home, места на выбранной общей смене и финальный invoice2027.']
    p['editorial_reason'] = 'Матвею по конкретному8–12 gate подходит короткое знакомство сVEX/Python/3D; для experienced engineer полезность зависит от сложности и часов. Оскару6–7 пока только общий лагерь.'
    for s in deepcopy(by_slug['la-garenne']['sources']):source(p,s['title'],s['url'])

    p = by_slug['ilc']
    p['price']['label'] = ('Недатированный прайс FUN6–9: одна неделя CHF2 915 day/3 995 board, две5 830/7 990. '
        'Adrenaline10–13: одна3 015/4 095, две6 030/8 190. Registration CHF200/stay отдельно, единицу на ребёнка подтвердить. '
        'Условный пример двоеFUN, две неделиboarding: 2×7 990+2×200+2×2×70laundry+2×350sharedGeneva = CHF17 360. '
        'Если Матвей10+ вAdrenaline, база+200 =17 560. Это расчёт по текущему недатированному прайсу, не подтверждённая цена2027 или полный invoice.')
    p['price']['extras'] = ('Laundry CHF70/неделя: прайс прямо пишет mandatory for2weeksstay; начисление обоим/применение кday или более длинным срокам подтвердить. '
        'Geneva CHF350/transfer именно за группу1–2человека, не350каждому; туда+обратно для двух вместе700. Для3people410/transfer,4people470. '
        'UM+160 и night21–06+60 отдельно. Tennis420/week, golf490, climbing/horse470, intensive EN/FR430/week,1ч17–18. '
        'Language-only700/week09–12 — отдельный продукт, не стоимость полного лагеря. Перелёт, одежда/страховка/прочие сборы и год тарифа ещё уточнить.')
    p['questions'] = ['Подтвердить год dates/prices и места, FUN/Adrenaline по DOB, registration unit, mandatory laundry для точного формата/срока, shared transfer и итоговый invoice; письменно разъяснить сочетание1000cancellation fee с процентами.']
    for title,url in [('FUN6–9:15часов языковых занятий/неделя иEN/FRpractice',ILC+'our-camps/summer-camp/megeve-france-en/fun'),('Полный текущий прайс:1/2недели, mandatorylaundry, groupedtransfer; года нет',ILC+'prices'),('Недатированные terms:1000fee ипроценты, взаимодействие неясно',ILC+'general-terms-and-conditions-of-sale'),('OwnFAQ:UMcontext, не гарантия услуг/страхования',ILC+'faq')]:source(p,title,url)

    p = by_slug['tecs-puerto-kids']
    p['price']['extras'] += (' Discountpage: два siblings25€/child, former30€, referral40€, combined camps200€; '
        'применимость к2027 и пакетам ещё неизвестна. Early40€until30.04.2026 истёк, не скидка/registrationdeadline2027. '
        'Механика combination исключает corporatecollective; referralreciprocal запрещён. Никакие скидки заранее из1730не вычитаются.')
    p['price']['deposit'] += ' Consumerinfo — общая страница прав клиента/неофициального обучения TheEnglishCentreSuppliersSL, не camprefundcontract. Catalogs page всё ещё TECS2026, brochure выдаётся через email leadform или account; контакт/аккаунт не отправлялся, public2027contract пока не получен.'
    p['questions'] = ['Подтвердить реальный год дат/пакета1730€, age7+ на заезд, final2027brochure/contract, insurance/transfer, применимость sibling discount и полный счёт обоим.']
    for title,url in [('Текущая PuertoKids:7–13, ENimmersion, boarding, даты безгода',TECS+'tecs-puerto-kids/'),('Owncatalogs:описание2026 иemailgate, без подписки',TECS+'catalogos/'),('Скидки:earlyuntil30Apr2026 истёк;2027 не установлен',TECS+'descuentos/'),('Generalconsumerinformation:неcampcancellationcontract',TECS+'informacion-para-el-consumidor/')]:source(p,title,url)

    from camp_americas_v90 import clean_profile
    for p in profiles:
        if p['slug'] in UPDATED or p['slug']=='village-leysin-stem':
            p['checked']=CHECKED
            if p['slug']=='village-leysin-stem':
                for s in p['sources']:s['checked']=CHECKED
            clean_profile(p)
    polish_europe_v94(by_slug, profiles[-1])


def polish_europe_v94(by_slug, stem):
    """Write family-facing prose directly; never translate substrings in dates/terms."""
    p=by_slug['les-elfes']
    p['price']['label']='Пансион: летние две недели CHF 4 990 / 5 900 / 6 500 / 6 200 / 5 700 / 4 750 по порядку шести смен. Весна CHF 4 850; зима CHF 2 200–2 950/неделя. Пример 15–28 августа 2027: 4 750 + 150 + 2×120 = CHF 5 140/ребёнок, двое CHF 10 280 с включённым Shelter Building. Дорога, трансфер и платные опции отдельно; это ещё не окончательный счёт. Аванс 1 000 входит в цену. Робототехника Матвею после 10-летия добавит 180.'
    p['price']['included']='Летом: комнаты на четверых с собственным санузлом, полный пансион и напитки, уборка, стирка постельного белья раз в неделю, основные спортивные занятия и экскурсии частным автобусом. Shelter Building с 6 лет можно выбрать как включённый обязательный мастер-класс. Стирка одежды оплачивается отдельно. Зима и весна имеют свои пакеты.'
    extra='ЛЕТО 2027: обязательный регистрационный сбор CHF 150/ребёнок и медицинская страховка CHF 120/неделя. Один мастер-класс на полдня за смену обязателен; Shelter Building 6+ включён. Платные варианты: робототехника 10+ CHF 180, искусство/театр 6–11 CHF 190, готовка 6–11 CHF 210, этикет 6–11 CHF 180. Страхование отмены CHF 80/неделя по желанию; стирка одежды CHF 60/мешок, фото 50, халяльное питание 100/неделя. Женева туда-обратно CHF 190, Martigny туда-обратно 80, другие даты 170 в одну сторону; единицу тарифа трансфера подтвердить. Языки EN/FR/ES/DE/CN: 8 занятий по ~50 минут в неделю за 200 или 12 за 350; период начисления суммы уточнить. Без языкового курса в эти часы предусмотрен обязательный спорт на территории. За четыре недели подряд скидка 1 000; нестандартные даты могут добавить 10% сервисного сбора.'
    terms='ТОЛЬКО ЛЕТО 2027: невозвратный аванс CHF 1 000 входит в цену; остаток за 30 дней. При регистрации менее чем за 30 дней сразу полная оплата. Страхование отмены CHF 80/неделя: при документированной болезни/травме/смерти близкого до 24 часов перед заездом возврат стоимости лагеря с удержанием аванса 1 000. Без этой страховки обычный возврат не обещан. §2 отдельно допускает полный возврат при подтверждённом отказе консульства Швейцарии в визе. Медицинское покрытие действует в Швейцарии во время лагеря и исключает существовавшие ранее болезни. Франшиза CHF 1 000 по гражданской ответственности AXA относится к страховому случаю, а не к обязательной доплате. Для зимы и весны нужны их отдельные условия.'
    p['price'].update(extras=extra+' ЗИМА: по отдельной зимней форме обязательны регистрация150, medical120/неделя и прокат шлема15/неделя; подробности в карточках зимних смен.',deposit=terms)
    p['questions']=['Подтвердить точные дни рождения, места, часы и язык робототехники, единицу летнего трансфера, начисление языкового курса, стирку одежды и итоговый семейный счёт. Для зимы/весны проверить их договоры.']
    for v in p['timing']['session_details']:
        if v['label'].startswith('Летний'):v.update(extras=extra,deposit=terms)

    extra='Трансферный PDF без года: Женева CHF 100 в одну сторону/200 туда-обратно, прилёт09–19/вылет11–19; вокзал Lausanne55/110,08–18. Дополнительная ночь215/ребёнок только по предварительной договорённости. Текущая форма предлагает необязательную страховку от травмы/болезни140/ребёнок/смена. У условий бронирования и буклета Leysin в метаданных2026: применимость к2027 подтвердить. Лояльность считается по разным летним сезонам семьи; две смены или двое детей в первое лето не дают скидку. После одного лета при следующем бронировании до конца ноября200/ребёнок, далее другие уровни. Скидку применяет оператор вручную после бронирования.'
    terms='Связанный PDF назван Parent Guide2026 в метаданных; окончательный договор2027 ещё нужен. В нём: невозвратный авансCHF1 000 в счёт цены за48ч, остаток к1мая; после1мая полная оплата за48ч. Отмена до1мая удерживает аванс,1–31мая50%оплаченных сборов, с1июня до заезда100%; после начала без возврата. При отмене тематической программы из-за малого набора предлагают альтернативу или возврат этой программы. Сборы за оплату картой неизвестны. Срок сведений о дороге расходится: PDF одновременно1мая и15мая, форма минимум30дней до приезда. Это не срок регистрации. Применимость условий2027 и расчёт удержаний подтвердить.'
    for q in [by_slug['village-leysin'],stem]:
        q['price'].update(extras=extra,deposit=terms)
    p=by_slug['village-leysin']
    p['price']['label']='Junior: CHF5 200/5 500/5 500/5 100 за две недели по порядку четырёх смен2027. Последняя смена двоим10 200 за лагерь. Если трансфер200 и необязательная страховка140 начисляются каждому, пример10 880 до прочих расходов. Трансферный тариф и договор2027 ещё подтвердить.'
    p['programme']='Junior Adventure7–9: общий пансион, возрастные игры, природа и спорт. Заявлены1вожатый на4детей, CPR/First Aid и медицинские специалисты; это сведения оператора. STEM10+, отдельные языковые курсы и Tennis — другие программы. Для первой поездки проверить самостоятельность и поддержку ребёнка.'
    p['accommodation']='Swiss Alpine Centre Leysin: комнаты3–4, большинство с собственным санузлом; распределение по возрасту/полу, три приёма пищи. Особое питание заранее согласовать. Junior перечисляет Geneva/Lausanne/chocolate factory/Aigle; итоговый маршрут уточнить. Буклет с2026 в метаданных обещает сопровождение до12лет, но в парках развлечений вожатые стоят у разных аттракционов; это не непрерывное сопровождение1:1.'
    p['questions']=['Подтвердить возраст каждого на заезд, английский Junior/STEM, одновременное размещение разных треков, договор2027, итоговый счёт, трансфер, стирку/карманные деньги и срок сведений о дороге при конфликте1мая/15мая/30дней.']
    stem['price']['label']='CHF5 500/ребёнок/две недели. Оскару6–7 нужен отдельный Junior после7-летия; в июльские смены его цена тоже5 500. Условная пара STEM+Junior11 000 за лагерь; с трансфером200 и необязательной страховкой140 каждому11 680 до прочих расходов. Тарифы трансфера и договор2027 ещё подтвердить.'
    stem['age']='10–17; допускаются новички и опытные участники'
    stem['programme']='LEGO Education SPIKE: передаточные отношения, датчики/моторы, программирование и условия/ветвления. Сначала основы с преподавателем, затем собственный робот и командные задачи. Финальный Robot Wars — внутренний конкурс лагеря. Общее расписание предусматривает3часа основного направления утром; фактические технические часы с учётом экскурсий/выходных ещё уточнить. Наборы, компьютеры, iPad и программы предоставляются и остаются в лагере.'
    stem['accommodation']='Swiss Alpine Centre Leysin: комнаты3–4, большинство с собственным санузлом. На собственной STEM-странице рядом с жильём Leysin перечислены Salzburg/Sigmund Thun Klam/Welten Museum и ссылка на Австрию. Это расхождение сайта; австрийские экскурсии не включены как обещанный маршрут швейцарского лагеря.'
    stem['family_fit']['matvey']['detail']='Только после фактического10-летия к заезду. После трёх лет соревнований нужны задачи для опытных участников; сложность, часы и английский преподавателя ещё неизвестны.'
    stem['questions']=['Подтвердить10-летие к заезду, английский технического инструктора, задачи для опытных участников, реальные часы, швейцарские экскурсии, одновременный Junior для брата7+ и полный договор/счёт2027.']

    p=by_slug['la-garenne']
    p['programme']='Общие языковые занятия, спорт, творчество и поездки. Текущее меню уже показывает Robotics в группах5–9 и10–12. Конкретные форма и договор2027 задают8–12: три занятия заCHF500. Оскару6–7 доступна общая программа. В мастер-классе заявлены VEX IQ/V5, Python и3Dдизайн; PDF содержит «три занятия» в заголовке и «два» в финале. Часы, язык и сложность уточнить: это короткая опция внутри смены.'
    p['questions']=['Подтвердить английский, часы и сложность мастер-класса8–12, количество оплачиваемых дней страховки, карманные деньги/скидку братьям, субботний режим дневного лагеря, места и итоговый счёт2027.']
    p=by_slug['garenne-robotics-workshop']
    p['programme']='Опция8–12: VEX IQ с датчиками/моторами и VEXcode Blocks; VEX V5 для более опытных по возрасту/уровню. Fusion360/Tinkercad, Bambu Lab3Dпечать, Tinkercad Circuits и основы Python для игры. Это возможные проекты, весь список за три занятия не обещан. Форма/договор2027: три занятияCHF500; PDF на одной странице пишет Three Sessions в заголовке и two sessions в конце. Описаны колонка Bluetooth в3Dкорпусе домой и сертификат прохождения; комплект2027, часы и английский подтвердить.'
    p['questions']=['Подтвердить английский/испанский технического инструктора, фактические часы трёх занятий, задачи для опытных участников, материалы/проект домой, места на общей смене и окончательный счёт2027.']

    p=by_slug['ilc']
    p['price']['label']='Текущий прайс без года: FUN6–9 одна неделяCHF2 915день/3 995пансион, две5 830/7 990; Adrenaline10–13 одна3 015/4 095, две6 030/8 190. Регистрация200за пребывание отдельно, единицу на ребёнка уточнить. Пример двоеFUN на две недели пансиона:2×7 990+2×200+2×2×70стирка+2×350общий трансфер =CHF17 360. Если Матвей10+ вAdrenaline, ещё200 =17 560. Год тарифа неизвестен; это условный расчёт, не предложение2027 или окончательный счёт.'
    p['price']['extras']='СтиркаCHF70/неделя обязательна для двухнедельного пребывания; начисление обоим, применение к дневному формату и другим срокам уточнить. Geneva350за трансфер группы1–2человека: две поездки для двоих вместе700. Для3человек410/поездка,4человек470. UM+160, ночью21–06ещё60. За неделю: теннис420, гольф490, скалолазание/лошади470, дополнительный EN/FR430 по1часу17–18. Только языковые уроки09–12за700/неделя — другой продукт. Перелёт, страховку, другие сборы и год тарифов подтвердить.'
    p['price']['deposit']='Условия без года: при отмене фиксированное удержаниеCHF1 000; рядом перечислены5%при отмене более чем за60дней,25%за60–30,100%менее чем за30. Как сочетаются фиксированное удержание и проценты, неясно; автоматически не суммируем. Это сбор за отмену, не подтверждённый аванс. Действующие условия2027 ещё нужны.'
    p['questions']=['Подтвердить год дат/тарифов, места, FUN/Adrenaline по дню рождения, единицу регистрации, обязательную стирку для выбранного срока/формата, общий трансфер и итоговый счёт. Письменно разъяснить сочетание удержания1000 с процентами отмены.']

    p=by_slug['tecs-puerto-kids']
    p['price']['extras']='Перелёт, страховку и личные расходы уточнить. Трансферы Madrid/Sevilla/Bilbao зависят от набора группы. Страница скидок: два ребёнка25€каждому, бывшим участникам30€, за рекомендацию40€, две программы вместе200€; применимость к2027 ещё не доказана. Ранняя скидка40€до30.04.2026 истекла. Взаимная рекомендация не допускается, корпоративные группы имеют другие условия. Из1730никакие скидки заранее не вычитаем.'
    p['price']['deposit']='Оплата и отмена конкретного сезона ещё неизвестны. Общая информация для потребителя The English Centre Suppliers SL описывает неофициальное обучение, но не заменяет договор лагеря. Страница каталогов всё ещё описывает TECS2026; буклет выдаётся через email-запрос или аккаунт. Контакты не отправлялись, актуальный договор2027 пока не получен.'
    p['questions']=['Подтвердить год дат и пакет за1730€, возраст7+ к заезду, буклет/договор2027, страховку/трансфер, скидку второму ребёнку и итоговый счёт обоим.']
    from camp_americas_v90 import clean_profile
    for q in [by_slug[s] for s in UPDATED]+[stem]:
        clean_profile(q)
        q['programme']=q['programme'].replace('i Pad','iPad')


def extend_report_v94(report):
    # Update current comparisons that contained the now-resolved menu10+ conflict.
    for q in report['shortlist']:
        if q['label']=='Швейцария · разные возрастные треки':
            q['slugs'].insert(q['slugs'].index('village-leysin')+1,'village-leysin-stem')
            q['reason']='JFK по возрасту обоим с6, ноEN ещё не установлен. Régent Labs только Матвею8+. Village Junior7–9 — четыре общие смены; отдельный STEM10–17 только две июльские. Нужны фактические7/10-летия иEN обеих групп. TASIS до7 предлагает Оскару только день.'
        elif q['label']=='Швейцария · школа, ski и инженерная опция':
            q['reason']='Integration5–14 — проба regularschoolclasses после проверки actualgrade/языка. SuperSki8+ требует red-run; English+Ski8+ — другой продукт. Мартовская вторая неделя без лыж. Летний Robotics: конкретные8–12/CHF500/3занятия подтвержденыform/contract2027; прежнееmenu10+ противоречие снято. Оскар6–7 ниже8+, EN/часы ещё неизвестны.'
    report['shortlist'].extend([
        dict(label='Швейцария · обязательные статьи в семейной смете',slugs=['les-elfes','la-garenne','village-leysin','village-leysin-stem'],reason='LesElfes15–28Aug2027: минимальный пример10 280CHFна двух сmandatory150+120/week ивключённымShelter, до дороги/опций. LaGarenne базовые13 680board/12 445dayпосле10%второму одной смены/формата, затемinsurance/pocketmoney/+500robotics Матвею. VillageиюльSTEM+Junior11 000base, но обоим требуются фактические10/7лет иEN. Сметы неfinalinvoice.'),
        dict(label='Франция · сравнить полную двухнедельную смету',slugs=['ilc'],reason='ILCFUN6–9, двое2weeksboard: tuition15 980+registration400+laundry280+sharedGeneva700 =17 360CHFпри указанной механике. Matvey10+Adrenaline добавляет200. Прайс/даты безгода, laundry/regunits ещё подтвердить; неготовое предложение2027. EN/FR15hweek/generaladventure, неробототехнический intensive.')])
    report['gaps'].extend([
        dict(country='Швейцария',iso='CHE',provider='v94 · Summer-specific contract и раздельные Village programmes',detail='LesElfes2027form: mandatory150+120/week, обязательный halfdayworkshop имеет бесплатныйShelter6+. CHF1000deposit входитвцену; summerinsuredcancellation удерживает1000, winterrule500 не перенесён. VillageCP051 теперь толькоJunior7–9/4смены; новыйSTEM10–17/2Julycohorts. EN обоихнеподтверждён; Austriaexcursions наSwissSTEMpage — conflict. Bookingconditions/Leysinbooklet metadata2026, хотяownparent2027ихссылает; travelMay1/May15/signup30days конфликт, неregistrationdeadline. Loyaltyпоhouseholdyears, не2childrenfirstsummerdiscount.',next_action='ФактическиеDOB/уровень/ENinstrutor, actualplaces, финальныеseason2027contracts исемейныйinvoice среальнымиtransfer/insurance/прачечной. Продолжить всех остальныхSwissoperators/worldscope.',url=ELFES),
        dict(country='Швейцария',iso='CHE',provider='v94 · LaGarenne: menu8–9 conflict снят, ноOscar6–7 ниже8+',detail='ТекущийmenuRobotics ужев5–9 и10–12. Form/contract2027 конкретно8–12,500/3sessions, поэтомуOscar6–7 недопущенпоrobotics. WorkshopPDFзаголовокThreeSessions/finaltwo наоднойpage4: осталсяdurationconflict. VEXIQ/V5,Python/3Dиspeaker — списоквозможныхпроектов, неallprojectsза3sessions.9pagecontract relevantpages4/8/9прочитанывизуально:familydiscount/medical10day/65days/28extras. Insuranceчислоdays/ENtechnical неизвестны.',next_action='Проверитьadvancedtasks/реальныеhours/язык Матвею, optionplaces иполныйinvoice; невыдаватьgeneralCampdateзаотдельнуюroboticscohort. ДругиепрограммыШвейцарии продолжаются.',url=G+'summer-camps/'),
        dict(country='Франция / Испания',iso='FRA',provider='v94 · ILC единицы расходов / TECS сезон ещё неизвестен',detail='ILC currentundatedFUNboard7990/2wk,reg200stay,laundry70weekmandatory2wk,transfer350за1–2peoplegroup.17 360длядвух — условнаяформула, не2027quote.1000cancelretention рядом5/25/100%невнятно, несуммированавтоматически. TECSheader2027 противcatalogdescription2026/bodydatesбезгода/1730buttonбезпакета. Early40untilApr30,2026истёк; siblings25perchildнеавтоматически2027. Emailbrochuregated/consumerinfoнеcamprefundcontract; lead/account/subscriptionнеподаны.',next_action='Актуальные2027programmecontracts/fullinvoice/places/ENsupport; остальныеFrance/Spain/Europe иTaiwan/Singapore/Korea/Japan/USA/Canada/LatAm/world остаются вцели. Ничегоорганизаторамнеотправлялось.',url=ILC+'prices')])
    from camp_americas_v90 import readable
    for q in report['shortlist']:
        if q['label'] in ['Швейцария · разные возрастные треки','Швейцария · школа, ski и инженерная опция'] or q in report['shortlist'][-2:]:
            q['reason']=readable(q['reason'])
    for q in report['gaps'][-3:]:
        for k in ['provider','detail','next_action']:q[k]=readable(q[k])
