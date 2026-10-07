"""Record selected primary evidence and the prepared local Asian increment."""
import collections,hashlib,json
from camp_asia_v134 import ROOT,BASE,CHECKED,NEW,COURSE,INDUSTRY,HOME,NATURE,AYLA
P=ROOT.parent/'stem-family-atlas-work/camp-asia-primary-v134'
d=json.loads((ROOT/'data/catalog.json').read_text());ps={p['slug']:p for p in d['camp_programmes']['profiles']}
sources=[]
for r in json.loads((P/'receipt.json').read_text()):
    q=dict(r,retrieval_method='direct_public_http')
    if q.get('status')==200:
        filename=q['key']+'.html';b=(P/filename).read_bytes();assert len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['sha256']
        q.update(raw_filename=filename,body_snapshot_retained=True,content_status='selected_html_programme_clauses')
        if q['key']=='camp-challenge-home':q['content_status']='navigation_discovery_not_full_provider_audit'
        if q['key']=='sg-gst':q['content_status']='official_standard_rate_clause_not_individual_camp_invoice'
        if q['key']=='grove-recheck':q['content_status']='existing_programme_rechecked_no_duplicate_added'
        if q['key'] in ['edutech-kids-archive','edutech-teens-archive']:q['content_status']='ended_september_2026_programme_not_current_camp'
    sources.append(q)
assert len(sources)==11 and all(q.get('status')==200 for q in sources)
plan=json.loads((ROOT/'data/research-plan.json').read_text())
publication=dict(plan['current_publication'],status='prepared_local_not_published',reason='Fresh native same-project get_site in v134 returned NOT_FOUND/project_not_found404: Sites project not found. No source push, saved site version or deployment for v134; same published project retained.',production_browser_qa=False)
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
blocks=collections.Counter(e['block'] for e in d['events']);review=d['camp_programmes']['family_review']
ics=(ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_text()
added=[e for e in d['events'] if e.get('camp_dossier_slug') in NEW]
audit=dict(version=134,asof=CHECKED,status='progress',scope='Four Singapore programme dossiers from two operators, two dated camp rows, one partial fee calculation and a scoped Camp Ayla tariff-name correction. Worldwide objective retained.',
    events=len(d['events']),competition_records=blocks['Соревнования'],event_records=blocks['События'],exhibition_records=blocks['События'],exhibition_records_unit='Mixed Events block, not major company exhibition count.',camp_learning_records=blocks['Лагеря'],
    programme_dossiers=len(ps),countries_with_dossiers=d['camp_programmes']['counts']['countries'],official_dossier_urls=d['camp_programmes']['counts']['source_urls'],editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=len(d['camp_planning']['offers']),
    new_dossiers=4,new_dossier_operator_count=2,updated_dossiers=['ayla-tokyo'],unchanged_dossiers=1097,new_calendar_rows=2,new_budget_scenarios=1,unchanged_budget_objects=56,
    unchanged_event_objects=3782,updated_event_objects=24,updated_event_scope='Only CP183 generated rows: tariff names/text and source check date. UID, dates, ages, languages and numerical fees unchanged.',
    dossier_ids=[ps[s]['id'] for s in NEW],new_calendar_ids=[e['id'] for e in added],family_review_candidates=review['coverage']['candidates'],family_review_countries=review['coverage']['countries'],
    source_retrieval_attempts=11,direct_successful_retrievals=11,retained_body_receipts=11,pdf_files=0,new_mobile_qa=False,production_browser_qa=False,
    family_ical=ics.count('BEGIN:VEVENT'),new_family_ical_entries=3,old_family_ical_blocks_preserved=2998,old_family_ical_blocks_updated_tariff_names=24,exhibition_ical=104,
    league_profiles=len(d['league_guide']['profiles']),new_league_profiles=0,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert len(added)==2 and audit['events']==3808 and audit['programme_dossiers']==1102 and audit['family_ical']==3025
for name in ['independent-check','functional-check']:
    f=P/(name+'.json')
    if f.exists():
        q=json.loads(f.read_text());assert q['status']=='passed' and q['version']==134;audit['verification'][name]=q
def write(stem,value):
    body=json.dumps(value,ensure_ascii=False,indent=2)+'\n';(ROOT/'data'/f'{stem}.json').write_text(body);(ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(body)
write('asia-camps-audit-v134',audit)
write('asia-camps-source-receipts-v134',dict(version=134,asof=CHECKED,sources=sources,external_actions=external,
    limits='11 retained HTTP200 bodies: selected programme clauses, ended September events, provider navigation, existing Grove recheck and IRAS rate. Not 11 whole camp websites/countries. No private raw HTML/text in repository or downloads; no PDF/mobile/production audit this pass.'))
write('family-camp-selection-v134',review)
lines=['# Сингапур: AI, семейный Ideathon и общий ноябрьский отдых',
    'Локальная версия 134 · проверено 6 октября 2026. Новая редакция ещё не опубликована: Sites возвращает «Sites project not found». Последняя подтверждённая публикация — 125.',
    'Добавлены четыре досье программ двух операторов и две датированные карточки. Итого 1 102 досье в 39 странах, 3 808 записей календаря и учебных направлений, 57 частичных смет. Досье могут описывать разные программы одного лагеря; количество не является мировым рейтингом.',
    'Матвей — 2017, Оскар — 2020: в 2026 возраст 8–9 / 5–6, в 2027 — 9–10 / 6–7. Точная дата рождения и класс определяют допуск. Язык преподавания EN/ES/RU новых программ пока не подтверждён прямым указанием организатора.',
    '## Что выбрать семье',
    '\n'.join(['| Программа | Когда | Для детей | Ограничения |','|---|---|---|---|',
        '| [EDUTech Industry]('+COURSE+') | 21–26 ноября 2026, шесть дней | Матвей входит в 7–15; Оскар младше | Язык, семейная цена, ежедневные часы и допуск к специальным выездам требуют подтверждения |',
        '| [5th Family AI Ideathon]('+COURSE+') | Внутри 21–26 ноября; точный день неизвестен | Оскар 5–6 с родителем | Отдельный младший компонент; цена неизвестна. Его условия не дают допуска ко всем шести дням |',
        '| [AI for Tweens]('+HOME+') | Октябрь–декабрь 2026, двухчасовые занятия на выходных | Матвей после девятого дня рождения | Срок октябрьского набора 18 сентября прошёл; набор ноября/декабря уточнить |',
        '| [Nature Quest]('+NATURE+') | 23–25 ноября 2026 | Оба входят в 5–10 | Общий отдых. Язык неизвестен; 25 ноября конец 20:00/20:30 расходится; 24 ноября другая площадка |']),
    'Industry включает AI-прототипы, работу с клиентом и ценой, презентации, две встречи с наставниками и три выезда. SGInnovate отмечает, что изменения организатора ещё не прошли его проверку. Заявленные встречи и доступ к специальным объектам требуют подтверждения. Внутреннее жюри и сертификат не означают международную победу.',
    'Цена курса $1 500 и диапазон S$200–1 500 за гибкое посещение ещё не образуют семейную смету: неизвестно, как цена начисляется детям и взрослым и какие пакеты доступны. Собственная страница включает транспорт программы, обеды, ужины и перерывы с кофе. Налоги, технические аккаунты, страховка и отмена не установлены. Регистрация И оплата до 15 ноября — опубликованный срок; заявка не отправлялась.',
    'Nature Quest: три дня — $356 до GST, один день — $145 до GST. При стандартном GST 9% расчёт составляет 388,04 на ребёнка / 776,08 за двоих. Сайт пишет $; SGD принят по местному контексту. Валюта и округление требуют счёта. Скидка 10% до 31 октября в этот расчёт не включена. Перелёт, жильё семьи, доставка к площадкам и неизвестные обязательные доплаты учитываются отдельно.',
    '23/25 ноября: KOKOMO Beach Club, 131 Pasir Ris Road. 24 ноября: Beach Station, Sentosa, 21 Beach View. Первые два дня — 09:00–17:30. На последний день заголовок указывает 09:00–20:00, подробный план — выдачу детей в 20:30. FAQ включает питание по расписанию; количество ведущих на ребёнка неизвестно. Родители обычно не остаются. При болезни день нужно пропустить; возврат не обещан.',
    '## Исправление Camp Ayla в Tokyo',
    '[Текущая страница]('+AYLA+') называет пакеты Prime 09–13, Regular 09–15, Extended 09–17, Super Extended 09–18. Исправлены названия в досье и 24 календарных вариантах. Даты, возраст, числовые цены и предупреждения о праздничных днях сохранены. Regular 09–15: ¥10 000 + 10% = ¥11 000 в день. Язык конкретной смены ещё уточнить. Транспорт не предоставляется; оплаченные сборы не возвращаются и не переносятся.',
    '## Полные новые досье']
for slug in NEW:
    p=ps[slug]
    lines += ['### '+p['id']+' · '+p['provider'],p['country']+' · '+p['place'],
        'Возраст: '+p['age'],'Язык: '+p['language'],'Содержание: '+p['programme'],'Когда: '+p['timing']['label'],
        'Цена: '+p['price']['label'],'Включено: '+p['price']['included'],'Доплаты: '+p['price']['extras'],'Оплата/возврат: '+p['price']['deposit'],
        'Проживание: '+p['accommodation'],'Матвей: '+p['family_fit']['matvey']['detail']+' Оскар: '+p['family_fit']['oscar']['detail'],
        'Источники: '+', '.join('['+s['title']+']('+s['url']+')' for s in p['sources'])+'. [Досье в локальном сайте](../index.html?camp='+slug+'#camps).']
lines += ['## Проверка и границы',
    '3 782 прежних события и 1 097 прежних досье сохранены полностью. У Camp Ayla исправлены 24 строки с названиями тарифов; даты, числовые цены, возраст и языковые теги прежние. Сохранены 56 прежних смет, 142 профиля лиг/программ, школы, история результатов и маршруты.',
    'Семейный ICS: 3 025 записей. Из прежних 2 998 VEVENT сохранены побайтно, у 24 Ayla исправлены подписи при прежних UID/датах. Добавлены две смены и срок регистрации полного лагеря 7–15. ICS 104 крупных выставок прежний. 197 записей смешанного блока «События» не означают 197 крупных мировых выставок.',
    'Сохранены 11 прямых HTTP-ответов: выбранные условия программ, две завершённые сентябрьские AI-программы, навигация, перепроверенный Grove и ставка IRAS. Это не 11 полностью изученных сайтов. Сырые страницы остаются приватно вне репозитория. Места, зачисление и английский ещё неизвестны. Сообщения, заявки и платежи не выполнялись.',
    'Мировая цель активна: все топовые общие и тематические лагеря 2026–2027 с EN/ES/RU, дневные программы, пансионы и семейные форматы; соревнования, лиги, крупные выставки, постоянные школы, история 5–10 лет и инженерные/предпринимательские маршруты. Приоритеты Европы, Азии, Северной и Латинской Америки сохранены. Полностью изученных стран — 0.']
(ROOT/'dist/downloads/STEM_лагеря_Сингапур_Япония_v134.md').write_text('\n\n'.join(lines)+'\n')
if plan['latest_validation'].get('version')!=134:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v133:14dossiers,12campvariants,visitorcard,partialbudget,independent/UIchecks,commit '+BASE+' and byte-verified local archive. Research can continue despite hosting outage.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Four selected dossiers,two datedrows,onebudget and scoped Ayla tariff correction; prepared locally, not published.'
plan['asia_camps_v134']=audit;plan['current_publication']=publication
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:q['evidence']='v134local:1102dossiers/39countries/1648URLs,4selectedSingaporeprogrammes;64familychoices/16countries,57partialbudgets. AI7–15 separateFamilyIdeathon5–6,unknownEnglish/feeunit,rolling9–14,5–10NatureQuest and corrected Ayla tariff names.0fullyauditedcountries;fullworldscopeactive.'
    elif q['id']=='unified_database':q['evidence']='v134local:3808events/1102dossiers/57partialbudgets in completeSQLite/JSON.3782oldobjectsunchanged,24Ayla tariff textcorrected,twoaddedcampcards.104major exhibitionICS. No push/save/deployment.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=134]+[dict(version=134,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=4,new_calendar_rows=2,new_budget_scenarios=1,official_primary_retrieval_attempts=11,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=133','?v=134').replace('data-ui-version="133"','data-ui-version="134"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"';link='<a class="button secondary" href="downloads/STEM_лагеря_Сингапур_Япония_v134.md" download>Сингапур · AI и ноябрьский семейный отдых</a>'
if link not in s:s=s.replace(anchor,link+'\n'+anchor)
f.write_text(s)
f=ROOT/'dist/assets/camp-programmes.js';s=f.read_text().replace('downloads/STEM_лагеря_Франция_Испания_v133.md','downloads/STEM_лагеря_Сингапур_Япония_v134.md');f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','family_review_candidates','family_ical','new_calendar_rows','goal']}))
