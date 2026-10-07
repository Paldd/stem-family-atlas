"""Family decision audit: CHE / ESP / FRA, without inventing future camp dates."""
import ast, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent / 'stem-family-atlas-work'
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert len(d['events']) == 1616 and d['completeness_audit']['version'] == 41
CHECKED = '2026-10-02'
new = []
byid = {e['id']: e for e in d['events']}
urls = json.loads((WORK / 'urls-europe-family-v42.json').read_text())
for n in ast.parse((ROOT / 'scripts/expand-oceania-v29.py').read_text()).body:
    if isinstance(n, ast.FunctionDef) and n.name in ['ref', 'event']:
        exec(compile(ast.Module(body=[n], type_ignores=[]), 'helpers', 'exec'))

def learning(id, title, city, key, age, mat, osc, gear, note, cost='',
             country='Испания', start='', end='', languages=(), mode='unconfirmed',
             priority='P2 — после проверки группы', regular=False):
    e = event(id, title, country, city, urls[key], age, mat, osc,
        'Подтвердить конкретную группу, уровень после трёх лет соревнований, язык технических объяснений, внешнюю запись и места.',
        gear, block='Лагеря', participation='day_camp', start=start, end=end,
        date_scope='camp_window', languages=languages, note=note,
        cost=cost or 'Стоимость выбранной группы пока не подтверждена', priority=priority, evidence='program')
    e.update(region='Европа', language_mode=mode)
    if regular:
        e.update(participation='regular', format='Регулярная учебная программа; отдельная запись в соревнования')
    if languages:
        e.update(language='У этой программы опубликован '+ '/'.join(languages)+'; роль языка указана отдельно.',
                 language_certainty='Подтверждение относится к указанной программе и сезону.')
    return e

for id,group,mat,osc in [
    ('L378','6–9','Условно: верхняя граница; более сложная группа 9–11 отдельно', 'Условно: возраст подходит; нужен опытный поток'),
    ('L379','9–11','Условно: возраст подходит; проверить самостоятельный код и уровень', 'Нет: ниже минимума 9 лет')]:
    e=learning(id,'ROBBO Barcelona · робототехника '+group+' · курс 2026/27',
        'Barcelona · Hot-Spot Creative Space, Carrer de Pere IV 192','robbo_home',group,mat,osc,
        'ROBBO Lab / Platform, механика, сенсоры, электроника и 3D; входной практический тест по уровню.',
        'Текущий набор идёт с октября по июнь. На главной и странице цен время старшей будничной группы различается: 18:30 / 19:00. Субботние группы ещё формируются. Старые страницы показывают другой адрес и тариф 2025/26. EN/ES/RU регулярного курса прямо не установлены; языки дня рождения не перенесены на курс. Соревновательная команда WRO / VEX и результаты не подтверждены.',
        'EUR200 за 8×55 минут дважды в неделю либо EUR150 за 4×85 минут еженедельно; проба EUR5. Это пакеты занятий, не календарный месяц.',regular=True)
    e['references']=[ref('Тарифы 2026/27 и различия расписания',urls['robbo_fees'])]
    e['period']='Курс октябрь 2026 — июнь 2027; конкретный слот и поздний вход подтвердить'
e=learning('L380','ROBBO Barcelona · субботний технологический мастер-класс · начало 3 октября',
    'Barcelona · Hot-Spot, Carrer de Pere IV 192','robbo_home','6–9 / 9–11 / 12–15, отдельные группы',
    'Условно: две возрастные группы пересекаются, нужен уровень','Условно: младшая группа 6–9',
    'Один проект: роботы, Scratch / Minecraft, цепи или 3D; точная тема дня отдельно.',
    'Опубликовано начало с 3 октября 2026, 11:45–13:15. Открытие зависит от минимального числа участников; проведение именно первого дня и язык ещё подтвердить. Не создана вымышленная серия всех суббот.',
    'EUR30 за 90 минут; EUR100 за четыре последовательных занятия',start='2026-10-03',priority='P4 — группа и язык ещё не подтверждены')
e['date_scope']='activity_start'
e=learning('L381','ROBBO Barcelona · зимний лагерь · ждать объявления',
    'Barcelona · новый адрес смены уточняется','robbo_home','Новый возрастной регламент ещё не опубликован',
    'Не подтверждено: правила зимней смены ожидаются','Не подтверждено: правила зимней смены ожидаются',
    'Робототехника / технологии по направлению клуба; программа зимнего лагеря ещё не опубликована.',
    'Главная обещает подробности зимнего лагеря в ноябре. Старый летний лагерь 2026 имел группы 6–8 и 9–13, но это не возраст, адрес, цена или языки зимней смены.',priority='P3 — ждать зимнего объявления')
e['period']='Зимние каникулы; точные даты не объявлены'
e['references']=[ref('Архив летнего лагеря 2026',urls['robbo_camp'])]

e=learning('L382','St George Barcelona · Robotics Summer Camp 2026 · архив',
    'Barcelona · Paseo de la Reina Elisenda de Montcada 18 bis','sgb_camp','6–10 лет',
    'Архив: возраст подходил; набор завершён','Архив: возраст подходил; набор завершён',
    'Робототехника, программирование и 3D-дизайн; собственные недельные проекты.',
    'Школа прямо называет робототехнический поток английским и открытым детям других школ. 6–31 июля 2026 — общая рамка четырёх недель, не непрерывный лагерь с выходными. Это архив для выбора следующего сезона.',
    '2026: EUR330 / неделя, 645 / две, 950 / три, 1240 / четыре; новые цены неизвестны.',
    start='2026-07-06',end='2026-07-31',languages=('EN',),mode='primary',priority='P4 — прошедший сезон')
e['references']=[ref('Брошюра явно датирует сезон 2026',urls['sgb_brochure'])]
e=learning('L383','St George Barcelona · английская робототехника 6–10 · следующий лагерь',
    'Barcelona · будущую площадку и смену подтвердить','sgb_camp','Архив 2026: 6–10; правила следующего сезона неизвестны',
    'Условно: в 2027 исполнится 10; нужна дата отсечения и новая смена','Условно: в 2027 исполнится 7; новый регламент ещё не объявлен',
    'Архивная техническая программа на английском: роботы, код, 3D; новый состав занятий подтвердить.',
    'Это кандидат на следующий набор. Указанные на странице даты относятся к брошюре 2026. Английский подтверждён прошлому робототехническому потоку; язык, возраст, место, цена и даты 2027 пока не обещаны.',priority='P3 — ждать сезона 2027')
e['language']='EN прямо подтверждён сезону 2026; язык следующего лагеря ещё не объявлен'
e['references']=[ref('Архивная брошюра 2026',urls['sgb_brochure'])]
e['period']='Следующий летний набор; даты 2027 ещё неизвестны'

e=learning('L384','Petit Univers · Future School Lab · 8–12 февраля 2027',
    'Saint-Maur-des-Fossés · 6 Avenue des Arts','pu_camp','7–12 лет',
    'Условно: по возрасту подходит; язык утренней технической части проверить',
    'Только после 7-летия; точная дата рождения неизвестна',
    'Утром робототехника, программирование и макет школы; после обеда английская речь и финальная презентация.',
    '09:00–17:00, обед с собой, материалы предоставляются. Английский описан как отдельная часть дня и презентация; английское преподавание утреннего кода не подтверждено. Упоминание STEM не является доказательством соревновательного отбора.',
    'EUR360 за пять дней на ребёнка',country='Франция',start='2027-02-08',end='2027-02-12',languages=('EN',),mode='language_lessons',priority='P4 — технический EN / ES не установлен')
e['language']='EN — занятия языком и презентация; язык технической части неизвестен'

e=learning('L385','AI Kids Club Alicante · летний проектный лагерь 2027 · ждать дат',
    'Alicante · место 2027 ещё не объявлено','ai_camp','2026: 8–12; возраст лагеря 2027 ещё объявят',
    'Не подтверждено: новый возраст / группа ожидаются','Не подтверждено: диапазон 2027 ожидается; общий клуб 7+ не правило лагеря',
    'Собственные приложения, игры и истории с AI, тестирование и семейный Demo Day; физические роботы не обещаны.',
    'Организатор анонсировал одну интенсивную неделю летом 2027. Английский с испанской помощью, EUR250 и MiCampus относятся к июлю 2026. Не перенесены на 2027. Страница лагеря упоминает weekly start 7 октября / EUR100, но главная относит новый Online Lab к coming soon: конкретный еженедельный набор не считается подтверждённым.',priority='P3 — ждать дат, языка и возрастов')
e['themes']=['ai','coding','games','technology']
e['period']='Лето 2027; даты / цена / возраст / язык ещё ожидаются'
e['references']=[ref('Текущие школьные программы и статус Online Labs','https://aikidsclub.org/en')]
e=learning('L386','AI Kids Club · школьные AI Labs · 7–14',
    'Alicante · школа-партнёр выбирает расписание и запись','ai_home','7–9 / 9–12 / 12–14',
    'Условно: возраст подходит; доступ внешнего ребёнка через школу отдельно','Нет сейчас: минимум 7; после 7-летия нужна конкретная группа',
    'Создание и проверка собственных AI-приложений, игр, комиксов; итоговая презентация семье.',
    'Главная прямо описывает школьное преподавание на EN с ES-помощью либо целиком на ES по выбору школы. Цена и запись через школу-партнёра. Это отдельный учебный трек, не WRO / VEX и не мировой чемпионат. Online Labs ещё coming soon.',languages=('EN','ES'),mode='primary',regular=True)
e['themes']=['ai','coding','games','technology']
e['language']='Школьный поток EN с ES-помощью или полностью ES; выбрать конкретную группу'

# Exact league and exhibition gates; keep dates that are actually announced.
byid['C906']['references'].append(ref('FAQ: Starter не даёт международной квалификации',urls['swiss_faq']))
byid['C906'].update(checked=CHECKED,reward='Место местного / швейцарского Starter по протоколу; международной квалификации нет',
    note=byid['C906']['note']+' FAQ прямо исключает международный отбор Starter. В 2026 в Swiss Final выходили лучшие 1–2 команды площадки по числу участников; это не будущая квота 2027.')
byid['C907']['references'].append(ref('FAQ: слишком молодой участник и запрет международной квалификации',urls['swiss_faq']))
byid['C907']['references'].append(ref('Национальный протокол: возраст, место и вид квоты',urls['swiss_results']))
byid['C907'].update(checked=CHECKED,note=byid['C907']['note']+' FAQ допускает местное исключение для отдельного слишком молодого участника, но такая команда не может квалифицироваться международно. Для совместного мирового Elementary-маршрута братьев ждать нынешнего возрастного окна 2028–2029.')
byid['E142'].update(checked=CHECKED,city='Lyon · Eurexpo (площадка 2027; старые правила описывают Centre de Congrès)',
    visitor_policy='adults_only',age='Последние опубликованные правила: 18+; студенческие исключения старших отдельно',
    mat='Нет по опубликованному правилу 18+; нового исключения 2027 не объявлено',osc='Нет по опубликованному правилу 18+; нового исключения 2027 не объявлено',
    priority='P4 — только взрослым по текущим правилам',
    entry='Для взрослого профильного посетителя — проверка профессионального бейджа. Условия детского исключения не опубликованы.',
    visitor_note='Страница условий прямо запрещает младше 18; календарные и студенческие детали там ещё относятся к 2026. На 2027 семейный вход не обещан.',
    note='Французская главная объявляет 15–16 сентября 2027 в Eurexpo; английская ещё показывает 2026. Страница входа запрещает младше 18 и описывает специальные студенческие часы 2026. Эти часы не перенесены на 2027. Дети исключены из семейного ICS; событие остаётся в отдельном календаре выставок.',
    references=[ref('Объявление 2027: дата и Eurexpo',urls['sido_french']),ref('18+ и старые детали 2026',urls['sido_rules'])])
byid['E140'].update(checked=CHECKED,note=byid['E140']['note']+' Дата 13 ноября 2026 и StageOne повторно подтверждены. Категория Students относится к BSc/MSc/PhD, не к детям 6/9.')
byid['E141'].update(checked=CHECKED,references=byid['E141']['references']+[ref('Новый сезон 15–18 марта 2027',urls['global_industrie'])])
byid['E145'].update(checked=CHECKED,visitor_note='Исключительно профессиональная выставка; допуск детей 6/9 не установлен. Студенческий день относится к финальным курсам degree / masters, а не Primaria.')

newschool=dict(id='S041',name='St George Barcelona',iso='ESP',country='Испания',region='Европа',city='Barcelona · Sarrià',school_type='private',
    curriculum='English National Curriculum 5–11; обязательные испанский и каталанский. IB Diploma — старшая программа по сообщению школы, не Primary IB.',
    ib_programmes=[dict(programme='DP',status='school_report')],ages='Primary 5–11; полная школа 2–18',instruction_languages=['EN'],
    language_note='EN прямо назван основным языком обучения в брошюре 2026/27; ES и Catalan входят в программу.',
    fit=dict(mat='candidate',osc='candidate',note='Оба кандидаты Primary; фактический Year определяет школа, точные дни рождения и классы неизвестны.'),
    boarding='unknown',boarding_note='Дневной семейный кандидат; младший пансион не установлен.',
    programme='ICT в Primary, робототехнический кружок Ignite и английский лагерь 6–10 по брошюре 2026. Действующая команда 2026/27, league/team code и призовые результаты не установлены.',
    labs='В лагере роботы, программирование и 3D; недельные часы и оборудование регулярного младшего клуба отдельно.',
    ai='Непрерывный младший AI-трек и техническая сложность не подтверждены.',results=[],evidence='programme',
    admissions='Primary допускает обращения весь год. Место, распределение по Year и включение в роботокоманду — отдельные решения школы.',
    cost='PDF 2026/27: Year1–2 EUR15180, Year3–4 EUR17500, Year5–6 EUR17750 в год. Если Оскар в Year1–2, Матвей в Year3–6: EUR32680–32930 tuition за двоих. Первое зачисление +EUR3500 на каждого, итого EUR39680–39930 до транспорта / клубов. EUR1000 enrolment зачтён в сентябрьской плате по PDF, не добавлен повторно. HTML объединяет Year3–6 по17500, поэтому расчёт использует подробный PDF. Тариф 2027/28 неизвестен.',
    questions=['Какие реальные Year, места и языковая поддержка подходят обоим?', 'Какой действующий младший team code, наставник, часы и результаты за три сезона?', 'Входит ли Ignite / соревнование в этот тариф? Какие платформа и уровень после трёх лет опыта?', 'Как зачтут EUR1000 при зачислении посреди года и какой полный индивидуальный счёт?'],
    sources=[dict(title=t,url=urls[k],claim=c,kind='school',checked=CHECKED) for t,k,c in [
        ('Primary 5–11 и ICT','sgb_primary_actual','Школьная ступень и учебная программа'),('Тариф и EN инструкция 2026/27','sgb_fee_pdf','Подробные Year / зачёт enrolment / основной EN'),('Текущая таблица цен','sgb_fees','HTML и PDF расходятся для Year5–6'),('Робототехнический кружок и лагерь 2026','sgb_brochure','Ignite / 6–10; не победа соревнования'),('Внешние дети и английский лагерный поток','sgb_camp','Открыт детям других школ')]],
    checked=CHECKED,priority=2,research_status='partial',verification='Прочитаны школа и тарифный PDF; мировой младший результат и доступ в команду не доказаны.')
d['schools'].append(newschool)
h=d['school_history']
for eid,name in [('CHE-STARLIGHT-FI','StarLight · Future Innovators Elementary'),('CHE-ROBOLIX-E','Robolix · RoboMission Elementary')]:
    h['entities'].append(dict(id=eid,name=name,kind='unresolved',country='Швейцария',age='primary',school_id=None,note='Школа, клуб и нынешний наставник в протоколе не указаны. Совпадение имени с другой категорией не доказывает ту же команду.'))
for id,eid,category,team,award,note in [
    ('H132','CHE-STARLIGHT-FI','Future Innovators Elementary','StarLight','1-е место и квалификация на International Final','160.25 балла. В протоколе FI возрастные категории сведены в одну таблицу; первое место этой Elementary-команды не названо отдельной мировой победой.'),
    ('H133','CHE-ROBOLIX-E','RoboMission Elementary','Robolix','2-е место; квота на Open Championship Zagreb','404 балла. В этом протоколе две звёздочки означают Open Championship, одна — International Final. Эти события не равны.')]:
    h['results'].append(dict(id=id,entity_id=eid,year=2026,league='WRO',category=category,stage='Swiss National Final · 20 июня 2026',award=award,level='national_other',source=urls['swiss_results'],team=team,team_id=None,provenance='organizer_protocol',note=note,checked=CHECKED))
h.update(version=42,checked=CHECKED,conclusion='133 отдельных результатов. Новые швейцарские записи разделяют национальное место, International Final и Open Championship; школа двух команд неизвестна. Полный рейтинг младших школ за 5–10 лет не установлен.')

d['events']+=new
f=d['europe_focus'];f.update(version=42,checked=CHECKED,
    conclusion='Мой первый европейский кандидат для вашей семьи — Испания: понятный независимый WRO-маршрут и испанский детей. Швейцария — сильная проба EN/DE VEX и дорогая школьная среда; братьев пока готовить раздельно. Франция — конкретная двуязычная проба в Париже, но выбирать технический EN-поток отдельно от английских уроков.',
    limitations='Седьмой ограниченный проход трёх стран: 194 карточки и 17 школьных досье. Новые учебные варианты, тариф 2026/27, швейцарские протоколы и ограничения SIDO проверены. Это частичный семейный аудит, не полный национальный календарь или измеренный мировой рейтинг школ.')
countries={c['iso']:c for c in f['countries']}
countries['ESP']['event_ids'] += [e['id'] for e in new if e['country']=='Испания']
countries['ESP']['school_ids'].append('S041')
countries['FRA']['event_ids'].append('L384')
countries['ESP']['camp']+=' St George Barcelona: EN-робототехника 6–10 и внешние дети подтверждены только лету 2026; следующий сезон недатирован. ROBBO ожидает зимние подробности в ноябре; AI Kids Alicante анонсирует лето 2027 без возраста / языка / дат.'
countries['ESP']['school']+=' St George Barcelona добавлен как EN Primary с робототехнической программой, без подтверждённого мирового титула.'
countries['ESP']['city_route']+=' Barcelona: ROBBO теперь Hot-Spot / Pere IV192, новый набор 2026/27; язык регулярного курса подтвердить. Старый адрес Via Laietana не перенесён на новый курс.'
countries['ESP']['budget']+=' St George PDF 2026/27 даёт EUR32680–32930 tuition за двоих при условном размещении Year1–2 / Year3–6; зачисление отдельно. Year5–6 дороже общей HTML-таблицы.'
countries['CHE']['risk']+=' Starter прямо не даёт международной квалификации. Местное исключение для слишком молодого Elementary-участника лишает такую команду международного отбора.'
countries['CHE']['results_check']+=' StarLight FI Elementary — первое место общей FI-таблицы и International Final; Robolix RM Elementary — второе и Open Zagreb. Школы неизвестны.'
countries['FRA']['camp']+=' Petit Univers 8–12 февраля2027: 7–12, EUR360, робототехника утром и английский после обеда. Полный технический EN не установлен; Оскару нужно уже исполниться7.'
countries['FRA']['risk']+=' SIDO: опубликованный запрет младше18; правила ещё2026, площадка2027 уже Eurexpo. Семейная поездка сюда не рекомендована без нового явного исключения.'
f['base_comparison']=[
    dict(iso='ESP',country='Испания',label='Первый кандидат для пробного триместра',
        conclusion='Ваша языковая подготовка подходит. Выбирать город по действующему наставнику и двухдетному маршруту, потом школу.',
        mat='WRO Elementary сейчас; параллельно собственный AI / программный продукт. Один основной чемпионат на сезон.',
        osc='RoboBasic и самостоятельный младший проект; Elementary по нынешним правилам с 2028.',
        school='Colegio Lar / Highlands — проверить нынешнюю команду и язык; St George / St PETER’S — школьная среда, роботонаставник отдельно.',
        budget='Пример частной EN-школы St George: EUR32680–32930 tuition за двоих в 2026/27 при указанных Year; первый год с зачислением EUR39680–39930. Это пример, не средняя цена страны.',
        trial='Сначала 2–4 недели у конкретного наставника. ROBBO предлагает короткие пакеты и тест уровня; его участие в WRO / VEX ещё не доказано.',
        gate='WRO разрешает независимую команду из 2–3 детей; это не подтверждает иностранную квоту. Местная регистрация закрывается за15дней или раньше при заполнении.',
        event_ids=['C910','C911','L378','L379'],school_ids=['S041','S027'],source_urls=[urls['spain_faq'],urls['sgb_fee_pdf'],urls['robbo_home']]),
    dict(iso='CHE',country='Швейцария',label='Техническая проба VEX; база после проверки бюджета',
        conclusion='Для Матвея найден конкретный EN/DE Competition Lab. Швейцарская научная среда интересна, но школьная лаборатория не гарантирует команду детям6/9.',
        mat='TechLabs Competition Lab9–14 и Elementary / VEX при правилах площадки; искать напарника нужной категории.',
        osc='Младший TechLabs / Ecolint и WRO Starter6–10. Starter имеет местный финал, международной квалификации нет.',
        school='IS Basel — проверить текущую Junior-команду; ISZL / Ecolint — EN Primary; TASIS приз относится к Middle School.',
        budget='Ранее прочитанный ISZL2026/27: CHF66400 tuition за двоих в Grades1–5, первый год CHF76400 до дополнений. Zürich Competition Lab CHF720 /16×90мин отдельно. Полный семейный бюджет не установлен.',
        trial='Согласовать пробный урок Матвея в Competition Lab и младшую группу Оскара; затем 2–4 недели школы. Alpine2027 принимает швейцарские команды.',
        gate='Слишком молодой участник может получить местное WRO-исключение, но такая команда не квалифицируется международно. Совместное Elementary-окно братьев по нынешним правилам2028–2029.',
        event_ids=['L331','L296','C906','C907','C549'],school_ids=['S023','S033','S037'],source_urls=[urls['swiss_faq'],urls['swiss_results']]),
    dict(iso='FRA',country='Франция',label='Каникулы и проба; база зависит от языковой адаптации',
        conclusion='У обоих есть двуязычная ABI-смена и регулярные EN-варианты. Для школы без французского сначала проверить конкретный класс и степень погружения.',
        mat='EN Scratch / Python / робототехнический проект; Coupe Junior / RoboCup требуют отдельно язык защиты, класс и команду.',
        osc='ABI5–8, Union младшие занятия, Tech Kids bilingual5–6. Нельзя заменить инженерную роль только английскими уроками.',
        school='ABI / Union — двуязычные младшие; Marymount — EN и FabLab. Младший мировой титул этих выбранных школ не установлен.',
        budget='ABI Haunted26–30октября: EUR980 за двоих по опубликованному недельному тарифу; жильё отдельно. UnionAcademyEUR2100 — внешкольный пакет, не годовая школа. Сопоставимый школьный счёт обоим ещё нужен.',
        trial='Париж: ABI Haunted26–30октября2026 или регулярный EN-поток TechKids. PetitUnivers7–12февраля? Точные даты смены8–12февраля2027; технический EN не подтверждён.',
        gate='PetitUnivers предлагает EN после утренней робототехники. SIDO младше18 запрещает в последних опубликованных правилах; семейные альтернативы — Cité / публичные дни.',
        event_ids=['L230','L356','L357','L384','E144','E142'],school_ids=['S025','S030','S038'],source_urls=[urls['pu_camp'],urls['sido_rules']])]
f['base_comparison'][2]['trial']='Париж: ABI Haunted26–30октября2026 или регулярный EN-поток TechKids. PetitUnivers8–12февраля2027 начинается с7лет; технический EN не подтверждён.'
f['comparison_note']='Это мой выбор по языкам, двум возрастам и доступному маршруту, а не рейтинг качества стран. Тарифы, школьное место, клуб, командный допуск и мировая квота проверяются отдельно. Ранее найденные тарифы имеют свои даты проверки в школьных досье.'
f['evidence_cards'].append(dict(title='Швейцария · International Final и Open — разные квоты',detail='Протокол20июня2026: SwissFire — первое RMElementary с мировой квотой, Robolix — второе с OpenZagreb; StarLight — первое общей FI-таблицы, возраст Elementary, квота InternationalFinal.',limit='Это национальные результаты и квоты, не мировые победы. Школы новых команд неизвестны; одинаковые названия разных категорий не объединены.',event_ids=['C907'],school_ids=[],source_urls=[urls['swiss_results']]))
f['evidence_cards'].append(dict(title='Испания · EN-школа и роботолагерь без выдуманной даты2027',detail='StGeorgeBarcelona: основной EN прямо вPDF2026/27; робототехнический лагерь6–10 наEN и внешние дети — архив2026. У Year5–6 PDF дороже общей HTML-таблицы.',limit='Школьная робототехническая программа подтверждена; младшая мировая медаль и место в команде нет. Следующий лагерь не вставлен в ICS.',event_ids=['L382','L383'],school_ids=['S041'],source_urls=[urls['sgb_fee_pdf'],urls['sgb_camp']]))
f['sources'] += [dict(title=title,url=urls[key],checked=CHECKED) for key,title in [
    ('spain_faq','WRO Spain: независимая команда, регистрация и стоимость этапов'),('swiss_faq','WRO Swiss: Starter и исключения младших'),('sgb_camp','St George: английский роботолагерь и внешние дети'),('sgb_fee_pdf','St George: подробные тарифы2026/27'),('robbo_home','ROBBO: новый адрес и набор2026/27'),('robbo_fees','ROBBO: короткие пакеты и группа'),('pu_camp','Petit Univers: разделение техники и English'),('ai_camp','AI Kids: анонс2027 без правил и дат'),('ai_home','AI Kids: язык школьного потока'),('sido_french','SIDO2027: даты и новая площадка'),('sido_rules','SIDO: опубликованный запрет младше18')]]

d['asof']=CHECKED
d['expansion_log'].append(dict(version=42,checked=CHECKED,scope='CHE/ESP/FRA family base comparison / current teaching and visitor gates',added=9,new_schools=1,history_added=2,status='partial; worldwide scope preserved'))
a=d['completeness_audit'];a['validation_previous']=a.get('validation',{})
a.update(version=42,checked=CHECKED,scope='CHE/ESP/FRA: семейный выбор, тарифы, языковые роли, отбор и доступ выставок; также сохранены новые данные Африки v41',
    status='Исследование продолжается',conclusion='Девять новых европейских учебных карточек, одно школьное досье, два швейцарских результата и сравнение баз для обоих детей. SIDO исключён из семейного календаря по опубликованному18+. Все ранее подготовленные африканские данные сохранены; мировой охват остаётся частичным.',
    new_ids=[e['id'] for e in new],new_profiles=[],new_school_ids=['S041'],updated_ids=['C906','C907','E140','E141','E142','E145'],updated_profile_ids=[],
    validation=dict(version=42,status='pending',publication='pending'))
d['camp_focus'].update(version=42,checked=CHECKED,added_ids=[e['id'] for e in new],updated_ids=[],conclusion='386 учебных и лагерных карточек. Новые испанские проекты и французская зимняя смена; EN прошлой смены и английские уроки отдельно от будущего технического EN.',validation=dict(version=42,status='pending'))
d['school_focus'].update(version=42,checked=CHECKED,conclusion='41 школьное досье. StGeorgeBarcelona добавлен как ENPrimary с технологической программой и прочитанным тарифом2026/27; мировой титул не установлен.')
known={s['url'] for s in d['sources']}
for key,url in urls.items():
    if key not in ['sgb_primary','jis_home','robbo_faq','pu_courses','pu_planning','pu_home','sido'] and url not in known:
        d['sources'].append(dict(url=url,title='Первичный источник · '+key,evidence='Прочитан организатор / школа; ограничения и сезон указаны в карточках',checked=CHECKED));known.add(url)
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=[]
for filename in ['receipt.json','receipt-extra.json','receipt-final.json']:
    rows+=json.loads((WORK/'sources-europe-family-v42'/filename).read_text())
receipt=dict(version=42,checked=CHECKED,scope='CHE/ESP/FRA current family routes',fetches=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in rows],
    web_opened=[dict(url=urls['advanced_factories'],note='Direct HTTP403; web.open succeeded. Latest professional/student FAQ read.')],
    conflicts=['StGeorgeHTMLYear3–6vsPDFYear5–6','SIDOFrench2027date/venuevsEnglish2026; entryrulesstill2026','ROBBOcurrent2026/27vslegacy2025/26andoldaddress','AIKidsweeklyOct7/campvsOnlineLabscomingsoon'],
    remaining='Foreign team quotas, actual school/team places, future camps and complete5–10yearschoolranking')
(ROOT/'data/europe-family-source-receipts-v42.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v42.json')
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=42,status='local_checks_pending_publication_pending')
r['research_passes'].append(dict(version=42,checked=CHECKED,scope='CHE/ESP/FRA: practical two-child comparison and age/language/visitor/fee audit',added_records=9,new_schools=1,history_added=2,status='partial',remaining='Futurecohorts,foreignquotas,school/teamplaces,5–10yearschoolranking;fullworldscope'))
r['next_research'].insert(0,'CHE/ESP/FRA v42: подтвердить новые зимние и летние лагеря, реальные текущие младшие команды и языковой поток; иностранную национальную квоту; SIDOправила2027. Остальная цель по миру сохраняется.')
for req in r['requirements']:
    if req['id']=='unified_database':req['evidence']='v42:1625records /125profiles /41schools /133historyresults; CHE/ESP/FRAcomparison andAfricaoverview; worldpartial.'
    elif req['id']=='camps':req['evidence']='v42:386learningrecords; newEuropeanage/languagegates andunannouncedfuturecampsseparate.'
    elif req['id']=='permanent_schools':req['evidence']='v42:41dossiers; StGeorgeEnglishPrimarywithcurrentPDFfees, juniorresultsnotestablished.'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=42,added=9,schools_added=1,history_added=2,records=len(d['events']),world_complete=False)))
