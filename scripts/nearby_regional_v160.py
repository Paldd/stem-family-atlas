"""Current local FIRST entry, regional operators and explicit next-season watches."""
from copy import deepcopy

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es):SPANISH[ru]=es;return ru
FLL='https://fundacionsteam.org/cmsevents/festival-nacional-de-robotica/'
PRICE='https://fundacionsteam.org/wp-content/uploads/2020/08/Precios-FLL-2027-1024x1024.png'
EXPLORE='https://drive.google.com/file/d/1fA4qSCYD0jrZjhTzPdUMJPcqZGOmub_y/view'
CHALLENGE='https://drive.google.com/file/d/1VCOn0NAPr1lR45w7GA9zzq6o5bW9uvMT/view'
NET='https://somosgrupora.com/torneo-robotica/'
NET_PDF='https://somosgrupora.com/assets/docs/reglamento-'
ACA='https://academiastem.org/championships/'
ACA_API='https://dobot.com.mx/api-dis/api/tournaments'
BLAST='https://sites.google.com/tec.mx/roboblasters/inicio'
FIRE='https://federacionfire.org/'
RCJ='https://robocupamericas.org/es/'
GUEST=RCJ+'new-country/'
PAN='https://www.eduvisionpnm.com/challenge/'
PAN_PDF=PAN+'assets/pdf/reglamento-'
LANG=T('Испанские страницы / документы прочитаны; язык очного судейства, интервью и возможность EN / ES для выбранной команды прямо не подтверждены. Язык сайта не является языком допуска.',
 'Leídas páginas / documentos en español; idioma de arbitraje presencial, entrevistas y posibilidad EN / ES para equipo elegido sin confirmar expresamente. Idioma de web no acredita idioma de admisión.')
GATE=T('Точный класс, дата рождения, состав, школьное / клубное представительство, иностранный приём и наличие мест подтвердить по выбранной категории. Форма, согласия и оплата не отправлялись.',
 'Confirmar curso real, fecha de nacimiento, composición, representación escolar / de club, admisión extranjera y plazas por categoría elegida. Sin enviar formulario, consentimientos ni pago.')
AWARD=T('Место или конкурсная награда только по официальному протоколу. Сертификат, медаль участника и институциональная аккредитация не доказывают международную победу.',
 'Puesto o premio competitivo solo según acta oficial. Certificado, medalla de participación y acreditación institucional no prueban victoria internacional.')

def ref(label,url):return dict(label=label,url=url)
def src(label,url):return dict(title=label,url=url,checked=CHECKED)
def event(ident,title,country,source,start='',end='',**fields):
 geo={'Коста-Рика':('CRI','Центральная Америка'),'Мексика':('MEX','Северная Америка'),'Эквадор':('ECU','Южная Америка'),'Панама':('PAN','Центральная Америка')}
 iso,region=geo.get(country,('','Глобально'))
 e=dict(id=ident,block='Соревнования',title=title,country=country,region=region,city='',start=start,end=end,
  period='',date_status='Подтверждено' if start else 'Не объявлено',deadline='',age='',mat='Условно',osc='Условно',
  format=T('Команда; точный состав по регламенту категории.','Equipo; composición exacta según reglamento de categoría.'),
  entry=GATE,gear=T('Комплект и технический регламент выбранной категории уточнить.','Confirmar kit y reglamento técnico de categoría elegida.'),
  language=LANG,cost=T('Тариф выбранного этапа и итоговый invoice не установлены; неизвестное не считается нулём.',
   'Tarifa de etapa elegida e invoice final sin establecer; desconocido no equivale a cero.'),level=T('C — региональный / местный маршрут','C — ruta regional / local'),reward=AWARD,
  priority=T('P3 — условия подтвердить','P3 — confirmar condiciones'),action=GATE,source=source,proof=T('Прочитан официальный источник; неизвестные условия сохранены явно.',
   'Fuente oficial leída; condiciones desconocidas conservadas expresamente.'),checked=CHECKED,status='Идея',note=GATE,
  iso=[iso] if iso else [],themes=['robotics'],scope='regional',languages=[],language_mode='unconfirmed',language_certainty=LANG,
  participation='team',admission_kind='unknown',evidence_level='event_page',date_scope='festival_window',references=[])
 e.update(fields)
 if 'language' in fields:e['language_certainty']=fields['language']
 return e

def programme(ident,name,group,age,tags,events,**fields):
 p=dict(id=ident,name=name,group=group,age_summary=age,age_tags=tags,summary='',categories=[],event_ids=events,legacy_ids=[],
  route=GATE,hardware='',language=LANG,importance='',strengths='',requirements=[GATE],nuances=[AWARD],cost='',award=AWARD,sources=[],evidence=GATE)
 p.update(fields);return p

FLL_COST=T('CRC: Explore — 1 команда 70000 / 1 kit; 3 команды 120000 / 3 kits; 5 команд 175000 / 5 kits. Challenge — 1 команда 220000 / 1 kit; 3 команды 265000 / 1 kit; 5 команд 295000 / 1 kit. Это командные пакеты, не тарифы на ребёнка. Постер включает регистрацию, set категории, цифровые материалы, медаль LEGO и цифровой сертификат участникам. Состав kit, включение программируемого робота, налоги, доставка, тренер, компьютер и дорога требуют отдельного счёта.',
 'CRC: Explore — 1 equipo 70000 / 1 kit; 3 equipos 120000 / 3 kits; 5 equipos 175000 / 5 kits. Challenge — 1 equipo 220000 / 1 kit; 3 equipos 265000 / 1 kit; 5 equipos 295000 / 1 kit. Paquetes por equipo, no tarifas por niño. Póster incluye inscripción, set de categoría, material digital, medalla LEGO y certificado digital para participantes. Contenido de kit, inclusión de robot programable, impuestos, envío, entrenador, ordenador y viaje requieren factura aparte.')
FLL_ENTRY=T('Местный оператор Fundación STEAM публикует обе регистрации до 30 ноября 2026 и национальный день 6 марта 2027. Explore требует 3–6 детей и одного тренера; Challenge 3–8 и одного тренера. Двух братьев недостаточно для отдельной команды. Независимый / иностранный состав и страна представительства ещё не подтверждены; формы при анонимном чтении вернули HTTP 401, поля не проверены. Это не доказательство закрытого набора.',
 'Operador local Fundación STEAM publica ambas inscripciones hasta 30 de noviembre de 2026 y día nacional 6 de marzo de 2027. Explore exige 3–6 niños y un entrenador; Challenge 3–8 y un entrenador. Dos hermanos no bastan para equipo separado. Composición independiente / extranjera y país representado sin confirmar; formularios devolvieron HTTP 401 en lectura anónima, campos sin revisar. No acredita cierre de inscripción.')
FLL_GEAR=T('Explore: LEGO SPIKE Essential, сезонный Explore set / tapete, собственная модель и постер по текущему BIOGLOW notebook. Challenge: опубликованный BIOGLOW rulebook допускает SPIKE Prime, SPIKE Essential, EV3, Robot Inventor, Powered Up, NXT / RCX; максимум один контроллер и четыре мотора в матче. Программируемый робот не объявлен явно включённым в регистрационный kit. Состав пакета и применимость последних правил подтвердить.',
 'Explore: LEGO SPIKE Essential, Explore set / tapete de temporada, modelo propio y póster según notebook BIOGLOW vigente. Challenge: rulebook BIOGLOW publicado permite SPIKE Prime, SPIKE Essential, EV3, Robot Inventor, Powered Up, NXT / RCX; máximo un controlador y cuatro motores en partida. Robot programable no declarado expresamente incluido en kit de inscripción. Confirmar contenido de paquete y aplicación de últimas reglas.')

def fll_rows(d):
 e=next(e for e in d['events'] if e['id']=='C003')
 e.update(title='FIRST LEGO League Costa Rica · BIOGLOW Founders · '+T('национальный фестиваль','festival nacional'),
  city=T('Коста-Рика · площадка ещё не объявлена','Costa Rica · sede aún sin anunciar'),start='2027-03-06',end='2027-03-06',deadline='2026-11-30',
  period=T('Общий национальный день 6 марта 2027; расписание отдельных категорий и время закрытия записи ещё уточнить.',
   'Día nacional general 6 de marzo de 2027; confirmar horarios de categorías y hora de cierre de inscripción.'),date_status='Подтверждено',
  age='Explore 6–10; Challenge 9–16',mat=T('Да по возрасту: Explore и Challenge; состав и допуск команды подтвердить.',
   'Sí por edad: Explore y Challenge; confirmar composición y admisión de equipo.'),osc=T('Explore по возрасту; состав и допуск команды подтвердить.',
   'Explore por edad; confirmar composición y admisión de equipo.'),format=T('Explore: 3–6 детей + тренер; Challenge: 3–8 детей + тренер.',
   'Explore: 3–6 niños + entrenador; Challenge: 3–8 niños + entrenador.'),entry=FLL_ENTRY,gear=FLL_GEAR,cost=FLL_COST,
  source=FLL,proof=T('Собственная действующая страница партнёра подтверждает BIOGLOW, дату, дедлайн и местный состав. Постер цен осмотрен. Два связанных PDF действительно BIOGLOW 2026, а не старый UNEARTHED; технические страницы осмотрены. Испанский Explore notebook содержит марку перевода República Dominicana: это учебный материал, не правило иностранного допуска Costa Rica.',
   'Página vigente del propio socio confirma BIOGLOW, fecha, plazo y composición local. Póster de precios inspeccionado. Dos PDF enlazados son BIOGLOW 2026, no UNEARTHED antiguo; páginas técnicas inspeccionadas. Notebook Explore español lleva marca de traducción República Dominicana: material educativo, no regla de admisión extranjera de Costa Rica.'),
  priority=T('P1 — местный старт до 30 ноября','P1 — inicio local antes de 30 de noviembre'),
  action=T('Для общей Explore найти ещё минимум одного ребёнка и тренера. Для Матвея Challenge и Оскара Explore нужны отдельные команды не менее трёх участников каждая. Подтвердить независимый / иностранный вход, состав kit, язык и место; затем план подготовки до 6 марта. Дата совпадает с последним днём TMR Zacatecas 3–6 марта: выбрать основное событие маршрута.',
   'Para Explore conjunta encontrar al menos otro niño y entrenador. Para Matvey Challenge y Oscar Explore se necesitan equipos separados de al menos tres integrantes cada uno. Confirmar acceso independiente / extranjero, contenido de kit, idioma y sede; después plan hasta 6 de marzo. Fecha coincide con último día TMR Zacatecas 3–6 de marzo: elegir evento principal del itinerario.'),
  note=T('Опубликован Founders, не переносить аппаратные условия Future Edition México на Costa Rica. Медаль и сертификат из пакета — участие; место Challenge и международная квота требуют отдельного протокола / решения. Цена одной Explore команды 70000; отдельных Challenge + Explore 220000 + 70000 = 290000 CRC до неподтверждённых доплат. Общая дата не устанавливает отдельный час Explore или Challenge.',
   'Publicado Founders, sin trasladar condiciones de equipo Future Edition México a Costa Rica. Medalla y certificado del paquete son participación; puesto Challenge y cupo internacional requieren acta / decisión separada. Una Explore cuesta 70000; Challenge + Explore separados 220000 + 70000 = 290000 CRC antes de suplementos sin confirmar. Fecha general no fija hora separada de Explore o Challenge.'),
  checked=CHECKED,language=LANG,languages=[],language_certainty=LANG,language_mode='unconfirmed',admission_kind='open_application',evidence_level='program',date_scope='festival_window',
  reward=T('Explore — фестиваль и признание участия; медаль и цифровой сертификат включены в пакет. Место Challenge подтверждается протоколом; международная квота в этом анонсе не установлена.',
   'Explore es festival y reconocimiento de participación; paquete incluye medalla y certificado digital. Puesto Challenge requiere acta; cupo internacional sin acreditar en este anuncio.'),
  registration_status=T('Дедлайн опубликован; поля форм, наличие мест и фактическое зачисление не проверены.',
   'Plazo publicado; campos de formularios, plazas y admisión efectiva sin verificar.'),
  references=[ref('Fundación STEAM · BIOGLOW 2026–2027',FLL),ref(T('Прайс командных пакетов','Precios de paquetes por equipo'),PRICE),ref('Explore BIOGLOW notebook',EXPLORE),ref('Challenge BIOGLOW robot game rules',CHALLENGE)])
 for k in ['deadline_utc','deadline_note']:e.pop(k,None)
 out=[]
 for ident,kind,age,minimum,maximum in [('C1295','Explore','6–10',3,6),('C1296','Challenge','9–16',3,8)]:
  row=deepcopy(e);row.update(id=ident,title='FIRST LEGO League Costa Rica · BIOGLOW '+kind,canonical_event_id='C003',parent_event_id='C003',age=age,team_min=minimum,team_max=maximum,
   format=str(minimum)+'–'+str(maximum)+T(' детей + один тренер',' niños + un entrenador'),registration_url='https://forms.gle/'+('rvxwMUYyn1Bmauee9' if kind=='Explore' else '2nkydXsggPWw2pdE8'))
  if kind=='Challenge':row['osc']=T('Нет: опубликован минимум 9 лет.','No: mínimo publicado 9 años.')
  out.append(row)
 return out

NET_ACCESS=T('Команду заявляет образовательное учреждение. 24 ноября — Fiscales, 25 ноября — Particulares. Не являющемуся клиентом частному учреждению FAQ разрешает только Sumo 25 ноября за $40; Sumo требует 12+. Поэтому младший школьный трек не означает открытый семейный вход. Членство школы в программе, эквивалент класса и иностранную команду подтвердить отдельно.',
 'Equipo inscrito por institución educativa. 24 de noviembre Fiscales, 25 de noviembre Particulares. FAQ permite a institución privada no cliente solo Sumo el 25 de noviembre por $40; Sumo exige 12+. Curso escolar menor no implica acceso familiar abierto. Confirmar relación del colegio con programa, equivalencia de curso y equipo extranjero aparte.')
NET_FEES=T('На странице $40 за команду в каждой категории; не за ребёнка и не за все дисциплины вместе. Код валюты, инвентарь, налоги и окончательный счёт подтвердить. Вход зрителей бесплатный по предварительной регистрации; форма требует 10-значную cédula, иностранный документ и вход детей-гостей не подтверждены.',
 'Página indica $40 por equipo en cada categoría; no por niño ni por todas disciplinas juntas. Confirmar código de moneda, material, impuestos y factura final. Visita gratis con registro previo; formulario exige cédula de 10 dígitos, documento extranjero y entrada de niños visitantes sin confirmar.')
NET_RULES=[
 ('boliche','Boliche','Primaria Menor','Alphabot',T('Числовой возраст и эквивалент Primaria Menor не указаны. Максимум 15 × 15 × 15 cm; только детали разрешённого kit.',
  'Edad numérica y equivalencia de Primaria Menor no indicadas. Máximo 15 × 15 × 15 cm; solo piezas del kit permitido.')),
 ('fragata','Fragata','EGB 5–7 · 8–12','Alphabot',T('Автономная гонка; максимум ширины 40 cm и глубины 20 cm. Матвею нужно соответствовать и возрасту, и EGB 5–7; для Оскара минимальные 8 ещё не наступили.',
  'Carrera autónoma; ancho máximo 40 cm y profundidad 20 cm. Matvey debe cumplir edad y EGB 5–7; Oscar aún menor del mínimo 8.')),
 ('persecucion','Persecución','EGB 8–10 · 12–15','Construbot Plus',T('Автономное преследование с обязательной задержкой 5 секунд; для обоих детей это более поздний возраст.',
  'Persecución autónoma con demora obligatoria de 5 segundos; edad posterior para ambos niños.')),
 ('saca-basura','Saca la Basura','EGB 8–BGU 3 · 12+','Construbot Plus',T('Автономный сбор объектов, 2 минуты на раунд. Минимум 12 и школьный уровень, не младшая LEGO категория.',
  'Recogida autónoma de objetos, 2 minutos por ronda. Mínimo 12 y nivel escolar, no categoría LEGO menor.')),
 ('saca-basura-beet-bot','Saca la Basura Beet Bot','EGB 8–BGU 3 · 12+','Beetbot Arduino 1',T('Отдельная аппаратная версия сбора объектов на Beetbot Arduino 1; не свободный выбор любого Arduino-робота.',
  'Versión de equipo separada de recogida de objetos con Beetbot Arduino 1; no elección libre de cualquier robot Arduino.')),
 ('sumo','Sumo','EGB 8–BGU 3 · 12+','Construbot Plus',T('PDF допускает комбинации Construbot Plus, Alphabot и деталей других систем при собственных ограничениях; заголовок 12+ имеет приоритет над общей фразой primaria / secundaria. Оба ребёнка младше опубликованного минимума.',
  'PDF permite combinar Construbot Plus, Alphabot y piezas de otros sistemas con restricciones propias; encabezado 12+ prevalece sobre frase general primaria / secundaria. Ambos niños menores del mínimo publicado.'))]

def netica_rows():
 out=[]
 for ident,day,label,venue in [('C1297','2026-11-24','Fiscales','Escuela de Educación Básica Dieciocho de Agosto · Santa Elena'),('C1298','2026-11-25','Particulares','Unidad Educativa Abraham Lincoln · '+T('адрес / муниципалитет уточнить','confirmar dirección / municipio'))]:
  e=event(ident,'Grupo R.A. × Nética · '+label+' 2026',T('Эквадор','Ecuador'),NET,day,day,city=venue,venue=venue,
   age=T('По дисциплине: Primaria Menor, EGB 5–7 / 8–12 либо EGB 8+ / 12+.','Por disciplina: Primaria Menor, EGB 5–7 / 8–12 o EGB 8+ / 12+.'),
   deadline='2026-11-17',deadline_utc='2026-11-18T04:59:00Z',
   deadline_note=T('Свежие HTML / FAQ: 17 ноября 2026, 23:59; data-cierre использует смещение −05:00 и границу следующей полуночи. Старый индекс поиска с 22 ноября не применён. В Коста-Рике объявленная минута: 17 ноября 22:59.',
    'HTML / FAQ actuales: 17 de noviembre de 2026, 23:59; data-cierre usa desplazamiento −05:00 y límite de medianoche siguiente. Índice antiguo con 22 de noviembre no aplicado. Minuto anunciado en Costa Rica: 17 de noviembre 22:59.'),
   start_time='09:00',timezone='America/Guayaquil',entry=NET_ACCESS,cost=NET_FEES,admission_kind='school',
   gear=T('Fiscales: Boliche / Primaria Menor / Alphabot; Fragata / EGB 5–7 / 8–12 / Alphabot; Persecución и Sumo 12+. Particulares: Boliche и четыре старшие дисциплины Persecución, Saca la Basura, Sumo, Saca la Basura Beet Bot. Только категории своей редакции.',
    'Fiscales: Boliche / Primaria Menor / Alphabot; Fragata / EGB 5–7 / 8–12 / Alphabot; Persecución y Sumo 12+. Particulares: Boliche y cuatro disciplinas superiores Persecución, Saca la Basura, Sumo, Saca la Basura Beet Bot. Solo categorías de edición correspondiente.'),
   mat=T('Условно: младшая школьная категория и институциональный допуск отдельно.','Condicional: categoría escolar menor y admisión institucional aparte.'),
   osc=T('Условно: только при подтверждённой Primaria Menor и школьном доступе.','Condicional: solo con Primaria Menor y acceso escolar confirmados.'),
   proof=T('Прямо прочитаны две текущие редакции страницы, deadline и шесть PDF; технические заголовки осмотрены. В HTML одновременно присутствуют шаблоны открытого / закрытого / заполненного состояния: это не доказательство свободного места.',
    'Leídas directamente dos ediciones actuales de página, plazo y seis PDF; encabezados técnicos inspeccionados. HTML contiene a la vez plantillas abierta / cerrada / completa: no acredita plaza libre.'),
   note=T('Сбор 08:15, начало 09:00; конец не опубликован, в календаре день без выдуманных часов окончания. Родители не помогают на поле; вопросы судье задают участники. Партнёр из México не превращает событие в мексиканский или мировой отбор.',
    'Convocatoria 08:15, inicio 09:00; fin sin publicar, calendario por día sin hora de fin inventada. Padres no ayudan en pista; participantes consultan al juez. Socio de México no convierte evento en clasificatorio mexicano o mundial.'))
  out.append(e)
 next_id=1299
 for parent,keys in [('C1297',['boliche','fragata','persecucion','sumo']),('C1298',['boliche','persecucion','saca-basura','sumo','saca-basura-beet-bot'])]:
  base=next(e for e in out if e['id']==parent)
  for key in keys:
   _,name,age,kit,note=next(x for x in NET_RULES if x[0]==key)
   e=deepcopy(base);e.update(id='C'+str(next_id),title=base['title']+' · '+name,canonical_event_id=parent,parent_event_id=parent,age=age,gear=kit+' · '+note,note=note+' '+NET_ACCESS,source=NET_PDF+key+'.pdf',references=[ref('Official edition / fees / admission',NET),ref(name+' · 2026 rules',NET_PDF+key+'.pdf')],evidence_level='rules')
   if key=='fragata':e['osc']=T('Нет по опубликованному минимуму 8 лет; реальный школьный уровень также обязателен.',
    'No por mínimo publicado de 8 años; nivel escolar real también obligatorio.')
   elif key not in ['boliche']:
    e['mat']=e['osc']=T('Нет сейчас: опубликован минимум 12 лет и старший школьный уровень.',
     'No actualmente: mínimo publicado 12 años y nivel escolar superior.');e['priority']=T('P4 — будущий возраст','P4 — edad futura')
   out.append(e);next_id+=1
 assert next_id==1308
 return out

def other_rows():
 out=[]
 out.append(event('C1308','Academia STEM · Chihuahua Zona Centro · 2026-11-09',T('Мексика','México'),ACA,'2026-11-09','2026-11-09',city='Facultad de Medicina UACH · Campus II · Poliforum Dr. Victor M. Gómez Moreno',
  age=T('API указывает Básico / Media Superior / Superior; разбивка младших внутри категорий не опубликована в этой карточке.',
   'API indica Básico / Media Superior / Superior; desglose de menores por categoría sin publicar en esta ficha.'),
  gear=T('В карточке Robótica Móvil, Robótica Colaborativa / Automatización, IoT и AI. Уровни и категория конкретного ребёнка подтверждаются отдельно; общий Básico не разрешает автоматически все четыре дисциплины шестилетним.',
   'Ficha incluye Robótica Móvil, Robótica Colaborativa / Automatización, IoT y AI. Confirmar nivel y categoría del niño por separado; Básico general no autoriza automáticamente cuatro disciplinas a niños de seis años.'),
  action=T('Проверить текущий приём, школьный класс и местные bases выбранной дисциплины. Не переносить цену и квоту другого чемпионата; до события мало времени, доступ семьи не подтверждён.',
   'Comprobar admisión actual, curso y bases locales de disciplina elegida. Sin trasladar tarifa ni cupo de otro campeonato; falta poco para evento, acceso familiar sin confirmar.'),
  references=[ref('Public list used by official championships app',ACA_API)],proof=T('Карточка публичного read-only API id 18, new_season 1, согласуется с индексом официального сайта. Старые события 2025 со status active не приняты за будущие регистрации.',
   'Ficha de API pública de solo lectura id 18, new_season 1, coincide con índice de web oficial. Eventos antiguos de 2025 con status active no tomados como inscripciones futuras.'),themes=['robotics','coding','ai'],admission_kind='open_application'))
 out.append(event('C1309','Robo Blasters 2026 · El Reto de la MUDANZA',T('Мексика','México'),BLAST,'2026-12-05','2026-12-05',city='Tecnológico de Monterrey · Campus Cuernavaca',deadline='2026-10-17',
  age=T('Только реальные 5–6 классы primaria и 1–3 secundaria; возраст не заменяет класс.','Solo cursos reales 5–6 de primaria y 1–3 de secundaria; edad no sustituye curso.'),
  gear=T('Команды и альянсы перевозят / размещают коробки на тематическом поле. Полный технический manual, разрешённый комплект и размер команды ещё не прочитаны.',
   'Equipos y alianzas transportan / colocan cajas en campo temático. Manual técnico completo, kit permitido y tamaño de equipo aún sin leer.'),
  priority=T('P4 — срок записи прошёл','P4 — plazo de inscripción vencido'),registration_status=T('На странице срок 17 октября 2026 уже прошёл; поздний вход не подтверждён.',
   'Plazo publicado 17 de octubre de 2026 ya vencido; admisión tardía sin confirmar.'),note=T('Страница Tecnológico de Monterrey подтверждает 5 декабря. Ни класс Матвея, ни класс Оскара не известны; ускоренный или обычный класс автоматически не назначен. Билет зрителя и следующая редакция не объявлены в прочитанной странице.',
   'Página de Tecnológico de Monterrey confirma 5 de diciembre. Cursos de Matvey y Oscar desconocidos; sin asignar curso acelerado ni ordinario automáticamente. Entrada de visitante y próxima edición sin anunciar en página leída.')))
 fire_age=T('Exploradores 7–9; Junior 10–12; Juvenil 13–15; Senior 16–19. Отсечка и размер команды ещё не установлены.',
  'Exploradores 7–9; Junior 10–12; Juvenil 13–15; Senior 16–19. Corte de edad y tamaño de equipo aún sin establecer.')
 out.append(event('C1310','FIRE · '+T('объявленная институциональная сеть / следующий набор','red institucional anunciada / próxima convocatoria'),T('Международная сеть · место ожидается','Red internacional · sede pendiente'),FIRE,
  age=fire_age,mat=T('Условно: сейчас 9, в 2027 возможен Junior с 10; правило отсечки и набор не опубликованы.',
   'Condicional: ahora 9, en 2027 podría Junior desde 10; corte y convocatoria sin publicar.'),osc=T('Нет сейчас: минимум 7. После 7-летия нужны новые правила и подтверждение группы.',
   'No actualmente: mínimo 7. Tras cumplir 7 años exige reglas nuevas y confirmación de grupo.'),scope='international',admission_kind='school',evidence_level='catalog',
  cost=T('Объявлены USD 100 / 500 / 990 за 12 месяцев институционального членства; F1 20 / F2 35 / F3 55 / F4 80 USD за команду. Это предложение, финальные условия подтверждаются письменно; льготы не применены автоматически. Нулевой обязательный платёж ученика не делает бесплатными учреждение, робот и поездку.',
   'Anunciados USD 100 / 500 / 990 por 12 meses de membresía institucional; F1 20 / F2 35 / F3 55 / F4 80 USD por equipo. Propuesta con condiciones finales por confirmar por escrito; sin descuentos automáticos. Cero pago obligatorio del alumno no hace gratuitos institución, robot ni viaje.'),
  gear=T('Заявлена технологическая нейтральность: Arduino, Raspberry Pi, LEGO Education, micro:bit, ESP32 и собственные роботы. Предельные размеры и ограничения выбранного состязания ещё нужны из полного регламента.',
   'Se declara neutralidad tecnológica: Arduino, Raspberry Pi, LEGO Education, micro:bit, ESP32 y robots propios. Aún hacen falta límites y restricciones del concurso elegido en reglamento completo.'),
  entry=T('Учреждение → членство → выбранный этап F1 / F2 / F3 / F4 → convocatoria. Семейная независимая команда, местный отбор и точные условия перехода не подтверждены.',
   'Institución → membresía → etapa F1 / F2 / F3 / F4 elegida → convocatoria. Equipo familiar independiente, selección local y condiciones exactas de avance sin confirmar.'),
  note=T('На странице названы Ecuador, Colombia, Perú, Argentina, México, España; даты и площадки не объявлены. Статистика говорит о трёх уровнях, схема показывает четыре. После национального уровня международная стадия 2027 ещё в определении. Заявлены Rescate Autónomo, Robofútbol, Copa de Innovación, но ниже rescate / drones / AI описаны как последующие: реальный перечень нуждается в convocatoria. Внешний мировой рейтинг и протоколы победителей в прочитанном материале не установлены.',
   'Página nombra Ecuador, Colombia, Perú, Argentina, México, España; fechas y sedes sin anunciar. Estadística dice tres niveles, esquema muestra cuatro. Etapa internacional 2027 posterior a nacional aún en definición. Anuncia Rescate Autónomo, Robofútbol, Copa de Innovación, pero después rescate / drones / AI como posteriores: oferta real requiere convocatoria. Ranking mundial externo y actas de ganadores sin acreditar en material leído.')))
 for ident,name,team in [('C1311','Soccer Entry','2–4'),('C1312','Rescue Line Entry','2–4'),('C1313','OnStage Entry','2–5')]:
  out.append(event(ident,'RoboCupJunior Américas · Primary · '+name+' · '+T('следующая редакция','próxima edición'),T('Америка / место ожидается','Américas / sede pendiente'),RCJ,
   age=T('Primary 10–14 на 1 июля года турнира; все участники в пределах. Правила конкретной редакции 2027 ещё проверить.',
    'Primary 10–14 al 1 de julio del año de torneo; todos integrantes dentro del rango. Verificar aún reglas de edición concreta 2027.'),
   mat=T('Условно в 2027: 2017 год рождения допускает возраст 10 на 1 июля только при рождении не позднее 1 июля. День рождения неизвестен.',
    'Condicional en 2027: nacido en 2017 cumple 10 al 1 de julio solo si nació hasta el 1 de julio inclusive. Cumpleaños desconocido.'),
   osc=T('Нет для Primary 2027: 2020 год рождения ниже 10 на 1 июля.',
    'No para Primary 2027: nacido en 2020 menor de 10 al 1 de julio.'),
   format=team+T(' ученика + mentor 19+ на событии; размер новой редакции подтвердить.',
    ' alumnos + mentor 19+ en evento; confirmar tamaño de nueva edición.'),scope='international',admission_kind='qualifier',parent_event_id='C042',canonical_event_id='C042',
   gear=name+T(' по правилам Entry выбранной редакции; собственный автономный робот / проект, не взрослое готовое решение.',
    ' según reglas Entry de edición elegida; robot / proyecto autónomo propio, no solución preparada por adulto.'),
   entry=T('Обычно региональный Open → представитель страны → квота → регистрация после подтверждения. Для страны без аккредитованного комитета можно запросить гостевое место, оно не даёт права на RCJ International. Гражданство México и ПМЖ Costa Rica автоматически не определяют страну команды.',
    'Normalmente Open regional → representante nacional → cupo → inscripción tras confirmar. País sin comité acreditado puede solicitar plaza invitada, sin derecho a RCJ International. Ciudadanía mexicana y residencia permanente costarricense no determinan automáticamente país de equipo.'),
   language=T('Правила на английском, English контролирует версию; язык интервью выбранной команды ещё согласовать.',
    'Reglas en inglés, versión English prevalece; acordar todavía idioma de entrevistas del equipo elegido.'),
   note=T('2027: место и даты выбираются, не перенесены канадские 22–25 октября 2026. Primary — международная SuperRegional, не мировой финал RCJ: International 14–19. Братья не могут вместе составить команду Primary 2027.',
    '2027: sede y fechas por elegir, sin trasladar fechas canadienses 22–25 de octubre de 2026. Primary es SuperRegional internacional, no final mundial RCJ: International 14–19. Hermanos no pueden formar juntos equipo Primary 2027.'),
   references=[ref('Official general age / team / route',RCJ),ref('Guest path without regional committee',GUEST)]))
 return out

PAN_RULES=[('animate','Animate · Green Planet',4,5,'Tale-Bot'),('iluminate','Iluminate · Sequence Challenge',6,7,'Tale-Bot'),('wonders-makers','Wonders Makers · Free Project',8,10,'Elecfreaks Wonder Building Kit 32 in 1 + micro:bit'),('robot-explorers','Robot Explorers · Line Follower',11,14,'mBot 2'),('sumo','Sumo Challenge · Robot Sumo',11,14,'mBot 2'),('off-road','Off Road Challenge · Extreme Circuit',15,18,'mBot Ranger')]
PAN_WATCH=T('Последняя опубликованная дата 7–9 октября 2026, Instituto Técnico Don Bosco, Paitilla / vía Israel / calle 71. Это уже прошедший сезон; дата и правила следующего набора не объявлены. Passline ведёт на общий home, билет и цена не подтверждены. Ссылка INSCRÍBETE AHORA не доказательство нового набора.',
 'Última fecha publicada 7–9 de octubre de 2026, Instituto Técnico Don Bosco, Paitilla / vía Israel / calle 71. Temporada pasada; fecha y reglas de próxima convocatoria sin anunciar. Passline redirige a home general, billete y precio sin confirmar. Enlace INSCRÍBETE AHORA no acredita convocatoria nueva.')

def panama_rows():
 parent=event('C1314','Eduvisión Robotics Challenge Panamá · '+T('следующий сезон / архив правил 2026','próxima temporada / archivo de reglas 2026'),T('Панама','Panamá'),PAN,
  period=PAN_WATCH,age=T('Правила 2026: шесть категорий 4–18, возраст на 31 марта 2026; на будущий сезон правило не перенесено автоматически.',
   'Reglas 2026: seis categorías 4–18, edad al 31 de marzo de 2026; regla no trasladada automáticamente a temporada futura.'),
  format=T('В PDF каждой категории 3 участника + один docente / coach старше 18; представляют учреждение.',
   'PDF de cada categoría exige 3 participantes + un docente / coach mayor de 18; representan institución.'),
  entry=T('В анонсе colegios / clubes, в PDF представительство учреждения. Независимую иностранную семейную команду, школьный эквивалент и язык интервью согласовать. Новая регистрация не установлена.',
   'Anuncio menciona colegios / clubes, PDF representación institucional. Acordar equipo familiar extranjero independiente, equivalencia escolar e idioma de entrevista. Sin acreditar inscripción nueva.'),
  published_start='2026-10-07',published_end='2026-10-09',evidence_level='historical_program',admission_kind='school',note=PAN_WATCH,
  gear=T('По правилам 2026: Tale-Bot для Animate / Iluminate, Wonder Building Kit 32 in 1 + micro:bit для Wonders Makers, mBot 2 для Robot Explorers / Sumo, mBot Ranger для Off Road. Приём следующего года не подтверждён.',
   'Según reglas 2026: Tale-Bot para Animate / Iluminate, Wonder Building Kit 32 in 1 + micro:bit para Wonders Makers, mBot 2 para Robot Explorers / Sumo, mBot Ranger para Off Road. Admisión de año siguiente sin confirmar.'),
  references=[ref('Official last-season date poster',PAN+'assets/images/fechas-evento.png'),ref('General rules 2026',PAN_PDF+'general-robotics-2026.pdf')])
 out=[parent]
 for number,(key,name,lo,hi,kit) in enumerate(PAN_RULES,1315):
  e=deepcopy(parent);e.update(id='C'+str(number),title='Eduvisión Panamá · '+name+' · '+T('правила 2026 / следующий набор','reglas 2026 / próxima convocatoria'),canonical_event_id='C1314',parent_event_id='C1314',
   age=str(lo)+'–'+str(hi)+T(' на 31 марта опубликованного года 2026; новый год ещё не объявлен.',
    ' al 31 de marzo del año publicado 2026; año nuevo aún sin anunciar.'),age_reference_date='2026-03-31',team_min=3,team_max=3,gear=kit,source=PAN_PDF+key+'.pdf',
   mat=T('Условно: будущий набор, новая отсечка и индивидуальный допуск не объявлены.',
    'Condicional: convocatoria futura, corte nuevo y admisión individual sin anunciar.'),
   osc=T('Условно: будущий набор, новая отсечка и индивидуальный допуск не объявлены.',
    'Condicional: convocatoria futura, corte nuevo y admisión individual sin anunciar.'),
   references=parent['references']+[ref(name+' · 2026 rules',PAN_PDF+key+'.pdf')])
  if lo>=11:e['mat']=e['osc']=T('Нет по опубликованным правилам 2026; следующий сезон отдельно, это более поздний возраст.',
   'No según reglas publicadas 2026; próxima temporada aparte, edad posterior.')
  elif key=='animate':e['mat']=T('Нет по диапазону 4–5; для Оскара архивная отсечка 31 марта 2026 и будущий набор различаются.',
   'No por rango 4–5; para Oscar corte archivado 31 de marzo de 2026 y convocatoria futura son distintos.')
  elif key=='iluminate':e['mat']=T('Нет по опубликованному максимуму 7; следующий сезон ещё не опубликован.',
   'No por máximo publicado 7; próxima temporada aún sin publicar.')
  elif key=='wonders-makers':e['osc']=T('Нет по опубликованному минимуму 8; будущий год правил ещё не объявлен.',
   'No por mínimo publicado 8; año futuro de reglas aún sin anunciar.')
  out.append(e)
 return out

def profiles():
 out=[]
 out.append(programme('fll-costa-rica-bioglow','FIRST LEGO League Costa Rica · BIOGLOW Founders','regional','Explore 6–10; Challenge 9–16',['6','9','10-12','teen'],['C003','C1295','C1296'],
  summary=T('Подтверждённый местный сезон с дедлайном 30 ноября 2026 и национальным днём 6 марта 2027. У братьев есть возрастной путь, но требуется дополнительный состав команды и подтверждение независимого / иностранного доступа.',
   'Temporada local confirmada con plazo 30 de noviembre de 2026 y día nacional 6 de marzo de 2027. Hermanos tienen vía por edad, pero requieren más integrantes y confirmación de acceso independiente / extranjero.'),
  categories=[dict(name='Explore',age='6–10',team='3–6 + coach',hardware='SPIKE Essential + Explore set / tapete',age_rule=T('Местная страница 6–10; точную отсечку подтвердить.','Página local 6–10; confirmar corte exacto.'),entry=FLL_ENTRY,event_id='C1295'),dict(name='Challenge',age='9–16',team='3–8 + coach',hardware=FLL_GEAR,age_rule=T('Местная страница 9–16; точную отсечку подтвердить.','Página local 9–16; confirmar corte exacto.'),entry=FLL_ENTRY,event_id='C1296')],
  route=T('Команда → местная регистрация до 30 ноября → подготовка BIOGLOW → национальный день 6 марта. Международная квота и её условия в этом анонсе не подтверждены.',
   'Equipo → inscripción local antes de 30 de noviembre → preparación BIOGLOW → día nacional 6 de marzo. Cupo internacional y sus condiciones sin confirmar en este anuncio.'),
  hardware=FLL_GEAR,importance=T('Приоритетная реальная возможность дома; не требует выбора новой страны ради первой заявки.',
   'Oportunidad real prioritaria en casa; no exige elegir nuevo país para primera solicitud.'),
  strengths=T('Explore позволяет общий семейный проект при третьем участнике. Challenge даёт Матвею соревновательные задачи, программирование, исследовательский проект и защиту; соответствие уровню после трёх лет практики оценивает тренер.',
   'Explore permite proyecto familiar conjunto con tercer integrante. Challenge ofrece a Matvey retos competitivos, programación, proyecto de investigación y defensa; entrenador evalúa adecuación tras tres años de práctica.'),
  requirements=[FLL_ENTRY,FLL_GEAR,T('Время закрытия записи, место финала, защита EN / ES и условия допуска семьи ещё требуют ответа оператора.',
   'Hora de cierre, sede final, defensa EN / ES y admisión familiar aún requieren respuesta del operador.')],
  nuances=[AWARD,T('Пакеты трёх / пяти Challenge команд содержат только один kit по постеру; не приравнивать к трём / пяти роботам. Explore пакет трёх / пяти команд содержит три / пять kits.',
   'Paquetes Challenge de tres / cinco equipos contienen solo un kit según póster; no equivalen a tres / cinco robots. Explore de tres / cinco equipos incluye tres / cinco kits.'),T('Один совместный Explore пакет 70000 CRC; два отдельных пакета Challenge + Explore 290000 CRC. Это не полный бюджет семьи и не подтверждённая личная сумма после разделения расходов с партнёрами.',
   'Un paquete Explore conjunto 70000 CRC; dos paquetes separados Challenge + Explore 290000 CRC. No es presupuesto familiar completo ni aportación personal confirmada tras repartir costes con compañeros.')],cost=FLL_COST,
  sources=[src('Costa Rica partner programme / date / deadline',FLL),src('Current team-package price poster',PRICE),src('Current BIOGLOW Explore notebook',EXPLORE),src('Current BIOGLOW Challenge rules',CHALLENGE)],
  evidence=T('Локальная страница, цена и связанные BIOGLOW материалы прочитаны. Формы недоступны при анонимном чтении; заявки не отправлялись.',
   'Leídos página local, precio y materiales BIOGLOW enlazados. Formularios inaccesibles en lectura anónima; sin solicitudes enviadas.')))
 out.append(programme('fire-institutional','FIRE · '+T('новая институциональная сеть','nueva red institucional'),'regional',T('Четыре возрастные группы 7–19; правило отсечки ещё не опубликовано.','Cuatro grupos de edad 7–19; corte aún sin publicar.'),['9','10-12','teen'],['C1310'],
  summary=T('Развивающийся оператор с институциональной моделью и объявленными странами. Календарь, полные технические регламенты и независимые исторические результаты пока не установлены по прочитанной странице.',
   'Operador emergente con modelo institucional y países anunciados. Calendario, reglamentos técnicos completos y resultados históricos independientes aún sin acreditar en página leída.'),
  categories=[dict(name=name,age=age,team=T('Не опубликовано','Sin publicar'),hardware=T('Платформа нейтральна по заявлению оператора; ограничения по будущей convocatoria.','Operador declara plataforma neutral; restricciones según futura convocatoria.'),age_rule=T('День отсечки и состав смешанных возрастов ещё подтвердить.','Confirmar fecha de corte y composición de edades mixtas.'),entry=T('Через учреждение и выбранный этап.','Mediante institución y etapa elegida.')) for name,age in [('Exploradores','7–9'),('Junior','10–12'),('Juvenil','13–15'),('Senior','16–19')]],
  route=T('F1 учреждение → F2 местный / региональный → F3 департамент → F4 национальный. Автоматический переход по оплате не установлен; международная стадия 2027 в определении.',
   'F1 institución → F2 local / regional → F3 departamento → F4 nacional. Sin acreditar avance automático por pago; etapa internacional 2027 en definición.'),
  hardware='Arduino / Raspberry Pi / LEGO Education / micro:bit / ESP32',
  importance=T('Дополнительный региональный кандидат; статус топовой мировой лиги не доказан.',
   'Candidato regional complementario; sin acreditar condición de liga mundial líder.'),
  strengths=T('Заявлены разные платформы и сочетание инженерных / проектных дисциплин; оценка фактического уровня возможна после правил и протоколов.',
   'Declara varias plataformas y combinación de ingeniería / proyectos; nivel real evaluable tras reglas y actas.'),
  requirements=[T('Нужна принимаемая оператором организация; приём независимой семейной команды не подтверждён.',
   'Exige organización aceptada por operador; admisión de equipo familiar independiente sin confirmar.'),GATE],
  nuances=[AWARD,T('Упоминания шести стран и международных конференций не подтверждают шесть действующих турниров. Страница одновременно показывает три уровня в счётчике и четыре в маршруте.',
   'Mencionar seis países y conferencias internacionales no acredita seis torneos operativos. Página muestra tres niveles en contador y cuatro en ruta.')],
  cost=T('Публичное предложение: членство учреждения USD 100 / 500 / 990 на 12 месяцев; F1 20 / F2 35 / F3 55 / F4 80 USD за команду. Финальные условия и применимость включённых регистраций подтвердить; полная семейная сумма не рассчитана.',
   'Propuesta pública: membresía institucional USD 100 / 500 / 990 por 12 meses; F1 20 / F2 35 / F3 55 / F4 80 USD por equipo. Confirmar condiciones finales e inscripciones incluidas; sin calcular coste familiar completo.'),sources=[src('Founding season / age groups / institutional fees',FIRE)],evidence=T('Прочитана собственная страница оператора, включая условность предложения, отсутствие календаря и будущую международную стадию.',
   'Leída página propia del operador, incluida provisionalidad de propuesta, ausencia de calendario y etapa internacional futura.')))
 out.append(programme('rcj-americas-primary','RoboCupJunior Américas · Primary / SuperRegional','international',T('Primary 10–14 на 1 июля; Secondary 14–19; даты 2027 выбираются.',
  'Primary 10–14 al 1 de julio; Secondary 14–19; fechas 2027 por elegir.'),['10-12','teen'],['C042','C1311','C1312','C1313'],
  summary=T('Международная региональная ступень самостоятельной робототехники для подростающего Матвея. Уровень Primary отличается от мирового финала RCJ 14–19.',
   'Etapa regional internacional de robótica autónoma para futuro de Matvey. Primary se distingue de final mundial RCJ 14–19.'),
  categories=[dict(name=name,age='10–14',team=team+' + mentor 19+',hardware=T('Автономные роботы / выступление по Entry rules.','Robots / actuación autónomos según Entry rules.'),age_rule=T('Все ученики 10–14 на 1 июля; новая редакция может уточнять размер команды.',
   'Todos alumnos 10–14 al 1 de julio; nueva edición puede precisar tamaño de equipo.'),entry=T('Квота представителя страны либо отдельно одобренное гостевое место.',
   'Cupo del representante nacional o plaza invitada aprobada por separado.'),event_id=ident) for ident,name,team in [('C1311','Soccer Entry','2–4'),('C1312','Rescue Line Entry','2–4'),('C1313','OnStage Entry','2–5')]],
  route=T('Региональный Open → решение страны → подтверждённая квота → регистрация в редакции. Страна без комитета может просить гостевое место; оно не даёт права на International.',
   'Open regional → decisión nacional → cupo confirmado → inscripción en edición. País sin comité puede solicitar plaza invitada; sin derecho a International.'),
  hardware=T('Самостоятельный автономный робот для Soccer / Rescue или сценический проект OnStage; технические пределы конкретной редакции отдельно.',
   'Robot autónomo propio para Soccer / Rescue o proyecto escénico OnStage; límites técnicos de edición concreta aparte.'),
  language=T('English rules — контролирующая версия; язык интервью уточняется.','English rules es versión prevalente; confirmar idioma de entrevistas.'),
  importance=T('Содержательная цель на возраст 10–12, с реальным отбором и технической самостоятельностью; не открытая семейная покупка мировой медали.',
   'Meta sustancial a los 10–12, con selección real y autonomía técnica; no compra familiar abierta de medalla mundial.'),
  strengths=T('Робот, код, устранение неполадок и объяснение своего вклада. Для участия младшего возраста существуют региональные Entry правила.',
   'Robot, código, resolver fallos y explicar aportación propia. Existen reglas Entry regionales para participantes menores.'),
  requirements=[T('Матвей 2017: для 2027 нужен день рождения не позднее 1 июля; иначе следующая возможность по той же отсечке в 2028. Оскар 2020 не проходит Primary 2027.',
   'Matvey de 2017: en 2027 exige cumpleaños hasta 1 de julio inclusive; de lo contrario siguiente posibilidad con mismo corte en 2028. Oscar de 2020 no cumple Primary 2027.'),T('Нужен другой подходящий ученик / команда и mentor 19+ на событии. Местные размеры и право представлять страну подтвердить.',
   'Exige otro alumno / equipo elegible y mentor 19+ en evento. Confirmar tamaños locales y derecho a representar país.')],
  nuances=[AWARD,T('Место / дата 2027 не объявлены. Прошедший Brampton 22–25 октября 2026 не перенесён автоматически на 2027. Гостевой путь для страны без комитета не означает автоматическое приглашение.',
   'Sede / fecha 2027 sin anunciar. Brampton pasado 22–25 de octubre de 2026 no trasladado automáticamente a 2027. Ruta invitada para país sin comité no significa invitación automática.')],
  cost=T('Тариф новой редакции не объявлен; робот, ноутбук, mentor, дорога и проживание отдельно. Публичный доступ зрителей и участие команды имеют разные условия.',
   'Tarifa de nueva edición sin anunciar; robot, portátil, mentor, viaje y alojamiento aparte. Acceso público de visitantes y participación del equipo tienen condiciones distintas.'),
  sources=[src('Current general age / divisions / country route',RCJ),src('Guest path without regional committee',GUEST),src('Event history and organiser',RCJ+'about/')],evidence=T('Текущие общие страницы и гостевой маршрут прочитаны; условия конкретной будущей редакции остаются неизвестными.',
   'Leídas páginas generales vigentes y ruta invitada; condiciones de futura edición concreta aún desconocidas.')))
 out.append(programme('eduvision-panama','Eduvisión Robotics Challenge Panamá','regional',T('Правила 2026: 4–18, отсечка 31 марта; будущий набор не объявлен.',
  'Reglas 2026: 4–18, corte 31 de marzo; convocatoria futura sin anunciar.'),['6','9','10-12','teen'],['C1314']+['C'+str(i) for i in range(1315,1321)],
  summary=PAN_WATCH,
  categories=[dict(name=name,age=str(lo)+'–'+str(hi),team='3 + coach',hardware=kit,age_rule=T('Архив 2026: возраст на 31 марта; правило следующего сезона ещё не установлено.',
   'Archivo 2026: edad al 31 de marzo; regla de próxima temporada aún sin establecer.'),entry=T('Через учреждение; новый приём и иностранная команда ещё не подтверждены.',
   'Por institución; convocatoria nueva y equipo extranjero sin confirmar.'),event_id='C'+str(i)) for i,(key,name,lo,hi,kit) in enumerate(PAN_RULES,1315)],
  route=T('Школьная / клубная подготовка → новая convocatoria → категория по опубликованной отсечке → местное состязание. Международная квалификация этим анонсом не установлена.',
   'Preparación escolar / club → nueva convocatoria → categoría por corte publicado → concurso local. Sin acreditar clasificación internacional mediante este anuncio.'),
  hardware=T('Tale-Bot для 4–5 / 6–7; Wonder Building Kit 32 in 1 + micro:bit для 8–10; mBot 2 для 11–14; mBot Ranger для 15–18. Свободный выбор любого робота не предусмотрен этими правилами.',
   'Tale-Bot para 4–5 / 6–7; Wonder Building Kit 32 in 1 + micro:bit para 8–10; mBot 2 para 11–14; mBot Ranger para 15–18. Reglas no ofrecen libre elección de cualquier robot.'),
  importance=T('Близкий региональный резерв с конкретной младшей структурой; не подтверждённая поездка 2027.',
   'Alternativa regional cercana con estructura menor concreta; no viaje 2027 confirmado.'),
  strengths=T('От программирования кнопками к micro:bit проекту, следованию линии, sumo и автономной навигации. Возраст и комплект отличаются по дисциплинам.',
   'Desde programación por botones hasta proyecto micro:bit, seguidor de línea, sumo y navegación autónoma. Edad y equipo varían por disciplina.'),
  requirements=[T('Каждая из шести PDF категорий требует три ученика и одного представителя / coach старше 18. Два брата не образуют такую команду; младшие идут в разные возрастные группы.',
   'Cada una de seis categorías PDF exige tres alumnos y un representante / coach mayor de 18. Dos hermanos no forman tal equipo; menores en grupos de edad distintos.'),GATE],
  nuances=[PAN_WATCH,T('Не вычислять допуск по возрасту в день турнира: в опубликованных правилах используется 31 марта. Для будущего года нужна новая редакция, не механическая замена 2026 на 2027.',
   'Sin calcular admisión por edad el día de torneo: reglas publicadas usan 31 de marzo. Año futuro requiere edición nueva, no sustitución mecánica de 2026 por 2027.')],
  cost=T('Взнос, kit, обслуживание и зрительский билет следующего сезона не установлены. Переход старой ссылки Passline на общий home не является доступным билетом.',
   'Tarifa, kit, mantenimiento y billete de visitante de próxima temporada sin establecer. Redirección de enlace Passline antiguo a home general no es billete disponible.'),
  sources=[src('Official programme / last-season date poster',PAN),src('Published October 2026 date',PAN+'assets/images/fechas-evento.png'),src('General rules 2026',PAN_PDF+'general-robotics-2026.pdf')]+[src(name+' · 2026 rules',PAN_PDF+key+'.pdf') for key,name,lo,hi,kit in PAN_RULES],
  evidence=T('Общий документ и шесть категорий прочитаны; все страницы возраста / состава / оборудования и дата постера осмотрены. Прайс и новые даты не найдены в этих источниках.',
   'Leídos documento general y seis categorías; inspeccionadas páginas de edad / composición / equipo y fecha de póster. Sin localizar tarifa ni fechas nuevas en estas fuentes.')))
 return out

def enrich_v160(d):
 rows=fll_rows(d)+netica_rows()+other_rows()+panama_rows();index={e['id']:e for e in rows};assert len(index)==26
 old={e['id'] for e in d['events']};d['events']=[index.get(e['id'],e) for e in d['events']]+[e for e in rows if e['id'] not in old]
 e=next(e for e in d['events'] if e['id']=='C042');sample=next(e for e in rows if e['id']=='C1311')
 for key in ['age','mat','osc','entry','language','language_certainty','note','references']:e[key]=deepcopy(sample[key])
 e.update(source=RCJ,checked=CHECKED,languages=[],language_mode='unconfirmed',period=T('Следующая редакция 2027: даты и место выбираются; канадский этап 2026 завершён.',
  'Próxima edición 2027: fechas y sede por elegir; edición canadiense 2026 finalizada.'),format=T('Обычно 2–4, OnStage до 5; mentor 19+; новый размер по редакции.',
  'Normalmente 2–4, OnStage hasta 5; mentor 19+; tamaño nuevo según edición.'),action=sample['entry'],proof=T('Текущая общая страница подтверждает Primary 10–14 на 1 июля, иностранный путь через страны и отсутствие места / дат 2027. Отдельно прочитан гостевой маршрут.',
  'Página general vigente confirma Primary 10–14 al 1 de julio, vía extranjera por países y ausencia de sede / fechas 2027. Ruta invitada leída por separado.'))
 guide=d['league_guide'];new=profiles();newmap={p['id']:p for p in new};known={p['id'] for p in guide['profiles']}
 guide['profiles']=[newmap.get(p['id'],p) for p in guide['profiles']]+[p for p in new if p['id'] not in known]
 guide.update(version=160,checked=CHECKED)
 p=next(p for p in guide['profiles'] if p['id']=='rcj')
 for category in p['categories']:
  if category['name']=='Entry / Primary':category['age_rule']=T('Americas: 10–14 на 1 июля по текущей общей странице; конкретную редакцию 2027 подтвердить отдельно.',
   'Americas: 10–14 al 1 de julio según página general actual; confirmar edición concreta 2027 aparte.')
 new_note=T('Americas Primary: Матвей 2017 проходит 2027 только при 10-летии не позднее 1 июля; Оскар 2020 не проходит. Для страны без комитета есть запрос гостевого места, который не даёт права на International; даты 2027 пока выбираются.',
  'Americas Primary: Matvey de 2017 cumple en 2027 solo si cumple 10 años no más tarde del 1 de julio inclusive; Oscar de 2020 no cumple. País sin comité puede pedir plaza invitada sin derecho a International; fechas 2027 por elegir.')
 if new_note not in p['nuances']:p['nuances'].append(new_note)
 p['sources']=list({s['url']:s for s in p['sources']+[src('Americas current general ages and route',RCJ),src('Americas guest teams',GUEST)]}.values())
 actions=[dict(period=T('До 30 ноября 2026','Antes de 30 de noviembre de 2026'),title=T('Коста-Рика: собрать действующую BIOGLOW команду','Costa Rica: formar equipo BIOGLOW vigente'),detail=T('Общая Explore: дети 6–10, минимум 3, значит братьям нужен ещё один участник и тренер; пакет команды 70000 CRC. Для большего соревновательного вызова Матвею проверить Challenge 9–16, минимум 3; Оскару отдельную Explore, минимум 3. Пакеты двух команд 220000 + 70000 = 290000 CRC, до роботов, компьютеров, подготовки, дороги и неподтверждённых доплат. Медаль участия из пакета не конкурсное место. Опубликованные формы требуют отдельной проверки доступа; личной регистрации пока нет.',
  'Explore conjunta: niños 6–10, mínimo 3, por tanto hermanos necesitan otro integrante y entrenador; paquete de equipo 70000 CRC. Para reto competitivo mayor de Matvey comprobar Challenge 9–16, mínimo 3; para Oscar Explore separada, mínimo 3. Paquetes de dos equipos 220000 + 70000 = 290000 CRC, antes de robots, ordenadores, preparación, viaje y suplementos sin confirmar. Medalla incluida de participación no es puesto competitivo. Verificar acceso a formularios publicados por separado; sin inscripción personal.')),
  dict(period='2027-03-06',title=T('Выбрать основной мартовский старт','Elegir competición principal de marzo'),detail=T('Национальный FLL Costa Rica объявлен на 6 марта; TMR Zacatecas на 3–6 марта. Расписание, допуск и место FLL ещё уточняются. При планировании полной программы одного из этих событий учесть совпадение даты в разных странах.',
   'FLL nacional Costa Rica anunciado para 6 de marzo; TMR Zacatecas para 3–6 de marzo. Horario, admisión y sede FLL aún por confirmar. Para programa completo de uno de estos eventos tener en cuenta coincidencia de fecha en países distintos.')),
  dict(period='2027–2028',title=T('Матвей: подготовка к RoboCup Primary','Matvey: preparación para RoboCup Primary'),detail=new_note)]
 strategy=d['family_strategy'];titles={a['title'] for a in actions};strategy['actions']=[a for a in strategy['actions'] if a['title'] not in titles]+actions;strategy.update(version=160,checked=CHECKED)
 strategy_sources=[src('Costa Rica national FIRST registration and date',FLL),src('Costa Rica FIRST team-package fees',PRICE),src('Americas Primary and cutoff',RCJ),src('Americas guest route',GUEST)]
 claims=[T('BIOGLOW: национальный день 6 марта 2027, дедлайн 30 ноября 2026; Explore и Challenge требуют минимум три ученика.',
  'BIOGLOW: día nacional 6 de marzo de 2027, plazo 30 de noviembre de 2026; Explore y Challenge exigen mínimo tres alumnos.'),
  T('Командные пакеты CRC и число сезонных kits; робот не объявлен явно включённым.',
  'Paquetes por equipo en CRC y cantidad de kits de temporada; robot no declarado expresamente incluido.'),
  T('Primary 10–14 на 1 июля; даты и место редакции 2027 выбираются.',
  'Primary 10–14 al 1 de julio; fechas y sede de edición 2027 por elegir.'),
  T('Для страны без комитета возможен запрос гостевого места; он не даёт права на International.',
  'País sin comité puede solicitar plaza invitada; sin derecho a International.')]
 for source,claim in zip(strategy_sources,claims):source['claim']=claim
 strategy['sources']=list({s['url']:s for s in strategy['sources']+strategy_sources}.values())
 urls={s['url'] for s in d['sources']}
 for item in d['events']:
  if item['id'] not in index and item['id'] not in ['C003','C042']:continue
  for s in [ref(item['title'],item['source'])]+item.get('references',[]):
   if s['url'] not in urls:
    d['sources'].append(dict(url=s['url'],title=s['label'],checked=CHECKED,evidence=T('Официальный источник регионального прохода; оговорки возраста, доступа и сезона сохранены.',
     'Fuente oficial de investigación regional; conservadas condiciones de edad, acceso y temporada.')));urls.add(s['url'])
 for profile in new:
  for s in profile['sources']:
   if s['url'] not in urls:d['sources'].append(dict(url=s['url'],title=s['title'],checked=s['checked'],evidence=T('Источник нового профиля программы; это не независимая мировая аккредитация.',
    'Fuente de nuevo perfil de programa; no es acreditación mundial independiente.')));urls.add(s['url'])
