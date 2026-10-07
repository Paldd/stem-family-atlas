"""Brazil / Uruguay / Paraguay / Bolivia primary-source follow-up, baseline v17.

No website language is promoted to teaching or judging language. Co-located
visitor access, project selection and championship qualification are distinct.
"""
import copy, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'data/catalog.json'
d = json.loads(PATH.read_text()); DAY = '2026-10-01'
assert len(d['events']) == 1102 and d['completeness_audit']['version'] == 17
baseline = copy.deepcopy(d['completeness_audit']['counts'])
byid = {e['id']: e for e in d['events']}; new = []; updated = []

def source(url, title, proof):
    row = next((s for s in d['sources'] if s['url'] == url), None)
    if row: row.update(checked=DAY, evidence=proof)
    else: d['sources'].append(dict(url=url, title=title, checked=DAY, evidence=proof))

def add(id, block, title, country, city, url, **kw):
    assert id not in byid
    e = dict(id=id, block=block, title=title, country=country, region='Южная Америка', city=city,
        source=url, checked=DAY, start='', end='', deadline='', period='Следующие даты не объявлены',
        date_status='Не объявлено', age='Минимальный возраст / класс не опубликован',
        mat='Условно — класс, иностранный и детский допуск подтвердить', osc='Условно — класс, иностранный и детский допуск подтвердить',
        format='Команда / группа по действующей категории', participation='team', admission_kind='open_application',
        entry='Согласовать конкретную категорию, документы, иностранный приём и язык до поездки.',
        gear='По текущим правилам категории / программы', cost='Текущий тариф выбранного набора уточнить',
        language='Язык занятий / судейства ES / EN не подтверждён', languages=[],
        language_certainty='Язык страницы или перевода правил не доказывает язык преподавания / интервью.',
        scope='national', level='Национальное направление / местный этап',
        importance_reason='Редакционная оценка по опубликованному формату и охвату; не мировой официальный рейтинг.',
        reward='Результат / сертификат выбранного формата; международный титул не гарантирован',
        priority='P2 — подготовка / поездка после подтверждения', status='Идея',
        action='Проверить новую convocatoria, возрастной уровень и право семейной заявки.',
        themes=['robotics','coding','technology'], evidence_level='rules', references=[], related_ids=[],
        registration_status='Семья не зарегистрирована; опубликованная форма не доказывает принятый допуск или места.',
        note='Точные дни рождения и школьные классы Матвея и Оскара неизвестны.', proof='Прочитан первичный источник.')
    e.update(kw)
    if e['start']: e['date_status']='Подтверждено'
    d['events'].append(e); byid[id]=e; new.append(id); source(url,title,e['proof']); return e

def ref(e,url,label,proof):
    e['references'].append(dict(url=url,label=label)); source(url,label,proof)

obr='https://obr.robocup.org.br/'
obrfaq=obr+'perguntas-frequentes/'
practice=obr+'wp-content/uploads/2026/03/OBR2026_MP_Manual-de-Inscricao.pdf%20'
theory=obr+'wp-content/uploads/2026/03/OBR2026_MT_Manual-de-Inscricao.pdf%20'
obrnews=obr+'2026/03/12/inscricoes-abertas-para-a-olimpiada-brasileira-de-robotica-2026/'
robotica='https://robotica.robocup.org.br/'
cbrcat='https://cbr.robocup.org.br/index.php/categorias/'
cbrentry='https://cbr.robocup.org.br/index.php/inscricoes/'
cbrpay='https://cbr.robocup.org.br/index.php/pagamentos/'
mnrtime='https://mnr.robocup.org.br/cronograma/'
mnrfaq='https://mnr.robocup.org.br/faq/'

# OBR is school-grade based. A garage tutor is expressly allowed for practical
# entries; it does not by itself establish tourist/foreign admission.
obr_ids=[]
for n,level,grade,exam in [(820,0,'1-й год Ensino Fundamental','10 вопросов / 1 час / одна фаза'),(821,1,'2–3-й год Ensino Fundamental','15 вопросов / 2 часа / две фазы'),(822,2,'4–5-й год Ensino Fundamental','15 вопросов / 2 часа / две фазы')]:
    id='C'+str(n); obr_ids.append(id)
    e=add(id,'Соревнования',f'OBR Brasil · Teórica Nível {level} · следующий сезон','Бразилия','Школьная площадка / разрешённая online application',theory,
        age=grade+'; максимум 19 лет в году соревнования, уровень определяется классом',participation='individual',admission_kind='school',
        format='Индивидуальная письменная олимпиада: '+exam,gear='Не требуется физический робот; задания / supervised exam по уровню',
        entry='Учитель / tutor регулярной школы подаёт ученика через Olimpo. В FAQ tutor 18+ связан со школой с INEP; эквивалент школы Costa Rica и иностранный допуск не установлен.',
        cost='OBR бесплатна, включая регистрацию и награды; поездка / подготовка отдельно',
        reward='Медаль по индивидуальному баллу; это не место роботизированной команды и не автоматическая RoboCup квота',
        proof='Прочитан PDF регистрации Teórica 2026, страницы 9–12: таблица классов, время, вопросы, школьная регистрация; FAQ и сезонная новость сверены.',
        historical_editions=[dict(year=2026,phase1_window_start='2026-06-08',phase1_window_end='2026-06-12',phase2_days=[] if level==0 else ['2026-08-11','2026-08-12','2026-08-13'])],
        note='2026 приём / экзамены прошли. Даты следующего сезона не объявлены. Возраст 6 / 9 не заменяет класс; бумаги на португальском не подтверждают экзамен ES / EN.')
    ref(e,obrfaq,'OBR FAQ · школьная регистрация','Теоретический tutor связан с INEP school; практическая garage team допускается отдельно.')
    ref(e,obrnews,'OBR 2026 · опубликованные прошлые сроки','2026 Teórica: регистрация до 12 июня; фаза 1 8–12 июня, фаза 2 11–13 августа.')
practical=[(823,'Resgate Nível 0','1–3-й год Ensino Fundamental','Региональный / штатный этап; национального финала для Nível 0 нет'),
 (824,'Resgate Nível 1','Регистрационный PDF: 1–8-й год Ensino Fundamental','Региональный / штатный этап → национальный отбор'),
 (825,'Artística Nível 1','Регистрационный PDF: 1–8-й год Ensino Fundamental','Региональный / штатный этап → национальный отбор'),
 (826,'Virtual Simulação Nível 1','Регистрационный PDF: 1–8-й год Ensino Fundamental','Virtual Simulação; отдельный порядок и дни объявляет coordenação')]
for n,name,grade,route in practical:
    id='C'+str(n);obr_ids.append(id)
    e=add(id,'Соревнования','OBR Brasil · '+name+' · следующий сезон','Бразилия','По региональному календарю' if n!=826 else 'Online · sBotics',practice,
        age=grade+'; уровень по классу, верхняя граница 19 в году',format='Команда одного уровня; численность по действующим правилам испытания',
        participation='team',admission_kind='school',scope='online' if n==826 else 'national',
        entry='Tutor / professor / collaborator, включая equipe de garagem без привязки tutor к учреждению. Ученик указывает класс и документы; иностранная школа и локальная зона требуют отдельного подтверждения. '+route+'.',
        gear='sBotics: виртуальный rescue robot' if n==826 else 'Авторский автономный робот; решение, сборка и программирование выполняются детьми',
        cost='OBR бесплатна; оборудование / поездка отдельно',reward='Региональная награда без национального / мирового выхода' if n==823 else 'Награда выбранного уровня; регистрационный PDF даёт RoboCup international route для Nível 2, не обещает его Nível 1',
        proof='Прочитан PDF Práticas 2026: с.9 уровни и маршруты, с.11 tutor / garage и класс, с.20 garage, с.34 паспорт / CPF; FAQ подтверждает различные школы одной команды.',
        note='Один ученик — одна presencial команда (Resgate ИЛИ Artística), допускается дополнительная virtual команда. Состав после квалификации не меняется. В PDF Nível 1 указан 1–8 и Nível 2 с 8: перекрытие 8-го класса и формулировка Anos Iniciais требуют проверки конкретного manual. Будущие дни не придуманы. Parents не работают над роботом и не входят в рабочую зону.',
        historical_editions=[dict(year=2026,regional_window_start='2026-05-29',regional_window_end='2026-09-13')])
    ref(e,obrfaq,'OBR FAQ · garage / tutor / школа','Garage разрешена только Práticas; tutor старше18; ученики разных школ могут объединяться; общий scope школы по территории Brasil.')
    ref(e,obrnews,'OBR 2026 · национальная дата','Новость национальный этап 23–29 ноября, мартовский PDF 23–27 ноября; младшая будущая региональная заявка из этого не следует.')

# Concrete CBR disciplines retain the CLOSED initial-entry deadline, not payment
# windows as if they were new application windows.
cbr_ids=[]
for n,title,age in [(827,'RCB Challenge','Страница категории: без ограничения возраста / школьного уровня'),(828,'RoboCupJunior Soccer Entry-Level','12–16 лет во время соревнования'),(829,'RoboCupJunior Soccer Infrared','14–19 лет на 1 июля года соревнования'),(830,'RoboCupJunior Soccer Vision','14–19 лет на 1 июля года соревнования')]:
    id='C'+str(n);cbr_ids.append(id)
    url='https://cbr.robocup.org.br/wp-content/uploads/2026/07/Regras_Challenge_2026_Portugues-V1.0.pdf' if n==827 else 'https://cbr.robocup.org.br/wp-content/uploads/2026/07/entry_rules_PtBR.pdf' if n==828 else 'https://cbr.robocup.org.br/wp-content/uploads/2026/06/rules_PtBR.pdf'
    e=add(id,'Соревнования','CBR Petrobras 2026 · '+title,'Бразилия','João Pessoa · Centro de Convenções',url,
        start='2026-11-23',end='2026-11-29',period='',deadline='2026-08-24',age=age,
        mat='Условно по возрасту RCB; приём 2026 уже закрыт и требуется учебное учреждение' if n==827 else 'Нет — младше '+('12' if n==828 else '14')+' лет',
        osc='Условно по возрасту RCB; приём 2026 уже закрыт и требуется учебное учреждение' if n==827 else 'Нет — младше '+('12' if n==828 else '14')+' лет',
        format='Команда учреждения; у RCJ 2–4 учащихся и mentor, у Challenge размер согласовать',
        entry='Первичная заявка Olimpo 22 июня–24 августа; команды представляют educational institution. Результаты отбора до 21 сентября. Новая заявка семьи в октябре не объявлена.',
        priority='P4 — приём закрыт; сохранить для будущего маршрута',status='Приём закрыт',
        registration_status='Первичная регистрация закрыта 24 августа. Early / Regular payment до 29 октября / 15 ноября относится к уже принятым командам; поздняя оплата только их дополнительным членам.',
        cost='RCJ: R$1130 Early / R$1460 Regular за 2 студентов и professor; иностранный RCJ тариф уточнить. Non-Brazilian Major: USD295 / 370 за 3 — не переносить автоматически на Junior.',
        gear='Один автономный робот ≤300×300 мм; hardware / kits свободны; камеры, LiDAR и обработка изображений запрещены' if n==827 else 'Один автономный robot, 1v1; только новые команды и никогда не участвовавший RCJ Soccer robot' if n==828 else 'Два автономных робота: Infrared ≤1.5 kg / Ø22cm; Vision Ø18cm без лимита веса',
        reward='Протокол CBR дисциплины; мировая квота зависит от national representative и правил лиги',
        proof='Прочитаны текущие category / entry / payment pages и связанный PDF: RCB hardware; Entry12–16; Soccer14–19 на1July. Initial deadline и foreign Major tariff отделены от Junior.',
        note='Даты — окно всего CBR; индивидуальный день дисциплины не опубликован в этих источниках. Entry максимум два участия и не международная лига финала. EN-приоритет текстов правил не доказывает EN интервью. RCJ ученик только одной категории всего события, включая OBR.')
    for u,label,proof in [(cbrcat,'CBR · категории 2026','RCB без возрастного минимума; RCJ Entry12–16; OBR и Junior не смешиваются.'),(cbrentry,'CBR · первичная регистрация','Подача до24Aug и institution обязательны; окна оплаты отдельные.'),(cbrpay,'CBR · правила оплаты / foreign teams','Non-Brazilian Major тариф опубликован; Junior2–4 и instructor visitor area only.')]:ref(e,u,label,proof)

mnr_ids=[]
for n,title,start,end,city,deadline,closed in [(831,'Nacional Virtual','2026-10-28','2026-10-30','Online · проектная защита','2026-07-15',True),(832,'Nacional Presencial · дни презентаций','2026-11-26','2026-11-28','João Pessoa · Centro de Convenções','2026-07-15',True),(833,'Mato Grosso · estadual','2026-10-22','2026-10-24','Rondonópolis · Universidade Federal de Rondonópolis','2026-10-04',False),(834,'Oiapoque · regional','2026-10-09','2026-10-09','Aldeia Manga · Escola Estadual Indígena Jorge Iaparrá, Amapá','2026-09-30',True)]:
    id='C'+str(n);mnr_ids.append(id)
    e=add(id,'Соревнования','MNR 2026 · '+title,'Бразилия',city,mnrtime,start=start,end=end,period='',deadline=deadline,
        age='Регулярно зачисленные школьники Ensino Fundamental / Médio / Técnico и старшие; минимальный возраст не указан',
        participation='team',admission_kind='school_selection',scope='online' if n==831 else 'national' if n in [831,832] else 'regional',
        format='Оценка проекта, не заезды; максимум 6 студентов + orientador + до 2 co-orientadores',
        entry='Подать проект и всех authors через Olimpo; пройти экспертную оценку. Школьный orientador входит в authors. Детские и иностранные документы / local quota уточнить.',
        gear='Робототехнический проект / статья или multimedia; presencial poster; virtual 5 минут защиты + 5 минут вопросов',
        cost='MNR публичная бесплатная инициатива; транспорт, poster / техника отдельно',
        priority='P4 — заявка закрыта / уже нужен отобранный проект' if closed else 'P2 — срок 4 октября, допуск подтвердить',
        status='Приём закрыт' if closed else 'Идея',registration_status='National подача до15July и выбор modality до30September уже закрыты.' if n in [831,832] else 'Опубликованный региональный срок '+deadline+'; иностранный / семейный приём и места не подтверждены.',
        reward='После оценки: публикация в Anais / certificado; для лучших школьных работ menção honrosa. Публикация не равна выигранной мировой медали.',
        proof='Прочитаны current cronograma / FAQ: будущий этап, registration deadline, max6 students, school enrollment, virtual / presencial formats и награды. Главный Robótica portal независимо подтверждает общий ноябрьский фестиваль.',
        note='National presencial event24–29Nov, проекты26–28Nov, cierre29Nov; не все7дней — защита ребёнка. Один national проект выбирает virtual ИЛИ presencial. Региональный этап не даёт автоматически национальную заявку после15July. В HTML MNR найдены посторонние SEO-вставки; точный локальный день и допуск перепроверить перед поездкой.')
    ref(e,mnrfaq,'MNR · авторы / школа / оценка','Max6 students, orientador, school enrollment; virtual5+5min, один national формат; escolar honorarymentions / anais / certificate.')
    if n==832:ref(e,robotica,'Robótica · общий фестиваль','23–29NovJoãoPessoa и MNR как отдельная project show; publicentryfree.')

# Paraguay local FLL requirements are not replaced with global default sizes.
pyseason='https://fll.robotica.com.py/temporada-2026-2027/'
fll_ids=[]
for n,name,ages,team,url in [(835,'Explore','6–10','3–6','https://fll.robotica.com.py/explore/'),(836,'Challenge','9–16','3–10','https://fll.robotica.com.py/challenge/')]:
    id='C'+str(n);fll_ids.append(id)
    e=add(id,'Соревнования','FIRST LEGO League Paraguay · '+name+' · BIOGLOW 2026–2027','Парагвай','Национальная площадка ещё не объявлена',url,
        age=ages+' лет; возрастное отсечение сезона / иностранный допуск уточнить',
        mat='Условно — подходит диапазон '+ages+'; страна, состав и cutoff требуют подтверждения',
        osc='Условно — подходит диапазон6–10; foreign entry / cutoff подтвердить' if n==835 else 'Нет — младше9 лет',
        format=team+' ребёнка + взрослый coach; братьев вдвоём недостаточно для опубликованного местного минимума3',
        entry='Национальный partner и действующая registration offer; нужна команда и регистрация именно Paraguay. Прямая заявка иностранной семьи / право представлять Paraguay не установлены.',
        gear='WeDo2.0 / SPIKE Essential, LEGO motorizedmodel и Show me Poster; минимум12sessions' if n==835 else 'Robotgame + innovationproject + corevalues; текущий разрешённый kit BIOGLOW подтвердить. Старая programme page называет EV3 / SPIKE Prime.',
        reward='Explore: фестивальное представление и признание; соревновательный мировой титул не обещан' if n==835 else 'Национальное место / award; WorldFestival только по подтверждённой квоте и отбору',
        proof='Прочитаны local pages Explore6–10,3–6; Challenge9–16,3–10,12weeks; separate2026–2027 season page BIOGLOW. Индивидуального будущего event date не найдено.',
        note='Основные programme pages сохраняют SUBMERGED2024–2025, registrationpage 2025–2026; seasonpage уже BIOGLOW. Это расхождение редакций, не доказательство действующей старой цены / EV3допуска. Будущая дата national не придумана.')
    ref(e,pyseason,'Paraguay · BIOGLOW 2026–2027','Прямое объявление текущей темы; даты, team deadlines и foreign rules не указаны.')
    ref(e,'https://fll.robotica.com.py/inscripciones/','Paraguay · страница регистрации','Страница формы без даты; часть navigation всё ещё2025–2026. Оплата / регистрация семьи не сделаны.')
vexpy='https://events.vex.com/robot-competitions/vex-iq-competition/RE-VIQRC-26-5257.html'
e=add('C837','Соревнования','LNR Paraguay · VEX IQ · следующий этап сезона 2026–2027','Парагвай','Asunción · следующую sede подтвердить',vexpy,
    age='Предыдущий этап: Grade Level All; global IQ Elementary ≤12 / Middle≤15, сезонное отсечение по действующим rules',
    mat='Условно — VEX IQ школьный путь; grade / nationality / national quota подтвердить',osc='Условно — Grade All не снимает требования самостоятельной работы и актуального age cutoff',
    format='Зарегистрированная VEX IQ team; Robot Skills / teamwork и очное judging / physical notebook',
    entry='Reeduca организует Paraguay LNR; eventregistration и country eligibility отдельны. Следующий конкретный этап не найден; 5 сентября уже прошёл.',
    cost='Прошедший RE-VIQRC-26-5257 был FREE; будущая team season registration / event fee не установлены',
    historical_editions=[dict(start='2026-09-05',end='2026-09-05',event_code='RE-VIQRC-26-5257',venue='Colegio del Sol · Asunción',registration_deadline='2026-09-03')],
    proof='Прочитана индивидуальная VEX page: дата5Sep, All grades, localteamregistration deadline3Sep, closed, in-person notebook. Sponsor current statement читан отдельно:4 preparatory+nationalfinal, без точных оставшихся дат.',
    note='Старый видимый счетчик17places относится к закрытому прошлому старту. Пять этапов не размножены в пять фиктивных дат. LNR Paraguay используетVEX и не является аргентинской LNR.')
pylnr='https://www.ueno.com.py/2026/07/24/la-liga-nacional-de-robotica-en-busca-de-los-proximos-campeones-mundiales/'
ref(e,pylnr,'LNR Paraguay · сообщение партнёра сезона','Season4preparatory+nationalfinal, nationalrepresentation; точные будущие дни и права foreign teams не опубликованы.')
ref(e,'https://library.globalrobotics.org/hc/en-us/articles/51371951587732-Student-Eligibility-Policy','VEX · ранее проверенные глобальные рамки','Ранее проверенный source в profileVEX; localAllGrades не отменяет global eligibility. Повторное чтение policy в этом проходе не заявлено.')

sucre='https://sucre.bo/%F0%9D%90%84%F0%9D%90%8B-11-%F0%9D%90%98-12-%F0%9D%90%83%F0%9D%90%84-%F0%9D%90%80%F0%9D%90%81%F0%9D%90%91%F0%9D%90%88%F0%9D%90%8B-%F0%9D%90%92%F0%9D%90%94%F0%9D%90%82%F0%9D%90%91%F0%9D%90%84/'
add('C838','Соревнования','Sucre–Bot · Campeonato Nacional Abierto · следующее издание','Боливия','Sucre · будущую sede подтвердить',sucre,
    age='Дети, студенты, amateurs / professionals; точного минимума6/9 и иностранных правил не опубликовано',format='Муниципальное объявление2026:2участника в команде',
    gear='Minisumo, linefollowing, soccer, robotcombat, maze, creativity / innovation — разные category rules',
    entry='Получить действующий reglamento конкретного испытания и иностранный/детский допуск. Название Abierto не подтверждает туристическую команду.',
    historical_editions=[dict(year=2026,start='2026-04-11',end='2026-04-12',registration_deadline='2026-04-10',venue='Coliseo de Facultad de Tecnología · Sucre')],
    proof='Прочитано организаторское municipal announcement1Apr2026:11–12Apr, deadline10Apr,2members и перечень дисциплин; следующий выпуск не объявлен.',
    reward='2026 municipal call: medals / certificates / cashprizes и internationalaccreditation winners; конкретная будущая квота / worldcompetition не установлены',
    note='Прошедшие дниApril2026 не перенесены в2027. Аккредитация организатора для выезда не равна подтверждённой международной победе.')
add('C839','Соревнования','FIRST Bolivia · национальная программа / следующий отбор','Боливия','Национальные / местные площадки уточнить','https://agetic.gob.bo/node/4303',
    age='AGETIC называет youth / schoolprogramme, но не публикует возраст Tecnólogos / Inventores на этой странице; FIRSTGlobal world14–18 — отдельная рамка',
    format='Национальная programme: Tecnólogos Disruptivos / Inventores Disruptivos; формат текущего отбора уточнить',admission_kind='school_selection',
    priority='P3 — будущий маршрут после конкретной convocatoria',
    entry='Местные Tecnólogos / Inventores и selection страны не смешивать с мировой FIRSTGlobal team. СемьяMexico/CostaRica не получает Bolivia country slot автоматически.',
    proof='Прочитана текущая AGETIC programme page: национальный отбор, две категории, STEM и countryrepresentation; нового calendar / localages / foreignentry нет.',
    note='Следующая национальная convocatoria и границы местных двух категорий неизвестны. Основная FIRSTGlobal сборная14–18 не подходит братьям сейчас; возраст местных Inventores отдельно не установлен.')

# Uruguay: published holiday cohorts are February 2026, not an announced 2027
# camp. Each curriculum and campus is separately selectable in the primary page.
wecode='https://www.wecode.edu.uy/verano'
for n,topic,grade,themes in [(155,'Laboratorio de verano','2–3-й школьный класс',['robotics','coding','technology']),(157,'Inteligencia Artificial','4–6-й школьный класс',['ai','coding','technology']),(159,'Minecraft Coding Nivel 1','4–6-й школьный класс',['games','coding','technology'])]:
    for j,city in enumerate(['Montevideo · Pocitos','Ciudad de la Costa']):
        add('L'+str(n+j),'Лагеря','WeCode · '+topic+' · '+city+' · следующий набор','Уругвай',city,wecode,
            age=grade+'; календарный возраст не указан',format='Каникулярный курс:3встречи в неделю, не целодневный лагерь',participation='regular',admission_kind='program',scope='local',themes=themes,
            gear='Laptop; robots / experiments' if n==155 else 'Laptop; обучение распознаванию изображений, звуков и движений' if n==157 else 'Laptop; программирование структур вMinecraft',
            entry='Сверить класс новой holidaycohort, foreignvisitor admission и преподавание ES/EN. Старый banner Inscripciones abiertas не является новой сменой.',
            reward='Учебный проект / сертификат курса; не международная соревновательная победа',evidence_level='historical_program',
            historical_editions=[dict(year=2026,month='2026-02',published_grade=grade,venue=city)],
            proof='Прочитана первичная summerpage: каждая curriculum/campus карточка явноFebrero2026, degree selector2026,3weeklymeetings; будущего2027calendar нет.',
            note='Noexperience required; regularFAQ certificates / extraclubs не доказывают holiday judging или языковую группу. Семья EN/ES готова, преподавание программы пока не установлено.')
mot='https://www.mindsoftomorrowparaguay.com/colonias-tecnologia'
mots2='https://www.mindsoftomorrowparaguay.com/colonia-s2-2026'
motcity='Asunción · Guardería Lullabies, 2-й этаж · Austria2400 / HerminioMaldonado, входB'
add('L161','Лагеря','Minds of Tomorrow Paraguay · Colonias de Tecnología · будущие каникулы','Парагвай',motcity,mot,
    age='5–12 лет по programme page; документы и конкретный поток подтвердить',mat='Да по возрасту5–12; будущий набор / язык / foreignentry подтвердить',osc='Да по возрасту5–12; будущий набор / язык / foreignentry подтвердить',
    participation='day_camp',admission_kind='program',scope='local',themes=['coding','robotics','technology','makers'],evidence_level='program',
    format='Разовые дни или недельные colonias;09:00–15:30 / полдня;extendedcareдо17 по запросу',
    entry='Подтвердить будущие summerdays и language; primarys2page сообщает новую sede с1Aug2026 вместо старого MayorRivarola465.',
    cost='GenericFAQ:Gs250000/day илиGs1200000/week; следующая конкретная offer / питание / extendedcare отдельно',
    reward='CreativeTech learningproject; это не FLL / VEX championship',
    proof='Прочитаны genericcamp page:5–12, day/week,09–15:30, fees; freshHTMLs2primary: новая sedeAustria2400 с1Aug2026.',
    note='Описания программ могут включать robotics/coding/engineering; точный curriculum каждого campday меняется. Старые2025–26summerdates не перенесены на2027. Старый genericaddress отличается от новой primarys2sede.')
e=add('L162','Лагеря','Minds of Tomorrow Paraguay · Colonia Halloween · 31 октября 2026','Парагвай',motcity,mots2,
    start='2026-10-31',end='2026-10-31',period='',age='5–12 лет',mat='Да по возрасту; доступ / language / места подтвердить',osc='Да по возрасту; доступ / language / места подтвердить',
    format='CreativeTech day09:00–15:30 или полдня09–12 /12:30–15:30',participation='day_camp',admission_kind='program',scope='local',themes=['technology','makers'],evidence_level='program',
    gear='HalloweenBingo, создание летучих мышей и pumpkins; наличие программирования / robots именно в этом дне не заявлено',
    date_scope='session_days',sessions=[dict(date='2026-10-31',topic='Colonia Halloween · творческие задания; robotics / coding не подтверждены для этого дня',start_time='09:00',end_time='15:30',timezone='America/Asuncion',time_note='Полдня09:00–12:00 либо12:30–15:30 — альтернативные варианты записи.')],
    cost='Конкретная текущая Halloweenoffer не прочитана; genericcampFAQ цены не считать оплаченной бронью',
    reward='Учебный день / поделки, без соревновательного международного титула',
    entry='Опубликован конкретный день и новая sede; подтвердить уровень, преподавание ES/EN и места у organizer.',
    proof='FreshpublicHTMLs2page прочитан напрямую:Halloween31.10.2026,5–12,09–15:30илиполдня,Austria2400новаяsede.',
    note='Предыдущие дни15Aug/28Sep2026 уже прошли. Это CreativeTech holidayday, не подтверждённая робототехническая смена. Текущий набор свободных мест и teachinglanguage не опубликованы.')
ref(e,mot,'MOT · общая programme','Общая programme5–12 иday/weekварианты; названиебренда не доказываетcodingвHalloween.')
add('L163','Лагеря','UMSA IIME · Robótica Especializada Nivel 1 · следующий набор','Боливия','La Paz · UMSA IIME · будущую учебную aula уточнить','https://ingenieriamecanica.umsa.bo/index.php/2026/08/14/titulo/',
    age='9–14 лет по прочитанному2026курсу',mat='Условно — достиг9, иностранный ребёнок / новый поток / язык подтвердить',osc='Нет — младше9',
    participation='regular',admission_kind='program',scope='local',evidence_level='historical_program',
    format='2026course:12sessions/30academic hours;Mon/Wed/Fri09–11:30 ИЛИ15–17:30, max15pergroup',
    gear='Tinkercad / blockcoding / Arduino / motors / sensors / Bluetooth; kits предоставлялись',cost='ПрошедшаяofferBs250inclkits; новый счёт / intake не объявлены',
    historical_editions=[dict(year=2026,published_window_start='2026-08-02',published_window_end='2026-09-25')],
    proof='Прочитан currentofficialIIMEHTML:9–14,dates2Aug–25Sep2026,12sessionplan,30academic hours,Bs250,max15,alternativetime.',
    note='Headerdated14Aug,footerposted13Sep; publishedstart2Augвоскресенье противMon/Wed/Fri,30academic hours противширокогоокна. Не создан вымышленный будущий календарь поbannerInscribite. Финальный учебныйtorneo не объявлен самостоятельноймеждународнойнаградой.')
add('L164','Лагеря','Jopoi Bolivia · Taller de Robótica micro:bit · следующий набор','Боливия','Porongo / Santa Cruz · Jopoi ecosistema · workshopvenue подтвердить','https://jopoi.com.bo/programas/taller-de-robotica/',
    age='8–12 лет',mat='Условно — возраст подходит; новый набор / язык / foreignentry подтвердить',osc='Нет — младше8лет',
    participation='regular',admission_kind='program',scope='local',evidence_level='program',format='Субботние workshops09:30–12:00; целодневные каникулы не объявлены',
    gear='micro:bit / MakeCodeArcade / roboticarm / 3Dprint/Tinkercad; материалы предоставляются',
    proof='Прочитана primaryroboticsprogramme:8–12,Saturday09:30–12,31August–30Novemberбез года; materialprovided.',
    note='Годroboticstermне указан; он не принят автоматически за2026. Отдельныйsummercamp2–20Decна сайте явно2024 и nature/art/horse activities; его не выдали заробототехническийлагерь2026/2027.')
add('L165','Лагеря','AGETIC Bolivia · CiberneTICs Kids · учебная программа','Боливия','Локальные aulas / новый набор уточнить','https://agetic.gob.bo/cibernetics',
    participation='regular',admission_kind='program',evidence_level='program',themes=['ai','robotics','coding','technology'],
    format='Государственная kidsprogramme; campdays, расписание иholidayformat не опубликованы',priority='P3 — изучить конкретную convocatoria',
    gear='Programming / robots / virtualreality / AI / digitalsafety поprogrammedescription',
    proof='Прочитана primaryAGETICprogramme: реальныеkidsaulas итемыAI/robotics; точныйage,foreigndocuments,newdaysиlanguageнеустановлены.',
    note='Национальнаяinitativeне являетсяподтверждённымтуристическимEN/ESлагерем; языковойфильтрне включён. Дни следующегонаборанепридуманы.')

e=add('E130','События','Robótica 2026 · публичное посещение фестиваля','Бразилия','João Pessoa · Centro de Convenções',robotica,
    start='2026-11-23',end='2026-11-29',period='',participation='visitor',admission_kind='visitor',scope='national',
    age='Entrada gratuita; отдельные возрастные условия посетителя6/9 наportalнеопубликованы',
    mat='Условно — входfree, minorvisitorpolicyподтвердить',osc='Условно — входfree, minorvisitorpolicyподтвердить',
    format='Посещение robotarenas / MNRprojects; academicworkshopsотдельно',entry='Главныйportalобъявляетбесплатныйвход. Уточнитьдетскийбилет/сопровождение иvisitorhours; competitorregistrationотдельна.',
    gear='Дляпосетителясобственныйrobotне нужен',cost='Общийвходfree; academicregistration/workshopможеттребоватьотдельныхусловий',priority='P3 — посещениеприудобнойпоездке',
    reward='Демонстрации / образовательныйвизит; наградасоревнованиянепредусмотрена',themes=['robotics','ai','technology'],evidence_level='event_page',
    proof='ПрочитанcurrentRobóticaportal:23–29Nov,CentrodeConvençõesJoãoPessoa,Entrada gratuita,CBR/OBR/MNRиacademicco-locatedevents.',
    note='Семидневноеокнофестивалянеозначаетсемьучебныхднейиликвотувфинал. Academicregistrationaccessксимпозиумамнеперенесённабесплатногопосетителя.',
    exhibition_tier='regional',visitor_policy='confirm_children',visitor_policy_note='Бесплатныйобщийвходпрямозаявлен; нижнийвозраст,childticket/supervisionещёуточнить.',
    highlights=['АвтономныероботыCBR','НациональныефиналыOBR','ОценкапроектовMNR'],
    exhibitor_note='Фестивальсоревнований/проектов; каталогвсехмировыхпроизводителейнеобещан.',exhibitor_directory_url=robotica,adult_entry='Входfreeпоглавномупорталу;режимvisitorhoursуточнить.')
ref(e,mnrtime,'MNR · точныеprojectdays','Проекты26–28Nov;nationalMNRevent24–29Nov,общийRobótica23–29Nov.')
e=add('E131','События','MuCi San Cosmos · цифровой планетарий / семейный STEM визит','Парагвай','Asunción · Complejo Textilia · actualshowticketvenueуточнить','https://muci.org/',
    age='Организатор:дети,молодёжь,взрослые;sessionageadvisory/сопровождениеуточнить',
    mat='Да пообщемусемейномуформату;возрастконкретногоshowуточнить',osc='Да пообщемусемейномуформату;возрастконкретногоshowуточнить',
    participation='visitor',admission_kind='visitor',scope='local',format='Регулярныедемонстрациицифровогопланетария;выбратьконкретныйshowtime',themes=['technology','science'],
    entry='ВыбратьдействующиесеансыSanCosmos/билеты. TatakuaLabзакрытсмарта2026;будущийосновнойMuseoпланируетсяпримерно2028.',
    gear='Цифровыеimmersiveshows;коммерческаяrobot/AItradeвыставканеобъявлена',
    reward='Семейныйобразовательныйвизит;соревновательныхнаграднет',priority='P3 — семейнаяальтернативаприпоездке',evidence_level='program',
    proof='ПрочитанprimaryMuCi:SanCosmosdigitalplanetariumдлядетей/взрослых,Textilia;TatakuaLabclosedпослеMarch2026,новыйMuseoapprox2028. ОстаточныйAstra14Octoberbannerс2025непревращёнв2026event.',
    note='Здесьнетновойдатированнойroboticsexpo. СтарыеASTRA/3D/TigoCampusPartyописаниянаhomeнеявляютсяновой2026выставкой. Бесплатныйcommunityextensionentryтребуетотдельнойкоординации,необщийfreefamilyticket.',
    exhibition_tier='family_alternative',visitor_policy='family',visitor_policy_note='Primaryназываетchildren/youth/adults;show-specificageиadultticketуточняются.',
    highlights=['Цифровойпланетарий','Иммерсивнаявизуализация','Семейнаянаучнаятехнология'],exhibitor_note='Educationalfamilyvenue;неведущиемировыекомпанииробототехники.',
    exhibitor_directory_url='https://muci.org/',adult_entry='Действующийshowticket/программазала;общийfreeвходнеподтверждён.')

# Existing umbrella retains its ID but no longer masquerades as an open entry.
e=byid['C046'];e.update(title='Robótica 2026 · обзор co-located OBR / CBR / MNR',checked=DAY,
    scope='national',admission_kind='qualifier',priority='P4 — обзор; новые заявки2026закрыты',
    entry='OBRнациональныйфиналдляужеотобранныхкоманд;CBRfirstentryзакрыт24Aug;MNRнациональныепроектыподаныдо15July. ПубличныйvisitorвходотдельнойкарточкойE130.',
    related_ids=cbr_ids+mnr_ids+['E130'],proof='ПовторнопрочитаныRobótica,CBRentry/payment/categories,OBRregistrationPDF/MNRcalendarиFAQ;разныеусловиявходаразнесеныпокарточкам.',
    note='OBR23–29Novвновостяхпротив23–27Novвмартовскомmanual;точныйденькомандыуточнить. C046являетсяобзоромфестиваля,неещёоднойсамостоятельнойзаявкойсемьи.')
updated.append('C046');source(e['source'],e['title'],e['proof'])
e=byid['C011'];e.update(languages=[],language='БразильскоеjudgingES/ENнеподтверждено;глобальныемировыеправилаотдельно',
    language_certainty='СтарыйEStagнебылподкреплённациональнымjudging;снят. СвязьсWROdirectoryнеподтверждаетязыклокальногоэтапа.',checked=DAY)
updated.append('C011')

profiles={p['id']:p for p in d['league_guide']['profiles']}
def profile(id,name,ids,ages,summary,route,nuances,sources):
    categories=[dict(name=byid[x]['title'],age=byid[x]['age'],team=byid[x]['format'],hardware=byid[x]['gear'],entry=byid[x]['entry'],age_rule='По текущему классу / возрастному отсечению конкретной категории',event_id=x,source=byid[x]['source'],checked=DAY,note=byid[x]['note']) for x in ids]
    d['league_guide']['profiles'].append(dict(id=id,name=name,group='regional',age_summary=ages,age_tags=['6','9','10-12','teen'],summary=summary,categories=categories,event_ids=ids,legacy_ids=[],route=route,
        hardware='По категории / типу проекта',language='ES/ENинтервьюнеподтверждены;PT/ESmaterialsненазначаютязыкjudging',
        importance='Национальный/региональныйпуть;международнаяквотатолькоподтверждённымположением.',strengths=summary,
        requirements=['Сверитькласс/возраст,foreignentry,состав,самостоятельныйвкладидокументы.', 'Регистрация,принятиезаявки,отборинаградапопротоколу—разныесостояния.'],nuances=nuances,
        cost='Действующиетарифыикитвкарточкевыбранногоэтапа;семейныйtravelbudgetнераcсчитан.',award='См.наградусвоегоформата;Anais/participation/mençãoнеобъединенывмировуюмедаль.',
        sources=[dict(title=label,url=u,checked=DAY) for label,u in sources],evidence='Прочитанылокальныепервичныеправила/программы;приёминостраннойсемьиотмеченотдельно.'))
profile('obr-brazil','Olimpíada Brasileira de Robótica · OBR',obr_ids,'Классы:теория0=1-й,1=2–3-й,2=4–5-й;практика0=1–3-й,1=1–8-йвPDF2026;Nível2с8-го',
    'Бесплатнаяшкольнаяолимпиадасиндивидуальнойтеориейиразнымипрактическимикомандами.',
    'Teórica→медальпобаллу. Resgate0→регион/штат. Resgate/Artística1→национальныйотбор. МеждународныйRoboCuprouteвmanualданNível2,правамиC/Rстранынеподменяется.',
    ['Практическийgaragecoachразрешён;теоретическийcoachнуженизрегулярнойINEPшколы.', '8-йклассвmanualперекрываетNível1/2;уточнитьcategoryspecificrules.', 'Одноpresencialиспытание+дополнительнаяvirtualкоманда;послеотборасоставнеизменяют.', 'Национальныедаты2026:manual23–27Novпротивновости23–29Nov;futureseasonнеобъявлен.'],[('Práticas2026manual',practice),('Teórica2026manual',theory),('FAQ',obrfaq),('Season2026news',obrnews)])
profile('cbr-brazil','Competição Brasileira de Robótica · CBR Petrobras',cbr_ids,'RCBChallengeбезagegradeлимита;RCJEntry12–16;SoccerIR/Vision14–19на1July',
    'Автономныеleagueиспытанияиинженернаяrobotics;разныедетскиеиMajorрежимы.',
    'Educationalinstitution→categoryapplication→technicalacceptance→payment→inspection/event. Для2026перваяподачауже24Augзакрыта.',
    ['Оплатадо29Octили15Novнеравнановойдопускающейзаявке.', 'Non-BrazilianMajorтарифнеподтверждаетforeignJuniorстоимость.', 'Entry12–16неявляетсямировойjuniorлигоюфинала;максимум2участия.', 'Оскар/МатвейнеподходятRCJ12+;дляRCBвозрастнеограничен,ноinstitution/closeddeadlineостаются.'],[('Categories',cbrcat),('Entrydeadline',cbrentry),('Paymentgates',cbrpay)])
profile('mnr-brazil','Mostra Nacional de Robótica · MNR',mnr_ids,'РегулярныеученикиEnsinoFundamentalи старше;точныйminimumageнеуказан',
    'ОцениваемаявыставкаробототехническихпроектовсAnais/сертификатами/mençãohonrosa.',
    'Проект/авторы→экспертнаяоценка→nationalvirtualИЛИpresencial. Localregionalзаявканеоткрываетзаднимчисломnationaldeadline.',
    ['National2026initialsubmission15July/interest30Septemberзакрыты.', 'Rondonópolislocaldeadline4Oct;internationalchildteamприёмещёнеподтверждён.', 'Max6students+orientador+2co-orientadores;regularschoolenrollment.', '5+5минvirtual;presencialprojects26–28Novвокне24–29Nov.', 'ШкольныйhonorarymentionиAnaisнеявляютсягарантированнойworldchampionshipпобедой.'],[('Currenttimeline',mnrtime),('Authors/assessment/awardFAQ',mnrfaq),('Co-locatedfestival',robotica)])
profile('lnr-paraguay','Liga Nacional de Robótica · Paraguay / VEX',['C837'],'От1-гошкольногокласса;VEXIQglobalage/gradeправилавыбранногосезона',
    'ParaguayReeducaVEXnetwork:4подготовительныхстартаинациональныйфиналпозаявлениюseasonpartner.',
    'VEXteam→localLNRstage→Paraguaynationalfinal→worldslotsпотекущимglobalrules;foreignteam/representationотдельно.',
    ['5Sep2026первыйстартпрошёл;число17placesнакартепрошлогоeventнеозначаетдоступныйновыйтурнир.', 'Точные4оставшиесядатыещёненайдены;счёт5competitionsнестал5fictionalcalendarrecords.', 'LNRParaguayиLNRArgentinaразныелига/robotplatform/чемпионат.'],[('VEXeventprimary',vexpy),('2026–2027partnerstatement',pylnr)])
profiles['first']['event_ids']+=fll_ids
profiles['first']['nuances'].append('ParaguayBIOGLOW:localExplore3–6иChallenge3–10,minimum3,foreignentryнеустановлен;старыеSUBMERGEDстраницысверенысновымseasonpage. Нетнайденнойнациональнойдаты.')
profiles['first']['sources'].append(dict(title='ParaguaylocalBIOGLOW',url=pyseason,checked=DAY))
profiles['vex']['event_ids'].append('C837')
profiles['vex']['nuances'].append('ParaguayLNR:первый2026–27старт5Sepпрошёл;AllGradesненазначаетcountryquotaиforeignrepresentation. Будущиеconcretestagesнеобъявленывпрочитанномevent.')
profiles['firstglobal']['event_ids'].append('C839')
profiles['firstglobal']['nuances'].append('BoliviaAGETIC:двелокальныекатегорииTecnólogos/Inventoresнеполучилиопубликованныхagesнаprogrammepage. Глобальнаясборная14–18отдельнаотвозможногодетскогопроекта.')
profiles['brazil']['event_ids']+=cbr_ids+mnr_ids+obr_ids
profiles['brazil'].update(route='ВыбратьOBRgrade-basedолимпиаду,CBRdisciplineилиMNRproject;каждойестьотдельныйпрофиль. БесплатныйvisitorE130отдельно.',evidence='Первичновывереныlocalregistrationmanuals/currentCBR/MNRrules;umbrellaC046несталоткрытойзаявкой.')
d['league_guide'].update(version=18,checked=DAY,methodology='67профилейсемейств/лиг/программ;все46прежнихмаршрутовсохранены. Бразилияразделенапоконкретнымформатам;мировойохватчастичный.')

a=d['completeness_audit']; focus=a['south_america_focus']
focus.update(name='Южная Америка · два первичных прохода',checked=DAY,isos=focus['isos']+['BRA','URY','PRY','BOL'],
    conclusion='ДобавленыБразилия,Уругвай,ПарагвайиБоливия. ДляБразилиибесплатныйvisitor,OBRgrade-basedотбор,CBRregistrationиMNRprojectразделены. ВПарагваеобъявленCreativeTechday31октября;даты2027иforeignteamгейтыпокауточняются.')
focus['routes'] += [
 dict(name='Бразилия · посетитьфестивальилиподатькоманду',detail='Robótica23–29ноябрявJoãoPessoaобъявляетfreeentry;детскийvisitorpolicyнужноподтвердить. CBRпервичнаязаявказакрыта24августа;оплатаосеньюнеоткрываетновыйприём. SoccerEntry12–16иIR/Vision14–19братьямпоканеподходят. RCBChallengeнеограничиваетвозраст,ноinstitution/registrationгейтыостаются.',ids=['E130']+cbr_ids),
 dict(name='Бразилия · OBRкласс/MNRоценкапроекта',detail='OBRопределяетуровеньклассом:Resgate0для1–3классовзаканчиваетсярегиональным/штатнымстартом;практическийgaragecoachразрешён. MNRprojectnationalsubmissionзакрыт;virtual28–30октября,presencialпроекты26–28ноября. MatoGrossoregional22–24октябряпубликуетсрок4октября,приёминостраннойсемьиуточнить.',ids=['C823','C824','C820','C821','C833','C831','C832']),
 dict(name='Парагвай · FLLиVEXкакразныемаршруты',detail='FLLExplore6–10,local3–6детей:братьямнужентретийучастник. Challenge9–16,local3–10:Матвейпослепроверкидопуска,Оскарещёмладше9. BIOGLOWанонсирован,датаnationalнет. LNRParaguayиспользуетVEX;непутатьсArgentinaLNR. Старт5сентябряпрошёл,оставшиедатыиквотуforeignteamподтвердить.',ids=['C835','C836','C837']),
 dict(name='Парагвай · конкретныйденьиканикулы',detail='MOTCreativeTech31октября5–12,09:00–15:30илиполдня,новаяsedeAustria2400савгуста2026. ТочныйteachingES/ENикодинг/роботыэтогоHalloweenднянеподтверждены. Futureweekcampбезновыхдней. SanCosmosсемейныйцифровойпланетарий:сеансыотдельно;TatakuaLabзакрыт,новыйMuseoориентировочно2028.',ids=['L162','L161','E131']),
 dict(name='Уругвай/Боливия · программаилиобъявленныйнабор',detail='WeCodeлетниеrobotics/AI/Minecraftкурсыпо2–3/4–6классамиплощадкамещёописываютфевраль2026;2027непридуман. UMSA9–14старыйcourseпрошёл25сентября,Jopoi8–12roboticsбезгода;егоsummerpage2024natureневыданазатехническийлагерь. CiberneTICsKids/ SucreBotреальныепрограммы,следующийдопуск/датыуточнить.',ids=['L155','L156','L157','L158','L159','L160','L163','L164','L165','C838','C839'])]
focus['open_questions'] += ['Brazil:foreigngarage/schoolдопуск,классы,OBR8-йклассперекрытие,individualnationaldaysиES/EN;MNRMatoGrossoforeignproject/regionдопуск.',
    'Paraguay:FLLBIOGLOWактуальныеfees/kits/agecutoff,датаnationalиforeignquota;оставшиесяVEXLNRstages.',
    'MOTHalloween:места,teachingES/ENиконкретныйцифровойcurriculum;summer2026–2027новыеднибезстарого2025–26переноса.',
    'Uruguay/Bolivia:newholidaycohorts/grade/minage/teachinglanguage/foreignchilddocuments;SucreBotworldaccreditationидействующийcategorymanual.',
    'MNRprimaryHTMLсодержитпосторонниеSEOвставки;локальноеподтверждениепередпоездкой. MuCiстарыйAstra14Octoberнеявляетсяновым2026анонсом.']
issues=[dict(name='OBR2026 · классинациональныедаты',status='ManualNível1=1–8/Nível2с8:перекрытие;мартовскийPDFnational23–27Novпротивновости23–29Nov. Длядетейкатегорияпоgrade,непо9/6.',official_alternative=practice),
 dict(name='CBR2026 · оплатанеравнановомуentry',status='Initialregistration24Augзакрыт,Earlypaymentдо29Oct/Regular15Novтолькопрошедшемуentry;Non-BrazilianMajorfeeненазначенJunior.',official_alternative=cbrentry),
 dict(name='MNR · primaryHTMLсSEOвставками',status='НаофициальномdomainвHTMLвставленысторонниегемблинг/replicaSEOlinks. Прочитаныорганизаторскийcalendar/FAQ;Robóticaнезависимоподтверждаетобщийfestival,локальныеschedule/foreignrulesнадоперепроверить. Scannedmanualзагружен,полноеOCRчтениепоканезаявлено.',official_alternative=robotica),
 dict(name='ParaguayFLL · сезонныеверсии',status='BIOGLOW2026–27отдельноанонсирован;programmepagesсохраняютSUBMERGED2024–25иEV3,registration2025–26. Новыеfees/EV3eligibility/dateнеперенесеныизстаройверсии.',official_alternative=pyseason),
 dict(name='MOT · адрес / старыеholidayoffers',status='GenericcampMayorRivarola465,primarys2newAustria2400с1Aug2026. Halloween31Octвновойsede;старые2025–26summerднине2027.',official_alternative=mots2),
 dict(name='WeCode/UMSA/Jopoi · даты / реальныеhours',status='WeCodepageFebruary2026;UMSA2Aug–25Sepпрошли,30academic hoursнеполныйширокийMonWedFriwindow;Jopoiroboticsбезгода,summerFAQявно2024иприрода/искусство.',official_alternative=wecode),
 dict(name='MuCi · закрытыйTatakuaLab',status='НаhomeсохранилсяAstra14Octoberbannerи2022/2023exhibitions;текущийтекстclosedMarch2026/newMuseoapprox2028. SanCosmosотдельнаядействующаясемейнаяплощадкабезновойrobotexpoдаты.',official_alternative='https://muci.org/')]
a.update(version=18,checked=DAY,baseline=baseline,new_ids=new,new_profiles=['obr-brazil','cbr-brazil','mnr-brazil','lnr-paraguay'],updated_ids=updated,
    scope='SouthAmericafollow-up:Бразилияgrade-basedOBR/CBR/MNRиvisitor,ПарагвайFLL/VEX/holidayday,УругвайAI/robotics/programmingплощадки,Боливияnational/programmeкандидаты. Девятьстрансзаписямивмаршрутах;полнотаместныхкалендарейнеподтверждена.')
a['source_issues']+=issues
a['caveats'] += ['33новыхкарточкивключаютвозрастныетреки/площадки/дисциплины,не33новыхнезависимыхфестиваля.', 'RegionalMNR,newVEXteamapplication,Nationalprojectselection,visitorfreeentry,HonorableMentionиworldmedalнеэквивалентны.', 'НиоднаизновыхучебныхпрограммнеполучилаES/ENtagтолькозаязыксайта.']
a['known_backlog'].append(dict(kind='SouthAmerica',name='Brazil/Uruguay/Paraguay/Boliviaследующиеcohortsиforeignдопуск',reason='; '.join(focus['open_questions'][-5:]),url=robotica))
d.update(asof=DAY,source_count=len(d['sources']))
d['expansion_log'].append(dict(version=18,date=DAY,scope='SouthAmericafour-countryprimaryfollow-up',added_ids=new,updated_ids=updated,notes=['All1102baselineIDs,63profiles,46legacyroutes/family/Taiwan/CRMXretained.', 'Closedinitialapplicationsnotreopenedbyfeephases;oldcampdatesnotreused.', 'Localgrade/team/countryrulesretained;nostandaloneinventedremainingVEXdates.']))
(ROOT/'data/south-america-audit-v18.json').write_text(json.dumps(dict(version=18,focus=focus,added_ids=new,updated_ids=updated,source_issues=issues),ensure_ascii=False,indent=2))
planpath=ROOT/'data/research-plan.json';plan=json.loads(planpath.read_text());plan.update(updated=DAY,status='active',completeness_audit='data/audit-v18.json')
for r in plan['requirements']:
    if r['id']=='global_competitions':r['evidence']='v18:Brazilgrade-basedOBR,CBR4disciplines/MNR4eventrecords;ParaguayFLL2paths/VEXnextstagewithoutfakedates;Bolivianprimarycandidates.67profiles,worldcoveragepartial.'
    if r['id']=='camps':r['evidence']='v18:WeCode6campus/curriculumcardswith2026historicalmonth,MOT31OctCreativeTech/5–12/newvenue,UMSA/Jopoi/AGETICnotinventedholidayshifts;teachingES/ENunknown.'
    if r['id']=='exhibitions':r['evidence']='v18:Robótica2026visitor23–29Novfreeentry/minorpolicyunknown;MuCiSanCosmosfamilydigitalvenue,TatakuaLabclosed,newMuseoapprox2028.78curatedcardsincludingfamilyalternatives,worldcoveragepartial.'
    if r['id']=='eligibility':r['evidence']='v18:OBRschoolgrade/garagevsregularschool,FLLParaguaymin3,CBRclosedentry/RCJ12+/MNRauthorsandnationalcutoff,foreigndocuments/teachinglanguageunknown.'
plan['latest_validation']=dict(version='v18',status='pending',research_status='active')
plan['next_research'].insert(0,'SouthAmericav18: '+'; '.join(focus['open_questions'][-5:]))
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2));PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2))
assert len(new)==33 and len(d['events'])==1135 and len(d['league_guide']['profiles'])==67
print(json.dumps(dict(added=len(new),total=len(d['events']),profiles=len(d['league_guide']['profiles']),new_ids=new),ensure_ascii=False))
