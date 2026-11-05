"""Chilean holiday robotics options, grade-based university courses and explicit gaps."""
from copy import deepcopy
from collections import Counter
from camp_europe_v148 import lesson,weekdays
CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
SUMMER='https://techlabkids.cl/producto/taller-vacaciones-de-verano-2027/'
CHRISTMAS='https://techlabkids.cl/producto/taller-vacaciones-de-navidad-2026/'
TERMS='https://techlabkids.cl/politica-reserva-descuentos-cancelaciones-devoluciones/'
HOLIDAYS='https://csigo.cancilleria.gob.ar/es/feriados-2026-1'
ROBOT='https://www.edv.uchile.cl/portfolio/exploradores-de-la-robotica-descubre-construye-y-aprende-como-funcionan-las-maquinas-del-futuro-2/'
SCRATCH='https://www.edv.uchile.cl/portfolio/desarrollando-el-pensamiento-computacional-en-scratch-5/'
EDV='https://www.edv.uchile.cl/postulacion-y-matricula/'
PDF='https://docs.google.com/document/d/1vvsr32wCL_eEGvxHbalL21-PxyPoh9Eb/export?format=pdf'
PROGRAMABLE='https://programable.com.ar/colonia-tecno-2027/'
WEEKS=[('2026-12-07','2026-12-11','Human Evolution'),('2026-12-14','2026-12-18','EVO BOTS'),('2027-01-04','2027-01-08','A · Earth'),('2027-01-11','2027-01-15','B · Ocean'),('2027-01-18','2027-01-22','C · Space'),('2027-01-25','2027-01-29','A · Earth'),('2027-02-01','2027-02-05','B · Ocean'),('2027-02-08','2027-02-12','C · Space'),('2027-02-15','2027-02-19','A · Earth'),('2027-02-22','2027-02-26','B · Ocean')]
LANG=T('Сайт и учебное описание по-испански; отдельного прямого подтверждения языка преподавания ES или EN не найдено. До ответа организатора не включать в фильтр подтверждённого EN/ES преподавания.',
       'Web y descripción académica en español; sin localizar confirmación expresa separada de enseñanza en ES o EN. Hasta respuesta del organizador no incluir en filtro de enseñanza EN/ES confirmada.')
TECH_TERMS=T('Приём до заполнения, оплата 100% либо резерв 50% с остатком не позднее 15 дней до старта; это срок остатка, не дедлайн регистрации. Общая политика: отмена письменно; за 7 и более календарных дней возврат 75% либо ваучер полной оплаченной суммы на год; менее 7 дней без возврата, медицинские исключения отдельно. После старта / no-show возврата нет, документированная невозможность посещать может давать 75%. При недоборе отменяет организатор с возвратом взноса, без иной компенсации. Согласие не давалось.',
 'Admisión hasta llenar plazas, pago 100% o reserva 50% con saldo como máximo 15 días antes de inicio; plazo del saldo, no de inscripción. Política general: cancelación escrita; con 7 o más días naturales devolución 75% o vale del total pagado por un año; menos de 7 días sin devolución, salvo excepciones médicas. Tras inicio / no-show sin devolución, imposibilidad justificada documentalmente puede dar 75%. Si falta mínimo cancela organizador y devuelve cuota, sin otra compensación. Sin dar consentimiento.')
DISCOUNT=T('Объявлена скидка 5%: братьям/сёстрам либо за две и более недели одним заказом. Основания не складываются. Общая политика запрещает накопление скидок; рождественская карточка исключает отдельные дни и рассрочку. Базу скидки, распределение между детьми и совместимость с резервом 50% подтвердить в счёте; в семейных сметах оставлена полная цена.',
 'Anunciado 5%: hermanos o dos o más semanas en mismo pedido. No acumular ambos motivos. Política general no acumula descuentos; Navidad excluye días sueltos y pagos en cuotas. Base, reparto entre hermanos y compatibilidad con reserva 50% deben figurar en invoice; presupuestos conservan tarifa íntegra.')
PRICE_LIST=T('CLP на ребёнка за неделю: 09:00–13:00 115000; 09:00–14:00 175000; 09:00–16:00 195000; 09:00–18:00 250000; 14:00–18:00 120000. Обед включён только в три плана 09:00–14:00 / 16:00 / 18:00. Отдельные дни от CLP 25000 требуют расчёта; эта минимальная цена не задаёт даты и полную стоимость выбранного дня.',
 'CLP por niño / semana: 09:00–13:00 115000; 09:00–14:00 175000; 09:00–16:00 195000; 09:00–18:00 250000; 14:00–18:00 120000. Almuerzo incluido solo en tres planes 09:00–14:00 / 16:00 / 18:00. Días sueltos desde CLP 25000 requieren presupuesto; sin inventar fechas ni total con esa tarifa mínima.')
HOLIDAY_GAP=T('7–11 декабря — опубликованная неделя, но 8 декабря 2026 официальный праздник Чили. Отдельное подтверждение работы во вторник не найдено: неделя показана окном, без выдуманных ежедневных часов и без заявления, что лагерь закрыт. Согласовать фактические дни и цену этой недели.',
 '7–11 de diciembre es semana publicada, pero el 8 de diciembre de 2026 es feriado oficial chileno. Sin confirmación separada de apertura el martes: semana mostrada como periodo, sin horas diarias inventadas ni afirmar cierre. Acordar días efectivos y precio de esa semana.')
EDV_TERMS=T('Конкурсный приём по годовым оценкам без вступительного теста; максимум три курса без пересечения. Обязателен требуемый класс: заявка не своего уровня аннулируется. Для этих карточек нужен 5°/6° в 2026 и certificado anual 2025. Правила для не-MINEDUC школ и возвращавшихся из-за рубежа не доказывают приём впервые прибывших иностранцев. После отбора WebPay. Общая страница всё ещё упоминает результаты 11 июня без подходящего сезона — не переносить это в 2027 дедлайн. Возврат только по исключительной причине до начала, удерживают 20%; запрос не позднее 5 рабочих дней до старта, обработка не менее 15 рабочих дней. Актуальность к выбранному лету и иностранный invoice уточнить.',
 'Admisión selectiva por notas anuales sin prueba; máximo tres cursos sin solaparse. Nivel exigido obligatorio: solicitud de otro nivel anulada. Estas fichas exigen 5°/6° en 2026 y certificado anual 2025. Reglas para escuelas no MINEDUC y quienes regresaron del extranjero no prueban admisión de extranjeros recién llegados. Tras selección WebPay. Página general aún menciona resultados el 11 de junio sin temporada adecuada: no convertir en plazo de 2027. Devolución solo excepcional antes de inicio, retienen 20%; pedir como máximo 5 días hábiles antes, tramitación al menos 15 días hábiles. Confirmar vigencia para verano elegido y factura extranjera.')
def source(title,url):return dict(title=title,url=url,checked=CHECKED)
def merge(p,rows):p['sources']=list({s['url']:s for s in p['sources']+rows}.values())
def profile(ident,slug,provider,age,themes,programme,fit):
 return dict(id=ident,slug=slug,provider=provider,country=T('Чили','Chile'),iso='CHL',place='Vitacura · Santiago',themes=themes,formats=['day'],age=age,language=LANG,confirmed_instruction_languages=[],language_evidence_role='unconfirmed',programme=programme,
  timing=dict(status='published_2026_27',label=T('Две рождественские недели декабря 2026 и восемь недель января–февраля 2027. Утро и день — разные выбираемые блоки; три расширенных тарифа присмотра приведены в прайсе, не отдельные независимые лагеря.',
   'Dos semanas navideñas de diciembre de 2026 y ocho semanas de enero–febrero de 2027. Mañana y tarde son bloques elegibles distintos; tres tarifas ampliadas de cuidado figuran en precios, sin ser campamentos independientes.'),sessions=[],session_details=[]),
  price=dict(year=2027,currency='CLP',amount=None,unit='week',label=PRICE_LIST,included=T('Киты и notebooks лаборатории включены, свой компьютер по желанию. Предыдущая подготовка не требуется; после трёх лет соревнований уровень группы согласовать.',
   'Kits y notebooks de laboratorio incluidos, ordenador propio opcional. Sin experiencia previa exigida; tras tres años de competiciones acordar nivel del grupo.'),extras=T('Перекусы, вода, шляпа и солнцезащита с собой; парковка платная. Родители не могут ждать в помещении. Договор предусматривает выход в парк в двух кварталах; условия сопровождения согласовать до согласия. Жильё и поездка семьи отдельно.',
   'Llevar colaciones, agua, gorro y protección solar; aparcamiento de pago. Padres no pueden esperar dentro. Contrato contempla salida al parque a dos cuadras; acordar acompañamiento antes de consentir. Alojamiento y viaje familiar aparte.'),deposit=TECH_TERMS+' '+DISCOUNT),
  accommodation=T('Дневной лабораторный центр Av. Vitacura 3568, Oficina 611; пансион не предложен.',
   'Centro diurno de laboratorio Av. Vitacura 3568, Oficina 611; sin residencia ofrecida.'),family_fit=fit,editorial_reason=T('Точные близкие технические недели и раздельные возрастные группы для семейной поездки; международная победа не обещается.',
   'Semanas técnicas próximas con fechas exactas y grupos de edad separados para viaje familiar; sin prometer victoria internacional.'),shortlist=['technical'],questions=[LANG,HOLIDAY_GAP,DISCOUNT,T('Подтвердить индивидуальный иностранный приём, свободное место и подходящую сложность. Регистрация, оплата, согласие на прогулку и фото не выполнялись.',
   'Confirmar admisión extranjera individual, plaza y dificultad adecuada. Sin registro, pago ni consentimiento de paseo o fotos.')],sources=[source(T('Лето 2027 · 8 недель и полная таблица тарифов','Verano 2027 · 8 semanas y tabla completa de tarifas'),SUMMER),source(T('Рождество 2026 · две недели','Navidad 2026 · dos semanas'),CHRISTMAS),source(T('Правила оплаты, отмены и скидок','Reglas de pago, cancelación y descuentos'),TERMS),source(T('Официальный праздник 8 декабря 2026','Feriado oficial del 8 de diciembre de 2026'),HOLIDAYS)],checked=CHECKED)
def make_profiles():
 candidate=lambda text:dict(status='candidate',detail=text)
 later=lambda text:dict(status='later',detail=text)
 a=profile('CP1183','techlab-chile-kids-holidays','TechLab Kids Chile · Kids WeDo · Robotics AM',T('Kids 6–8; старшая группа 9–11 отдельно.','Kids 6–8; grupo mayor 9–11 separado.'),['robotics','coding'],T('Утро 09:00–13:00: основы робототехники на LEGO WeDo 2.0. Темы Earth / Ocean / Space циклически повторяются летом; это не восемь разных продвинутых уровней.',
 'Mañana 09:00–13:00: bases de robótica con LEGO WeDo 2.0. Temas Earth / Ocean / Space se repiten cíclicamente en verano; sin ser ocho niveles avanzados distintos.'),dict(matvey=dict(status='not_eligible',detail=T('Семья сообщила возраст Матвея 9 лет: Kids максимум 8, поэтому нужен отдельный Junior. В начале 2027 ему 9–10.',
 'Familia informó que Matvey tiene 9 años: Kids admite hasta 8, necesita Junior separado. A inicio de 2027 tiene 9–10.')),oscar=candidate(T('Семья сообщила возраст Оскара 6 лет: в декабре 2026 и начале 2027 диапазон 6–8 подходит.',
 'Familia informó que Oscar tiene 6 años: en diciembre de 2026 e inicio de 2027 cumple rango 6–8.'))))
 b=profile('CP1184','techlab-chile-junior-holidays','TechLab Kids Chile · Junior EV3 · Robotics AM',T('Junior 9–11; в тексте ниже также 9+, поэтому верхнюю границу отдельного EV3-потока согласовать.',
 'Junior 9–11; texto inferior también dice 9+, confirmar límite superior del grupo EV3 separado.'),['robotics','coding'],T('Утро 09:00–13:00: LEGO Mindstorms EV3, датчики и механизмы. Kids WeDo и Junior EV3 — разные возрастные группы одной площадки; дневной Scratch/MakeCode отдельный выбор.',
 'Mañana 09:00–13:00: LEGO Mindstorms EV3, sensores y mecanismos. Kids WeDo y Junior EV3 son grupos de edad distintos de una sede; Scratch/MakeCode de tarde se elige aparte.'),dict(matvey=candidate(T('Семья сообщила возраст Матвея 9 лет: декабрь 2026 и январь–февраль 2027 входят в Junior 9–11. Сложность после соревнований согласовать.',
 'Familia informó que Matvey tiene 9 años: diciembre de 2026 y enero–febrero de 2027 cumplen Junior 9–11. Acordar dificultad tras competiciones.')),oscar=later(T('Оскар ниже 9; доступен отдельный Kids 6–8.', 'Oscar menor de 9; existe Kids 6–8 separado.'))))
 c=profile('CP1185','techlab-chile-coding-afternoon','TechLab Kids Chile · Scratch / MakeCode · PM',T('Kids и Junior 6–11. В одном месте Navidad указано mayores de 6, в общей таблице 6–11: допуск ровно в 6 уточнить.',
 'Kids y Junior 6–11. Un apartado Navidad dice mayores de 6 y tabla general 6–11: confirmar admisión con exactamente 6.'),['coding','gaming'],T('День 14:00–18:00: логика видеоигр, Scratch и MakeCode для 6–11. Python / Roblox Studio относятся к отдельному 12+ Teens, не к этому детскому блоку. Обед в тариф дневного блока не заявлен.',
 'Tarde 14:00–18:00: lógica de videojuegos, Scratch y MakeCode para 6–11. Python / Roblox Studio pertenecen a Teens separado de 12+, no a este bloque infantil. Tarifa de tarde sin almuerzo anunciado.'),dict(matvey=candidate(T('Возраст Матвея по сообщению семьи 9; в начале 2027 ему 9–10, входит в 6–11. Сложность и место отдельно.',
 'Edad de Matvey informada por familia 9; a inicio de 2027 tiene 9–10, cumple 6–11. Dificultad y plaza aparte.')),oscar=dict(status='conditional',detail=T('Семья сообщила возраст Оскара 6 лет; в 2027 ему 6–7. Подтвердить противоречие 6–11 / mayores de 6 до признания допуска.',
 'Familia informó que Oscar tiene 6 años; en 2027 tiene 6–7. Confirmar conflicto 6–11 / mayores de 6 antes de dar admisión por confirmada.'))))
 for p in [a,b,c]:
  pm=p['id']=='CP1185';price=120000 if pm else 115000;p['price']['amount']=price
  for start,end,theme in WEEKS:
   fit=deepcopy(p['family_fit'])
   v=dict(start=start,end=end,label=theme+(' · Coding PM' if pm else ' · Robotics AM'),price='CLP '+str(price)+T(' / ребёнок / неделя',' / niño / semana'),source=SUMMER if start>='2027' else CHRISTMAS,formats=['day'],family_fit=fit,date_scope='session_days',proof=T('Неделя и блок опубликованы оператором; это варианты для выбора, не принятая заявка.',
       'Semana y bloque publicados por operador; opciones para elegir, no solicitud aceptada.'))
   if start=='2026-12-07':v.update(date_scope='camp_window',proof=HOLIDAY_GAP)
   else:v['sessions']=[lesson(day,'14:00' if pm else '09:00','18:00' if pm else '13:00','America/Santiago',p['programme']) for day in weekdays(start,end)]
   p['timing']['sessions'].append([start,end]);p['timing']['session_details'].append(v)
 out=[a,b,c]
 for ident,slug,title,url,robot in [('CP1186','uchile-edv-robotics-2027','Exploradores de la Robótica',ROBOT,True),('CP1187','uchile-edv-scratch-2027','Pensamiento Computacional en Scratch',SCRATCH,False)]:
  p=profile(ident,slug,'Universidad de Chile · EdV · '+title,T('Класс 5° или 6° Educación Básica во время 2026; это не возраст 5–6 лет.',
   'Cursando 5° o 6° Educación Básica durante 2026; no es edad de 5–6 años.'),['robotics','coding'] if robot else ['coding'],T('Очный университетский курс. Электроника / LED, HelloBlocks, Arduino, датчики, servomotors и итоговый проект. PDF содержит 5 сессий: 09:00–10:30 и 11:00–12:30; между ними перерыв. Диплом участия не международная медаль.',
   'Curso universitario presencial. Electrónica / LED, HelloBlocks, Arduino, sensores, servomotors y proyecto final. PDF contiene 5 sesiones: 09:00–10:30 y 11:00–12:30; pausa entre bloques. Diploma de participación no es medalla internacional.') if robot else T('Очный курс логики и вычислительного мышления в Scratch: декомпозиция, закономерности, последовательности и совместное решение задач. Присутствие 09:00–12:30 опубликовано, отдельное ежедневное содержание не дано.',
   'Curso presencial de lógica y pensamiento computacional en Scratch: descomposición, patrones, secuencias y resolución colaborativa. Horario 09:00–12:30 publicado, sin contenidos diarios separados.'),dict(matvey=dict(status='conditional',detail=T('Нужен действительный 5°/6° класс в 2026 и отбор по оценкам; год 2017 это не доказывает.',
   'Exige cursar realmente 5°/6° en 2026 y selección por notas; año 2017 no lo demuestra.')),oscar=later(T('Курс 5°/6° класса: для Оскара будущая ступень, действительный класс семьи неизвестен. Возраст не заменяет школьный документ.',
   'Curso de 5°/6°: etapa futura para Oscar, curso escolar real de familia desconocido. Edad no sustituye documento escolar.'))))
  p['place']='Beauchef 850 · Facultad de Ciencias Físicas y Matemáticas · Santiago';p['shortlist']=['technical']
  p['timing']=dict(status='published_2027',label=T('4–8 января 2027, 09:00–12:30; выборочное зачисление. Два курса идут одновременно, их нельзя выбрать вместе.',
   '4–8 de enero de 2027, 09:00–12:30; matrícula selectiva. Ambos cursos simultáneos, no se pueden elegir juntos.'),sessions=[['2027-01-04','2027-01-08']],session_details=[])
  v=dict(start='2027-01-04',end='2027-01-08',label=title,price='CLP 98000',source=url,formats=['day'],admission_kind='qualifier',entry=EDV_TERMS,date_scope='session_days' if robot else 'camp_session',proof=T('Карточка EdV сезона 2027: цена 98000 CLP, 50 мест — объявленный лимит, не live-остаток. Класс и документы обязательны.',
   'Ficha EdV de temporada 2027: precio 98000 CLP, 50 plazas es límite anunciado, no disponibilidad en vivo. Nivel y documentos obligatorios.'))
  if robot:v['sessions']=[lesson(day,'09:00','12:30','America/Santiago',T('Присутствие EdV: два блока по 90 минут и перерыв; не 3.5 часа непрерывного обучения.',
   'Presencia EdV: dos bloques de 90 minutos y pausa; no 3.5 horas de enseñanza continua.')) for day in weekdays(v['start'],v['end'])]
  p['timing']['session_details']=[v]
  p['price']=dict(year=2027,currency='CLP',amount=98000,unit='course',label=T('CLP 98000 за выбранный курс 4–8 января 2027; два курса в одно время не суммировать как совместный маршрут.',
   'CLP 98000 por curso elegido del 4–8 de enero de 2027; no sumar ambos simultáneos como itinerario conjunto.'),included=T('FAQ включает учебные материалы; тетрадь и ручка с собой. Право забрать киты домой не заявлено.',
   'FAQ incluye materiales académicos; llevar cuaderno y lápiz. Sin promesa de llevar kits a casa.'),extras=T('Питание, транспорт и жильё не включены; помощи с отелями нет. Приём иностранных документов, язык и refund подтвердить.',
   'Comida, transporte y alojamiento no incluidos; sin ayuda de hoteles. Confirmar documentos extranjeros, idioma y refund.'),deposit=EDV_TERMS)
  p['accommodation']=T('Дневные занятия в университете, не школа-пансион и не жилой лагерь.', 'Clases diurnas universitarias, sin ser colegio interno ni campamento residencial.')
  p['editorial_reason']=T('Чёткая университетская программа для будущего школьного уровня; текущий семейный допуск не установлен.',
   'Programa universitario claro para futuro nivel escolar; admisión familiar actual sin establecer.')
  p['questions']=[LANG,EDV_TERMS,T('Уточнить текущие даты подачи 2027, эквивалент иностранного класса, документы, сложность, свободные места и подтверждение зачисления. Регистрация не подана.',
   'Confirmar plazos actuales de 2027, equivalencia escolar extranjera, documentos, dificultad, plazas y aceptación. Sin solicitud presentada.')]
  p['sources']=[source(T('Карточка курса января 2027','Ficha de curso de enero de 2027'),url),source(T('Отбор, обязательный класс, стоимость материалов и возврат','Selección, nivel obligatorio, materiales y devolución'),EDV)]
  if robot:p['sources'].append(source(T('Связанный учебный PDF · пять сессий','PDF académico enlazado · cinco sesiones'),PDF))
  out.append(p)
 return out

def update_report(r):
 profiles={p['id']:p for p in r['profiles']}
 p=profiles['CP046'];p['checked']=CHECKED
 merge(p,[source(T('Colonia 2027 · повторно проверены недели и ARS 95000','Colonia 2027 · semanas y ARS 95000 revisados otra vez'),PROGRAMABLE)])
 for ident,url in [('CP309','https://www.wecode.edu.uy/cursos/lab-pocitos'),('CP310','https://www.wecode.edu.uy/cursos/ia-pocitos'),('CP311','https://www.wecode.edu.uy/cursos/minecraft1-pocitos')]:
  p=profiles[ident];p['checked']=CHECKED
  p['timing']['label']=T('Перепроверено 5 ноября: текущая летняя страница всё ещё явно Feb 2026 и классы в 2026. Даты 2027 не объявлены; это архивный курс / ожидание следующего набора. Не переносить недельные встречи и цены в новый сезон.',
   'Revisado el 5 de noviembre: página estival actual aún dice expresamente Feb 2026 y niveles de 2026. Fechas de 2027 sin anunciar; curso de archivo / próximo periodo pendiente. No trasladar encuentros ni precios a nueva temporada.')
  merge(p,[source(T('Текущая карточка старого летнего набора','Ficha actual de periodo estival antiguo'),url),source(T('Летняя страница с явным 2026','Página estival con 2026 expreso'),'https://www.wecode.edu.uy/verano')])
 new=make_profiles();index={p['id']:p for p in new};old={p['id'] for p in r['profiles']}
 r['profiles']=[index.get(p['id'],p) for p in r['profiles']]+[p for p in new if p['id'] not in old]
 r['counts'].update(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))
 counts=Counter(p['country'] for p in r['profiles'])
 for item in r['countries']:item['count']=counts[item['country']]
 r.update(version=155,asof=CHECKED)

def enrich_v155(d):
 rows={e['id']:e for e in d['events']};e=rows['L033']
 e.update(age=T('Kids 6–8, Junior 9–11; отдельные Infant 3–5 и Teens 12+ не смешивать с младшими треками.',
  'Kids 6–8, Junior 9–11; Infant 3–5 y Teens 12+ separados sin mezclarlos con cursos menores.'),language=LANG,languages=[],language_mode='unconfirmed',title=T('TechLab Kids Chile · действующие каникулярные треки 2026–27','TechLab Kids Chile · programas vacacionales vigentes de 2026–27'),source=SUMMER,checked=CHECKED,
  period=T('Декабрь 2026 и январь–февраль 2027: точные варианты в связанных досье Kids / Junior / Tardes Tech. Это обзор оператора, не дополнительная самостоятельная смена.',
   'Diciembre de 2026 y enero–febrero de 2027: opciones exactas en fichas Kids / Junior / Tardes Tech enlazadas. Resumen de operador, no sesión independiente adicional.'),cost=PRICE_LIST,
  note=LANG+' '+HOLIDAY_GAP,related_ids=[e['id'] for e in d['events'] if e.get('camp_programme_id') in ['CP1183','CP1184','CP1185']])
 offers=d['camp_planning']['offers'];new=[]
 for key,label,amount,end,lunch in [('am','Robotics AM',115000,'13:00',False),('lunch','AM + Lunch',175000,'14:00',True),('extended','AM + Extended',195000,'16:00',True),('full','Full Day',250000,'18:00',True),('pm','Coding PM',120000,'18:00',False)]:
  new.append(dict(id='techlab-chile-both-'+key+'-2026-27',slug='techlab-chile-coding-afternoon' if key=='pm' else 'techlab-chile-junior-holidays',label='TechLab Chile · '+label+' · '+T('оба ребёнка / одна неделя','ambos niños / una semana'),currency='CLP',price_year=2027,format='day',children=['matvey','oscar'],base_by_child=dict(matvey=amount,oscar=amount),discount_second=0,required=[],unknown_required=[],optional=[],unknown_trip=['travel','lodging','misc'],sessions=[[a,b] for a,b,_ in WEEKS],sources=[SUMMER,CHRISTMAS,TERMS],checked=CHECKED,
   gate=T('Семья указала возраст Матвея 9 и Оскара 6: утром Junior и Kids — разные группы. После полудня для ровно 6 есть противоречивые формулировки. Язык, международный индивидуальный приём и место не подтверждены.',
    'Familia indicó edades de Matvey 9 y Oscar 6: Junior y Kids son grupos matinales distintos. Por la tarde existe formulaciones contradictorias para exactamente 6. Idioma, admisión internacional individual y plaza sin confirmar.'),deposit_note=TECH_TERMS+' '+DISCOUNT,included=T('Киты и лабораторные notebooks; обед только когда выбранный план его включает.',
    'Kits y notebooks de laboratorio; almuerzo solo cuando plan elegido lo incluye.'),scope=('14:00' if key=='pm' else '09:00')+'–'+end+'; '+(T('Обед включён. ','Almuerzo incluido. ') if lunch else T('Обед не включён. ','Almuerzo no incluido. '))+T('Опубликованная база за двоих без автоматической скидки 5%. Расширенный тариф не новая независимая программа. Точные дни первой декабрьской недели и invoice согласовать; уход за детьми вне часов, жильё взрослых и перелёты отдельно.',
    'Base publicada de ambos sin descuento automático de 5%. Tarifa ampliada no es programa independiente nuevo. Acordar días efectivos de primera semana de diciembre y factura; cuidado fuera de horario, alojamiento adulto y vuelos aparte.')))
 index={o['id']:o for o in new};old={o['id'] for o in offers};d['camp_planning']['offers']=[index.get(o['id'],o) for o in offers]+[o for o in new if o['id'] not in old]
 d['camp_planning'].update(version=155,asof=CHECKED)
