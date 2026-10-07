"""Primary-source local pass. Run once against research v15 / 1063 records.

FTC spectator admission and overseas advancement remain separate from dates.
Future TecPro Match 2 receives no borrowed Match 1 dates or registration form.
Language tags for camps require evidence about teaching, not website language.
"""
import copy, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/catalog.json'
d = json.loads(PATH.read_text())
DAY = '2026-10-01'
assert len(d['events']) == 1063 and d['completeness_audit']['version'] == 15
assert d['family_context']['learning_languages'] == ['EN', 'ES']
baseline = copy.deepcopy(d['completeness_audit']['counts'])
byid = {e['id']: e for e in d['events']}
new, updated = [], []

def source(url, title, proof):
    row = next((s for s in d['sources'] if s['url'] == url), None)
    if row: row.update(checked=DAY, evidence=proof)
    else: d['sources'].append(dict(url=url, title=title, checked=DAY, evidence=proof))

def update(id, **kw):
    e = byid[id]; e.update(checked=DAY, **kw)
    if id not in updated: updated.append(id)
    source(e['source'], e['title'], e['proof'])
    return e

def reference(e, url, label, proof):
    if not any(r['url'] == url for r in e.setdefault('references', [])):
        e['references'].append(dict(url=url, label=label))
    source(url, label, proof)

def clone(parent, id, **kw):
    assert id not in byid
    e = copy.deepcopy(byid[parent]); e.update(id=id, checked=DAY, **kw)
    d['events'].append(e); byid[id]=e; new.append(id)
    source(e['source'], e['title'], e['proof'])
    return e

ftc_program = 'https://www.firstinspires.org/programs/ftc/'
ftc_local = 'https://www.first.org.mx/fm/que-es-el-first-tech-challenge/'
ftc_cost = 'https://www.first.org.mx/fm/costo-y-registro/'
ftc_schedule = 'https://www.first.org.mx/fm/'
old_rules = 'https://www.first.org.mx/fm/lineamientos-oficiales-para-la-participacion-en-regionales-y-clasificacion-al-nacional-de-ftc-temporada-2024-2025-de-mexico/'
ftc_rows = [
    ('C789','Regional CDMX · Tec de Monterrey','regional-cdmx-tec-de-monterrey','2026-11-27','2026-11-28','Ciudad de México · Tecnológico de Monterrey, Campus CDMX, Calle del Puente 222, Tlalpan',30),
    ('C790','Regional Nuevo León · San Pedro','regional-nuevo-leon-san-pedro','2026-11-27','2026-11-28','Monterrey · Las Torres, Paseo del Acueducto 2610, Del Paseo Residencial',31),
    ('C791','Regional CDMX · Maguen David','regional-cdmx-colegio-hebreo-maguen-david','2026-12-09','2026-12-10','Ciudad de México · Colegio Hebreo Maguen David, Camino Tecamachalco 370, Cuajimalpa',10),
    ('C792','Regional Coahuila · Torreón','regional-coahuila-torreon','2026-12-11','2026-12-12','Torreón · Colegio Cervantes, campus Vigata, Calzada José Vasconcelos 545',30),
    ('C793','Regional Jalisco · Guadalajara','regional-jalisco-guadalajara','2026-12-11','2026-12-12','San Pedro Tlaquepaque · TecMilenio Guadalajara, Av. Milenio 8640',20),
    ('C794','Regional Chihuahua','regional-chihuahua-chihuahua','2026-12-18','2026-12-19','Chihuahua · Universidad Tec Milenio, Sexta y de la Llave 1803, Centro',18),
    ('C795','Regional Estado de México · Toluca','regional-edo-mex-metepec','2026-12-18','2026-12-19','Toluca / Metepec · Tecmilenio Toluca, Guadalupe Victoria 221-Norte, Las Jaras',24),
    ('C796','Regional Yucatán · Mérida','regional-yucatan-merida','2027-01-15','2027-01-16','Mérida · Tecmilenio, Calle 53 Diagonal 665, Real Montejo',16),
    ('C797','Regional San Luis Potosí','regional-slp-san-luis-potosi','2027-01-22','2027-01-23','San Luis Potosí · Campus San Luis, Av. Chapultepec 1550, Garita de Jalisco',18),
    ('C798','Regional Estado de México · Cuautitlán','regional-edo-mex-cuautitlan','2027-01-29','2027-01-30','Cuautitlán Izcalli · Tecmilenio, Dr. J. Jiménez Cantú, Manzana 006 Lote 6, Ex Hacienda de San Miguel',20),
    ('C799','Regional Nuevo León · San Nicolás','regional-nuevo-leon-san-nicolas','2027-02-05','2027-02-06','San Nicolás de los Garza · Iztaccihuatl 431, Las Puentes 3er Sector',24),
    ('C800','Nacional CDMX · Azcapotzalco','torneo-nacional-cdmx-azcapotzalco','2027-02-12','2027-02-13','Ciudad de México · Tecmilenio Ferrería, Azcapotzalco',44),
]
ftc_ids=[]
for id, name, slug, start, end, city, displayed in ftc_rows:
    national = id == 'C800'
    url = 'https://www.first.org.mx/fm/evento/'+slug+'/'
    e = dict(id=id, block='Соревнования', title='FTC México · '+name+' · BIOBUZZ 2026–2027',
        country='Мексика', region='Северная Америка', city=city, source=url,
        references=[], checked=DAY, start=start, end=end, period='', date_status='Подтверждено', deadline='',
        age='FIRST: 12–18 лет, Grades 7–12; México: Grades 7–12, команда до 15 учеников',
        mat='Нет — 2017 год рождения: младше опубликованного уровня FTC 12–18',
        osc='Нет — 2020 год рождения: младше опубликованного уровня FTC 12–18',
        format='Команда до 15 учеников + взрослые наставники; автономные и управляемые матчи в альянсах',
        team_max=15, participation='team', admission_kind='qualifier' if national else 'open_application',
        entry=('Официальная команда FIRST → разрешённые региональные этапы → отбор на национальный. Действующий порядок квалификации 2026–2027 и иностранную квоту подтвердить.' if national else 'Активировать официальную команду FIRST → местный сезонный платёж → отдельная заявка на региональный этап. Приём команды из Costa Rica и право на национальную квоту подтвердить.'),
        gear='FTC kit, система управления, разрешённые компоненты и поле BIOBUZZ текущего сезона; LEGO FLL / VEX kit не заменяет FTC kit',
        cost='Страница México: US$350 активация FIRST + MX$7 500 сезон; второй региональный MX$3 750 с IVA. Действующий счёт, состав тарифа и национальный взнос подтвердить; робот, поле и поездки отдельно.',
        language='ES: местные страницы; EN: глобальные материалы. Язык интервью выбранного этапа уточнить',
        languages=[], language_certainty='Языки документации не являются подтверждением языка интервью и поддержки иностранной команды.',
        scope='national' if national else 'regional', level='Национальный финал FTC México' if national else 'Региональный этап FTC México',
        importance_reason='Этап крупной международной сети FIRST; региональная победа и национальная / мировая квота — разные результаты.',
        reward='Матчи, judged awards и отбор по действующим правилам; медали / квоты по официальному результату',
        priority='P3 — будущая траектория; детский зрительский вход уточнить', status='Идея для дальнейшего возраста',
        action='Сейчас выбирать младшие FIRST / WRO / VEX IQ программы. Для ознакомительного семейного визита отдельно подтвердить доступ посетителей и детей.',
        themes=['robotics','coding','technology'], evidence_level='event_page',
        registration_status='Даты страницы не подтверждают свободные места или принятую заявку. Семья не зарегистрирована.',
        proof='Прочитана индивидуальная event page: точные Start / End Date, площадка и местный сезон BIOBUZZ. Отдельно прочитаны глобальная FTC page, местные Grades 7–12 / до 15 и Costo y Registro.',
        note=f'На странице поле Number of Participants: {displayed} команд; это не проверенный остаток мест. Время на страницах не принято за полное расписание: у CDMX Tec показано 03:00. Старые lineamientos имеют версии 2024–2025 / 2025–2026; их HOME EVENT и квоты не перенесены на сезон 2026–2027. Детские зрительские пропуска не опубликованы в прочитанных страницах.')
    assert id not in byid
    d['events'].append(e);byid[id]=e;new.append(id);ftc_ids.append(id)
    source(url,e['title'],e['proof'])
    reference(e,ftc_program,'FIRST FTC · возраст и сезон','Первичная страница: 12–18, Grades 7–12, BIOBUZZ 2026–2027.')
    reference(e,ftc_local,'México · команда и школьный уровень','До 15 членов; Grades 7–12, взрослые mentors.')
    reference(e,ftc_cost,'México · опубликованный порядок и тарифы','Активация, местный платёж, отдельная регистрация каждого этапа; национальную квалификацию и текущий счёт уточнить.')
    reference(e,ftc_schedule,'México · календарь, страницы 1 и 2','Прочитаны обе страницы календаря и все 12 отдельных событий, включая национальный.')
    e['related_ids'] = ['C800'] if not national else ftc_ids[:-1]

tec_url='https://tdrobotica.co/tecpro-challenge-2026-2027'
tec_virtual='https://drive.google.com/file/d/1UQ-IF-hHl0svWxMTaNlo9qI2H_29MxNi/preview?usp=drive_link'
tec_presencial='https://drive.google.com/file/d/155FHPkwTjHMRqx2FVbaGtKlrFt3H2VA9/preview?usp=drive_link'
conflict='В виртуальном PDF v1.0 таблица на стр. 6 даёт Entornos Inteligentes 13–18, а раздел 3.4.4 на стр. 17 — 15–18. Приоритет версии / границу уточнить. У Animaciones 5–9 и Videojuegos 8–12 такого расхождения не найдено.'
e=update('C079',title='TecPro Challenge Virtual · Match 1 · 2026',
    age='Animaciones 5–9; Videojuegos 8–12; Automatización 10–14; Entornos: конфликт 13–18 / 15–18',
    age_conflict=conflict, related_ids=['C078','C801','C802','C803','C804'],
    period='10 октября 2026 — награждение; подача зарегистрированных команд до 4 октября',
    note='Прочитанный PDF v1.0: новый приём завершился 28 сентября. Подача до 4 октября — для уже зарегистрированных команд, не новая заявка. Темы двух matches независимы. '+conflict,
    proof='Повторно прочитаны календарь и виртуальный PDF: 2–4 ученика, категория по большинству возрастов, 5–9 / 8–12, необязательный hardware для Animaciones; deadline и отдельный конфликт старшей категории.')
reference(e,tec_virtual,'TecPro Virtual · первичный v1.0','Стр. 6–7, 15–21: возраст, состав, два matches; видео ≤5 минут, минимум 3 фото, bitácora минимум 3 страницы, код; conflicting Entornos ages.')
for id,title,age,mat,osc,gear in [
    ('C801','Animaciones e Historias Interactivas','5–9 лет; категория по возрасту большинства команды',
     'Условно — в 2027 исполняется 10; нужна дата старта, возрастное отсечение и правило смешанной команды',
     'Условно — по возрасту 6–7 в 2027 подходит; действующий набор и допуск подтвердить',
     'mBlock; animaciones / интерактивная история / stop motion; физический hardware в этой категории необязателен по v1.0'),
    ('C802','Desarrollo de Videojuegos','8–12 лет; категория по возрасту большинства команды',
     'Условно — по возрасту 9–10 в 2027 подходит; действующий набор и допуск подтвердить',
     'Нет — 2020 год рождения: в 2027 максимум 7, категория начинается с 8',
     'TecPro D / E, mBlock, HaloCode / playBoard; программируемый физический интерфейс и оригинальный видеоигровой проект'),
    ('C803','Automatización','10–14 лет; категория по возрасту большинства команды',
     'Условно — в 2027 исполняется 10; конкретный день отсечения и смешанную команду подтвердить',
     'Нет — минимум категории 10, в 2027 максимум 7',
     'TecPro D / E / F / G, датчики и исполнительные устройства; mBlock / Arduino IDE / AppInventor'),
    ('C804','Entornos Inteligentes','Конфликт: таблица 13–18, раздел 3.4.4 15–18; действующую границу уточнить',
     'Нет — 2017 младше обеих опубликованных границ в 2027',
     'Нет — 2020 младше обеих опубликованных границ в 2027',
     'TecPro G / I / J, Arduino / Thonny / Visual Studio Code; connected systems, IoT / AI по проекту')]:
    e=clone('C079',id,title='TecPro Virtual · Match 2 (2027) · '+title,
        start='',end='',deadline='',deadline_utc='',deadline_label='',deadline_note='',
        date_status='Даты не объявлены',period='Второй независимый match в 2027; точный набор, подача и награждение не объявлены',
        age=age,mat=mat,osc=osc,gear=gear,
        format='2–4 ученика + взрослый mentor, уполномоченный учебным учреждением; категория по большинству возрастов',team_min=2,team_max=4,
        entry='Готовить проект по теме Bienestar Integral: Tecnología para la vida. Дождаться отдельного Match 2 calendar / convocatoria; подтвердить независимую семейную команду, смешанный возраст и школьное разрешение mentor.',
        action='Оскару рассмотреть Animaciones. Матвею Videojuegos или после возрастного отсечения Automatización. Подтвердить правила нового match до покупки набора.',
        priority='P1 — онлайн маршрут 2027 после объявления условий' if id!='C804' else 'P3 — будущий старший уровень',
        status='Следующий match ещё не открыт по опубликованному календарю',
        registration_status='Сроки и отдельная форма Match 2 не объявлены; форма Match 1 не перенесена.',
        proof='Прочитан первичный виртуальный PDF v1.0: Match 2 2027 и тема Bienestar Integral, общие категории и состав. Следующие точные дни не опубликованы.',
        references=[dict(url=tec_virtual,label='Общие правила двух matches · v1.0')],
        related_ids=['C079'], parent_event_id='', date_scope='',evidence_level='rules',admission_kind='school',
        note='Это будущая категория конкурса, не подтверждённый мировой финал. Общий v1.0 требует видео до 5 минут, минимум 3 фото, bitácora PDF минимум 3 страницы и ссылки на код; для нового набора возможна редакция. Матвей 2017 в течение 2027 меняет возраст с 9 на 10; день рождения неизвестен. '+(conflict if id=='C804' else 'EN / ES судейство конкретного match не установлено.'))
    e.pop('age_conflict',None)
    if id=='C804':e['age_conflict']=conflict

e=update('C078',title='TecPro Costa Rica · общий очный старт · 8 октября 2026',
    related_ids=['C805','C806','C079'],team_min=2,team_max=4, admission_kind='school',evidence_level='rules',
    proof='Повторно прочитаны первичный календарь и очный PDF v1.0: San José / Pueblo Antiguo 08.10.2026, 2–4 участника и уполномоченный школой взрослый; категории / техника разделены.',
    note='Это общая карточка очного старта; младшие Artifact и Game имеют отдельные карточки. Оскар и Матвей не образуют одну возрастную команду этих категорий. Независимый семейный вход ещё не подтверждён; проект готовят сами дети.')
reference(e,tec_presencial,'TecPro Presencial · v1.0','Стр. 5–8: команды 2–4, взрослый представитель школы, разные категории 6–8 / 9–12; hardware для Artifact / Game обязателен.')
for id,title,age,mat,osc,gear in [
    ('C805','Artifact Fest','6–8 лет',
     'Нет — семья сообщила возраст Матвея 9; младшая категория заканчивается в 8',
     'Условно — подходит по сообщённому возрасту 6; школьный / семейный допуск и состав подтвердить',
     'Обязательная основа playBlocks TecPro A / B; дополнительная электроника вне A / B запрещена; разрешены доступные материалы'),
    ('C806','Game Fest','9–12 лет',
     'Условно — подходит по сообщённому возрасту 9; школьный / семейный допуск и состав подтвердить',
     'Нет — сообщённый возраст 6, категория начинается с 9',
     'TecPro D / E (HaloCode), mBlock и физический интерфейс; готовая оригинальная игра по теме водных ресурсов')]:
    e=clone('C078',id,title='TecPro Costa Rica · '+title+' · 2026',age=age,mat=mat,osc=osc,gear=gear,
        related_ids=['C078'],parent_event_id='C078',event_type='Discipline',
        format='2–4 ученика + взрослый наставник, уполномоченный учебным учреждением; местный максимум уточнить',
        entry='Через специалиста TecPro / Santillana Costa Rica. Подтвердить набор именно в эту категорию, независимую семейную команду, партнёра подходящего возраста и оборудование.',
        action='Найти возрастного партнёра для категории; подтвердить места и допуск. Документация готового проекта — не позднее дня перед событием, это не установленный срок регистрации.',
        proof='Прочитаны первичный календарь San José 08.10.2026 и очный v1.0: возраст категории, 2–4, школьный mentor, собственный готовый проект и обязательный TecPro kit.',
        note='Отдельная дисциплина одного старта C078. Общий семейный состав 6 / 9 не подходит одной этой возрастной категории. Свободные места и исключение для независимой команды не подтверждены.')

# MakeX exact Jan 1 gate, re-read current source PDF. No birthday was supplied.
e=update('C609',age='6–9 лет на 01.01.2026; один ребёнок + mentor 18+',
    mat='Да по возрасту — 2017: 8–9 лет на 01.01.2026; местный допуск подтвердить',
    osc='Условно — для 2020 года рождения минимум 6 на 01.01.2026 выполняется только при рождении 1 января; точный день неизвестен',
    age_reference_date='2026-01-01',
    action='Матвею проверить Codey Rocky и действующую регистрацию. Оскару прежде всего mTiny / Soccer / Inspire / Starter; Codey возможен только после подтверждения точной даты рождения и правил.',
    proof='Повторно прочитаны местная Codey event page и PDF: 1 ученик, mentor 18+, 6–9 на 1 января текущего года; новая дата рождения семьи сопоставлена с отсечением.',
    note='Два ребёнка не могут делить одного робота между двумя командами. Для 2020 года рождения текущие 6 лет не доказывают 6 лет на 01.01.2026: без 1 января дня рождения Оскар младше минимума. Общие дни 27–29 ноября не устанавливают день Codey. Иностранный вход, взнос и deadline ещё подтвердить.')
reference(e,'https://s3.us-east-1.amazonaws.com/lms.creativakids.com/makex/Reglamento+Codey+Rocky+Theme+Park.pdf','Codey Rocky · точное возрастное отсечение','Прочитанный раздел Requisitos de participación: 6–9 на 1 января; 1 участник и mentor 18+.')

e=update('L023',city='Heredia Centro · Centro Comercial Mapache, local 2',
    age='Регулярная робототехника от 3 лет; отдельные Programming / Web курсы 14+ не перенесены на детей 6 / 9',
    themes=['robotics','coding','technology'], languages=[],language='Язык конкретных занятий не указан; ES / EN подтвердить',
    language_certainty='Испанский сайт не доказывает язык выбранной группы. Семья может учиться на EN / ES, но провайдер ещё не подтвердил преподавание.',
    participation='regular',admission_kind='program',evidence_level='program',
    format='Регулярные занятия среди недели и по субботам; точные часы выбранной группы запрашиваются отдельно',
    gear='Страница описывает LEGO Education, датчики, моторы, контроллеры и ноутбуки / планшеты; включение оборудования в тариф и платформу группы уточнить',
    entry='Выбрать группу 6 и 9 лет, оценить уровень после трёх лет соревнований и подтвердить тренера под конкретную лигу.',
    proof='Повторно прочитана первичная homepage: Heredia, занятия 3+ среди недели / субботы, LEGO Education и отдельные Web 14+. Часы, каникулярные смены и язык группы не опубликованы.',
    note='Публичная страница подтверждает учебную робототехнику, но не обещает тренерскую подготовку к конкретному международному отбору. Регулярный кружок не добавлен в календарь как зимний лагерь.')
e=update('L028',languages=[],language='Язык конкретной зимней смены не указан; ES / EN подтвердить',
    language_certainty='Испанский текст страницы каникул и CER не подтверждает преподавание выбранной смены.',
    gear='CER описывает LEGO Education, компьютеры и тестовые столы. Включение техники и конкретную платформу зимней смены подтвердить.',
    proof='Повторно прочитаны страницы Vacacionales и CER: Navidad / Año Nuevo, Pascua, verano; конкретные будущие дни, возраст и язык зимней смены не опубликованы.',
    note='Регулярные LEGO Education классы описаны отдельно от каникул. Возраст и дни регулярной группы не перенесены на зимний лагерь. Семья не зарегистрирована.')
reference(e,'https://www.robotecnia.mx/services-4','CER · оснащение и обычные занятия','Материал LEGO Education и компьютеры; это не расписание или языковое подтверждение следующего лагеря.')
update('L119',proof='Повторно прочитана первичная CS-Camp page: внешние дети, 2–8, декабрь / январь, пн–пт 08–12, Technology среди других активностей; точные дни 2026–2027 и язык не объявлены.')
update('L139',proof='Повторно прочитана первичная course page: 5 конкретных дней 7–11 декабря 2026, 10–12 лет, 10:00–12:00, presencial. Матвей 2017 не достигнет 10 в декабре 2026.',
    cost='На странице US$180 + 2% IVA; включённые материалы, место и актуальный набор уточнить',
    sessions=[dict(date='2026-12-'+str(day).zfill(2),topic='Maker: роботы, микроконтроллеры и прототипирование',start_time='10:00',end_time='12:00',timezone='America/Costa_Rica') for day in range(7,12)],date_scope='session_days')

profiles={p['id']:p for p in d['league_guide']['profiles']}
first=profiles['first'];first['event_ids'] += ftc_ids
first['nuances'].append('FTC México 2026–2027: добавлены 11 региональных этапов и национальный 12–13 февраля 2027. Сейчас оба ребёнка младше FTC. Посещение с детьми, иностранный HOME EVENT и мировая квота требуют отдельных подтверждений; старые правила 2025–2026 не перенесены.')
first['sources'] += [dict(title='FIRST FTC · текущий возраст и BIOBUZZ',url=ftc_program,checked=DAY),dict(title='FIRST México · календарь FTC',url=ftc_schedule,checked=DAY),dict(title='FIRST México · тариф и регистрация',url=ftc_cost,checked=DAY)]
first['evidence']='Дополнено по 12 индивидуальным event pages México 2026–2027, глобальной FTC странице и местному описанию / тарифам; FLL и FTC — отдельные программы.'
tec=profiles['tecpro'];tec['event_ids'] += ['C801','C802','C803','C804','C805','C806']
tec.update(name='TecPro Challenge · LATAM / Virtual',
    age_summary='Очные: Artifact 6–8, Game 9–12, Smart Cities 13–18, URFI 11–16. Virtual: 5–9 / 8–12 / 10–14; Entornos 13–18 или 15–18 — конфликт.',
    route='Очный специалист страны / школа → команда своей категории. Virtual Match 1 закрыт для новых заявок; Match 2 2027 с самостоятельной темой, точные дни не объявлены.',
    nuances=['Очный состав 6 / 9 лет не подходит одной Artifact / Game категории: нужны разные партнёры и команды.', 'Виртуальная категория определяется большинством возрастов; смешанную команду заранее согласовать. В 2027 Матвей меняет возраст с 9 на 10.', conflict, 'В virtual Animaciones hardware необязателен; это исключение не относится к очному Artifact / Game. Видео до 5 минут, минимум 3 фото и bitácora минимум 3 страницы по общему v1.0.'],
    evidence='Повторно прочитаны оба первичных v1.0 PDF и текущий календарь: аппаратные / возрастные различия и будущие сроки разделены.')
tec['sources'] += [dict(title='TecPro Presencial v1.0',url=tec_presencial,checked=DAY),dict(title='TecPro Virtual v1.0',url=tec_virtual,checked=DAY)]
for id in ['C805','C806','C801','C802','C803','C804']:
    e=byid[id]
    tec['categories'].append({k:e[k] for k in ['age','entry','language','note','source','checked']}|dict(name=e['title'],team=e['format'],hardware=e['gear'],event_id=id,age_rule='Следовать категории и действующему локальному возрастному отсечению.'))
d['league_guide'].update(version=16,checked=DAY,methodology='62 профиля семейств, лиг и программ; все 46 прежних маршрутов сохранены. Проход v16 добавляет FTC México и различия TecPro; полнота мирового календаря остаётся неподтверждённой.')

local=dict(checked=DAY,status='partial',name='Коста-Рика и Мексика',
    family='Матвей 2017 и Оскар 2020. Оба могут учиться весь день на английском и испанском — подтверждено семьёй. Точные дни рождения и классы неизвестны.',
    conclusion='Ближайший очный TecPro требует разных команд. Для ноября есть младшие MakeX-маршруты; зимние лагеря проверяются по конкретной смене. FTC добавлен для дальнейшего возраста, детский зрительский доступ не подтверждён.',
    routes=[
        dict(name='8 октября · местный старт TecPro',detail='San José, Pueblo Antiguo: Оскару Artifact 6–8, Матвею Game 9–12. Каждому нужен возрастной партнёр, собственный готовый проект и подходящий набор. Приём независимой семейной команды и свободные места ещё не подтверждены. 7 октября — срок документации по общему регламенту, а не установленный срок регистрации.',ids=['C078','C805','C806']),
        dict(name='27–29 ноября · младшие MakeX в CDMX',detail='Оскару прежде всего mTiny; общие возрастные варианты для братьев есть в Soccer, Inspire / Starter по отдельным правилам. Codey для Матвея подходит по возрасту. Оскар 2020 проходит минимум 6 на 1 января 2026 только при дне рождения 1 января; его нынешние 6 не доказывают допуск.',ids=['C020','C608','C609','C613','C614','C615']),
        dict(name='Каникулы · только конкретные смены',detail='Mount View публикует 2–8: Матвей 9 не проходит, Оскару возраст подходит; будущие дни и язык не объявлены. CENFOTEC 7–11 декабря рассчитан на 10–12: оба не подходят в 2026. RoboTecnia и Cerebritos описывают зимние лагеря без будущих точных дней, возраста и языка. Liota имеет конфликт периода и числа недель; планировать обучение по этому окну нельзя.',ids=['L119','L139','L028','L140','L141']),
        dict(name='Подготовка рядом с домом и онлайн 2027',detail='Curious Lab Minds в Heredia: регулярная LEGO-робототехника 3+, часы / язык и тренера для конкретной лиги уточнить. TecPro Match 2: для Оскара Animaciones, для Матвея Videojuegos или после отсечения Automatización. Для общей Animaciones команды в 2027 нужно уточнение: Матвею исполняется 10. Точные дни Match 2 не объявлены.',ids=['L023','C079','C801','C802','C803']),
        dict(name='FTC México · следующий возрастной уровень',detail='Первичные страницы перечисляют 11 региональных этапов с ноября 2026 по февраль 2027 и национальный 12–13 февраля в CDMX. FTC рассчитан на 12–18 / Grades 7–12: сейчас оба младше. Для семейного ознакомительного посещения нужно отдельное подтверждение; дата турнира не даёт детский пропуск или мировую квоту.',ids=ftc_ids)],
    language_result='Доступные семье EN / ES сохранены. У Curious Lab Minds и RoboTecnia убраны подтверждённые ES-теги: язык преподавания в прочитанных страницах не указан. Тайваньские Expedition27 и The Grove с явным английским сохранены.',
    open_questions=['Допуск независимых семейных команд TecPro Costa Rica, возрастные партнёры и места на 8 октября.', 'Точные даты рождения для январского отсечения MakeX; категории и день выступления внутри 27–29 ноября.', 'Классы обоих детей для школьных лиг и лагерей; год рождения не заменяет класс.', 'Зимние группы México / Costa Rica: фактические дни занятий, возраст, EN / ES, оборудование, уровень после трёх лет соревнований.', 'FTC México 2026–2027: правила иностранной команды, HOME EVENT, национальная / международная квалификация и детские посетители.'])
a=d['completeness_audit']
a.update(version=16,checked=DAY,baseline=baseline,new_ids=new,new_profiles=[],updated_ids=updated,promoted_exhibition_ids=[],local_focus=local,
    scope='Первичный аудит ближайших Costa Rica / México маршрутов: 12 датированных FTC этапов для дальнейшего возраста, отдельные младшие очные TecPro и 4 категории будущего virtual Match 2, точное отсечение Codey и перепроверка учебных кандидатов. Тайваньский раздел сохранён. Полный мировой охват ещё не подтверждён.')
a['caveats'] += ['v16: 12 FTC карточек — 11 региональных и 1 национальная. Это отдельные этапы одной сети; дети 2017 / 2020 сейчас младше FTC.', 'Будущие TecPro Match 2 карточки не имеют точных дней; dates / формы Match 1 не перенесены. Очные Artifact / Game — отдельные дисциплины одного C078.', 'Испанский сайт не доказывает преподавание на ES: для двух учебных кандидатов language tags исправлены. Языки семьи и языка программы хранятся отдельно.']
a['source_issues'] += [dict(name='TecPro Virtual · Entornos Inteligentes',status=conflict,official_alternative=tec_virtual),dict(name='FTC México · разные поколения правил',status='Календарь и регистрация указывают 2026–2027; lineamientos по прежнему URL озаглавлены 2025–2026, v080925. Их HOME EVENT, исключения и квоты не считаются текущим регламентом 2026–2027.',official_alternative=old_rules)]
a['source_issues'][-1]['status']+=' На старой странице тарифы MX$6 960 / 3 500; Costo y Registro с ссылкой на сезон 2026–2027 показывает MX$7 500 / 3 750. Для оплаты нужен действующий счёт; прошлые суммы не применены.'
source(old_rules,'FTC México · прежние lineamientos v080925','Прочитана первичная страница: заголовок 2025–2026, версия 080925, deadline 31.10.2025, старые тарифы и HOME EVENT. Не перенесена на 2026–2027.')
a['known_backlog'].append(dict(kind='Коста-Рика / Мексика',name='Независимый допуск, зимние смены и FTC правила нового сезона',reason='; '.join(local['open_questions']),url=tec_url))
d.update(asof=DAY,source_count=len(d['sources']))
d['expansion_log'].append(dict(version=16,date=DAY,scope='Costa Rica / Mexico primary near-term and progression pass',added_ids=new,updated_ids=updated,notes=['Сохранены все 1063 исходных ID, 62 профиля, 46 маршрутов и 37 тайваньских карточек.', '11 FTC региональных и национальный имеют отдельные прочитанные event pages.', 'Год рождения Оскара сопоставлен с январским отсечением Codey; неподтверждённые camp ES tags убраны.', 'Никаких вымышленных зимних смен или дней virtual Match 2.']))
(ROOT/'data/local-audit-v16.json').write_text(json.dumps(dict(version=16,focus=local,added_ids=new,updated_ids=updated,source_issues=a['source_issues'][-2:]),ensure_ascii=False,indent=2))
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text())
plan.update(updated=DAY,status='active',completeness_audit='data/audit-v16.json')
for r in plan['requirements']:
    if r['id']=='global_competitions':r['evidence']='v16: добавлены 11 региональных FTC México + национальный, 2 очные младшие TecPro категории и 4 future Match 2. 62 профиля и 46 маршрутов сохранены; местный мировой охват частичный.'
    if r['id']=='camps':r['evidence']='v16: первично перепроверены Curious Lab Minds, RoboTecnia, Mount View и CENFOTEC. Отменены два неподтверждённых ES-тега; конкретные зимние дни не придуманы. Две тайваньские EN-смены сохранены.'
    if r['id']=='eligibility':
        r['evidence']='v16: семья 2017 / 2020 и EN / ES подтверждены. Codey требует возраста на 01.01.2026; Оскару нужен точный день. TecPro очный требует разных команд, FTC младше возрастного уровня; виртуальный Entornos имеет конфликт 13–18 / 15–18.'
        r['remaining']='Точные дни рождения и школьные классы; семейный / иностранный допуск, язык конкретных занятий и судейства, действующие правила национальных квот.'
plan['latest_validation']=dict(version='v16',status='pending',research_status='active')
plan['next_research'].insert(0,'Costa Rica / México: '+ '; '.join(local['open_questions']))
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2))
PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(dict(added=len(new),total=len(d['events']),updated=updated,new_ids=new),ensure_ascii=False))
