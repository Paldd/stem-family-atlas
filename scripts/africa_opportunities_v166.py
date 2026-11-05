"""Primary African opportunities, current holiday sessions and explicit rule conflicts."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
from camp_east_asia_v159 import base, add, age_fit, candidate
from nearby_regional_v160 import event, programme

ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-11-05';SPANISH={}
def T(a,b):SPANISH[a]=b;return a
NAM='https://www.robotschoolnamibia.com/'
X='https://xtreamrobotics.com/'
PI='https://projektinspire.co.tz/programmes/'
TTC='https://ttc.or.tz/events/singapore/'
RGSC='https://rgsc.govmu.org/rgsc/?page_id=648171'
ROBO='https://www.swsu-online.ru/robo_africa/'
JETS='https://www.dnsc.gov.zm/jets26/index.php?year=2026'
ITU='https://aiforgood.itu.int/event/robotics-for-good-youth-challenge-zambia-2/'
IRC='https://international-robotchallenge.org/competition/robo-boom'
CYBER='https://www.cyberskills.mu/courses/the-coding-wizards/'
CHILD='https://mdpa.govmu.org/mdpa/index.php/children-innovative-learning-design-child-programme/'
LANG=T('Язык именно занятий EN / ES / RU не подтверждён. Английская страница не означает английское преподавание; помощь выбранной группе проверить.',
 'Idioma de estas clases EN / ES / RU sin confirmar. Página inglesa no equivale a enseñanza inglesa; comprobar apoyo al grupo elegido.')
GATE=T('Подтвердить индивидуальный иностранный доступ, язык ведущего, подходящий уровень, место и полный счёт. Возрастная возможность не зачисление. Формы, согласия, заявки, сообщения и оплаты не выполнялись.',
 'Confirmar acceso extranjero individual, idioma docente, nivel adecuado, plaza y factura completa. Compatibilidad de edad no es admisión. Sin formularios, consentimientos, solicitudes, mensajes ni pagos.')
TRIP=T('Перелёты, жильё и сопровождение родителей, питание, трансферы, страховка, техника и условия отмены требуют окончательного счёта; неизвестные расходы не ноль.',
 'Vuelos, alojamiento y acompañamiento parental, comida, traslados, seguro, equipo y cancelación requieren factura final; gastos desconocidos no son cero.')
UNKNOWN=T('Стоимость, валюта, включения и сроки выбранного потока не опубликованы в прочитанном источнике; запросить полный счёт.',
 'Precio, moneda, inclusiones y fechas del grupo elegido no publicados en fuente leída; solicitar factura completa.')
EDU=T('Обучение / собственный проект; сертификат и внутренний конкурс не международная победа.',
 'Aprendizaje / proyecto propio; certificado y concurso interno no equivalen a victoria internacional.')
CLOSED=T('Регистрация закрыта по текущей странице, даже если дата ещё впереди. Это архив / наблюдение за будущим набором, не открытое предложение семье.',
 'Inscripción cerrada según página actual aunque fecha sea futura. Archivo / seguimiento de próxima convocatoria, no oferta abierta familiar.')
X_CANCEL=T('Оплата подтверждает заказ; учебные программы обычно без возврата. Перенос на другой доступный курс или продукт возможен только по решению оператора. Для регулярного прекращения нужен письменный срок 30 дней; пропуски обычно не переносятся. Условия не принимались.',
 'Pago confirma pedido; programas educativos generalmente sin devolución. Traslado a otro curso o producto disponible solo con decisión del operador. Baja recurrente exige aviso escrito de 30 días; ausencias normalmente sin reposición. Condiciones sin aceptar.')
NAM_FEE=T('2026: NAD 450 за ребёнка / выбранное утро; member 225. Non-member Book 6 get 3 free: 9 выбранных утр за 2700 на одного, при применимости предложения. Два брата в разных возрастных группах: 900 за общее утро или 5400 за 9 утр каждому. Совмещение льгот и счёт подтвердить. В 2027 опубликован тариф 481.50 / 240.75, но смены 2027 здесь не объявлены.',
 '2026: NAD 450 por niño / mañana elegida; member 225. Non-member Book 6 get 3 free: 9 mañanas elegidas por 2700 para uno, si aplica oferta. Dos hermanos en grupos de edad distintos: 900 por mañana compartida o 5400 por 9 mañanas cada uno. Confirmar combinación de ventajas y factura. En 2027 publicada tarifa 481.50 / 240.75, pero sesiones 2027 no anunciadas aquí.')
NAM_TIMING=T('Текущая система показывает 14 отдельных утр 23 ноября – 11 декабря 2026, 09:00–12:00; 10 декабря в списке нет. Старые август–сентябрь из поискового описания не перенесены. Места — изменяемый снимок, не бронь.',
 'Sistema actual muestra 14 mañanas independientes 23 de noviembre – 11 de diciembre 2026, 09:00–12:00; 10 de diciembre no figura. Sin trasladar agosto–septiembre antiguos del resumen de búsqueda. Plazas son instantánea variable, no reserva.')
NAM_CONTRACT=T('Членство 2027 на 12 календарных месяцев с автоматическим продлением; письменное уведомление не менее 30 дней до продления. Registration NAD 160.50 за ребёнка, VAT включён, без возврата. Месячная цена не разовая цена каникул; пропуски не возвращаются. Условия лагеря и membership различаются, согласие не давалось.',
 'Membresía 2027 por 12 meses naturales con renovación automática; aviso escrito al menos 30 días antes de renovar. Registration NAD 160.50 por niño, VAT incluido, sin devolución. Precio mensual no es tarifa vacacional única; ausencias sin devolución. Condiciones de campamento y membresía distintas, sin consentimiento.')
PI_AGE=T('4–6 и 7–14, отдельные возрастные группы; оба ребёнка подходят по возрасту, но язык, уровень и иностранный приём не подтверждены.',
 '4–6 y 7–14, grupos de edad separados; ambos niños compatibles por edad, pero idioma, nivel y admisión extranjera sin confirmar.')
IRC_GATE=T('На сайте 3–5 участников; у RoboParade PDF допускает 1–3. PDF задают школьный класс или иной возраст, чем карточки сайта. Это опубликованные ссылки на старые редакции, не новый handbook Egypt 2027. Разрешить расхождения письменно до выбора состава / kit; два брата не объявлены автоматически допущенной командой.',
 'Web indica 3–5 participantes; PDF RoboParade admite 1–3. PDF fijan curso escolar u otra edad frente a fichas web. Enlaces publicados a ediciones anteriores, no handbook nuevo Egypt 2027. Resolver discrepancias por escrito antes de elegir equipo / kit; dos hermanos no declarados equipo automáticamente admitido.')
IRC_DATE=T('Egypt 2027 объявлен. Countdown 2027-03-26T24:00:00 не заменяет подтверждённые дни и venue; точные даты, дедлайн и взносы не установлены.',
 'Egypt 2027 anunciado. Countdown 2027-03-26T24:00:00 no sustituye días y venue confirmados; fechas exactas, plazo y cuotas sin establecer.')
GRADE=T('Условно — реальный школьный класс и применимость старого PDF к 2027 неизвестны; возраст его не заменяет.',
 'Condicional — curso escolar real y aplicación de PDF antiguo a 2027 desconocidos; edad no sustituye curso.')
SCHOOL_GRADE=T('Условно — фактический школьный класс, местная школа и иностранный доступ не установлены. Возраст не заменяет школьный уровень.',
 'Condicional — curso escolar real, escuela local y acceso extranjero sin establecer. Edad no sustituye nivel escolar.')

def facts():return json.loads((ROOT/'data/africa-native-v166.json').read_text())
def src(label,url):return dict(title=label,url=url,checked=CHECKED)
def refs(p,*items):p['sources']=[src(a,b) for a,b in items]
def B(i,slug,name,iso,place,themes,age,lo=None,hi=None):
 countries={'NAM':'Намибия','BWA':'Ботсвана','ZAF':'ЮАР','TZA':'Танзания','SGP':'Сингапур','MUS':'Маврикий'}
 p=base('CP'+str(i),slug,name,iso,countries[iso],place,themes)
 p.update(age=age,language=LANG,questions=[GATE],shortlist=[])
 p['timing'].update(status='next_unannounced',label=UNKNOWN)
 p['price'].update(label=UNKNOWN,extras=TRIP,deposit=UNKNOWN)
 if lo is not None:p['family_fit']=age_fit(lo,hi,'2026-11-05')
 return p

def make_profiles():
 out=[];n=facts()
 for i,key,lo,hi in [(1292,'JUNIOR',4,8),(1293,'SENIOR',9,14)]:
  p=B(i,'robotschool-namibia-holiday-'+key.lower(),'Robotschool Namibia · Holiday '+key,'NAM','16 Seder Street · Suiderhof · Windhoek',['robotics','coding','engineering'],str(lo)+'–'+str(hi),lo,hi)
  p['programme']=T('Практические утренние занятия робототехникой: сборка, код, тестирование и улучшение проекта. Junior 4–8 для Оскара и Senior 9–14 для Матвея идут в одинаковые часы; дети не в одной возрастной группе. У каждой группы максимум 8 детей.',
   'Clases prácticas matinales de robótica: construir, programar, probar y mejorar proyecto. Junior 4–8 para Oscar y Senior 9–14 para Matvey tienen mismo horario; niños en grupos de edad distintos. Cada grupo tiene máximo 8 niños.')
  p['timing'].update(status='published_2026_27',label=NAM_TIMING)
  p['price'].update(year=2026,currency='NAD',amount=450,unit='child_session',label=NAM_FEE,included=T('Одно выбранное утро 09:00–12:00; состав материалов, ноутбук, питание и возврат именно лагеря подтвердить.',
   'Una mañana elegida 09:00–12:00; confirmar materiales, portátil, comida y devolución específica del campamento.'))
  days=[x['date'] for x in n['namibia_sessions'] if x['group']==key]
  add(p,days[0],days[-1],key.lower(),'Holiday '+key,NAM_FEE,NAM+'holiday-camp',days=days,begin='09:00',finish='12:00',zone='Africa/Windhoek',admission_kind='open_application')
  refs(p,('Current Holiday Camp',NAM+'holiday-camp'),('Public available dates snapshot',NAM+'api/holiday-camp-availability'));out.append(p)
 for i,key,lo,hi,fee in [(1294,'Junior',6,8,1125),(1295,'Senior',9,11,1230)]:
  p=B(i,'robotschool-namibia-2027-'+key.lower(),'Robotschool Namibia · '+key+' membership 2027','NAM','16 Seder Street · Suiderhof · Windhoek',['robotics','coding'],str(lo)+'–'+str(hi),lo,hi)
  p['programme']=T('Постоянная возрастная программа робототехники. Это членство на учебный год, не смена лагеря; индивидуальное распределение по уровню и расписание подтвердить.',
   'Programa permanente de robótica por edad. Membresía de año educativo, no sesión de campamento; confirmar nivel individual y horario.')
  p['programme_type']='regular';p['timing'].update(status='partial_2027',label=NAM_CONTRACT)
  p['price'].update(year=2027,currency='NAD',amount=fee,unit='child_month',label='NAD '+str(fee)+' / month + 160.50 registration. '+NAM_CONTRACT,deposit=NAM_CONTRACT)
  refs(p,('Current 2027 registration and membership contract',NAM+'register'));out.append(p)
 for i,key,title,iso,place,lo,hi,amount,currency,start,end,begin,finish in [
  (1296,'green','Green Light Robotics & Coding','BWA','Block 8 · Gaborone · Green Light Day Care Centre',4,6,1150,'BWP','2026-11-23','2026-11-27','08:00','13:00'),
  (1297,'steam','Treasure Quest STEAM','BWA','Partial · Gaborone · Treasure Quest Pre School',4,9,550,'BWP','2026-09-07','2026-09-09','09:00','12:00'),
  (1298,'fun','Treasure Quest Robotics Fun','BWA','Partial · Gaborone · Treasure Quest Pre School',4,12,550,'BWP','2026-09-10','2026-09-12','09:00','12:00'),
  (1299,'hillcrest','Hillcrest Robotics & AI','ZAF','Hillcrest Secondary School · Durban',7,13,800,'ZAR','2026-08-14','2026-08-15','08:00','13:00')]:
  pages={'green':'robotics-coding-camp-green-light-day-care-centre/','steam':'steam-camp-treasure-quest-preschool/','fun':'robotics-fun-camp-treasure-quest-preschool/','hillcrest':'robotics-ai-camp-hillcrest-secondary-school/'};url=X+pages[key]
  p=B(i,'xtream-'+key+'-2026','Xtream Robotics · '+title,iso,place,['robotics','coding','engineering']+(['ai'] if key=='hillcrest' else []),str(lo)+'–'+str(hi),lo,hi)
  p['programme']=T('Сборка роботов, игровые задачи программирования, Scratch, электроника и STEM. Внутренние team competitions и Certificate of Participation не мировой титул.',
   'Construcción de robots, retos lúdicos de programación, Scratch, electrónica y STEM. Team competitions internos y Certificate of Participation no son título mundial.')
  p['availability']=dict(status='closed',label=CLOSED);p['timing'].update(status='published_2026' if key=='green' else 'archive_next_unannounced',label=CLOSED+' '+start+'–'+end+' · '+begin+'–'+finish)
  p['price'].update(year=2026,currency=currency,amount=amount,unit='child_camp',label=currency+' '+str(amount)+' / child / camp. '+X_CANCEL,deposit=X_CANCEL)
  add(p,start,end,key,title,p['price']['label'],url,availability=dict(status='closed',label=CLOSED),admission_kind='closed',registration_status=CLOSED)
  refs(p,(title,url),('Current closed camp directory',X+'physical-steam-robotics-camps/'),('Refund policy',X+'refund-policy/'));out.append(p)
 p=B(1300,'xtream-weekend-gaborone','Xtream Robotics · Saturday term classes','BWA','Treasure Quest Pre School · Plot 5438 · Partial · Gaborone',['robotics','coding','ai','engineering'],'4–7 / 8–12',4,12)
 p['programme_type']='regular';p['programme']=T('10 суббот по 2 часа за term, не каникулярный лагерь. Младшая группа 4–7: 09:00–11:00; старшая 8–12: 12:00–14:00. Это разные часы братьев. Robotics, block coding, circuits и основы AI по уровню; даты term не объявлены.',
  '10 sábados de 2 horas por term, no campamento vacacional. Grupo menor 4–7: 09:00–11:00; mayor 8–12: 12:00–14:00. Hermanos en horarios distintos. Robotics, block coding, circuits y fundamentos AI por nivel; fechas del term sin anunciar.')
 p['price'].update(currency='BWP',amount=2500,unit='child_term',label=T('BWP 2500 за ребёнка / term из 10 двухчасовых занятий; для обоих 5000 до неуказанных доплат.',
  'BWP 2500 por niño / term de 10 clases de dos horas; ambos 5000 antes de cargos no indicados.'),deposit=X_CANCEL)
 refs(p,('Weekend classes programme',X+'weekend-robotics-coding-classes/'),('Refund policy',X+'refund-policy/'));out.append(p)
 for i,key,label in [(1301,'holiday-camps','Holiday Camps'),(1302,'saturday-stem-sessions','Saturday STEM'),(1303,'daily-private-sessions','Private STEM')]:
  p=B(i,'projekt-inspire-'+key,'Projekt Inspire · '+label,'TZA','Dar es Salaam · выбранную площадку подтвердить',['science','engineering','coding'], '4–6 / 7–14',4,14)
  p['programme']=PI_AGE+' '+(T('Каникулы NECTA / Cambridge: Пн–Пт до четырёх недель, утро или после обеда по 2½ часа с перерывом 30 минут. Конкретный поток и робототехническую тему выбрать; не весь диапазон каникул означает одну смену.',
   'Vacaciones NECTA / Cambridge: lunes–viernes hasta cuatro semanas, mañana o tarde de 2½ horas con descanso de 30 minutos. Elegir grupo y tema de robótica concreto; todo período vacacional no equivale a una sesión.') if i==1301 else T('Субботняя группа 10:00–13:00, 3 часа с перерывом 30 минут; регулярные занятия, не лагерь.',
   'Grupo de sábado 10:00–13:00, 3 horas con descanso de 30 minutos; clases regulares, no campamento.') if i==1302 else T('Индивидуальные STEM занятия по 2½ часа с перерывом 30 минут; назначаются внутри рабочего окна 08:30–17:00. Не целый день и не лагерь.',
   'Clases STEM individuales de 2½ horas con descanso de 30 minutos; concertadas dentro de horario laboral 08:30–17:00. No jornada completa ni campamento.'))
  p['programme_type']='holiday' if i==1301 else 'regular';refs(p,(label,PI+key));out.append(p)
 p=B(1304,'projekt-inspire-youth-bootcamp','Projekt Inspire · STEM Youth Bootcamp','TZA','Tanzania · площадка следующего выпуска не объявлена',['robotics','coding','engineering','entrepreneurship'],'O-Level / A-Level / college / university')
 p['programme']=T('Ежегодный youth bootcamp: coding, robotics, engineering, digital tools, leadership, проекты и pitch. Принимает O-Level и старше; оба ребёнка ещё младше требуемого школьного уровня. Новые даты coming soon, ночёвки не установлены.',
  'Youth bootcamp anual: coding, robotics, engineering, digital tools, leadership, proyectos y pitch. Admite O-Level y superiores; ambos niños aún menores del nivel escolar requerido. Fechas nuevas coming soon, pernocta sin establecer.')
 p['accommodation']=T('Дневной / жилой формат не подтверждён; обеим детям это будущая школьная ступень.','Formato diurno / residencial sin confirmar; para ambos niños es nivel escolar futuro.')
 p['formats']=['unknown']
 p['family_fit']={c:candidate('not_eligible',p['programme']) for c in ['matvey','oscar']};refs(p,('Youth bootcamp programme',PI+'youth-bootcamps'));out.append(p)
 p=B(1305,'ttc-singapore-exchange-2026','TTC · Tanzania–Singapore STEM Exchange','SGP','Singapore · поездка из Dar es Salaam',['robotics','ai','coding','science'],'8–17',8,17);p['formats']=['boarding']
 p['programme']=T('Организатор из Танзании заявляет STEM поездку в Singapore, robotics / AI / coding, OWIS, Science Centre, NUS и IEEE session. Эти посещения заявлены TTC, отдельно принимающими площадками не подтверждены. Программа адресована Tanzanian students; иностранный семейный вход и сопровождение неизвестны.',
  'Organizador de Tanzania anuncia viaje STEM a Singapore, robotics / AI / coding, OWIS, Science Centre, NUS e IEEE session. Visitas declaradas por TTC, sin confirmación separada de sedes receptoras. Programa dirigido a Tanzanian students; acceso familiar extranjero y acompañamiento desconocidos.')
 p['accommodation']=T('Заявлены shared 4/5-star accommodation, все приёмы пищи и транспорт Singapore; это учебная поездка, не школьный пансион. Правила сопровождения, размещения и страховой договор не прочитаны.',
  'Anunciados shared 4/5-star accommodation, todas comidas y transporte Singapore; viaje educativo, no internado escolar. Reglas de supervisión, alojamiento y contrato de seguro sin leer.')
 p['timing'].update(status='published_2026_27',label=T('7–17 декабря 2026 по странице. Организатор называет 10 Days, но включительно это 11 календарных дат; точный маршрут / число ночей подтвердить. Надпись 6 slots — изменяемый анонс, не гарантия места.',
  '7–17 de diciembre 2026 según página. Organizador dice 10 Days, pero son 11 fechas naturales inclusive; confirmar itinerario / noches exactos. Rótulo 6 slots es anuncio variable, no garantía de plaza.'))
 p['price'].update(currency='',amount=None,unit='child_trip',label=T('На странице $2850 DAR-to-DAR и возможная доплата до $350 за перелёт, то есть до $3200. Код валюты не указан. До Dar es Salaam, расходы родителей, паспортные / въездные процедуры, исключения страховки и отмена отдельно; all-inclusive не полный семейный бюджет.',
  'Página indica $2850 DAR-to-DAR y posible suplemento de hasta $350 por vuelo, es decir hasta $3200. Código de moneda no indicado. Llegada a Dar es Salaam, gastos parentales, trámites de pasaporte / entrada, exclusiones de seguro y cancelación aparte; all-inclusive no es presupuesto familiar completo.'))
 add(p,'2026-12-07','2026-12-17','exchange','STEM Exchange',p['price']['label'],TTC,admission_kind='school')
 refs(p,('TTC programme and package inclusions',TTC));out.append(p)
 p=B(1306,'cyberskills-coding-wizards','Cyberskills · The Coding Wizards','MUS','Zone 5 · Freeport · Mer Rouge · Mauritius',['coding','games'],'8–13',8,13)
 p['programme']=T('Начальный очный workshop Scratch / Blockly: 3 последовательных дня по 1 часу, всего 3 часа; не полнодневный или многонедельный лагерь. Interactive story, debugging и показ семье. После трёх лет соревнований сложность для Матвея нужно оценить.',
  'Workshop presencial inicial Scratch / Blockly: 3 días consecutivos de 1 hora, total 3 horas; no campamento de jornada completa ni de varias semanas. Interactive story, debugging y muestra familiar. Tras tres años de competiciones evaluar dificultad para Matvey.')
 p['language']=T('Сайт и syllabus прямо требуют Basic English; английский нужен для участия. Точный язык объяснений и возможность испанской / русской помощи не указаны.',
  'Web y syllabus exigen expresamente Basic English; inglés necesario para participar. Idioma exacto de explicaciones y apoyo español / ruso sin indicar.')
 p['confirmed_support_languages']=['EN'];p['language_evidence_role']='english_prerequisite_not_explicit_teaching_language'
 refs(p,('Specific workshop',CYBER),('Published course syllabus','https://www.cyberskills.mu/wp-content/uploads/2025/04/Course-Content-The-Coding-Wizards.pdf'));out.append(p)
 p=B(1307,'mauritius-child-school-programme','MDPA · ChILD school coding & robotics','MUS','Primary schools · Mauritius',['robotics','coding'],'Grades 4–6')
 p['programme_type']='school_route';p['programme']=T('Государственная программа ChILD знакомит учеников Grades 4–6 с coding и robotics через школы Mauritius и SENA. Это школьная инициатива, не открытый иностранный летний лагерь; возраст не заменяет класс и зачисление в школу.',
  'Programa público ChILD introduce coding y robotics a alumnos Grades 4–6 mediante escuelas de Mauritius y SENA. Iniciativa escolar, no campamento estival extranjero abierto; edad no sustituye curso y matrícula escolar.')
 p['family_fit']={c:candidate('unknown',SCHOOL_GRADE) for c in ['matvey','oscar']};refs(p,('Official ChILD programme',CHILD));out.append(p)
 assert len(out)==16
 return out

def update_report(report):
 rows=make_profiles();idx={p['id']:p for p in rows};old={p['id'] for p in report['profiles']}
 report['profiles']=[idx.get(p['id'],p) for p in report['profiles']]+[p for p in rows if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())];report.update(version=166,asof=CHECKED)

def E(d,ident,title,iso,url,start='',end='',**fields):
 c=next(c for c in d['countries'] if c['iso']==iso)
 e=event(ident,title,c['country'],url,start,end,region=c['region'],iso=[iso],language=LANG,language_certainty=LANG,entry=GATE,action=GATE,cost=UNKNOWN,note=GATE,checked=CHECKED)
 e.update(fields);return e

def enrich_v166(d):
 n=facts();rows=[];profiles=make_profiles()
 for e in d['events']:
  if e.get('camp_programme_id') in ['CP1296','CP1297','CP1298','CP1299']:e.update(priority=T('P4 — регистрация закрыта','P4 — inscripción cerrada'),registration_status=CLOSED,admission_kind='closed')
 for i,p in enumerate([p for p in profiles if not p['timing']['sessions']]):
  fit={'candidate':T('Да по возрасту; зачисление отдельно','Sí por edad; admisión aparte'),'conditional':T('Условно — класс / язык / доступ проверить','Condicional — verificar curso / idioma / acceso'),'unknown':SCHOOL_GRADE,'not_eligible':T('Нет — возраст или школьный уровень не подходит','No — edad o nivel escolar incompatible'),'later':T('Нет сейчас — будущий возраст','No ahora — edad futura')}
  mode='regular' if p.get('programme_type') in ['regular','school_route'] else 'day_camp'
  rows.append(E(d,'L'+str(464+i),p['provider'],p['iso'],p['sources'][0]['url'],block='Лагеря',city=p['place'],age=p['age'],format=p['accommodation'],mat=fit[p['family_fit']['matvey']['status']],osc=fit[p['family_fit']['oscar']['status']],gear=p['programme'],language=p['language'],language_certainty=p['language'],cost=p['price']['label'],entry=GATE,period=p['timing']['label'],note=p['programme']+' '+GATE,participation=mode,camp_programme_id=p['id'],camp_dossier_slug=p['slug'],themes=p['themes'],reward=EDU,scope='local',level=T('D — местная учебная программа','D — programa educativo local'),references=[dict(label=s['title'],url=s['url']) for s in p['sources']]))
 by={e['id']:e for e in d['events']};e=by['C069'];e.update(checked=CHECKED,age=T('Семь RoboBoom дисциплин: возраст и школьный класс различаются, сайт расходится с PDF.','Siete disciplinas RoboBoom: edad y curso escolar distintos, discrepancia web / PDF.'),mat=GRADE,osc=GRADE,entry=IRC_GATE,format=IRC_GATE,note=IRC_GATE,period=IRC_DATE,proof=T('Свежий bundle сайта и все семь связанных PDF прочитаны. Общая отметка 6–10 заменена условиями категорий; старые редакции не названы новым регламентом 2027.',
  'Leídos bundle actual y siete PDF enlazados. Etiqueta general 6–10 sustituida por condiciones de categorías; ediciones anteriores no declaradas reglamento nuevo 2027.'),languages=[],language=LANG,language_certainty=LANG)
 gear={
 'discover':T('Крупные блоки любого бренда, механическая перевозка и рука, 10 минут; PDF ≤6, сайт 4–6. Точный возраст Оскара на дате ещё неизвестен.', 'Bloques grandes de cualquier marca, transporte mecánico y brazo, 10 minutos; PDF ≤6, web 4–6. Edad exacta de Oscar en fecha aún desconocida.'),
 'smart':T('Preschool в PDF; только ручные механизмы, без автоматических моторов, sensors и controllers. Сайт 4–6. Нужен дошкольный статус, не только возраст.', 'Preschool en PDF; mecanismos manuales, sin motores automáticos, sensors ni controllers. Web 4–6. Requiere condición preescolar, no solo edad.'),
 'racing':T('PDF ≤ Grade 4; LEGO, размеры <20 × <20 × <20 cm, масса <1.5 kg, Drive Motors <3; autonomous line sprint. В revisions 30 минут debugging, в теле 60 — конфликт сохранить.', 'PDF ≤ Grade 4; LEGO, tamaño <20 × <20 × <20 cm, masa <1.5 kg, Drive Motors <3; autonomous line sprint. Revisions indican 30 minutos debugging, cuerpo 60 — conservar conflicto.'),
 'lego':T('PDF ≤ Grade 3, LEGO WeDo, сборка и программирование на месте 40 минут. В документе осталась тема 2022–2023; не применять как сезонную тему 2027.', 'PDF ≤ Grade 3, LEGO WeDo, construcción y programación presencial 40 minutos. Documento conserva tema 2022–2023; no aplicar como tema estacional 2027.'),
 'challenge':T('PDF ≤9, сайт 6–10. Пластиковые блоки, controller ports ≤4; разрешены подготовленный robot и code, автономные и remote-control задания. Матвею в 2027 будет 9–10: точный день и cutoff решают допуск.', 'PDF ≤9, web 6–10. Bloques plásticos, controller ports ≤4; robot y code preparados permitidos, tareas autónomas y remote-control. Matvey en 2027 tendrá 9–10: día exacto y cutoff determinan acceso.'),
 'curling':T('PDF ≤ Grade 3; remote-control curling, максимум 5 минут за раунд и два раунда. Сайт 6–10 не заменяет школьную группу.', 'PDF ≤ Grade 3; remote-control curling, máximo 5 minutos por ronda y dos rondas. Web 6–10 no sustituye grupo escolar.'),
 'parade':T('PDF ≤12 и 1–3 участника, одному снижается teamwork score; сайт 6–10 и 3–5. Полностью автономный line-following float с остановкой перед другим robot. Двое братьев численно подходят только по PDF, не подтверждённый допуск Egypt 2027.', 'PDF ≤12 y 1–3 participantes, uno recibe menor teamwork score; web 6–10 y 3–5. Float line-following totalmente autónomo con parada ante otro robot. Dos hermanos cumplen número solo según PDF, sin admisión Egypt 2027 acreditada.')}
 for r in n['egypt_roboboom']:
  mat=GRADE;osc=GRADE
  if r['key'] in ['discover','smart']:mat=T('Нет — младшая / дошкольная группа.','No — grupo menor / preescolar.')
  rows.append(E(d,r['id'],'IRC Egypt 2027 · '+r['name'],'EGY',IRC,age=r['pdf_group']+' · '+', '.join(r['website_details']),mat=mat,osc=osc,format=IRC_GATE,entry=IRC_GATE,gear=gear[r['key']],period=IRC_DATE,scope='international',league_id='irc',references=[dict(label='Published category PDF · '+r['pdf_revision'],url=r['pdf_url'])],note=IRC_GATE+' '+gear[r['key']],parent_event_id='C069',rules_year=int(r['pdf_revision'].split('-')[1].split('.')[0])))
 for stop in n['robo_africa']:
  is_mu=stop['iso']=='MUS';lang=T('Sessions are held in English прямо объявлено RGSC.','RGSC declara expresamente Sessions are held in English.') if is_mu else LANG
  rows.append(E(d,stop['id'],'ROBO Africa 2026 · '+stop['city'],stop['iso'],RGSC if is_mu else ROBO,stop['start'],stop['end'],block='События',city=stop['city'],age=T('Школьники / студенты / преподаватели; минимальный детский возраст не опубликован.','Escolares / estudiantes / docentes; edad mínima infantil no publicada.'),mat=T('Условно — возрастной вход и выбранную группу подтвердить.','Condicional — confirmar acceso por edad y grupo elegido.'),osc=T('Условно — младший ребёнок, вход и сопровождение подтвердить.','Condicional — niño menor, confirmar entrada y acompañamiento.'),format=T('Выставка, demos, VR / AR и workshops; не международный конкурс и не пансион.','Exposición, demos, VR / AR y workshops; no concurso internacional ni residencia.'),gear=T('Робототехника, AI, образовательные технологии, VR и подготовка к олимпиадам. На Mauritius опубликован дневной план 09:30–16:30; участие всей семьи и детские группы уточнить.',
   'Robótica, AI, tecnologías educativas, VR y preparación de olimpiadas. En Mauritius publicado plan diurno 09:30–16:30; confirmar participación familiar y grupos infantiles.'),cost=T('Участие бесплатно по организатору; регистрация, места, возраст и расходы поездки отдельно.','Participación gratuita según organizador; registro, plazas, edad y gastos de viaje aparte.'),language=lang,language_certainty=lang,languages=['EN'] if is_mu else [],language_mode='primary' if is_mu else 'unconfirmed',participation='visitor',scope='international',level=T('C — региональный образовательный roadshow','C — roadshow educativo regional'),visitor_policy='check',visitor_policy_note=GATE,adult_entry=GATE,references=[dict(label='Organiser route and free participation',url=ROBO)]+([dict(label='Host programme and English sessions',url=RGSC)] if is_mu else []),reward=EDU))
 rows.append(E(d,'C1450','Zambia JETS · Digital, Robotics & Intelligent Systems','ZMB',JETS,age='ECE / Primary / Secondary · TETS: tertiary',mat=SCHOOL_GRADE,osc=SCHOOL_GRADE,format=T('Школьная проектная / research программа; точный состав и уровень по локальным guidelines.','Programa escolar de proyectos / research; composición y nivel según guidelines locales.'),entry=T('Школа → district → province → national. Государственный календарь Zambia, не свободный иностранный семейный турнир. 2026 National Fair указан в сентябре; новый сезон и приём иностранцев не установлены.',
  'Escuela → district → province → national. Calendario público de Zambia, no torneo familiar extranjero libre. National Fair 2026 indicado en septiembre; nueva temporada y admisión extranjera sin establecer.'),gear=T('Software, robotics, AI, automation и IoT; пять доменов и Skills оцениваются по своим рубрикам.','Software, robotics, AI, automation e IoT; cinco dominios y Skills evaluados según sus rúbricas.'),scope='national',league_id='zambia-jets',period=T('Только сентябрь 2026 в анонсе; точные дни не восстановлены, 2027 не объявлен.','Solo septiembre 2026 en anuncio; días exactos sin recuperar, 2027 sin anunciar.')))
 rows.append(E(d,'C1451','Robotics for Good Youth Challenge Zambia · 2026 archive','ZMB',ITU,'2026-03-31','2026-03-31',city='Lusaka · Mulungushi International Conference Centre',age='10–18',mat=T('Нет — 31.03.2026 родившемуся в 2017 было 8–9, минимум 10.','No — el 31.03.2026 quien nació en 2017 tenía 8–9, mínimo 10.'),osc=T('Нет — младше 10.','No — menor de 10.'),entry=T('Прошедший национальный отбор к Geneva 2026; applications closed. Глобальная открытость не устанавливает иностранный допуск этого национального этапа. Новый Zambia 2027 не объявлен.',
  'Selección nacional pasada hacia Geneva 2026; applications closed. Apertura global no establece acceso extranjero a esta etapa nacional. Zambia 2027 nuevo sin anunciar.'),gear='Food security / agriculture · open-source hardware and software',priority=T('P4 — прошедший старший отбор','P4 — selección pasada de mayores'),scope='national',registration_status='Applications closed'))
 rows.append(E(d,'C1452','TTC · Junior Maker Hackathon · Q4 2026 watch','TZA','https://ttc.or.tz/',age=T('Primary students; числовой возраст не указан.','Primary students; edad numérica sin indicar.'),mat=SCHOOL_GRADE,osc=SCHOOL_GRADE,format=T('Первый software / hardware prototype для primary learners; состав команды и judging не опубликованы.','Primer software / hardware prototype para primary learners; composición y judging sin publicar.'),period='Q4 2026 · exact dates TBA',gear='Software / hardware prototypes',scope='local'))
 for row in rows:
  if row['id'] in ['C1443','C1444']:row['themes']=['robotics','engineering','technology']
  elif row['id'] in ['C1445','C1446','C1447','C1448','C1449']:row['themes']=['robotics','coding','technology']
  elif row['id'] in ['E232','E233']:row['themes']=['robotics','ai','technology']
  elif row['id']=='E234':row['themes']=['robotics','ai','coding','games','technology']
  elif row['id'] in ['C1450','C1451']:row['themes']=['robotics','ai','coding','technology']
  elif row['id']=='C1452':row['themes']=['coding','engineering','technology']
  if row['id'] in by:by[row['id']].update(row)
  else:d['events'].append(row);by[row['id']]=row
  if row.get('camp_programme_id'):
   report=d['camp_programmes'];p=next(p for p in report['profiles'] if p['id']==row['camp_programme_id'])
   p['related_event_ids']=list(dict.fromkeys(p.get('related_event_ids',[])+[row['id']]))
   if not any(x['programme_id']==p['id'] and x['event_id']==row['id'] for x in report['event_links']):report['event_links'].append(dict(programme_id=p['id'],event_id=row['id'],relation='existing_programme'))
 irc=next(p for p in d['league_guide']['profiles'] if p['id']=='irc');irc.update(checked=CHECKED,age_summary=by['C069']['age'],summary=by['C069']['proof'],route=IRC_GATE,hardware=T('Семь категорий с разными kit и ограничениями; выбирать по PDF и согласованному 2027 handbook.','Siete categorías con kits y límites distintos; elegir según PDF y handbook 2027 acordado.'),requirements=[IRC_GATE,IRC_DATE,GATE],nuances=[IRC_GATE,IRC_DATE],event_ids=['C069']+[x['id'] for x in n['egypt_roboboom']],categories=[dict(name=r['name'],age=by[r['id']]['age'],team=IRC_GATE,hardware=by[r['id']]['gear'],entry=IRC_GATE,event_id=r['id']) for r in n['egypt_roboboom']],sources=[src('Current category pages',IRC)]+[src(r['name']+' · linked PDF',r['pdf_url']) for r in n['egypt_roboboom']])
 pr=programme('zambia-jets','Zambia JETS · Digital, Robotics & Intelligent Systems','regional','ECE / Primary / Secondary',['6','9','10-12','teen'],['C1450'],summary=by['C1450']['gear'],route=by['C1450']['entry'],hardware=by['C1450']['gear'],requirements=[GRADE,GATE],nuances=[EDU],cost=UNKNOWN,award=EDU,language=LANG,sources=[src('DNSC official programme',JETS)],evidence=by['C1450']['proof'])
 ps=d['league_guide']['profiles'];ps[:]=[pr if p['id']==pr['id'] else p for p in ps]
 if not any(p['id']==pr['id'] for p in ps):ps.append(pr)
 d['league_guide'].update(version=166,checked=CHECKED)
 offers=[]
 for key,count,cost in [('one-morning',1,450),('nine-mornings-offer',9,2700)]:
  offers.append(dict(id='namibia-siblings-'+key+'-2026',slug='robotschool-namibia-holiday-junior',label='Robotschool Namibia · Junior + Senior · '+str(count)+' mornings',currency='NAD',price_year=2026,format='day',children=['matvey','oscar'],base_by_child=dict(matvey=cost,oscar=cost),discount_second=0,required=[],unknown_required=[dict(id='uncosted',unit='money',rate=1,min=0,label=UNKNOWN)],optional=[],unknown_trip=['travel','lodging','misc'],sessions=[['2026-11-23','2026-12-11']],sources=[NAM+'holiday-camp'],checked=CHECKED,gate=GATE,included=NAM_FEE,deposit_note=UNKNOWN,scope=NAM_TIMING+' '+NAM_FEE+' '+TRIP))
 ids={o['id'] for o in offers};d['camp_planning']['offers']=[o for o in d['camp_planning']['offers'] if o['id'] not in ids]+offers;d['camp_planning'].update(version=166,checked=CHECKED)
 known={s['url'] for s in d['sources']}
 for e in rows+[by['C069']]:
  for s in [dict(url=e['source'],title=e['title'])]+[dict(url=x['url'],title=x['label']) for x in e.get('references',[])]:
   if s['url'] not in known:d['sources'].append(dict(**s,checked=CHECKED,evidence=e['proof']));known.add(s['url'])
 d['africa_v166']=dict(version=166,checked=CHECKED,scope='selected_primary_opportunities',new_camp_dossiers=16,new_direct_events=len(rows),fully_audited_countries=0,worldwide_complete=False)
