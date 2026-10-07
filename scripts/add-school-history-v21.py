"""One-time, evidence-bounded retrospective. Run before build-database.py."""
import copy, json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
WORK=ROOT.parent/'stem-family-atlas-work'
d=json.loads((ROOT/'data/catalog.json').read_text()); assert 'school_history' not in d
CHECKED='2026-10-01'
entities={}; results=[]; receipts=[]
def source(url,title,claim,kind='organizer'):
    if url not in {s['url'] for s in d['sources']}:
        d['sources'].append(dict(url=url,title=title,evidence=claim,checked=CHECKED))
    return dict(url=url,title=title,claim=claim,kind=kind,checked=CHECKED)
def entity(id,name,kind,country,age='secondary',school_id=None,note=''):
    entities[id]=dict(id=id,name=name,kind=kind,country=country,age=age,school_id=school_id,note=note)
def result(e,year,league,category,stage,award,level,url,provenance='organizer_protocol',team='',team_id=None,note=''):
    r=dict(id='H'+str(len(results)+1).zfill(3),entity_id=e,year=year,league=league,category=category,stage=stage,award=award,level=level,source=url,provenance=provenance,team=team,team_id=team_id,note=note,checked=CHECKED)
    results.append(r); return r
frc={
 '973':('Atascadero High School','Greybots','school','USA','S018'),
 '1011':('Sonoran Science Academy · Tucson','CRUSH','school','USA',None),
 '2928':('Ballard High School','Viking Robotics','school','USA',None),
 '5499':('Berkeley High School','The Bay Orangutans','school','USA',None),
 '2767':('Stryke Force · Kalamazoo County 4-H','Stryke Force','community','USA',None),
 '254':('Bellarmine College Preparatory','The Cheesy Poofs','school','USA','S012'),
 '862':('Plymouth-Canton district · 3 школы','Lightning Robotics','mixed','USA',None),
 '1676':('Pascack Valley Regional High School District','The Pascack PI-oneers','mixed','USA',None),
 '148':('Greenville High School','Robowranglers','school','USA',None),
 '2976':('Skyline High School · Washington','Spartabots','school','USA',None),
 '3075':('Hadarim High School','Ha-Dream Team','school','Israel',None),
 '27':('Clarkston High School','Team RUSH','school','USA',None),
 '2708':('Limestone District School Board','Lake Effect Robotics','mixed','Canada',None),
 '4027':('Centre County 4-H','Centre County 4-H Robotics','community','USA',None),
 '1323':('Madera High School','MadTown Robotics','school','USA','S017'),
 '5026':('Burlingame High School','The Iron Panthers','school','USA','S019'),
 '4201':('Da Vinci Science','The Vitruvian Bots','school','USA',None),
 '3707':('Brighton High School','Brighton TechnoDogs','school','USA',None),
 '217':('Utica Community Schools','ThunderChickens','mixed','USA',None),
 '4481':('Rembrandts · AAE / Fontys / school partners','Team Rembrandts','mixed','Netherlands',None),
 '1218':('Springside Chestnut Hill Academy','SCH Vulcan Robotics','school','USA',None),
 '1619':('GEAR Alliance · Up-A-Creek','Up-A-Creek Robotics','community','USA',None),
 '3175':('University Liggett School','Knight Vision','school','USA',None),
 '6672':('Cistercian Preparatory School','Fusion Corps','school','USA',None),
 '4414':('HighTide · community team','HighTide','community','USA',None),
 '4096':('Ctrl-Z · community team','Ctrl-Z','community','USA',None),
 '2609':('Our Lady of Lourdes Catholic High School','Beaverworx','school','Canada',None),
 '1690':('Cramim Atid · Binyamina','Orbit','school','Israel',None),
 '4522':('Smith-Cotton High School','Team SCREAM','school','USA',None),
 '9432':('Team 8-Bit · community team','Team 8-Bit','community','USA',None),
 '321':('Central High School · Philadelphia','RoboLancers','school','USA',None),
 '2910':('Henry M. Jackson High School','Jack in the Bot','school','USA',None),
 '4272':('McCutcheon High School','Maverick Robotics','school','USA',None),
 '4065':('Lake Minneola High School','Nerds of Prey','school','USA',None),
 '1538':('High Tech High School','The Holy Cows','school','USA',None),
 '3132':('Thunder Down Under · several schools','Thunder Down Under','mixed','Australia',None),
 '2614':('Mountaineer Area RoboticS','MARS','community','USA',None),
 '1311':('Kell Robotics · several schools','Kell Robotics','mixed','USA',None),
 '2834':('Bloomfield Hills High School','Bionic Black Hawks','school','USA',None),
 '1902':('Orange County 4-H','Exploding Bacon','community','USA',None),
 '1816':('Edina Senior High School','The Green Machine','school','USA',None),
 '1629':('Northern / Southern Garrett High Schools','Garrett Coalition','mixed','USA',None),
 '2486':('Coconino High School','CocoNuts','school','USA',None),
 '5985':('Project Bucephalus · community team','Project Bucephalus','community','Australia',None),
 '6352':('LAUNCH TEAM · community team','LAUNCH TEAM','community','USA',None),
}
for id,(name,team,kind,country,sid) in frc.items():
    entity('FRC'+id,name,kind,country,school_id=sid,note='Школьная / общественная связь прочитана в протоколе указанного сезона. Приём, текущий состав и язык не установлены; страна указана для организации, а не для поездки на финал.')
extracted=json.loads((WORK/'frc-history-extract-v21.json').read_text())
assert len(extracted)==11 and not any(x.get('error') for x in extracted)
for event in extracted:
    y=event['year']; place={'CMPTX':'Houston','CMPMO':'St Louis','CMPMI':'Detroit'}[event['event']]
    u=event['url']; source(u,f'FIRST official {y} {place} awards','Championship Winner и главный Chairman / Impact; школьная связь в таблице')
    receipts.append(dict(url=u,year=y,sha256=event['sha256'],categories=['Championship Winner','Chairman / FIRST Impact Award']))
    for row in event['rows']:
        if row['text'].startswith('Championship Winner '):
            id=row['teams'][0]; result('FRC'+id,y,'FRC','High school',f'FIRST Championship · {place}','Championship Winner','world_match',u,team=frc[id][1],team_id=id,note='Член победившего альянса; не индивидуальный титул и не победа дивизиона. В 2017–2019 были два самостоятельных Championship. Festival of Champions 2017 вне данной серии.')
        elif row['text'].startswith(("Chairman's Award ",'FIRST Impact Award ')) and 'Finalist' not in row['text']:
            id=row['teams'][0]; result('FRC'+id,y,'FRC','High school',f'FIRST Championship · {place}',"Chairman's Award" if y<2023 else 'FIRST Impact Award','world_judged',u,team=frc[id][1],team_id=id,note='Главная оценённая награда за программу и влияние; считается отдельно от результата матчей.')
assert sum(r['level']=='world_match' for r in results)==44
assert sum(r['level']=='world_judged' for r in results)==11
result('FRC254',2026,'FRC','High school','FIRST Championship · Curie Division','Championship Division Winner','world_division','https://frc-events.firstinspires.org/2026/team/254',team='The Cheesy Poofs',team_id='254',note='Победа Curie Division, не Championship Winner мирового финала 2026.')
def school_source(sid,url,title,claim,kind='organizer'):
    s=next(s for s in d['schools'] if s['id']==sid); x=source(url,title,claim,kind)
    if url not in {x['url'] for x in s['sources']}: s['sources'].append(x)
    return s
for r in list(results):
    sid=entities[r['entity_id']]['school_id']
    if sid=='S012':
        s=school_source(sid,r['source'],'FIRST Championship awards',r['award'])
        s['results'].append(dict(league='FIRST Robotics Competition',season=r['year'],stage=r['stage'],award=r['award'],team=r['team'],team_id=r['team_id'],source=r['source'],provenance=r['provenance'],limit=r['note']))
def new_school(id,name,iso,city,school_type,ages,sources,programme,admissions,language=[],fit='future',cost='Актуальные расходы на обучение, команду и поездки не установлены.'):
    c=next(c for c in d['countries'] if c['iso']==iso)
    s=dict(id=id,name=name,iso=iso,country=c['country'],region=c['region'],city=city,school_type=school_type,curriculum=ages,ib_programmes=[],ages=ages,instruction_languages=language,language_note='EN преподавание и поддержка новичков отдельно не подтверждены.' if not language else 'EN / другая языковая ступень подтверждается указанным источником; язык команды отдельно уточнить.',fit=dict(mat=fit,osc=fit,note='Школьная ступень подходит для дальнейшей проверки; поступление и место в команде не подтверждены.' if fit=='candidate' else 'Оба ребёнка младше high school; маршрут на подростковый возраст.'),boarding='unknown',boarding_note='Пансион не подтверждён.',programme=programme,labs='Оборудование, часы работы и доступ новичков уточнить у действующей команды.',ai='Отдельный AI-курс не установлен.',results=[],evidence='world_result',admissions=admissions,cost=cost,questions=['Уточнить язык команды, минимальный класс, отбор и реальные обязанности новичка.','Проверить тренера, доступ к лаборатории, расходы и график текущего сезона.'],sources=[source(*x) for x in sources],checked=CHECKED,priority=2,research_status='partial',verification='Документальная проверка; школа и команда не подтверждали приём детей.')
    d['schools'].append(s); return s
for sid,tid,name,city,registry,ages in [
 ('S017','1323','Madera High School','Madera · California','https://www.cde.ca.gov/schooldirectory/details?cdscode=20652432035707','Государственная High School · Grades 9–12 по CDE, запись обновлена 25.08.2026.'),
 ('S018','973','Atascadero High School','Atascadero · California','https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?ID=060330000247','Государственная High School · Grades 9–12 по NCES, данные 2024–2025.'),
 ('S019','5026','Burlingame High School','Burlingame · California','https://www.cde.ca.gov/SchoolDirectory/details?cdscode=41690474130472','Государственная High School · Grades 9–12 по CDE, запись обновлена 25.08.2026.')]:
    programme='FRC '+tid+' · '+frc[tid][1]+'. Повторные Championship Winner в официальных протоколах.'
    src=[(registry,'Official school directory','Тип и Grades 9–12','government')]
    if tid=='5026': src.append(('https://ironpanthers.com/join','Iron Panthers recruitment 2026','Представляет BHS; вход всем ученикам школы; Fall 2026 нагрузка','school_team'))
    if tid=='973': src.append(('https://www.greybots.com/','Greybots','Действующая high school команда; 2019 Houston title','school_team'))
    s=new_school(sid,name,'USA',city,'public',ages,src,programme,'Проверить правила школьного округа, адрес / резидентство, документы и международную заявку; доступ иностранца не установлен.')
    for r in results:
        if r['entity_id']=='FRC'+tid:
            school_source(sid,r['source'],'FIRST official awards',r['award'])
            s['results'].append(dict(league='FIRST Robotics Competition',season=r['year'],stage=r['stage'],award=r['award'],team=r['team'],team_id=tid,source=r['source'],provenance=r['provenance'],limit=r['note']))
    if tid=='5026': s['programme']+=' Команда сообщает о 60+ учениках; опыт до вступления не обязателен. Junior outreach / лагерь не равны месту в FRC.'

# WRO: exact first place in seven explicitly selected categories, not all gold medals.
wro=json.loads((WORK/'wro-winners-v21.json').read_text()); assert len(wro)==28
for x in wro:
    assert x['category'] in ['RoboMission','Future Innovators','Future Engineers']
    id='WRO'+str(x['year'])+re.sub('[^A-Za-z]','',x['category']+x['age_group'])
    name=re.sub(r'^\d+ - ','',x['team']); name=re.sub(r' \([KL]\d+\)$','',name)
    entity(id,name,'unresolved',x['country'],age='primary' if x['age_group']=='Elementary' else 'secondary',note='Протокол подтверждает команду и страну. Школа, клуб, внешние наставники и открытый набор не определены; похожие имена разных сезонов автоматически не объединяются.')
    source(x['source'],f'WRO International Final {x["year"]} scoring','Первые места RM / FI по трём возрастам и Future Engineers')
    result(id,x['year'],'WRO',x['category']+' · '+x['age_group'],'WRO International Final','1-е место','world_match' if x['category']=='RoboMission' else 'world_judged' if x['category']=='Future Innovators' else 'world_skills',x['source'],team=name,note='Первое место конкретной категории. Gold medal без первого места не приравнивается к победе. RoboSports и специальные награды не входят в этот извлечённый набор.')
for u in sorted({x['source'] for x in wro}):
    a=[x for x in wro if x['source']==u]; receipts.append(dict(url=u,year=a[0]['year'],sha256=a[0]['sha256'],categories=['RoboMission Elementary/Junior/Senior','Future Innovators Elementary/Junior/Senior','Future Engineers']))
sprout=next(e for e in entities.values() if e['name']=='Sprout')
sprout['note']='Команда Costa Rica; WRO называет тренером отца участников. Связь с Lincoln встречается в местной публикации, но официальный школьный статус команды и вклад школы здесь не подтверждены.'
source('https://wro-association.org/wro-2025-concludes-host-2026-revealed/','WRO 2025 wrap-up','Sprout Future Innovators Senior; семейное наставничество')

# Literal school-reported achievements already audited in the school catalogue.
levels={'S003':['world_division'],'S008':['world_judged','national_match','national_skills'],'S013':[],'S014':['world_division','world_judged'],'S015':['world_judged'],'S006':['national_match','national_match','national_other']}
for sid in ['S003','S008','S014','S015','S006']:
    s=next(s for s in d['schools'] if s['id']==sid); entity(sid,s['name'],'school',s['country'],'primary' if sid=='S006' else 'secondary',sid)
    for i,r in enumerate(s['results']):
        result(sid,int(r['season']), 'VEX' if 'VEX' in r['league'] else 'FLL' if 'LEGO' in r['league'] else 'FRC' if 'FIRST Robotics' in r['league'] else 'Singapore national',r['league'],r['stage'],r['award'],levels[sid][min(i,len(levels[sid])-1)],r['source'],r['provenance'],r['team'],r.get('team_id'),r.get('limit',''))
hu='https://www.horizonpri.moe.edu.sg/our-pride/achievements/achievements-2024/'
hs=school_source('S006',hu,'Horizon official 2024 achievements','NRPC overall; IDE Sumobot / Maker; WRO Nationals Elementary','public_school')
for league,award in [('National Robotics Programming Competition','Overall Champion'),('IDE Primary Sumobot','1-е место'),('IDE Maker Primary','Champion'),('WRO RoboMission Elementary · Singapore Nationals','Champion / Best Performing School')]:
    result('S006',2024,'WRO' if league.startswith('WRO') else 'Singapore national',league,'Singapore national',award,'national_match',hu,'school_report',team='Horizon Star Coders / Robotics CCA',note='Национальный этап. Школьная страница CCA прямо называет WRO Nationals; не WRO International Final.')
    hs['results'].append(dict(league=league,season=2024,stage='Singapore national',award=award,team='Horizon Star Coders / Robotics CCA',team_id=None,source=hu,provenance='school_report',limit='Национальные результаты; не мировой финал.'))
qe='https://www.qebarnet.co.uk/category/stem/'
school_source('S008',qe,'QE STEM reports 2026','6 VEX Worlds qualifiers; Intel UK age-category firsts 2024 / 2025','school')
school_source('S008','https://www.qebarnet.co.uk/robotics-teams-qualify-for-world-championships-at-the-very-first-attempt-2/','QE Worlds qualification 2017','Две команды получили Worlds qualification','school')
result('S008',2017,'VEX','IQ','Worlds qualification','2 команды квалифицированы','qualification','https://www.qebarnet.co.uk/robotics-teams-qualify-for-world-championships-at-the-very-first-attempt-2/','school_report',note='Квалификация не является мировым титулом.')
result('S008',2026,'VEX','IQ / V5','Worlds qualification','6 школьных команд квалифицированы','qualification',qe,'school_report',note='3 IQ + 3 V5. Независимая и смешанная команды школьников описаны отдельно; они не добавлены к школьной шестёрке.')
for y in [2024,2025]: result('S008',y,'AI / Intel','Возрастная категория · UK','Intel AI Global Impact Festival · UK','1-е место среди UK entrants','national_other',qe,'school_report',team='Paarth Aggarwal',note='Отчёт школы; национальный результат в рамках глобального фестиваля. Не мировой Gold Award.')
url='https://www.hawaiianelectric.com/documents/about_us/news/2024/20240220_hawaii_vexiq_robotics_teams_qualify_for_world_championship.pdf'
s=school_source('S013',url,'Hawaiʻi Space Grant 2024 results','Mānoa Green Tigers: state Excellence + Teamwork Champion','regional_organizer')
entity('S013',s['name'],'school',s['country'],'primary','S013')
s['evidence']='national_result'
for award,level in [('Excellence Award','regional_judged'),('Teamwork Champion','regional_match')]:
    s['results'].append(dict(league='VEX IQ',season=2024,stage='Hawaiʻi State Championship · elementary',award=award,team='Green Tigers',team_id=None,source=url,provenance='organizer_protocol',limit='Штат Hawaiʻi; квалификация на Worlds, не победа мирового финала.'))
    result('S013',2024,'VEX','IQ Elementary','Hawaiʻi State Championship',award,level,url,team='Green Tigers',note='Совместная Teamwork победа с Hāleʻiwa; государственный elementary-кейс, а не мировой титул.')

asturl='https://www.astaichung.com/articles/51?locale=tw'
s=new_school('S020','American School in Taichung · AST','TWN','Taichung','private','Elementary G1–5; Middle G6–8; High G9–12. G1 с 6 лет к 31 августа.',[
 ('https://www.astaichung.com/policies_procedures','Admission requirements','Non-ROC / non-PRC passport; EN interview / tests; G1 minimum age','school'),
 ('https://www.astaichung.com/elementary','Elementary curriculum','ICT, STEM makerspace, English Language Arts','school'),
 ('https://www.astaichung.com/robotics','TAI-VEX programme','Elementary–High School; 2023 семь Worlds-команд G5–12; 2022 World Champions без категории','school'),
 (asturl,'2024 VEX Worlds report','66799T division title; 66799E Build; точная overall категория не установлена','school'),
 ('https://www.astaichung.com/tuition_fees','Tuition and fees','G1–5 NTD249500 / semester; год таблицы не указан','school')],
 'TAI-VEX / AST-onishing. Junior makerspace, robotics Elementary–High School; соревновательные Worlds команды 2023 указаны для G5–12.',
 'G1: EN interview; G2+: English proficiency и math test на EN. Действующий иностранный паспорт и предыдущие оценки; точный класс / EAL / место определяет admissions.',fit='candidate',cost='Таблица без указанного учебного года: Elementary NTD249500 за семестр; application 3000, entrance 50000, annual registration 40000, capital 30000 за семестр; поддержку, поездки, еду и автобус проверять отдельно.')
s['language_note']='EN interview и English/math assessment подтверждены. Наличие English Language Arts и ICT не устанавливает язык каждого предмета или язык тренера; основной технический EN нужно подтвердить.'
entity('S020',s['name'],'school',s['country'],'primary','S020',note='У школы есть elementary; World-команды описаны для более старших. Шестилетний новичок не считается членом команды мирового уровня.')
for year,award,level,url,team,tid,note in [
 (2022,'World Champions · категория не указана','unclassified','https://www.astaichung.com/robotics','AST-onishing',None,'Самоописание школы; точный протокол, категория и награда не установлены. Не включено в счёт мировых побед.'),
 (2023,'7 команд квалифицированы / отправлены','qualification','https://www.astaichung.com/robotics','AST-onishing',None,'G5–12; Worlds qualification не равно титул.'),
 (2024,'Division Champion','world_division',asturl,'AST-onishing','66799T','По отчёту школы. Не абсолютная Teamwork победа; Skills / Teamwork третьи места не классифицированы без division / overall протокола.'),
 (2024,'Build Award','world_judged',asturl,'AST-onishing','66799E','По отчёту школы; награда мирового события. Дивизион / общий уровень награды уточнить.')]:
    result('S020',year,'VEX','IQ / V5 · категория требует протокола','VEX Worlds',award,level,url,'school_report',team,tid,note)
    s['results'].append(dict(league='VEX',season=year,stage='VEX Worlds',award=award,team=team,team_id=tid,source=url,provenance='school_report',limit=note))

fll=[(2022,'Legotronics Beavers','Spain','https://fllblog.wordpress.com/2022/04/28/2022-first-lego-league-world-festival-recap/'),(2023,'FSINGENIUM Team','Spain','https://fllblog.wordpress.com/2023/04/28/thats-a-wrap-on-firstchamp/'),(2024,'LOS ATOMICOS','Brazil','https://fllblog.wordpress.com/2024/04/26/its-time-for-a-firstchamp-curtain-call/'),(2026,'ROBOTECH','Spain','https://www.archaeological.org/team-robotech-of-barcelona-wins-the-2026-first-lego-league-champions-award/')]
for year,name,country,u in fll:
    id='FLL'+str(year);entity(id,name,'unresolved',country,'unknown',note='Команда подтверждена; школьная принадлежность / смешанный состав не установлены. Не перенесено на школу по названию города или клуба.')
    source(u,f'FLL Champion’s Award {year}','Победитель конкретного World Festival года','season_partner' if year==2026 else 'organizer')
    result(id,year,'FLL','Challenge','FIRST World Festival · Houston','Champion’s Award Winner','world_judged',u,'season_partner_report' if year==2026 else 'organizer_protocol',name,note='Комплексная оценённая награда FLL. Не отдельно победа Robot Performance. Школа команды ещё не определена.')
u='https://fllblog.wordpress.com/2024/04/26/its-time-for-a-firstchamp-curtain-call/'
entity('FLLHeroes2024','SESI Heroes · кампус 2024 не установлен','unresolved','Brazil','unknown',note='Организатор называет команду; соответствие конкретному кампусу SESI Jundiaí этого года не доказано.')
result('FLLHeroes2024',2024,'FLL','Challenge','FIRST World Festival · Houston','Innovation Project Award Finalist','world_finalist',u,team='SESI Heroes',note='SESI Heroes названа организатором; связь с тем же кампусом в этом году требует отдельного подтверждения.')
school_source('S015',u,'Official FLL 2024 results','Heroes Innovation Project Award Finalist')

ai='https://www.waicy.org/waicy-2025/'
source(ai,'WAICY 2025 Global winners','Школы названы буквально; Global и Country различаются')
entity('NEOM','NEOM Community School','school','Saudi Arabia','primary',note='Одна подтверждённая глобальная редакция 2025. Приём, кампус и EN junior не исследованы; устойчивое 5-летнее лидерство не доказано.')
entity('MISK','Misk Schools','school','Saudi Arabia','primary','S021',note='Global Elementary LLM Silver; не Country first place. Один сезон не подтверждает многолетнее лидерство.')
for e,cat,award,project in [('NEOM','Elementary · AI Showcase','Silver Award','Lugagge Sense'),('NEOM','Elementary · AI Showcase','Bronze Award','LAN-GI'),('MISK','Elementary · AI Large Language Model','Silver Award','Sleep Buddy')]:
    result(e,2025,'WAICY',cat,'WAICY Global',award,'world_judged',ai,team=project,note='Награда указанного трека и возраста. Не Global overall championship, не country award; не доказательство повторного лидерства.')
s=new_school('S021','Misk Schools','SAU','Riyadh','private','PreK–Grade12; официальный сайт описывает Lower Primary 6–9. Точный минимальный возраст ежегодно определяет Ministry of Education.',[
 ('https://www.miskschools.edu.sa/about-us','About Misk Schools','Private international; British / Saudi; EN + Arabic','school'),
 ('https://www.miskschools.edu.sa/faqs','Age FAQ','Minimum age refreshed by Ministry of Education','school'),
 ('https://www.miskschools.edu.sa/arabic/home','Learning journey','Lower Primary ages6–9','school'),
 (ai,'WAICY organizer Global winners','Elementary LLM Sleep Buddy Silver','organizer')],
 'Проверяемый AI-кейс: Sleep Buddy Global Silver 2025. Техническая школьная программа и роботокоманда требуют отдельного аудита.',
 'Международный приём, residency, точный класс и язык команды не подтверждены. Проверить возможность набора иностранной семьи.',language=['EN'],fit='candidate')
s['language_note']='Школа прямо указывает обучение на English и Arabic; отдельный язык AI / robotics группы уточнить.'
s['results'].append(dict(league='WAICY',season=2025,stage='WAICY Global · Elementary LLM',award='Silver Award',team='Sleep Buddy',team_id=None,source=ai,provenance='organizer_protocol',limit='Трековая глобальная серебряная награда. Country first place этой команды — отдельная награда; не суммировать.'))

coverage=[
 dict(id='FRC',name='FIRST Robotics Competition',role='Подростковая инженерия; крупные роботы и альянсы',status='bounded_complete',detail='Все 44 Championship Winner и 11 Chairman / Impact Winner в 11 сыгранных Championship 2017–2019 и 2022–2026. Полнота относится к этим двум категориям, а не ко всем наградам / дивизионам / местным этапам.',years={str(y):'complete' if y not in [2020,2021] else 'cancelled' if y==2020 else 'awards_only' for y in range(2017,2027)},sources=[x['url'] for x in extracted]),
 dict(id='WRO',name='World Robot Olympiad',role='Junior / elementary робототехника и инновационные проекты',status='partial',detail='2022–2025: извлечены 28 первых мест в семи категориях RM / FI / FE. RoboSports, все медали, специальные награды и школьные связи не проаудированы. International Final 2026 ещё впереди; Open не подменяет Final.',years={str(y):'complete_selected' if y in range(2022,2026) else 'pending' if y==2026 else 'archive_gap' for y in range(2017,2027)},sources=sorted({x['source'] for x in wro})+['https://wro-association.org/competition/international-events/']),
 dict(id='VEX',name='VEX IQ / V5',role='Доступный младший путь; отдельные возрастные финалы',status='partial',detail='Документированы кейсы QE, TAS, AST, Mānoa. 2018 Overall Excellence, 2024 / 2025 division и национальные результаты разделены. Десятилетний полный протокол всех возрастов не собран.',years={str(y):'case' if y in [2017,2018,2022,2023,2024,2025,2026] else 'archive_gap' for y in range(2017,2027)},sources=['https://events.vex.com/robot-competitions/vex-iq-competition/RE-VIQRC-26-4029.html','https://www.qebarnet.co.uk/beyond-the-classroom/clubs-extra-curricular/robotics-showcase/','https://www.astaichung.com/robotics']),
 dict(id='FLL',name='FIRST LEGO League Challenge',role='Robot game + исследование + командная работа',status='partial',detail='Champion’s Award 2022–2026: 2022–2024 протоколы организатора, 2025 отчёт SESI-SP, 2026 рассказ партнёра сезона AIA. Полные ранние годы и школьные связи большинства победителей ещё не собраны.',years={str(y):'protocol' if y in [2022,2023,2024] else 'report' if y in [2025,2026] else 'archive_gap' for y in range(2017,2027)},sources=[x[3] for x in fll]+[next(s for s in d['schools'] if s['id']=='S015')['results'][0]['source']]),
 dict(id='WAICY',name='WAICY · ИИ',role='Глобальные AI-проекты / LLM / art / video; с 6 лет',status='partial',detail='Существует с 2018. Открыт официальный архив 2018–2025; добавлены школьные результаты Global 2025. Нет доказанного 5–10-летнего школьного лидера: часто указан проект / страна без школы. Результаты 2026 не сформированы.',years={str(y):'not_started' if y==2017 else 'case' if y==2025 else 'pending' if y==2026 else 'archive_gap' for y in range(2017,2027)},sources=['https://www.waicy.org/',ai]),
 dict(id='FTC',name='FIRST Tech Challenge',role='Подростковая инженерия; Inspire отдельно от Winning Alliance',status='gap',detail='Лига и маршруты есть в атласе. Полная история мировых winning / Inspire команд и их школьных связей в этом наборе ещё не восстановлена.',years={str(y):'archive_gap' for y in range(2017,2027)},sources=['https://ftc-events.firstinspires.org/']),
 dict(id='RoboCupJunior',name='RoboCupJunior',role='Автономные rescue / soccer / onstage роботы',status='gap',detail='Открыт официальный итоговый сайт 2025. Полная серия Junior результатов и соответствие школам отсутствуют. KidSize / университетские Major-лиги нельзя считать детскими по имени категории.',years={str(y):'archive_gap' for y in range(2017,2027)},sources=['https://2025.robocup.org/wrap-up/']),
]
for c in coverage:
    for u in c['sources']: source(u,c['name']+' archive / rules',c['detail'])
for u,title,claim in [('https://frc-events.firstinspires.org/2021/CMPAW','FIRST 2021 awards-only event','Championship cancelled; remote awards distinct'),('https://www.firstinspires.org/sites/default/files/uploads/annual-report/fy2020-annual-impact-report.pdf','FIRST 2020 impact report','2020 Championship cancellation')]:source(u,title,claim)
d['school_history']=dict(version=21,checked=CHECKED,status='partial',period=[2017,2026],recent_period=[2022,2026],entities=list(entities.values()),results=results,coverage=coverage,
 conclusion='Повторное лидерство надёжнее всего доказано внутри FRC: Madera 4, Bellarmine 3, Atascadero и Burlingame по 2 победных сезона. Это история конкретной лиги и старших команд, не общий рейтинг школ мира.',
 methodology=['Считаем разные сезоны победы одной команды, а не число сертификатов. Сезоны 2017–2026 — десять календарных лет; последние пять — 2022–2026 по состоянию на 01.10.2026.',
 'FRC Championship Winner означает члена победившего альянса. 2017–2019 имели два финальных Championship; отдельный Festival of Champions 2017 вне этой серии. 2020 отменён, 2021 имел отдельные awards-only форматы; отсутствие матчевого титула в эти годы не считается поражением.',
 'Абсолютная победа, оценённая награда, division, финалист, национальный / штатный результат и квалификация не складываются в общий балл. Отсутствие записи означает пробел, а не отсутствие участия / проигрыш.',
 'Результат школы относится к конкретному кампусу, команде и году. Community, district, смешанные команды и неизвестная школьная связь видны отдельно. Страны описывают организации; финал мог проходить в другой стране.',
 'В WRO выведены только первые места семи категорий. Много Gold medals не означает много победителей категории. Similar team names не устанавливают тождество команды или школы между годами.',
 'В VEX school-report World Champions без категории остаётся неклассифицированным. В ИИ Global и Country awards, возраст и трек сохраняются буквально. Школьный report отличается от протокола организатора.',
 'Коммерческие доли рынка, стоимость обучения и академическое качество по титулу команды не измеряются. Список лидеров — вывод по проверенным соревнованиям, а не полный мировой рыночный рейтинг.'],
 family_routes=[
 dict(name='Сейчас · 6 и 9 лет',ids=['S006','S003','S020','S001','S002'],detail='Проверять junior наставника, глубину задач после трёх лет соревнований и реальный вход в команду. Horizon показывает повторные национальные результаты; TAS / AST — путь junior → старшие VEX. Costa Rica / México остаются первыми по доступности, но школа не обязана быть источником мирового титула.'),
 dict(name='К 10–12 годам',ids=['S008','S003','S020'],detail='Выбрать одну техническую лигу на сезон плюс собственный AI-проект; фиксировать код, журнал сборки, видео автономности и личный вклад. QE — будущий 11+ конкурс; AST Worlds 2023 описывает G5–12. Возраст, школа и национальный допуск уточняются отдельно.'),
 dict(name='Подростковый мировой уровень',ids=['S017','S012','S019','S018'],detail='Рассмотреть доказанную FRC-программу и сравнить доступ новичка, наставника, роль в команде, мастерскую и нагрузки. Madera имеет 3 победных сезона в последних пяти, Bellarmine и Burlingame по одному; Atascadero — 2 исторических сезона и ни одного Championship Winner в 2022–2026. Это не отсутствие других наград.'),
 dict(name='ИИ как отдельный путь',ids=['S021','S008'],detail='Misk: официальный Global Elementary LLM Silver 2025; многолетнее лидерство не доказано. QE: UK age-category Intel first 2024 / 2025, будущая secondary. WAICY допускает с 6 лет и дистанционные проекты; для реального навыка оценивать код / данные / объяснение ребёнка отдельно от AI-art наград.')],
 gaps=['Полный десятилетний многолиговый рейтинг школ не завершён: FTC, RoboCupJunior, ранние WRO / FLL, все возрастные VEX, MakeX, IRO, ENJOY AI требуют отдельного восстановления.',
 'Азиатские WRO победители найдены, но принадлежность к школам ещё не доказана. Например UP UP CHM 2024 / 2025 не объединены автоматически; World Open Italy не смешивается с International Final Türkiye.',
 'У Sprout Costa Rica титул Senior 2025 подтверждён WRO; связь с Lincoln и роль внешнего семейного тренера нельзя превратить в победу формальной школьной команды без доказательства.',
 'Для большинства лидеров нет подтверждённого международного приёма, языка технической группы, места для 6 / 9 лет и полного бюджета. Пансионы с красивой STEM-программой не считаются победителями без результата.'])
d['school_focus']['version']=21;d['school_focus']['conclusion']='Каталог расширен и добавлена ретроспектива 2017–2026. Полный школьный мировой аудит не завершён; возрастная кандидатура не подтверждает приём / команду.'
d['school_focus']['gaps'][0]='21 школа в 14 странах; мировой справочник 249 стран и территорий. Полностью проаудированных стран по школам: 0.'
d['school_focus']['routes'][1]['ids'].append('S020')
d['school_focus']['routes'][3]['ids']+=['S017','S018','S019']
d['completeness_audit']['version']=21
d['completeness_audit']['school_history']=dict(status='partial',period=[2017,2026],results=len(results),frc_championship_winner_rows=44,frc_main_judged_winner_rows=11,wro_selected_first_places=28,limit='Полнота относится к указанным FRC категориям; школы и другие лиги исследованы частично.')
(ROOT/'data/catalog.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/history-source-receipts-v21.json').write_text(json.dumps(dict(checked=CHECKED,receipts=receipts,interpretation='Хеши публичных документов на момент извлечения. Персональные данные учеников не архивируются. Школьные новости читаются отдельно и не выдаются за независимые протоколы.'),ensure_ascii=False,indent=2)+'\n')
plan=json.loads((ROOT/'data/research-plan.json').read_text()); plan['objective']+=' Анализ результатов ведущих детских STEM-лиг за 2017–2026 и 2022–2026; устойчивые школьные лидеры, кампусы, клубы и уровень наград.'
plan['requirements'].append(dict(id='school_retrospective',requirement='История 5 / 10 лет и подтверждённые школьные лидеры',status='bounded_pass_completed_worldwide_partial',evidence='v21: FRC 44 Championship Winner + 11 main judged awards; WRO 28 selected first places; VEX / FLL / AI cases; 21 school dossiers; interactive windows and source exports',remaining='FTC, RoboCupJunior, all-age VEX, early WRO / FLL and current school affiliation / admission'))
(ROOT/'data/research-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(schools=len(d['schools']),history_entities=len(entities),results=len(results),frc_winners=44,wro_winners=len(wro))))
