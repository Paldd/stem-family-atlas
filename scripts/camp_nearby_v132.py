"""Selected nearby curricula and separately registered Mexican VEX categories."""
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '73fdacf3161cab06984573f631682bc4b6dc1831'
CHECKED = '2026-10-06'
CENFO = 'https://ucenfotec.ac.cr/ecommerce/'
MAKERS = CENFO+'producto/ruta-makers-lab/'
AI = CENFO+'producto/ruta-explorador-ia/'
CYBER = CENFO+'producto/ciberheroes-introduccion-a-la-seguridad-digital-y-privacidad/'
TERMS = CENFO+'terminos-y-condiciones/'
CURIOUS = 'https://curiouslabminds.com/'
CEREBRITOS = 'https://www.cerebritosdelfuturo.com/'
ROCKET = 'https://www.rocketgirls.org/rocket-babies'
POLICY = 'https://library.globalrobotics.org/hc/en-us/articles/51371951587732-Student-Eligibility-Policy'
MEXPDF = 'https://www.vexrobotics.com.mx/docs/Comunicado-temporada%202026-2027.pdf'
NEW = ['cenfotec-ai-teen','cenfotec-cyber-teen','curious-heredia-regular','cerebritos-holiday-watch','rocket-babies-workshop']
EVENT_IDS = ['C1155','C1156','C1157','C1158']
UNKNOWN_LANG = 'Язык преподавания прямо не установлен. Испанская страница не подтверждает ES, EN или двуязычный учебный поток; в фильтре подтверждённого языка пока отсутствует.'
REFUND = 'Общие terms: возврат 100% до одного рабочего дня перед курсом, 80% позднее, после начала нет; отмена покупки возможна до часа перед стартом. Однако ниже та же страница ограничивает refund/change семью днями до начала. Это противоречие требует письменных условий конкретного заказа, а не обещания безусловного возврата. Курс могут перенести/отменить при малом наборе, с уведомлением минимум за день и возвратом по запросу.'

def add_nearby_v132(add,src,fit,profiles):
    def emit(i,name,iso,place,themes,age,programme,timing,price,mf,of,sources,kind,
             status='next_unannounced',sessions=None):
        add(NEW[i],name,{'CRI':'Коста-Рика','MEX':'Мексика'}[iso],iso,place,themes,'day',age,UNKNOWN_LANG,
            programme,timing,price,'Без подтверждённого пансиона. Дневной формат не устанавливает полный день: длительность приведена в описании.',mf,of,
            'Кандидат по собственной учебной программе. Независимый мировой рейтинг и личный допуск семьи не установлены; кружок, короткий workshop и каникулярная программа различаются.',
            ['Проверить возрастную группу, язык преподавания, конкретные даты/часы, доступность места, итоговый счёт и возврат.'],
            sources,status=status,sessions=sessions)
        p=profiles[-1];p['checked']=CHECKED;p['programme_type']=kind
        if kind=='holiday_workshop':p['catalog_participation']='holiday_workshop'
        for s in p['sources']:s['checked']=CHECKED
        return p
    tuition=dict(year=2026,label='USD 120 + 2% IVA = USD 122.40 за учебный курс; US$ установлено общими terms, а не только символом $.',
        included='10 часов очного обучения. Не установлен отдельный take-home kit или включённый полный комплект техники.',
        extras='Дорога, семейное жильё, питание, страховка и другие неуказанные расходы отдельно; это не полная поездочная смета.',deposit=REFUND)
    later=fit('later','Оба ребёнка младше опубликованной подростковой группы; это будущая учебная ступень, не нынешнее зачисление.')
    emit(0,'CENFOTEC · Explorador IA · подростковый творческий ИИ','CRI','San José · учебный кабинет/кампус уточнить',
        'ai,art,coding','14–16',
        'Generative AI: prompts, цифровые изображения, творческие истории и этика. Базовый очный курс 10 часов, пять дней по два часа. Это AI literacy/content creation, не соревнование или углублённое обучение моделей.',
        '7–11 декабря 2026, Пн–Пт 10:00–12:00; преподаватель Janet Melissa Vargas Mata. Будущий набор 2027 не опубликован.',
        dict(tuition),later,later,[src('Точные дни 2026, 14–16, syllabus и $120 + IVA',AI),src('Валюта US$ и расходящиеся refund/change clauses',TERMS)],
        'holiday_workshop',status='published_2026',sessions=[['2026-12-07','2026-12-11']])
    emit(1,'CENFOTEC · Ciberhéroes · подростковая цифровая безопасность','CRI','San José · учебный кабинет/кампус уточнить',
        'technology,coding','13–15',
        'Безопасные пароли, персональные данные, digital footprint, phishing и ответственное поведение в сети. Базовые 10 часов очно; это цифровая безопасность, не robotics camp и не юниорский hacking contest.',
        'Старт обозначен «Lunes 7 de diciembre» без года; далее Пн–Пт 10:00–12:00. В отличие от Makers/IA год 2026 здесь явно не напечатан: датированные смены и ICS не создаются.',
        dict(tuition,year=None,label='На текущей странице USD 120 + 2% IVA = USD 122.40; год выбранного набора не указан. Не объявлять прайсом 2027.'),
        later,later,[src('13–15, содержание, 10 часов и декабрь без явного года',CYBER),src('US$ и конфликт общего возврата',TERMS)],'holiday_workshop')
    conditional=fit('conditional','Возраст выше опубликованного минимума 3; конкретную возрастную/уровневую группу, язык и место необходимо подтвердить.')
    emit(2,'Curious Lab Minds · регулярная робототехника Heredia','CRI','Heredia Centro · Centro Comercial Mapache, Local #2',
        'robotics,coding,engineering','Робототехника с 3 лет; верхняя граница и состав групп не опубликованы',
        'Регулярные занятия: LEGO Education, датчики, моторы, контроллеры и laptop/tablet. Ребёнок проектирует решение, строит и программирует, испытывает и представляет работу. Версия набора/язык программирования не указаны. Web development 14+ — другой курс, не программа братьев.',
        'Регулярные занятия по будням и субботам. Точные часы и набор 2026–2027 неизвестны; это возможная постоянная база, не датированный holiday camp.',
        dict(year=None,label='Цена не опубликована.',included='Оборудование описано для занятий; включение в оплату и выдача домой не установлены.',
             extras='Расходники, регулярный взнос, индивидуальные занятия, дорога и соревнования отдельно уточнить.',deposit='Договор, оплата и отмена не опубликованы.'),
        conditional,conditional,[src('3+, адрес, регулярные дни и учебный процесс LEGO',CURIOUS)],'regular_learning')
    unknown=fit('unknown','Возрастной диапазон индивидуального клуба/мини-лагеря не опубликован; нельзя считать допуск братьев подтверждённым.')
    emit(3,'Cerebritos del Futuro · каникулы и клуб Playa del Carmen','MEX','Playa del Carmen · точный адрес площадки уточнить',
        'robotics,engineering,technology', 'Возраст клуба и каникулярных mini camps неизвестен',
        'Робототехника, 3D-дизайн и 3D-печать; regular club и утренние mini camps на каникулах. Школьные/mobile/Home Schools услуги адресованы группам и учреждениям, не обещают индивидуальное семейное зачисление. Собственные заявления о призах не содержат сезона/лиги/team ID и не внесены как доказанные международные результаты.',
        'Клуб Пн–Пт 16:00–17:30 или 18:00–19:30. Mini camps утром на Semana Santa, в декабре и летом; конкретных дат, часов, года набора и мест нет. Смены 2026–2027 в календарь не придуманы.',
        dict(year=None,label='Прайс клуба и mini camp не опубликован.',included='Учебные направления описаны, но комплект и объём включённых материалов неизвестны.',
             extras='Жильё семьи, транспорт, питание и техника отдельно уточнить.',deposit='Аванс, отмена и возврат неизвестны.'),
        unknown,unknown,[src('Клуб, часы и сезонность mini camps',CEREBRITOS),src('Собственные неподтверждённые истории результатов',CEREBRITOS+'copy-of-qui%C3%A9nes-somos'),src('Услуги учебным группам не индивидуальный admission',CEREBRITOS+'home-schools')],'holiday_camp_and_regular_learning')
    gender=fit('unknown','Заголовок адресован девочкам, FAQ говорит о детях обоих полов; допуск мальчиков на конкретный открытый workshop пока не установлен. Возраст 6+ проверять на день занятия.')
    emit(4,'Rocket Babies · короткие открытые STEAM workshops','CRI','CETAV, Fátima de Desamparados · конкретный workshop уточнить',
        'science,robotics,ai,games','В заголовке девочки 6–13; смешанные формулировки FAQ требуют уточнения допуска мальчиков',
        'Трёхчасовые практические STEAM workshops: от простых цепей до знакомства с AI; FAQ перечисляет programming, игры, chemistry и robotics. Тема каждого объявления отдельная: нельзя обещать одновременно все направления. Participation certificate не международная победа.',
        'Часть занятий открыта публике в CETAV; другие проходят по школьным/корпоративным партнёрствам. Объявления минимум за месяц; точных дат 2026–2027 на прочитанной странице нет.',
        dict(year=None,label='CRC 33 000 за workshop, IVA включён; конкретный сезон/дата тарифа не указаны.',included='Материалы, перекус, сертификат участия.',
             extras='Транспорт, сопровождающие, жильё и прочие расходы отдельно; не полный лагерь/поездочный пакет.',deposit='Условия оплаты/возврата выбранного объявления неизвестны.'),
        gender,gender,[src('3 часа, 6–13, CRC/IVA, открытые и школьные занятия; гендерное противоречие',ROCKET)],'workshop')

def extend_report_v132(r):
    r.update(version=132,asof=CHECKED)
    p=next(p for p in r['profiles'] if p['slug']=='cenfotec-makers')
    p['checked']=CHECKED
    for s in p['sources']:s['checked']=CHECKED
    if not any(s['url']==TERMS for s in p['sources']):
        p['sources'].append(dict(title='Общие покупки: US$ и конфликт сроков возврата',url=TERMS,checked=CHECKED))
    p['price']['label']='USD 180 + 2% IVA = USD 183.60 за workshop до неизвестных доплат. US$ дополнительно подтверждено общими terms; это не семейная поездочная смета.'
    p['price']['deposit']=REFUND
    p['questions'] += ['Согласовать применимое правило возврата: один рабочий день / семь дней до курса на одной общей странице расходятся.']
    r['shortlist'] += [dict(label='Коста-Рика и Мексика · регулярная база и каникулярные кандидаты',slugs=NEW[2:],reason='Heredia 3+ — ближайший условный кандидат регулярного LEGO обучения. Playa del Carmen mini camps без точных дат/возраста; Rocket Babies с противоречивым допуском мальчиков. EN/ES teaching ещё не доказан.'),
        dict(label='CENFOTEC · будущие ступени с разными возрастами',slugs=['cenfotec-makers']+NEW[:2],reason='Makers 10–12, Cyber 13–15, IA 14–16. Makers и IA имеют 7–11 декабря 2026; Cyber не печатает год. В декабре 2026 братья младше всех трёх треков.')]
    gaps=[('CRI','CENFOTEC · возврат и младший набор',TERMS,'Одна страница содержит refund до рабочего дня и семь дней до старта. Makers 10–12, Cyber 13–15, IA 14–16 не младшие 6–9; цены с IVA не полный поездочный счёт.'),
        ('CRI','CENFOTEC · Cyber без года',CYBER,'Monday 7 December и Пн–Пт без напечатанного года недостаточны для точной смены 2026 или 2027. Нет нового календарного ряда.'),
        ('CRI','Curious Lab Minds · регулярная база',CURIOUS,'Робототехника 3+ и адрес подтверждены; конкретная группа, верхний возраст, язык преподавания, fees и участие в официальной лиге неизвестны. Mobile service не семейный camp admission.'),
        ('MEX','Cerebritos · дата/возраст и доказательства результата',CEREBRITOS,'Есть сезонные mini camps и часы клуба, но нет точных дней, возраста, fees или EN teaching. Победы в собственном описании без team ID/лиги/сезона не включены в school retrospective.'),
        ('CRI','Rocket Babies · допуск мальчиков',ROCKET,'Заголовок girls 6–13 расходится с boys/girls в FAQ. Публичные workshops и institutional alliances различаются; дата/язык/refund неизвестны. 3 часа не пансион или полный день.'),
        ('MEX','Liota · недостаточная новая первичная выдача','https://liotacamps.com/','Обычный HTTP вернул JS shell без условий. Search snippet не разрешает прежние Winter 19 дней / четыре недели, возраст и тариф. Старое досье сохранено; новые даты, EN и цены не выведены из сниппета.')]
    r['gaps'] += [dict(iso=iso,country={'CRI':'Коста-Рика','MEX':'Мексика'}[iso],provider='v132 · '+title,url=url,detail=detail,
        next_action='Продолжить первичные условия местных и всех мировых приоритетных программ; полностью изученных стран по-прежнему 0.') for iso,title,url,detail in gaps]
    review=r['family_review'];ps={p['slug']:p for p in r['profiles']}
    assert not any(q['slug']=='curious-heredia-regular' for q in review['entries'])
    review['entries'].append(dict(slug='curious-heredia-regular',goals=['technical'],reason='Проверить регулярную LEGO Education базу рядом с домом, начиная с подходящей возрастной/уровневой группы.',
        key_limit='Это кружок с опубликованным минимумом 3+, не датированный лагерь; язык, часы, цена, уровень и официальный соревновательный трек ещё неизвестны.',dossier_checked=CHECKED))
    review.update(version=132,asof=CHECKED)
    review['coverage']=dict(candidates=len(review['entries']),countries=len({ps[q['slug']]['iso'] for q in review['entries']}),fully_audited_countries=0)
    r['counts']=dict(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),swiss=sum(p['iso']=='CHE' for p in r['profiles']),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))

def enrich_v132(d):
    specs=[
        ('C1155','RE-VIQRC-26-5506','XVIII Campeonato Nacional de Robótica y STEM · VEX IQ Middle','2027-03-03','2027-03-05','Puebla','iq','Middle School','open_application',
         'Портал USD 0; body обещает опубликовать стоимость на Academia STEM. Итоговая цена не установлена — не объявлять бесплатно.',
         'Центр Puebla · Blvd. Héroes del 5 de Mayo 402, Centro histórico, 72000',40,'notebook на бумаге или USB','Национальный этап; Awards/квота Worlds на прочитанной карточке не установлены.'),
        ('C1156','RE-VIQRC-26-5423','Torneo Estatal de Chihuahua · VEX IQ Middle','2027-01-26','2027-01-26','Ciudad Juárez','iq','Middle School','invitation',
         'Карточка FREE; годовая команда, техника, поездка и возможные внешние взносы отдельно. Refund No Aplica не полный договор семьи.',
         'Universidad Tecnológica de Ciudad Juárez · Av. Universidad Tecnológica 3051, Lote Bravo II, 32695',99,'физический engineering notebook',
         'Региональный этап. Type Open Tournament, но Format In-Person Invitational и приветствие командам Chihuahua; иностранный/другой штат отдельно. Payment 26/ene/2026 расходится с 2027 и не стало новым deadline.'),
        ('C1157','RE-V5RC-26-5511','XVIII Campeonato Nacional de Robótica y STEM · VEX V5 High','2027-03-03','2027-03-05','Puebla','v5','High School','open_application',
         'Портал USD 0; стоимость будет опубликована на Academia STEM. FREE или полный пакет семьи не подтверждены.',
         'Центр Puebla · Blvd. Héroes del 5 de Mayo 402, Centro histórico, 72000',99,'notebook на бумаге или USB','Национальная категория V5 High; не тот же robot/уровень, что IQ. Worlds quota не установлена.'),
        ('C1158','RE-V5RC-26-5435','VII Campeonato Internacional de Robótica y habilidades STEM · VEX V5 High','2027-01-27','2027-01-29','Ciudad Juárez','v5','High School','open_application',
         'Карточка FREE; команда, робот, поле, поездка и внешние взносы отдельно. Refund No Aplica не полная гарантия возврата.',
         'Universidad Tecnológica de Ciudad Juárez · Av. Universidad Tecnológica 3051, Lote Bravo II, 32695',98,'физический engineering notebook',
         'Турнир с международным названием, не мировой финал. Payment 27/ene/26 расходится с 2027; в карточке есть шаблон judging. VURC/AI Skills Yes не даёт автоматически U/AI-заявку в V5 High.')]
    rows=[]
    for ident,code,title,start,end,city,program,grade,admission,cost,venue,capacity,notebook,note in specs:
        iq=program=='iq';url='https://events.vex.com/robot-competitions/'+('vex-iq-competition/' if iq else 'vex-robotics-competition/')+code+'.html'
        age='IQ Middle: максимум 15 лет на 01.06.2027; 2+ учащихся в команде' if iq else 'V5 High: максимум 19 на 01.06.2027 и не окончил secondary school; 1+ учащихся'
        gate='Условно по верхней возрастной рамке; нижний возраст/местный grade-допуск, выбранный уровень и сложность проверить. Для старта братьев сначала IQ Elementary, не автоматическая запись в эту категорию.'
        rows.append(dict(block='Соревнования',id=ident,title=title,country='Мексика',region='Северная Америка',city=city,start=start,end=end,period='',date_status='Подтверждено',
            deadline=start,deadline_utc=start+'T17:00:00Z',deadline_label='Регистрация VEX',deadline_note='Карточка: 12:00 EST в день начала = 17:00 UTC = 11:00 Коста-Рика. Это регистрация, не ошибочное Payment поле 2026.',
            age=age,mat=gate,osc=gate,format=('Зарегистрированная IQ команда 2+' if iq else 'Зарегистрированная V5 команда 1+')+' и взрослый наставник; один уровень в программе одновременно.',
            entry='Подтвердить VEX-ID 2026/27, local/foreign eligibility, '+grade+', состав и доступность; Open Tournament не персональное принятие.',
            gear='VEX IQ Level Up; IQ robot/manual, notebook; LEGO/V5 не заменяют' if iq else 'VEX V5 Override; V5 robot/manual, notebook; IQ/LEGO не заменяют',
            language='ES/EN судейство и notebook для этой команды ещё не подтверждены; испанский body не гарантия языка.',languages=[],language_mode='unconfirmed',language_certainty='Учебный/судейский язык прямо не установлен выбранной карточкой.',
            cost=cost,scope='national' if '5511' in code or '5506' in code else 'regional',level='B — национальный этап' if 'Nacional' in title else 'C — региональный турнир',
            importance_reason='Отдельная официальная категория; национальное/международное название не равно мировому финалу или подтверждённой квоте.',reward='Награды, отбор и квоту Worlds проверить отдельно; победа семьи не заявляется.',
            priority='P3 — отдельная категория после проверки уровня',action='Выбрать Elementary маршрут или подтвердить именно '+grade+'; подготовить '+notebook+', робот и согласовать местный допуск/цену.',
            source=url,references=[dict(label='Сезонный возраст и команда',url=POLICY),dict(label='Мексиканский сезон 2026–2027, VEX-ID и порталы',url=MEXPDF)],
            proof='Выбранные поля собственной карточки прочитаны web primary reader; прямой HTTP 403 не представлен как сохранённый текст. Дата/категория подтверждены, актуальные свободные места и admission семьи нет.',
            checked=CHECKED,status='Идея',note=note+' Очное судейство и Skills Yes; '+notebook+'. Capacity '+str(capacity)+' — лимит, не обещание текущего места. Политика возраста не публикует здесь нижний порог; возраст братьев не причина выдумать отказ.',
            iso=['MEX'],themes=['robotics','makers','coding'],participation='team',related_ids=['C024'],event_code=code,event_region='Mexico',venue=venue,admission_kind=admission,
            evidence_level='event_page',registration_status='Прочитан публичный снимок карточки; live остаток мест/учётная запись/регистрация не проверялись.',event_type='Open Tournament',grade_level=grade))
    existing={e['event_code']:e['id'] for e in d['events'] if e.get('event_code') and e['id'] not in EVENT_IDS}
    assert not set(existing)&{e['event_code'] for e in rows}, 'Do not duplicate an existing category under a new ID'
    d['events']=[e for e in d['events'] if e['id'] not in EVENT_IDS]+rows
    guide=d['league_guide'];p=next(p for p in guide['profiles'] if p['id']=='vex')
    for ident in EVENT_IDS:
        if ident not in p['event_ids']:p['event_ids'].append(ident)
    nuance='v132 · Мексика: Puebla 3–5 марта 2027 IQ Middle/V5 High, Chihuahua 26 января IQ Middle и Juárez 27–29 января V5 High — отдельные категории. June 1 age caps не задают нижний возраст; подтверждать уровень и местный допуск. Братьям первично сравнить IQ Elementary C180/C513/C514/C597. USD 0 на национальном портале не окончательный fee; Chihuahua Invitational и payment year 2026 требуют уточнения.'
    if nuance not in p['nuances']:p['nuances'].append(nuance)
    for e in rows:
        if not any(s['url']==e['source'] for s in p['sources']):p['sources'].append(dict(title=e['title'],url=e['source'],checked=CHECKED))
    guide.update(version=132,checked=CHECKED)
    urls={s['url'] for s in d['sources']}
    for title,url in [(e['title'],e['source']) for e in rows]+[('Мексиканский VEX сезон 2026–2027: первичный communiqué',MEXPDF)]:
        if url not in urls:d['sources'].append(dict(title=title,url=url,checked=CHECKED,evidence='Выбранная первичная категория/сезон; не принятие семьи или полная проверка страны.'));urls.add(url)
    d['family_strategy']['nearby_participation_v132']=dict(version=132,checked=CHECKED,status='editorial_plan_unconfirmed_admission',
        scope='Дополнение местной базы и отдельных мексиканских категорий; прежний план v118 сохранён.',
        local_base='Curious Heredia 3+ условно обоим: сначала уровень, язык, расписание и цена. Cerebritos Playa mini camps — возраст/дни ещё неизвестны.',
        future='CENFOTEC Makers 10–12, Cyber 13–15, IA 14–16. Декабрьские 2026 курсы не подходят братьям по возрасту.',
        first_competition_ids=['C180','C513','C514','C597'],additional_category_ids=EVENT_IDS,
        limitation='Elementary карточки не удалось заново прочитать в этом проходе: их прежние checked/facts сохранены. Новые Middle/V5 страницы не подтверждают места Elementary или Worlds квоту.',
        route=['Подобрать регулярную команду/наставника, определить самостоятельный уровень каждого.',
            'Для общего старта проверить IQ Elementary 2+ и VEX-ID; оборудование Level Up и детский notebook.',
            'Сравнить существующие Elementary выезды Chihuahua/Juárez/Puebla; подтвердить приглашение, международный допуск, цену и отбор.',
            'Middle/V5 выбирать после готовности и местного согласования категории; международный заголовок не гарантирует награды.'])
