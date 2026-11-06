"""Sourced Southeast Asian holiday programmes, fees and national STEM routes."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from datetime import date,timedelta
import json
from camp_east_asia_v159 import base,add,age_fit,candidate
from camp_europe_v148 import weekdays
from nearby_regional_v160 import event,programme

ROOT=Path(__file__).resolve().parents[1];CHECKED='2026-11-05';SPANISH={}
def T(a,b):SPANISH[a]=b;return a
FRESH='https://learningfresh.org/holiday-camps/freshenglish-santa-camp'
H3D='https://harimau3d.com/collections/color-swatch-bulk-pack/products/-h3d-2026-december-fmp-holiday-camp-7th-to-12-december-'
STRAT='https://camps.stratford-education.com/holiday-program/summer-winter-holiday-camp/'
NEWTON='https://newtonshow.my/winter-camp'
ADV='https://advaspire.com/events'
GUIDE='https://guidepost.id/programs/winter-camp'
GUIDE_PDF='https://guidepost.id/uploads/PDF/2026-Guidepost-AYANA-Bali-Winter-Camp_260918.pdf'
PADI='https://padikidscamp.com/camps/winter-camp-2026'
GREEN='https://greencampbali.com/'
CIS='https://www.cisp.edu.kh/student-life/camps'
SHANTI='https://shantivillage.com/worldschooling/'
DEV='https://devcon.ph/programs/kids/'
GENIUS='https://ir.geniusgroup.net/news-events/press-releases/detail/269/genius-group-and-koding-next-launch-national-ai-robotics'
TECH='https://worldtechlympics.org/kh'
DCCI='https://www.malaysia.dccisummit.com/'
MTE='https://www.mte.org.my/'
STEM='https://startupcambodia.gov.kh/event/799'
GATE=T('Возрастной кандидат не означает зачисление. Подтвердить выбранную смену, места, иностранный индивидуальный вход, уровень после трёх лет соревнований, язык и полный счёт. Сообщения, формы, согласия и платежи не отправлялись.',
 'Candidato por edad no significa admisión. Confirmar turno elegido, plazas, acceso extranjero individual, nivel tras tres años de competiciones, idioma y factura completa. Sin mensajes, formularios, consentimientos ni pagos.')
LANG=T('Язык преподавания / судейства этой программы прямо не подтверждён. Английский сайт, переключатель EN / ID или native-English teachers сами по себе не доказывают английский язык всех занятий.',
 'Idioma de enseñanza / evaluación de este programa sin confirmar expresamente. Web inglesa, selector EN / ID o native-English teachers no acreditan por sí solos inglés en todas clases.')
UNKNOWN=T('Полный текущий счёт и неизвестные обязательные доплаты уточнить; пустые расходы не считаются нулём.',
 'Confirmar factura actual completa y suplementos obligatorios desconocidos; gastos vacíos no equivalen a cero.')
TRIP=T('Перелёт, жильё семьи, местный транспорт, личная страховка и неуказанные расходы отдельно.',
 'Vuelos, alojamiento familiar, transporte local, seguro personal y gastos no indicados aparte.')
EDU=T('Учебные проекты, внутренние игры и сертификат не являются доказательством международной конкурсной победы.',
 'Proyectos educativos, juegos internos y certificado no acreditan victoria competitiva internacional.')
EN=T('Оператор прямо подтверждает английский именно в этой программе; язык сайта не использован как доказательство.',
 'Operador confirma expresamente inglés en este programa concreto; idioma web no usado como prueba.')
GREEN_TERMS=T('Не менее 8 участников; оператор может отменить / перенести за 3 недели при недоборе. Поздняя запись до 2 дней, для пансиона дополнительно наличие комнаты. По FAQ письменная отмена за 45 и более дней даёт 50% возврат, менее 45 дней — без возврата; пропуски / no-show без cash refund. Есть условный переносимый voucher на 1 год, не безусловный возврат. Отмена оператором — полный возврат. On-site insurance не заменяет личную туристическую страховку.',
 'Mínimo 8 participantes; operador puede cancelar / cambiar a 3 semanas por falta de inscritos. Inscripción tardía hasta 2 días, residencia además sujeta a habitación. Según FAQ cancelación escrita con 45 o más días permite devolución 50%, menos de 45 días sin devolución; ausencias / no-show sin cash refund. Existe voucher transferible condicional por 1 año, no devolución incondicional. Cancelación del operador: devolución total. On-site insurance no sustituye seguro personal de viaje.')
NEXT=T('Опубликованный сезон 2026 завершён; правила, даты и запись следующего сезона ещё не установлены.',
 'Temporada publicada 2026 terminada; reglas, fechas e inscripción siguiente aún sin establecer.')

def refs(p,*items):
 translations={
  'Santa programme: ages, English, dates and four packages':'Programa Santa: edades, inglés, fechas y cuatro paquetes',
  'Actual Primary content, English and variant availability':'Contenido Primary, inglés y disponibilidad de variante',
  'Goods policy is not camp cancellation terms':'Política de productos, sin condiciones de cancelación del campamento',
  'Current winter prices, intake options and camp-specific conditions':'Tarifas invernales, inicios y condiciones del campamento',
  'Winter themes, window, inclusions and from-price':'Temas de invierno, período, inclusiones y precio desde',
  'Public structured FAQ answers':'Respuestas FAQ estructuradas públicas',
  'Actual standalone camp, not December assessment':'Campamento específico, separado de evaluación de diciembre',
  'Winter dates and bilingual instruction':'Fechas invernales y enseñanza bilingüe',
  'Actual winter fees and offers: physical PDF pages 6 and 8':'Tarifas y ofertas de invierno: páginas físicas PDF 6 y 8',
  'Winter window and current camp fees':'Período invernal y tarifas del campamento',
  'Fee conditions and expired early bird':'Condiciones de tarifas y early bird vencido',
  'Programme overview without language confirmation':'Descripción del programa sin confirmar idioma',
  'Actual programme, English and dated options':'Programa concreto, inglés y opciones fechadas',
  'Refund, transfer and insurance qualifications':'Condiciones de devolución, traslado y seguro',
  'Cancellation policy':'Política de cancelación',
  'Actual open-to-external-children camp page':'Página del campamento abierta a niños externos',
  'Actual family dates, age tariffs and inclusions':'Fechas familiares, tarifas por edad e inclusiones',
  'Actual school programme and campaign windows':'Programa escolar y períodos de campaña',
 }
 p['sources']=[dict(title=T(a,translations.get(a,a)),url=b,checked=CHECKED)for a,b in items]
def B(i,slug,title,iso,place,themes,age,lo=None,hi=None,start='2026-12-01'):
 country={'MYS':T('Малайзия','Malasia'),'IDN':T('Индонезия','Indonesia'),'KHM':T('Камбоджа','Camboya'),'PHL':T('Филиппины','Filipinas')}[iso]
 p=base('CP'+str(i),slug,title,iso,country,place,themes)
 p.update(age=age,language=LANG,questions=[GATE],shortlist=[])
 if lo is not None:p['family_fit']=age_fit(lo,hi,start)
 p['price'].update(currency={'MYS':'MYR','IDN':'IDR','KHM':'USD','PHL':'PHP'}[iso],amount=None,label=UNKNOWN,extras=TRIP,deposit=UNKNOWN)
 return p
def season(p,start,end):
 p['timing'].update(precision='season_window',sessions=[[start,end]],session_details=[],variant_keyed=False)
def teach(p,bilingual=False):p.update(confirmed_instruction_languages=['EN'],language_evidence_role='bilingual'if bilingual else'primary',language=EN)

def make_profiles():
 out=[]
 for i,name,lo,hi in [(1340,'Juniors',4,7),(1341,'Masters',7,12)]:
  p=B(i,'freshenglish-santa-'+name.lower(),'Learning Fresh · Santa’s Workshop · '+name,'MYS','Mont Kiara / KLCC / Damansara Heights · Kuala Lumpur',['languages','general','art','engineering'],str(lo)+'–'+str(hi),lo,hi)
  teach(p);p['programme']=T('Английская грамотность через творческие проекты: Juniors — phonics, письмо букв и простые предложения; Masters — абзацы, редактирование, чтение и презентации. Есть maker / North Pole engineering, кулинария и театр; робототехническая специализация не заявлена. Возрастные группы и три площадки различаются; конкретную группу подтвердить.',
   'Lectoescritura inglesa mediante proyectos creativos: Juniors — phonics, letras y frases sencillas; Masters — párrafos, edición, lectura y presentaciones. Incluye maker / North Pole engineering, cocina y teatro; sin especialización robótica anunciada. Grupos por edad y tres sedes distintos; confirmar grupo concreto.')
  p['programme']+=' '+T('Для семьи нужны две группы: Матвей — Masters 7–12, Оскар — Juniors 4–7; общая смета не означает допуск обоих в один класс.',
   'Familia necesita dos grupos: Matvey — Masters 7–12, Oscar — Juniors 4–7; presupuesto conjunto no implica admisión de ambos en una clase.')
  p['timing'].update(status='published_2026',label=T('14–18 декабря: 5 дней; 14–23 декабря: 8 будних дней. Полдня 09:30–13:30 или полный день 09:30–15:30. Расписание по каждой площадке отдельно подтвердить.',
   '14–18 de diciembre: 5 días; 14–23 de diciembre: 8 días laborables. Media jornada 09:30–13:30 o jornada completa 09:30–15:30. Confirmar horario por sede.'))
  p['price'].update(label=T('MYR за ребёнка: 5 дней half 1250 / full 1575; 8 дней half 1850 / full 2050. Обед и все доплаты не раскрыты; в списке вещей лёгкий snack. Drop-in формулирует исключение дат 14–23 декабря, поэтому отдельные дни на эти даты не обещаны.',
   'MYR por niño: 5 días half 1250 / full 1575; 8 días half 1850 / full 2050. Almuerzo y cargos completos sin detallar; lista de objetos incluye snack ligero. Drop-in excluye literalmente fechas 14–23 de diciembre, sin prometer días sueltos en esas fechas.'))
  for count,end,half,full in [(5,'2026-12-18',1250,1575),(8,'2026-12-23',1850,2050)]:
   for mode,price,finish in [('half',half,'13:30'),('full',full,'15:30')]:add(p,'2026-12-14',end,str(count)+'-days-'+mode,str(count)+' days · '+mode,'MYR '+str(price),FRESH,weekdays('2026-12-14',end),'09:30',finish,'Asia/Kuala_Lumpur')
  refs(p,('Santa programme: ages, English, dates and four packages',FRESH));out.append(p)
 p=B(1342,'harimau3d-primary-december','HariMau3D · Future Makers Primary','MYS','Tropika Welcome Centre · Setia Tropika · Johor Bahru',['ai','engineering','science'],'9–12',9,12);teach(p)
 p['programme']=T('Product Design Thinking, AI для идей и практическая 3D-печать. В Primary прямо НЕ включён Onshape; его нельзя обещать Матвею по старшему описанию. Предоставляют 1 laptop каждому, минимум 1 принтер на 2 участников, материалы / инструменты, halal lunch и refreshments. После трёх лет соревнований начальную сложность согласовать.',
  'Product Design Thinking, AI para ideas e impresión 3D práctica. Primary excluye expresamente Onshape; sin prometerlo a Matvey desde descripción mayor. Facilitan 1 laptop por participante, mínimo 1 impresora por 2, materiales / herramientas, halal lunch y refreshments. Acordar dificultad inicial tras tres años de competiciones.')
 p['timing'].update(status='published_2026',label='7–8 December 2026 · 10:00–18:00 · arrival from 09:00')
 p['price'].update(amount=299,label=T('MYR 299 за Primary 9–12, два дня. Старшие 13–18 платят 349, взрослые 19+ 399: эти цены не детский семейный пакет. Goods refund policy магазина не является договором отмены лагеря.',
  'MYR 299 para Primary 9–12, dos días. Mayores 13–18 pagan 349, adultos 19+ 399: no paquete infantil familiar. Goods refund policy de tienda no es contrato de cancelación del campamento.'),included=p['programme'])
 p['availability']=dict(status='unknown',label=T('В первичном HTML Kids available=true; публичный остаток 2 на дату проверки не бронь. Generic Sold Out badge помечен aria-hidden и не доказывает закрытие курса. Текущее место подтвердить.',
  'HTML primario indica Kids available=true; stock público 2 en fecha de revisión no es reserva. Generic Sold Out badge lleva aria-hidden y no acredita cierre del curso. Confirmar plaza actual.'))
 add(p,'2026-12-07','2026-12-08','primary','Primary · 2 days','MYR 299',H3D,['2026-12-07','2026-12-08'],'10:00','18:00','Asia/Kuala_Lumpur');refs(p,('Actual Primary content, English and variant availability',H3D),('Goods policy is not camp cancellation terms','https://harimau3d.com/legal/refund-policy'));out.append(p)
 p=B(1343,'stratford-junior-winter','Stratford · Junior English Holiday Program','MYS','Kuala Lumpur',['languages','general'],'6–14 header; 6–15 FAQ',6,14,'2027-01-01');teach(p)
 p['programme']=T('Английский по уровню от beginner до advanced, placement в первый день; возраст и уровень определяют группу, свободная смена группы не обещана. Принимают местных и иностранных детей по условиям оператора. Заголовок 6–14 / FAQ 6–15: дети внутри пересечения. Пример 09:30–15:30 включает перерывы / обед, это не 6 часов чистого преподавания. Пансион, обеды и экскурсии в базовую цену не включены; до 13 на экскурсии нужен родитель.',
  'Inglés por nivel beginner a advanced, placement primer día; edad y nivel determinan grupo, sin prometer cambio libre. Admite niños locales y extranjeros según condiciones del operador. Título 6–14 / FAQ 6–15: niños en intersección. Ejemplo 09:30–15:30 incluye descansos / almuerzo, no 6 horas netas de enseñanza. Residencia, almuerzos y excursiones no incluidos; menores de 13 requieren padre en excursiones.')
 p['timing'].update(status='partial_2026_27',label=T('Зимнее окно 28.12.2026–26.02.2027; опубликованы восемь стартов, в том числе не по понедельникам. 28.06 и 27.12.2027 — только будущие старты без полного периода / цены. Конечные даты и праздничные дни не рассчитаны. Заголовок 2–8 недель против прайса / формы 1–8: недельный набор подтвердить.',
  'Ventana invernal 28.12.2026–26.02.2027; ocho inicios publicados, algunos fuera de lunes. 28.06 y 27.12.2027 solo inicios futuros sin período / precio completo. Sin calcular finales ni festivos. Título 2–8 semanas frente a precios / formulario 1–8: confirmar opción semanal.'))
  # The published intake is an event; a duration choice does not establish its end.
 native=json.loads((ROOT/'data/southeast-asia-native-v170.json').read_text())
 for start in native['stratford']['winter_intake_starts']+native['stratford']['future_start_only']:
  add(p,start,start,'intake-'+start,'Intake · '+start,UNKNOWN,STRAT);p['timing']['session_details'][-1]['date_scope']='activity_start'
 p['price'].update(label=T('MYR за ребёнка по фактической странице: 1 неделя 1650; 2 — 2400; 3 — 3150; 4 — 3900; 5 — 4650; 6 — 5300; 7 — 6150; 8 — 6900. Старые поисковые 2750 / 7000 не использованы. Это зимний прайс, не цена лета / декабря 2027. Включены материалы, light snacks и вода; lunch, жильё, transfer и экскурсии отдельно.',
  'MYR por niño según página real: 1 semana 1650; 2 — 2400; 3 — 3150; 4 — 3900; 5 — 4650; 6 — 5300; 7 — 6150; 8 — 6900. Precios antiguos de búsqueda 2750 / 7000 no usados. Tarifa invernal, no precio verano / diciembre 2027. Incluye materiales, light snacks y agua; lunch, alojamiento, transfer y excursiones aparte.'),deposit=T('Форма сама по себе не booking; после рассмотрения acceptance email и полный счёт, место после платежа и при наличии ресурсов. Старт может измениться. При отмене за 30 дней или меньше возврата нет; более ранний полный возврат не обещан. Согласия не давались.',
   'Formulario solo no es booking; tras revisión acceptance email y factura, plaza después de pago y según recursos. Inicio puede cambiar. Cancelación con 30 días o menos sin devolución; no se promete devolución íntegra anterior. Sin consentimientos.'))
 refs(p,('Current winter prices, intake options and camp-specific conditions',STRAT));out.append(p)
 for i,name,themes in [(1344,'Science from the North Pole',['science','engineering']),(1345,'Kawaii Winter Wonderland',['science','art','engineering']),(1346,'Jolly-Mix Multi-Activity',['science','art','general','robotics','engineering'])]:
  p=B(i,'newton-my-winter-'+str(i),'Newtonshow Malaysia · '+name,'MYS','Bangsar / Bukit Bintang · Kuala Lumpur; Johor Bahru; Penang',themes,'3–12',3,12,'2027-01-01')
  p['programme']=T('Три разные темы: Science — лёд, химия и инженерные опыты; Kawaii — art, sensory science и DIY; Jolly-Mix — science, art, cooking, motorised toys и внутренние Robo Olympics. Общая сеть не доказывает одинаковое содержание каждой группы. Два ребёнка могут выбирать разные темы при наличии.',
   'Tres temas distintos: Science — hielo, química y experimentos de ingeniería; Kawaii — art, sensory science y DIY; Jolly-Mix — science, art, cooking, motorised toys y Robo Olympics internos. Red general no acredita mismo contenido de cada grupo. Dos niños pueden elegir temas distintos según disponibilidad.')
  p['timing'].update(status='partial_2026_27',label=T('Сезон 23.11.2026–29.01.2027, Пн–Пт 09–16, arrival 08:30 без доплаты; праздники работают по FAQ. Нет таблицы тема × площадка × неделя: это сезонное окно, не ежедневные подтверждённые занятия.',
   'Temporada 23.11.2026–29.01.2027, lunes–viernes 09–16, arrival 08:30 sin cargo; FAQ indica actividad en festivos. Sin tabla tema × sede × semana: ventana estacional, no clases diarias confirmadas.'));season(p,'2026-11-23','2027-01-29')
  p['price'].update(label=T('От MYR 600 / неделя; точный день / выбранная тема / площадка требуют quote. Включены материалы, lunch и 2 snacks. Native English teachers подтверждены FAQ, но прямой язык всех занятий не установлен; strict EN не включён автоматически.',
   'Desde MYR 600 / semana; día exacto / tema / sede requieren quote. Incluye materiales, lunch y 2 snacks. FAQ confirma native English teachers, sin establecer idioma directo de todas clases; strict EN no activado automáticamente.'),deposit=T('FAQ JSON-LD: отмена до 1 недели до начала допускает возврат без указанной суммы; после старта cash refund нет, неиспользованные дни / болезнь — переносимые credits. Trial day оплачивается как 1 день, затем credits. Родители во время обычного camp не остаются.',
   'FAQ JSON-LD: cancelación hasta 1 semana antes permite devolución sin importe indicado; después sin cash refund, días sin usar / enfermedad con credits transferibles. Trial day se cobra como 1 día, después credits. Padres no permanecen durante campamento regular.'))
  refs(p,('Winter themes, window, inclusions and from-price',NEWTON),('Public structured FAQ answers','https://newtonshow.my/faq'));out.append(p)
 p=B(1347,'advaspire-holiday-november','Advaspire · School Holiday Robotics','MYS','Semenyih · Selangor',['robotics','coding'],'Academy 6–18; camp cutoff unannounced')
 p['programme']=T('Четыре утра: собрать, запрограммировать, отладить робота и пройти маленький challenge. Принимают новичков, ранее не учившихся в Advaspire; все материалы предоставлены, собственность на робота не обещана. Общий возраст академии 6–18 не объявлен возрастом конкретного лагеря; обоим нужен отдельный допуск.',
  'Cuatro mañanas: construir, programar, depurar robot y superar pequeño challenge. Para principiantes que no estudiaron antes en Advaspire; materiales facilitados, sin prometer propiedad del robot. Edad general de academia 6–18 no declarada edad del campamento; ambos requieren acceso concreto.')
 p['timing'].update(status='published_2026',label=T('24–27 ноября 2026 · четыре утра; точные часы не опубликованы.','24–27 de noviembre 2026 · cuatro mañanas; horas exactas sin publicar.'))
 add(p,'2026-11-24','2026-11-27','four-mornings','Four mornings',UNKNOWN,ADV);p['timing']['session_details'][-1]['date_scope']='camp_window';refs(p,('Actual standalone camp, not December assessment',ADV));out.append(p)
 p=B(1348,'guidepost-bali-winter-2026','Guidepost AYANA Bali · Winter Montessori','IDN','AYANA Farm · Jimbaran · Badung · Bali',['general','languages','culture','art','science'],'3–6',3,6)
 teach(p,True);p['language']=T('Конкретный зимний лагерь: English & Mandarin immersion; это билингвальная среда, не только английский.','Campamento invernal concreto: English & Mandarin immersion; entorno bilingüe, no inglés exclusivo.')
 p['programme']=T('Montessori, культура Бали, природа и farm-to-table; ребёнок без постоянного сопровождения на занятиях, в конце недели optional parent-child Memorable Moments. Это не пансион и не робототехнический интенсив. Матвею 9 — вне 3–6, Оскару 6 — возрастной кандидат.',
  'Montessori, cultura balinesa, naturaleza y farm-to-table; niño sin acompañante constante en clases, al final de semana optional parent-child Memorable Moments. No residencia ni intensivo robótico. Matvey 9 fuera de 3–6, Oscar 6 candidato por edad.')
 p['timing'].update(status='published_2026',label='14–18 / 21–24 / 28–31 December 2026 · half 08:30–13:00 / full 08:30–15:30')
 p['price'].update(label=T('Платёж IDR за одну выбранную неделю: неделя 1 half 8800000 / full 10600000; недели 2–3 half 7500000 / full 8900000. USD 499 / 601 / 425 / 505 в PDF — справочные эквиваленты, не вторые платежи. Плюс 11% sales tax и 10% AYANA service; база начисления неизвестна, не выдуман итог 21% или 22.1%. Lunch включён, жильё / flight отдельно. EB 10% закончился 30.10.2026; другие 5% условия / максимум 20% не применены автоматически.',
  'Pago IDR por una semana elegida: semana 1 half 8800000 / full 10600000; semanas 2–3 half 7500000 / full 8900000. USD 499 / 601 / 425 / 505 del PDF son equivalencias, no segundos pagos. Más 11% sales tax y 10% AYANA service; base de cálculo desconocida, sin inventar total 21% o 22.1%. Lunch incluido, alojamiento / flight aparte. EB 10% terminó 30.10.2026; otras condiciones 5% / máximo 20% no aplicadas automáticamente.'))
 for week,(start,end)in enumerate([('2026-12-14','2026-12-18'),('2026-12-21','2026-12-24'),('2026-12-28','2026-12-31')],1):
  for mode,amount,finish in [('half',8800000 if week==1 else 7500000,'13:00'),('full',10600000 if week==1 else 8900000,'15:30')]:
   add(p,start,end,'week-'+str(week)+'-'+mode,'Week '+str(week)+' · '+mode,'IDR '+str(amount)+' + 11% tax + 10% service',GUIDE_PDF,weekdays(start,end),'08:30',finish,'Asia/Makassar')
 refs(p,('Winter dates and bilingual instruction',GUIDE),('Actual winter fees and offers: physical PDF pages 6 and 8',GUIDE_PDF));out.append(p)
 p=B(1349,'padi-bali-winter','Padi Kids Camp · Winter Nature & Projects','IDN','Bidadari Art Space · Mas · Ubud · Bali',['general','science','art','culture'],'3–11; groups 3–6 / 7–11',3,11,'2027-01-01')
 p['programme']=T('Nature / art / science / culture; Kecil 3–6 и Muda 7–11. Оба ребёнка подходят общему возрасту, конкретная группа определяется днём рождения. EN / ID — язык интерфейса, преподавание не подтверждено. Открытый счётчик мест не является бронью.',
  'Nature / art / science / culture; Kecil 3–6 y Muda 7–11. Ambos compatibles con edad general, grupo concreto según cumpleaños. EN / ID son idiomas de interfaz, enseñanza sin confirmar. Contador público de plazas no es reserva.')
 p['timing'].update(status='partial_2026_27',label=T('14.12.2026–08.01.2027, заявлено Пн–Пт 09–14:30, день / неделя. Работа 25 декабря и 1 января отдельной таблицей не установлена; сезонное окно не превращено в ежедневные занятия. Срок регистрации 07.12.2026.',
  '14.12.2026–08.01.2027, anuncia lunes–viernes 09–14:30, día / semana. Sin tabla específica de apertura 25 de diciembre y 1 de enero; ventana estacional no convertida en clases diarias. Plazo de inscripción 07.12.2026.'));season(p,'2026-12-14','2027-01-08');p['timing']['deadline']='2026-12-07'
 p['price'].update(label=T('IDR / ребёнок: non-member неделя 2000000; member 1900000; день 425000. Lunch и snack включены. Member уже на 5% ниже общего прайса — ещё 5% повторно не вычтены. Sibling 5% требует базы скидки; EB 10% истёк 14.02.2026. Дневные регистрации без скидок. Field trip 350000 / неделя с пометкой weeks 3 & 5 — не даты зимнего выезда, пятую зимнюю неделю не придумываем.',
  'IDR / niño: semana non-member 2000000; member 1900000; día 425000. Lunch y snack incluidos. Member ya 5% menor que tarifa general: sin restar 5% otra vez. Sibling 5% requiere base de descuento; EB 10% venció 14.02.2026. Inscripciones diarias sin descuento. Field trip 350000 / semana con weeks 3 & 5 no son fechas de excursión invernal; sin inventar quinta semana.'))
 refs(p,('Winter window and current camp fees',PADI),('Fee conditions and expired early bird','https://padikidscamp.com/fees'),('Programme overview without language confirmation','https://padikidscamp.com/about'));out.append(p)
 green=json.loads((ROOT/'data/southeast-asia-native-v170.json').read_text())['green_programmes']
 specs=[(1350,'green-english-camp','Green English',7,12,['languages','science','general'],'08:30','15:00'),(1351,'green-camp-playgroup','Playgroup',4,6,['general','art','science'],'09:00','15:00'),(1352,'5-day-junior-naturalist-camp','Junior Naturalist',7,12,['science','general'],'08:30','16:00'),(1353,'3-day-green-explorer-camp','Green Explorer · 3 days',7,12,['general','culture','art'],'08:30','16:00'),(1354,'5-day-green-explorer-camp','Green Explorer · 5 days',7,12,['general','culture','science'],'08:30','16:00'),(1355,'5-day-mini-changemakers-camp','Mini Changemakers',8,12,['general','science'],'11:30','16:00')]
 for i,key,name,lo,hi,themes,begin,finish in specs:
  g=green[key];p=B(i,'green-bali-'+key,'Green Camp Bali · '+name,'IDN','Sibang Kaja · Abiansemal · Bali',themes,str(lo)+'–'+str(hi),lo,hi,'2027-01-01');teach(p)
  p['programme']=T('Природа и проекты: Green English — английский, math и regenerative science; Playgroup — сенсорика / животные / craft; Naturalist — экология, наблюдения и тесты воды; Explorer — outdoor / творчество; Mini Changemakers — лидерство, sustainability и вечерние активности. Технологические соревнования не заявлены. Язык всех программ прямо English, нужно уверенное общение.',
   'Naturaleza y proyectos: Green English — inglés, math y regenerative science; Playgroup — experiencias sensoriales / animales / craft; Naturalist — ecología, observación y pruebas de agua; Explorer — outdoor / creatividad; Mini Changemakers — liderazgo, sustainability y actividades nocturnas. Sin competiciones tecnológicas anunciadas. Todos programas expresamente English, exige comunicación suficiente.')
  overnight=key=='5-day-mini-changemakers-camp'
  if overnight:p.update(formats=['boarding'],accommodation=T('Только Mini Changemakers: 5 дней / 4 ночи в Bamboo Accommodations, питание включено. Жильё родителей отдельно.','Solo Mini Changemakers: 5 días / 4 noches en Bamboo Accommodations, comidas incluidas. Alojamiento parental aparte.'))
  else:p['accommodation']=T('Дневная программа. Общий пункт 24-hour supervision в карточке не делает её пансионом.','Programa diurno. Cláusula general 24-hour supervision en ficha no la convierte en residencia.')
  p['timing'].update(status='partial_2026_27'if any(not v['days_match']for v in g['dates'])else'published_2026_27',label=T('Даты взяты из конкретного продукта. Для Green English только будни; в остальных точные последовательные дни могут включать выходные. Несогласованные окна сохранены как план и в календарь занятий не включены.',
   'Fechas tomadas del producto concreto. Green English solo laborables; otros días consecutivos publicados pueden incluir fines de semana. Ventanas discordantes conservadas como plan, sin incluir en calendario de clases.'),planned_windows=[dict(start=v['start'],end=v['end'],status='duration_conflict')for v in g['dates']if not v['days_match']])
  if p['timing']['planned_windows']:
   p['timing']['label']+=' '+T('Конфликт: '+('; '.join(v['start']+'–'+v['end']+' = '+str(len(v['listed_days']))+' / '+str(v['expected_days'])+' days'for v in g['dates']if not v['days_match']))+'. Требуется новая таблица оператора.',
    'Conflicto: '+('; '.join(v['start']+'–'+v['end']+' = '+str(len(v['listed_days']))+' / '+str(v['expected_days'])+' days'for v in g['dates']if not v['days_match']))+'. Requiere nueva tabla del operador.')
  p['price'].update(label=T('От IDR '+str(g['minimum_price'])+' за участника / эту программу. Это нижний опубликованный тариф, не подтверждённый invoice выбранной даты. Meals / snacks включены; transfer до / из лагеря не включён. Специальная community-скидка не применена.',
   'Desde IDR '+str(g['minimum_price'])+' por participante / este programa. Tarifa mínima publicada, no invoice confirmado de fecha elegida. Meals / snacks incluidos; transfer al / desde campamento no incluido. Descuento community especial no aplicado.'),deposit=GREEN_TERMS)
  for v in g['dates']:
   if not v['days_match']:continue
   fit=age_fit(lo,hi,v['start'])
   add(p,v['start'],v['end'],'session-'+v['start'],name+' · '+v['start'],'from IDR '+str(g['minimum_price']),g['source'],None if overnight else v['listed_days'],None if overnight else begin,finish,'Asia/Makassar',family_fit=fit)
   last=p['timing']['session_details'][-1];last['deadline']=(date.fromisoformat(v['start'])-timedelta(days=2)).isoformat()
   last['proof']=T('Даты опубликованы оператором; поздний срок заявки рассчитан по правилу за 2 дня до старта: '+last['deadline']+'. Час отсечения не указан. Наличие места и факт проведения нужно подтвердить.',
    'Fechas publicadas por operador; límite de inscripción tardía calculado según regla de 2 días antes: '+last['deadline']+'. Hora de cierre sin indicar. Confirmar plaza y celebración efectiva.')
   if v['status']=='Limited':p['timing']['session_details'][-1]['availability']=dict(status='unknown',label=T('Оператор показывает Limited; реальное место ещё подтвердить.','Operador muestra Limited; confirmar plaza real.'))
  refs(p,('Actual programme, English and dated options',g['source']),('Refund, transfer and insurance qualifications',GREEN+'about/faq/'),('Cancellation policy',GREEN+'about/cancellation-policy/'));out.append(p)
 p=B(1356,'cis-phnom-penh-camps','CIS Phnom Penh · STEAM / Arts / Sports Camps','KHM','Koh Pich · Phnom Penh',['science','engineering','art','sport','general'],T('Возраст конкретной смены не опубликован.','Edad del turno concreto sin publicar.'))
 p['programme']=T('Winter / Summer / Volleyball camps открыты внешним детям Phnom Penh; STEAM, arts и sports. Возраст, EN-преподавание именно camp и иностранный туристический вход не раскрыты. Canadian / IB название школы не заменяет языковую политику программы.',
  'Winter / Summer / Volleyball camps abiertos a niños externos de Phnom Penh; STEAM, arts y sports. Edad, enseñanza EN concreta y acceso de turistas extranjeros sin detallar. Marca Canadian / IB del colegio no sustituye política lingüística del programa.')
 p['timing'].update(status='next_unannounced',label=T('Winter — December. Summer June29–July17 / July27–August14 без явного года; даты 2027 не выдуманы.','Winter — December. Summer June29–July17 / July27–August14 sin año expreso; sin inventar fechas 2027.'));refs(p,('Actual open-to-external-children camp page',CIS));out.append(p)
 for i,key,rate,adult,slots in [(1357,'kampot',150,200,[['2026-12-11','2026-12-18'],['2027-01-15','2027-01-22'],['2027-02-12','2027-02-19'],['2027-03-05','2027-03-12'],['2027-04-09','2027-04-16']]),(1358,'island',100,150,[['2026-12-21','2026-12-26'],['2027-01-25','2027-01-29'],['2027-02-22','2027-02-26'],['2027-03-14','2027-03-18'],['2027-04-19','2027-04-23']])]:
  p=B(i,'shanti-'+key+'-family','Shanti Shanti · '+('Kampot Family Hub'if key=='kampot'else'Koh Rong Island Family Extension'),'KHM','Kampot'if key=='kampot'else'Koh Rong · Long Set Beach',['general','culture','science'],T('Все возрасты; тариф ребёнка 4–11, взрослого 12+.','Todas edades; tarifa infantil 4–11, adulto 12+.'))
  p.update(formats=['family'],accommodation=T('Семейная программа с родителями; жильё отдельно, не детский пансион.','Programa familiar con padres; alojamiento aparte, no residencia infantil.'),programme=T('Worldschooling, культурные экскурсии, природа, творчество и семейные занятия. Kampot sample содержит 8 дней, Island sample 5 дней; Christmas Island окно длиннее sample. Это общий семейный маршрут, не robotics / AI camp. Язык именно занятий не подтверждён английским текстом и bilingual songs.',
   'Worldschooling, excursiones culturales, naturaleza, creatividad y actividades familiares. Sample Kampot contiene 8 días, Island sample 5 días; ventana Christmas Island más larga que sample. Ruta familiar general, no robotics / AI camp. Texto inglés y bilingual songs no acreditan idioma concreto de actividades.'))
  p['timing'].update(status='published_2026_27',label=T('Опубликованные окна семейных заездов; часы / дни конкретных экскурсий уточнить. В календаре только общий период, не ежедневные уроки.','Ventanas publicadas de estancias familiares; confirmar horas / días de excursiones concretas. Calendario solo período general, no clases diarias.'))
  included=T('Kampot: 2 lunches, 2 dinners, snacks, transport и activities; Island: 1 lunch, 1 dinner, snacks и activities, транспорт не обещан.',
   'Kampot: 2 lunches, 2 dinners, snacks, transport y activities; Island: 1 lunch, 1 dinner, snacks y activities, sin transporte prometido.')
  p['price'].update(amount=rate,unit='participant',label=T('USD за опубликованный период: ребёнок 4–11 '+str(rate)+'; взрослый 12+ '+str(adult)+'. Жильё и остальные meals отдельно. Sibling 10% и alumni 10% не применены без базы / условий. В смете сопровождение взрослых — отдельный обязательный компонент, не цена каждого ребёнка.',
   'USD por período publicado: niño 4–11 '+str(rate)+'; adulto 12+ '+str(adult)+'. Alojamiento y otras meals aparte. Sibling 10% y alumni 10% sin aplicar sin base / condiciones. En presupuesto acompañantes adultos son componente obligatorio separado, no precio de cada niño.'),included=included)
  for start,end in slots:
   add(p,start,end,'family-'+start,'Family window · '+start,'USD '+str(rate)+' child + '+str(adult)+' adult',SHANTI);p['timing']['session_details'][-1]['date_scope']='camp_window'
  refs(p,('Actual family dates, age tariffs and inclusions',SHANTI));out.append(p)
 p=B(1359,'devcon-kids-hour-ai','DEVCON Kids · Hour of AI / school STEM','PHL','Philippines · participating schools',['ai','coding','robotics'],'K–12; actual grade required')
 p['programme']=T('Школьная computer science / AI literacy и code camps с micro:bit / mBot / Arduino. Не открытый иностранный каникулярный лагерь: школа выбирает дату и согласует участие. Бесплатный training 14 / 21 / 28 ноября предназначен teachers / volunteers, не детям. Awards night 05.02.2027 — Hour of AI / chapters, не обещанная детская конкурсная награда.',
  'Computer science / AI literacy escolar y code camps con micro:bit / mBot / Arduino. No campamento vacacional extranjero abierto: colegio elige fecha y acuerda participación. Training gratuito 14 / 21 / 28 de noviembre para teachers / volunteers, no niños. Awards night 05.02.2027 corresponde a Hour of AI / chapters, no premio infantil competitivo prometido.')
 p['timing'].update(status='partial_2026',label=T('Первая волна Nov23–26 в summary против Nov23–27 в подробном плане; вторая Dec7–18 2026. Это окна выбора школьной даты, не ежедневное расписание и не открытые поездки семьи.',
  'Primera oleada Nov23–26 en summary frente a Nov23–27 en plan detallado; segunda Dec7–18 2026. Ventanas para elegir fecha escolar, no horario diario ni viajes familiares abiertos.'),precision='season_window',sessions=[['2026-11-23','2026-11-27'],['2026-12-07','2026-12-18']],variant_keyed=False)
 refs(p,('Actual school programme and campaign windows',DEV));out.append(p)
 return out

def update_report(report):
 rows=make_profiles();by={p['id']:p for p in rows};old={p['id']for p in report['profiles']}
 report['profiles']=[by.get(p['id'],p)for p in report['profiles']]+[p for p in rows if p['id']not in old]
 report['counts'].update(dossiers=len(report['profiles']),countries=len({p['iso']for p in report['profiles']}),swiss=sum(p['iso']=='CHE'for p in report['profiles']),by_status=dict(Counter(p['timing']['status']for p in report['profiles'])),source_urls=len({s['url']for p in report['profiles']for s in p['sources']}))
 report['countries']=[dict(country=c,count=n)for c,n in sorted(Counter(p['country']for p in report['profiles']).items())];report.update(version=170,asof=CHECKED)

def enrich_v170(d):
 by={e['id']:e for e in d['events']};rows=[]
 country=lambda iso:next(c for c in d['countries']if c['iso']==iso)
 c=country('IDN')
 rows.append(event('C1479','ENJOY AI Indonesia · Genius × Koding Next · announced national route',c['country'],GENIUS,iso=['IDN'],region=c['region'],city='Nuanu · Bali / Indonesian schools and centres',age=T('Глобальные ENJOY AI 3–22 — заявление пресс-релиза; местные возрастные категории и cutoff ещё не опубликованы.','ENJOY AI global 3–22 según comunicado; categorías locales y cutoff aún sin publicar.'),format=T('Индивидуальный / командный формат и состав ещё неизвестны.','Formato individual / por equipo y composición aún desconocidos.'),participation='unconfirmed_program',league_id='enjoy',gear='WhalesBot · local rulebook pending',language=LANG,entry=T('MOU от 05.11.2026: планируются training camps, школьные / клубные квалификации и национальный финал Genius Future Festival Bali 2027 с дальнейшим Global Final route. Это объявленный путь, не опубликованный регламент / открытая запись. Иностранный доступ и квоту подтвердить.',
  'MOU 05.11.2026: previstos training camps, clasificaciones escolares / de centros y final nacional Genius Future Festival Bali 2027 con posterior Global Final route. Ruta anunciada, no reglamento publicado / inscripción abierta. Confirmar acceso extranjero y cupo.'),period=T('Национальный финал обещан на 2027 без точных дат.','Final nacional anunciada para 2027 sin fechas exactas.'),admission_kind='qualification',evidence_level='organizer_announcement',date_scope='next_season_watch',note=T('1000 студентов первого года — цель проекта, не число принятых участников. MOU не превращён в работающий лагерь; заявления о мировой крупнейшей серии не независимый рейтинг.',
  '1000 alumnos primer año es objetivo del proyecto, no inscritos aceptados. MOU no convertido en campamento operativo; afirmaciones de mayor serie mundial no son ranking independiente.')))
 c=country('KHM')
 for i,name,themes in [(1480,'Bayon Clash · Battle Bot',['robotics','engineering']),(1481,'Garuda Wings · Drone Challenge',['drones','coding']),(1482,'Unsolved · CSI Challenge',['science']),(1483,'FC-1 · Fastest Coder',['coding'])]:
  rows.append(event('C'+str(i),'World Techlympics Cambodia · '+name+' · next season',c['country'],TECH,iso=['KHM'],region=c['region'],city='Phnom Penh · next venue unannounced',league_id='world-techlympics-kh',age=T('2026: общий возраст 9–17 и Junior Grades3–6 / Senior Grades7–9. Возраст и школьный класс проверить вместе; правила 2027 неизвестны.',
   '2026: edad general 9–17 y Junior Grades3–6 / Senior Grades7–9. Verificar edad y curso conjuntamente; reglas 2027 desconocidas.'),mat=T('Условно: возраст 9 подходит общему диапазону, школьный класс / национальный вход / новый сезон подтвердить.',
   'Condicional: edad 9 compatible con rango general, confirmar curso / acceso nacional / nueva temporada.'),osc=T('Нет сейчас: опубликован минимум 9, в календарном 2027 исполнится только 7.',
   'No ahora: mínimo publicado 9, en año natural 2027 cumple solo 7.'),team_min=2,team_max=2,format=T('2 ученика одной школы; coach и технический регламент уточнить.','2 alumnos del mismo colegio; confirmar coach y reglamento técnico.'),entry=T('В 2026 отбор 3–4 октября и дедлайн 30 сентября уже прошли. Победители категорий направляются в Malaysia World Techlympics 14–16 ноября 2026; это не свободная новая заявка семьи. Противоречие same school / clubs welcome и нерезидентский вход уточнить.',
   'Selección 2026 del 3–4 de octubre y plazo 30 de septiembre ya pasados. Ganadores de categorías avanzan a Malaysia World Techlympics 14–16 de noviembre 2026; no nueva solicitud familiar libre. Aclarar contradicción same school / clubs welcome y acceso no residente.'),gear=T('Дисциплина указана; детальные ограничения модального регламента не прочитаны, набор / размеры не выдуманы.',
   'Disciplina indicada; límites detallados del reglamento modal sin leer, sin inventar kit / dimensiones.'),language=LANG,cost=T('Архив 2026: USD35 за команду из 2; тариф 2027 не установлен. Подготовка / техника / поездка отдельно.','Archivo 2026: USD35 por equipo de 2; tarifa 2027 sin establecer. Preparación / equipo / viaje aparte.'),period=NEXT,registration_status=NEXT,scope='national',admission_kind='qualification',date_scope='next_season_watch',reward=T('По анонсу podium 1 / 2 / 3 получает 100% / 50% / 25% ground travel, hotel, food к мировому этапу. Airfare прямо не обещан; сертификат участника и место различаются, нужен протокол.',
   'Anuncio ofrece a podium 1 / 2 / 3: 100% / 50% / 25% ground travel, hotel, food para etapa mundial. Airfare no prometido expresamente; certificado y puesto diferentes, exige acta.'),note=NEXT,themes=themes))
 expo_specs=[('E237','Datacentre & Cloud Infrastructure Expo · DCCI Malaysia 2027','MYS','2027-05-04','2027-05-05',DCCI,'Kuala Lumpur Convention Centre',['technology','ai']),('E238','Malaysia Technology Expo · next physical edition','MYS','','',MTE,'World Trade Centre Kuala Lumpur · past venue',['technology','engineering','robotics']),('E239','Annual Cambodia STEM Festival · next edition','KHM','','',STEM,'Phnom Penh · next venue unannounced',['technology','science','coding','games'])]
 for ident,title,iso,start,end,url,place,themes in expo_specs:
  c=country(iso);e=event(ident,title,c['country'],url,start,end,block='События',iso=[iso],region=c['region'],city=place,themes=themes,participation='visitor',admission_kind='visitor',date_scope='exhibition_window',scope='national'if iso=='KHM'else'international',visitor_policy='confirm_children',visitor_policy_note=GATE,age=T('Точный допуск детей 6 / 9 лет не установлен.','Acceso concreto de niños 6 / 9 sin establecer.'),language=LANG,gear=T('Экспонентов выбранного выпуска и роботов в экспозиции подтвердить по текущему каталогу.','Confirmar expositores de edición elegida y robots presentes en catálogo actual.'),entry=GATE,cost=UNKNOWN,reward=T('Посещение / знакомства / мастерские; не конкурсная победа.','Visita / contactos / talleres; no victoria competitiva.'),level=T('C — тематическая выставка / национальный фестиваль','C — exposición temática / festival nacional'),importance_reason=T('Редакционный профильный кандидат; масштаб и международный состав не являются мировым рейтингом.','Candidato temático editorial; escala y participación internacional no constituyen ranking mundial.'))
  e.update(adult_entry=GATE,exhibitor_note=T('Компании и демонстрации выбранного нового выпуска не подтверждены по отдельному каталогу. Старые логотипы и прогноз числа участников не означают присутствие всех компаний.',
   'Empresas y demostraciones de nueva edición elegida sin confirmar en catálogo separado. Logotipos anteriores y previsión de asistentes no implican presencia de todas empresas.'),exhibitor_directory_url='',highlights=[T('Технологии, обучение и прикладные проекты','Tecnología, aprendizaje y proyectos aplicados')])
  if ident=='E237':e.update(exhibition_tier='regional_major',period='4–5 May 2027',entry=T('B2B datacentre / cloud expo с предварительно квалифицируемыми business delegates. Публичный семейный вход, конкретный pass, цена и дети не подтверждены.',
   'Expo B2B datacentre / cloud con business delegates precalificados. Acceso familiar público, pass concreto, precio y niños sin confirmar.'))
  if ident=='E238':e.update(exhibition_tier='regional_major',period=T('Главный очный MTE на сайте всё ещё 9–11 апреля 2026 и завершён. 8–10 апреля 2027 относятся к VIRTUAL Healthcare / SDG Awards, а не к новой очной выставке. Даты следующей поездки не установлены.',
   'MTE presencial principal en web aún 9–11 de abril 2026, ya terminado. 8–10 de abril 2027 corresponde a VIRTUAL Healthcare / SDG Awards, no nueva exposición presencial. Fechas de próximo viaje sin establecer.'))
  if ident=='E239':e.update(period=T('Официальная запись относится к прошедшему 7 февраля 2026: math, games, programming; 2027 не объявлен.','Registro oficial corresponde al pasado 7 de febrero 2026: math, games, programming; 2027 sin anunciar.'),evidence_level='official_host_announcement')
  rows.append(e)
 for e in rows:
  if e['id']in by:by[e['id']].update(e)
  else:d['events'].append(e);by[e['id']]=e
 by['E077'].update(checked=CHECKED,proof=T('Повторно прочитаны первичные public / MakerFest страницы: 21–22.11.2026, SPICE Arena / Concourse, 09–17, публичный walk-in без регистрации. MakerFest 4×4 public driving только 22 ноября; возраст конкретной активности отдельно.',
  'Releídas páginas primarias public / MakerFest: 21–22.11.2026, SPICE Arena / Concourse, 09–17, acceso público sin registro. MakerFest 4×4 public driving solo 22 de noviembre; edad de actividad concreta aparte.'),references=[dict(url='https://www.mypenang.gov.my/view_events.php?id=SEFjMEtKdm9qTlVzK004WkJZM3NhUT09',label='Государственное туристическое бюро: дата и место 2026'),dict(url='https://pisf.pscpen.com/public/',label='Правила public walk-in'),dict(label=T('Даты активности MakerFest','Fechas de actividad MakerFest'),url='https://pisf.pscpen.com/makerfest/')])
 by['E162'].update(checked=CHECKED,note=T('Страница INTI Robot по-прежнему показывает 11–13 августа 2026, уже прошедшие. Даты 2027 не объявлены; общий маркетинговый масштаб не список компаний следующего выпуска. Детский допуск остаётся неизвестным.',
  'INTI Robot aún muestra 11–13 de agosto 2026, ya pasados. Fechas 2027 sin anunciar; escala promocional general no es lista de empresas de próxima edición. Acceso infantil sigue desconocido.'))
 profiles=make_profiles();manual=[p for p in profiles if p['timing'].get('precision')=='season_window'or not p['timing']['sessions']]
 for n,p in enumerate(manual,485):
  c=country(p['iso']);fit=lambda k:T('Да по возрасту; набор и язык отдельно','Sí por edad; convocatoria e idioma aparte')if p['family_fit'][k]['status']=='candidate'else T('Условно — подтвердить конкретный допуск','Condicional — confirmar acceso concreto')
  e=event('L'+str(n),p['provider'],c['country'],p['sources'][0]['url'],block='Лагеря',iso=[p['iso']],region=c['region'],city=p['place'],age=p['age'],mat=fit('matvey'),osc=fit('oscar'),format=p['accommodation'],gear=p['programme'],language=p['language'],languages=p['confirmed_instruction_languages'],cost=p['price']['label'],entry=GATE,period=p['timing']['label'],note=GATE,scope='local',participation='unconfirmed_program',camp_programme_id=p['id'],camp_dossier_slug=p['slug'],reward=EDU,level=T('D — учебная программа','D — programa educativo'),references=[dict(label=s['title'],url=s['url'])for s in p['sources']])
  e['deadline']=p['timing'].get('deadline','')
  if e['id']in by:by[e['id']].update(e)
  else:d['events'].append(e);by[e['id']]=e
  q=next(q for q in d['camp_programmes']['profiles']if q['id']==p['id']);q['related_event_ids']=list(dict.fromkeys(q.get('related_event_ids',[])+[e['id']]))
  if not any(x['programme_id']==p['id']and x['event_id']==e['id']for x in d['camp_programmes']['event_links']):d['camp_programmes']['event_links'].append(dict(programme_id=p['id'],event_id=e['id'],relation='existing_programme'))
 catrows=rows[1:5];pr=programme('world-techlympics-kh','World Techlympics · Cambodia national route','regional',catrows[0]['age'],['9','teen'],[e['id']for e in catrows],summary=catrows[0]['entry'],route=catrows[0]['entry'],hardware=catrows[0]['gear'],language=LANG,cost=catrows[0]['cost'],award=catrows[0]['reward'],requirements=[GATE,catrows[0]['format']],nuances=[NEXT,catrows[0]['reward']],importance=T('Национальная STEM-серия с объявленным международным маршрутом; независимый мировой рейтинг силы не установлен.','Serie STEM nacional con ruta internacional anunciada; sin ranking mundial independiente de fuerza establecido.'),sources=[dict(title='Actual 2026 national call and published route',url=TECH,checked=CHECKED)],evidence=NEXT,categories=[dict(name=e['title'],age=e['age'],team=e['format'],hardware=e['gear'],entry=e['entry'],event_id=e['id'])for e in catrows])
 ps=d['league_guide']['profiles'];existing=next((p for p in ps if p['id']==pr['id']),None)
 if existing:existing.update(pr)
 else:ps.append(pr)
 d['league_guide'].update(version=170,checked=CHECKED)
 pd={p['id']:p for p in profiles};offers=[]
 def O(key,pid,label,bases,dates,required=None,unknown=None,price_basis=None):
  p=pd[pid];o=dict(id=key,slug=p['slug'],label=label,currency=p['price']['currency'],price_year=2026,format=p['formats'][0],children=list(bases),base_by_child=bases,discount_second=0,required=required or [],unknown_required=unknown or [dict(id='unpriced',label=UNKNOWN,unit='money',rate=1,min=0)],optional=[],unknown_trip=['travel','lodging','misc'],sessions=dates,sources=[s['url']for s in p['sources']],checked=CHECKED,gate=GATE,included=p['price'].get('included')or p['programme'],deposit_note=p['price']['deposit'],scope=TRIP)
  if price_basis:o['price_basis']=price_basis
  offers.append(o)
 for key,amount,days in [('5-half',1250,5),('5-full',1575,5),('8-half',1850,8),('8-full',2050,8)]:
  O('fresh-santa-2026-'+key,'CP1341','FreshEnglish · siblings · separate age groups · '+key,dict(matvey=amount,oscar=amount),[['2026-12-14','2026-12-18'if days==5 else'2026-12-23']])
  offers[-1]['gate']+=' '+T('Матвей в Masters, Оскар в Juniors: возрастные группы разные, одну и ту же площадку подтвердить.',
   'Matvey en Masters, Oscar en Juniors: grupos de edad distintos, confirmar misma sede.')
 O('h3d-primary-2026-matvey','CP1342','HariMau3D · Primary · Matvey only',dict(matvey=299),[['2026-12-07','2026-12-08']])
 strat_native=json.loads((ROOT/'data/southeast-asia-native-v170.json').read_text())['stratford']
 for weeks,fee in strat_native['winter_MYR_by_weeks'].items():O('stratford-winter-'+weeks+'-weeks','CP1343','Stratford · siblings · '+weeks+' weeks',dict(matvey=fee,oscar=fee),[[start,start]for start in strat_native['winter_intake_starts'][:9-int(weeks)]])
 for key,fee,start,end in [('week1-half',8800000,'2026-12-14','2026-12-18'),('week1-full',10600000,'2026-12-14','2026-12-18'),('week2-3-half',7500000,'2026-12-21','2026-12-31'),('week2-3-full',8900000,'2026-12-21','2026-12-31')]:
  dates=[['2026-12-21','2026-12-24'],['2026-12-28','2026-12-31']]if key.startswith('week2-3')else[[start,end]]
  O('guidepost-winter-2026-'+key,'CP1348','Guidepost · Oscar only · one selected week · '+key,dict(oscar=fee),dates,unknown=[dict(id='sales_tax',unit='money',rate=1,min=0,label=T('Обязательный 11% sales tax: сумма по invoice, база расчёта уточняется','Sales tax obligatorio 11%: importe según invoice, base de cálculo por confirmar')),dict(id='ayana_service',unit='money',rate=1,min=0,label=T('Обязательный 10% AYANA service: сумма по invoice','AYANA service obligatorio 10%: importe según invoice'))])
 O('padi-winter-nonmember-siblings-week','CP1349','Padi · siblings · non-member week',dict(matvey=2000000,oscar=2000000),[['2026-12-14','2027-01-08']])
 O('green-bali-parallel-christmas-from','CP1352','Green Bali · separate sibling programmes · from',dict(matvey=9200000,oscar=3900000),[['2026-12-20','2026-12-24']],price_basis='from')
 offers[-1]['gate']+=' '+T('Матвей в Junior Naturalist: 5 дней 20–24 декабря, 08:30–16; Оскар в Playgroup: 4 дня 21–24 декабря, 09–15. Одна площадка, разные периоды / часы.',
  'Matvey en Junior Naturalist: 5 días 20–24 de diciembre, 08:30–16; Oscar en Playgroup: 4 días 21–24 de diciembre, 09–15. Misma sede, períodos / horas distintos.')
 O('green-mini-changemakers-matvey-from','CP1355','Green Bali · overnight · Matvey only · from',dict(matvey=10050000),[['2026-12-20','2026-12-24']],price_basis='from')
 for pid,key,child,adult in [('CP1357','kampot',150,200),('CP1358','island',100,150)]:
  for parents in [1,2]:O('shanti-'+key+'-'+str(parents)+'-adult-siblings',pid,'Shanti · '+key+' · '+str(parents)+' adult + 2 children',dict(matvey=child,oscar=child),pd[pid]['timing']['sessions'],required=[dict(id='accompanying_adults',label=T('Обязательное сопровождение: '+str(parents)+' взрослых','Acompañamiento obligatorio: '+str(parents)+' adultos'),amount=parents*adult)])
 ids={o['id']for o in offers};d['camp_planning']['offers']=[o for o in d['camp_planning']['offers']if o['id']not in ids]+offers;d['camp_planning'].update(version=170,checked=CHECKED)
 known={s['url']for s in d['sources']}
 for e in rows+[by['E077'],by['E162']]:
  for s in [dict(title=e['title'],url=e['source'])]+[dict(title=x['label'],url=x['url'])for x in e.get('references',[])]:
   if s['url']not in known:d['sources'].append(dict(**s,checked=CHECKED,evidence=GATE));known.add(s['url'])
 d['southeast_asia_v170']=dict(version=170,checked=CHECKED,new_camp_dossiers=20,new_competition_route_watches=5,new_exhibition_events=3,new_league_profiles=1,new_budget_offers=len(offers),fully_audited_countries=0,worldwide_complete=False)
