"""CHE/ESP/FRA: public season dates, family access, language conflicts and school alternatives."""
import ast
import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('/Users/pal/.codex/workspaces/stem-family-atlas-work')
CHECKED = '2026-10-02'
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert len(d['events']) == 1666 and d['completeness_audit']['version'] == 44
urls = json.loads((WORK / 'urls-europe-calendar-v45.json').read_text())
byid = {e['id']: e for e in d['events']}
new = []
tree = ast.parse((ROOT / 'scripts/expand-oceania-v29.py').read_text())
for name in ['ref', 'event']:
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'event_helpers', 'exec'))
base_event = event


def event(*args, **kwargs):
    e = base_event(*args, **kwargs)
    e['region'] = 'Европа'
    return e


# Read the public JOIN list in an anonymous browser; no coach login or application.
# Month/day + explicitly labelled 2026/27 season establishes the year; no home placeholder becomes a tournament.
rows = json.loads((WORK / 'hot-swiss-v45.json').read_text())
swiss_ids = []
swiss_days = {'NOV': (2026, 11), 'DEZ': (2026, 12), 'JAN': (2027, 1), 'MÄR': (2027, 3)}
for row in rows:
    parts = row['text'].splitlines()
    if len(parts) != 7:
        continue
    _, day, month, city, country, registered, division = parts
    if city.startswith(('Zu Hause', 'Zuhause')):
        continue
    assert country == 'CH'
    year, number = swiss_days[month]
    date = dt.date(year, number, int(day)).isoformat()
    i = f'C{1089 + len(swiss_ids):03d}'
    full = registered.split(' Teams')[0].split(' / ')
    full = full[0] == full[1]
    age = {'Explore': 'FAQ 6–9; division 6–10. Верхнюю границу и возрастной срез подтвердить',
           'Challenge': '9–16 лет; контрольную дату сезона подтвердить',
           'Future 8+': '8–16; Grades 4–10; команда 4–8, группа 8 / 16 / 24'}[division]
    mat = ('Условно: возраст / класс и язык защиты подтвердить' if division != 'Explore' else
           'Условно: в 2027 исполняется 10; противоречие Explore 6–9 / 6–10 ещё не разрешено')
    osc = ('Условно: 6/7 лет; язык и место подтвердить' if division == 'Explore' else
           'Нет: ниже опубликованного минимального возраста')
    if full:
        mat = 'Мест нет по снимку JOIN 02.10.2026; ждать подтверждённого изменения'
        if division == 'Explore':
            osc = mat
    gear = ('LEGO Computer Science & AI 8+ / 11+: два комплекта; минимум четыре участника' if division == 'Future 8+' else
            'Founders: модель, плакат, SPIKE Essential / WeDo 2.0' if division == 'Explore' else
            'Founders: автономный LEGO-робот, Innovation Project, Robot Design, Core Values')
    e = event(i, f'FLL Switzerland · {city} · {division} · BIOGLOW 2026/27', 'Швейцария', city,
              row['url'], age, mat, osc,
              'Регистрация в JOIN у выбранной площадки. Иностранная команда может участвовать; '
              'продвижение Challenge / Future возможно только через страну команды. Место семьи не подтверждено.',
              gear, start=date, end=date, scope='regional', date_scope='event',
              priority='P4 — лимит заполнен на дату проверки' if full else 'P2 — после подтверждения языка и допуска',
              language='По FAQ — официальный язык страны / региона; EN / ES интервью согласовать с площадкой.',
              note=f'В публичном списке JOIN на 02.10.2026: {registered}. Это число записанных команд / лимит, '
                   'а не подтверждение доступного места семье. Год определён по сезону 2026/27 и месяцу в списке. '
                   'Explore — оценка и признание проекта каждой команды, без общего турнирного победителя. '
                   'At Home и ошибочные даты 1970 не использованы как очные события.',
              cost='Explore: опубликовано EUR199 + CH shipping42; набор и поездка отдельно.' if division == 'Explore' else
                   'Взнос выбранной редакции и поездка отдельно; счёт площадки подтвердить')
    if division == 'Explore':
        e['reward'] = 'Признание модели и команды; не рейтинговая победа и не мировой отбор'
        e['deadline'] = (dt.date.fromisoformat(date) - dt.timedelta(days=28)).isoformat()
        e['deadline_note'] = 'Рассчитано: четыре недели до выставки по division Explore; места могут закончиться раньше. Час не объявлен.'
        e['deadline_label'] = 'Расчётный последний день Explore при свободных местах'
    else:
        e['deadline'] = '2026-10-31'
        e['deadline_note'] = 'Срок сезонной регистрации; наличие места и час закрытия отдельно.'
    e['references'] = [ref('Публичный список BIOGLOW 2026/27', urls['hot_join']),
                       ref('Иностранные команды / язык / размеры команд', urls['hot_faq']),
                       ref('Редакция и возраст', urls['hot_explore'] if division == 'Explore' else
                           urls['hot_8'] if division == 'Future 8+' else byid['C909']['source'])]
    e['registration_status'] = ('Лимит площадки заполнен на снимке 02.10.2026; это не окончательный отказ организатора.'
                                if full else 'В списке есть незаполненный лимит на 02.10.2026; актуальное место не подтверждено.')
    e['level'] = 'Региональный этап международной лиги' if division != 'Explore' else 'Региональная проектная выставка лиги'
    swiss_ids.append(i)
assert len(swiss_ids) == 12

e = event('C1101', 'FLL Spain · Jaén · региональный BIOGLOW 2027', 'Испания',
          'Jaén · Universidad de Jaén, Campus de Las Lagunillas', urls['jaen'],
          'Поток в анонсе не указан; национальные Founders: Challenge10–16 / Explore6–9. Не переносить K8 на Jaén.',
          'Условно: в 2027 исполняется 10; редакцию, возрастной срез и допуск подтвердить',
          'Только если площадка подтвердит Explore; анонс не доказывает младший поток',
          'Анонс адресован образовательным центрам Jaén / provincia. Независимая группа разрешена национальной '
          'регистрацией, но foreign / независимый вход именно в Jaén не установлен.',
          'Робот, Innovation Project и командная работа; набор после выбора редакции', start='2027-02-20', scope='regional',
          note='Поле UJA «начало 29.09.2026» обозначает окно анонса, не месяцы турнира. Текст прямо называет один день '
               '20 февраля 2027. Возраст / редакция конкретной площадки пока не указаны.', date_scope='event')
e['references'] = [ref('Национальная регистрация: редакции / возраст / независимые группы', urls['es_registration'])]

e = event('C1102', 'FLL France · Nouvelle-Aquitaine · Le Lab · BIOGLOW 2027', 'Франция',
          'Nouvelle-Aquitaine · точное место региональной встречи уточнить', urls['fr_lab'], 'Challenge9–16 по организатору',
          'Условно: возрастной диапазон подходит; язык, класс и команда отдельно', 'Нет: младше Challenge9',
          'Через Le Lab / местного партнёра; подтвердить точную площадку, возрастной срез и EN / ES защиту.',
          'LEGO SPIKE / проект BIOGLOW; редакцию этапа подтвердить', start='2027-02-07', scope='regional',
          note='Текущая форма членства 2026/27 прямо объявляет региональную встречу 7 февраля 2027. '
               'Членство в клубе не является регистрацией в турнире и не гарантирует состав команды.', date_scope='event')
e['references'] = [ref('Клуб и возраст Challenge', urls['fr_lab_info'])]
e = event('C1103', 'FLL France · Nantes · Finale Régionale Ouest 2027', 'Франция',
          'Nantes · École Polytech, Campus de la Chantrerie', urls['fr_botfest'], 'Локальная программа11–16; национальный FAQ9–16',
          'Нет по опубликованной местной границе11; в 2027 исполняется10', 'Нет: младше11',
          'Местный состав / региональные условия; разницу11–16 против общих9–16 уточнить, исключение не обещано.',
          'FLL BIOGLOW; три команды по локальному анонсу проходят на национальный фестиваль', start='2027-02-13',
          scope='regional', priority='P4 — младше опубликованной местной границы',
          note='Программа организатора предварительная. Семейный вход E179 отдельный и открыт всем; '
               'посещение не является допуском в соревновательную команду.', date_scope='event')
e['references'] = [ref('Посещение и возрастные условия', urls['fr_botfest_info']), ref('Национальные условия9–16', urls['fr_faq'])]
e = event('C1104', 'FLL France · Festival National 2027 · Futuroscope', 'Франция',
          'Poitiers / Chasseneuil-du-Poitou · Palais des Congrès du Futuroscope', urls['fr_festival'],
          '9–16 по FAQ фестиваля; финальный регламент потока отдельно',
          'Условно: возраст подходит; нужно пройти региональный отбор', 'Нет для Challenge; семейное посещение E180',
          'Национальный фестиваль для команд, квалифицировавшихся на региональных этапах. '
          'Прямая иностранная заявка и мировая квота не подтверждены.',
          'BIOGLOW: Robot Game, Innovation Project, Robot Design и Core Values; редакция по правилам команды',
          start='2027-03-26', end='2027-03-28', scope='national', date_scope='festival_window',
          note='Пятница — установка / открытие; основное судейство и матчи27–28 марта по предварительному плану. '
               'Старая национальная страница всё ещё описывает Mulhouse2026; для2027 использован новый официальный сайт фестиваля.')
e['admission_kind'] = 'qualifier'
e['related_ids'] = ['E180', 'C1102', 'C1103']
e['references'] = [ref('Квалификация и9–16', urls['fr_faq']), ref('Предварительный план27–28марта', urls['fr_planning'])]


def learning(i, title, country, city, source, age, mat, osc, gear, note, start='', end='', cost='Стоимость конкретной группы уточнить'):
    return event(i, title, country, city, source, age, mat, osc,
                 'Подтвердить группу, уровень после трёх лет опыта, язык техники, место и возрастной срез до записи.',
                 gear, block='Лагеря', participation='day_camp', start=start, end=end, note=note, cost=cost,
                 date_scope='camp_window', priority='P4 — язык / возраст / новая смена требуют подтверждения')

e = learning('L402', 'LIFE Summer Tech · Tres Cantos · кандидат будущего набора', 'Испания', 'Tres Cantos · Madrid',
             urls['life_camp'], 'Последний опубликованный набор2026:10–14',
             'Будущая ступень после10-летия; дат2027нет', 'Нет: минимум10 в последнем наборе',
             'VEX EXP STEM Labs: механика, автономный код, лабиринт и инженерные задачи',
             'Лето2026завершено:22июня–10июля, три недельные смены. Робототехника прямо на английском, '
             'принимали внешкольных детей. Это обучение VEX EXP, не VEX IQ / V5 рейтинговый турнир; '
             'внутренний Robot Challenge не мировая квалификация. Новые смены2027не объявлены.',
             cost='Архив2026:EUR280/неделя, питание и бассейн;2027цену не переносить')
e.update(language='Робототехническая программа2026прямо на английском; новый поток2027подтвердить',
         languages=['EN'], language_mode='primary', evidence_level='historical_program',
         language_certainty='Язык последнего конкретного лагеря подтверждён; будущая смена ещё не объявлена.',
         period='Следующий набор не объявлен; архив2026только для планирования',
         priority='P4 — Матвею после10-летия и объявления нового набора', related_school_ids=['S045'])
for i, start, end in [('L403', '2026-10-19', '2026-10-23'), ('L404', '2026-10-26', '2026-10-30')]:
    e = learning(i, 'LMO Lyon · Thymio / Arduino / AI · '+start, 'Франция',
                 'Lyon5 ·26 rue du Commandant Charcot', urls['lmo_camp'], 'От CE1 до14лет; класс отдельно от рождения',
                 'Условно: нужен CE1+ и понятный технический язык',
                 'Не установлен: CE1 обычно следующая ступень; текущий класс неизвестен',
                 'Scratch3, Thymio, Arduino Uno, 3Dмоделирование и AI',
                 'Для повторных участников неделя2углубляет программы / робота / 3D. '
                 'Актуальная страница не подтверждает техническое EN / ES. График9:00–17:30на сайте — '
                 'контактные часы школы, не доказанное расписание лагеря. Цена годовой школы не использована как цена смены.',
                 start=start, end=end)
    if i == 'L404':
        e['note'] += (' В строке недели2указано«среда30октября», но30.10.2026—пятница. '
                     'Использовано опубликованное окно26–30; ежедневное расписание и опечатку подтвердить.')
    e['language'] = 'EN / ES / RU технических занятий не подтверждены'
    e['references'] = [ref('Программа2026/27и CE1', urls['lmo_general'])]
e = learning('L405', 'Le Lab Saint-Gervais · регулярная робототехника / FLL', 'Франция',
             'Saint-Gervais · Gironde, Nouvelle-Aquitaine; точную площадку подтвердить', urls['fr_lab'],
             'Членство«старше6»; Explore6–9 / Challenge9–16',
             'Условно: Challengeпо возрасту; технический язык и команда отдельно',
             'Граница«старше6» против Explore6–9; шестилетний вход уточнить',
             'Scratch, LEGO SPIKE, Makeblock, Minecraft Education, mBot, Arduino',
             'Субботы10:00–12:00вне каникул. Участвуют в FLL; RoboCupв марте/мае2027без точных дней, '
             'WROмаршрут«подробнее позже». EN / ES преподавание не установлено. '
             'Членство, взнос команды и квалификация — отдельные условия.',
             cost='2026/27:EUR60первому,45второму, parent accompagnateur5. Условно110за двух+одного родителя; '
                  'оборудование, турниры, поездки и обязательность parent fee уточнить.')
e.update(participation='regular', format='Регулярный клуб; жильё семьи отдельно', date_scope='season_window',
         period='Членство01.06.2026–31.05.2027; субботний слот и место подтвердить',
         related_ids=['C1102', 'C1104'], language='EN / ES / RU техники и защиты не подтверждены')
e['references'] = [ref('Challengeи местный клуб', urls['fr_lab_info'])]
e = learning('L406', 'Devoxx4Kids · Bot Fest Nantes2027 · детский workshop', 'Франция',
             'Nantes · École Polytech', urls['fr_botfest_info'], '8–12лет',
             'Условно: возраст подходит; EN / ES занятие и место отдельно', 'Нет: минимум8',
             'Введение в программирование; конкретную тему и сложность уточнить',
             'Бесплатный workshop, запись объявлена с20ноября2026. Время слота и технический язык не опубликованы; '
             'общие часы фестиваля10:00–16:30не перенесены на длительность занятия.', start='2027-02-13', end='2027-02-13',
             cost='Бесплатно по программе; запись обязательна, место не подтверждено')
e.update(date_scope='event', participation='holiday_workshop', format='Отдельный workshop по записи; не недельный лагерь',
         themes=['coding','games'], related_ids=['E179'], registration_opens='2026-11-20',
         language='EN / ES технического workshop не подтверждены')

for i, title, city, source, start, end, age, mat, osc, note, related in [
    ('E179', 'Bot Fest Nantes2027 · семейный робототехнический фестиваль',
     'Nantes · École Polytech, Rue Christian Pauc', urls['fr_botfest_info'], '2027-02-13', '2027-02-13',
     'Фестиваль все возраста; Devoxx8–12, FLL11–16, SumoBot16+',
     'Да для семейного просмотра; Devoxx8–12после подтверждения языка и записи',
     'Да для семейной программы; Devoxx8+и FLL11+не подходят',
     '10:00–16:30предварительно. Бесплатные соревнования и демонстрации; запись нужна на отдельные workshops. '
     'Мировой масштаб промышленной выставки не заявлен.', ['C1103','L406']),
    ('E180', 'FLL France2027 · Futuroscope · бесплатное семейное посещение',
     'Poitiers / Chasseneuil-du-Poitou · Palais des Congrès du Futuroscope', urls['fr_faq'],
     '2027-03-26', '2027-03-28', 'Публичная семейная программа; возраст отдельного workshop уточнить',
     'Да для семейного просмотра; участие в Challengeтолько по отбору',
     'Да для семейного просмотра; это не соревновательный допуск',
     'FAQпрямо подтверждает бесплатный семейный вход. Матчи и судейство преимущественно27–28марта. '
     'Отдельный билет в парк Futuroscope, проживание и отдельные активности этим не включены.', ['C1104']),
]:
    e = event(i, title, 'Франция', city, source, age, mat, osc,
              'Посещение с родителем; возраст / язык и запись на выбранный workshop отдельно.',
              'Роботоматчи, инженерные проекты, демонстрации и программирование', block='События',
              participation='visitor', start=start, end=end, priority='P2 — семейный визит',
              cost='Публичный вход бесплатный; поездка / проживание и extras отдельно', note=note)
    e.update(exhibition_tier='family_alternative', visitor_policy='family', related_ids=related,
             visitor_policy_note='Семейный / публичный вход прямо заявлен; отдельное занятие по своим условиям.',
             adult_entry='Родитель / сопровождающий; часы и отдельную активность сверить.',
             highlights=['Матчи роботов','Проекты команд','Детские демонстрации / workshops'],
             exhibitor_note='Образовательный фестиваль; присутствие всех мировых компаний не заявлено.',
             exhibitor_directory_url=urls['fr_botfest'] if i=='E179' else urls['fr_spaces'])
    e['references'] = [ref('Программа', urls['fr_botfest'] if i=='E179' else urls['fr_planning'])]

assert len(new) == 23
d['events'] += new

# Refine earlier records; conflicts remain explicit rather than silently choosing one source.
e = byid['C906']; e.update(checked=CHECKED, languages=['DE','FR','IT'],
    language='Starterкурсы и конкурс на языке соответствующего региона по организатору; EN / ES поток не подтверждён.',
    language_certainty='Региональный язык прямо указан; конкретный иной язык должен подтвердить организатор.')
e['note'] += (' Страница2026прямо указывает язык региона; франкоязычных workshopsв2026не было. '
             'На2027это отсутствие не перенесено. Для трёхлетнего опыта есть возможность пропустить вводные '
             'два workshopи идти в два конкурсных, но только после согласования и нового набора.')
e = byid['C972']; e.update(checked=CHECKED, city='Chur ·28ноября2026есть в JOIN; другие Swiss Futureплощадки не установлены')
e['entry'] = ('Группа8/16/24; конкурсная команда4–8, все входят в зарегистрированную группу. '
             'Два брата не образуют достаточную Future8+команду. Иностранные участвуют без продвижения через чужую страну.')
e['note'] = e['note'].replace('Швейцарские даты в JOIN ещё не получены.', 'Получен JOIN: Chur28ноября2026, C1089.')
e['related_ids'] = ['C1089']
e = byid['L278']; e.update(checked=CHECKED,
    gear='CS & AI5+: divisionпишет1на4детей, FAQпишет2на4. Покупку и состав комплекта подтвердить; SPIKEне совместим.')
e['entry'] = ('Группа до24, команды до4. Division2026/27пишет«нет официальных событий», '
             'FAQожидает«несколько или ни одного». Конкретная Future5+дата в Швейцарии не найдена.')
e['references'].append(ref('FAQ: расходится по hardwareи числу будущих событий', urls['hot_faq']))
e['note'] += ' Противоречие1 /2CS&AI5+комплекта на4детей не разрешено. Не выдавать педагогическое season setза robot hardware.'
e = byid['C916']; e.update(checked=CHECKED,
    entry='Текущая регистрация через французского партнёра; региональный отбор→Festival National26–28марта2027. '
          'Для национального участия нужна квалификация; EN / ES интервью и иностранная мировая квота не установлены.',
    related_ids=['C1102','C1103','C1104','E180'])
e['note'] += ' Национальный FAQ2027указывает9–16; локальный Nantes11–16строже, его границу не отменять общим диапазоном.'
e['references'].append(ref('Национальный фестиваль2027и отбор', urls['fr_faq']))

# Two actual school alternatives, with no invented competitive record.
life = dict(id='S045', name='LIFE International School · Tres Cantos', iso='ESP', country='Испания', region='Европа',
    city='Tres Cantos · Ronda de Poniente3, Madrid', school_type='private',
    curriculum='Американская программа; ElementaryGrades1–6. Христианская модель, Bible Literacyи Valuesв учебном плане.',
    ib_programmes=[], ages='EarlyChildhood3–5; ElementaryGrades1–6; Secondary7–12', instruction_languages=['EN','ES'],
    language_note='Primary: все предметы наEN, кроме SpanishLanguage / Culture. Язык конкретной роботокоманды отдельно.',
    fit=dict(mat='candidate',osc='candidate',note='Обоим школьный класс по assessment; нужный робототехнический состав не установлен.'),
    boarding='unknown', boarding_note='Дневная школа; пансион для младших не установлен.',
    programme='Technologyв Primary; летний VEXEXPнаEN10–14в2026, внешним детям доступен. '
              'EXPSTEMLabs—обучение; действующая VEXIQ / WROкоманда6/9не подтверждена.',
    labs='Точный младший набор, технические часы и самостоятельные проекты нужно получить.',
    ai='Обязательный AIтрек для6/9не подтверждён.', results=[], evidence='programme',
    admissions='Визит / Zoom→tour→onlineapplication. FAQ: разные национальности и убеждения допускаются при понимании '
               'христианской модели; приём по свободным местам. Год рождения не определяет класс автоматически.',
    cost='2026/27: Grades1–3EUR682×10, Grades4–6EUR738×10. Условно за двоих tuitionEUR13640–14200 '
         'при обоих в1–3либо одном в4–6. Первый год +EUR3444за двух(100assessment+825enrolment+565resources+232uniform каждому), '
         'итого17084–17644до питания / кружков / транспорта и дополнительных материалов. Скидки не предположены.',
    questions=['Подходит ли семье христианская образовательная модель?',
               'Как распределят обоих по классам и есть ли места?',
               'Есть ли нынешние WRO / VEXIQteam codes, младший наставник и протоколы трёх сезонов?',
               'Какой полный счёт и доля инженерной работы обоих?'],
    sources=[dict(title=t,url=urls[k],claim=c,kind='school',checked=CHECKED) for t,k,c in [
        ('Primaryи американская программа','life_academic','Grades1–6, EN, Technology, Bible Literacy'),
        ('FAQ','life_faq','EN, разнообразный приём и христианская модель'),
        ('Школьные тарифы2026/27','life_fees','Помещённый тариф; расчёт по двум возможным классам'),
        ('Летний VEXEXP2026','life_camp','EN10–14, программа не турнир'),
        ('Admission','life_admissions','Визит / Zoom, заявка отдельно')]],
    checked=CHECKED,priority=3,research_status='partial',
    verification='Первичные школьные страницы прочитаны; конкурентные результаты и текущая младшая команда не установлены.')
nejapa = dict(id='S046', name='CEIP Ciudad de Nejapa · Tres Cantos', iso='ESP', country='Испания', region='Европа',
    city='Tres Cantos · Labradores26, Madrid', school_type='public', curriculum='Испанская государственная Primary; технология и робототехника в4ºи6º.',
    ib_programmes=[], ages='Infantil / Primaria; нынешний сайт также перечисляет1º /2ºESO, приём по ступени отдельно',
    instruction_languages=['ES','EN','FR'], language_note='Primary:5ENсессий/неделя и Science / Artsпо описанию школы. '
    'Artв4º–6ºнаFR. Язык Tecnología y Robóticaне указан отдельно; Englishbilingualне означает весь деньEN.',
    fit=dict(mat='candidate',osc='candidate',note='Школьная Primaryвозможна обоим по распределению. '
        'Явный roboticsпредмет только4º /6º; Оскару такую младшую команду не обещать.'),
    boarding='unknown',boarding_note='Государственная дневная школа; младший пансион не установлен.',
    programme='Tecnología y Robótica: вычислительное мышление, STEAM, программирование и проекты. '
              'Победы, team codeи фактическая внешкольная младшая команда не найдены.',
    labs='Конкретный набор, лаборатория и часы нужно подтвердить.', ai='Самостоятельный обязательный AIкурс6/9не установлен.',
    results=[],evidence='programme',admissions='Через Secretaríaи официальный местный процесс. '
        'Запись по месту, классу и свободным местам отдельно; visitingfamilyприём не предположен.',
    cost='Текущий полный счёт не установлен; питание, внешкольный клуб и соревнования отдельно. Частные тарифы LIFEне применены.',
    questions=['Какой класс получит каждый и возможен ли текущий приём?',
               'Какой язык / часы roboticsв4ºи6º, что доступно младшим?',
               'Какой внешний наставник сможет вести WROElementary / RoboBasic?',
               'Есть ли реальные текущие team codesи официальные результаты?'],
    sources=[dict(title=t,url=urls[k],claim=c,kind='school',checked=CHECKED) for t,k,c in [
        ('Tecnología y Robótica','nejapa','Предмет в4º /6º, не доказанная чемпионская команда'),
        ('Языки по предметам','nejapa_language','ENи FRне перенесены на все предметы'),
        ('Secretaría','nejapa_admissions','Местный школьный процесс')]],
    checked=CHECKED,priority=3,research_status='partial',verification='Первичные EducaMadridстраницы прочитаны; результатов мирового уровня не найдено.')
d['schools'] += [life, nejapa]

profiles = {p['id']: p for p in d['league_guide']['profiles']}
p = profiles['fll-swiss-junior']; p['checked'] = CHECKED
p['event_ids'] += swiss_ids
p['categories'][0]['hardware'] = 'CS&AI5+: division1 / FAQ2комплекта на4детей; разницу подтвердить'
p['categories'][0]['entry'] = 'Учебная программа; divisionнет / FAQнесколько либо ни одного завершающего события. Swissдата не установлена.'
p['categories'][2]['team'] = 'Конкурсная команда4–8; группа8 /16 /24'
p['language'] = 'Защита и судейство обычно на официальном языке страны / региона; EN / ES согласовать с конкретной площадкой.'
p['nuances'] = [n for n in p['nuances'] if 'JOIN' not in n]
p['nuances'] += ['Получено12очных записей JOINв7площадках сезона2026/27. Два лимита заполнены на02.10.2026.',
    'At Homeне признан очным турниром. Публичная домашняя Challengeкарточка имеет ошибочный1970год; дату не переносить.',
    'FAQи divisionFuture5+расходятся по1 /2hardwareкомплекта; покупку подтвердить.',
    'Подготовка Challengeи Futureв один день не рекомендована оператором: расписания могут перекрываться.']
p['sources'] += [dict(title=t,url=urls[k],checked=CHECKED) for t,k in [('JOINBIOGLOW','hot_join'),('Future5+division','hot_5')]]
p = profiles['fll-europe-three']; p['checked'] = CHECKED
p['summary'] = ('2026/27: SwissChallenge9–16, SpainFounders10–16 / FutureK8с8. Французский FestivalNational9–16 '
               'после регионального отбора; Nantesлокально11–16. Текущие швейцарские региональные даты добавлены.')
p['categories'][-1].update(age='Национальный FAQ9–16; Nantes11–16',age_rule='Локальная граница не отменяется общей',
    entry='Региональный отбор→FestivalNational26–28марта2027; иностранная квота и ENсудейство отдельно')
p['event_ids'] += ['C1101','C1102','C1103','C1104']
p['sources'].append(dict(title='Французский FestivalNational2027FAQ',url=urls['fr_faq'],checked=CHECKED))
p = copy.deepcopy(p); p.update(id='fll-france-2027',name='FIRST LEGO League France · реальные этапы2026/27',
    age_summary='Challenge9–16по национальному FAQ; Nantes11–16. ExploreLeLab6–9.',
    summary='Матвею возможен Challengeв доступном региональном потоке; Nantesпока рано. Оскару Exploreпри местном '
            'возрастном правиле. Оба могут посетить национальный фестиваль бесплатно как семья.',
    categories=[dict(name='Challenge · Le Lab',age='9–16',team='Размер / класс по местному сезонному правилу',hardware='РедакцияFounders / Futureпо регистрации',
        age_rule='Возрастной срез и класс подтвердить',entry='Nouvelle-Aquitaine7февраля2027; затем национальный отбор'),
        dict(name='Challenge · Nantes',age='11–16локально',team='Местный регламент',hardware='BIOGLOW',
        age_rule='Матвею2017в2027исполняется10; нельзя обещать допуск по общему9+',entry='13февраля; заявлены3квоты на национальный этап'),
        dict(name='Национальный Festival',age='9–16по FAQ',team='Только квалифицировавшиеся команды',hardware='Поток по команде',
        age_rule='Локальная квалификация и окончательные правила',entry='26–28марта2027, основная программа27–28'),
        dict(name='Explore · Le Lab',age='6–9',team='Младший состав подтвердить',hardware='SPIKE / учебная модель',
        age_rule='Клуб пишет«старше6», что требует уточнения для Оскара',entry='Учебный путь; точная выставкаExploreне объявлена')],
    event_ids=['C916','C1102','C1103','C1104','L405','E179','E180'],
    route='Конкретный регион / младший наставник→подготовка и язык защиты→региональный результат→национальный отбор '
          'вPoitiers→международная квота только по отдельным условиям.',
    requirements=['Прямая национальная заявка не заменяет региональную квалификацию.',
                  'Nantes11–16строже общегоFAQ9–16; младших не включать по умолчанию.',
                  'Семейное посещение не является соревновательным допуском.'],
    nuances=['Старая национальная страница2026и новый2027festivalне смешаны.',
             'EN / ES техническое судейство и иностранная мировая квота не подтверждены.',
             'Окончательные потоки Founders / Futureи структура после2026/27нуждаются в ежегодной проверке.'],
    strengths='Виден конкретный региональный маршрут и отдельно бесплатная семейная поездка; гарантии результата нет.',
    sources=[dict(title=t,url=urls[k],checked=CHECKED) for t,k in [('Национальная дата','fr_festival'),('NationalFAQ','fr_faq'),
        ('LeLab2026/27','fr_lab'),('NantesProgramme','fr_botfest'),('NantesFamily','fr_botfest_info')]])
d['league_guide']['profiles'].append(p)
d['league_guide'].update(version=45,checked=CHECKED)

f = d['europe_focus']; f.update(version=45,checked=CHECKED,
    limitations='Девятый ограниченный проход:225карточек трёх стран и20школьных досье. '
                'Добавлены12очных SwissFLLкатегорий в7площадках, новые2027этапы, семейные альтернативы '
                'и два школьных варианта. Полные национальные календари, иностранные квоты и мировой рейтинг школ не установлены.')
for c in f['countries']:
    c['event_ids'] += [e['id'] for e in new if e['country'] == c['name']]
    if c['iso'] == 'ESP':
        c['school_ids'] += ['S045','S046']
        c['camp'] += ' LIFE SummerTech—реальнаяENробототехника10–14в2026; Матвею после10-летия и нового объявления, Оскару рано.'
        c['school'] += (' TresCantos: LIFE—ENамериканская школа с христианской моделью; CiudaddeNejapa—государственная '
                       'Primaryс roboticsв4º /6º. Обе имеют programme evidence, чемпионские младшие результаты не установлены.')
        c['city_route'] += (' TresCantos—сравнить школу и независимую команду. Jaén20февраля2027есть в календаре, '
                          'но анонс не устанавливает FutureK8или младшийExploreпоток.')
        c['budget'] += (' LIFE2026/27: условно tuition13640–14200EURза двоих, первый год17084–17644до extras; '
                       'точные Gradeещё неизвестны. Это сравнение опубликованных тарифов, не цена страны.')
    elif c['iso'] == 'CHE':
        c['risk'] += (' WROStarterпрямо проводится на языке региона, EN / ESне подтверждены. '
                     'Future5+hardware: division1 / FAQ2комплекта на4детей; расхождение не разрешено.')
        c['city_route'] += (' JOIN: Chur / Yverdon28ноября2026, Lausanne12декабря, Windisch16января2027, '
                          'Jura23января, Freiamt13марта, Zürich20марта. Это категории отдельных событий; '
                          'JuraChallengeи YverdonExploreзаполнены на дату проверки.')
        c['osc'] += ' ПередStarterпроверить язык региона. Exploreне даёт мировой рейтинговой победы.'
    else:
        c['profile_ids'].append('fll-france-2027')
        c['city_route'] += (' Nouvelle-Aquitaine7февраля / Nantes13февраля / Poitiers26–28марта2027. '
                          'Nantesсоревнование11+пока рано обоим, зато фестиваль семейный.')
        c['risk'] += (' Nantes11–16строже национальных9–16; не переносить общий возраст на конкретный турнир. '
                     'LMOимеет даты robotics, но EN / ESне подтверждены.')
        c['camp'] += (' LMO19–23 /26–30октября: CE1+, Scratch / Thymio / Arduino / AI; язык EN / ESещё не подтверждён. '
                    'DevoxxNantes8–12—отдельный workshopпо записи, не пансион.')
        c['mat'] += ' LeLabChallenge9–16условно; Nantes11–16пока не подходит.'
f['evidence_cards'] += [
    dict(title='Швейцария · получен живой JOINкалендарь',
         detail='12очных записей Explore / Challenge / Future8+в7площадках. Два лимита заполнены на02.10.2026. '
                'Иностранное участие допускается; продвижение только через страну команды.',
         limit='AtHomeне назван очным турниром. EN / ES судейство отдельно; Exploreпризнание не мировой титул.',
         event_ids=swiss_ids,school_ids=[],source_urls=[urls['hot_join'],urls['hot_faq']]),
    dict(title='Испания · две школьные модели одного города',
         detail='LIFE: ENPrimaryи будущая10+ступень VEXEXP; христианская модель. CiudaddeNejapa: '
                'государственная Primary, roboticsв4º /6º, языки по предметам.',
         limit='Нет подтверждённого младшего мирового титула. Школа выбирается отдельно от действующей команды.',
         event_ids=['L402','C910','C911'],school_ids=['S045','S046'],source_urls=[urls['life_academic'],urls['nejapa']]),
    dict(title='Франция · местный возраст строже национального',
         detail='NationalFAQ9–16; Nantes11–16. РегионLeLab7февраля, Nantes13февраля, национальный26–28марта2027.',
         limit='Матвей2017достигает10в2027; Nantesне объявлен доступным соревнованием. Семейный просмотр открыт обоим.',
         event_ids=['C1102','C1103','C1104','E179','E180'],school_ids=[],source_urls=[urls['fr_faq'],urls['fr_botfest']]),
]
f['shortlist'].append(dict(title='Франция · бесплатные семейные роботоматчи2027',
    detail='BotFestNantes13февраля: оба зрителями, Матвею возможен workshop8–12по записи. '
           'Futuroscope26–28марта: семейный вход бесплатный; участие команды в национальном только по отбору.',
    event_ids=['E179','E180','L406']))
f['season_stops'] = [dict(country=country,date=date,title=title,detail=detail,event_ids=ids) for country,date,title,detail,ids in [
    ('Швейцария','28.11.2026','Chur / Yverdon','Chur:Explore /Challenge /Future8+. Yverdon:Exploreлимит заполнен, Challengeотдельно.',swiss_ids[:3]+swiss_ids[9:11]),
    ('Швейцария','12.12.2026','Lausanne','Exploreдля младших; ChallengeМатвею при допуске и языке.',swiss_ids[6:8]),
    ('Швейцария','16–23.01.2027','Windisch / Jura','WindischChallenge16января. JuraExplore23января; Challengeлимит заполнен.',swiss_ids[4:6]+swiss_ids[8:9]),
    ('Франция','07–13.02.2027','Nouvelle-Aquitaine / Nantes','LeLab7февраля:Challenge9–16. Nantes13февраля:семья; FLL11+пока рано обоим.',['C1102','C1103','E179','L406']),
    ('Испания','20.02.2027','Jaén','День объявлен UJA; редакцию / возраст / независимую группу на этой площадке подтвердить.',['C1101']),
    ('Швейцария','13–20.03.2027','Freiamt / Zürich','Две младшиеExploreвыставки. Это проектное признание, не турнирный мировой отбор.',[swiss_ids[3],swiss_ids[11]]),
    ('Франция','26–28.03.2027','FestivalNational · Futuroscope','Команды после региональной квалификации. Оба могут приехать зрителями; основной план27–28марта.',['C1104','E180']),
]]
for b in f['base_comparison']:
    if b['iso'] == 'ESP':
        b['school'] += ' TresCantos:LIFE /CiudaddeNejapaдобавлены как учебные варианты, не мировые лидеры.'
        b['school_ids'] += ['S045','S046']
        b['budget'] += (' LIFEдешевле по опубликованному примеру:tuition13640–14200EURза двоих; '
                       'это другое curriculumи христианская модель, качество команды не доказано.')
    elif b['iso'] == 'CHE':
        b['gate'] += ' WROStarterна языке региона. FLLJOINпубликует12очных записей; язык судейства отдельно.'
    else:
        b['trial'] += ' Nantes13февраля /Poitiers26–28марта2027:бесплатный семейный просмотр; команды по своим условиям.'
        b['event_ids'] += ['E179','E180']
for key in ['hot_join','hot_faq','hot_5','swiss_starter','jaen','es_registration','fr_festival','fr_faq','fr_planning',
            'fr_lab','fr_botfest','fr_botfest_info','lmo_camp','life_camp','life_academic','life_fees','nejapa','nejapa_language']:
    f['sources'].append(dict(title='Уточнённый первичный источник · '+key,url=urls[key],checked=CHECKED))

d['asof'] = CHECKED
d['expansion_log'].append(dict(version=45,checked=CHECKED,scope='CHE/ESP/FRA public season and family gates',added=23,
                               new_schools=2,new_profiles=1,status='partial; worldwide objective preserved'))
a = d['completeness_audit']; a['validation_previous'] = a.get('validation',{})
a.update(version=45,checked=CHECKED,status='Исследование продолжается',
    scope='CHE/ESP/FRA: новые реальные этапы2026/27, семейные посещения и школьные модели',
    conclusion='23новые карточки, один национальный FLLпрофиль и два школьных варианта. '
               'Локальные возраста, языковые и hardwareпротиворечия отмечены; остальной мировой каталог сохранён.',
    new_ids=[e['id'] for e in new],new_profiles=['fll-france-2027'],new_school_ids=['S045','S046'],
    updated_ids=['C906','C972','L278','C916'],updated_profile_ids=['fll-swiss-junior','fll-europe-three'],
    validation=dict(version=45,status='pending',publication='pending'))
d['camp_focus'].update(version=45,checked=CHECKED,added_ids=[e['id'] for e in new if e['block']=='Лагеря'],
    updated_ids=['L278'],conclusion='406учебных / лагерных карточек; новый ENVEXEXP10+архив отделён от будущих смен, '
                'LMOи Devoxxс неизвестным техническим EN / ESне включены в семейный календарь.',validation=dict(version=45,status='pending'))
d['school_focus'].update(version=45,checked=CHECKED,
    conclusion='46досье; LIFEи CiudaddeNejapaс programme evidenceи без выдуманного младшего мирового титула.')
known = {s['url'] for s in d['sources']}
for key in ['hot_join','hot_faq','hot_5','hot_8','hot_explore','swiss_starter','jaen','es_registration','fr_festival',
            'fr_faq','fr_planning','fr_spaces','fr_lab','fr_lab_info','fr_botfest','fr_botfest_info','lmo_camp','lmo_general',
            'life_camp','life_home','life_academic','life_faq','life_admissions','life_fees','nejapa','nejapa_language','nejapa_admissions']:
    if urls[key] not in known:
        d['sources'].append(dict(url=urls[key],title='Первичный источник · '+key,checked=CHECKED,
            evidence='Организатор / школа прочитаны; конкретные условия и пробелы помечены.'))
        known.add(urls[key])

def readable(value, key=''):
    """Only polish changed prose; identifiers, source URLs and dated fields stay exact."""
    if isinstance(value, dict):
        return {k: readable(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [readable(v, key) for v in value]
    if not isinstance(value, str) or key in ['id','iso','source','url','source_urls','event_ids','school_ids','profile_ids',
            'related_ids','related_school_ids','legacy_ids','start','end','deadline','checked','registration_opens',
            'priority','language_mode','school_type','evidence','research_status','participation','admission_kind','scope',
            'evidence_level','exhibition_tier','visitor_policy','date_scope','group'] or value.startswith('https://'):
        return value
    for a, b in {'TresCantos':'Tres Cantos','CiudaddeNejapa':'Ciudad de Nejapa','VEXEXP':'VEX EXP',
        'NationalFAQ':'National FAQ','FestivalNational':'Festival National','SwissFLL':'Swiss FLL',
        'STEMLabs':'STEM Labs','EarlyChildhood':'Early Childhood','SpanishLanguage':'Spanish Language',
        'Exploreдля':'Explore для','ChallengeМатвею':'Challenge Матвею','CS&AI':'CS & AI',
        'RobotChallenge':'Robot Challenge','AtHome':'At Home','SumoBot':'SumoBot',
        'Englishbilingual':'Двуязычная школа','programme evidence':'подтверждённая учебная программа',
        'LEGOrobot':'LEGO-робот','founders':'Founders','roboticsв':'робототехника в',
        'team codes':'коды команд','Challengeв':'Challenge в','WROмаршрут':'WRO-маршрут',
        'workshopsв':'workshops в','workshopи':'workshop и','Swissдата':'Swiss дата',
        'ENсудейство':'EN-судейство','ENробототехника':'EN-робототехника','VEXIQ':'VEX IQ',
        'FutureK':'Future K','Future5':'Future 5','Future8':'Future 8','SwissFuture':'Swiss Future',
        'robot hardware':'оборудование робота','season set':'сезонный комплект',
        'ENVEX':'EN VEX','Primaryвозможна':'Primary возможна','codeи':'code и',
        'hardwareи':'hardware и','campus2026':'campus 2026'}.items():
        value = value.replace(a, b)
    value = re.sub(r'(?<=[А-Яа-яЁёA-Za-z])(?=\d)|(?<=\d)(?=[А-Яа-яЁёA-Za-z])', ' ', value)
    value = re.sub(r'(?<=[А-Яа-яЁё])(?=[A-Za-z])|(?<=[A-Za-z])(?=[А-Яа-яЁё])', ' ', value)
    value = re.sub(r'([,;:])(?=[А-Яа-яЁёA-Za-z])', r'\1 ', value)
    value = re.sub(r'\b(P|C|E|L|S|H|CE|V|K) (?=\d)', r'\1', value)
    value = value.replace('Devoxx 4 Kids', 'Devoxx4Kids')
    value = value.replace('3 D', '3D').replace('V 5', 'V5').replace('season set', 'сезонный комплект')
    value = value.replace('педагогическое сезонный комплектза', 'педагогический сезонный комплект за')
    value = re.sub(r'(?<!\d)([:;])(?=\d)|(?<=\+)(?=[А-Яа-яЁёA-Za-z])', lambda m: m.group(0)+' ', value)
    value = re.sub(r'(?<=\d): (?=\d{2}(?!\d))', ':', value)
    value = value.replace('WROStarter', 'WRO Starter').replace('FLLJOIN', 'FLL JOIN').replace('ExploreLeLab', 'Explore Le Lab').replace('PrimaryGrades', 'Primary Grades')
    return value

for index, record in enumerate(d['events']):
    if record['id'] in [e['id'] for e in new] + ['C906','C972','L278','C916']:
        d['events'][index] = readable(record)
d['schools'][-2:] = [readable(s) for s in d['schools'][-2:]]
for index, profile in enumerate(d['league_guide']['profiles']):
    if profile['id'] in ['fll-swiss-junior','fll-europe-three','fll-france-2027']:
        d['league_guide']['profiles'][index] = readable(profile)
d['europe_focus'] = readable(f)
for k in ['completeness_audit','camp_focus','school_focus']:
    d[k] = readable(d[k])
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

fetches = []
for name in ['receipt.json','receipt-extra.json','receipt-schools.json','receipt-schools-extra.json']:
    fetches += json.loads((WORK / 'sources-europe-calendar-v45' / name).read_text())
receipt = dict(version=45,checked=CHECKED,scope='CHE/ESP/FRA public season and family gates',
    fetches=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in fetches],
    public_browser=dict(url=urls['hot_join'],rows=rows,
        sha256=hashlib.sha256((WORK/'sources-europe-calendar-v45/hot_join_rendered.txt').read_bytes()).hexdigest(),
        interpretation='12on-site entries in7locations. Two AtHomeentries excluded; month/day plus2026/27season yields dates. '
                       'Individual handson.toolsviews did not load reliably; no extra claims based on their HTTP200shell.'),
    source_limitations=['HelloAssodirectfetch403; current organiser2026/27form read throughweb.',
                       'EducaMadridrobotics/language/admissionsdirectfetches failed; primary bodies read throughweb.',
                       'JOINseats are a snapshot, not held places; no application submitted.',
                       'School statements are programme evidence; no independently verified world title inferred.'],
    conflicts=['Future5+:FAQtwo /divisiononeCS&AIkit per4children; hardwarepurchase unresolved.',
               'Future5+:divisionno /FAQfew ornoofficialevents2026/27; noSwissdatedevent found.',
               'Explore:FAQ6–9 /division6–10; cutoff not resolved.',
               'FranceNational9–16 /Nanteslocal11–16; localgate retained.',
               'LMO26–30October2026endweekday saysWednesdaybut30isFriday; weekwindow preserved, no daily slots inferred.',
               'Franceoldnationalpage2026versusdedicatednew2027festival.',
               'AtHomeChallenge1970andExploreheader30April/localdate29April; neither invented as on-site competition.'],
    remaining='Exact birthdays/classes, current mentors/places, technical-language exceptions, foreign quota, full national and worldwide coverage.')
(ROOT/'data/europe-calendar-source-receipts-v45.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
rp = ROOT/'data/research-plan.json'; r = json.loads(rp.read_text())
r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v45.json')
r['latest_validation_previous'] = r['latest_validation']
r['latest_validation'] = dict(version=45,status='local_checks_pending_publication_pending')
r['previous_goal_turn_classification'] = dict(version=44,classification='progress',
    evidence='Published86c4d838d6bd883c63580bf0d1f8053809658d51; anonymous live QA and all78distSHA256matched. '
             'CHE/ESP/FRApractical pass delivered; full-world objective remains active.')
r['research_passes'].append(dict(version=45,checked=CHECKED,scope='CHE/ESP/FRA public season and school alternatives',
    added_records=23,new_schools=2,new_profiles=1,status='partial',
    remaining='Individual venue schedule / languages, mentors, foreign quotas, future camps and worldwide objective'))
r['next_research'].insert(0,'CHE/ESP/FRA v45: текущие младшие команды / наставники; ResolveExplore6–9/10,Future5+hardware, '
    'EN / ESзащита и иностранная квота; новые2027лагеря. Singapore /HongKongсобранные источники ждут отдельного прохода; '
    'остальные страны и континенты продолжаются.')
for req in r['requirements']:
    if req['id']=='unified_database':req['evidence']='v45:1689cards/130profiles/46schools/136boundedresults; worldwidepartial.'
    elif req['id']=='camps':req['evidence']='v45:406learningcards; actuallanguage,age,futurecohortandworkshop distinctions.'
    elif req['id']=='permanent_schools':req['evidence']='v45:46dossiers; newprivateEnglishandpublicSpanishoptions with programme evidence.'
    elif req['id']=='global_competitions':req['evidence']='v45:1103competition/programme cards;12datedSwissentries,FR2027stagesandJaén.'
    elif req['id']=='exhibitions':req['evidence']='v45:180eventcards; twofreefamilyFRfestivals separate from industrialworldexpos.'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=45,added=len(new),records=len(d['events']),new_profiles=1,new_schools=2,world_complete=False)))
