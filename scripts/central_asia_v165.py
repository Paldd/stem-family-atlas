"""Official season snapshots, year-of-birth categories and regional entry gates."""
from copy import deepcopy
from pathlib import Path
import json
from nearby_regional_v160 import event as _event, programme

CHECKED='2026-11-05';SPANISH={}
def T(a,b):SPANISH[a]=b;return a
ROOT=Path(__file__).resolve().parents[1]
FIRST='https://firstrobotics.kz/'
RULES='https://docs.google.com/document/d/1UYpkDZL86SZpFMcgtpUmEJi4qnT7Oj-1BdGGisJD9ws/edit'
SHEET='https://docs.google.com/spreadsheets/d/1QJbpsCGQfsV_idUxsbKhKHm1SgQgFZAqQCVM67HY6VY/edit'
RGT='https://rgt.robotek.kz/'
MARC='https://www.marc-association.org/post/marc-2027-international-final-coming-to-taiwan'
PDF_IDS={'rgt':'1yMRdrTBuEpfDksU-C0ViP6vfu3SuInWQ','lom':'1D-yhgab1kvzpFs0MTa2pSqrN-BLjKCee','lom-season':'1FKDiyNJScbgF7EmEUxPZjTT5f8VU1LpD','lom-awards':'1goY8Ask7w7GpXaRMdUqJTrPjxVcYVVGH','rising':'16hLampOpxPmeO-bzCKjPGn8gcfiA6wHh','rising-entry':'1cwAf_q4wMxlPcSoK05KyzztvheN-yK-D','task':'124BV9Ayo34ZDyhlywWc6-j8Caj-EJhyg'}
def pdf(k):return 'https://drive.google.com/file/d/'+PDF_IDS[k]+'/view'
def ref(title,url):return dict(label=title,url=url)
LANG=T('Есть официальные материалы на русском / английском; язык судейства, интервью и поддержка выбранной команды требуют подтверждения. Язык документа не означает язык всех занятий.',
 'Existen materiales oficiales en ruso / inglés; confirmar idioma de arbitraje, entrevista y apoyo al equipo elegido. Idioma del documento no equivale al de todas las clases.')
GATE=T('Годы рождения 2017 / 2020 известны; точные дни рождения и классы не установлены. Проверить командный допуск, язык, места и полный счёт. Заявки, согласия, сообщения и оплаты не выполнялись.',
 'Años de nacimiento 2017 / 2020 conocidos; fechas exactas y cursos sin establecer. Verificar admisión del equipo, idioma, plazas y factura completa. Sin solicitudes, consentimientos, mensajes ni pagos.')
PRICE=T('Тариф участия, robot kit, наставник, дорога и жильё отдельно не подтверждены; неизвестная сумма не ноль.',
 'Tarifa de participación, robot kit, mentor, viaje y alojamiento sin confirmar por separado; importe desconocido no es cero.')
LOCAL=T('Регламент оператора: в 2026 Explore / Challenge получают квоту только в своём регионе. Для январского Qualifier опубликован перечень допустимых регионов; иностранная семейная команда не считается местной по паспорту или туристической поездке. Для Кыргызстана / Узбекистана местный допуск и применение возрастных правил отдельно подтвердить.',
 'Reglamento del operador: en 2026 Explore / Challenge obtienen cupo solo en su región. Qualifier de enero tiene lista de regiones admitidas; pasaporte o viaje turístico no convierte equipo familiar extranjero en local. Confirmar por separado admisión y aplicación de edades en Kirguistán / Uzbekistán.')
FIRST_ENTRY=T('Регистрация через uSTEM Connect и местный Team Number, форму заполняет взрослый наставник. Наличие ссылки не подтверждает открытую запись именно выбранного турнира, места или принятие семьи. Regional / Qualifier / Championship — разные этапы; квота не автоматическая.',
 'Registro mediante uSTEM Connect y Team Number local, formulario a cargo de mentor adulto. Enlace no acredita inscripción abierta del torneo elegido, plazas ni admisión familiar. Regional / Qualifier / Championship son etapas distintas; cupo no automático.')
FIRST_AGE=T('Локальный регламент требует соблюдения возраста на основном сезоне и до 01.05.2027 включительно; off-season проверяется на дату своего события. Это не правило только по году рождения.',
 'Reglamento local exige cumplir edad durante temporada principal y hasta 01.05.2027 inclusive; off-season se verifica en fecha de su evento. No es regla solo por año de nacimiento.')
P2=T('P2 — подтверждённый маршрут; допуск команды уточнить','P2 — ruta acreditada; confirmar admisión de equipo')
P3=T('P3 — региональные условия / будущий ориентир','P3 — condiciones regionales / referencia futura')
P4=T('P4 — старшая категория / связанная запись','P4 — categoría superior / registro vinculado')
CITY_RU={'Semey':'Семей','Oskemen':'Усть-Каменогорск','Pavlodar':'Павлодар','Burabay':'Бурабай','Petropavl':'Петропавловск','Kostanay':'Костанай','Astana':'Астана','Karaganda':'Караганда','Zhezkazgan':'Жезказган','Almaty':'Алматы','Qonaev':'Конаев','Bishkek':'Бишкек','Taldykorgan':'Талдыкорган','Taraz':'Тараз','Aktau':'Актау','Shymkent':'Шымкент','Turkistan':'Туркестан','Atyrau':'Атырау','Oral':'Уральск','Kyzylorda':'Кызылорда','Aktobe':'Актобе','Tashkent':'Ташкент','Zhylandy':'Жыланды'}

def ev(d,ident,title,iso,source,start='',end='',**fields):
 c=next(c for c in d['countries'] if c['iso']==iso)
 e=_event(ident,title,c['country'],source,start,end or start)
 e.update(region=c['region'],iso=[iso],language=LANG,language_certainty=LANG,entry=GATE,cost=PRICE,
  action=GATE,note=GATE,checked=CHECKED,priority=P3,proof=T('Прочитан официальный источник текущего прохода; ограничения сохранены явно.',
  'Fuente oficial leída en esta revisión; límites conservados expresamente.'),date_scope='festival_window',support_languages=[],evidence_level='program')
 e.update(fields);return e

def first_fields(code):
 common=dict(entry=FIRST_ENTRY+' '+LOCAL,note=FIRST_AGE,language=LANG,language_certainty=LANG,references=[ref('FIRST season 2026–27 rules',RULES),ref('Official season calendar',SHEET)],provider='USTEM Foundation / FIRST Central Asia',league_id='first-central-asia',priority=P3,admission_kind='qualification',themes=['robotics','coding','technology'])
 if code=='FLL-E':common.update(age='Explore 6–10',team_min=2,team_max=4,format=T('2–4 ребёнка, один или два тренера 18+; два брата удовлетворяют числу участников.',
  '2–4 niños, uno o dos mentores 18+; dos hermanos cumplen número de participantes.'),mat=T('Условно — 6–10 подходит; регион, этап и допуск команды подтвердить.',
  'Condicional — 6–10 compatible; confirmar región, etapa y admisión de equipo.'),osc=T('Условно — 6–10 подходит; нужна самостоятельная роль и допуск команды.',
  'Condicional — 6–10 compatible; requiere función propia y admisión de equipo.'),gear='LEGO WeDo / SPIKE Essential + Explore set / poster',reward=T('Explore — фестиваль, интервью и командные отметки; это не абсолютный матчевый титул. Квота на следующий этап требует отдельного решения.',
  'Explore es festival, entrevista y reconocimientos de equipo; no título absoluto de partidos. Cupo a etapa siguiente requiere decisión separada.'))
 elif code=='FLL-D':common.update(age='Discover 4–6',team_min=2,team_max=4,format=T('2–4 ребёнка, до двух тренеров 18+.','2–4 niños, hasta dos mentores 18+.'),mat=T('Нет — старше Discover 4–6.','No — mayor que Discover 4–6.'),osc=T('Условно — сейчас 6; сохранение возраста до 01.05.2027 зависит от точного дня рождения.',
  'Condicional — ahora 6; mantener edad hasta 01.05.2027 depende de fecha exacta.'),gear='LEGO DUPLO / Discover set',reward=T('Младший фестиваль и признание вклада; не международное призовое место по одному факту участия.',
  'Festival infantil y reconocimiento de contribución; participar por sí solo no equivale a puesto internacional.'))
 elif code=='FLL-C':common.update(age='Challenge 10–16',team_min=2,team_max=8,format=T('2–8 участников, до двух тренеров 18+.','2–8 participantes, hasta dos mentores 18+.'),mat=T('Условно — сейчас 9; в 2027 исполнится 10, но нужны точная дата, основной cutoff и право входа в сезон.',
  'Condicional — ahora 9; en 2027 cumple 10, pero requiere fecha exacta, cutoff principal y acceso a temporada.'),osc=T('Нет — младше местного минимума 10.','No — menor del mínimo local 10.'),gear='LEGO SPIKE Prime / permitted legacy system + BIOGLOW field',reward=T('Отдельные Robot Performance, Innovation Project и judged awards; квалификация и Houston не обещаны.',
  'Robot Performance, Innovation Project y judged awards separados; clasificación y Houston no prometidos.'))
 else:common.update(age='FTC 12–18',team_min=2,team_max=15,format=T('2–15 участников, до двух тренеров 18+.','2–15 participantes, hasta dos mentores 18+.'),mat=T('Нет — младше FTC 12.','No — menor que FTC 12.'),osc=T('Нет — младше FTC 12.','No — menor que FTC 12.'),gear='FTC kit / BIOBUZZ 2026–27',priority=P4,reward=T('Старшая инженерная лига; матчевые и judged awards учитываются отдельно.',
  'Liga de ingeniería de mayores; premios de partidos y judged awards separados.'))
 return common

def enrich_v165(d):
 n=json.loads((ROOT/'data/central-asia-native-v165.json').read_text());new=[];byid={e['id']:e for e in d['events']}
 for r in n['first_fixture_rows']:
  fields=first_fields(r['programme']);stage=r['stage']
  stage_label={'regional':T('Региональный этап FIRST','Etapa regional FIRST'),'qualifier':T('Зональный Qualifier FIRST','Qualifier zonal FIRST'),'championship':T('Национальный / Центральная Азия · не мировой финал','Nacional / Asia Central · no final mundial'),'off_season':T('Off-season · практика вне основного отбора','Off-season · práctica fuera de selección principal')}[stage]
  fields.update(city=T(CITY_RU.get(r['city'],r['city']),r['city']),period=r['date_label'],scope='international' if stage=='championship' else 'regional',level=stage_label,fixture_id=r['fixture_id'],registration_status=FIRST_ENTRY)
  if r['programme']=='FLL-C' and r['start'].startswith('2026'):
   fields.update(mat=T('Нет — в 2026 родившемуся в 2017 только 9, а местный Challenge начинается с 10.',
    'No — en 2026 quien nació en 2017 tiene solo 9, y Challenge local empieza en 10.'),priority=P4)
  if r.get('territory'):fields['entry']+=' '+r['territory']
  if r.get('venue'):fields['city']+=' · '+r['venue']
  if stage=='off_season':fields['entry']+=T(' Off-season — практика; национальная квота из такого старта не установлена.',
   ' Off-season es práctica; sin acreditar cupo nacional desde este evento.')
  e=ev(d,r['id'],r['name']+' · '+r['programme'],r['iso'],FIRST,r['start'],r['end'],**fields)
  # The archived fixture snapshot supplies defaults for newer verified records.
  current=byid.get(r['id'])
  if current and current.get('checked','')>CHECKED:
   e.update(current)
  if r['id'] in ['C874','C875']:byid[r['id']].update(e)
  else:new.append(e)
 rgt_common=dict(source=RGT,checked=CHECKED,provider='Robotek / MARC',city=T('Астана','Astana'),language=LANG,language_certainty=LANG,cost=PRICE,
  references=[ref('RGT 2027 official regulation',pdf('rgt')),ref('MARC LOM 2027',pdf('lom')),ref('MARC LOM 2027 awards',pdf('lom-awards'))],priority=P2,scope='international',participation='team',admission_kind='qualification',evidence_level='program',date_scope='festival_window',date_status='Подтверждено')
 rgt_entry=T('Положение 2027 п.4.2 допускает команды школ, клубов и частных лиц из Казахстана и других стран. Международный RGT — Астана 03–04.03.2027. В Казахстане есть два отбора: государственная лига Дарын до 15.02.2027 и частная Бірлік 30–31.01.2027, заявка до 20.01.2027. Маршрут иностранной команды и место семьи требуют решения оргкомитета; местная лига не становится доступной по гражданству.',
  'Reglamento 2027 art.4.2 admite equipos escolares, clubes y particulares de Kazajistán y otros países. RGT internacional en Astana 03–04.03.2027. Kazajistán tiene dos selecciones: liga pública Daryn hasta 15.02.2027 y privada Birlik 30–31.01.2027, solicitud hasta 20.01.2027. Vía extranjera y plaza familiar requieren decisión del comité; ciudadanía no habilita liga local.')
 taiwan=T('Отбор в MARC Taiwan возможен только через LOM / Rising Pioneers / Task Master. Положение не фиксирует число лицензий и Wild Card: нужны итоговый протокол, соответствие правилам партнёра и подтверждение участия. Проезд, проживание, визовые процедуры и взносы оплачиваются отдельно. Это не автоматическая путёвка и не оплата поездки.',
  'Selección a MARC Taiwan posible solo mediante LOM / Rising Pioneers / Task Master. Reglamento no fija número de licencias ni Wild Card: exige acta final, requisitos del socio y confirmación. Viaje, alojamiento, trámites migratorios y cuotas aparte. No es acceso automático ni viaje financiado.')
 lom_award=T('В LOM Elementary Gold / Silver / Bronze — поощрительные сертификаты всем завершившим квалификацию: верхняя треть / средняя треть / остальные. Отдельно считаются место альянса, special award и Wild Card. Club Division не даёт формального рейтинга, special awards или прохода дальше; в RGT Club отдельно не объявлен.',
  'En LOM Elementary Gold / Silver / Bronze son certificados de estímulo para quienes terminan clasificación: tercio superior / tercio medio / resto. Puesto de alianza, special award y Wild Card se cuentan aparte. Club Division no otorga ranking formal, special awards ni avance; Club no anunciado por separado en RGT.')
 e=byid['C869'];e.update(rgt_common);e.update(title='Robotek Grand Tournament 2027 · LOM Elementary',age='2016–2021',mat=T('Да по году рождения 2017; команда и иностранный вход требуют подтверждения.',
  'Sí por nacimiento 2017; confirmar equipo y admisión extranjera.'),osc=T('Да по году рождения 2020; команда и иностранный вход требуют подтверждения.',
  'Sí por nacimiento 2020; confirmar equipo y admisión extranjera.'),team_min=2,team_max=3,format=T('2–3 ребёнка + один тренер 18+; оба брата подходят по годам и минимальному составу.',
  '2–3 niños + un mentor 18+; ambos hermanos cumplen años y composición mínima.'),entry=rgt_entry,gear=T('LOM: MATRIX Mini V2.0+ или R4 V1.0, MATRIX MJ2 / MJ5, максимум два MATRIX TT drive motors; старт 32 × 32 cm и до 1200 g для Elementary. Структурные детали Elementary могут быть не MATRIX по глобальным правилам; локальное применение подтвердить. Нужны свои robot kit, ноутбук и питание.',
  'LOM: MATRIX Mini V2.0+ o R4 V1.0, MATRIX MJ2 / MJ5, máximo dos MATRIX TT drive motors; inicio 32 × 32 cm y hasta 1200 g en Elementary. Reglas globales permiten piezas estructurales no MATRIX en Elementary; confirmar aplicación local. Robot kit, portátil y alimentación propios.'),reward=lom_award,note=taiwan+' '+lom_award,proof=T('Прочитаны положение RGT 2027 и актуальные PDF MARC. Правила отбора 2026 не перенесены; свежий 2027 действительно содержит две казахстанские лиги.',
  'Leídos reglamento RGT 2027 y PDF MARC actuales. Sin trasladar selección 2026; documento nuevo 2027 sí contiene dos ligas kazajas.'),action=GATE)
 for r in n['rgt_rows']:
  e=ev(d,r['id'],r['title'],'KAZ',RGT,r['start'],r['end'],**{k:v for k,v in rgt_common.items() if k!='source'});e.update(r);e['entry']=rgt_entry+' '+r.get('entry_extra','');e['note']=taiwan+' '+r.get('note','')
  if not e['start']:e.update(date_status='Не объявлено',city=T('Казахстан · областные центры','Kazajistán · centros regionales'),scope='regional')
  new.append(e)
 alias=byid['C870'];alias.update(title=T('Маршрут RGT → MARC Taiwan · актуальный финал C1189','Ruta RGT → MARC Taiwan · final vigente C1189'),start='',end='',deadline='',period=T('Старые 29–30.05.2027 заменены; актуальный MARC Final 20–23.05.2027 в C1189.',
  'Fechas antiguas 29–30.05.2027 sustituidas; MARC Final vigente 20–23.05.2027 en C1189.'),date_status='Не объявлено',canonical_event_id='C1189',superseded_by='C1189',priority=P4,checked=CHECKED,source=MARC,entry=taiwan,note=taiwan,proof=T('Текущая страница RGT и собственный анонс MARC согласуются по 20–23 мая. ID C870 сохранён как связанный маршрут без второго календарного события.',
  'Página RGT actual y anuncio propio MARC coinciden en 20–23 de mayo. ID C870 conservado como ruta vinculada sin segundo evento de calendario.'),related_ids=['C869','C1189'])
 final=byid['C1189'];final.update(checked=CHECKED,age=T('Опубликованы общие правила MARC 2027: LOM Elementary 2016–2021; TM / Rising Pioneers Elementary 2015–2019. Окончательный набор категорий и квоты самого Taipei Final требуют event handbook.',
  'Publicadas reglas generales MARC 2027: LOM Elementary 2016–2021; TM / Rising Pioneers Elementary 2015–2019. Categorías finales y cupos del Taipei Final requieren event handbook.'))
 for title,key in [('MARC LOM 2027','lom'),('MARC Rising Pioneers 2027','rising'),('MARC Task Master 2027','task')]:
  if not any(x['url']==pdf(key) for x in final.get('references',[])):final.setdefault('references',[]).append(ref(title,pdf(key)))
 if taiwan not in final['note']:final['note']+=' '+taiwan
 for r in n['other_rows']:
  fields={k:v for k,v in r.items() if k not in ['id','title','iso','source','start','end']}
  if r.get('participation')=='individual':fields['format']=T('Индивидуальное участие; школьный / местный допуск отдельно.','Participación individual; admisión escolar / local aparte.')
  if r['iso']=='GEO':fields['city']=T('Тбилиси','Tbilisi')
  if r['iso']=='ARM':fields['city']=T('Армения · участвующая школа','Armenia · escuela participante')
  if r['iso']=='UZB':fields['city']=T('Ташкент','Tashkent')
  if r.get('team_min')==1:fields['format']=T('1–3 участника, индивидуально или командой; один наставник.','1–3 participantes, individual o equipo; un mentor.')
  if r.get('team_max')==5:fields['format']=T('2–5 участников; текущая карточка 16+, оба ребёнка младше.','2–5 participantes; ficha actual 16+, ambos niños menores.')
  new.append(ev(d,r['id'],r['title'],r['iso'],r['source'],r.get('start',''),r.get('end',''),**fields))
 for e in new:
  old=byid.get(e['id'])
  if old:old.update(e)
  else:d['events'].append(e);byid[e['id']]=e
 profile=programme('first-central-asia','FIRST Central Asia · Kazakhstan / Kyrgyzstan / Uzbekistan','regional','Discover 4–6; Explore 6–10; Challenge 10–16; FTC 12–18',['6','9','10-12','teen'],[r['id'] for r in n['first_fixture_rows']],summary=T('Официальная сетка сезона 2026–27; домашний регион, этап и возраст до 01.05.2027 имеют значение.',
  'Calendario oficial 2026–27; importan región de origen, etapa y edad hasta 01.05.2027.'),route=FIRST_ENTRY+' '+LOCAL,language=LANG,hardware='LEGO DUPLO / WeDo / SPIKE / FTC · separate categories',requirements=[FIRST_AGE,FIRST_ENTRY,LOCAL],nuances=[T('В Explore 2–4 участника, в Challenge 2–8; два брата подходят численно только для Explore. Challenge здесь с 10, не с глобальных 9. Future Edition K–2 — 5–7 и неизвестный минимум команды; 3–8 — 8–16, 4–8 участников и реальные Grades 3–8. Программа Future Edition не объявлена во всех турнирах сетки.',
  'Explore tiene 2–4 participantes, Challenge 2–8; dos hermanos cumplen número solo en Explore. Challenge aquí desde 10, no desde 9 globales. Future Edition K–2 es 5–7 con mínimo de equipo desconocido; 3–8 es 8–16, 4–8 participantes y Grades 3–8 reales. Future Edition no anunciada en todos los torneos del calendario.')],cost=PRICE,award=T('Фестивальное признание, призовое место, national quota и Houston различаются; числа мировых квот на 2027 ещё ожидаются.',
  'Reconocimiento de festival, puesto, national quota y Houston son distintos; números de cupos mundiales 2027 aún pendientes.'),sources=[dict(title='Current season operator',url=FIRST,checked=CHECKED),dict(title='Official calendar snapshot',url=SHEET,checked=CHECKED),dict(title='Local season rulebook',url=RULES,checked=CHECKED)],evidence=T('Календарь и программные данные проверены по публичным данным оператора, правила — по полному документу.',
  'Calendario y programas verificados en datos públicos del operador; reglas en documento completo.'))
 profile['categories']=[dict(name=byid[r['id']]['title'],age=byid[r['id']]['age'],team=byid[r['id']]['format'],hardware=byid[r['id']]['gear'],entry=byid[r['id']]['entry'],event_id=r['id']) for r in n['first_fixture_rows'] if r['stage']=='championship' and r['city']=='Astana']
 old=next((p for p in d['league_guide']['profiles'] if p['id']==profile['id']),None)
 if old:old.update(profile)
 else:d['league_guide']['profiles'].append(profile)
 p=next(p for p in d['league_guide']['profiles'] if p['id']=='robotek-rgt');p.update(age_summary='LOM 2016–2021; Robotek 2014–2018; RP / TM 2015–2019',summary=T('RGT 2027: возрастные правила опубликованы, иностранные команды разрешены; местный отбор и международный финал различаются.',
  'RGT 2027: reglas de edad publicadas, equipos extranjeros admitidos; selección local y final internacional son distintos.'),route=rgt_entry,requirements=[GATE],nuances=[taiwan,lom_award],hardware=byid['C869']['gear'],award=lom_award,sources=[dict(title='RGT 2027 official regulation',url=pdf('rgt'),checked=CHECKED),dict(title='RGT current season',url=RGT,checked=CHECKED)],evidence=byid['C869']['proof'])
 p['categories']=[dict(name=byid[k]['title'],age=byid[k]['age'],team=byid[k]['format'],hardware=byid[k]['gear'],entry=byid[k]['entry'],event_id=k) for k in ['C869']+n['rgt_category_ids']]
 p['event_ids']=list(dict.fromkeys(['C869','C1189']+[r['id'] for r in n['rgt_rows']]))
 p=next(p for p in d['league_guide']['profiles'] if p['id']=='marc');p['nuances']=list(dict.fromkeys(p['nuances']+[lom_award,taiwan]));p['categories']=[dict(c,age=byid['C1189']['age']) if c.get('event_id')=='C1189' else c for c in p['categories']]
 rp=byid[n['other_rows'][-1]['id']]
 p['age_summary']=T('LOM Elementary: 2016–2021, 2–3; Task Master: 2015–2019, 2–3; Rising Pioneers: 2015–2019, 1–3.',
  'LOM Elementary: 2016–2021, 2–3; Task Master: 2015–2019, 2–3; Rising Pioneers: 2015–2019, 1–3.')
 p['hardware']=byid['C869']['gear']+' '+rp['gear']
 p['route']=T('Октябрьская запись ERA Taiwan уже закрыта. Международный финал Taipei 20–23.05.2027 — отдельный этап с подтверждением квоты. Для глобального Rising Pioneers 2027 опубликованы правила, но URL подачи и квартальные даты ещё требуют объявления.',
  'Registro de octubre ERA Taiwan ya cerrado. Final internacional Taipei 20–23.05.2027 es etapa separada con confirmación de cupo. Rising Pioneers global 2027 tiene reglas publicadas, pero URL de entrega y fechas trimestrales aún requieren anuncio.')
 p['event_ids']=list(dict.fromkeys(p['event_ids']+[rp['id']]))
 if not any(c.get('event_id')==rp['id'] for c in p['categories']):p['categories'].append(dict(name=rp['title'],age=rp['age'],team=rp['format'],hardware=rp['gear'],entry=rp['entry'],event_id=rp['id']))
 for url in [pdf('lom'),pdf('rising'),pdf('task')]:
  if not any(s['url']==url for s in p['sources']):p['sources'].append(dict(title='MARC 2027 category rules',url=url,checked=CHECKED))
 focus=d['kazakhstan_focus'];focus.update(version=165,checked=CHECKED,conclusion=T('Для обоих вместе: RGT LOM по годам рождения 2016–2021 и составу 2–3. Explore FIRST 6–10 / 2–4 тоже подходит по возрасту и числу, но региональная привязка и квота требуют проверки. Robotek и Rising Pioneers доступны Матвею по году рождения; Task Master требует второго подходящего партнёра. В Казахстане не подтверждена постоянная школьная база семьи.',
  'Para ambos juntos: RGT LOM por nacimiento 2016–2021 y equipo 2–3. FIRST Explore 6–10 / 2–4 también compatible por edad y número, pero confirmar región y cupo. Robotek y Rising Pioneers compatibles con nacimiento de Matvey; Task Master exige segundo compañero elegible. Sin acreditar base escolar familiar permanente en Kazajistán.'),announced=[dict(id='C869',date='03–04.03.2027',city=T('Астана','Astana'),label='RGT · LOM 2016–2021'),dict(id='C1189',date='20–23.05.2027',city=T('Тайбэй','Taipéi'),label=T('MARC · лицензия по правилам','MARC · licencia según reglas'))],gates=[FIRST_AGE,LOCAL,FIRST_ENTRY,taiwan,lom_award,LANG],limitations=T('Полностью извлечены только выбранные вкладки официальной сетки. Скримиджи, школьные и все областные события, лагеря и школы не объявлены полностью проаудированными. Ничего не зарегистрировано.',
  'Extraídas completas solo pestañas elegidas del calendario oficial. Scrimmages, eventos escolares y regionales, campamentos y escuelas sin declarar auditoría completa. Sin registrar nada.'))
 for c in focus['children']:
  c['detail']=T('Матвей 2017: совместная LOM с Оскаром либо отдельные Robotek / Rising Pioneers; Task Master требует второго подходящего ребёнка. Нельзя одновременно выступать в нескольких RGT категориях. Explore FIRST подходит по возрасту; местный Challenge с 10 — проверка дня рождения и допуска в 2027, в 2026 возраст не подходит.',
   'Matvey 2017: LOM con Oscar o Robotek / Rising Pioneers separados; Task Master exige segundo niño elegible. No se puede competir simultáneamente en varias categorías RGT. FIRST Explore compatible por edad; Challenge local desde 10 requiere comprobar cumpleaños y acceso 2027, edad insuficiente en 2026.') if c['id']=='mat' else T('Оскар 2020: LOM Elementary 2016–2021 вместе с Матвеем и Explore FIRST 6–10. Для Task Master / Rising Pioneers 2015–2019 он пока не подходит. Discover 4–6 требует сохранения возраста до 01.05.2027; точный день неизвестен. WRO Elementary 8+ остаётся будущим направлением.',
   'Oscar 2020: LOM Elementary 2016–2021 con Matvey y FIRST Explore 6–10. Aún no elegible para Task Master / Rising Pioneers 2015–2019. Discover 4–6 exige mantener edad hasta 01.05.2027; día exacto desconocido. WRO Elementary 8+ sigue como vía futura.')
  c['event_ids']=list(dict.fromkeys(['C869','C874']+(n['rgt_category_ids']+['C875'] if c['id']=='mat' else [])+c['event_ids']))
 focus['event_ids']=list(dict.fromkeys(focus['event_ids']+[e['id'] for e in new if 'KAZ' in e.get('iso',[])]+['C1189']))
 focus['sources']+= [dict(title='Current FIRST season',url=FIRST,checked=CHECKED),dict(title='Current RGT regulation',url=pdf('rgt'),checked=CHECKED)] if not any(s['url']==pdf('rgt') for s in focus['sources']) else []
 known={s['url'] for s in d['sources']}
 for e in [byid[k] for k in ['C869','C870','C874','C875','C1189']]+new:
  for source in [dict(url=e['source'],title=e['title'])]+[dict(url=x['url'],title=x['label']) for x in e.get('references',[])]:
   if source['url'] not in known:d['sources'].append(dict(**source,checked=CHECKED,evidence=e['proof']));known.add(source['url'])
 d['central_asia_v165']=dict(version=165,checked=CHECKED,fixture_rows=len(n['first_fixture_rows']),new_catalogue_rows=len(new),status='partial',worldwide_complete=False)
 d['league_guide'].update(version=165,checked=CHECKED)
