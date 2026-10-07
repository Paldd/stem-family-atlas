"""Add the first evidence-led permanent-school pass without altering events.

Run once against the v19 catalog. Later research extends schools directly or in
new migrations; school years are not calendar events.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert not d.get('schools'), 'School migration already applied'
assert len(d['events']) == 1170
countries = {c['iso']: c for c in d['countries']}
schools = []

def source(title, url, claim, kind='school'):
    return dict(title=title, url=url, claim=claim, kind=kind, checked='2026-10-01')

def result(league, season, stage, award, team, url, provenance='school_report', limit='', team_id=None):
    return dict(league=league, season=season, stage=stage, award=award, team=team,
                team_id=team_id, source=url, provenance=provenance, limit=limit)

def school(id, name, iso, city, type, curriculum, ib, ages, languages, language_note,
           mat, osc, fit_note, boarding, boarding_note, programme, labs, ai,
           results, evidence, admissions, cost, questions, sources, priority=2):
    c = countries[iso]
    s = dict(id=id, name=name, iso=iso, country=c['country'], region=c['region'], city=city,
             school_type=type, curriculum=curriculum, ib_programmes=ib, ages=ages,
             instruction_languages=languages, language_note=language_note,
             fit=dict(mat=mat, osc=osc, note=fit_note), boarding=boarding,
             boarding_note=boarding_note, programme=programme, labs=labs, ai=ai,
             results=results, evidence=evidence, admissions=admissions, cost=cost,
             questions=questions, sources=sources, checked='2026-10-01', priority=priority,
             research_status='partial', verification='Документальная проверка; школа и место в команде не подтверждали приём детей.')
    assert all(r['source'] in {x['url'] for x in sources} for r in results)
    schools.append(s)

school('S001', 'Lincoln School', 'CRI', 'Heredia · Costa Rica (точный адрес проверить)', 'private',
 'Международная школа; elementary Grades 1–5, MYP Grades 6–10, старшая DP.',
 [{'programme':'PYP','status':'candidate'},{'programme':'MYP','status':'school_report'},{'programme':'DP','status':'school_report'}],
 'Начальная и средняя школа; нужный класс определяется по документам.', [],
 'Английский и испанский в программах есть; основной язык конкретного младшего класса и команды в этом проходе не установлен.',
 'candidate','candidate','Начальная ступень существует для обоих; вступительная оценка, точный класс и младшая команда требуют проверки.',
 'unknown','Пансион не подтверждён.',
 'Innovation Center проводит робототехнику. Часы, лига и актуальный отбор в младшую команду неизвестны.',
 'Подтверждён Innovation Center для совместной проектной работы.',
 'Computer Science в DP; отдельная младшая AI-программа не подтверждена.', [], 'programme',
 'Есть официальный раздел Apply Now. Места, иностранные документы и вступительные требования к конкретному классу уточнить.',
 'Актуальный тариф 2026–27 / 2027–28 не установлен.',
 ['Нужна команда соревновательного уровня после трёх лет опыта, а не только начальный кружок.','Запросить протоколы последних трёх сезонов и язык команды.'],
 [source('Technology / Innovation Center','https://www.lincoln.ed.cr/en/services/technology','Робототехника и Innovation Center'),
  source('Elementary','https://www.lincoln.ed.cr/en/academics/elementary','Grades 1–5; PYP candidate'),
  source('IB Program','https://www.lincoln.ed.cr/en/academics/ib-program','MYP / DP и Computer Science'),
  source('Apply Now','https://www.lincoln.ed.cr/en/admissions/apply-now','Официальный путь обращения в admissions')],1)

school('S002','American School Foundation of Monterrey · ASFM','MEX','Santa Catarina · агломерация Monterrey','private',
 'Международная дневная школа Nursery–Grade 12; американская программа и AP.', [],
 'Kinder–Grade 5 для младших; FTC относится к Middle / High School.', ['EN'],
 'Школа прямо называет английский основным языком обучения; испанский — предмет. Язык соревнований отдельно.',
 'candidate','candidate','Младшая ступень есть; допуск каждого в FLL Explore и уровень после трёх лет опыта не установлен.',
 'no','Школа описана как day school.',
 'Начальная команда FLL Explore; Robotic Eagles в FTC для Middle / High School. Есть собственные турнирные инициативы.',
 'Проверены команды и extended learning; оборудование, доступ в лабораторию и недельные часы уточнить.',
 'Младший AI-курс не подтверждён.',
 [result('FLL Explore','не указан на странице','Этап на странице не уточнён','Programming Award; далее участие в Nationals','Elementary robotics team','https://www.asfm.edu.mx/extended-learning',limit='Нельзя называть эту награду победой в мировом финале или приписывать ей 2026 год.')],
 'other_result',
 'На странице приёма: заявки на январь 2027 с 4 сентября 2026; Kinder–Grade 11 на 2027–28 — с октября 2026, точный день не указан. Оценка и решение admissions обязательны.',
 '2026–27: K–5 при оплате одним взносом MXN 334 620 для первого ребёнка, MXN 296 670 для второго и далее. Отдельно регистрация MXN 32 760 и entrance fee USD 9 550; проверить начисления на каждого ребёнка. Тариф 2027–28 неизвестен.',
 ['Уточнить текущую младшую лигу и путь после перехода FIRST K–8.','Получить расписание, размер команды, результаты с сезоном и полную смету для двоих.'],
 [source('Extended Learning','https://www.asfm.edu.mx/extended-learning','Младшая FLL Explore и старшая FTC; награда без сезона'),
  source('Admissions','https://www.asfm.edu.mx/admissions','Международная day school; окна подачи'),
  source('Application process','https://www.asfm.edu.mx/admissions/application-process','Оценка и решение о приёме'),
  source('Tuition 2026–27','https://www.asfm.edu.mx/admissions/tuition-fees','Годовой взнос K–5, регистрация и entrance fee'),
  source('Work at ASFM','https://www.asfm.edu.mx/work-at-asfm','English как основной язык; испанский как предмет')],1)

school('S003','Taipei American School · TAS','TWN','Taipei · Tianmu','private',
 'Pre-K–Grade 12; американская программа, AP / IB Diploma в старшей школе.',
 [{'programme':'DP','status':'school_report'}],
 '6 лет к 1 сентября для Grade 1; остальные классы — по возрасту, подготовке и документам.', ['EN'],
 'Admissions оценивает английский уже в Pre-K–Grade 2; для Grades 3–5 и 6–12 требования выше. Язык конкретного клуба уточнить.',
 'candidate','candidate','Оба — кандидаты в Lower School; мировая награда относится к Middle School, а не к группе 6–9 лет.',
 'unknown','Пансион не подтверждён.',
 'Tech Cube охватывает младшую, среднюю и старшую ступени; нижняя — физическое программирование и робототехника. Старшие команды VEX / FRC.',
 'На старшей ступени: электроника, CNC, CAD/CAM, 3D-производство, вычислительные ресурсы и поле FRC; доступ младшим к этим ресурсам не доказан.',
 'AI / Machine Learning прямо указаны в продвинутой программе Upper School; не переносим их на Lower School.',
 [result('VEX V5 High Stakes',2025,'VEX World Championship · Engineering Division','Division Champion','Middle School Terminus','https://www.tas.edu.tw/community/news/story/~board/tas-news/post/middle-school-robotics-team-terminus-makes-history-at-vex-world-championship',limit='Победа в дивизионе, не абсолютная победа всего чемпионата; сообщение школы.')],
 'world_result',
 'Нужны иностранный паспорт ребёнка и дополнительный документ о гражданстве / въезде из перечня TAS. Интервью, академические документы, английский и наличие мест. Для Grades 5+ стандартизированный тест. Возраст отсчитывается на 1 сентября; точные дни рождения детей неизвестны.',
 'Application fee NTD 10 000; это не стоимость обучения. Актуальный годовой тариф и остальные сборы не установлены.',
 ['Проверить конкретный младший роботоклуб и путь Lower → Middle VEX.','Школа и участники имеют разный национальный допуск на турниры; паспорт не гарантирует квоту.'],
 [source('Terminus at Worlds 2025','https://www.tas.edu.tw/community/news/story/~board/tas-news/post/middle-school-robotics-team-terminus-makes-history-at-vex-world-championship','Engineering Division Champion 2025'),
  source('Tech Cube','https://www.tas.edu.tw/academics/the-tech-cube-program','Разные ступени: младшие проекты, старшие лаборатории и AI'),
  source('How to Apply','https://www.tas.edu.tw/admissions/how-to-apply','Иностранный паспорт, возраст, английский, документы, application fee')],1)

school('S004','Kang Chiao International School · Xiugang campus','TWN','New Taipei · Xindian','private',
 'Именно Xiugang: Grades 7–12. Junior MYP, старшие IB DP / AP.',
 [{'programme':'MYP','status':'school_report'},{'programme':'DP','status':'school_report'}],
 'Grades 7–12; младшие Qingshan и Linkou — другие кампусы и отдельная проверка.', [],
 'Американский и IB пути описаны; язык конкретного класса и команды не подтверждён этим проходом.',
 'future','future','Оба пока младше ступени Xiugang. Результаты этого кампуса нельзя автоматически присвоить начальным кампусам сети.',
 'unknown','Режим проживания и возраст пансиона не установлены.',
 'VEX Taiwan Open 2024: команда Xiugang 14683B вошла в top four; независимый протокол и действующий состав проверить.',
 'Оборудование и недельная нагрузка команды не установлены.',
 'AI-курс не подтверждён.', [result('VEX',2024,'VEX Taiwan Open','Top four in finals','Xiugang','https://news.kcis.ntpc.edu.tw/vex-robotics-2024-fall-xiuguan-taiwan-open/',team_id='14683B',limit='Top four по сообщению школы; не победа или мировой титул.')], 'other_result',
 'Для будущего secondary: проверить язык выбранного пути, тесты, иностранный приём и места именно в Xiugang.',
 'Актуальная стоимость не установлена.',
 ['Проверить VEX awards по официальному протоколу.','Начальные Qingshan / Linkou оценивать отдельными карточками после проверки собственных команд.'],
 [source('Xiugang About Us','https://www.kcis.com.tw/EN/AboutUs.html','Точный кампус Grades 7–12'),
  source('Junior High','https://www.kcis.com.tw/EN/JH.html','Junior / MYP'),
  source('Senior High','https://www.kcis.com.tw/EN/SH.html','Grades 10–12; DP / AP'),
  source('VEX Taiwan Open report','https://news.kcis.ntpc.edu.tw/vex-robotics-2024-fall-xiuguan-taiwan-open/','2024: Xiugang 14683B top four; не мировой титул')],2)

school('S005','Dulwich College Shanghai Pudong','CHN','Shanghai · Pudong','private',
 'Международная школа: DUCKS, Junior и Senior; точный возрастный cut-off уточнить. Старшая программа требует отдельной проверки IB.', [],
 'Есть Junior School; класс и возраст оцениваются admissions.', ['EN'],
 'Admissions FAQ описывает требования к английскому и поддержку неанглоязычных; доступность поддержки зависит от ступени.',
 'candidate','candidate','Младшая ступень есть; конкретный возраст Panther Robotics CCA и допуск обоих не подтверждены.',
 'unknown','Пансион не подтверждён.',
 'SE21, Junior Panther Robotics CCA и межшкольные робототехнические встречи; национальный результат найден также в инженерном STEM Racing.',
 'SE21 пространство работает на разных ступенях; оборудование и часы младшей группы уточнить.',
 'Отдельная младшая AI-программа не подтверждена.',
 [result('STEM Racing',2026,'Национальный этап Китая','National Champion','Dulwich Dynamos','https://shanghai-pudong.dulwich.org/learning/holistic-education/stem',limit='Инженерный racing-проект; это не победа в робототехнической лиге и не мировой титул.')],
 'national_result',
 'Проверить актуальные муниципальные условия для иностранных семей, паспорт / документы родителей, класс и английский. Указанное окно 2026–27 исторически открывалось в 2025; наличие мест сегодня не доказано.',
 'Актуальная стоимость и обязательные сборы не установлены.',
 ['Получить возраст и часы Junior Robotics, последние VEX-протоколы.','Проверить eligibility именно Pudong, не переносить правила Puxi.'],
 [source('STEM / SE21','https://shanghai-pudong.dulwich.org/learning/holistic-education/stem','Junior robotics; национальный STEM Racing 2026'),
  source('Admissions FAQ','https://shanghai-pudong.dulwich.org/admissions/apply/frequently-asked-questions','Английский и поддержка'),
  source('Apply Now','https://shanghai-pudong.dulwich.org/admissions/apply-now','Процесс поступления; ограничения муниципального допуска')],2)

school('S006','Horizon Primary School','SGP','Singapore · Punggol','public',
 'Государственная начальная школа, национальная программа Singapore.', [], 'Primary; точный класс и возрастный вход требуют проверки MOE.', [],
 'EN как основной язык системы требует отдельной проверки доступного документа MOE; язык робототехнической CCA пока не подтверждён.',
 'candidate','candidate','Начальная ступень; CCA может начинаться позже первого класса. Иностранный приём и назначение школы не гарантированы.',
 'unknown','Пансион не подтверждён; исследована начальная школа.',
 'Подтверждены национальные результаты по робототехнике и школьному hackathon за 2025.',
 'Конкретное оборудование, AI-лаборатория и тренировочные часы не установлены.', 'Отдельный AI-курс не подтверждён.',
 [result('NRPC',2025,'Национальные соревнования Singapore','Overall Champion','Horizon Primary robotics','https://www.horizonpri.moe.edu.sg/our-pride/achievements/achievements-2025/',limit='Национальный результат по сообщению школы; не мировой титул.'),
  result('IDE',2025,'Singapore · Primary SumoBot','Overall Championship','Horizon Primary robotics','https://www.horizonpri.moe.edu.sg/our-pride/achievements/achievements-2025/'),
  result('Pei Hwa Hackathon',2025,'Школьный / межшкольный этап','2nd Runner-up','Horizon Primary','https://www.horizonpri.moe.edu.sg/our-pride/achievements/achievements-2025/')],
 'national_result',
 'Иностранцам нужен отдельный путь MOE. Текущие даты P1 / AEIS, возрастные рамки, тесты и возможность выбрать именно Horizon не установлены; страницы MOE частично блокируют чтение.',
 'Тариф зависит от статуса и категории иностранного ребёнка; действующая сумма не установлена.',
 ['Нужны актуальные правила MOE и язык команды.','Проверить возраст старта CCA и выход на международную лигу.'],
 [source('Achievements 2025','https://www.horizonpri.moe.edu.sg/our-pride/achievements/achievements-2025/','NRPC, IDE и Pei Hwa Hackathon 2025', 'public_school')],2)

school('S007','Rulang Primary School','SGP','Singapore · Jurong West','public',
 'Государственная начальная школа; Applied Learning Programme.', [], 'Primary; класс и правила иностранного входа уточнить.', [],
 'Основной язык класса и команды в этом проходе не подтверждены прямым прочитанным документом.',
 'candidate','candidate','Начальная ступень есть; возраст и отбор робототехнической AEP / ALP не установлены.',
 'unknown','Пансион не подтверждён.',
 'Robotics Accelerated Education Programme включён в Applied Learning Programme. Само название AEP не доказывает международные победы.',
 'Точная робототехническая лаборатория и оборудование не установлены.', 'AI-курс не подтверждён.', [], 'programme',
 'Проверить путь MOE для иностранцев и школьное назначение. Наличие такой программы не означает свободную покупку места в государственной школе.',
 'Актуальная плата для иностранцев не установлена.',
 ['Найти результаты последних трёх сезонов и код команды.','Установить язык, часы, начальный класс и доступность AEP для новых детей.'],
 [source('Learning Experiences','https://www.rulangpri.moe.edu.sg/rulang-learning-experiences/','Школьные программы', 'public_school'),
  source('AEP / ALP Robotics','https://www.rulangpri.moe.edu.sg/rulang-learning-experiences/accelerated-education-programme-aep/','Робототехническая AEP / ALP', 'public_school')],2)

school('S008',"Queen Elizabeth’s School · Barnet",'GBR','London · Barnet','public',
 'Государственная селективная школа для мальчиков; вход Year 7, внешнего поступления в Sixth Form нет.', [],
 'Year 7 с 11 лет. VEX IQ в примере 2024 — Years 8–9; VRC — Years 10 и 12.', [],
 'Основной язык EN вероятен по системе, но отдельный прямой документ о языке команды ещё не проверен.',
 'future','future','Будущий маршрут: Матвею 11 исполнится в 2028, Оскару — в 2031; класс поступления зависит от точной даты рождения и правил.',
 'unknown','Пансион не подтверждён.',
 'VEX IQ / VRC, постоянная robotics room. Есть мировой оценённый результат и недавние национальные результаты.',
 'Отдельная robotics room с 2019; текущий парк и часы уточнить.', 'AI-курс не подтверждён.',
 [result('VEX IQ',2018,'VEX World Championship','Overall Excellence Award','QE robotics','https://www.qebarnet.co.uk/beyond-the-classroom/clubs-extra-curricular/robotics-showcase/',limit='Оценённая Excellence Award; не автоматически победа Robot Game. Исторический 2018, не текущий сезон.'),
  result('VEX IQ',2024,'UK national championship','Teamwork Champion','Gearsquad','https://www.qebarnet.co.uk/ready-to-take-on-the-world/'),
  result('VEX IQ',2024,'UK national championship','Robot Skills Champion','Circuit Breakers','https://www.qebarnet.co.uk/ready-to-take-on-the-world/')],
 'world_result',
 'Вступительный тест в Year 7 и Common Application через местный орган. Иностранное проживание, адрес, текущая процедура и дедлайн нужного года отдельно; победы в робототехнике не отменяют конкурс.',
 'Школьная плата и расходы для статуса семьи отдельно; актуальная полная смета не установлена.',
 ['Добавить протоколы 2025–26, а не считать старый Excellence текущим мировым титулом.','Проверить проживание, сроки entrance test и доступ нового ученика к команде.'],
 [source('Robotics Showcase','https://www.qebarnet.co.uk/beyond-the-classroom/clubs-extra-curricular/robotics-showcase/','Исторический Excellence 2018, robotics room', 'public_school'),
  source('Ready to take on the world','https://www.qebarnet.co.uk/ready-to-take-on-the-world/','2024: национальные результаты и классы', 'public_school'),
  source('Admissions','https://www.qebarnet.co.uk/admissions-information/','11+ вход, тест и отсутствие внешнего Sixth Form', 'public_school')],3)

school('S009','Aiglon College','CHE','Chesières · Villars-sur-Ollon','private',
 'Junior / Senior; IB Diploma. Частная международная школа с дневным и пансионным режимами.',
 [{'programme':'DP','status':'authorized_registry'}],
 'Junior: на одной странице заголовок 7–11, описание 6–11 / Years 2–6. Требуется разрешить расхождение.', ['EN'],
 'IB registry подтверждает EN для Diploma. Язык junior и робототехнической группы отдельно не установлен.',
 'candidate','unknown','Для Матвея junior по возрасту вероятен; для Оскара нижняя граница противоречива. Точный класс и дневной режим проверить.',
 'yes','Junior: day Years 3–4; boarding с Year 5. Возраст ребёнка сам по себе не подтверждает нужный Year.',
 'Applied Innovation Robotics AIR lab и junior robotics подтверждены; результатов мировых команд в этом проходе нет.',
 'AIR lab; оборудование и тренировочная нагрузка для младших уточнить.', 'Отдельный AI-курс младших не подтверждён.', [], 'programme',
 'Admissions: проверить junior entry, тесты / интервью, day для семьи на месте и boarding только с разрешённой ступени.',
 'Тариф day / boarding нужного учебного года не установлен.',
 ['Разрешить 6 / 7 лет и язык junior.','Проверить соревнования, код команды и результаты; IB и AIR lab не равны мировому рейтингу.'],
 [source('Learning / AIR','https://www.aiglon.ch/learning','AIR lab и junior robotics'),
  source('Junior School','https://www.aiglon.ch/juniorschool','Противоречие возраста; day и boarding по Year'),
  source('IB registry: Aiglon','https://ibo.org/school/006328/','Private; authorised DP; English DP; mixed boarding', 'registry')],2)

school('S010','Ermitage International School · IB programmes','FRA','Maisons-Laffitte · рядом с Paris','private',
 'Англоязычная primary 5–11; школа описывает MYP / DP. Проверка относится к IB-пути, не ко всем французским классам.',
 [{'programme':'PYP','status':'candidate'},{'programme':'MYP','status':'school_report'},{'programme':'DP','status':'school_report'}],
 'IB primary 5–11; пансион 11–18.', ['EN'],
 'Primary страница прямо описывает англоязычную среду и помощь неанглоязычным; французский — отдельное обучение.',
 'candidate','candidate','Оба в возрастной рамке дневной primary; фактический класс, места и возраст robotics after-school уточнить.',
 'yes','Пансион только 11–18; для 6 и 9 лет — дневной путь с семьёй.',
 'Coding & Robotics после уроков; точная соревновательная лига и награды не установлены.',
 'Конкретная robotics lab не подтверждена.', 'Отдельная младшая AI-программа не подтверждена.', [], 'programme',
 'Уточнить документы, английский, стоимость и допуск к выбранному after-school. Candidate PYP ещё не означает авторизацию IB.',
 'Дневной тариф primary и будущий boarding не установлены.',
 ['Найти действующую команду и результаты.','Подтвердить авторизацию нужной программы в IB registry и уровень робототехники после трёх лет опыта.'],
 [source('IB Primary','https://www.ermitage.fr/ib-programs/ib-pyp','5–11, English primary, PYP candidate'),
  source('Extracurricular activities','https://www.ermitage.fr/ib-programs/ib-extracurricular-activities','Coding & Robotics after-school'),
  source('Boarding','https://www.ermitage.fr/boarding','Возраст 11–18 и режимы проживания')],2)

school('S011','Brains International School · La Moraleja','ESP','Alcobendas · Madrid','private',
 'Частная международная школа; Primary 6–12. IB-статусы ниже — по странице самой школы.',
 [{'programme':'PYP','status':'school_report_authorized'},{'programme':'MYP','status':'candidate'},{'programme':'DP','status':'school_report_authorized'}],
 'Primary 6–12; указанный FLL путь описан для Secondary.', ['EN','ES'],
 'Школа прямо описывает bilingual English / Spanish Primary; язык конкретной роботокоманды уточнить.',
 'candidate','candidate','Оба — кандидаты в Primary. Соревновательная FLL описана у старших: место в команде младших не установлено.',
 'unknown','Пансион не подтверждён.',
 'Программирование и робототехника с младших ступеней; FLL и clauTIC упомянуты как участие, без доказанной мировой награды.',
 'Технологические пространства заявлены школой; состав оборудования и доступ младшим требуют проверки.',
 'Отдельный младший AI-курс не подтверждён.', [], 'programme',
 'Проверить класс, admissions-оценку, документы иностранцев, bilingual требования и реальный junior competition track.',
 'Найденная страница упоминает тариф старого года; актуальная сумма не установлена.',
 ['Получить протоколы FLL / clauTIC и junior team.','Проверить IB registry: авторизация каждой программы и кампуса отдельно.'],
 [source('La Moraleja official profile','https://www.colegiobrains.com/colegios/la-moraleja/','Тип, bilingual primary, IB-статусы и робототехническое участие')],2)

school('S012','Bellarmine College Preparatory','USA','San José · California','private',
 'Secondary для мальчиков, AP / Honors; точные входные классы и международная заявка требуют проверки.', [],
 'High school; оба ребёнка пока младше школьной ступени.', [],
 'EN вероятен, но язык обучения и тестовый порог для иностранных кандидатов отдельно не установлен.',
 'future','future','Долгосрочный secondary-маршрут; наличие FRC 254 не делает школу доступной детям 6 / 9.',
 'unknown','Пансион не подтверждён.',
 'FRC Team 254 Cheesy Poofs, FTC с 2023; 4 FTC команды. Проектирование, программирование, управление и наставничество.',
 'Сильная инженерная команда и Maker Lab в школьной структуре; доступ новичка и недельная нагрузка уточнить.',
 'Отдельный AI-курс не подтверждён.',
 [result('FIRST Robotics Competition',2026,'FIRST Championship · Curie Division','Championship Division Winner','The Cheesy Poofs','https://frc-events.firstinspires.org/2026/team/254','organizer_protocol','Победа дивизиона. Школа отдельно сообщает, что абсолютный финал 2026 не выигран.', '254')],
 'world_result',
 'Отдельный admissions-конкурс. Уточнить приём иностранных школьников, возможный visa support, класс, требования и дату нужного года.',
 'Актуальный tuition и дополнительные расходы не установлены.',
 ['Проверить вход в Team 254, отбор и обязанности ученика.','Подобрать младшую подготовительную школу отдельно; не приписывать ей результат Bellarmine.'],
 [source('Robotics','https://www.bcp.org/student-life/robotics','FRC / FTC и инженерная команда'),
  source('2026 season school report','https://www.bcp.org/p/~board/bellarmine-college-preparatory-news/post/bellarmine-robotics-closes-out-another-successful-season','Curie winner; не абсолютный чемпион'),
  source('FIRST official 254 / 2026','https://frc-events.firstinspires.org/2026/team/254','Официальная награда и код команды', 'organizer'),
  source('Admissions','https://www.bcp.org/admissions','Мальчики; AP / Honors; отдельный процесс приёма')],3)

school('S013','Mānoa Elementary School','USA','Honolulu · Oʻahu, Hawaiʻi','public',
 'Hawaiʻi DOE public elementary K–Grade 5.', [], 'Kindergarten–Grade 5.', [],
 'Язык конкретного роботокружка и помощь иностранным детям не установлены.',
 'candidate','candidate','Начальная ступень есть; приём связан с проживанием в округе. Кружок 2025 не доказывает набор 2026.',
 'unknown','Пансион не подтверждён.',
 'В историческом Spring 2025 Cub Clubs указаны LEGO robotics / Bricks 4 Kidz. Активная соревновательная команда 2026 и мировые награды не подтверждены.',
 'Оборудование и постоянная лаборатория не установлены.', 'AI-курс не подтверждён.', [], 'programme',
 'Официальная регистрация требует проживания в школьном округе, школьных и медицинских документов. Правовой статус семьи и возможность приёма иностранцев отдельно.',
 'Полная смета для статуса семьи, кружок и проживание не установлены.',
 ['Подтвердить текущий роботоклуб и соревнования.','Проживание, статус и документальное право на запись важнее наличия веб-формы.'],
 [source('Hawaiʻi DOE school directory','https://hawaiipublicschools.org/schools/manoa-elementary/','Public K–5 и точная школа', 'registry'),
  source('School site / Cub Clubs','https://www.manoaschool.com/','Историческая notice Spring 2025: LEGO robotics', 'public_school'),
  source('Registration','https://www.manoaschool.com/apps/pages/index.jsp?uREC_ID=2890263&type=d&pREC_ID=2333150','Обязательное проживание в округе и документы', 'public_school')],2)

school('S014','Barker College','AUS','Hornsby · Sydney','private',
 'Частная co-educational школа от младших ступеней до Year 12; boarding с Year 10.', [],
 'Младшая школа существует; VEX / FRC награды старших не определяют возраст младшего robotics.', [],
 'EN вероятен, но язык и требования к иностранному ребёнку в конкретной junior группе пока не установлены.',
 'candidate','candidate','Day junior — кандидаты для обоих. Нужный Year, доступ в robotics и международный приём отдельно.',
 'yes','Обычный boarding начинается в Year 10; для 6 / 9 лет не подходит. Указан приоритет rural / regional families Australia.',
 'VEX и FRC 4613; dedicated robotics programme. Условия младшей группы и перехода в старшую команду требуют проверки.',
 'VEX lab с 2022; полноразмерное поле FRC, CNC / prototyping у старшей команды.',
 'Отдельная младшая AI-программа не подтверждена.',
 [result('FIRST Robotics Competition',2025,'FIRST Championship · Daly Division','Championship Division Winner','Barker Redbacks','https://frc-events.firstinspires.org/2025/team/4613','organizer_protocol','Победа дивизиона, не абсолютный мировой титул.', '4613'),
  result('FIRST Robotics Competition',2025,'FIRST Championship · Daly Division','Industrial Design Award','Barker Redbacks','https://frc-events.firstinspires.org/2025/team/4613','organizer_protocol','Оценённая инженерная награда.', '4613')],
 'world_result',
 'На странице enrolments — ограниченная доступность и waiting lists; точки входа Pre-K / K / Years 3, 5, 7. Наличие места для иностранной семьи не подтверждено.',
 'Day / boarding и обязательные сборы нужного года не установлены.',
 ['Подтвердить junior robotics, часы и EN support.','Проверить очередь, иностранный вход и текущие fees; boarding сейчас исключён по ступени.'],
 [source('Barker Robotics','https://www.barker.college/co-curricular/barker-robotics/','VEX / FRC и лаборатории'),
  source('FIRST official 4613 / 2025','https://frc-events.firstinspires.org/2025/team/4613','Daly winner и Industrial Design Award', 'organizer'),
  source('Enrolments','https://www.barker.college/enrolments/','Waiting lists, точки входа; boarding Year 10')],2)

school('S015','Escola SESI-SP Jundiaí · Heroes','BRA','Jundiaí · São Paulo','private_industry',
 'Школа сети SESI-SP. Точная связь действующей Heroes с кампусом / CE и младшими классами требует проверки.', [],
 'Сеть обучает школьников; конкретный младший класс и возраст вступления в Heroes не установлены.', [],
 'EN / ES преподавание не подтверждено; сайт и регион работают на португальском. Не считается англоязычным вариантом.',
 'unknown','unknown','Сильная команда подтверждена, но младший вход, язык и кампус для детей пока не установлены.',
 'unknown','Пансион не подтверждён.',
 'SESI-SP: учебный компонент Programming & Robotics, проекты и отборные команды. Heroes получила мировую оценённую награду FLL.',
 'Точный доступ младших к оборудованию конкретного кампуса не установлен.',
 'Сеть описывает AI-проекты в robotics curriculum; наличие курса для нужного класса не доказано.',
 [result('FIRST LEGO League Challenge',2025,'FIRST World Festival · Houston','Champion’s Award','SESI Heroes · Jundiaí','https://www.sesisp.org.br/noticia/sesi-sp-brilha-no-mundial-de-robotica-nos-eua-e-conquista-o-maior-premio-com-equipe-de-jundiai','school_operator_report','Оценённая комплексная награда FLL. Источник — SESI-SP; независимый FIRST протокол и точный кампус ещё проверить.')],
 'world_result',
 'Приоритет детям работников индустрии и связанных организаций; прочие кандидаты — при оставшихся местах. Ранние классы: lottery; со 2-го класса: школьный отбор. Страница описывает набор 2026 с датами 2025, не новое окно 2027. Иностранный статус отдельно.',
 'Плата, льготы сети и статус иностранного ребёнка не установлены.',
 ['Установить точный действующий кампус Heroes, младший набор и язык.','Получить независимый FIRST протокол и результаты других сезонов.'],
 [source('SESI-SP at Worlds 2025','https://www.sesisp.org.br/noticia/sesi-sp-brilha-no-mundial-de-robotica-nos-eua-e-conquista-o-maior-premio-com-equipe-de-jundiai','Heroes Jundiaí: Champion’s Award 2025', 'school_operator'),
  source('Robótica Educacional','https://jundiai.sesisp.org.br/robotica-educacional-na-escola','Учебный компонент, Programming / Prototyping и AI-проекты сети'),
  source('SESI admission process','https://jundiai.sesisp.org.br/processo-seletivo','Приоритет, lottery / тест; исторический набор 2026')],3)

school('S016','Northlands Primary School','ZAF','Durban North','public',
 'Public primary с платой; тип подтверждён историческим государственным перечнем, текущую классификацию перепроверить. Grades 000–7.', [],
 'Coding & Robotics с Grade R; начальные ступени до Grade 7.', ['EN'],
 'Admissions прямо указывает English medium school; язык роботокоманды уточнить.',
 'candidate','candidate','Оба — кандидаты в начальные классы; класс, места и уровень FLL после трёх лет опыта отдельно.',
 'unknown','Пансион не подтверждён.',
 'Coding & Robotics, FIRST LEGO League и specialist learning. В этом проходе точный международный протокол не прочитан; не отмечено мировой победой.',
 'Computer lab: 16 iMacs; junior iPads; Innovation Hub с laser cutter и 3D-принтером.',
 'AI-курс не подтверждён.', [], 'programme',
 'Для иностранцев страница требует residence permit и study visa, подтверждение адреса, учебные и медицинские документы. Дедлайн 2027 был 31 июля 2026; после него обработка до внутреннего предела, свободные места не доказаны.',
 'School fees 2026: ZAR 48 600; ожидается рост в 2027, новая сумма не установлена. Дополнительные расходы проверить.',
 ['Найти первичный протокол Smooth Sailors и действующий FLL набор.','Проверить наличие места после дедлайна, документы и тариф 2027.'],
 [source('Specialist learning','https://www.northlandsprimary.co.za/department/specialist-learning','Coding / robotics с Grade R, FLL и оборудование'),
  source('Admissions / Apply','https://www.northlandsprimary.co.za/apply','English medium, foreign documents, deadlines и fees'),
  source('Government school allocations 2008','https://www.treasury.gov.za/documents/provincial%20budget/2008/Allocations/KwaZulu-Natal%20-%20Transfers%20to%20Schools.pdf','Исторический тип public primary: North Durban 236430, не одноимённая школа', 'historical_registry')],2)

d['schools'] = schools
d['school_focus'] = dict(
 checked='2026-10-01', version=20, status='partial',
 family='Матвей — 2017, Оскар — 2020; оба могут учиться на английском и испанском. Точные дни рождения и классы неизвестны.',
 conclusion='Первый документальный проход, не полный мировой список и не рейтинг качества школы. Ни одна школа не подтвердила приём детей или место в команде.',
 methodology=[
  'Сильный результат команды отделён от общего STEM-маркетинга, лаборатории и начального кружка.',
  'Division Champion, Excellence / Champion’s Award, национальная победа и участие описываются буквально; они не заменяют друг друга.',
  'FIRST-протоколы имеют отдельную отметку. Новости школы — первичный рассказ участника, но не независимое подтверждение организатора.',
  'IB candidate отличается от авторизованной программы. Проверка авторизации относится к программе и кампусу.',
  'Младшая школа, соревновательная команда, язык занятий и возраст пансиона проверяются отдельно.',
  'Англоязычный сайт не считается доказательством EN преподавания. Язык DP не переносится на junior.',
  'Государственная школа может требовать адрес, статус, распределение или тест. Наличие сайта не означает международный свободный приём.',
  'Для детей с трёхлетним соревновательным опытом нужно отдельно проверить наставника, уровень группы и путь на отборный этап.',
  'Школа — постоянная организация, а не календарная карточка; дедлайны без точного дня не превращаются в события.'
 ],
 routes=[
  dict(name='Начать рядом', ids=['S001','S002'], detail='Lincoln: проверить действующую младшую команду и язык. ASFM: подтверждены Elementary FLL Explore и старшая FTC; проверить уровень для обоих, новый сезон FIRST и полную цену.'),
  dict(name='Тайвань и Азия', ids=['S003','S004','S005','S006','S007'], detail='TAS: реальный Lower → Middle путь с результатом старших; иностранный паспорт и English assessment. Xiugang — будущая secondary. Shanghai и Singapore требуют отдельного иностранного допуска.'),
  dict(name='Дневная школа и будущий пансион', ids=['S009','S010','S011','S014'], detail='Возраст школы не равен возрасту пансиона: Aiglon по Year, Ermitage с 11, Barker с Year 10. Для 6 / 9 сначала проверять day и проживание с семьёй.'),
  dict(name='Будущая сильная команда', ids=['S008','S012','S014','S015'], detail='QE, Bellarmine, Barker и SESI имеют результаты старших. Построить младший маршрут, доказать собственный вклад ребёнка и проверить отбор; титул команды не обещает титул новому ученику.')
 ],
 gaps=[
  'Пока 16 школ в 13 странах, из мирового справочника 249 стран и территорий. Полностью проаудированных стран по школам: 0.',
  'Нет полного обзора школ Costa Rica / México, других стран LatAm, Taiwan primary campuses, Hong Kong, Japan, Korea, India, Middle East и Европы.',
  'Для большинства отсутствуют язык роботокоманды, junior league age, недели нагрузки, текущий набор, тариф и результаты трёх сезонов.',
  'Доступ к AI у 6 / 9 лет почти нигде не подтверждён. Продвинутый Upper / Secondary курс не считается младшей AI-программой.',
  'Сеть SESI требует уточнения кампуса; IB-статусы по сообщениям школы дополнительно сверять с registry.',
  'Жильё семьи, иммиграция, школьные визы, поездки команды и полная смета ещё не оценены.'
 ])
urls={s['url'] for s in d['sources']}
for s in schools:
    for x in s['sources']:
        if x['url'] not in urls:
            d['sources'].append(dict(url=x['url'],title=x['title'],evidence=x['kind']+': '+x['claim'],checked=x['checked']))
            urls.add(x['url'])
d['source_count']=len(d['sources'])
d['expansion_log'].append(dict(version=20, checked='2026-10-01', description='Школы: первый отдельный проход, 16 организаций в 13 странах; события и лиги не изменены.',new_school_ids=[s['id'] for s in schools],new_ids=[]))
a=d['completeness_audit']
a.update(version=20,checked='2026-10-01',new_ids=[],new_profiles=[],new_school_ids=[s['id'] for s in schools])
a['scope']='Мировой календарь, лиги, выставки, лагеря и отдельный каталог постоянных школ. v20 добавляет первый школьный проход; прежние 1170 событий сохранены.'
a['school_focus']=d['school_focus']
a['known_backlog'].append(dict(name='Постоянные школы и junior команды',reason='Первый проход 16 школ / 13 стран; нужен более широкий аудит кампусов, языка, результатов последних сезонов и иностранного приёма.',url=''))
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/schools-audit-v20.json').write_text(json.dumps(d['school_focus'],ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(schools=len(schools),countries=len({s['iso'] for s in schools}),events=len(d['events'])),ensure_ascii=False))
