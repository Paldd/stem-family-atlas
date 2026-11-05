"""Japan's actual junior routes, Asian exhibition windows and sourced winter camps."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
from camp_east_asia_v159 import base, add, age_fit, candidate
from camp_europe_v148 import weekdays
from nearby_regional_v160 import event, programme
from world_exhibitions_v162 import event as expo

ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-11-05';SPANISH={}
def T(a,b):SPANISH[a]=b;return a
RCJ='https://www.robocupjunior.jp/2027amagasaki_rule.html'
RCJ_DATES='https://www.robocupjunior.jp/2027amagasaki_outline.html'
RCJ_PDF='https://drive.google.com/uc?export=download&id=1ZB16rlv9flh-L2RZobxL1oL_uDYUnBaW'
KANTO='https://rcjj-kanto.org/'
KANTO_AI=KANTO+'kanto/archives/2457/'
HALO='https://www.haloschool.tw/halocamp/'
KID='https://kidleaderhub.com/courses/winter-camp/'
KID_BLOG='https://kidleaderhub.com/winter-camp-tphcm/'
KID_TERMS='https://kidleaderhub.com/terms-condition/'
BLANK='https://blankspace-studio.com/holiday-camps'
ANNE='https://annehill.school/holiday-camps/'
ANNE_PDF='https://annehill.school/wp-content/uploads/2026/10/AHI-Winter-Camp-2026-Booklet-2.pdf'
AI='https://ai-expo.tw/en/exhibit.html'
AI_VISIT='https://www.ai-expo.tw/en/early_visit.html'
AW='https://www.automationworld.co.kr/?hl=en'
AW_QA='https://www.automationworld.co.kr/sub-10'
SIIF='https://www.coex.co.kr/en/exhibitions/2026-seoul-international-invention-fair/'
FLL='https://firstjapan.jp/events/fll-explore-2026-2027/'
GATE=T('Место, иностранный индивидуальный приём, язык конкретной группы, уровень и полный счёт подтвердить. Возраст / дата не означают зачисление. Формы, согласия, сообщения и оплаты не выполнялись.',
 'Confirmar plaza, admisión extranjera individual, idioma del grupo concreto, nivel y factura completa. Edad / fecha no significan admisión. Sin formularios, consentimientos, mensajes ni pagos.')
LANG=T('Преподавание или судейство EN / ES / RU именно этой программы не подтверждено. Язык страницы / регламента не доказывает язык общения.',
 'Enseñanza o evaluación EN / ES / RU de este programa sin confirmar. Idioma de página / reglamento no acredita idioma de comunicación.')
UNKNOWN=T('Полная цена и условия выбранного набора ещё не установлены; неизвестные расходы не считаются нулём.',
 'Precio completo y condiciones de convocatoria elegida sin establecer; gastos desconocidos no equivalen a cero.')
TRIP=T('Жильё семьи, перелёты, местный транспорт, сопровождение, личная страховка и неуказанные доплаты отдельно.',
 'Alojamiento familiar, vuelos, transporte local, acompañamiento, seguro personal y cargos no indicados aparte.')
GRADE=T('Условно — требуется опубликованный школьный класс. Реальные классы детей неизвестны; возраст не подменяет класс. Иностранный доступ и язык отдельно.',
 'Condicional — exige curso escolar publicado. Cursos reales de niños desconocidos; edad no sustituye curso. Acceso extranjero e idioma aparte.')
EDU=T('Учебный проект / внутренние задания; это не подтверждённая международная конкурсная победа.',
 'Proyecto educativo / retos internos; no es victoria competitiva internacional acreditada.')
ROUTE=T('Внутренний путь: ближайший к месту проживания node → block → рекомендация на Japan Open. В PDF предусмотрены overseas slots, но конкретная заявка иностранной семьи, квота и сроки не установлены. Название Open не означает свободный семейный вход. Состав фиксируется с первого отбора; добавлять / заменять участников затем нельзя.',
 'Ruta doméstica: node cercano a residencia → block → recomendación a Japan Open. PDF contempla overseas slots, pero solicitud concreta de familia extranjera, cupo y plazos sin establecer. Nombre Open no implica acceso familiar libre. Equipo queda fijado desde primera selección; sin añadir / sustituir integrantes después.')
RCJ_AGE=T('Общий японский предел ≤19 на 01.07.2027, нижнего возраста нет. Challenge Entry / Youth дополнительно требуют не выше junior high на момент block. Нужно самостоятельно объяснять свой робот; возрастная возможность не доказывает навыки, допуск и мировой отбор.',
 'Límite japonés general ≤19 al 01.07.2027, sin edad mínima. Challenge Entry / Youth además exigen no superar junior high en block. Deben explicar robot propio; compatibilidad de edad no acredita capacidad, admisión ni selección mundial.')
RCJ_FIT=T('Условно — общего нижнего возраста в Japan Open нет. Самостоятельность, класс нужной категории, местный / overseas route, состав и язык интервью подтвердить.',
 'Condicional — Japan Open sin edad mínima general. Confirmar autonomía, curso de categoría, ruta local / overseas, equipo e idioma de entrevista.')
ADMIN=T('Нужен постер для Web-публикации: A3 landscape PDF ≤20MB; формат имени и сроки задаёт технический комитет. Соблюдать правила аккумуляторов; минимум 1 представитель команды (наставник, родитель или выпускник) помогает волонтёром на соревновании.',
 'Requiere póster para publicación Web: A3 landscape PDF ≤20MB; comité técnico fija nombre de archivo y plazos. Cumplir reglas de baterías; al menos 1 representante del equipo (mentor, padre o antiguo participante) ayuda como voluntario en el torneo.')
AI_RULE=T('Kanto 2027: AI / библиотеки не дают разрешения сдавать чужую работу. Ребёнок должен понимать алгоритм, объяснять применённый AI, запросы и собственную конструкцию; робот наставника запрещён. Это местное разъяснение, не универсальный регламент всех лиг.',
 'Kanto 2027: AI / bibliotecas no autorizan presentar trabajo ajeno. Niño debe entender algoritmo, explicar AI utilizado, instrucciones y construcción propia; robot del mentor prohibido. Aclaración local, no reglamento universal de ligas.')

def refs(p,*items):p['sources']=[dict(title=a,url=b,checked=CHECKED) for a,b in items]
def B(i,slug,title,iso,place,themes,age):
 p=base('CP'+str(i),slug,title,iso,T('Тайвань','Taiwán') if iso=='TWN' else T('Вьетнам','Vietnam'),place,themes)
 p.update(age=age,language=LANG,questions=[GATE],shortlist=[])
 p['price'].update(label=UNKNOWN,extras=TRIP,deposit=UNKNOWN)
 return p

def make_profiles():
 out=[]
 halo=[(1321,'lego-wedo','LEGO mechanics & WeDo','Grades 1–3',['robotics','coding','engineering'],[('2027-01-21','2027-01-22',4280)]),
  (1322,'lego-spike','LEGO SPIKE Challenge','Grades 3–9',['robotics','coding','engineering'],[('2027-01-25','2027-01-27',6280)]),
  (1323,'minecraft-redstone','Minecraft Redstone','Grades 1–3',['coding','games','engineering'],[('2027-01-25','2027-01-27',6280),('2027-01-28','2027-01-29',4280)]),
  (1324,'minecraft-makecode','Minecraft MakeCode','Grades 3–9',['coding','games'],[('2027-01-28','2027-01-29',4280),('2027-02-01','2027-02-03',6280)]),
  (1325,'vex-go','VEX GO RC Battles','Grades 1–6',['robotics','coding','engineering'],[('2027-02-01','2027-02-03',6280)]),
  (1326,'3d-printing','3D Printing & Tinkercad','Grades 3–9',['engineering','art'],[('2027-01-21','2027-01-22',5200)])]
 for i,key,title,age,themes,slots in halo:
  p=B(i,'halo-kaohsiung-winter-'+key,'Halo School · '+title,'TWN','556 Heti Road · 2F · Sanmin · Kaohsiung',themes,age)
  p['family_fit']={c:candidate('conditional',GRADE) for c in ['matvey','oscar']}
  p['programme']=T('Очный практический курс: '+title+'. Школьные уровни и задачи различаются; VEX GO — базовые RC / командные испытания, а не турнир VEX IQ. У Redstone и MakeCode двухдневные и трёхдневные версии имеют разные задания. 3–8 детей, обычно 6–8; набор запускают от 3.',
   'Curso práctico presencial: '+title+'. Niveles escolares y tareas distintos; VEX GO son retos básicos RC / grupales, no torneo VEX IQ. Versiones de dos y tres días de Redstone y MakeCode tienen tareas distintas. 3–8 niños, normalmente 6–8; inicia desde 3.')
  p['timing']['label']=T('Конкретные восемь потоков в январе / феврале 2027. Занятия 09–12 и 13:30–16, приём с 08:30, забрать до 17. Публикация даты не подтверждает остаток мест.',
   'Ocho grupos concretos en enero / febrero 2027. Clases 09–12 y 13:30–16, acogida 08:30, recogida hasta 17. Fecha publicada no confirma saldo de plazas.')
  p['timing']['status']='published_2027'
  p['price'].update(year=2027,currency='TWD',amount=slots[0][2],unit='child_camp',label=T('Два дня 4280 元, три дня 6280; 3D отдельно 5200 + обязательные материалы 800 = 6000. Валюта TWD по тайваньскому контексту, счёт подтвердить. До 20.11.2026: одиночный early bird платит 88% tuition; два потока одного ребёнка или братья / сёстры платят 85%. Акции не складываются, 800 материалов без скидки.',
   'Dos días 4280 元, tres días 6280; 3D aparte 5200 + materiales obligatorios 800 = 6000. Moneda TWD por contexto taiwanés, confirmar factura. Antes del 20.11.2026: early bird individual paga 88% de tuition; dos grupos de un niño o hermanos pagan 85%. Sin acumular promociones, 800 de materiales sin descuento.'),included=T('Обед включён. Для 3D — печатная ручка в подарок, модели печатают позже и отправляют; доставку и адрес иностранца согласовать.',
   'Almuerzo incluido. 3D incluye lápiz de impresión, modelos impresos y enviados después; acordar entrega y dirección extranjera.'),extras=T('Свой ноутбук / планшет нужен для занятий; аренда 100 元 / день, для 3D рекомендуют ноутбук. Забрать позже 17:00: 100 / полчаса. При погодной отмене сначала перенос, затем возврат если перенести нельзя; обычный добровольный отказ не описан. '+TRIP,
   'Portátil / tableta propio requerido; alquiler 100 元 / día, para 3D recomiendan portátil. Recogida después de 17:00: 100 / media hora. Cancelación meteorológica primero cambio, después devolución si imposible; baja voluntaria común sin describir. '+SPANISH[TRIP]))
  for n,(start,end,fee) in enumerate(slots,1):add(p,start,end,key+'-'+str(n),title+' · '+str(n),'TWD '+str(fee)+(' + 800 materials' if i==1326 else ''),HALO,weekdays(start,end),'09:00','16:00','Asia/Taipei',admission_kind='open_application')
  refs(p,('Current winter 2027 grid, equipment and discounts',HALO));out.append(p)
 p=B(1327,'kidleader-hcmc-winter','Kid LEADER Hub · Winter STEM / English','VNM','M7 Midtown · Phú Mỹ Hưng · District 7 · Ho Chi Minh City',['robotics','coding','ai','games','science','general'],'Camp 5–12; general terms 6–18')
 p.update(language=T('Курс прямо обещает обучение, общение и презентации на английском на протяжении всей программы; помощь преподавателя начинающим. Это конкретный EN лагерь, не вывод из языка сайта.',
  'Curso promete expresamente aprender, comunicarse y presentar en inglés durante todo programa; docentes apoyan principiantes. Campamento EN concreto, sin deducirlo del idioma web.'),confirmed_instruction_languages=['EN'],language_evidence_role='primary',family_fit=age_fit(6,12,'2026-12-21'),shortlist=['both','technical'])
 p['programme']=T('Группы 5–7 и 8–12: LEGO robotics, coding, science lab, arts / culture, physical games, Young Leaders и финансовые игровые проекты. Для 5–7 Scratch Jr без обязательного чтения. Выдают устройства и материалы; после трёх лет соревнований сложность согласовать. Общие terms пишут 6–18 вместо camp 5–12: оба ребёнка в пересечении, особый camp contract нужен.',
  'Grupos 5–7 y 8–12: LEGO robotics, coding, science lab, arts / culture, physical games, Young Leaders y proyectos financieros lúdicos. Scratch Jr para 5–7 sin lectura obligatoria. Facilitan dispositivos y material; acordar dificultad tras tres años de competiciones. Terms generales dicen 6–18 frente a camp 5–12: ambos en intersección, requiere contrato específico del camp.')
 p['timing'].update(status='published_2026_27',label=T('21 декабря 2026 – 8 января 2027, Пн–Пт 09–15:15; не работают 1 января. 25 декабря источником не исключено. Виджет пишет 15 buổi, но опубликованные будни без 1 января дают 14 дней: противоречие сохранено, пятнадцатый день не придуман.',
  '21 de diciembre 2026 – 8 de enero 2027, lunes–viernes 09–15:15; cerrado 1 de enero. Fuente no excluye 25 de diciembre. Widget dice 15 buổi, pero días laborables publicados sin 1 de enero suman 14: discrepancia conservada, sin inventar día quince.'))
 p['price'].update(year=2026,currency='VND',label=UNKNOWN,included=T('Робототехнические наборы, планшеты и инструменты лаборатории предоставляются по программе. Полный состав включений и обязательные материалы в счёте ещё проверить.',
  'Programa facilita kits robóticos, tabletas e instrumentos de laboratorio. Verificar inclusiones completas y materiales obligatorios en factura.'),extras=T('Обед можно заказать у центра; это дополнительный выбор, включение / стоимость не опубликованы. Допускается забирать ребёнка на обед. Депозит, возврат, техника на дом и все тарифы требуют отдельного счёта. '+TRIP,
  'Puede pedirse almuerzo al centro; opción adicional, inclusión / precio sin publicar. Permiten recoger al niño para almorzar. Depósito, devolución, equipo para casa y tarifas requieren factura aparte. '+SPANISH[TRIP]))
 for n,(start,end) in enumerate([('2026-12-21','2026-12-25'),('2026-12-28','2026-12-31'),('2027-01-04','2027-01-08')],1):add(p,start,end,'winter-week-'+str(n),'Winter week '+str(n),UNKNOWN,KID,weekdays(start,end),'09:00','15:15','Asia/Ho_Chi_Minh',admission_kind='open_application')
 refs(p,('Actual winter curriculum, English, hours and equipment',KID),('Specific 2026/27 dates and excluded January 1',KID_BLOG),('General services ages, not a camp-specific refund agreement',KID_TERMS));out.append(p)
 p=B(1328,'blank-space-saigon-winter','Blank Space Studio · Winter Art Camp','VNM','4 Nguyễn Quý Cảnh · An Khánh · Ho Chi Minh City',['general','art','culture'],'4–12')
 p.update(confirmed_instruction_languages=['EN'],language_evidence_role='bilingual',language=T('В описании именно holiday camps указаны Vietnamese и English. Это доступная билингвальная программа, не обещание только английского в любой группе.',
  'Descripción de holiday camps indica Vietnamese y English. Programa bilingüe disponible, sin promesa de inglés exclusivo en cualquier grupo.'),family_fit={c:candidate('conditional',GATE) for c in ['matvey','oscar']},availability=dict(status='unknown',label=T('Статус противоречив: holiday page Registration Open, главная Full / Registration Closed у того же Winter Camp. Места не подтверждены; согласовать до поездки.',
  'Estado contradictorio: holiday page Registration Open, portada Full / Registration Closed para mismo Winter Camp. Plazas sin confirmar; acordar antes de viajar.')))
 p['programme']=T('Полудневный художественный camp: fluid art, splatter / motion painting, общие полотна и зимние поделки. 5–8 детей, обычно группы 4–6 и 7–12 при достаточном наборе. Это творческий отдых, не робототехника или coding.',
  'Camp artístico de media jornada: fluid art, splatter / motion painting, lienzos grupales y manualidades invernales. 5–8 niños, normalmente grupos 4–6 y 7–12 con suficientes inscritos. Descanso creativo, no robótica ni coding.')
 p['timing'].update(status='published_2026_27',label=T('Четыре недели: 14–18, 21–24, 28–31 декабря 2026 и 4–8 января 2027; утро 09–12 или после обеда 14–17. 25 декабря и 1 января закрыто. Общий footer Mon Closed конфликтует с опубликованными camp Mondays; подтвердить выбранный поток.',
  'Cuatro semanas: 14–18, 21–24, 28–31 de diciembre 2026 y 4–8 de enero 2027; mañana 09–12 o tarde 14–17. Cerrado 25 de diciembre y 1 de enero. Footer general Mon Closed contradice lunes del camp publicados; confirmar grupo elegido.'))
 p['price'].update(year=2026,currency='VND',amount=1200000,unit='child_half_day',label=T('До 8% VAT: разовое полдня 1200000, пакет 4 дней 4000000, 5 дней 4800000. До 30.11 early bird соответственно 960000 / 3200000 / 3840000. VAT прибавляется отдельно; оплата картой ещё 3%, базу начисления подтвердить. Это цены выбранного полудневного блока, не полного дня.',
  'Antes de 8% VAT: media jornada suelta 1200000, paquete 4 días 4000000, 5 días 4800000. Antes del 30.11 early bird respectivamente 960000 / 3200000 / 3840000. VAT aparte; pago con tarjeta añade 3%, confirmar base de cálculo. Precios de bloque elegido de media jornada, no jornada completa.'),included=T('Перекус, материалы, фартуки, инструменты и уборка включены. Полноценный обед и присмотр между утренним / дневным блоком не обещаны.',
  'Merienda, materiales, delantales, herramientas y limpieza incluidos. Sin promesa de almuerzo completo ni supervisión entre bloques.'),deposit=T('Депозит VND 1000000 за место ребёнка, остаток в первый день. Депозит входит в цену, повторно не добавлен. Условия возврата не установлены: ссылка Terms of Service вернула главную, а не договор. Готовую картину забирают через 2–3 рабочих дня; доставка возможна, цена отдельно.',
  'Depósito VND 1000000 por plaza infantil, saldo primer día. Depósito incluido en precio, sin añadir otra vez. Devolución sin establecer: enlace Terms of Service devolvió portada, no contrato. Recoger obra tras 2–3 días laborables; entrega posible, precio aparte.'))
 for n,(start,end) in enumerate([('2026-12-14','2026-12-18'),('2026-12-21','2026-12-24'),('2026-12-28','2026-12-31'),('2027-01-04','2027-01-08')],1):
  for key,begin,finish in [('am','09:00','12:00'),('pm','14:00','17:00')]:add(p,start,end,'week-'+str(n)+'-'+key,'Winter art week '+str(n)+' · '+key,'VND '+str(4800000 if n in [1,4] else 4000000)+' + 8% VAT',BLANK,weekdays(start,end),begin,finish,'Asia/Ho_Chi_Minh',admission_kind='open_application')
 refs(p,('Actual camp languages, dated weeks, VAT and card fees',BLANK),('Homepage conflicting full / closed camp banner','https://blankspace-studio.com/'));out.append(p)
 for i,key,lo,hi in [(1329,'younger',5,7),(1330,'older',8,14)]:
  p=B(i,'anne-hill-winter-'+key,'Anne Hill · Winter Expedition '+key,'VNM','Primary Campus · 31 Giang Van Minh · An Khánh · Ho Chi Minh City',['general','sport','art','science']+(['robotics','coding'] if key=='older' else []),str(lo)+'–'+str(hi)+(' · Years 1–3' if key=='younger' else ' · Years 4–10'))
  p['family_fit']=age_fit(lo,hi,'2026-12-14')
  for c in p['family_fit']:
   if p['family_fit'][c]['status']=='candidate':p['family_fit'][c]=candidate('conditional',GRADE)
  p['programme']=T('Дневной общий camp. Group A 5–7 / Years 1–3: спорт, art, handwriting, STEM в среду; robotics / coding в его sample timetable нет. Group B 8–10 и C 8–14: robotics в среду и coding в четверг, плюс спорт / STEM. Поэтому программа Матвея и Оскара различается; placement C зависит от числа записей. 18 декабря — выезд, обычных уроков нет.',
   'Camp general diurno. Group A 5–7 / Years 1–3: deporte, art, handwriting, STEM miércoles; sin robotics / coding en su sample timetable. Group B 8–10 y C 8–14: robotics miércoles y coding jueves, más deporte / STEM. Programas de Matvey y Oscar distintos; placement C depende de inscritos. 18 de diciembre es excursión, sin clases normales.')
  p['timing'].update(status='published_2026',label=T('Только весь camp из 12 дней: 14–18, 21–24 и 28–30 декабря 2026, 08:30–15:00. Недельная / гибкая покупка не предлагается. Регистрация до 20 ноября, оплата до 27 ноября; early bird 23 октября уже истёк.',
   'Solo camp completo de 12 días: 14–18, 21–24 y 28–30 de diciembre 2026, 08:30–15:00. Sin compra semanal / flexible. Inscripción hasta 20 de noviembre, pago hasta 27 de noviembre; early bird 23 de octubre ya vencido.'))
  p['price'].update(year=2026,currency='VND',amount=20400000,unit='child_full_camp',label=T('VND 20400000 за ребёнка 5–14 / весь camp. Младшему sibling −10% tuition: двум 38760000 при подтверждённом placement. Старый early bird −10% не применён. Bus 1600000 в одну сторону / 2200000 туда-обратно; aftercare 15–17 по 250000 / час, единицы сервиса подтвердить.',
   'VND 20400000 por niño 5–14 / camp completo. Hermano menor −10% tuition: ambos 38760000 con placement confirmado. Early bird antiguo −10% sin aplicar. Bus 1600000 un trayecto / 2200000 ida y vuelta; aftercare 15–17 a 250000 / hora, confirmar unidades del servicio.'),included=T('Обед включён. Школа предоставляет нужное учебное оборудование; требования к одежде / спорту и дополнительному выезду ещё согласовать.',
   'Almuerzo incluido. Escuela facilita equipo educativo necesario; acordar ropa / deporte y excursión adicional.'),deposit=T('PDF прямо: все оплаченные fees без возврата. Зачисление только на полный camp; окончательный invoice после регистрации. Формы, медицинские согласия и договор не принимались.',
   'PDF expresa que todos fees pagados son no reembolsables. Matrícula solo camp completo; invoice final tras inscripción. Sin formularios, consentimientos médicos ni contrato.'))
  days=[day for day in weekdays('2026-12-14','2026-12-30') if day!='2026-12-25']
  add(p,days[0],days[-1],'winter-full-camp-2026','Winter Expedition · full 12-day camp',p['price']['label'],ANNE,days,'08:30','15:00','Asia/Ho_Chi_Minh',deadline='2026-11-20',admission_kind='open_application')
  refs(p,('Open to school and external children; exact seasonal window',ANNE),('2026 brochure · prices and separate age-group timetables',ANNE_PDF));out.append(p)
 assert len(out)==10
 return out

def update_report(report):
 rows=make_profiles();by={p['id']:p for p in rows};old={p['id'] for p in report['profiles']}
 report['profiles']=[by.get(p['id'],p) for p in report['profiles']]+[p for p in rows if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),swiss=sum(p['iso']=='CHE' for p in report['profiles']),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())];report.update(version=168,asof=CHECKED)

def competition_rows(d):
 country=next(c for c in d['countries'] if c['iso']=='JPN');rows=[]
 cats=[('Soccer Vision','World',2,4,'Soccer Rules 2027 · Vision local rules',''),('Soccer Infrared','World',2,4,'Soccer Rules 2027 · new official IR ball',''),('Soccer Youth','Challenge',2,4,'Soccer 2027 · RCJ-05R','youth'),('Soccer Entry','Challenge',2,4,'Soccer 2027 local rules · RCJ-05R','soccer-entry'),('Rescue Line','World',2,4,'Rescue Line 2026 + announced local amendments',''),('Rescue Maze','World',2,4,'Rescue Maze 2026 + announced local amendments',''),('Rescue Simulation','World',2,4,'Rescue Simulation 2026 · Erebus 26.1',''),('Rescue Line Entry','Challenge',1,2,'Japanese Rescue Line Entry 2026 + local amendments','line-entry'),('Rescue Maze Entry','Challenge',1,2,'Japanese Rescue Maze Entry 2026 + local amendments','maze-entry'),('Rescue Simulation Entry','Challenge',1,2,'Simplified Rescue Simulation 2026 · Erebus 26.1','sim-entry'),('RCAP CoSpace Autonomous Driving','Challenge',1,4,'RCAP 2023 U-19 · CoSpace Auto-Driving 2022 V22.4.4','cospace'),('OnStage','World',2,5,'Domestic rules based on RoboCup 2026 OnStage',''),('OnStage Entry','Challenge',1,6,'OnStage Challenge Class rulebook','onstage-entry')]
 history={
 'soccer-entry':T('Нельзя с прежним Japan Open Soccer Entry / Japan League; онлайн 2021 не считается.','Excluye experiencia previa Japan Open Soccer Entry / Japan League; online 2021 no cuenta.'),
 'line-entry':T('Нельзя с прежним Japan Open Rescue Line Entry.','Excluye experiencia previa Japan Open Rescue Line Entry.'),
 'maze-entry':T('Нельзя с прежним World Rescue Maze на Japan Open или top 3 Maze Entry. Одно прошлое участие Entry не запрещено.','Excluye World Rescue Maze previo en Japan Open o top 3 Maze Entry. Simple participación Entry anterior permitida.'),
 'sim-entry':T('Нельзя с прежним World Rescue Simulation на Japan Open. Entry новая: нет зон 3–4, floating tiles и буквенных victims; сложность снижена, не произвольная игра на любом симуляторе.','Excluye World Rescue Simulation previo en Japan Open. Entry nueva: sin zonas 3–4, floating tiles ni victims con letras; dificultad reducida, no juego libre en cualquier simulador.'),
 'onstage-entry':T('Нельзя с прежним World OnStage на Japan Open или top 3 старой OnStage Japan League; онлайн 2021 не считается. Обычное прошлое Entry участие допускается.','Excluye World OnStage previo en Japan Open o top 3 antigua OnStage Japan League; online 2021 no cuenta. Simple participación Entry anterior permitida.'),
 'cospace':T('На Japan Open эта дисциплина проводится последний раз в 2027. Не выше 19 на 01.07.2027, без дополнительной junior-high границы.','Última edición de esta disciplina en Japan Open en 2027. Máximo 19 al 01.07.2027, sin límite adicional junior-high.'),
 'youth':T('Не выше junior high; число предыдущих выступлений не ограничено.','No superar junior high; actuaciones anteriores sin límite.')}
 for i,(name,kind,lo,hi,gear,key) in enumerate(cats,1453):
  nuance=history.get(key,T('Младшие могут участвовать во внутреннем World Class, но международные критерии и квоту это не заменяет.','Menores pueden competir en World Class doméstico, sin sustituir criterios internacionales ni cupo.'))
  reward=T('Только World Class выбирает рекомендации к RoboCup 2027; даже победа в Challenge Class не мировой отбор. RCAP / другие superregional рекомендации этим Japan Open не отбираются.',
   'Solo World Class selecciona recomendaciones a RoboCup 2027; ganar Challenge Class no clasifica al mundial. Este Japan Open no selecciona recomendaciones RCAP / otros superregional.')
  row=event('C'+str(i),'RoboCupJunior Japan Open 2027 · '+name,country['country'],RCJ_DATES,'2027-03-20','2027-03-21',region=country['region'],iso=['JPN'],city='Baycom General Gymnasium · Amagasaki · Hyogo',league_id='rcj-japan',age=RCJ_AGE,mat=RCJ_FIT,osc=RCJ_FIT,team_min=lo,team_max=hi,format=str(lo)+'–'+str(hi)+T(' участника + наставник 18+; мировой наставник 19+.',' integrantes + mentor 18+; mentor mundial 19+.'),entry=ROUTE+' '+ADMIN,gear=gear,language=LANG,language_certainty=LANG,cost=UNKNOWN,scope='national',level=T('B — национальный финал / местные правила','B — final nacional / reglas locales'),reward=reward,note=nuance+' '+AI_RULE,action=ROUTE,period=T('20–21 марта — два общих дня соревнования; setup 19 марта отдельно. Расписание конкретной дисциплины ещё уточняется.','20–21 de marzo son dos días generales de competición; setup 19 de marzo aparte. Horario de disciplina concreta por precisar.'),date_scope='assigned_day_window',admission_kind='qualification',references=[dict(label='2027 competition guidelines · pages 1–9',url=RCJ_PDF),dict(label='Official rules page',url=RCJ),dict(label='Kanto-specific AI clarification',url=KANTO_AI)])
  row['themes']=['robotics','coding','engineering'];row['participation']='individual_or_team' if lo==1 else 'team';rows.append(row)
 for i,key,title,start,end in [(1466,'tokyokanagawa2027/','Tokyo / Kanagawa joint node','2026-11-14','2026-11-15'),(1467,'chiba2027/','Chiba node','2026-11-29','2026-11-29'),(1468,'kanto2027/','Kanto block','2027-01-10','2027-01-11')]:
  cost=T('Цена выбранного этапа не установлена.','Precio de etapa elegida sin establecer.')
  if i==1467:cost=T('JPY 2000 / команда + 1000 / участник; двоим в одной команде 4000 до техники и дороги. До 18 лет нужен Chiba Children Exchange Center usage card; оформление для иностранца отдельно.',
   'JPY 2000 / equipo + 1000 / integrante; ambos en un equipo 4000 antes de equipo y viaje. Menores de 18 requieren usage card de Chiba Children Exchange Center; trámite para extranjero aparte.')
  rows.append(event('C'+str(i),'RoboCupJunior Japan · '+title,country['country'],KANTO+key,start,end,region=country['region'],iso=['JPN'],city='Chiba Children Exchange Center' if i==1467 else 'Tokyo Metropolitan College of Industrial Technology · Shinagawa Campus',league_id='rcj-japan',age=RCJ_AGE,mat=RCJ_FIT,osc=RCJ_FIT,entry=ROUTE,gear=T('Дисциплину и локальные различия проверить; не все 13 национальных категорий автоматически проводятся в каждом node.',
   'Comprobar disciplina y diferencias locales; no todas 13 categorías nacionales se celebran automáticamente en cada node.'),format=T('Состав по дисциплине: от 1 ребёнка в разрешённых Entry, до 6 в OnStage Entry.','Equipo según disciplina: desde 1 niño en Entry permitidas, hasta 6 en OnStage Entry.'),cost=cost,language=LANG,language_certainty=LANG,deadline='2026-10-25' if i!=1468 else '',registration_status=T('Node entry до 25 октября 2026 уже завершён; поздний / иностранный приём не подтверждён. Block требует отбора, не свободной новой заявки.',
   'Node entry hasta 25 de octubre 2026 ya terminado; acceso tardío / extranjero sin confirmar. Block requiere selección, no nueva solicitud libre.'),action=ROUTE,note=AI_RULE,scope='regional',date_scope='assigned_day_window',admission_kind='qualification',references=[dict(label='Common national eligibility',url=RCJ_PDF)]))
 return rows

def enrich_v168(d):
 rows=competition_rows(d);by={e['id']:e for e in d['events']}
 for i in range(1134,1145):
  e=by['C'+str(i)];e['checked']=CHECKED
  e['registration_status']=T('Explore / Challenge: командная регистрация завершилась 31.10.2026; текущий поздний приём не обещан. National — через опубликованный отбор / отдельные условия. Future Edition имеет отдельный срок 31.12.2026.',
   'Explore / Challenge: inscripción de equipos terminó 31.10.2026; sin promesa de acceso tardío actual. National mediante selección publicada / condiciones separadas. Future Edition tiene plazo distinto 31.12.2026.')
  if i==1144:e['registration_status']=T('Future Edition: опубликована регистрация до 31.12.2026. Нужны 4–10 детей, подходящий класс на контрольную дату и согласованный иностранный доступ; два брата не готовая команда.',
   'Future Edition: inscripción publicada hasta 31.12.2026. Requiere 4–10 niños, curso adecuado en fecha de referencia y acceso extranjero acordado; dos hermanos no son equipo listo.')
 by['C1143'].update(period=T('Предварительно 14 февраля 2027, Institute of Science Tokyo; содержание и способ участия должны объявить в ноябре. Дата остаётся планом, start / end пусты.',
  'Provisionalmente 14 de febrero 2027, Institute of Science Tokyo; contenido y acceso se anunciarían en noviembre. Fecha sigue prevista, start / end vacíos.'),planned_windows=[['2027-02-14','2027-02-14']],source=FLL)
 e=by['E025'];e.update(start='2027-03-24',end='2027-03-26',date_status=T('Подтверждено','Confirmado'),date_scope='exhibition_window',checked=CHECKED,source=AI,city='Taipei Expo Dome · Yuanshan · Taipei',period='24–26 March 2027 · 09:00–16:30',age=T('Детский вход 6 / 9 лет не установлен.','Entrada infantil de 6 / 9 años sin establecer.'),entry=T('Есть visitor pre-registration отдельно от exhibitor interest. Это B2B выставка; форма интереса не билет и не подтверждённый детский допуск.',
  'Visitor pre-registration separado de exhibitor interest. Exposición B2B; formulario de interés no es entrada ni acceso infantil confirmado.'),language=LANG,language_certainty=LANG,languages=[],cost=UNKNOWN,visitor_policy='confirm_children',visitor_policy_note=GATE,exhibitor_note=T('Четыре темы 2027: inference economy, enterprise AI, sovereign AI, physical AI. Около 30000 buyers — маркетинговое описание, не гарантированная посещаемость / список всех компаний 2027.',
  'Cuatro temas 2027: inference economy, enterprise AI, sovereign AI, physical AI. Unos 30000 buyers es descripción comercial, no asistencia garantizada / lista completa de empresas 2027.'),references=[dict(label='Official 2027 exhibition',url=AI),dict(label='Visitor interest route',url=AI_VISIT)],themes=['ai','robotics','technology'],action=GATE)
 e.update(language_mode='unconfirmed',proof=T('Прочитаны официальные exhibition и visitor страницы 2027: даты 24–26 марта и площадка подтверждены; возраст посетителей и полный билетный тариф ещё не установлены.',
  'Leídas páginas oficiales exhibition y visitor 2027: fechas 24–26 de marzo y sede confirmadas; edad de visitantes y tarifa completa aún sin establecer.'),note=GATE,adult_entry=GATE,exhibitor_directory_url='')
 for i,name,start,end,url,place in [(235,'Seoul International Invention Fair · SIIF 2026','2026-12-02','2026-12-05',SIIF,'Coex · Hall C · Seoul'),(236,'Automation World · AW 2027','2027-03-03','2027-03-05',AW,'Coex · Seoul')]:
  row=expo(i,name,'KOR',place,start,end,url,['robotics','ai','technology','engineering'],[T('Изобретения, технологии и прикладная инженерия','Inventos, tecnología e ingeniería aplicada')])
  row.update(checked=CHECKED,visitor_policy='confirm_children',visitor_policy_note=GATE,age=T('Детский вход в 6 / 9 лет не подтверждён; семейный визит согласовать.','Entrada infantil a 6 / 9 años sin confirmar; acordar visita familiar.'),language=LANG,language_certainty=LANG,languages=[],adult_entry=GATE,themes=['technology','engineering']+(['ai'] if i==236 else []),importance_reason=T('Международная профильная площадка для изобретателей / промышленной автоматизации. Наличие роботов и конкретных компаний в выбранном выпуске проверить по его списку участников.',
   'Plataforma internacional especializada para inventores / automatización industrial. Comprobar robots y empresas concretas de edición elegida en su lista de participantes.'))
  if i==235:row.update(cost=T('Бесплатный вход по официальному Coex; это не бесплатная подача изобретения на конкурс. Детский допуск и расходы поездки отдельно.',
   'Entrada gratuita según Coex oficial; no es presentación gratuita de invento a concurso. Acceso infantil y gastos de viaje aparte.'),period='2–4 December · 10:00–17:00; 5 December · 10:00–15:00')
  else:row.update(cost=T('Тариф 2027 не установлен. FAQ под заголовком 2027 всё ещё даёт срок 11.03.2025 и onsite KRW 20000: это старые условия, они не использованы как текущая цена или дедлайн.',
   'Tarifa 2027 sin establecer. FAQ bajo título 2027 aún indica plazo 11.03.2025 y onsite KRW 20000: condiciones antiguas, sin usarlas como precio o plazo vigente.'),references=[dict(label='Current March 2027 window',url=AW),dict(label='FAQ retained stale 2025 terms',url=AW_QA)],exhibitor_note=T('Сайт предлагает AI Factory и автоматизацию; ссылка списка экспонентов относится к 2026. Компании прошлого выпуска не объявлены участниками 2027.',
   'Web ofrece AI Factory y automatización; enlace de expositores corresponde a 2026. Empresas anteriores no declaradas participantes 2027.'))
  rows.append(row)
 for row in rows:
  if row['id'] in by:by[row['id']].update(row)
  else:d['events'].append(row);by[row['id']]=row
 catrows=rows[:13];pr=programme('rcj-japan','RoboCupJunior Japan · World / Challenge Class','regional',RCJ_AGE,['6','9','10-12','teen'],[r['id'] for r in rows[:16]],summary=RCJ_AGE,route=ROUTE,hardware=T('Автономный Soccer / Rescue, симуляторы Erebus и CoSpace, сценический робот; выбранные локальные ограничения по дисциплине.',
  'Soccer / Rescue autónomos, simuladores Erebus y CoSpace, robot escénico; límites locales según disciplina.'),language=LANG,cost=UNKNOWN,award=catrows[0]['reward'],requirements=[ROUTE,RCJ_AGE,ADMIN,GATE],nuances=[AI_RULE,catrows[0]['reward']],sources=[dict(title='2027 guidelines · v1.0 · 25 Sep 2026',url=RCJ_PDF,checked=CHECKED),dict(title='National dates',url=RCJ_DATES,checked=CHECKED)],categories=[dict(name=e['title'].split(' · ')[-1],age=e['age'],team=e['format'],hardware=e['gear'],entry=e['note'],event_id=e['id']) for e in catrows])
 ps=d['league_guide']['profiles'];ps[:]=[pr if p['id']==pr['id'] else p for p in ps]
 if not any(p['id']==pr['id'] for p in ps):ps.append(pr)
 d['league_guide'].update(version=168,checked=CHECKED)
 offers=[]
 def O(key,slug,label,bases,currency,dates,sources,gate,included,required=None,optional=None,discount=0):
  offers.append(dict(id=key,slug=slug,label=label,currency=currency,price_year=2026 if currency=='VND' else 2027,format='day',children=list(bases),base_by_child=bases,discount_second=discount,required=required or [],unknown_required=[dict(id='unpriced',label=UNKNOWN,unit='money',rate=1,min=0)],optional=optional or [],unknown_trip=['travel','lodging','misc'],sessions=dates,sources=sources,checked=CHECKED,gate=gate,included=included,deposit_note=GATE,scope=TRIP))
 profiles=make_profiles();pd={p['id']:p for p in profiles}
 for key,bases,pid,dates,material in [('two-day-mixed',dict(matvey=5200,oscar=4280),'CP1326',[['2027-01-21','2027-01-22']],800),('three-day-siblings',dict(matvey=6280,oscar=6280),'CP1322',[['2027-01-25','2027-01-27']],0),('3d-matvey-only',dict(matvey=5200),'CP1326',[['2027-01-21','2027-01-22']],800)]:
  count=2 if key=='two-day-mixed' else 3 if key=='three-day-siblings' else 2
  O('halo-winter-2027-'+key,pd[pid]['slug'],'Halo · '+key,bases,'TWD',dates,[HALO],GRADE+' '+LANG+' '+GATE,pd[pid]['price']['included'],required=[dict(id='materials',label=T('Обязательные 3D материалы без скидки','Materiales 3D obligatorios sin descuento'),amount=material)] if material else [],optional=[dict(id='rental',label=T('Аренда устройства каждому ребёнку на выбранные дни','Alquiler de dispositivo para cada niño durante días elegidos'),amount=100*count*len(bases))])
 for days,regular,promo in [(5,4800000,3840000),(4,4000000,3200000)]:
  p=pd['CP1328'];dates=[v for v in p['timing']['sessions'] if (5 if v[0] in ['2026-12-14','2027-01-04'] else 4)==days]
  for rate,amount in [('standard',regular),('early-bird',promo)]:
   O('blank-winter-'+str(days)+'-days-'+rate,p['slug'],'Blank Space · '+str(days)+' half-days · '+rate,dict(matvey=amount,oscar=amount),'VND',dates,[BLANK],p['availability']['label']+' '+p['price']['label']+' '+GATE,p['price']['included'],required=[dict(id='vat',label='8% VAT · 2 children',amount=amount*2*.08)])
 p=pd['CP1330'];O('anne-hill-winter-2026-siblings',p['slug'],'Anne Hill · separate sibling curricula · full 12 days',dict(matvey=20400000,oscar=20400000),'VND',p['timing']['sessions'],[ANNE,ANNE_PDF],p['programme']+' '+p['price']['label']+' '+LANG,p['price']['included'],discount=.1)
 ids={o['id'] for o in offers};d['camp_planning']['offers']=[o for o in d['camp_planning']['offers'] if o['id'] not in ids]+offers;d['camp_planning'].update(version=168,checked=CHECKED)
 known={s['url'] for s in d['sources']}
 for e in rows+[by['E025']]+[by['C'+str(i)] for i in range(1134,1145)]:
  for s in [dict(title=e['title'],url=e['source'])]+[dict(title=x['label'],url=x['url']) for x in e.get('references',[])]:
   if s['url'] not in known:d['sources'].append(dict(**s,checked=CHECKED,evidence=GATE));known.add(s['url'])
 d['asia_v168']=dict(version=168,checked=CHECKED,new_camp_dossiers=10,new_competitions=16,new_exhibition_events=2,new_league_profiles=1,new_budget_offers=len(offers),fully_audited_countries=0,worldwide_complete=False)
