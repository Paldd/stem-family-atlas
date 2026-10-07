"""Append the primary-source holiday and game-event pass to the v12 inventory."""
import copy, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=ROOT/'data/catalog.json';d=json.loads(p.read_text());DAY='2026-09-30'
assert len(d['events'])==1008 and d['completeness_audit']['version']==12, 'Run once against v12'
before={e['id'] for e in d['events']};baseline=copy.deepcopy(d['completeness_audit']['counts']);new=[];updated=[];promoted=[]
byid={e['id']:e for e in d['events']}
def source(url,title,evidence='Первичная страница прочитана; ограничения указаны в карточке.'):
    old=next((s for s in d['sources'] if s['url']==url),None)
    if old: old.update(checked=DAY,evidence=evidence)
    else: d['sources'].append(dict(url=url,title=title,evidence=evidence,checked=DAY))
def add(id,block,title,country,region,city,url,start='',end='',**kw):
    assert id not in before|set(new)
    e=dict(id=id,block=block,title=title,country=country,region=region,city=city,start=start,end=end or start,
        period='' if start else 'Будущие точные дни выбранного курса не подтверждены',date_status='Подтверждено' if start else 'Даты не объявлены',
        deadline='',age='Условия уточнить',mat='Условно — подтвердить допуск',osc='Условно — подтвердить допуск',format='Посещение / программа',
        entry='Выбрать конкретный выпуск и получить подтверждение допуска.',gear='По программе',language='Язык конкретной активности не подтверждён',languages=[],
        language_certainty='Язык сайта не доказывает язык преподавания или поддержки семьи.',cost='Тариф выбранного варианта уточнить',
        level='Образовательное событие',scope='local',importance_reason='Редакционный ориентир по опубликованной программе и географии; не официальный мировой рейтинг.',
        reward='Обучение / посещение; не соревновательная победа',priority='P2 — после проверки допуска и наличия мест',
        action='Подтвердить возраст на дату события, язык, места и условия регистрации.',source=url,references=[],proof='Прочитан первичный источник; неизвестные условия выделены отдельно.',
        checked=DAY,status='Идея',note='',themes=['technology'],participation='day_camp' if block=='Лагеря' else 'visitor',
        admission_kind='program' if block=='Лагеря' else 'visitor',evidence_level='program' if block=='Лагеря' else 'event_page',
        registration_status='Семья не записана; дата и опубликованный тариф не гарантируют наличие мест.')
    e.update(kw);d['events'].append(e);new.append(id);source(url,title);return e
def curate(e,policy,highlights,tier='global'):
    e.update(exhibition_tier=tier,visitor_policy=policy,visitor_policy_note=e['age'],adult_entry=e['entry'],highlights=highlights,
        exhibitors=[],exhibitor_note='Имена компаний выбранного выпуска не проверены; прошлый список не гарантирует участие в новом сезоне.',
        exhibitor_directory_url=e['source'],event_group=e['title'].split('202')[0].strip(),admission_kind='visitor')

# Exactly nine dated local Junior offerings. The generic LEGO 6+ course does
# not make robotics available in every Zurich week.
tsa='https://zurich.techsparkacademy.ch/zurich-day-camps/'
robot='https://online.techsparkacademy.ch/robotics-course/'
weeks=[('2026-10-06','2026-10-09','Bleicherweg 27','09:30–15:00',790),('2026-10-13','2026-10-16','Freies Gymnasium Zürich, Arbenzstrasse 19','10:00–15:30',790),
    ('2027-04-26','2027-04-29','Freies Gymnasium Zürich, Arbenzstrasse 19','10:00–15:30',790),('2027-05-03','2027-05-05','Bleicherweg 27','09:30–15:00',645),
    ('2027-06-21','2027-06-25','Bleicherweg 27','09:30–15:00',890),('2027-07-19','2027-07-23','Freies Gymnasium Zürich, Arbenzstrasse 19','10:00–15:30',890),
    ('2027-08-16','2027-08-20','Bleicherweg 27','09:30–15:00',890),('2027-10-11','2027-10-14','Bleicherweg 27','09:30–15:00',790),
    ('2027-10-19','2027-10-22','Freies Gymnasium Zürich, Arbenzstrasse 19','10:00–15:30',790)]
for n,(start,end,venue,hours,price) in enumerate(weeks,122):
    add(f'L{n:03}','Лагеря',f'TechSpark Zürich · Animation / Game Design Junior · {start}','Швейцария','Европа','Zürich',tsa,start,end,
        age='Animation / Game Design Junior: от 7 лет; Python Junior — отдельный курс от 10',mat='Да по возрасту для Game Design 7+; наличие места подтвердить',
        osc='Нет в 6 лет: минимум 7' if start.startswith('2026') else 'Условно: если к смене исполнится 7; дата рождения не известна',
        format=f'Дневная смена без проживания; {hours} по опубликованному расписанию площадки',venue=venue,
        entry='Выбрать Junior Animation / Game Design, точную неделю и площадку; подтвердить возраст и способность следовать инструкциям на английском.',
        gear='Инструменты выбранного Junior-курса; аренду / включение ноутбука уточнить при записи',language='EN — основное преподавание, если описание курса не задаёт исключение',
        languages=['EN'],language_certainty='FAQ филиала: курсы обычно на английском; нужно понимать базовые устные и письменные инструкции. Поддержка DE/FR зависит от преподавателя.',
        cost=f'Junior CHF {price}; включение обеда и выбранного оборудования уточнить',level='D — обучение',themes=['games','coding'],
        note='На этой датированной сетке опубликованы Animation / Game Design Junior 7+, не Robotics LEGO 6+. Общий каталог курсов нельзя автоматически перенести на каждую неделю. Состояние мест и приём иностранного ребёнка не проверены.',
        references=[dict(url=robot,label='Отдельный общий курс Robotics LEGO Junior 6+: его доступность по датам не доказана')])
add('L131','Лагеря','TechSpark · Robotics LEGO Junior 6+ · смену согласовать','Швейцария','Европа','Филиал и конкретная смена ещё не выбраны',robot,
    age='Robotics LEGO Junior: от 6 лет; Arduino Robotics — другой курс от 12',mat='Да по возрасту; нужен подтверждённый LEGO-поток',osc='Да по возрасту; нужен подтверждённый LEGO-поток',
    format='Очный Junior-курс; будущая робототехническая смена и длительность не подтверждены',participation='regular',
    entry='Запросить именно Robotics LEGO Junior 6+ на нужные каникулы; получить конкретные дни, площадку и язык.',gear='LEGO Robotics Junior; оборудование выбранного курса',
    language='EN / DE / FR — опубликованные языковые варианты; нужный поток согласовать',languages=['EN'],language_certainty='Общая Robotics course page указывает EN/DE/FR для Junior; это выбор вариантов, не гарантия EN на выбранной неделе.',
    themes=['robotics','coding'],level='D — обучение',note='Страница общего курса содержит календарь лагерей, однако датированная сетка Zürich предлагает Game Design 7+. Не создано фиктивных робототехнических смен из общего календаря.',
    references=[dict(url=tsa,label='Zürich: реальные датированные курсы отличаются от общего каталога')])

ntk='https://newtechkids.com/en/'
for n,start,end,title in [(132,'2026-10-12','2026-10-16','Autumn: robots and art'),(133,'2026-12-21','2026-12-24','Before Christmas: film robots'),(134,'2026-12-28','2026-12-31','After Christmas: robots and art')]:
    add(f'L{n}','Лагеря',f'NewTechKids Amsterdam · {title} 2026','Нидерланды','Европа','Amsterdam Public Library near Centraal Station',ntk,start,end,
        age='8–12 лет',mat='Да по возрасту; EN-поддержку и место подтвердить',osc='Нет — минимум 8 лет',format='Дневной bootcamp; точные часы и тариф не указаны на прочитанной главной',
        entry='Выбрать Holiday bootcamp по официальной ссылке регистрации; подтвердить английскую поддержку для ребёнка без нидерландского и приём иностранной семьи.',
        gear='LEGO-роботы, задачи и работа в парах',language='EN / NL — двуязычные занятия',languages=['EN'],
        language_certainty='Организатор прямо описывает двуязычные программы EN/NL; полное сопровождение только на EN не обещано.',themes=['robotics','coding','games'],
        level='D — обучение',note='Бесплатный / льготный Stadspas для отдельных жителей Amsterdam не является общим тарифом иностранной семьи. Наличие места, расписание и оплата уточняются отдельно.')

bricks='https://bricks4kidz.us/tennessee-franklin/2026-fall-winter-lego-camps/'
for n,start,end,title,cost in [(135,'2026-10-12','2026-10-16','Fall Break','$339 за 5 полных дней; $215 за половины дня; полный разовый день $79'),
    (136,'2026-11-23','2026-11-25','Thanksgiving','$199 за 3 полных дня; $129 за половины дня; разовый полный / половина $79 / $49'),
    (137,'2026-12-21','2026-12-24','Winter week 1','$279 за 4 полных дня; $169 за половины дня; разовый полный / половина $79 / $49'),
    (138,'2026-12-28','2026-12-31','Winter week 2','$279 за 4 полных дня; $169 за половины дня; разовый полный / половина $79 / $49')]:
    add(f'L{n}','Лагеря',f'Bricks4Kidz Franklin · {title} 2026','США','Северная Америка','Franklin, Tennessee · Dance Mania Studio',bricks,start,end,
        age='5–12 лет',mat='Да по возрасту; иностранный приём и места уточнить',osc='Да по возрасту; иностранный приём и места уточнить',
        format='Полный день 09:00–15:00; варианты половины дня или отдельных дней',entry='Официальная регистрация Bricks4Kidz: выбрать смену и полный / половину дня; подтвердить язык преподавания и документы иностранного ребёнка.',
        gear='LEGO, инженерные задачи, робототехника / программирование по программе смены',language='EN кандидат: преподавание на английском прямо не подтверждено',languages=[],
        language_certainty='Нельзя считать англоязычный сайт и местоположение США доказательством языка преподавания. EN требуется подтвердить до записи.',
        cost=cost,level='D — обучение',themes=['robotics','coding','technology'],
        note='Возраст, точные дни, дневные варианты и тарифы опубликованы; гарантии роботов или выбранной темы в каждый день нет. Язык EN/ES и иностранный приём неизвестны; в EN-фильтр карточка не включена.')

# Public exhibition dates exclude dedicated business/media days.
e=add('E113','События','PAX Unplugged Philadelphia 2026','США','Северная Америка','Philadelphia · Pennsylvania Convention Center',
    'https://unplugged.paxsite.com/philly/en-us.html','2026-12-04','2026-12-06',
    age='FAQ: до 6 включительно бесплатно со взрослым с badge; детский badge 7–12. FAQ и продажа расходятся по детским дням.',mat='Да по возрасту; проверить вариант Kids badge',osc='Да по возрасту; бесплатный проход до 6 включительно по FAQ, возраст на день визита уточнить',
    format='Публичная выставка настольных игр; expo hall 10:00–18:00',entry='Официальный visitor badge; отдельные турниры и игровые столы могут требовать дополнительной записи.',gear='Не нужен для входа',
    language='EN; язык выбранного игрового стола отдельно',cost='Страница продажи: Kids 3-Day $47.25, Kids single day $21. FAQ ещё пишет Sunday-only; подтвердить перед покупкой.',
    scope='international',level='E — игровая выставка',themes=['games'],priority='P3 — посещение при удобной поездке',
    note='Это tabletop / board games, не робототехническая выставка компаний. Продажа предлагает Kids на все дни, а FAQ говорит о Sunday-only; конфликт сохранён. Билет посетителя не является регистрацией в турнир.',
    references=[dict(url='https://unplugged.paxsite.com/philly/en-us/info/faq.html',label='FAQ: возраст / Sunday-only'),dict(url='https://unplugged.paxsite.com/philly/en-us/registration/buy-badges.html',label='Продажа: Kids 3-Day и отдельные дни')])
curate(e,'family',['Настольные игры','Игровые столы и демо','Турниры с отдельными правилами'])
e=add('E114','События','PAX Unplugged Houston 2027','США','Северная Америка','Houston · George R. Brown Convention Center',
    'https://unplugged.paxsite.com/houston/en-us.html','2027-06-25','2027-06-27',age='Билеты Coming Soon; возрастные правила Houston 2027 ещё не опубликованы в прочитанном источнике',
    format='Публичная tabletop выставка; expo hall 10:00–18:00',entry='Дождаться собственных Houston badge / FAQ; не переносить тариф Philadelphia.',gear='Не нужен для входа',
    themes=['games'],scope='international',level='E — игровая выставка',priority='P3 — посещение при удобной поездке',note='Philadelphia и Houston — разные издания; детский возраст и бесплатные билеты одного не применены автоматически к другому.')
curate(e,'confirm_children',['Настольные игры','Expo hall','Игровые активности'])
e=add('E115','События','PAX East Boston 2027','США','Северная Америка','Boston · Thomas M. Menino Convention & Exhibition Center',
    'https://east.paxsite.com/en-us/info/faq.html','2027-04-22','2027-04-25',age='FAQ: all ages; отдельные 13+ активности и контент имеют ограничения',mat='Да по возрасту; выбирать детский контент',osc='Да по возрасту; выбирать детский контент',
    format='Публичная игровая выставка / фестиваль',entry='Visitor badge и сопровождение родителем; турниры проверяются отдельно, часто first come / предварительная запись.',gear='Не нужен для входа',
    themes=['games','technology'],scope='international',level='E — игровая выставка',priority='P3 — посещение при удобной поездке',
    note='Страница текущего издания даёт 22–25 апреля; старый сетевой пункт навигации Apr 21 не выбран как дата. Детский тариф / бесплатный проход 2027 не подтверждены.')
curate(e,'family',['Игровые демо','Панели и фестиваль','Турниры: отдельный допуск'])
e=add('E116','События','gamescom asia Thailand 2026 · публичные дни','Таиланд','Азия','Bangkok · Queen Sirikit National Convention Center',
    'https://gamescom.asia/ent/b2c-faqs','2026-10-30','2026-11-01',age='Дети до 12 включительно со взрослым; бесплатный проход зависит от роста, не возраста',mat='Да по возрасту со взрослым; измерить рост',osc='Да по возрасту со взрослым; измерить рост',
    format='Public Entertainment area; 29 октября — отдельный business day',entry='Публичный билет на 30 октября – 1 ноября; взрослый сопровождает ребёнка.',gear='Не нужен для входа',
    cost='FAQ: рост ниже 110 см бесплатно; выше 110 см детский дневной 200 THB / fast track 300 THB. Ровно 110 см уточнить.',themes=['games','technology'],
    scope='international',level='E — игровая выставка',priority='P3 — посещение при удобной поездке',note='Общая шапка фестиваля 29 октября – 1 ноября включает B2B. В семейный календарь внесены только публичные дни 30 октября – 1 ноября. Возрастной рейтинг игры проверяется отдельно.')
curate(e,'family',['Игры и entertainment','Региональная индустрия игр','Публичные демо'])
e=add('E117','События','Taipei Game Show 2027 · B2C public zone','Тайвань','Азия','Taipei · TaiNEX 1, Nangang Exhibition Center Hall 1',
    'https://tgs.tca.org.tw/?p=event_info_e','2027-01-21','2027-01-24',age='B2C публичная зона; конкретный детский допуск 6/9 и тариф текущего выпуска не подтверждены',
    format='B2C публичная игровая выставка',entry='Отдельный B2C ticket; подтвердить детский вход. B2B / APGS 21–22 января — другая категория.',gear='Не нужен для входа',
    themes=['games','technology'],scope='international',level='E — игровая выставка',priority='P3 — посещение при удобной поездке',note='Публичные дни 21–24 января подтверждены; возрастные правила 2023 или других шоу Тайваня не перенесены на 2027.')
curate(e,'confirm_children',['B2C game exhibition','Отдельная B2B зона','APGS — отдельная программа'])
e=add('E118','События','G-STAR Busan 2026 · BTC exhibition','Южная Корея','Азия','Busan · BEXCO',
    'https://gstar.or.kr/gstar/gstar_info.do','2026-11-19','2026-11-22',age='BTC visitor programme; возрастной допуск 6/9 не указан в прочитанном overview',
    format='Публичная игровая BTC-выставка; B2B / G-CON отдельно',entry='Visitor ticket текущего BTC-издания; уточнить детские условия у организатора.',gear='Не нужен для входа',
    themes=['games','technology'],scope='international',level='E — игровая выставка',priority='P3 — посещение при удобной поездке',note='Game Awards 18 ноября не являются публичным днём BTC. Тарифы и правила из архивных выпусков не перенесены на 2026.')
curate(e,'confirm_children',['Корейская игровая индустрия','BTC game demos','Отдельные B2B / G-CON форматы'])
add('E119','События','EU Code Week 2026 · карта местных активностей','Мир / Европа','Европа','Местные площадки / онлайн по карте активности',
    'https://codeweek.eu/blog/eu-code-week-2026-october-events/','2026-10-10','2026-10-25',age='Нет одного возрастного допуска: возраст и язык каждой активности на карте отдельные',
    format='Сеть практических coding / digital skills активностей; не одна выставочная площадка',entry='Найти на официальной карте подходящий детский workshop и его собственную запись; общий период сети не гарантирует занятие каждый день.',
    gear='По workshop',themes=['coding','ai','games','technology'],scope='international',level='E — образовательная сеть',priority='P2 — после выбора конкретной активности',
    date_scope='festival_window',note='10–25 октября — окно кампании по Европе. Учительские вебинары и policy launch не приравнены к детскому лагерю или соревнованию. Язык EN/ES выбранной детской активности пока не подтверждён.')

# Existing game events become discoverable in the curated major-expo view;
# retain all existing records and source-year uncertainties.
policies={'E034':'family','E035':'family','E036':'family','E037':'confirm_children','E038':'family','E039':'family','E040':'confirm_children','E079':'confirm_children'}
for id,policy in policies.items():
    e=byid[id];curate(e,policy,['Игровые демонстрации','Публичный visitor programme','Ограничения отдельных игр / турниров'])
    promoted.append(id)
byid['E034']['note']+=' Повторно opening-times / visitors вернули только заголовок; точные дни 2027 не перенесены из поискового фрагмента в подтверждённый календарь.'
byid['E035']['references']=[dict(url='https://latam.gamescom.global/en/terms-of-use/',label='Текущие общие условия: младше 14 с сопровождающим')]
byid['E036']['references']=[dict(url='https://www.parisgamesweek.com/fr/billetterie/billet-2-jours-open',label='2-day Open: до 8 €0 / 8–25 €34'),dict(url='https://www.parisgamesweek.com/fr/espaces/pgw-family',label='Семейная зона')]
byid['E039']['references']=[dict(url='https://aus.paxsite.com/en-us/terms-and-conditions.html',label='Terms: badge с 6; FAQ: бесплатно до 6 включительно')]
byid['E039']['proof']='Повторно прочитаны FAQ и Terms: даты 9–11 октября подтверждены; противоречие по badge ровно в 6 лет осталось.'
updated+=['E034','E035','E036','E039']
for id in ['L116','L117','L118']:
    byid[id]['checked']=DAY;byid[id]['proof']='Повторно прочитана services page: Christmas Diciembre 2026, Easter / Summer Próximo 2027; точные дни и возраст лагерей не объявлены.'
    updated.append(id)
source('https://www.ciberbots.com.mx/services','Ciberbots México: holiday programmes','Christmas 2026 / Easter and Summer 2027 подтверждены только как периоды; школьные возраста не применены к лагерям.')

bafta='https://www.bafta.org/programmes/young-game-designer/'
add('C776','Соревнования','BAFTA Young Game Designers · следующая заявка','Великобритания','Европа','UK residents / online submission',bafta,
    age='2026: 10–14 / 15–18; UK residents, до 16 — родитель / опекун тоже UK resident',mat='Нет сейчас — 9 лет и проживание в Costa Rica',osc='Нет — 6 лет и проживание в Costa Rica',
    format='Индивидуально / пара / команда до 3; все в одной возрастной группе',participation='individual_or_team',admission_kind='direct',evidence_level='rules',
    entry='Следующий call и требования резидентства проверить; текущая семейная заявка недоступна.',gear='Game Concept либо Game Making: оригинальная идея / playable level',
    themes=['games','coding'],scope='national',level='Национальная программа BAFTA',priority='P4 — семья сейчас не соответствует требованиям',
    reward='YGD award при победе; международная поездка или участие не заменяют UK eligibility',registration_status='Заявки 2026 закрыты; следующий набор не опубликован',
    note='Правила 2026 относятся к school year с 3 сентября 2025 (Scotland 13 августа). Возраст 10 сам по себе не открывает допуск семье из Costa Rica. Использование AI нужно раскрывать; самостоятельная работа оценивается отдельно.')
profile=dict(id='bafta-ygd',name='BAFTA Young Game Designers',group='games',age_summary='10–14 / 15–18; UK residents',age_tags=['10-12','teen'],
    summary='Конкурс оригинальных игровых идей и созданных игр.',categories=[dict(name='Game Concept / Game Making',age='10–14 / 15–18',team='1–3, одна возрастная группа',hardware='Идея / playable level',entry='UK residency; online call',age_rule='School year текущего call')],
    event_ids=['C776'],legacy_ids=[],route='UK eligibility → самостоятельная идея / игра → submission → judging.',hardware='По категории',language='Язык поддержки следующего call проверить',
    importance='BAFTA programme; национальный допуск. Редакционная оценка, не мировой рейтинг.',strengths='Дизайн и создание игр',requirements=['UK residency; до 16 также UK-resident guardian.'],
    nuances=['Сейчас семье недоступно: возраст и резидентство.','AI раскрывать; правила следующего сезона могут измениться.'],cost='Следующий call не объявлен',award='YGD award при победе',
    sources=[dict(title='Первичные правила 2026',url=bafta,checked=DAY)],evidence='Прочитан действующий overview / FAQ 2026; заявки закрыты, будущие даты не придуманы.')
d['league_guide']['profiles'].append(profile);d['league_guide']['version']=13;d['league_guide']['checked']=DAY
d['league_guide']['methodology']='60 семейств и программ; все 46 прежних маршрутов сохранены. Это частичная карта лиг, а не доказанный полный мировой список. Возраст и резидентство проверяются для конкретного сезона.'

for e in d['events']:
    if e['id'] in new+updated:
        for ref in e.get('references',[]):
            # Prior sources such as PGW Family are retained without claiming
            # a fresh full read. Sources below were actually opened this pass.
            if ref['url'].endswith('/espaces/pgw-family'): continue
            source(ref['url'],ref['label'])
a=d['completeness_audit'];a.update(version=13,checked=DAY,baseline=baseline,new_ids=new,new_profiles=['bafta-ygd'],updated_ids=updated,promoted_exhibition_ids=promoted,
    scope='Инвентаризация всех трёх блоков; новый проход по будущим каникулярным сменам и игровым выставкам. Повторная проверка каждого старого источника и полного календаря каждой страны не завершена.')
a['caveats']=[s for s in a['caveats'] if not s.startswith('Лагеря в этом проходе')]+[
    'Добавлено 16 датированных смен и один недатированный курс. Язык EN явно указан для 12 датированных смен; четыре Bricks4Kidz остаются кандидатами с неизвестным языком.',
    'TechSpark LEGO Junior 6+ в общем каталоге не гарантирует робототехнику на каждой датированной неделе Zürich: проверенные недели Game Design начинаются с 7 лет.',
    'Kids badge / бесплатный детский вход определяется конкретным изданием и возрастом на день визита, иногда ростом; правила разных PAX и разных лет не взаимозаменяемы.',
    'Публичные дни выставки отделены от business/media days. Билет посетителя не регистрирует ребёнка в отдельный турнир.',
    'EN/NL двуязычный bootcamp не гарантирует полное обучение только на EN; иностранный приём, язык и наличие места требуют подтверждения.']
a['source_issues'] += [dict(name='gamescom Cologne 2027',status='Opening-times / visitors повторно дали только заголовок. Поисковый фрагмент не использован как подтверждённая дата; карточка остаётся без точных дней.',official_alternative='https://www.gamescom.global/en/info/opening-times'),
    dict(name='PAX Aus: ровно 6 лет',status='FAQ допускает бесплатный вход до 6 включительно; Terms требуют badge с 6. Противоречие подтверждено повторным чтением, не снято.',official_alternative='https://aus.paxsite.com/en-us/terms-and-conditions.html'),
    dict(name='PAX Unplugged Philadelphia: Kids days',status='FAQ пишет Sunday-only, а buy-badges предлагает Kids 3-Day / Fri / Sat / Sun. Уточнить действующий вариант до покупки.',official_alternative='https://unplugged.paxsite.com/philly/en-us/registration/buy-badges.html'),
    dict(name='Helvetic Institute Zug / TechLabKids Barcelona',status='Агрегатор / общий каталог не подтвердил точную будущую STEM-смену и язык. Не добавлены вымышленные даты или бесплатный тариф 0€ из placeholder.',official_alternative='')]
a['known_backlog'] += [dict(kind='Лагеря',name='Costa Rica / México: будущие ES/EN каникулы',reason='Ciberbots подтвердил периоды 2026–2027 без точных дней и возрастов; новые конкретные смены Costa Rica и иностранный приём всё ещё требуют поиска.',url='https://www.ciberbots.com.mx/services'),
    dict(kind='Выставки',name='ChinaJoy / оставшиеся PAX / национальные игровые шоу',reason='Общий игровой бренд не заменяет список всех изданий; будущие даты, child gates и возраст турниров проверяются отдельно.',url=''),
    dict(kind='Лагеря',name='Испанские региональные STEM-провайдеры',reason='TechLabKids / FunTech: будущая смена, возраст, ES versus Catalan и фактические места ещё не подтверждены.',url='https://techlabkids.com/campamentos/')]
d['source_count']=len(d['sources']);d['asof']=DAY
d['expansion_log'].append(dict(version=13,date=DAY,scope='Future holiday camps, public game exhibitions and residency-gated game-design competition',added_ids=new,updated_ids=updated,promoted_exhibition_ids=promoted,
    notes=['Все 1008 прежних карточек сохранены; 8 ранее добавленных игровых шоу теперь видны в подборке крупных выставок.','Общие каталоги, прошлые условия и языки сайта не превращены в гарантии конкретной смены.']))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text());plan['updated']=DAY;plan['status']='active';plan['completeness_audit']='data/audit-v13.json'
for r in plan['requirements']:
    if r['id']=='global_competitions':r['evidence']='v13: 776 competition cards / 60 profiles. BAFTA YGD UK residency and closed2026call explicit; full local qualifiers and all leagues still incomplete.'
    if r['id']=='camps':r['evidence']='v13: 138 camp/program cards; 16 new future dated shifts plus one undated LEGO6+ route. 12 dated shifts explicit EN or EN/NL, four US shifts teaching language unconfirmed. All121 previous cards retained.'
    if r['id']=='exhibitions':r['evidence']='v13: 119 event cards; 67 curated major edition/venue cards, including six new public gaming editions and eight existing records added to major view. Business days and child gates distinguished.'
    if r['id']=='eligibility':r['evidence']='v13: per-course7+ versus genericLEGO6+ separated; EN/NL versus EN-only uncertain; PAXexact6 badge conflict retained; gamescomAsia heightgate explicit; BAFTAUKresidency excludesfamily. DOB/grade and national quotas remain missing.'
plan['latest_validation']={'version':'v13','status':'pending','research_status':'active'}
plan['next_research'].insert(0,'Holiday camps: confirm Costa Rica/México future exact shifts first; TechSpark Robotics6+ actual venue/week, NewTechKids EN-only support, Bricks4Kidz teaching language/foreign child documents. Every programme still needs vacancies.')
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2))
print(json.dumps(dict(added=len(new),promoted=len(promoted),total=len(d['events']),added_ids=new),ensure_ascii=False))
