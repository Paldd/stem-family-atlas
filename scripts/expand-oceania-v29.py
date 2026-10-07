"""Primary-source Pacific programmes and games; preserve prior world inventory."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/catalog.json';d=json.loads(path.read_text())
assert len(d['events'])==1250 and d['completeness_audit']['version']==28
new=[];profiles=[];byid={e['id']:e for e in d['events']}
CHECKED='2026-10-01'
def ref(label,url):return dict(label=label,url=url)
def event(id,title,country,city,source,age,mat,osc,entry,gear,block='Соревнования',start='',end='',deadline='',scope='local',participation='team',priority='P2 — после проверки допуска',note='',cost='Текущую стоимость и валюту подтвердить',themes=('robotics','coding'),language='Язык занятия / защиты не подтверждён; EN-сайт не является доказательством',languages=(),evidence='event_page',date_scope='festival_window'):
 e=dict(id=id,block=block,title=title,country=country,region='Океания',city=city,source=source,checked=CHECKED,
  start=start,end=end or start,deadline=deadline,period='',date_status='Подтверждено' if start else 'Не объявлено',
  age=age,mat=mat,osc=osc,format={'day_camp':'Дневной лагерь; жильё семьи отдельно','holiday_workshop':'Однодневный каникулярный мастер-класс','individual_or_team':'Индивидуально или командой','visitor':'Посещение / онлайн-показ','team':'Команда'}[participation],
  participation=participation,admission_kind='program' if block=='Лагеря' else 'visitor' if participation=='visitor' else 'open_application',
  entry=entry,gear=gear,language=language,languages=list(languages),support_languages=[],cost=cost,scope=scope,
  level='Местная учебная программа' if block=='Лагеря' else 'Национальный конкурс' if scope=='national' else 'Образовательное событие',
  importance_reason='Оценка масштаба конкретной программы; наличие сайта и сертификата не доказывает место в мировом рейтинге.',
  reward='Обучение / собственный проект; сертификат обучения не равен победе' if block=='Лагеря' else 'Результат конкретного конкурса по официальному протоколу' if block=='Соревнования' else 'Посещение / изучение проектов; награда посетителю не обещана',
  priority=priority,status='Идея',action='Подтвердить конкретный поток, язык, класс, доступ иностранной семьи и наличие мест до записи или поездки.',
  proof='Прочитан первичный источник; дата / возраст и неизвестные условия разделены.',evidence_level=evidence,references=[],note=note,
  registration_status='Заявка семьи не подана; опубликованная программа не подтверждает место.',
  language_certainty='Язык сайта не перенесён на язык преподавания / судейства.',themes=list(themes),date_scope=date_scope)
 if block=='Лагеря':e['language_mode']='unconfirmed'
 assert id not in byid and id not in [x['id'] for x in new];new.append(e);return e

fiji='https://www.kidzcodecamp.com/'
e=event('L211','KidzCodeCamp Fiji · дневная робототехника для туристов','Фиджи','Nadi · Aliz Centre, Level 2, Martintar',fiji,
 '6–16 лет','Условно: по возрасту подходит; язык и выбранный день подтвердить','Условно: по возрасту подходит; язык и выбранный день подтвердить',
 'Выбрать доступный будний день; подтвердить EN-преподавание, загрузку группы и гостиничный трансфер.',
 'Java, 3D simulator и физический робот; устройство предоставляется по описанию оператора.',block='Лагеря',participation='day_camp',
 note='Оператор предлагает один день по будням 09:00–15:30, питание, компьютер и обратный трансфер. Конкретная будущая смена не датирована. Туристический формат подтверждён; занятия на EN прямо не подтверждены в прочитанных актуальных деталях. Это кандидат для семейной поездки, не доказанный лучший международный лагерь.',
 cost='Introductory offer $199 / человек на сайте; валюта и текущая цена не указаны однозначно.',evidence='program')
e['period']='Будние дни 09:00–15:30 по времени Фиджи; конкретный день и места уточнить'
e['references']=[ref('Tourism Fiji: туристический формат и трансфер','https://www.fiji.travel/deals-and-offers/experiences/kids-code-camp')]

steam='https://steamed.nz/holiday-programmes/'
days=[('L212','2026-10-05','Robotics Carnival Rides','Конструирование и программирование carnival rides с robotics kits.',('robotics','coding')),
 ('L213','2026-10-07','Gears, Pulleys, Levers and Elastics','Механизмы, передачи и рычаги с robotics kits.',('robotics','technology')),
 ('L214','2026-10-08','Imagination & Movie-making','Сборка персонажа с движущимися частями и собственный фильм; программирование не обещано.',('technology',)),
 ('L215','2026-10-09','Freestyle Robotics','Самостоятельный выбор конструкции из robotics kit.',('robotics','coding'))]
for id,date,title,gear,themes in days:
 e=event(id,'STEAM-ED · '+title,'Новая Зеландия','Tauranga · 671 Cameron Road, Tauranga South',steam,'5–13 лет в описании именно этого дня',
  'Условно: возраст подходит; EN и иностранный приём подтвердить','Условно: возраст подходит; EN и иностранный приём подтвердить',
  'Запись на один выбранный день; согласовать язык, доступ visiting family и наличие мест.',gear,
  block='Лагеря',start=date,participation='holiday_workshop',priority='P3 — короткое занятие при удобной поездке',
  cost='$63 / ребёнок / день на странице; валюту и текущий счёт подтвердить.',themes=themes,
  note='09:00–15:00 местного времени Новой Зеландии. Четыре карточки — четыре опубликованных учебных дня одного оператора, не четыре независимых международных лагеря. Жильё семьи отдельно. Для поездки из Коста-Рики очень короткий срок; качество или международный рейтинг не доказаны.',date_scope='session_days')
 e['sessions']=[dict(date=date,topic=title,start_time='09:00',end_time='15:00',timezone='Pacific/Auckland',time_note='Опубликовано оператором; место не подтверждено.')]

brain='https://mairangi-arts-centre.live.baluu.co.uk/event/code-club-with-brain-play-1787526688'
e=event('L216','BrainPlay / Mairangi Arts Centre · Code Club','Новая Зеландия','Auckland · Mairangi Arts Centre, 20 Hastings Road',brain,
 '7–12 лет: страница записи требует оставаться в указанном диапазоне',
 'Условно: 9 лет подходит; EN и иностранный приём подтвердить','Нет: 6 лет ниже минимального возраста 7 на странице записи',
 'Запись у принимающего Mairangi Arts Centre; своё устройство или заранее подтверждённая аренда.',
 'Python, JavaScript и game programming; iPad / tablet / laptop / Chromebook.',block='Лагеря',start='2026-10-09',participation='holiday_workshop',
 cost='От $71.25 за трёхчасовое занятие на странице записи; валюта и итоговая цена уточняются.',themes=('coding','games'),
 note='Обзор BrainPlay пишет 5–12, но действующая страница этого занятия — 7–12. Использована конкретная граница места записи. Обзор даёт 10:00–13:00, принимающая площадка подтверждает дату и длительность 3 часа; окончательный слот подтвердить. Это отдельный день, не пансион и не соревнование.')
e['references']=[ref('Обзор с конфликтом возраста','https://www.brainplay.co.nz/events-and-holidays'),ref('Календарь принимающей площадки','https://mairangi-arts-centre.live.baluu.co.uk/events')]

games='https://www.stemgames.org.au/'
game_rules='https://www.stemgames.org.au/shared/files/stem-rules.pdf'
e=event('C903','Australian STEM Video Game Challenge · следующий сезон','Австралия','Онлайн; обучение в австралийской школе / homeschool',games,
 'Year 3–12; год рождения не заменяет школьную категорию',
 'Нет для текущего зарубежного школьного маршрута: требуется школа / homeschool в Австралии и citizenship / residency',
 'Нет для текущего зарубежного школьного маршрута; кроме того нужен Year 3–12',
 'По действующим связанным правилам: Australian citizen или resident И Year 3–12 в Австралии; взрослый mentor 18+, родительское разрешение.',
 'Scratch / Godot / open engine, playable game, source code, GDD и 1–5 minute recording. Roblox / Minecraft Education / Gamestar Mechanic не принимаются.',
 scope='national',participation='individual_or_team',priority='P4 — текущая зарубежная семья не соответствует условиям',
 themes=('games','coding'),language='Подача всех материалов на английском прямо обязательна в §6 правил.',languages=('EN',),evidence='historical_program',
 note='Приём сезона 2026 закончился: регистрация 7 августа, submission 9 сентября. Даты 2027 не объявлены и не придуманы. Индивидуально или 2–4 участника; mentor должен иметь Working With Children Check по challenge page. Школы / клубы дают минимум одного судью. AI требует своего вклада и описания. PDF с ваучером $500 и текущая страница с hoodie расходятся по призам — конкретный приз не гарантирован.')
e['references']=[ref('Текущие связанные правила: national eligibility и English',game_rules),ref('Категории, mentor и материалы','https://www.stemgames.org.au/the-challenge')]
e['admission_kind']='national_school';e['related_ids']=['E139']
e=event('E139','Australian STEM Video Game Challenge 2026 · online showcase / результаты','Австралия','Онлайн · время / публичная ссылка пока не опубликованы',games,
 'Посетитель; школьные границы конкурса не являются автоматически границами просмотра',
 'Условно: публичный доступ к трансляции не подтверждён','Условно: публичный доступ к трансляции не подтверждён',
 'Проверить объявленную онлайн-ссылку, время, публичность и формат детского просмотра ближе к событию.',
 'Просмотр авторских игр и результатов, не подача нового проекта.',block='События',start='2026-11-24',scope='national',participation='visitor',
 priority='P3 — онлайн-посещение после подтверждения доступа',themes=('games','coding'),
 note='Первичная страница прямо объявляет online winner announcement and showcase 24 ноября 2026. Это не очная выставка компаний и не открытый конкурс: submission уже закончился. Доступ зрителей и час пока не установлены.')
e['related_ids']=['C903'];e['references']=[ref('Правила конкурсной заявки, отдельно от зрителей',game_rules)]

tdw='https://www.getintostem.edu.au/students/they-did-what-competition/'
e=event('C904','They Did What? 2026 · детский STEM-видеоконкурс','Австралия','Онлайн · Australian STEM star',tdw,
 'Foundation–Year 10; младшая категория Foundation–Year 4',
 'Условно: подтвердить класс и допуск ребёнка из зарубежной школы','Условно: подтвердить класс Foundation / начальную ступень и зарубежный допуск',
 'Своё видео об Australian STEM star / человеке, работающем в Австралии; solo / team / class. В прочитанных условиях международный приём прямо не подтверждён.',
 'Самостоятельное видео до 3 минут, MP4, максимум 600 MB. Взрослый может помогать практически, но не заменять детскую работу.',
 deadline='2026-10-16',scope='national',participation='individual_or_team',themes=('technology',),
 note='Это конкурс научной коммуникации, а не инженерный турнир роботов. Приём заканчивается 16 октября 2026 в 17:00 AEDT; winners notified 16 ноября. Отсутствие явного citizenship запрета не доказательство зарубежного допуска. Язык видео прямо не установлен; англоязычная страница не стала подтверждённым EN.',date_scope='submission_window')
e.update(deadline_utc='2026-10-16T06:00:00Z',deadline_label='Подача видео',deadline_note='16 октября 2026, 17:00 AEDT (UTC+11) = 06:00 UTC. Только дедлайн; дни самого мероприятия не объявлены.')

poly='https://inutai.nati.pf/index.html'
e=event('C905','Inutai · Concours robotique et codage 2026 · архив школьного отбора','Французская Полинезия','Школы Polynésie française · CM1 / CM2',poly,
 'Только классы CM1 / CM2 школ Французской Полинезии; это школьное правило, не числовой возраст',
 'Нет для текущего зарубежного школьного маршрута; будущий местный класс требует отдельного допуска',
 'Нет для текущей младшей / зарубежной школьной ступени',
 'Школьная команда через местную образовательную платформу Inutai. Закрытый сезон не обещает приём зарубежной семейной команды.',
 'Школьная робототехника и код; подробная платформа / требования в открытой карточке не установлены.',
 start='2025-09-01',end='2026-03-20',scope='national',priority='P4 — архив и местный школьный маршрут',
 note='Первичная платформа указывает 33 команды и завершённое окно 1 сентября 2025–20 марта 2026; отдельный финал 20–30 апреля 2026, 17 команд. CSSU-financed школьная платформа, а не текущий международный финал. Будущий сезон 2027 не объявлен. Общую активность Inutai до июля 2027 не выдали за robotics calendar.',evidence='historical_program',date_scope='submission_window')

e=byid['L019'];e.update(checked=CHECKED,source='https://www.brainplay.co.nz/events-and-holidays',languages=[],language_mode='unconfirmed',
 language='Язык преподавания не подтверждён прямо; EN-сайт не доказывает EN-занятия.',
 age='В обзоре некоторые занятия 5–12; у Code Club 9 октября 2026 точное правило 7–12. Другие города / темы отдельно.',
 references=[ref('Code Club: принимающая площадка, 7–12',brain)],
 proof='Прочитаны текущий обзор BrainPlay и конкретная страница принимающего Mairangi Arts Centre.',
 note='Обобщённая программа оператора; конкретный день L216 имеет минимум 7 лет. Обзор 5–12 не использован как допуск Оскара в Code Club. Старый EN-тег снят до прямого подтверждения преподавания.')

rcja='https://www.robocupjunior.org.au/wp-content/uploads/2026/02/2026-RCJA-General-Rules.pdf'
rescue='https://www.robocupjunior.org.au/rescue-line/'
rescue_rules='https://www.robocupjunior.org.au/wp-content/uploads/2026/02/RCJA-Rescue-Line-Rules-2026.pdf'
nat='https://www.robocupjunior.org.au/challenge-regions/nat/'
e=byid['C775'];e.update(checked=CHECKED,source=nat,admission_kind='open_application',
 age='Riley Rover: Primary / Secondary; Primary Rescue: все члены команды — primary school. Мировой порог 14+ к местной Primary не применён.',
 format='Australian Open: 2–4 ученика и mentor старше 19; разовое solo только с разрешением координатора',
 mat='Условно: младший школьный маршрут и foreign team разрешены; класс, категория и новый этап уточняются',
 osc='Условно: подтвердить recognised primary school / equivalent school age и младшую категорию; foreign team разрешены',
 entry='National Open не требует regional / state отбора; international teams прямо допускаются по правилам 1.4.3. Конкретную дату, division и EN-интервью подтвердить.',
 references=[ref('2026 General Rules: team / foreign / prizes',rcja),ref('Primary / Riley Rover divisions',rescue),ref('Rescue Line 2026: код, poster, interviews',rescue_rules)],
 note='По General Rules 2026 иностранная команда может получать равное 1–3 место вместе со следующей местной командой; для Australian Open это обязательное правило, для региональных этапов решение координатора. Иностранцы НЕ могут квалифицироваться через Австралию на мировой RoboCupJunior. Rescue 2026 требует annotated code; poster нужен для special awards. Следующий этап не датирован: шаблон event-calendar без загрузки не считается доказательством отсутствия мероприятий.',
 proof='Прочитаны Australian Open overview, General Rules 2026 и Rescue Line Rules 2026; мировой отбор и национальные награды разделены.')

kiwi='https://www.kiwibots.co.nz/nationals'
e=byid['C385'];e.update(checked=CHECKED,age='VIQRC Elementary: рождён после 1 мая 2014; оба года рождения 2017 /2020 подходят по этому условию.',
 mat='Условно: год рождения подходит; национальный / иностранный вход команды не подтверждён',
 osc='Условно: год рождения подходит; самостоятельная командная работа и национальный вход не подтверждены',
 languages=[],language='Язык интервью / notebook у этого этапа прямо не подтверждён; EN-сайт не является доказательством.',
 proof='Даты 11–13 декабря 2026 и Elementary cutoff дополнительно подтверждены первичным KiwiBots Nationals overview. Новая регистрация / иностранный доступ не установлены.',
 note=e['note']+' KiwiBots подтверждает 11–13 декабря 2026, Central Energy Trust Arena Manawatu, Elementary born after 1 May 2014 и четыре Elementary Worlds slots. Квота не подтверждает приглашение семьи. EN-тег как только язык сайта снят.')
e['references'].append(ref('KiwiBots Nationals: даты, возраст, квоты',kiwi))

def profile(id,name,group,age,summary,categories,event_ids,route,requirements,nuances,sources,age_tags=('6','9','10-12','teen')):
 p=dict(id=id,name=name,group=group,age_summary=age,age_tags=list(age_tags),summary=summary,categories=categories,event_ids=event_ids,legacy_ids=[],
  route=route,hardware='См. категории и связанную карточку; платформы не взаимозаменяемы.',language='EN-подача прямо обязательна только там, где это указано в правилах; язык интервью / преподавания отдельно.',
  importance='Отдельный национальный маршрут, не мировой рейтинг.',strengths=summary,requirements=requirements,nuances=nuances,
  cost='Оборудование, взнос и поездка по конкретному этапу; место не подтверждено.',award='Награда конкретного этапа по протоколу; мировой отбор и certificate of learning отдельно.',
  sources=[dict(title=t,url=u,checked=CHECKED) for t,u in sources],evidence='Прочитаны первичные страницы / связанные правила; условия будущего сезона не выдуманы.')
 profiles.append(p)
profile('stemgames-au','Australian STEM Video Game Challenge','games','Year 3–12 в Австралии; current season 2026 закрыт',
 'Оригинальная игра с кодом, GDD и gameplay-видео; национальный конкурс с прямым школьным / residency условием.',
 [dict(name=name,age=age,team='1–4; mentor 18+',hardware=hw,age_rule='Класс в год судейства',entry='Australian citizen / resident И школа / homeschool в Австралии') for name,age,hw in [
 ('Primary: Scratch / Open','Year 3–6','Scratch или open engine'),('Middle: Godot / Open','Year 7–9','Godot или open engine'),('Senior: Open','Year 10–12','Open engine')]],
 ['C903','E139'],'Соответствующая школа / residency → mentor и свой game + code + GDD → submission → rubric judging → финал / результаты.',
 ['2026 приём закрыт; даты 2027 неизвестны.','English submission обязательна; Roblox / Minecraft Education не принимаются.','Школы / клубы предоставляют минимум одного судью; mentor Working With Children Check.'],
 ['Возраст 9 не заменяет Year 3 и местный школьный допуск.','Ноябрьский showcase — просмотр, а не новая конкурсная заявка.','PDF и текущий сайт расходятся в призовом наборе.'],
 [('Home: 2026 calendar',games),('Challenge: categories','https://www.stemgames.org.au/the-challenge'),('Rules: eligibility / English',game_rules)],age_tags=('9','10-12','teen'))
profile('rcja-au','RoboCupJunior Australia · Primary / Australian Open','regional','Местная Primary / Secondary; мировой RCJ — отдельная старшая ступень',
 'Практический младший путь для иностранной команды с явными национальными наградами; не канал foreign qualification на мировой финал.',
 [dict(name='Riley Rover Rescue',age='Primary / Secondary школьный возраст',team='Australian Open 2–4; mentor >19',hardware='LEGO / другая автономная платформа по Rescue rules',age_rule='Признанное школьное обучение / equivalent school age; местный division подтвердить',entry='National Open без обязательного регионального отбора; foreign teams допускаются'),
  dict(name='Primary Rescue Line',age='Все участники — primary school',team='Australian Open 2–4; mentor >19',hardware='Автономная линия / rescue robot; annotated code и техническая защита',age_rule='Школьная ступень, не универсальная граница 14+',entry='Иностранный приём по General Rules 2026; новый этап / язык уточнить')],
 ['C775'],'Младшая автономная Rescue-команда → актуальный national event и подтверждённый division → technical interview и награды. Мировой отбор иностранной команды — через её свой регион.',
 ['Работа и объяснения детей; mentor не строит / программирует вместо них.','Annotated code обязателен; technical poster нужен для special awards Rescue 2026.','Указанные правила 2026 не автоматически действуют в 2027.'],
 ['Foreign top-3 awarded as equal placing; на Australian Open обязательно, region/state по решению координатора.','Foreign teams не могут пройти через Australia на RoboCupJunior International.','Разовое solo с разрешением не является стандартной индивидуальной лигой.'],
 [('National overview',nat),('General Rules 2026',rcja),('Rescue Line divisions',rescue),('Rescue Line Rules 2026',rescue_rules)])

rcj=next(p for p in d['league_guide']['profiles'] if p['id']=='rcj')
rcj['nuances'].append('Australia Primary имеет отдельный младший foreign-team вход: C775 / профиль rcja-au. National Open не требует регионального отбора, но иностранная команда не может через Australia получить мировой слот; national top-3 equal placing отдельно.')
rcj['sources'].append(dict(title='Australia General Rules 2026: foreign entry versus world qualification',url=rcja,checked=CHECKED))
d['events'].extend(new);d['league_guide']['profiles'].extend(profiles);d['league_guide']['checked']=CHECKED
known={s['url'] for s in d['sources']}
for e in new+[byid[x] for x in ['L019','C775','C385']]:
 for u,t in [(e['source'],e['title'])]+[(r['url'],r['label']) for r in e['references']]:
  if u not in known:d['sources'].append(dict(url=u,title=t,checked=CHECKED,evidence='Прочитан первичный источник; ограничения записаны в связанных карточках.'));known.add(u)
a=d['completeness_audit'];a.update(version=29,checked=CHECKED,status='partial',
 conclusion='Частичный мировой каталог. v29: 10 записей Океании / Тихого океана, 2 национальных профиля и 3 исправленные карточки. Короткие дни обучения, закрытые школьные конкурсы и foreign-team награды отделены от мирового отбора.',
 scope='Мировой аудит продолжается. Этот проход: Фиджи, Новая Зеландия, Австралия, Французская Полинезия; реальные возрастные правила, языки и игровые конкурсы.',
 new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=['L019','C775','C385'])
a['caveats'].append('v29: четыре даты STEAM-ED — дни одного оператора; EN преподавание у Fiji / STEAM-ED / BrainPlay не доказано. Австралийские школьные национальные правила не означают зарубежный допуск. Архив Французской Полинезии не является будущим конкурсом.')
a['source_issues'].extend([
 dict(name='BrainPlay overview versus Mairangi host age',status='Обзор 5–12, конкретная запись Code Club 9 октября 2026 строго 7–12; Оскар исключён из этого дня.',official_alternative=brain),
 dict(name='National school gates and open foreign teams',status='STEM Video Game Challenge требует Australian citizenship/residency И Year3–12 в Австралии; RCJA прямо допускает foreign teams, но не их мировой отбор.',official_alternative=rcja),
 dict(name='Fiji camp language and price',status='Туристический формат и возраст6–16 подтверждены. В индексированных booking summaries встречается English, но прочитанные текущие vendor details не подтверждают язык преподавания; $199 без однозначной валюты.',official_alternative=fiji),
 dict(name='RCJA dynamic calendar',status='Прочитанная выгрузка календаря содержит шаблоны без загруженных дат; это пробел проверки, не доказательство отсутствия соревнований.',official_alternative='https://www.robocupjunior.org.au/challenge-regions/nat/nat-events/')])
o=next(x for x in a['continents'] if x['name']=='Океания');o['remaining']='Добавлены Fiji tourist camp, NZ реальные учебные дни, Australian national game/video contests и закрытый школьный архив French Polynesia. Остаются языки / foreign admission лагерей, динамический RCJA calendar, другие острова и локальные турниры.'
c=d['camp_focus'];c.update(version=29,checked=CHECKED,conclusion='EN / ES / RU семейные языки. v29 добавляет 6 тихоокеанских учебных карточек; их EN-преподавание не подтверждено. Новые кандидаты не повышены до лучших лагерей по одному описанию оператора.',added_ids=[e['id'] for e in new if e['block']=='Лагеря'],updated_ids=['L019'])
c['routes'].append(dict(name='Океания · короткие учебные дни',detail='Fiji KidzCodeCamp6–16 рассчитан на туристов. STEAM-ED5–13 публикует4 дня5/7/8/9 октября2026; BrainPlay CodeClub9 октября строго7–12, дляМатвея. У всех новых кандидатов точный EN и место не подтверждены, жилья / пансиона нет.',ids=['L211','L212','L213','L214','L215','L216']))
c['source_issues'].extend(a['source_issues'][-4:])
d['expansion_log'].append(dict(version=29,checked=CHECKED,added=len(new),updated_ids=a['updated_ids'],note='Pacific learning programmes, national game/video competitions and explicit Australian foreign-team award rules; no new top-pick quality claim.'))
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rpath=ROOT/'data/research-plan.json';r=json.loads(rpath.read_text());r['updated']=CHECKED;r['status']='active';r['completeness_audit']='data/audit-v29.json'
r.setdefault('research_passes',[]).append(dict(version=29,scope='Oceania / Pacific and games',added_records=len(new),new_profiles=2,updated_records=3,status='partial',remaining='Verify camp instruction / foreign entry, dynamic RCJA event calendar, other Pacific countries; retain full worldwide goal.'))
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=29,new_ids=[e['id'] for e in new],new_profiles=[p['id'] for p in profiles],updated_ids=a['updated_ids'],world_complete=False)))
