"""Winter 2026/27 day camps and actual FunTech boarding offers for August 2027."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from camp_europe_v148 import lesson, weekdays

CHECKED='2026-11-05'
SPANISH={}
def T(ru,es): SPANISH[ru]=es; return ru
UWR='https://uniqueworldrobotics.com/winter-camp/'
UWR_REG='https://winter.uwr.ae/'
BLUE='https://www.blueshift.education/'
BLUE_FAQ=BLUE+'apps/frequently-asked-questions'
STEMA='https://surrey.stemalearning.com/product/steam-winter-camp/'
STEMA_TERMS='https://surrey.stemalearning.com/terms-policies-waiver/'
ZEBRA='https://www.zebrarobotics.com/langley/'
FUN='https://funtech.co.uk/'
FUN_OFFERS=FUN+'residentials/offer_search'
FUN_TERMS=FUN+'terms/holiday-camps'
W5='https://w5online.co.uk/whats-on/the-great-christmas-build-off-2026'
BEARS='https://thestemhub.org.uk/events/more-information/threebears-panto-coding-adventure'
BEARS_RES='https://www.getwiththeprogram.org.uk/three-bears-free-resources-2026'
SCIENCE='https://www.sciencenorth.ca/school-break-camps'
BC_TIME='https://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/daylight-saving-time'
BC_NEWS='https://news.gov.bc.ca/releases/2026AG0013-000209'
BC_TIME_NOTE=T('Pacific time для Surrey / Langley: UTC-7 круглый год после 8 марта 2026; 1 ноября 2026 часы не переводятся. UTC рассчитан по официальной реформе, независимо от старой базы часовых поясов компьютера. Исключения других районов провинции не перенесены на эти две площадки.',
 'Pacific time para Surrey / Langley: UTC-7 todo el año después del 8 de marzo de 2026; el 1 de noviembre de 2026 no cambian los relojes. UTC calculado según reforma oficial, independiente de base horaria antigua del ordenador. Excepciones de otras regiones provinciales no se trasladan a estas dos sedes.')
LANG=T('Сайт и материалы на английском; отдельное прямое подтверждение языка преподавания для этой смены не найдено. EN/ES обучение пока не подтверждено.',
 'Web y materiales en inglés; sin localizar confirmación expresa separada del idioma de enseñanza de esta sesión. Enseñanza EN/ES aún sin confirmar.')
GATE=T('Подтвердить язык преподавателя, иностранный индивидуальный приём, уровень после трёх лет соревнований и место. Заявки и оплаты не выполнялись.',
 'Confirmar idioma docente, admisión extranjera individual, nivel tras tres años de competiciones y plaza. Sin solicitudes ni pagos.')
GRADE=T('Допуск по реальному школьному классу и согласованию уровня; класс детей неизвестен, возраст сам по себе его не доказывает.',
 'Admisión según curso escolar real y nivel acordado; cursos de los niños desconocidos, la edad por sí sola no los acredita.')
TRIP=T('Жильё семьи, поездка, питание вне включений и окончательный счёт отдельно.',
 'Alojamiento familiar, viaje, comidas fuera de inclusiones y factura final aparte.')
BLUE_TERMS=T('Camp FAQ: отмена за 14+ дней — полный возврат либо кредит; за 13–7 дней — 50% возврата либо полный кредит; внутри недели — кредит без cash refund. Первому клиенту после первого дня обещан возврат оставшихся дней, после начала второго — кредит. Пропуск дня, опоздание и ранний уход не возмещаются. CampShift за 7+ дней зависит от мест; кредит только до конца календарного года. Проверить применимость к декабрю; договор не принимался.',
 'Camp FAQ: cancelación con 14+ días — devolución total o crédito; con 13–7 — devolución 50% o crédito total; dentro de una semana — crédito sin cash refund. Primer cliente tras primer día: devolución de días restantes; desde segundo día: crédito. Ausencias, retraso y salida anticipada sin reembolso. CampShift con 7+ días sujeto a plazas; crédito solo hasta fin del año natural. Confirmar aplicación a diciembre; contrato sin aceptar.')
STEMA_CANCEL=T('Camp terms, обновлены 22 июля 2026: полная оплата при регистрации; отмена за 3+ недели — удержание CAD 20, за 2–3 недели — CAD 50, внутри 14 дней и после старта возврата нет. Перевод зависит от мест. Налоги не включены согласно price specification; итоговую ставку подтвердить.',
 'Camp terms, actualizados el 22 de julio de 2026: pago total al inscribir; cancelación con 3+ semanas — retención CAD 20, con 2–3 semanas — CAD 50, dentro de 14 días y tras inicio sin devolución. Cambio sujeto a plazas. Impuestos excluidos según price specification; confirmar tipo final.')
ZEBRA_CANCEL=T('Camp policy: отмена за 3+ недели — возврат минус CAD 50; ближе к началу без возврата. Погодное закрытие лагеря не даёт makeup. Правила ежемесячного курса не заменяют правила лагеря.',
 'Camp policy: cancelación con 3+ semanas — devolución menos CAD 50; más cerca del inicio sin devolución. Cierre meteorológico del campamento sin makeup. Reglas de curso mensual no sustituyen reglas del campamento.')
FUN_CANCEL=T('Промо November Sale: GBP 1095 вместо стандартных 1595 за один заезд; срок окончания скидки не установлен. Terms: Flash Sale невозвратен; Early Bird / full fee — аванс невозвратен, за 40+ дней возврат минус аванс, за 39–31 день 50% минус аванс, за 30 и менее без возврата. Определить договорную категорию November Sale. Swap до двух недель зависит от мест; минимум четыре ученика для запуска. GBP 50 deposit не полная цена. Договор и согласия не принимались.',
 'Promoción November Sale: GBP 1095 frente a 1595 estándar por estancia; sin fecha final de descuento acreditada. Terms: Flash Sale no reembolsable; Early Bird / full fee — depósito no reembolsable, con 40+ días devolución menos depósito, con 39–31 días 50% menos depósito, con 30 o menos sin devolución. Determinar categoría contractual de November Sale. Swap hasta dos semanas sujeto a plazas; mínimo cuatro alumnos para apertura. GBP 50 deposit no es precio completo. Sin aceptar contrato ni consentimientos.')

def source(title,url):return dict(title=title,url=url,checked=CHECKED)
def fit(status,ru,es):return dict(status=status,detail=T(ru,es))
def merge(p,rows):p['sources']=list({s['url']:s for s in p['sources']+rows}.values())
def base(ident,slug,provider,country,iso,place,age,themes,formats=None):
 return dict(id=ident,slug=slug,provider=provider,country=country,iso=iso,place=place,age=age,themes=themes,formats=formats or ['day'],
  language=LANG,confirmed_instruction_languages=[],language_evidence_role='unconfirmed',programme='',
  timing=dict(status='published_2026_27',label='',sessions=[],session_details=[],variant_keyed=True),
  price=dict(year=2026,currency='',amount=None,unit='programme',label='',included='',extras=TRIP,deposit=''),
  accommodation=T('Дневная программа без пансиона.','Programa diurno sin residencia.'),family_fit={k:dict(status='conditional',detail=GRADE) for k in ['matvey','oscar']},
  editorial_reason=T('Сравнивать содержание, язык, реальную возрастную группу и итоговую цену. Учебный проект не международная медаль; независимое место в мировом рейтинге не установлено.',
   'Comparar contenido, idioma, grupo de edad real y precio final. Proyecto educativo no es medalla internacional; sin puesto acreditado en ranking mundial independiente.'),
  shortlist=['technical'],questions=[GATE,LANG],sources=[],checked=CHECKED)
def add(p,start,end,label,price,url,key,begin=None,finish=None,zone=None,**extra):
 v=dict(start=start,end=end,label=label,price=price,source=url,formats=p['formats'],variant_key=key,date_scope='camp_session',**extra)
 if begin:
  days=[start] if start==end else weekdays(start,end)
  v.update(date_scope='session_days',sessions=[lesson(day,begin,finish,zone,p['programme']) for day in days])
 p['timing']['sessions'].append([start,end]);p['timing']['session_details'].append(v)

def make_profiles():
 out=[]
 for ident,group,age in [('CP1190','Cadets','5–7'),('CP1191','Pioneers','8–11')]:
  p=base(ident,'uwr-dubai-winter-'+group.lower(),'Unique World Robotics · '+group,T('ОАЭ','Emiratos Árabes Unidos'),'ARE','Dubai · Al Karama / JVC',age,['robotics','coding','ai'] if group=='Pioneers' else ['robotics','coding'])
  p['timing'].update(status='partial_2026',label=T('КОНФЛИКТ: основная страница 14–25 декабря 2026, связанная winter.uwr.ae 14–30 декабря. Обе обещают две недели, пять дней в неделю, 09:00–13:00. Точные смены и площадки не согласованы; в календарь даты не поставлены.',
   'CONFLICTO: página principal 14–25 de diciembre de 2026, winter.uwr.ae enlazada 14–30 de diciembre. Ambas anuncian dos semanas, cinco días semanales, 09:00–13:00. Sesiones y sedes exactas sin conciliar; sin fechas en calendario.'))
  p['programme']=T('Cadets 5–7: танцующий / рисующий робот, простые музыкальные цепи, Ferris wheel, механический корабль и анимация. Python старшего Architects 12+ сюда не переносится.',
   'Cadets 5–7: robot que baila / dibuja, circuitos musicales sencillos, Ferris wheel, barco mecánico y animación. Python de Architects 12+ no se traslada a este grupo.') if group=='Cadets' else T('Pioneers 8–11: robot drummer, управление рисунком через AI / лицо, синхронизированные робосветильники, механический корабль и 3D art. Сложность конкретного проекта согласовать.',
   'Pioneers 8–11: robot drummer, dibujo controlado con AI / rostro, luces robóticas sincronizadas, barco mecánico y 3D art. Acordar dificultad de proyecto concreto.')
  p['price'].update(currency='AED',label=T('Тариф не опубликован; бесплатным не считать.','Tarifa sin publicar; no considerar gratuito.'),included=T('Описание занятий; предоставление персонального устройства не обещано.',
   'Descripción de actividades; sin prometer dispositivo personal.'),extras=T('Обязателен заряженный ноутбук или iPad с зарядкой / адаптерами. Для iPad перечислены LEGO Education SPIKE, Microbit, MatataCode (VinciBot), PictoBlox / Junior. Еда, вода и блокнот с собой; питание не предоставляется. Дополнительные материалы могут сообщить позднее.',
   'Obligatorio portátil o iPad cargado con cargador / adaptadores. Para iPad se indican LEGO Education SPIKE, Microbit, MatataCode (VinciBot), PictoBlox / Junior. Llevar comida, agua y cuaderno; sin comida incluida. Pueden comunicar materiales adicionales después.'),deposit=T('Цена, налоги, возвраты и правила выбранной площадки не установлены.',
   'Precio, impuestos, devoluciones y reglas de sede elegida sin establecer.'))
  p['accommodation']=T('День: UWR Al Karama либо ERYX Circle Mall JVC; распределение группы по площадкам подтвердить.',
   'Diurno: UWR Al Karama o ERYX Circle Mall JVC; confirmar sede del grupo.')
  p['family_fit']=dict(matvey=fit('not_eligible','Матвею 9, Cadets максимум 7.','Matvey tiene 9, Cadets máximo 7.') if group=='Cadets' else fit('candidate','Матвею 9, подходит Pioneers 8–11 по возрасту.','Matvey tiene 9, cumple Pioneers 8–11 por edad.'),oscar=fit('candidate','Оскару 6, подходит Cadets 5–7 по возрасту.','Oscar tiene 6, cumple Cadets 5–7 por edad.') if group=='Cadets' else fit('later','Оскару 6, Pioneers начинается с 8; выбирать Cadets.','Oscar tiene 6, Pioneers desde 8; elegir Cadets.'))
  p['questions'] += [p['timing']['label'],p['price']['extras']]
  p['sources']=[source('Winter Camp 2026',UWR),source('Linked winter page · conflicting final day',UWR_REG)];out.append(p)
 blue=[('CP1192','winter-wonder-workshop-ages-5-8',True,'2026-12-14','2026-12-18',400),('CP1193','december-workshop-senior-8-14',False,'2026-12-14','2026-12-18',400),('CP1194','winter-workshop-ages-5-8-two-days',True,'2026-12-21','2026-12-22',160),('CP1195','winter-workshop-21st-22nd-december-senior',False,'2026-12-21','2026-12-22',160)]
 for ident,handle,junior,start,end,amount in blue:
  url=BLUE+'products/'+handle
  p=base(ident,'blueshift-'+handle,'BlueShift · '+('Junior 5–8' if junior else 'Senior 8–14'),T('Великобритания','Reino Unido'),'GBR','London · Notting Hill Prep', '5–8' if junior else '8–14',['robotics','coding','games','design'])
  if start=='2026-12-14':
   p['programme']=T('Junior 14–18 декабря: понедельник Jingle-bots, вторник Merry Minecraft, среда Handcrafted Holiday Animatronics, четверг Sleigh Racing Robotics, пятница Digital Arctic Animation. Тематические учебные дни, не квалификация международной лиги.',
    'Junior 14–18 de diciembre: lunes Jingle-bots, martes Merry Minecraft, miércoles Handcrafted Holiday Animatronics, jueves Sleigh Racing Robotics, viernes Digital Arctic Animation. Días educativos temáticos, sin clasificación de liga internacional.') if junior else T('Senior 14–18 декабря: понедельник Jingle-bots, вторник Merry Minecraft, среда Young Architects / TinkerCAD, четверг Python Wonderland, пятница Vibe Coding. Это отдельное содержание старшего потока; младшая animatronics-программа его не заменяет.',
    'Senior 14–18 de diciembre: lunes Jingle-bots, martes Merry Minecraft, miércoles Young Architects / TinkerCAD, jueves Python Wonderland, viernes Vibe Coding. Contenido específico del grupo mayor; programa menor de animatronics no lo sustituye.')
  else:
   p['programme']=T('Junior 21–22 декабря: Jingle-bots в понедельник и Sleigh Racing Robotics во вторник. Два тематических учебных дня, не международный конкурс.',
    'Junior 21–22 de diciembre: Jingle-bots lunes y Sleigh Racing Robotics martes. Dos días educativos temáticos, no concurso internacional.') if junior else T('Senior 21–22 декабря: Winter Game Design Jam в понедельник и Frosty Micro:bit во вторник. Два разных проекта в одном пакете; jam не объявлен официальной международной лигой.',
    'Senior 21–22 de diciembre: Winter Game Design Jam lunes y Frosty Micro:bit martes. Dos proyectos distintos en paquete; jam no declarado liga internacional oficial.')
  p['timing']['label']=T('Подтверждённые декабрьские даты 2026. Учебный день 10:00–16:00, прибытие 09:00–10:00; в timed календаре только 10:00–16:00. Пакет и билет на отдельный день — альтернативы одной программы.',
   'Fechas de diciembre de 2026 confirmadas. Jornada educativa 10:00–16:00, llegada 09:00–10:00; calendario timed solo 10:00–16:00. Paquete y billete diario son alternativas de mismo programa.')
  p['price'].update(currency='GBP',amount=amount,unit='week' if amount==400 else 'two_days',label=T('GBP 400 за пять дней; 4 дня тоже 400, 3 дня 300, 2 дня 200, 1 день 100. Пакет 21–22 декабря GBP 160, один день 100. Прежняя зачёркнутая цена не текущий тариф.',
   'GBP 400 por cinco días; 4 días también 400, 3 días 300, 2 días 200, 1 día 100. Paquete 21–22 de diciembre GBP 160, un día 100. Precio anterior tachado no es tarifa vigente.'),included=T('Ноутбуки / iPad на площадке и обучение включены; опция borrow laptop GBP 0. Своё устройство необязательно. Перекусы указаны в FAQ.',
   'Portátiles / iPad en sede y enseñanza incluidos; opción borrow laptop GBP 0. Dispositivo propio opcional. FAQ indica meriendas.'),extras=T('Обед и вода с собой. Налоговый режим и полный семейный счёт подтвердить; sibling discount автоматически не применён.',
   'Llevar almuerzo y agua. Confirmar régimen fiscal y factura familiar final; sin aplicar automáticamente sibling discount.'),deposit=BLUE_TERMS)
  p['accommodation']='Notting Hill Prep · Jane Cameron Building, 124 Lancaster Road, London W11 1QQ'
  p['family_fit']=dict(matvey=fit('not_eligible','Матвею 9, Junior максимум 8.','Matvey tiene 9, Junior máximo 8.') if junior else fit('candidate','Матвею 9, входит в Senior 8–14.','Matvey tiene 9, cumple Senior 8–14.'),oscar=fit('candidate','Оскару 6: соответствует и заголовку Junior 5–8, и более узкому 5–6 в одном подзаголовке.','Oscar tiene 6: cumple tanto título Junior 5–8 como subtítulo más estrecho 5–6.') if junior else fit('later','Оскару 6, Senior от 8.','Oscar tiene 6, Senior desde 8.'))
  p['questions'].append(T('Junior содержит подзаголовок 5–6 при заголовке 5–8; у Senior двух дней ошибочные младшие product tags. Возраст принят по заголовку и описанию, не по техническим tags. Точный состав группы подтвердить.',
   'Junior contiene subtítulo 5–6 frente a título 5–8; Senior de dos días tiene product tags menores erróneos. Edad tomada de título y descripción, no de tags técnicos. Confirmar composición exacta.'))
  p['sources']=[source('Selected winter product',url),source('December 2026 campaign',BLUE+'pages/december-camp-2026'),source('Camp FAQ and cancellation',BLUE_FAQ)]
  add(p,start,end,'Junior' if junior else 'Senior','GBP '+str(amount),url,'package','10:00','16:00','Europe/London');out.append(p)
 for ident,junior in [('CP1196',True),('CP1197',False)]:
  p=base(ident,'stema-surrey-winter-'+('junior' if junior else 'explorer'),'STEMA Surrey · '+('Junior K–2' if junior else 'Explorer 3–6'),T('Канада','Canadá'),'CAN','Surrey · 703–9686 137 Street','Grades K–2' if junior else 'Grades 3–6',['robotics','coding','design'] if junior else ['robotics','coding','ai','games'])
  p['programme']=T('Junior K–2: первая неделя — роботы / датчики / простые машины утром и 3D art на iPad после обеда; вторая — LEGO конструкции утром, ScratchJr истории и анимация после обеда. Это школьные уровни, не возраст 0–2.',
   'Junior K–2: primera semana robots / sensores / máquinas sencillas por mañana y 3D art con iPad por tarde; segunda LEGO estructuras por mañana, historias y animación ScratchJr por tarde. Niveles escolares, no edad 0–2.') if junior else T('Explorer Grades 3–6: первая неделя VEX robotics утром, Hour of AI / machine learning и computer vision после обеда; вторая Minecraft Education CyberFUNdamentals утром, Scratch 3 games после обеда. Full day объединяет два блока и обеденный перерыв.',
   'Explorer Grades 3–6: primera semana VEX robotics por mañana, Hour of AI / machine learning y computer vision por tarde; segunda Minecraft Education CyberFUNdamentals por mañana, Scratch 3 games por tarde. Full day combina dos bloques y pausa de almuerzo.')
  p['timing']['label']=T('21–24 и 28–31 декабря 2026, по четыре дня. AM 09–12, PM 13–16, full 09–16; обеденный перерыв 12–13 не учебный час. Старый доступный вариант декабря 2025 исключён.',
   '21–24 y 28–31 de diciembre de 2026, cuatro días cada semana. AM 09–12, PM 13–16, full 09–16; pausa 12–13 no es hora lectiva. Variante antigua disponible de diciembre de 2025 excluida.')
  p['price'].update(currency='CAD',amount=159,unit='half_day_week',label=T('CAD на ребёнка: одна четырёхдневная неделя AM 159, PM 159, full 299; обе недели AM 299, PM 299, full 589. Две отдельные full недели 598, bundle 589; пакет не новая отдельная смена.',
   'CAD por niño: semana de cuatro días AM 159, PM 159, full 299; ambas semanas AM 299, PM 299, full 589. Dos semanas full separadas 598, bundle 589; paquete no es sesión independiente nueva.'),included=T('Образовательные материалы, роботы, киты и craft supplies включены. Использование iPad описано; необходимость личного устройства подтвердить.',
   'Material educativo, robots, kits y craft supplies incluidos. Se describe uso de iPad; confirmar si exige dispositivo propio.'),extras=T('Обед, перекусы и вода с собой; налоги сверх опубликованной цены, точную ставку согласовать.',
   'Llevar almuerzo, meriendas y agua; impuestos adicionales al precio publicado, acordar tipo exacto.'),deposit=STEMA_CANCEL)
  p['sources']=[source('STEAM Winter Camp · current variants',STEMA),source('Camp terms · updated 22 July 2026',STEMA_TERMS)]
  for start,end in [('2026-12-21','2026-12-24'),('2026-12-28','2026-12-31')]:
   for key,b,e,amount in [('am','09:00','12:00',159),('pm','13:00','16:00',159),('full','09:00','16:00',299)]:add(p,start,end,key.upper(),'CAD '+str(amount),STEMA,start.replace('-','')+'-'+key,b,e,'America/Vancouver')
  out.append(p)
 evidence=json.loads((Path(__file__).resolve().parents[1]/'data/winter-camp-native-schedules-v158.json').read_text())
 for ident,key,code,name,age in [('CP1198','building','SR150','Building Enthusiasts','Grades 1–3 · approx 6–8'),('CP1199','adventures','SR350','Adventures in Building','Grades 3–4 · approx 8–9'),('CP1200','engineer','SR400','Robotics Engineer I Bootcamp','Grades 4–9 · approx 9–14')]:
  ev=evidence['zebra'][key];url=ev['url']
  p=base(ident,'zebra-langley-'+key,'Zebra Robotics Langley · '+code+' '+name,T('Канада','Canadá'),'CAN','Langley · Unit 108, 20486 64 Avenue',age,['robotics'] if key=='building' else ['robotics','coding'])
  descriptions={
   'building':T('Powered LEGO машины, моторы, батарейные блоки и механизмы. Это начальное конструирование; программирование блоками для SR150 не обещано.',
    'Máquinas LEGO motorizadas, motores, baterías y mecanismos. Construcción inicial; sin prometer programación por bloques para SR150.'),
   'adventures':T('LEGO WeDo, моторы и датчики, модели и программирование блоками. Для ребёнка с опытом соревнований согласовать сложность и школьный уровень.',
    'LEGO WeDo, motores y sensores, modelos y programación por bloques. Acordar dificultad y nivel escolar para niño con experiencia competitiva.'),
   'engineer':T('LEGO SPIKE Prime: rover, датчики, навигация и линия, передачи; уровни 1–3. Прогрессия к команде соревнований описана отдельно и не гарантируется одной неделей.',
    'LEGO SPIKE Prime: rover, sensores, navegación y línea, engranajes; niveles 1–3. Progresión a equipo competitivo descrita aparte, sin garantizarla por una semana.')}
  p['programme']=descriptions[key]
  p['timing']['label']=T('13 опубликованных периодов с декабря 2026 по сентябрь 2027; это зимние, весенние и летние варианты трёх программ, не 117 независимых лагерей. Отдельные субботы 9 января / 20 февраля. Неделя 2–6 августа не опубликована и не добавлена.',
   '13 periodos publicados de diciembre de 2026 a septiembre de 2027; opciones invernales, primaverales y estivales de tres programas, no 117 campamentos independientes. Sábados sueltos 9 de enero / 20 de febrero. Semana 2–6 de agosto sin publicar ni añadir.')
  p['price'].update(year=2027,currency='CAD',amount=None,unit='session',label=T('CAD до налогов: зимние 4 дня full 396 / half 198; один день 99 / 50; весенние 4 дня 410 / 240; 5 дней 495 / 290. Применён тариф фактического периода и batch type, не линейная экстраполяция.',
   'CAD antes de impuestos: invierno 4 días full 396 / half 198; un día 99 / 50; primavera 4 días 410 / 240; 5 días 495 / 290. Tarifa del periodo y batch type reales, sin extrapolación lineal.'),included=T('Занятия в центре. Личный компьютер / комплект и питание для очного лагеря прямо не уточнены; Windows-требования виртуального курса сюда не переносить.',
   'Clases en centro. Ordenador / kit personal y comida de campamento presencial sin aclarar expresamente; no trasladar requisitos Windows del curso virtual.'),extras=T('Нативная branch_tax 0.05 и fee_tax_ind 1: расчёт 5% показан как расчёт по настройке оператора, итог подтвердить invoice. added_fee — необязательная продлёнка full / PM до 17:30: 10 CAD за фактический день (40 / 50 за 4 / 5 дней). Для AM и двух отдельных суббот продлёнка не предложена.',
   'Configuración nativa branch_tax 0.05 y fee_tax_ind 1: cálculo 5% mostrado como cálculo según configuración del operador, confirmar invoice final. added_fee es cuidado opcional full / PM hasta 17:30: 10 CAD por día real (40 / 50 por 4 / 5 días). AM y dos sábados sueltos sin cuidado ampliado ofrecido.'),deposit=ZEBRA_CANCEL)
  p['sources']=[source('Selected course and native session / fee data',url),source('Camp-specific cancellation policy',ZEBRA+'policy'),source('FAQ · distinguish virtual device requirements','https://www.zebrarobotics.com/faq')]
  for week in ev['weeks']:
   for v in week['variants']:
    add(p,week['start'],week['end'],code+' · '+v['key'].upper(),'CAD '+str(v['amount']),url,week['start'].replace('-','')+'-'+v['key'],v['start_time'],v['end_time'],'America/Vancouver',proof=T('Даты, формат и тариф сопоставлены с нативными sessions и detailedFees: число дней, delivery_type_id, half_day_ind и camp_type_id. Открытый вариант не подтверждает приём семьи.',
     'Fechas, formato y tarifa cotejados con sessions y detailedFees nativos: número de días, delivery_type_id, half_day_ind y camp_type_id. Opción abierta no confirma admisión familiar.'))
  out.append(p)
 p=base('CP1201','w5-christmas-minecraft-2026','W5 LIFE · The Great Christmas Build-Off',T('Великобритания','Reino Unido'),'GBR','Belfast · W5 LIFE, The O2 Belfast, 2 Queens Quay BT3 9QQ','8+',['coding','games'])
 p['catalog_participation']='holiday_workshop'
 p['programme']=T('Двухчасовой Minecraft Education Christmas build-off, праздничные постройки и творческая работа. Дружеское задание не официальная международная лига. Содержание повторяется во всех четырёх сеансах: организатор просит выбрать только один.',
  'Christmas build-off de Minecraft Education de dos horas, construcciones festivas y creatividad. Reto amistoso no es liga internacional oficial. Contenido repetido en las cuatro sesiones: organizador pide elegir solo una.')
 p['family_fit']=dict(matvey=fit('candidate','Матвею 9: соответствует 8+.','Matvey tiene 9: cumple 8+.'),oscar=fit('later','Оскару 6: ниже 8+, младший доступ не обещан.','Oscar tiene 6: menor de 8+, sin prometer excepción.'))
 p['timing']['label']=T('12 и 19 декабря 2026: 10–12 либо 13:30–15:30. Прибытие за 15 минут, забрать к окончанию. Всего 16 участников в сеансе — вместимость, не остаток мест.',
  '12 y 19 de diciembre de 2026: 10–12 o 13:30–15:30. Llegar 15 minutos antes y recoger al final. 16 participantes por sesión es capacidad, no plazas restantes.')
 p['price'].update(currency='GBP',amount=10,unit='session',label=T('GBP 10 на ребёнка за один двухчасовой сеанс.','GBP 10 por niño por sesión de dos horas.'),included=T('Участие в workshop; питание и свободный вход в остальной W5 не заявлены.',
  'Participación en workshop; sin acreditar comida ni entrada general a W5.'),deposit=T('Сроки отмены выбранного билета и оборудование подтвердить до оплаты.','Confirmar cancelación del billete elegido y equipo antes de pagar.'))
 p['sources']=[source('Christmas Build-Off 2026 · age, dates and price',W5)]
 for day in ['2026-12-12','2026-12-19']:
  for k,b,e in [('am','10:00','12:00'),('pm','13:30','15:30')]:add(p,day,day,'Minecraft · '+k.upper(),'GBP 10',W5,day.replace('-','')+'-'+k,b,e,'Europe/London')
 out.append(p)
 p=base('CP1202','three-bears-coding-show-2026','STEM Hub / Get with the Program · Three Bears',T('Великобритания','Reino Unido'),'GBR',T('Онлайн · Microsoft Teams Live','En línea · Microsoft Teams Live'),T('Целевая группа 5–7 / KS1','Grupo objetivo 5–7 / KS1'),['coding'],['online'])
 p['catalog_participation']='online'
 p['programme']=T('Бесплатная coding pantomime: алгоритмы и debugging, затем печатные задания и Bee-Bot grid. Примерно 25 минут шоу с вступлением в 30-минутном слоте; это не многодневный лагерь. Ресурсы и trailer не означают запись всей трансляции или доступ on demand.',
  'Coding pantomime gratuita: algoritmos y debugging, después fichas imprimibles y Bee-Bot grid. Unos 25 minutos de show con introducción en franja de 30 minutos; no campamento de varios días. Recursos y trailer no significan grabación completa ni acceso on demand.')
 p['timing']['label']=T('10 декабря 2026: host и заголовок ресурса 09:15–09:45 AM; ниже в ресурсе ошибочно 9:15 PM. Часовой пояс прямо не указан: сохранена дата без выдуманного UTC / времени Коста-Рики.',
  '10 de diciembre de 2026: host y cabecera del recurso 09:15–09:45 AM; texto inferior del recurso dice 9:15 PM por error. Zona horaria no explícita: fecha conservada sin UTC / hora de Costa Rica inventados.')
 p['family_fit']=dict(matvey=fit('conditional','Матвею 9, старше целевой KS1 5–7: скорее совместный показ с братом, не продвинутый трек и не установленный юридический запрет.','Matvey tiene 9, mayor que objetivo KS1 5–7: posible sesión con hermano, no itinerario avanzado ni prohibición formal acreditada.'),oscar=fit('candidate','Оскару 6, соответствует целевой группе 5–7. Семейный доступ из-за рубежа согласовать.','Oscar tiene 6, cumple objetivo 5–7. Acordar acceso familiar desde extranjero.'))
 p['price'].update(currency='GBP',amount=0,unit='show',label=T('Шоу и задания бесплатно.','Show y fichas gratuitos.'),included=T('Teams Live show и бесплатные printable resources. Сертификат занятия не международная конкурсная награда.',
  'Teams Live show y printable resources gratuitos. Certificado educativo no es premio competitivo internacional.'),extras=T('Нужны интернет, устройство и взрослый для подключения; аккаунт / допуск семьи вне UK не подтверждены.',
  'Requiere internet, dispositivo y adulto para conexión; cuenta / acceso familiar fuera de UK sin confirmar.'),deposit=T('Учительская / семейная регистрация не выполнялась; бесплатность не подтверждает свободный индивидуальный вход.',
  'Sin registro docente / familiar; gratuidad no confirma entrada individual libre.'))
 p['sources']=[source('STEM Hub · date and morning slot',BEARS),source('Resources · header and PM text conflict',BEARS_RES)]
 add(p,'2026-12-10','2026-12-10','Online coding show',T('Бесплатно','Gratis'),BEARS,'show');out.append(p)
 courses=[('CP1203','roblox','roblox-level-1','Roblox Game Designer','8–10',[('2027-08-08','2027-08-13')],['coding','games']),('CP1204','python','python-coder','Python Coder','10–16',[('2027-08-08','2027-08-13'),('2027-08-15','2027-08-20')],['coding']),('CP1205','3d','unreal-game-design','3D Game Design Developer','10–14',[('2027-08-08','2027-08-13')],['coding','games','design']),('CP1206','ai','ai-vibe-coder','AI Vibe Coder','10–16',[('2027-08-08','2027-08-13')],['coding','ai'])]
 for ident,key,handle,name,age,stays,themes in courses:
  url=FUN+'camp_types/view_residential/'+handle
  p=base(ident,'funtech-tonbridge-'+key+'-2027','FunTech Tonbridge · '+name,T('Великобритания','Reino Unido'),'GBR','Tonbridge School · Kent',age,themes,['boarding'])
  content={
   'roblox':T('Roblox Studio: terrain, checkpoints, multiplayer, физические объекты и GUI. Это Game Designer, не отдельный старший Roblox Lua Coder. Курс рекомендует 7–10, но проживание строго от 8: рабочее пересечение 8–10.',
    'Roblox Studio: terrain, checkpoints, multiplayer, objetos físicos y GUI. Game Designer, no curso mayor Roblox Lua Coder. Curso orientativo 7–10, residencia estrictamente desde 8: intersección 8–10.'),
   'python':T('Python: логика, flowcharts / pseudocode, типы данных, переменные, ввод, ветвления, циклы и функции. Не смешивать с Python OOP 11+ и Machine Learning 12+.',
    'Python: lógica, flowcharts / pseudocode, tipos de datos, variables, entradas, decisiones, bucles y funciones. No mezclar con Python OOP 11+ ni Machine Learning 12+.'),
   '3d':T('Визуальные скрипты, переменные, ветвления, циклы, события и 3D-модели для собственной игры. На странице осталось старое обозначение UE4 как latest: реальную версию инструмента уточнить, не утверждать актуальность этой фразы.',
    'Scripts visuales, variables, decisiones, bucles, eventos y modelos 3D para juego propio. Página conserva referencia antigua a UE4 como latest: confirmar versión real sin afirmar vigencia de esa frase.'),
   'ai':T('AI как помощник разработки: prompts, проверка и улучшение результата, библиотеки, assets, version control, документация и webapps. Это создание проектов с AI, не отдельный курс обучения ML-моделей 12+.',
    'AI como asistente de desarrollo: prompts, revisión y mejora de resultados, bibliotecas, assets, version control, documentación y webapps. Creación de proyectos con AI, no curso separado de entrenar modelos ML de 12+.')}
  p['programme']=content[key]
  p['timing'].update(status='published_2027',label=T('Актуальные варианты offer_search: воскресенье–пятница, заезд 17:00 в воскресенье, выезд 16:00 в пятницу. Занятия понедельник–пятница; календарь отражает проживание целым окном, не шесть учебных дней. Старые скрытые даты августа 2020 исключены.',
   'Opciones actuales de offer_search: domingo–viernes, llegada 17:00 domingo, salida 16:00 viernes. Clases lunes–viernes; calendario refleja estancia completa, no seis días lectivos. Fechas antiguas ocultas de agosto de 2020 excluidas.'))
  p['family_fit']=dict(matvey=fit('candidate','Матвею летом 2027 будет 9–10: входит в пансион Roblox 8–10. Самостоятельность, язык и место отдельно.','Matvey en verano de 2027 tendrá 9–10: cumple residencia Roblox 8–10. Autonomía, idioma y plaza aparte.') if key=='roblox' else fit('conditional','Матвею нужен уже исполненный возраст 10 на начало заезда. Год рождения 2017 без даты рождения это не подтверждает.','Matvey debe haber cumplido 10 al inicio de estancia. Año 2017 sin fecha de nacimiento no lo acredita.'),oscar=fit('later','Оскару летом 2027 будет 6–7, ниже пансионного порога 8.','Oscar en verano de 2027 tendrá 6–7, por debajo de mínimo residencial 8.'))
  p['price'].update(year=2027,currency='GBP',amount=1095,unit='stay',label=T('GBP 1095 November Sale на ребёнка за один заезд; обычная цена 1595. FAQ прямо включает VAT. Доступность промо и итоговый счёт подтвердить.',
   'GBP 1095 November Sale por niño / estancia; precio estándar 1595. FAQ incluye VAT expresamente. Confirmar disponibilidad de promoción y factura final.'),included=T('Пансион, три приёма пищи и перекусы, учебные компьютеры, занятия и отдельная круглосуточная pastoral care. Свою технику и дневную аренду GBP 70 к пансионной цене не добавлять.',
   'Residencia, tres comidas y meriendas, ordenadores educativos, clases y pastoral care separada permanente. No añadir dispositivo propio ni alquiler diurno GBP 70 a tarifa residencial.'),extras=T('Airport transfer отдельно: Heathrow / Gatwick GBP 345 в одну сторону, 650 туда-обратно; тариф за journey, число пассажиров и условия уточнить. Страховка, авиабилеты, одежда и пребывание родителей отдельно.',
   'Airport transfer aparte: Heathrow / Gatwick GBP 345 ida, 650 ida y vuelta; tarifa por journey, confirmar pasajeros y condiciones. Seguro, vuelos, ropa y estancia parental aparte.'),deposit=FUN_CANCEL)
  p['accommodation']=T('FunTech использует кампус Tonbridge School; это лагерь внешнего провайдера, не поступление в школу. Общие / отдельные комнаты, общие санузлы, полный пансион.',
   'FunTech utiliza campus de Tonbridge School; campamento de proveedor externo, no admisión escolar. Habitaciones compartidas / individuales, baños compartidos, pensión completa.')
  p['sources']=[source('Actual dated offers and sale price',FUN_OFFERS),source('Subject content and age guide',url),source('Boarding inclusions and transfers',FUN+'residential-kids-coding-camps'),source('VAT and provided residential computers',FUN+'faqs'),source('Holiday camp terms',FUN_TERMS)]
  for start,end in stays:add(p,start,end,name,'GBP 1095 November Sale / 1595 standard · VAT included',FUN_OFFERS,start.replace('-',''))
  out.append(p)
 p=base('CP1207','science-north-robo-ready-9-11','Science North Sudbury · Robo Ready 9–11',T('Канада','Canadá'),'CAN','Sudbury · 100 Ramsey Lake Road','9–11',['robotics','coding'])
 p['language']=T('Лендинг предлагает отдельные English / French потоки; выбран English. Рабочий билет возрастной группы сейчас не открывается, язык и место в новом билете перепроверить.',
  'Landing ofrece grupos English / French separados; elegido English. Billete del grupo de edad ahora no abre; revisar idioma y plaza en nuevo billete.')
 p.update(confirmed_instruction_languages=['EN'],language_evidence_role='primary')
 p['programme']=T('Robo Ready: основы кода, управление разными роботами, движения, решения и задания. Текущий лендинг явно связывает 20 ноября с группами 4–5, 6–8 и 9–11. Старое противоречивое название карточки 9–11 не выдано за исправленный рабочий билет.',
  'Robo Ready: bases de código, control de robots distintos, movimientos, decisiones y retos. Landing actual relaciona expresamente 20 de noviembre con grupos 4–5, 6–8 y 9–11. Título antiguo contradictorio de ficha 9–11 no se presenta como billete operativo corregido.')
 p['family_fit']=dict(matvey=fit('conditional','Матвею уже 9, подходит группа 9–11 по возрасту; актуальная ссылка билета 404, приём / место не подтверждены.','Matvey ya tiene 9, cumple grupo 9–11 por edad; enlace actual de billete 404, admisión / plaza sin confirmar.'),oscar=fit('later','Оскару 6: выбирать отдельное досье Robo Ready 6–8 CP218.','Oscar tiene 6: elegir ficha separada Robo Ready 6–8 CP218.'))
 p['timing'].update(status='partial_2026',label=T('20 ноября 2026 — опубликованный PA Day Robo Ready. Общая площадка принимает 08:30–09:00 и выдаёт детей 16:00–16:30; рабочий билет возрастной группы отсутствует, timed занятие не выдумано.',
  '20 de noviembre de 2026 — PA Day Robo Ready publicado. Sede general recibe 08:30–09:00 y recoge 16:00–16:30; sin billete operativo del grupo, no inventar clase timed.'))
 p['price'].update(currency='',amount=None,unit='day',label=T('Общая таблица PA Day: public $57 / member $51.50. Валюту, налоги и цену нового рабочего билета подтвердить; не считать членскую цену доступной семье.',
  'Tabla general PA Day: public $57 / member $51.50. Confirmar moneda, impuestos y precio del nuevo billete operativo; no dar precio de socio por disponible a familia.'),included=T('Дневная учебная программа; состав техники и питания уточнить.','Programa educativo diurno; confirmar equipo y comidas.'),deposit=T('Проверить новые условия брони и отмены: текущая ссылка 9–11 https://order.sciencenorth.ca/183346/183381 отвечает 404. Согласия и заявка не отправлялись.',
  'Comprobar condiciones actuales de reserva y cancelación: enlace 9–11 https://order.sciencenorth.ca/183346/183381 responde 404. Sin consentimientos ni solicitud.'))
 p['sources']=[source('Current School Break landing · Robo Ready three age groups',SCIENCE)]
 add(p,'2026-11-20','2026-11-20','Robo Ready 9–11',p['price']['label'],SCIENCE,'pa-day',admission_kind='open_application');out.append(p)
 for p in out:
  if p['id'] in ['CP1196','CP1197','CP1198','CP1199','CP1200']:
   p['questions'].append(BC_TIME_NOTE)
   p['sources'] += [source('B.C. official permanent UTC-7 rule',BC_TIME),source('B.C. government announcement · 2 March 2026',BC_NEWS)]
  if p['timing']['status']=='published_2026_27' and p['timing']['sessions'] and all(end<'2027' for start,end in p['timing']['sessions']):p['timing']['status']='published_2026'
 return out

def update_report(r):
 rows={p['id']:p for p in r['profiles']}
 for ident in ['CP296','CP297','CP298']:
  p=rows[ident];p['checked']=CHECKED
  for s in p['sources']:
   if s['url'] in ['https://www.brainstemlearning.ca/programs/winter-camp','https://stemotics.com/product/winter-break-camp/']:s['checked']=CHECKED
 rows['CP296']['family_fit']['oscar']=fit('candidate','Семья сообщила, что Оскару уже 6: Little Brains 4–6 подходит по возрасту.','Familia informó que Oscar ya tiene 6: cumple Little Brains 4–6 por edad.')
 rows['CP297']['family_fit']=dict(matvey=fit('candidate','Семья сообщила, что Матвею уже 9: Specialists 7–11 подходит.','Familia informó que Matvey ya tiene 9: cumple Specialists 7–11.'),oscar=fit('later','Оскару уже 6, Specialists от 7; выбирать Little Brains.','Oscar ya tiene 6, Specialists desde 7; elegir Little Brains.'))
 rows['CP298']['family_fit']=dict(matvey=fit('candidate','Матвею уже 9, соответствует старшему потоку 9–12; опубликованный конфликт цен не разрешён.','Matvey ya tiene 9, cumple grupo mayor 9–12; conflicto publicado de precios sin resolver.'),oscar=fit('candidate','Оскару уже 6, соответствует младшему потоку 4–8; язык и места уточнить.','Oscar ya tiene 6, cumple grupo menor 4–8; confirmar idioma y plazas.'))
 for ident in ['CP296','CP297']:
  merge(rows[ident],[source('Current FAQ · tax exemption and camp cancellation','https://www.brainstemlearning.ca/faqs')])
 p=rows['CP218'];p['checked']=CHECKED
 p['family_fit']=dict(matvey=fit('not_eligible','Матвею уже 9, эта группа 6–8 не подходит; опубликован отдельный 9–11, досье CP1207 с нерабочей ссылкой билета.','Matvey ya tiene 9, este grupo 6–8 no cumple; grupo 9–11 publicado, ficha CP1207 con enlace de billete no operativo.'),oscar=fit('conditional','Оскару уже 6, диапазон 6–8 подходит; прежний билет теперь 404, место и новый билет согласовать.','Oscar ya tiene 6, cumple rango 6–8; billete anterior ahora 404, acordar plaza y billete nuevo.'))
 p['timing']['label']=T('20 ноября 2026. Текущий лендинг ясно перечисляет Robo Ready 4–5 / 6–8 / 9–11. Прежняя ссылка билета 6–8 теперь 404; рабочий билет 9–11 также не найден. Дата лендинга подтверждена, admission и исправление старого билета не подтверждены.',
  '20 de noviembre de 2026. Landing actual enumera claramente Robo Ready 4–5 / 6–8 / 9–11. Enlace anterior de billete 6–8 ahora 404; tampoco localizado billete 9–11 operativo. Fecha del landing confirmada, admisión y corrección del billete antiguo sin confirmar.')
 p['questions'].append(T('v158: получить действующий билет на нужную возрастную English-группу; зимние Robobuilders SPIKE / Tech Lab 12–13 не подменяют детские 6–8 / 9–11.',
  'v158: obtener billete operativo para grupo English de edad correcta; Robobuilders SPIKE / Tech Lab 12–13 de invierno no sustituyen grupos 6–8 / 9–11.')) if not any('v158:' in s for s in p['questions']) else None
 merge(p,[source('Current landing · all three Robo Ready age groups',SCIENCE)])
 p=rows['CP020'];p['checked']=CHECKED;p.update(confirmed_instruction_languages=['EN'],language_evidence_role='primary',language=T('Tech Camp прямо указывает: всё обучение на английском, рекомендуется B1+ в устной и письменной речи; формальных уроков английского нет. Это подтверждение оператора, не гарантия конкретной новой смены.',
  'Tech Camp indica expresamente: toda enseñanza en inglés, recomienda B1+ oral y escrito; sin clases formales de inglés. Confirmación del operador, no garantía de sesión nueva concreta.'))
 p['age']='9–17';p['timing']['label']=T('Winchester / Sparsholt: пасхальный и августовский пансион описан, но точные будущие даты и тариф выбранного курса в прочитанной booking-странице не показаны. В календарь не добавлены.',
  'Winchester / Sparsholt: residencia en Pascua y agosto descrita, pero booking leído no muestra fechas futuras exactas ni tarifa del curso elegido. Sin añadir al calendario.')
 merge(p,[source('Overseas campers · all-English and B1+','https://www.techcamp.org.uk/info/overseas-campers'),source('Residential format and venue','https://www.techcamp.org.uk/info/residential-camps'),source('Booking shell · ages 9–17','https://booking.techcamp.org.uk?location=Winchester')])
 p=rows['CP375'];p['checked']=CHECKED;p['timing'].update(status='partial_2027',label=T('Обзор оператора: подтверждены предложения Tonbridge 8–13 и 15–20 августа 2027. Конкретные Roblox, Python, 3D и AI заезды в досье CP1203–CP1206; этот обзор не создаёт повторную календарную смену.',
  'Resumen del operador: ofertas Tonbridge 8–13 y 15–20 de agosto de 2027 confirmadas. Estancias Roblox, Python, 3D y AI concretas en fichas CP1203–CP1206; resumen sin crear estancia duplicada.'))
 p['price'].update(year=2027,currency='GBP',amount=1095,label=T('November Sale GBP 1095 / standard 1595 за заезд, VAT включён; выбранный предмет и наличие места отдельно.',
  'November Sale GBP 1095 / estándar 1595 por estancia, VAT incluido; asignatura elegida y plaza aparte.'),deposit=FUN_CANCEL)
 p['price']['extras']=T('Текущая таблица Heathrow / Gatwick GBP 345 one-way / 650 return за journey; число пассажиров и окончательный тариф подтвердить. Поездка, страховка и проживание родителей отдельно.',
  'Tabla actual Heathrow / Gatwick GBP 345 one-way / 650 return por journey; confirmar pasajeros y tarifa final. Viaje, seguro y alojamiento parental aparte.')
 merge(p,[source('Actual residential dates and offers',FUN_OFFERS),source('Current residential inclusions',FUN+'residential-kids-coding-camps'),source('VAT and provided residential computers',FUN+'faqs'),source('Camp terms',FUN_TERMS)])
 new=make_profiles();index={p['id']:p for p in new};old={p['id'] for p in r['profiles']}
 r['profiles']=[index.get(p['id'],p) for p in r['profiles']]+[p for p in new if p['id'] not in old]
 r['counts'].update(dossiers=len(r['profiles']),countries=len({p['iso'] for p in r['profiles']}),by_status=dict(Counter(p['timing']['status'] for p in r['profiles'])),source_urls=len({s['url'] for p in r['profiles'] for s in p['sources']}))
 countries=Counter(p['country'] for p in r['profiles']);r['countries']=[dict(country=k,count=v) for k,v in sorted(countries.items())]
 r.update(version=158,asof=CHECKED)

def enrich_v158(d):
 offers=[]
 def offer(ident,slug,label,currency,base_by_child,sessions,sources,gate,**extra):
  offers.append(dict(id=ident,slug=slug,label=label,currency=currency,price_year=2027 if all(a>='2027' for a,b in sessions) else 2026,format=extra.pop('format','day'),children=list(base_by_child),base_by_child=base_by_child,discount_second=0,required=extra.pop('required',[]),unknown_required=extra.pop('unknown_required',[]),optional=extra.pop('optional',[]),unknown_trip=['travel','lodging','misc'],sessions=sessions,sources=sources,checked=CHECKED,gate=gate,deposit_note=extra.pop('deposit_note',T('Точный договор и места подтвердить; заявка не отправлялась.','Confirmar contrato exacto y plazas; sin solicitud.')),included=extra.pop('included',T('Учебная программа; конкретные включения в досье.','Programa educativo; inclusiones concretas en ficha.')),scope=extra.pop('scope',TRIP),**extra))
 for suffix,slug,amount,sessions in [('week','blueshift-december-workshop-senior-8-14',400,[['2026-12-14','2026-12-18']]),('two-days','blueshift-winter-workshop-21st-22nd-december-senior',160,[['2026-12-21','2026-12-22']])]:
  offer('blueshift-both-'+suffix+'-2026',slug,'BlueShift · Junior + Senior · '+T('оба ребёнка','ambos niños'),'GBP',dict(matvey=amount,oscar=amount),sessions,[BLUE+'pages/december-camp-2026',BLUE_FAQ],GATE,unknown_required=[dict(id='tax',label=T('Налоговый режим и окончательный счёт','Régimen fiscal y factura final'),unit='amount',rate=1,min=0)],deposit_note=BLUE_TERMS,included=T('Две отдельные возрастные группы; компьютеры включены. Обед с собой.','Dos grupos de edad separados; ordenadores incluidos. Llevar almuerzo.'))
 for key,amount,sessions in [('am-week',159,[['2026-12-21','2026-12-24'],['2026-12-28','2026-12-31']]),('full-week',299,[['2026-12-21','2026-12-24'],['2026-12-28','2026-12-31']]),('full-two-weeks',589,[['2026-12-21','2026-12-31']])]:
  offer('stema-surrey-both-'+key+'-2026','stema-surrey-winter-explorer','STEMA Surrey · '+key+' · '+T('оба ребёнка','ambos niños'),'CAD',dict(matvey=amount,oscar=amount),sessions,[STEMA,STEMA_TERMS],GRADE+' '+GATE,unknown_required=[dict(id='tax',label=T('Дополнительные налоги: точную ставку подтвердить','Impuestos adicionales: confirmar tipo exacto'),unit='amount',rate=1,min=0)],deposit_note=STEMA_CANCEL,scope=T('Одна неделя выбирается из двух; пакет обеих недель содержит восемь занятий, 25–27 декабря не посещение. Это альтернатива двум отдельным оплатам, не дополнительный лагерь.',
   'Se elige una de dos semanas; paquete de ambas contiene ocho jornadas, 25–27 de diciembre sin asistencia. Alternativa a dos pagos separados, no campamento adicional.'))
 for key,amount,tax,care in [('am',198,19.8,80),('pm',198,19.8,80),('full',396,39.6,80)]:
  offer('zebra-langley-both-winter-'+key+'-2026','zebra-langley-adventures','Zebra Langley · '+key+' · '+T('оба ребёнка / 4 дня','ambos niños / 4 días'),'CAD',dict(matvey=amount,oscar=amount),[['2026-12-21','2026-12-24']],[ZEBRA+'camps/58',ZEBRA+'camps/61',ZEBRA+'policy'],GRADE+' '+GATE,required=[dict(id='tax',label=T('Расчёт 5% по branch_tax оператора; итог invoice подтвердить','Cálculo 5% según branch_tax del operador; confirmar invoice final'),amount=tax)],optional=[] if key=='am' else [dict(id='extended',label=T('Продлёнка до 17:30 для двух детей, 4 дня · до налога','Cuidado hasta 17:30 para dos niños, 4 días · antes de impuesto'),amount=care)],deposit_note=ZEBRA_CANCEL,scope=T('Предполагаются согласованные школьные группы обоих детей. AM и PM — альтернативные полдня, не оба блока; optional продлёнка недоступна AM. Её налог и личные материалы уточнить.',
   'Se suponen grupos escolares acordados de ambos niños. AM y PM son medias jornadas alternativas, no ambos bloques; cuidado opcional no disponible AM. Confirmar impuesto de ese extra y materiales personales.'))
 offer('funtech-tonbridge-roblox-matvey-2027','funtech-tonbridge-roblox-2027','FunTech Roblox · Tonbridge · '+T('Матвей / пансион','Matvey / residencia'),'GBP',dict(matvey=1095),[['2027-08-08','2027-08-13']],[FUN_OFFERS,FUN+'faqs',FUN_TERMS],T('Матвею летом 2027 9–10, подходит Roblox 8–10. Оскар 6–7 в пансион не допускается. Язык и самостоятельность подтвердить.',
  'Matvey en verano de 2027 tendrá 9–10, cumple Roblox 8–10. Oscar de 6–7 no cumple residencia. Confirmar idioma y autonomía.'),format='boarding',optional=[dict(id='heathrow-return',label=T('Heathrow return · тариф journey, пассажиров подтвердить','Heathrow return · tarifa journey, confirmar pasajeros'),amount=650)],deposit_note=FUN_CANCEL,included=T('VAT, проживание, три приёма пищи, перекусы, компьютеры и pastoral care включены.',
  'VAT, alojamiento, tres comidas, meriendas, ordenadores y pastoral care incluidos.'))
 offer('w5-minecraft-matvey-one-session-2026','w5-christmas-minecraft-2026','W5 Christmas Build-Off · '+T('Матвей / один сеанс','Matvey / una sesión'),'GBP',dict(matvey=10),[['2026-12-12','2026-12-12'],['2026-12-19','2026-12-19']],[W5],T('Матвей 9 соответствует 8+, Оскар 6 не подходит. Выбрать один сеанс: все четыре повторяют содержание.',
  'Matvey de 9 cumple 8+, Oscar de 6 no. Elegir una sesión: las cuatro repiten contenido.'))
 idx={o['id']:o for o in offers};old={o['id'] for o in d['camp_planning']['offers']}
 d['camp_planning']['offers']=[idx.get(o['id'],o) for o in d['camp_planning']['offers']]+[o for o in offers if o['id'] not in old]
 d['camp_planning'].update(version=158,asof=CHECKED)
