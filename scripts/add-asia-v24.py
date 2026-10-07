"""Add dated Japanese camps and independently read current Indian competition rules."""
import copy, datetime, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'stem-family-atlas-work'/'research-v24'
p=ROOT/'data/catalog.json'; d=json.loads(p.read_text()); old=copy.deepcopy(d)
assert d['completeness_audit']['version']==23
CHECKED='2026-10-01'
added=[]; receipts=[]
def source(url,title,claim,filename=None):
    if url not in {s['url'] for s in d['sources']}:
        d['sources'].append(dict(url=url,title=title,evidence=claim,checked=CHECKED))
    r=dict(url=url,title=title,claim=claim,checked=CHECKED,kind='primary',read=True)
    if filename and (WORK/filename).exists():
        b=(WORK/filename).read_bytes(); r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    receipts.append(r)
    return dict(url=url,title=title,checked=CHECKED)
def card(id,block,title,country,city,url,**extra):
    x=dict(id=id,block=block,title=title,country=country,region='Азия',city=city,source=url,checked=CHECKED,
      start='',end='',deadline='',period='Новые точные даты не объявлены',date_status='Ожидаются даты',
      age='Уточнить текущие условия',mat='Условно — допуск требует подтверждения',osc='Условно — допуск требует подтверждения',
      format='Условия конкретного этапа',participation='individual_or_team',admission_kind='unknown',
      entry='Уточнить иностранный вход и место; семья не зарегистрирована.',gear='По текущим правилам',
      cost='Тариф и валюта конкретного этапа требуют подтверждения',language='Язык технических занятий / защиты не подтверждён',
      languages=[],support_languages=[],language_mode='unconfirmed',language_certainty='Язык сайта не доказывает язык занятий или судейства.',
      scope='national',level='Этап программы; не прямой вход в мировой финал',
      importance_reason='Редакционная оценка содержания и семейной доступности; не мировой рейтинг.',
      reward='Результат / награду установить по протоколу; участие не является победой',
      priority='P2 — после допуска и подтверждения места',status='Идея',
      action='Подтвердить категорию, иностранный вход, актуальный срок, язык и место до поездки.',
      themes=['robotics','coding','technology'],evidence_level='rules',references=[],related_ids=[],
      registration_status='Семья не зарегистрирована; опубликованное предложение не подтверждает место.',note='',proof='',provider='')
    x.update(extra)
    assert id not in {e['id'] for e in d['events']}
    d['events'].append(x); added.append(id); return x

# Four separate published cohorts, not invented weekly combinations.
tcc=[]
sessions=[('L198','Fall Break · Session 1','fall','1','2026-10-12','2026-10-16'),
          ('L199','Fall Break · Session 2','fall','2','2026-10-19','2026-10-23'),
          ('L200','Winter Break · Session 1','winter','1','2026-12-14','2026-12-18'),
          ('L201','Winter Break · Session 2','winter','2','2026-12-19','2026-12-23')]
for id,name,season,n,start,end in sessions:
    url=f'https://www.tokyocodingclub.com/camp/2026-code-quest-tokyo-{season}-break-session-{n}/'
    tcc.append(source(url,'Tokyo Coding Club · '+name,
      'Published 2026 five-day cohort; 5–12; entirely English; 129000 JPY + tax; robotics / AI at selected sessions.',{'L199':'fall2.html','L200':'winter1.html'}.get(id)))
    card(id,'Лагеря','Tokyo Coding Club · Code Quest 2026 · '+name,'Япония','Tokyo · Nishi-Azabu',url,
      start=start,end=end,period='',date_status='Подтверждено',date_scope='camp_window',
      age='5–12; все уровни; сложность после трёх лет опыта согласовать',
      mat='Да по возрасту 5–12; группа и место отдельно',osc='Да по возрасту 5–12; группа и место отдельно',
      format='Дневная 5-дневная смена, примерно 09:00–17:00; 15+ часов tech lessons и экскурсии',
      participation='day_camp',admission_kind='program',scope='local',provider='Tokyo Coding Club',
      entry='Официальная запись через страницу смены. Japanese не требуется; достаточно понимать простые инструкции на EN. Подтверждение организатора и оплаты отдельно.',
      gear='Minecraft / coding; Roblox, robotics и AI зависят от выбранной смены. Оборудование включено.',
      cost='129 000 JPY + налог за 5 дней; обед / snacks, оборудование, экскурсионный транспорт и билеты включены. Семейное жильё / перелёт отдельно.',
      language='Все занятия и camp staff — English; non-native speakers принимаются',languages=['EN'],language_mode='primary',
      language_certainty='Страница именно этой смены прямо указывает entirely in English и FAQ для non-native speakers.',
      evidence_level='program',themes=['robotics','ai','coding','games'],level='Образовательный лагерь; экскурсии занимают часть дня',
      reward='Учебные проекты; не международная соревновательная медаль',related_ids=['L020'],
      note=('Окно включает экскурсии; не 40 часов робототехники. Robotics & AI заявлены только для select sessions: подтвердить тему и уровень выбранной группы. '
      'Winter Session 2 идёт 19–23 декабря, суббота–среда. На странице смены / footer расходятся этажи Nishi-Azabu; точку передачи ребёнка уточнить в parent guide. '
      'Метка доступности на сайте не является бронью; японский не обязателен.'),
      action='Выбрать одну опубликованную смену, подтвердить robotics / AI и уровень обеих групп, место и parent guide.',
      proof='Прочитаны индивидуальная страница смены и общий список camps; возраст, даты, EN, цена и ограничение select sessions.')
index=source('https://www.tokyocodingclub.com/our-camps/','Tokyo Coding Club · announced camps','All four fall / winter 2026 cohorts are listed.')
for e in d['events']:
    if e['id']=='L020':
        e['related_ids']=list(dict.fromkeys(e.get('related_ids',[])+[i[0] for i in sessions]));e['checked']=CHECKED
        e['note']+=' Осенние / зимние смены 2026 подтверждены отдельно: L198–L201; старая летняя смена не переносится на новый сезон.'

# International residential course: exact age at arrival, not birth-year eligibility.
hu='https://winter.harrowappi.jp/'
hs=source(hu,'Harrow Appi Japan · winter 2026','13–19 December, residential English engineering / snow sports camp, 9–13 throughout, JPY440000 incl tax; deadline November13.','harrow.html')
he=source('https://www.harrowappi.jp/events/','Harrow Appi · school events','Official school links the winter camp and confirms December13–19,2026.')
card('L202','Лагеря','Harrow Appi Japan · Winter Camp 2026','Япония','Appi Kogen · Iwate; трансфер Morioka Station',hu,
    start='2026-12-13',end='2026-12-19',deadline='2026-11-13',deadline_label='Приём заявки на зимний лагерь',
    deadline_note='Дата 13 ноября опубликована; час / timezone cutoff не указан.',period='',date_status='Подтверждено',date_scope='camp_window',
    age='9–13 на протяжении смены; точный день рождения важен',mat='Условно — должен быть возраст 9 лет уже 13 декабря',osc='Нет — минимум 9 лет',
    format='Пансион: 6 ночей; 13 / 19 декабря приезд / отъезд; пять учебных дней 14–18 декабря',
    participation='residential',admission_kind='program',scope='international',provider='Harrow Appi Japan',
    entry='Опубликованный международный Winter Camp; заявка через OpenApply. Место, документы, уровень EN и самостоятельность в пансионе подтверждаются отдельно.',
    gear='Проект управляемой модели: рама, micro:bit, gyroscope, программирование, физика / математика и тестирование; лыжи / snowboard после обеда.',
    cost='440 000 JPY с применимыми налогами; пансион, питание, трансфер Morioka, занятия / lifts и аренда снежного оборудования. Льготные 352 000 JPY — только текущим ученикам Harrow.',
    language='English residential camp; техническая программа на английском',languages=['EN'],language_mode='primary',
    language_certainty='Официальная страница описывает full residential English camp; минимальный языковой уровень отдельно.',
    evidence_level='program',level='Учебная инженерная программа с зимним спортом',
    reward='Внутренний Race Day и награды лагеря; не титул международной робототехнической лиги',
    references=[dict(url=he['url'],label='Подтверждение дат на сайте школы')],
    note='Итоговый заезд относится к лагерю. 13–19 декабря — пребывание, а не семь полных дней robotics. Родители не включены в детский пансион. Точные birthday / место и иностранные документы пока не подтверждены.',
    proof='Прочитана официальная сезонная страница: возраст throughout, EN, расписание, micro:bit / gyroscope, цена, срок и трансфер. Сайт школы связывает сезон с 2026.')

# This is a regular programme. The available July camp calendar is past-only.
cu='https://codinglab.jp/'
cs=source(cu,'Coding Lab Japan · junior programmes','English instruction expressly stated; 5–6 Junior Coder ScratchJr / LEGO Robots; 7–9 Scratch. No new holiday cohort established.','codinglab.html')
for id,name,age,mat,osc,gear in [
    ('L203','Junior Coder · 5–6','5–6','Нет — старше этой группы','Да по возрасту 5–6; точную группу и место подтвердить','ScratchJr / LEGO Robots; ранняя математика и объяснение проекта'),
    ('L204','Lower Primary · 7–9','7–9','Да по возрасту 7–9; после трёх лет опыта нужен assessment','Нет — минимум этой группы 7 лет','Scratch: условия, циклы, координаты; advanced AI / Python не обещаны этой группе')]:
    card(id,'Лагеря','Coding Lab Japan · '+name,'Япония','Tokyo · Shirokanedai / online по конкретному курсу',cu,
        age=age,mat=mat,osc=osc,format='Регулярные занятия; конкретная праздничная смена не объявлена',participation='regular',
        period='Регулярное обучение; новый camp-календарь после июля 2026 не установлен',
        admission_kind='program',scope='local',provider='Coding Lab Japan',entry='Школа предлагает assessment / trial; группа определяется уровнем. EN заявлен прямо, иностранное место и visiting-family пакет уточнить.',
        gear=gear,language='Classes are conducted in English',languages=['EN'],language_mode='primary',
        language_certainty='Прочитано прямое утверждение о языке преподавания, а не только английский сайт.',evidence_level='program',
        level='Coding school / регулярный курс',reward='Собственный учебный проект; world-result и конкурсная квота не установлены',
        cost='Полная цена выбранного курса неизвестна; ¥0 на динамических карточках не принято как бесплатный лагерь.',
        note='В календаре найдены июльские смены 2026; даты не перенесены на 2027. Headline AI / Robotics относится ко всему оператору; возрастные группы изучают разное.',
        proof='Прочитана homepage: прямое EN instruction, отдельные 5–6 / 7–9 программы и assessment.')

# Current Nuxt page payload and linked 2026 rules were read, not the linked stale FAQ.
au='https://community.avishkaar.cc/avishkaar-league-2026'
asrc=source(au,'Avishkaar League · season 2026','Eight exact zonals; provisional Jan15–16,2027 Delhi finale; four disciplines; foreign admission not established.','avishkaar.html')
competitions={}
for k,code in [('irc','irc_2026'),('makeathon','am_2026'),('codequest','cq_2026'),('battlegrounds','rb_2026')]:
    competitions[k]=json.loads((WORK/(k+'.nuxt.json')).read_text())['state']['events']['event_details_by_code']
    source('https://community.avishkaar.cc/competitions/'+code,'Avishkaar · current '+code,
        'Current categories and team size read from first-party page state. Registration dates conflict with landing timeline.',k+'.html')
pdfs=[]
for k,field,filename,title in [('irc','3_card_link_0','irc-primary.pdf','IRC Primary rules 2026'),('irc','3_card_link_1','irc-junior.pdf','IRC Junior rules 2026'),
    ('irc','3_card_link_4','fair-play.pdf','IRC / Battlegrounds Fair Play 2026'),('makeathon','0_card_link_1','makeathon-rules.pdf','Makeathon problem statement 2026'),
    ('makeathon','3_card_link_0','makeathon-guidelines.pdf','Makeathon submission 2026'),('codequest','3_card_link_0','codequest-junior.pdf','CodeQuest Junior 2026'),
    ('battlegrounds','0_card_link_1','battlegrounds-rules.pdf','Robo Battlegrounds 2026')]:
    pdfs.append(source(competitions[k][field],title,'Current linked 2026 PDF downloaded and read; specific discipline requirements.',filename))
conflict='Landing: virtual stage 1 Sep–30 Nov и Delhi final 15–16 Jan2027 с пометкой subject to change. Current Makeathon / CodeQuest page state: registration ends 30 Oct2026; IRC narrative: Delhi dates TBA. Не выбран вымышленный единый срок.'
foreign='Иностранный допуск / связь с индийской школой и язык защиты уточнить. Worldwide marketing не является подтверждением семейной заявки. '
irs=[]
for id,key,name,age,team,gear,details in [
    ('C849','irc','IRC · миссии робота','Primary Grades 1–2; Junior 3–5; Middle 6–8; Senior 9–12','1–4',
     'Primary: только MEX, максимум 2 мотора. Junior: ручной SAR + автономный line follower, разрешённые ER / MEX детали.',
     'Primary 3 минуты; Junior 4 минуты и два робота. Класс, а не только возраст. В одной группе братьев нельзя считать допущенными автоматически.'),
    ('C850','makeathon','Makeathon · проекты','Junior до Grade 5; Middle до Grade 8; Senior до Grade 12; нижняя граница отдельно','1–4',
     'Working prototype: disaster response; любой kit по submission guidelines, видео 4–6 минут.',
     'Stage 1 — видео проекта, Stage 2 — очный показ. Часть Stage1 баллов за likes; это не чистая оценка инженерного результата. Idea document до 30 октября даёт больший балл, это не окончательный срок видео.'),
    ('C851','codequest','CodeQuest · AI game hackathon','Junior Grades 1–5; Middle 6–8; Senior 9–12','1–2',
     'Avishkaar Game Builder; hand / pose tracking, спасательная игра; свой code file и gameplay video 2–4 минуты.',
     'Junior может дать одну пару братьев только если оба Grade1–5 и иностранный вход разрешён. Stage1 remote, Stage2 live hackathon; PDF содержит старые gl_2025 / gl_2026 footers.'),
    ('C852','battlegrounds','Robo Battlegrounds · Robo Soccer','Landing: Grades 1–12 для League; отдельное возрастное распределение Robo Soccer не опубликовано','1–2',
     'Робот из Avishkaar ER series; 1v1, 3 минуты, текущий Fair Play.',
     'Robo Soccer; не свободный бой любых платформ. Отдельный junior допуск и смешанный возраст подтвердить; page state Dec31 расходится с общим Jan15–16 финалом.')]:
    url='https://community.avishkaar.cc/competitions/'+competitions[key]['event_code']
    e=card(id,'Соревнования','Avishkaar League 2026 · '+name,'Индия','Региональные этапы / online → Delhi по отбору',url,
        age=age,mat='Условно — нужна школьная категория и подтверждённый иностранный вход',osc='Условно — нужен Grade 1+ либо подтверждённый junior допуск',
        format='Индивидуально / команда '+team+' учащихся',participation='individual_or_team',admission_kind='open_application',
        entry=foreign+'Регистрация через текущую страницу дисциплины; приглашение друзей в команду и zonal / virtual отбор. Финал не открытая туристическая заявка.',
        gear=gear,provider='Avishkaar',scope='international',level='Международная сеть; национальные зоналы и отбор в Delhi',
        period='Сезон 2026–27; Oct–Dec zonals / Sep–Nov virtual; финал предварительно 15–16 января 2027',
        date_status='Сроки требуют уточнения',deadline_note=conflict,reward='Оцениваемый конкурс; trophy / medal и статус результата подтверждаются протоколом.',
        note=details+' '+conflict,proof='Прочитано актуальное first-party page state и связанные PDF2026; старый FAQ2025–26 не использован как текущий регламент.',
        references=[dict(url=s['url'],label=s['title']) for s in pdfs if (key=='irc' and s['title'].startswith('IRC')) or (key=='makeathon' and s['title'].startswith('Makeathon')) or (key=='codequest' and s['title'].startswith('CodeQuest')) or (key=='battlegrounds' and 'Battlegrounds' in s['title'])])
    if key=='codequest':e['themes']=['ai','coding','games']
    if key=='makeathon':e['themes']=['makers','robotics','technology']
    irs.append(e)
zonals=[('Mumbai','2026-10-10','Venue TBA'),('Gurugram','2026-10-17','Euro International School, Sector48'),
        ('Kerala','2026-10-24','Amrita University; конкретный campus / город уточнить'),('Hyderabad','2026-11-14','Venue TBA'),
        ('Bengaluru','2026-11-21','NPS KR Puram'),('South Delhi','2026-11-21','Bloom Public School'),
        ('West Delhi','2026-12-05','Mata Jai Kaur Public School'),('Pune','2026-12-05','Venue TBA')]
for n,(city,date,venue) in enumerate(zonals,853):
    # December closing dates conflict with the general November30 page cutoff.
    deadline=(datetime.date.fromisoformat(date)-datetime.timedelta(days=1)).isoformat() if date<'2026-12-01' else ''
    card(f'C{n}','Соревнования','Avishkaar 2026 · IRC / Robo Soccer zonal · '+city,'Индия',city,au,
        start=date,end=date,period='',date_status='Подтверждено',deadline=deadline,deadline_label='Zonal registration · сверить доступность',
        deadline_note='Landing: закрытие за день до zonal, час не указан. Для December zonals правило даёт Dec4, но current page state IRC / Soccer — Nov30: подтвердить, единый дедлайн не экспортирован.',
        age=irs[0]['age']+'; отдельную Robo Soccer категорию уточнить',
        format='IRC миссии / Robo Soccer: категории имеют разные правила и состав',participation='individual_or_team',
        admission_kind='open_application',scope='regional',provider='Avishkaar',venue=venue,
        entry=foreign+'Online team registration + zonal pass. Точная дата не подтверждает открытое место. '+venue,
        gear='IRC 1–4; Soccer 1–2; только разрешённые Avishkaar parts. Младшие категории — по классу.',
        related_ids=['C849','C852','C861'],level='Региональный отбор; не мировой финал',
        note='Восьмь точных дат прочитаны на landing. Sikkim December tentative, Chennai / Indore / Rudrapur TBA не превращены в точные события. '+conflict,
        proof='Первичный календарь сезона 2026; venue без подтверждённого адреса отмечен TBA. Правила прочитаны отдельно.',references=[dict(url=irs[0]['source'],label='IRC категории и командные правила')])
card('C861','Соревнования','Avishkaar League · Delhi international finale 2027','Индия','Delhi · venue TBA',au,
     period='Предварительно 15–16 января 2027; subject to change и противоречия страниц',date_status='Предварительно',
     participation='individual_or_team',admission_kind='qualifier',scope='international',provider='Avishkaar',
     age='Категория / классы соответствующей дисциплины; не единый возраст всего финала',entry=foreign+'После zonal / virtual отбора. Приглашение на конкретную дисциплину и билет / квота отдельно.',
     format='IRC / Robo Soccer finale; Makeathon выставка; CodeQuest live hackathon',
     related_ids=[e['id'] for e in irs],note=conflict+' Battlegrounds state содержит Dec31. Пока не экспортируется как подтверждённая дата.',
     proof='На landing явно стоят Jan15–16,2027 с subject to change; page-state / IRC narrative не подтверждают единое окончательное расписание.')
profile=dict(id='avishkaar',name='Avishkaar League · IRC / Makeathon / CodeQuest / Soccer',group='ai',
    age_summary='Классы 1–12; IRC Primary 1–2, Junior 3–5; правила дисциплин различаются',age_tags=['6','9','10-12','teen'],
    summary='Младшие роботомиссии и AI-games, проекты и Robo Soccer. Не путать границы классов с возрастом.',
    categories=[dict(name=e['title'].split(' · ',1)[1],age=e['age'],age_rule='Класс на сезон; иностранную эквивалентность подтвердить',team=e['format'],hardware=e['gear'],entry=e['entry'],event_id=e['id']) for e in irs],
    event_ids=[f'C{i}' for i in range(849,862)],legacy_ids=[e['id'] for e in irs],
    route='Подходящий класс / дисциплина → самостоятельный robot / game / prototype → zonal или virtual stage → приглашение в Delhi.',
    hardware='IRC / Soccer только разрешённые Avishkaar parts; Makeathon любой kit; CodeQuest Game Builder.',
    language='Материалы EN; язык защиты / поддержки иностранной команды не установлен.',importance='Практический дополнительный путь; не доказанная замена национального WRO / FIRST / VEX сезона.',
    strengths='Четыре различных формата и ранняя Grade1–2 категория.',
    requirements=['Классы обоих, mixed-grade команда, иностранный вход и язык защиты подтвердить до оплаты / поездки.',
                  'IRC 1–4, Makeathon 1–4, CodeQuest / Soccer 1–2; состав IRC после регистрации нельзя подменять.',
                  'Оборудование и формат — по конкретному PDF; MEX Primary не означает свободный вход с LEGO.'],
    nuances=[conflict,'Ссылка FAQ на landing ведёт на 2025–26. Current PDF имеют отдельные старые footers; использовано их сезонное содержание 2026.',
             'Makeathon Stage1 включает popularity likes; инженерное качество и социальное продвижение различаются.',
             'CodeQuest Junior Grade1–5 может подойти паре братьев; это условный вывод, классы / иностранный допуск неизвестны.'],
    cost='На page state есть суммы без проверенной валюты / полной сметы; не выданы за итоговый тариф.',award='Оцениваемые награды; международность и конкретное место устанавливаются протоколом.',
    sources=[asrc]+[dict(url=e['source'],title=e['title'],checked=CHECKED) for e in irs]+pdfs,evidence='Текущие first-party данные и PDF прочитаны; семейный допуск не подтверждён.')
d['league_guide']['profiles'].append(profile)

# Seven dated host editions, with their actual future hardware, not an assumed Challenge.
fu='https://www.firstrobotics.co.in/first-lego-league/'
fs=source(fu,'FIRST India / Infinity X · FLL2026–27','Future8–16 up to8; Explore6–10 up to6; six regionals and Pune national; fresh header closes registration September30.','fll-primary.html')
es=source('https://fll.edutechindia.com/','Edutech · current FLL delivery organiser','Current page identifies Infinity X as the India competition contact; Edutech is hardware reseller.')
fll=[('Ahmedabad','2027-01-08','2027-01-10','2026/08/ahd2.png','fll-ahmedabad.png'),
     ('Hyderabad','2027-01-08','2027-01-10','2026/07/hyd1-1.png','fll-hyderabad.png'),
     ('Mumbai','2027-01-30','2027-01-31','2026/09/mum2.jpg','fll-mumbai.jpg'),
     ('Delhi NCR','2027-01-22','2027-01-24','2026/07/del1.png','fll-delhi.png'),
     ('Bengaluru','2027-01-29','2027-01-31','2026/07/bl1.png','fll-bengaluru.png'),
     ('Pune · regional','2027-01-29','2027-01-31','2026/07/pn1.png','fll-pune.png'),
     ('Pune · National Championship','2027-02-11','2027-02-14','2026/07/pnqc.png','fll-national.png')]
for n,(city,start,end,img,filename) in enumerate(fll,862):
    iu='https://www.firstrobotics.co.in/wp-content/uploads/'+img
    isrc=source(iu,'FIRST India calendar · '+city,f'Official date image visually read: {start}–{end}.',filename)
    card(f'C{n}','Соревнования','FIRST LEGO League India · BIOGLOW 2026–27 · '+city,'Индия',city.split(' · ')[0],fu,
         start=start,end=end,period='',date_status='Подтверждено',date_scope='festival_window',provider='Infinity X / FIRST India',
         age='Future Edition 8–16, до 8 в команде; Explore 6–10, до 6. Точное отсечение возраста уточнить.',
         mat='Условно — возраст подходит Future / Explore; регистрация и иностранный вход не подтверждены',
         osc='Условно — только Explore 6–10; Future8+ пока не подходит',
         participation='team',admission_kind='qualifier' if n==868 else 'open_application',scope='national' if n==868 else 'regional',
         format='Окно турнира / фестиваля; точный день каждой программы не опубликован',
         entry='Партнёр India — Infinity X. Свежая страница 1 октября: Registrations Closes 30th Sept. Поздний / иностранный вход и национальную квоту подтвердить; наличия form-link недостаточно.',
         gear='Future: LEGO Education Computer Science & AI (два sets на команду8; доп. motors / controllers для8+). Explore: genuine LEGO, SPIKE Essential рекомендован; альтернативу согласовать.',
         registration_status='Баннер указывает закрытие 30 сентября; год на баннере не написан. В контексте сезона 2026–27 обычный срок, вероятно, прошёл. Поздний вход не подтверждён.',
         language='English страницы / ресурсы; язык судейства и помощи выбранному этапу уточнить',languages=[],
         level='National / regional India; не открытый международный World Festival',reward='Explore: показ и признание. Future: формат оценки / отбор по местному регламенту; world-квота отдельно.',
         cost='Полный тариф / поздняя регистрация и оборудование требуют подтверждения; hardware отдельно от team registration.',
         references=[dict(url=iu,label='Официальное изображение точных дат'),dict(url=es['url'],label='Разделение организатора и hardware reseller')],
         related_ids=['C868'] if n!=868 else [f'C{i}' for i in range(862,868)],
         note='Даты прочитаны на изображениях календаря, не из агрегатора. Конкретные площадки / часы / распределение Explore и Future не установлены. Старый EV3 / SPIKE Challenge текст на Edutech не заменяет current Futurehardware.',
         proof='Прочитаны официальный organiser и все семь изображений; header свежего HTML сверён с обновившимся web-read: Sept30 вместо cached registrations open.')
first=next(g for g in d['league_guide']['profiles'] if g['id']=='first')
first['event_ids']+= [f'C{i}' for i in range(862,869)]
first['categories'].append(dict(name='India · BIOGLOW Future / Explore 2026–27',age='Future8–16; Explore6–10',age_rule='India cutoff / foreign entry отдельно',team='Future до8; Explore до6',hardware='Future CS&AI; Explore genuine LEGO / SPIKE Essential рекомендован',entry='Срок Sept30 на свежей странице; поздний вход и местные квоты уточнить',event_id='C868'))
first['sources']+= [fs,es]
first['nuances'].append('India2026–27: шесть региональных окон и национальный Pune11–14Feb2027. Future8–16 / Explore6–10 имеют разные hardware; баннерSept30 не принят как открытый набор. Иностранная квота не подтверждена.')

# Rechecked Panama historical programmes remain historical; do not fabricate 2027 dates.
pu='https://www.explorapanama.org/'
ps=source(pu,'Explora Panama · current homepage','Homepage still advertises Cursos de Verano2026; a 2027 robotics cohort / technical English is not established.')
for e in d['events']:
    if e['id'] in ['L042','L043']:
        e.update(checked=CHECKED,evidence_level='historical_program')
        e['note']+=' Повторная проверка 01.10.2026: homepage всё ещё Cursos de Verano2026; новые даты2027 не найдены. Bilingual preschool не доказывает EN технического лагеря.'

issues=[
 dict(name='Avishkaar · разный текущий срок',status=conflict,official_alternative=au),
 dict(name='FIRST India · открыто / закрыто',status='Cached page показывала registrations now open; свежий HTML и повторный web-read показывают Sept30. Late / foreign entry и год cutoff уточнить.',official_alternative=fu),
 dict(name='Japan · Robotics AI select sessions',status='TCC не обещает robotics / AI каждой группе. Coding Lab новый holiday-календарь не установлен; ¥0 не признано реальным тарифом.',official_alternative=index['url']),
 dict(name='Panama · старый summer2026',status='Explora2027 не объявлен в прочитанной homepage. Cacao Camps nature / adventure не принят как robotics camp.',official_alternative=pu),
 dict(name='Korea · первичная страница недоступна для повторной сверки',status='ROBOTWORLD English visitor page вернула пустой HTTP200; Korean root — редиректную оболочку. Предыдущие E010 факты сохранены, новый camp6/9EN не подтверждён.',official_alternative='https://eng.robotworld.or.kr/visitors/information.php'),
 dict(name='iREX2027 · точные дни ещё не установлены',status='Primary search / report остаётся Early December2027 tentative. На повторном открытии403; вымышленные December1–4 не добавлены.',official_alternative='https://irex.nikkan.co.jp/')]
cf=d['camp_focus']; cf.update(version=24,checked=CHECKED,
 conclusion='Мировой аудит остаётся частичным. v24 добавляет четыре опубликованные EN-смены Tokyo, один инженерный EN-пансион Harrow Appi, две регулярные EN-группы Coding Lab и текущие младшие пути India. Не каждый ресурс — доступный лагерь, не каждый точный турнир — открытая регистрация.',
 added_ids=added.copy(),updated_ids=['L020','L042','L043'])
cf['carried_forward_ids']=list(dict.fromkeys(cf.get('carried_forward_ids',[])+old['camp_focus']['added_ids']))
cf['hack_event_ids']=list(dict.fromkeys(cf['hack_event_ids']+['C850','C851']))
cf['routes']+= [
 dict(name='Япония · обоим на английском',detail='TCC5–12: Oct12–16 / Oct19–23 / Dec14–18 / Dec19–23, дневные смены129000JPY+tax; Robotics&AI только select sessions. Coding Lab имеет отдельные EN5–6 /7–9 регулярные группы, новая holiday-смена пока неизвестна.',ids=['L198','L199','L200','L201','L203','L204']),
 dict(name='Япония · инженерный зимний пансион',detail='Harrow AppiDec13–19,9–13throughout,EN,440000JPY,заявкадоNov13. Micro:bit+gyroscope,физика+ски. Матвею9надатуприезда; Оскару пока рано. InternalRaceDay — не победа мировой лиги.',ids=['L202']),
 dict(name='Индия · младшие конкурсы и школьные категории',detail='AvishkaarIRCPrimary1–2 /Junior3–5; CodeQuestJunior1–5,1–2участника,AIgesturegames. Makeathonprototype1–4,частьбалловзалайки. Иностранныйвход/ENнеподтверждены; текущие срокиOct30/Nov30конфликтуют. IndiaFLLсемьдат2027,баннерSept30: позднийвходотдельно.',ids=['C849','C850','C851','C861','C868'])]
# Human-readable text is kept separate from technical identifiers.
for r in cf['routes'][-3:]:
    if r['name'].endswith('пансион'):r['detail']='Harrow Appi: 13–19 декабря, 9–13 весь период, English, 440 000 JPY; заявка до 13 ноября. Micro:bit / gyroscope, физика и лыжи. Матвею нужно быть 9 лет на приезд; Оскару рано. Race Day — внутренний результат лагеря.'
    if r['name'].startswith('Индия'):r['detail']='Avishkaar: IRC Primary классы 1–2 / Junior 3–5; CodeQuest Junior 1–5, 1–2 участника, AI gesture games; Makeathon prototype 1–4, часть баллов за likes. Иностранный вход и EN защиты неизвестны; сроки 30 октября / 30 ноября конфликтуют. Семь дат FLL India 2027, баннер закрытия 30 сентября; поздний вход отдельно.'
cf['source_issues']+=issues
cf['gaps'].append('v24: Япония получила пять будущих смен и две регулярные EN-группы. India: текущие дисциплины / даты, но иностранный вход, технический язык и спорные дедлайны не закрыты. Panama2027 и Korea junior6/9EN robotics остаются пробелами. Все лагеря этих стран не собраны.')
cf['validation']=dict(status='pending',version='v24')
audit=d['completeness_audit'];audit.update(version=24,checked=CHECKED,new_ids=added,new_profiles=['avishkaar'],updated_ids=['L020','L042','L043'],
    conclusion='Частичный мировой каталог. v24: 27 карточек Японии / Индии, Avishkaar профиль; исторические Panama camps повторно проверены. Школы, семейная стратегия и результаты прошлых сезонов сохранены.',
    scope='Все континенты и три блока; этот проход закрывает часть японских смен и индийских младших маршрутов, не полный мировой аудит.')
audit['source_issues']+=issues; audit['validation']=dict(status='pending',version='v24')
d['expansion_log'].append(dict(version=24,checked=CHECKED,added=len(added),note='7 learning records (5 dated camp cohorts, 2 regular groups); 20 competition records (current pathways, 8 zonals, provisional final, 7 India FLL windows); new Avishkaar profile.'))
assert len(added)==27 and len(d['events'])==1204
assert d['schools']==old['schools'] and d['school_history']==old['school_history'] and d['family_strategy']==old['family_strategy']
assert d['development_routes']==old['development_routes']
assert all(e==old['events'][i] for i,e in enumerate(d['events'][:1177]) if e['id'] not in ['L020','L042','L043'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/asia-source-receipts-v24.json').write_text(json.dumps(dict(checked=CHECKED,scope='Primary content read; SHA receipts are independent of admission / registration.',sources=receipts,issues=issues),ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/camps-audit-v24.json').write_text(json.dumps(cf,ensure_ascii=False,indent=2)+'\n')
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text())
plan.update(updated=CHECKED,status='active')
plan['research_passes'].append(dict(version=24,checked=CHECKED,scope='Japan announced EN camps, India current junior rules / regional dates, Panama historical recheck',added=27,remaining='Worldwide coverage, current cohorts / foreign entry / language gaps remain.'))
plan['latest_validation_previous']=plan.get('latest_validation');plan['latest_validation']=dict(status='pending',version='v24')
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'README.md').open('a') as f:
    f.write('\nAsia v24 (2026-10-01): 27 additions, 1204 event records / 71 profiles. Five dated Japanese EN camp cohorts (four TCC day shifts5–12, Harrow Appi residential9–13), two Coding Lab regular EN tracks; current Avishkaar2026 categories / rules and eight zonals; provisional Delhi finale stays undated; seven FLL India2027 host windows visually read from organiser images. Avishkaar deadline / current-page conflicts and FLL Sept30 closure remain explicit; no foreign admission is assumed. Explora2026 programmes remain historical; Panama2027 / Korea junior EN camps not established. 22 schools, 116 historical results, seven family bases and prior event IDs preserved. Research stays active and incomplete; no applications or messages sent.\n')
print(json.dumps(dict(added=added,events=len(d['events']),profiles=len(d['league_guide']['profiles'])),ensure_ascii=False))
