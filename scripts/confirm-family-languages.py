"""Apply a direct family clarification without changing provider language evidence."""
import json, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
catalog=ROOT/'data/catalog.json'
planpath=ROOT/'data/research-plan.json'
d=json.loads(catalog.read_text())
plan=json.loads(planpath.read_text())
assert len(d['events'])==1063 and d['completeness_audit']['version']==15
context=plan['family_context']
context.update(learning_languages=['EN','ES'],
    learning_languages_by_child={'mat':['EN','ES'],'osc':['EN','ES']},
    full_day_english_readiness=True,
    language_confirmation='Прямое сообщение пользователя 01.10.2026: оба могут учиться на английском и испанском.')
d['family_context']=dict(context)
focus=d['completeness_audit']['focused_country']
focus['family']='Матвей — 2017, Оскар — 2020 год рождения. В 2027 году им исполняется 10 и 7 лет. Оба могут учиться на английском и испанском — подтверждено семьёй. Точные дни рождения и текущие классы пока неизвестны.'
focus['learning_languages']=['EN','ES']
focus['routes'][1]['detail']='Expedition27: Тайбэй, 21 января — 3 февраля, десять будней. Рекомендуемые 8–12 лет подходят Матвею; Оскар младше диапазона. Английское обучение подходит обоим по сообщению семьи. Полный пакет пересекается с MARC 1 февраля в другом городе; иностранный приём и место в лагере ещё нужно подтвердить.'
a=d['completeness_audit']
a['caveats']=[x.replace('Точные дни рождения, классы и готовность к целому дню на английском неизвестны.','Точные дни рождения и классы неизвестны. Обучение на английском и испанском подходит обоим детям — семья подтвердила.') for x in a['caveats']]
for e in d['events']:
    if e['id']=='L142':
        e['entry']='Согласовать иностранный приём, возраст и свободное место. Обучение на английском подходит обоим детям по сообщению семьи. Запрос информации не резервирует место или скидку. Минимум 8, максимум 12 участников.'
        e['language_certainty']='Английский конкретной Expedition27 прямо указан провайдером. Семья подтвердила, что оба ребёнка могут учиться на EN / ES; возраст и иностранный приём проверяются отдельно.'
    if e['id']=='L143':
        e['entry']='Согласовать возраст обоих детей и иностранные документы; оба могут учиться на английском по сообщению семьи. Форма → подтверждение в LINE → депозит NT$2 000 для резервирования. Свободные места неизвестны. Если провайдер проводит собственную оценку уровня, её условия уточнить.'
for row in plan['requirements']:
    if row['id']=='eligibility':
        row['evidence']='Пользователь сообщил годы рождения 2017 / 2020 и возможность обучения обоих детей на английском / испанском. MARC TM и TURBOT ноября 2026 исключают Оскара; CENFOTEC Makers декабря 2026 исключает Матвея. Классы и точные дни рождения неизвестны. ERA: иностранный вход; TIRT: дедлайн; GRG AIMS: конфликт возраста.'
        row['remaining']='Точные дни рождения, классы, национальная связь / иностранные разрешения и актуальные регламенты.'
plan['family_context']=context
plan['latest_validation']['family_languages_confirmed']=['EN','ES']
auditpath=ROOT/'data/taiwan-audit-v15.json'
audit=json.loads(auditpath.read_text());audit['focus']=focus
auditpath.write_text(json.dumps(audit,ensure_ascii=False,indent=2))
catalog.write_text(json.dumps(d,ensure_ascii=False,indent=2))
planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2))
print('Family EN / ES confirmed; all provider language tags and age gates retained.')
