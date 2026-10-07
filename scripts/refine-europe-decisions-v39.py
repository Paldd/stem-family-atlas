"""Family decision pass: present-day evidence, future ages and actual team gates."""
import ast, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT.parent / 'stem-family-atlas-work'
path = ROOT / 'data/catalog.json'
d = json.loads(path.read_text())
assert d['completeness_audit']['version'] == 38 and len(d['events']) == 1573
CHECKED = '2026-10-02'
new = []
byid = {e['id']: e for e in d['events']}
for node in ast.parse((ROOT / 'scripts/expand-oceania-v29.py').read_text()).body:
    if isinstance(node, ast.FunctionDef) and node.name in ['ref', 'event']:
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'helpers', 'exec'))

swiss = 'https://wro.swiss/teilnahmebedingungen/'
starter = 'https://wro.swiss/informationen/kategorien-und-altersklassen/wro-starter/'
spain = 'https://www.wroboto.es/competicion/'
faq = 'https://www.wroboto.es/faqs/'
france = 'https://www.coupederobotique.fr/participer-a-la-coupe-junior/'
grenoble = 'https://www.planete-sciences.org/aura/animations/individuel/a-grenoble/stages/'
vendee = 'https://www.planete-sciences.org/vendee/clubs/'

e = event('L351', 'Planète Sciences Grenoble · Construis ton robot · 21–22 октября 2026',
    'Франция', 'Grenoble · Pôle associatif Châtelet, 48 Avenue Washington', grenoble, '8–12 лет для этой смены',
    'Условно: возраст подходит; язык и уровень после трёх лет опыта подтвердить', 'Нет: ниже минимума 8 лет',
    'Два дня 10:00–16:30; до 10–12 детей. Публичная запись через HelloAsso; иностранный приём и язык занятий уточнить.',
    'Электричество, механика и сборка собственного моторизованного робота, который ребёнок забирает домой; программирование в описании этой смены не обещано.',
    block='Лагеря', start='2026-10-21', end='2026-10-22', participation='day_camp',
    priority='P4 — EN / ES и иностранный приём не подтверждены', cost='EUR100 за два дня; обед принести с собой',
    themes=('robotics','technology'), date_scope='camp_window',
    note='Датированная короткая учебная смена. EN / ES не подтверждены; не рекомендована как готовая англоязычная поездка. После трёх лет соревнований проект может оказаться начальным. Это не соревновательный отбор.')
e['region'] = 'Европа'

for id, title, age, mat, osc, gear, note in [
    ('L352', 'Multi Découverte des Sciences', '7–9: среда 13:30–15:00; 10+ отдельная группа',
     'Условно: 9 лет входит в младшую группу; в 2027 перейти в следующую по возрасту на занятии',
     'Сейчас нет: минимум 7; в 2027 после 7-летия — кандидат при сохранении правил',
     'Смешанные научные проекты: механика, электричество, химия и другие темы; не ежедневная робототехника',
     'Нижний возраст научного клуба не равен возрасту команды Coupe Junior. Соревновательный Club Ados на этой же странице начинается с 12 лет.'),
    ('L353', 'Multi Découverte Tech', '10+ по возрасту курса; верхняя граница не опубликована',
     'Будущая ступень: после 10-летия в 2027; текущий возраст 9 ниже минимума', 'Нет: ниже минимума 10 лет',
     'Электричество, робототехника, программирование и 3D-печать; индивидуальные проекты нескольких недель',
     'Это подготовка, а не запись в соревновательную команду: Club Ados / Coupe Junior указан отдельно для 12–17 лет.')]:
    e = event(id, 'Planète Sciences Vendée · '+title+' · регулярный клуб 2026/27',
        'Франция', 'La Roche-sur-Yon · точную площадку подтвердить', vendee, age, mat, osc,
        'Сентябрь–июнь, 90 минут в неделю. При заполнении предлагается лист ожидания. EN / ES, приём внешней семьи и новый сезон подтвердить.', gear,
        block='Лагеря', participation='day_camp', evidence='program',
        priority='P4 — EN / ES и иностранный приём не подтверждены', cost='EUR185 за опубликованный год, включая индивидуальное членство 2026; цена 2027/28 неизвестна',
        note=note+' Старт цикла уже прошёл. На странице есть конфликт weekday/date для Club Ados; точный новый сеанс не назначен в календаре.')
    e.update(region='Европа', participation='regular', format='Регулярный внешкольный клуб; 90 минут в неделю',
        period='Цикл сентябрь 2026–июнь 2027; конкретные доступные сеансы и поздняя запись уточняются')

updated = ['C906','C907']
byid['C906']['cost'] = 'Starter-страница: курс и конкурс бесплатно. Общие условия 2026: CHF150 / team с возвратом после регионального участия. Применяется ли этот платёж к Starter — уточнить; тариф 2027 неизвестен.'
byid['C907']['cost'] = 'Общие условия 2026: CHF150 / team, возвращается после регионального участия при указании банковских реквизитов. Мат / комплект включены по категории и наличию. Условия 2027, робот и поездка отдельно.'
for id in updated:
    e=byid[id]; e['checked']=CHECKED
    e['note'] += ' Повторно прочитаны условия: один ребёнок может участвовать только в одной категории / команде за сезон WRO Switzerland. Общая регистрация 2026 требует CHF150 с возвратом; у Starter есть отдельное обещание бесплатного курса и конкурса, расхождение не скрыто.'

p = next(p for p in d['league_guide']['profiles'] if p['id']=='wro-switzerland')
p['requirements'].append('В одном сезоне WRO Switzerland ребёнок входит только в одну команду / категорию; одновременное участие Starter и Elementary не разрешено общими условиями 2026.')
p['cost'] = '2026: общие условия CHF150 за команду с возвратом после регионального турнира. Starter отдельно объявлен бесплатным — применимость первоначального платежа уточнить. Правила и тарифы 2027 неизвестны.'
for s in p['sources']:
    if s['url'] in [swiss, starter]: s['checked']=CHECKED

f = d['europe_focus']; f['version']=39; f['checked']=CHECKED
f['decision_note'] = 'Это рекомендация для вашей семьи по доступному языку, возрасту и входу в действующую команду. Сравнительный мировой рейтинг качества школ не установлен; свободные места не подтверждены.'
f['decisions'] = [
    dict(id='base', title='Постоянная база и две команды', country='Испания',
        conclusion='Первый кандидат для пробного триместра — Испания. Подбирать город по наставнику и фактической команде Elementary, затем школу.',
        mat='Matвей: автономная RoboMission Elementary или собственный продукт Future Innovators Elementary; нужен напарник минимум 8 лет.',
        osc='Оскар: RoboBasic 6–12 и собственный инженерный проект. В 2027 ему исполняется 7 — Elementary ещё рано.',
        gate='Два брата могут идти вместе в RoboBasic, но для глубокой подготовки Матвея лучше отдельная более сильная категория. Независимая команда разрешена; иностранная мировая квота ещё не подтверждена.',
        event_ids=['C910','C911','L336'], source_urls=[spain,faq]),
    dict(id='camp', title='Короткая семейная проба на английском', country='Франция · Париж',
        conclusion='ABI Haunted STEAM Lab 26–30 октября 2026 — конкретная двуязычная смена с отдельными группами для обоих детей.',
        mat='Inventor 9–12: заранее согласовать сложность, долю кода и проект для ребёнка с трёхлетним соревновательным опытом.',
        osc='Explorer 5–8: отдельная младшая дорожка; оба ребёнка могут учиться в одной локации.',
        gate='Это обучение, а не национальный отбор. По опубликованному тарифу двое за полную неделю — EUR980, без жилья и поездки. Места и иностранный приём подтвердить.',
        event_ids=['L230'], source_urls=[byid['L230']['source'],'https://abischool.fr/holiday-workshops']),
    dict(id='vex', title='VEX IQ и английская школьная среда', country='Швейцария · Zürich / Basel',
        conclusion='Для Матвея TechLabs Competition Lab 9–14 — конкретная подготовка на EN/DE. Школа и соревновательная команда проверяются отдельно.',
        mat='Конструирование, код, журнал и командная работа; в Zürich опубликовано 16 субботних занятий по 90 минут за CHF720.',
        osc='Оскар ниже минимального возраста этого Competition Lab. Нужна отдельная младшая группа; возраст курса не является общей нижней границей мировой VEX IQ.',
        gate='CHF720 / 16 занятий = CHF45 за 90 минут, арифметика по опубликованному циклу. Alpine 2027 не принимает нешвейцарские команды; внешняя запись на курс не устанавливает национальный допуск.',
        event_ids=['L331','L330','L296','C549'], source_urls=[byid['L331']['source'],byid['C549']['source']])
]
for q in f['decisions']: q['mat']=q['mat'].replace('Matвей','Матвей')
f['age_route_note'] = 'Возраст здесь — сколько исполняется в календарном году, по годам рождения 2017 и 2020. Будущие категории — прогноз при сохранении сегодняшних правил, не объявленные турниры. WRO использует календарный год; лагеря, школьные классы и другие лиги могут проверять день рождения или класс.'
f['age_routes'] = [
    dict(year=2026, mat_age=9, osc_age=6, mat='Elementary / VEX IQ при допуске команды.', osc='RoboBasic (ES), Starter (CHE), младшие учебные проекты.', together='В WRO Elementary вместе нельзя: Оскар младше 8. Возможна общая RoboBasic / Starter при соответствии национальным правилам и уровню.', technical='Матвею найти второго ребёнка своей категории; Оскару дать собственную механику и код, а не вспомогательную роль.'),
    dict(year=2027, mat_age=10, osc_age=7, mat='WRO Elementary; технический пансион Brillantmont 10–16 после достижения возраста и проверки места.', osc='RoboBasic / Starter. Junior Robotics Lab 7–9 — возможная подготовка после 7-летия; новый набор неизвестен.', together='Elementary всё ещё требует разных команд. Пансион 10+ подходит только Матвею по будущему возрасту; семейный дневной лагерь проще для обоих.', technical='Начать текстовый код для задач робота, измерения и журнал тестов; выбирать новую LEGO / FIRST ветку только по конкретному местному запуску.'),
    dict(year=2028, mat_age=11, osc_age=8, mat='Последовательно усиливать Elementary; переход Junior допустим по правилам выбранной категории, но не обязателен.', osc='Впервые входит в WRO Elementary по текущему минимуму 8 лет.', together='Первое возможное общее окно Elementary: 11 и 8. Общая команда имеет смысл только при самостоятельной работе обоих и местном допуске.', technical='Разделить ответственность: механика, код, тесты и защита. Совместный продукт — второй проект, а не ещё одна обязательная лига.'),
    dict(year=2029, mat_age=12, osc_age=9, mat='Последний календарный год Elementary по нынешней верхней границе 12.', osc='Elementary; набирать собственный автономный код и инженерный журнал.', together='Второе и последнее общее окно Elementary по нынешним правилам: 12 и 9.', technical='Цель — сильный национальный результат и квалификация по квоте; медаль не гарантируется поездкой на международный этап.'),
    dict(year=2030, mat_age=13, osc_age=10, mat='WRO Junior по нынешним правилам; следующий шаг выбирать по интересу к автономии, электронике или продуктам.', osc='Остаётся в Elementary.', together='Снова разные возрастные категории. Общая мастерская и семейный продукт возможны; соревновательные команды отдельные.', technical='Сохранить глубину в одной основной лиге, открытый код / журнал и самостоятельный проект с реальным пользователем.')
]
f['selection_checks'] = [
    dict(title='Одна действующая команда', detail='Получить team code, возрастную категорию, имя нынешнего наставника и протоколы трёх последних сезонов. Награда старшей команды не доказывает младший путь.'),
    dict(title='Два самостоятельных участника', detail='Пробное занятие для каждого: что ребёнок сам строит, программирует и объясняет? Три года опыта требуют проверки сложности, особенно у вводных лагерей.'),
    dict(title='Язык технической работы', detail='Подтвердить язык наставника, кода / объяснений, защиты и судейства выбранной группы. Английский язык школы или сайта не подтверждает язык турнира.'),
    dict(title='Полный бюджет и допуск', detail='Отдельно считать школу, клуб, набор, поле, регистрационные платежи, поездки и проживание. Школьное место, запись в клуб и национальная квота — отдельные подтверждения.')
]
fra=next(c for c in f['countries'] if c['iso']=='FRA')
fra['event_ids'] += [e['id'] for e in new]
fra['camp'] += ' Grenoble 21–22 октября: моторизованный робот 8–12, EUR100, EN/ES неизвестен. Vendée: научный клуб 7+, Tech 10+, 90 минут в неделю / EUR185 за год; соревновательный клуб отдельно 12–17.'
fra['risk'] += ' Порог лиги Junior 8 лет не гарантирует вход в конкретный клуб: Club Ados Vendée имеет минимум 12. Французские группы не считаются EN по языку сайта.'
che=next(c for c in f['countries'] if c['iso']=='CHE')
che['budget'] += ' WRO2026: общие условия требуют CHF150 с возвратом после регионального участия; Starter отдельно объявлен бесплатным, применение платежа уточнить. Цена 2027 неизвестна.'
che['risk'] += ' По правилам WRO2026 ребёнок участвует только в одной команде / категории за сезон.'
f['limitations'] = 'Пятый ограниченный проход CHE / ESP / FRA. 174 карточки трёх стран включают регулярные программы, будущие кандидаты и несколько смен одних операторов. Полный национальный календарь и мировой рейтинг школ за 5–10 лет не установлены. Будущая возрастная схема — прогноз; даты 2027/28 и национальный допуск подтверждают отдельно.'

fresh = [(swiss,'WRO Switzerland: плата и одна команда за сезон'),(starter,'WRO Starter: отдельное обещание бесплатного участия'),(spain,'WRO Spain: категории и календарный возраст'),(faq,'WRO Spain: независимые команды'),(france,'Coupe Junior: местный вход и возраст'),(grenoble,'Grenoble: робототехническая смена 21–22 октября'),(vendee,'Vendée: разные возрастные пороги учебных и конкурсного клубов')]
for key in ['sources']:
    lookup={s['url']:s for s in d[key]}
    for url,title in fresh:
        if url in lookup: lookup[url]['checked']=CHECKED
        else: d[key].append(dict(url=url,title=title,checked=CHECKED,evidence='Прочитан первичный источник; язык, архивные цены и будущий допуск не подразумеваются.'))
focus_sources={s['url']:s for s in f['sources']}
for url,title in fresh:
    if url in focus_sources: focus_sources[url]['checked']=CHECKED
    else:f['sources'].append(dict(url=url,title=title,checked=CHECKED))

a=d['completeness_audit'];a['validation_previous']=a['validation']
a.update(version=39,checked=CHECKED,status='partial',scope='CHE / ESP / FRA: семейный выбор базы, возраста 2026–2030 и реальные пороги команд / клубов',
    conclusion='3 дополнительные французские учебные программы; 2 уточнения стоимости WRO Switzerland и правила одной команды. Добавлены 3 семейных сценария и возрастный маршрут до 2030. 174 карточки CHE / ESP / FRA; мировой охват частичный.',
    new_ids=[e['id'] for e in new],new_profiles=[],updated_ids=updated,updated_profile_ids=['wro-switzerland'],new_school_ids=[],validation=dict(version=39,status='pending',publication='pending'))
a['source_issues'].append(dict(name='Swiss Starter fee conflict / actual local club minimum',status='Starter says free; general2026 terms CHF150 refundable. Vendée junior competition club starts12 despite national league page8. Both exact distinctions retained.',official_alternative=swiss,checked=CHECKED))
a['caveats'].append('v39: возрастный маршрут 2026–2030 рассчитан по текущим правилам и не создаёт будущих дат турниров. Возможное общее окно WRO Elementary братьев — 2028/29; иностранная квота не подтверждена.')
d['camp_focus']['validation_previous']=d['camp_focus']['validation']
d['camp_focus'].update(version=39,checked=CHECKED,added_ids=[e['id'] for e in new],updated_ids=[],validation=dict(version=39,status='pending'),conclusion='353 лагерных / учебных карточки. 3 новых France: датированный моторизованный робот8–12 и regular7+ /10+. EN/ES неизвестен; семейная ICS не включает эти неподтверждённые языковые варианты.')
d['expansion_log'].append(dict(version=39,checked=CHECKED,added=3,updated_ids=updated,note='CHE / ESP / FRA family decisions, five age years, Swiss refundable fee conflict, actual French learning versus competition club gates.'))
d['events'].extend(new)
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
receipts=json.loads((W/'sources-europe-decision-v39/receipt.json').read_text())
(ROOT/'data/europe-decision-source-receipts-v39.json').write_text(json.dumps(dict(checked=CHECKED,method='Primary HTML read; raw sources outside repo. Inference and arithmetic labelled, no registration.',sources=[{k:r[k] for k in ['name','url','status','resolved','mime','bytes','sha256','error'] if k in r} for r in receipts]),ensure_ascii=False,indent=2)+'\n')
rp=ROOT/'data/research-plan.json';r=json.loads(rp.read_text());r.update(updated=CHECKED,status='active',completeness_audit='data/audit-v39.json')
r.setdefault('research_passes',[]).append(dict(version=39,checked=CHECKED,scope='CHE / ESP / FRA decision and age gates',added_records=3,new_profiles=0,new_schools=0,new_school_results=0,status='partial',remaining='School / team places, foreign quota, camp language and unannounced future editions; full world coverage'))
r['latest_validation_previous']=r.get('latest_validation',{});r['latest_validation']=dict(version=39,status='local_checks_pending_publication_pending')
for q in r['requirements']:
    if q['id']=='unified_database':q['evidence']='v39:1576 records;120 profiles,36 schools,118 history results. Three family decision scenarios / five forecast age years in Europe web and downloadable database.'
    if q['id']=='camps':q['evidence']='v39:353 learning/camp records;3 additional France programmes have unconfirmed EN/ES and remain outside family ICS.'
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(version=39,new=3,updated=updated,total=len(d['events']),world_complete=False)))
