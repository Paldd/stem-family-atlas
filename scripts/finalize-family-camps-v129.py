"""Record the actual read-only evidence and a locally prepared family decision layer."""
import collections, hashlib, json, subprocess
from pypdf import PdfReader
from camp_family_review_v129 import ROOT, BASE, CHECKED, CHOICES

P=ROOT.parent/'stem-family-atlas-work/camp-europe-primary-v129'
d=json.loads((ROOT/'data/catalog.json').read_text())
b=json.loads(subprocess.check_output(['git','show',BASE+':data/catalog.json'],cwd=ROOT))
assert d['events']==b['events'] and d['camp_planning']==b['camp_planning']
before={p['slug']:p for p in b['camp_programmes']['profiles']}
after={p['slug']:p for p in d['camp_programmes']['profiles']}
assert before.keys()==after.keys() and [s for s in before if before[s]!=after[s]]==['roches-ai']
assert after['roches-ai']['confirmed_instruction_languages']==['EN']
review=d['camp_programmes']['family_review']
assert review['coverage']==dict(candidates=41,countries=16,fully_audited_countries=0)
sources=[]
for f in sorted(P.glob('receipt-*.json')):
    for old in json.loads(f.read_text()):
        q=dict(old,checked=CHECKED,retrieval_method='direct_public_http',content_scope='Selected primary clauses, discovery and rechecks; not the entire operator website or country.')
        if q.get('status')==200:
            filename=q['key']+('.pdf' if (P/(q['key']+'.pdf')).exists() else '.html')
            raw=(P/filename).read_bytes()
            retained=hashlib.sha256(raw).hexdigest()==q['sha256'] and len(raw)==q['bytes']
            q.update(raw_filename=filename if retained else None,body_snapshot_retained=retained,
                     content_status='selected_pdf_clauses_or_discovery' if retained and filename.endswith('.pdf') else 'selected_html_clauses_or_discovery' if retained else 'earlier_duplicate_body_overwritten')
            if not retained:
                assert q['key'] in ['prefleuri-fees','prefleuri-terms']
                q['resolution']='An earlier duplicate receipt preserves the HTTP outcome/hash, but its first raw body was overwritten by a later retrieval under the same private key. The later separately recorded snapshot is retained. No first-body content evidence is claimed.'
        else:
            q.update(body_snapshot_retained=False,content_status='retrieval_error_not_content_evidence')
            q['resolution']='No challenge bypass. Kandalore selected primary clauses were available through the web reader. A guessed Lighthouse course path and TASIS old navigation path returned404; neither supports programme content.'
        sources.append(q)
assert len(sources)==61 and sum(q.get('status')==200 for q in sources)==56
assert sum(q['body_snapshot_retained'] for q in sources)==54
external=dict(messages_sent=False,applications_submitted=False,payments_made=False,accounts_created=False,subscriptions_created=False,automations_created=False,consent_accepted=False)
publication=dict(status='prepared_local_not_published',project_id='appgprj_6abd44bca1348191809b7260dcb46d87',
    reason='Two fresh native get_site calls in v129 returned SitesConnectorError: Sites project not found. Versions126–129 have no source-push/save/deployment receipt; no older credential was reused.',
    last_confirmed_published_version=125,last_confirmed_deployment_id='appgdep_6ac4ff3f3c7481918fe3d668d24574b0',last_confirmed_success_at='2026-10-06T14:02:09.803197+00:00',production_browser_qa=False)
blocks=collections.Counter(e['block'] for e in d['events'])
audit=dict(version=129,asof=CHECKED,status='progress',scope='Deep selected Swiss programme/contract rechecks and an editorial family selection over existing dossiers across16countries. No new operator/dossier count inflation.',
    events=len(d['events']),competition_records=blocks['Соревнования'],exhibition_records=blocks['События'],camp_learning_records=blocks['Лагеря'],
    programme_dossiers=1034,countries_with_dossiers=39,official_dossier_urls=1582,editorial_scenarios=len(d['camp_programmes']['shortlist']),budget_scenarios=53,
    new_dossiers=0,new_events=0,new_budget_scenarios=0,family_review_candidates=41,family_review_countries=16,
    unchanged_dossiers=1033,corrected_dossier='roches-ai',correction='Explicit English technical instruction now appears in the English filter;11+andarchived2026remain.',
    unchanged_event_objects=3775,unchanged_budget_objects=53,source_retrieval_attempts=61,unique_requested_urls=58,direct_successful_retrievals=56,retrieval_errors=5,
    retained_body_receipts=54,earlier_overwritten_duplicate_receipts=2,pdf_files=7,pdf_text_pages_extracted=sum(len(PdfReader(f).pages) for f in P.glob('*.pdf')),
    visual_pdf_pages_checked=[dict(filename='garenne-conditions.pdf',page=3),dict(filename='roches-brochure.pdf',page=8)],primary_reader_selected_clause_checks=1,
    family_ical=2991,exhibition_ical=104,league_profiles=141,goal='active',worldwide_complete=False,fully_audited_countries=0,external_actions=external,publication=publication,verification={})
assert audit['pdf_text_pages_extracted']==72
assert (ROOT/'dist/downloads/STEM_подтвержденные_даты.ics').read_bytes().count(b'BEGIN:VEVENT')==2991
assert (ROOT/'dist/downloads/STEM_крупные_выставки.ics').read_bytes().count(b'BEGIN:VEVENT')==104
for n in ['independent-check.json','functional-check.json']:
    if (P/n).exists():
        v=json.loads((P/n).read_text());assert v['status']=='passed' and v['version']==129;audit['verification'][n.removesuffix('.json')]=v
def write(stem,value):
    text=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    (ROOT/'data'/f'{stem}.json').write_text(text)
    (ROOT/'dist/downloads'/('STEM_'+stem.replace('-','_')+'.json')).write_text(text)
write('family-camps-audit-v129',audit)
reader=(P/'kandalore-reader.txt').read_bytes()
write('family-camps-source-receipts-v129',dict(version=129,asof=CHECKED,scope=audit['scope'],sources=sources,
    primary_reader_excerpts=[dict(url='https://www.kandalore.com/rates-and-dates/',filename='kandalore-reader.txt',sha256=hashlib.sha256(reader).hexdigest(),scope='Selected2027birth-year/internationalfee/taxclauses;notwholeHTML.')],
    visual_pdf_pages_checked=audit['visual_pdf_pages_checked'],pdf_text_pages_extracted=72,external_actions=external,
    limits='61HTTP attempts/58requestedURLs,56HTTP200;54bodyreceipts retained,2earlierduplicateraws overwritten. SevenPDFs72pages text-extracted,selectedclauses read,2pages visually checked. This is not61campwebsites fullyaudited. No accounts/forms/messages/consent/payment.'))
write('family-camp-selection-v129',review)

lines=['# Лагеря и пансионы: семейный выбор 2026–2027',
    'Подготовлено локально 6 октября 2026. Эта версия 129 ещё не опубликована: Sites возвращает «Sites project not found». Последняя подтверждённая публикация 125.',
    '41 кандидат на сравнение в 16 странах выбран из 1034 существующих досье. Новых лагерей или операторов этим проходом не добавлено. Это редакционный семейный выбор, не независимый мировой рейтинг и не полный аудит стран.',
    'Матвей 2017 и Оскар 2020; EN/ES/RU. В 2027 им будет 9–10 и 6–7: день рождения влияет на ступени 7/8/10/11+. Точный класс также определяет школьные категории.',
    '## Как пользоваться',
    'В разделе лагерей появился «Семейный выбор»: выберите страну, ребёнка и задачу. Кнопка открывает полное досье с источниками; существующий календарь, карта, сравнение и 53 частичные сметы сохранены.',
    '## Что проверено в этом проходе',
    'Выбранные страницы программы, возрастов, языка, проживания, цены, приёма и договора: особенно La Garenne, Le Rosey, TASIS, Préfleuri, Aiglon и BeauSoleil; Франция/Испания и азиатские/американские кандидаты. 61 HTTP-попытка, 58 запрошенных URL, 56 ответов HTTP 200. Это не 61 полностью изученный лагерь. Из 7 PDF извлечён текст 72 страниц; проверены выбранные положения и визуально 2 страницы. Два первых дубликата сырого HTML перезаписаны более поздними снимками; ранние receipt не выдаются за сохранённый текст.',
    'AI Camp École des Roches прямо обозначен English в программе и брошюре. Исправлен английский фильтр. Возраст 11+ и архив 2026 сохранены: новая смена 2027 не выдумана.',
    '## Основной маршрут']
for s in review['recommended_sequence']:lines += ['### '+s['stage'],s['detail']]
lines += ['## Сравнение кандидатов']
for iso in dict.fromkeys(after[q['slug']]['iso'] for q in review['entries']):
    entries=[q for q in review['entries'] if after[q['slug']]['iso']==iso]
    lines += ['### '+after[entries[0]['slug']]['country']]
    for q in entries:
        p=after[q['slug']]
        lines += ['**'+p['provider']+'**',q['reason']+' '+q['key_limit'],
                  'Возраст: '+p['age']+' Язык: '+p['language'],
                  'Когда: '+p['timing']['label'],
                  'Цена ('+str(p['price']['year'] or 'год не установлен')+'): '+p['price']['label'],
                  'Досье: ['+p['id']+'](../index.html?camp='+p['slug']+'#camps). Источник: ['+p['sources'][0]['title']+']('+p['sources'][0]['url']+'). Дата досье: '+p['checked']+'. Полный состав тарифа, доплаты и отмена — в досье.']
lines += ['## До окончательного выбора']+['- '+s for s in review['methodology']]
lines += ['## Полнота и дальнейшая работа',
    'Мировая цель остаётся активной: все общие и тематические лагеря 2026–27 на EN/ES/RU, дневные/пансионные/семейные, мировые соревнования/лиги/выставки, постоянные школы и результаты 5–10 лет, инженерные и предпринимательские маршруты. Приоритеты: Швейцария, Франция, Испания/Европа, Тайвань, Сингапур, ЮжнаяКорея, Япония, США/Канада, Коста-Рика, Мексика и LATAM; затем остальные страны. Полностью изученных стран 0.',
    'Перед поездкой ещё нужны места, иностранный приём, конкретный преподаватель/группа, полный счёт, техника в собственность или аренду, ночной присмотр, страхование и действующий договор. Заявки, сообщения и оплаты не выполнялись.']
(ROOT/'dist/downloads/STEM_семейный_выбор_лагерей_v129.md').write_text('\n\n'.join(lines)+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text())
if plan['latest_validation'].get('version')!=129:plan['latest_validation_previous']=plan['latest_validation']
plan['previous_goal_turn_classification']=dict(classification='progress',asof=CHECKED,evidence='v128local19dossiers/6datedrows/3budgets,verified and committed '+BASE+';publication unavailable,meaningfulresearchcontinues.')
plan['latest_validation']={k:audit[k] for k in ['version','asof','events','competition_records','exhibition_records','camp_learning_records','programme_dossiers','countries_with_dossiers','official_dossier_urls','editorial_scenarios','budget_scenarios','family_ical','exhibition_ical','league_profiles','worldwide_complete','fully_audited_countries']}
plan['latest_validation']['status']='Selected Swiss and international primary rechecks and41familychoices prepared locally;publication unavailable.'
plan['family_camp_review_v129']=audit;plan['current_publication']=publication
plan['human_scope_expansion']=dict(status='active',content='Все топовые общие, тематические и робототехнические лагеря 2026–27 по всем странам: EN/ES/RU, день/пансион/семья; первичные программы, полный прайс техники и обязательных сборов, приём и возраст. Особенная глубина CHE/FRA/ESP/Europe, TWN/SGP/KOR/JPN, USA/CAN, CRI/MEX/LATAM. Соревнования, лиги, выставки, школы/5–10 лет результатов и маршруты сохраняются.',source='Explicit human messages in this conversation;nativegoalkeptactive,notreplaced.')
for field,name in [('complete_database_download','STEM_database_download.json'),('complete_json_download','STEM_database_json_download.json')]:plan[field]=json.loads((ROOT/'dist/downloads'/name).read_text())
for q in plan['requirements']:
    if q['id'] in ['camps','family_top_picks']:
        q['evidence']='v129local:41editorialfamilycandidates/16countriesover1034existingdossiers;selectedSwiss2027curricula/contractrechecks,EnglishAI11+filtercorrection. No newdossierinflation. Worldwideprioritycountry/generalENESRUscopeactive;0fullyauditedcountries.'
    elif q['id']=='unified_database':q['evidence']='v129local:3775events/1034dossiers/39countries/53partialbudgets,allold3775events/53offerspreserved;fullSQL/JSONand41familychoices;publicationunavailable.'
plan['research_passes']=[q for q in plan.get('research_passes',[]) if q.get('version')!=129]+[dict(version=129,asof=CHECKED,status='progress',scope=audit['scope'],new_dossiers=0,new_calendar_rows=0,family_review_candidates=41,official_primary_retrieval_attempts=61,not_complete_worldwide=True,publication='prepared_local_not_published')]
plan.update(updated=CHECKED,status='active',native_goal_status='active');write('research-plan',plan)
f=ROOT/'dist/index.html';s=f.read_text().replace('?v=128','?v=129').replace('data-ui-version="128"','data-ui-version="129"')
anchor='<a class="button secondary" href="downloads/STEM_research_plan.json"'
link='<a class="button secondary" href="downloads/STEM_семейный_выбор_лагерей_v129.md" download>Семейный выбор ·41 программа в 16 странах</a>'
if link not in s:assert anchor in s;s=s.replace(anchor,link+anchor,1)
f.write_text(s)
print(json.dumps({k:audit[k] for k in ['version','events','programme_dossiers','family_review_candidates','family_review_countries','new_dossiers','source_retrieval_attempts','publication']}))
