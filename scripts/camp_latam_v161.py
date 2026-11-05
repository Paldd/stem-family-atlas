"""Project-level Guatemala timetable and explicit Latin American programme gates."""
from collections import Counter
from copy import deepcopy
from camp_east_asia_v159 import base,candidate,add,source,NO_BOOKING
from camp_europe_v148 import weekdays

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
COS='https://www.cosami.com.gt/cursos-vacacionales-2026/'
POSTER='https://bucket-l1kf8c.s3.amazonaws.com/wp-content/uploads/2026/09/horarios-robotica-2.jpg'
FORM='https://forms.cloud.microsoft/r/MtvhMtb5CB'
MUNI='https://muniguatealfrente.com/tec-camp-las-vacaciones-se-convierten-en-una-aventura-tecnologica-para-ninos-y-jovenes/'
CAJA='https://market.cajamag.com.co/product-page/119'
CULT='https://cultivatec.com.mx/curso-robotics-winter-camp.html'
ROBO='https://www.robotiki.com.ar/'
VST='https://villacampast.com/campamentos'
UVM='https://uvm.edu.ve/uvm-impulsa-talento-juvenil-con-el-inicio-del-plan-vacacional-power-on/'
UTP='https://sistemasinteligentes.utp.ac.pa/2026/03/24/labsi-summer-camp-de-robotica-basica-2026/'
COUNTRIES={'GTM':'Гватемала','COL':'Колумбия','MEX':'Мексика','ARG':'Аргентина','DOM':'Доминиканская Республика','VEN':'Венесуэла','PAN':'Панама'}
LANG=T('Описание по-испански; прямое подтверждение языка выбранной группы EN / ES и иностранного индивидуального доступа не найдено. Язык страницы не заменяет язык преподавания.',
 'Descripción en español; sin localizar confirmación expresa del idioma EN / ES del grupo elegido ni acceso extranjero individual. Idioma de página no sustituye idioma de enseñanza.')
ACCESS=T('Проверить возраст и уровень после трёх лет соревнований, язык занятий, точную площадку, свободное место, иностранный приём и итоговый счёт. Формы, сообщения, согласия и платежи не отправлялись.',
 'Verificar edad y nivel tras tres años de competiciones, idioma de clases, sede exacta, plaza, admisión extranjera y factura final. Sin enviar formularios, mensajes, consentimientos ni pagos.')
UNKNOWN_PRICE=T('Полный тариф и условия отмены не опубликованы в прочитанном источнике; неизвестная сумма не ноль.',
 'Tarifa completa y condiciones de cancelación sin publicar en fuente leída; importe desconocido no es cero.')
UNKNOWN_AGE=T('Числовой возраст выбранного лагеря ещё подтвердить; возраст соседнего регулярного курса не перенесён автоматически.',
 'Confirmar edad numérica del campamento elegido; sin trasladar automáticamente edad de curso regular vecino.')
def B(i,slug,name,iso,place,themes,age):
 p=base('CP'+str(i),slug,name,iso,COUNTRIES[iso],place,themes);p.update(age=age,language=LANG,questions=[ACCESS])
 p['timing'].update(status='next_unannounced',label=T('Следующая точная смена и наличие мест ещё не объявлены.','Próxima sesión exacta y plazas aún sin anunciar.'))
 p['price'].update(year=None,label=UNKNOWN_PRICE,included=T('Включения, техника для занятий и kit домой требуют подтверждения.','Confirmar inclusiones, equipo de clase y kit para llevar.'),deposit=UNKNOWN_PRICE)
 return p
def fits(mat='conditional',osc='conditional',detail=ACCESS):return {k:candidate(v,detail) for k,v in [('matvey',mat),('oscar',osc)]}

REGIONS=[('totonicapan','Totonicapán'),('quetzaltenango','Quetzaltenango'),('quiche','Quiché'),('nebaj','Nebaj'),('suchitepequez','Suchitepéquez'),('retalhuleu','Retalhuleu'),('solola','Sololá')]
# Exact cells transcribed from the original 1920 px operator poster, not inferred weekdays.
MATRIX=[
 ('walls','Robot seguidor de paredes',1,'08:00','12:00',['03/11/2026','05/11/2026','24/11/2026','26/11/2026','10/11/2026','12/11/2026','17/11/2026']),
 ('obstacles','Robot evita obstáculos',1,'14:00','17:30',['03/11/2026','05/11/2026','24/11/2026','26/11/2026','10/11/2026','12/11/2026','17/11/2026']),
 ('light','Robot seguidor de luz',1,'08:00','12:00',['10/11/2026','12/11/2026','03/11/2026','05/11/2026','17/11/2026','19/11/2026','24/11/2026']),
 ('button','Robot push button control',1,'14:00','17:30',['10/11/2026','12/11/2026','03/11/2026','05/11/2026','17/11/2026','26/11/2026','24/11/2026']),
 ('coding','First coding',2,'08:00','12:00',['24/11/2026','26/11/2026','17/11/2026','19/11/2026','03/11/2026','05/11/2026','10/11/2026']),
 ('pneumatics','Stem pneumatics',2,'14:00','17:30',['24/11/2026','26/11/2026','17/11/2026','19/11/2026','03/11/2026','05/11/2026','10/11/2026']),
 ('mechanics','Stem mechanic 2.0',2,'08:00','12:00',['17/11/2026','19/12/2026','10/11/2026','12/11/2026','24/11/2026','26/11/2026','03/11/2026']),
 ('electronics','Stem electronics',2,'14:00','17:30',['17/11/2026','19/12/2026','10/11/2026','12/11/2026','24/11/2026','26/11/2026','03/11/2026'])]
def native_cells():
 out=[]
 for key,name,level,begin,finish,dates in MATRIX:
  for (region,place),value in zip(REGIONS,dates):
   day,month,year=value.split('/');date=year+'-'+month+'-'+day
   out.append(dict(project=key,name=name,level=level,region=region,place=place,reported_date=date,start_time=begin,end_time=finish,timezone='America/Guatemala',min_age=8 if level==1 else 11,max_age=10 if level==1 else 14,status='conflict-with-November-window' if month=='12' else 'published-poster-cell',source=POSTER))
 return out

def make_profiles():
 out=[]
 for i,level,ages in [(1251,1,'8–10'),(1252,2,'11–14')]:
  p=B(i,'cosami-robotics-level'+str(level),'COSAMI · Robótica Educativa · Nivel '+str(level),'GTM','Aulas COSAMI · 7 '+T('регионов, адреса уточнить','regiones, confirmar direcciones'),['robotics','coding','engineering'],ages)
  p['programme']=T('Практические проекты по отдельным датам: следование стене, объезд препятствий, следование свету и управление кнопкой для Nivel 1; First coding, pneumatics, mechanics и electronics для Nivel 2. Это выбор отдельных занятий, не ежедневный полный день в течение месяца.',
   'Proyectos prácticos en fechas separadas: seguir pared, evitar obstáculos, seguir luz y control por botón para Nivel 1; First coding, pneumatics, mechanics y electronics para Nivel 2. Selección de clases individuales, no jornada completa diaria durante un mes.')
  p['timing'].update(status='published_2026',label=T('Объявлен период 3–26 ноября 2026. Оригинальный плакат содержит семь регионов и восемь проектов; каждому соответствует отдельный день и утренний либо дневной блок. Две ячейки Quetzaltenango показывают 19 декабря вопреки ноябрьскому периоду: оставлены на уточнение без календарной даты. Набор уже начался, поздний вход не подтверждён.',
   'Periodo anunciado 3–26 de noviembre de 2026. Póster original contiene siete regiones y ocho proyectos; cada uno tiene día separado y bloque matutino o vespertino. Dos celdas de Quetzaltenango dicen 19 de diciembre contra periodo de noviembre: pendientes de aclaración sin fecha de calendario. Convocatoria ya iniciada, incorporación tardía sin confirmar.'))
  p['price'].update(year=2026,currency='GTQ',amount=0,unit='workshop',label=T('Обучение объявлено GRATIS. Это нулевой учебный взнос, не бесплатная поездка семьи; условия иностранного / неассоциированного приёма не установлены.',
   'Enseñanza anunciada GRATIS. Cuota académica cero, no viaje familiar gratuito; admisión extranjera / no asociada sin establecer.'))
  p['family_fit']=fits('candidate' if level==1 else 'later','later',T('Nivel 1: Матвей 9 входит в 8–10; Оскар 6 младше минимума 8. Nivel 2 11–14 пока не подходит обоим. Членство, документы, конкретная группа и язык отдельно; публичная Microsoft форма показала только Loading.',
   'Nivel 1: Matvey de 9 cumple 8–10; Oscar de 6 menor del mínimo 8. Nivel 2 de 11–14 aún no corresponde a ninguno. Membresía, documentos, grupo concreto e idioma aparte; formulario público Microsoft solo mostró Loading.'))
  p['sources']=[source('Cursos Vacacionales 2026 · ages / free tuition',COS),source('Original project × region × day timetable',POSTER),source('Linked public form · fields unavailable',FORM)]
  p['programme_type']='holiday_workshop';p['catalog_participation']='holiday_workshop'
  for c in native_cells():
   if c['level']!=level or c['status']!='published-poster-cell':continue
   add(p,c['reported_date'],c['reported_date'],c['region']+'-'+c['project'],c['place']+' · '+c['name'],'GRATIS',POSTER,days=[c['reported_date']],begin=c['start_time'],finish=c['end_time'],zone=c['timezone'],place='COSAMI · '+c['place']+' · '+T('точный адрес уточнить','confirmar dirección exacta'),admission_kind='unknown')
  out.append(p)
 for i,slug,name,age,start,end,days,place,blocks in [
  (1253,'munitec-37','MuniTec 3/7 · Tec Camp','10–14','2026-11-03','2026-11-26',[1,3],'39 calle 10-70, zona 3 · Ciudad de Guatemala',[('am','09:00','12:00'),('pm','14:00','17:00')]),
  (1254,'munitec-21-junior','MuniTec 21 · Tec Camp Junior','10–14','2026-11-04','2026-11-27',[2,4],'4.ª avenida y 6.ª calle, zona 21 · Ciudad de Guatemala',[('am','09:00','12:00')]),
  (1255,'munitec-21-teen','MuniTec 21 · Tec Camp Teen','15–17','2026-11-04','2026-11-27',[2,4],'4.ª avenida y 6.ª calle, zona 21 · Ciudad de Guatemala',[('am','09:00','12:00')])]:
  p=B(i,slug,name,'GTM',place,['robotics','coding','engineering'],age)
  p['programme']=T('Программирование, робототехника и 3D-печать в четырёхнедельном муниципальном каникулярном курсе. Требуются свидетельство о рождении, DPI ответственного взрослого и счёт за услуги с адресом в municipio de Guatemala. Отдельный иностранный доступ не подтверждён.',
   'Programación, robótica e impresión 3D en curso municipal vacacional de cuatro semanas. Exige certificado de nacimiento, DPI del adulto responsable y recibo de servicios con dirección en municipio de Guatemala. Acceso extranjero separado sin confirmar.')
  p['timing'].update(status='published_2026',label=T('Начало 3 либо 4 ноября 2026 и четыре недели дважды в неделю опубликованы пресс-службой. Последние дни рассчитаны по этому правилу, а не отдельной дате окончания; присоединение после начала не подтверждено.',
   'Prensa publica inicio 3 o 4 de noviembre de 2026 y cuatro semanas dos veces por semana. Últimos días calculados con esa regla, no fecha de cierre separada; incorporación tras inicio sin confirmar.'))
  p['family_fit']=fits('later','later',T('Оба младше опубликованной возрастной группы; муниципальный адрес и документы также обязательны. Это резерв более позднего возраста.',
   'Ambos menores del grupo de edad publicado; dirección municipal y documentos también obligatorios. Alternativa para edad posterior.'))
  p['sources']=[source('Municipal press · starts, weekdays, ages and documents',MUNI)]
  for key,begin,finish in blocks:add(p,start,end,key,name+' · '+key,UNKNOWN_PRICE,MUNI,days=[d for d in weekdays(start,end) if __import__('datetime').date.fromisoformat(d).weekday() in days],begin=begin,finish=finish,zone='America/Guatemala',admission_kind='unknown',entry=p['programme']+' '+ACCESS,date_precision='published_rule',date_rule=p['timing']['label'])
  p['programme_type']='holiday_workshop';p['catalog_participation']='holiday_workshop';out.append(p)
 p=B(1256,'cajamag-robotics-december','Cajamag · Vacacional de Robótica 12 horas','COL','Santa Marta · Av. del Libertador #19–97',['robotics','coding'],T('Описание 5–17; системное поле 14–99 — конфликт.','Descripción 5–17; campo de sistema 14–99: conflicto.'))
 p['programme']=T('Короткий курс робототехники общей длительностью 12 часов. Описание указывает будни 14:00–17:00, но конкретные четыре учебных дня не опубликованы. Окно витрины 1–31 декабря 08:00–18:00 не означает ежедневные занятия весь месяц.',
  'Curso breve de robótica de 12 horas totales. Descripción indica días laborables 14:00–17:00, sin publicar cuatro días lectivos concretos. Ventana de catálogo 1–31 de diciembre 08:00–18:00 no implica clases diarias todo el mes.')
 p['timing'].update(status='partial_2026',label=T('Декабрь 2026; точные учебные дни и конфликт возрастного поля требуют подтверждения. Окно 1–31 декабря сохранено в доказательствах, без операционной календарной смены.',
  'Diciembre de 2026; confirmar días lectivos exactos y conflicto de edad. Ventana 1–31 de diciembre conservada en evidencias, sin sesión operativa de calendario.'))
 p['price'].update(year=2026,currency='',amount=None,label=T('Показаны категории A $27600, B $31100, C $69000, D $76000. Код валюты прямо не установлен в прочитанной карточке; льготную категорию семьи и единицу тарифа подтвердить. Цена A не применена автоматически.',
  'Muestra categorías A $27600, B $31100, C $69000, D $76000. Código de moneda sin establecer expresamente en ficha leída; confirmar categoría familiar y unidad de tarifa. Sin aplicar automáticamente precio A.'))
 p['sources']=[source('Own market listing · conflicting ages and category fees',CAJA)];p['programme_type']='holiday_workshop';out.append(p)
 p=B(1257,'cultivatec-winter-online','Cultivatec · Robotics Winter Camp online','MEX',T('Онлайн · часовой пояс не объявлен','En línea · zona horaria sin anunciar'),['robotics','coding','engineering'],'10–13')
 p['formats']=['online'];p['catalog_participation']='online_camp';p['accommodation']=T('Дома через браузер; это онлайн-курс, не пансион.','Desde casa con navegador; curso en línea, sin residencia.')
 p['programme']=T('Tinkercad: 3D-механизмы, виртуальные схемы, программирование и автоматизация. Пять суббот по два часа, всего десять часов; покупать электронные компоненты не требуется по описанию. Требования компьютера, подключения и уровень отдельно.',
  'Tinkercad: mecanismos 3D, circuitos virtuales, programación y automatización. Cinco sábados de dos horas, diez horas totales; descripción no exige comprar componentes electrónicos. Ordenador, conexión y nivel aparte.')
 p['timing']['label']=T('Написано 19 декабря–23 января без года, часов и часового пояса. В возможном сезоне 2026–2027 это шесть календарных суббот против пяти занятий: пропуск не указан. Год не выведен из copyright; датированные занятия не созданы.',
  'Indica 19 de diciembre–23 de enero sin año, horario ni zona horaria. Posible temporada 2026–2027 contiene seis sábados frente a cinco clases: sin indicar omisión. Sin deducir año del copyright ni crear clases fechadas.')
 p['price'].update(currency='MXN',amount=1599,unit='programme',label=T('MXN 1599 за объявленный курс; год, налоги, способы оплаты и возврат подтвердить.',
  'MXN 1599 por curso anunciado; confirmar año, impuestos, pagos y devolución.'))
 p['family_fit']=fits('later','later',T('Сейчас 9 и 6, оба ниже минимума 10. Для будущего Матвея сначала установить год курса и возраст в день старта.',
  'Actualmente 9 y 6, ambos menores del mínimo 10. Para Matvey futuro primero establecer año del curso y edad al inicio.'))
 p['sources']=[source('Specific winter course / five sessions / MXN',CULT),source('Operator and separate school courses','https://cultivatec.com.mx/')];out.append(p)
 for i,regular in [(1258,False),(1259,True)]:
  p=B(i,'robotiki-constructores' if regular else 'robotiki-holiday-camps','Robotiki · '+('Constructores' if regular else 'Colonias tecnológicas'),'ARG',T('Buenos Aires · площадку уточнить','Buenos Aires · confirmar sede elegida'),['robotics','coding','engineering'], '6–10' if regular else UNKNOWN_AGE)
  p['programme']=T('LEGO Education, программирование, электроника, первые 3D и AI проекты. Для каникул объявлены полный / неполный день и Zona Activa Belgrano либо партнёрские площадки; footer указывает офис Vicente López, это не автоматически площадка лагеря. Constructores — отдельный регулярный начальный курс 6–10.',
   'LEGO Education, programación, electrónica y primeros proyectos 3D y AI. Para vacaciones anuncia jornada completa / media jornada en Zona Activa Belgrano o sedes asociadas; footer indica oficina Vicente López, no sede automática de campamento. Constructores es curso regular inicial separado de 6–10.')
  if regular:p['programme_type']='regular_learning';p['catalog_participation']='regular';p['family_fit']=fits('candidate','candidate',T('Оба входят в 6–10 регулярной группы. Это начальная программа: после трёх лет соревнований нужен подбор сложности; не подтверждённая возрастная группа лагеря.',
   'Ambos cumplen 6–10 del grupo regular. Programa inicial: tras tres años de competiciones exige ajustar dificultad; no grupo de edad de campamento confirmado.'))
  else:p['family_fit']=fits('unknown','unknown',UNKNOWN_AGE)
  p['sources']=[source('Holiday structure, no upcoming dates',ROBO+'campamentos-tecnologicos-vacaciones-caba'),source('Own regular group 6–10',ROBO+'sedes/para-constructores'),source('Operator / office and groups',ROBO)];out.append(p)
 for i,name,themes,programme in [(1260,'Titan Bot · VEX IQ',['robotics','coding','engineering'],T('Конструирование и программирование VEX IQ, сенсоры, передачи, логика и стратегия команды.','Diseño y programación VEX IQ, sensores, engranajes, lógica y estrategia de equipo.')),(1261,'Neural Ninja · AI Revolution',['ai','coding'],T('Модели, интеллектуальные решения, автоматизированные игры и собственные AI проекты.','Modelos, soluciones inteligentes, juegos automatizados y proyectos propios AI.')),(1262,'Studio Prime · Creator Lab',['art','technology'],T('Кино, podcast, монтаж, визуальный рассказ и производство цифрового контента.','Cine, podcast, edición, relato visual y producción de contenido digital.'))]:
  p=B(i,'vst-camp-'+str(i),'Villacampa · '+name,'DOM','Santo Domingo · '+T('архив ABC School, будущую площадку уточнить','archivo ABC School, confirmar sede futura'),themes,T('Общий camp 6–17, возраст конкретного трека отдельно.','Campamento general 6–17, edad de pista concreta aparte.'))
  p['programme']=programme;p['timing'].update(status='archive_next_unannounced',label=T('Архив: начало 22 июня 2026, пять недель Пн–Пт 09:00–14:00 в ABC School; набор закрыт. Новые даты и цена не опубликованы. Lista de interés не резервирует место и не создаёт оплату.',
   'Archivo: inicio 22 de junio de 2026, cinco semanas L–V 09:00–14:00 en ABC School; convocatoria cerrada. Sin fechas ni precio nuevos. Lista de interés no reserva plaza ni genera pago.'))
  p['price'].update(year=2026,currency='USD',amount=800,unit='programme',label=T('Архивная цена USD 800 за пять недель 2026; не тариф будущего сезона. Включения, материалы и отмена ещё согласуются.',
   'Precio archivado USD 800 por cinco semanas de 2026; no tarifa futura. Confirmar inclusiones, materiales y cancelación.'))
  p['sources']=[source('Own three closed camps and future watchlist',VST)];out.append(p)
 p=B(1263,'uvm-poweron','UVM · POWER ON · Inglés Básico + Robótica','VEN','Trujillo · sede Estovacuy',['robotics','languages','engineering'],UNKNOWN_AGE)
 p['programme']=T('Каникулярный курс базового английского и робототехники: лаборатории, 3D-модели и практические проекты. Английский — отдельный изучаемый предмет; язык объяснения робототехники не установлен.',
  'Curso vacacional de inglés básico y robótica: laboratorios, modelos 3D y proyectos prácticos. Inglés es asignatura de aprendizaje separada; idioma de explicación robótica sin establecer.')
 p.update(confirmed_instruction_languages=['EN'],language_evidence_role='language_lessons',language=p['programme'])
 p['family_fit']=fits('unknown','unknown',UNKNOWN_AGE)
 p['timing'].update(status='archive_next_unannounced',label=T('Университет сообщил о начавшемся курсе 12 августа 2026. Дата новости не дата следующего старта; длительность, числовой возраст и сезон 2027 ещё не установлены.',
  'Universidad informó de curso iniciado el 12 de agosto de 2026. Fecha de noticia no es próximo inicio; duración, edad numérica y temporada 2027 sin establecer.'))
 p['sources']=[source('University report · English as a subject plus robotics',UVM)];out.append(p)
 p=B(1264,'utp-labsi-summer','UTP · LabSI Summer Camp de Robótica Básica','PAN','Campus Metropolitano Dr. Víctor Levi Sasso · '+T('площадку следующего курса уточнить','confirmar sede de próximo curso'),['robotics','coding','engineering'],UNKNOWN_AGE)
 p['programme']=T('Архивный университетский курс: 20 академических часов, программирование, сенсоры, актуаторы и финальный проект. Успешным участникам выдавали возрастные kits; это не подтверждает включение kit в будущую неизвестную цену. Академический час не приравнен автоматически к 60 минутам.',
  'Curso universitario archivado: 20 horas académicas, programación, sensores, actuadores y proyecto final. Participantes que completaron recibieron kits por edad; no confirma kit incluido en futura tarifa desconocida. Sin equiparar automáticamente hora académica a 60 minutos.')
 p['timing'].update(status='archive_next_unannounced',label=T('Отчёт 24 марта 2026 сообщает о завершении; конкретные прошлые дни и будущая дата не объявлены. Двуязычная статья не доказывает английский учебный поток.',
  'Informe de 24 de marzo de 2026 comunica finalización; sin días pasados concretos ni fecha futura. Artículo bilingüe no acredita grupo docente en inglés.'))
 p['sources']=[source('University laboratory completion report · no future intake',UTP)];out.append(p)
 p['family_fit']=fits('unknown','unknown',UNKNOWN_AGE)
 assert len(out)==14
 return out

def update_report(report):
 rows=make_profiles();index={p['id']:p for p in rows};old={p['id'] for p in report['profiles']}
 report['profiles']=[index.get(p['id'],p) for p in report['profiles']]+[p for p in rows if p['id'] not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso'] for p in report['profiles']}),by_status=dict(Counter(p['timing']['status'] for p in report['profiles'])),source_urls=len({s['url'] for p in report['profiles'] for s in p['sources']}))
 report['countries']=[dict(country=c,count=n) for c,n in sorted(Counter(p['country'] for p in report['profiles']).items())];report.update(version=161,asof=CHECKED)

def enrich_v161(d):
 offer=dict(id='cosami-matvey-light-totonicapan-2026',slug='cosami-robotics-level1',label=T('COSAMI · Матвей · световой робот · Totonicapán 10 ноября','COSAMI · Matvey · robot de luz · Totonicapán 10 de noviembre'),currency='GTQ',price_year=2026,format='day',children=['matvey'],base_by_child={'matvey':0},discount_second=0,required=[],unknown_required=[dict(id='food_materials',unit='money',rate=1,min=0,label=T('Питание, выдача kit домой и неуказанные обязательные расходы','Comida, kit para llevar y costes obligatorios no indicados'))],optional=[],unknown_trip=['travel','lodging','misc'],sessions=[['2026-11-10','2026-11-10']],sources=[COS,POSTER,FORM],checked=CHECKED,gate=T('Только Матвей 8–10; Оскар 6 ниже минимума. Плакат 10 ноября 08:00–12:00, адрес, иностранный / неассоциированный приём и язык уточнить. Нулевая опубликованная стоимость обучения не полная стоимость поездки.',
  'Solo Matvey 8–10; Oscar de 6 menor del mínimo. Póster 10 de noviembre 08:00–12:00; confirmar dirección, admisión extranjera / no asociada e idioma. Precio académico publicado cero no es coste completo de viaje.'),included=T('Объявленное бесплатное обучение одному выбранному проекту.','Enseñanza gratuita anunciada de un proyecto elegido.'),deposit_note=UNKNOWN_PRICE,scope=ACCESS)
 offers=d['camp_planning']['offers'];d['camp_planning']['offers']=[o for o in offers if o['id']!=offer['id']]+[offer];d['camp_planning'].update(version=161,checked=CHECKED)
