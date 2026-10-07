"""Build the web catalog and portable database from the tracked source of truth."""
import csv, datetime, json, pathlib, re, sqlite3
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/'data/catalog.json'
d=json.loads(DATA.read_text())
from camp_europe_v75 import correct_catalog
correct_catalog(d)
from camp_asia_v76 import correct_catalog_v76
correct_catalog_v76(d)
from camp_asia_europe_v109 import correct_catalog_v109
correct_catalog_v109(d)
from camp_catalog_bridge import integrate
camp_report_file=ROOT/'data/camp-programmes-deep-2026-2027.json'
if camp_report_file.exists():
    integrate(d,json.loads(camp_report_file.read_text()))
from camp_americas_v110 import extend_planning_v110
extend_planning_v110(d)
from camp_europe_v111 import extend_planning_v111
extend_planning_v111(d)
from camp_asia_v112 import extend_planning_v112
extend_planning_v112(d)
from camp_latam_v113 import extend_planning_v113
extend_planning_v113(d)
from camp_northamerica_v114 import extend_planning_v114
extend_planning_v114(d)
from camp_europe_v115 import extend_planning_v115
extend_planning_v115(d)
from camp_asia_v116 import extend_planning_v116
extend_planning_v116(d)
from camp_latam_v117 import extend_planning_v117
extend_planning_v117(d)
from nearby_participation_v118 import enrich as enrich_nearby_v118
enrich_nearby_v118(d)
from camp_swiss_v119 import extend_planning_v119
extend_planning_v119(d)
from camp_europe_v120 import extend_planning_v120
extend_planning_v120(d)
from camp_europe_v124 import extend_planning_v124
extend_planning_v124(d)
from camp_asia_v125 import extend_planning_v125
extend_planning_v125(d)
from camp_europe_v127 import extend_planning_v127
extend_planning_v127(d)
from camp_asia_v128 import extend_planning_v128
extend_planning_v128(d)
from camp_europe_canada_v130 import extend_planning_v130
extend_planning_v130(d)
from camp_northamerica_v131 import enrich_v131
enrich_v131(d)
from camp_nearby_v132 import enrich_v132
enrich_v132(d)
from camp_europe_v133 import extend_planning_v133,enrich_v133
extend_planning_v133(d)
enrich_v133(d)
from camp_asia_v134 import extend_planning_v134
extend_planning_v134(d)
from nearby_robotics_v135 import enrich_v135
enrich_v135(d)
from camp_asia_v136 import extend_planning_v136
extend_planning_v136(d)
d['source_count']=len(d['sources'])
aliases={'Гонконг':['HKG'],'США':['USA'],'США / национальные площадки':['USA'],'Великобритания':['GBR'],'Южная Корея':['KOR'],'Тайвань':['TWN'],'Коста-Рика':['CRI'],'Мексика':['MEX'],'Мексика / региональные страны':['MEX'],'Пуэрто-Рико':['PRI'],'Онлайн / Бразилия':['BRA'],'Австралия / Новая Зеландия':['AUS','NZL'],'ОАЭ':['ARE'],'Турция':['TUR'],'ЮАР':['ZAF'],'Венесуэла':['VEN'],'Россия':['RUS'],'Vietnam':['VNM'],'Netherlands':['NLD'],'Нидерланды':['NLD']}
countries=d['countries']
for c in countries:
    if c['iso']=='TW': c['iso']='TWN'
for e in d['events']:
    e['iso']=aliases.get(e['country'],[c['iso'] for c in countries if e['country'] in [c['country'],c['en']]])
    if 'themes' not in e:
        text=e['title']+' '+e['gear']+' '+e['age']
        themes=[]
        if re.search(r'робо|robo|WRO|FLL|FIRST|VEX|WER|MakeX|Mecha|RECF|ENJOY|TIRT|IRO|IYRC|sumo',text,re.I): themes.append('robotics')
        if re.search(r'\bAI\b|\bИИ\b|интеллект|Intelligence|Codeavour|WAICY|ENJOY AI',text,re.I): themes.append('ai')
        if re.search(r'games?|игр|Roblox|Minecraft',text,re.I): themes.append('games')
        if re.search(r'coding|coders?|code|программ|Bebras|computational|вычисл|Coolest Projects',text,re.I): themes.append('coding')
        e['themes']=themes or ['technology']
    if 'scope' not in e:
        t=e['title'].lower()
        if re.search(r'international|world|миров|международ|global|europe|superregional|latam',t) or e['id'] in ['C021','C024','C029','C031','C037','C038','C039','C040','C052','E016','E017','E018','E019','E028','E029']:
            scope='international'
        elif e['id'] in ['C003','C004','C005','C006','C007','C008','C009','C010','C011','C012','C013','C014','C015','C016','C043','C044','C064']:
            scope='national'
        elif e['id'] in ['C047','C048','C049','C050']: scope='regional'
        elif e['block']=='Лагеря': scope='local'
        else: scope='unclassified'
        e['scope']=scope
        e['importance_reason']='Редакционная классификация по названию/формату и источнику. '+e['level']
    if 'languages' not in e:
        # A proposed "EN согласовать" must not appear as a confirmed EN program.
        s=e['language']
        e['languages']=[x for x in ['EN','ES','RU'] if re.search(r'^(?:EN|ES|RU)(?:\s*/\s*(?:EN|ES|RU))*\b',s) and re.search(r'\b'+x+r'\b',s.split(';')[0])] if not re.search(r'не подтверж|не найден|согласовать|\?',s,re.I) else []
    if 'participation' not in e:
        if e['block']=='События': mode='visitor'
        elif e['block']=='Лагеря':
            mode='regular' if re.search('регуляр|подготовка|обучение /|страница без',e['title'],re.I) else 'residential' if re.search('residential|overnight',e['title']+' '+e['format'],re.I) else 'day_camp'
        else: mode='team' if re.search('команд|team|2–|2-',e['format'],re.I) else 'individual'
        e['participation']=mode
    e.setdefault('language_certainty','Языковая отметка описывает найденный вариант; точный поток и язык преподавания/судейства проверяются перед записью')
    assert e['source'].startswith('http') and e['checked']
    if e['start']:
        assert e['date_status'] in ['Подтверждено','Опубликованное правило · даты рассчитаны']
        if e['date_status']=='Опубликованное правило · даты рассчитаны':
            assert e.get('date_precision')=='published_rule' and e.get('date_rule') and e.get('camp_programme_id')
        assert datetime.date.fromisoformat(e['start'])<=datetime.date.fromisoformat(e['end'])
assert len(set(e['id'] for e in d['events']))==len(d['events'])
coverage=[]
for c in countries:
    a=[e for e in d['events'] if c['iso'] in e['iso']]
    row=dict(iso=c['iso'],country=c['country'],region=c['region'],research_status='Частично: есть записи; полный местный аудит не завершён' if a else 'Местный календарь ещё не исследован',competitions=sum(e['block']=='Соревнования' for e in a),exhibitions=sum(e['block']=='События' for e in a),camps=sum(e['block']=='Лагеря' for e in a),dated=sum(bool(e['start']) for e in a),organizer=c['wro'],organizer_url=c['url'])
    coverage.append(row)
d['coverage']=coverage
d['coverage_summary']=dict(countries=len(countries),countries_with_records=sum(r['competitions']+r['exhibitions']+r['camps']>0 for r in coverage),fully_audited_countries=0,unmapped_global_records=sum(not e['iso'] for e in d['events']))
if 'schools' in d:
    schools=d['schools']; country_ids={c['iso'] for c in countries}
    assert len({s['id'] for s in schools})==len(schools)
    for s in schools:
        assert s['iso'] in country_ids and s['sources'] and s['checked']
        assert all(r['source'] in {x['url'] for x in s['sources']} for r in s['results'])
    d['school_focus']['counts']=dict(records=len(schools),countries=len({s['iso'] for s in schools}),
        public=sum(s['school_type']=='public' for s in schools),
        private=sum(s['school_type'] in ['private','private_industry'] for s in schools),
        boarding=sum(s['boarding']=='yes' for s in schools),
        world_result=sum(s['evidence']=='world_result' for s in schools),
        organizer_protocol=sum(any(r['provenance']=='organizer_protocol' for r in s['results']) for s in schools),
        fully_audited_countries=0)
    d['school_focus']['coverage']=[dict(iso=c['iso'],country=c['country'],region=c['region'],
        records=sum(s['iso']==c['iso'] for s in schools),status='partial' if any(s['iso']==c['iso'] for s in schools) else 'unresearched') for c in countries]
    d['completeness_audit']['school_focus']=d['school_focus']
    (ROOT/f"data/schools-audit-v{d['school_focus']['version']}.json").write_text(json.dumps(d['school_focus'],ensure_ascii=False,indent=2)+'\n')
if 'camp_focus' in d:
    camps=[e for e in d['events'] if e['block']=='Лагеря']
    d['camp_focus']['counts']=dict(records=len(camps),
        holiday=sum(e['participation'] in ['day_camp','residential','mixed_camp','holiday_workshop'] for e in camps),
        regular=sum(e['participation']=='regular' for e in camps),
        self_paced_materials=sum(bool(e.get('materials_only')) for e in camps),
        boarding=sum(e['participation'] in ['residential','mixed_camp'] for e in camps),
        en_es_instruction=sum(e.get('language_mode') in ['primary','bilingual'] and bool({'EN','ES'}&set(e['languages'])) for e in camps),
        en_es_support=sum(e.get('language_mode')=='support' and bool({'EN','ES'}&set(e.get('support_languages',[]))) for e in camps),
        family_instruction=sum(e.get('language_mode') in ['primary','bilingual'] and bool(set(d['family_context']['learning_languages'])&set(e['languages'])) for e in camps),
        family_support=sum(e.get('language_mode')=='support' and bool(set(d['family_context']['learning_languages'])&set(e.get('support_languages',[]))) for e in camps),
        ru_instruction=sum(e.get('language_mode') in ['primary','bilingual'] and 'RU' in e['languages'] for e in camps),
        language_lessons=sum(e.get('language_mode')=='language_lessons' for e in camps),
        camp_life_language=sum(e.get('language_mode')=='camp_life' for e in camps),
        language_unclassified=sum(not e.get('language_mode') for e in camps),
        countries=len({i for e in camps for i in e['iso']}))
    d['completeness_audit']['camp_focus']=d['camp_focus']
if 'completeness_audit' in d:
    audit=d['completeness_audit']
    audit['counts'].update(cards=len(d['events']),competition_cards=sum(e['block']=='Соревнования' for e in d['events']),
        event_cards=sum(e['block']=='События' for e in d['events']),camp_cards=sum(e['block']=='Лагеря' for e in d['events']),
        league_profiles=len(d['league_guide']['profiles']),major_exhibition_cards=sum(bool(e.get('exhibition_tier')) for e in d['events']))
    inventory=[]
    for p in d['league_guide']['profiles']:
        a=[e for e in d['events'] if e['id'] in p['event_ids'] and e['block']=='Соревнования']
        related=[e for e in d['events'] if e['id'] in p['event_ids']]
        inventory.append(dict(id=p['id'],name=p['name'],group=p['group'],event_ids=[e['id'] for e in a],cards=len(a),
            future_dated=sum(bool(e['start']) and e['end']>=audit['checked'] for e in a),
            linked_card_count=len(related),
            status='Есть профиль и карточки; местный охват частичный' if a else 'Учебная / посещаемая программа; конкурсных этапов нет' if related else 'Только профиль; календарь этапов не добавлен',
            source=p['sources'][0]['url'],new=p['id'] in audit['new_profiles']))
    audit['league_inventory']=inventory
    audit['counts']['vex_cards']=next(p['cards'] for p in inventory if p['id']=='vex')
    audit['exhibition_inventory']=[dict(id=e['id'],name=e['title'],country=e['country'],region=e['region'],start=e['start'],end=e['end'],
        visitor_policy=e['visitor_policy'],source=e['source'],new=e['id'] in audit['new_ids']) for e in d['events'] if e.get('exhibition_tier')]
    audit['counts']['countries_with_records']=d['coverage_summary']['countries_with_records']
    audit['counts']['fully_audited_countries']=d['coverage_summary']['fully_audited_countries']
    for row in audit['continents']:
        a=[e for e in d['events'] if e['region'] in row['regions']]
        row['countries_with_records']=len({i for e in a for i in e['iso']})
        row.update(total=len(a),competitions=sum(e['block']=='Соревнования' for e in a),events=sum(e['block']=='События' for e in a),
            camps=sum(e['block']=='Лагеря' for e in a),major_exhibitions=sum(bool(e.get('exhibition_tier')) for e in a))
    audit['interregional_cards']=len(d['events'])-sum(c['total'] for c in audit['continents'])
    (ROOT/f"data/audit-v{audit['version']}.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2))
d['methodology']={
 'scope':'Масштаб — редакционная оценка по источнику; международная сеть не делает каждый этап мировым финалом.',
 'priority':'P0: действующий семейный срок; P1: местный/онлайн путь участия; P2: подготовка или поездка после допуска; P3: посещение при удобной поездке; P4: исключено.',
 'coverage':'Наличие страны в справочнике не означает полный аудит. Каждое местное направление требует отдельных источников.',
 'language':'ES / EN / RU фильтр включает языковые варианты, поддержку и найденные материалы. RU-правила не доказывают RU-судейство. Отдельный фильтр различает основной технический язык, билингвальность, помощь, языковые уроки и неподтверждённые записи.',
 'dates':'Дата виртуального судейства не означает очную выставку; школьный отбор не является открытой семейной заявкой. Точная дата события не равна открытому набору или принятой регистрации. Необъявленные смены не получают вымышленных дат. Опубликованные окна каникул показываются отдельно от точных дней занятий и не экспортируются в календарь.'}
DATA.write_text(json.dumps(d,ensure_ascii=False,indent=2))
assets=ROOT/'dist/assets'; out=ROOT/'dist/downloads';out.mkdir(exist_ok=True)
web={k:d[k] for k in ['asof','baseline_asof','events','countries','leagues','coverage','coverage_summary','methodology','league_guide','development_routes','completeness_audit']}
if 'family_context' in d: web['family_context']=d['family_context']
if 'camp_focus' in d: web['camp_focus']=d['camp_focus']
if 'camp_planning' in d: web['camp_planning']=d['camp_planning']
if 'camp_programmes' in d:
    web['camp_programmes']=d['camp_programmes']
    (out/'STEM_camp_programmes_deep_2026_2027.json').write_text(json.dumps(d['camp_programmes'],ensure_ascii=False,indent=2)+'\n')
if 'schools' in d: web.update(schools=d['schools'],school_focus=d['school_focus'])
if 'school_history' in d: web['school_history']=d['school_history']
if 'project_focus' in d: web['project_focus']=d['project_focus']
if 'family_strategy' in d: web['family_strategy']=d['family_strategy']
if 'kazakhstan_focus' in d: web['kazakhstan_focus']=d['kazakhstan_focus']
if 'europe_focus' in d: web['europe_focus']=d['europe_focus']
if 'north_europe_focus' in d: web['north_europe_focus']=d['north_europe_focus']
if 'south_europe_focus' in d: web['south_europe_focus']=d['south_europe_focus']
if 'southeast_asia_focus' in d: web['southeast_asia_focus']=d['southeast_asia_focus']
if 'africa_focus' in d: web['africa_focus']=d['africa_focus']
if 'middleeast_focus' in d: web['middleeast_focus']=d['middleeast_focus']
if 'asia_english_focus' in d: web['asia_english_focus']=d['asia_english_focus']
if 'east_asia_focus' in d: web['east_asia_focus']=d['east_asia_focus']
if 'top_picks' in d: web['top_picks']=d['top_picks']
web.update(audit_count=len(d['audit']),wro_members=d['wro_members'])
(assets/'data.js').write_text('window.STEM_DATA='+json.dumps(web,ensure_ascii=False,separators=(',',':'))+';\n')
(out/'STEM_database.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
from database_download import package_json
json_database_download = package_json(out/'STEM_database.json')
if 'top_picks' in d:
    top=d['top_picks']
    event_ids={e['id'] for e in d['events']}; school_ids={s['id'] for s in d['schools']}; profile_ids={g['id'] for g in d['league_guide']['profiles']}
    for pick in top['picks']:
        valid=school_ids if pick['category']=='school' else profile_ids if pick['category']=='league' else event_ids
        assert all(i in valid for i in pick['target_ids']), pick['id']
        assert all(i in event_ids for i in pick['event_ids']), pick['id']
    (out/'STEM_top_picks.json').write_text(json.dumps(top,ensure_ascii=False,indent=2)+'\n')
    lines=['# '+top['title'],'',top['basis'],'',top['recommendation'],'','## Как выбирали','']+['- '+s for s in top['methodology']]
    for category,label in top['categories'].items():
        lines+=['','## '+label,'']
        for p in [p for p in top['picks'] if p['category']==category]:
            lines+=['### '+p['title'],'',p['place']+' · '+('Будущий маршрут' if p['horizon']=='future' else 'Возрастная ступень для рассмотрения сейчас'),'',p['label'],'',p['why'],'','Подтверждено: '+p['facts'],'','Условия: '+p['gate'],'','Следующий шаг: '+p['next_action'],'']
            lines+=['- ['+s['title']+']('+s['url']+')' for s in p['sources']]
    (out/'STEM_top_picks.md').write_text('\n'.join(lines)+'\n')
if 'kazakhstan_focus' in d:
    k=d['kazakhstan_focus']; (out/'STEM_Kazakhstan.json').write_text(json.dumps(k,ensure_ascii=False,indent=2)+'\n')
    lines=['# '+k['title'],'',k['conclusion'],'',k['limitations'],'','## Объявленные этапы','']
    lines += ['- '+a['date']+' · '+a['city']+' · '+a['id'] for a in k['announced']]
    for child in k['children']: lines += ['','## '+child['name'],'',child['detail'],'']+['- '+i for i in child['event_ids']]
    lines += ['','## Условия участия','']+['- '+s for s in k['gates']]+['','## Первичные источники','']+['- ['+s['title']+']('+s['url']+')' for s in k['sources']]
    (out/'STEM_Kazakhstan.md').write_text('\n'.join(lines)+'\n')
for focus_key,download_name in [('europe_focus','STEM_Europe_CHE_ESP_FRA'),('north_europe_focus','STEM_Europe_DEU_NLD_BEL'),('south_europe_focus','STEM_Europe_ITA_PRT'),('southeast_asia_focus','STEM_Southeast_Asia'),('africa_focus','STEM_Africa'),('middleeast_focus','STEM_Middle_East'),('asia_english_focus','STEM_Singapore_HongKong'),('east_asia_focus','STEM_East_Asia_JPN_CHN_TWN')]:
    if focus_key not in d: continue
    f=d[focus_key]
    assert all(set(c['event_ids']) <= {e['id'] for e in d['events']} for c in f['countries'])
    assert all(set(c['school_ids']) <= {s['id'] for s in d['schools']} for c in f['countries'])
    (out/(download_name+'.json')).write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
    lines=['# '+f['title'],'',f['family'],'',f['conclusion'],'',f['limitations'],'']
    if f.get('probe_scenarios'):
        lines += ['## Выбор страны по цели семьи','','Предварительная оценка соответствия семье; место, класс, язык группы и квота не подтверждены.','']
        for scenario in f['probe_scenarios']:
            lines += ['### '+scenario['label'],'',scenario['intro'],'']
            for choice in scenario['countries']:
                country=next(c['country'] for c in d['countries'] if c['iso']==choice['iso'])
                lines += ['#### '+country+' · '+choice['verdict'],'',choice['reason'],'',choice['gate'],'']
                lines += ['- '+id+': '+next(e['source'] for e in d['events'] if e['id']==id) for id in choice['event_ids']]+['']
        lines += ['## Маршрут на 10–12 лет','','Это план навыков, а не гарантия будущих дат, допусков или побед.','']
        for phase in f['development_phases']:
            lines += ['### '+phase['period']+' · '+phase['title'],'',phase['detail'],'']
    if f.get('family_picks'):
        lines += ['## Выбор для Матвея и Оскара','',f['family_picks_note'],'']
        for pick in f['family_picks']:
            lines += ['### '+pick['country']+' · '+pick['title'],'',pick['why'],'',pick['gate'],'']
            lines += ['- '+id+': '+next(e['source'] for e in d['events'] if e['id']==id) for id in pick['event_ids']]
            lines += ['- '+next(s['name'] for s in d['schools'] if s['id']==id)+' · '+id for id in pick['school_ids']]
            lines += ['- '+url for url in pick['source_urls']]+['']
    if f.get('base_comparison'):
        lines += ['## Мой выбор для вашей семьи','',f['comparison_note'],'']
        for pick in f['base_comparison']:
            lines += ['### '+pick['country']+' · '+pick['label'],'',pick['conclusion'],'']
            for label,key in [('Матвей','mat'),('Оскар','osc'),('Школа','school'),('Бюджет','budget'),('Проба','trial'),('Условия','gate')]:
                lines += [label+': '+pick[key],'']
            lines += ['- '+url for url in pick['source_urls']]+['']
    for stop in f.get('season_stops',[]):
        lines += ['## '+stop['date']+' · '+stop['title'],'',stop['country'],'',stop['detail'],'']
        lines += ['- '+id+': '+next(e['source'] for e in d['events'] if e['id']==id) for id in stop['event_ids']]+['']
    for pick in f.get('shortlist',[]):
        lines += ['## '+pick['title'],'',pick['detail'],'']
    if f.get('evidence_cards'):
        lines += ['## Результаты команд и условия младших программ','']
        for pick in f['evidence_cards']:
            lines += ['### '+pick['title'],'',pick['detail'],'',pick['limit'],'']
            lines += ['- '+url for url in pick['source_urls']]+['']
    if f.get('decisions'):
        lines += ['## Выбор семейного маршрута','',f['decision_note'],'']
        for pick in f['decisions']:
            lines += ['### '+pick['title']+' · '+pick['country'],'',pick['conclusion'],'','Матвей: '+pick['mat'],'','Оскар: '+pick['osc'],'','Условия: '+pick['gate'],'']
        lines += ['## Возрастный маршрут 2026–2030','',f['age_route_note'],'']
        for year in f['age_routes']:
            lines += ['### '+str(year['year'])+' · Матвей '+str(year['mat_age'])+' / Оскар '+str(year['osc_age']),'','Матвей: '+year['mat'],'','Оскар: '+year['osc'],'','Одна команда: '+year['together'],'',year['technical'],'']
        lines += ['## Выбор школы и наставника','']
        for check in f['selection_checks']:
            lines += ['### '+check['title'],'',check['detail'],'']
    for c in f['countries']:
        lines+=['## '+c['name'],'',c['verdict'],'',c['reason'],'','Матвей: '+c['mat'],'','Оскар: '+c['osc'],'','Лагеря: '+c['camp'],'','Школы: '+c['school'],'','Условия: '+c['risk'],'']
        for label,key in [('Город для пробного периода','city_route'),('Стоимость и технические часы','budget'),('Что доказано о результатах','results_check')]:
            if c.get(key): lines += [label+': '+c[key],'']
    for s in f['steps']: lines+=['## '+s['title'],'',s['detail'],'']
    lines+=['## Первичные источники','']+['- ['+s['title']+']('+s['url']+')' for s in f['sources']]
    (out/(download_name+'.md')).write_text('\n'.join(lines)+'\n')
if 'family_strategy' in d:
    f=d['family_strategy']
    assert len(f['bases'])==7 and len(f['tracks'])==3 and set(f['children'])=={'mat','osc'}
    assert all(set(b['school_ids']) <= {s['id'] for s in d['schools']} for b in f['bases'])
    assert all(s['url'] in {r['url'] for r in d['sources']} for s in f['sources'])
    (out/'STEM_family_strategy.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
    lines=['# Семейный маршрут: инженерия, ИИ и предпринимательство','',f['conclusion'],'',f['rationale'],'',f"Проверено {f['checked']}. Редакционная рекомендация с условиями; места / стоимость / миграционный допуск не подтверждены.",'','## Исходные условия','']+['- '+x for x in f['assumptions']]
    lines+=['','## Как выбирать базу','',f['decision'],'']
    if f.get('scenarios'):
        lines+=['## Три сценария для сравнения','',f.get('confidence',''),'']
        for scenario in f['scenarios']:
            lines+=['### '+scenario['name'],'',scenario['title'],scenario['detail'],'Матвей: '+scenario['mat'],'Оскар: '+scenario['osc'],'']+['- '+x for x in scenario['steps']]+['']
    for b in f['bases']:
        lines+=['## '+b['name'],'',b['role']+' · '+b['verdict'],'',b['recommendation'],'Подтверждено в источниках: '+b['verified'],'Матвей: '+b['child_notes']['mat'],'Оскар: '+b['child_notes']['osc'],'','Условия:']+['- '+x for x in b['gates']]
        lines+=['','Следующий шаг: '+b['next'],'']+[f"- [{s['title']}]({s['url']})" for s in b['sources']]+['']
    if f.get('cost_comparison'):
        comparison=f['cost_comparison']
        lines+=['## Обучение обоих: '+comparison['school_year'],'',comparison['note'],'']
        for cost in comparison['schools']:
            assert cost['school_id'] in {s['id'] for s in d['schools']}
            lines+=['### '+cost['name'],'','Ежегодно: '+cost['annual'],'Разовые взносы / заявки: '+cost['entry'],'Первый год / полное обязательство: '+cost['first'],cost['formula'],f"[Тариф школы]({cost['url']})",'']
    lines+=['## Три направления развития','']
    for t in f['tracks']:
        lines+=['### '+t['name'],'',t['detail'],'Матвей: '+t['mat'],'Оскар: '+t['osc'],'Что проверяем: '+t['proof'],'']
    for c in f['children'].values():
        lines+=['## '+c['name'],'',c['default'],c['detail'],'']+['- '+x for x in c['current']]+['','Через сезон: '+c['proof'],'']
    lines+=['## Горизонты','']
    for h in f['horizons']:
        lines+=['### '+h['name'],'','Матвей: '+h['mat'],'Оскар: '+h['osc'],h['base'],h['decision'],'']
    lines+=['## Первые 90 дней','']
    for a in f['actions']: lines+=['### '+a['period']+' · '+a['title'],'',a['detail'],'']
    lines+=['## Проверка школы и команды','']+['- '+x for x in f['selection']]+['','## Неизвестные условия и границы','']+['- '+x for x in f['gaps']]
    lines+=['','## Официальные источники','']+[f"- [{s['title']}]({s['url']}) — {s['claim']}" for s in f['sources']]
    (out/'STEM_family_strategy.md').write_text('\n'.join(lines)+'\n')
if 'project_focus' in d:
    focus=d['project_focus']
    (out/'STEM_junior_projects.json').write_text(json.dumps(focus,ensure_ascii=False,indent=2)+'\n')
    lines=['# Младшие международные приложения, игры и космический код','',focus['conclusion'],'',f"Проверено {focus['checked']}. Кандидат по возрасту не означает принятую заявку.",'']
    for r in focus['routes']:
        lines+=['## '+r['name'],'',r['status'],r['detail'],'Матвей: '+r['fit_note']['mat'],'Оскар: '+r['fit_note']['osc'],'Следующий шаг: '+r['next'],'Карточки: '+', '.join(r['ids']),'Источник: '+r['source'],'']
    lines+=['## Что ещё уточнить','']+['- '+x for x in focus['gaps']]
    (out/'STEM_junior_projects.md').write_text('\n'.join(lines)+'\n')
if 'school_history' in d:
    history=d['school_history']; entities={e['id']:e for e in history['entities']}
    assert len(entities)==len(history['entities'])
    assert len({r['id'] for r in history['results']})==len(history['results'])
    assert all(r['entity_id'] in entities and r['source'] in {s['url'] for s in d['sources']} for r in history['results'])
    assert all(not e['school_id'] or e['school_id'] in {s['id'] for s in d['schools']} for e in history['entities'])
    (out/'STEM_school_history.json').write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n')
    with (out/'STEM_school_history.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f); w.writerow(['ID','Entity','Kind','Country','School ID','Year','League','Category','Stage','Award','Level','Team','Team ID','Provenance','Source','Limit'])
        for r in history['results']:
            e=entities[r['entity_id']]
            w.writerow([r['id'],e['name'],e['kind'],e['country'],e['school_id'],r['year'],r['league'],r['category'],r['stage'],r['award'],r['level'],r['team'],r['team_id'],r['provenance'],r['source'],r['note']])
    h=['# История STEM соревнований и школьные лидеры','',f"Проверено {history['checked']}. Периоды 2017–2026 и 2022–2026. Охват частичный.",'',history['conclusion'],'','## Повторные FRC Championship Winner','',
       '| Школа / организация | Тип | 2017–2026, разные сезоны | 2022–2026 | Годы |','|---|---|---:|---:|---|']
    ranked=[]
    for e in history['entities']:
        years=sorted({r['year'] for r in history['results'] if r['entity_id']==e['id'] and r['league']=='FRC' and r['level']=='world_match'})
        if len(years)>1: ranked.append((e,years))
    for e,years in sorted(ranked,key=lambda x:(-len(x[1]),-sum(y>=2022 for y in x[1]),x[0]['name'])):
        h.append(f"| {e['name']} | {e['kind']} | {len(years)} | {sum(y>=2022 for y in years)} | {', '.join(map(str,years))} |")
    h+=['','Член победившего альянса; 2017–2019 — два Championship. Community / mixed не считаются одной школой. 2020 / 2021 не считаются поражением.','','## Методика','']+['- '+x for x in history['methodology']]
    h+=['','## Какие лиги и годы проверены','']
    for c in history['coverage']: h+=['### '+c['name'],'',c['detail'],'']+['- '+u for u in c['sources']]+['']
    h+=['## Семейные маршруты','']
    for r in history['family_routes']: h+=['### '+r['name'],'',r['detail'],'']
    h+=['## Результаты и ссылки','']
    for r in history['results']:
        h+=[f"- {r['year']} · {entities[r['entity_id']]['name']} · {r['league']} / {r['category']} · {r['stage']} · {r['award']} · {r['provenance']}. {r['note']} Источник: {r['source']}"]
    h+=['','## Пробелы','']+['- '+x for x in history['gaps']]
    (out/'STEM_school_history.md').write_text('\n'.join(h)+'\n')
(out/'STEM_league_guide.json').write_text(json.dumps({k:d[k] for k in ['league_guide','development_routes']},ensure_ascii=False,indent=2))
(out/'STEM_completeness_audit.json').write_text(json.dumps(d['completeness_audit'],ensure_ascii=False,indent=2))
a=d['completeness_audit']; n=a['counts']
report=['# STEM Atlas: аудит полноты', '', 'Проверка: '+a['checked']+f". Версия {a['version']}.", '', '**'+a['conclusion']+'**', '', a['scope'], '',
    f"Карточек в базе: {n['cards']}; соревнований: {n['competition_cards']}; событий: {n['event_cards']}; лагерей / программ: {n['camp_cards']}. Профилей лиг и программ: {n['league_profiles']}. Карточек крупных и профильных выставок: {n['major_exhibition_cards']} — это издания и площадки, не число уникальных брендов.", '',
    f"Конкретные записи есть для {n['countries_with_records']} из {len(countries)} стран и территорий; полностью проаудированных стран: {n['fully_audited_countries']}. Новых карточек: {len(a['new_ids'])}; новых профилей: {len(a['new_profiles'])}. Все прежние карточки сохранены.", '',
    '## Охват по континентам', '', '| Континент | Страны / территории с записями | Соревнования | Крупные выставки | Лагеря / программы |', '|---|---:|---:|---:|---:|']
report += [f"| {c['name']} | {c['countries_with_records']} | {c['competitions']} | {c['major_exhibitions']} | {c['camps']} |" for c in a['continents']]
report += ['',f"Межрегиональные / глобальные карточки, не приписанные одному континенту: {a['interregional_cards']}. Северная Америка включает Центральную Америку и Карибский регион. Количества показывают инвентарь базы, а не процент полноты.", '',
    f"VEX: {n['vex_cards']} из {n['competition_cards']} карточек соревнований ({100*n['vex_cards']/n['competition_cards']:.1f}%). Это явный перекос охвата.", '', '## Что осталось', '']
report += [f"- **{b['name']}**. {b['reason']}"+(f" Источник для дальнейшей проверки: {b['url']}" if b['url'] else '') for b in a['known_backlog']]
report += ['', '## Границы проверки', '']+[f"- {s}" for s in a['caveats']]+['', '## Профили лиг и программ', '']
report += [f"- **{g['name']}**: {g['cards']} карточек, {g['future_dated']} с будущими точными датами. {g['status']}. {g['source']}" for g in a['league_inventory']]
report += ['', '## Крупные выставки: календарные карточки', '']
gates={'family':'Со взрослым; условия взрослого входа отдельно','adults_only':'Детям 6/9 нельзя','confirm_children':'Детский допуск уточнить'}
report += [f"- **{e['name']}** — {e['country']}; {e['start'] or 'дата неизвестна'}"+(f" – {e['end']}" if e['end'] and e['end']!=e['start'] else '')+f". {gates[e['visitor_policy']]}. {e['source']}" for e in a['exhibition_inventory']]
report += ['', '## Добавлено в этой версии', '']
report += [f"- {e['id']} · **{e['title']}** · {e['country']} · {e['start'] or 'новые даты не объявлены'} · {e['source']}" for e in d['events'] if e['id'] in a['new_ids']]
report += ['', '## Расхождения и доступ к источникам', '']+[f"- **{s['name']}**. {s['status']}"+(f" {s['official_alternative']}" if s['official_alternative'] else '') for s in a['source_issues']]
(out/'STEM_completeness_audit.md').write_text('\n'.join(report)+'\n')
focus=a.get('focused_country')
if focus:
    local=[e for e in d['events'] if focus['iso'] in e['iso']]
    (out/'STEM_Taiwan.json').write_text(json.dumps(dict(audit=focus,events=local),ensure_ascii=False,indent=2))
    local_report=['# Taiwan STEM: семейные маршруты','',focus['family'],'',focus['conclusion'],'',focus['language_result'],'']
    for route in focus['routes']:
        local_report += ['## '+route['name'],'',route['detail'],'']
    local_report += ['## Карточки и первичные источники','']
    for e in local:
        local_report += ['### '+e['id']+' · '+e['title'],'',
            'Дата: '+(e['start']+' — '+e['end'] if e['start'] else (e['period'] or 'Период / расписание пока не установлены')),
            'Возраст: '+e['age'],'Матвей: '+e['mat'],'Оскар: '+e['osc'],
            'Язык: '+e['language'],'Вход: '+e['entry'],'Стоимость: '+e['cost'],
            'Ограничения: '+e['note'],'Источник: '+e['source'],'Проверено: '+e['checked'],'']
    local_report += ['## Ещё проверить','']+['- '+x for x in focus['open_questions']]
    (out/'STEM_Taiwan.md').write_text('\n'.join(local_report)+'\n')
south_focus=a.get('south_america_focus')
if south_focus:
    rows=[e for e in d['events'] if any(i in e['iso'] for i in south_focus['isos'])]
    (out/'STEM_South_America.json').write_text(json.dumps(dict(audit=south_focus,events=rows),ensure_ascii=False,indent=2))
    south_report=['# Южная Америка: семейные STEM маршруты','',south_focus['family'],'',south_focus['conclusion'],'',south_focus['language_result'],'']
    for route in south_focus['routes']:
        south_report += ['## '+route['name'],'',route['detail'],'']
    south_report += ['## Карточки и первичные источники','']
    for e in rows:
        south_report += ['### '+e['id']+' · '+e['title'],'',
            'Дата: '+(e['start']+' — '+e['end'] if e['start'] else (e['period'] or 'Период / расписание пока не установлены')),
            'Возраст: '+e['age'],'Матвей: '+e['mat'],'Оскар: '+e['osc'],
            'Язык: '+e['language'],'Вход: '+e['entry'],'Стоимость: '+e['cost'],
            'Ограничения: '+e['note'],'Источник: '+e['source'],'Проверено: '+e['checked'],'']
    south_report += ['## Ещё проверить','']+['- '+x for x in south_focus['open_questions']]
    (out/'STEM_South_America.md').write_text('\n'.join(line.rstrip() for line in south_report)+'\n')
local_focus=a.get('local_focus')
if local_focus:
    local=[e for e in d['events'] if any(i in e['iso'] for i in ['CRI','MEX'])]
    route_ids={id for r in local_focus['routes'] for id in r['ids']}
    # Include the virtual programme in the route export without assigning an
    # international online match to a physical country.
    local += [e for e in d['events'] if e['id'] in route_ids and e not in local]
    (out/'STEM_CostaRica_Mexico.json').write_text(json.dumps(dict(audit=local_focus,events=local),ensure_ascii=False,indent=2))
    report=['# Коста-Рика / Мексика: семейные STEM-маршруты','',local_focus['family'],'',local_focus['conclusion'],'',local_focus['language_result'],'']
    if local_focus.get('family_picks'):
        report += ['## '+local_focus['family_picks_heading'],'',local_focus['family_picks_note'],'']
        for pick in local_focus['family_picks']:
            report += ['### '+pick['country']+' · '+pick['title'],'',pick['why'],'',pick['gate'],'']
            report += ['- '+url for url in pick['source_urls']]+['']
    for r in local_focus['routes']:
        report+=['## '+r['name'],'',r['detail'],'']
    report+=['## Карточки и первичные источники','']
    for e in local:
        report+=['### '+e['id']+' · '+e['title'],'','Дата: '+(e['start']+' — '+e['end'] if e['start'] else (e['period'] or 'Период / расписание пока не установлены')),
            'Возраст: '+e['age'],'Матвей: '+e['mat'],'Оскар: '+e['osc'],'Язык: '+e['language'],
            'Вход: '+e['entry'],'Стоимость: '+e['cost'],'Ограничения: '+e['note'],'Источник: '+e['source'],'Проверено: '+e['checked'],'']
    report+=['## Ещё проверить','']+['- '+x for x in local_focus['open_questions']]
    (out/'STEM_CostaRica_Mexico.md').write_text('\n'.join(report)+'\n')
(out/'STEM_research_plan.json').write_text((ROOT/'data/research-plan.json').read_text())
if 'schools' in d:
    (out/'STEM_schools.json').write_text(json.dumps(dict(audit=d['school_focus'],schools=d['schools']),ensure_ascii=False,indent=2))
    fields=['id','name','country','iso','region','city','school_type','curriculum','ib_programmes','ages','instruction_languages','language_note','fit','boarding','boarding_note','programme','labs','ai','results','evidence','admissions','cost','questions','sources','checked','research_status']
    with (out/'STEM_schools.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        w.writerows({k:json.dumps(s[k],ensure_ascii=False) if isinstance(s[k],(list,dict)) else s[k] for k in fields} for s in d['schools'])
    with (out/'STEM_school_country_coverage.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=['iso','country','region','records','status']);w.writeheader();w.writerows(d['school_focus']['coverage'])
    report=['# Постоянные школы: первый мировой проход','',d['school_focus']['family'],'',d['school_focus']['conclusion'],'','## Границы проверки','']+['- '+s for s in d['school_focus']['methodology']]
    for s in d['schools']:
        report+=['','## '+s['id']+' · '+s['name'],'',s['country']+' · '+s['city'],'Тип: '+s['school_type'],s['curriculum'],'Возраст: '+s['ages'],'Матвей: '+s['fit']['mat']+'; Оскар: '+s['fit']['osc']+'. '+s['fit']['note'],'Язык: '+s['language_note'],'Пансион: '+s['boarding_note'],'Робототехника: '+s['programme'],'Лаборатории: '+s['labs'],'ИИ: '+s['ai'],'Приём: '+s['admissions'],'Стоимость: '+s['cost'],'']
        report+=['- Результат: '+str(r['season'])+' · '+r['league']+' · '+r['stage']+' · '+r['award']+' · '+r['team']+'. '+r['limit']+' Источник: '+r['source'] for r in s['results']]
        report+=['','Источники (проверка '+s['checked']+'):']+['- '+x['title']+': '+x['url']+' — '+x['claim'] for x in s['sources']]
        report+=['','Осталось проверить:']+['- '+x for x in s['questions']]
    report+=['','## Пробелы охвата','']+['- '+x for x in d['school_focus']['gaps']]
    (out/'STEM_schools.md').write_text('\n'.join(report)+'\n')
if 'camp_focus' in d:
    focus=d['camp_focus']; camps=[e for e in d['events'] if e['block']=='Лагеря']
    project_ids=set(focus['hack_event_ids'])
    (out/'STEM_camps.json').write_text(json.dumps(dict(audit=focus,programmes=camps,project_events=[e for e in d['events'] if e['id'] in project_ids]),ensure_ascii=False,indent=2))
    report=['# Лагеря, пансионы и детские проекты', '',focus['family'],'',focus['conclusion'],'',
        'Карточки включают разные треки / смены / площадки и регулярное обучение; это не число уникальных лагерей.','',
        'Основной технический язык, помощь на втором языке и отдельные языковые уроки имеют разные отметки. Неуточнённые прежние записи не получили подтверждённого основного языка автоматически.','']
    for route in focus['routes']:report+=['## '+route['name'],'',route['detail'],'']
    report+=['## Пробелы охвата','']+['- '+s for s in focus['gaps']]+['','## Карточки и первичные источники','']
    for e in camps+[e for e in d['events'] if e['id'] in project_ids]:
        report+=['### '+e['id']+' · '+e['title'],'','Место: '+e['country']+' · '+e['city'],
            'Дата: '+(e['start']+' — '+e['end'] if e['start'] else (e['period'] or 'Период / расписание пока не установлены')),
            'Возраст: '+e['age'],'Матвей: '+e['mat'],'Оскар: '+e['osc'],
            'Формат: '+e['participation'],'Язык: '+e['language'],
            'Языковая отметка: '+e.get('language_mode','не классифицировано')+'; поддержка: '+(', '.join(e.get('support_languages',[])) or 'не заявлена'),
            'Стоимость: '+e['cost'],'Вход: '+e['entry'],'Ограничения: '+e['note'],
            'Источник: '+e['source'],'Проверено: '+e['checked'],'']
    (out/'STEM_camps.md').write_text('\n'.join(report)+'\n')
audits=list((ROOT/'data').glob('audit-v[0-9]*.json'))
if audits:
    latest=max(audits,key=lambda p:int(re.search(r'audit-v(\d+)',p.name).group(1)))
    (out/'STEM_source_audit_latest.json').write_text(latest.read_text())
with (out/'STEM_catalog.csv').open('w',newline='',encoding='utf-8-sig') as f:
    keys=['id','block','title','country','region','city','start','end','period','date_status','deadline','deadline_label','deadline_note','deadline_utc','registration_status','age','mat','osc','format','participation','entry','gear','language','cost','scope','level','importance_reason','reward','priority','action','source','references','proof','checked','status','note','themes','languages','language_certainty','iso','related_ids','event_code','event_type','event_region','venue','admission_kind','evidence_level','published_start','published_end','sessions','planned_windows','parent_event_id','registration_url','age_reference_date','birth_start','birth_end','team_min','team_max','date_scope','exhibition_tier','visitor_policy','visitor_policy_note','adult_entry','highlights','exhibitors','exhibitor_note','exhibitor_directory_url','historical_editions','public_days','event_group','camp_dossier_slug','camp_programme_id','date_precision','date_rule','attendance_weekdays']
    keys+=['language_mode','support_languages','provider']
    w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows({k:json.dumps(e.get(k,''),ensure_ascii=False) if isinstance(e.get(k),(list,dict)) else e.get(k,'') for k in keys} for e in d['events'])
with (out/'STEM_country_coverage.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(coverage[0]));w.writeheader();w.writerows(coverage)
db=out/'STEM_database.sqlite';db.unlink(missing_ok=True)
con=sqlite3.connect(db)
# The export stores many long JSON/text records. Smaller pages reduce padding
# in the full database; a verified ZIP keeps the export portable as it grows.
# This changes storage layout only; the schema and complete records are retained.
con.execute('PRAGMA page_size=1024');con.execute('PRAGMA foreign_keys=ON')
con.executescript('''
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE countries(iso TEXT PRIMARY KEY,country TEXT NOT NULL,region TEXT NOT NULL,coverage_json TEXT NOT NULL);
CREATE TABLE events(id TEXT PRIMARY KEY,block TEXT NOT NULL,title TEXT NOT NULL,country TEXT NOT NULL,start_date TEXT,end_date TEXT,deadline TEXT,scope TEXT NOT NULL,priority TEXT NOT NULL,checked TEXT NOT NULL,source_url TEXT NOT NULL,record_json TEXT NOT NULL,CHECK(start_date IS NULL OR end_date>=start_date));
CREATE TABLE event_countries(event_id TEXT REFERENCES events(id),country_iso TEXT REFERENCES countries(iso),PRIMARY KEY(event_id,country_iso));
CREATE TABLE event_themes(event_id TEXT REFERENCES events(id),theme TEXT NOT NULL,PRIMARY KEY(event_id,theme));
CREATE TABLE sources(url TEXT PRIMARY KEY,title TEXT,evidence TEXT,checked TEXT);
CREATE TABLE camp_programmes(id TEXT PRIMARY KEY,slug TEXT UNIQUE NOT NULL,country_iso TEXT REFERENCES countries(iso),provider TEXT NOT NULL,checked TEXT NOT NULL,record_json TEXT NOT NULL);
CREATE TABLE camp_programme_sources(programme_id TEXT REFERENCES camp_programmes(id),source_url TEXT REFERENCES sources(url),PRIMARY KEY(programme_id,source_url));
CREATE TABLE camp_programme_events(programme_id TEXT REFERENCES camp_programmes(id),event_id TEXT REFERENCES events(id),relation TEXT NOT NULL,PRIMARY KEY(programme_id,event_id));
CREATE TABLE schools(id TEXT PRIMARY KEY,name TEXT NOT NULL,country_iso TEXT REFERENCES countries(iso),school_type TEXT NOT NULL,evidence TEXT NOT NULL,checked TEXT NOT NULL,record_json TEXT NOT NULL);
CREATE TABLE school_sources(school_id TEXT REFERENCES schools(id),source_url TEXT REFERENCES sources(url),PRIMARY KEY(school_id,source_url));
CREATE TABLE school_results(school_id TEXT REFERENCES schools(id),result_index INTEGER,league TEXT NOT NULL,season TEXT,stage TEXT NOT NULL,award TEXT NOT NULL,source_url TEXT REFERENCES sources(url),provenance TEXT NOT NULL,record_json TEXT NOT NULL,PRIMARY KEY(school_id,result_index));
CREATE TABLE history_entities(id TEXT PRIMARY KEY,name TEXT NOT NULL,kind TEXT NOT NULL,school_id TEXT REFERENCES schools(id),record_json TEXT NOT NULL);
CREATE TABLE history_results(id TEXT PRIMARY KEY,entity_id TEXT REFERENCES history_entities(id),year INTEGER NOT NULL,league TEXT NOT NULL,level TEXT NOT NULL,source_url TEXT REFERENCES sources(url),record_json TEXT NOT NULL);
CREATE INDEX history_year_league ON history_results(year,league);
CREATE TABLE leagues(event_id TEXT PRIMARY KEY REFERENCES events(id),record_json TEXT NOT NULL);
CREATE TABLE input_audit(id INTEGER PRIMARY KEY,record_json TEXT NOT NULL);
CREATE INDEX event_date_index ON events(start_date);
CREATE INDEX event_scope_index ON events(scope);
''')
for k in ['asof','baseline_asof','methodology','coverage_summary','expansion_log','import_audits','league_guide','development_routes','completeness_audit']: con.execute('INSERT INTO metadata VALUES (?,?)',(k,json.dumps(d[k],ensure_ascii=False)))
if 'family_context' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('family_context',json.dumps(d['family_context'],ensure_ascii=False)))
if 'camp_planning' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('camp_planning',json.dumps(d['camp_planning'],ensure_ascii=False)))
if 'camp_focus' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('camp_focus',json.dumps(d['camp_focus'],ensure_ascii=False)))
if 'school_focus' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('school_focus',json.dumps(d['school_focus'],ensure_ascii=False)))
if 'school_history' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('school_history',json.dumps({k:v for k,v in d['school_history'].items() if k not in ['entities','results']},ensure_ascii=False)))
if 'project_focus' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('project_focus',json.dumps(d['project_focus'],ensure_ascii=False)))
if 'family_strategy' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('family_strategy',json.dumps(d['family_strategy'],ensure_ascii=False)))
if 'kazakhstan_focus' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('kazakhstan_focus',json.dumps(d['kazakhstan_focus'],ensure_ascii=False)))
for focus_key in ['europe_focus','north_europe_focus','south_europe_focus','southeast_asia_focus','africa_focus','middleeast_focus','asia_english_focus','east_asia_focus']:
    if focus_key in d: con.execute('INSERT INTO metadata VALUES (?,?)',(focus_key,json.dumps(d[focus_key],ensure_ascii=False)))
if 'top_picks' in d: con.execute('INSERT INTO metadata VALUES (?,?)',('top_picks',json.dumps(d['top_picks'],ensure_ascii=False)))
for c in coverage: con.execute('INSERT INTO countries VALUES (?,?,?,?)',(c['iso'],c['country'],c['region'],json.dumps(c,ensure_ascii=False)))
for e in d['events']:
    con.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(e['id'],e['block'],e['title'],e['country'],e['start'] or None,e['end'] or None,e['deadline'] or None,e['scope'],e['priority'],e['checked'],e['source'],json.dumps(e,ensure_ascii=False)))
    con.executemany('INSERT INTO event_countries VALUES (?,?)',[(e['id'],i) for i in e['iso']])
    con.executemany('INSERT INTO event_themes VALUES (?,?)',[(e['id'],t) for t in e['themes']])
for s in d['sources']: con.execute('INSERT INTO sources VALUES (?,?,?,?)',(s['url'],s['title'],s['evidence'],s.get('checked','2026-09-29')))
if 'camp_programmes' in d:
    if 'family_review' in d['camp_programmes']:
        con.execute('INSERT INTO metadata VALUES (?,?)',('camp_family_review',json.dumps(d['camp_programmes']['family_review'],ensure_ascii=False)))
    for p in d['camp_programmes']['profiles']:
        con.execute('INSERT INTO camp_programmes VALUES (?,?,?,?,?,?)',(p['id'],p['slug'],p['iso'],p['provider'],p['checked'],json.dumps(p,ensure_ascii=False)))
        con.executemany('INSERT INTO camp_programme_sources VALUES (?,?)',[(p['id'],s['url']) for s in p['sources']])
    con.executemany('INSERT INTO camp_programme_events VALUES (?,?,?)',[(x['programme_id'],x['event_id'],x['relation']) for x in d['camp_programmes']['event_links']])
for s in d.get('schools',[]):
    con.execute('INSERT INTO schools VALUES (?,?,?,?,?,?,?)',(s['id'],s['name'],s['iso'],s['school_type'],s['evidence'],s['checked'],json.dumps(s,ensure_ascii=False)))
    con.executemany('INSERT INTO school_sources VALUES (?,?)',[(s['id'],x['url']) for x in s['sources']])
    for i,r in enumerate(s['results']):
        con.execute('INSERT INTO school_results VALUES (?,?,?,?,?,?,?,?,?)',(s['id'],i,r['league'],str(r['season']),r['stage'],r['award'],r['source'],r['provenance'],json.dumps(r,ensure_ascii=False)))
for l in d['leagues']: con.execute('INSERT INTO leagues VALUES (?,?)',(l['id'],json.dumps(l,ensure_ascii=False)))
for e in d.get('school_history',{}).get('entities',[]):
    con.execute('INSERT INTO history_entities VALUES (?,?,?,?,?)',(e['id'],e['name'],e['kind'],e['school_id'],json.dumps(e,ensure_ascii=False)))
for r in d.get('school_history',{}).get('results',[]):
    con.execute('INSERT INTO history_results VALUES (?,?,?,?,?,?,?)',(r['id'],r['entity_id'],r['year'],r['league'],r['level'],r['source'],json.dumps(r,ensure_ascii=False)))
for a in d['audit']: con.execute('INSERT INTO input_audit(record_json) VALUES (?)',(json.dumps(a,ensure_ascii=False),))
con.commit(); assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not con.execute('PRAGMA foreign_key_check').fetchall();con.close()
from database_download import package_database
database_download = package_database(db)

# The ready-to-import calendar must be generated from this same catalog, not a
# retained baseline artifact. Include actual event/score windows and distinct
# future deadlines. Undated programs and historical-only dates have no VEVENT.
def calendar_excluded(e):
    return e['priority'].startswith('P4') or e['date_status']=='Закрыто' or e.get('availability',{}).get('status')=='closed' or (e['mat'].startswith('Нет') and e['osc'].startswith('Нет'))
def ical_escape(value):
    return str(value).replace('\\','\\\\').replace('\r\n','\n').replace('\r','\n').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
def ical_fold(line):
    lines=[];chunk=''
    for char in line:
        if len((chunk+char).encode('utf-8'))>73:
            lines.append(chunk);chunk=' '+char
        else:chunk+=char
    lines.append(chunk)
    return '\r\n'.join(lines)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
cal=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//STEM Atlas//Family calendar//RU','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:STEM Atlas — даты и сроки для планирования','X-WR-TIMEZONE:America/Costa_Rica']
ical_count=0;deadline_seen=set()
def cal_event(e,uid,title,start,end,timed=False):
    global ical_count
    description=f"Идея для планирования, не принятая регистрация. ID {e['id']}. {e.get('session_note','')}. Матвей: {e['mat']}; Оскар: {e['osc']}. Как попасть: {e['entry']}. Следующий шаг: {e['action']}. {e['note']}. {e.get('deadline_note','')}. {e.get('registration_status','')}. Источник проверен {e['checked']}."
    cal.extend(['BEGIN:VEVENT','UID:stem-'+uid+'@family-stem.local','DTSTAMP:'+stamp,'SUMMARY:'+ical_escape(title),('DTSTART:' if timed else 'DTSTART;VALUE=DATE:')+start,('DTEND:' if timed else 'DTEND;VALUE=DATE:')+end,'DESCRIPTION:'+ical_escape(description),'LOCATION:'+ical_escape(e['city']+', '+e['country']),'URL:'+e['source'],'STATUS:TENTATIVE','TRANSP:TRANSPARENT','END:VEVENT'])
    ical_count+=1
for e in d['events']:
    if calendar_excluded(e):continue
    if e['start'] and e['end']>=d['asof']:
        if e.get('date_scope')=='session_days':
            for session in e['sessions']:
                if session['date']<d['asof']:continue
                row=dict(e,session_note=f"Занятие: {session['topic']}; {session['start_time']}–{session['end_time']} {session['timezone']}. {session.get('time_note','')}")
                if session.get('ical_timed'):
                    from zoneinfo import ZoneInfo
                    zone=ZoneInfo(session['timezone'])
                    start_dt=datetime.datetime.fromisoformat(session['date']+'T'+session['start_time']).replace(tzinfo=zone).astimezone(datetime.timezone.utc)
                    end_dt=datetime.datetime.fromisoformat(session['date']+'T'+session['end_time']).replace(tzinfo=zone).astimezone(datetime.timezone.utc)
                    assert end_dt>start_dt
                    cal_event(row,e['id']+'-'+session['date'],'[Учебный день] '+e['title'],start_dt.strftime('%Y%m%dT%H%M%SZ'),end_dt.strftime('%Y%m%dT%H%M%SZ'),True)
                    continue
                end=(datetime.date.fromisoformat(session['date'])+datetime.timedelta(days=1)).strftime('%Y%m%d')
                cal_event(row,e['id']+'-'+session['date'],'[Учебный день] '+e['title'],session['date'].replace('-',''),end)
        else:
            prefix='[Открытие регистрации] ' if e.get('date_scope')=='registration_open' else '[Открытие подачи проектов] ' if e.get('date_scope')=='submission_open' else '[Виртуальная защита] ' if e.get('date_scope')=='judging' else '[Окно подачи результатов] ' if e.get('date_scope')=='submission_window' else '[Дни мероприятия] ' if e.get('date_scope')=='festival_window' else '[Окно смены · расписание уточнить] ' if e.get('date_scope')=='camp_window' else '[Начало · полный период уточнить] ' if e.get('date_scope')=='activity_start' else '[Дни выбора мастер-класса] ' if e.get('date_scope')=='workshop_window' else ('[Окно дневного лагеря · Пн–Пт] ' if e.get('attendance_weekdays') else '[Окно дневного лагеря · расписание уточнить] ') if e.get('date_scope')=='day_camp_window' else '[Смена лагеря] ' if e.get('date_scope')=='camp_session' else '[Идея] '
            end=(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d')
            cal_event(e,e['id'],prefix+e['title'],e['start'].replace('-',''),end)
    deadline=e.get('deadline','')
    if deadline and deadline>=d['asof'] and (deadline,e['source']) not in deadline_seen:
        deadline_seen.add((deadline,e['source']))
        instant=e.get('deadline_utc')
        if not instant and e['id'] in ('C033','C034','C035') and deadline=='2026-10-22':instant='2026-10-22T15:59:00Z'
        if not instant and e['id']=='C025' and deadline=='2027-01-18':instant='2027-01-18T17:00:00Z'
        label=e.get('deadline_label') or 'Дедлайн'
        if instant:
            dt=datetime.datetime.fromisoformat(instant.replace('Z','+00:00')).astimezone(datetime.timezone.utc)
            cal_event(e,e['id']+'-deadline','['+label+'] '+e['title'],dt.strftime('%Y%m%dT%H%M%SZ'),(dt+datetime.timedelta(minutes=1)).strftime('%Y%m%dT%H%M%SZ'),True)
        else:
            end=(datetime.date.fromisoformat(deadline)+datetime.timedelta(days=1)).strftime('%Y%m%d')
            cal_event(e,e['id']+'-deadline','['+label+', час уточнить] '+e['title'],deadline.replace('-',''),end)
cal.append('END:VCALENDAR')
def write_ical(path,body):
    # Keep unchanged subscriptions stable even when another event is added.
    stable=lambda b:re.sub(br'(?m)^DTSTAMP:[^\r\n]*\r?\n',b'',b)
    event_pattern=br'BEGIN:VEVENT\r?\n.*?END:VEVENT\r?\n'
    if path.exists():
        old=path.read_bytes()
        if stable(old)==stable(body):return
        def uid(block):
            match=re.search(br'(?m)^UID:([^\r\n]+)',block)
            return match.group(1) if match else None
        previous={uid(m.group()):m.group() for m in re.finditer(event_pattern,old,re.S)}
        def preserve(match):
            block=match.group();before=previous.get(uid(block))
            return before if before and stable(before)==stable(block) else block
        body=re.sub(event_pattern,preserve,body,flags=re.S)
    path.write_bytes(body)
write_ical(out/'STEM_подтвержденные_даты.ics',('\r\n'.join(ical_fold(line) for line in cal)+'\r\n').encode('utf-8'))
# An independent exhibition calendar includes adult-only options with explicit
# gates. The family calendar above continues to exclude children-prohibited fairs.
expo_cal=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//STEM Atlas//Exhibitions calendar//RU','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:STEM Atlas — выставки, допуск детей отдельно','X-WR-TIMEZONE:America/Costa_Rica']
expo_count=0
for e in d['events']:
    if not e.get('exhibition_tier') or not e['start'] or e['end']<d['asof']:continue
    gate={'family':'семейный вариант','adults_only':'детям 6/9 нельзя','confirm_children':'допуск детей уточнить'}[e['visitor_policy']]
    desc=f"Идея посещения, не принятая регистрация. {e['visitor_policy_note']} Взрослый вход: {e['adult_entry']}. {e['note']} Компании: {e['exhibitor_note']}. Источник проверен {e['checked']}."
    expo_cal.extend(['BEGIN:VEVENT','UID:stem-exhibition-'+e['id']+'@family-stem.local','DTSTAMP:'+stamp,'SUMMARY:'+ical_escape('[Выставка · '+gate+'] '+e['title']),'DTSTART;VALUE=DATE:'+e['start'].replace('-',''),'DTEND;VALUE=DATE:'+(datetime.date.fromisoformat(e['end'])+datetime.timedelta(days=1)).strftime('%Y%m%d'),'DESCRIPTION:'+ical_escape(desc),'LOCATION:'+ical_escape(e['city']+', '+e['country']),'URL:'+e['source'],'STATUS:TENTATIVE','TRANSP:TRANSPARENT','END:VEVENT'])
    expo_count+=1
expo_cal.append('END:VCALENDAR')
write_ical(out/'STEM_крупные_выставки.ics',('\r\n'.join(ical_fold(line) for line in expo_cal)+'\r\n').encode('utf-8'))
print(json.dumps({'events':len(d['events']),'dated':sum(bool(e['start']) for e in d['events']),'ical_events':ical_count,'exhibition_ical_events':expo_count,'coverage':d['coverage_summary'],'database':str(out/database_download['download']),'database_download':database_download}))
