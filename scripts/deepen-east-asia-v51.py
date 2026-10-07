"""Japan / mainland China / Taiwan: bounded primary-source family audit."""
import ast, copy, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED='2026-10-02'
p=ROOT/'data/catalog.json';d=json.loads(p.read_text())
assert d['completeness_audit']['version']==50 and len(d['events'])==1773
u=json.loads((WORK/'urls-east-asia-v51.json').read_text())
u.update(asij_admit='https://www.asij.ac.jp/admissions/admissions-home',asij_faq='https://www.asij.ac.jp/admissions/admissions-faq',asij_guidelines='https://www.asij.ac.jp/admissions/admissions-guidelines',
 isb_criteria='https://www.isb.cn/admissions/application-process/admissions-criteria-policies',sq_esm='https://steamsquad.io/en/courses/k3-esm',sq_ccm='https://steamsquad.io/en/courses/computer-controlled-machines',sq_code='https://steamsquad.io/en/courses/code-club',
 kcis_es='https://web.kcislk.ntpc.edu.tw/en/es/',jp_vex_es='https://events.vex.com/robot-competitions/vex-iq-competition/RE-VIQRC-26-4838.html',ypao_board='https://www.ykpaoschool.cn/News-and-Events/New-Stories/723',ypao_admit='https://www.ykpaoschool.cn/Admission/Admissions-Criteria-and-Process')
new=[];byid={e['id']:e for e in d['events']}
tree=ast.parse((ROOT/'scripts/expand-oceania-v29.py').read_text())
for name in ['ref','event']:
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name)
 exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))

# A current header/body conflict is deliberately removed from the dated calendar.
e=byid['C537'];e.update(checked=CHECKED,start='',end='',deadline='',date_status='Конфликт источника',period='Header: 31.01.2027; EN / JP body: 20–21.02.2027. Дату необходимо согласовать.',
 entry='Только команды, зарегистрированные и преимущественно работающие в Японии, с местной Qualification Spot из Approved Tournament. Японский team number при тренировках за рубежом недостаточен.',
 note='На одной странице расходятся даты события, notebook и оплаты. Header: 31 января, registration 22 января; body: 20–21 февраля, notebook 12 февраля. Спорные даты исключены из ICS. Registration ещё не открыта; полная национальная квота Japan. Scrimmage / workshop / skills-only не дают national Qualification Spot. Нужен минимум один volunteer на команду, Consent Forms и самостоятельная работа детей.',
 proof='Прочитаны одновременно header, General Info на EN / JP и календарный блок. Конфликт сохранён, а не разрешён предположением.',
 action='Сначала получить единую дату и подтвердить реальную японскую базу команды и qualification. Семья, тренирующаяся только за рубежом, не может считать этот National открытым туристическим стартом.')

# FIRST Japan has country-specific school-grade and interpreter rules.
venues=[('Kanto','Tokyo · JICA (площадка планируется)','2026-12-13'),('Tokai','Nagoya · Ozora High School (площадка планируется)','2026-12-13'),('Kansai','Osaka · Osaka Kyoiku University Tennoji (площадка планируется)','2026-12-06'),('Kyushu','Iizuka · Kyushu Institute of Technology (площадка планируется)','2026-12-06')]
for i,(region,city,date)in enumerate(venues):
 e=event(f'C{1134+i}','FIRST Japan · FLL Explore BIOGLOW · '+region+' · 2026','Япония',city,u['jp_explore'],
  'Grades 1–4 на 02.04.2026; международные школьные классы согласовать.',
  'Условно: школьный класс на контрольную дату и международный допуск.',
  'Условно: должен соответствовать Grade 1 на контрольную дату; год рождения недостаточен.',
  '2–6 детей + 1–2 наставника; Event Dock. Японский переводчик разрешён после предварительного согласования.',
  'SPIKE Essential / WeDo 2.0, модель и poster; робот-набор отдельно от сезонного набора.',start=date,deadline='2026-10-31',scope='national',
  cost='JPY31 900 / команда за регион; National JPY28 600 отдельно; robot kit и поездка отдельно.',
  language='Японский; для команды на другом языке допускается согласованный японский переводчик.',
  note='Даты объявлены, площадки планируются и могут измениться. Explore — фестиваль проектов без ранжирования команд. National 14.02.2027 пока планируется; мировая поездка / квота не объявлена. Регистрация до 31 октября, конец дня Japan, может закрыться при заполнении.',evidence='official_rules',date_scope='festival_day')
 e.update(region='Азия',format='2–6 детей + 1–2 наставника',reward='Обратная связь и признание работы команды; места чемпиона Explore не присваиваются.',deadline_note='31 октября 2026, конец дня Japan; раньше при заполнении.')
for i,(region,city,date)in enumerate(venues):
 if region=='Kanto':city='Tokyo · Iriairai Daiichi Elementary / Smile Omori (планируется)';date='2026-12-19'
 e=event(f'C{1138+i}','FIRST Japan · FLL Challenge BIOGLOW · '+region+' · 2026','Япония',city,u['jp_challenge'],
  'Grades 4–High School 1 на 02.04.2026; обычно 9–16. Международные классы согласовать.',
  'Условно: 9 лет не подтверждают Grade 4 на 02.04.2026.', 'Нет: ниже национальной ступени Challenge.',
  '2–10 детей + 1–2 coach; местный отбор, затем National. Японский переводчик после согласования.',
  'SPIKE Prime / EV3 (также NXT / RCX по национальной странице), notebook, инновационный проект, поле.',
  start=date,end='2026-12-20'if region=='Kanto'else date,deadline='2026-10-31',scope='national',
  cost='JPY49 500 / команда за регион; National JPY31 900 дополнительно; hardware / дорога отдельно.',
  language='Японский; согласованный переводчик для иноязычной команды разрешён.',
  note='Tokyo: команда приходит в один из двух назначенных дней, не два полных дня матчей. Площадка планируется; число мест / внешний допуск проверяются отдельно. Founders — последний FLL сезон 2026/27, дальнейший hardware путь отдельно.',evidence='official_rules',date_scope='assigned_day_window'if region=='Kanto'else'competition_day')
 e.update(region='Азия',format='2–10 детей + 1–2 coach',deadline_note='31 октября 2026, конец дня Japan; раньше при заполнении.')
e=event('C1142','FIRST Japan · FLL Challenge · National BIOGLOW 2027','Япония','Tokyo · Institute of Science Tokyo (площадка планируется)',u['jp_challenge'],
 'Grades 4–High School 1 на 02.04.2026; international grade placement отдельно.','Условно: класс, команда, японский отбор.','Нет: ступень Challenge.',
 'Через японский региональный отбор, а не свободная запись на National.','Founders kit; SPIKE Prime / EV3, notebook, project.',start='2027-02-14',scope='national',
 cost='JPY31 900 national fee, сверх регионального и остальных расходов.',language='Японский; переводчик согласуется заранее.',note='Дата объявлена; площадка планируется. Qualification / международная квота и место ребёнка требуют отдельного подтверждения.',evidence='official_rules',date_scope='competition_day');e.update(region='Азия',admission_kind='qualifier')
e=event('C1143','FIRST Japan · FLL Explore · National Festival 2027 · планируется','Япония','Tokyo · Institute of Science Tokyo (планируется)',u['jp_explore'],
 'Grades 1–4 на 02.04.2026.','Условно: класс / место / иностранная команда.','Условно: класс / место / иностранная команда.',
 'Условия National должны объявить в ноябре; мировой выбор отдельно.','Explore model и poster.',scope='national',cost='JPY28 600 / команда, сверх региона / дороги.',
 language='Японский; переводчик согласуется заранее.',note='14 февраля 2027 отмечено организатором как planned. В ICS не добавлено. Explore не ранжирует команды; World Expo участие не гарантировано.',evidence='program');e.update(region='Азия',period='Предварительно 14.02.2027; дата требует подтверждения',date_status='Предварительно')
e=event('C1144','FIRST Japan · Future Edition 8+ · National BIOGLOW 2027','Япония','Tokyo · Ookayama campus, Institute of Science Tokyo (планируется)',u['jp_future'],
 'Grades 3–High School 1 на 02.04.2026; обычно 8–16; международные классы согласовать.',
 'Условно: проверить Grade 3 на контрольную дату; подходит по обычному возрасту.', 'Нет: ниже ступени 8+ / Grade 3.',
 'В первый сезон напрямую на National: 4–10 детей + 1–2 coach. Event Dock до 31.12.2026; иностранный приём согласовать.',
 'Два LEGO Education Computer Science & AI 8+ или 11+ комплекта; connection card; общий red / blue field. SPIKE не замена.',
 start='2027-02-13',deadline='2026-12-31',scope='national',cost='JPY49 500 / команда с сезонным набором; два robot kits, подготовка и дорога отдельно.',
 language='Японский; предварительно согласованный японский переводчик возможен.',
 note='В первый сезон региональных qualifiers нет. В игре четыре роли. World event планируется, страна / дата не опубликованы. Не подменять hardware Founders комплекта новым AI набором.',themes=('robotics','ai'),evidence='official_rules',date_scope='competition_day');e.update(region='Азия',format='4–10 детей + 1–2 coach',deadline_note='31 декабря 2026, конец дня Japan; раньше при заполнении.')

def camp(id,title,country,city,source,age,mat,osc,gear,cost,note,language='',mode='unconfirmed',themes=('robotics','coding')):
 e=event(id,title,country,city,source,age,mat,osc,'Подтвердить следующий набор, приём внешних детей, класс, язык и места; 2027 не объявлен.',gear,block='Лагеря',participation='day_camp',cost=cost,note=note,evidence='program',date_scope='future_cohort_unknown',themes=themes)
 e.update(region='Азия',language=language or e['language'],language_mode=mode,languages=['EN']if mode=='primary'else[],language_certainty='Язык данного предложения прямо указан.'if mode=='primary'else'Язык сайта или соседнего лагеря не подтверждает технический язык выбранной группы.')
 return e
camp('L454','ASIJ Chofu · Summer Day Camp · следующий набор','Япония','Tokyo · Chofu',u['asij_camp'],
 'Последний 2026 набор: Grades 1–6 по японской школьной сетке.','Условно: класс нового набора.','Условно: Grade 1 по японской сетке / birthday; не просто возраст 6.',
 'Малые программируемые роботы для всех классов внутри общей программы; английский, спорт, crafts.',
 '2026 ориентир: JPY92 000 / 5 дней общий; International Student Programme JPY126 000 / 5 дней. 2027 цена неизвестна.',
 'Все активности на EN прямо заявлены. Смены июля–августа 2026 прошли; не перенесены на 2027. Robotics — одна активность, технические часы неизвестны. Международный пакет и общий пакет имеют разные цены; жильё родителей отдельно.',
 language='Все активности преподаются на английском.',mode='primary',themes=('robotics','technology'))
e=camp('L455','YWIES Tongxiang · VEX Summer Camp · день / пансион · следующий набор','Китай','Tongxiang · Zhejiang',u['ycyw_primary'],
 '2026: Grades 4–12, интерес к VEX или школьная VEX team.','Условно: нужен Grade 4 нового набора.','Нет для опубликованного G4–12.',
 'Анализ правил сезона, первая сборка робота, основы программирования; модель VEX / IQ отдельно уточнить.',
 '2026 Primary: day RMB10 960, boarding RMB12 100; Secondary14 660 /15 280. Внешним ученикам те же цены. 2027 неизвестно.',
 '2026: 28 июня–5 июля, уже завершено. Есть day / boarding и внешний приём. EN-страница не устанавливает технический EN. Пансион лагеря не устанавливает возраст постоянного пансиона школы.');e.update(participation='mixed_camp',format='Дневной либо с пансионом; 2027 проживание / состав пакета отдельно')
camp('L456','YCIS Beijing · VEX Robot Olympics & Sports · следующий набор','Китай','Beijing',u['ycyw_primary'],
 '2026: Y4–9 и 8–13; следующий cutoff неизвестен.','Условно: класс и возраст, EN тренер.','Нет для опубликованного 8–13 / Y4–9.',
 'VEX robotics / coding и спорт; hardware выбранной группы уточнить.','2026 RMB9 500; 2027 неизвестно.',
 '2026 22 июня–1 июля прошли. EN teaching прямо указан соседнему CREST, но не этой VEX группе; язык не перенесён между программами.')
camp('L457','YCIS Shanghai Pudong · English Enrichment + STEAM · следующий набор','Китай','Shanghai · Regency Park',u['ycyw_primary'],
 '2026: 8–10 и Y4–6; новый набор отдельно.','Условно: возраст / класс; программа английского и общего STEAM.','Нет для опубликованных 8–10.',
 'PBL, digital technology, STEAM, искусство / музыка / service learning. Физическая робототехника не заявлена.',
 '2026 RMB10 800 / 2 недели; 2027 неизвестно.','2026 смены 22 июня–3 июля и 6–17 июля прошли. Развитие английского / общего STEAM, не подтверждённый соревновательный robotics camp.',language='English enrichment, EAL support; английская учебная программа.',mode='primary',themes=('technology',))
e=camp('L458','Young Coders Academy · Beijing / Shanghai · текущий набор уточнить','Китай','Beijing / Shanghai',u['yca_weekends'],
 'Возраст нового набора не проверен; архив летнего2026 описывал 5–7 /7–10 /10–14 /14–18.',
 'Кандидат после восстановления свежих условий.','Кандидат после восстановления свежих условий.',
 'Архив: LEGO, VEX GO / IQ, coding; weekend1.5h / competition2h.',
 'Текущая цена неизвестна.','Поисковая копия сайта описывает преимущественно EN и отдельные bilingual modules. Прямой запрос сейчас возвращает Coming soon; свежий набор / teaching EN не подтверждены. Архивные даты не добавлены в календарь. Не использовать как подтверждённую бронь.',themes=('robotics','coding'));e.update(participation='unconfirmed_program',priority='P3 — свежая программа недоступна',format='Архивный кандидат; действующее регулярное / camp предложение уточнить',evidence_level='historical_program')
e=camp('L459','STEAM SQUAD · ESM Early Simple Machines · регулярный курс','Тайвань','Taipei · Beitou',u['sq_esm'],
 '4–6 / Kindergarten; 40 занятий на год.','Нет: старше опубликованного диапазона.','По возрасту подходит; сложность после 3 лет опыта проверить.',
 'LEGO механизмы, шестерни, измерения; без заявленного программируемого робота.',
 'Сумма не опубликована; trial / годовой пакет отдельно.',
 'Старт группы16.10.2026, пятница19:00–20:00 Taiwan; 10 мест максимум. Это начало годового курса, не лагерь на один день. English используется для объяснения моделей; основной язык всего урока прямо не установлен.',language='Английская речь / материалы подтверждены; основной язык урока уточнить.',themes=('technology',));e.update(participation='regular',format='40 годовых занятий; пятница19:00–20:00',period='Старт16.10.2026; годовая сетка отдельно',date_scope='regular_schedule',support_languages=['EN'],language_mode='support',language_certainty='English with a purpose / explain in English — поддержка подтверждена; full English-led не заявлен.')
e=camp('L460','STEAM SQUAD · WeDo Computer Controlled Machines · регулярный EN курс','Тайвань','Taipei · Beitou',u['sq_ccm'],
 'Обычно 9–11, readiness Grade3; возраст ориентир, placement индивидуальный.',
 'Подходит по ориентиру; нужна проба сложности после 3 лет соревнований.','Ниже обычных9–11; возможное исключение только от оператора.',
 'LEGO WeDo2.0, сенсоры / motor / hub; 8 missions ×4 lessons =32 занятия; тестирование и debugging.',
 'Цена не опубликована; trial / комплект / весь курс отдельно.',
 'English-led прямо заявлено. Старт17.10.2026, суббота13:30–15:00; максимум10. Регулярный учебный курс не даёт готовую VEX / WRO team или Worlds qualification.',language='English-led; коммуникация с родителями EN / Traditional Chinese.',mode='primary');e.update(participation='regular',format='32 занятия; суббота13:30–15:00',period='Старт17.10.2026; регулярная сетка отдельно',date_scope='regular_schedule')
e=camp('L461','STEAM SQUAD · Code Club Python Foundation · регулярный курс','Тайвань','Taipei',u['sq_code'],
 '9–12 / Grades4–6; проба чтения / typing / логики.',
 'Условно: Grade4 readiness; прошлый опыт оценить.','Нет для опубликованных9–12.',
 'Python, десять глав, собственные программы; это software, физические роботы не заявлены.',
 'Цена и текущая сетка не опубликованы.',
 'Чтение и обсуждение на английском с sentence frames; полный основной язык урока не заявлен. Это регулярный курс, не датированный лагерь.',language='Английские инструкции / объяснения с поддержкой; полный язык урока уточнить.',themes=('coding',));e.update(participation='regular',format='Регулярный курс; график / trial отдельно',date_scope='regular_schedule',language_mode='support',support_languages=['EN'])
camp('L462','YCIS Beijing · CREST Science & Sports · следующий EN набор','Китай','Beijing',u['ycyw_primary'],
 '2026: Y1–6 / 5–10.','По опубликованному возрасту; новый возраст и класс отдельно.','По опубликованному возрасту; новый возраст и класс отдельно.',
 'Научные проекты, терминология, CREST и спорт. Роботы не заявлены.',
 '2026 RMB9 500 / person, оператор пишет10 days; новый пакет неизвестен.',
 'EN teaching прямо указано конкретному Science camp. 22 июня–1 июля2026 прошли; операторское10days не трактуется как10полных будних robotics дней.',language='English language instruction прямо указано программе.',mode='primary',themes=('technology',))
camp('L463','YCIS Qingdao · Immersive English + AI · следующий набор','Китай','Qingdao',u['ycyw_primary'],
 '2026: Grades1–6; numeric age не установлен.',
 'Кандидат по начальной ступени; новый набор / класс.','Условно: Grade1 и новый набор.',
 'Семь тем включая AI exploration / application, science и English phonics. Hardware / кодинг-часы не заявлены.',
 '2026 early bird RMB2 580 / неделю; multiple/friend2 380. Не цена2027.',
 '2026 три недели6–24июля прошли. Общий English/AI camp, не подтверждённая интенсивная robotics подготовка. AI содержанию нужен возрастной и технический разбор.',language='All-day immersive English прямо заявлен.',mode='primary',themes=('ai','technology'))

def src(key,title,claim,kind='school'):
 return dict(url=u[key],title=title,claim=claim,kind=kind,checked=CHECKED)
def school(id,name,iso,city,age,langs,boarding,boardnote,programme,admission,sources,evidence='programme',priority=2,mat='candidate',osc='candidate',cost='Свежая полная смета не проверена; tuition, admission, поддержка, bus, lab / competitions отдельно.',curriculum='',language_note='',results=None):
 s=dict(id=id,name=name,iso=iso,country={'JPN':'Япония','CHN':'Китай','TWN':'Тайвань'}[iso],region='Азия',city=city,school_type='private',curriculum=curriculum or age,ib_programmes=[],ages=age,instruction_languages=langs,
 language_note=language_note or 'Основной язык школы указан в источниках; язык конкретного junior coach и интервью проверяется отдельно.',
 fit=dict(mat=mat,osc=osc,note='Учебная ступень не подтверждает admission или место в команде.'),boarding=boarding,boarding_note=boardnote,programme=programme,labs='Доступ именно младшим, часы в неделю, coach и свободное место требуют проверки.',ai='Отдельная действующая junior AI программа не подтверждена.',results=results or [],evidence=evidence,admissions=admission,cost=cost,
 questions=['Кто тренирует именно возраст6/9, на каком языке, с каким team ID и текущим schedule?','Есть ли место обоим, placement по классам, самостоятельная роль, доступ к лаборатории и полная смета?'],sources=sources,checked=CHECKED,priority=priority,research_status='partial',verification='Первичные документы проверены; ни admission, ни enrolment, ни team place не подтверждены школой.')
 d['schools'].append(s);return s
school('S053','The American School in Japan · Chofu · ASIJ','JPN','Tokyo · Chofu','K–12; точный класс по placement',['EN'],'no','Day school; ученики живут с parent/guardian в Tokyo.',
 'ES: makerspace, простое coding / engineering. Семь VEX teams и annual tournament относятся к middle / high school; младшая competitive team не установлена.',
 'Гражданство США не требуется; один родитель fluent EN; проживание с родителями в Tokyo. Высокий EN, G1–8 language support. Reports / recommendations и индивидуальное screening.',
 [src('asij_faq','ASIJ FAQ','EN instruction; no citizenship restriction; day / parent residence'),src('asij_admit','ASIJ admissions','Parent EN / Tokyo residence'),src('asij_activities','ASIJ STEM activities','Primary coding; annual VEX MS/HS'),src('asij_spaces','ASIJ creative spaces','Elementary makerspace / design labs')],curriculum='American K–12; AP в старшей школе, не IB PYP')
school('S054','Christian Academy in Japan · CAJ / DOXA','JPN','Tokyo · Higashikurume','K–12; G1:6к01.09 при EN grade-level, при низкомEN6к01.04',['EN'],'no','Boarding programme отсутствует; жить с родителем / guardian.',
 'DOXA VEX programme действует с2015 по команде; 99484A. Текущая команда младших / IQ не установлена.',
 'Christian education; EN proficiency, reports2prior years, ES teacher recommendation. G1–8 EN within one grade; K/G1 исключения индивидуальны.',
 [src('caj_admit','CAJ eligibility','Age, parent residence, no boarding, EN proficiency'),src('doxa','DOXA programme','School team; claims10consecutive Worlds qualifications, unverified by yearly protocols')],
 evidence='other_result',results=[dict(league='VEX',season='Дата заявления не указана',stage='Worlds qualification',award='10 consecutive years — самоописание программы',team='DOXA',team_id='99484A',source=u['doxa'],provenance='school_report',limit='Период / дивизион / award не установлены. Не включено в числовой рейтинг мировых побед.')],priority=3)
school('S055','Harrow International School Appi Japan · permanent boarding','JPN','Iwate · Appi Kogen','11–18 / Years7–13',['EN'],'yes','Full boarding11–18; winter camp9–13 имеет другой возраст.',
 'British secondary pathway; конкретная текущая junior robotics команда / World award не установлены. Micro:bit camp — отдельная короткая программа.',
 'CAT4, handwritten EN essay и интервью; Y7–8 минимумCEFR A2,Y9B1,Y10+B2. Минимум short stay один term; fees / deposit отдельно.',
 [src('happi','Permanent school age','11–18 / full boarding'),src('happi_faq','Harrow admissions FAQ','EN levels, tests, minimum1term'),src('happi_camp','Winter camp is separate','9–13; December2026 camp is not school admission')],mat='future',osc='future',priority=4)
s=school('S056','Shen Wai International School · SWIS · Nanshan','CHN','Shenzhen · Nanshan','Early Years / Primary PYP → MYP / DP; exact entry age проверить',['EN'],'no','IB registry: DAY для всех трёх программ.',
 'IB PYP primary на английском. Актуальные team ID, младший тренер и соревновательный результат требуют отдельного подтверждения.',
 'Школьный Admissions shell доступен, но критерии / school profile не загрузились. Нужны foreign eligibility, классы и место в English junior team.',
 [src('swis_ib','IB official registry050023','PRIVATE; PYP/MYP/DP in English; DAY',kind='accreditor'),src('swis','SWIS official campus','Nanshan address / programmes'),src('swis_admit','Admissions shell limitation','Criteria dynamically missing')],priority=2)
s['ib_programmes']=[dict(programme=x,status='authorized_registry')for x in ['PYP','MYP','DP']];s['language_note']='EN / DAY подтверждены официальным IB registry для PYP, MYP, DP. Registry PRIVATE — классификация IB, а не проверка формы управления школы.'
school('S057','International School of Beijing · ISB','CHN','Beijing · Shunyi','Early Years–G12; placement / grade cutoff проверить',['EN'],'unknown','Day / boarding не установлен из прочитанных admissions страниц; проживание семьи отдельно.',
 'Design Center: robotics / electronics, fabrication; есть primary pathway, но основной Robotics Center помечен MS/HS. Primary coach / VEX place не установлены.',
 'English-medium или Dual Language. Foreign-school national categories / priority, EN placement, records и family meeting; foreign passport сам по себе не подтверждает все документы.',
 [src('isb_criteria','ISB admissions criteria','English-medium / dual-language, EY–12, foreign eligibility and priority'),src('isb_campus','ISB campus facilities','Robotics / electronics center labelled MS/HS')],
 language_note='Выбирать English-medium pathway; Dual Language имеет другой language balance. Junior технический EN отдельно.',priority=3)
school('S058','YK Pao School · Shanghai · primary / later boarding','CHN','Shanghai · Wuding Primary / later Songjiang','Primary Years1–5; middle6–8; high9–12',['EN','ZH'],'yes','Сообщение школы2020 подтверждает high-school boarding в Songjiang. Текущие условия и возраст начального / middle boarding не подтверждены. Для обоих сейчас проверять primary day.',
 'Двуязычная Chinese-English immersion; primary coding / robotics. Есть младшие VEX IQ награды2023 и2025 с точно ограниченным regional / Asia qualifier stage.',
 'Admission проверяет Chinese, English, Mathematics и Shanghai categories. Без китайского entry / language support не считать установленными.',
 [src('ypao_cs','School computer science journey','Primary computing, robotics; later Java / IB CS'),src('ypao_news2023','Pao report2023','Y4/Y5 VEX Asia junior2nd prize'),src('ypao_news2025','Pao report2025','Y6 East China regional VIQ ES Teamwork/Division champion'),src('ypao_board','Songjiang boarding campus · school report2020','High school boarding; current junior boarding ages not established'),src('ypao_admit','Admissions criteria · primary indexed text','Chinese / English / Maths assessment; Shanghai eligibility categories; direct full page timed out')],evidence='other_result',priority=3,
 language_note='Chinese / English immersion; это не полностью English primary. Технический язык / перевод и Chinese admission assessment согласовать.')
school('S059','Harrow LiDe School Hengqin · Zhuhai','CHN','Guangdong · Hengqin','K–12; Junior Boarding8–11, Senior11–18',['EN','ZH'],'yes','Junior boarding8–11; weekly Sunday evening–Friday, flexi варианты. Oscar6 ниже минимума8.',
 'Bilingual / bicultural LiDe; Deep Learning practical problem solving. Доказанный текущий junior league coach / World title не найден в прочитанном материале.',
 'Уточнить Chinese / English subject balance, foreign pupil route, placement, team и конкретный weekly / flexi slot.',
 [src('hengqin','School programme','Bilingual K–12; day and board'),src('hengqin_board','Boarding ages','Junior8–11; Senior11–18; five nights'),src('hengqin_fee','2026/27 fee table','Primary tuition, boarding, sibling discount')],priority=3,
 cost='2026/27: G1 RMB256 000/year; G2 265 000; G3–6 278 000. Weekly boarding100 000/year дополнительно; bus16 000/year; day meals53/day. 2nd biological sibling tuition−5% по условиям; не boarding. Не смета2027/28.',
 language_note='Bilingual Chinese / English; minimum EN / язык junior robotics не установлен. School English acquisition не доказывает all-English teaching.')
school('S060','Morrison Academy · Taichung · day / later dorm','TWN','Taichung','Elementary → high school; точный класс по admissions',['EN'],'yes','Dorm только для high-school; обычно минимум1год обучения в Morrison прежде заявки. Boarding admission отдельно; missionaries exceptions.',
 'American Christian curriculum, elementary technology integration. Современная junior competition team / World result не подтверждены. Это вариант школы с будущим пансионом, не установленный лидер robotics.',
 'Valid foreign passport, English / academic screening; ELL places и fees отдельно. Christian educational model. Домашний язык влияет на ELL conditions; статус определяет школа.',
 [src('morrison_admit','Morrison admissions / dorm FAQ','English proficiency; foreign eligibility; prior year before HS dorm'),src('morrison_es','Elementary curriculum','Technology integration, elementary stages')],priority=3,
 language_note='Academic English и English proficiency / ELL подтверждены admissions; junior coach technical language отдельно.')
school('S061','Taipei European School · British Primary Section','TWN','Taipei · Shilin · primary campus','British Primary Nursery–Year6',['EN'],'unknown','Постоянный пансион в прочитанных источниках не установлен.',
 'Primary STEAM / construction / junior architecture / animation. VEX в общей странице относится к Secondary campus; младшая competitive VEX team не подтверждена.',
 'Foreign passport + assessment / tryout / interview. BPS Y1–6 Semester1 2026/27 intake закрыт; Semester2 February–June2027 applications принимаются к рассмотрению, места не обещаны.',
 [src('tes_apply','Current admissions windows','Semester1 closed; Semester2 consideration; foreign passport'),src('tes_bps','British Primary','Y1–6; separate Chinese Enrichment Pathway'),src('tes_cca','Primary versus secondary CCAs','Primary STEAM; Secondary VEX'),src('tes_faq','EAL support','BPS English support')],priority=2,
 language_note='English British pathway выбирать отдельно от English/Chinese CEP и French/German sections; название TES не означает единый язык всех секций.')
school('S062','Kang Chiao Linkou · Elementary campus','TWN','New Taipei · Linkou','Elementary; exact grade / admission cutoff проверить',['EN','ZH'],'unknown','Наличие пансиона у secondary campus не переносится на elementary; junior boarding не подтверждён.',
 'Taiwan national elementary curriculum + international English division. Robotics team / results конкретно Linkou primary не подтверждены.',
 'Уточнить subject language, Chinese readiness и foreign admission. Linkou primary и Xiugang Grades7–12 — разные учебные ступени / кампусы.',
 [src('kcis_es','Linkou elementary programme','National curriculum + English division; exact current robotics team not established')],priority=3,
 language_note='Bilingual environment; English division не доказывает full English maths / science / robotics. Xiugang results не перенесены сюда.')

# Bounded reported awards; no inferred decade-long ranking or World title.
h=d['school_history'];h['entities'].append(dict(id='JPN-CHN-YKPAO',name='YK Pao School · campus/grade-specific results',kind='school',country='China',age='Y4–Y6',school_id='S058',note='School reports only; exact stage retained; not a World champion claim.'))
for id,year,stage,award,grade,key in [('H151',2023,'15th VEX Asia competition · junior school group','2nd prize','Y4/Y5','ypao_news2023'),('H152',2025,'VEX Asia China qualifier · East China regional · VIQ Elementary','Division Champion and Teamwork Overall Champion','Y6','ypao_news2025')]:
 h['results'].append(dict(id=id,entity_id='JPN-CHN-YKPAO',year=year,league='VEX IQ',category=grade,stage=stage,award=award,level='regional_podium'if year==2023 else'regional_match',source=u[key],provenance='school_report',team='Pao pupils; formal team ID not established',team_id=None,note='Школьный отчёт. Не мировой титул; участие детей не устанавливает школу как владельца внешней команды.',checked=CHECKED))
h.update(version=51,checked=CHECKED)
next(s for s in d['schools']if s['id']=='S058')['results']=[dict(league=r['league'],season=str(r['year']),stage=r['stage'],award=r['award'],team=r['team'],team_id='',source=r['source'],provenance=r['provenance'],limit=r['category']+'; '+r['note'])for r in h['results'][-2:]]

def profile(id,name,summary,categories,ids,keys,nuances,language):
 q=dict(id=id,name=name,group='regional',age_summary=' / '.join(c['age']for c in categories),age_tags=['6','9','10-12'],summary=summary,categories=categories,event_ids=ids,legacy_ids=[],route=['Проверить класс / реальную базу команды','Выбрать наставника и язык','Уточнить регистрацию / квоту и hardware','Местный сезон и самостоятельная работа','Дальнейший national / World отбор отдельно'],hardware='См. категории; новый AI hardware и Founders не взаимозаменяемы.',language=language,importance='Национальный путь крупной мировой сети; отдельные фестивали не ранжируют участников.',strengths=summary,requirements=['Самостоятельная инженерная работа детей','Класс и текущая команда важнее только года рождения','Заявка семьи не подана'],nuances=nuances,cost='См. конкретные карточки; kit, взносы и дорога отдельно.',award='Worlds qualification, regional title, фестивальное признание и World Champion — разные результаты.',sources=[dict(title=k,url=u[k],checked=CHECKED)for k in keys],evidence='Прочитаны первичные национальные programme / eligibility pages; ограничения указаны.',checked=CHECKED)
 d['league_guide']['profiles'].append(q);return q
def cat(name,age,team,hw,rule,entry):return dict(name=name,age=age,team=team,hardware=hw,age_rule=rule,entry=entry)
profiles=[profile('first-japan-junior','FIRST Japan · Explore / Challenge / Future 2026–27',
 'Национальные классы на02.04.2026 и Japanese interpreter gate. Оскар: Explore после проверки Grade1; Матвей: Explore либо Challenge/Future по классу.',
 [cat('Explore','G1–4','2–6 +1–2 mentor','SPIKE Essential / WeDo2.0','Класс02.04.2026; international school согласовать','Region festival → planned National; World recommendation неизвестна'),cat('Challenge','G4–High1; обычно9–16','2–10 +1–2 coach','SPIKE Prime / EV3','Класс02.04.2026; international school согласовать','Japan region → National → отдельная World quota'),cat('Future8+','G3–High1; обычно8–16','4–10 +1–2 coach','2 CS&AI8+ или11+ комплекта','Класс02.04.2026','Первый сезон напрямую National13.02.2027')],
 [f'C{i}'for i in range(1134,1145)],['jp_explore','jp_challenge','jp_future'],['Переводчик разрешён только после предварительного согласования','Explore не присваивает чемпиона','2027/28 FIRST / LEGO пути и hardware проверяются заново'], 'Японский; иноязычная команда может согласовать сопровождающего переводчика.'),
 profile('vex-japan-junior','VEX IQ Japan · domestic qualification route','Japan National требует реальной японской деятельности команды, а не номера или туристической поездки.',
 [cat('VEX IQ Elementary','Elementary по текущим правилам','Registered team; состав / Student definition по manual','VEX IQ Level Up','Grade / age by current manual; roster каждого ребёнка','Approved Japan tournament → Qualification Spot → National')],['C140','C335','C377','C464','C537','C602'],['jp_vex_es'],['C537 date header / body conflict, исключён из датированного календаря','Scrimmage / workshop / skills-only не дают national Qualification Spot','Registered Japan team с основной базой за рубежом не подтверждает eligibility'], 'Язык выбранного coach / notebook / judging уточнить; EN-страница event не доказывает EN интервью.'),
 profile('china-junior-school-route','China · junior VEX / FIRST through school or academy','Подбирать English junior coach и конкретный team ID; Shanghai bilingual / Shenzhen IB / Beijing English-medium — разные пути.',
 [cat('VEX IQ school route','Elementary; event/manual отдельно','Registered school / academy team','VEX IQ; VEX GO учебный kit не равен IQ competition robot','Класс и roster по event/manual','Regular tournament → разрешённая national / Signature route'),cat('English academy candidate','Свежий набор / возраст не подтверждены','Coach/team acceptance отдельно','По выбранной programme','Не из языка сайта','YCA current site Coming soon; сначала восстановить свежие правила')],['C285','C419','C577','L455','L456','L458'],['ycyw_primary','yca_weekends','swis_ib','isb_criteria'],['ACAMIS school / membership / foreign entry не считать свободной записью','Школьная лаборатория secondary не доказывает primary доступ','YCIS CREST EN не перенесён на соседний VEX camp'], 'SWIS IB PYP EN и ISB English-medium подтверждены; camp/junior coach EN проверяется независимо.')]
d['league_guide'].update(version=51,checked=CHECKED)

f=dict(version=51,checked=CHECKED,status='partial',region_key='east_asia_focus',title='Япония / Китай / Тайвань · школы, лагеря, английский и соревнования',region_label='ВОСТОЧНАЯ АЗИЯ · ДВА РЕБЁНКА, ТРИ СТРАНЫ',heading='Школа, команда и язык. Отдельный путь каждому.',
 family='Матвей (2017) и Оскар (2020): сейчас 9 и 6 лет, в 2027 исполняется 10 и 7. Оба могут учиться на английском и испанском; есть трёхлетний опыт робототехники. Точные даты рождения и школьные классы ещё не установлены.',
 conclusion='Моя оценка для семьи: первой пробовать Тайвань как постоянную базу, Японию — для короткой английской инженерной программы и сравнения школ; Китай — после проверки конкретной English junior team и китайского языкового баланса. Сейчас я бы предпочёл дневную школу для обоих с проживанием семьи рядом. Это оценка соответствия, не рейтинг стран или гарантия побед.',
 limitations='Частичный углублённый проход трёх стран. Нет полного списка всех азиатских школ / лагерей или 5–10-летнего рейтинга. School English, camp English, coach English, место и foreign quota проверяются отдельно. Глобальное исследование продолжается; заявки, сообщения школам и платежи не отправлялись.',
 family_picks_heading='Лучшие следующие проверки для вашей семьи',family_picks_note='Выбор по возрасту, документально подтверждённому языку и полезности пробы; известная программа не означает свободное место.',
 countries=[],family_picks=[],probe_scenarios=[],development_phases=[],steps=[],sources=[])
specs=[
 ('Тайвань','TWN','Первая семейная база для проверки','Выбор TAS / AST / TES плюс отдельная English junior тренировка; сначала проверить, где реально примут обоих и дадут инженерные роли.',
  'CCM English-led9–11; после3лет опыта оценить сложность. AST Worlds2023 былиG5–12 — младший отбор не установлен.',
  'Дневная elementary / ESM4–6 с EN поддержкой; Kindergarten/G1 определяется cutoff, не только2020.',
  'Expedition27 — English STEAM8–12, Оскар ниже ориентира. Grove EN+ZH engineering age unknown. TYPA robotics camp technical EN пока не подтверждён.',
  'TAS,S003; AST,S020; TES BPS,S061. Morrison dorm толькоhighschool+prior year. Linkou primary не равен Xiugang.',
  'Taipei/Beitou для пробы; Taichung если coach/AST действительно подходят обоим.', ['L142','L143','L144','L146','L459','L460','L461','C027','C033','C034','C035','C356','C778','C870'],['vex','first','marc'],['S003','S020','S061','S060','S062']),
 ('Япония','JPN','Самая конкретная короткая English проба','Есть датированные TCC недели и Harrow winter; ASIJ day school / EN summer candidate. National leagues требуют класса и местной команды.',
  'TCC5–12 сейчас; Harrow Winter9–13 при birthday. Future8+ возможен поGrade3; Challenge не из одного возраста9.',
  'TCC5–12; ASIJ Summer толькоGrade1–6. Harrow Winter и permanent school не подходят сейчас.',
  'TCC Fall12–16 /19–23Oct; Winter14–18 /19–23Dec. Robotics content выбранной недели согласовать. Harrow13–19Dec включает только5учебных дней.',
  'ASIJ — English day/ESmakerspace; CAJ — English Christian day. Их старший VEX не равен junior месту. Harrow permanent11–18.',
  'Tokyo/Chofu day programme; Appi отдельно только Матвею, если семья принимает разные программы.', ['L198','L199','L200','L201','L202','L454','C1134','C1138','C1142','C1144','C537'],['first-japan-junior','vex-japan-junior'],['S053','S054','S055']),
 ('Китай','CHN','Индустрия и школьная команда после языковой проверки','Сравнивать Shenzhen English IB, Beijing English-medium и Shanghai bilingual отдельно. Много VEX events не доказывает открытый вход иностранной команды.',
  'SWIS PYP / конкретный coach; YK Pao требует Chinese readiness. Hengqin boarding8+ по возрасту возможно, junior robotics strength не установлена.',
  'English primary путь SWIS/ISB проверять, общий EN CREST5–10 кандидат; Hengqin boarding8+ сейчас нет.',
  'Tongxiang VEXG4–12 day/boarding: EN не установлен. Beijing VEX8–13 age/class gate; English CREST5–10 отдельно. Все summer2026 прошли;2027 даты неизвестны.',
  'SWIS EN PYP day; ISB English-medium / Dual Language выбор; YK Pao bilingual primary; Harrow Hengqin bilingual junior boarding8+.',
  'Shenzhen/Nanshan прежде других: одна школа+mentor+industrial visit после проверки. Beijing/Shanghai альтернативы.', ['C285','C419','C577','L455','L456','L457','L458','L462','L463'],['china-junior-school-route','vex','first'],['S056','S057','S058','S059'])]
for name,iso,verdict,reason,mat,osc,camptext,schooltext,city,ids,pids,sids in specs:
 f['countries'].append(dict(name=name,iso=iso,verdict=verdict,reason=reason,mat=mat,osc=osc,camp=camptext,school=schooltext,city_route=city,event_ids=ids,profile_ids=pids,school_ids=sids,
  risk='Точный класс, coach, технический язык, foreign entry и место обоим до выбора базы.',
  budget={'TWN':'AST: опубликованная elementary tuitionNTD249500/semester без года; дополнительные fees / поддержка отдельно. Новая семейная смета не подтверждена.', 'JPN':'TCC129000JPY+tax/5days; Harrow winter440000JPY на одного. ASIJ2026 general92000 / international126000 за5days. School annual fee отдельно.', 'CHN':'Hengqin2026/27 G1+G3 tuition534000RMB/year до sibling discount и extras. Возможные5% для второго ребёнка: G1discount12800, итого521200. Это пример классов, не назначенный placement; boarding только старшему +100000.'}[iso],
  results_check={'TWN':'У TAS/AST есть отдельные исторические school results; текущая primary team и персональный admission не установлены.', 'JPN':'CAJ:10 consecutive Worlds qualification — school claim без годовых протоколов. ASIJ junior World winners не подтверждены.', 'CHN':'YK Pao: награды младших2023 и East China VIQ Elementary2025 по сообщениям школы; не мировые титулы. Актуальную младшую команду SWIS и тренера ещё нужно подтвердить.'}[iso]))

def pick(kind,country,title,why,gate,ids=(),sids=(),keys=()):
 f['family_picks'].append(dict(kind=kind,country=country,title=title,why=why,gate=gate,event_ids=list(ids),school_ids=list(sids),source_urls=[u[k]for k in keys]))
pick('camp','Япония','Вдвоём: TCC сейчас / ASIJ летом после объявления','TCC опубликован5–12; ASIJ2026 всеактивностиEN и roboticsG1–6. Это проба обучения и бытовой адаптации.', 'У TCC robot project конкретной недели неизвестен; ASIJ2027 даты ещё не объявлены. Оскару проверитьGrade1.', ['L198','L199','L200','L201','L454'],keys=['asij_camp'])
pick('camp','Япония','Матвею: Harrow winter micro:bit + skiing','13–19декабря2026, English boarding camp9–13,5учебных дней; осмысленная инженерная проба.', 'Оскар6 не проходит; camp не равно permanent school11+. Место / birthday / готовность к пансиону.', ['L202'],['S055'],['happi_camp','happi_faq'])
pick('league','Япония','FIRST с согласованным переводчиком','В Explore возможно проверить обоих; Матвею Future8+ либоChallenge по классу; правила национального оператора уточнены.', 'Японский школьный класс на02.04.2026; international school и иностранный приём согласовать до заявки.',['C1134','C1138','C1144'],keys=['jp_explore','jp_challenge','jp_future'])
pick('school','Тайвань','TAS / AST / TES: начать со школьного и coach интервью','English школьная среда и доступ к начальной ступени; TAS/AST имеют отдельные исторические robotics результаты.', 'Место9/6, действующая junior team, trainer EN и campus. TES Semester1 закрыт, Semester2 толькоconsideration.',sids=['S003','S020','S061'],keys=['tes_apply','tes_cca'])
pick('camp','Тайвань','Регулярная English robotics проба CCM','Конкретно English-led,8WeDo missions,32занятия; можно оценить наставника.', 'Обычно9–11/Grade3: Матвею после опыта не обязательно достаточно сложно, Оскару исключение не обещано. Это не holiday camp.',['L460','L459','L461'],keys=['sq_ccm','sq_esm'])
pick('school','Китай','Shenzhen SWIS и Beijing ISB: English pathway','SWIS официально EnglishPYPday, ISB допускает English-medium вариант. Лучше проверять конкретную младшую группу.', 'SWIS Admissions content неполный; ISB roboticscenterMS/HS не доказывает primary lab/Worlds place.',sids=['S056','S057'],keys=['swis_ib','isb_criteria','isb_campus'])
pick('camp','Китай','VEX camp с day / boarding: Tongxiang','Опубликованный campG4–12 с внешним приёмом, правила/сборка/coding; реальные разные ценыday/boarding.', '2026прошёл,2027необъявлен. EN technical teaching неизвестен; ОскарнижеG4.',['L455'],keys=['ycyw_primary'])
pick('school','Китай','Hengqin: самый ранний подтверждённый пансион в этой выборке','Junior boarding8–11; current2026/27fee tableпрочитана и осмотрена.', 'Матвею по возрасту кандидат, Оскару6 нельзя; bilingual Chinese-English. Нужна доказанная junior robotics team.',sids=['S059'],keys=['hengqin_board','hengqin_fee'])

for id,label,intro,verdicts,events,schools in [
 ('season','Каникулы вдвоём','Для короткой пробы сначала выбирать возраст и конкретную смену с EN; техническая сложность после3лет опыта важнее словаSTEM.',
  ['Taipei: школа + отдельный курс; camp младшему не гарантирован','Tokyo: наиболее конкретные English варианты5–12','China: EN Science для обоих; robotics язык ещё уточнять'],
  [['L142','L143','L459','L460'],['L198','L199','L200','L201','L454'],['L455','L462','L463']], [[],[],[]]),
 ('school','Школа на 2–3 года','Сначала проверять обоим школьное место и отдельную действующую команду; переносить семью ради логотипа leagues я бы не стал.',
  ['Taiwan: первый shortlist семейной базы','Japan: сильная English day среда, junior coach отдельно','Shenzhen / Beijing: English pathway + foreign gate'],
  [['L460','C356'],['C1134','C1144'],['C285','L458']], [['S003','S020','S061'],['S053','S054'],['S056','S057','S058']]),
 ('boarding','Пансион: сейчас или позже','В проверенной выборке нет установленного полностью English постоянного пансиона, подходящего обоим сейчас. Разделять детей ради boarding в этом возрасте я бы не предлагал.',
  ['Morrison: highschool, prior1year; сейчасday','HarrowAppi:11+school,9+camp','Hengqin:8+boarding, bilingual; Оскарунет'],
  [[],['L202'],['L455']], [['S060'],['S055'],['S059']])]:
 f['probe_scenarios'].append(dict(id=id,label=label,intro=intro,countries=[dict(iso=c['iso'],verdict=v,reason=c['reason'],gate=c['risk'],event_ids=eids,school_ids=sids)for c,v,eids,sids in zip(f['countries'],verdicts,events,schools)]))
f['development_phases']=[
 dict(period='2026–2028 ·9/6→11/8',title='Одна база, два самостоятельных проекта',detail='Дневная школа, один устойчивый coach, каждую неделю сборка/coding/тесты/EN объяснение. Оскару механика и датчик, Матвею autonomous missions и notebook. Одна основная league на сезон; менять hardware под опубликованные2027/28правила.'),
 dict(period='2028–2031 ·11/8→14/11',title='От junior команды к инженерной глубине',detail='VEX IQ / WRO либо актуальная младшая FIRST программа по местному классу. CAD, электроника, Python/C++, измеримые эксперименты и публичное портфолио. Языковая подготовка к judging; World quota только из фактического квалификационного результата.'),
 dict(period='2031–2034 ·14/11→17/14',title='Выбрать соревновательную команду и реальную лабораторию',detail='Матвею FTC/V5/FRC по возрасту и школе; Оскару свой переход. Пансион рассматривать по самостоятельности и действующему coach, а не по раннему престижу. Проектыcomputer vision,automation и реальные пользовательские задачи.'),
 dict(period='2034–2038 ·17/14→21/18',title='Инженерия и предпринимательство',detail='Research/internship и свой работающий продукт, интервью пользователей, прототип, тесты, стоимость производства, презентация и честная роль каждого. Азияhardwareecosystem полезна при доступе к людям/лабораториям; медали остаются частью портфолио, а не всей целью.')]
f['steps']=[dict(title='Сначала тест обеих возрастных ступеней',detail='Визит/пробное занятие у2–3school/coach кандидатов; получитьweekly timetable и поимённую роль ребёнка. Для Матвея не повторять beginnerWeDo без более сложного проекта.'),dict(title='Проверить English именно в технологии',detail='School medium, technical coach, camp lessons и competition judging — четыре отдельных подтверждения. Пробная техническая задача и объяснение наEN полезнее обещаниябилингвальности.'),dict(title='Сверить admission и национальную принадлежность',detail='Exact birthdays / текущиеgrades остаютсянеизвестны; checkschoolcutoff. Японский NationalVEX требует Japanbasedteam; FIRSTJapan позволяет interpreter после согласования. Переезд не даётавтоматическиschool/Worldquota.'),dict(title='Сравнить полный семейный год',detail='Tuitionдвухдетей + admission/EAL + жильё/дорога + robotkits/coach/competitiontravel. Цены2026/27 и прошлыхsummer — ориентир, не будущая смета. PublicfullENjunior school в этомпроходене подтверждена; не заявлено, что таких нет.')]
source_names={'asij_faq':'ASIJ: язык и приём','asij_camp':'ASIJ: английский дневной лагерь','asij_activities':'ASIJ: возраст и команды VEX','caj_admit':'CAJ: возраст и проживание с родителями','doxa':'DOXA: школьная команда VEX','happi':'Harrow Appi: постоянный пансион','happi_faq':'Harrow Appi: язык и поступление','happi_camp':'Harrow Appi: зимний лагерь','hengqin_board':'Harrow Hengqin: возраст пансиона','hengqin_fee':'Harrow Hengqin: тарифы 2026/27','swis_ib':'SWIS: официальный реестр IB','isb_criteria':'ISB Beijing: язык и критерии поступления','tes_apply':'TES: текущие окна подачи','tes_cca':'TES: младшие STEAM и старшие VEX','morrison_admit':'Morrison: поступление и общежитие','kcis_es':'Kang Chiao Linkou: начальная школа','jp_explore':'FIRST Japan: Explore BIOGLOW','jp_challenge':'FIRST Japan: Challenge BIOGLOW','jp_future':'FIRST Japan: Future 8+','jp_vex_es':'VEX Japan National: допуск и конфликт дат','ycyw_primary':'YCYW: опубликованные лагеря 2026','sq_ccm':'STEAMSQUAD: английская робототехника WeDo','sq_esm':'STEAMSQUAD: механизмы для младших'}
f['sources']=[dict(title=title,url=u[k],checked=CHECKED)for k,title in source_names.items()]

# Improve spacing in newly authored prose while preserving identifiers and URLs.
def readable(value):
 if isinstance(value,dict):return {k:(v if k in ('id','url','source','team_id','region_key') else readable(v))for k,v in value.items()}
 if isinstance(value,list):return [readable(v)for v in value]
 if isinstance(value,str)and not value.startswith(('https://','http://')):
  value=re.sub(r'([А-Яа-яЁё])(?=[0-9A-Za-z])',r'\1 ',value)
  value=re.sub(r'([0-9A-Za-z])(?=[А-Яа-яЁё])',r'\1 ',value)
  return value
 return value
for e in new:e.update(readable(e))
for s in d['schools'][-10:]:s.update(readable(s))
for q in profiles:q.update(readable(q))
def polish_focus(f):
 reasons=[
  'Сравнить TAS, AST и британскую начальную ступень TES. Сначала проверить места обоим детям, действующего младшего тренера и самостоятельные инженерные роли.',
  'Есть английские недели TCC и зимний лагерь Harrow. ASIJ и CAJ — кандидаты для дневной школы. В национальных лигах отдельно проверяются школьный класс и местная команда.',
  'Сравнивать английский IB в Шэньчжэне, английскую программу в Пекине и двуязычную школу в Шанхае. Большое число VEX-турниров само по себе не подтверждает свободный иностранный допуск.'
 ]
 for c,reason in zip(f['countries'],reasons):
  c['reason']=reason;c['risk']='До выбора базы подтвердить класс, места обоим, язык технических занятий, тренера и допуск иностранной семьи.'
 labels={
  'season':['Тайбэй: отдельный курс; лагерь младшему ещё уточнить','Токио: английские программы для 5–12 лет','Китай: английская наука для обоих; язык VEX уточнить'],
  'school':['Тайвань: первый список для семейной базы','Япония: английская дневная школа и отдельный тренер','Шэньчжэнь / Пекин: английский путь и условия приёма'],
  'boarding':['Morrison: старшая школа после года обучения','Harrow Appi: школа с 11, лагерь с 9 лет','Hengqin: пансион с 8; Оскару пока рано']
 }
 boarding_reasons=[
  'В Morrison общежитие доступно старшеклассникам после минимум года в школе; заявление на проживание рассматривается отдельно. Сейчас обоим искать дневную ступень.',
  'Постоянный английский пансион Harrow Appi принимает с 11 лет. Зимний лагерь 9–13 — самостоятельная программа: Матвей кандидат, Оскар младше минимума.',
  'Harrow Hengqin объявляет младший пансион 8–11 лет. Матвей подходит по возрасту; Оскар — нет. Учебная среда китайско-английская, младшую команду робототехники ещё нужно подтвердить.'
 ]
 for scenario in f['probe_scenarios']:
  for i,c in enumerate(scenario['countries']):
   c['verdict']=labels[scenario['id']][i]
   c['reason']=boarding_reasons[i]if scenario['id']=='boarding'else reasons[i]
   c['gate']='Возраст программы, принятая заявка, язык тренера и место ребёнка — отдельные условия.'
 f['probe_scenarios'][0]['intro']='Для короткой поездки сначала выбрать конкретную английскую смену и подходящий возраст. После трёх лет опыта детям важна сложность проекта, а не только слово STEM.'
 f['probe_scenarios'][1]['intro']='Сначала получить школьное место для обоих и проверить отдельную действующую команду. Основание для переезда — наставник, регулярные занятия и учебная среда.'
 f['probe_scenarios'][2]['intro']='В проверенной выборке не установлен постоянный полностью английский пансион, подходящий обоим сейчас. Для этого возраста мой первый выбор — дневная школа и проживание семьи рядом.'
 pick_copy=[
  ('Вдвоём: TCC сейчас, ASIJ после объявления новой смены','TCC публикует возраст 5–12. В ASIJ все активности на английском, робототехника входит в общую программу 1–6 классов. Это проба обучения и бытовой адаптации.','Проект робота конкретной недели TCC ещё уточнить. ASIJ не объявил смены 2027; Оскару проверить соответствие первому классу.'),
  ('Матвею: зимний Harrow, micro:bit и лыжи','13–19 декабря 2026: английский лагерь с проживанием для 9–13 лет, пять учебных дней. Инженерный проект совмещён с лыжами.','Оскар ниже минимального возраста. Лагерь не подтверждает поступление в постоянную школу с 11 лет; место и готовность ребёнка проверяются отдельно.'),
  ('FIRST Japan с согласованным переводчиком','Explore можно рассмотреть для обоих после проверки класса. Матвею также Future 8+ или Challenge по японским школьным правилам.','Проверить школьный класс на 2 апреля 2026, соответствие международной школы, иностранный приём и разрешение на японского переводчика.'),
  ('TAS / AST / TES: школа и интервью с младшим тренером','Английская школьная среда и начальная ступень. У TAS и AST есть отдельные исторические результаты, которые не доказывают место в нынешней команде.','Подтвердить класс, кампус, места обоим и технический английский тренера. В TES первый семестр закрыт, заявки на второй рассматриваются без гарантии места.'),
  ('Тайбэй: пробный английский курс робототехники CCM','Оператор прямо пишет об английском преподавании: восемь миссий WeDo, 32 занятия. Можно оценить наставника на пробе.','Обычно 9–11 лет и готовность третьего класса. Матвею курс может быть прост после его опыта; Оскару исключение не обещано. Это регулярный курс.'),
  ('SWIS в Шэньчжэне и ISB в Пекине: английская программа','У SWIS английский PYP подтверждён реестром IB. В ISB можно выбирать английскую программу отдельно от двуязычной.','Текущие критерии SWIS загрузились не полностью. Робототехнический центр ISB для средних и старших не доказывает доступ младших или мировые победы.'),
  ('Tongxiang: VEX-лагерь дневной или с проживанием','Опубликован лагерь для 4–12 классов с внешним приёмом: правила соревнования, сборка и основы программирования. Дневной пакет и пансион имеют разные цены.','Смена 2026 уже прошла, 2027 не объявлена. Технический английский не подтверждён; Оскар ниже указанной школьной ступени.'),
  ('Hengqin: наиболее ранний подтверждённый пансион в этой выборке','Младший пансион 8–11 лет. Проверены тарифы 2026/27 на обучение, проживание и скидку второму ребёнку.','Матвей кандидат по возрасту, Оскар пока младше минимума. Школа двуязычная; действующую младшую команду и язык тренера ещё нужно подтвердить.')
 ]
 for pick,(title,why,gate)in zip(f['family_picks'],pick_copy):pick.update(title=title,why=why,gate=gate)
 f['steps']=[
  dict(title='Проба для обеих возрастных ступеней',detail='Посетить 2–3 школы и тренера, получить недельное расписание и конкретную роль каждого ребёнка. Матвею после трёх лет опыта нужна задача сложнее повторного знакомства с WeDo.'),
  dict(title='Английский именно на технических занятиях',detail='Язык школы, тренера, лагеря и судейства проверяется отдельно. На пробе ребёнок собирает или программирует механизм и объясняет решение по-английски.'),
  dict(title='Поступление и право команды на отбор',detail='Уточнить точные даты рождения и классы детей. Японский VEX National требует команды с реальной японской базой; FIRST Japan позволяет согласовать переводчика. Переезд не подтверждает школьное место или мировую квоту.'),
  dict(title='Полная стоимость семейного года',detail='Сравнить обучение двоих, вступительные платежи, языковую поддержку, жильё, дорогу, оборудование, тренера и поездки команды. Цены 2026/27 — ориентир. Полностью английская государственная младшая школа в этом проходе не подтверждена; поиск таких школ остаётся открытым.')
 ]
 return f
f=readable(polish_focus(f))
d['east_asia_focus']=f
d['events'].extend(new)

known={s['url']for s in d['sources']}
items=[dict(url=e['source'],title=e['title'],checked=CHECKED,evidence='Первичная programme/event page; ограничения указаны.')for e in new+[byid['C537']]]
for s in d['schools'][-10:]:items += [dict(url=x['url'],title=x['title'],checked=CHECKED,evidence=x['claim'])for x in s['sources']]
for q in profiles:items +=[dict(url=x['url'],title=x['title'],checked=CHECKED,evidence='Первичный источник; актуальность/ограничения указаны.')for x in q['sources']]
for x in items:
 if x['url']not in known:d['sources'].append(x);known.add(x['url'])
a=d['completeness_audit'];a.update(version=51,checked=CHECKED,new_ids=[e['id']for e in new],new_profiles=[q['id']for q in profiles],updated_ids=['C537'],new_school_ids=[f'S{i:03}'for i in range(53,63)],updated_profile_ids=[],validation_previous=copy.deepcopy(a['validation']),validation=dict(version=51,status='pending',publication='pending'),conclusion='Восточная Азия углублена: школьные campus/возраст/язык, camp и national eligibility разделены. Противоречивый японский National исключён из датированного календаря. Мировой аудит остаётся частичным.')
a['source_issues'] += [dict(name='Japan VEX National C537',status='31.01.2027 header versus20–21.02.2027 EN/JPbody; Japanese domestic activity required; disputed dates excluded fromICS.',official_alternative=u['jp_vex_es']),dict(name='YCA current pages',status='Live Coming soon versus richer cachedsearchbody; current Englishcohort notconfirmed.',official_alternative=u['yca_weekends']),dict(name='SWIS admissions / IB registry',status='Schoolbodydynamiccontentmissing; IBregistryreadinprimaryindexedtext despite direct403. Exact foreignentry/grade/currentcoach unknown.',official_alternative=u['swis_ib']),dict(name='YK Pao sources',status='Primaryschoolnewsread throughweb; direct requests timedout. Regional awards notWorld title; Chinese entry remains a gate.',official_alternative=u['ypao_news2025'])]
d['school_focus'].update(version=51,checked=CHECKED,conclusion='Добавлены10досье EastAsia; English school / junior team / boarding подтверждаются отдельно. Полного мирового school ranking нет.')
d['camp_focus'].update(version=51,checked=CHECKED,added_ids=[e['id']for e in new if e['block']=='Лагеря'],updated_ids=[],validation=dict(version=51,status='pending'))
d['asof']=CHECKED;d['expansion_log'].append(dict(version=51,checked=CHECKED,scope='Japan China Taiwan school boarding camp English junior competition routes',added=len(new),new_profiles=len(profiles),new_schools=10,new_history_results=2,status='partial; worldwide objective preserved'))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=json.loads((WORK/'sources-east-asia-v51/receipt.json').read_text())
read={'asij_activities','asij_spaces','asij_camp','asij_camp_home','doxa','happi','happi_faq','happi_camp','hengqin','hengqin_board','ycis_camp','morrison_admit','morrison_es','tes_cca','first_jp','jp_explore','jp_challenge','jp_future','caj_admit','hengqin_fee','tes_apply','tes_bps','tes_faq','isb_campus','ycyw_primary'}
for row in receipts:
 row.pop('path',None);row['primary_body_read']=row['status']==200 and row['name']in read
 if row['name']in ['yca_camp','yca_weekends','yca_home']:row['limitation']='Current page Coming soon; cached full programme not confirmed live.'
extra=[dict(name=k,url=u[k],channel='web_primary_page'if k!='ypao_admit'else'web_primary_indexed_text',checked=CHECKED,limitation='See scoped claim / source issues')for k in ['sq_ccm','sq_esm','sq_code','jp_vex_es','asij_admit','asij_faq','asij_guidelines','isb_criteria','swis_ib','kcis_es','ypao_cs','ypao_news2023','ypao_news2025','ypao_board','ypao_admit']]
(ROOT/'data/east-asia-source-receipts-v51.json').write_text(json.dumps(dict(version=51,checked=CHECKED,sources=receipts,additional_primary_reads=extra,visually_inspected_pdf_pages={'hengqin_fee':[1]}),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,completeness_audit='data/audit-v51.json',latest_validation_previous=r['latest_validation'],latest_validation=dict(version=51,status='pending',publication='pending'))
r['research_passes'].append(dict(version=51,checked=CHECKED,scope='User-requested Japan/China/Taiwan schools boarding camps EN and competition pathways',status='implementation; validation pending',added=len(new),new_profiles=len(profiles),new_schools=10,new_history_results=2))
r['previous_goal_turn_classification']=dict(status='progress',evidence='v50 publicly deployed; current human steering is East Asia. Earlier Europe and local routes preserved.',remaining='Fullworldcoverage; exactschool/coachplaces andcountry-specificeligibility. Goalactive.')
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=51,events=len(d['events']),added=len(new),schools=len(d['schools']),profiles=len(d['league_guide']['profiles']),history=len(h['results'])),ensure_ascii=False))
