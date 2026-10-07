"""Readable family copy for the bounded Singapore/Hong Kong evidence pass."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/catalog.json';d=json.loads(p.read_text());assert d['completeness_audit']['version']==48
def readable(value):
    if isinstance(value,str):
        if value.startswith(('http','data/','dist/')):return value
        value=re.sub(r'([А-Яа-яЁё])([A-Za-z0-9])',r'\1 \2',value)
        value=re.sub(r'([A-Za-z0-9])([А-Яа-яЁё])',r'\1 \2',value)
        value=re.sub(r'([,;:])(?=[^\s\d/])',r'\1 ',value)
        return value
    if isinstance(value,list):return [readable(v)for v in value]
    if isinstance(value,dict):return {k:(v if k in ['id','entity_id','school_id','iso','source','url','source_urls','event_ids','profile_ids','school_ids','legacy_ids','references','sources'] else readable(v))for k,v in value.items()}
    return value
new_ids=set(d['completeness_audit']['new_ids'])
for i,e in enumerate(d['events']):
    if e['id']in new_ids:d['events'][i]=readable(e)
for i,s in enumerate(d['schools']):
    if s['id']in ['S050','S051']:d['schools'][i]=readable(s)
for i,l in enumerate(d['league_guide']['profiles']):
    if l['id']in d['completeness_audit']['new_profiles']:d['league_guide']['profiles'][i]=readable(l)
for i,r in enumerate(d['school_history']['results']):
    if r['id']in ['H147','H148','H149','H150']:d['school_history']['results'][i]=readable(r)
by={e['id']:e for e in d['events']}
for id in ['C1106','C1107','C1108','C1109','C1110']:
    e=by[id];e['note']='FAQ закрывает регистрацию 31 января 2027 в 10:00 SGT. Старая registration-страница ещё содержит 2025/26: её даты и рождения не применены к BIOGLOW. Дни 24–25 / 27 марта опубликованы для Challenge и Future 8+; дата Explore неизвестна. Homepage указывает 2–5 участников, точный состав согласовать. EN-интервью не подтверждено.'
    e['cost']='$233 за Explore; $220–590 за Challenge / Future 8+ с вариантами kit на non-MOE страницах. Валюту, текущую скидку и полный счёт подтвердить.'
    e['reward']='Overseas Category: Champion, 1st Runner Up, 2nd Runner Up. Зарубежная организация не получает право представлять Сингапур на World Festival.'
    e['deadline_note']='FAQ: 31 Jan 2027, 10am SGT = 02:00 UTC. Срок не гарантирует свободное место.'
    e['city']='Площадка Сингапура и личный слот ещё не объявлены в прочитанных деталях'
    if 'final' in e['title']:e['entry']=e['entry'].replace('прошедший qualifier состав','состав, прошедший qualifier')
for id in ['C1111','C1112','C1113','C1114','C1115']:
    e=by[id];e['note']='Сезон 2026 закончился: соревнования 17–28 августа, награждение 1 сентября. Даты 2027 не объявлены; возрастные правила 2026 не являются гарантированными правилами следующего сезона. Общий список контроллеров расходится с Lower WeDo / Essential: нужен пакет именно выбранной категории.'
    e['period']='Следующий сезон не датирован; последние опубликованные правила — 2026'
    e['priority']='P2 — проверить новый возраст и иностранный допуск'
by['C1111'].update(mat='Нет: старше 6 лет',osc='Условно: сейчас 6; в 2027 исполнится 7, новый возрастной срез обязателен',gear='KUBO; 2–5 детей и максимум 2 наставника.')
by['C1112'].update(mat='Условно: сейчас 9; в 2027 исполнится 10, вероятен переход в Upper по новым правилам',osc='Нет сейчас: 6 ниже минимума 7; возможен будущий Lower после проверки cutoff',gear='SPIKE Essential / WeDo по описанию Lower; 2–3 ученика + coach, робот в кубе 25 см.')
by['C1113'].update(mat='Нет сейчас: 9; в 2027 исполнится 10, новый возрастной срез и класс проверить',osc='Нет: ниже 10 лет',gear='SPIKE Prime / EV3 / Robot Inventor; 2–3 ученика + coach, робот в кубе 25 см.')
for id in ['C1114','C1115']:by[id]['osc']='Нет сейчас: 6 ниже минимума 7; возрастной срез будущего сезона ещё не опубликован'
by['C1114']['gear']='Свободные hardware / software; 2–3 ученика; стенд 2×2 м, инженерный проект и предпринимательская защита.'
by['C1115']['gear']='Свободный робот 25×25 см без ограничения высоты; 2–3 ученика; для Primary требуется минимум платформа блочного кода; AI / ML миссии.'
for id in ['C1116','C1117']:
    e=by[id];e['note']='Сезон 2026 прошёл 8–11 сентября в Singapore Polytechnic. RoboMission Elementary / Junior закрывались по вместимости. Season Quests дают 20% preliminary; формула финала 50/50 описана отдельно. Старые взносы и рождения не перенесены на 2027. Взрослый не должен строить или программировать за ребёнка.'
    e['period']='Сезон 2027, место, иностранный вход и право мировой квалификации пока не подтверждены'
    e['entry']='Команда 2–3 ученика + coach; международный coach — 18+. Один ученик может участвовать только в одной команде, команда — только в одной категории за сезон. Национальный допуск иностранцев и мировая квота требуют отдельного подтверждения.'
for id in ['C1118','C1119','C1120','C1121','C1122','C1123']:
    e=by[id];e['note']='Видео до 5 минут, не ниже 720p. Движение робота от старта до остановки без ускорения или монтажа; вступление можно соединить с этим клипом. Unlisted YouTube или Google Drive по ссылке. Иностранную школьную заявку, документы и английский язык ещё подтвердить. Результаты — февраль 2027, без точного дня. Название WRO HK не доказывает отбор на World Final.'
    e['entry']='Индивидуально: 1 ребёнок + coach; команда: 2–4 ребёнка + coach. Видеоподача с 7 декабря по 24 января. Иностранный приём и EN-подача не подтверждены; опубликован процесс через школу / организацию.'
    e['cost']='HKD 390 за 1 ребёнка + coach; HKD 720 за команду 2–4 + coach.'
    e['reward']='Оценка заданий и LEGO-сертификаты с уровнями. Международный подиум или национальная квота WRO Worlds этим конкурсом не подтверждены.'
    if id=='C1123':e['gear']='SPIKE Prime / EV3; 7 космических миссий за 2 минуты. Старые field kits сняты с продажи.'
    else:e['gear']='WeDo 2.0 / SPIKE Essential / Makerzoid Robot Master. Механический curling не требует программирования.'
by['L445'].update(age='5–7 лет и Grades 1–3 по странице BIOGLOW',osc='Условно: возраст подходит; класс Grade 1–3 и открытый набор не подтверждены',note='Категория описана, но non-MOE список показывает Out of stock. Даты младшего занятия или события не объявлены. Это кандидат учебного маршрута, без подтверждённого места и мировой квоты.',period='BIOGLOW 2026/27; текущий набор и даты Future 5+ неизвестны')
by['L446'].update(title='Cobo Hong Kong · Vibe Coding Hackathon · будущая ступень 12–14',gear='Vibe coding и авторский цифровой проект внутри учебного лагеря. Открытый международный конкурсный протокол и призовой фонд не установлены.',note='Есть четыре общие октябрьские недели, но сочетание этой темы, недели и кампуса не опубликовано. Поэтому конкретные даты hackathon не придуманы. Набор, место и иностранный приём ещё не подтверждены.')
by['E185'].update(title='Industrial Transformation Asia-Pacific 2026',cost='Бесплатный Visitor для industry professionals; Delegate — SGD 100 за конференцию и выставку, тариф 2026.',note='Выпуск 2026: 21–22 октября. Детский / семейный вход не подтверждён. Кнопка регистрации не означает полученный билет или разрешение детям.')
by['E186'].update(title='Industrial Transformation Asia-Pacific 2027',cost='Тариф 2027 не установлен; SGD 100 за Delegate в 2026 не перенесён.',note='20–22 июля 2027 в Marina Bay Sands прямо указаны организатором. Билеты, семейный доступ, программа и список компаний будущего выпуска проверяются отдельно.')
by['E187'].update(title='GITEX AI ASIA 2027',visitor_policy_note='Строго старше 18 лет; только trade and business professionals.',note='Организатор прямо ограничивает выставку посетителями старше 18 лет. Полезен отдельный взрослый маршрут; дети 6 / 9 не включены в семейный календарь.')
by['E078']['note']=by['E078']['note'].split(' Перепроверено')[0]+' Перепроверено: 24 октября–1 ноября 2026. Выходные 10:00–18:00, будни 10:00–17:00. Семейный формат подтверждён; язык, возраст и квоту каждого мастер-класса проверить отдельно.'
by['E078']['exhibitor_note']='Полный список компаний не проверен; около 150 мастер-классов не означает 150 производителей роботов.'

f=d['asia_english_focus'];cs={c['iso']:c for c in f['countries']}
f['season_kicker']='2026 / 2027 · ЛАГЕРЯ, ВИДЕОКОНКУРС И ПОЕЗДКИ'
f['conclusion']='Я бы начал с короткой английской пробы Worklab или Cobo: у обоих детей есть отдельные возрастные группы. Для сезонных наград сначала выяснить классы: Singapore Challenge требует Grade 5, Future 8+ — Grade 4; Hong Kong Winter Challenge привязан к Primary 3 / 6. Переезд оценивать после встречи с действующим младшим наставником. Коста-Рика / Мексика остаются приоритетной базой основного маршрута.'
cs['SGP'].update(reason='Worklab прямо указывает технические лагеря на английском. FLL разделяет Founders / Future по классам; NRC и WRO имеют разных национальных организаторов.',
    mat='В 9 лет подходят Worklab Junior / Senior / SPIKE и AI после выбора уровня. Singapore Challenge требует Grade 5, Future 8+ — Grade 4. Explore Grades 1–4 может соответствовать классу, но сложность нужно оценить после трёх лет опыта.',
    osc='Worklab Apprentice 4.5–7. FLL Explore 6–10 / Grades 1–4 или Future 5+ / Grades 1–3 после проверки класса. NRC KUBO 5–6 — правило 2026; в 2027 Оскару исполнится 7.',
    camp='20 новых Worklab-смен: четыре октябрьские недели по пять треков. У Computhink сохранены 22 реальные смены ноября / декабря, но технический язык не подтверждён. Дневное обучение, жильё семьи отдельно.',
    school='SAS: английская Elementary STEAM с kindergarten, затем VEX IQ / FRC / VEX V5 / MATE ROV. Досье Horizon и Rulang сохранены; приём в местную публичную школу — отдельное условие. Мировое лидерство младшей команды SAS не установлено.',
    city_route='Forum / Orchard для AI и Apprentice; UE Square / Coronation для робототехники. SAS в Woodlands для школьного визита. Выбрать конкретный кампус и слот.',
    budget='Worklab: базовые 3 дня Apprentice $449, Junior / Senior $499; 4 дня SPIKE $500, 3 дня AI $425. Валюту и полный счёт подтвердить. Годовой счёт SAS 2026/27 не извлечён.',
    results_check='FLL 2025/26 отдельно награждает школы, частные центры и Overseas. SOR CIRCUIT SHREDDER — WRO Singapore Elementary Champion 2026; школа не установлена. Эти победы не являются мировыми титулами.')
cs['HKG'].update(reason='Cobo прямо пишет Medium of Instruction: English для лагерей Junior 6–8 / Senior 9–11. Winter Challenge допускает индивидуальную видеоподачу; InnoCarnival — бесплатный семейный фестиваль.',
    mat='Cobo Senior 9–11. Winter Lower требует Primary 3 или ниже; Upper Space — Primary 6 или ниже с уточнением нижней ступени. Иностранный школьный эквивалент и допуск семьи неизвестны.',
    osc='Cobo Junior 6–8 подходит по возрасту. Winter Lower зависит от класса и школьного документа. Поступление в Grade 1 AIS не означает место в опубликованной команде Grades 2–4.',
    camp='Cobo: 5–9 / 12–16 / 20–23 / 26–30 октября, слот 10:00–12:00 или 14:00–16:00. Vibe Coding Hackathon для 12–14 — будущая ступень; конкретная тематическая неделя не установлена.',
    school='AIS: American curriculum на английском, Elementary Grades 1–4, VEX GO для Grades 2–4. AIS14 имеет региональные награды Guangzhou 2026. Школе не приписан мировой чемпионский титул.',
    city_route='Wan Chai для Cobo; отдельные Kowloon Tong классы по запросу и AIS. Science Park для InnoCarnival. Winter Challenge — видео из дома, поездка не требуется.',
    budget='Cobo: HKD 4500 за 5 дней или 3600 за 4 дня, по два часа в день. Winter: HKD 390 solo / 720 команда. Опубликованные AIS fees относятся к 2025/26; текущий полный счёт неизвестен.',
    results_check='AIS14: региональные Excellence Award и Skills №1. AIS13: внутрешкольный Champion 10 июня 2026. Сертификаты Winter не являются подтверждённым международным подиумом.',
    risk='Иностранный школьный эквивалент, английская подача Winter, места Cobo / AIS и возраст / язык конкретного мастер-класса ещё не подтверждены.')
f['limitations']='Частичный проход двух направлений. Карточки недель и дисциплин не равны числу независимых фестивалей. Полный местный и мировой охват не завершён. HKTDC InnoEx / Electronics не отдали доступное тело страницы: новые даты и детские правила по ним не придуманы.'
pick_copy=[
 ('Оскару Apprentice, Матвею Senior или SPIKE. Технический английский прямо подтверждён.', 'Перед записью: уровень, день рождения, кампус, приём visiting family и свободное место. Это учебная проба.'),
 ('Explore для младших. Матвей входит в Challenge / Future 8+ только при подходящем школьном классе.', 'Overseas Category имеет свои местные награды, но не даёт право представлять Сингапур на World Festival.'),
 ('STEAM начинается в Elementary; дальше описан путь VEX IQ / FRC / ROV в английской учебной среде.', 'Проверить младшую команду, наставника, assessment / EAL, места обоим и полный текущий счёт.'),
 ('Оба имеют возрастные группы 6–8 / 9–11 и темы роботов, игр и AI на английском.', 'По два часа в день; тему, неделю и кампус подтвердить. Hackathon 12–14 пока рано.'),
 ('Можно заявить одного ребёнка с coach или команду 2–4. Для видеоподачи ехать не нужно.', 'Зарубежные классы и английский не подтверждены. Награды — LEGO-сертификаты с уровнями; World Final не обещан.'),
 ('Школа подтверждает англоязычное Elementary и региональные награды своей команды Grades 2–4.', 'Текущие места, младший coach и fees неизвестны; региональный школьный отчёт не является мировым протоколом.')]
for pick,(why,gate)in zip(f['family_picks'],pick_copy):pick.update(why=why,gate=gate)
stop_copy=[
 'Worklab: четыре недели по пять треков, базовые 3 / 4 дня. Cobo: четыре недели, 20–23 октября — четыре дня. Отдельная группа каждому ребёнку.',
 'Science Park, все активности объявлены бесплатными. Возраст, язык и запись конкретного мастер-класса проверить.',
 'Lower: Primary 3 или ниже; Upper: Primary 6 или ниже. Solo: 1 + coach; команда: 2–4 + coach. Иностранный приём и EN ещё неизвестны.',
 'Challenge: Grades 5–10; Future 8+: Grades 4–10. FAQ закрывает регистрацию 31 января в 10:00 SGT. Overseas без Singapore World Festival квоты.']
for stop,detail in zip(f['season_stops'],stop_copy):stop['detail']=detail
ev_copy=[
 ('BIOGLOW Founders / Future имеют разные наборы и Grades. FAQ ограничивает международный путь Overseas-команды.', 'Рождения и даты старого registration 2025/26 не применены к новому BIOGLOW.'),
 ('NRC Science Centre имеет KUBO / Lower / Upper / Open / AI. Национальный WRO Singapore теперь у Space Faculty.', 'Правила и даты 2026 не являются будущим сезоном. В 2027 детям исполнится 7 / 10: категории могут измениться.'),
 ('VEX GO Guangzhou 2026: AIS14 получил Excellence Award и первое место Driving / Autonomous Skills. AIS13 победил во внутреннем турнире AIS.', 'Разные категории и уровни, источник — школьный отчёт. Мировая победа не приписана.'),
 ('Kindergarten — robotics / coding; Grade 2 — океанские cleanup robots; Grade 3 — delivery robots. Middle School — VEX IQ, High School — FRC / VEX V5 / MATE ROV.', 'Достижения старших не перенесены на Elementary. Граница EAL в двух школьных страницах неоднозначна.'),
 ('Worklab и Cobo прямо указывают English instruction. Computhink публикует реальные смены без прямого языка технических занятий.', '22 смены Computhink сохранены, но фильтр подтверждённого EN-преподавания их не включает.'),
 ('InnoCarnival семейный; у ITAP детское правило неизвестно; GITEX AI Asia строго для посетителей старше 18.', 'GITEX — взрослый маршрут. Нынешние HKTDC правила в этом проходе не удалось прочитать.')]
for row,(detail,limit)in zip(f['evidence_cards'],ev_copy):row.update(detail=detail,limit=limit)
f['shortlist'][0]['detail']='Одна учебная неделя с отдельными задачами обоим и проверкой наставника. Для опытных детей оценивать собственный код, механику и документацию.'
f['shortlist'][1]['detail']='Сначала класс, дата рождения, иностранный допуск и язык; затем заявка конкретного сезона. Финал требует квалификации и места в команде.'
steps=[
 'Сопоставить точные даты рождения и фактические классы с FLL Grades и Hong Kong Primary 3 / 6. Возраст сам по себе не определяет класс.',
 'Пробный проект; действующий coach, код команды, частота тренировок, места обоим, самостоятельный детский код и организаторские протоколы результатов.',
 'Overseas-награда и международная квота различаются. WRO и NRC самостоятельны; Winter-сертификат не World Final. Сохранить основной национальный маршрут.',
 'Полный школьный счёт, длительность дневного лагеря, жильё семьи, технический язык, питание / трансфер и правила выставки подтвердить до записи.']
for row,detail in zip(f['steps'],steps):row['detail']=detail
for s in d['schools']:
    if s['id']=='S050':
        s.update(programme='Elementary Grades 1–4 с STEAM specialist. VEX GO команда Grades 2–4 участвовала в Guangzhou 2026. Роботокоманду для Grade 1 проверить отдельно.',language_note='English educational programme подтверждена прямо. Mandarin обязателен Early Childhood–Grade 8; Spanish только в High School, это не язык Primary STEM.',
          admissions='Grade 1–12: assessment английского и математики; overseas online assessment предусмотрено. Сайт принимает 2027/28 и 2028/29, текущие места 2026/27 ограничены.',
          cost='Прочитанная таблица явно 2025/26: Grades 1–4 HKD 152800 в год; levy первого ребёнка 12000, второго 8000. Полный тариф 2026/27 не установлен; это старый ориентир, не бюджет переезда.')
    if s['id']=='S051':
        s.update(programme='Elementary STEAM K–5: kindergarten robotics / coding, Grade 2 cleanup robots, Grade 3 delivery robots, Grade 5 сенсоры и cleanup robots. Затем Middle School VEX IQ, High School FRC / VEX V5 / MATE ROV.',
          labs='Школа описывает 2026/27: пять science / engineering labs, четыре STEAM teachers, три assistants. Это оборудование и штат, не результат мирового рейтинга.',
          language_note='Школьное обучение на EN. В Elementary ежедневно изучают Chinese или Spanish как языковой предмет; STEM на испанском этим не подтверждён. EAL — по assessment.',
          admissions='Возрастной срез 1 сентября; для Grade 1 требуется 6 лет. Подробная EAL-страница: Grade 3 — Intermediate / Transition, Grades 4–5 — Transition. Общая language policy неоднозначна по EAL после Grade 4; профиль нового ученика согласовать.',
          cost='На fees-странице указана таблица 2026/27 PDF; её суммы в этом проходе не извлечены. Tuition, development, EAL и extracurricular требуют полного текущего счёта.')
    if s['id']in ['S050','S051']:
        s['questions']=['Какой класс и языковое assessment получит каждый ребёнок?','Кто действующий младший coach, код команды, часы тренировок и есть ли место обоим?','Какие organizer protocols за последние 3–5 сезонов и условия международной квоты?','Какой полный нынешний годовой счёт и стоимость EAL / extracurricular?']
        for r in s['results']:
            r.setdefault('team','AIS14' if 'Guangzhou' in r['stage'] else 'AIS13')
            r.setdefault('limit','Школьный отчёт; региональный или внутришкольный уровень, не мировой титул.')
        s['verification']='Прочитаны школьные первичные источники. Место, нынешний наставник и мировой результат младших требуют дополнительного подтверждения.'
for profile in d['league_guide']['profiles']:
    if profile['id']in d['completeness_audit']['new_profiles']:
        profile['evidence']='Прочитаны первичные страницы и указанные разделы PDF. Неизвестные условия допуска и следующего сезона отмечены.'
        profile['nuances']=[readable(n)for n in profile['nuances']]
    if profile['id']=='fll-singapore-bioglow':
        profile['summary']='Для Матвея возраст недостаточен: Challenge требует Grade 5, Future 8+ — Grade 4. Оскару Explore / Future 5+ после проверки класса. Зарубежной организации только Overseas Category, без Singapore World Festival квоты.'
        profile['route']='Класс и редакция → местная или Overseas команда → qualifier → final → World Festival только по отдельной разрешённой национальной квоте.'
        profile['nuances'][1]='Старая registration 2025/26 не задаёт новые рождения. Дата Explore не выведена из даты Challenge.'
        profile['nuances'][2]='FAQ: early bird 31.12.2026 в 22:00 SGT; регистрация 31.01.2027 в 10:00 SGT. Места ограничены.'
    if profile['id']=='nrc-singapore':
        profile['summary']='Младшая практика, AI и инженерные проекты; сезон 2026 закончился. В 2027 Оскару исполнится 7, Матвею 10 — нужно заново проверить KUBO / Lower / Upper.'
        profile['route']='Школьная ступень и возраст → разрешённая частная / школьная команда → пакет категории → NRC. Национальный WRO идёт отдельно через Space Faculty.'
        profile['nuances']=['International school не означает любой зарубежный family team.','Lower WeDo / Essential расходится с общим списком контроллеров: пакет конкретной категории обязателен.','Архивная таблица наград 2023 на Duck Learning не является результатами 2026.']
    if profile['id']=='wro-singapore-spacefaculty':
        profile['summary']='Матвею Elementary по возрасту, Оскару пока рано. Space Faculty — отдельный национальный WRO-организатор. Даты 2027 и иностранная мировая квота неизвестны.'
        profile['route']='Наставник → национальный / иностранный допуск → самостоятельный робот → национальный результат → World Final по подтверждённой квоте.'
        profile['nuances']=['Не solo: 2–3 ребёнка. Международный coach 18+, один ученик в одной команде за сезон.','2026 прошёл 8–11 сентября; старые взносы SGD 149 / 249 / 599 не являются ценами 2027.','Season Quests 20% относятся к preliminary, а не ко всему финальному результату.']
    if profile['id']=='hongkong-winter-robot':
        profile['summary']='Дистанционный зимний конкурс со школьными категориями. Индивидуальный вход возможен; награды — LEGO-сертификаты с уровнями. Иностранный класс, английский и WRO World Final квота не подтверждены.'
        profile['route']='Подтвердить класс, иностранный вход и язык → выбрать миссию → собственный робот → видео до 5 минут → оценка в феврале 2027, точный день неизвестен.'
        profile['nuances']=['WRO HK название не означает квалификацию World Final.','Окно видеоподачи не является многодневной очной поездкой.','Mechanical curling без программирования; цветовая классификация не доказанная AI / ML задача.']
for e in d['school_history']['entities']:
    if e['id']=='AIS-HK':e['note']='Младшие Grades 2–4, VEX GO. Региональные и внутришкольные результаты не являются мировым VEX IQ титулом.'
    if e['id']=='SG-WRO-SOR-CIRCUIT':e['note']='WRO Singapore 2026 Elementary Champion по организатору. Школа / академия не определена по префиксу SOR.'
for r in d['school_history']['results']:
    if r['id']=='H147':r['note']='Школьный отчёт от 8 июня 2026. Комплексная региональная награда; не VEX IQ или WRO World Champion.'
    if r['id']=='H148':r['note']='Первое место технической региональной категории; не общий мировой титул.'
    if r['id']=='H149':r['note']='16 команд, 48 учеников одной школы. 31 очко qualifier дали ничью; champion определён playoff с 14 очками.'
    if r['id']=='H150':r['note']='Национальный champion по организатору. Школа, иностранная квота и результат World Final не установлены.'
d['completeness_audit']['conclusion']='43 новые карточки: 18 дисциплин / этапов, 22 учебные смены / программы и 3 выставки. Две школы, четыре результата с точными уровнями. Мировой охват остаётся частичным.'
d['camp_focus']['conclusion']='446 учебных карточек. Worklab: 20 реальных октябрьских смен на английском; Cobo прямо подтверждает EN. Future 5+ и hackathon 12–14 — отдельные кандидаты без дат. Технический язык Computhink неизвестен.'
d['school_focus']['conclusion']='51 школьное досье. AIS Hong Kong имеет региональные и внутришкольные результаты VEX GO; SAS — Elementary STEAM и дальнейший соревновательный маршрут. Новые младшие мировые титулы не приписаны.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Polished Singapore/Hong Kong family copy without changing dates or unrelated records.')
