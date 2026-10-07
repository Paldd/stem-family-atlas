"""Refine the existing family strategy; preserve the worldwide inventory."""
import copy, json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'data/catalog.json'
d = json.loads(path.read_text())
assert d['completeness_audit']['version'] == 24
before = {k: copy.deepcopy(d[k]) for k in ['events', 'leagues', 'school_history']}
f = d['family_strategy']
f.update(version=25, checked='2026-10-01',
    conclusion='Главное сравнение для следующей постоянной базы — Мексика и Тайвань: Monterrey / ASFM плюс независимая команда, либо Taipei / TAS и Taichung / AST. Мексика — первый практический визит; Тайвань — первый азиатский кандидат. США можно выбирать уже сейчас, если бизнес семьи, смета и конкретная младшая команда совпадут. Коста-Рика сохраняет регулярную практику на время выбора.',
    decision='Одна постоянная база на 2–3 сезона, отдельная команда и роль каждому ребёнку. Сравнивать доступ к школе, младшей команде и наставнику вместе с проживанием семьи и первым годом расходов.',
    confidence='Средняя: младшие программы найдены, но свободные места, текущие тренеры и самостоятельный уровень детей ещё не подтверждены.')
f['assumptions'][2] = 'Семья готова к переезду и рассматривает несколько оснований проживания. Для выбора принята практическая доступность текущей базы и Мексики; другие основания — рассматриваемые варианты. Индивидуальное миграционное право этим исследованием не установлено.'
bases = {b['iso']: b for b in f['bases']}
bases['MEX'].update(role='Первый практический визит и основной вариант в Латинской Америке', verdict='Первый практический визит',
    recommendation='При доступности жизни в Мексике я бы начинал сравнение с Monterrey. ASFM — кандидат на общую школу обоим, а для Матвея параллельно проверять независимую Challenge / WRO / VEX IQ команду. Школьная младшая Explore сама по себе может не дать ему достаточной сложности после трёх лет опыта.')
bases['TWN'].update(role='Первый азиатский кандидат для постоянной инженерной среды', verdict='Главный азиатский кандидат',
    recommendation='TAS — наиболее цельный найденный азиатский кандидат для обучения обоих от младшей робототехники к старшим лабораториям; AST — второй вариант. Проверять одновременно с Мексикой. Переезд выбирать после мест обоим, текущего junior-тренера и понятной сложности, а не только по наличию Gold Card или наградам старших.')
bases['USA'].update(role='Полноценный вариант сейчас при подходящем бизнесе и младшей команде', verdict='Команда + бизнес + смета',
    recommendation='США не нужно автоматически откладывать до подросткового возраста. Если семья планирует действующий бизнес там и найдёт подходящую junior-команду обоим, это полноценный вариант уже сейчас. При отсутствии такой команды — целевые лагеря / турниры; в 12–18 лет отдельно сравнивать FTC / FRC. Наш нынешний список американских школ не доказывает, что место обоим в младшей команде уже есть.')
bases['USA']['gates'].append('E-2 — неиммиграционный инвесторский путь: гражданство страны договора, существенная инвестиция и действующее предприятие проверяются отдельно. Наличие страны в договорном списке не является одобрением семьи.')
bases['TWN']['gates'].append('Employment Gold Card и зависимый ARC семьи — отдельный путь проживания. TAS независимо требует иностранное гражданство ребёнка, проживание с родителем / опекуном в Greater Taipei и решение admissions.')
f['bases'] = [bases[k] for k in ['MEX', 'TWN', 'USA', 'PAN', 'CRI', 'BRA', 'RUS']]
f['scenarios'] = [
    {'id':'fast','name':'Быстрый переход','iso':'MEX','title':'Коста-Рика → сравнение в Monterrey → одна база',
     'detail':'Проверить ASFM и независимую команду в одной поездке. Если сильный тренер доступен вне школы, выбрать школу по общему качеству и благополучию, а робототехнику — по фактической команде.',
     'mat':'Challenge / WRO / VEX IQ у подходящего наставника; школьная Explore не заменяет проверку сложности.',
     'osc':'Собственная младшая группа: Explore / конструирование / код; личная работа и объяснение проекта.',
     'steps':['Сейчас: сохранить занятия в Коста-Рике и измерить уровень каждого.', 'Ближайшее сравнение: ASFM и внешняя команда; январский приём 2027 указан школой, K–G11 на 2027–28 — с октября 2026.', 'После подтверждения мест и тренера: выбрать один учебный год и один основной соревновательный сезон.']},
    {'id':'asia','name':'Инженерная база в Азии','iso':'TWN','title':'Taipei / TAS против Taichung / AST',
     'detail':'Сравнить полноценную младшую программу и конкретные кружки обоим; старшие AI / fabrication / VEX / FRC показывают дальнейший путь, но их оборудование и команды не обещаются детям 6 / 9 лет.',
     'mat':'Задача с датчиками, собственный код и испытания; junior-команда и её возраст / класс отдельно.',
     'osc':'Младшие механизмы и coding; сверить класс по точному дню рождения, а не только 2020 году.',
     'steps':['До поездки: проверить школьные места, документы и подходящие технические группы.', 'Очное сравнение: урок / мастерская, действующий тренер, расписание, работы ровесников.', 'Постоянная база: только когда решены семейное проживание, приём обоих и полная смета; TAS принимает заявки на 2027–28.']},
    {'id':'business','name':'США и семейный бизнес','iso':'USA','title':'Выбрать город по доступной младшей команде',
     'detail':'Если действующий бизнес семьи и обучение совпадают в одном месте, США могут выиграть уже на нынешнем этапе. Пока город и junior-команда не выбраны, нельзя сделать этот вариант победителем только по масштабу страны.',
     'mat':'Начальная школа / community-команда FLL, WRO или VEX IQ; FTC / FRC — по отдельному возрастному и школьному допуску.',
     'osc':'Поток для 6 лет и собственная роль; лагерь 7–8+ не подходит автоматически.',
     'steps':['Сначала: определить подходящий бизнес семьи и 2–3 реальные junior-команды.', 'Сравнить: школьный округ / частный приём, расписание, тренера и первый год расходов.', 'После подтверждения: одна постоянная команда; поездки и будущие FTC / FRC подбирать по правилам сезона.']},
]
fee_urls = {
 'S002':'https://www.asfm.edu.mx/admissions/tuition-fees',
 'S003':'https://www.tas.edu.tw/admissions/tuition-fees',
 'S022':'https://isp.edu.pa/admissions/',
}
f['cost_comparison'] = {
 'school_year':'2026–2027',
 'note':'Расчёты ниже — ориентир по опубликованным тарифам 2026–27 для двух новых учеников младшей ступени. Классы и счёт школы ещё не определены. Тарифы 2027–28 не объявляются равными этим; валюты не пересчитываются. Жильё, переезд, питание, транспорт, поездки и дополнительные технические занятия в суммы не включены.',
 'schools':[
  {'school_id':'S002','name':'ASFM · Monterrey','iso':'MEX',
   'annual':'MXN 631 290 · обучение обоих',
   'entry':'MXN 65 520 + USD 19 100 · разовые взносы обоих',
   'first':'MXN 696 810 + USD 19 100 · обучение и указанные разовые взносы',
   'formula':'K–Grade 5: 334 620 + 296 670 MXN (старший Child 1, младший Child 2+). Registration 32 760 MXN и entrance USD 9 550 на нового ученика — разовые по странице школы.',
   'components':{'tuition_two_mxn':631290,'registration_two_mxn':65520,'entrance_two_usd':19100,'first_mxn':696810},
   'url':fee_urls['S002']},
  {'school_id':'S003','name':'TAS · Taipei','iso':'TWN',
   'annual':'NT$1 926 540 · обучение и building fee обоих',
   'entry':'NT$720 000 · capital fee и новые заявки обоих',
   'first':'NT$2 646 540 + расходы по классу · первый год',
   'formula':'Pre-K–Grade 5: 956 770 × 2 + building fee 6 500 × 2. Capital 350 000 × 2 и application 10 000 × 2. Enrollment deposit 50 000 уже входит в годовую tuition; повторно не прибавлен. Скидки siblings нет. Обязательный outdoor fee зависит от класса и здесь не включён.',
   'components':{'tuition_two_ntd':1913540,'building_two_ntd':13000,'capital_two_ntd':700000,'application_two_ntd':20000,'annual_ntd':1926540,'first_ntd':2646540},
   'url':fee_urls['S003']},
  {'school_id':'S022','name':'ISP · Panamá','iso':'PAN',
   'annual':'USD 33 168 · обучение и ежегодная registration обоих',
   'entry':'USD 32 500 · полное обязательство capital и новые заявки обоих',
   'first':'USD 65 668 · годовой ориентир с полным capital обязательством',
   'formula':'PK4–Grade 5, Non-Institutional (семья платит без возмещения работодателем): tuition 15 584 × 2 + annual registration 1 000 × 2. Application 250 × 2, capital 16 000 × 2. Capital оплачивается двумя этапами: USD 16 000 на обоих при приёме, ещё USD 16 000 при следующем re-enrollment в марте; USD 65 668 — не единовременный платёж. Для employer-supported семьи другая registration. На странице есть устаревшая строка обработки заявок 2025–26 рядом с тарифами 2026–27; текущий приём и счёт уточняются.',
   'components':{'tuition_two_usd':31168,'registration_two_usd':2000,'application_two_usd':500,'capital_two_usd':32000,'capital_first_stage_two_usd':16000,'capital_second_stage_two_usd':16000,'annual_usd':33168,'full_commitment_usd':65668},
   'url':fee_urls['S022']},
 ]}
extra_sources = [
 {'title':'ASFM · tuition 2026–27','url':fee_urls['S002'],'claim':'K–5 tuition with sibling rate; registration and entrance are stated as one-time first-enrolment fees. Two-child arithmetic is editorial.','checked':'2026-10-01'},
 {'title':'TAS · tuition and fees 2026–27','url':fee_urls['S003'],'claim':'Pre-K–5 tariff, capital / building / application fees; deposit part of tuition, no sibling discount. Two-child arithmetic is editorial.','checked':'2026-10-01'},
 {'title':'ISP · admissions and fees 2026–27','url':fee_urls['S022'],'claim':'PK4–5 annual tuition, Non-Institutional registration, capital paid in two stages and applications. Stale 2025–26 application sentence retained as a source issue.','checked':'2026-10-01'},
 {'title':'US Department of State · treaty countries','url':'https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/fees/treaty.html','claim':'Mexico is in the E-2 treaty list; treaty nationality is only one eligibility condition. No individual family approval established.','checked':'2026-10-01'},
 {'title':'US Department of State · E-2 requirements','url':'https://travel.state.gov/content/travel/en/us-visas/employment/treaty-trader-investor-visa-e.html','claim':'Nonimmigrant investor visa: nationality, substantial investment, real operating enterprise; spouse and unmarried children under 21 may apply as dependents.','checked':'2026-10-01'},
 {'title':'Taiwan NIA · Gold Card family residency','url':'https://news.immigration.gov.tw/NewsSection/Detail/b635eaf3-a81e-46d6-82e6-e50cae07949d?lang=EN','claim':'NIA article of 18 January 2025 describes separate dependent ARC applications for spouse / children. It is general background, not a current individual approval or school place.','checked':'2026-10-01'},
]
for source in extra_sources:
 if source['url'] not in {x['url'] for x in d['sources']}:
  d['sources'].append({'url':source['url'],'title':source['title'],'evidence':source['claim'],'checked':source['checked']})
 if source['url'] not in {x['url'] for x in f['sources']}: f['sources'].append(source)
for iso, urls in {'MEX':[fee_urls['S002']], 'TWN':[fee_urls['S003'],extra_sources[-1]['url']], 'PAN':[fee_urls['S022']], 'USA':[extra_sources[-3]['url'],extra_sources[-2]['url']]}.items():
 for url in urls:
  if url not in {s['url'] for s in bases[iso]['sources']}:bases[iso]['sources'].append(next(s for s in extra_sources if s['url']==url))
schools={s['id']:s for s in d['schools']}
for cost in f['cost_comparison']['schools']:
 s=schools[cost['school_id']]
 s['cost']=cost['annual']+'; '+cost['entry']+'. '+cost['formula']+' Опубликовано на 2026–27; 2027–28 и индивидуальный счёт не установлены.'
 if cost['url'] not in {x['url'] for x in s['sources']}:
  s['sources'].append({'title':'Tuition and fees 2026–27','url':cost['url'],'claim':'Published primary tariff; two-child calculation in the family strategy is editorial.','checked':'2026-10-01','kind':'school'})
f['actions'][1]['detail']='Сравнить ASFM с независимой командой и TAS / AST; ISP — резерв. Классы и места обоим, текущий junior robotics тренер, часы, проба если разрешена, протоколы и язык. США включать в тот же цикл, если найдены конкретный бизнес и младшая команда. Никакие обращения этим обновлением не отправлены.'
f['actions'][2]['detail']='Разделить recurring расходы и разовые вступительные взносы. Получить полную семейную смету на первый и следующие годы; выбрать тренера, команду, национальное представительство и оборудование по правилам. До этого сохранять регулярную практику в Коста-Рике.'
f['horizons'][0]['base']='Коста-Рика на время проверки → главное сравнение Мексики и Тайваня; США при совпадении бизнеса и junior-команды, Панама как резерв. Переезд после реальных мест обоим.'
f['gaps'][3]='Приём в школы, места в командах, национальные квоты, английский в конкретном кружке и индивидуальное право жить / учиться не подтверждены. Тарифы трёх школ на 2026–27 проверены, но стоимость нужного 2027–28 учебного года и полный семейный бюджет пока неизвестны.'
f['gaps'].append('Общие источники E-2 и Gold Card не проверяют семейные документы. Возможные основания проживания в Бразилии / Панаме приняты как условие семьи и не обозначены как одобренный ПМЖ / ВНЖ.')
d['completeness_audit'].update(version=25,checked='2026-10-01')
d['completeness_audit'].setdefault('source_issues',[]).append({'name':'v25 · school fees and family residency background','status':'ISP retains a 2025–26 application-processing sentence beside published 2026–27 fees; no current place inferred. Direct Gold Card FAQ fetches failed.','official_alternative':'Opened Taiwan NIA article of 18 January 2025 used only for general dependent ARC background; no current fee / visa-free nationality / individual approval claims.'})
assert all(d[k] == v for k, v in before.items())
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
plan_path=root/'data/research-plan.json';plan=json.loads(plan_path.read_text())
plan['status']='active';plan['updated']='2026-10-01'
plan['latest_validation_previous']=plan.get('latest_validation',{})
plan['latest_validation']={'version':'v25','status':'pending','scope':'Family base scenarios and primary 2026–27 cost comparison; existing world inventory unchanged.'}
plan.setdefault('research_passes',[]).append({'version':25,'checked':'2026-10-01','scope':'Refine seven family bases after mobility context; three selectable scenarios and three two-child tuition comparisons','new_event_ids':[],'remaining':'Original worldwide event / league / camp / exhibition / school coverage remains active and incomplete.'})
plan['completeness_audit']='data/audit-v25.json'
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'strategy_version':25,'bases':len(f['bases']),'scenarios':len(f['scenarios']),'cost_comparisons':len(f['cost_comparison']['schools']),'existing_events_preserved':len(d['events']),'private_family_migration_specifics_published':False}))
